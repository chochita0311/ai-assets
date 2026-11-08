// Shared by the read-only observer, materializer and inert selection bridge.
const geometry = (() => {
  const clipParent = element => {
    if (element.matches(':modal, :popover-open')) return null;
    // Positioned HTML boxes escape DOM overflow ancestors until their actual layout
    // parent. The browser also resolves transform/filter/containment boundaries.
    if (element instanceof HTMLElement && element.getClientRects().length &&
        ['absolute', 'fixed'].includes(getComputedStyle(element).position)) return element.offsetParent;
    return element.parentElement;
  };
  const clip = (r, element, includeSelf = false) => {
    let x = Math.max(0, r.x), y = Math.max(0, r.y);
    let right = Math.min(innerWidth, r.right), bottom = Math.min(innerHeight, r.bottom);
    for (let parent = includeSelf ? element : clipParent(element); parent; parent = clipParent(parent)) {
      const style = getComputedStyle(parent);
      if (style.overflowX === 'visible' && style.overflowY === 'visible') continue;
      // Root overflow, and body overflow propagated through a visible root,
      // apply to the viewport already intersected above, not a short body box.
      if (parent === document.documentElement) continue;
      const rootStyle = parent === document.body ? getComputedStyle(document.documentElement) : null;
      if (rootStyle?.overflowX === 'visible' && rootStyle.overflowY === 'visible') continue;
      const box = parent.getBoundingClientRect();
      const scaleX = parent.offsetWidth ? box.width / parent.offsetWidth : 1;
      const scaleY = parent.offsetHeight ? box.height / parent.offsetHeight : 1;
      const left = box.left + parent.clientLeft * scaleX;
      const top = box.top + parent.clientTop * scaleY;
      if (style.overflowX !== 'visible') {
        x = Math.max(x, left); right = Math.min(right, left + parent.clientWidth * scaleX);
      }
      if (style.overflowY !== 'visible') {
        y = Math.max(y, top); bottom = Math.min(bottom, top + parent.clientHeight * scaleY);
      }
    }
    if (right <= x || bottom <= y) return null;
    return {x, y, width: right - x, height: bottom - y};
  };
  const visible = element => {
    if (getComputedStyle(element).visibility !== 'visible') return false;
    for (let node = element; node; node = node.parentElement) {
      const style = getComputedStyle(node);
      if (style.display === 'none' || Number(style.opacity) === 0) return false;
    }
    return element.getClientRects().length > 0;
  };
  const selector = element => {
    const parts = [];
    for (let node = element; node; node = node.parentElement) {
      if (node.id && document.querySelectorAll('#' + CSS.escape(node.id)).length === 1) {
        parts.unshift('#' + CSS.escape(node.id)); break;
      }
      const siblings = node.parentElement ? [...node.parentElement.children].filter(item => item.localName === node.localName) : [];
      parts.unshift(node.localName + (siblings.length > 1 ? `:nth-of-type(${siblings.indexOf(node) + 1})` : ''));
    }
    return parts.join(' > ');
  };
  return {clip, visible, selector};
})();
