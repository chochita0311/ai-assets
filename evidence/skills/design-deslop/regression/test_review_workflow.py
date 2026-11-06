#!/usr/bin/env python3
"""Stdlib regressions for DOM-only evidence and partial-adoption feedback.

Run independently with Python 3.9+. Existing suites supply synthetic fixture
utilities only; no browser or third-party dependency is needed.
DESIGN_DESLOP_TEST_WORK_ROOT chooses the task-owned temporary parent directory.
"""

import copy
import json
import unittest

from test_dom_review import DOMFixture
from test_review_artifact import embedded_data, tree_snapshot


class ReviewWorkflowTests(unittest.TestCase):
    def setUp(self):
        self.fixture = DOMFixture(self._testMethodName)
        self.with_png = self.fixture.with_documents()
        self.manifest = copy.deepcopy(self.with_png)
        for view in self.manifest["views"]:
            view.pop("before")
            view.pop("regions")
        for item in self.manifest["proposals"] + self.manifest["combinations"]:
            item.pop("captures")
            item.pop("regions")

    def tearDown(self):
        self.fixture.close()

    def build(self, manifest=None):
        result = self.fixture.build(self.manifest if manifest is None else manifest)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        return embedded_data(self.fixture.review)

    def assert_rejected(self, result, reason):
        self.assertNotEqual(result.returncode, 0, "Invalid input was accepted: " + result.stdout)
        self.assertIn(reason, result.stderr)

    def assert_ready(self, selected, preview=None, data=None, review=None):
        receipt = self.fixture.receipt(selected, "apply-selected", preview, data)
        result = self.fixture.check(receipt, review=review)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        summary = json.loads(result.stdout)
        self.assertEqual(summary["result"], "application-ready")
        self.assertEqual(summary["selected"], selected)
        self.assertEqual(summary["source_files_checked"], ["notebook.html"])
        return receipt

    def test_dom_only_normalization_and_exact_application_are_read_only(self):
        original = tree_snapshot(self.fixture.site)
        data = self.build()
        for view in data["views"]:
            self.assertIsNone(view["before"])
            self.assertNotIn("regions", view)
            self.assertIn("<!doctype html>", view["document"]["html"])
        for item in data["proposals"] + data["combinations"]:
            self.assertEqual(item["captures"], {"desktop": None, "phone": None})
            self.assertNotIn("regions", item)
        self.assert_ready(["P1"])
        self.assert_ready(["P2", "P1"], "C12")
        self.assertEqual(original, tree_snapshot(self.fixture.site))

    def test_dom_only_applied_manifests_keep_the_exact_outcome_and_stage_lock(self):
        for selected in [["P1"], ["P1", "P2"]]:
            with self.subTest(selected=selected):
                manifest = copy.deepcopy(self.manifest)
                manifest.update({"stage": "applied", "applied": selected})
                data = self.build(manifest)
                self.assertEqual(data["applied"], selected)
                preview = "P1" if len(selected) == 1 else "C12"
                receipt = self.fixture.receipt(selected, "review-feedback", preview)
                result = self.fixture.check(receipt)
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                receipt["intent"] = "apply-selected"
                self.assert_rejected(self.fixture.check(receipt), "only in proposal stage")

    def test_missing_dom_without_png_blocks_apply_and_applied_outcomes(self):
        for side in ["baseline", "proposal", "combination"]:
            for missing in ["absent", "null"]:
                with self.subTest(side=side, missing=missing):
                    manifest = copy.deepcopy(self.manifest)
                    selected, preview = (["P1", "P2"], "C12") if side == "combination" else (["P1"], "P1")
                    if side == "baseline":
                        mapping, key = manifest["views"][1], "document"
                    else:
                        mapping = manifest["proposals" if side == "proposal" else "combinations"][0]["documents"]
                        key = "phone"
                    if missing == "absent":
                        mapping.pop(key)
                    else:
                        mapping[key] = None
                    self.build(manifest)
                    receipt = self.fixture.receipt(selected, "apply-selected", preview)
                    self.assert_rejected(self.fixture.check(receipt), "missing for view phone")
                    receipt["intent"] = "review-feedback"
                    result = self.fixture.check(receipt)
                    self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                    manifest.update({"stage": "applied", "applied": selected})
                    self.assert_rejected(self.fixture.build(manifest), "Invalid applied selection")

    def test_explicit_missing_dom_cannot_be_masked_by_pngs(self):
        for side in ["baseline", "proposal", "combination"]:
            with self.subTest(side=side):
                manifest = copy.deepcopy(self.with_png)
                selected, preview = (["P1", "P2"], "C12") if side == "combination" else (["P1"], "P1")
                if side == "baseline":
                    manifest["views"][1]["document"] = None
                else:
                    manifest["proposals" if side == "proposal" else "combinations"][0]["documents"]["phone"] = None
                self.build(manifest)
                receipt = self.fixture.receipt(selected, "apply-selected", preview)
                self.assert_rejected(self.fixture.check(receipt), "DOM document is missing for view phone")
                manifest.update({"stage": "applied", "applied": selected})
                self.assert_rejected(self.fixture.build(manifest), "DOM document is missing for view phone")

    def test_invalid_dom_cannot_be_masked_by_pngs(self):
        invalid = self.fixture.root / "invalid.html"
        invalid.write_text("<article>An incomplete HTML document</article>", encoding="utf-8")
        for side in ["baseline", "proposal", "combination"]:
            with self.subTest(side=side):
                manifest = copy.deepcopy(self.with_png)
                descriptor = (manifest["views"][1]["document"] if side == "baseline" else
                              manifest["proposals" if side == "proposal" else "combinations"][0]["documents"]["phone"])
                descriptor["html"] = invalid.name
                self.assert_rejected(self.fixture.build(manifest), "complete HTML document")

    def test_mixed_dom_and_legacy_png_evidence_is_resolved_per_side_and_view(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["views"][1].pop("document")
        manifest["views"][1]["before"] = self.fixture.manifest["views"][1]["before"]
        manifest["proposals"][0]["documents"].pop("desktop")
        manifest["proposals"][0]["captures"] = {
            "desktop": self.fixture.manifest["proposals"][0]["captures"]["desktop"], "phone": None}
        self.build(manifest)
        self.assert_ready(["P1"])

    def test_optional_captures_keep_exact_mapping_and_png_region_contracts(self):
        for kind in ["proposals", "combinations"]:
            for captures in [None, {}, {"desktop": None}, {"desktop": None, "phone": None, "extra": None}]:
                with self.subTest(kind=kind, captures=captures):
                    manifest = copy.deepcopy(self.manifest)
                    manifest[kind][0]["captures"] = captures
                    self.assert_rejected(self.fixture.build(manifest), ".captures")
        for side in ["baseline", "proposal", "combination"]:
            with self.subTest(regions_without_png=side):
                manifest = copy.deepcopy(self.manifest)
                if side == "baseline":
                    manifest["views"][0]["regions"] = self.with_png["views"][0]["regions"]
                else:
                    kind = "proposals" if side == "proposal" else "combinations"
                    manifest[kind][0]["regions"] = self.with_png[kind][0]["regions"]
                self.assert_rejected(self.fixture.build(manifest), "requires a corresponding PNG capture")

    def test_dom_does_not_bypass_rendered_evidence_or_exact_combination(self):
        for kind, selected, preview in [("proposals", ["P1"], "P1"), ("combinations", ["P1", "P2"], "C12")]:
            for evidence in ["concept", "unavailable"]:
                with self.subTest(kind=kind, evidence=evidence):
                    manifest = copy.deepcopy(self.manifest)
                    manifest[kind][0]["evidence"] = evidence
                    self.build(manifest)
                    receipt = self.fixture.receipt(selected, "apply-selected", preview)
                    self.assert_rejected(self.fixture.check(receipt), "not rendered evidence")
                    manifest.update({"stage": "applied", "applied": selected})
                    self.assert_rejected(self.fixture.build(manifest), "not rendered evidence")
        self.build()
        for selected, preview in [(["P1", "P2"], "P1"), (["P1", "P3"], "P1")]:
            with self.subTest(selected=selected, preview=preview):
                receipt = self.fixture.receipt(selected, "apply-selected", preview)
                self.assert_rejected(self.fixture.check(receipt), "no exact selected preview")

    def test_dom_application_still_requires_current_source_identity(self):
        manifest = copy.deepcopy(self.manifest)
        manifest["baseline"]["files"] = {}
        self.build(manifest)
        receipt = self.fixture.receipt(["P1"], "apply-selected")
        self.assert_rejected(self.fixture.check(receipt), "requires baseline source file fingerprints")
        self.build()
        receipt = self.fixture.receipt(["P1"], "apply-selected")
        self.assert_rejected(self.fixture.check(receipt, source=False), "requires --source-root")
        source = self.fixture.site / "notebook.html"
        source.write_bytes(source.read_bytes() + b"<!-- changed after review -->")
        changed = tree_snapshot(self.fixture.site)
        self.assert_rejected(self.fixture.check(receipt), "Stale baseline source")
        self.assertEqual(changed, tree_snapshot(self.fixture.site))

    def test_revise_preserves_feedback_without_accepting_the_current_proposal(self):
        self.build()
        receipt = self.fixture.receipt([], "review-feedback", "P2")
        receipt["decisions"]["P2"] = {"status": "revise", "note": "Keep the spacing; restore the section heading."}
        result = self.fixture.check(receipt)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["selected"], [])
        saved = json.loads((self.fixture.root / "decisions.json").read_text(encoding="utf-8"))
        self.assertEqual(saved, receipt)
        receipt["intent"] = "apply-selected"
        self.assert_rejected(self.fixture.check(receipt), "requires a nonempty selection")

    def test_revise_is_excluded_from_the_exact_applied_selection(self):
        self.build()
        receipt = self.fixture.receipt(["P1"], "apply-selected")
        receipt["decisions"]["P2"] = {"status": "revise", "note": "Use only half the proposed spacing."}
        result = self.fixture.check(receipt)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["selected"], ["P1"])
        receipt["preview_id"] = "C12"
        self.assert_rejected(self.fixture.check(receipt), "no exact selected preview")
        receipt["selected"] = ["P1", "P2"]
        for intent in ["apply-selected", "review-feedback"]:
            with self.subTest(intent=intent):
                receipt["intent"] = intent
                self.assert_rejected(self.fixture.check(receipt), "exactly match the accepted decision statuses")

    def test_legacy_png_reviews_and_receipts_remain_application_ready(self):
        self.build(self.fixture.manifest)
        self.assert_ready(["P1"])
        self.assert_ready(["P1", "P2"], "C12")
        legacy, data = self.fixture.write_legacy_artifact()
        self.assert_ready(["P1"], data=data, review=legacy)
        self.assert_ready(["P1", "P2"], "C12", data=data, review=legacy)


if __name__ == "__main__":
    unittest.main()
