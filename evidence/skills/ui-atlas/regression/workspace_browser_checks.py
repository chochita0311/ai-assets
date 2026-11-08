"""Synthetic workspace entry, sheet switching, history and draft-lifetime witnesses."""
import copy
import json
import shutil

import atlas
import workspace


def active_sheet(page, key=None):
    if key:
        page.wait_for_function('key=>document.querySelector(".atlas-host.active")?.dataset.run===key', arg=key)
    locator=page.locator('.atlas-host.active')
    frame=locator.element_handle().content_frame()
    frame.wait_for_selector('#sheet-picker:not([hidden])',state='attached')
    if page.viewport_size['width']>560 and frame.locator('#sheet-picker').is_hidden():
        print('Unexpected hidden desktop selector:',frame.evaluate("()=>({width:innerWidth,height:innerHeight,sidebarHidden:document.querySelector('#sidebar').hidden,body:document.body.className})"),flush=True)
        frame.wait_for_selector('#sheet-picker',timeout=3000)
    return frame


def choose_sheet(page, key):
    active_sheet(page).locator('#sheet-select').select_option(key)
    return active_sheet(page,key)


def select_results(frame):
    frame.locator('[data-state="loaded"]').click()
    frame.locator('#regions button').filter(has_text='Results').click()
    frame.wait_for_function("document.querySelector('#selected-selector').textContent==='#results'")


def guarded(page):
    return page.evaluate('''()=>{const e=new Event('beforeunload',{cancelable:true});window.dispatchEvent(e);return e.defaultPrevented;}''')


def check_workspace_navigation(browser, owner):
    root=workspace.initialize(owner/'workspace-consumer')
    original=atlas.read_json(owner/'run/atlas.json')
    keys={}
    old_a=None
    for suffix in ('b','c','d','e','a','a'):
        ident='workspace-'+suffix
        run=workspace.reserve(root,ident)
        shutil.copytree(owner/'run/frames',run/'frames')
        data=copy.deepcopy(original);data['id']=ident;data['title']=('First sheet' if suffix=='a' else 'Sheet '+suffix.upper())
        if suffix=='b':data['journey_failures']=[{'id':'synthetic-after-frame','surface':'Notes','reason':'Synthetic terminal failure'}]
        data['freshness']=atlas.check_sources(data)
        atlas.write_json(run/'atlas.json',data);atlas.package(run/'atlas.json',run/'index.html')
        if suffix=='a' and old_a is None:old_a=run.name
        keys[suffix]=run.name
    pending=workspace.reserve(root,'workspace-pending')
    corrupt=workspace.reserve(root,'workspace-bad');(corrupt/'atlas.json').write_text('{broken');(corrupt/'index.html').write_text('Preserved old output')
    workspace.catalog(root)
    context=browser.new_context(viewport={'width':1440,'height':1000},accept_downloads=True)
    page=context.new_page();errors=[];requests=[]
    page.on('pageerror',lambda e:errors.append(str(e)))
    page.on('request',lambda r:requests.append(r.url) if r.url.startswith(('http:','https:')) else None)
    try:
        page.goto((root/'index.html').as_uri())
        first=active_sheet(page,keys['a'])
        assert page.locator('#workspace-fallback').is_hidden()
        assert first.locator('#sheet-select option').count()==6
        order=first.evaluate('''()=>({picker:document.querySelector('#sheet-picker').getBoundingClientRect().bottom,tabs:document.querySelector('#sidebar>.panel-tabs').getBoundingClientRect().top})''')
        assert order['picker']<=order['tabs']
        select_results(first)
        first.locator('#note-kind').select_option('observation');first.locator('#note').fill('Draft A belongs to Results')
        second=choose_sheet(page,keys['b']);select_results(second)
        assert second.locator('#note').input_value()=='' and second.locator('#note-count').inner_text()=='0'
        second.locator('#note').fill('Draft B belongs to Results')
        for suffix in ('c','d','e'):choose_sheet(page,keys[suffix])
        assert page.locator('.atlas-host').count()<=5, 'Only dirty sheets and a bounded clean cache remain mounted'
        first=choose_sheet(page,keys['a'])
        assert first.locator('#selected-selector').text_content()=='#results'
        assert first.locator('#note').input_value()=='Draft A belongs to Results'
        assert first.locator('#note-kind').input_value()=='observation'
        assert guarded(page),'Hidden drafts also guard the root page'

        # A failed browser save must stay pinned even after its textarea is cleared.
        first.evaluate('''()=>{window.realSetItem=Storage.prototype.setItem;Storage.prototype.setItem=function(k,v){if(k.startsWith('ui-atlas:notes:workspace-a:'))throw new DOMException('synthetic quota','QuotaExceededError');return realSetItem.call(this,k,v);};}''')
        first.locator('#note-form button').click()
        first.wait_for_function("document.querySelector('#note-count').textContent==='1'")
        assert first.locator('#note').input_value()==''
        for suffix in ('c','d','e'):choose_sheet(page,keys[suffix])
        first=choose_sheet(page,keys['a'])
        assert 'Draft A belongs to Results' in first.locator('#frame-notes').inner_text()
        first.locator('#file-menu-button').click()
        assert first.locator('#retry-notes').is_visible()
        with page.expect_download() as download:first.locator('#notes-download').click()
        exported=owner/'workspace-pending-note.json';download.value.save_as(exported)
        assert json.loads(exported.read_text())['notes'][0]['message']=='Draft A belongs to Results'
        second=choose_sheet(page,keys['b'])
        assert second.locator('#note').input_value()=='Draft B belongs to Results'
        second.locator('#note-form button').click()
        first=choose_sheet(page,keys['a'])
        first.evaluate('()=>{Storage.prototype.setItem=window.realSetItem;}')
        first.locator('#file-menu-button').click();first.locator('#retry-notes').click()
        first.wait_for_function("document.querySelector('#retry-notes').hidden")
        page.wait_for_function('''()=>{const e=new Event('beforeunload',{cancelable:true});window.dispatchEvent(e);return !e.defaultPrevented;}''')
        for suffix in ('c','d','e'):choose_sheet(page,keys[suffix])
        second=choose_sheet(page,keys['b'])
        assert second.locator('#note-count').inner_text()=='1'
        assert page.locator('.atlas-host').count()<=3

        # Root entry restores the last atlas without requiring a URL fragment.
        page.goto((root/'index.html').as_uri());second=active_sheet(page,keys['b'])
        assert second.locator('#note-count').inner_text()=='1'
        second.locator('#sheet-select').select_option('@catalog')
        second.locator('#workspace-catalog').wait_for(state='visible')
        text=second.locator('#workspace-list').inner_text()
        assert '일부 실패' in text and pending.name in text and corrupt.name in text
        second.locator('#workspace-search').fill('First sheet')
        assert second.locator('#workspace-list .workspace-run').count()==2
        second.locator('#workspace-list details summary').click()
        second.locator('.workspace-run[data-run="'+old_a+'"]').click()
        older=active_sheet(page,old_a)
        assert '이전 실행' in older.locator('#sheet-select option:checked').inner_text()
        assert 'run=' in page.url
        older.locator('#sheet-select').select_option('@catalog')
        older.locator('#workspace-catalog').wait_for(state='visible')
        page.keyboard.press('Escape')
        assert older.locator('#workspace-catalog').is_hidden()
        assert older.locator('#sheet-select').input_value()==old_a
        page.go_back();active_sheet(page,keys['b'])
        page.go_forward();active_sheet(page,old_a)

        # Only a registered direct child with its connection token can select.
        page.evaluate("()=>window.postMessage({channel:'ui-atlas-workspace/v1',type:'select',atlasId:'workspace-a',token:'wrong',dirty:false,key:'unknown'},'*')")
        assert page.locator('.atlas-host.active').get_attribute('data-run')==old_a
        page.set_viewport_size({'width':390,'height':844})
        older=active_sheet(page,old_a)
        if older.locator('#sidebar').is_hidden():older.locator('#toggle-sidebar').click()
        box=older.locator('#sheet-picker').bounding_box()
        assert box['x']>=0 and box['x']+box['width']<=390
        older.locator('#sheet-select').select_option('@catalog')
        older.locator('#workspace-catalog').wait_for(state='visible')
        assert older.evaluate('document.documentElement.scrollWidth<=390')
        older.locator('#close-workspace-catalog').click()
        assert not errors and not requests,(errors,requests)

        standalone=context.new_page();standalone.goto((root/'runs'/keys['b']/'index.html').as_uri())
        assert standalone.locator('#sheet-picker').is_hidden()
        assert standalone.locator('#note-count').inner_text()=='1', 'Standalone and embedded views retain the same saved opinions'
        standalone.close()
    finally:context.close()
    # A blocked preference store cannot prevent direct entry into a sheet.
    unavailable=browser.new_context()
    unavailable.add_init_script("if(window.parent===window){Storage.prototype.getItem=function(){throw Error('synthetic blocked preference storage')}}")
    try:
        page=unavailable.new_page();page.goto((root/'index.html').as_uri());active_sheet(page,keys['a'])
    finally:unavailable.close()
    assert (corrupt/'atlas.json').read_text()=='{broken'
    print('Workspace browser checks passed: direct entry, picker hierarchy, last-sheet restore, history/search/status, draft and pending-note retention, bounded clean cache, unload guard, 390px and standalone compatibility.')
