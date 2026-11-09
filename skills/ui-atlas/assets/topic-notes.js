// A topic is a view of original observations, never a new feedback namespace.
class AtlasTopicNotes {
  constructor(atlas, onChange, onError) {
    this.atlas = atlas;
    this.frames = new Map(atlas.frames.filter(frame => frame.origin).map(frame => [frame.id, frame.origin]));
    this.visible = new Set([...this.frames.values()].map(origin => JSON.stringify([origin.atlas, origin.frame])));
    this.stores = new Map(Object.keys(atlas.composition.observations)
      .map(id => [id, new AtlasNotes(id, onChange, onError)]));
  }
  key(owner, id) { return JSON.stringify([owner, id]); }
  included(owner, note) {
    const recorded = this.atlas.composition.observations[owner].states;
    return this.visible.has(this.key(owner, note.frame)) || !recorded.includes(note.frame);
  }
  project(owner, note) {
    return {...note, id: this.key(owner, note.id), frame: owner + '::' + note.frame,
      origin: {atlas: owner, frame: note.frame, id: note.id}};
  }
  get items() {
    return [...this.stores].flatMap(([owner, store]) => store.items
      .filter(note => this.included(owner, note)).map(note => this.project(owner, note)))
      .sort((a, b) => (a.created_at || '').localeCompare(b.created_at || '') || a.id.localeCompare(b.id));
  }
  get pending() {
    return new Map([...this.stores].flatMap(([owner, store]) => [...store.pending].map(([id, value]) => [this.key(owner, id), value])));
  }
  refresh() { return [...this.stores.values()].map(store => store.refresh()).every(Boolean); }
  change(additions = [], removals = []) {
    const changes = new Map([...this.stores.keys()].map(owner => [owner, {add: [], remove: []}]));
    for (const note of additions) {
      const origin = note.origin || this.frames.get(note.frame);
      if (!origin || !changes.has(origin.atlas)) throw new Error('의견의 원본 화면을 확인할 수 없습니다.');
      const {origin: ignored, ...raw} = note;
      changes.get(origin.atlas).add.push({...raw, id: origin.id || note.id, frame: origin.frame});
    }
    for (const id of removals) {
      const [owner, original] = JSON.parse(id);
      if (!changes.has(owner)) throw new Error('의견의 원본 전개도를 확인할 수 없습니다.');
      changes.get(owner).remove.push(original);
    }
    const results = [];
    for (const [owner, store] of this.stores) {
      const change = changes.get(owner);
      if (change.add.length || change.remove.length || store.pending.size) results.push(store.change(change.add, change.remove));
    }
    return results.every(Boolean);
  }
  export() {
    return {schema: 'ui-atlas.notes/v2', topic: this.atlas.id, sources: [...this.stores].map(([owner, store]) =>
      ({schema: 'ui-atlas.notes/v1', atlas: owner, notes: store.items.filter(note => this.included(owner, note))}))};
  }
  planImport(value) {
    const sources = value?.schema === 'ui-atlas.notes/v2' ? value.sources : [value];
    if (!Array.isArray(sources) || !sources.length) throw new Error('의견 파일 형식을 확인해 주세요.');
    const plans = [], owners = new Set(), conflicts = [], before = new Map();
    for (const source of sources) {
      const store = this.stores.get(source?.atlas);
      if (!store || owners.has(source.atlas)) throw new Error('이 주제에 속한 원본 시트의 의견 파일인지 확인해 주세요.');
      owners.add(source.atlas);
      const plan = store.planImport(source);
      plans.push({owner: source.atlas, store, plan});
      for (const note of plan.conflicts) conflicts.push(this.project(source.atlas, note));
      for (const [id, note] of plan.before) before.set(this.key(source.atlas, id), this.project(source.atlas, note));
    }
    return {plans, conflicts, before};
  }
  applyImport(bundle, choices = new Map()) {
    // Validate every original namespace before any of the planned writes.
    for (const {store, plan} of bundle.plans) store.importAdditions(plan,
      new Map([...plan.incoming.keys()].map(id => [id, choices.get(this.key(store.atlasId, id))])));
    return bundle.plans.map(({owner, store, plan}) => store.applyImport(plan,
      new Map([...plan.incoming.keys()].map(id => [id, choices.get(this.key(owner, id))])))).every(Boolean);
  }
}
