import importlib.util
from pathlib import Path
import plistlib
import sys
import tempfile
import unittest
from unittest.mock import patch


SOURCE = Path(__file__).resolve().parents[1] / "render_launch_agent.py"
SPEC = importlib.util.spec_from_file_location("render_launch_agent", SOURCE)
renderer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(renderer)


class RenderTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="reset-agent-test-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        self.monitor = self.root / "monitor with spaces.py"
        self.monitor.write_text("# synthetic monitor\n", encoding="utf-8")
        self.output = self.root / "candidate.plist"
        self.state = self.root / "runtime state"

    def args(self, output=None, state=None):
        return [
            str(SOURCE), "--python", sys.executable, "--monitor", str(self.monitor),
            "--state-dir", str(state or self.state), "--timezone", "Asia/Seoul",
            "--label", "local.example-reset", "--output", str(output or self.output),
        ]

    def test_rendered_job_checks_every_hour_and_preserves_paths(self):
        with patch.object(sys, "argv", self.args()):
            renderer.main()
        with self.output.open("rb") as source:
            job = plistlib.load(source)
        self.assertEqual(job["StartCalendarInterval"], {"Minute": 0})
        self.assertEqual(job["Label"], "local.example-reset")
        self.assertEqual(job["ProgramArguments"], [
            sys.executable, "-B", str(self.monitor), "--state-dir", str(self.state),
            "--timezone", "Asia/Seoul",
        ])

    def test_existing_output_is_never_overwritten(self):
        self.output.write_text("existing content", encoding="utf-8")
        with patch.object(sys, "argv", self.args()):
            with self.assertRaises(SystemExit):
                renderer.main()
        self.assertEqual(self.output.read_text(encoding="utf-8"), "existing content")

    def test_checkout_rejects_machine_local_output_and_state(self):
        checkout = self.root / "checkout"
        checkout.mkdir()
        checkout = checkout.resolve()
        with patch.object(renderer, "source_checkout", return_value=checkout):
            with patch.object(sys, "argv", self.args(output=checkout / "example-rendered.plist")):
                with self.assertRaises(SystemExit):
                    renderer.main()
            with patch.object(sys, "argv", self.args(state=checkout / "example-runtime")):
                with self.assertRaises(SystemExit):
                    renderer.main()

    def test_separate_monitor_checkout_is_also_protected(self):
        checkout = (self.root / "other-checkout").resolve()
        checkout.mkdir()
        (checkout / ".git").write_text("gitdir: synthetic\n", encoding="utf-8")
        self.monitor = checkout / "reset_alert.py"
        self.monitor.write_text("# synthetic monitor\n", encoding="utf-8")
        inside_output = checkout / "generated.plist"
        with patch.object(sys, "argv", self.args(output=inside_output)):
            with self.assertRaises(SystemExit):
                renderer.main()
        self.assertFalse(inside_output.exists())
        with patch.object(sys, "argv", self.args(state=checkout / "runtime")):
            with self.assertRaises(SystemExit):
                renderer.main()
        self.assertFalse(self.output.exists())
        link = self.root / "checkout-link"
        link.symlink_to(checkout, target_is_directory=True)
        with patch.object(sys, "argv", self.args(output=link / "through-link.plist")):
            with self.assertRaises(SystemExit):
                renderer.main()
        self.assertFalse((checkout / "through-link.plist").exists())
        with patch.object(sys, "argv", self.args()):
            renderer.main()
        self.assertTrue(self.output.is_file())

    def test_malformed_label_and_timezone_are_rejected(self):
        args = self.args()
        args[args.index("--label") + 1] = "bad label"
        with patch.object(sys, "argv", args):
            with self.assertRaises(SystemExit):
                renderer.main()
        args = self.args()
        args[args.index("--timezone") + 1] = "Not/AZone"
        with patch.object(sys, "argv", args):
            with self.assertRaises(SystemExit):
                renderer.main()


if __name__ == "__main__":
    unittest.main()
