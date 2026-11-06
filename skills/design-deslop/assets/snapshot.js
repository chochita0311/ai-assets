async () => {
  "use strict";
  // Evaluate this function in an already rendered page. It returns inert,
  // self-contained source HTML; it does not capture a screenshot or run an app.
  const fail = message => { throw new Error(`DOM snapshot: ${message}`); };
  const unsupported = "canvas,video,audio,iframe,frame,frameset,object,embed,portal,marquee,animate,animateMotion,animateTransform,set";
  if (!document.documentElement || !document.head || !document.body) fail("a complete HTML document is required");
  const doctype = document.doctype;
  if (document.compatMode !== "CSS1Compat" || !doctype || doctype.name.toLowerCase() !== "html" || doctype.publicId ||
      (doctype.systemId && doctype.systemId !== "about:legacy-compat")) {
    fail("an HTML5 standards-mode source document is required; quirks and legacy-doctype modes are not supported");
  }
  if (document.fullscreenElement || document.querySelector(":popover-open, :modal")) {
    fail("open top-layer popover, modal dialog, and fullscreen states cannot be serialized faithfully");
  }
  if (document.adoptedStyleSheets.length) fail("adopted stylesheets are not supported");
  if (document.querySelector(unsupported)) fail("canvas, media, embedded documents, and SVG animation are not supported");
  if (document.getAnimations().length) {
    fail("active, paused, or fill-mode animations/transitions must be made static before capture");
  }
  await document.fonts.ready;
  const originals = [document.documentElement, ...document.documentElement.querySelectorAll("*")];
  for (const element of originals) {
    if (element.shadowRoot || element.localName.includes("-") || element.hasAttribute("is")) {
      fail(`shadow DOM/custom elements are not supported (${element.localName})`);
    }
    if (element.hasAttribute("xml:base") || element.hasAttribute("manifest")) fail("XML base/application manifest attributes are not supported");
    if (element instanceof HTMLInputElement && (element.indeterminate || (element.type === "file" && element.files.length))) {
      fail("indeterminate checkboxes and populated file inputs cannot be serialized");
    }
    if (element instanceof HTMLSelectElement && !element.multiple && element.options.length && element.selectedIndex < 0) {
      fail("a single-select with no selected option cannot be serialized faithfully");
    }
  }
  const clone = document.documentElement.cloneNode(true);
  const copies = [clone, ...clone.querySelectorAll("*")];
  const copyFor = new Map(originals.map((element, index) => [element, copies[index]]));
  const cache = new Map();
  const declaredFonts = new Map();
  const imageTypes = new Set(["image/png", "image/jpeg", "image/webp", "image/svg+xml"]);
  const fontTypes = new Set(["font/woff", "font/woff2", "font/ttf", "font/otf", "application/font-woff",
    "application/x-font-woff", "application/x-font-ttf", "application/x-font-opentype"]);
  const cssUnescape = value => value.replace(/\\(?:\r\n|[\r\n\f])/g, "")
    .replace(/\\([0-9a-f]{1,6})(?:\r\n|[ \t\r\n\f])?|\\([^\r\n\f])/gi, (_, hex, literal) => {
      const number = hex ? parseInt(hex, 16) : 0;
      return hex ? String.fromCodePoint(number > 0 && number <= 0x10ffff ? number : 0xfffd) : literal;
    });
  const urlPattern = () => /\burl\s*\(\s*(?:"((?:\\.|[^"\\])*)"|'((?:\\.|[^'\\])*)'|((?:\\.|[^)\\])*?))\s*\)/gi;
  const assertCSS = css => {
    const tokens = cssUnescape(css.replace(/\/\*[\s\S]*?\*\//g, ""));
    if (/@import\b|\b(?:image-set|-webkit-image-set|paint|element|-webkit-canvas|local|expression)\s*\(/i.test(tokens)) {
      fail("CSS imports left unresolved, dynamic/image-set assets, or local() font sources are not supported");
    }
  };
  const dataURI = blob => new Promise((resolve, reject) => {
    const reader = new FileReader();
    reader.onload = () => resolve(reader.result);
    reader.onerror = () => reject(new Error("DOM snapshot: asset bytes could not be encoded"));
    reader.readAsDataURL(blob);
  });

  const validateSVG = async (blob, address) => {
    const raw = await blob.text();
    const svg = new DOMParser().parseFromString(raw, "image/svg+xml");
    if (svg.querySelector("parsererror") || svg.documentElement.localName !== "svg" || svg.doctype) {
      fail(`malformed or declaration-bearing SVG asset (${address})`);
    }
    for (const element of [svg.documentElement, ...svg.querySelectorAll("*")]) {
      if (/^(script|foreignObject|iframe|object|embed|animate|animateMotion|animateTransform|set)$/i.test(element.localName)) {
        fail(`active or unsupported SVG image content (${address})`);
      }
      for (const attribute of element.attributes) {
        if (/^on/i.test(attribute.name) || attribute.name === "xml:base") fail(`active attribute in SVG image (${address})`);
        if (["href", "xlink:href", "src"].includes(attribute.name) && !attribute.value.startsWith("#")) {
          fail(`SVG image with nested resource is not supported (${address})`);
        }
      }
      const css = element.localName === "style" ? element.textContent : element.getAttribute("style") || "";
      assertCSS(css);
      for (const match of cssUnescape(css).matchAll(urlPattern())) {
        if (!cssUnescape(match[1] ?? match[2] ?? match[3]).trim().startsWith("#")) {
          fail(`SVG image with CSS resource is not supported (${address})`);
        }
      }
      for (const attribute of element.attributes) {
        if (/\burl\s*\(/i.test(cssUnescape(attribute.value))) {
          for (const match of cssUnescape(attribute.value).matchAll(urlPattern())) {
            if (!cssUnescape(match[1] ?? match[2] ?? match[3]).trim().startsWith("#")) {
              fail(`SVG image with resource-bearing attribute is not supported (${address})`);
            }
          }
        }
      }
    }
    // XML serialization removes prologs while retaining the actual image DOM.
    return new Blob([new XMLSerializer().serializeToString(svg.documentElement)], {type: "image/svg+xml"});
  };

  const embed = async (reference, base, kind = "either") => {
    reference = reference.trim();
    if (reference.startsWith("#") && reference.length > 1) return reference;
    let address;
    try { address = new URL(reference, base).href; }
    catch (_) { fail(`invalid asset address (${reference})`); }
    if (!/^(https?:|data:|blob:|file:)/i.test(address)) fail(`unsupported asset URL scheme (${address})`);
    const key = `${kind}:${address}`;
    if (!cache.has(key)) {
      cache.set(key, (async () => {
        let response;
        try { response = await fetch(address, {credentials: "same-origin", cache: "force-cache"}); }
        catch (_) { fail(`asset is unreadable; use readable same-origin/CORS assets (${address})`); }
        if (!response.ok) fail(`asset read failed with HTTP ${response.status} (${address})`);
        let blob = await response.blob();
        let mime = blob.type.split(";", 1)[0].toLowerCase();
        if (!mime || mime === "application/octet-stream") {
          const extension = new URL(address).pathname.split(".").pop().toLowerCase();
          mime = {png: "image/png", jpg: "image/jpeg", jpeg: "image/jpeg", webp: "image/webp", svg: "image/svg+xml",
            woff: "font/woff", woff2: "font/woff2", ttf: "font/ttf", otf: "font/otf"}[extension] || mime;
          blob = new Blob([blob], {type: mime});
        }
        if (!blob.size || !(kind === "image" ? imageTypes.has(mime) : imageTypes.has(mime) || fontTypes.has(mime))) {
          fail(`unsupported or empty asset type ${mime || "unknown"} (${address})`);
        }
        if (mime === "image/png" || mime === "image/webp") {
          const bytes = new Uint8Array(await blob.arrayBuffer());
          const view = new DataView(bytes.buffer);
          let offset = mime === "image/png" ? 8 : 12;
          while (offset + 8 <= bytes.length) {
            const png = mime === "image/png";
            const typeAt = offset + (png ? 4 : 0);
            const type = String.fromCharCode(...bytes.subarray(typeAt, typeAt + 4));
            if (type === (png ? "acTL" : "ANIM")) fail(`animated image assets are not supported (${address})`);
            const length = view.getUint32(offset + (png ? 0 : 4), !png);
            offset += length + (png ? 12 : 8 + (length % 2));
          }
        }
        if (mime === "image/svg+xml") blob = await validateSVG(blob, address);
        return dataURI(blob);
      })());
    }
    return cache.get(key);
  };

  const rewriteCSS = async (css, base) => {
    assertCSS(css);
    const matches = [...css.matchAll(urlPattern())];
    if (matches.length !== (cssUnescape(css).match(/\burl\s*\(/gi) || []).length) fail("unparseable or escaped CSS asset URL");
    let result = "", offset = 0;
    for (const match of matches) {
      const reference = cssUnescape(match[1] ?? match[2] ?? match[3]).trim();
      const embedded = await embed(reference, base);
      result += css.slice(offset, match.index) + `url("${embedded.replace(/"/g, "%22")}")`;
      offset = match.index + match[0].length;
    }
    return result + css.slice(offset);
  };

  const stylesheetText = async (sheet, ancestors = new Set()) => {
    if (ancestors.has(sheet)) fail("cyclic CSS imports are not supported");
    const next = new Set(ancestors).add(sheet);
    let rules;
    try { rules = [...sheet.cssRules]; }
    catch (_) { fail(`stylesheet is unreadable; use readable same-origin/CORS CSS (${sheet.href || "inline"})`); }
    const base = sheet.href || document.baseURI;
    const result = [];
    for (const rule of rules) {
      if (rule.type === CSSRule.IMPORT_RULE) {
        if (!rule.styleSheet) fail(`imported stylesheet is unavailable (${rule.href})`);
        if (/\blayer(?:\s|\(|;)|\bsupports\s*\(/i.test(rule.cssText)) {
          fail("@import layer/supports qualifiers are not supported");
        }
        const imported = await stylesheetText(rule.styleSheet, next);
        result.push(rule.media.mediaText ? `@media ${rule.media.mediaText} {\n${imported}\n}` : imported);
      } else {
        const registerFonts = item => {
          if (item.type === CSSRule.FONT_FACE_RULE) {
            const family = cssUnescape(item.style.getPropertyValue("font-family")).trim().replace(/^(['"])(.*)\1$/, (_match, _quote, family) => family).toLowerCase();
            declaredFonts.set(family, (declaredFonts.get(family) || 0) + 1);
          }
          if (item.cssRules) for (const child of item.cssRules) registerFonts(child);
        };
        registerFonts(rule);
        result.push(await rewriteCSS(rule.cssText, base));
      }
    }
    return result.join("\n");
  };

  for (const sheet of document.styleSheets) {
    const owner = sheet.ownerNode;
    if (!owner || !copyFor.has(owner)) fail("stylesheet ownership cannot be serialized");
    const originalCopy = copyFor.get(owner);
    if (sheet.disabled) { originalCopy.remove(); continue; }
    const replacement = document.createElement("style");
    for (const name of ["id", "class", "media"]) {
      if (owner.hasAttribute(name)) replacement.setAttribute(name, owner.getAttribute(name));
    }
    replacement.textContent = await stylesheetText(sheet);
    originalCopy.replaceWith(replacement);
  }
  const loadedFonts = new Map();
  for (const face of document.fonts) {
    const family = cssUnescape(face.family).trim().replace(/^(['"])(.*)\1$/, (_match, _quote, family) => family).toLowerCase();
    loadedFonts.set(family, (loadedFonts.get(family) || 0) + 1);
    if (loadedFonts.get(family) > (declaredFonts.get(family) || 0)) {
      fail(`font created outside stylesheet @font-face rules cannot be serialized (${face.family})`);
    }
  }

  for (const original of originals) {
    const copy = copyFor.get(original);
    if (!clone.contains(copy) && copy !== clone) continue;
    if (original.matches("script,base,link,meta[http-equiv],template,noscript,source")) { copy.remove(); continue; }
    if (original.hasAttribute("style")) copy.setAttribute("style", await rewriteCSS(original.style.cssText, original.baseURI));
    for (const attribute of [...copy.attributes]) {
      if (/^on/i.test(attribute.name) || ["autofocus", "action", "formaction", "ping", "srcset", "sizes", "imagesrcset"].includes(attribute.name)) {
        copy.removeAttribute(attribute.name);
      }
    }
    if (original.matches("a,area")) {
      // Keep native link styling/focus semantics, but discard the navigation
      // destination. The viewer prevents even this in-document activation.
      if (copy.hasAttribute("href") || copy.hasAttribute("xlink:href")) copy.setAttribute("href", "#deslop-inert-link");
      copy.removeAttribute("xlink:href");
      copy.removeAttribute("target");
      copy.removeAttribute("download");
    }
    if (original instanceof HTMLImageElement) {
      if (!original.complete || !original.naturalWidth) fail(`image is not fully rendered (${original.currentSrc || original.src || "empty src"})`);
      const embedded = await embed(original.currentSrc || original.src, original.baseURI, "image");
      const decoded = new Image();
      decoded.src = embedded;
      try { await decoded.decode(); }
      catch (_) { fail("embedded image could not be decoded"); }
      if (decoded.naturalWidth !== original.naturalWidth || decoded.naturalHeight !== original.naturalHeight) {
        fail("selected image has responsive intrinsic density that cannot be preserved without its source selection rules");
      }
      copy.setAttribute("src", embedded);
      copy.removeAttribute("loading");
    } else {
      for (const attribute of ["src", "href", "xlink:href", "background"]) {
        if (!copy.hasAttribute(attribute)) continue;
        const value = copy.getAttribute(attribute);
        copy.setAttribute(attribute, await embed(value, original.baseURI, "image"));
      }
    }
    // SVG presentation attributes can contain resource URLs without a style attribute.
    if (original.namespaceURI === "http://www.w3.org/2000/svg") {
      for (const attribute of [...copy.attributes]) {
        if (/\burl\s*\(/i.test(cssUnescape(attribute.value))) copy.setAttribute(attribute.name, await rewriteCSS(attribute.value, original.baseURI));
      }
    }
    if (original instanceof HTMLInputElement) {
      copy.setAttribute("value", original.value);
      copy.toggleAttribute("checked", original.checked);
    } else if (original instanceof HTMLTextAreaElement) {
      copy.textContent = original.value;
    } else if (original instanceof HTMLOptionElement) {
      copy.toggleAttribute("selected", original.selected);
    } else if (original instanceof HTMLDetailsElement) {
      copy.toggleAttribute("open", original.open);
    }
  }
  // HTML parsing consumes one LF immediately after these start tags. Add the
  // consumed LF to the serialization, not to the source page's actual state.
  for (const element of clone.querySelectorAll("textarea,pre,listing")) {
    if (element.innerHTML.startsWith("\n")) element.prepend("\n");
  }
  return "<!DOCTYPE html>\n" + clone.outerHTML;
}
