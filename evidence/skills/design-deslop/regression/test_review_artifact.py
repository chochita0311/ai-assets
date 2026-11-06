#!/usr/bin/env python3
"""Contract-based tests for the self-contained design review artifact.

Run the stdlib builder/consumer checks with Python 3.9+, or add ``--browser``
for headless Playwright or ``--headed`` for a visible local Chromium installation.
These tests generate synthetic source and PNG files; they never need a website.
DESIGN_DESLOP_TEST_WORK_ROOT chooses a task-owned temporary parent directory.
DESIGN_DESLOP_KEEP_TEST_ARTIFACTS=1 retains fixtures for active failure diagnosis.
DESIGN_DESLOP_BROWSER_EXECUTABLE selects an existing browser, if necessary.
"""

import base64
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import struct
import subprocess
import sys
import tempfile
import unittest
import zlib


REPOSITORY = Path(__file__).resolve().parents[4]
BUILDER = REPOSITORY / "skills/design-deslop/scripts/review.py"
TEMPLATE = REPOSITORY / "skills/design-deslop/assets/review.html"
RUN_HEADED = "--headed" in sys.argv
RUN_BROWSER = "--browser" in sys.argv or RUN_HEADED
for flag in ["--browser", "--headed"]:
    if flag in sys.argv:
        sys.argv.remove(flag)


def png_bytes(width, height, color, regions=()):
    """Produce a real, decodable RGB PNG using only the standard library."""
    def chunk(kind, value):
        return (struct.pack(">I", len(value)) + kind + value
                + struct.pack(">I", zlib.crc32(kind + value) & 0xffffffff))

    rows = [bytearray(bytes(color) * width) for _ in range(height)]
    for rect, fill in regions:
        x, y = rect["x"], rect["y"]
        for row in rows[y:y + rect["height"]]:
            row[x * 3:(x + rect["width"]) * 3] = bytes(fill) * rect["width"]
    pixels = b"".join(b"\0" + bytes(row) for row in rows)
    return (b"\x89PNG\r\n\x1a\n"
            + chunk(b"IHDR", struct.pack(">IIBBBBB", width, height, 8, 2, 0, 0, 0))
            + chunk(b"IDAT", zlib.compress(pixels))
            + chunk(b"IEND", b""))


def embedded_data(path):
    html = Path(path).read_text(encoding="utf-8")
    match = re.search(
        r'<script\b(?=[^>]*\bid=[\"\x27]review-data[\"\x27])[^>]*>(.*?)</script\s*>',
        html, re.DOTALL | re.IGNORECASE)
    if not match:
        raise AssertionError("Generated review has no review-data JSON script")
    return json.loads(match.group(1))


def tree_snapshot(root):
    return {
        path.relative_to(root).as_posix(): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in sorted(Path(root).rglob("*")) if path.is_file()
    }


class Fixture:
    def __init__(self, label):
        parent = os.environ.get("DESIGN_DESLOP_TEST_WORK_ROOT")
        if parent:
            Path(parent).mkdir(parents=True, exist_ok=True)
        self.root = Path(tempfile.mkdtemp(prefix=label + "-", dir=parent))
        self.site = self.root / "site"
        self.site.mkdir()
        source = b"<!doctype html><title>Synthetic notebook</title><main>Notes</main>\n"
        (self.site / "notebook.html").write_bytes(source)
        self.manifest_path = self.root / "manifest.json"
        self.review = self.root / "review.html"
        views = []
        for name, width, height in [("desktop", 960, 720), ("phone", 390, 844)]:
            before = "before-" + name + ".png"
            (self.root / before).write_bytes(png_bytes(width, height, (230, 230, 230)))
            views.append({"id": name, "label": name.title(), "width": width,
                          "height": height, "conditions": "/notebook.html; default; top",
                          "before": before})
        proposals = []
        definitions = [
            ("P1", "Header option", "header", [], []),
            ("P1-B", "Alternate header", "header", [], []),
            ("P2", "List spacing", "list", [], []),
            ("P3", "Dependent detail", "detail", ["P1"], []),
            ("P4", "Conflicting layout", "layout", [], ["P1"]),
        ]
        for index, (identifier, title, group, requires, conflicts) in enumerate(definitions):
            captures = {}
            for view in views:
                capture = identifier + "-" + view["id"] + ".png"
                (self.root / capture).write_bytes(png_bytes(
                    view["width"], view["height"], (35 + index * 35, 80, 150)))
                captures[view["id"]] = capture
            proposals.append({
                "id": identifier, "group": group, "title": title,
                "observation": "Repeated introduction delays notes.",
                "benefit": "Notes begin earlier.",
                "tradeoff": "Less introductory context.",
                "question": "Does this change fit the notebook?",
                "scope": ["notebook.html: main"],
                "preserved": ["Note content and search"],
                "checks": ["Desktop and phone captures available"],
                "requires": requires, "conflicts": conflicts,
                "evidence": "rendered", "captures": captures,
            })
        combined = {}
        for view in views:
            name = "combined-" + view["id"] + ".png"
            (self.root / name).write_bytes(png_bytes(view["width"], view["height"], (80, 160, 60)))
            combined[view["id"]] = name
        self.manifest = {
            "version": 1, "review_id": "synthetic-notebook-r1", "round": 1,
            "language": "en", "stage": "proposal", "title": "Synthetic notebook review",
            "summary": "Compare focused changes using synthetic local captures.",
            "baseline": {"label": "Original", "description": "Current synthetic source.",
                         "files": {"notebook.html": hashlib.sha256(source).hexdigest()}},
            "views": views, "proposals": proposals,
            "combinations": [{"id": "C12", "proposals": ["P1", "P2"],
                              "evidence": "rendered", "captures": combined}],
            "applied": [],
        }

    def with_components(self):
        """Measure each exact synthetic capture independently, with unequal boxes."""
        manifest = copy.deepcopy(self.manifest)
        manifest["components"] = [
            {"id": "intro", "label": "Introduction"},
            {"id": "record", "label": "Representative note"},
            {"id": "list", "label": "Note list"},
            {"id": "footer", "label": "Footer"},
        ]

        def rect(x, y, width, height):
            return {"x": x, "y": y, "width": width, "height": height}

        baseline = {
            "desktop": {"intro": rect(40, 30, 520, 120), "record": rect(80, 210, 400, 90),
                        "list": rect(30, 350, 850, 300), "footer": rect(10, 680, 80, 30)},
            "phone": {"intro": rect(20, 20, 340, 100), "record": rect(30, 160, 300, 80),
                      "list": rect(15, 280, 360, 480), "footer": rect(15, 795, 200, 30)},
        }
        scopes = {"P1": ["intro", "record"], "P1-B": ["intro"], "P2": ["list"],
                  "P3": ["record"], "P4": ["list"]}
        results = {
            "P1": {"desktop": {"intro": rect(100, 70, 300, 90), "record": rect(120, 260, 420, 100)},
                   "phone": {"intro": rect(30, 45, 300, 70), "record": rect(30, 180, 310, 100)}},
            "P1-B": {"desktop": {"intro": rect(80, 50, 440, 100)},
                     "phone": {"intro": rect(25, 30, 320, 90)}},
            "P2": {"desktop": {"list": rect(50, 330, 820, 340)},
                   "phone": {"list": rect(20, 240, 350, 500)}},
            "P3": {"desktop": {"record": rect(90, 180, 420, 100)},
                   "phone": {"record": rect(25, 130, 310, 80)}},
            "P4": {"desktop": {"list": rect(40, 320, 850, 360)},
                   "phone": {"list": rect(20, 260, 350, 520)}},
        }
        combined = {
            "desktop": {"intro": rect(60, 25, 480, 100), "record": rect(100, 190, 460, 80),
                        "list": rect(50, 300, 850, 360)},
            "phone": {"intro": rect(25, 20, 320, 65), "record": rect(30, 120, 280, 70),
                      "list": rect(20, 230, 350, 500)},
        }
        self.component_colors = {
            "baseline": {"intro": (190, 30, 40), "record": (190, 140, 25),
                         "list": (30, 130, 90), "footer": (100, 70, 160)},
            "proposal": {"intro": (35, 100, 210), "record": (10, 145, 170), "list": (90, 160, 35)},
            "combination": {"intro": (90, 45, 195), "record": (185, 80, 25), "list": (20, 120, 145)},
        }
        # The bright background is intentionally unlike every crop. Screenshots
        # expose an incorrect origin or unclipped neighboring source pixels.
        def paint(path, view, regions, colors):
            (self.root / path).write_bytes(png_bytes(
                view["width"], view["height"], (247, 0, 247),
                [(box, colors[identifier]) for identifier, box in regions.items()]))

        for view in manifest["views"]:
            view["regions"] = baseline[view["id"]]
            paint(view["before"], view, view["regions"], self.component_colors["baseline"])
        for proposal in manifest["proposals"]:
            proposal["components"] = scopes[proposal["id"]]
            proposal["regions"] = results[proposal["id"]]
            for view in manifest["views"]:
                paint(proposal["captures"][view["id"]], view, proposal["regions"][view["id"]],
                      self.component_colors["proposal"])
        manifest["combinations"][0]["regions"] = combined
        for view in manifest["views"]:
            paint(manifest["combinations"][0]["captures"][view["id"]], view, combined[view["id"]],
                  self.component_colors["combination"])
        return manifest

    def write_legacy_artifact(self):
        """Make a pre-component payload without consulting the current normalizer."""
        data = copy.deepcopy(self.manifest)

        def embed(path):
            return "data:image/png;base64," + base64.b64encode((self.root / path).read_bytes()).decode("ascii")

        for view in data["views"]:
            view["before"] = embed(view["before"])
        for item in data["proposals"] + data["combinations"]:
            item["captures"] = {key: embed(path) for key, path in item["captures"].items()}
        template = ('<!doctype html><title>Legacy review fixture</title>'
                    '<script id="review-data" type="application/json">__REVIEW_DATA__</script>')
        canonical = json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=True)
        data["review_fingerprint"] = hashlib.sha256((canonical + template).encode("utf-8")).hexdigest()
        legacy = self.root / "legacy-review.html"
        legacy.write_text(template.replace("__REVIEW_DATA__", json.dumps(
            data, sort_keys=True, separators=(",", ":"), ensure_ascii=True)), encoding="utf-8")
        return legacy, data

    def build(self, manifest=None, output=None):
        self.manifest_path.write_text(json.dumps(
            self.manifest if manifest is None else manifest, ensure_ascii=False), encoding="utf-8")
        return subprocess.run(
            [sys.executable, str(BUILDER), "build", str(self.manifest_path),
             "--output", str(output or self.review)], cwd=self.root,
            text=True, capture_output=True, timeout=30)

    def receipt(self, selected=(), intent="review-feedback", preview=None, data=None):
        data = data or embedded_data(self.review)
        selected = list(selected)
        if preview is None and len(selected) == 1:
            preview = selected[0]
        return {
            "format": "design-deslop-decisions", "version": 1,
            "review_id": data["review_id"], "round": data["round"],
            "review_fingerprint": data["review_fingerprint"], "intent": intent,
            "preview_id": preview, "selected": selected, "review_note": "",
            "decisions": {p["id"]: {"status": "accept" if p["id"] in selected else "pending",
                                      "note": ""} for p in data["proposals"]},
            "exported_at": "2026-01-01T00:00:00.000Z",
        }

    def check(self, receipt, source=True, review=None):
        decision_path = self.root / "decisions.json"
        decision_path.write_text(json.dumps(receipt), encoding="utf-8")
        command = [sys.executable, str(BUILDER), "check", str(review or self.review), str(decision_path)]
        if source:
            command.extend(["--source-root", str(self.site)])
        return subprocess.run(command, cwd=self.root, text=True, capture_output=True, timeout=30)

    def close(self):
        if os.environ.get("DESIGN_DESLOP_KEEP_TEST_ARTIFACTS") == "1":
            print("Retained test fixture: " + str(self.root), file=sys.stderr)
        else:
            shutil.rmtree(self.root)


class BuilderAndReceiptTests(unittest.TestCase):
    def setUp(self):
        self.fixture = Fixture(self._testMethodName)

    def tearDown(self):
        self.fixture.close()

    def build(self, manifest=None):
        result = self.fixture.build(manifest)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return embedded_data(self.fixture.review)

    def assert_rejected(self, result):
        self.assertNotEqual(result.returncode, 0, "Invalid input was accepted: " + result.stdout)
        self.assertTrue((result.stdout + result.stderr).strip(), "Failure must explain the invalid input")

    def test_normalization_fingerprint_safe_embedding_and_no_source_writes(self):
        original = tree_snapshot(self.fixture.site)
        manifest = copy.deepcopy(self.fixture.manifest)
        dangerous = '</script><img src="https://invalid.example/leak" onerror="window.injected=1">&'
        manifest["title"] = dangerous
        manifest.pop("language")
        manifest.pop("stage")
        manifest.pop("applied")
        for key in ["preserved", "checks"]:
            manifest["proposals"][0].pop(key)
        for key in ["group", "requires", "conflicts"]:
            manifest["proposals"][2].pop(key)
        data = self.build(manifest)
        self.assertEqual(data["title"], dangerous)
        self.assertEqual(data["language"], "en")
        self.assertEqual(data["stage"], "proposal")
        self.assertEqual(data["applied"], [])
        self.assertEqual(data["proposals"][0]["preserved"], [])
        self.assertEqual(data["proposals"][0]["checks"], [])
        self.assertEqual(data["proposals"][2]["group"], "P2")
        self.assertEqual(data["proposals"][2]["requires"], [])
        self.assertEqual(data["proposals"][2]["conflicts"], [])
        fingerprint = data.pop("review_fingerprint")
        canonical = json.dumps(data, sort_keys=True, separators=(",", ":"), ensure_ascii=True).encode("utf-8")
        template = TEMPLATE.read_bytes()
        if b"__DOM_PREVIEW__" in template:
            template = template.replace(b"__DOM_PREVIEW__", (TEMPLATE.parent / "dom-preview.js").read_bytes())
        self.assertEqual(fingerprint, hashlib.sha256(canonical + template).hexdigest())
        for view in data["views"]:
            self.assertTrue(view["before"].startswith("data:image/png;base64,"))
            self.assertTrue(base64.b64decode(view["before"].split(",", 1)[1]).startswith(b"\x89PNG"))
        html = self.fixture.review.read_text(encoding="utf-8")
        self.assertNotIn(dangerous, html)
        self.assertIn("\\u003c", html)
        self.assertEqual(original, tree_snapshot(self.fixture.site))

    def test_malformed_manifest_and_impossible_sets_rejected(self):
        cases = {}

        def changed(label, change):
            manifest = copy.deepcopy(self.fixture.manifest)
            change(manifest)
            cases[label] = manifest

        changed("unknown field", lambda m: m.update({"unknown": True}))
        changed("boolean version", lambda m: m.update({"version": True}))
        changed("boolean round", lambda m: m.update({"round": True}))
        changed("unsupported language", lambda m: m.update({"language": "xx"}))
        changed("unknown stage", lambda m: m.update({"stage": "ready"}))
        changed("unknown baseline field", lambda m: m["baseline"].update({"unknown": True}))
        changed("unknown view field", lambda m: m["views"][0].update({"unknown": True}))
        changed("unknown proposal field", lambda m: m["proposals"][0].update({"unknown": True}))
        changed("unknown combination field", lambda m: m["combinations"][0].update({"unknown": True}))
        changed("missing required detail", lambda m: m["proposals"][0].pop("question"))
        changed("invalid scope structure", lambda m: m["proposals"][0].update({"scope": "notebook.html"}))
        changed("nonpositive width", lambda m: m["views"][0].update({"width": 0}))
        changed("invalid ID", lambda m: m["proposals"][0].update({"id": "P/1"}))
        changed("duplicate ID", lambda m: m["proposals"][1].update({"id": "P1"}))
        changed("colliding combination ID", lambda m: m["combinations"][0].update({"id": "P1"}))
        changed("unknown capture view", lambda m: m["proposals"][0]["captures"].update({"tablet": None}))
        changed("missing capture view", lambda m: m["proposals"][0]["captures"].pop("phone"))
        changed("wrong PNG width", lambda m: m["views"][0].update({"before": "before-phone.png"}))
        changed("URL capture", lambda m: m["views"][0].update({"before": "https://invalid.example/test.png"}))
        changed("source traversal", lambda m: m["baseline"].update({"files": {"../outside": "a" * 64}}))
        changed("invalid source digest", lambda m: m["baseline"].update({"files": {"notebook.html": "A" * 64}}))
        changed("self requirement", lambda m: m["proposals"][0].update({"requires": ["P1"]}))
        changed("unknown requirement", lambda m: m["proposals"][0].update({"requires": ["missing"]}))
        changed("same group requirement", lambda m: m["proposals"][0].update({"requires": ["P1-B"]}))
        changed("requires cycle", lambda m: m["proposals"][0].update({"requires": ["P3"]}))
        changed("self conflict", lambda m: m["proposals"][0].update({"conflicts": ["P1"]}))
        changed("combination sibling variants", lambda m: m["combinations"][0].update({"proposals": ["P1", "P1-B"]}))
        changed("combination conflict reversed", lambda m: m["combinations"][0].update({"proposals": ["P1", "P4"]}))
        changed("combination missing dependency", lambda m: m["combinations"][0].update({"proposals": ["P2", "P3"]}))
        changed("nonempty proposal applied set", lambda m: m.update({"applied": ["P1"]}))
        changed("retained has applied set", lambda m: m.update({"stage": "retained", "applied": ["P1"]}))
        changed("applied missing combined preview", lambda m: m.update({"stage": "applied", "applied": ["P1", "P3"]}))
        changed("applied empty set", lambda m: m.update({"stage": "applied", "applied": []}))
        for label, manifest in cases.items():
            with self.subTest(label=label):
                self.assert_rejected(self.fixture.build(manifest))

    def test_receipt_identity_shape_selection_and_preview(self):
        self.build()
        good = self.fixture.receipt(["P1"], "apply-selected")
        result = self.fixture.check(good)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        mutations = {
            "stale fingerprint": lambda r: r.update({"review_fingerprint": "0" * 64}),
            "different review": lambda r: r.update({"review_id": "another-review"}),
            "different round": lambda r: r.update({"round": 2}),
            "unknown option": lambda r: r["decisions"].update({"unknown": {"status": "pending", "note": ""}}),
            "missing option": lambda r: r["decisions"].pop("P2"),
            "selected not accepted": lambda r: r.update({"selected": ["P2"]}),
            "invalid status": lambda r: r["decisions"]["P2"].update({"status": "maybe"}),
            "non-string note": lambda r: r["decisions"]["P2"].update({"note": 7}),
            "missing review note": lambda r: r.pop("review_note"),
            "non-string review note": lambda r: r.update({"review_note": 7}),
            "wrong displayed preview": lambda r: r.update({"preview_id": "P2"}),
            "no displayed preview": lambda r: r.update({"preview_id": None}),
        }
        for label, change in mutations.items():
            with self.subTest(label=label):
                receipt = copy.deepcopy(good)
                change(receipt)
                self.assert_rejected(self.fixture.check(receipt))
        combined = self.fixture.receipt(["P2", "P1"], "apply-selected", "C12")
        self.assertEqual(self.fixture.check(combined).returncode, 0)

    def test_source_freshness_missing_and_symlink_escape_are_read_only(self):
        self.build()
        receipt = self.fixture.receipt(["P1"], "apply-selected")
        original = tree_snapshot(self.fixture.site)
        self.assertEqual(self.fixture.check(receipt).returncode, 0)
        self.assertEqual(original, tree_snapshot(self.fixture.site))
        self.assert_rejected(self.fixture.check(receipt, source=False))
        source = self.fixture.site / "notebook.html"
        original_bytes = source.read_bytes()
        source.write_bytes(original_bytes + b"<!-- later edit -->")
        changed = tree_snapshot(self.fixture.site)
        self.assert_rejected(self.fixture.check(receipt))
        self.assertEqual(changed, tree_snapshot(self.fixture.site))
        source.unlink()
        self.assert_rejected(self.fixture.check(receipt))
        outside = self.fixture.root / "outside.html"
        outside.write_bytes(original_bytes)
        source.symlink_to(outside)
        self.assert_rejected(self.fixture.check(receipt))
        self.assertEqual(outside.read_bytes(), original_bytes)

    def test_artifact_content_tampering_invalidates_its_identity(self):
        self.build()
        receipt = self.fixture.receipt(["P1"], "apply-selected")
        original = self.fixture.review.read_text(encoding="utf-8")
        changed = original.replace("Compare focused changes using synthetic local captures.",
                                   "Content changed after review identity was generated.")
        self.assertNotEqual(original, changed)
        tampered = self.fixture.root / "tampered.html"
        tampered.write_text(changed, encoding="utf-8")
        self.assert_rejected(self.fixture.check(receipt, review=tampered))

    def test_feedback_allows_constraints_but_apply_and_retain_enforce_them(self):
        self.build()
        for selected in [["P3"], ["P1", "P4"], ["P1", "P1-B"], ["P1", "P3"]]:
            with self.subTest(selected=selected):
                feedback = self.fixture.receipt(selected, "review-feedback", "P1")
                self.assertEqual(self.fixture.check(feedback).returncode, 0)
                feedback["intent"] = "apply-selected"
                self.assert_rejected(self.fixture.check(feedback))
        self.assertEqual(self.fixture.check(self.fixture.receipt([], "retain-original")).returncode, 0)
        self.assert_rejected(self.fixture.check(self.fixture.receipt(["P1"], "retain-original")))

    def test_incomplete_evidence_and_final_stages_cannot_authorize_apply(self):
        variants = {}
        for kind in ["missing-baseline", "missing-result", "concept", "no-source", "applied", "retained"]:
            manifest = copy.deepcopy(self.fixture.manifest)
            if kind == "missing-baseline":
                manifest["views"][1]["before"] = None
            elif kind == "missing-result":
                manifest["proposals"][0]["captures"]["phone"] = None
            elif kind == "concept":
                manifest["proposals"][0]["evidence"] = "concept"
            elif kind == "no-source":
                manifest["baseline"]["files"] = {}
            elif kind == "applied":
                manifest.update({"stage": "applied", "applied": ["P1"]})
            else:
                manifest["stage"] = "retained"
            variants[kind] = manifest
        for kind, manifest in variants.items():
            with self.subTest(kind=kind):
                self.build(manifest)
                self.assert_rejected(self.fixture.check(self.fixture.receipt(["P1"], "apply-selected")))
                self.assertEqual(self.fixture.check(self.fixture.receipt(["P1"], "review-feedback")).returncode, 0)
        empty = copy.deepcopy(self.fixture.manifest)
        empty["proposals"] = []
        empty["combinations"] = []
        self.build(empty)
        self.assertEqual(self.fixture.check(self.fixture.receipt([], "retain-original")).returncode, 0)
        feedback = self.fixture.receipt([], "review-feedback")
        feedback["review_note"] = "Keep the current design; revisit after new content."
        self.assertEqual(self.fixture.check(feedback).returncode, 0)
        for malformed in [None, 7]:
            receipt = copy.deepcopy(feedback)
            if malformed is None:
                receipt.pop("review_note")
            else:
                receipt["review_note"] = malformed
            with self.subTest(no_change_review_note=malformed):
                self.assert_rejected(self.fixture.check(receipt))

    def test_legacy_optional_absence_and_original_artifact_fingerprint(self):
        current = self.build()
        self.assertNotIn("components", current)
        for view in current["views"]:
            self.assertNotIn("regions", view)
        for item in current["proposals"] + current["combinations"]:
            self.assertNotIn("components", item)
            self.assertNotIn("regions", item)
        legacy, original = self.fixture.write_legacy_artifact()
        receipt = self.fixture.receipt(["P1"], "apply-selected", data=original)
        self.assertNotEqual(current["review_fingerprint"], original["review_fingerprint"])
        result = self.fixture.check(receipt, review=legacy)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assert_rejected(self.fixture.check(receipt))
        legacy.write_text(legacy.read_text(encoding="utf-8").replace(
            "Legacy review fixture", "Changed legacy viewer"), encoding="utf-8")
        self.assert_rejected(self.fixture.check(receipt, review=legacy))

    def test_component_normalization_sparse_null_and_separate_namespaces(self):
        manifest = self.fixture.with_components()
        manifest["components"].extend([{"id": "P1", "label": "An independently named component"},
                                       {"id": "desktop", "label": "View-name component"}])
        manifest["views"][0]["regions"]["intro"] = {
            "x": 0.25, "y": 0.75, "width": 200.5, "height": 120.25}
        manifest["views"][1]["regions"] = {"intro": None}
        manifest["proposals"][0]["regions"] = {"desktop": {"record": None}}
        manifest["proposals"][1].pop("regions")
        manifest["proposals"][2]["regions"] = {}
        manifest["combinations"][0]["regions"] = {"phone": {"list": None}}
        data = self.build(manifest)
        self.assertEqual(data["components"], manifest["components"])
        for original, normalized in zip(manifest["views"], data["views"]):
            self.assertEqual(original["regions"], normalized["regions"])
        for original, normalized in zip(manifest["proposals"], data["proposals"]):
            self.assertEqual(original["components"], normalized["components"])
            self.assertEqual("regions" in original, "regions" in normalized)
            if "regions" in original:
                self.assertEqual(original["regions"], normalized["regions"])
        self.assertEqual(data["combinations"][0]["regions"], manifest["combinations"][0]["regions"])
        # Sparse crop evidence does not change the valid full-screen application.
        receipt = self.fixture.receipt(["P1", "P2"], "apply-selected", "C12")
        result = self.fixture.check(receipt)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(set(receipt), {"format", "version", "review_id", "round", "review_fingerprint",
                                       "intent", "preview_id", "selected", "review_note", "decisions", "exported_at"})
        empty = copy.deepcopy(self.fixture.manifest)
        empty["components"] = []
        empty["views"][0]["regions"] = {}
        empty["proposals"][0]["components"] = []
        empty["proposals"][0]["regions"] = {}
        empty["combinations"][0]["regions"] = {}
        self.assertEqual(self.build(empty)["components"], [])
        absent_capture = copy.deepcopy(manifest)
        absent_capture["views"][1]["before"] = None
        absent_capture["proposals"][0]["captures"]["phone"] = None
        absent_capture["proposals"][0]["regions"]["phone"] = {"intro": None}
        absent_capture["combinations"][0]["captures"]["phone"] = None
        self.build(absent_capture)

    def test_component_scopes_and_region_keys_are_validated(self):
        base = self.fixture.with_components()
        cases = {}

        def changed(label, change):
            manifest = copy.deepcopy(base)
            change(manifest)
            cases[label] = manifest

        changed("components must be array", lambda m: m.update({"components": {"intro": "Introduction"}}))
        changed("null components", lambda m: m.update({"components": None}))
        changed("component must be object", lambda m: m["components"].append("intro"))
        changed("component missing ID", lambda m: m["components"][0].pop("id"))
        changed("empty component ID", lambda m: m["components"][0].update({"id": ""}))
        changed("non-ASCII component ID", lambda m: m["components"][0].update({"id": "소개"}))
        changed("boolean component ID", lambda m: m["components"][0].update({"id": True}))
        changed("duplicate component ID", lambda m: m["components"].append(copy.deepcopy(m["components"][0])))
        changed("missing component label", lambda m: m["components"][0].pop("label"))
        changed("empty component label", lambda m: m["components"][0].update({"label": ""}))
        changed("nonstring component label", lambda m: m["components"][0].update({"label": 7}))
        changed("unknown component field", lambda m: m["components"][0].update({"extra": True}))
        changed("proposal components must be array", lambda m: m["proposals"][0].update({"components": "intro"}))
        changed("null proposal components", lambda m: m["proposals"][0].update({"components": None}))
        changed("duplicate proposal component", lambda m: m["proposals"][0].update({"components": ["intro", "intro"]}))
        changed("unknown proposal component", lambda m: m["proposals"][0].update({"components": ["unknown"]}))
        changed("undeclared global components", lambda m: m.pop("components"))
        changed("baseline regions must be object", lambda m: m["views"][0].update({"regions": []}))
        changed("null baseline regions", lambda m: m["views"][0].update({"regions": None}))
        changed("unknown baseline component", lambda m: m["views"][0]["regions"].update({"unknown": None}))
        changed("proposal regions must be object", lambda m: m["proposals"][0].update({"regions": []}))
        changed("null proposal regions", lambda m: m["proposals"][0].update({"regions": None}))
        changed("proposal view map must be object", lambda m: m["proposals"][0]["regions"].update({"desktop": []}))
        changed("null proposal view map", lambda m: m["proposals"][0]["regions"].update({"desktop": None}))
        changed("unknown proposal view", lambda m: m["proposals"][0]["regions"].update({"tablet": {}}))
        changed("unknown proposal region component", lambda m: m["proposals"][0]["regions"]["desktop"].update({"unknown": None}))
        changed("proposal component outside scope", lambda m: m["proposals"][0]["regions"]["desktop"].update({"list": None}))
        changed("proposal region without declared scope", lambda m: m["proposals"][0].pop("components"))
        changed("proposal region with empty scope", lambda m: m["proposals"][0].update({"components": []}))
        changed("combination regions must be object", lambda m: m["combinations"][0].update({"regions": []}))
        changed("null combination regions", lambda m: m["combinations"][0].update({"regions": None}))
        changed("null combination view map", lambda m: m["combinations"][0]["regions"].update({"desktop": None}))
        changed("unknown combination view", lambda m: m["combinations"][0]["regions"].update({"tablet": {}}))
        changed("unknown combination component", lambda m: m["combinations"][0]["regions"]["desktop"].update({"unknown": None}))
        changed("combination component outside union", lambda m: m["combinations"][0]["regions"]["desktop"].update({"footer": None}))
        for label, manifest in cases.items():
            with self.subTest(label=label):
                self.assert_rejected(self.fixture.build(manifest))

    def test_component_rectangles_and_corresponding_captures_are_validated(self):
        base = self.fixture.with_components()
        invalid = [[], "rect", {}, {"x": 0, "y": 0, "width": 2},
                   {"x": 0, "y": 0, "width": 2, "height": 2, "extra": 0}]
        for field in ["x", "y", "width", "height"]:
            for value in [True, False, None, "1", float("nan"), float("inf"), float("-inf")]:
                rect = {"x": 1, "y": 1, "width": 50, "height": 50}
                rect[field] = value
                invalid.append(rect)
        for field, value in [("x", -0.01), ("y", -0.01), ("width", 0), ("height", 0),
                             ("width", -1), ("height", -1), ("width", 960), ("height", 720)]:
            rect = {"x": 1, "y": 1, "width": 50, "height": 50}
            rect[field] = value
            invalid.append(rect)
        for rect in invalid:
            for location in ["baseline", "proposal", "combination"]:
                with self.subTest(rect=rect, location=location):
                    manifest = copy.deepcopy(base)
                    regions = (manifest["views"][0]["regions"] if location == "baseline" else
                               manifest["proposals" if location == "proposal" else "combinations"][0]
                               ["regions"]["desktop"])
                    regions["intro"] = rect
                    self.assert_rejected(self.fixture.build(manifest))
        for location in ["baseline", "proposal", "combination"]:
            with self.subTest(missing_capture=location):
                manifest = copy.deepcopy(base)
                if location == "baseline":
                    manifest["views"][0]["before"] = None
                else:
                    manifest["proposals" if location == "proposal" else "combinations"][0]["captures"]["desktop"] = None
                self.assert_rejected(self.fixture.build(manifest))

    def test_component_bounds_use_actual_png_height_and_allow_exact_edges(self):
        manifest = self.fixture.with_components()
        edge = {"x": 0, "y": 1000, "width": 960, "height": 100}
        for filename in ["before-desktop.png", "P1-desktop.png", "combined-desktop.png"]:
            (self.fixture.root / filename).write_bytes(png_bytes(960, 1100, (60, 80, 100)))
        manifest["views"][0]["regions"]["intro"] = copy.deepcopy(edge)
        manifest["proposals"][0]["regions"]["desktop"]["intro"] = copy.deepcopy(edge)
        manifest["combinations"][0]["regions"]["desktop"]["intro"] = copy.deepcopy(edge)
        data = self.build(manifest)
        self.assertEqual(data["views"][0]["height"], 720)
        self.assertEqual(data["views"][0]["regions"]["intro"], edge)
        for location in ["baseline", "proposal", "combination"]:
            for field in ["width", "height"]:
                with self.subTest(location=location, overflow=field):
                    invalid = copy.deepcopy(manifest)
                    regions = (invalid["views"][0]["regions"] if location == "baseline" else
                               invalid["proposals" if location == "proposal" else "combinations"][0]
                               ["regions"]["desktop"])
                    regions["intro"][field] += 0.01
                    self.assert_rejected(self.fixture.build(invalid))


@unittest.skipUnless(RUN_BROWSER, "Add --browser to run actual local-browser interactions")
class BrowserReviewTests(unittest.TestCase):
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
        self.fixture = Fixture(self._testMethodName)
        self.original_source = tree_snapshot(self.fixture.site)
        self.context = self.browser.new_context(viewport={"width": 1440, "height": 1000}, accept_downloads=True)
        self.context.set_default_timeout(7000)
        self.page = self.context.new_page()
        self.network = []
        self.page.on("request", lambda request: self.network.append(request.url)
                     if re.match(r"https?://", request.url) else None)
        self.export_number = 0

    def tearDown(self):
        try:
            self.assertEqual(self.network, [], "The local viewer made external network requests")
            self.assertEqual(self.original_source, tree_snapshot(self.fixture.site), "Viewer changed source files")
        finally:
            self.context.close()
            self.fixture.close()

    def load(self, manifest=None):
        result = self.fixture.build(manifest)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.data = embedded_data(self.fixture.review)
        self.page.goto(self.fixture.review.as_uri())
        self.page.wait_for_function("() => document.readyState === 'complete'")

    # These adapters are intentionally separate from the contract assertions.
    # They bind the public controls to the implementation's accessible DOM.
    def proposal(self, identifier):
        return self.page.locator('button[data-action="preview"][data-proposal-id="' + identifier + '"]')

    def status_button(self, identifier, status):
        action = "reset" if status == "pending" else status
        return self.page.locator('button[data-action="' + action + '"][data-proposal-id="' + identifier + '"]')

    def choose(self, identifier, status):
        if status in {"defer", "pending"}:
            self.proposal(identifier).click()
        self.status_button(identifier, status).click()

    def action(self, intent):
        return self.page.locator("#" + intent)

    def open_details(self, selector):
        details = self.page.locator(selector)
        if not details.evaluate("element => element.open"):
            details.locator(":scope > summary").click()

    def overall_note(self):
        self.open_details("#overall-feedback")
        return self.page.locator("#review-note")

    def review_details(self):
        self.page.locator("#show-help").click()
        self.open_details("#help-dialog details")

    def handoff(self, intent="review-feedback"):
        if not self.page.locator("#export-dialog").is_visible():
            self.page.locator("#open-handoff").click()
        self.action(intent).click()
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

    def images(self):
        return self.page.locator("#before-image"), self.page.locator("#after-image")

    def panes(self):
        return self.page.locator("#before-pane"), self.page.locator("#after-pane")

    def selection(self):
        self.page.locator("#integrated-comparison").click()

    def component(self, identifier):
        self.page.locator("#focus-component").click()
        self.page.locator("#component-select").select_option(identifier)
        self.wait_images()

    def component_ids(self):
        return self.page.locator("#component-select option").evaluate_all(
            "options => options.map(option => option.value)")

    def crop_geometry(self, side):
        return self.page.evaluate("""side => {
            const clip = document.getElementById(`${side}-clip`);
            const image = document.getElementById(`${side}-image`);
            const viewport = document.getElementById(`${side}-viewport`);
            const style = getComputedStyle(viewport);
            const bounds = element => {
                const {x, y, width, height} = element.getBoundingClientRect();
                return {x, y, width, height};
            };
            return {clip: bounds(clip), image: bounds(image),
                natural: {width: image.naturalWidth, height: image.naturalHeight},
                overflow: [getComputedStyle(clip).overflowX, getComputedStyle(clip).overflowY],
                available: viewport.clientWidth - parseFloat(style.paddingLeft) - parseFloat(style.paddingRight),
                viewportWidth: viewport.clientWidth, viewportHeight: viewport.clientHeight,
                scrollWidth: viewport.scrollWidth, scrollHeight: viewport.scrollHeight};
        }""", side)

    def assert_crop_pair(self, before, after, zoom="fit"):
        from playwright.sync_api import expect
        # Decoding can finish before the viewer's async load handler unhides
        # the pair. Geometry assertions require the displayed comparison.
        for image in self.images():
            expect(image).to_be_visible()
        geometry = [self.crop_geometry(side) for side in ["before", "after"]]
        scale = 1 if zoom == "actual" else min(
            min(item["available"] for item in geometry) / max(before["width"], after["width"]), 1)
        for side, region, item in zip(["before", "after"], [before, after], geometry):
            with self.subTest(side=side, region=region, zoom=zoom):
                clip, image = item["clip"], item["image"]
                self.assertTrue(all(value in {"hidden", "clip"} for value in item["overflow"]),
                                "The measured region requires a real clipping wrapper")
                self.assertAlmostEqual(image["width"] / item["natural"]["width"], scale, delta=0.002)
                self.assertAlmostEqual(image["height"] / item["natural"]["height"], scale, delta=0.002)
                self.assertAlmostEqual(clip["width"], region["width"] * scale, delta=0.6)
                self.assertAlmostEqual(clip["height"], region["height"] * scale, delta=0.6)
                self.assertAlmostEqual(image["x"] - clip["x"], -region["x"] * scale, delta=0.6)
                self.assertAlmostEqual(image["y"] - clip["y"], -region["y"] * scale, delta=0.6)
                if zoom == "actual" and clip["width"] > item["viewportWidth"]:
                    self.assertGreater(item["scrollWidth"], item["viewportWidth"])
                if zoom == "actual" and clip["height"] > item["viewportHeight"]:
                    self.assertGreater(item["scrollHeight"], item["viewportHeight"])
        return geometry

    def assert_crop_pixels(self, side, color):
        screenshot = self.page.locator("#" + side + "-clip").screenshot(scale="css")
        uri = "data:image/png;base64," + base64.b64encode(screenshot).decode("ascii")
        # Fractional CSS crop edges are antialiased when Chrome downsamples the
        # source. Probe inside that boundary; assert_crop_pair checks the exact
        # clipping bounds, scale, and origin separately.
        pixels = self.page.evaluate("""async uri => {
            const image = new Image(); image.src = uri; await image.decode();
            const canvas = document.createElement('canvas');
            canvas.width = image.naturalWidth; canvas.height = image.naturalHeight;
            const context = canvas.getContext('2d'); context.drawImage(image, 0, 0);
            const xs = [3, Math.floor(canvas.width / 2), canvas.width - 4];
            const ys = [3, Math.floor(canvas.height / 2), canvas.height - 4];
            return ys.flatMap(y => xs.map(x => [...context.getImageData(x, y, 1, 1).data]));
        }""", uri)
        for pixel in pixels:
            self.assertTrue(all(abs(actual - expected) <= 1 for actual, expected in zip(pixel, color)),
                            "Crop contains pixels outside its measured component: " + str(pixel))
            self.assertEqual(pixel[3], 255)

    def wait_images(self):
        self.page.wait_for_function("""() => [...document.images].every(image =>
            image.complete || !image.getAttribute('src'))""")
        self.page.evaluate("""async () => {
            await Promise.allSettled([...document.images].map(image => image.decode()));
            await new Promise(requestAnimationFrame);
        }""")

    def assert_apply(self, enabled):
        from playwright.sync_api import expect
        if enabled:
            expect(self.action("apply-selected")).to_be_enabled()
        else:
            expect(self.action("apply-selected")).to_be_disabled()

    def test_initial_pair_view_zoom_and_phone_layout(self):
        self.load()
        self.wait_images()
        self.assert_apply(False)
        self.assertTrue(self.action("retain-original").is_enabled())
        self.assertEqual(self.export()["selected"], [])
        self.selection()
        self.wait_images()
        for width, height in [(1440, 1000), (390, 844)]:
            with self.subTest(viewport=(width, height)):
                self.page.set_viewport_size({"width": width, "height": height})
                self.wait_images()
                before, after = self.panes()
                boxes = [before.bounding_box(), after.bounding_box()]
                self.assertTrue(all(boxes), "Both comparison panes must be visible")
                left, right = boxes
                self.assertLess(left["x"], right["x"])
                self.assertLessEqual(left["x"] + left["width"], right["x"] + 2)
                self.assertLess(abs(left["y"] - right["y"]), 4, "Phone panes must stay side by side")
                self.assertGreater(left["height"], 60)
                self.assertGreater(right["height"], 60)
                self.assertLess(left["y"], height)
                images = self.images()
                scales = [image.evaluate("image => image.getBoundingClientRect().width / image.naturalWidth")
                          for image in images]
                self.assertAlmostEqual(scales[0], scales[1], places=3)
                self.assertEqual(images[0].get_attribute("src"), images[1].get_attribute("src"))
                self.page.screenshot(path=str(self.fixture.root / ("pair-" + str(width) + ".png")))
        self.page.locator("#view-select").select_option("phone")
        self.wait_images()
        self.assertEqual(self.images()[0].evaluate("image => image.naturalWidth"), 390)
        self.review_details()
        body = self.page.locator("#help-dialog").inner_text()
        self.assertIn("390", body)
        self.assertIn("844", body)
        self.page.locator("#close-help").click()
        self.page.locator("#zoom-actual").click()
        self.assertAlmostEqual(self.images()[0].evaluate(
            "image => image.getBoundingClientRect().width / image.naturalWidth"), 1, places=3)
        self.open_details("details.viewer-more")
        self.page.locator("#linked-scroll").check()
        self.page.locator("details.viewer-more > summary").click()
        self.page.locator("#before-viewport").evaluate(
            "element => { element.scrollTop = 100; element.scrollLeft = 80; }")
        self.page.wait_for_function("""() => {
            const after = document.querySelector('#after-viewport');
            return after.scrollTop > 0 && after.scrollLeft > 0;
        }""")
        self.page.locator("#zoom-fit").click()
        self.assertLess(self.images()[0].evaluate(
            "image => image.getBoundingClientRect().width / image.naturalWidth"), 1)

    def test_phone_choice_controls_are_reachable(self):
        self.load()
        for width, height in [(390, 844), (320, 568)]:
            with self.subTest(viewport=(width, height)):
                self.page.set_viewport_size({"width": width, "height": height})
                self.wait_images()
                self.proposal("P4").click(timeout=4000)
                self.status_button("P4", "accept").click(timeout=4000)
                self.page.screenshot(path=str(self.fixture.root / ("controls-" + str(width) + ".png")))
                geometry = {"after_option": [pane.bounding_box() for pane in self.panes()]}
                # Mobile choices may be below the paired viewer. Returning to
                # the comparison must permit both panes to be viewed together.
                self.selection()
                self.wait_images()
                self.page.screenshot(path=str(self.fixture.root / ("selection-" + str(width) + ".png")))
                geometry["after_view_selection"] = [pane.bounding_box() for pane in self.panes()]
                (self.fixture.root / ("geometry-" + str(width) + ".json")).write_text(
                    json.dumps(geometry, indent=2), encoding="utf-8")
                for pane in self.panes():
                    box = pane.bounding_box()
                    self.assertGreater(min(box["y"] + box["height"], height) - max(box["y"], 0), 0,
                                       "Comparison pane unavailable after returning to viewer: " + str(box))
                before, after = geometry["after_view_selection"]
                self.assertLess(abs(before["y"] - after["y"]), 4)
                self.assertLessEqual(before["x"] + before["width"], after["x"] + 2)
                self.assertEqual(self.export()["selected"], ["P4"])
                self.choose("P4", "pending")
                self.assertEqual(self.export()["selected"], [])

    def test_status_controls_notes_keyboard_and_exclusive_alternatives(self):
        self.load()
        self.proposal("P1").click()
        self.wait_images()
        self.assertEqual(self.images()[1].get_attribute("src"), self.data["proposals"][0]["captures"]["desktop"])
        self.assertEqual(self.export()["selected"], [])
        self.choose("P1", "accept")
        self.assertEqual(self.export()["selected"], ["P1"])
        self.assertEqual(self.status_button("P1", "accept").get_attribute("aria-pressed"), "true")
        self.choose("P1", "accept")
        self.assertEqual(self.export()["decisions"]["P1"]["status"], "pending")
        self.assertEqual(self.status_button("P1", "accept").get_attribute("aria-pressed"), "false")
        for status in ["revise", "reject", "defer", "pending"]:
            self.choose("P1", status)
            self.assertEqual(self.export()["decisions"]["P1"]["status"], status)
        self.choose("P1", "accept")
        self.choose("P1-B", "accept")
        receipt = self.export()
        self.assertEqual(receipt["selected"], ["P1-B"])
        self.assertEqual(receipt["decisions"]["P1"]["status"], "pending")
        self.assertIn("Header option", self.page.locator("#notice").inner_text())
        self.proposal("P1-B").click()
        self.page.locator("#feedback-note").fill("Keep the accent. <literal feedback>")
        self.assertEqual(self.export()["decisions"]["P1-B"]["note"], "Keep the accent. <literal feedback>")
        accept = self.status_button("P2", "accept")
        accept.focus()
        accept.press("Space")
        self.assertTrue(accept.evaluate("""element => {
            const style = getComputedStyle(element);
            return element.matches(':focus-visible') &&
                ((style.outlineStyle !== 'none' && parseFloat(style.outlineWidth) > 0)
                 || style.boxShadow !== 'none');
        }"""), "Keyboard focus must have a visible indicator")
        self.assertIn("P2", self.export()["selected"])

    def test_exact_selected_combination_and_readiness_invalidation(self):
        self.load()
        self.choose("P1", "accept")
        self.selection()
        self.wait_images()
        self.assert_apply(True)
        self.choose("P2", "accept")
        self.assert_apply(False)
        self.selection()
        self.wait_images()
        self.assert_apply(True)
        self.assertEqual(self.images()[1].get_attribute("src"), self.data["combinations"][0]["captures"]["desktop"])
        receipt = self.export("apply-selected")
        self.assertEqual(set(receipt["selected"]), {"P1", "P2"})
        self.assertEqual(receipt["preview_id"], "C12")
        result = self.fixture.check(receipt)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.proposal("P1").click()
        self.wait_images()
        self.assert_apply(False)
        self.assertEqual(self.images()[1].get_attribute("src"), self.data["proposals"][0]["captures"]["desktop"])
        self.selection()
        self.wait_images()
        self.assert_apply(True)

    def test_requirements_conflicts_and_missing_combination_keep_feedback_available(self):
        self.load()
        self.choose("P3", "accept")
        self.selection()
        self.assert_apply(False)
        receipt = self.export()
        self.assertEqual(receipt["selected"], ["P3"], "A dependency must never be auto-accepted")
        self.assertIn("Header option", self.page.locator("#constraints").inner_text())
        self.assertEqual(self.fixture.check(receipt).returncode, 0)
        self.choose("P1", "accept")
        self.selection()
        self.wait_images()
        self.assert_apply(False)
        receipt = self.export()
        self.assertEqual(set(receipt["selected"]), {"P1", "P3"})
        self.assertNotEqual(receipt["preview_id"], "C12")
        self.assertFalse(self.images()[1].is_visible(), "A member image cannot stand in for the exact combination")
        self.assertTrue(self.page.locator("#after-empty").is_visible())
        self.assertTrue(self.page.locator("#preview-notice").is_visible())
        self.assertRegex(self.page.locator("#preview-notice").inner_text(), r"(?i)(no|missing|unavailable).*(combined|combination)")
        self.assertEqual(self.fixture.check(receipt).returncode, 0)
        self.choose("P3", "pending")
        self.choose("P4", "accept")
        self.selection()
        self.assert_apply(False)
        receipt = self.export()
        self.assertEqual(set(receipt["selected"]), {"P1", "P4"})
        diagnostic = self.page.locator("#constraints").inner_text()
        self.assertIn("Header option", diagnostic)
        self.assertIn("Conflicting layout", diagnostic)
        self.assertEqual(self.fixture.check(receipt).returncode, 0)

    def test_missing_evidence_and_image_decode_failure_block_apply(self):
        for kind in ["missing-baseline", "missing-result", "concept", "no-source"]:
            with self.subTest(evidence=kind):
                manifest = copy.deepcopy(self.fixture.manifest)
                if kind == "missing-baseline":
                    manifest["views"][1]["before"] = None
                elif kind == "missing-result":
                    manifest["proposals"][0]["captures"]["phone"] = None
                elif kind == "concept":
                    manifest["proposals"][0]["evidence"] = "concept"
                else:
                    manifest["baseline"]["files"] = {}
                self.load(manifest)
                self.choose("P1", "accept")
                self.selection()
                self.wait_images()
                self.assert_apply(False)
                self.assertEqual(self.export()["selected"], ["P1"])
                if kind in ["missing-baseline", "missing-result"]:
                    self.page.locator("#view-select").select_option("phone")
                    self.wait_images()
                    side = "before" if kind == "missing-baseline" else "after"
                    self.assertFalse(self.page.locator("#" + side + "-image").is_visible())
                    self.assertTrue(self.page.locator("#" + side + "-empty").is_visible())
                    self.assertTrue(self.page.locator("#" + side + "-empty").inner_text().strip())
        self.load()
        self.choose("P1", "accept")
        self.selection()
        self.wait_images()
        self.assert_apply(True)
        self.images()[1].evaluate("image => { image.src = 'data:image/png;base64,AA=='; }")
        self.wait_images()
        self.assert_apply(False)
        self.assertEqual(self.export()["selected"], ["P1"])

    def test_import_validation_and_fingerprint_scoped_drafts(self):
        self.load()
        self.choose("P1", "accept")
        self.page.locator("#feedback-note").fill("Imported note")
        self.overall_note().fill("Review the overall balance after the header change.")
        expected = self.export()
        fingerprint = expected["review_fingerprint"]
        keys = self.page.evaluate("Object.keys(localStorage)")
        self.assertTrue(any(fingerprint in key for key in keys))
        self.page.reload()
        reloaded = self.export()
        self.assertEqual(reloaded["decisions"], expected["decisions"])
        self.assertEqual(reloaded["review_note"], expected["review_note"])
        self.choose("P1", "pending")
        import_path = self.fixture.root / "import.json"
        import_path.write_text(json.dumps(expected), encoding="utf-8")
        self.page.locator('input[type="file"]').set_input_files(str(import_path))
        self.assertEqual(self.export()["decisions"], expected["decisions"])
        mutations = {
            "another fingerprint": lambda r: r.update({"review_fingerprint": "0" * 64}),
            "another round": lambda r: r.update({"round": r["round"] + 1}),
            "unknown option": lambda r: r["decisions"].update({"unknown": {"status": "accept", "note": ""}}),
        }
        for label, change in mutations.items():
            with self.subTest(import_case=label):
                invalid = copy.deepcopy(expected)
                change(invalid)
                import_path.write_text(json.dumps(invalid), encoding="utf-8")
                self.page.locator('input[type="file"]').set_input_files(str(import_path))
                unchanged = self.export()
                self.assertEqual(unchanged["decisions"], expected["decisions"])
                self.assertEqual(unchanged["review_note"], expected["review_note"])
        other = copy.deepcopy(self.fixture.manifest)
        other["title"] = "A separate artifact with changed content"
        self.load(other)
        self.assertNotEqual(self.data["review_fingerprint"], fingerprint)
        fresh = self.export()
        self.assertEqual(fresh["selected"], [])
        self.assertEqual(fresh["review_note"], "")

    def test_no_change_global_feedback_export_import_reload_and_validation(self):
        from playwright.sync_api import expect
        manifest = copy.deepcopy(self.fixture.manifest)
        manifest["proposals"] = []
        manifest["combinations"] = []
        self.load(manifest)
        note = self.overall_note()
        self.assertTrue(note.is_visible())
        self.assertTrue(note.evaluate(
            "element => [...element.labels].some(label => label.textContent.trim())"))
        text = "Keep the original. 원본 유지.\nRevisit after new content <literal feedback>."
        note.fill(text)
        for intent in ["review-feedback", "retain-original"]:
            receipt = self.export(intent)
            self.assertEqual(receipt["intent"], intent)
            self.assertEqual(receipt["review_note"], text)
            self.assertEqual(receipt["selected"], [])
            self.assertEqual(receipt["decisions"], {})
            result = self.fixture.check(receipt)
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.page.reload()
        expect(note).to_have_value(text)
        self.assertEqual(self.export()["review_note"], text)
        import_path = self.fixture.root / "global-feedback-import.json"
        valid = self.export("review-feedback")
        for malformed in [None, 7]:
            with self.subTest(review_note=malformed):
                self.overall_note().fill("An unsent local edit that import should replace.")
                import_path.write_text(json.dumps(valid), encoding="utf-8")
                self.page.locator("#import-file").set_input_files(str(import_path))
                expect(note).to_have_value(text)
                expect(self.page.locator("#notice")).to_contain_text(re.compile(r"imported", re.I))
                invalid = copy.deepcopy(valid)
                if malformed is None:
                    invalid.pop("review_note")
                else:
                    invalid["review_note"] = malformed
                import_path.write_text(json.dumps(invalid), encoding="utf-8")
                self.page.locator("#import-file").set_input_files(str(import_path))
                expect(self.page.locator("#notice")).to_contain_text(re.compile(r"reject", re.I))
                expect(note).to_have_value(text)
                unchanged = self.export()
                self.assertEqual(unchanged["review_note"], text)
                self.assertEqual(unchanged["decisions"], {})
        self.page.reload()
        expect(note).to_have_value(text)

    def test_storage_and_clipboard_unavailable_use_local_fallbacks(self):
        self.page.add_init_script("""Object.defineProperty(window, 'localStorage', {
            get() { throw new DOMException('Storage unavailable in this test', 'SecurityError'); }
        });
        Object.defineProperty(navigator, 'clipboard', { get() { return undefined; } });""")
        self.load()
        self.choose("P1", "accept")
        self.overall_note().fill("Keep this feedback when browser storage is unavailable.")
        receipt = self.export()
        self.assertEqual(receipt["selected"], ["P1"])
        self.assertEqual(receipt["review_note"], "Keep this feedback when browser storage is unavailable.")
        self.handoff()
        self.open_details("details.export-details")
        self.page.locator("#copy-json").click()
        fields = self.page.locator("textarea:visible").all()
        copies = []
        for field in fields:
            try:
                value = json.loads(field.input_value())
            except ValueError:
                continue
            if isinstance(value, dict) and value.get("format") == "design-deslop-decisions":
                copies.append((field, value))
        self.assertEqual(len(copies), 1, "Copy fallback must expose selectable JSON")
        self.assertEqual(copies[0][1]["selected"], ["P1"])
        self.assertEqual(copies[0][1]["review_note"], receipt["review_note"])
        self.assertFalse(copies[0][0].is_disabled())
        self.assertTrue(copies[0][0].evaluate(
            "element => element.selectionStart === 0 && element.selectionEnd === element.value.length"))

    def test_untrusted_text_is_literal_and_language_follows_manifest(self):
        manifest = copy.deepcopy(self.fixture.manifest)
        attack = '</script><img src="https://invalid.example/leak" onerror="window.injected=1">&'
        manifest["title"] = attack
        manifest["language"] = "ko"
        manifest["proposals"][0]["observation"] = attack
        self.load(manifest)
        self.assertEqual(self.page.locator("html").get_attribute("lang"), "ko")
        self.assertIn(attack, self.page.locator("body").inner_text())
        self.assertIsNone(self.page.evaluate("window.injected"))
        self.assertEqual(self.page.locator('img[src^="https://"]').count(), 0)

    def test_no_change_applied_and_retained_outcomes(self):
        no_change = copy.deepcopy(self.fixture.manifest)
        no_change["proposals"] = []
        no_change["combinations"] = []
        self.load(no_change)
        self.wait_images()
        self.assertEqual(self.images()[0].get_attribute("src"), self.images()[1].get_attribute("src"))
        self.assert_apply(False)
        retained = self.export("retain-original")
        self.assertEqual(retained["selected"], [])
        self.assertEqual(retained["intent"], "retain-original")
        self.assertEqual(self.fixture.check(retained).returncode, 0)
        for stage in ["applied", "retained"]:
            manifest = copy.deepcopy(self.fixture.manifest)
            manifest["stage"] = stage
            manifest["applied"] = ["P1", "P2"] if stage == "applied" else []
            self.load(manifest)
            self.wait_images()
            expected = (self.data["combinations"][0]["captures"]["desktop"] if stage == "applied"
                        else self.data["views"][0]["before"])
            self.assertEqual(self.images()[1].get_attribute("src"), expected)
            self.assert_apply(False)
            for status in ["accept", "revise", "reject", "defer", "pending"]:
                self.assertTrue(self.status_button("P1", status).is_disabled())
            self.assertTrue(self.action("retain-original").is_disabled())
            self.overall_note().fill("Follow-up feedback on the " + stage + " result.")
            feedback = self.export()
            self.assertEqual(feedback["intent"], "review-feedback")
            self.assertEqual(feedback["review_note"], "Follow-up feedback on the " + stage + " result.")
            self.page.reload()
            self.assertEqual(self.page.locator("#review-note").input_value(), feedback["review_note"])

    def test_legacy_review_has_no_artificial_component_controls(self):
        self.load()
        self.wait_images()
        self.assertFalse(self.page.locator("#component-navigation").is_visible())
        self.assertFalse(self.page.locator("#component-select").is_visible())
        self.proposal("P1").click()
        self.choose("P1", "accept")
        self.selection()
        self.wait_images()
        self.assert_apply(True)
        self.assertEqual(self.export("apply-selected")["selected"], ["P1"])

    def test_component_crop_unequal_boxes_shared_scale_pixels_and_phone(self):
        manifest = self.fixture.with_components()
        self.load(manifest)
        self.proposal("P1").click()
        self.wait_images()
        self.assertTrue(self.page.locator("#component-navigation").is_visible())
        selector = self.page.locator("#component-select")
        self.assertEqual(selector.input_value(), "intro")
        self.assertTrue(selector.evaluate(
            "element => Boolean(element.getAttribute('aria-label')?.trim()) || [...element.labels].some(label => label.textContent.trim())"))
        self.assertEqual(self.component_ids(), ["intro", "record"])
        before = manifest["views"][0]["regions"]["intro"]
        after = manifest["proposals"][0]["regions"]["desktop"]["intro"]
        for width, height in [(1440, 1000), (390, 844)]:
            with self.subTest(browser_viewport=(width, height)):
                self.page.set_viewport_size({"width": width, "height": height})
                self.page.locator("#zoom-fit").click()
                self.wait_images()
                self.assert_crop_pair(before, after)
                for side, kind in [("before", "baseline"), ("after", "proposal")]:
                    self.assert_crop_pixels(side, self.fixture.component_colors[kind]["intro"])
                left, right = [pane.bounding_box() for pane in self.panes()]
                self.assertLess(abs(left["y"] - right["y"]), 4)
                self.assertLessEqual(left["x"] + left["width"], right["x"] + 2)
                self.page.locator("#zoom-actual").click()
                self.assert_crop_pair(before, after, zoom="actual")
        self.page.locator("#view-select").select_option("phone")
        self.page.locator("#zoom-fit").click()
        self.wait_images()
        self.assert_crop_pair(manifest["views"][1]["regions"]["intro"],
                              manifest["proposals"][0]["regions"]["phone"]["intro"])
        # A narrow component must not be enlarged above source pixel size.
        self.page.set_viewport_size({"width": 1440, "height": 1000})
        self.selection()
        self.component("footer")
        self.assert_crop_pair(manifest["views"][1]["regions"]["footer"],
                              manifest["views"][1]["regions"]["footer"])

    def test_component_navigation_preserves_proposal_scope_decisions_and_notes(self):
        manifest = self.fixture.with_components()
        self.load(manifest)
        self.proposal("P1").click()
        self.choose("P1", "accept")
        self.page.locator("#feedback-note").fill("Keep both parts of this inseparable proposal.")
        self.overall_note().fill("Review the complete selected change.")
        expected = self.export()
        scope = self.page.locator("#component-scope")
        self.review_details()
        self.assertTrue(scope.is_visible())
        self.assertIn("Introduction", scope.inner_text())
        self.assertIn("Representative note", scope.inner_text())
        self.page.locator("#close-help").click()
        self.component("record")
        self.page.locator("#view-select").select_option("phone")
        self.wait_images()
        self.assertEqual(self.page.locator("#component-select").input_value(), "record")
        self.page.locator("#focus-whole").click()
        self.wait_images()
        self.assertEqual(self.images()[1].get_attribute("src"), self.data["proposals"][0]["captures"]["phone"])
        full = self.crop_geometry("after")
        self.assertAlmostEqual(full["image"]["x"], full["clip"]["x"], delta=0.6)
        self.assertAlmostEqual(full["image"]["y"], full["clip"]["y"], delta=0.6)
        self.component("intro")
        actual = self.export()
        for field in ["decisions", "selected", "review_note", "preview_id"]:
            self.assertEqual(actual[field], expected[field])
        self.assertEqual(actual["selected"], ["P1"])
        self.assertEqual(actual["preview_id"], "P1")
        self.component("record")
        self.proposal("P3").click()
        self.wait_images()
        self.assertEqual(self.page.locator("#component-select").input_value(), "record")
        self.proposal("P1").click()
        self.wait_images()
        self.assertEqual(self.page.locator("#component-select").input_value(), "record",
                         "An available focus should survive comparison of another proposal")
        self.choose("P1-B", "accept")
        self.proposal("P1-B").click()
        self.wait_images()
        self.assertEqual(self.component_ids(), ["intro"])
        alternate = self.export()
        self.assertEqual(alternate["selected"], ["P1-B"])
        self.assertEqual(alternate["decisions"]["P1"]["status"], "pending")
        self.assertEqual(alternate["decisions"]["P1"]["note"], expected["decisions"]["P1"]["note"])

    def test_viewport_missing_region_preserves_focus_and_whole_screen_apply(self):
        base = self.fixture.with_components()
        for missing in ["null", "sparse-component", "sparse-view", "baseline"]:
            with self.subTest(missing_region=missing):
                manifest = copy.deepcopy(base)
                if missing == "null":
                    manifest["proposals"][0]["regions"]["phone"]["record"] = None
                elif missing == "sparse-component":
                    manifest["proposals"][0]["regions"]["phone"].pop("record")
                elif missing == "sparse-view":
                    manifest["proposals"][0]["regions"].pop("phone")
                else:
                    manifest["views"][1]["regions"]["record"] = None
                self.load(manifest)
                self.proposal("P1").click()
                self.choose("P1", "accept")
                self.selection()
                self.component("record")
                self.assert_apply(True)
                self.page.locator("#view-select").select_option("phone")
                self.wait_images()
                self.assertEqual(self.page.locator("#component-select").input_value(), "record")
                self.assert_apply(False)
                side = "before" if missing == "baseline" else "after"
                self.assertFalse(self.page.locator("#" + side + "-image").is_visible())
                empty = self.page.locator("#" + side + "-empty")
                self.assertTrue(empty.is_visible())
                self.assertRegex(empty.inner_text(), r"(?i)(region|component|crop)")
                self.assertEqual(self.export()["selected"], ["P1"])
                self.page.locator("#focus-whole").click()
                self.wait_images()
                self.assertTrue(all(image.is_visible() for image in self.images()))
                self.assert_apply(True)
                receipt = self.export("apply-selected")
                self.assertEqual(receipt["selected"], ["P1"])
                result = self.fixture.check(receipt)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_exact_selection_uses_combination_regions_and_complete_adoption_scope(self):
        manifest = self.fixture.with_components()
        self.load(manifest)
        self.proposal("P1").click()
        self.choose("P1", "accept")
        self.selection()
        self.component("record")
        self.assert_apply(True)
        self.choose("P2", "accept")
        self.assert_apply(False)
        self.selection()
        self.wait_images()
        self.assertEqual(set(self.component_ids()), {"intro", "record", "list"})
        # Accepting P2 enters its individual scope, whose only component is
        # list. Returning to the selection preserves that available focus.
        self.assertEqual(self.page.locator("#component-select").input_value(), "list")
        self.component("record")
        self.assert_crop_pair(manifest["views"][0]["regions"]["record"],
                              manifest["combinations"][0]["regions"]["desktop"]["record"])
        self.assert_crop_pixels("after", self.fixture.component_colors["combination"]["record"])
        self.assertEqual(self.images()[1].get_attribute("src"), self.data["combinations"][0]["captures"]["desktop"])
        summary = self.page.locator("#selection-title")
        self.review_details()
        self.assertTrue(summary.is_visible())
        for title in ["Header option", "List spacing"]:
            self.assertIn(title, summary.inner_text())
        self.page.locator("#close-help").click()
        self.assert_apply(True)
        receipt = self.export("apply-selected")
        self.assertEqual(set(receipt["selected"]), {"P1", "P2"})
        self.assertEqual(receipt["preview_id"], "C12")
        self.assertEqual(self.fixture.check(receipt).returncode, 0)
        self.component("list")
        self.assert_crop_pair(manifest["views"][0]["regions"]["list"],
                              manifest["combinations"][0]["regions"]["desktop"]["list"])
        self.assertEqual(self.export()["decisions"], receipt["decisions"])
        self.proposal("P1").click()
        self.wait_images()
        self.assertEqual(self.page.locator("#component-select").input_value(), "intro")
        self.assertEqual(self.component_ids(), ["intro", "record"])
        self.assert_apply(False)

    def test_missing_combination_does_not_borrow_individual_component_geometry(self):
        manifest = self.fixture.with_components()
        self.load(manifest)
        self.proposal("P1").click()
        self.choose("P1", "accept")
        self.choose("P3", "accept")
        self.selection()
        self.component("record")
        self.assert_apply(False)
        diagnostic = self.page.locator("#preview-notice")
        self.assertTrue(diagnostic.is_visible())
        self.assertRegex(diagnostic.inner_text(), r"(?i)(no|missing|unavailable).*(combined|combination)")
        self.assertFalse(self.images()[1].is_visible(), "An individual crop cannot stand in for a missing combination")
        self.assertTrue(self.page.locator("#after-empty").is_visible())
        receipt = self.export()
        self.assertEqual(set(receipt["selected"]), {"P1", "P3"})
        self.assertNotEqual(receipt["preview_id"], "C12")
        self.assertEqual(self.fixture.check(receipt).returncode, 0)

    def test_combination_sparse_regions_are_not_replaced_by_member_geometry(self):
        manifest = self.fixture.with_components()
        manifest["combinations"][0]["regions"]["desktop"].pop("record")
        self.load(manifest)
        self.proposal("P1").click()
        self.choose("P1", "accept")
        self.choose("P2", "accept")
        self.selection()
        self.component("record")
        self.assert_apply(False)
        self.assertFalse(self.images()[1].is_visible())
        self.assertTrue(self.page.locator("#after-empty").is_visible())
        self.component("intro")
        self.assert_crop_pair(manifest["views"][0]["regions"]["intro"],
                              manifest["combinations"][0]["regions"]["desktop"]["intro"])
        self.assert_apply(True)
        self.component("record")
        self.page.locator("#focus-whole").click()
        self.wait_images()
        self.assert_apply(True)
        self.assertEqual(set(self.export("apply-selected")["selected"]), {"P1", "P2"})

    def test_baseline_retained_and_applied_component_geometry_and_locks(self):
        base = self.fixture.with_components()
        for stage in ["proposal", "retained", "applied"]:
            with self.subTest(stage=stage):
                manifest = copy.deepcopy(base)
                manifest["stage"] = stage
                manifest["applied"] = ["P1", "P2"] if stage == "applied" else []
                self.load(manifest)
                if stage == "proposal":
                    self.selection()
                self.component("record")
                after = (manifest["combinations"][0]["regions"]["desktop"]["record"] if stage == "applied"
                         else manifest["views"][0]["regions"]["record"])
                self.assert_crop_pair(manifest["views"][0]["regions"]["record"], after)
                expected = (self.data["combinations"][0]["captures"]["desktop"] if stage == "applied"
                            else self.data["views"][0]["before"])
                self.assertEqual(self.images()[1].get_attribute("src"), expected)
                self.assert_apply(False)
                if stage != "proposal":
                    for status in ["accept", "revise", "reject", "defer", "pending"]:
                        self.assertTrue(self.status_button("P1", status).is_disabled())
                    self.assertTrue(self.action("retain-original").is_disabled())
                else:
                    self.assertEqual(set(self.component_ids()), {"intro", "record", "list", "footer"})
                    self.assertEqual(self.export()["selected"], [])


if __name__ == "__main__":
    unittest.main(verbosity=2)
