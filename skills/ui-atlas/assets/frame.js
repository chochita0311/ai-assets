(config) => {
  'use strict';
  /* ATLAS_GEOMETRY */
  const send = (type, detail = {}) => parent.postMessage({channel: 'ui-atlas-dom', token: config.token, type, ...detail}, '*');
  const byId = id => document.querySelector('[data-atlas-node="' + CSS.escape(id) + '"]');
  const box = element => {
    const rect = element.getBoundingClientRect();
    return {x: rect.x, y: rect.y, width: rect.width, height: rect.height};
  };
  function describe(element) {
    if (!element || !geometry.visible(element)) return null;
    const rect = geometry.clip(element.getBoundingClientRect(), element);
    if (!rect) return null;
    const ancestors = [];
    for (let node = element; node; node = node.parentElement) if (node.dataset.atlasNode) ancestors.push(node.dataset.atlasNode);
    return {id: element.dataset.atlasNode, rect, ancestors};
  }
  function pick(x, y) {
    return document.elementFromPoint(x, y)?.closest('[data-atlas-node]');
  }
  // Product actions never run in the observation canvas. Interaction uses the
  // parent's transparent hit surface, including over disabled native controls.
  document.addEventListener('click', event => event.preventDefault(), true);
  document.addEventListener('submit', event => event.preventDefault(), true);
  window.addEventListener('message', event => {
    const data = event.data;
    if (event.source !== parent || data?.channel !== 'ui-atlas-dom' || data.token !== config.token) return;
    if (data.type === 'pick' || data.type === 'hover') {
      send(data.type === 'pick' ? 'selected' : 'hovered', {element: describe(pick(data.x, data.y)), request: data.request});
    } else if (data.type === 'select') {
      send('selected', {element: describe(byId(data.id)), request: data.request});
    } else if (data.type === 'measure') {
      send('measured', {elements: [...document.querySelectorAll('[data-atlas-node]')].map(element => ({id: element.dataset.atlasNode, rect: box(element)}))});
    }
  });
  async function initialize() {
    // The embedded bridge runs before the closing body tag; wait for parsing
    // before restoring native state and declaring the frame ready.
    if (document.readyState === 'loading') await new Promise(resolve => document.addEventListener('DOMContentLoaded', resolve, {once: true}));
    await document.fonts.ready;
    for (const element of document.querySelectorAll('[data-atlas-indeterminate]')) element.indeterminate = true;
    for (const element of document.querySelectorAll('select[data-atlas-no-selection]')) element.selectedIndex = -1;
    const modals = [...document.querySelectorAll('[data-atlas-modal]')].sort((a, b) => Number(a.hasAttribute('data-atlas-top-modal')) - Number(b.hasAttribute('data-atlas-top-modal')));
    for (const element of modals) {
      element.removeAttribute('open'); element.showModal();
      // Native top-layer centering is not fully represented by resolved margins.
      // Preserve the observed viewport position without flattening its children.
      const expected = JSON.parse(element.dataset.atlasTopLayerBox);
      Object.assign(element.style, {position: 'fixed', inset: 'auto', margin: '0',
        left: expected.x + 'px', top: expected.y + 'px'});
    }
    for (const element of document.querySelectorAll('[data-atlas-popover]')) element.showPopover();
    for (const element of document.querySelectorAll('[data-atlas-scroll-y]')) {
      element.scrollTo({left: Number(element.dataset.atlasScrollX), top: Number(element.dataset.atlasScrollY), behavior: 'instant'});
    }
    window.scrollTo({left: config.scroll.x, top: config.scroll.y, behavior: 'instant'});
    document.body.getBoundingClientRect();
    send('ready', {count: document.querySelectorAll('[data-atlas-node]').length});
  }
  return initialize().catch(error => { send('error', {message: error.message}); throw error; });
}
