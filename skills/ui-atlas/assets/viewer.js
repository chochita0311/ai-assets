(() => {
  'use strict';
  const atlas = JSON.parse(document.querySelector('#atlas-data').textContent);
  const $ = selector => document.querySelector(selector);
  const make = (tag, text, className) => {
    const element = document.createElement(tag);
    if (text !== undefined) element.textContent = text;
    if (className) element.className = className;
    return element;
  };
  const button = (text, action, className) => {
    const element = make('button', text, className);
    element.type = 'button'; element.addEventListener('click', action); return element;
  };
  const frames = atlas.frames.filter(frame => frame.status === 'rendered');
  const missing = atlas.frames.filter(frame => frame.status !== 'rendered');
  const frameById = new Map(frames.map(frame => [frame.id, frame]));
  const catalog = new AtlasCatalog(frames);
  const mounted = new Map();
  const positions = new Map();
  const expandedNodes = new Map();
  // A draft belongs to its original state/element, including when selection clears.
  const drafts = new Map();
  let draftKey = null, searchKey = '', searchPage = 0;
  const narrow = () => matchMedia('(max-width: 560px)').matches;
  let wasNarrow = narrow();
  const zoomPercent = zoom => Number((zoom * 100).toPrecision(3));
  let selectedFrame = null, selectedElement = null, selectionRect = null;
  let activePanel = 'screens', activeTab = 'element', hoveredFrame = null;
  let announcementTimer, hoverTick, pendingHover, lastClick = null, layoutTick;
  let pendingPick = null, pickSerial = 0, comparison = null, viewRevision = 0;
  let sheetPicker = null;
  const labels = {unverified: '미확인', unimplemented: '미구현', 'not-applicable': '해당 없음', 'render-failed': '재현 실패'};
  function announce(message) {
    $('#announcement').textContent = message;
    clearTimeout(announcementTimer);
    announcementTimer = setTimeout(() => $('#announcement').textContent = '', 4500);
  }
  const notes = atlas.composition ? new AtlasTopicNotes(atlas, updateNotes, announce) : new AtlasNotes(atlas.id, updateNotes, announce);
  let viewportVariant = 'wide';
  const expandedFeatures = new Set();
  if (atlas.composition) catalog.filter(viewportVariant);
  const canvas = new AtlasCanvas($('#canvas'), $('#world'), atlas.id, {
    zoom: zoom => { $('#zoom-value').textContent = zoomPercent(zoom) + '%'; scheduleLayout(); },
    position: moveFrame,
    members: id => catalog.sections.get(id).frames.map(frame => ({id: frame.id, ...positions.get(frame.id)})),
    section: id => chooseSection(catalog.sections.get(id)),
    click: clickCanvas,
    hover: hoverCanvas,
    clearHover: () => paintBox('hover', null),
    error: announce
  });
  const sections = new AtlasSections($('#world'), catalog, positions, chooseSection);
  const selectionBox = make('div', undefined, 'selection-box');
  const hoverBox = make('div', undefined, 'hover-box');
  for (let i = 0; i < 4; i++) selectionBox.append(make('i'));
  const dimensionLabel = make('span', '', 'selection-size'); selectionBox.append(dimensionLabel);

  function post(frameId, type, detail = {}) {
    const target = mounted.get(frameId);
    if (target?.ready) target.iframe.contentWindow.postMessage({channel: 'ui-atlas-dom', token: target.token, type, ...detail}, '*');
  }
  function scheduleLayout() {
    if (layoutTick) return;
    layoutTick = requestAnimationFrame(() => {
      layoutTick = null;
      sections.update(); sections.labels(canvas.camera.zoom, selectedFrame);
      document.body.classList.toggle('canvas-overview', canvas.camera.zoom < .45);
      for (const [id, entry] of mounted) entry.card.title = canvas.camera.zoom < .28 ? frameById.get(id).label : '';
      renderPins(); renderStateConnections();
    });
  }
  function embeddedDocument(frame, token) {
    const html = frame.document, [headEnd, bodyEnd] = frame.document_slots;
    const nonce = crypto.randomUUID().replaceAll('-', '');
    const policy = `default-src 'none'; img-src data:; font-src data:; style-src 'unsafe-inline'; script-src 'nonce-${nonce}'; connect-src 'none'; form-action 'none'; base-uri 'none'`;
    const script = '(' + atlasFrameBridge.toString() + ')(' + JSON.stringify({token, scroll: frame.scroll || {x: 0, y: 0}}).replaceAll('<', '\\u003c') + ');';
    const embedded = html.slice(0, headEnd) + '<meta http-equiv="Content-Security-Policy" content="' + policy + '">' +
      html.slice(headEnd, bodyEnd) + '<script nonce="' + nonce + '">' + script + '<' + '/script>' + html.slice(bodyEnd);
    return embedded.replace(/atlas-resource:([a-f0-9]{64})/g, (_, key) => atlas.resources[key] || '');
  }
  function createFrame(frame, position) {
    const card = make('section', undefined, 'artboard');
    card.dataset.frame = frame.id;
    card.style.width = frame.viewport.width + 'px'; card.style.height = frame.viewport.height + 'px';
    const label = make('div', undefined, 'frame-label');
    label.append(make('span', String(catalog.section(frame).frames.indexOf(frame) + 1).padStart(2, '0'), 'step-number'),
      make('strong', frame.label), make('small', frame.viewport.width + ' × ' + frame.viewport.height));
    label.title = frame.surface + ' / ' + frame.label;
    const iframe = make('iframe'); iframe.title = frame.label;
    iframe.setAttribute('sandbox', 'allow-scripts'); iframe.tabIndex = -1;
    const token = crypto.randomUUID();
    mounted.set(frame.id, {card, iframe, token, ready: false});
    card.append(label, iframe, make('div', undefined, 'hit-surface'));
    $('#world').append(card);
    moveFrame(frame.id, position);
    // Establish the iframe's viewport before its bridge restores native state.
    // A srcdoc bridge can otherwise run while the child has no layout boxes.
    iframe.getBoundingClientRect();
    iframe.srcdoc = embeddedDocument(frame, token);
  }
  function moveFrame(id, position) {
    positions.set(id, position);
    const card = mounted.get(id)?.card;
    if (card) {
      card.style.left = position.x + 'px'; card.style.top = position.y + 'px';
      card.dataset.x = position.x; card.dataset.y = position.y;
    }
    if (selectedFrame?.id === id && selectionRect) paintBox('selection', {frame: id, rect: selectionRect});
    scheduleLayout();
  }
  function buildCanvas() {
    $('#world').replaceChildren(); mounted.clear(); positions.clear();
    let y = 160;
    for (const section of catalog.sections.values()) {
      const byFlow = new Map();
      for (const frame of section.frames) {
        const key = atlas.composition ? frame.origin.atlas + ':' + frame.journey : section.id;
        if (!byFlow.has(key)) byFlow.set(key, []);
        byFlow.get(key).push(frame);
      }
      const flows = [...byFlow.values()];
      for (const flow of flows) {
        let x = 520, rowHeight = 680, column = 0;
        for (const frame of flow) {
          if (atlas.composition && column === 4) { y += rowHeight + 160; x = 520; rowHeight = 680; column = 0; }
          createFrame(frame, canvas.position(frame, {x, y}));
          x += frame.viewport.width + 160; rowHeight = Math.max(rowHeight, frame.viewport.height); column++;
        }
        y += rowHeight + (atlas.composition ? 200 : 680);
      }
      if (atlas.composition) y += 480;
    }
    sections.build();
    $('#world').append(hoverBox, selectionBox);
    hoverBox.hidden = true; selectionBox.hidden = true;
    $('#empty').hidden = mounted.size > 0;
    renderScreens(); scheduleLayout();
    if (atlas.composition) $('#coverage').textContent = `현재 ${mounted.size} · 전체 ${frames.length}개 장면` + (missing.length ? ` · 범위 확인 ${missing.length}` : '');
  }
  function setVariant(variant, fit = true) {
    if (!atlas.composition) return;
    const feature = selectedFrame?.feature?.id;
    clearSelection(); viewportVariant = variant; $('#viewport-filter').value = variant;
    catalog.filter(variant); buildCanvas();
    if (fit) {
      const section = catalog.sections.get(feature) || [...catalog.sections.values()][0];
      if (section) canvas.fit(frameBounds(section.frames[0]), .6); else fitAll();
    }
  }
  function ensureMounted(frame) {
    if (atlas.composition && !mounted.has(frame.id)) setVariant(frame.variant, false);
  }
  function stateButton(frame) {
    const item = button('', () => chooseFrame(frame, true), 'screen-item' + (selectedFrame?.id === frame.id ? ' active' : ''));
    item.dataset.state = frame.id;
    item.append(make('span', '▧', 'frame-icon'), make('span', frame.label));
    return item;
  }
  function renderScreens() {
    $('#screens').replaceChildren();
    if (atlas.composition) {
      for (const section of catalog.sections.values()) {
        const details = make('details', undefined, 'feature-tree');
        details.open = expandedFeatures.has(section.id) || !!selectedFrame && catalog.section(selectedFrame).id === section.id;
        const summary = make('summary', section.label); summary.append(make('small', String(section.frames.length))); details.append(summary);
        details.ontoggle = () => { if (details.open) expandedFeatures.add(section.id); else expandedFeatures.delete(section.id); };
        summary.onclick = event => {
          event.preventDefault();
          if (details.open) { expandedFeatures.delete(section.id); details.open = false; }
          else { expandedFeatures.add(section.id); chooseSection(section); }
        };
        const flows = new Map();
        for (const frame of section.frames) {
          const key = frame.origin.atlas + ':' + frame.journey;
          if (!flows.has(key)) flows.set(key, []); flows.get(key).push(frame);
        }
        for (const flow of flows.values()) {
          if (flow.length === 1) details.append(stateButton(flow[0]));
          else {
            const branch = make('details', undefined, 'flow-tree');
            branch.open = flow.some(frame => frame.id === selectedFrame?.id);
            branch.append(make('summary', flow[0].flow_label || flow[0].journey_label));
            for (const frame of flow) branch.append(stateButton(frame)); details.append(branch);
          }
        }
        for (const gap of missing.filter(frame => frame.feature?.id === section.id && (!frame.variant || viewportVariant === 'all' || frame.variant === viewportVariant))) {
          const control = button((labels[gap.status] || gap.status) + ' · ' + gap.label, () => $('#information').showModal(), 'state-gap');
          control.title = gap.reason; details.append(control);
        }
        $('#screens').append(details);
      }
      return;
    }
    for (const surface of [...new Set(frames.map(frame => frame.surface))]) {
      const matching = frames.filter(frame => frame.surface === surface && mounted.has(frame.id));
      if (!matching.length) continue;
      const heading = make('div', surface, 'surface-heading'); heading.append(make('span', matching.length)); $('#screens').append(heading);
      for (const section of [...catalog.sections.values()].filter(section => section.surface === surface)) {
        $('#screens').append(button(section.label, () => chooseSection(section), 'section-item'));
        for (const frame of section.frames) {
          const item = button('', () => chooseFrame(frame, true), 'screen-item' + (selectedFrame?.id === frame.id ? ' active' : ''));
          item.dataset.state = frame.id;
          item.append(make('span', String(section.frames.indexOf(frame) + 1).padStart(2, '0'), 'frame-icon'), make('span', frame.label));
          $('#screens').append(item);
        }
      }
    }
  }
  function renderLayers() {
    $('#layers').replaceChildren();
    if (!selectedFrame) { $('#layers').append(make('p', '화면을 선택하세요.', 'panel-empty')); return; }
    const frame = selectedFrame, index = catalog.index(frame);
    if (!expandedNodes.has(frame.id)) {
      const open = new Set();
      for (const root of index.regions.values()) for (const node of catalog.ancestors(frame, root)) open.add(node.id);
      for (const node of frame.elements) if (['html', 'body'].includes(node.tag)) open.add(node.id);
      expandedNodes.set(frame.id, open);
    }
    const open = expandedNodes.get(frame.id);
    // Non-rendering wrappers can still have visible children (display:contents,
    // or a zero-height wrapper with viewport-fixed descendants).
    const visibleChildren = id => (index.children.get(id) || []).flatMap(child => child.visible ? [child] : visibleChildren(child.id));
    const visit = (element, depth) => {
      const children = visibleChildren(element.id);
      const row = make('div', undefined, 'layer-row'); row.style.paddingLeft = Math.min(depth, 8) * 9 + 'px';
      const toggle = button(children.length ? open.has(element.id) ? '⌄' : '›' : '', () => {
        if (open.has(element.id)) open.delete(element.id); else open.add(element.id); renderLayers();
      }, 'tree-toggle');
      toggle.disabled = !children.length;
      toggle.setAttribute('aria-label', catalog.name(frame, element) + (open.has(element.id) ? ' 접기' : ' 펼치기'));
      const item = button('', () => requestSelection(frame, element), 'layer-item' + (selectedElement?.id === element.id ? ' active' : ''));
      item.dataset.node = element.id;
      item.setAttribute('role', 'treeitem'); item.setAttribute('aria-level', depth + 1);
      item.setAttribute('aria-selected', selectedElement?.id === element.id ? 'true' : 'false');
      if (children.length) item.setAttribute('aria-expanded', String(open.has(element.id)));
      item.append(make('span', element.tag === 'svg' || element.tag === 'use' ? '◇' : element.text ? 'T' : '▧', 'layer-tag'), make('span', catalog.name(frame, element)));
      item.title = element.selector; row.append(toggle, item); $('#layers').append(row);
      if (open.has(element.id)) for (const child of children) visit(child, depth + 1);
    };
    for (const root of visibleChildren(null)) visit(root, 0);
  }
  function renderSearch() {
    const query = $('#search').value.trim();
    $('#screens').hidden = activePanel !== 'screens' || !!query;
    $('#layers').hidden = activePanel !== 'layers' || !!query;
    $('#reviews').hidden = activePanel !== 'reviews';
    $('#search-results').hidden = !query || activePanel === 'reviews';
    if (activePanel === 'reviews') { renderReviewList(); return; }
    $('#search-results').replaceChildren();
    if (!query) return;
    if (activePanel === 'layers' && !selectedFrame) { $('#search-results').append(make('p', '화면을 선택하세요.', 'panel-empty')); return; }
    const matches = catalog.search(query, activePanel === 'layers' ? selectedFrame : null);
    const key = JSON.stringify([query, activePanel, activePanel === 'layers' ? selectedFrame?.id : null]);
    if (key !== searchKey) { searchKey = key; searchPage = 0; }
    const start = searchPage * 200, end = Math.min(start + 200, matches.length);
    $('#search-results').append(make('p', matches.length + '개 결과' + (matches.length ? ` · ${start + 1}–${end}` : ''), 'panel-empty'));
    if (matches.length > 200) {
      const paging = make('div', undefined, 'search-paging');
      for (const [label, direction, disabled] of [['이전 결과', -1, start === 0], ['다음 결과', 1, end === matches.length]]) {
        const control = button(label, () => { searchPage += direction; renderSearch(); $('#search-results').scrollTop = 0; });
        control.disabled = disabled; paging.append(control);
      }
      $('#search-results').append(paging);
    }
    for (const hit of matches.slice(start, end)) {
      const item = button('', () => {
        if (hit.element) requestSelection(hit.frame, hit.element, {fit: true}); else chooseFrame(hit.frame, true);
      }, 'search-result');
      item.dataset.frameResult = hit.frame.id;
      if (hit.element) item.dataset.nodeResult = hit.element.id;
      item.append(make('strong', hit.element ? catalog.name(hit.frame, hit.element) : hit.frame.label),
        make('small', hit.frame.surface + ' / ' + hit.frame.label));
      $('#search-results').append(item);
    }
  }
  function showPanel(panel) {
    activePanel = panel;
    document.querySelectorAll('[data-panel]').forEach(item => item.classList.toggle('active', item.dataset.panel === panel));
    $('#sidebar').hidden = false; document.body.classList.remove('focus-view'); $('#focus-view').setAttribute('aria-pressed', 'false');
    $('#search').value = ''; renderLayers(); renderSearch();
  }
  function frameBounds(frame) { return {...positions.get(frame.id), ...frame.viewport}; }
  function fitAll() {
    if (!mounted.size) return;
    const rectangles = [...catalog.sections.values()].map(section => sections.bounds(section));
    const x = Math.min(...rectangles.map(rect => rect.x)), y = Math.min(...rectangles.map(rect => rect.y)) - 100;
    canvas.fit({x, y, width: Math.max(...rectangles.map(rect => rect.x + rect.width)) - x,
      height: Math.max(...rectangles.map(rect => rect.y + rect.height)) - y}, .6);
  }
  function fitSelection() {
    if (!selectedFrame) { fitAll(); return; }
    const position = positions.get(selectedFrame.id);
    const rect = selectionRect || {x: 0, y: 0, ...selectedFrame.viewport};
    canvas.fit({x: position.x + rect.x, y: position.y + rect.y, width: rect.width, height: rect.height}, 2);
  }
  function pointInFrame(event, frameId) {
    const box = mounted.get(frameId).card.getBoundingClientRect();
    return {x: (event.clientX - box.x) / canvas.camera.zoom, y: (event.clientY - box.y) / canvas.camera.zoom};
  }
  function clickCanvas(event, card) {
    if (!card) { clearSelection(); return; }
    const frame = frameById.get(card.dataset.frame);
    const point = pointInFrame(event, frame.id);
    if (point.y < 0) { chooseFrame(frame, true); return; }
    const fit = lastClick?.id === frame.id && event.timeStamp - lastClick.time < 350;
    lastClick = {id: frame.id, time: event.timeStamp};
    if (!mounted.get(frame.id).ready) { chooseFrame(frame); return; }
    requestSelection(frame, null, {fit, point, follow: $('#interaction-mode').value === 'follow'});
  }
  function hoverCanvas(event) {
    const card = event.target.closest('.artboard');
    if (!card || canvas.tool === 'hand' || canvas.space) { hoveredFrame = null; paintBox('hover', null); return; }
    hoveredFrame = card.dataset.frame;
    pendingHover = {id: hoveredFrame, point: pointInFrame(event, hoveredFrame)};
    if (hoverTick) return;
    hoverTick = requestAnimationFrame(() => {
      hoverTick = null;
      if (pendingHover) post(pendingHover.id, 'hover', pendingHover.point);
    });
  }
  function paintBox(kind, selection) {
    const overlay = kind === 'selection' ? selectionBox : hoverBox;
    if (!selection || !positions.has(selection.frame) || selection.rect.width <= 0 || selection.rect.height <= 0) { overlay.hidden = true; return; }
    const {rect} = selection, position = positions.get(selection.frame);
    Object.assign(overlay.style, {left: position.x + rect.x + 'px', top: position.y + rect.y + 'px', width: rect.width + 'px', height: rect.height + 'px'});
    overlay.hidden = false;
    if (kind === 'selection') dimensionLabel.textContent = Math.round(rect.width) + ' × ' + Math.round(rect.height);
  }
  function clearSelection() {
    saveDraft(); draftKey = null;
    viewRevision++;
    pendingPick = null; comparison = null; $('#comparison-status').hidden = true;
    selectedFrame = null; selectedElement = null; selectionRect = null;
    $('#inspector').hidden = true; paintBox('selection', null); paintBox('hover', null);
    for (const entry of mounted.values()) entry.card.classList.remove('selected');
    renderScreens(); renderLayers(); scheduleLayout();
  }
  function chooseFrame(frame, fit = false, comparing = false) {
    ensureMounted(frame);
    saveDraft();
    viewRevision++;
    pendingPick = null;
    if (!comparing) { comparison = null; $('#comparison-status').hidden = true; }
    selectedFrame = frame; selectedElement = null; selectionRect = null;
    for (const [id, entry] of mounted) entry.card.classList.toggle('selected', id === frame.id);
    $('#inspector').hidden = false; paintBox('selection', null);
    if (narrow()) $('#sidebar').hidden = true;
    renderInspector(); renderScreens(); renderLayers();
    if (activePanel === 'layers') renderSearch();
    scheduleLayout();
    if (fit || narrow() && !comparing) fitLater(() => canvas.fit(frameBounds(frame)));
  }
  function fitLater(action) {
    const revision = viewRevision;
    requestAnimationFrame(() => { if (revision === viewRevision) action(); });
  }
  function chooseSection(section) {
    chooseFrame(section.frames[0]); showTab('description');
    fitLater(() => canvas.fit(sections.bounds(section), 1));
  }
  function requestSelection(frame, element, options = {}) {
    chooseFrame(frame, false, options.comparing);
    showTab('element');
    pendingPick = {frame: frame.id, element: element?.id, request: ++pickSerial, ...options};
    sendSelection();
  }
  function sendSelection() {
    if (!pendingPick) return;
    const pick = pendingPick;
    post(pick.frame, pick.point ? 'pick' : 'select', {id: pick.element, ...pick.point, request: pick.request});
  }
  function selectElement(frame, detail, request) {
    if (!pendingPick || request !== pendingPick.request || frame.id !== pendingPick.frame) return;
    const pick = pendingPick; pendingPick = null;
    if (!detail || detail.rect.width <= 0 || detail.rect.height <= 0) { announce('이 상태에서 요소를 선택할 수 없습니다.'); return; }
    saveDraft();
    selectedElement = frame.elements.find(element => element.id === detail.id);
    if (!selectedElement) return;
    if (pick.follow) {
      const links = elementLinks(frame, selectedElement);
      if (links.length === 1) { followLink(links[0]); return; }
      announce(links.length ? '연결된 상태에서 분기를 선택하세요.' : '이 요소의 연결된 관찰 상태가 없습니다.');
    }
    selectionRect = detail.rect;
    const open = expandedNodes.get(frame.id);
    for (const ancestor of catalog.ancestors(frame, selectedElement)) open?.add(ancestor.id);
    paintBox('selection', {frame: frame.id, rect: detail.rect}); paintBox('hover', null);
    renderInspector(); renderLayers();
    if (pick.anchor) placeAtAnchor(frame, detail.rect, pick.anchor);
    else if (pick.fit || narrow() && !pick.comparing) fitLater(fitSelection);
    if (pick.comparing) {
      $('#comparison-status').hidden = false; $('#comparison-status').textContent = '같은 요소 · 확대 수준 유지';
    }
    scheduleLayout();
  }
  function placeAtAnchor(frame, rect, anchor) {
    const position = positions.get(frame.id), zoom = canvas.camera.zoom;
    canvas.camera.x = anchor.x - (position.x + rect.x + rect.width / 2) * zoom;
    canvas.camera.y = anchor.y - (position.y + rect.y + rect.height / 2) * zoom;
    canvas.paint();
  }
  function showTab(tab) {
    activeTab = tab;
    for (const name of ['element', 'description', 'payload']) $('#' + name + '-panel').hidden = name !== tab;
    document.querySelectorAll('[data-tab]').forEach(item => item.classList.toggle('active', item.dataset.tab === tab));
    if (selectedFrame) $('#selection-title').textContent = tab === 'description' ? catalog.section(selectedFrame).label :
      selectedElement ? catalog.name(selectedFrame, selectedElement) : selectedFrame.label;
  }
  function renderInspector() {
    const frame = selectedFrame;
    if (!frame) return;
    showTab(activeTab);
    $('#state-label').textContent = frame.label;
    $('#breadcrumbs').replaceChildren();
    if (selectedElement) {
      for (const element of catalog.ancestors(frame, selectedElement).slice(-5)) {
        const crumb = button(catalog.name(frame, element), () => requestSelection(frame, element));
        crumb.title = catalog.name(frame, element); $('#breadcrumbs').append(crumb);
      }
    }
    const rect = selectionRect || {x: 0, y: 0, ...frame.viewport};
    $('#dimensions').replaceChildren();
    for (const [label, value] of [['X', rect.x], ['Y', rect.y], ['W', rect.width], ['H', rect.height]]) {
      const row = make('div', undefined, 'dimension'); row.append(make('span', label), make('span', Math.round(value * 10) / 10)); $('#dimensions').append(row);
    }
    $('#properties').replaceChildren();
    const fields = selectedElement ? [['종류', selectedElement.tag], ['글자', selectedElement.properties?.fontSize], ['굵기', selectedElement.properties?.fontWeight], ['색상', selectedElement.properties?.color], ['모서리', selectedElement.properties?.radius], ['간격', selectedElement.properties?.gap]] : [['언어', frame.locale], ['테마', frame.theme], ['요소', frame.elements.length + '개']];
    for (const [label, value] of fields) if (value) {
      const row = make('div', undefined, 'property'); row.append(make('span', label), make('span', value)); $('#properties').append(row);
    }
    $('#regions').replaceChildren();
    if (!selectedElement) for (const region of frame.regions) {
      const item = button('▧  ' + region.label, () => {
        const element = frame.elements.find(node => node.regions?.includes(region.id) && !frame.elements.find(parent => parent.id === node.parent)?.regions?.includes(region.id));
        if (element) requestSelection(frame, element);
      });
      item.disabled = !region.rect; item.title = region.reason || region.label; $('#regions').append(item);
    }
    $('#selected-selector').textContent = selectedElement?.selector || 'body';
    const region = frame.regions.find(item => selectedElement?.regions?.includes(item.id) && item.source);
    $('#source-reference').textContent = region?.source || '';
    const evidence = quoteEvidence();
    $('#quote').value = evidence.quote;
    $('#quote').hidden = !evidence.quote;
    $('#quote-limit').hidden = !evidence.clipped;
    draftKey = JSON.stringify([frame.id, frame.identity, selectedElement?.id || null]);
    const draft = drafts.get(draftKey);
    $('#note').value = draft?.message || '';
    $('#note-kind').value = draft?.kind || 'proposal';
    $('#conditions').textContent = frame.conditions || '';
    const origin = frame.origin;
    const observed = origin ? atlas.composition.observations[origin.atlas] : null;
    $('#observation-link').hidden = !origin;
    if (origin) $('#observation-link').href = '../' + origin.manifest;
    $('#payload').textContent = JSON.stringify({state: origin?.frame || frame.id,
      ...(origin ? {origin: {atlas: origin.atlas, manifest: origin.manifest, identity: frame.identity, captured_at: observed.captured_at, source_revision: observed.source.revision ?? null, recipe_sha256: observed.recipe.sha256 ?? null}} : {}),
      viewport: frame.viewport, locale: frame.locale, theme: frame.theme, ...frame.payload}, null, 2);
    const section = catalog.section(frame), journey = catalog.flow(frame), index = journey.indexOf(frame);
    $('#previous').disabled = index <= 0; $('#next').disabled = index >= journey.length - 1;
    const details = make('dl');
    for (const [name, value] of catalog.description(section)) details.append(make('dt', name), make('dd', value));
    $('#section-details').replaceChildren(make('p', frame.evidence === 'synthetic' ? '합성 조건으로 관찰한 상태입니다.' : '기록된 화면 상태입니다.'), details);
    $('#journey-steps').replaceChildren();
    for (const step of journey) {
      const item = make('li'); item.append(button(step.label, () => chooseFrame(step, true), step.id === frame.id ? 'active' : ''));
      $('#journey-steps').append(item);
    }
    renderNotes(); renderStateLinks();
  }
  function elementLinks(frame, element) {
    const selectors = new Set(catalog.ancestors(frame, element).map(node => node.selector));
    return (frame.transitions || []).filter(link => frameById.has(link.target) && selectors.has(link.selector));
  }
  function renderStateLinks() {
    const list = $('#state-links'); list.replaceChildren();
    if (!selectedFrame) return;
    const specific = selectedElement ? elementLinks(selectedFrame, selectedElement) : [];
    const links = specific.length ? specific : (selectedFrame.transitions || []).filter(link => frameById.has(link.target));
    if (!links.length) return;
    list.append(make('strong', specific.length ? '선택 요소에서 이어지는 상태' : '이 화면에서 이어지는 상태'));
    for (const link of links) {
      const control = button('→ ' + link.label, () => followLink(link));
      control.dataset.targetState = link.target; list.append(control);
    }
  }
  function followLink(link) {
    const target = frameById.get(link.target);
    const element = link.target_node ? catalog.index(target).elements.get(link.target_node) : null;
    if (element) requestSelection(target, element, {fit: true});
    else chooseFrame(target, true);
  }
  function renderStateConnections() {
    $('#world').querySelector('.state-connections')?.remove();
    if (!atlas.composition) return;
    const svg = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    svg.classList.add('state-connections'); svg.setAttribute('aria-hidden', 'true');
    for (const frame of frames) {
      const from = positions.get(frame.id); if (!from) continue;
      for (const link of frame.transitions || []) {
        const target = frameById.get(link.target), to = positions.get(link.target);
        if (!to || !target || link.target === frame.id) continue;
        const x = from.x + frame.viewport.width, y = from.y + frame.viewport.height / 2;
        const tx = to.x, ty = to.y + target.viewport.height / 2, bend = Math.max(80, Math.abs(tx - x) / 2);
        const path = document.createElementNS(svg.namespaceURI, 'path');
        path.setAttribute('d', `M${x},${y} C${x + bend},${y} ${tx - bend},${ty} ${tx},${ty}`);
        svg.append(path);
      }
    }
    $('#world').prepend(svg);
  }
  function quoteEvidence() {
    const texts = selectedFrame?.texts.filter(item => item.selector === selectedElement?.selector) || [];
    return {quote: texts.map(item => item.text).join(' '), clipped: texts.some(item => item.clipped)};
  }
  function saveDraft() {
    if (!draftKey) return;
    const message = $('#note').value;
    if (message) drafts.set(draftKey, {message, kind: $('#note-kind').value});
    else drafts.delete(draftKey);
  }
  function hasUnsavedWork() {
    saveDraft();
    return notes.pending.size > 0 || [...drafts.values()].some(draft => draft.message.trim());
  }
  function recheckReason(note) {
    const frame = frameById.get(note.frame), reasons = [];
    if (!frame) reasons.push('현재 전개도에 이 화면이 없습니다.');
    else if (frame.identity !== note.identity) reasons.push('저장 당시와 관찰 근거가 달라졌습니다.');
    const freshness = frame?.origin?.freshness || atlas.freshness;
    if (freshness.status === 'changed') reasons.push('현재 소스·재현 파일이 관찰 당시와 다릅니다.');
    else if (freshness.status === 'unavailable') reasons.push('현재 소스·재현 파일을 확인할 수 없습니다.');
    return reasons.join(' ');
  }
  function renderNotes() {
    $('#frame-notes').replaceChildren();
    if (!selectedFrame) return;
    for (const note of notes.items.filter(item => item.frame === selectedFrame.id)) {
      const row = make('div', undefined, 'saved-note');
      row.dataset.note = note.id;
      row.append(make('span', note.kind === 'observation' ? '관찰 메모' : '수정 제안', 'note-kind'));
      if (recheckReason(note)) row.append(make('span', '재확인 필요 · ' + recheckReason(note), 'stale'));
      if (note.quote) row.append(make('blockquote', note.quote));
      if (note.clipped) row.append(make('small', '화면에는 문구 일부만 보입니다.', 'note-kind'));
      row.append(make('p', note.message), noteActions(note));
      $('#frame-notes').append(row);
    }
  }
  function noteActions(note) {
    const actions = make('div', undefined, 'note-actions');
    actions.append(button('위치 보기', () => locateNote(note)),
      button(note.status === 'reviewed' ? '확인 완료 · 되돌리기' : '확인 완료로 표시', () => notes.change([{...note, status: note.status === 'reviewed' ? 'open' : 'reviewed'}])),
      button('삭제', () => notes.change([], [note.id])));
    return actions;
  }
  function locateNote(note) {
    const frame = frameById.get(note.frame);
    if (!frame) { announce('현재 전개도에 이 화면이 없습니다. 의견은 보관되어 있습니다.'); return; }
    const element = catalog.noteTarget(frame, note);
    if (element) requestSelection(frame, element, {fit: true});
    else { chooseFrame(frame, true); showTab('element'); announce('대응 요소를 확인할 수 없어 화면을 표시합니다.'); }
    if (recheckReason(note)) announce(recheckReason(note) + ' 대상과 내용을 다시 확인해 주세요.');
  }
  function renderReviewList() {
    $('#review-list').replaceChildren();
    const filter = $('#review-filter').value, query = $('#search').value.trim().toLocaleLowerCase();
    const items = notes.items.filter(note => (filter === 'all' || filter === 'stale' && recheckReason(note) || (note.status || 'open') === filter) &&
      [note.message, note.quote, frameById.get(note.frame)?.label].join(' ').toLocaleLowerCase().includes(query));
    if (!items.length) $('#review-list').append(make('p', '표시할 의견이 없습니다.', 'panel-empty'));
    for (const note of items) {
      const row = make('div', undefined, 'review-item'); row.dataset.note = note.id;
      row.append(make('small', (note.kind === 'observation' ? '관찰 메모' : '수정 제안') + ' · ' + (note.status === 'reviewed' ? '확인 완료' : '미검토')),
        button(frameById.get(note.frame)?.label || '현재 화면 없음', () => locateNote(note)), make('p', note.message));
      if (note.quote) row.append(make('small', note.quote));
      if (note.clipped) row.append(make('small', '화면에는 문구 일부만 보입니다.', 'note-kind'));
      if (recheckReason(note)) row.append(make('span', '재확인 필요 · ' + recheckReason(note), 'stale'));
      row.append(noteActions(note)); $('#review-list').append(row);
    }
  }
  function renderPins() {
    $('#world').querySelectorAll('.note-pin').forEach(pin => pin.remove());
    if (!$('#show-notes').checked) return;
    const groups = new Map(), zoom = canvas.camera.zoom;
    for (const note of notes.items) {
      const frame = frameById.get(note.frame); if (!frame) continue;
      const element = catalog.noteTarget(frame, note);
      const key = frame.id + ':' + (zoom < .35 ? 'frame' : element?.id || 'frame');
      if (!groups.has(key)) groups.set(key, {frame, element: zoom < .35 ? null : element, notes: []});
      groups.get(key).notes.push(note);
    }
    for (const group of groups.values()) {
      const position = positions.get(group.frame.id); if (!position) continue;
      const rect = group.element?.visibleRect || group.element?.rect;
      const point = rect ? {x: Math.max(14 / zoom, Math.min(group.frame.viewport.width - 14 / zoom, rect.x + rect.width)),
        y: Math.max(14 / zoom, Math.min(group.frame.viewport.height - 14 / zoom, rect.y))} : {x: group.frame.viewport.width - 16 / zoom, y: 16 / zoom};
      const pin = button(String(group.notes.length), () => { showPanel('reviews'); locateNote(group.notes[0]); }, 'note-pin');
      pin.dataset.canvasAction = 'note'; pin.dataset.note = group.notes[0].id;
      pin.classList.toggle('reviewed', group.notes.every(note => note.status === 'reviewed'));
      pin.classList.toggle('stale-pin', group.notes.some(recheckReason));
      pin.title = group.notes.map(note => note.message).join('\n'); pin.setAttribute('aria-label', group.frame.label + ' · 의견 ' + group.notes.length + '개');
      Object.assign(pin.style, {left: (position.x + point.x) + 'px', top: (position.y + point.y) + 'px'}); $('#world').append(pin);
    }
  }
  function updateNotes() {
    $('#note-count').textContent = notes.items.length; $('#retry-notes').hidden = !notes.pending.size;
    renderNotes(); renderReviewList(); scheduleLayout(); sheetPicker?.changed();
  }
  function requestText() {
    return [`UI Atlas · ${atlas.title}`, `${atlas.composition ? '가장 최근 관찰' : '관찰'}: ${atlas.captured_at}`, `범위: ${atlas.scope}`, '', ...notes.items.map((note, index) => {
      const frame = frameById.get(note.frame);
      return `${index + 1}. ${frame ? frame.surface + ' / ' + frame.label : '현재 화면 없음'} [${note.frame}]\n` +
        (note.origin ? `원본 시트: ${note.origin.atlas} / ${note.origin.frame}\n` : '') + `요소: ${note.selector || note.region || '화면'}\n` + (note.quote ? `문구: ${note.quote}\n` : '') +
        (note.clipped ? '문구 관찰: 화면에는 일부만 보였으며 인용은 DOM 전체 문구입니다.\n' : '') +
        (note.source ? `확인한 소스: ${note.source}\n` : '') + `종류: ${note.kind === 'observation' ? '관찰 메모' : '수정 제안'} · ${note.status === 'reviewed' ? '확인 완료' : '미검토'}\n의견: ${note.message}\n` +
        (recheckReason(note) ? '재확인: ' + recheckReason(note) + '\n' : '') + `관찰 식별: ${note.identity}`;
    }), '', '현재 소스와 재현 조건을 확인한 뒤 요청의 뜻과 범위에 맞게 진행해 주세요. 저장만으로 소스 변경을 승인한 것은 아닙니다.'].join('\n\n');
  }
  function handoff(title, description, content) {
    $('#handoff-title').textContent = title; $('#handoff-description').textContent = description;
    $('#handoff-text').value = content; $('#handoff').showModal();
  }
  function download(name, value) {
    const url = URL.createObjectURL(new Blob([JSON.stringify(value, null, 2)], {type: 'application/json'}));
    const link = make('a'); link.href = url; link.download = name; link.click();
    setTimeout(() => URL.revokeObjectURL(url), 1000);
  }
  window.addEventListener('message', event => {
    const message = event.data;
    if (message?.channel !== 'ui-atlas-dom') return;
    const found = [...mounted].find(([, entry]) => entry.iframe.contentWindow === event.source && entry.token === message.token);
    if (!found) return;
    const [id, entry] = found;
    if (message.type === 'ready') {
      entry.ready = true; entry.card.dataset.ready = 'true';
      if (pendingPick?.frame === id) sendSelection();
      if (document.activeElement === entry.iframe) $('#canvas').focus({preventScroll: true});
    }
    else if (message.type === 'error') {
      entry.card.append(make('div', message.message, 'frame-error')); entry.card.dataset.ready = 'error';
    } else if (message.type === 'selected') selectElement(frameById.get(id), message.element, message.request);
    else if (message.type === 'hovered' && hoveredFrame === id && !canvas.drag) paintBox('hover', message.element ? {frame: id, rect: message.element.rect} : null);
  });
  $('#note-form').onsubmit = event => {
    event.preventDefault();
    const message = $('#note').value.trim();
    if (!message || !selectedFrame) return;
    const region = selectedFrame.regions.find(item => selectedElement?.regions?.includes(item.id));
    const saved = notes.change([{id: crypto.randomUUID(), frame: selectedFrame.id, identity: selectedFrame.identity,
      node: selectedElement?.id || null, region: region?.id || null, ...quoteEvidence(),
      selector: selectedElement?.selector || '', source: region?.source || '', kind: $('#note-kind').value, status: 'open', message, created_at: new Date().toISOString()}]);
    drafts.delete(draftKey); $('#note').value = ''; if (saved) announce('의견을 저장했습니다.');
  };
  $('#note').oninput = saveDraft;
  $('#note-kind').onchange = saveDraft;
  window.addEventListener('beforeunload', event => {
    if (hasUnsavedWork()) { event.preventDefault(); event.returnValue = ''; }
  });
  $('#replay').onclick = () => handoff('상태 재현', '이 장면은 고정된 DOM입니다. 아래 명령은 격리된 실제 앱을 같은 상태까지 실행합니다.', (selectedFrame.origin?.replay || atlas.replay).replaceAll('STATE_ID', selectedFrame.origin?.frame || selectedFrame.id));
  $('#requests').onclick = () => showPanel('reviews');
  $('#collect-notes').onclick = () => handoff('의견 모으기', '선택한 요소와 의견을 함께 복사해 작업 세션에 전달하세요.', requestText());
  $('#review-filter').onchange = renderReviewList;
  $('#close-handoff').onclick = () => $('#handoff').close();
  $('#copy-request').onclick = async () => {
    try { await navigator.clipboard.writeText($('#handoff-text').value); announce('복사했습니다.'); }
    catch { $('#handoff-text').focus(); $('#handoff-text').select(); }
  };
  $('#notes-download').onclick = () => { download(atlas.id + '-notes.json', notes.export()); $('#file-menu').hidden = true; };
  $('#retry-notes').onclick = () => { if (notes.change()) announce('의견을 저장했습니다.'); $('#file-menu').hidden = true; };
  $('#import').onclick = () => { $('#import-file').click(); $('#file-menu').hidden = true; };
  function chooseImportedNotes(plan) {
    const dialog = $('#note-import'), list = $('#import-conflicts'), choices = new Map();
    const names = {message: '의견', status: '검토 상태', kind: '종류', quote: '인용 문구', clipped: '일부 문구만 표시됨',
      frame: '화면', selector: '요소', source: '소스', region: '영역', identity: '관찰 식별', created_at: '작성 시각', node: '관찰 요소 식별'};
    const display = (key, value) => {
      if (key === 'status') return value === 'reviewed' ? '확인 완료' : '미검토';
      if (key === 'kind') return value === 'observation' ? '관찰 메모' : '수정 제안';
      return value == null ? '없음' : typeof value === 'string' ? value : JSON.stringify(value);
    };
    list.replaceChildren(); dialog.returnValue = 'cancel';
    for (const note of plan.conflicts) {
      const current = plan.before.get(note.id), row = make('section', undefined, 'import-conflict');
      row.append(make('h3', current.message || note.message));
      const frame = frameById.get(current.frame);
      row.append(make('p', (frame ? frame.surface + ' / ' + frame.label : current.frame) + ' · ' + (current.selector || current.region || '화면 전체')));
      const select = make('select'); select.setAttribute('aria-label', '사용할 의견');
      for (const [value, label] of [['local', '현재 의견 유지'], ['file', '파일 의견 사용']]) {
        const option = make('option', label); option.value = value; select.append(option);
      }
      choices.set(note.id, select); row.append(select);
      const differences = make('dl');
      for (const key of new Set([...Object.keys(current), ...Object.keys(note)])) {
        if (JSON.stringify(current[key]) === JSON.stringify(note[key])) continue;
        differences.append(make('dt', names[key] || key), make('dd', '현재: ' + display(key, current[key])), make('dd', '파일: ' + display(key, note[key])));
      }
      row.append(differences); list.append(row);
    }
    return new Promise(resolve => {
      dialog.addEventListener('close', () => resolve(dialog.returnValue === 'apply'
        ? new Map([...choices].map(([id, select]) => [id, select.value])) : null), {once: true});
      dialog.showModal();
    });
  }
  $('#import-file').onchange = async event => {
    try {
      if (!event.target.files.length) return;
      const plan = notes.planImport(JSON.parse(await event.target.files[0].text()));
      const choices = plan.conflicts.length ? await chooseImportedNotes(plan) : new Map();
      if (choices === null) { announce('가져오기를 취소했습니다.'); return; }
      if (notes.applyImport(plan, choices)) announce('선택한 의견을 반영했습니다. 변경된 화면의 의견은 재확인이 필요합니다.');
    } catch (error) { announce(error.message); }
    finally { event.target.value = ''; }
  };
  $('#file-menu-button').onclick = () => $('#file-menu').hidden = !$('#file-menu').hidden;
  document.addEventListener('click', event => { if (!event.target.closest('#file-menu,#file-menu-button')) $('#file-menu').hidden = true; });
  $('#reset-layout').onclick = () => { clearSelection(); canvas.reset(); buildCanvas(); fitAll(); $('#file-menu').hidden = true; };
  $('#toggle-sidebar').onclick = () => $('#sidebar').hidden = !$('#sidebar').hidden;
  $('#close-inspector').onclick = clearSelection;
  document.querySelectorAll('[data-panel]').forEach(item => item.onclick = () => showPanel(item.dataset.panel));
  document.querySelectorAll('[data-tab]').forEach(item => item.onclick = () => showTab(item.dataset.tab));
  $('#search').oninput = renderSearch;
  $('#search').onkeydown = event => {
    if (event.key === 'Enter' && activePanel !== 'reviews') { event.preventDefault(); $('#search-results .search-result')?.click(); }
  };
  $('#previous').onclick = () => navigate(-1); $('#next').onclick = () => navigate(1);
  function navigate(direction) {
    const flow = catalog.flow(selectedFrame);
    const next = flow[flow.indexOf(selectedFrame) + direction]; if (!next) return;
    if (!selectedElement && !comparison) { chooseFrame(next, true); return; }
    if (!comparison) comparison = {frame: selectedFrame, element: selectedElement, rect: selectionRect};
    const rect = selectionRect || comparison.rect, position = positions.get(selectedFrame.id), camera = canvas.camera;
    comparison.rect = rect; // Missing states carry the most recently inspected geometry.
    const anchor = {x: camera.x + (position.x + rect.x + rect.width / 2) * camera.zoom,
      y: camera.y + (position.y + rect.y + rect.height / 2) * camera.zoom};
    const target = catalog.match(comparison.frame, comparison.element, next);
    if (target) requestSelection(next, target, {comparing: true, anchor});
    else {
      chooseFrame(next, false, true); placeAtAnchor(next, rect, anchor);
      $('#comparison-status').hidden = false; $('#comparison-status').textContent = '대응 요소 없음 또는 식별 불가 · 같은 위치 유지';
    }
  }
  function setTool(tool) {
    canvas.setTool(tool);
    $('#select-tool').classList.toggle('active', tool === 'select'); $('#hand-tool').classList.toggle('active', tool === 'hand');
  }
  $('#select-tool').onclick = () => setTool('select'); $('#hand-tool').onclick = () => setTool('hand');
  $('#zoom-in').onclick = () => canvas.zoomAt(canvas.camera.zoom * 1.25);
  $('#zoom-out').onclick = () => canvas.zoomAt(canvas.camera.zoom / 1.25);
  $('#zoom-value').onclick = () => {
    $('#view-menu').hidden = !$('#view-menu').hidden;
    $('#zoom-value').setAttribute('aria-expanded', String(!$('#view-menu').hidden));
    $('#zoom-input').value = zoomPercent(canvas.camera.zoom);
  };
  function closeViewMenu() { $('#view-menu').hidden = true; $('#zoom-value').setAttribute('aria-expanded', 'false'); }
  $('#zoom-input').onchange = () => {
    const value = Number($('#zoom-input').value);
    if (Number.isFinite(value) && value > 0) canvas.zoomAt(value / 100);
    $('#zoom-input').value = zoomPercent(canvas.camera.zoom);
  };
  $('#zoom-input').onkeydown = event => {
    if (event.key === 'Enter') { $('#zoom-input').onchange(); closeViewMenu(); }
    else if (event.key === 'Escape') { closeViewMenu(); $('#zoom-value').focus(); }
  };
  $('#menu-fit-all').onclick = () => { fitAll(); closeViewMenu(); };
  $('#menu-fit-selection').onclick = () => { fitSelection(); closeViewMenu(); };
  $('#menu-actual-size').onclick = () => { canvas.zoomAt(1); closeViewMenu(); };
  $('#fit-all').onclick = fitAll;
  $('#show-descriptions').onchange = () => { sections.showDescriptions = $('#show-descriptions').checked; scheduleLayout(); };
  $('#show-notes').onchange = renderPins;
  $('#focus-view').onclick = () => {
    const focused = document.body.classList.toggle('focus-view');
    $('#focus-view').setAttribute('aria-pressed', String(focused));
    $('#focus-view').setAttribute('aria-label', focused ? '패널 펼치기' : '패널 접기');
    scheduleLayout();
  };
  document.addEventListener('click', event => { if (!event.target.closest('#view-menu,#zoom-value')) closeViewMenu(); });
  window.addEventListener('resize', () => {
    const compact = narrow();
    if (compact !== wasNarrow) { $('#sidebar').hidden = compact; wasNarrow = compact; }
    scheduleLayout(); if (selectedFrame) fitLater(fitSelection);
  });
  window.addEventListener('keydown', event => {
    if (event.target.closest('input,textarea,select,[contenteditable=true]') || document.querySelector('dialog[open]')) return;
    if (event.code === 'Space') { event.preventDefault(); canvas.space = true; canvas.setTool(canvas.tool); }
    else if (event.key.toLowerCase() === 'h') setTool('hand');
    else if (event.key.toLowerCase() === 'v') setTool('select');
    else if (event.shiftKey && event.code === 'Digit1') { event.preventDefault(); fitAll(); }
    else if (event.shiftKey && event.code === 'Digit2') { event.preventDefault(); fitSelection(); }
    else if (event.key === 'Escape') { closeViewMenu(); clearSelection(); }
    else if (event.key === 'Enter' && !event.target.closest('button,[role=button]') && selectedElement?.parent) requestSelection(selectedFrame, catalog.index(selectedFrame).elements.get(selectedElement.parent));
  });
  window.addEventListener('keyup', event => { if (event.code === 'Space') { canvas.space = false; canvas.setTool(canvas.tool); } });
  $('#title').textContent = atlas.title; document.title = atlas.title + ' · Atlas';
  $('#freshness-dot').classList.toggle('changed', atlas.freshness.status !== 'matched');
  const freshness = {matched: '생성 시 선언된 소스와 일치', changed: '소스 변경 · 갱신 필요', unavailable: '소스 확인 불가'}[atlas.freshness.status];
  for (const text of [atlas.scope, `${frames.length}개 DOM 장면 · ${frames.reduce((sum, frame) => sum + frame.elements.length, 0)}개 요소`,
    '상태별 실제 DOM을 고정한 관찰 화면입니다. 앱 동작은 Payload의 상태 재현에서 실행합니다.',
    freshness, (atlas.composition ? '가장 최근 관찰: ' : '관찰: ') + atlas.captured_at, '소스 확인: ' + atlas.freshness.checked_at,
    '파일 변경을 자동으로 감시하지 않습니다.', ...atlas.limitations, ...atlas.freshness.changed, ...atlas.freshness.unavailable,
    ...(atlas.journey_failures || []).map(failure => '시나리오 실패: ' + failure.id + ' · ' + failure.reason),
    ...frames.flatMap(frame => (frame.warnings || []).map(warning => frame.label + ': ' + warning))]) $('#provenance').append(make('p', text));
  for (const frame of missing) $('#missing-states').append(make('strong', (labels[frame.status] || frame.status) + ' · ' + frame.label), make('p', frame.reason));
  $('#coverage').textContent = `${frames.length}개 장면` + (missing.length ? ` · 범위 확인 ${missing.length}` : '');
  $('#info').onclick = $('#coverage').onclick = () => $('#information').showModal();
  $('#close-info').onclick = () => $('#information').close();
  $('#topic-tools').hidden = !atlas.composition;
  $('#viewport-filter').onchange = () => setVariant($('#viewport-filter').value);
  if (narrow()) $('#sidebar').hidden = true;
  buildCanvas(); updateNotes();
  if (atlas.composition) {
    const first = [...catalog.sections.values()][0]?.frames[0];
    if (first) canvas.fit(frameBounds(first), .6);
  }
  sheetPicker = new AtlasSheetPicker(atlas.id, hasUnsavedWork);
})();
