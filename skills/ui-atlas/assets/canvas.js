class AtlasCanvas {
  constructor(viewport, world, atlasId, callbacks) {
    this.viewport = viewport;
    this.world = world;
    this.callbacks = callbacks;
    this.storageKey = 'ui-atlas:layout:' + atlasId;
    this.camera = {x: 64, y: 95, zoom: .32};
    this.positions = {};
    this.tool = 'select';
    this.space = false;
    this.drag = null;
    try { this.positions = JSON.parse(localStorage.getItem(this.storageKey) || '{}'); } catch { /* Use generated layout. */ }
    if (!this.positions || typeof this.positions !== 'object') this.positions = {};
    viewport.addEventListener('pointerdown', event => this.down(event));
    viewport.addEventListener('pointermove', event => this.move(event));
    viewport.addEventListener('pointerup', event => this.up(event));
    viewport.addEventListener('pointercancel', () => this.cancel());
    viewport.addEventListener('lostpointercapture', () => this.cancel());
    viewport.addEventListener('wheel', event => {
      event.preventDefault();
      if (event.shiftKey) {
        this.camera.x -= event.deltaY; this.camera.y -= event.deltaX; this.paint();
      } else this.zoomAt(this.camera.zoom * Math.exp(-event.deltaY * .0015), event.clientX, event.clientY);
    }, {passive: false});
    window.addEventListener('blur', () => { this.space = false; this.cancel(); });
    this.paint();
  }
  setTool(tool) {
    this.tool = tool;
    this.viewport.classList.toggle('hand', tool === 'hand' || this.space);
  }
  paint() {
    const {x, y, zoom} = this.camera;
    this.world.style.transform = `translate(${x}px,${y}px) scale(${zoom})`;
    document.documentElement.style.setProperty('--zoom', zoom);
    this.callbacks.zoom?.(zoom);
  }
  zoomAt(value, clientX, clientY) {
    if (!Number.isFinite(value) || value <= 0) return;
    const box = this.viewport.getBoundingClientRect();
    const x = (clientX ?? box.x + box.width / 2) - box.x;
    const y = (clientY ?? box.y + box.height / 2) - box.y;
    const zoom = Math.max(Number.EPSILON, Math.min(4, value));
    const ratio = zoom / this.camera.zoom;
    this.camera.x = x - (x - this.camera.x) * ratio;
    this.camera.y = y - (y - this.camera.y) * ratio;
    this.camera.zoom = zoom;
    this.paint();
  }
  fit(rect, maximum = 1.2) {
    const box = this.viewport.getBoundingClientRect();
    const zoom = Math.min(maximum, Math.max(1, box.width - 100) / Math.max(1, rect.width), Math.max(1, box.height - 145) / Math.max(1, rect.height));
    this.camera = {zoom, x: box.width / 2 - (rect.x + rect.width / 2) * zoom,
      y: (box.height - 35) / 2 - (rect.y + rect.height / 2) * zoom};
    this.paint();
  }
  position(frame, fallback) {
    const saved = this.positions[frame.id];
    const valid = saved && Number.isFinite(saved.x) && Number.isFinite(saved.y);
    return valid ? saved : fallback;
  }
  down(event) {
    if (event.target.closest('.canvas-controls')) return;
    if (event.button !== 0 && event.button !== 1) return;
    if (event.button === 0 && !this.space && this.tool === 'select' && event.target.closest('[data-canvas-action]')) return;
    event.preventDefault();
    this.viewport.focus({preventScroll: true});
    const frame = event.target.closest('.artboard');
    const movingFrame = !this.space && this.tool === 'select' && event.button === 0 && event.target.closest('.frame-label');
    const section = !this.space && this.tool === 'select' && event.button === 0 && event.target.closest('.section-caption');
    this.drag = {pointer: event.pointerId, x: event.clientX, y: event.clientY, moved: false,
      camera: {...this.camera}, frame, mode: section ? 'section' : movingFrame ? 'frame' : 'pan',
      section: section?.dataset?.section, members: section ? this.callbacks.members(section.dataset.section) : [],
      frameX: frame ? Number(frame.dataset.x) : 0, frameY: frame ? Number(frame.dataset.y) : 0};
    this.viewport.setPointerCapture(event.pointerId);
  }
  move(event) {
    if (!this.drag) { this.callbacks.hover?.(event); return; }
    const drag = this.drag;
    const dx = event.clientX - drag.x, dy = event.clientY - drag.y;
    if (!drag.moved && Math.hypot(dx, dy) < 4) return;
    drag.moved = true;
    this.viewport.classList.add('panning');
    this.callbacks.clearHover?.();
    if (drag.mode === 'section') {
      for (const member of drag.members) {
        const position = {x: member.x + dx / this.camera.zoom, y: member.y + dy / this.camera.zoom};
        this.positions[member.id] = position; this.callbacks.position(member.id, position);
      }
    } else if (drag.mode === 'frame') {
      const position = {x: drag.frameX + dx / this.camera.zoom, y: drag.frameY + dy / this.camera.zoom};
      this.positions[drag.frame.dataset.frame] = position;
      this.callbacks.position(drag.frame.dataset.frame, position);
    } else {
      this.camera.x = drag.camera.x + dx;
      this.camera.y = drag.camera.y + dy;
      this.paint();
    }
  }
  up(event) {
    const drag = this.drag;
    if (!drag) return;
    if (drag.moved && ['frame', 'section'].includes(drag.mode)) {
      try { localStorage.setItem(this.storageKey, JSON.stringify(this.positions)); }
      catch { this.callbacks.error?.('화면 배치를 저장하지 못했습니다.'); }
    } else if (!drag.moved && !this.space && this.tool === 'select') {
      if (drag.section) this.callbacks.section(drag.section);
      else this.callbacks.click?.(event, drag.frame);
    }
    this.cancel();
  }
  cancel() {
    const pointer = this.drag?.pointer;
    this.drag = null;
    this.viewport.classList.remove('panning');
    if (pointer != null && this.viewport.hasPointerCapture(pointer)) this.viewport.releasePointerCapture(pointer);
  }
  reset() {
    this.positions = {};
    try { localStorage.removeItem(this.storageKey); } catch { /* In-memory layout is still reset. */ }
  }
}
