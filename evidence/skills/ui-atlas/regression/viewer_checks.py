"""Behavior witnesses for section navigation and element-linked review."""
import re


def camera(page):
    return page.evaluate('''() => { const m = new DOMMatrix(getComputedStyle(document.querySelector('#world')).transform);
      return {x:m.e,y:m.f,zoom:m.a}; }''')


def set_zoom(page, value):
    page.locator('#zoom-value').click()
    page.locator('#zoom-input').fill(str(value))
    page.locator('#zoom-input').press('Enter')
    page.wait_for_timeout(50)


def check_review_navigation(page):
    page.locator('[data-panel="screens"]').click()
    page.locator('#search').fill('두 번째 노트')
    page.locator('.search-result[data-node-result]').first.click()
    page.wait_for_function("document.querySelector('#selected-selector').textContent === '#results'")
    page.wait_for_timeout(100)
    assert page.locator('.artboard[data-ready=true]').count() == 7, 'Search must keep mounted observations intact'
    page.locator('#search').fill('')
    before_zoom = camera(page)['zoom']
    before_box = page.locator('.selection-box').bounding_box()
    page.locator('#next').click()
    page.wait_for_function("document.querySelector('#state-label').textContent === 'Hover' && document.querySelector('#selected-selector').textContent === '#results'")
    after_box = page.locator('.selection-box').bounding_box()
    assert camera(page)['zoom'] == before_zoom
    assert max(abs(before_box[k] - after_box[k]) for k in ('x', 'y', 'width', 'height')) < 1
    assert '같은 요소' in page.locator('#comparison-status').inner_text()

    page.locator('[data-tab="description"]').click()
    assert 'Review loading and sync copy' in page.locator('#section-details').inner_text()
    assert page.locator('#journey-steps li').count() == 7
    page.locator('[data-tab="element"]').click()
    page.locator('[data-panel="layers"]').click()
    assert page.get_by_role('treeitem', name=re.compile('Results$')).count() == 1
    expanded = page.locator('.layer-row').count()
    page.locator('.tree-toggle:not([disabled])').first.click()
    assert page.locator('.layer-row').count() < expanded
    page.locator('.tree-toggle:not([disabled])').first.click()

    page.locator('[data-panel="screens"]').click()
    page.locator('[data-state="modal"]').click()
    page.locator('#regions button').filter(has_text='Settings').click()
    page.wait_for_function("document.querySelector('#selected-selector').textContent === '#settings'")
    before_zoom = camera(page)['zoom']
    page.locator('#next').click()
    page.wait_for_function("document.querySelector('#comparison-status').textContent.includes('대응 요소 없음')")
    assert camera(page)['zoom'] == before_zoom
    assert page.locator('.selection-box').is_hidden()
    page.locator('#previous').click()
    page.wait_for_function("document.querySelector('#selected-selector').textContent === '#settings'")
    assert camera(page)['zoom'] == before_zoom

    # Same positional path with changed meaning must not become a correspondence.
    assert page.evaluate('''() => {
      const a={id:'a',surface:'test',journey:'test',regions:[],elements:[{id:'e1',parent:null,tag:'p',selector:'div > p:nth-of-type(1)',label:'Old item',text:'Old item',visible:true}]};
      const b={...a,id:'b',elements:[{...a.elements[0],label:'Different item',text:'Different item'}]};
      const catalog=new AtlasCatalog([a,b]); return catalog.match(a,a.elements[0],b)===null;
    }''')

    page.locator('#close-inspector').click()
    for zoom in (6, 10, 16, 20, 26, 32, 50, 100, 200, 400):
        set_zoom(page, zoom)
        collisions = page.evaluate('''() => {
          const labels=[...document.querySelectorAll('.section-caption,.frame-label')]
            .filter(e=>getComputedStyle(e).visibility!=='hidden').map(e=>e.getBoundingClientRect());
          return labels.some((a,i)=>labels.slice(i+1).some(b=>a.left<b.right&&a.right>b.left&&a.top<b.bottom&&a.bottom>b.top));
        }''')
        assert not collisions, f'Visible title collision at {zoom}%'

    page.locator('#fit-all').click(); page.wait_for_timeout(50)
    old = page.locator('.artboard').evaluate_all('es=>es.map(e=>({id:e.dataset.frame,x:+e.dataset.x,y:+e.dataset.y}))')
    title = page.locator('.section-caption').bounding_box()
    page.mouse.move(title['x']+20,title['y']+10);page.mouse.down()
    page.mouse.move(title['x']+70,title['y']+40,steps=5);page.mouse.up()
    new = page.locator('.artboard').evaluate_all('es=>es.map(e=>({id:e.dataset.frame,x:+e.dataset.x,y:+e.dataset.y}))')
    dx,dy=new[0]['x']-old[0]['x'],new[0]['y']-old[0]['y']
    assert dx > 0 and dy > 0
    assert all(abs(b['x']-a['x']-dx)<.01 and abs(b['y']-a['y']-dy)<.01 for a,b in zip(old,new))

    page.locator('#zoom-value').click();page.locator('#show-descriptions').uncheck()
    page.locator('.section-description').wait_for(state='hidden')
    page.locator('#show-descriptions').check();page.locator('#zoom-value').click()
    page.locator('#focus-view').click()
    assert page.locator('#sidebar').is_hidden()
    page.locator('#focus-view').click()
    assert page.locator('#sidebar').is_visible()

    page.locator('[data-state="loaded"]').click()
    page.locator('#note').fill('Review status witness');page.locator('#note-form button').click()
    page.locator('#requests').click()
    row=page.locator('#review-list .review-item').filter(has_text='Review status witness')
    row.get_by_role('button',name='확인 완료로 표시',exact=True).click()
    page.locator('#review-filter').select_option('reviewed')
    assert 'Review status witness' in page.locator('#review-list').inner_text()
    page.locator('#review-filter').select_option('open')
    assert 'Review status witness' not in page.locator('#review-list').inner_text()
    page.locator('#review-filter').select_option('reviewed')
    row.get_by_role('button',name='위치 보기',exact=True).click()
    assert page.locator('#state-label').inner_text()=='Loaded'
    page.wait_for_timeout(100)
    assert page.locator('.note-pin').count() > 0
    row.get_by_role('button',name='삭제',exact=True).click()
    page.locator('#review-filter').select_option('all')
    page.locator('[data-panel="screens"]').click()
