class AtlasSections {
  constructor(world, catalog, positions, onSelect) {
    this.world = world;
    this.catalog = catalog;
    this.positions = positions;
    this.onSelect = onSelect;
    this.entries = new Map();
    this.showDescriptions = true;
  }
  build() {
    this.entries.clear();
    for (const section of this.catalog.sections.values()) {
      const boundary = document.createElement('div'); boundary.className = 'section-boundary';
      const title = document.createElement('div'); title.className = 'section-caption';
      title.dataset.section = section.id; title.tabIndex = 0; title.setAttribute('role', 'button');
      title.textContent = section.frames[0].feature ? section.label : section.surface + ' / ' + section.label;
      title.title = section.surface + ' / ' + section.label;
      title.onkeydown = event => {
        if (event.key === 'Enter' || event.code === 'Space') { event.preventDefault(); event.stopPropagation(); this.onSelect(section); }
      };
      const card = document.createElement('button'); card.className = 'section-description';
      card.dataset.canvasAction = 'description'; card.title = '설명과 단계 보기';
      card.onclick = () => this.onSelect(section);
      const label = document.createElement('strong'); label.textContent = section.label; card.append(label);
      const evidence = document.createElement('small');
      evidence.textContent = section.frames.every(frame => frame.evidence === 'synthetic') ? '합성 조건으로 관찰' : '기록된 화면 관찰'; card.append(evidence);
      for (const [name, value] of this.catalog.description(section).slice(1, 4)) {
        const heading = document.createElement('span'); heading.textContent = name;
        const text = document.createElement('p'); text.textContent = value;
        card.append(heading, text);
      }
      this.world.append(boundary, card, title);
      this.entries.set(section.id, {section, boundary, title, card});
    }
    this.update();
  }
  bounds(section, description = this.showDescriptions) {
    const rects = section.frames.map(frame => ({...this.positions.get(frame.id), ...frame.viewport}));
    const left = Math.min(...rects.map(rect => rect.x)), top = Math.min(...rects.map(rect => rect.y));
    const x = left - (description ? 480 : 48), y = top - 120;
    return {x, y, width: Math.max(...rects.map(rect => rect.x + rect.width)) - x + 48,
      height: Math.max(top + (description ? 680 : 0), ...rects.map(rect => rect.y + rect.height)) - y + 48};
  }
  update() {
    for (const entry of this.entries.values()) {
      const bounds = this.bounds(entry.section);
      Object.assign(entry.boundary.style, {left: bounds.x + 'px', top: bounds.y + 'px', width: bounds.width + 'px', height: bounds.height + 'px'});
      Object.assign(entry.title.style, {left: bounds.x + 'px', top: bounds.y + 'px', maxWidth: bounds.width + 'px'});
      Object.assign(entry.card.style, {left: (bounds.x + 24) + 'px', top: (bounds.y + 120) + 'px'});
      entry.card.hidden = !this.showDescriptions;
    }
  }
  labels(zoom, selectedFrame) {
    // Very small overviews have less vertical gap than constant-size captions.
    // Use the empty left gutter so feature names survive without covering frames.
    const worldBox = this.world.getBoundingClientRect();
    const viewport = this.world.parentElement.getBoundingClientRect();
    if (zoom < .12) for (const entry of this.entries.values()) {
      const bounds = this.bounds(entry.section);
      const gutter = worldBox.left + bounds.x * zoom - viewport.left - 24;
      if (gutter > 48) {
        const width = Math.min(180, gutter);
        entry.title.style.left = (bounds.x - (width + 12) / zoom) + 'px';
        entry.title.style.maxWidth = (width / zoom) + 'px';
      }
    }
    const allLabels = [...this.world.querySelectorAll('.frame-label, .section-caption')];
    const candidates = [];
    for (const label of allLabels) {
      const frame = label.closest('.artboard');
      const selected = frame?.dataset.frame === selectedFrame?.id;
      label.style.visibility = '';
      label.classList.toggle('selected-label', selected);
      const eligible = !frame || selected || zoom >= .28;
      if (!eligible) { label.style.visibility = 'hidden'; continue; }
      candidates.push({label, selected, rank: selected ? 0 : frame ? 2 : 1, rect: label.getBoundingClientRect()});
    }
    const accepted = [];
    const overlaps = (a, b) => a.left < b.right + 3 && a.right + 3 > b.left && a.top < b.bottom + 3 && a.bottom + 3 > b.top;
    const frames = [...this.world.querySelectorAll('.artboard')].map(frame => frame.getBoundingClientRect());
    for (const item of candidates.sort((a, b) => a.rank - b.rank)) {
      if (accepted.some(rect => overlaps(item.rect, rect)) || frames.some(rect => overlaps(item.rect, rect))) item.label.style.visibility = 'hidden';
      else accepted.push(item.rect);
    }
  }
}
