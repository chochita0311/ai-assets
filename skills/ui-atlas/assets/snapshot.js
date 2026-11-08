async (definitions) => {
  'use strict';
  /* ATLAS_GEOMETRY */
  definitions = definitions || [];
  const fail = message => { throw new Error('DOM frame: ' + message); };
  if (document.compatMode !== 'CSS1Compat') fail('A standards-mode document is required');
  if (!Element.prototype.computedStyleMap) fail('Computed sizing requires CSS Typed OM support');
  await document.fonts.ready;
  const originalNodes = [document.documentElement, ...document.documentElement.querySelectorAll('*')];
  const root = document.documentElement.cloneNode(true);
  const clonedNodes = [root, ...root.querySelectorAll('*')];
  const copies = new Map(originalNodes.map((element, index) => [element, clonedNodes[index]]));
  const skip = 'script,style,link,meta,base,template,noscript,source';
  const unsupported = 'canvas,iframe,frame,object,embed,video,audio,foreignObject,plaintext,xmp,noembed,noframes,animate,set,animateColor,animateTransform,animateMotion,discard';
  const assets = new Map();
  const styles = new Map();
  const rules = [];
  const computedRules = [];
  const elements = [];
  const ids = new Map();
  const sprites = new Map();
  const warnings = [];
  const viewport = {width: innerWidth, height: innerHeight};

  const rect = element => {
    const box = element.getBoundingClientRect();
    return {x: box.x, y: box.y, width: box.width, height: box.height};
  };
  const encode = blob => new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = reject;
    reader.readAsDataURL(blob);
  });
  async function resource(value, base = document.baseURI) {
    if (!value || value.startsWith('#') || value.startsWith('data:')) return value;
    const address = new URL(value, base);
    if (address.origin !== location.origin && address.protocol !== 'blob:') fail('Resource outside the isolated app: ' + address.origin);
    const fragment = address.hash; address.hash = '';
    if (!assets.has(address.href)) {
      assets.set(address.href, (async () => {
        const response = await fetch(address.href, {credentials: 'same-origin'});
        if (!response.ok) fail('Resource unavailable: ' + address.pathname);
        return encode(await response.blob());
      })());
    }
    return (await assets.get(address.href)) + fragment;
  }
  async function cssAssets(text, base = document.baseURI) {
    const pattern = /url\(\s*(?:"([^"\n]*)"|'([^'\n]*)'|([^)]*))\s*\)/gi;
    let result = '', cursor = 0;
    for (const match of text.matchAll(pattern)) {
      result += text.slice(cursor, match.index) + 'url("' + await resource((match[1] ?? match[2] ?? match[3]).trim(), base) + '")';
      cursor = match.index + match[0].length;
    }
    return result + text.slice(cursor);
  }
  async function computed(element, pseudo) {
    const style = getComputedStyle(element, pseudo);
    const declarations = {};
    for (const property of style) {
      if (property.startsWith('--') || /^(animation|transition|scroll-timeline|view-timeline)/.test(property)) continue;
      // Resolved physical properties already include writing-mode mapping.
      // Reapplying logical aliases can override a different physical longhand.
      if (/^(?:min-|max-)?(?:block-size|inline-size)$|^(?:margin|padding|inset|border|overflow|scroll-margin|scroll-padding)-(?:block|inline)|^border-(?:start|end)-/.test(property)) continue;
      let value = style.getPropertyValue(property);
      if (value.includes('url(')) value = await cssAssets(value);
      declarations[property] = value;
    }
    declarations.animation = 'none'; declarations.transition = 'none';
    // A definite height prevents a block's last child margin from collapsing.
    // Keep auto only where that relationship can occur; other resolved heights
    // also stabilize native/normal line boxes across standalone browser contexts.
    const collapsingChildren = !pseudo && ['block', 'list-item'].includes(style.display) &&
      style.overflowX === 'visible' && style.overflowY === 'visible' &&
      parseFloat(style.paddingBottom) === 0 && parseFloat(style.borderBottomWidth) === 0 &&
      [...element.children].some(child => {
        const childStyle = getComputedStyle(child);
        return childStyle.display !== 'none' && !childStyle.display.startsWith('inline') &&
          !['absolute', 'fixed'].includes(childStyle.position) && childStyle.float === 'none';
      });
    if (collapsingChildren && element.computedStyleMap().get('height')?.toString() === 'auto') declarations.height = 'auto';
    return declarations;
  }
  async function fontRules(sheet, base = document.baseURI) {
    base = sheet.href || base;
    let css;
    try { css = sheet.cssRules; } catch { fail('Stylesheet fonts are not readable'); }
    for (const rule of css) {
      if (rule.type === CSSRule.FONT_FACE_RULE) rules.push(await cssAssets(rule.cssText, base));
      else if (rule.type === CSSRule.IMPORT_RULE) await fontRules(rule.styleSheet);
      else if (rule.cssRules) await fontRules(rule, base);
    }
  }
  for (const sheet of document.styleSheets) if (!sheet.disabled) await fontRules(sheet);
  for (const sheet of document.adoptedStyleSheets) await fontRules(sheet);

  for (const original of originalNodes) {
    const copy = copies.get(original);
    if (!root.contains(copy) && copy !== root) continue;
    if (original.matches(skip)) { copy.remove(); continue; }
    if (original.shadowRoot || original.matches(unsupported)) fail('Unsupported rendering surface: ' + original.localName);
    const id = 'e' + ids.size;
    ids.set(original, id);
    copy.setAttribute('data-atlas-node', id);
    const style = await computed(original);
    const styleKey = JSON.stringify(style);
    if (!styles.has(styleKey)) {
      const key = 's' + styles.size;
      styles.set(styleKey, key);
      computedRules.push({selector: `[data-atlas-style="${key}"]`, properties: style});
    }
    copy.removeAttribute('style');
    copy.setAttribute('data-atlas-style', styles.get(styleKey));
    for (const pseudo of ['::before', '::after', '::marker', '::backdrop']) {
      const state = getComputedStyle(original, pseudo);
      if (pseudo === '::backdrop' ? !original.matches(':modal') : pseudo === '::marker' ? getComputedStyle(original).display !== 'list-item' : ['none', 'normal', ''].includes(state.content)) continue;
      computedRules.push({selector: `[data-atlas-node="${id}"]${pseudo}`, properties: await computed(original, pseudo)});
    }
    for (const attribute of [...copy.attributes]) {
      if (/^on/i.test(attribute.name) || ['is','autofocus','action','formaction','ping','srcset','sizes','target','download','nonce','integrity'].includes(attribute.name)) copy.removeAttribute(attribute.name);
    }
    if (original.matches('a,area')) copy.setAttribute('href', '#');
    if (original instanceof HTMLImageElement) {
      if (!original.complete || !original.naturalWidth) fail('Image is not ready: ' + original.currentSrc);
      copy.setAttribute('src', await resource(original.currentSrc || original.src));
      copy.removeAttribute('loading');
    } else if (original instanceof HTMLInputElement && original.type === 'image' && original.src) {
      copy.setAttribute('src', await resource(original.src));
    } else if (original.localName === 'use') {
      const href = original.getAttribute('href') || original.getAttribute('xlink:href');
      if (href && !href.startsWith('#')) {
        const address = new URL(href, document.baseURI);
        if (address.origin !== location.origin) fail('External SVG sprite is not isolated');
        const fragment = address.hash.slice(1); address.hash = '';
        if (!sprites.has(address.href)) {
          const response = await fetch(address.href);
          if (!response.ok) fail('SVG sprite is unavailable');
          const svg = new DOMParser().parseFromString(await response.text(), 'image/svg+xml');
          // Imported nodes do not pass through the source DOM traversal. Reject
          // styles that could escape the external document's scope, and apply
          // the same unsupported-surface boundary before recording this state.
          if (svg.querySelector('parsererror,script,style,link,base,template,noscript,image,use,' + unsupported)) fail('Unsupported SVG sprite content');
          const prefix = 'atlas-sprite-' + sprites.size + '-';
          for (const node of svg.querySelectorAll('[id]')) node.id = prefix + node.id;
          for (const node of svg.querySelectorAll('*')) for (const attribute of [...node.attributes]) {
            if (/^on/i.test(attribute.name)) node.removeAttribute(attribute.name);
            else if (['href', 'xlink:href'].includes(attribute.name) && attribute.value.startsWith('#')) {
              node.setAttribute(attribute.name, '#' + prefix + attribute.value.slice(1));
            } else if (/url\(/i.test(attribute.value)) {
              node.setAttribute(attribute.name, attribute.value.replace(/url\(\s*(['"]?)#([^\s)'"]+)\1\s*\)/gi,
                (_, quote, id) => 'url(#' + prefix + id + ')'));
            }
          }
          sprites.set(address.href, {prefix, html: svg.documentElement.innerHTML});
        }
        copy.removeAttribute('xlink:href');
        copy.setAttribute('href', '#' + sprites.get(address.href).prefix + fragment);
      }
    } else if (original.namespaceURI === 'http://www.w3.org/2000/svg') {
      for (const name of ['href', 'xlink:href']) if (copy.hasAttribute(name)) copy.setAttribute(name, await resource(copy.getAttribute(name)));
    }
    if (original instanceof HTMLInputElement) {
      if (original.type === 'file' && original.files.length) fail('Selected file inputs require an app-owned preview');
      copy.setAttribute('value', original.value);
      copy.toggleAttribute('checked', original.checked);
      if (original.indeterminate) copy.setAttribute('data-atlas-indeterminate', '');
    }
    if (original instanceof HTMLTextAreaElement) copy.textContent = original.value;
    if (original instanceof HTMLOptionElement) copy.toggleAttribute('selected', original.selected);
    if (original instanceof HTMLSelectElement && original.selectedIndex === -1) copy.setAttribute('data-atlas-no-selection', '');
    if (original instanceof HTMLDetailsElement) copy.toggleAttribute('open', original.open);
    if (original.matches(':modal')) {
      if (getComputedStyle(original).transform !== 'none') fail('Transformed top-layer dialogs need an app-owned preview');
      copy.setAttribute('data-atlas-modal', '');
      copy.setAttribute('data-atlas-top-layer-box', JSON.stringify(rect(original)));
    }
    if (original.matches(':modal') && original.contains(document.activeElement)) copy.setAttribute('data-atlas-top-modal', '');
    if (original.matches(':popover-open')) copy.setAttribute('data-atlas-popover', '');
    if (original.scrollTop || original.scrollLeft) {
      copy.setAttribute('data-atlas-scroll-x', original.scrollLeft);
      copy.setAttribute('data-atlas-scroll-y', original.scrollTop);
    }
    const directText = [...original.childNodes].filter(node => node.nodeType === Node.TEXT_NODE).map(node => node.textContent).join(' ').replace(/\s+/g, ' ').trim();
    const box = rect(original);
    const appearance = getComputedStyle(original);
    const visibleRect = geometry.visible(original) ? geometry.clip(original.getBoundingClientRect(), original) : null;
    elements.push({id, parent: ids.get(original.parentElement) || null, tag: original.localName,
      selector: geometry.selector(original), text: directText,
      regions: definitions.filter(region => original.closest(region.selector)).map(region => region.id),
      label: original.getAttribute('aria-label') || directText.slice(0, 80) || original.getAttribute('title') || original.getAttribute('placeholder') || original.localName + (original.id ? '#' + original.id : ''),
      rect: box, visibleRect, visible: !!visibleRect,
      properties: {color: appearance.color, background: appearance.backgroundColor, font: appearance.fontFamily,
        fontSize: appearance.fontSize, fontWeight: appearance.fontWeight, padding: appearance.padding,
        gap: appearance.gap, radius: appearance.borderRadius, display: appearance.display}});
  }
  const head = root.querySelector('head');
  // Share computed defaults across nodes without changing their resolved values.
  // This keeps a canvas of many real DOM documents small enough to inspect.
  const frequencies = new Map();
  for (const rule of computedRules) for (const [property, value] of Object.entries(rule.properties)) {
    if (!frequencies.has(property)) frequencies.set(property, new Map());
    const values = frequencies.get(property); values.set(value, (values.get(value) || 0) + 1);
  }
  const common = Object.fromEntries([...frequencies].map(([property, values]) => [property, [...values].sort((a, b) => b[1] - a[1])[0][0]]));
  const declarations = properties => Object.entries(properties).map(([key, value]) => key + ':' + value + ';').join('');
  // Share defaults only with pseudos observed in the source. A majority value
  // such as content:"|" must not create new pseudos on unrelated elements.
  const commonSelectors = ['[data-atlas-style]', ...computedRules.filter(rule => rule.selector.includes('::')).map(rule => rule.selector)];
  rules.push(commonSelectors.join(',') + '{' + declarations(common) + '}');
  for (const rule of computedRules) rules.push(rule.selector + '{' + declarations(Object.fromEntries(Object.entries(rule.properties).filter(([key, value]) => value !== common[key]))) + '}');
  const stylesheet = document.createElement('style');
  stylesheet.textContent = rules.join('\n'); head.append(stylesheet);
  const meta = document.createElement('meta'); meta.setAttribute('charset', 'utf-8'); head.prepend(meta);
  if (sprites.size) {
    const sprite = document.createElementNS('http://www.w3.org/2000/svg', 'svg');
    sprite.setAttribute('style', 'display:none');
    sprite.innerHTML = [...sprites.values()].map(item => item.html).join('');
    root.querySelector('body').append(sprite);
  }
  for (const element of root.querySelectorAll('textarea,pre')) if (element.innerHTML.startsWith('\n')) element.prepend('\n');
  return {html: '<!doctype html>\n' + root.outerHTML, elements, viewport, scroll: {x: scrollX, y: scrollY}, warnings};
}
