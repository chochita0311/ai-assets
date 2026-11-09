import assert from 'node:assert/strict';
import fs from 'node:fs';
import vm from 'node:vm';
import test from 'node:test';

function fixture() {
  const values = new Map(), listeners = [], blocked = new Set();
  const storage = {
    get length() { return values.size; }, key(index) { return [...values.keys()][index]; },
    getItem(key) { return values.get(key) ?? null; },
    setItem(key, value) { if (blocked.has(key)) throw new Error('quota'); values.set(key, value); },
    removeItem(key) { if (blocked.has(key)) throw new Error('quota'); values.delete(key); }
  };
  const context = vm.createContext({localStorage: storage, window: {addEventListener(type, callback) { listeners.push(callback); }}});
  for (const name of ['notes.js', 'topic-notes.js']) vm.runInContext(fs.readFileSync(new URL('../assets/' + name, import.meta.url), 'utf8'), context);
  const create = vm.runInContext('(atlas, changed, failed) => new AtlasTopicNotes(atlas, changed, failed)', context);
  const original = vm.runInContext('(id) => new AtlasNotes(id, () => {}, () => {})', context);
  const atlas = {id: 'settings', composition: {observations: {alpha: {states: ['entry', 'other']}, beta: {states: ['entry']}}},
    frames: [{id: 'alpha::entry', origin: {atlas: 'alpha', frame: 'entry'}}, {id: 'beta::entry', origin: {atlas: 'beta', frame: 'entry'}}]};
  const errors = [], changed = [];
  const note = (id, message = 'Synthetic opinion', frame = 'entry') => ({id, frame, identity: 'synthetic-identity', message,
    status: 'open', kind: 'proposal', created_at: '2026-01-01T00:00:00Z'});
  const key = (owner, id) => 'ui-atlas:notes:' + owner + ':' + id;
  const read = (owner, id) => JSON.parse(storage.getItem(key(owner, id)));
  return {values, blocked, storage, listeners, errors, atlas, note, key, read, original,
    create: () => create(atlas, () => changed.push(true), error => errors.push(error))};
}

test('same legacy IDs in different atlases remain distinct without migrating keys', () => {
  const f = fixture();
  f.storage.setItem(f.key('alpha', 'same-id'), JSON.stringify(f.note('same-id', 'Alpha')));
  f.storage.setItem(f.key('beta', 'same-id'), JSON.stringify(f.note('same-id', 'Beta')));
  const notes = f.create();
  assert.equal(notes.items.length, 2);
  assert.notEqual(notes.items[0].id, notes.items[1].id);
  notes.change([{...notes.items.find(note => note.origin.atlas === 'alpha'), status: 'reviewed'}]);
  assert.equal(f.read('alpha', 'same-id').status, 'reviewed');
  assert.equal(f.read('beta', 'same-id').status, 'open');
  assert.equal(f.read('alpha', 'same-id').frame, 'entry');
  assert.equal(f.read('alpha', 'same-id').origin, undefined);
});

test('new opinions and deletion write only to the original observation', () => {
  const f = fixture(), notes = f.create();
  notes.change([{...f.note('new'), frame: 'beta::entry'}]);
  assert.equal(f.read('beta', 'new').frame, 'entry');
  assert.equal(f.storage.getItem(f.key('alpha', 'new')), null);
  notes.change([], [notes.items[0].id]);
  assert.equal(f.storage.length, 0);
});

test('topic export retains original v1 records and is accepted by the original viewer', () => {
  const f = fixture(), notes = f.create();
  notes.change([{...f.note('new'), frame: 'beta::entry'}]);
  const file = notes.export();
  assert.equal(file.schema, 'ui-atlas.notes/v2');
  assert.equal(file.sources.find(source => source.atlas === 'beta').notes[0].id, 'new');
  const original = f.original('beta');
  original.change([], ['new']);
  assert.equal(original.applyImport(original.planImport(file)), true);
  assert.equal(f.read('beta', 'new').frame, 'entry');
});

test('legacy import merges opinions into a topic without touching another owner', () => {
  const f = fixture(), notes = f.create();
  const plan = notes.planImport({schema: 'ui-atlas.notes/v1', atlas: 'alpha', notes: [f.note('legacy')]});
  assert.equal(notes.applyImport(plan), true);
  assert.equal(notes.items[0].frame, 'alpha::entry');
  assert.equal(f.storage.getItem(f.key('beta', 'legacy')), null);
});

test('missing old frames stay visible, while another topic’s known frames stay scoped', () => {
  const f = fixture();
  f.storage.setItem(f.key('alpha', 'orphan'), JSON.stringify(f.note('orphan', 'Missing frame', 'retired')));
  f.storage.setItem(f.key('alpha', 'outside'), JSON.stringify(f.note('outside', 'Other topic', 'other')));
  const notes = f.create();
  assert.equal(notes.items.length, 1);
  assert.equal(notes.items[0].origin.frame, 'retired');
  assert.equal(notes.export().sources[0].notes[0].id, 'orphan');
  assert.equal(f.read('alpha', 'outside').frame, 'other');
});

test('failed writes survive refresh and retry, including independent source owners', () => {
  const f = fixture(), notes = f.create();
  f.blocked.add(f.key('alpha', 'pending'));
  assert.equal(notes.change([{...f.note('pending'), frame: 'alpha::entry'}, {...f.note('saved'), frame: 'beta::entry'}]), false);
  assert.equal(notes.pending.size, 1);
  notes.refresh();
  assert.equal(notes.items.length, 2);
  f.blocked.clear();
  assert.equal(notes.change(), true);
  assert.equal(notes.pending.size, 0);
  assert.equal(f.read('alpha', 'pending').message, 'Synthetic opinion');
  assert.equal(f.read('beta', 'saved').message, 'Synthetic opinion');
});

test('conflicting imports retain explicit local/file choices', () => {
  const f = fixture();
  f.storage.setItem(f.key('alpha', 'same'), JSON.stringify(f.note('same', 'Local')));
  const notes = f.create();
  let plan = notes.planImport({schema: 'ui-atlas.notes/v1', atlas: 'alpha', notes: [f.note('same', 'File')]});
  assert.equal(plan.conflicts.length, 1);
  notes.applyImport(plan, new Map([[plan.conflicts[0].id, 'local']]));
  assert.equal(f.read('alpha', 'same').message, 'Local');
  plan = notes.planImport({schema: 'ui-atlas.notes/v1', atlas: 'alpha', notes: [f.note('same', 'File')]});
  notes.applyImport(plan, new Map([[plan.conflicts[0].id, 'file']]));
  assert.equal(f.read('alpha', 'same').message, 'File');
});

test('concurrent import changes are detected across all owners before the first write', () => {
  const f = fixture(), notes = f.create();
  const plan = notes.planImport({schema: 'ui-atlas.notes/v2', sources: [
    {schema: 'ui-atlas.notes/v1', atlas: 'alpha', notes: [f.note('new')]},
    {schema: 'ui-atlas.notes/v1', atlas: 'beta', notes: [f.note('raced')]}
  ]});
  f.storage.setItem(f.key('beta', 'raced'), JSON.stringify(f.note('raced', 'Other tab')));
  assert.throws(() => notes.applyImport(plan), /바뀌었습니다/);
  assert.equal(f.storage.getItem(f.key('alpha', 'new')), null);
  assert.equal(f.read('beta', 'raced').message, 'Other tab');
});

test('a malformed bundle or duplicate owner is refused without changing storage', () => {
  const f = fixture(), notes = f.create();
  assert.throws(() => notes.planImport({schema: 'ui-atlas.notes/v2', sources: null}));
  const source = {schema: 'ui-atlas.notes/v1', atlas: 'alpha', notes: [f.note('new')]};
  assert.throws(() => notes.planImport({schema: 'ui-atlas.notes/v2', sources: [source, source]}));
  assert.equal(f.storage.length, 0);
});
