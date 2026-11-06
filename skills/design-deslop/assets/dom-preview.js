/* Frozen DOM frames. The source application never executes in this viewer. */
(() => {
  "use strict";

  function bridge(config) {
    "use strict";
    const send = (type, detail = {}) => parent.postMessage({ channel: "design-deslop-dom", token: config.token, type, ...detail }, "*");
    // Keep structural selectors faithful to the source after the bridge starts.
    document.currentScript.remove();
    let dirty = false;
    let ready = false;
    let picker = config.picker === true;
    let focusId = config.componentId;
    let focused = null;
    let availabilityProblem = null;
    let cssBaseline = "";
    let formBaseline = "";
    let suppressScroll = false;
    function markDirty() {
      if (dirty) return;
      dirty = true;
      send("state", { status: "dirty", reason: "The inspected DOM or styles changed. Reset preview to restore the embedded document." });
    }
    const observer = new MutationObserver(records => { if (records.length) markDirty(); });
    observer.observe(document.documentElement, { subtree: true, childList: true, attributes: true, characterData: true });

    function cssState() {
      return [...document.styleSheets].map(sheet => `${sheet.disabled}|${sheet.media.mediaText}|${[...sheet.cssRules].map(rule => rule.cssText).join("\n")}`).join("\n---\n") +
        [...document.adoptedStyleSheets].map(sheet => [...sheet.cssRules].map(rule => rule.cssText).join("\n")).join("\n");
    }
    function formState() {
      return JSON.stringify([...document.querySelectorAll("input,textarea,select,details")].map(element => [element.tagName, element.value, element.checked, element.indeterminate, element.selectedIndex, element.options ? [...element.options].map(option => option.selected) : null, element.open]));
    }
    function inspect() {
      if (observer.takeRecords().length) markDirty();
      if (ready && (cssState() !== cssBaseline || formState() !== formBaseline)) markDirty();
      return dirty;
    }
    function selectorProblem() {
      if (!focusId) return "";
      const selector = config.selectors[focusId];
      if (!selector) return `No DOM selector was supplied for component ${focusId}.`;
      let matches;
      try { matches = document.querySelectorAll(selector); }
      catch (error) { return `Invalid selector for ${focusId}: ${selector}`; }
      if (matches.length !== 1) return `Selector for ${focusId} matches ${matches.length} elements: ${selector}`;
      const element = matches[0];
      const rect = element.getBoundingClientRect();
      if (!rect.width || !rect.height) return `The component ${focusId} has no visible DOM area: ${selector}`;
      if (getComputedStyle(element).visibility !== "visible") return `The component ${focusId} is hidden: ${selector}`;
      for (let current = element; current; current = current.parentElement) {
        const style = getComputedStyle(current);
        if (style.opacity === "0" || style.display === "none") return `The component ${focusId} is hidden: ${selector}`;
      }
      return "";
    }
    function status(requestId) {
      try {
        inspect();
        const problem = selectorProblem();
        if (ready && !dirty && problem !== availabilityProblem) updateFocus(problem);
        const rect = focused?.getBoundingClientRect();
        send("state", { requestId, status: dirty ? "dirty" : !ready ? "loading" : problem ? "selector-missing" : "ready", reason: problem, focusRect: rect ? { x: rect.left, y: rect.top, width: rect.width, height: rect.height } : null });
      } catch (error) { send("state", { requestId, status: "error", reason: String(error.message || error) }); }
    }
    function paint(element) {
      const rect = element?.isConnected ? element.getBoundingClientRect() : null;
      send("highlight", { rect: rect ? { x: rect.left, y: rect.top, width: rect.width, height: rect.height } : null });
    }
    function updateFocus(problem) {
      availabilityProblem = problem;
      focused = null;
      if (focusId && !problem) {
        focused = document.querySelector(config.selectors[focusId]);
        focused.scrollIntoView({ block: "start", inline: "nearest", behavior: "instant" });
      } else if (!focusId) window.scrollTo({ top: 0, left: 0, behavior: "instant" });
      paint(focused);
    }
    function focusComponent() {
      updateFocus(selectorProblem());
      status();
    }
    function uniqueSelector(element) {
      if (element.id) {
        const id = `#${CSS.escape(element.id)}`;
        if (document.querySelectorAll(id).length === 1) return id;
      }
      const parts = [];
      for (let current = element; current && current.nodeType === Node.ELEMENT_NODE; current = current.parentElement) {
        if (current.id && document.querySelectorAll(`#${CSS.escape(current.id)}`).length === 1) {
          const selector = [`#${CSS.escape(current.id)}`, ...parts].join(" > ");
          if (document.querySelectorAll(selector).length === 1) return selector;
        }
        const siblings = current.parentElement ? [...current.parentElement.children].filter(item => item.localName === current.localName) : [current];
        parts.unshift(`${CSS.escape(current.localName)}${siblings.length === 1 ? "" : `:nth-of-type(${siblings.indexOf(current) + 1})`}`);
      }
      if (document.querySelectorAll(parts.join(" > ")).length === 1) return parts.join(" > ");
      throw new Error("A unique selector could not be determined.");
    }
    document.addEventListener("click", event => {
      event.preventDefault();
      event.stopImmediatePropagation();
      if (!picker || !(event.target instanceof Element)) return;
      try {
        const element = event.target;
        const selector = uniqueSelector(element);
        const component = Object.entries(config.selectors).find(([, candidate]) => {
          try {
            const matches = document.querySelectorAll(candidate);
            return matches.length === 1 && matches[0].contains(element);
          } catch (error) { return false; }
        })?.[0] || null;
        paint(element);
        send("picked", { selector, component, text: (element.innerText || element.textContent || element.getAttribute("aria-label") || "").replace(/\s+/g, " ").trim().slice(0, 180), tag: element.localName });
      } catch (error) { send("state", { status: "error", reason: String(error.message || error) }); }
    }, true);
    for (const name of ["auxclick", "submit", "beforeinput", "dragstart", "drop"]) document.addEventListener(name, event => event.preventDefault(), true);
    document.addEventListener("keydown", event => {
      if (event.ctrlKey || event.metaKey || event.key === "Tab" || event.key === "Escape" || /^F\d+$/.test(event.key)) return;
      if (event.target.closest?.("input,textarea,select,button,a,summary,[contenteditable]")) event.preventDefault();
    }, true);
    document.addEventListener("pointermove", event => { if (picker && event.target instanceof Element) paint(event.target); }, true);
    document.addEventListener("pointerleave", () => paint(focused));
    window.addEventListener("scroll", () => {
      paint(focused);
      if (suppressScroll) return;
      const root = document.scrollingElement;
      send("scroll", { x: root.scrollLeft / Math.max(1, root.scrollWidth - innerWidth), y: root.scrollTop / Math.max(1, root.scrollHeight - innerHeight) });
    }, { passive: true });
    window.addEventListener("message", event => {
      const message = event.data;
      if (event.source !== parent || !message || message.channel !== "design-deslop-dom-control" || message.token !== config.token) return;
      if (message.type === "check") status(message.requestId);
      if (message.type === "picker") { picker = message.enabled === true; if (!picker) paint(focused); }
      if (message.type === "focus") { focusId = message.componentId || null; focusComponent(); }
      if (message.type === "scroll" && Number.isFinite(message.x) && Number.isFinite(message.y)) {
        suppressScroll = true;
        const root = document.scrollingElement;
        window.scrollTo({ left: Math.max(0, Math.min(1, message.x)) * (root.scrollWidth - innerWidth), top: Math.max(0, Math.min(1, message.y)) * (root.scrollHeight - innerHeight), behavior: "instant" });
        requestAnimationFrame(() => { suppressScroll = false; });
      }
    });
    setInterval(() => {
      if (!ready) return;
      try {
        inspect();
        if (!dirty && selectorProblem() !== availabilityProblem) focusComponent();
      } catch (error) { send("state", { status: "error", reason: String(error.message || error) }); }
    }, 250);
    (async () => {
      try {
        // Anchor freshness before loading can admit CSSOM or form-value edits.
        cssBaseline = cssState();
        formBaseline = formState();
        await Promise.all([...document.images].map(image => image.decode()));
        await document.fonts.ready;
        // The parent lays out the new frame after insertion. Measure on a painted
        // layout, not the parser's first microtask, which can still report zero.
        await new Promise(resolve => requestAnimationFrame(() => requestAnimationFrame(resolve)));
        ready = true;
        focusComponent();
      } catch (error) { send("state", { status: "error", reason: `A snapshot asset could not load: ${error.message || error}` }); }
    })();
  }

  function frameDocument(html, config) {
    if (typeof html !== "string" || !/<html[\s>]/i.test(html) || !/<body[\s>]/i.test(html)) throw new Error("A complete frozen HTML document is required.");
    const document = new DOMParser().parseFromString(html, "text/html");
    if (document.querySelector("script,base,iframe,frame,frameset,object,embed,portal")) throw new Error("Active or embedded application content is not a frozen DOM snapshot.");
    for (const meta of document.querySelectorAll("meta[http-equiv]")) {
      if (meta.httpEquiv.toLowerCase() === "refresh") throw new Error("Snapshot navigation is not allowed.");
      meta.remove();
    }
    for (const element of document.querySelectorAll("*")) {
      for (const attribute of [...element.attributes]) {
        if (/^on/i.test(attribute.name)) throw new Error("Snapshot event handlers are not allowed.");
        if (["src", "poster", "background", "xlink:href"].includes(attribute.name) && !/^(data:|#)/i.test(attribute.value)) throw new Error("Snapshot resources must be embedded.");
      }
      if (element.localName === "link") throw new Error("Snapshot styles and fonts must be embedded.");
      if (element.localName === "a" || element.localName === "area") {
        if (element.hasAttribute("href") && !element.getAttribute("href").startsWith("#")) element.setAttribute("href", "#deslop-inert-link");
        element.removeAttribute("target");
      }
      if (element.localName === "form") { element.removeAttribute("action"); element.removeAttribute("target"); }
    }
    const policy = document.createElement("meta");
    policy.httpEquiv = "Content-Security-Policy";
    policy.content = `default-src 'none'; img-src data:; font-src data:; media-src data:; style-src 'unsafe-inline'; script-src 'nonce-${config.token}'; connect-src 'none'; form-action 'none'; base-uri 'none'; object-src 'none'; frame-src 'none'`;
    document.head.prepend(policy);
    const script = document.createElement("script");
    script.setAttribute("nonce", config.token);
    script.textContent = `(${bridge.toString()})(${JSON.stringify(config).replace(/</g, "\\u003c")});`;
    document.body.append(script);
    // HTML parsing consumes the first LF in these elements. Compensate for the
    // second parse into srcdoc without changing the final source text or value.
    for (const element of document.querySelectorAll("textarea,pre,listing")) {
      if (element.innerHTML.startsWith("\n")) element.insertBefore(document.createTextNode("\n"), element.firstChild);
    }
    return "<!doctype html>\n" + document.documentElement.outerHTML;
  }

  function create({ host, side, onState, onPick, onScroll }) {
    let frame = null;
    let context = null;
    let token = "";
    let sequence = 0;
    let request = 0;
    let loadingTimer;
    let currentStatus = "missing";
    let picker = false;
    let scale = 1;
    let highlightRect = null;
    const highlightLayer = document.createElement("div");
    highlightLayer.setAttribute("aria-hidden", "true");
    highlightLayer.style.cssText = "position:absolute;inset:0;overflow:hidden;pointer-events:none;z-index:1";
    const outline = document.createElement("div");
    outline.style.cssText = "position:absolute;box-sizing:border-box;pointer-events:none;border:2px solid #2478cc;background:transparent;display:none";
    highlightLayer.append(outline);
    host.append(highlightLayer);
    const pending = new Map();
    const validRect = rect => rect && [rect.x, rect.y, rect.width, rect.height].every(Number.isFinite) && rect.width > 0 && rect.height > 0;
    function drawHighlight() {
      outline.style.display = highlightRect ? "block" : "none";
      if (!highlightRect) return;
      outline.style.left = `${highlightRect.x * scale}px`;
      outline.style.top = `${highlightRect.y * scale}px`;
      outline.style.width = `${highlightRect.width * scale}px`;
      outline.style.height = `${highlightRect.height * scale}px`;
    }
    function publish(status, reason = "", focusRect = null) {
      currentStatus = status;
      onState({ status, reason, focusRect, context });
    }
    function post(type, detail = {}) { frame?.contentWindow?.postMessage({ channel: "design-deslop-dom-control", token, type, ...detail }, "*"); }
    function settle() { for (const { resolve, timer } of pending.values()) { clearTimeout(timer); resolve(false); } pending.clear(); }
    window.addEventListener("message", event => {
      const message = event.data;
      if (!frame || event.source !== frame.contentWindow || !message || message.channel !== "design-deslop-dom" || message.token !== token) return;
      if (message.type === "state" && ["loading", "ready", "dirty", "error", "selector-missing"].includes(message.status)) {
        if (message.status !== "loading") clearTimeout(loadingTimer);
        const rect = message.focusRect;
        const focusRect = validRect(rect) ? rect : null;
        publish(message.status, typeof message.reason === "string" ? message.reason : "", focusRect);
        if (message.status === "ready") post("picker", { enabled: picker });
        const check = pending.get(message.requestId);
        if (check) { clearTimeout(check.timer); pending.delete(message.requestId); check.resolve(message.status === "ready"); }
      }
      if (message.type === "highlight") { highlightRect = validRect(message.rect) ? message.rect : null; drawHighlight(); }
      if (message.type === "picked" && typeof message.selector === "string" && typeof message.text === "string") onPick({ side, ...context, selector: message.selector, text: message.text, component: message.component, tag: message.tag });
      if (message.type === "scroll" && Number.isFinite(message.x) && Number.isFinite(message.y)) onScroll?.({ x: message.x, y: message.y });
    });
    async function check() {
      if (!frame) return currentStatus === "missing";
      const requestId = ++request;
      return new Promise(resolve => {
        const timer = setTimeout(() => { pending.delete(requestId); publish("error", "The preview did not answer its freshness check. Reset preview."); resolve(false); }, 1800);
        pending.set(requestId, { resolve, timer });
        post("check", { requestId });
      });
    }
    async function load(descriptor, nextContext, reset = false) {
      const operation = ++sequence;
      if (frame && !reset) await check();
      if (operation !== sequence) return;
      clearTimeout(loadingTimer);
      settle();
      frame?.remove();
      frame = null;
      highlightRect = null;
      drawHighlight();
      context = nextContext;
      token = "";
      if (!descriptor) { publish("missing"); return; }
      try {
        token = [...crypto.getRandomValues(new Uint8Array(18))].map(value => value.toString(16).padStart(2, "0")).join("");
        const source = frameDocument(descriptor.html, { token, selectors: descriptor.selectors || {}, componentId: nextContext.componentId, picker });
        frame = document.createElement("iframe");
        frame.id = `${side}-frame`;
        frame.title = `${side}: frozen DOM snapshot · ${nextContext.viewId} · ${nextContext.previewId}`;
        frame.setAttribute("sandbox", "allow-scripts");
        frame.setAttribute("referrerpolicy", "no-referrer");
        frame.style.width = `${nextContext.width}px`;
        frame.style.height = `${nextContext.height}px`;
        frame.srcdoc = source;
        host.append(frame);
        publish("loading");
        loadingTimer = setTimeout(() => { if (operation === sequence) publish("error", "The frozen DOM frame did not become ready. Reset preview or request a new snapshot."); }, 8000);
      } catch (error) { publish("error", String(error.message || error)); }
    }
    return {
      load, check,
      setPicker(enabled) { picker = enabled; post("picker", { enabled }); },
      setScale(nextScale, width, height) { scale = nextScale; host.style.width = `${width * scale}px`; host.style.height = `${height * scale}px`; if (frame) frame.style.transform = `scale(${scale})`; drawHighlight(); },
      scroll(position) { post("scroll", position); },
    };
  }
  window.DesignDOMPreview = Object.freeze({ create });
})();
