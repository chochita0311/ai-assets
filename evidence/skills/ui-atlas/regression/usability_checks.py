"""Synthetic witnesses for drafts, clipping, large sheets/search and narrow layout."""
import copy
import json

import atlas
from capture import capture_frame
from viewer_checks import camera


def check_usability(browser, owner):
    source = owner / "usability-source.html"
    source.write_text('''<!doctype html><html lang="en"><meta charset="utf-8"><style>
      body {margin:20px;font:14px/20px sans-serif}
      #flow p {margin:0 0 16px} #flow {max-width:500px}
      #partial {width:90px;white-space:nowrap;overflow:hidden;margin:0}
      #clip {height:24px;overflow:hidden} #hidden {margin-top:80px}
      #outside {position:absolute;top:5000px}
      #items {display:grid;grid-template-columns:repeat(20,1fr);font:9px/14px sans-serif}
      table {border-collapse:collapse} td {border:1px solid;padding:2px}
      </style><body><div id="flow"><p>Margin collapse witness</p></div><button id="after-flow">Following button</button>
      <p id="a">Draft alpha</p><p id="b">Draft beta</p>
      <p id="partial">Partially clipped quote must retain its qualification</p>
      <div id="clip"><span>Visible in clipping parent</span><p id="hidden">Hidden by ancestor</p></div>
      <p id="outside">Outside viewport</p><p style="opacity:0">Invisible opacity</p>
      <div style="display:flex;gap:8px"><button disabled>Disabled control</button><span>Flex sibling</span></div>
      <table><tr><td>Table sizing</td><td>Second cell</td></tr></table>
      <div id="items">''' + ''.join(f'<span id="item-{i}">Match {i:03}</span>' for i in range(420)) + '</div></body></html>')
    context = browser.new_context(viewport={"width": 1000, "height": 800})
    page = context.new_page(); page.goto(source.as_uri())
    observed = capture_frame(page, [], owner / "usability-frame.html")
    elements = {element["selector"]: element for element in observed["elements"]}
    assert not elements["#outside"]["visible"] and not elements["#hidden"]["visible"]
    assert elements["#a"]["visibleRect"] == elements["#a"]["rect"]
    assert any(t["selector"] == "#partial" and t["clipped"] for t in observed["texts"])
    frame = {"id": "one", "label": "Witness", "surface": "Fixture", "journey": "observe", "status": "rendered",
             "evidence": "synthetic", "document": "usability-frame.html", **observed}
    manifest = {"schema": "ui-atlas/v2", "id": "usability", "title": "Synthetic usability",
                "scope": "Known regression cases only", "captured_at": atlas.now(),
                "source": atlas.source_identity(owner, [source.name]), "frames": [frame]}
    path = owner / "usability.json"; path.write_text(json.dumps(manifest))
    atlas.package(path, owner / "usability.html")
    view = context.new_page(); view.goto((owner / "usability.html").as_uri())
    view.wait_for_selector('[data-ready="true"]')

    def select(selector, query):
        if view.locator('#sidebar').is_hidden(): view.locator('#toggle-sidebar').click()
        view.locator('[data-panel="screens"]').click()
        view.locator('#search').fill(query)
        view.locator(f'.search-result[data-node-result="{elements[selector]["id"]}"]').click()
        view.wait_for_function('s => document.querySelector("#selected-selector").textContent === s', arg=selector)

    select('#a', 'Draft alpha'); view.locator('#note').fill('Owned by alpha')
    select('#b', 'Draft beta'); assert view.locator('#note').input_value() == ''
    view.locator('#note').fill('Owned by beta')
    view.locator('#note-kind').select_option('observation')
    view.locator('#close-inspector').click()
    select('#a', 'Draft alpha'); assert view.locator('#note').input_value() == 'Owned by alpha'
    view.locator('#note-form button').click()
    select('#b', 'Draft beta'); assert view.locator('#note').input_value() == 'Owned by beta'
    assert view.locator('#note-kind').input_value() == 'observation'
    view.locator('#note-form button').click()
    select('#partial', 'Partially clipped quote')
    assert view.locator('#quote-limit').is_visible()
    view.locator('#note').fill('Clipped evidence'); view.locator('#note-form button').click()
    view.locator('#file-menu-button').click()
    with view.expect_download() as exported: view.locator('#notes-download').click()
    download = owner / 'usability-notes.json'; exported.value.save_as(download)
    notes = json.loads(download.read_text())['notes']
    assert [(note['selector'], note['message']) for note in notes] == [('#a', 'Owned by alpha'), ('#b', 'Owned by beta'), ('#partial', 'Clipped evidence')]
    assert notes[2]['clipped'] is True and notes[2]['quote'].endswith('qualification')
    assert notes[0]['clipped'] is False
    view.locator('#requests').click(); view.locator('#collect-notes').click()
    assert '화면에는 일부만 보였으며' in view.locator('#handoff-text').input_value()
    view.locator('#close-handoff').click()
    assert '화면에는 문구 일부만 보입니다.' in view.locator('#review-list').inner_text()
    view.locator('[data-panel="screens"]').click(); view.locator('#search').fill('Outside viewport')
    assert view.locator('.search-result').count() == 0
    view.locator('#search').fill('Hidden by ancestor'); assert view.locator('.search-result').count() == 0
    view.locator('#search').fill('Match ')
    assert view.locator('.search-result').count() == 200
    view.locator('#search').press('Enter')
    view.wait_for_function('document.querySelector("#selected-selector").textContent === "#item-0"')
    view.get_by_role('button', name='다음 결과', exact=True).click()
    view.locator('#search').press('Enter')
    view.wait_for_function('document.querySelector("#selected-selector").textContent === "#item-200"')
    view.get_by_role('button', name='다음 결과', exact=True).click()
    assert view.locator('.search-result').count() == 20
    view.locator(f'.search-result[data-node-result="{elements["#item-419"]["id"]}"]').click()
    view.wait_for_function('document.querySelector("#selected-selector").textContent === "#item-419"')
    # Programmatic selection is also bounded by the bridge, even for old inventories.
    assert view.frame_locator('iframe').locator('#outside').evaluate(
        '(el) => { /* ATLAS_GEOMETRY */ return geometry.clip(el.getBoundingClientRect(), el); }'.replace(
            '/* ATLAS_GEOMETRY */', (atlas.ASSETS / 'geometry.js').read_text())) is None
    view.set_viewport_size({'width': 390, 'height': 844})
    select('#a', 'Draft alpha'); view.wait_for_timeout(100)
    bounds = view.locator('#canvas').bounding_box(); inspector = view.locator('#inspector').bounding_box()
    assert bounds['width'] == 390 and bounds['height'] > 250
    assert bounds['y'] + bounds['height'] <= inspector['y'] + 1
    selection = view.locator('.selection-box').bounding_box()
    assert bounds['y'] <= selection['y'] <= bounds['y'] + bounds['height']
    assert view.evaluate('document.documentElement.scrollWidth <= innerWidth')
    view.locator('[data-tab="payload"]').click(); assert '"state": "one"' in view.locator('#payload').inner_text()
    view.locator('[data-tab="element"]').click(); view.locator('#note').fill('Narrow note')
    view.locator('#note-form button').click(); assert view.locator('#note-count').inner_text() == '4'
    view.locator('#fit-all').click()
    context.close()

    # Native top-layer UI escapes overflow ancestors without escaping its own bounds.
    nested = owner / 'nested-dialog.html'
    nested.write_text('<!doctype html><div style="width:100px;height:40px;overflow:hidden"><dialog id="nested"><p>Nested modal</p><button id="nested-action">Nested modal action</button></dialog></div>')
    context = browser.new_context(viewport={"width": 1000, "height": 800})
    page = context.new_page(); page.goto(nested.as_uri())
    page.evaluate('document.querySelector("#nested").showModal()')
    modal = capture_frame(page, [], owner / 'nested-frame.html')
    modal_nodes = {node['selector']: node for node in modal['elements']}
    assert modal_nodes['#nested']['visible'] and modal_nodes['#nested-action']['visible']
    assert any(text['text'] == 'Nested modal action' for text in modal['texts'])
    manifest['id'] = 'nested-modal'
    manifest['source'] = atlas.source_identity(owner, [nested.name])
    manifest['frames'] = [{**frame, **modal, 'document': 'nested-frame.html'}]
    path.write_text(json.dumps(manifest)); atlas.package(path, owner / 'nested.html')
    page.goto((owner / 'nested.html').as_uri()); page.wait_for_selector('[data-ready="true"]')
    page.locator('#search').fill('Nested modal action')
    page.locator('.search-result[data-node-result]').click()
    page.wait_for_function('document.querySelector("#selected-selector").textContent === "#nested-action"')
    page.wait_for_timeout(100)
    box = page.locator('.selection-box').bounding_box()
    page.mouse.click(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2)
    page.wait_for_function('document.querySelector("#selected-selector").textContent === "#nested-action"')
    assert page.frame_locator('iframe').locator('#nested').evaluate('e => e.matches(":modal")')
    context.close()

    # Large-sheet stress uses explicitly repeated synthetic fixtures, not claimed app coverage.
    context = browser.new_context(viewport={"width": 1440, "height": 1000})
    small_source = owner / 'small-source.html'; small_source.write_text('<!doctype html><p>Small DOM for sheet stress</p>')
    manifest['source'] = atlas.source_identity(owner, [small_source.name])
    page = context.new_page(); page.goto(small_source.as_uri())
    small = capture_frame(page, [], owner / 'small-frame.html')
    base = {**frame, **small, 'document': 'small-frame.html'}
    for name, grouping in [('rows', 5), ('long-row', 100)]:
        manifest['id'] = 'stress-' + name
        manifest['frames'] = [{**copy.deepcopy(base), 'id': f'frame-{i}', 'journey': f'group-{i // grouping}'} for i in range(100)]
        path.write_text(json.dumps(manifest)); atlas.package(path, owner / 'stress.html')
        page.goto((owner / 'stress.html').as_uri())
        page.wait_for_function('document.querySelectorAll("[data-ready=true]").length === 100')
        page.locator('#fit-all').click(); page.wait_for_timeout(100)
        assert camera(page)['zoom'] < .06
        outside = page.evaluate('''() => {const box=document.querySelector('#canvas').getBoundingClientRect();
          return [...document.querySelectorAll('.artboard')].filter(el=>{const r=el.getBoundingClientRect();
            return r.left<box.left||r.right>box.right||r.top<box.top||r.bottom>box.bottom;}).length;}''')
        assert outside == 0, (name, outside)
        assert page.locator('#zoom-value').inner_text() != '0%'
    context.close()
    print('Usability checks passed: target-owned drafts, clipped quotes, 420-result pagination, hidden-element exclusion, 390px inspector, 100-frame row/column fit, auto-height geometry.')
