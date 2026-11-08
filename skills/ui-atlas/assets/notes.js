class AtlasNotes {
  constructor(atlasId, onChange, onError) {
    this.atlasId = atlasId;
    this.prefix = 'ui-atlas:notes:' + atlasId + ':';
    this.onChange = onChange;
    this.onError = onError;
    this.items = [];
    this.pending = new Map(); // Unsaved local writes; null means a pending deletion.
    this.refresh();
    window.addEventListener('storage', event => {
      if (event.key !== null && !event.key.startsWith(this.prefix)) return;
      this.refresh(); this.onChange();
    });
  }
  valid(note) {
    return note && typeof note === 'object' &&
      ['id', 'frame', 'identity', 'message'].every(key => typeof note[key] === 'string') &&
      ['quote', 'selector', 'source', 'region', 'created_at', 'node'].every(key => note[key] == null || typeof note[key] === 'string') &&
      (note.status == null || ['open', 'reviewed'].includes(note.status)) &&
      (note.clipped == null || typeof note.clipped === 'boolean') &&
      (note.kind == null || ['proposal', 'observation'].includes(note.kind));
  }
  read() {
    const notes = [];
    for (let index = 0; index < localStorage.length; index++) {
      const key = localStorage.key(index);
      if (!key?.startsWith(this.prefix)) continue;
      const value = localStorage.getItem(key);
      try {
        const note = JSON.parse(value);
        if (this.valid(note)) notes.push(note);
      } catch { /* A malformed entry must not hide other feedback. */ }
    }
    return notes.sort((a, b) => (a.created_at || '').localeCompare(b.created_at || '') || a.id.localeCompare(b.id));
  }
  overlay(items) {
    const merged = new Map(items.map(note => [note.id, note]));
    for (const [id, note] of this.pending) {
      if (note === null) merged.delete(id); else merged.set(id, note);
    }
    return [...merged.values()].sort((a, b) => (a.created_at || '').localeCompare(b.created_at || '') || a.id.localeCompare(b.id));
  }
  refresh() {
    try { this.items = this.overlay(this.read()); return true; }
    catch { return false; } // Keep the visible in-memory copy available for export.
  }
  change(additions = [], removals = []) {
    for (const id of removals) this.pending.set(id, null);
    for (const note of additions) this.pending.set(note.id, note);
    this.items = this.overlay(this.items);
    // Deletions can free quota for previously failed additions. A successful
    // write clears only its own pending entry, never another unsaved opinion.
    const writes = [...this.pending].sort((a, b) => Number(a[1] !== null) - Number(b[1] !== null));
    for (const [id, note] of writes) {
      try {
        if (note === null) localStorage.removeItem(this.prefix + id);
        else localStorage.setItem(this.prefix + id, JSON.stringify(note));
        this.pending.delete(id);
      } catch { /* Retain this operation across reads and other-tab updates. */ }
    }
    const readable = this.refresh(), saved = readable && this.pending.size === 0;
    if (!saved) this.onError([...this.pending.values()].includes(null)
      ? '삭제를 저장하지 못했습니다. 이 창을 유지하고 파일 메뉴에서 저장을 다시 시도해 주세요. 의견 파일은 삭제 작업을 복구하지 않습니다.'
      : '브라우저 저장을 사용할 수 없습니다. 의견 파일을 저장해 주세요.');
    this.onChange();
    return saved;
  }
  same(left, right) {
    const canonical = value => value == null ? null : Object.entries({...value, kind: value.kind ?? 'proposal', status: value.status ?? 'open', clipped: value.clipped ?? false})
      .sort(([a], [b]) => a.localeCompare(b));
    return JSON.stringify(canonical(left)) === JSON.stringify(canonical(right));
  }
  planImport(value) {
    if (!value || value.schema !== 'ui-atlas.notes/v1' || value.atlas !== this.atlasId || !Array.isArray(value.notes) || !value.notes.every(note => this.valid(note))) {
      throw new Error('이 전개도의 의견 파일인지 확인해 주세요.');
    }
    const incoming = new Map();
    for (const note of value.notes) {
      if (incoming.has(note.id) && !this.same(incoming.get(note.id), note)) throw new Error('파일 안에 같은 ID의 서로 다른 의견이 있습니다. 파일을 확인해 주세요.');
      incoming.set(note.id, JSON.parse(JSON.stringify(note)));
    }
    this.requireSettledImport(incoming);
    if (!this.refresh()) throw new Error('현재 저장된 의견을 읽을 수 없습니다. 저장소가 복구된 뒤 다시 가져와 주세요.');
    const before = new Map(this.items.map(note => [note.id, note]));
    const conflicts = [...incoming.values()].filter(note => before.has(note.id) && !this.same(before.get(note.id), note));
    return {incoming, before, conflicts};
  }
  applyImport(plan, choices = new Map()) {
    this.requireSettledImport(plan.incoming);
    if (!this.refresh()) throw new Error('현재 저장된 의견을 읽을 수 없습니다. 저장소가 복구된 뒤 다시 가져와 주세요.');
    const current = new Map(this.items.map(note => [note.id, note]));
    const additions = [];
    for (const [id, note] of plan.incoming) {
      const previous = plan.before.get(id), latest = current.get(id);
      if (!this.same(previous, latest)) throw new Error('가져오기를 검토하는 동안 의견이 바뀌었습니다. 파일을 다시 열어 확인해 주세요.');
      if (this.same(latest, note)) continue;
      if (previous) {
        const choice = choices.get(id);
        if (!['local', 'file'].includes(choice)) throw new Error('서로 다른 의견 중 사용할 내용을 선택해 주세요.');
        if (choice === 'local') continue;
      }
      additions.push(note);
    }
    return this.change(additions);
  }
  requireSettledImport(incoming) {
    if ([...incoming.keys()].some(id => this.pending.has(id))) throw new Error('가져올 의견에 저장 대기 중인 변경이 있습니다. 먼저 파일 메뉴에서 저장을 다시 시도하거나, 의견 파일을 보관하고 새 창에서 가져와 주세요.');
  }
  export() { return {schema: 'ui-atlas.notes/v1', atlas: this.atlasId, notes: this.items}; }
}
