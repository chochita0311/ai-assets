(definitions) => {
  // Read-only viewport observations; no changes to product nodes or styles.
  const viewport = {width: innerWidth, height: innerHeight};
  /* ATLAS_GEOMETRY */
  const {clip, visible, selector} = geometry;
  const regions = definitions.map(definition => {
    const nodes = document.querySelectorAll(definition.selector);
    const node = nodes.length === 1 ? nodes[0] : null;
    const rect = node && visible(node) ? clip(node.getBoundingClientRect(), node) : null;
    return {...definition, rect, reason: rect ? null : nodes.length > 1 ? 'Selector matches multiple elements' : 'Not visible in this viewport/state'};
  });
  const texts = [];
  const walker = document.createTreeWalker(document.body, NodeFilter.SHOW_TEXT);
  for (let node; (node = walker.nextNode());) {
    const element = node.parentElement;
    if (!element || element.closest('script,style,noscript,template') || !node.textContent.trim() || !visible(element)) continue;
    const range = document.createRange(); range.selectNodeContents(node);
    const original = range.getBoundingClientRect();
    const rect = clip(original, element, true);
    if (!rect) continue;
    const hit = document.elementFromPoint(rect.x + rect.width / 2, rect.y + rect.height / 2);
    const transparentHit = getComputedStyle(element).pointerEvents === 'none' && hit?.contains(element);
    if (!hit || !(element === hit || element.contains(hit) || transparentHit)) continue;
    const clipped = rect.width + 0.5 < original.width || rect.height + 0.5 < original.height;
    texts.push({text: node.textContent.trim(), selector: selector(element), rect, clipped,
      regions: definitions.filter(item => element.closest(item.selector)).map(item => item.id)});
  }
  return {viewport, regions, texts, scroll: {x: scrollX, y: scrollY}};
}
