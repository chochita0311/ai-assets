"""Offline portability checks; no real Codex or launchd invocation."""

import importlib.util
import os
from pathlib import Path
import plistlib
import shutil
import subprocess
import tempfile
import unittest


REPO = Path(__file__).resolve().parents[1]
ADAPTER = REPO / "agents/adapters/codex"
RENDERER = ADAPTER / "scripts/render-model-binding-launchagent.py"
SPEC = importlib.util.spec_from_file_location("audit_launchagent", RENDERER)
RENDER = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(RENDER)


class LaunchAgentTests(unittest.TestCase):
    def test_render_preserves_paths_schedule_and_xml_characters(self):
        result = RENDER.render(Path("/opt/AI assets & tools"), Path("/opt/bin/codex"),
                               Path("/opt/profiles/work"), Path("/opt/logs/audit"),
                               "local.audit", "/opt/bin:/usr/bin:/bin")
        result = plistlib.loads(plistlib.dumps(result))
        self.assertEqual(result["WorkingDirectory"], "/opt/AI assets & tools")
        self.assertEqual(result["ProgramArguments"][1],
                         "/opt/AI assets & tools/agents/adapters/codex/scripts/run-model-binding-audit.sh")
        self.assertEqual(result["StartCalendarInterval"], {"Weekday": 1, "Hour": 9, "Minute": 0})
        self.assertEqual(result["EnvironmentVariables"]["CODEX_MODEL_AUDIT_BIN"], "/opt/bin/codex")
        self.assertEqual(result["EnvironmentVariables"]["CODEX_HOME"], "/opt/profiles/work")
        self.assertEqual(result["StandardErrorPath"], "/opt/logs/audit/launchd.stderr.log")

    def test_cli_creates_only_requested_file_and_refuses_overwrite(self):
        with tempfile.TemporaryDirectory(prefix="ai-assets-plist-test-") as scratch:
            root = Path(scratch)
            output = root / "audit.plist"
            command = ["python3", str(RENDERER), "--codex-bin", "/bin/sh",
                       "--codex-home", str(root / "runtime"), "--log-dir", str(root / "logs"),
                       "--output", str(output)]
            first = subprocess.run(command, capture_output=True, text=True)
            self.assertEqual(first.returncode, 0, first.stderr)
            original = output.read_bytes()
            self.assertEqual(set(root.iterdir()), {output})
            second = subprocess.run(command, capture_output=True, text=True)
            self.assertNotEqual(second.returncode, 0)
            self.assertEqual(output.read_bytes(), original)
            alias = root / "existing-link.plist"
            alias.symlink_to(output)
            linked = subprocess.run(command[:-1] + [str(alias)], capture_output=True, text=True)
            self.assertNotEqual(linked.returncode, 0)
            self.assertTrue(alias.is_symlink())
            self.assertEqual(output.read_bytes(), original)

    def test_cli_rejects_output_in_checkout(self):
        command = ["python3", str(RENDERER), "--codex-bin", "/bin/sh",
                   "--codex-home", "/opt/runtime", "--log-dir", "/opt/logs",
                   "--output", str(REPO / "must-not-create.plist")]
        result = subprocess.run(command, capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("outside the source checkout", result.stderr)
        self.assertFalse((REPO / "must-not-create.plist").exists())


class RunnerTests(unittest.TestCase):
    def run_fixture(self, status="NO_BINDING_CHANGE", model="fixture-model", missing_binary=False):
        with tempfile.TemporaryDirectory(prefix="ai-assets-runner-test-") as scratch:
            root = Path(scratch)
            checkout = root / "different checkout & spaces"
            adapter = checkout / "agents/adapters/codex"
            (adapter / "scripts").mkdir(parents=True)
            (adapter / "profiles").mkdir()
            (adapter / "custom-agents").mkdir()
            (adapter / "profiles/model-binding-audit.config.toml").write_text('model = "fixture-model"\n')
            runner = adapter / "scripts/run-model-binding-audit.sh"
            shutil.copyfile(ADAPTER / "scripts/run-model-binding-audit.sh", runner)
            bin_dir = root / "bin"
            bin_dir.mkdir()
            fake = bin_dir / "codex"
            fake.write_text('''#!/bin/sh
printf '%s\\n' "$@" > "$AUDIT_FIXTURE_ARGS"
printf 'model: %s\\n' "$AUDIT_FIXTURE_MODEL" >&2
while [ "$#" -gt 0 ]; do
  if [ "$1" = "--output-last-message" ]; then
    shift
    printf 'Status: %s\\n' "$AUDIT_FIXTURE_STATUS" > "$1"
    exit 0
  fi
  shift
done
exit 1
''')
            fake.chmod(0o700)
            env = os.environ.copy()
            for key in tuple(env):
                if key.startswith("CODEX_MODEL_AUDIT_"):
                    del env[key]
            env.update({
                "PATH": f"{bin_dir}:/usr/bin:/bin",
                "CODEX_MODEL_AUDIT_LOG_DIR": str(root / "logs"),
                "CODEX_MODEL_AUDIT_DOCS_HELPER": str(root / "unavailable-helper.mjs"),
                "AUDIT_FIXTURE_ARGS": str(root / "arguments.txt"),
                "AUDIT_FIXTURE_MODEL": model,
                "AUDIT_FIXTURE_STATUS": status,
            })
            if missing_binary:
                env["CODEX_MODEL_AUDIT_BIN"] = str(root / "no-such-codex")
            result = subprocess.run(["/bin/sh", str(runner)], cwd=root, env=env,
                                    capture_output=True, text=True)
            persisted = (root / "logs/latest-status.txt").read_text()
            if not missing_binary:
                args = (root / "arguments.txt").read_text().splitlines()
                self.assertEqual(Path(args[args.index("--cd") + 1]).resolve(), checkout.resolve())
                self.assertEqual(args[args.index("--sandbox") + 1], "read-only")
                self.assertEqual(args[args.index("--profile") + 1], "model-binding-audit")
            else:
                self.assertFalse((root / "arguments.txt").exists())
            self.assertFalse(any((root / "logs").glob(".report.*")))
            return result.returncode, persisted, (root / "logs/attention-required.txt").exists()

    def test_relocated_checkout_and_path_binary_discovery(self):
        code, status, attention = self.run_fixture()
        self.assertEqual(code, 0)
        self.assertIn("Status: NO_BINDING_CHANGE", status)
        self.assertFalse(attention)

    def test_status_and_model_guards_survive_path_changes(self):
        for emitted, model, code, expected in [
            ("REVIEW_REQUIRED", "fixture-model", 0, "REVIEW_REQUIRED"),
            ("SOURCE_UNAVAILABLE", "fixture-model", 2, "SOURCE_UNAVAILABLE"),
            ("NOT_A_STATUS", "fixture-model", 5, "INVALID_AUDIT_OUTPUT"),
            ("NO_BINDING_CHANGE", "different-model", 6, "AUDIT_MODEL_MISMATCH"),
        ]:
            with self.subTest(status=emitted, model=model):
                actual, persisted, attention = self.run_fixture(emitted, model)
                self.assertEqual(actual, code)
                self.assertIn(f"Status: {expected}", persisted)
                self.assertTrue(attention)

    def test_missing_explicit_binary_does_not_fall_back(self):
        code, status, attention = self.run_fixture(missing_binary=True)
        self.assertEqual(code, 4)
        self.assertIn("Status: AUDIT_RUN_FAILED", status)
        self.assertTrue(attention)


if __name__ == "__main__":
    unittest.main()
