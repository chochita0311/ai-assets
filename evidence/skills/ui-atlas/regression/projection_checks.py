"""Visible tree projection and accepted inert-document bridge boundaries."""
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
import subprocess
import sys
import threading
import atlas
from capture import capture_frame
from reliability_checks import build_view, frame_for, search_select


def check_scroll_restore(browser, owner):
    source = owner / 'scroll-source.html'
    context = browser.new_context(viewport={'width': 1000, 'height': 800})
    page = context.new_page()
    for behavior in ('auto', 'smooth'):
        source.write_text('''<!doctype html><html><head><style>
          html,#scroller {scroll-behavior:''' + behavior + '''}
          body {margin:0;width:1500px;height:2400px}
          #window-target {position:absolute;left:200px;top:1100px}
          #scroller {position:fixed;left:400px;top:300px;width:250px;height:180px;overflow:auto}
          #content {position:relative;width:1000px;height:1200px}
          #container-target {position:absolute;left:220px;top:550px}
          </style></head><body><button id="window-target">Window target</button>
          <div id="scroller"><div id="content"><button id="container-target">Container target</button></div></div></body></html>''')
        page.goto(source.as_uri())
        page.evaluate('scrollTo({left:100,top:1000,behavior:"instant"});document.querySelector("#scroller").scrollTo({left:160,top:500,behavior:"instant"})')
        document = 'scroll-' + behavior + '.html'
        observed = capture_frame(page, [], owner / document)
        assert observed['scroll'] == {'x': 100, 'y': 1000}
        _, output, _ = build_view(owner, 'scroll-view-' + behavior, source, [frame_for(observed, document, 'one')])
        page.goto(output.as_uri()); page.wait_for_selector('[data-ready="true"]')
        dom = page.frame_locator('iframe')
        for delay in (0, 150):
            page.wait_for_timeout(delay)
            offsets = dom.locator('html').evaluate('el=>[scrollX,scrollY]')
            assert offsets == [100, 1000], (behavior, delay, offsets)
            offsets = dom.locator('#scroller').evaluate('el=>[el.scrollLeft,el.scrollTop]')
            assert offsets == [160, 500], (behavior, delay, offsets)
        for selector, query in (('#window-target', 'Window target'), ('#container-target', 'Container target')):
            search_select(page, query, selector)
            assert page.locator('.selection-box').is_visible()
    context.close()


def check_native_forms(browser, owner):
    source = owner / 'native-source.html'
    source.write_text('''<!doctype html><input id="file" type="file" style="width:300px;height:30px">
      <input id="text" value="Kept value"><select id="choice" style="width:200px;height:30px"><option>Alpha</option><option>Beta</option></select>
      <select id="multi" multiple><option>One</option><option>Two</option></select>''')
    context = browser.new_context(viewport={'width': 1000, 'height': 800})
    page = context.new_page()
    for selected in (-1, 1):
        page.goto(source.as_uri()); page.locator('#choice').evaluate('(el,index)=>el.selectedIndex=index', selected)
        document = f'native-{selected}.html'
        observed = capture_frame(page, [], owner / document)
        _, output, _ = build_view(owner, f'native-view-{selected}', source, [frame_for(observed, document, 'one')])
        page.goto(output.as_uri()); page.wait_for_selector('[data-ready="true"]')
        dom = page.frame_locator('iframe')
        assert dom.locator('#choice').evaluate('el=>el.selectedIndex') == selected
        assert dom.locator('#multi').evaluate('el=>el.selectedOptions.length') == 0
        assert dom.locator('#file').evaluate('el=>el.files.length') == 0
        assert dom.locator('#text').input_value() == 'Kept value'
    page.goto(source.as_uri())
    page.locator('#file').evaluate('el=>{const dt=new DataTransfer();dt.items.add(new File(["synthetic"],"report.txt"));el.files=dt.files}')
    destination = owner / 'selected-file.html'
    try:
        capture_frame(page, [], destination)
        raise AssertionError('Selected file state was accepted as an empty input')
    except Exception as error:
        assert 'Selected file inputs require an app-owned preview' in str(error), str(error)
    assert not destination.exists()
    context.close()


def check_embedded_resources(browser, owner, browser_path):
    class QuietHandler(SimpleHTTPRequestHandler):
        def log_message(self, *args):
            pass
    icon = '<svg xmlns="http://www.w3.org/2000/svg" width="40" height="40"><rect width="40" height="40" fill="red"/></svg>'
    (owner / 'icon.svg').write_text(icon)
    (owner / 'sprite.svg').write_text('''<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" width="40" height="40">
      <defs><linearGradient id="base"><stop stop-color="red"/><stop offset="1" stop-color="blue"/></linearGradient>
      <linearGradient id="derived" href="#base"/><linearGradient id="legacy" xlink:href="#base"/></defs>
      <g id="mark"><rect width="40" height="40" fill="url( '#derived' )"/></g>
      <g id="other"><rect width="40" height="40" fill="url(#legacy)"/></g></svg>''')
    source = owner / 'resources-source.html'
    source.write_text('''<!doctype html><input id="image-input" type="image" src="/icon.svg" width="40" height="40">
      <input id="data-input" type="image" src="data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='40' height='40'%3E%3Crect width='40' height='40' fill='red'/%3E%3C/svg%3E" width="40" height="40">
      <img id="image" src="/icon.svg" width="40" height="40">
      <svg width="40" height="40"><use href="/sprite.svg#mark"/></svg>
      <svg width="40" height="40"><use href="/sprite.svg#other"/></svg>''')
    server = ThreadingHTTPServer(('127.0.0.1', 0), partial(QuietHandler, directory=str(owner)))
    thread = threading.Thread(target=server.serve_forever, daemon=True); thread.start()
    context = browser.new_context(viewport={'width': 1000, 'height': 800})
    try:
        page = context.new_page(); page.goto(f'http://127.0.0.1:{server.server_port}/{source.name}')
        page.wait_for_load_state('networkidle')
        observed = capture_frame(page, [], owner / 'resources-frame.html')
        _, output, _ = build_view(owner, 'embedded-resources', source, [frame_for(observed, 'resources-frame.html', 'one')])
        requests = []; page.on('request', lambda request: requests.append(request.url))
        page.goto(output.as_uri()); page.wait_for_selector('[data-ready="true"]')
        dom = page.frame_locator('iframe')
        for selector in ('#image-input', '#data-input', '#image'):
            assert dom.locator(selector).get_attribute('src').startswith('data:image/')
        for name in ('derived', 'legacy'):
            gradient = dom.locator(f'linearGradient[id$="-{name}"]')
            assert gradient.evaluate('el=>{const href=el.getAttribute("href")||el.getAttribute("xlink:href");return document.getElementById(href.slice(1))?.querySelectorAll("stop").length}') == 2
        assert dom.locator('linearGradient[id$="-base"]').count() == 1
        for name in ('mark', 'other'):
            assert dom.locator(f'g[id$="-{name}"] rect').evaluate(r'el=>{const match=el.getAttribute("fill").match(/^url\(#(.+)\)$/);return !!match&&!!document.getElementById(match[1])}')
        assert not any(url.startswith(('http:', 'https:')) for url in requests)
        # Imported styles must not recolor unrelated source elements, and SMIL
        # must fail its own journey instead of aborting the whole package.
        for name, content in (
            ('style', '<style>.paint{fill:red}</style><g id="mark"><rect class="paint" width="40" height="40"/></g>'),
            ('smil', '<g id="mark"><rect width="40" height="40"><animate attributeName="fill" values="red;blue" dur="1s" repeatCount="indefinite"/></rect></g>'),
            ('static', '<g id="mark"><rect width="40" height="40" fill="red"/></g>'),
        ):
            (owner / (name + '-sprite.svg')).write_text('<svg xmlns="http://www.w3.org/2000/svg">' + content + '</svg>')
            (owner / (name + '-sprite.html')).write_text('<!doctype html><svg width="40" height="40"><rect id="local" class="paint" width="40" height="40" fill="blue"/></svg><svg width="40" height="40"><use href="/' + name + '-sprite.svg#mark"/></svg>')
        (owner / 'inline-smil.html').write_text('<!doctype html><svg width="40" height="40"><rect width="40" height="40"><animate attributeName="fill" values="red;blue" dur="1s" repeatCount="indefinite"/></rect></svg>')
        names = ('style-sprite', 'smil-sprite', 'inline-smil', 'static-sprite')
        recipe = {'schema': 'ui-atlas.recipe/v1', 'id': 'sprite-boundaries', 'title': 'Sprite boundaries',
                  'source_files': [name + '.html' for name in names] + [name + '-sprite.svg' for name in ('style', 'smil', 'static')],
                  'journeys': [{'id': name, 'surface': 'Sprite', 'evidence': 'synthetic', 'viewport': {'width': 1000, 'height': 800},
                                'steps': [{'action': 'goto', 'url': '/' + name + '.html'}, {'action': 'frame', 'id': name, 'label': name}]} for name in names]}
        recipe_path = owner / 'sprite-recipe.json'; atlas.write_json(recipe_path, recipe)
        run = owner / 'sprite-boundary-run'
        result = subprocess.run([sys.executable, '-B', str(Path(atlas.__file__).with_name('capture.py')), str(recipe_path),
                                 '--source-root', str(owner), '--base-url', f'http://127.0.0.1:{server.server_port}',
                                 '--browser', str(browser_path), '--out', str(run)], capture_output=True, text=True)
        assert result.returncode == 2, result.stdout + result.stderr
        manifest = atlas.read_json(run / 'atlas.json')
        assert [frame['status'] for frame in manifest['frames']] == ['render-failed'] * 3 + ['rendered']
        for frame in manifest['frames'][:3]:
            assert 'Unsupported' in frame['reason']
            assert not (run / 'frames' / (frame['id'] + '.html')).exists()
        page.goto((run / 'index.html').as_uri()); page.wait_for_selector('[data-ready="true"]')
        assert page.locator('.artboard').count() == 1
        assert page.frame_locator('iframe').locator('#local').evaluate('el=>getComputedStyle(el).fill') == 'rgb(0, 0, 255)'
    finally:
        context.close(); server.shutdown(); server.server_close(); thread.join()


def check_pseudo_defaults(browser, owner):
    context = browser.new_context(viewport={'width': 1000, 'height': 800})
    page = context.new_page(); source = owner / 'pseudo-source.html'
    for count, positioned in ((1, False), (8, False), (8, True)):
        layout = 'html,body{width:1000px;height:800px;margin:0;font:16px/24px monospace}body{position:absolute;left:0;top:0}span{position:absolute;left:50px;width:80px;height:24px}#plain{position:absolute;left:700px;top:200px}' if positioned else ''
        source.write_text('<!doctype html><style>span::before,span::after{content:"|"}' + layout + '</style><button id="plain">Plain control</button>' + ''.join(f'<span style="top:{40+i*30}px">Item</span>' for i in range(count)))
        page.goto(source.as_uri())
        expected = page.locator('html,body,#plain,span').evaluate_all('nodes=>nodes.map(el=>[getComputedStyle(el,"::before").content,getComputedStyle(el,"::after").content])')
        name = f'pseudo-{count}-{int(positioned)}'; document = name + '.html'
        observed = capture_frame(page, [], owner / document)
        _, output, _ = build_view(owner, name, source, [frame_for(observed, document, 'one')])
        page.goto(output.as_uri()); page.wait_for_selector('[data-ready="true"]')
        actual = page.frame_locator('iframe').locator('html,body,#plain,span').evaluate_all('nodes=>nodes.map(el=>[getComputedStyle(el,"::before").content,getComputedStyle(el,"::after").content])')
        assert actual == expected, (name, actual, expected)
        search_select(page, 'Plain control', '#plain')
        assert page.locator('.selection-box').is_visible()
    context.close()


def check_projection(browser, owner, browser_path):
    check_scroll_restore(browser, owner)
    check_native_forms(browser, owner)
    check_embedded_resources(browser, owner, browser_path)
    check_pseudo_defaults(browser, owner)
    source = owner / 'projection-source.html'
    source.write_text('''<!doctype html><html><head><meta charset="utf-8"></head><body>
      <main id="contents" style="display:contents"><button id="target">Visible action</button></main>
      <div id="zero" style="height:0"><button id="fixed" style="position:fixed;left:260px;top:220px">Fixed child</button></div>
      <div style="display:none"><button id="hidden">Hidden child</button></div></body></html>''')
    context = browser.new_context(viewport={'width': 1000, 'height': 800})
    page = context.new_page(); page.goto(source.as_uri())
    observed = capture_frame(page, [], owner / 'projection-frame.html')
    elements = {node['selector']: node for node in observed['elements']}
    assert not elements['#contents']['visible'] and not elements['#zero']['visible']
    path, output, _ = build_view(owner, 'projection', source, [frame_for(observed, 'projection-frame.html', 'one')])
    page.goto(output.as_uri()); page.wait_for_selector('[data-ready="true"]')
    for selector, query in [('#target', 'Visible action'), ('#fixed', 'Fixed child')]:
        search_select(page, query, selector)
        page.locator('#search').fill(''); page.locator('[data-panel="layers"]').click()
        row = page.locator(f'.layer-item[data-node="{elements[selector]["id"]}"]')
        assert row.is_visible() and row.get_attribute('aria-selected') == 'true'
        row.click(); assert page.locator('.selection-box').is_visible()
    for selector in ('#contents', '#zero', '#hidden'):
        assert page.locator(f'.layer-item[data-node="{elements[selector]["id"]}"]').count() == 0

    document = owner / 'projection-frame.html'
    original = document.read_text()
    # Markup-looking comments, attributes, raw style text and non-BMP Unicode
    # must not become bootstrap insertion points or change JS string offsets.
    changed = original.replace('<head>', '<!-- 🧭 <head> -->\r\n<HEAD data-note="🧭\u2028<head>">')
    changed = changed.replace('</head>', '<style>/* </body> */</style></HEAD>')
    changed = changed.replace('</body>', '<!-- 🧭 </body> --></BODY>')
    assert changed != original
    document.write_text(changed)
    atlas.package(path, output)
    requests = []; page.on('request', lambda request: requests.append(request.url))
    page.goto(output.as_uri()); page.wait_for_selector('[data-ready="true"]')
    search_select(page, 'Visible action', '#target')
    assert page.locator('.selection-box').is_visible()
    dom = page.frame_locator('iframe')
    assert dom.locator('head > meta[http-equiv="Content-Security-Policy"]').count() == 1
    assert dom.locator('body > script[nonce]').count() == 1
    assert not any(url.startswith(('http:', 'https:')) for url in requests)
    # A dynamic region must retain its explicit unavailable status in navigation.
    source.write_text('<!doctype html><button class="action">Original action</button>')
    page.goto(source.as_uri()); definitions = [{'id': 'action', 'label': 'Action', 'selector': '.action'}]
    one = capture_frame(page, definitions, owner / 'region-one.html')
    page.evaluate('document.body.insertAdjacentHTML("afterbegin",\'<button class="action">Other action</button>\')')
    two = capture_frame(page, definitions, owner / 'region-two.html')
    assert two['regions'][0]['rect'] is None and 'multiple' in two['regions'][0]['reason']
    _, output, _ = build_view(owner, 'region-ambiguity', source,
        [frame_for(one, 'region-one.html', 'one'), frame_for(two, 'region-two.html', 'two')])
    page.goto(output.as_uri()); page.wait_for_function('document.querySelectorAll("[data-ready=true]").length===2')
    page.locator('[data-state="one"]').click(); page.locator('#regions button').click()
    page.wait_for_function('document.querySelector("#selected-selector").textContent!==""')
    page.locator('#next').click()
    page.wait_for_function('document.querySelector("#comparison-status").textContent.includes("대응 요소 없음")')
    assert page.locator('.selection-box').is_hidden()
    page.locator('#previous').click(); page.wait_for_function('document.querySelector("#selected-selector").textContent!==""')

    # SMIL can change color without tripping geometry guards. Refuse the state
    # explicitly, while static SVG remains materializable and selectable.
    source.write_text('<!doctype html><svg width="200" height="120"><rect id="shape" width="180" height="100" fill="red"><animate attributeName="fill" values="red;blue;red" dur="0.6s" repeatCount="indefinite"/></rect></svg>')
    page.goto(source.as_uri())
    try:
        capture_frame(page, [], owner / 'animated.svg.html')
        raise AssertionError('Animated SVG was silently accepted as a frozen frame')
    except Exception as error:
        assert 'Unsupported rendering surface: animate' in str(error), str(error)
    page.locator('animate').evaluate('el=>el.remove()')
    static = capture_frame(page, [], owner / 'static-svg.html')
    assert next(node for node in static['elements'] if node['selector'] == '#shape')['visible']
    context.close()
    print('Projection checks passed: instant window/container scroll restoration, native controls, selected-file refusal, embedded image inputs/sprite references, partial canvas after sprite/inline refusals, pseudo-default isolation, visible descendants, hidden-node exclusion, parsed bootstrap/Unicode boundaries and unavailable-region correspondence.')
