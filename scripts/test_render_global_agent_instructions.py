#!/usr/bin/env python3
"""Tests for policy extraction and generated-bundle freshness checks."""

from __future__ import annotations

import tempfile
import unittest
from contextlib import redirect_stderr, redirect_stdout
from io import StringIO
from pathlib import Path

import render_global_agent_instructions as renderer


class GlobalAgentInstructionsTests(unittest.TestCase):
    def make_sources(self, root: Path) -> None:
        for key, _, relative in renderer.SOURCES:
            path = root / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(
                "# Maintainer policy\n\nNot installed.\n\n"
                f"<!-- ai-assets:{key}:start -->\n"
                f"- {key}: must keep conditions, `literal text`, and exceptions.\n"
                "  - Keep this nested rule.\n"
                f"<!-- ai-assets:{key}:end -->\n\n"
                "## Evidence limits\n\nNot an installed instruction.\n",
                encoding="utf-8",
            )

    def run_main(self, root: Path, *args: str) -> int:
        with redirect_stdout(StringIO()), redirect_stderr(StringIO()):
            return renderer.main(args, root=root)

    def test_bundle_preserves_rules_and_order_without_maintainer_material(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_sources(root)
            rendered = renderer.render(root)

        previous = -1
        for key, title, _ in renderer.SOURCES:
            start = rendered.index(f"<!-- ai-assets:{key}:start -->")
            self.assertGreater(start, previous)
            previous = start
            self.assertIn(f"## {title}\n", rendered)
            self.assertIn(
                f"- {key}: must keep conditions, `literal text`, and exceptions.\n"
                "  - Keep this nested rule.\n",
                rendered,
            )
        self.assertNotIn("Not installed", rendered)
        self.assertNotIn("Evidence limits", rendered)
        self.assertNotIn("Codex adapter", rendered)

    def test_invalid_markers_are_rejected(self) -> None:
        start = "<!-- ai-assets:sample:start -->"
        end = "<!-- ai-assets:sample:end -->"
        invalid = {
            "missing start": f"rules\n{end}",
            "missing end": f"{start}\nrules",
            "duplicate start": f"{start}\n{start}\nrules\n{end}",
            "duplicate end": f"{start}\nrules\n{end}\n{end}",
            "reversed": f"{end}\nrules\n{start}",
            "empty": f"{start}\n \n{end}",
            "nested": f"{start}\n<!-- ai-assets:other:start -->\n{end}",
        }
        for name, text in invalid.items():
            with self.subTest(name=name), self.assertRaises(ValueError):
                renderer.extract_rules(text, "sample", Path("policy.md"))

    def test_check_detects_missing_and_stale_output_without_writing(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_sources(root)
            target = root / renderer.TARGET
            self.assertEqual(self.run_main(root, "--check"), 1)
            self.assertFalse(target.exists())

            target.parent.mkdir(parents=True)
            target.write_text("An older bundle.\n", encoding="utf-8")
            self.assertEqual(self.run_main(root, "--check"), 1)
            self.assertEqual(target.read_text(), "An older bundle.\n")

    def test_generation_and_check_follow_policy_changes(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_sources(root)
            self.assertEqual(self.run_main(root), 0)
            self.assertEqual(self.run_main(root, "--check"), 0)

            source = root / renderer.SOURCES[0][2]
            source.write_text(
                source.read_text().replace("must keep conditions", "must retain conditions"),
                encoding="utf-8",
            )
            self.assertEqual(self.run_main(root, "--check"), 1)
            self.assertEqual(self.run_main(root), 0)
            self.assertEqual(self.run_main(root, "--check"), 0)
            self.assertIn("must retain conditions", (root / renderer.TARGET).read_text())

    def test_invalid_source_does_not_replace_existing_bundle(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_sources(root)
            self.assertEqual(self.run_main(root), 0)
            target = root / renderer.TARGET
            original = target.read_bytes()
            (root / renderer.SOURCES[-1][2]).unlink()
            self.assertEqual(self.run_main(root), 2)
            self.assertEqual(target.read_bytes(), original)

    def test_explanatory_change_does_not_change_runtime_rules(self) -> None:
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            self.make_sources(root)
            original = renderer.render(root)
            source = root / renderer.SOURCES[0][2]
            source.write_text(
                source.read_text().replace("Not installed.", "New maintainer example."),
                encoding="utf-8",
            )
            self.assertEqual(renderer.render(root), original)

    def test_current_repository_bundle_matches_policy_sources(self) -> None:
        target = renderer.REPOSITORY_ROOT / renderer.TARGET
        self.assertEqual(target.read_text(encoding="utf-8"), renderer.render())


if __name__ == "__main__":
    unittest.main()
