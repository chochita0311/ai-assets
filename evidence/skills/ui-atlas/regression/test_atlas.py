"""Portable behavior checks. Browser check requires Playwright and Chromium."""
import argparse
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import threading
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[4]
SCRIPTS = ROOT / "skills/ui-atlas/scripts"
sys.path.insert(0, str(SCRIPTS))
import atlas
from capture import recipe_identity
from viewer_checks import check_review_navigation
from workspace_checks import WorkspaceTests
from workspace_browser_checks import check_workspace_navigation
from usability_checks import check_usability
from reliability_checks import check_reliability
from conflict_checks import check_conflicts
from projection_checks import check_projection
import workspace


class PackageTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="ui-atlas-unit-")
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        (self.root / "source.txt").write_text("original")
        (self.root / "frame.html").write_text('<!doctype html><html data-atlas-node="e0"><head></head><body data-atlas-node="e1"><button data-atlas-node="e2">Example</button></body></html>')
        self.data = {"schema":"ui-atlas/v2","id":"example","title":"</script><script>broken</script>",
            "captured_at":atlas.now(),"source":atlas.source_identity(self.root,["source.txt"]),
            "scope":"One synthetic frame","limitations":[],"replay":"not supplied",
            "frames":[{"id":"loaded","label":"Loaded","surface":"Inbox","journey":"load","status":"rendered",
                       "evidence":"synthetic","document":"frame.html","elements":[{"id":"e0","parent":None,"tag":"html","selector":"html"},{"id":"e1","parent":"e0","tag":"body","selector":"body"},{"id":"e2","parent":"e1","tag":"button","selector":"button"}],"viewport":{"width":1,"height":1},"regions":[],"texts":[]}]}

    def write(self):
        path = self.root / "atlas.json"
        path.write_text(json.dumps(self.data))
        return path

    def test_atomic_manifest_preserves_previous_on_interrupted_write(self):
        path = self.write(); original = path.read_bytes()
        def interrupted(value, stream, **kwargs):
            stream.write('{"frames":[')
            raise OSError("Simulated interrupted serialization")
        with patch.object(atlas.json, 'dump', side_effect=interrupted):
            with self.assertRaises(OSError): atlas.write_json(path, {"new": True})
        self.assertEqual(path.read_bytes(), original)
        self.assertEqual(list(self.root.glob('.*.writing')), [])
        atlas.write_json(path, {"new": "Complete manifest"})
        self.assertEqual(atlas.read_json(path), {"new": "Complete manifest"})
        self.assertEqual(list(self.root.glob('.*.writing')), [])

    def test_standalone_and_inert_metadata(self):
        atlas.package(self.write(), self.root / "index.html")
        html = (self.root / "index.html").read_text()
        self.assertIn("data-atlas-node",html)
        self.assertNotIn("data:image/png;base64,",html)
        self.assertNotIn("</script><script>broken",html)
        self.assertIn(r"\u003c/script>",html)

    def test_document_envelope_rejects_missing_and_repeated_tags(self):
        path = self.root / 'frame.html'; original = path.read_text()
        for body in (original.replace('<head></head>', ''), original.replace('</body>', ''),
                     original.replace('<head></head>', '<head></head><head></head>')):
            path.write_text(body)
            with self.assertRaisesRegex(ValueError, 'document envelope|explicit html, head and body'):
                atlas.package(self.write(), self.root / 'index.html')

    def test_raw_text_and_declarative_animation_boundaries(self):
        path = self.root / 'frame.html'; original = path.read_text()
        button = '<button data-atlas-node="e2">Example</button>'
        for tag in ('plaintext', 'xmp', 'noembed', 'noframes', 'noscript', 'template',
                    'animate', 'set', 'animateColor', 'animateTransform', 'animateMotion', 'discard'):
            path.write_text(original.replace(button, f'<{tag} data-atlas-node="e2">Example</{tag}>'))
            with self.assertRaisesRegex(ValueError, 'Active/unsupported DOM tag'):
                atlas.package(self.write(), self.root / 'index.html')
        for tag in ('style', 'title', 'textarea'):
            path.write_text(original.replace(button, f'<{tag} data-atlas-node="e2"/>'))
            with self.assertRaisesRegex(ValueError, 'explicit closing tag'):
                atlas.package(self.write(), self.root / 'index.html')
        path.write_text(original.replace(button, '<textarea data-atlas-node="e2">Text </body> </html></textarea>'))
        self.data['frames'][0]['elements'][-1].update(tag='textarea', selector='textarea')
        atlas.package(self.write(), self.root / 'index.html')

    def test_selected_file_value_refused(self):
        path = self.root / 'frame.html'; original = path.read_text()
        button = '<button data-atlas-node="e2">Example</button>'
        self.data['frames'][0]['elements'][-1].update(tag='input', selector='input')
        path.write_text(original.replace(button, '<input type="file" data-atlas-node="e2" value="report.txt">'))
        with self.assertRaisesRegex(ValueError, 'Selected file inputs'):
            atlas.package(self.write(), self.root / 'index.html')
        path.write_text(original.replace(button, '<input type="file" data-atlas-node="e2" value="">'))
        atlas.package(self.write(), self.root / 'index.html')

    def test_region_without_bounds_cannot_supply_an_empty_rectangle(self):
        region = {'id': 'action', 'label': 'Action', 'selector': 'button', 'rect': None, 'reason': 'Not observed'}
        self.data['frames'][0]['regions'] = [region]
        atlas.validate(self.data)
        region['rect'] = {}
        with self.assertRaises(ValueError): atlas.validate(self.data)

    def test_optional_descriptions_preserve_plain_text_and_reject_invalid_fields(self):
        frame = self.data['frames'][0]
        frame['description'] = {'purpose': 'Inspect the loading copy', 'exceptions': '</script><script>unsafe</script>'}
        packaged = atlas.package(self.write(), self.root / 'index.html')
        self.assertEqual(packaged['frames'][0]['description'], frame['description'])
        self.assertNotIn('</script><script>unsafe', (self.root / 'index.html').read_text())
        for description in ({'purpose': []}, {'unrecognized': 'value'}, None):
            frame['description'] = description
            with self.assertRaises(ValueError): atlas.validate(self.data)

    def test_source_change_and_unavailable_are_not_current(self):
        self.assertEqual(atlas.check_sources(self.data)["status"],"matched")
        (self.root / "source.txt").write_text("changed")
        self.assertEqual(atlas.check_sources(self.data)["status"],"changed")
        (self.root / "source.txt").unlink()
        self.assertEqual(atlas.check_sources(self.data)["status"],"unavailable")

    def test_outside_documents_and_missing_dom_refused(self):
        self.data["frames"][0]["document"] = "../outside.html"
        with self.assertRaises(ValueError): atlas.package(self.write(), self.root / "index.html")
        self.data["frames"][0]["document"] = "frame.html"
        self.data["frames"][0]["elements"].pop()
        with self.assertRaises(ValueError): atlas.package(self.write(), self.root / "index.html")

    def test_active_dom_and_image_substitutes_refused(self):
        for markup in ('<script>alert(1)</script>', '<button onclick="alert(1)">x</button>', '<iframe src="https://example.invalid"></iframe>'):
            (self.root / 'frame.html').write_text(markup)
            with self.assertRaises(ValueError): atlas.package(self.write(), self.root / "index.html")
        self.data['frames'][0]['image']='screen.png'
        with self.assertRaises(ValueError): atlas.validate(self.data)

    def test_incomplete_states_cannot_masquerade_as_captures(self):
        self.data["frames"][0].update(status="unverified",reason="No reproduction")
        with self.assertRaises(ValueError): atlas.validate(self.data)
        del self.data["frames"][0]["document"]
        atlas.validate(self.data)
        self.data["frames"].append(dict(self.data["frames"][0]))
        with self.assertRaises(ValueError): atlas.validate(self.data)

    def test_out_of_bounds_regions_refused(self):
        self.data["frames"][0]["regions"]=[{"id":"results","label":"Results","selector":"#results","rect":{"x":0,"y":0,"width":2,"height":1}}]
        with self.assertRaises(ValueError): atlas.validate(self.data)

    def test_visible_element_bounds_and_status_agree(self):
        element = self.data["frames"][0]["elements"][0]
        element.update(visible=True, visibleRect={"x":0,"y":0,"width":1,"height":1})
        atlas.validate(self.data)
        element["visibleRect"]["width"] = 2
        with self.assertRaises(ValueError): atlas.validate(self.data)
        element["visibleRect"] = None
        with self.assertRaises(ValueError): atlas.validate(self.data)
        element["visible"] = False
        atlas.validate(self.data)


    def test_missing_inspection_arrays_refused(self):
        for key in ("regions", "texts", "elements"):
            removed = self.data["frames"][0].pop(key)
            with self.assertRaises(ValueError): atlas.package(self.write(), self.root / "index.html")
            self.data["frames"][0][key] = removed

    def test_recipe_fixture_and_support_drift(self):
        (self.root / "response.json").write_text('[]')
        (self.root / "launch.py").write_text('# fixture launcher')
        recipe = {"support_files": ["launch.py"], "journeys": [
            {"routes": [{"response": {"file": "response.json"}}], "steps": []}]}
        path = self.root / "recipe.json"
        path.write_text(json.dumps(recipe))
        self.data["recipe"] = recipe_identity(path, recipe)
        first = atlas.package(self.write(), self.root / "index.html")["frames"][0]["identity"]
        self.assertEqual(atlas.check_sources(self.data)["status"], "matched")
        (self.root / "response.json").write_text('["new data"]')
        self.assertIn("[recipe file] response.json", atlas.check_sources(self.data)["changed"])
        self.data["recipe"] = recipe_identity(path, recipe)
        second = atlas.package(self.write(), self.root / "index.html")["frames"][0]["identity"]
        self.assertNotEqual(first, second)
        (self.root / "launch.py").unlink()
        self.assertIn("[recipe file] launch.py", atlas.check_sources(self.data)["unavailable"])


def observer_checks(browser):
    page = browser.new_page(viewport={"width":1000,"height":800})
    page.set_content('''<style>
      #panel {height:40px; width:300px; overflow:hidden;}
      #hidden {margin-top:90px;}
      #partial {height:12px; overflow:hidden; font:20px/30px sans-serif;}
      dialog {width:300px;}
      </style><div id="panel"><div>Visible line</div><div id="hidden">Clipped away</div></div>
      <div id="partial">Partially visible</div><p aria-hidden="true">Painted aria-hidden text</p>
      <dialog id="first"><p>Lower modal</p></dialog><dialog id="second"><p>Top modal</p></dialog>''')
    observer = atlas.browser_script("observe.js")
    result = page.evaluate(observer, [{"id":"hidden","label":"Hidden","selector":"#hidden"}])
    assert result['regions'][0]['rect'] is None
    assert not any('Clipped away' in text['text'] for text in result['texts'])
    assert any(text['text']=='Partially visible' and text['clipped'] for text in result['texts'])
    assert any(text['text']=='Painted aria-hidden text' for text in result['texts'])
    page.evaluate("document.querySelector('#first').showModal(); document.querySelector('#second').showModal();")
    result = page.evaluate(observer, [])
    assert any(text['text']=='Top modal' for text in result['texts'])
    assert not any(text['text']=='Lower modal' for text in result['texts'])
    page.close()


def browser_check(browser_path, workspace_only=False):
    from playwright.sync_api import sync_playwright
    source = Path(__file__).parent / "inputs"
    class Handler(SimpleHTTPRequestHandler):
        writes = 0
        def log_message(self,*args): pass
        def do_POST(self):
            Handler.writes += 1
            self.send_error(500)
    server=ThreadingHTTPServer(("127.0.0.1",0),partial(Handler,directory=str(source)))
    thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
    with tempfile.TemporaryDirectory(prefix="ui-atlas-browser-") as temporary:
        owner=Path(temporary)
        recipe={"schema":"ui-atlas.recipe/v1","id":"fixture","title":"Fieldbook · Atlas","source_files":["index.html"],
          "scope":"Synthetic loading, loaded, hover, focus, modal, sync failure and one missing state.",
          "journeys":[{"id":"notes","surface":"Notes","label":"Load and review","description":{"purpose":"Review loading and sync copy","action":"Load notes, open settings, then request sync","result":"Loaded notes and a mocked sync error","exceptions":"Offline remains unexamined"},"evidence":"synthetic","viewport":{"width":1000,"height":800},"locale":"ko-KR",
            "routes":[{"id":"items","url":"/api/items","hold":True},{"id":"sync","url":"/api/sync","method":"POST","hold":True}],
            "regions":[{"id":"results","label":"Results","selector":"#results"},{"id":"modal","label":"Settings","selector":"#settings"}],
            "steps":[{"action":"goto","url":"/"},{"action":"wait","selector":"#results span","text":"불러오는 중…"},
              {"action":"capture","id":"loading","label":"Loading"},
              {"action":"respond","route":"items","response":{"json":["첫 번째 노트","두 번째 노트"]}},
              {"action":"wait","selector":"#results","text":"첫 번째 노트 · 두 번째 노트"},
              {"action":"capture","id":"loaded","label":"Loaded"},
              {"action":"hover","selector":"#help"},{"action":"capture","id":"hover","label":"Hover"},
              {"action":"focus","selector":"#help"},{"action":"capture","id":"focus","label":"Focus"},
              {"action":"click","selector":"#open"},{"action":"capture","id":"modal","label":"Modal"},
              {"action":"click","selector":"#close"},{"action":"click","selector":"#sync"},
              {"action":"capture","id":"syncing","label":"Syncing"},
              {"action":"respond","route":"sync","response":{"status":500,"json":{}}},
              {"action":"wait","selector":"#notice","text":"동기화하지 못했습니다. 다시 시도해 주세요."},
              {"action":"capture","id":"failed","label":"Failed"}]}],
          "coverage":[{"id":"offline","label":"Offline","surface":"Notes","journey":"missing","status":"unverified","reason":"Not exercised"}]}
        path=owner/"recipe.json";path.write_text(json.dumps(recipe,ensure_ascii=False))
        command=[sys.executable,"-B",str(SCRIPTS/"capture.py"),str(path),"--source-root",str(source),"--base-url",f"http://127.0.0.1:{server.server_port}","--browser",str(browser_path)]
        try:
            subprocess.run(command+["--out",str(owner/"run")],check=True)
            manifest=atlas.read_json(owner/"run/atlas.json")
            assert len([f for f in manifest['frames'] if f['status']=='rendered'])==7
            assert Handler.writes==0, "Real POST reached fixture backend"
            modal=next(f for f in manifest['frames'] if f['id']=='modal')
            assert any('실제 모달' in t['text'] for t in modal['texts'])
            assert any(r['id']=='modal' and r['rect'] for r in modal['regions'])
            replay = subprocess.run(command+["--replay","loading","--headless","--replay-seconds","0.4"],check=True,capture_output=True,text=True)
            assert not replay.stderr, replay.stderr
            assert not list((owner/'run').rglob('*.png')), "Screenshots must not be a canvas dependency"
            assert manifest['frames'][0]['payload']['routes'][0]['hold'] is True
            assert manifest['frames'][1]['payload']['routes'][0]['hold'] is False
            if workspace_only:
                with sync_playwright() as p:
                    browser=p.chromium.launch(executable_path=str(browser_path))
                    try:check_workspace_navigation(browser, owner)
                    finally:browser.close()
                return
            with sync_playwright() as p:
                browser=p.chromium.launch(executable_path=str(browser_path))
                observer_checks(browser)
                context=browser.new_context(viewport={"width":1440,"height":1000})
                page=context.new_page()
                errors=[];requests=[]
                page.on('pageerror',lambda e:errors.append(str(e)))
                page.on('request',lambda request:requests.append(request.url))
                page.goto((owner/"run/index.html").as_uri())
                page.wait_for_function("document.querySelectorAll('.artboard[data-ready=true]').length===7")
                assert page.locator('.artboard').count()==7
                assert page.locator('.artboard > iframe').count()==7
                assert page.locator('.artboard > img').count()==0
                for observed in (f for f in manifest['frames'] if f['status']=='rendered'):
                    dom=page.frame_locator('[data-frame="'+observed['id']+'"] iframe')
                    actual=dom.locator('[data-atlas-node]').evaluate_all('(nodes)=>Object.fromEntries(nodes.map(n=>{const r=n.getBoundingClientRect();return[n.dataset.atlasNode,{x:r.x,y:r.y,width:r.width,height:r.height}]}))')
                    for element in observed['elements']:
                        if not element['visible']:continue
                        assert all(abs(actual[element['id']][key]-element['rect'][key])<=3 for key in ('x','y','width','height')),(observed['id'],element['selector'],element['rect'],actual[element['id']])
                assert not any(url.startswith(('http:', 'https:')) for url in requests), requests
                page.locator('[data-state="loaded"]').click();page.wait_for_timeout(100)
                loaded=page.frame_locator('[data-frame="loaded"] iframe')
                def pick(state, selector):
                    node=page.frame_locator('[data-frame="'+state+'"] iframe').locator(selector)
                    rect=node.evaluate('(e)=>{const r=e.getBoundingClientRect();return{x:r.x,y:r.y,width:r.width,height:r.height}}')
                    outer=page.locator('[data-frame="'+state+'"]').bounding_box();scale=outer['width']/1000
                    page.mouse.click(outer['x']+(rect['x']+rect['width']/2)*scale,outer['y']+(rect['y']+rect['height']/2)*scale)
                pick('loaded','#results')
                page.wait_for_function("document.querySelector('#selected-selector').textContent === '#results'")
                assert page.locator('.selection-box').is_visible()
                page.locator('#note').fill('이 문구를 짧게 해 주세요.');page.locator('#note-form button').click()
                assert page.locator('#note-count').inner_text()=='1'
                other=context.new_page();other.goto((owner/'run/index.html').as_uri())
                other.locator('[data-state="loaded"]').click()
                other.locator('#note').fill('두 번째 탭 의견');other.locator('#note-form button').click()
                page.wait_for_function("document.querySelector('#note-count').textContent==='2'")
                other.locator('.saved-note').filter(has_text='두 번째 탭 의견').get_by_role('button',name='삭제',exact=True).click()
                page.wait_for_function("document.querySelector('#note-count').textContent==='1'");other.close()
                page.locator('#requests').click()
                page.locator('#collect-notes').click()
                assert '#results' in page.locator('#handoff-text').input_value()
                assert '이 문구를 짧게' in page.locator('#handoff-text').input_value()
                page.locator('#close-handoff').click()
                page.locator('#file-menu-button').click()
                with page.expect_download() as info:page.locator('#notes-download').click()
                exported=owner/'notes.json';info.value.save_as(exported)
                saved=json.loads(exported.read_text());saved['notes'][0].update(id='legacy',identity='v1-image-evidence')
                exported.write_text(json.dumps(saved));page.locator('#import-file').set_input_files(exported)
                page.wait_for_function("document.querySelector('#note-count').textContent==='2'")
                assert page.locator('#frame-notes .stale').inner_text() == '재확인 필요 · 저장 당시와 관찰 근거가 달라졌습니다.'
                page.locator('[data-panel="screens"]').click()
                page.locator('[data-tab="payload"]').click()
                assert '첫 번째 노트' in page.locator('#payload').inner_text()
                page.locator('#replay').click();assert page.locator('#handoff').is_visible();page.locator('#close-handoff').click()
                page.locator('[data-tab="element"]').click()
                pick('loaded','#fixture-mark')
                page.wait_for_function("document.querySelector('#selected-selector').textContent==='#fixture-mark'")
                page.keyboard.press('Enter')
                page.wait_for_function("document.querySelector('#selected-selector').textContent==='#fixture-icon'")
                page.locator('[data-state="syncing"]').click();page.wait_for_timeout(100)
                disabled=page.frame_locator('[data-frame="syncing"] iframe').locator('#sync')
                assert disabled.is_disabled()
                pick('syncing','#sync')
                page.wait_for_function("document.querySelector('#selected-selector').textContent==='#sync'")
                assert Handler.writes==0
                page.locator('[data-state="modal"]').click();page.wait_for_timeout(100)
                assert page.frame_locator('[data-frame="modal"] iframe').locator('#settings').evaluate('(element)=>element.matches(":modal")')
                page.locator('#close-inspector').click()
                camera='() => {const m=new DOMMatrix(getComputedStyle(document.querySelector("#world")).transform);return {x:m.e,y:m.f,zoom:m.a}}'
                before=page.evaluate(camera);bounds=page.locator('#canvas').bounding_box()
                x=bounds['x']+12;y=bounds['y']+12
                page.mouse.move(x,y);page.mouse.down();page.mouse.move(x+70,y+45,steps=5);page.mouse.up()
                after=page.evaluate(camera)
                assert abs(after['x']-before['x']-70)<1 and abs(after['y']-before['y']-45)<1
                x=round(bounds['x']+bounds['width']*.7);y=round(bounds['y']+bounds['height']*.7)
                before=page.evaluate(camera);world_before=((x-bounds['x']-before['x'])/before['zoom'],(y-bounds['y']-before['y'])/before['zoom'])
                page.mouse.move(x,y);page.mouse.wheel(0,-220);page.wait_for_timeout(100)
                after=page.evaluate(camera);world_after=((x-bounds['x']-after['x'])/after['zoom'],(y-bounds['y']-after['y'])/after['zoom'])
                assert after['zoom']>before['zoom'] and max(abs(a-b) for a,b in zip(world_before,world_after))<.05,(before,after,world_before,world_after,bounds)
                page.locator('[data-state="loaded"]').click();page.wait_for_timeout(100)
                card=page.locator('[data-frame="loaded"]');before=card.evaluate('(e)=>({x:+e.dataset.x,y:+e.dataset.y})')
                label=card.locator('.frame-label').bounding_box();page.mouse.move(label['x']+20,label['y']+10)
                page.mouse.down();page.mouse.move(label['x']+90,label['y']+40,steps=5);page.mouse.up()
                moved=card.evaluate('(e)=>({x:+e.dataset.x,y:+e.dataset.y})');assert moved!=before
                page.reload();page.wait_for_function("document.querySelectorAll('.artboard[data-ready=true]').length===7")
                assert page.locator('[data-frame="loaded"]').evaluate('(e)=>({x:+e.dataset.x,y:+e.dataset.y})')==moved
                page.locator('[data-panel="screens"]').click()
                page.locator('#search').fill('두 번째 노트');assert page.locator('.artboard').count()>0
                page.locator('#search').fill('')
                check_review_navigation(page)
                page.set_viewport_size({'width':390,'height':844})
                assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
                page.locator('#info').click();assert page.get_by_text('파일 변경을 자동으로 감시하지 않습니다.',exact=True).is_visible()
                page.locator('#close-info').click()
                recipe['journeys'][0]['steps']=[{'action':'goto','url':'/'},{'action':'frame','id':'before-failure','label':'Before failure'},{'action':'wait','selector':'#not-present'}]
                path.write_text(json.dumps(recipe))
                consumer=owner/'consumer';consumer.mkdir()
                shutil.copy2(source/'index.html',consumer/'index.html')
                workspace_root=workspace.initialize(consumer)
                corrupt=workspace.reserve(workspace_root, 'old')
                (corrupt/'index.html').write_text('Preserved prior output')
                corrupt_bytes=b'{"frames":['
                (corrupt/'atlas.json').write_bytes(corrupt_bytes)
                default_command=command.copy()
                default_command[default_command.index('--source-root')+1]=str(consumer)
                failed=subprocess.run(default_command+['--timeout','0.2'],capture_output=True,text=True)
                assert failed.returncode==2,failed.stderr
                run=next(p for p in (workspace_root/'runs').iterdir() if p != corrupt)
                catalog=(workspace_root/'index.html').read_text()
                assert '일부 실패' in catalog and '읽을 수 없는 실행' in catalog
                assert (corrupt/'atlas.json').read_bytes()==corrupt_bytes
                assert (corrupt/'index.html').read_text()=='Preserved prior output'
                assert (workspace_root/'.gitignore').read_text()=='*\n'
                failed_manifest=atlas.read_json(run/'atlas.json')
                assert failed_manifest['frames'][0]['status']=='rendered'
                assert failed_manifest['journey_failures'][0]['id']=='notes'
                page.goto((run/'index.html').as_uri());page.locator('#info').click()
                assert '시나리오 실패: notes' in page.locator('#provenance').inner_text()
                assert not errors,errors
                check_usability(browser, owner)
                check_reliability(browser, owner)
                check_conflicts(browser, owner)
                check_projection(browser, owner, browser_path)
                check_workspace_navigation(browser, owner)
                browser.close()
            print('Browser checks passed: real DOM, geometry, modal, disabled-element picking, pointer zoom/pan, frame layout persistence, payload, replay, cross-tab notes, legacy import, isolated preview, narrow provenance, terminal failure.')
        finally:
            server.shutdown();server.server_close();thread.join()


if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--browser',type=Path)
    parser.add_argument('--workspace-only',action='store_true',help='Run workspace navigation browser witnesses only')
    args=parser.parse_args()
    if args.workspace_only and not args.browser:parser.error('--workspace-only requires --browser')
    suite=unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromTestCase(case) for case in (PackageTests, WorkspaceTests))
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    if not result.wasSuccessful():sys.exit(1)
    if args.browser:browser_check(args.browser,args.workspace_only)
