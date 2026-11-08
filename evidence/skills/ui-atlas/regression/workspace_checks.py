"""Generic consumer-repo artifact ownership, retention and relocation witnesses."""
import json
import re
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest

import atlas
import workspace
from capture import recipe_identity


class WorkspaceTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="ui-atlas-workspace-")
        self.addCleanup(self.temp.cleanup)
        self.repo = Path(self.temp.name).resolve() / "repo"
        self.repo.mkdir()

    def test_default_custom_and_idempotent_ignore(self):
        subprocess.run(["git", "init", "-q", str(self.repo)], check=True)
        root = workspace.initialize(self.repo)
        self.assertEqual(root, self.repo / ".artifacts/ui-atlas")
        recipe = root / "recipes/example/recipe.json"
        recipe.parent.mkdir(); recipe.write_text("{}")
        self.assertEqual(workspace.initialize(self.repo), root)
        self.assertEqual(recipe.read_text(), "{}")
        self.assertEqual(subprocess.run(["git", "-C", str(self.repo), "status", "--porcelain"], capture_output=True, text=True, check=True).stdout, "")
        custom = self.repo / "custom-observations"
        self.assertEqual(workspace.initialize(self.repo, custom), custom)
        with self.assertRaises(ValueError): workspace.initialize(self.repo, self.repo)

    def test_catalog_keeps_partial_latest_history_and_pending(self):
        root = workspace.initialize(self.repo)
        older = workspace.reserve(root, "app")
        latest = workspace.reserve(root, "app")
        pending = workspace.reserve(root, "app")
        for run, failed in ((older, False), (latest, True)):
            (run / "index.html").write_text("kept")
            (run / "atlas.json").write_text(json.dumps({"id": "app", "title": "<App>", "frames": [{"status": "rendered"}],
                                                        "freshness": {"status": "changed" if failed else "matched"},
                                                        "journey_failures": [{"id": "after-last-frame"}] if failed else []}))
        text = workspace.catalog(root).read_text()
        self.assertIn("&lt;App&gt;", text)
        self.assertIn("일부 실패", text)
        self.assertIn("소스 변경 · 갱신 필요", text)
        self.assertIn("생성 시 소스 일치", text)
        self.assertLess(text.index(latest.name), text.index(older.name))
        self.assertIn(pending.name, text)
        self.assertEqual((older / "index.html").read_text(), "kept")
        self.assertEqual(list((root / "tmp").iterdir()), [])
        with self.assertRaises(ValueError): workspace.reserve(root, "../escape")

    def test_relocated_source_recipe_and_support_verify_original_hashes(self):
        source = self.repo / "source.txt"; source.write_text("original")
        recipe = self.repo / "recipe.json"; recipe.write_text('{"support_files":["fixture.json"],"journeys":[]}')
        (self.repo / "fixture.json").write_text("[]")
        data = {"source": atlas.source_identity(self.repo, ["source.txt"]),
                "recipe": recipe_identity(recipe, json.loads(recipe.read_text()))}
        moved = self.repo.parent / "moved"; shutil.copytree(self.repo, moved); shutil.rmtree(self.repo)
        self.assertEqual(atlas.check_sources(data)["status"], "unavailable")
        self.assertEqual(atlas.check_sources(data, moved, moved / "recipe.json")["status"], "matched")
        (moved / "fixture.json").write_text("[1]")
        self.assertEqual(atlas.check_sources(data, moved, moved / "recipe.json")["changed"], ["[recipe file] fixture.json"])

    def test_catalog_isolates_bad_manifests_and_preserves_originals(self):
        root = workspace.initialize(self.repo)
        valid = {"id": "app", "title": "Valid run", "frames": [{"status": "rendered"}]}
        cases = ['{"frames":[', '[]', json.dumps({**valid, 'frames': [None]}),
                 json.dumps({**valid, 'frames': [{'status': []}]}),
                 json.dumps({**valid, 'freshness': {'status': []}})]
        preserved = {}
        for body in [json.dumps(valid), *cases]:
            run = workspace.reserve(root, 'app')
            (run / 'atlas.json').write_text(body)
            (run / 'index.html').write_text('Preserved canvas')
            preserved[run] = body
        text = workspace.catalog(root).read_text()
        self.assertIn('Valid run', text)
        self.assertIn('최근 열 수 있는 실행', text)
        self.assertIn('읽을 수 없는 실행', text)
        for run, body in preserved.items():
            self.assertIn(run.name, text)
            self.assertEqual((run / 'atlas.json').read_text(), body)
            self.assertEqual((run / 'index.html').read_text(), 'Preserved canvas')
        self.assertEqual(list((root / 'tmp').iterdir()), [])

    def test_workspace_payload_preserves_history_and_escapes_labels_and_paths(self):
        root = workspace.initialize(self.repo)
        title = '</script><script>syntheticMarkup()</script>'
        run = root / 'runs' / 'synthetic # run'; run.mkdir()
        (run / 'index.html').write_text('Preserved standalone viewer')
        (run / 'atlas.json').write_text(json.dumps({'id': 'app', 'title': title,
                                                    'frames': [{'status': 'rendered'}, {'status': 'unverified'}]}))
        html = workspace.catalog(root).read_text()
        payload = re.search(r'<script type="application/json" id="workspace-data">(.*?)</script>', html, re.S).group(1)
        data = json.loads(payload)
        self.assertNotIn('</script>', payload)
        self.assertEqual(data['groups'][0]['runs'][0]['title'], title)
        self.assertEqual(data['groups'][0]['runs'][0]['url'], 'runs/synthetic%20%23%20run/index.html')
        self.assertEqual(data['groups'][0]['runs'][0]['gaps'], 1)
        self.assertEqual((run / 'index.html').read_text(), 'Preserved standalone viewer')
