#!/usr/bin/env python3
"""Materialize selectable DOM states, or replay them through the actual app."""
from __future__ import annotations

import argparse
from datetime import datetime
from fnmatch import fnmatchcase
import json
from pathlib import Path
import sys
import time
from urllib.parse import urljoin, urlsplit

from atlas import ID, browser_script, digest, local_file, now, package, read_json, require, source_identity, validate, validate_description, validate_document, write_json
import workspace

CHECKPOINTS = {"frame", "capture"}  # Accept existing recipes without a screenshot fallback.
ACTIONS = {"goto", "click", "hover", "focus", "fill", "press", "wait", "wait-ms",
           "respond", "scroll", "advance-clock"} | CHECKPOINTS


def validate_recipe(recipe):
    require(recipe.get("schema") == "ui-atlas.recipe/v1", "Unsupported recipe schema")
    require(ID.fullmatch(recipe.get("id", "")) is not None and bool(recipe.get("title")), "Missing atlas identity")
    require(bool(recipe.get("source_files")), "Declare source_files including shared styles and fixtures")
    require(bool(recipe.get("journeys")), "No journeys")
    require(isinstance(recipe.get("support_files", []), list), "support_files must be an array")
    frames, journeys = set(), set()
    for journey in recipe["journeys"]:
        require(ID.fullmatch(journey.get("id", "")) is not None and journey["id"] not in journeys, "Repeated journey ID")
        journeys.add(journey["id"])
        require(bool(journey.get("surface")), "Missing surface")
        require(journey.get("evidence") in ("synthetic", "observed"), "Declare evidence kind")
        validate_description(journey.get("description", {}))
        viewport = journey.get("viewport", {})
        require(all(isinstance(viewport.get(k), int) and viewport[k] > 0 for k in ("width", "height")), "Invalid viewport")
        rules = set()
        for rule in journey.get("routes", []):
            require(bool(rule.get("id")) and rule["id"] not in rules and bool(rule.get("url")), "Invalid route")
            rules.add(rule["id"])
            require(rule.get("hold") is True or isinstance(rule.get("response"), dict), "Route needs hold or response")
        for step in journey.get("steps", []):
            require(step.get("action") in ACTIONS, f"Unknown action: {step.get('action')}")
            if step["action"] in CHECKPOINTS:
                require(ID.fullmatch(step.get("id", "")) is not None and step["id"] not in frames, "Repeated state ID")
                require(bool(step.get("label")), "Missing state label")
                frames.add(step["id"])
            if step["action"] == "respond":
                require(step.get("route") in rules and isinstance(step.get("response"), dict), "Unknown response route")
    require(bool(frames), "No capture checkpoints")
    for frame in recipe.get("coverage", []):
        require(frame.get("id") not in frames and frame.get("status") in ("unverified", "unimplemented", "not-applicable"), "Invalid coverage entry")
        frames.add(frame.get("id"))
    return recipe


def recipe_identity(path, recipe):
    files = set(recipe.get("support_files", []))
    for journey in recipe["journeys"]:
        for item in journey.get("routes", []) + journey.get("steps", []):
            response = item.get("response", {})
            if "file" in response:
                files.add(response["file"])
    return {"path": str(path), "sha256": digest(path.read_bytes()),
            "files": {name: digest(local_file(path.parent, name).read_bytes()) for name in sorted(files)}}


class Responses:
    """Own held requests and their fixture responses for one isolated context."""
    def __init__(self, rules, origin, owner):
        self.rules = {item["id"]: dict(item) for item in rules}
        self.pending = {key: [] for key in self.rules}
        self.origin, self.owner = origin, owner
        self.blocked = set()

    def fulfill(self, route, response):
        if response.get("forward"):
            request = route.request
            parsed = urlsplit(request.url)
            require(request.method == "GET" and (parsed.scheme, parsed.netloc) == self.origin,
                    "Forwarding is restricted to GET on the isolated app origin")
            actual = route.fetch(max_redirects=0)
            if "merge" not in response:
                route.fulfill(response=actual)
                return
            def merge(value, patch):
                if isinstance(value, list):
                    require(all(str(key).isdigit() and int(key) < len(value) for key in patch), "Array merge index is out of range")
                    result = list(value)
                    for key, item in patch.items():
                        index = int(key)
                        result[index] = merge(result[index], item) if isinstance(item, dict) and isinstance(result[index], (dict, list)) else item
                    return result
                result = dict(value)
                for key, item in patch.items():
                    result[key] = merge(result[key], item) if isinstance(item, dict) and isinstance(result.get(key), (dict, list)) else item
                return result
            route.fulfill(response=actual, json=merge(actual.json(), response["merge"]))
            return
        kwargs = {"status": response.get("status", 200)}
        if "file" in response:
            kwargs["body"] = local_file(self.owner, response["file"]).read_bytes()
        elif "json" in response:
            kwargs["json"] = response["json"]
        else:
            kwargs["body"] = response.get("body", "")
        if "content_type" in response:
            kwargs["content_type"] = response["content_type"]
        route.fulfill(**kwargs)

    def handle(self, route):
        request = route.request
        parsed = urlsplit(request.url)
        path = parsed.path + ("?" + parsed.query if parsed.query else "")
        for key, rule in self.rules.items():
            target = request.url if "://" in rule["url"] else path
            if fnmatchcase(target, rule["url"]) and request.method == rule.get("method", "GET"):
                if rule.get("hold"):
                    self.pending[key].append(route)
                else:
                    self.fulfill(route, rule["response"])
                return
        if (parsed.scheme, parsed.netloc) == self.origin and request.method in ("GET", "HEAD"):
            route.continue_()
        else:
            self.blocked.add(request.method + " " + request.url)
            route.abort("blockedbyclient")

    def respond(self, key, response):
        self.rules[key].update(hold=False, response=response)
        pending, self.pending[key] = self.pending[key], []
        for route in pending:
            self.fulfill(route, response)

    def cancel_pending(self):
        for key, pending in self.pending.items():
            self.pending[key] = []
            for route in pending:
                route.abort("aborted")


def capture_frame(page, definitions, destination):
    observer = browser_script("observe.js")
    page.evaluate("() => document.fonts.ready")
    before = page.evaluate(observer, definitions)
    materialized = page.evaluate(browser_script("snapshot.js"), definitions)
    # Reject a nonpackageable document inside the state boundary, so later
    # journeys and their partial canvas survive an unsupported observation.
    validate_document(materialized["html"], materialized["elements"])
    preview = page.context.new_page()
    try:
        preview.set_content(materialized["html"])
        preview.evaluate(browser_script("frame.js"),
                         {"token": "geometry-check", "scroll": materialized["scroll"]})
        measured = preview.locator("[data-atlas-node]").evaluate_all("""nodes => Object.fromEntries(nodes.map(node => {
            const r = node.getBoundingClientRect();
            return [node.dataset.atlasNode, {x:r.x, y:r.y, width:r.width, height:r.height}];
        }))""")
        maximum = 0
        for element in materialized["elements"]:
            if not element["visible"]:
                continue
            actual = measured.get(element["id"])
            require(actual is not None, "A source DOM element is missing from its preview")
            difference = max(abs(actual[key] - element["rect"][key]) for key in ("x", "y", "width", "height"))
            require(difference <= 3, f"DOM geometry differs by {difference:.2f}px at {element['selector']}")
            maximum = max(maximum, difference)
        materialized["geometry"] = {"max_delta_px": round(maximum, 3), "tolerance_px": 3}
        if maximum > 1:
            materialized["warnings"].append(f"DOM line-box/layout rounding differs by up to {maximum:.2f} CSS pixels")
    finally:
        preview.close()
    after = page.evaluate(observer, definitions)
    require(before == after, "Visible text or geometry changed during materialization; hold the relevant response or clock and retry")
    destination.write_text(materialized.pop("html"), encoding="utf-8")
    before.update(elements=materialized["elements"], geometry=materialized["geometry"], dom_warnings=materialized["warnings"])
    return before


def perform(page, step, responses, base):
    action = step["action"]
    selector = step.get("selector")
    if action == "goto":
        url = urljoin(base + "/", step["url"])
        require(urlsplit(url)[:2] == urlsplit(base)[:2], "Navigation left the declared app origin")
        page.goto(url, wait_until="domcontentloaded")
    elif action in ("click", "hover", "focus"):
        getattr(page.locator(selector), action)()
    elif action == "fill":
        page.locator(selector).fill(step["value"])
    elif action == "press":
        if selector:
            page.locator(selector).press(step["key"])
        else:
            page.keyboard.press(step["key"])
    elif action == "wait":
        locator = page.locator(selector)
        locator.wait_for(state=step.get("state", "visible"))
        if "text" in step:
            from playwright.sync_api import expect
            expect(locator).to_have_text(step["text"])
    elif action == "wait-ms":
        page.wait_for_timeout(step["ms"])
    elif action == "advance-clock":
        page.clock.run_for(step["ms"])
    elif action == "respond":
        responses.respond(step["route"], step["response"])
    elif action == "scroll":
        coordinates = {"left": step.get("x", 0), "top": step.get("y", 0), "behavior": "instant"}
        if selector:
            page.locator(selector).evaluate("(el, position) => el.scrollTo(position)", coordinates)
        else:
            page.evaluate("position => scrollTo(position)", coordinates)


def run(args):
    from playwright.sync_api import sync_playwright

    recipe_path = args.recipe.resolve()
    recipe = validate_recipe(read_json(recipe_path))
    base = args.base_url or recipe.get("base_url")
    require(base and urlsplit(base).scheme in ("http", "https"), "Supply the app's --base-url")
    root = args.source_root or recipe.get("source_root")
    require(root, "Supply --source-root")
    source = source_identity(root, recipe["source_files"])
    recipe_files = recipe_identity(recipe_path, recipe)
    output = args.out.resolve() if args.out else None
    owner = None
    if not args.replay:
        if output:
            require(not output.exists(), "Capture --out must be a new artifact-owned directory")
            output.mkdir(parents=True)
        else:
            owner = workspace.initialize(root, args.workspace)
            output = workspace.reserve(owner, recipe["id"])
            workspace.catalog(owner)
        (output / "frames").mkdir()
    journeys = recipe["journeys"]
    if args.replay:
        journeys = [j for j in journeys if any(s.get("id") == args.replay and s["action"] in CHECKPOINTS for s in j["steps"])]
        require(len(journeys) == 1, "Replay state not found")
    atlas = {"schema": "ui-atlas/v2", "id": recipe["id"], "title": recipe["title"],
             "captured_at": now(), "source": source,
             "recipe": recipe_files,
             "scope": recipe.get("scope", "Declared journeys only"),
             "replay": recipe.get("replay", "Run capture.py with this recipe, a running isolated app and --replay STATE_ID."),
             "frames": [], "journey_failures": [], "limitations": recipe.get("limitations", [])}
    with sync_playwright() as playwright:
        launch = {"headless": not args.replay or args.headless}
        if args.browser:
            launch["executable_path"] = str(args.browser)
        browser = playwright.chromium.launch(**launch)
        try:
            for journey in journeys:
                context = browser.new_context(viewport=journey["viewport"], device_scale_factor=1,
                    locale=journey.get("locale", "en-US"), color_scheme=journey.get("theme", "light"),
                    service_workers="block", reduced_motion=journey.get("reduced_motion", "no-preference"))
                parsed = urlsplit(base)
                responses = Responses(journey.get("routes", []), (parsed.scheme, parsed.netloc), recipe_path.parent)
                context.route("**/*", responses.handle)
                if journey.get("storage"):
                    context.add_init_script("for (const [k,v] of Object.entries(" + json.dumps(journey["storage"]).replace("<", "\\u003c") + ")) localStorage.setItem(k,v);")
                page = context.new_page()
                page.set_default_timeout(args.timeout * 1000)
                page.set_default_navigation_timeout(args.timeout * 1000)
                errors = []
                page.on("pageerror", lambda error: errors.append(str(error)))
                if journey.get("clock"):
                    page.clock.install(time=datetime.fromisoformat(journey["clock"]))
                started = time.monotonic()
                failure = None
                previous_frame = None
                pending_actions = []
                try:
                    for step_index, step in enumerate(journey["steps"]):
                        if step["action"] not in CHECKPOINTS:
                            if failure is None:
                                try:
                                    if previous_frame is not None and step['action'] in ('click', 'fill', 'hover', 'focus', 'press', 'scroll', 'goto', 'respond', 'advance-clock'):
                                        selector = step.get('selector')
                                        observed_selector = ''
                                        if selector and page.locator(selector).count() == 1:
                                            observed_selector = page.locator(selector).evaluate('(node) => {' + browser_script('geometry.js') + '; return geometry.selector(node); }')
                                        pending_actions.append({'action': step['action'], 'selector': observed_selector})
                                    perform(page, step, responses, base)
                                except Exception as error:
                                    failure = f"{step['action']}: {error}"
                            continue
                        if args.replay:
                            if failure:
                                raise ValueError(failure)
                            if step["id"] == args.replay:
                                print(f"Replay ready: {args.replay}; close its browser window or press Ctrl-C to finish.", flush=True)
                                until = time.monotonic() + args.replay_seconds if args.replay_seconds else None
                                while not page.is_closed() and (until is None or time.monotonic() < until):
                                    try:
                                        page.wait_for_timeout(200)
                                    except Exception:
                                        if page.is_closed() or not browser.is_connected():
                                            break
                                        raise
                                return 0
                            continue
                        frame = {"id": step["id"], "label": step["label"], "surface": journey["surface"],
                                 "journey": journey["id"], "journey_label": journey.get("label", journey["id"]),
                                 "locale": journey.get("locale", "en-US"), "theme": journey.get("theme", "light"),
                                 "evidence": journey["evidence"], "conditions": journey.get("conditions", ""),
                                 "description": journey.get("description", {}),
                                 "elapsed_ms": round((time.monotonic() - started) * 1000),
                                 "payload": {"routes": json.loads(json.dumps(list(responses.rules.values()))), "storage": journey.get("storage", {}),
                                             "clock": journey.get("clock"), "steps": journey["steps"][:step_index + 1]},
                                 "status": "render-failed"}
                        if not failure:
                            try:
                                document = "frames/" + step["id"] + ".html"
                                definitions = step.get("regions", journey.get("regions", [{"id": "screen", "label": "Screen", "selector": "body"}]))
                                observed = capture_frame(page, definitions, output / document)
                                frame.update(observed, status="rendered", document=document,
                                             warnings=sorted(responses.blocked) + list(errors) + observed.pop("dom_warnings", []))
                            except Exception as error:
                                failure = f"capture: {error}"
                        if failure:
                            frame["reason"] = failure
                        if previous_frame is not None and previous_frame['status'] == frame['status'] == 'rendered' and pending_actions:
                            controls = [action for action in pending_actions if action['action'] not in ('goto', 'respond', 'advance-clock')]
                            trigger = controls[0] if len(controls) == 1 and pending_actions[0] is controls[0] else {'action': 'sequence' if controls else pending_actions[0]['action'], 'selector': ''}
                            previous_frame.setdefault('transitions', []).append({**trigger, 'target': frame['id'], 'label': frame['label']})
                        previous_frame = frame
                        pending_actions = []
                        atlas["frames"].append(frame)
                        print(f"{frame['id']}: {frame['status']}", flush=True)
                    if failure:
                        atlas["journey_failures"].append({"id": journey["id"], "surface": journey["surface"],
                                                          "reason": failure})
                finally:
                    if browser.is_connected():
                        if not page.is_closed():
                            responses.cancel_pending()
                        context.unroute_all(behavior="ignoreErrors")
                        context.close()
        finally:
            browser.close()
    atlas["frames"].extend(recipe.get("coverage", []))
    validate(atlas)
    manifest = output / "atlas.json"
    write_json(manifest, atlas)
    built = package(manifest, output / "index.html")
    atlas["freshness"] = built["freshness"]
    write_json(manifest, atlas)
    print(str(output / "index.html"), flush=True)
    if owner:
        print(str(workspace.catalog(owner)), flush=True)
    return 2 if atlas["journey_failures"] or built["freshness"]["status"] != "matched" else 0


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("recipe", type=Path)
    parser.add_argument("--source-root", type=Path)
    parser.add_argument("--base-url")
    destination = parser.add_mutually_exclusive_group()
    destination.add_argument("--out", type=Path, help="Explicit new run directory; bypass managed workspace")
    destination.add_argument("--workspace", type=Path, help="Artifact workspace (default: SOURCE_ROOT/.artifacts/ui-atlas)")
    parser.add_argument("--browser", type=Path, help="Existing Chromium executable; otherwise use Playwright's installed browser")
    parser.add_argument("--timeout", type=float, default=12)
    parser.add_argument("--replay", help="Replay to one state in a fresh headed browser")
    parser.add_argument("--headless", action="store_true", help="Headless replay for verification")
    parser.add_argument("--replay-seconds", type=float, help="Close a verification replay after this duration")
    args = parser.parse_args()
    try:
        return run(args)
    except KeyboardInterrupt:
        return 130
    except ImportError as error:
        parser.exit(1, f"Browser capture requires Playwright in this Python environment: {error}\n")
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(1, f"UI Atlas: {error}\n")


if __name__ == "__main__":
    sys.exit(main())
