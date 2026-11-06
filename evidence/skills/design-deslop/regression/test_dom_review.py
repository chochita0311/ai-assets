#!/usr/bin/env python3
"""Contract regressions for frozen, inspectable DOM in the design-review artifact.

The builder cases use only Python's standard library. Add ``--browser`` for
headless Playwright or ``--headed`` for a visible existing Chromium installation.
The original resource suite
is imported only for its synthetic fixture utilities and is run independently.
DOM assertions inspect native frame nodes; they are not screenshot comparisons.

DESIGN_DESLOP_TEST_WORK_ROOT, DESIGN_DESLOP_KEEP_TEST_ARTIFACTS and
DESIGN_DESLOP_BROWSER_EXECUTABLE have the same meanings as in the original suite.
"""

import base64
import copy
from contextlib import contextmanager
import functools
import http.server
import importlib.util
import json
import os
from pathlib import Path
import re
import shutil
import sys
import threading
import unittest
from unittest.mock import patch


RUN_HEADED = "--headed" in sys.argv
RUN_BROWSER = "--browser" in sys.argv or RUN_HEADED
for flag in ["--browser", "--headed"]:
    if flag in sys.argv:
        sys.argv.remove(flag)

from test_review_artifact import BUILDER, Fixture, embedded_data, png_bytes, tree_snapshot


ASSETS = BUILDER.parent.parent / "assets"


def snapshot_html(identity, view):
    """Authored DOM with distinguishable baseline, proposal and combined states."""
    colors = {"BASE": "rgb(31, 65, 104)", "P1": "rgb(137, 41, 58)",
              "C12": "rgb(38, 112, 67)"}
    color = colors.get(identity, "rgb(92, 54, 143)")
    return f'''<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>{identity} {view}</title>
<style>
html {{ background: white; }} body {{ margin: 0; padding: 24px; font: 16px Arial; }}
#intro {{ padding: 12px; }} h3 {{ color: {color}; margin: 0 0 12px; font-size: 24px; }}
#record {{ padding: 18px; background: rgb(232, 239, 245); margin: 24px 0; }}
#list {{ min-height: 1400px; padding: 20px; background: rgb(246, 242, 232); }}
#viewport-marker {{ width: 50vw; height: 10vh; border-top: 2px solid black; box-sizing: border-box; }}
#record::before {{ content: "Captured state"; display: block; }}
@media (max-width: 500px) {{ h3 {{ font-size: 19px; }} }}
</style></head><body data-snapshot="{identity}-{view}">
<section id="intro" class="source-intro"><h3 id="page-heading">{identity} {view} notebook</h3>
<p class="repeated">First source detail</p><p class="repeated">Second source detail</p></section>
<div id="hidden-component" hidden>Invisible component probe</div>
<article id="record" class="source-record"><label for="query">Saved search</label>
<input id="query" value="{identity} saved query" readonly>
<p class="record-summary">A native article, preserved from {identity}.</p>
<a id="source-link" href="#footer">Original local navigation</a>
<details open><summary>Captured details</summary>Visible captured detail</details></article>
<div id="viewport-marker"></div><section id="list"><h4>{identity} list</h4>
<p>Long component starts here.</p><div style="height:1200px"></div><p id="list-end">Long component ends here.</p></section>
<footer id="footer">{identity} footer</footer></body></html>'''


class DOMFixture(Fixture):
    def with_documents(self):
        manifest = self.with_components()
        selectors = {key: "#" + key for key in ["intro", "record", "list", "footer"]}

        def descriptor(identity, view, scope):
            name = identity + "-" + view + ".html"
            (self.root / name).write_text(snapshot_html(identity, view), encoding="utf-8")
            return {"html": name, "selectors": {key: selectors[key] for key in scope}}

        for view in manifest["views"]:
            view["document"] = descriptor("BASE", view["id"], selectors)
        for proposal in manifest["proposals"]:
            proposal["documents"] = {
                view["id"]: descriptor(proposal["id"], view["id"], proposal["components"])
                for view in manifest["views"]}
        for combination in manifest["combinations"]:
            members = [item for item in manifest["proposals"] if item["id"] in combination["proposals"]]
            scope = sorted({key for member in members for key in member["components"]})
            combination["documents"] = {
                view["id"]: descriptor(combination["id"], view["id"], scope)
                for view in manifest["views"]}
        return manifest


class DocumentBuilderTests(unittest.TestCase):
    def setUp(self):
        self.fixture = DOMFixture(self._testMethodName)
        self.manifest = self.fixture.with_documents()

    def tearDown(self):
        self.fixture.close()

    def build(self, manifest=None):
        result = self.fixture.build(self.manifest if manifest is None else manifest)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return embedded_data(self.fixture.review)

    def assert_rejected(self, manifest=None, output=None):
        result = self.fixture.build(self.manifest if manifest is None else manifest, output=output)
        self.assertNotEqual(result.returncode, 0, "Invalid DOM input was accepted")
        self.assertTrue((result.stdout + result.stderr).strip(), "Failure must explain the invalid input")

    def test_embedded_documents_scope_sparse_null_and_legacy_absence(self):
        data = self.build()
        for authored, normalized in zip(self.manifest["views"], data["views"]):
            expected = (self.fixture.root / authored["document"]["html"]).read_text(encoding="utf-8")
            self.assertEqual(normalized["document"]["html"], expected)
            self.assertEqual(normalized["document"]["selectors"], authored["document"]["selectors"])
        for kind in ["proposals", "combinations"]:
            for authored, normalized in zip(self.manifest[kind], data[kind]):
                for view, document in authored["documents"].items():
                    self.assertEqual(normalized["documents"][view]["html"],
                                     (self.fixture.root / document["html"]).read_text(encoding="utf-8"))
                    self.assertEqual(normalized["documents"][view]["selectors"], document["selectors"])
        self.manifest["views"][1]["document"] = None
        self.manifest["proposals"][0]["documents"] = {"desktop": None}
        self.manifest["proposals"][1]["documents"] = {}
        self.manifest["combinations"][0]["documents"]["desktop"]["selectors"] = {}
        sparse = self.build()
        self.assertIsNone(sparse["views"][1]["document"])
        self.assertEqual(sparse["proposals"][0]["documents"], {"desktop": None})
        self.assertEqual(sparse["proposals"][1]["documents"], {})
        self.assertEqual(sparse["combinations"][0]["documents"]["desktop"]["selectors"], {})
        old = self.build(self.fixture.manifest)
        self.assertTrue(all("document" not in view for view in old["views"]))
        self.assertTrue(all("documents" not in item for item in old["proposals"] + old["combinations"]))

    def test_document_identity_scopes_and_descriptor_types_rejected(self):
        cases = {
            "unknown baseline component": lambda m: m["views"][0]["document"]["selectors"].update({"unknown": "#record"}),
            "unknown proposal view": lambda m: m["proposals"][0]["documents"].update({"tablet": None}),
            "unknown combination view": lambda m: m["combinations"][0]["documents"].update({"tablet": None}),
            "proposal selector out of scope": lambda m: m["proposals"][0]["documents"]["desktop"]["selectors"].update({"footer": "#footer"}),
            "combination selector out of union": lambda m: m["combinations"][0]["documents"]["desktop"]["selectors"].update({"footer": "#footer"}),
            "empty selector": lambda m: m["views"][0]["document"]["selectors"].update({"intro": "  "}),
            "non-string selector": lambda m: m["views"][0]["document"]["selectors"].update({"intro": 7}),
            "selector list": lambda m: m["views"][0]["document"].update({"selectors": ["#intro"]}),
            "descriptor string": lambda m: m["views"][0].update({"document": "BASE-desktop.html"}),
            "missing selectors": lambda m: m["views"][0]["document"].pop("selectors"),
            "extra descriptor field": lambda m: m["views"][0]["document"].update({"url": "unused"}),
        }
        for label, change in cases.items():
            with self.subTest(label=label):
                manifest = copy.deepcopy(self.manifest)
                change(manifest)
                self.assert_rejected(manifest)
        # Syntax and cardinality require a browser; Python must not pretend to
        # have validated CSS syntax or invent a DOM match from the PNG regions.
        self.manifest["views"][0]["document"]["selectors"]["intro"] = "[invalid("
        self.build()

    def test_local_document_paths_html_shape_and_portable_resources_rejected(self):
        for path in ["https://invalid.example/snapshot.html", "missing.html"]:
            with self.subTest(path=path):
                manifest = copy.deepcopy(self.manifest)
                manifest["views"][0]["document"]["html"] = path
                self.assert_rejected(manifest)
        invalid = {
            "empty": "  ",
            "fragment": "<article>Missing document envelope</article>",
            "unclosed": "<!doctype html><html><head><title>x</title></head><body><article>x</body></html>",
            "script": '<script>window.activated = true</script>',
            "handler": '<button onclick="window.activated=true">Activate</button>',
            "embed": '<iframe srcdoc="hello"></iframe>',
            "base": '<base href="https://invalid.example/">',
            "refresh": '<meta http-equiv="refresh" content="0;url=https://invalid.example/">',
            "remote image": '<img src="https://invalid.example/pixel.png">',
            "remote stylesheet": '<link rel="stylesheet" href="https://invalid.example/style.css">',
            "remote css image": '<style>body {background-image:url(https://invalid.example/pixel.png)}</style>',
        }
        path = self.fixture.root / "invalid.html"
        for label, body in invalid.items():
            with self.subTest(label=label):
                html = body if label in {"empty", "fragment", "unclosed"} else (
                    "<!doctype html><html><head><title>Invalid</title></head><body>" + body + "</body></html>")
                path.write_text(html, encoding="utf-8")
                manifest = copy.deepcopy(self.manifest)
                manifest["views"][0]["document"]["html"] = path.name
                self.assert_rejected(manifest)

    def test_html_input_overwrite_protection_and_content_fingerprint(self):
        first = self.build()
        source = self.fixture.root / self.manifest["proposals"][0]["documents"]["desktop"]["html"]
        original = source.read_text(encoding="utf-8")
        self.assert_rejected(output=source)
        self.assertEqual(source.read_text(encoding="utf-8"), original)
        source.write_text(original.replace("P1 desktop notebook", "Revised P1 notebook"), encoding="utf-8")
        second = self.build()
        self.assertNotEqual(first["review_fingerprint"], second["review_fingerprint"])
        receipt = self.fixture.receipt(["P1"], "apply-selected", data=second)
        checked = self.fixture.check(receipt)
        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
        tampered = self.fixture.root / "tampered.html"
        tampered.write_text(self.fixture.review.read_text(encoding="utf-8").replace(
            "Revised P1 notebook", "Unrecorded change"), encoding="utf-8")
        self.assertNotEqual(self.fixture.check(receipt, review=tampered).returncode, 0)

    def test_dom_replaces_optional_png_but_not_source_or_rendered_evidence(self):
        for missing in ["png", "source", "concept"]:
            with self.subTest(missing=missing):
                manifest = copy.deepcopy(self.manifest)
                if missing == "png":
                    manifest["proposals"][0]["captures"]["phone"] = None
                    manifest["proposals"][0]["regions"].pop("phone")
                elif missing == "source":
                    manifest["baseline"]["files"] = {}
                else:
                    manifest["proposals"][0]["evidence"] = "concept"
                data = self.build(manifest)
                receipt = self.fixture.receipt(["P1"], "apply-selected", data=data)
                checked = self.fixture.check(receipt)
                if missing == "png":
                    self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
                else:
                    self.assertNotEqual(checked.returncode, 0)
                receipt["intent"] = "review-feedback"
                checked = self.fixture.check(receipt)
                self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)

    def test_old_artifact_and_minimal_template_keep_original_fingerprint_semantics(self):
        legacy, data = self.fixture.write_legacy_artifact()
        receipt = self.fixture.receipt(["P1"], "apply-selected", data=data)
        result = self.fixture.check(receipt, review=legacy)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        spec = importlib.util.spec_from_file_location("dom_review_builder_test", BUILDER)
        builder = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(builder)
        template = self.fixture.root / "minimal-template.html"
        template.write_text('<!doctype html><title>Minimal</title><script id="review-data" '
                            'type="application/json">__REVIEW_DATA__</script>', encoding="utf-8")
        self.fixture.manifest_path.write_text(json.dumps(self.manifest), encoding="utf-8")
        with patch.object(builder, "TEMPLATE_PATH", template):
            builder.build(self.fixture.manifest_path, self.fixture.review)
        self.assertEqual(builder.load_review(self.fixture.review)["review_id"], self.manifest["review_id"])
        self.assertNotIn("__DOM_PREVIEW__", self.fixture.review.read_text(encoding="utf-8"))


@unittest.skipUnless(RUN_BROWSER, "add --browser to exercise native DOM in Chromium")
class DOMBrowserTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        from playwright.sync_api import sync_playwright
        cls.playwright = sync_playwright().start()
        executable = os.environ.get("DESIGN_DESLOP_BROWSER_EXECUTABLE")
        if not executable:
            candidates = ["/Applications/Google Chrome.app/Contents/MacOS/Google Chrome",
                          shutil.which("chromium"), shutil.which("chromium-browser"),
                          shutil.which("google-chrome")]
            executable = next((path for path in candidates if path and Path(path).is_file()), None)
        cls.browser = cls.playwright.chromium.launch(
            executable_path=executable, headless=not RUN_HEADED,
            args=["--allow-file-access-from-files", "--disable-background-networking"])

    @classmethod
    def tearDownClass(cls):
        cls.browser.close()
        cls.playwright.stop()

    def setUp(self):
        self.fixture = DOMFixture(self._testMethodName)
        self.manifest = self.fixture.with_documents()
        self.original_source = tree_snapshot(self.fixture.site)
        self.context = self.browser.new_context(viewport={"width": 1440, "height": 1000}, accept_downloads=True)
        self.context.set_default_timeout(7000)
        self.page = self.context.new_page()
        self.network = []
        self.page.on("request", lambda request: self.network.append(request.url)
                     if re.match(r"https?://", request.url) and not request.url.startswith("http://127.0.0.1:") else None)
        self.page.add_init_script("""window.__domMessages = [];
            window.addEventListener('message', event => {
                if (event.data?.channel === 'design-deslop-dom') {
                    window.__domMessages.push({data:event.data,
                        side:['before','after'].find(side =>
                            document.getElementById(side + '-frame')?.contentWindow === event.source)});
                }
            });""")
        self.export_number = 0

    def tearDown(self):
        try:
            self.assertEqual(self.network, [], "The local viewer made external network requests")
            self.assertEqual(self.original_source, tree_snapshot(self.fixture.site), "Viewer changed source files")
        finally:
            self.context.close()
            self.fixture.close()

    def load(self, manifest=None):
        result = self.fixture.build(self.manifest if manifest is None else manifest)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.data = embedded_data(self.fixture.review)
        self.page.goto(self.fixture.review.as_uri())
        self.page.wait_for_function("() => document.readyState === 'complete'")

    def load_with_bridge_probe(self, source):
        # Build a test-local bridge resource so the control is installed before
        # the embedded bridge starts, independent of iframe init-script timing.
        resource = self.fixture.root / "dom-preview-probe.js"
        resource.write_text(source, encoding="utf-8")
        self.fixture.manifest_path.write_text(json.dumps(self.manifest), encoding="utf-8")
        spec = importlib.util.spec_from_file_location("dom_probe_builder", BUILDER)
        builder = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(builder)
        with patch.object(builder, "DOM_PREVIEW_PATH", resource):
            builder.build(self.fixture.manifest_path, self.fixture.review)
        self.data = embedded_data(self.fixture.review)
        self.page.goto(self.fixture.review.as_uri())
        self.page.wait_for_function("() => document.readyState === 'complete'")

    def frame(self, side):
        handle = self.page.locator("#" + side + "-frame").element_handle()
        frame = handle.content_frame()
        self.assertIsNotNone(frame, "The native DOM frame must exist")
        return frame

    def wait_ready(self):
        from playwright.sync_api import TimeoutError
        try:
            self.page.wait_for_function("""() => ['before','after'].every(side =>
                document.getElementById(side + '-dom-host').dataset.status === 'ready')""")
        except TimeoutError as error:
            state = self.page.evaluate("""() => ({
                before:document.getElementById('before-dom-host').dataset.status,
                after:document.getElementById('after-dom-host').dataset.status,
                reason:document.getElementById('dom-status').textContent,
                lastMessages:window.__domMessages.slice(-4).map(message => message.data)
            })""")
            raise AssertionError("Native DOM pair did not become ready: " + json.dumps(state)) from error

    def choose(self, identifier, status="accept"):
        action = "reset" if status == "pending" else status
        if status in {"defer", "pending"}:
            self.proposal(identifier)
        self.page.locator(f'button[data-action="{action}"][data-proposal-id="{identifier}"]').click()

    def proposal(self, identifier):
        self.page.locator(f'button[data-action="preview"][data-proposal-id="{identifier}"]').click()
        self.wait_ready()

    def component(self, identifier):
        self.page.locator("#focus-component").click()
        self.page.locator("#component-select").select_option(identifier)
        self.wait_ready()

    def integrated(self):
        self.page.locator("#integrated-comparison").click()

    def assert_apply(self, enabled):
        from playwright.sync_api import expect
        action = self.page.locator("#apply-selected")
        if enabled:
            expect(action).to_be_enabled()
        else:
            expect(action).to_be_disabled()

    def open_details(self, selector):
        details = self.page.locator(selector)
        if not details.evaluate("element => element.open"):
            details.locator(":scope > summary").click()

    def overall_note(self):
        self.open_details("#overall-feedback")
        return self.page.locator("#review-note")

    def reset_preview(self):
        self.open_details("details.viewer-more")
        self.page.locator("#reset-preview").click()
        self.page.locator("details.viewer-more > summary").click()

    def handoff(self, intent="review-feedback"):
        if not self.page.locator("#export-dialog").is_visible():
            self.page.locator("#open-handoff").click()
        self.page.locator("#" + intent).click()
        self.page.wait_for_function("intent => JSON.parse(document.getElementById('export-json').value).intent === intent", arg=intent)

    def export(self, intent="review-feedback"):
        self.handoff(intent)
        self.open_details("details.export-details")
        with self.page.expect_download() as download:
            self.page.locator("#download-json").click()
        self.export_number += 1
        path = self.fixture.root / ("export-" + str(self.export_number) + ".json")
        download.value.save_as(str(path))
        receipt = json.loads(path.read_text(encoding="utf-8"))
        self.page.locator("#close-export").click()
        return receipt

    def select_one(self):
        self.proposal("P1")
        self.choose("P1")
        self.page.locator("#feedback-note").fill("Keep the saved search.")
        self.overall_note().fill("The overall content must remain.")
        self.integrated()
        self.wait_ready()
        self.assert_apply(True)

    def assert_saved_choices(self):
        receipt = self.export()
        self.assertEqual(receipt["selected"], ["P1"])
        self.assertEqual(receipt["decisions"]["P1"]["note"], "Keep the saved search.")
        self.assertEqual(receipt["review_note"], "The overall content must remain.")

    def wait_dirty(self):
        self.page.wait_for_function("""() => [...document.querySelectorAll('[id$="-dom-host"]')]
            .some(host => host.dataset.status === 'dirty')""")
        self.assert_apply(False)

    def test_native_nodes_styles_cdp_inspection_and_fixed_capture_viewport(self):
        self.load()
        self.proposal("P1")
        self.assertEqual(self.page.locator("#source-dom, #source-capture").count(), 0)
        self.assertTrue(self.page.locator("#after-dom-host").is_visible())
        for view, width, height in [("desktop", 960, 720), ("phone", 390, 844)]:
            with self.subTest(view=view):
                self.page.locator("#view-select").select_option(view)
                self.wait_ready()
                for side, identity, color in [("before", "BASE", "rgb(31, 65, 104)"),
                                               ("after", "P1", "rgb(137, 41, 58)")]:
                    frame = self.frame(side)
                    observed = frame.evaluate("""() => ({
                        width: innerWidth, height: innerHeight,
                        heading: document.querySelector('#page-heading').tagName,
                        article: document.querySelector('#record').tagName,
                        input: document.querySelector('#query').tagName,
                        value: document.querySelector('#query').value,
                        text: document.querySelector('#page-heading').textContent,
                        color: getComputedStyle(document.querySelector('#page-heading')).color,
                        size: getComputedStyle(document.querySelector('#page-heading')).fontSize,
                        vh: document.querySelector('#viewport-marker').getBoundingClientRect().height,
                        scrollHeight: document.documentElement.scrollHeight
                    })""")
                    self.assertEqual((observed["width"], observed["height"]), (width, height))
                    self.assertEqual((observed["heading"], observed["article"], observed["input"]),
                                     ("H3", "ARTICLE", "INPUT"))
                    self.assertEqual(observed["text"], f"{identity} {view} notebook")
                    self.assertEqual(observed["value"], identity + " saved query")
                    self.assertEqual(observed["color"], color)
                    self.assertEqual(observed["size"], "19px" if view == "phone" else "24px")
                    self.assertAlmostEqual(observed["vh"], height / 10, delta=0.02)
                    self.assertGreater(observed["scrollHeight"], height)
                    self.assertEqual(self.page.locator("#" + side + "-frame").get_attribute("sandbox"), "allow-scripts")
        # Chrome DevTools uses this same DOM/Runtime protocol. Resolve the real
        # child element, not the outer iframe element or a raster substitute.
        session = self.context.new_cdp_session(self.frame("after"))
        try:
            session.send("DOM.enable")
            root = session.send("DOM.getDocument", {"depth": -1, "pierce": True})["root"]
            node = session.send("DOM.querySelector", {"nodeId": root["nodeId"], "selector": "#page-heading"})["nodeId"]
            self.assertNotEqual(node, 0)
            obj = session.send("DOM.resolveNode", {"nodeId": node})["object"]["objectId"]
            native = session.send("Runtime.callFunctionOn", {"objectId": obj,
                "functionDeclaration": "function(){return {tag:this.tagName,id:this.id,text:this.textContent}}",
                "returnByValue": True})["result"]["value"]
            self.assertEqual(native, {"tag": "H3", "id": "page-heading", "text": "P1 phone notebook"})
        finally:
            session.detach()
        frame = self.frame("after")
        self.assertTrue(frame.evaluate("""() => document.querySelector('#page-heading').dispatchEvent(
            new MouseEvent('contextmenu', {bubbles:true, cancelable:true, button:2}))"""),
            "The native context menu must not be cancelled by the picker bridge")
        self.page.set_viewport_size({"width": 390, "height": 844})
        self.page.locator("#zoom-fit").click()
        panes = [self.page.locator("#" + side + "-pane").bounding_box() for side in ["before", "after"]]
        self.assertTrue(all(panes), "Both native DOM panes must remain visible on phone")
        left, right = panes
        self.assertLess(left["x"], right["x"])
        self.assertLessEqual(left["x"] + left["width"], right["x"] + 2)
        self.assertLess(abs(left["y"] - right["y"]), 4)
        self.assertLess(left["y"], 844)
        for side in ["before", "after"]:
            self.assertEqual(self.frame(side).evaluate("[innerWidth, innerHeight]"), [390, 844])
        self.page.locator("#zoom-actual").click()
        self.assertAlmostEqual(self.page.locator("#after-frame").evaluate(
            "frame => frame.getBoundingClientRect().width / frame.clientWidth"), 1, places=3)

    def test_parent_host_visibility_recovers_real_focused_geometry_without_reset_or_dirty(self):
        self.page.add_init_script("""if (window === window.top) addEventListener('DOMContentLoaded', () => {
            const style = document.createElement('style');
            style.id = 'parent-availability-probe';
            style.textContent = '.dom-host { display:none !important; }';
            document.head.append(style);
        });""")
        measure = """() => {
            const rect = document.querySelector('#intro').getBoundingClientRect();
            return {width:innerWidth,height:innerHeight,html:document.body.outerHTML,
                    box:{x:rect.x,y:rect.y,width:rect.width,height:rect.height}};
        }"""
        self.load()
        restriction = self.page.locator("#parent-availability-probe")
        for side in ["before", "after"]:
            frame = self.frame(side)
            frame.locator("#intro").wait_for(state="attached")
            frame.locator("#intro").wait_for(state="hidden")
            initial = frame.evaluate(measure)
            self.assertEqual((initial["box"]["width"], initial["box"]["height"]), (0, 0),
                             "The hidden-parent witness must use real zero-area source geometry")
            self.assertEqual(self.page.locator("#" + side + "-frame").evaluate(
                "frame => [frame.style.width, frame.style.height]"), ["960px", "720px"])
            # With a display:none parent, Chrome can report either the declared
            # native viewport or an uninitialized 0x0 viewport. Recovery below
            # still requires the exact declared viewport and source geometry.
            self.assertIn((initial["width"], initial["height"]), [(0, 0), (960, 720)],
                          "Hidden initialization must not produce a partial or different viewport size")
        self.assert_apply(False)
        restriction.evaluate("style => style.disabled = true")
        self.wait_ready()
        self.choose("P1")
        self.page.locator("#feedback-note").fill("Keep the inspected source.")
        self.integrated()
        self.component("intro")
        self.wait_ready()
        self.assertEqual(self.page.locator("#focus-component").get_attribute("aria-pressed"), "true")
        self.assertEqual(self.page.locator("#component-select").input_value(), "intro")
        self.assert_apply(True)
        frames = {side: self.frame(side) for side in ["before", "after"]}
        before = {side: frame.evaluate(measure) for side, frame in frames.items()}
        # Hidden initialization can pause native rendering. This second real
        # availability transition exercises recovery from selector-missing after
        # the source has already been ready, without replacing the documents.
        restriction.evaluate("style => style.disabled = false")
        for side, frame in frames.items():
            frame.locator("#intro").wait_for(state="hidden")
            hidden = frame.evaluate(measure)
            self.assertEqual((hidden["box"]["width"], hidden["box"]["height"]), (0, 0))
            self.assertEqual(hidden["html"], before[side]["html"])
        self.page.locator("#apply-selected").dispatch_event("click")
        self.page.wait_for_function("""() => ['before','after'].every(side =>
            document.getElementById(side + '-dom-host').dataset.status === 'selector-missing')""")
        self.assert_apply(False)
        self.assertFalse(self.page.locator("#export-dialog").is_visible())
        restriction.evaluate("style => style.disabled = true")
        self.wait_ready()
        self.assert_apply(True)
        for side, frame in frames.items():
            recovered = frame.evaluate(measure)
            self.assertEqual((recovered["width"], recovered["height"]), (960, 720))
            self.assertEqual(recovered["html"], before[side]["html"])
            self.assertGreater(recovered["box"]["width"], 0)
            self.assertGreater(recovered["box"]["height"], 0)
            for dimension in ["width", "height"]:
                self.assertAlmostEqual(recovered["box"][dimension], before[side]["box"][dimension], delta=0.5)
            self.assertGreaterEqual(recovered["box"]["y"], -1)
            self.assertLess(recovered["box"]["y"], recovered["height"])
            self.assertTrue(frame.locator("#intro").is_visible())
        self.assertEqual(self.page.locator("#dom-status").get_attribute("data-dirty"), "false")
        self.assertFalse(self.page.evaluate("""window.__domMessages.some(message =>
            message.data.type === 'state' && message.data.status === 'dirty')"""))
        self.assertEqual(self.page.locator("#feedback-note").input_value(), "Keep the inspected source.")
        self.assertEqual(self.page.locator('button[data-action="accept"][data-proposal-id="P1"]').get_attribute("aria-pressed"), "true")

    def test_component_focus_tall_scroll_and_integrated_exact_combination(self):
        self.load()
        self.proposal("P1")
        self.choose("P1")
        self.page.locator("#feedback-note").fill("Preserve both proposal parts.")
        self.overall_note().fill("Compare the full composition.")
        self.component("record")
        focused = self.frame("after").locator("#record").evaluate(
            "element => ({top:element.getBoundingClientRect().top,bottom:element.getBoundingClientRect().bottom,height:innerHeight})")
        self.assertLess(focused["top"], focused["height"])
        self.assertGreater(focused["bottom"], 0)
        self.choose("P2")
        self.integrated()
        self.wait_ready()
        self.assertEqual(self.page.locator("#focus-whole").get_attribute("aria-pressed"), "true")
        self.assertEqual(self.frame("after").locator("body").get_attribute("data-snapshot"), "C12-desktop")
        self.assertEqual(self.frame("after").locator("#page-heading").inner_text(), "C12 desktop notebook")
        self.assertEqual(self.frame("after").locator("#list h4").inner_text(), "C12 list")
        self.assert_apply(True)
        receipt = self.export("apply-selected")
        self.assertEqual(receipt["preview_id"], "C12")
        self.assertEqual(set(receipt["selected"]), {"P1", "P2"})
        self.component("list")
        self.frame("after").locator("#list-end").scroll_into_view_if_needed()
        self.assertEqual(self.frame("after").evaluate("innerHeight"), 720)
        self.assertGreater(self.frame("after").evaluate("scrollY"), 0)
        self.page.locator("#view-select").select_option("phone")
        self.wait_ready()
        self.assertEqual(self.page.locator("#component-select").input_value(), "list")
        self.reset_preview()
        self.wait_ready()
        kept = self.export()
        self.assertEqual(kept["decisions"], receipt["decisions"])
        self.assertEqual(kept["review_note"], receipt["review_note"])
        self.assertEqual(kept["selected"], receipt["selected"])
        self.choose("P1", "pending")
        self.choose("P2", "pending")
        self.integrated()
        self.wait_ready()
        self.assertEqual(self.frame("after").locator("body").get_attribute("data-snapshot"), "BASE-phone")
        self.assertEqual(self.export()["selected"], [])

    def test_missing_exact_combination_never_borrows_a_member_document(self):
        self.load()
        self.choose("P1")
        self.choose("P3")
        self.integrated()
        self.assert_apply(False)
        self.assertRegex(self.page.locator("#preview-notice").inner_text(), r"(?i)(missing|no|unavailable).*(combination|combined)")
        self.assertNotEqual(self.page.locator("#after-dom-host").get_attribute("data-status"), "ready")
        receipt = self.export()
        self.assertEqual(set(receipt["selected"]), {"P1", "P3"})
        self.assertNotEqual(receipt["preview_id"], "C12")

    def test_picker_reference_copy_and_proposal_or_overall_feedback(self):
        self.context.add_init_script("""Object.defineProperty(navigator, 'clipboard', {
            configurable:true, value:{writeText:async value => {window.__copiedReference = value;}}
        });""")
        self.load()
        self.proposal("P1")
        self.page.locator("#zoom-actual").click()
        self.page.locator("#element-picker").click()
        self.frame("after").locator("#page-heading").click()
        reference = self.page.locator("#element-reference")
        from playwright.sync_api import expect
        expect(reference).not_to_have_value("")
        text = reference.input_value()
        for fragment in ["after", "desktop", "P1", "#page-heading", "P1 desktop notebook", "intro"]:
            self.assertIn(fragment, text)
        self.assertEqual(self.frame("after").locator("#page-heading").count(), 1)
        self.page.locator("#copy-reference").click()
        self.assertEqual(self.page.evaluate("window.__copiedReference"), text)
        self.page.locator("#add-reference").click()
        self.assertFalse(self.page.locator("#element-tools").is_visible())
        self.assertEqual(reference.input_value(), "")
        receipt = self.export()
        self.assertEqual(receipt["selected"], [], "Picking must never accept a proposal")
        self.assertIn(text, receipt["decisions"]["P1"]["note"])
        self.choose("P1")
        self.choose("P2")
        self.integrated()
        self.wait_ready()
        if self.page.locator("#element-picker").get_attribute("aria-pressed") != "true":
            self.page.locator("#element-picker").click()
        self.frame("before").locator("#page-heading").click()
        expect(reference).to_have_value(re.compile(r"side=before;.*preview=baseline", re.DOTALL))
        baseline_ref = reference.input_value()
        self.assertIn("before", baseline_ref)
        self.assertIn("baseline", baseline_ref.lower())
        self.frame("after").locator("#page-heading").click()
        expect(reference).to_have_value(re.compile(r"side=after;.*preview=C12", re.DOTALL))
        combined_ref = reference.input_value()
        self.assertIn("C12", combined_ref)
        self.page.locator("#add-reference").click()
        self.assertFalse(self.page.locator("#element-tools").is_visible())
        self.assertEqual(reference.input_value(), "")
        receipt = self.export()
        self.assertIn(combined_ref, receipt["review_note"])
        self.assertIn(text, receipt["decisions"]["P1"]["note"])
        self.assert_apply(True)

    def test_picker_structural_selector_manual_copy_and_no_source_activation(self):
        self.context.add_init_script("""Object.defineProperty(navigator, 'clipboard', {
            configurable:true, value:{writeText:async () => {throw new Error('Unavailable');}}
        });""")
        self.load()
        self.proposal("P1")
        self.page.locator("#zoom-actual").click()
        self.page.locator("#element-picker").click()
        self.frame("after").locator(".record-summary").click()
        reference = self.page.locator("#element-reference")
        from playwright.sync_api import expect
        expect(reference).not_to_have_value("")
        text = reference.input_value()
        self.assertIn("A native article, preserved from P1.", text)
        selector = re.search(r"^selector: (.+)$", text, re.MULTILINE)
        self.assertIsNotNone(selector, "The reference must expose its CSS selector")
        selected = self.frame("after").locator(selector.group(1))
        self.assertEqual(selected.count(), 1)
        self.assertEqual(selected.inner_text(), "A native article, preserved from P1.")
        # The actual serialized reference field is readable even when the
        # clipboard is denied. Selection exposes the same text for manual copy.
        self.page.locator("#copy-reference").click()
        selected = reference.evaluate("element => element.value.slice(element.selectionStart,element.selectionEnd)")
        self.assertEqual(selected, text)
        self.assertTrue(reference.is_visible())
        self.assertEqual(self.export()["selected"], [])
        self.page.locator("#element-picker").click()
        old_location = self.frame("after").evaluate("location.href")
        self.frame("after").locator("#source-link").click()
        self.assertEqual(self.frame("after").evaluate("location.href"), old_location,
                         "The frozen viewer must not activate source navigation")
        self.assertFalse(self.frame("after").evaluate("Boolean(window.activated)"))

    def test_ready_frame_keeps_active_picker_before_delayed_control_delivery(self):
        script = (ASSETS / "dom-preview.js").read_text(encoding="utf-8")
        entry = 'function bridge(config) {\n    "use strict";'
        picker_handler = '      if (message.type === "picker")'
        self.assertEqual(script.count(entry), 1)
        self.assertEqual(script.count(picker_handler), 1)
        probe = """
    let holdPickerControls = true;
    window.__queuedPickerControls = [];
    window.__releasePickerControls = () => {
      holdPickerControls = false;
      for (const message of window.__queuedPickerControls.splice(0)) {
        window.dispatchEvent(new MessageEvent('message', {data:message, source:parent}));
      }
    };"""
        script = script.replace(entry, entry + probe).replace(picker_handler, """
      if (message.type === 'picker' && holdPickerControls) {
        window.__queuedPickerControls.push(message);
        return;
      }
""" + picker_handler)
        self.load_with_bridge_probe(script)
        self.wait_ready()
        self.page.locator("#zoom-actual").click()
        self.page.locator("#element-picker").click()
        for side in ["before", "after"]:
            self.frame(side).evaluate("window.__releasePickerControls()")
        self.choose("P1")
        self.choose("P2")
        self.integrated()
        self.wait_ready()
        # No control release or interactive frame read precedes the native pick
        # in the new frame. Its initial picker state must already be usable.
        self.frame("before").locator("#page-heading").click()
        reference = self.page.locator("#element-reference")
        from playwright.sync_api import expect
        expect(reference).to_have_value(re.compile(r"side=before;.*preview=baseline", re.DOTALL))
        self.frame("after").locator("#page-heading").click()
        expect(reference).to_have_value(re.compile(r"side=after;.*preview=C12", re.DOTALL))
        combined_ref = reference.input_value()
        for side in ["before", "after"]:
            frame = self.frame(side)
            frame.wait_for_function("window.__queuedPickerControls.some(message => message.enabled === true)")
            frame.evaluate("window.__releasePickerControls()")
        self.page.locator("#element-picker").click()
        self.frame("before").locator("#page-heading").click()
        self.assertEqual(reference.input_value(), combined_ref, "The disabled picker must not replace the reference")
        self.page.locator("#element-picker").click()
        self.frame("before").locator("#page-heading").click()
        expect(reference).to_have_value(re.compile(r"side=before;.*preview=baseline", re.DOTALL))

    def test_loading_edits_cannot_become_the_freshness_baseline(self):
        script = (ASSETS / "dom-preview.js").read_text(encoding="utf-8")
        entry = 'function bridge(config) {\n    "use strict";'
        self.assertEqual(script.count(entry), 1)
        probe = """
    const nativeFrame = window.requestAnimationFrame.bind(window);
    let releasePaint = false;
    const pendingPaint = [];
    window.__loadingPaintGate = {
      pending:pendingPaint,
      release() {
        releasePaint = true;
        for (const callback of pendingPaint.splice(0)) nativeFrame(callback);
      }
    };
    window.requestAnimationFrame = callback => {
      if (releasePaint) return nativeFrame(callback);
      pendingPaint.push(callback);
      return pendingPaint.length;
    };"""
        script = script.replace(entry, entry + probe)

        def gated_frames():
            frames = {side: self.frame(side) for side in ["before", "after"]}
            for frame in frames.values():
                frame.wait_for_function("window.__loadingPaintGate.pending.length > 0")
            return frames

        measure = """() => ({color:getComputedStyle(document.querySelector('h3')).color,
            value:document.querySelector('#query').value,html:document.body.outerHTML})"""
        for kind in ["CSSOM", "form value"]:
            with self.subTest(kind=kind):
                self.load_with_bridge_probe(script)
                frames = gated_frames()
                for side in frames:
                    self.assertEqual(self.page.locator("#" + side + "-dom-host").get_attribute("data-status"), "loading")
                after = frames["after"]
                initial = after.evaluate(measure)
                if kind == "CSSOM":
                    after.evaluate("""() => {
                        const rule = [...document.styleSheets[0].cssRules].find(rule => rule.selectorText === 'h3');
                        rule.style.color = 'rgb(1, 2, 3)';
                    }""")
                    self.assertEqual(after.evaluate(measure)["color"], "rgb(1, 2, 3)")
                else:
                    after.evaluate("document.querySelector('#query').value = 'loading-time edit'")
                    self.assertEqual(after.evaluate(measure)["value"], "loading-time edit")
                self.assertEqual(after.locator("body").evaluate("element => element.outerHTML"), initial["html"],
                                 "This witness must change properties without a DOM mutation")
                for frame in frames.values():
                    frame.evaluate("window.__loadingPaintGate.release()")
                self.page.wait_for_function("""() => ['before','after'].every(side =>
                    ['ready','dirty'].includes(document.getElementById(side + '-dom-host').dataset.status))""")
                self.assertEqual(self.page.locator("#dom-status").get_attribute("data-dirty"), "true",
                                 "A loading-time edit was trusted as the embedded baseline")
                self.assert_apply(False)
                self.choose("P1")
                self.page.locator("#feedback-note").fill("Keep the saved search.")
                self.overall_note().fill("The overall content must remain.")
                previous = [self.page.locator("#" + side + "-frame").element_handle()
                            for side in ["before", "after"]]
                self.integrated()
                for frame in previous:
                    self.page.wait_for_function("frame => !frame.isConnected", arg=frame)
                for frame in gated_frames().values():
                    frame.evaluate("window.__loadingPaintGate.release()")
                self.wait_ready()
                self.assertEqual(self.page.locator("#dom-status").get_attribute("data-dirty"), "true")
                self.assert_apply(False)
                self.page.locator("#apply-selected").dispatch_event("click")
                self.assertFalse(self.page.locator("#export-dialog").is_visible())
                self.reset_preview()
                for frame in gated_frames().values():
                    frame.evaluate("window.__loadingPaintGate.release()")
                self.wait_ready()
                self.assertEqual(self.frame("after").evaluate(measure), initial)
                self.assert_apply(True)
                self.assert_saved_choices()
                # Each loading witness starts with its own pending choices.
                self.page.evaluate("localStorage.clear()")

    def test_dom_edits_block_application_until_reset_and_keep_choices(self):
        self.load()
        self.select_one()
        self.frame("after").locator("#page-heading").evaluate("element => element.textContent = 'DevTools DOM change'")
        self.wait_dirty()
        self.assertEqual(self.frame("after").locator("#page-heading").inner_text(), "DevTools DOM change")
        self.page.locator("#focus-component").click()
        self.assert_apply(False)
        self.page.locator("#focus-whole").click()
        self.assert_apply(False)
        self.reset_preview()
        self.wait_ready()
        self.assertEqual(self.frame("after").locator("#page-heading").inner_text(), "P1 desktop notebook")
        self.assert_apply(True)
        self.assert_saved_choices()

    def test_immediate_dom_export_rechecks_current_document(self):
        self.load()
        self.select_one()
        self.frame("after").locator("#record").evaluate("element => element.setAttribute('data-devtools-edit', 'yes')")
        self.page.locator("#apply-selected").dispatch_event("click")
        self.wait_dirty()
        self.assertFalse(self.page.locator("#export-dialog").is_visible(),
                         "The export path must reject a recently mutated native document")

    def test_cssom_insert_rule_and_immediate_rule_style_export_are_rechecked(self):
        self.load()
        self.select_one()
        self.frame("after").evaluate("document.styleSheets[0].insertRule('h3 {color:purple !important}',0)")
        self.wait_dirty()
        self.reset_preview()
        self.wait_ready()
        self.assert_apply(True)
        # CSSStyleDeclaration changes do not produce DOM mutation records. The
        # export click follows immediately, without awaiting periodic detection.
        self.frame("after").evaluate("""() => {
            const rule = [...document.styleSheets[0].cssRules].find(rule => rule.selectorText === 'h3');
            rule.style.color = 'rgb(1, 2, 3)';
        }""")
        self.page.locator("#apply-selected").dispatch_event("click")
        self.wait_dirty()
        self.assertFalse(self.page.locator("#export-dialog").is_visible(),
                         "A cached ready state must not export recently edited CSSOM")
        self.reset_preview()
        self.wait_ready()
        self.assertEqual(self.frame("after").locator("#page-heading").evaluate(
            "element => getComputedStyle(element).color"), "rgb(137, 41, 58)")
        self.assert_saved_choices()

    def test_wrong_window_and_previous_generation_bridge_messages_are_ignored(self):
        self.load()
        self.select_one()
        self.page.locator("#zoom-actual").click()
        self.page.locator("#element-picker").click()
        self.frame("after").locator("#page-heading").click()
        self.page.wait_for_function("""() => window.__domMessages.some(message =>
            message.side === 'after' && message.data.type === 'picked')""")
        old_pick = self.page.evaluate("""() => window.__domMessages.filter(message =>
            message.side === 'after' && message.data.type === 'picked').at(-1).data""")
        old_ready = self.page.evaluate("""() => window.__domMessages.filter(message =>
            message.side === 'after' && message.data.type === 'state' && message.data.status === 'ready').at(-1).data""")
        self.reset_preview()
        self.wait_ready()
        reference = self.page.locator("#element-reference")
        self.assertEqual(reference.input_value(), "")
        if self.page.locator("#element-picker").get_attribute("aria-pressed") != "true":
            self.page.locator("#element-picker").click()
        self.frame("after").locator("#page-heading").click()
        self.page.wait_for_function("""token => window.__domMessages.some(message =>
            message.side === 'after' && message.data.type === 'picked' && message.data.token !== token)""",
            arg=old_pick["token"])
        current_pick = self.page.evaluate("""() => window.__domMessages.filter(message =>
            message.side === 'after' && message.data.type === 'picked').at(-1).data""")
        good_reference = reference.input_value()
        spoof = dict(current_pick, text="Injected unrelated-window reference")
        # Same current token, wrong WindowProxy: an opaque origin is not identity.
        self.page.evaluate("message => window.postMessage(message, '*')", spoof)
        self.page.wait_for_function("""() => window.__domMessages.some(message =>
            message.data.text === 'Injected unrelated-window reference')""")
        self.assertEqual(reference.input_value(), good_reference)
        late = dict(old_pick, text="Late old-generation reference")
        # Correct current WindowProxy, previous token: source alone is insufficient.
        self.frame("after").evaluate("message => parent.postMessage(message, '*')", late)
        self.page.wait_for_function("""() => window.__domMessages.some(message =>
            message.data.text === 'Late old-generation reference')""")
        self.assertEqual(reference.input_value(), good_reference)
        self.frame("after").locator("#record").evaluate("element => element.textContent = 'Edited in DevTools'")
        self.wait_dirty()
        self.frame("after").evaluate("message => parent.postMessage(message, '*')", old_ready)
        # A round trip through the same event queue observes processing of the
        # replay without an arbitrary sleep or a timer-dependent pass.
        self.frame("after").evaluate("parent.postMessage({channel:'design-deslop-dom',type:'test-observed'}, '*')")
        self.page.wait_for_function("""() => window.__domMessages.some(message =>
            message.data.type === 'test-observed')""")
        self.assertEqual(self.page.locator("#after-dom-host").get_attribute("data-status"), "dirty")
        self.assert_apply(False)

    def test_native_form_property_edits_invalidate_periodic_and_immediate_export_until_reset(self):
        document = self.fixture.root / self.manifest["proposals"][0]["documents"]["desktop"]["html"]
        document.write_text(document.read_text(encoding="utf-8").replace("</article>",
            '<select id="multiple" multiple><option selected>A</option><option>B</option><option>C</option></select>'
            '<input id="indeterminate" type="checkbox"></article>'), encoding="utf-8")
        self.load()
        self.select_one()
        state = """() => {
            const select = document.querySelector('#multiple');
            const input = document.querySelector('#indeterminate');
            return {selected:[...select.options].map(option => option.selected),
                    value:select.value,index:select.selectedIndex,indeterminate:input.indeterminate,
                    checked:input.checked,markup:select.outerHTML + input.outerHTML};
        }"""
        baseline = self.frame("after").evaluate(state)
        for name, mutation in [
            ("multiple selected options", "document.querySelector('#multiple').options[2].selected = true"),
            ("indeterminate input", "document.querySelector('#indeterminate').indeterminate = true"),
        ]:
            for timing in ["periodic", "immediate export"]:
                with self.subTest(property=name, timing=timing):
                    if self.page.locator("#export-dialog").is_visible():
                        self.page.locator("#close-export").click()
                    self.reset_preview()
                    self.wait_ready()
                    self.assert_apply(True)
                    self.assertEqual(self.frame("after").evaluate(state), baseline)
                    self.frame("after").evaluate(mutation)
                    changed = self.frame("after").evaluate(state)
                    self.assertEqual(changed["markup"], baseline["markup"],
                                     "This witness must change real properties without DOM attribute changes")
                    self.assertEqual(changed["value"], baseline["value"])
                    self.assertEqual(changed["index"], baseline["index"])
                    self.assertEqual(changed["checked"], baseline["checked"])
                    if name == "multiple selected options":
                        self.assertEqual(changed["selected"], [True, False, True])
                    else:
                        self.assertTrue(changed["indeterminate"])
                    if timing == "immediate export":
                        self.page.locator("#apply-selected").dispatch_event("click")
                    self.wait_dirty()
                    self.assertFalse(self.page.locator("#export-dialog").is_visible())
                    self.reset_preview()
                    self.wait_ready()
                    self.assert_apply(True)
                    self.assertEqual(self.frame("after").evaluate(state), baseline)
        self.assert_saved_choices()

    def test_bridge_preserves_source_structural_selectors_and_visible_child_override(self):
        source = '''<!doctype html><html><head><title>Source selector semantics</title><style>
body {margin:0; background:rgb(255,255,255)}
body:last-child {background:rgb(241,244,247)}
body > article:last-child {color:rgb(15,85,125); padding-top:17px}
#hidden-parent {visibility:hidden}
#intro {visibility:visible; width:320px; height:90px}
</style></head><body><div id="hidden-parent"><section id="intro"><h3>Visible override</h3></section></div>
<article id="record">Tail article</article></body></html>'''
        measure = """() => ({
            tailCount:document.querySelectorAll('body > article:last-child').length,
            bodyCount:document.querySelectorAll('body:last-child').length,
            color:getComputedStyle(document.querySelector('#record')).color,
            padding:getComputedStyle(document.querySelector('#record')).paddingTop,
            background:getComputedStyle(document.body).backgroundColor,
            ancestor:getComputedStyle(document.querySelector('#hidden-parent')).visibility,
            target:getComputedStyle(document.querySelector('#intro')).visibility
        })"""
        self.page.set_content(source)
        expected = self.page.evaluate(measure)
        self.assertEqual(expected, {"tailCount": 1, "bodyCount": 1, "color": "rgb(15, 85, 125)",
                                    "padding": "17px", "background": "rgb(241, 244, 247)",
                                    "ancestor": "hidden", "target": "visible"})
        document = self.fixture.root / "structural-selectors.html"
        document.write_text(source, encoding="utf-8")
        descriptor = {"html": document.name, "selectors": {"intro": "#intro", "record": "#record"}}
        self.manifest["views"][0]["document"] = descriptor
        self.manifest["proposals"][0]["documents"]["desktop"] = descriptor
        self.load()
        self.page.wait_for_function("""() => ['before','after'].every(side =>
            ['ready','selector-missing'].includes(document.getElementById(side + '-dom-host').dataset.status))""")
        with self.subTest(contract="source structural selector semantics"):
            for side in ["before", "after"]:
                self.assertEqual(self.frame(side).evaluate(measure), expected,
                                 "Inspection machinery must not change native source selector semantics")
                self.assertTrue(self.frame(side).locator("#intro").is_visible())
        with self.subTest(contract="visible child overrides ancestor visibility"):
            self.wait_ready()
            self.choose("P1")
            self.integrated()
            self.wait_ready()
            self.assert_apply(True)
            self.component("record")
            self.component("intro")
            self.assert_apply(True)
            self.assertEqual(self.frame("after").evaluate(measure), expected)

    def test_missing_documents_and_selector_errors_cannot_fall_back_to_hidden_pngs(self):
        variants = {
            "missing document": lambda m: m["proposals"][0]["documents"].update({"desktop": None}),
            "missing selector": lambda m: m["proposals"][0]["documents"]["desktop"]["selectors"].pop("intro"),
            "no match": lambda m: m["proposals"][0]["documents"]["desktop"]["selectors"].update({"intro": "#absent"}),
            "nonunique": lambda m: m["proposals"][0]["documents"]["desktop"]["selectors"].update({"intro": ".repeated"}),
            "nonvisible": lambda m: m["proposals"][0]["documents"]["desktop"]["selectors"].update({"intro": "#hidden-component"}),
            "invalid syntax": lambda m: m["proposals"][0]["documents"]["desktop"]["selectors"].update({"intro": "[invalid("}),
        }
        for label, change in variants.items():
            with self.subTest(label=label):
                manifest = copy.deepcopy(self.manifest)
                change(manifest)
                self.load(manifest)
                self.choose("P1")
                self.integrated()
                self.page.locator("#focus-component").click()
                self.page.locator("#component-select").select_option("intro")
                self.page.wait_for_function("""() => ['missing','error','selector-missing'].includes(
                    document.getElementById('after-dom-host').dataset.status)""")
                self.assert_apply(False)
                self.assertEqual(self.page.locator("#source-dom, #source-capture").count(), 0)
                diagnostic = self.page.locator("#after-empty" if label == "missing document" else "#dom-status")
                self.assertTrue(diagnostic.is_visible())
                self.assertTrue(diagnostic.inner_text().strip())
                if label != "missing document":
                    self.page.locator("#focus-whole").click()
                    self.wait_ready()
                    self.assert_apply(True)
                    self.page.locator("#focus-component").click()
                    self.page.wait_for_function("""() => document.getElementById('after-dom-host')
                        .dataset.status === 'selector-missing'""")
                    self.assert_apply(False)
                image = self.page.locator("#after-image")
                self.assertFalse(image.is_visible(), "A PNG must not hide unavailable DOM evidence")
                self.assertTrue(self.data["proposals"][0]["captures"]["desktop"],
                                "This witness requires a PNG that could otherwise mask the DOM failure")
                self.assert_apply(False)
                self.assertEqual(self.export()["selected"], ["P1"])

    def test_dom_mode_preserves_evidence_constraints_and_final_stage_locks(self):
        for kind in ["capture", "source", "requires", "retained", "applied"]:
            with self.subTest(kind=kind):
                manifest = copy.deepcopy(self.manifest)
                if kind == "capture":
                    manifest["proposals"][0]["captures"]["phone"] = None
                    manifest["proposals"][0]["regions"].pop("phone")
                elif kind == "source":
                    manifest["baseline"]["files"] = {}
                elif kind in {"retained", "applied"}:
                    manifest["stage"] = kind
                    manifest["applied"] = ["P1"] if kind == "applied" else []
                self.load(manifest)
                if kind not in {"retained", "applied"}:
                    self.choose("P3" if kind == "requires" else "P1")
                    self.integrated()
                self.wait_ready()
                self.assert_apply(kind == "capture")
                if kind in {"retained", "applied"}:
                    for status in ["accept", "revise", "reject", "defer", "reset"]:
                        self.assertTrue(self.page.locator(f'button[data-action="{status}"][data-proposal-id="P1"]').is_disabled())
                receipt = self.export()
                if kind == "requires":
                    self.assertEqual(receipt["selected"], ["P3"])

    def test_dom_only_partial_request_reference_survives_switch_reload_and_import(self):
        from playwright.sync_api import expect
        for view in self.manifest["views"]:
            view.pop("before")
            view.pop("regions")
        for item in self.manifest["proposals"] + self.manifest["combinations"]:
            item.pop("captures")
            item.pop("regions")
        self.load()
        self.wait_ready()
        self.assertEqual(self.page.locator("#integrated-comparison").count(), 1)
        self.assertEqual(self.page.locator("#view-selection, #source-dom, #source-capture").count(), 0)
        self.assertEqual(self.page.locator('#proposal-list button[data-proposal-id="P1"][data-action]').count(), 4,
                         "Each row has one preview target and three choice actions")
        self.assertTrue(all(view["before"] is None for view in self.data["views"]))
        self.assertTrue(all(capture is None for capture in self.data["proposals"][0]["captures"].values()))
        self.choose("P1")
        self.assertEqual(self.export()["selected"], ["P1"])
        self.choose("P1", "revise")
        note = "Keep only the title spacing; preserve the existing background."
        self.page.locator("#feedback-note").fill(note)
        self.page.locator("#zoom-actual").click()
        self.page.locator("#element-picker").click()
        self.frame("after").locator("#page-heading").click()
        reference = self.page.locator("#element-reference")
        expect(reference).not_to_have_value("")
        selected_reference = reference.input_value()
        self.page.locator("#add-reference").click()
        expect(self.page.locator("#element-tools")).to_be_hidden()
        expect(reference).to_have_value("")
        expected_note = note + "\n\n" + selected_reference
        expect(self.page.locator("#feedback-note")).to_have_value(expected_note)
        partial = self.export()
        self.assertEqual(partial["selected"], [])
        self.assertEqual(partial["decisions"]["P1"], {"status": "revise", "note": expected_note})
        self.proposal("P2")
        self.proposal("P1")
        expect(self.page.locator("#feedback-note")).to_have_value(expected_note)
        self.choose("P2")
        self.integrated()
        self.wait_ready()
        self.assertEqual(self.page.locator("#focus-whole").get_attribute("aria-pressed"), "true")
        self.assertTrue(self.page.locator("#overall-feedback").evaluate("element => element.open"))
        self.assert_apply(True)
        expected = self.export("apply-selected")
        self.assertEqual(expected["selected"], ["P2"])
        self.assertEqual(expected["preview_id"], "P2")
        self.assertEqual(expected["decisions"]["P1"], partial["decisions"]["P1"])
        checked = self.fixture.check(expected)
        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
        self.page.reload()
        self.wait_ready()
        reloaded = self.export()
        self.assertEqual(reloaded["decisions"], expected["decisions"])
        self.assertEqual(reloaded["selected"], ["P2"])
        self.choose("P1", "pending")
        self.page.locator("#feedback-note").fill("Replace this local draft on import.")
        path = self.fixture.root / "partial-request.json"
        # Feedback permits restoring the draft independently of the active
        # preview; re-enter the exact selection before requesting application.
        expected["intent"] = "review-feedback"
        path.write_text(json.dumps(expected), encoding="utf-8")
        self.page.locator("#show-help").click()
        self.assertTrue(self.page.locator("#import-decisions").is_visible())
        self.page.locator("#import-file").set_input_files(str(path))
        expect(self.page.locator("#notice")).to_contain_text(re.compile("imported", re.I))
        self.page.locator("#close-help").click()
        restored = self.export()
        self.assertEqual(restored["decisions"], expected["decisions"])
        self.assertEqual(restored["selected"], ["P2"])
        self.proposal("P1")
        expect(self.page.locator("#feedback-note")).to_have_value(expected_note)

    def test_partial_request_from_integrated_pending_proposal_opens_its_note(self):
        from playwright.sync_api import expect
        self.load()
        self.wait_ready()
        self.integrated()
        self.wait_ready()
        expect(self.page.locator("#proposal-details")).to_be_hidden()
        self.assertEqual(self.frame("after").locator("body").get_attribute("data-snapshot"), "BASE-desktop")
        self.choose("P1", "revise")
        self.wait_ready()
        note = self.page.locator("#feedback-note")
        expect(note).to_be_visible()
        self.assertEqual(note.get_attribute("data-proposal-id"), "P1")
        self.assertEqual(self.frame("after").locator("body").get_attribute("data-snapshot"), "P1-desktop")
        note.fill("Keep the heading; revise the rest.")
        receipt = self.export()
        self.assertEqual(receipt["selected"], [])
        self.assertEqual(receipt["decisions"]["P1"], {"status": "revise", "note": "Keep the heading; revise the rest."})

    def test_mixed_dom_and_png_sides_switch_automatically_and_apply_exact_selection(self):
        from playwright.sync_api import expect
        self.manifest["proposals"][0]["documents"].pop("desktop")
        self.manifest["views"][1].pop("document")
        self.load()
        self.choose("P1")
        self.integrated()
        self.assertEqual(self.page.locator("#source-dom, #source-capture").count(), 0)
        for view, dom_side, png_side, identity in [
            ("desktop", "before", "after", "BASE"), ("phone", "after", "before", "P1")
        ]:
            with self.subTest(view=view, dom_side=dom_side):
                self.page.locator("#view-select").select_option(view)
                self.page.wait_for_function("side => document.getElementById(side + '-dom-host').dataset.status === 'ready'", arg=dom_side)
                expect(self.page.locator("#" + dom_side + "-dom-host")).to_be_visible()
                self.assertEqual(self.frame(dom_side).locator("body").get_attribute("data-snapshot"), identity + "-" + view)
                image = self.page.locator("#" + png_side + "-image")
                expect(image).to_be_visible()
                self.page.wait_for_function("side => {const image=document.getElementById(side + '-image'); return image.complete && image.naturalWidth > 0;}", arg=png_side)
                expected = (self.data["proposals"][0]["captures"][view] if png_side == "after" else
                            next(item["before"] for item in self.data["views"] if item["id"] == view))
                self.assertEqual(image.get_attribute("src"), expected)
                self.assertFalse(self.page.locator("#" + png_side + "-dom-host").is_visible())
                self.assert_apply(True)
                self.page.locator("#focus-component").click()
                self.page.locator("#component-select").select_option("intro")
                self.page.wait_for_function("side => document.getElementById(side + '-dom-host').dataset.status === 'ready'", arg=dom_side)
                expect(image).to_be_visible()
                dom_scale = self.page.locator("#" + dom_side + "-frame").evaluate("frame => frame.getBoundingClientRect().width / frame.clientWidth")
                png_scale = image.evaluate("image => image.getBoundingClientRect().width / image.naturalWidth")
                self.assertAlmostEqual(dom_scale, png_scale, delta=0.002,
                                       msg="Mixed DOM and PNG components must use the same comparison scale")
                region = (self.manifest["proposals"][0]["regions"][view]["intro"] if png_side == "after" else
                          next(item["regions"]["intro"] for item in self.manifest["views"] if item["id"] == view))
                clip_width = self.page.locator("#" + png_side + "-clip").bounding_box()["width"]
                self.assertAlmostEqual(clip_width, region["width"] * png_scale, delta=0.6)
                self.assert_apply(True)
                receipt = self.export("apply-selected")
                self.assertEqual(receipt["selected"], ["P1"])
                self.assertEqual(receipt["preview_id"], "P1")
                checked = self.fixture.check(receipt)
                self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)

    def test_png_only_view_uses_image_evidence_when_another_view_has_dom(self):
        from playwright.sync_api import expect
        self.manifest["views"][1].pop("document")
        self.manifest["proposals"][0]["documents"].pop("phone")
        self.load()
        self.select_one()
        self.page.locator("#view-select").select_option("phone")
        for side in ["before", "after"]:
            image = self.page.locator("#" + side + "-image")
            expect(image).to_be_visible()
            self.page.wait_for_function("side => {const image=document.getElementById(side + '-image'); return image.complete && image.naturalWidth > 0;}", arg=side)
            self.assertFalse(self.page.locator("#" + side + "-dom-host").is_visible())
        self.assertFalse(self.page.locator("#element-picker").is_visible())
        self.assert_apply(True)
        receipt = self.export("apply-selected")
        self.assertEqual(receipt["selected"], ["P1"])
        checked = self.fixture.check(receipt)
        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)
        self.page.locator("#view-select").select_option("desktop")
        self.wait_ready()
        self.assertTrue(self.page.locator("#element-picker").is_visible())
        self.assert_apply(True)
        self.assert_saved_choices()

    def test_locked_outcomes_keep_proposal_notes_reachable_without_changing_result(self):
        from playwright.sync_api import expect
        for stage in ["applied", "retained"]:
            with self.subTest(stage=stage):
                manifest = copy.deepcopy(self.manifest)
                manifest.update({"stage": stage, "applied": ["P1"] if stage == "applied" else []})
                self.load(manifest)
                self.wait_ready()
                before = self.frame("after").locator("body").get_attribute("data-snapshot")
                self.page.locator('button[data-action="preview"][data-proposal-id="P2"]').click()
                self.wait_ready()
                note = self.page.locator("#feedback-note")
                expect(note).to_be_visible()
                self.assertEqual(note.get_attribute("data-proposal-id"), "P2")
                text = "Follow up on the list spacing after the " + stage + " outcome."
                note.fill(text)
                self.assertEqual(self.frame("after").locator("body").get_attribute("data-snapshot"), before)
                for action in ["accept", "revise", "reject", "defer", "reset"]:
                    self.assertTrue(self.page.locator(f'button[data-action="{action}"][data-proposal-id="P2"]').is_disabled())
                self.assert_apply(False)
                receipt = self.export()
                self.assertEqual(receipt["decisions"]["P2"]["note"], text)
                self.assertEqual(receipt["selected"], manifest["applied"])
                self.integrated()
                self.wait_ready()
                self.assertEqual(self.frame("after").locator("body").get_attribute("data-snapshot"), before)
                self.assert_apply(False)

    def test_dom_only_active_frames_ignore_unused_corrupt_capture_images(self):
        for view in self.manifest["views"]:
            view.pop("before")
            view.pop("regions")
        for item in self.manifest["proposals"] + self.manifest["combinations"]:
            item.pop("captures")
            item.pop("regions")
        self.load()
        self.select_one()
        # Simulate a native decode failure in the unused capture elements.
        # The frozen DOM is the authoritative evidence for both active sides.
        for side in ["before", "after"]:
            image = self.page.locator("#" + side + "-image")
            image.evaluate("image => image.src = 'data:image/png;base64,AA=='")
        self.page.wait_for_function("""() => ['before','after'].every(side => {
            const image = document.getElementById(side + '-image');
            return image.complete && image.naturalWidth === 0;
        })""")
        self.wait_ready()
        self.assert_apply(True)
        for side in ["before", "after"]:
            self.assertFalse(self.page.locator("#" + side + "-image").is_visible())
            self.assertTrue(self.page.locator("#" + side + "-dom-host").is_visible())
        receipt = self.export("apply-selected")
        self.assertEqual(receipt["selected"], ["P1"])
        checked = self.fixture.check(receipt)
        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)

    def test_handoff_message_and_receipt_distinguish_partial_feedback_from_apply(self):
        from playwright.sync_api import expect
        self.context.add_init_script("""Object.defineProperty(navigator, 'clipboard', {
            configurable:true, value:{writeText:async value => {window.__copiedMessage = value;}}
        });""")
        self.load()
        self.choose("P1", "revise")
        note = "Keep the title spacing, but restore the old background."
        self.page.locator("#feedback-note").fill(note)
        self.choose("P2")
        self.integrated()
        self.wait_ready()
        self.page.locator("#open-handoff").click()
        message = self.page.locator("#handoff-message")
        expect(message).to_be_visible()
        self.assertFalse(self.page.locator("details.export-details").evaluate("element => element.open"))
        feedback_text = message.input_value()
        for text in ["Prepare a new before/after preview", "Do not apply these drafts", "Take part / request changes", note]:
            self.assertIn(text, feedback_text)
        feedback = json.loads(self.page.locator("#export-json").input_value())
        self.assertEqual(feedback["intent"], "review-feedback")
        self.assertEqual(feedback["selected"], ["P2"])
        self.assertEqual(feedback["decisions"]["P1"]["status"], "revise")
        self.page.locator("#copy-message").click()
        self.page.wait_for_function("text => window.__copiedMessage === text", arg=feedback_text)
        self.handoff("apply-selected")
        application_text = message.input_value()
        self.assertNotEqual(application_text, feedback_text)
        self.assertIn("after checking the current source", application_text)
        self.assertIn("Do not apply partial requests", application_text)
        self.assertIn("Apply this exact selection: P2 (P2)", application_text)
        self.assertNotIn("Apply this exact selection: P1", application_text)
        self.assertIn(note, application_text, "The partial note remains available for a later preview")
        applied = json.loads(self.page.locator("#export-json").input_value())
        self.assertEqual(applied["intent"], "apply-selected")
        self.assertEqual(applied["selected"], ["P2"])
        self.assertEqual(applied["preview_id"], "P2")
        self.assertEqual(applied["decisions"]["P1"], feedback["decisions"]["P1"])
        self.page.locator("#copy-message").click()
        self.page.wait_for_function("text => window.__copiedMessage === text", arg=application_text)
        downloaded = self.export("apply-selected")
        for key in ["intent", "selected", "preview_id", "decisions"]:
            self.assertEqual(downloaded[key], applied[key])
        checked = self.fixture.check(downloaded)
        self.assertEqual(checked.returncode, 0, checked.stdout + checked.stderr)

    def test_handoff_copy_fallback_exposes_selectable_message_and_receipt(self):
        self.context.add_init_script("Object.defineProperty(navigator, 'clipboard', {get() {return undefined;}});")
        self.load()
        self.choose("P1", "revise")
        self.page.locator("#feedback-note").fill("Keep only the heading change.")
        self.handoff()
        self.page.locator("#copy-message").click()
        message = self.page.locator("#handoff-message")
        self.assertTrue(message.is_visible())
        self.assertEqual(message.evaluate("element => element.value.slice(element.selectionStart, element.selectionEnd)"),
                         message.input_value())
        self.assertIn("Keep only the heading change.", message.input_value())
        self.assertRegex(self.page.locator("#export-status").inner_text(), r"(?i)keyboard")
        self.open_details("details.export-details")
        self.page.locator("#copy-json").click()
        receipt = self.page.locator("#export-json")
        self.assertTrue(receipt.is_visible())
        self.assertEqual(receipt.evaluate("element => element.value.slice(element.selectionStart, element.selectionEnd)"),
                         receipt.input_value())
        self.assertEqual(json.loads(receipt.input_value())["decisions"]["P1"]["status"], "revise")

    def test_apply_handoff_rechecks_native_dom_before_copy_or_download(self):
        self.context.add_init_script("""Object.defineProperty(navigator, 'clipboard', {
            configurable:true, value:{writeText:async value => {window.__copiedMessage = value;}}
        });""")
        self.load()
        self.select_one()
        downloads = []
        self.page.on("download", lambda download: downloads.append(download.suggested_filename))
        for action in ["copy-message", "copy-json", "download-json"]:
            with self.subTest(action=action):
                self.reset_preview()
                self.wait_ready()
                self.handoff("apply-selected")
                if action != "copy-message":
                    self.open_details("details.export-details")
                # Queue a real source edit from the trusted click's capture
                # phase. The following freshness-check message reaches that
                # same frame after this mutation message, without a timer race
                # against automatic closing of an already-dirty handoff.
                self.frame("after").evaluate("""addEventListener('message', event => {
                    if (event.source === parent && event.data?.type === 'test-edit-before-export')
                        document.querySelector('#record').textContent = 'Edited at export time';
                })""")
                button = self.page.locator("#" + action)
                button.evaluate("""button => button.addEventListener('click', () => {
                    document.getElementById('after-frame').contentWindow.postMessage({type:'test-edit-before-export'}, '*');
                }, {capture:true, once:true})""")
                button.click()
                self.wait_dirty()
                self.assertFalse(self.page.locator("#export-dialog").is_visible())
                self.assertIsNone(self.page.evaluate("window.__copiedMessage"))
                self.assertEqual(downloads, [])

    @contextmanager
    def local_server(self):
        class QuietHandler(http.server.SimpleHTTPRequestHandler):
            def log_message(self, *args):
                pass
        handler = functools.partial(QuietHandler, directory=str(self.fixture.root))
        server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            yield "http://127.0.0.1:" + str(server.server_address[1])
        finally:
            server.shutdown()
            server.server_close()
            thread.join(timeout=5)

    def test_snapshot_preserves_native_state_css_order_pseudos_and_loaded_image(self):
        (self.fixture.root / "style.css").write_text(
            '.card {color:rgb(110,20,30); padding-left:17px} .card::before {content:"From stylesheet"}', encoding="utf-8")
        image = png_bytes(3, 2, (20, 90, 40))
        (self.fixture.root / "pixel.png").write_bytes(image)
        source = '''<!doctype html><html><head><title>Ordinary source</title>
<link rel="stylesheet" href="style.css" media="(min-width:600px)">
<style>.card {color:rgb(20,90,40)} .card::before {content:"Current pseudo"}</style>
</head><body><article id="ordinary" class="card">Actual source article</article>
<form action="/write"><input id="text" value="attribute"><input id="check" type="checkbox">
<textarea id="notes">attribute</textarea><select id="option"><option>A</option><option>B</option></select>
<button onclick="window.activated=true">Write</button></form><details id="details"><summary>Details</summary>Body</details>
<img id="source-image" src="pixel.png" width="3" height="2"><a href="/navigate">Navigation</a>
<script>window.sourceScriptRan = true;</script></body></html>'''
        (self.fixture.root / "ordinary.html").write_text(source, encoding="utf-8")
        with self.local_server() as address:
            self.page.goto(address + "/ordinary.html")
            self.page.locator("#text").fill("current value")
            self.page.locator("#check").check()
            self.page.locator("#notes").fill("current notes")
            self.page.locator("#option").select_option(label="B")
            self.page.locator("#details").evaluate("element => element.open = true")
            frozen = self.page.evaluate((ASSETS / "snapshot.js").read_text(encoding="utf-8"))
        self.assertIsInstance(frozen, str)
        self.assertIn("data:image/png;base64," + base64.b64encode(image).decode("ascii"), frozen)
        result = self.fixture.root / "frozen.html"
        result.write_text(frozen, encoding="utf-8")
        self.page.goto(result.as_uri())
        observed = self.page.evaluate("""() => ({
            tag:document.querySelector('#ordinary').tagName,
            text:document.querySelector('#text').value, checked:document.querySelector('#check').checked,
            notes:document.querySelector('#notes').value, option:document.querySelector('#option').value,
            open:document.querySelector('#details').open,
            color:getComputedStyle(document.querySelector('#ordinary')).color,
            padding:getComputedStyle(document.querySelector('#ordinary')).paddingLeft,
            pseudo:getComputedStyle(document.querySelector('#ordinary'),'::before').content,
            image:document.querySelector('#source-image').naturalWidth,
            scripts:document.querySelectorAll('script').length,
            handlers:[...document.querySelectorAll('*')].some(el => [...el.attributes].some(a => /^on/i.test(a.name))),
            action:document.querySelector('form').getAttribute('action'), href:document.querySelector('a').getAttribute('href')
        })""")
        self.assertEqual(observed["tag"], "ARTICLE")
        self.assertEqual(observed["text"], "current value")
        self.assertTrue(observed["checked"])
        self.assertEqual(observed["notes"], "current notes")
        self.assertEqual(observed["option"], "B")
        self.assertTrue(observed["open"])
        self.assertEqual(observed["color"], "rgb(20, 90, 40)")
        self.assertEqual(observed["padding"], "17px")
        self.assertEqual(observed["pseudo"], '"Current pseudo"')
        self.assertEqual(observed["image"], 3)
        self.assertEqual(observed["scripts"], 0)
        self.assertFalse(observed["handlers"])
        self.assertFalse(observed["action"])
        self.assertTrue(not observed["href"] or observed["href"].startswith("#"),
                        "Frozen link style may retain an inert local fragment, but never a source destination")
        self.page.set_viewport_size({"width": 390, "height": 844})
        self.assertEqual(self.page.locator("#ordinary").evaluate(
            "element => getComputedStyle(element).paddingLeft"), "0px",
            "Inlining must preserve the original stylesheet's media condition")
        # Snapshot output must be accepted by the same authoring path as a
        # manually authored frozen document, including its embedded assets.
        self.manifest["views"][0]["document"] = {"html": result.name, "selectors": {}}
        built = self.fixture.build(self.manifest)
        self.assertEqual(built.returncode, 0, built.stdout + built.stderr)

    def test_snapshot_preserves_leading_line_feed_in_native_textarea_pre_and_listing(self):
        self.page.set_content('<!doctype html><html><head><title>Leading LF</title></head>'
                              '<body><textarea id="notes"></textarea><pre id="code"></pre>'
                              '<listing id="listing"></listing></body></html>')
        self.page.evaluate("""() => {
            document.querySelector('#notes').value = '\\nleading notes\\nsecond line';
            document.querySelector('#code').textContent = '\\nleading code\\nsecond line';
            document.querySelector('#listing').textContent = '\\nleading listing\\nsecond line';
        }""")
        state = """() => ({notes:document.querySelector('#notes').value,
                            code:document.querySelector('#code').textContent,
                            listing:document.querySelector('#listing').textContent})"""
        before = self.page.evaluate(state)
        self.assertEqual(before, {"notes": "\nleading notes\nsecond line",
                                  "code": "\nleading code\nsecond line",
                                  "listing": "\nleading listing\nsecond line"})
        frozen = self.page.evaluate((ASSETS / "snapshot.js").read_text(encoding="utf-8"))
        self.page.set_content(frozen)
        self.assertEqual(self.page.evaluate(state), before,
                         "Parsing the frozen HTML must not consume the source's first line feed")
        document = self.fixture.root / "leading-lf.html"
        document.write_text(frozen, encoding="utf-8")
        self.manifest["proposals"][0]["documents"]["desktop"] = {"html": document.name, "selectors": {}}
        self.load()
        self.page.locator("#focus-whole").click()
        self.wait_ready()
        self.assertEqual(self.frame("after").evaluate(state), before,
                         "The viewer's document serialization must also preserve the first line feed")

    def test_snapshot_density_preserves_intrinsic_and_rendered_size_or_fails_clearly(self):
        from playwright.sync_api import Error
        context = self.browser.new_context(viewport={"width": 800, "height": 600}, device_scale_factor=2)
        try:
            source = context.new_page()
            restored = context.new_page()
            base = "data:image/png;base64," + base64.b64encode(png_bytes(20, 20, (20, 90, 40))).decode("ascii")
            dense = "data:image/png;base64," + base64.b64encode(png_bytes(40, 40, (20, 90, 40))).decode("ascii")
            source.set_content('<!doctype html><html><head><title>Image density</title></head>'
                               f'<body><img id="image" src="{base}" srcset="{dense} 2x"></body></html>')
            source.locator("#image").evaluate("image => image.decode()")
            self.assertEqual(source.locator("#image").evaluate("image => image.currentSrc"), dense,
                             "The probe must actually select the 2x candidate")
            measure = """() => {
                const image = document.querySelector('#image');
                const rect = image.getBoundingClientRect();
                return {naturalWidth:image.naturalWidth,naturalHeight:image.naturalHeight,
                        width:rect.width,height:rect.height};
            }"""
            before = source.evaluate(measure)
            self.assertEqual(before, {"naturalWidth": 20, "naturalHeight": 20, "width": 20, "height": 20})
            try:
                frozen = source.evaluate((ASSETS / "snapshot.js").read_text(encoding="utf-8"))
            except Error as error:
                self.assertRegex(str(error), r"(?i)(density|intrinsic)",
                                 "An unsupported density must be explained explicitly")
                self.assertRegex(str(error), r"(?i)(unsupported|cannot|not support)")
            else:
                restored.set_content(frozen)
                restored.locator("#image").evaluate("image => image.decode()")
                self.assertEqual(restored.evaluate(measure), before,
                                 "Freezing selected source bytes must not enlarge a density-corrected image")
        finally:
            context.close()

    def test_snapshot_top_layer_and_quirks_fail_clearly_while_standards_remain_supported(self):
        from playwright.sync_api import Error
        expression = (ASSETS / "snapshot.js").read_text(encoding="utf-8")
        for state, body, activate, active in [
            ("popover", '<div id="target" popover>Visible popover</div>',
             "document.querySelector('#target').showPopover()", ":popover-open"),
            ("modal", '<dialog id="target">Visible modal</dialog>',
             "document.querySelector('#target').showModal()", ":modal"),
        ]:
            with self.subTest(state=state):
                self.page.set_content('<!doctype html><html><head><title>Top layer</title></head>'
                                      '<body>' + body + '</body></html>')
                self.page.evaluate(activate)
                self.assertTrue(self.page.locator("#target").evaluate("(element, selector) => element.matches(selector)", active))
                self.assertTrue(self.page.locator("#target").is_visible())
                with self.assertRaisesRegex(Error, r"(?i)(popover|modal|top.layer)"):
                    self.page.evaluate(expression)
        body = ('<html><head><title>Compatibility mode</title>'
                '<style>#box{width:100px;padding:10px;border:5px solid}</style></head>'
                '<body><div id="box">Box</div><textarea id="notes">Ordinary state</textarea></body></html>')
        self.page.set_content(body)
        self.assertEqual(self.page.evaluate("document.compatMode"), "BackCompat")
        with self.assertRaisesRegex(Error, r"(?i)(standards|quirks|compat)"):
            self.page.evaluate(expression)
        self.page.set_content("<!doctype html>" + body)
        self.assertEqual(self.page.evaluate("document.compatMode"), "CSS1Compat")
        before = self.page.locator("#box").evaluate("element => element.getBoundingClientRect().width")
        frozen = self.page.evaluate(expression)
        self.page.set_content(frozen)
        self.assertEqual(self.page.evaluate("document.compatMode"), "CSS1Compat")
        self.assertEqual(self.page.locator("#box").evaluate("element => element.getBoundingClientRect().width"), before)
        self.assertEqual(self.page.locator("#notes").input_value(), "Ordinary state")

    def test_snapshot_unportable_rendering_and_missing_assets_fail_explicitly(self):
        expression = (ASSETS / "snapshot.js").read_text(encoding="utf-8")
        for label, body, prepare in [
            ("canvas", '<canvas id="drawing"></canvas>', "document.querySelector('canvas').getContext('2d').fillRect(0,0,4,4)"),
            ("shadow", '<div id="host"></div>', "document.querySelector('#host').attachShadow({mode:'open'}).innerHTML='<p>Shadow content</p>'"),
        ]:
            with self.subTest(label=label):
                self.page.set_content("<!doctype html><html><head><title>Unsupported</title></head><body>" + body + "</body></html>")
                self.page.evaluate(prepare)
                with self.assertRaisesRegex(Exception, r"(?i)(canvas|shadow|unsupported|snapshot)"):
                    self.page.evaluate(expression)
        missing = self.fixture.root / "missing-asset.html"
        missing.write_text('<!doctype html><html><head><title>Missing asset</title></head>'
                           '<body><img src="does-not-exist.png"></body></html>', encoding="utf-8")
        with self.local_server() as address:
            self.page.goto(address + "/missing-asset.html")
            with self.assertRaisesRegex(Exception, r"(?i)(asset|image|fetch|load|portable|snapshot)"):
                self.page.evaluate(expression)


if __name__ == "__main__":
    unittest.main(verbosity=2)
