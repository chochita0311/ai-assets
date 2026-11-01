"""Selection and string-preservation checks; requires Python 3.11+ for tomllib."""

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import tomllib
import unittest


PACKAGE_DIR = Path(__file__).resolve().parents[1]
SCRIPT = PACKAGE_DIR / "scripts/render_presets.py"
SPEC = importlib.util.spec_from_file_location("render_presets", SCRIPT)
RENDERER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RENDERER)


class RenderPresetsTests(unittest.TestCase):
    def setUp(self):
        temporary = tempfile.TemporaryDirectory(prefix="prompt-presets-test-")
        self.addCleanup(temporary.cleanup)
        self.root = Path(temporary.name)
        self.package = self.root / "package"
        self.package.mkdir()

    def write_catalog(self, entries):
        (self.package / "catalog.json").write_text(json.dumps(entries), encoding="utf-8")

    def test_packaged_sources_round_trip_without_input_changes(self):
        catalog = json.loads((PACKAGE_DIR / "catalog.json").read_text(encoding="utf-8"))
        parsed = tomllib.loads(RENDERER.render_presets(PACKAGE_DIR, []))["tui"]["presets"]
        self.assertEqual(list(parsed), sorted(catalog, key=int))
        for number, entry in catalog.items():
            self.assertEqual(parsed[number]["label"], entry["label"])
            self.assertEqual(
                parsed[number]["input"],
                (PACKAGE_DIR / entry["prompt_file"]).read_bytes().decode("utf-8"),
            )

    def test_future_selection_omits_unrequested_entries_and_deduplicates(self):
        (self.package / "prompt.md").write_text("Shared synthetic input", encoding="utf-8")
        self.write_catalog({
            str(number): {"label": f"Preset {number}", "prompt_file": "prompt.md"}
            for number in range(1, 6)
        })
        parsed = tomllib.loads(
            RENDERER.render_presets(self.package, ["1", "3", "4", "5", "3"])
        )["tui"]["presets"]
        self.assertEqual(list(parsed), ["1", "3", "4", "5"])

    def test_unknown_number_exits_without_partial_output(self):
        result = subprocess.run(
            [sys.executable, str(SCRIPT), "1", "999999"], capture_output=True, check=False
        )
        self.assertEqual(result.returncode, 2)
        self.assertEqual(result.stdout, b"")
        self.assertIn(b"unknown preset numbers: 999999", result.stderr)

    def test_literal_input_round_trips_quotes_newlines_unicode_and_table_text(self):
        text = 'Keep $skill and $(literal) \\path """\r\n[tui.presets.9]\n한글 🐾\x7f\n'
        (self.package / "prompt.md").write_bytes(text.encode("utf-8"))
        label = 'Synthetic "label" 🐾'
        self.write_catalog({"1": {"label": label, "prompt_file": "prompt.md"}})
        parsed = tomllib.loads(RENDERER.render_presets(self.package, []))["tui"]["presets"]
        self.assertEqual(parsed, {"1": {"label": label, "input": text}})

    def test_prompt_path_cannot_escape_package(self):
        (self.root / "outside.md").write_text("Outside source", encoding="utf-8")
        self.write_catalog({"1": {"label": "Outside", "prompt_file": "../outside.md"}})
        with self.assertRaisesRegex(ValueError, "inside this package"):
            RENDERER.render_presets(self.package, [])


if __name__ == "__main__":
    unittest.main()
