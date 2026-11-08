"""Failure/recovery witnesses: storage, clipping, comparison and evidence drift."""
import json

import atlas
from capture import capture_frame
from viewer_checks import camera, set_zoom


def check_note_recovery(browser, owner):
    source = owner / 'storage.html'; source.write_text('<!doctype html><title>Storage witness</title>')
    context = browser.new_context(); page = context.new_page(); page.goto(source.as_uri())
    page.add_script_tag(content=(atlas.ASSETS / 'notes.js').read_text())
    result = page.evaluate('''() => {
      const errors=[], notes=new AtlasNotes('storage-witness',()=>{},e=>errors.push(e));
      const make=id=>({id,frame:'one',identity:'observed',message:id,created_at:id});
      const ids=()=>notes.export().notes.map(n=>n.id).sort().join(',');
      const assert=(ok,label)=>{if(!ok)throw new Error(label);};
      const set=Storage.prototype.setItem, remove=Storage.prototype.removeItem, get=Storage.prototype.getItem;
      let quota=false, failAdd=false, failDelete=false, failRead=false;
      Storage.prototype.setItem=function(key,value){
        if(key.startsWith(notes.prefix) && (failAdd && key.endsWith(':pending') || quota && !get.call(this,key) && this.length>=1))
          throw new DOMException('Synthetic quota failure','QuotaExceededError');
        return set.call(this,key,value);
      };
      Storage.prototype.removeItem=function(key){
        if(failDelete && key.endsWith(':pending'))throw new DOMException('Synthetic delete failure','SecurityError');
        return remove.call(this,key);
      };
      Storage.prototype.getItem=function(key){
        if(failRead)throw new DOMException('Synthetic read failure','SecurityError');
        return get.call(this,key);
      };
      const update=()=>window.dispatchEvent(new StorageEvent('storage',{key:notes.prefix+'other'}));
      try {
        assert(notes.change([make('old')]),'normal save');
        quota=true;
        assert(!notes.change([make('pending')]),'quota must report failure');
        assert(ids()==='old,pending','failed addition remains exportable');
        update(); assert(ids()==='old,pending','storage event retains pending opinion');
        assert(notes.change([],['old']),'deletion frees quota and retries pending addition');
        assert(ids()==='pending' && JSON.parse(get.call(localStorage,notes.prefix+'pending')).id==='pending','pending survives recovery');
        quota=false; failAdd=true;
        assert(!notes.change([{...make('pending'),message:'Latest unsaved edit'}]),'failed edit');
        assert(!notes.change([make('other')]),'unrelated successful write must not mask failed edit');
        set.call(localStorage,notes.prefix+'external',JSON.stringify(make('external'))); update();
        assert(ids()==='external,other,pending','merge external note without dropping pending edit');
        assert(notes.items.find(n=>n.id==='pending').message==='Latest unsaved edit','failed edit wins over old stored bytes');
        failRead=true; update(); assert(ids()==='external,other,pending','read failure retains visible memory');
        failRead=false; failAdd=false;
        assert(notes.change(),'retry flushes pending edit');
        assert(JSON.parse(get.call(localStorage,notes.prefix+'pending')).message==='Latest unsaved edit','recovered stored bytes');
        failDelete=true;
        assert(!notes.change([],['pending']),'delete failure'); update();
        assert(ids()==='external,other','pending deletion is not resurrected by storage event');
        failDelete=false; assert(notes.change(),'retry deletion');
        assert(get.call(localStorage,notes.prefix+'pending')===null,'recovered deletion');
        assert(notes.export().schema==='ui-atlas.notes/v1','portable schema retained');
        return {errors:errors.length,notes:ids()};
      } finally {
        Storage.prototype.setItem=set; Storage.prototype.removeItem=remove; Storage.prototype.getItem=get;
      }
    }''')
    assert result['errors'] >= 4 and result['notes'] == 'external,other'
    context.close()


def build_view(owner, name, source, frames):
    manifest = {'schema': 'ui-atlas/v2', 'id': name, 'title': 'Synthetic ' + name,
                'scope': 'Bounded failure and recovery witnesses', 'captured_at': atlas.now(),
                'source': atlas.source_identity(owner, [source.name]), 'frames': frames}
    path = owner / (name + '.json'); atlas.write_json(path, manifest)
    output = owner / (name + '.html')
    return path, output, atlas.package(path, output)


def frame_for(observed, document, state):
    return {'id': state, 'label': state, 'surface': 'Fixture', 'journey': 'compare',
            'status': 'rendered', 'evidence': 'synthetic', 'document': document, **observed}


def search_select(page, query, selector):
    if page.locator('#sidebar').is_hidden(): page.locator('#toggle-sidebar').click()
    page.locator('[data-panel="screens"]').click()
    page.locator('#search').fill(query)
    page.locator('.search-result[data-node-result]').first.click()
    page.wait_for_function('s=>document.querySelector("#selected-selector").textContent===s', arg=selector)
    page.wait_for_timeout(80)


def check_fixed_geometry(browser, owner):
    source = owner / 'fixed-source.html'
    source.write_text('''<!doctype html><html><style>
      body {margin:0;font:14px/20px sans-serif}
      .clip {position:relative;width:100px;height:40px;overflow:hidden;margin:20px}
      .escaped {position:fixed;left:300px;top:300px;width:200px;height:40px}
      #absolute {position:absolute;left:300px;top:100px;width:200px;height:40px}
      #fixed-box {position:fixed;left:300px;top:400px;width:100px;height:25px;overflow:hidden}
      #inside-hidden {display:block;margin-top:80px}
      </style><body><div class="clip">
      <button class="escaped" id="target"><span id="fixed-child">Fixed overlay</span><svg id="fixed-icon" width="16" height="16"><circle cx="8" cy="8" r="6" /></svg></button>
      <button id="absolute">Clipped absolute</button>
      <div id="fixed-box">Visible box<span id="inside-hidden">Clipped inside fixed</span></div>
      </div>''' + ''.join(f'<div class="clip" style="{rule}"><button class="escaped" id="bound-{index}">Bounded overlay {index}</button></div>'
                         for index, rule in enumerate(('transform:translateZ(0)', 'filter:blur(0px)', 'contain:layout', 'contain:paint', 'will-change:transform', 'content-visibility:auto'))) + '</body></html>')
    context = browser.new_context(viewport={'width': 1000, 'height': 800})
    page = context.new_page(); page.goto(source.as_uri())
    assert page.evaluate("document.elementFromPoint(310,310).closest('button')?.id") == 'target'
    observed = capture_frame(page, [], owner / 'fixed-frame.html')
    elements = {node['selector']: node for node in observed['elements']}
    for selector in ('#target', '#fixed-child', '#fixed-icon', '#fixed-box'):
        assert elements[selector]['visible'] and elements[selector]['visibleRect'], selector
    for selector in ('#absolute', '#inside-hidden', *(f'#bound-{i}' for i in range(6))):
        assert not elements[selector]['visible'] and elements[selector]['visibleRect'] is None, selector
    assert any(text['text'] == 'Fixed overlay' for text in observed['texts'])
    assert not any('Bounded overlay' in text['text'] or 'Clipped' in text['text'] for text in observed['texts'])
    _, output, _ = build_view(owner, 'fixed-geometry', source, [frame_for(observed, 'fixed-frame.html', 'one')])
    page.goto(output.as_uri()); page.wait_for_selector('[data-ready="true"]')
    search_select(page, 'Fixed overlay', '#fixed-child')
    assert page.locator('.selection-box').is_visible()
    box = page.locator('.selection-box').bounding_box()
    page.mouse.click(box['x'] + box['width'] / 2, box['y'] + box['height'] / 2)
    page.wait_for_function('document.querySelector("#selected-selector").textContent==="#fixed-child"')
    context.close()


def check_absolute_geometry(browser, owner):
    source = owner / 'absolute-source.html'
    wrapped = '<div id="outer"><div id="clip"><button id="target">Absolute target</button></div></div>'
    cases = [
        ('escape-' + overflow, '#outer{position:relative}#clip{height:40px;width:100px;overflow:' + overflow + '}', wrapped, True)
        for overflow in ('hidden', 'clip', 'auto', 'scroll')
    ] + [
        ('relative', '#clip{position:relative;height:40px;width:100px;overflow:hidden}', wrapped, False),
        ('transformed', '#clip{transform:translateZ(0);height:40px;width:100px;overflow:hidden}', wrapped, False),
        ('body-viewport', 'body{overflow:hidden;height:0;position:relative}', '<button id="target">Absolute target</button>', True),
        ('body-clipped', 'html{overflow:hidden}body{overflow:hidden;height:0;position:relative}', '<button id="target">Absolute target</button>', False),
        ('root-viewport', 'html{overflow:hidden;height:0}', '<button id="target">Absolute target</button>', True),
        ('contents', '#clip{position:relative;height:40px;width:100px;overflow:hidden}#contents{display:contents;position:absolute}',
         '<div id="clip"><div id="contents"><button id="target" style="position:static;margin-left:300px;margin-top:200px">Absolute target</button></div></div>', False),
    ]
    context = browser.new_context(viewport={'width': 1000, 'height': 800})
    page = context.new_page()
    for name, css, content, visible in cases:
        source.write_text('<!doctype html><html><head><style>body{margin:0}#target{position:absolute;left:300px;top:200px;width:100px;height:30px}' + css + '</style></head><body>' + content + '</body></html>')
        page.goto(source.as_uri())
        hit = page.locator('#target').evaluate('el=>{const r=el.getBoundingClientRect();return document.elementFromPoint(r.x+10,r.y+10)?.id==="target"}')
        assert hit == visible, name
        document = 'absolute-' + name + '.html'
        observed = capture_frame(page, [], owner / document)
        target = next(node for node in observed['elements'] if node['selector'] == '#target')
        assert target['visible'] == visible and bool(target['visibleRect']) == visible, name
        assert any(text['text'] == 'Absolute target' for text in observed['texts']) == visible, name
        if visible:
            _, output, _ = build_view(owner, 'absolute-view-' + name, source, [frame_for(observed, document, 'one')])
            page.goto(output.as_uri()); page.wait_for_selector('[data-ready="true"]')
            search_select(page, 'Absolute target', '#target')
            assert page.locator('.selection-box').is_visible(), name
    context.close()


def check_comparison_and_freshness(browser, owner):
    source = owner / 'comparison-source.html'
    original = '<!doctype html><style>body{margin:30px}button{margin:100px;width:180px;height:40px}</style><button id="target">Review target</button>'
    source.write_text(original)
    context = browser.new_context(viewport={'width': 1000, 'height': 800})
    page = context.new_page(); page.goto(source.as_uri())
    observed = capture_frame(page, [], owner / 'comparison-frame.html')
    page.locator('#target').evaluate('el=>{el.style.marginLeft="220px";el.style.marginTop="160px";}')
    moved = capture_frame(page, [], owner / 'moved-frame.html')
    page.locator('#target').evaluate('el=>el.remove()')
    missing = capture_frame(page, [], owner / 'missing-frame.html')
    frames = [frame_for(observed, 'comparison-frame.html', 'one'),
              frame_for(moved, 'moved-frame.html', 'two'),
              frame_for(missing, 'missing-frame.html', 'missing')]
    path, output, packaged = build_view(owner, 'comparison-freshness', source, frames)
    identities = [frame['identity'] for frame in packaged['frames']]
    for width, height in ((1440, 1000), (390, 844)):
        page.set_viewport_size({'width': width, 'height': height}); page.goto(output.as_uri())
        page.wait_for_function('document.querySelectorAll("[data-ready=true]").length===3')
        search_select(page, 'Review target', '#target')
        set_zoom(page, 150)
        before = page.locator('.selection-box').bounding_box()
        page.locator('#next').click()
        page.wait_for_function('document.querySelector("#state-label").textContent==="two" && document.querySelector("#selected-selector").textContent==="#target"')
        page.wait_for_timeout(100)
        after = page.locator('.selection-box').bounding_box()
        assert camera(page)['zoom'] == 1.5, (width, camera(page))
        assert max(abs(before[key] - after[key]) for key in ('x', 'y', 'width', 'height')) < 1, (width, before, after)
        page.locator('#next').click()
        page.wait_for_function('document.querySelector("#comparison-status").textContent.includes("대응 요소 없음")')
        assert camera(page)['zoom'] == 1.5 and page.locator('.selection-box').is_hidden()
        page.locator('#previous').click()
        page.wait_for_function('document.querySelector("#selected-selector").textContent==="#target"')
        page.wait_for_timeout(100)
        assert camera(page)['zoom'] == 1.5
        recovered = page.locator('.selection-box').bounding_box()
        assert max(abs(after[key] - recovered[key]) for key in ('x', 'y', 'width', 'height')) < 1, (width, after, recovered)

    page.set_viewport_size({'width': 1440, 'height': 1000})
    page.locator('#note').fill('Recheck this observed copy'); page.locator('#note-form button').click()
    page.locator('#requests').click()
    page.locator('#review-filter').select_option('stale')
    assert page.locator('#review-list .review-item').count() == 0
    prior = owner / 'prior-notes.json'
    prior.write_text(json.dumps({'schema': 'ui-atlas.notes/v1', 'atlas': 'comparison-freshness', 'notes': [
        {'id': 'prior-identity', 'frame': 'one', 'identity': 'earlier-evidence', 'message': 'Older observation note'},
        {'id': 'prior-frame', 'frame': 'removed', 'identity': 'earlier-evidence', 'message': 'Removed frame note'}]}))
    page.locator('#import-file').set_input_files(prior)
    page.wait_for_function('document.querySelector("#note-count").textContent==="3"')
    cases = [('changed', original.replace('Review target', 'Updated target')),
             ('unavailable', None), ('matched', original)]
    for status, content in cases:
        if content is None: source.unlink()
        else: source.write_text(content)
        rebuilt = atlas.package(path, output)
        assert rebuilt['freshness']['status'] == status
        assert [frame['identity'] for frame in rebuilt['frames']] == identities, 'Current checks must not forge new observation identities'
        page.reload(); page.wait_for_function('document.querySelectorAll("[data-ready=true]").length===3')
        assert page.locator('#note-count').inner_text() == '3'
        page.locator('#requests').click(); page.locator('#review-filter').select_option('stale')
        assert page.locator('#review-list .review-item').count() == (2 if status == 'matched' else 3)
        for message, warning in [('Older observation note', '저장 당시와 관찰 근거가 달라졌습니다.'),
                                 ('Removed frame note', '현재 전개도에 이 화면이 없습니다.')]:
            assert warning in page.locator('#review-list .review-item').filter(has_text=message).inner_text()
        reason = {'changed': '현재 소스·재현 파일이 관찰 당시와 다릅니다.',
                  'unavailable': '현재 소스·재현 파일을 확인할 수 없습니다.'}.get(status)
        if reason:
            current = page.locator('#review-list .review-item').filter(has_text='Recheck this observed copy')
            assert reason in current.locator('.stale').inner_text()
            current.get_by_role('button', name='위치 보기', exact=True).click()
            assert reason in page.locator('#frame-notes .stale').inner_text()
            page.wait_for_selector('.stale-pin')
            page.locator('#requests').click()
        else:
            assert page.locator('.stale-pin').count() > 0, 'Identity warning remains after matching source check'
        page.locator('#collect-notes').click(); text = page.locator('#handoff-text').input_value()
        if reason: assert '재확인: ' + reason in text
        assert text.count('재확인:') == (3 if reason else 2)
        page.locator('#close-handoff').click()

    # The real form must retain a failed save for export and warn before closing.
    search_select(page, 'Review target', '#target')
    page.evaluate('''() => {
      window.restoreNoteWrite=Storage.prototype.setItem;
      Storage.prototype.setItem=function(key,value){
        if(key.startsWith('ui-atlas:notes:'))throw new DOMException('Synthetic quota failure','QuotaExceededError');
        return window.restoreNoteWrite.call(this,key,value);
      };
    }''')
    page.locator('#note').fill('Unsaved form opinion'); page.locator('#note-form button').click()
    assert page.locator('#note-count').inner_text() == '4' and page.locator('#note').input_value() == ''
    unload = '() => {const e=new Event("beforeunload",{cancelable:true});window.dispatchEvent(e);return e.defaultPrevented;}'
    assert page.evaluate(unload), 'Failed saved-note write needs the unsaved-work guard'
    page.locator('#file-menu-button').click()
    with page.expect_download() as downloaded: page.locator('#notes-download').click()
    export = owner / 'failed-save-notes.json'; downloaded.value.save_as(export)
    assert any(note['message'] == 'Unsaved form opinion' for note in json.loads(export.read_text())['notes'])
    page.evaluate('() => {Storage.prototype.setItem=window.restoreNoteWrite;}')
    page.locator('#note').fill('Recovery opinion'); page.locator('#note-form button').click()
    assert page.locator('#note-count').inner_text() == '5'
    assert not page.evaluate(unload), 'Successful retry must clear the pending-work guard'
    page.reload(); assert page.locator('#note-count').inner_text() == '5'
    context.close()


def check_reliability(browser, owner):
    check_note_recovery(browser, owner)
    check_fixed_geometry(browser, owner)
    check_absolute_geometry(browser, owner)
    check_comparison_and_freshness(browser, owner)
    print('Reliability checks passed: quota/read/delete recovery, external-note merge, fixed/absolute overlays and containment, viewport/body overflow, 390px comparison zoom/anchor, changed/unavailable note warnings with unchanged observed identities.')
