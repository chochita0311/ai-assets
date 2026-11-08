"""Ambiguous correspondence and portable note recovery/conflict witnesses."""
import json

import atlas
from capture import capture_frame
from reliability_checks import build_view, frame_for, search_select


def check_correspondence(browser, owner):
    source = owner / 'correspondence-source.html'
    source.write_text('<!doctype html><style>body{margin:30px}button{width:120px;height:40px;margin:30px}</style><button id="a">Remove item</button><button id="b">Remove item</button>')
    context = browser.new_context(viewport={'width': 1000, 'height': 800})
    page = context.new_page(); page.goto(source.as_uri())
    original = capture_frame(page, [], owner / 'correspondence-original.html')
    page.locator('#a').evaluate('el=>el.remove()')
    missing = capture_frame(page, [], owner / 'correspondence-missing.html')
    frames = [frame_for(original, 'correspondence-original.html', 'one'),
              frame_for(original, 'correspondence-original.html', 'same'),
              frame_for(missing, 'correspondence-missing.html', 'missing')]
    _, output, _ = build_view(owner, 'correspondence', source, frames)
    for width, height in ((1440, 1000), (390, 844)):
        page.set_viewport_size({'width': width, 'height': height}); page.goto(output.as_uri())
        page.wait_for_function('document.querySelectorAll("[data-ready=true]").length===3')
        search_select(page, 'Remove item', '#a')
        page.locator('#next').click()
        page.wait_for_function('document.querySelector("#state-label").textContent==="same" && document.querySelector("#selected-selector").textContent==="#a"')
        page.locator('#next').click()
        page.wait_for_function('document.querySelector("#comparison-status").textContent.includes("대응 요소 없음")')
        assert page.locator('.selection-box').is_hidden(), 'Never substitute the surviving same-label #b'
        page.locator('#previous').click()
        page.wait_for_function('document.querySelector("#selected-selector").textContent==="#a"')
    page.evaluate('''() => {
      const node=(id,text,regions=[])=>({id,parent:null,selector:'#'+id,tag:'button',text,label:text,visible:true,regions});
      const frame=(id,elements,regions=[])=>({id,surface:'test',journey:'test',elements,regions});
      const match=(a,b)=>new AtlasCatalog([a,b]).match(a,a.elements[0],b);
      const assert=(ok,label)=>{if(!ok)throw new Error(label);};
      const a=frame('from',[node('a','Remove')]);
      assert(match(a,frame('to',[node('renamed','Remove')]))?.id==='renamed','unique semantics on both sides');
      assert(match(a,frame('to',[node('b','Remove'),node('c','Remove')]))===null,'ambiguous destination');
      const source=frame('from',[node('a','Remove'),node('b','Keep')]);
      assert(match(source,frame('to',[node('b','Remove')]))===null,'do not rename a known other control by text');
      const r=[{id:'action',label:'Primary action',rect:{x:0,y:0,width:100,height:20}}];
      const named=frame('from',[node('a','Before',['action'])],r);
      assert(match(named,frame('to',[node('different','After',['action'])],r))?.id==='different','named region identity');
      const grouped=frame('from',[node('a','Remove',['left']),node('b','Remove',['right'])]);
      assert(match(grouped,frame('to',[node('c','Remove',['left'])]))?.id==='c','unique meaning within declared region');
      const other=node('b','Keep',['action-b']);other.selector='body > button:nth-of-type(2)';
      const rooted=frame('from',[node('a','Remove'),other],[{id:'action-b',label:'Other action',rect:{x:0,y:0,width:100,height:20}}]);
      const remaining={...other,id:'next-b',text:'Remove',label:'Remove',selector:'body > button'};
      assert(match(rooted,frame('to',[remaining],rooted.regions))===null,'a named region also identifies an already-distinct control');
      const unavailable=[{...r[0],rect:null,reason:'Selector matches multiple elements'}];
      assert(match(named,frame('to',[node('first','Other',['action']),node('second','Before',['action'])],unavailable))===null,'unavailable region cannot become a first-root match');
      assert(match(named,frame('to',[node('first','Other',['action']),node('second','Before',['action'])],r))===null,'contradictory multiple roots are not a verified identity');
    }''')
    context.close()


def check_import_contract(browser, owner):
    source = owner / 'import-contract.html'; source.write_text('<!doctype html><title>Note import</title>')
    context = browser.new_context(); page = context.new_page(); page.goto(source.as_uri())
    page.add_script_tag(content=(atlas.ASSETS / 'notes.js').read_text())
    page.evaluate('''() => {
      const assert=(ok,label)=>{if(!ok)throw new Error(label);};
      const throws=(fn,label)=>{let threw=false;try{fn();}catch{threw=true;}assert(threw,label);};
      const make=()=>new AtlasNotes('import-witness',()=>{},()=>{});
      const value=notes=>({schema:'ui-atlas.notes/v1',atlas:'import-witness',notes});
      const original={id:'one',frame:'one',identity:'observed',message:'Keep my decision',status:'open'};
      const first=make();assert(first.change([original]),'normal save');
      const set=Storage.prototype.setItem;
      Storage.prototype.setItem=()=>{throw new DOMException('Synthetic quota failure','QuotaExceededError');};
      assert(!first.change([{...original,status:'reviewed'}]),'pending same-ID update');
      const exported=JSON.parse(JSON.stringify(first.export()));Storage.prototype.setItem=set;
      throws(()=>first.planImport(value([original])),'pending same-ID write must settle before import begins');
      const reopened=make(),plan=reopened.planImport(exported);
      assert(plan.conflicts.length===1,'same-ID difference must be surfaced');
      throws(()=>reopened.applyImport(plan),'no unresolved overwrite');
      assert(reopened.items[0].status==='open','unresolved import unchanged');
      assert(reopened.applyImport(plan,new Map([['one','file']])),'chosen recovery');
      assert(make().items[0].status==='reviewed','recovered status persists');
      const old=reopened.planImport(value([original]));
      assert(reopened.applyImport(old,new Map([['one','local']])),'retain current choice');
      assert(make().items[0].status==='reviewed','older export does not overwrite newer work');
      const mixed=reopened.planImport(value([{...original,id:'new'},original]));
      const external=make();external.change([{...original,status:'reviewed',message:'Concurrent decision'}]);
      throws(()=>reopened.applyImport(mixed,new Map([['one','file']])),'recheck while dialog was open');
      assert(!make().items.some(n=>n.id==='new'),'no partial additions before conflict is rechecked');
      assert(make().items[0].message==='Concurrent decision','concurrent work survives');
      throws(()=>reopened.planImport(value([original,{...original,message:'Conflicting duplicate'}])),'conflicting duplicate IDs');
      const duplicated=reopened.planImport(value([{...original,id:'new'},{...original,id:'new'}]));
      assert(reopened.applyImport(duplicated),'identical duplicate input');
      assert(make().items.filter(n=>n.id==='new').length===1,'deduplicate identical input');
      assert(reopened.same(original,{...original,kind:'proposal',clipped:false}),'compatible omitted defaults');
      throws(()=>reopened.planImport(null),'invalid envelope');
      const get=Storage.prototype.getItem;
      Storage.prototype.getItem=()=>{throw new DOMException('Synthetic read failure','SecurityError');};
      throws(()=>reopened.planImport(value([{...original,id:'unread'}])),'cannot decide conflicts without reading local work');
      Storage.prototype.getItem=get;
      assert(!make().items.some(n=>n.id==='unread'),'read failure writes nothing');
      const settled=make(), pendingPlan=settled.planImport(value([{...original,message:'Imported'}]));
      Storage.prototype.setItem=()=>{throw new DOMException('Synthetic quota failure','QuotaExceededError');};
      settled.change([{...original,message:'Local pending'}]);Storage.prototype.setItem=set;
      make().change([{...original,message:'External saved'}]);
      throws(()=>settled.applyImport(pendingPlan,new Map([['one','file']])),'pending operation added during comparison stops import');
      assert(make().items.find(n=>n.id==='one').message==='External saved','import must not settle a hidden storage conflict');
      assert(settled.export().notes.find(n=>n.id==='one').message==='Local pending','pending work remains exportable');
      assert(settled.change(),'explicit retry resolves local pending write');
      const retry=settled.planImport(value([{...original,message:'Imported'}]));
      assert(settled.applyImport(retry,new Map([['one','file']])),'import works after pending operation is settled');
    }''')
    context.close()


def check_import_ui(browser, owner):
    source = owner / 'import-source.html'
    source.write_text('<!doctype html><button id="target">Review target</button>')
    context = browser.new_context(viewport={'width': 1000, 'height': 800})
    page = context.new_page(); page.goto(source.as_uri())
    observed = capture_frame(page, [], owner / 'import-frame.html')
    _, output, _ = build_view(owner, 'import-ui', source, [frame_for(observed, 'import-frame.html', 'one')])
    page.set_viewport_size({'width': 1440, 'height': 1000}); page.goto(output.as_uri())
    page.wait_for_selector('[data-ready="true"]'); search_select(page, 'Review target', '#target')
    page.locator('#note').fill('Pending review decision'); page.locator('#note-form button').click()
    page.evaluate('''() => {Storage.prototype.setItem=()=>{throw new DOMException('Synthetic quota failure','QuotaExceededError');};}''')
    page.locator('#frame-notes').get_by_role('button', name='확인 완료로 표시', exact=True).click()
    page.locator('#file-menu-button').click()
    with page.expect_download() as info: page.locator('#notes-download').click()
    exported = owner / 'pending-review.json'; info.value.save_as(exported)
    saved = json.loads(exported.read_text()); assert saved['notes'][0]['status'] == 'reviewed'
    page.close()

    page = context.new_page(); page.goto(output.as_uri()); page.wait_for_selector('[data-ready="true"]')
    page.locator('#requests').click()
    assert page.locator('#review-list').get_by_role('button', name='확인 완료로 표시', exact=True).count() == 1
    # Cancel discards the whole import, including unrelated new IDs.
    mixed = owner / 'mixed-notes.json'
    mixed.write_text(json.dumps({**saved, 'notes': [*saved['notes'], {**saved['notes'][0], 'id': 'new', 'message': 'New imported note'}]}))
    page.locator('#import-file').set_input_files(mixed); page.locator('#note-import').wait_for(state='visible')
    assert '현재: 미검토' in page.locator('#import-conflicts').inner_text()
    assert '파일: 확인 완료' in page.locator('#import-conflicts').inner_text()
    assert 'Fixture / one · #target' in page.locator('#import-conflicts').inner_text()
    page.locator('#note-import').get_by_role('button', name='취소', exact=True).click()
    page.wait_for_function('document.querySelector("#import-file").value===""')
    assert page.locator('#note-count').inner_text() == '1'
    page.locator('#import-file').set_input_files(exported)
    page.locator('#note-import select').select_option('file')
    page.locator('#note-import').get_by_role('button', name='선택한 내용으로 가져오기', exact=True).click()
    page.wait_for_function('document.querySelector("#import-file").value===""')
    page.locator('#review-list').get_by_role('button', name='확인 완료 · 되돌리기', exact=True).wait_for()
    page.reload(); page.locator('#requests').click()
    assert page.locator('#review-list').get_by_role('button', name='확인 완료 · 되돌리기', exact=True).count() == 1

    old = owner / 'older-review.json'; old.write_text(json.dumps({**saved, 'notes': [{**saved['notes'][0], 'status': 'open'}]}))
    page.set_viewport_size({'width': 390, 'height': 844})
    page.locator('#import-file').set_input_files(old)
    assert page.locator('#note-import select').input_value() == 'local'
    assert page.evaluate('document.documentElement.scrollWidth<=innerWidth')
    page.locator('#note-import').get_by_role('button', name='선택한 내용으로 가져오기', exact=True).click()
    page.wait_for_function('document.querySelector("#import-file").value===""')
    assert page.locator('#review-list').get_by_role('button', name='확인 완료 · 되돌리기', exact=True).count() == 1

    # A second tab changes the opinion while the first is choosing its import.
    page.locator('#import-file').set_input_files(old)
    page.locator('#note-import').wait_for(state='visible')
    other = context.new_page(); other.goto(output.as_uri()); other.locator('#requests').click()
    other.locator('#review-list').get_by_role('button', name='확인 완료 · 되돌리기', exact=True).click()
    page.wait_for_function('document.querySelector("#review-list").textContent.includes("확인 완료로 표시")')
    page.locator('#note-import select').select_option('file')
    page.locator('#note-import').get_by_role('button', name='선택한 내용으로 가져오기', exact=True).click()
    page.wait_for_function('document.querySelector("#announcement").textContent.includes("검토하는 동안 의견이 바뀌었습니다")')
    assert page.locator('#review-list').get_by_role('button', name='확인 완료로 표시', exact=True).count() == 1
    other.close()
    page.evaluate('''() => {
      window.restoreRemoval=Storage.prototype.removeItem;
      Storage.prototype.removeItem=()=>{throw new DOMException('Synthetic delete failure','SecurityError');};
    }''')
    page.locator('#review-list').get_by_role('button', name='삭제', exact=True).click()
    assert page.locator('#note-count').inner_text() == '0'
    assert '의견 파일은 삭제 작업을 복구하지 않습니다.' in page.locator('#announcement').inner_text()
    page.evaluate('() => {Storage.prototype.removeItem=window.restoreRemoval;}')
    page.locator('#file-menu-button').click(); page.locator('#retry-notes').click()
    page.reload(); assert page.locator('#note-count').inner_text() == '0'
    assert page.locator('#retry-notes').is_hidden()
    context.close()


def check_conflicts(browser, owner):
    check_correspondence(browser, owner)
    check_import_contract(browser, owner)
    check_import_ui(browser, owner)
    print('Conflict checks passed: ambiguous-source/destination exclusion, known-other controls, unique/region matches, same-ID recovery, older imports, cancel, duplicate IDs, read failure and cross-tab changes during import.')
