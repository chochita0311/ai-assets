#!/usr/bin/env python3
"""Validate and package observed UI frames into an offline observation board."""
from __future__ import annotations

import argparse
import hashlib
from html.parser import HTMLParser
import json
import math
import os
from pathlib import Path
import re
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

ASSETS = Path(__file__).resolve().parents[1] / "assets"
STATUSES = {"rendered", "unverified", "unimplemented", "not-applicable", "render-failed"}
ID = re.compile(r"^[A-Za-z0-9][A-Za-z0-9._-]*$")


def now():
    return datetime.now(timezone.utc).isoformat()


def digest(data):
    return hashlib.sha256(data).hexdigest()


def read_json(path):
    return json.loads(Path(path).read_text(encoding="utf-8"))


def write_json(path, value):
    """Publish a complete manifest, retaining the old one if writing fails."""
    path = Path(path)
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                         prefix="." + path.name + ".", suffix=".writing", delete=False) as stream:
            temporary = Path(stream.name)
            json.dump(value, stream, ensure_ascii=False, indent=2)
            stream.flush()
            os.fsync(stream.fileno())
        temporary.replace(path)
    finally:
        if temporary is not None:
            temporary.unlink(missing_ok=True)


def browser_script(name):
    return (ASSETS / name).read_text(encoding="utf-8").replace(
        "/* ATLAS_GEOMETRY */", (ASSETS / "geometry.js").read_text(encoding="utf-8"))


def require(condition, message):
    if not condition:
        raise ValueError(message)


def local_file(root, relative):
    root = Path(root).resolve()
    path = (root / relative).resolve()
    require(not Path(relative).is_absolute() and root in path.parents,
            f"Expected a file inside its declared owner: {relative}")
    require(path.is_file(), f"Missing file: {relative}")
    return path


def source_identity(root, files):
    root = Path(root).resolve()
    require(bool(files), "Declare the source files whose UI is observed")
    hashes = {name: digest(local_file(root, name).read_bytes()) for name in files}
    revision = None
    result = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"],
                            capture_output=True, text=True, check=False)
    if result.returncode == 0:
        revision = result.stdout.strip()
    return {"root": str(root), "revision": revision, "files": hashes}


def check_sources(atlas, root=None, recipe_path=None):
    source = atlas["source"]
    owner = Path(root or source["root"])
    changed, unavailable = [], []
    for name, expected in source["files"].items():
        try:
            if digest(local_file(owner, name).read_bytes()) != expected:
                changed.append(name)
        except (OSError, ValueError):
            unavailable.append(name)
    recipe = atlas.get("recipe", {})
    require(not recipe_path or recipe.get("path"), "No recorded recipe identity to check at the supplied path")
    if recipe.get("path"):
        recipe_owner = Path(recipe_path or recipe["path"])
        try:
            if digest(recipe_owner.read_bytes()) != recipe["sha256"]:
                changed.append("[recipe]")
        except OSError:
            unavailable.append("[recipe]")
        for name, expected in recipe.get("files", {}).items():
            label = "[recipe file] " + name
            try:
                if digest(local_file(recipe_owner.parent, name).read_bytes()) != expected:
                    changed.append(label)
            except (OSError, ValueError):
                unavailable.append(label)
    return {"status": "changed" if changed else "unavailable" if unavailable else "matched",
            "checked_at": now(), "changed": changed, "unavailable": unavailable,
            "scope": "Declared source, recipe and recipe support files only; not an exhaustive dependency check."}


def valid_rect(rect, viewport):
    require(isinstance(rect, dict), "Rectangle must be an object")
    for key in ("x", "y", "width", "height"):
        value = rect.get(key)
        require(isinstance(value, (int, float)) and not isinstance(value, bool)
                and math.isfinite(value), f"Invalid rectangle {key}")
    require(rect["x"] >= 0 and rect["y"] >= 0 and rect["width"] > 0 and rect["height"] > 0,
            "Rectangle must be visible")
    require(rect["x"] + rect["width"] <= viewport["width"] + 0.01
            and rect["y"] + rect["height"] <= viewport["height"] + 0.01,
            "Rectangle exceeds its captured viewport")


def validate_description(description):
    require(isinstance(description, dict) and all(key in {"purpose", "action", "result", "exceptions"}
            and isinstance(value, str) for key, value in description.items()), "Invalid observed journey description")


def validate(atlas):
    require(atlas.get("schema") == "ui-atlas/v2", "This DOM canvas needs ui-atlas/v2; rerun the app recipe to replace image-only frames")
    require(ID.fullmatch(atlas.get("id", "")) is not None, "Invalid atlas ID")
    require(bool(atlas.get("title")), "Missing title")
    atlas.setdefault("limitations", [])
    atlas.setdefault("scope", "Declared frames only")
    atlas.setdefault("replay", "No replay command supplied; consult the owning recipe.")
    atlas.setdefault("journey_failures", [])
    require(isinstance(atlas["limitations"], list) and all(isinstance(item, str) for item in atlas["limitations"]),
            "limitations must be an array of strings")
    require(isinstance(atlas["replay"], str), "replay must be text")
    require(isinstance(atlas["journey_failures"], list), "journey_failures must be an array")
    for failure in atlas["journey_failures"]:
        require(all(isinstance(failure.get(key), str) and failure[key] for key in ("id", "surface", "reason")),
                "Unidentified journey failure")
    source = atlas.get("source", {})
    require(bool(source.get("root")) and bool(source.get("files")), "Missing source identity")
    for value in source["files"].values():
        require(isinstance(value, str) and re.fullmatch(r"[a-f0-9]{64}", value), "Invalid source digest")
    seen = set()
    require(isinstance(atlas.get("frames"), list) and atlas["frames"], "No frames or coverage entries")
    for frame in atlas["frames"]:
        key = frame.get("id", "")
        require(ID.fullmatch(key) is not None and key not in seen, f"Invalid or repeated state ID: {key}")
        seen.add(key)
        require(all(isinstance(frame.get(k), str) and frame[k] for k in ("label", "surface", "journey")),
                f"Missing frame labels: {key}")
        require(frame.get("status") in STATUSES, f"Unknown state status: {key}")
        if frame["status"] != "rendered":
            require(bool(frame.get("reason")) and not frame.get("document") and not frame.get("image"),
                    f"Unrendered states need a reason and cannot carry a document: {key}")
            continue
        viewport = frame.get("viewport", {})
        require(all(isinstance(viewport.get(k), int) and not isinstance(viewport[k], bool)
                    and viewport[k] > 0 for k in ("width", "height")), "Invalid viewport")
        require(frame.get("evidence") in ("synthetic", "observed"), "Declare synthetic or observed evidence")
        validate_description(frame.get("description", {}))
        require(bool(frame.get("document")) and not frame.get("image"), "Rendered frames require HTML, not a screen image")
        require(isinstance(frame.get("regions"), list) and isinstance(frame.get("texts"), list),
                "Rendered frames require regions and texts arrays, even when empty")
        require(isinstance(frame.get("elements"), list) and frame["elements"], "Missing selectable DOM elements")
        element_ids = set()
        for element in frame["elements"]:
            require(ID.fullmatch(element.get("id", "")) and element["id"] not in element_ids, "Invalid element ID")
            require(bool(element.get("selector")) and bool(element.get("tag")), "Missing element identity")
            if "visibleRect" in element:
                if element["visibleRect"] is not None:
                    valid_rect(element["visibleRect"], viewport)
                require(element.get("visible") is (element["visibleRect"] is not None), "Visibility and visible rectangle disagree")
            element_ids.add(element["id"])
        require(all(element.get("parent") is None or element["parent"] in element_ids for element in frame["elements"]),
                "Unknown element parent")
        regions = set()
        for region in frame.get("regions", []):
            require(ID.fullmatch(region.get("id", "")) is not None and region["id"] not in regions,
                    "Invalid or repeated region ID")
            regions.add(region["id"])
            require(bool(region.get("label")) and bool(region.get("selector")), "Unidentified region")
            if region.get("rect") is not None:
                valid_rect(region["rect"], viewport)
            else:
                require(bool(region.get("reason")), "Unavailable region needs a reason")
        for item in frame.get("texts", []):
            require(bool(item.get("text")) and bool(item.get("selector")), "Unidentified captured text")
            require(isinstance(item.get("regions"), list) and all(key in regions for key in item["regions"]),
                    "Captured text requires known region IDs, or an empty regions array")
            valid_rect(item["rect"], viewport)
    return atlas


class InertDocument(HTMLParser):
    """Accept source DOM only; the builder supplies its own inspection bridge."""
    # Keep RCDATA boundaries consistent on older supported Python parsers too.
    CDATA_CONTENT_ELEMENTS = (*HTMLParser.CDATA_CONTENT_ELEMENTS, "title", "textarea")
    def __init__(self, source):
        super().__init__()
        self.element_ids = set()
        self.source = source
        self.envelope = {}
        self.lines = [0] + [index + 1 for index, char in enumerate(source) if char == '\n']

    def source_offset(self):
        line, column = self.getpos()
        return self.lines[line - 1] + column

    def handle_starttag(self, tag, attributes):
        require(tag not in {"script", "iframe", "frame", "object", "embed", "base", "link",
                            "plaintext", "xmp", "noembed", "noframes", "noscript", "template",
                            "animate", "set", "animatecolor", "animatetransform", "animatemotion", "discard"},
                f"Active/unsupported DOM tag: {tag}")
        if tag in {"html", "head", "body"}:
            require(tag not in self.envelope, f"Repeated document envelope: {tag}")
            self.envelope[tag] = self.source_offset() + len(self.get_starttag_text())
        attributes = dict(attributes)
        require(not (tag == "input" and (attributes.get("type") or "").lower() == "file" and attributes.get("value")),
                "Selected file inputs require an app-owned preview")
        for name, value in attributes.items():
            require(not name.startswith("on") and name not in {"srcdoc", "action", "formaction", "autofocus", "is", "ping"},
                    f"Active DOM attribute: {name}")
            if name in {"src", "href", "xlink:href", "background"}:
                require((value or "").startswith(("data:image/", "#")), f"Nonembedded DOM resource: {name}")
        require(not (tag == "meta" and "http-equiv" in attributes), "Source HTTP directives are not allowed")
        if "data-atlas-node" in attributes:
            value = attributes["data-atlas-node"]
            require(value not in self.element_ids, "Repeated DOM element marker")
            self.element_ids.add(value)

    def handle_startendtag(self, tag, attributes):
        require(tag not in {"style", "title", "textarea"}, f"Raw-text DOM tag needs an explicit closing tag: {tag}")
        self.handle_starttag(tag, attributes)

    def handle_endtag(self, tag):
        if tag in {"html", "head", "body"}:
            require('/' + tag not in self.envelope, f"Repeated document envelope: /{tag}")
            self.envelope['/' + tag] = self.source_offset()

    def parts(self):
        """Use parsed tag locations, never matching tag-like comments or text."""
        names = ('html', 'head', '/head', 'body', '/body', '/html')
        require(all(name in self.envelope for name in names), "Inert documents require explicit html, head and body opening/closing tags")
        locations = [self.envelope[name] for name in names]
        require(locations == sorted(locations), "Invalid inert document envelope order")
        head, body = self.envelope['head'], self.envelope['/body']
        return (self.source[:head], self.source[head:body], self.source[body:])


def validate_document(document, elements):
    """Validate inert DOM and return parsed chunks for trusted bootstrap insertion."""
    parser = InertDocument(document); parser.feed(document); parser.close()
    parts = parser.parts()
    require(parser.element_ids == {element["id"] for element in elements}, "DOM and selectable-element inventory differ")
    return parts


def package(manifest, output, root=None, recipe_path=None):
    manifest, output = Path(manifest).resolve(), Path(output).resolve()
    atlas = validate(read_json(manifest))
    atlas["freshness"] = check_sources(atlas, root, recipe_path)
    # Rebind locators in this rebuilt view only; recorded hashes and original
    # observations stay intact. A moved path never makes changed bytes current.
    if root:
        atlas["source"]["root"] = str(Path(root).resolve())
    if recipe_path:
        atlas["recipe"]["path"] = str(Path(recipe_path).resolve())
    atlas["resources"] = {}
    for frame in atlas["frames"]:
        if frame["status"] != "rendered":
            continue
        document = local_file(manifest.parent, frame["document"]).read_text(encoding="utf-8")
        parts = validate_document(document, frame["elements"])
        identity = {"document": digest(document.encode()), "regions": frame.get("regions", []),
                    "renderer": digest(browser_script("frame.js").encode()),
                    "texts": frame.get("texts", []), "files": atlas["source"]["files"],
                    "recipe": atlas.get("recipe", {}).get("sha256"),
                    "recipe_files": atlas.get("recipe", {}).get("files", {})}
        frame["identity"] = digest(json.dumps(identity, sort_keys=True).encode())
        def share_resource(match):
            value = match.group(0)
            key = digest(value.encode())
            atlas["resources"][key] = value
            return "atlas-resource:" + key
        parts = [re.sub(r"data:[a-zA-Z0-9.+/-]+;base64,[a-zA-Z0-9+/=]+", share_resource, part) for part in parts]
        frame["document"] = ''.join(parts)
        # JavaScript slices UTF-16 code units; source text can contain emoji.
        head_end = len(parts[0].encode('utf-16-le')) // 2
        frame["document_slots"] = [head_end, head_end + len(parts[1].encode('utf-16-le')) // 2]
    payload = json.dumps(atlas, ensure_ascii=False).replace("<", "\\u003c").replace("\u2028", "\\u2028").replace("\u2029", "\\u2029")
    html = (ASSETS / "viewer.html").read_text(encoding="utf-8")
    html = html.replace("/* ATLAS_CSS */", (ASSETS / "viewer.css").read_text(encoding="utf-8"))
    html = html.replace("/* ATLAS_JS */", (ASSETS / "viewer.js").read_text(encoding="utf-8"))
    html = html.replace("/* ATLAS_FRAME */", browser_script("frame.js"))
    html = html.replace("/* ATLAS_NOTES */", (ASSETS / "notes.js").read_text(encoding="utf-8"))
    html = html.replace("/* ATLAS_CANVAS */", (ASSETS / "canvas.js").read_text(encoding="utf-8"))
    html = html.replace("/* ATLAS_CATALOG */", (ASSETS / "catalog.js").read_text(encoding="utf-8"))
    html = html.replace("/* ATLAS_SECTIONS */", (ASSETS / "sections.js").read_text(encoding="utf-8"))
    html = html.replace("/* ATLAS_SHEET_PICKER */", (ASSETS / "sheet-picker.js").read_text(encoding="utf-8"))
    html = html.replace("ATLAS_PAYLOAD", payload)
    output.parent.mkdir(parents=True, exist_ok=True)
    temporary = output.with_suffix(output.suffix + ".writing")
    require(not temporary.exists(), f"Output staging file already exists: {temporary}")
    try:
        temporary.write_text(html, encoding="utf-8")
        temporary.replace(output)
    finally:
        temporary.unlink(missing_ok=True)
    return atlas


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    build = commands.add_parser("build", help="Build a standalone HTML board")
    build.add_argument("manifest", type=Path)
    build.add_argument("--out", type=Path, required=True)
    build.add_argument("--source-root", type=Path)
    build.add_argument("--recipe", type=Path, help="Relocated recipe; verify its recorded hashes")
    check = commands.add_parser("check", help="Check declared source and recipe drift")
    check.add_argument("manifest", type=Path)
    check.add_argument("--source-root", type=Path)
    check.add_argument("--recipe", type=Path)
    init = commands.add_parser("init", help="Initialize the repo's private artifact workspace")
    init.add_argument("--source-root", type=Path, required=True)
    init.add_argument("--workspace", type=Path)
    listing = commands.add_parser("catalog", help="Refresh a workspace entry from its retained runs")
    listing.add_argument("workspace", type=Path)
    args = parser.parse_args()
    try:
        if args.command in ("init", "catalog"):
            import workspace
            owner = workspace.initialize(args.source_root, args.workspace) if args.command == "init" else args.workspace
            print(workspace.catalog(owner))
        elif args.command == "build":
            atlas = package(args.manifest, args.out, args.source_root, args.recipe)
            print(json.dumps({"html": str(args.out.resolve()), "states": len(atlas["frames"]),
                              "freshness": atlas["freshness"]["status"]}))
        else:
            result = check_sources(validate(read_json(args.manifest)), args.source_root, args.recipe)
            print(json.dumps(result, ensure_ascii=False, indent=2))
            return 0 if result["status"] == "matched" else 2
    except (OSError, ValueError, KeyError, TypeError) as error:
        parser.exit(1, f"UI Atlas: {error}\n")
    return 0


if __name__ == "__main__":
    sys.exit(main())
