(() => {
  'use strict';
  const data = JSON.parse(document.querySelector('#workspace-data').textContent);
  const channel = 'ui-atlas-workspace/v1';
  const groups = data.groups;
  const runs = new Map(groups.flatMap(group => group.runs.map(run => [run.key, {...run, atlasId: group.id}])));
  const mounted = new Map();
  const storageKey = 'ui-atlas:workspace:last:' + location.pathname;
  const fallback = document.querySelector('#workspace-fallback');
  const loading = document.querySelector('#workspace-loading');
  let selected = null, serial = 0;

  function initialRun() {
    const query = new URLSearchParams(location.hash.slice(1));
    if (runs.has(query.get('run'))) return runs.get(query.get('run'));
    const group = groups.find(item => item.id === query.get('atlas'));
    if (group) return runs.get(group.runs[0].key);
    try {
      const saved = JSON.parse(localStorage.getItem(storageKey));
      if (saved?.run && runs.has(saved.run)) return runs.get(saved.run);
      const previous = groups.find(item => item.id === saved?.atlas);
      if (previous) return runs.get(previous.runs[0].key);
    } catch { /* The first available sheet also works without browser storage. */ }
    return groups.length ? runs.get(groups[0].runs[0].key) : null;
  }
  function remember(run, historyMode) {
    const latest = groups.find(group => group.id === run.atlasId).runs[0].key === run.key;
    try { localStorage.setItem(storageKey, JSON.stringify({atlas: run.atlasId, run: latest ? null : run.key})); }
    catch { /* Preference storage must not prevent opening a sheet. */ }
    if (historyMode !== 'none') {
      const hash = new URLSearchParams(latest ? {atlas: run.atlasId} : {run: run.key});
      history[historyMode === 'push' ? 'pushState' : 'replaceState'](null, '', '#' + hash);
    }
  }
  function prune() {
    // A dirty or not-yet-connected sheet owns state we cannot safely discard.
    const clean = [...mounted.values()].filter(entry => entry.key !== selected && entry.dirty === false)
      .sort((a, b) => a.used - b.used);
    while (clean.length > 2) {
      const entry = clean.shift();
      clearTimeout(entry.timeout); entry.frame.remove(); mounted.delete(entry.key);
    }
  }
  function connect(entry) {
    entry.frame.contentWindow.postMessage({channel, type: 'connect', token: entry.token,
      current: entry.key, groups, unfinished: data.unfinished, unreadable: data.unreadable}, '*');
  }
  function open(run, historyMode = 'push') {
    if (!run) return;
    fallback.hidden = true;
    let entry = mounted.get(run.key);
    if (!entry) {
      const frame = document.createElement('iframe');
      frame.className = 'atlas-host'; frame.title = run.title; frame.dataset.run = run.key;
      entry = {key: run.key, atlasId: run.atlasId, frame, token: crypto.randomUUID(), dirty: null, ready: false};
      mounted.set(run.key, entry);
      frame.addEventListener('load', () => {
        clearTimeout(entry.timeout);
        connect(entry);
        entry.timeout = setTimeout(() => {
          if (!entry.ready && selected === entry.key) {
            fallback.hidden = false; loading.hidden = true;
            const message = document.querySelector('#workspace-error');
            message.textContent = '이 실행의 뷰어를 연결하지 못했습니다. 이전 뷰어는 다시 빌드하거나 아래 독립 시트로 열어 주세요.';
            message.hidden = false;
          }
        }, 3000);
      });
      document.body.prepend(frame);
      // A warm file can parse before layout and otherwise initialize at 300px.
      frame.getBoundingClientRect();
      frame.src = run.url;
    }
    selected = run.key; entry.used = ++serial;
    for (const item of mounted.values()) {
      const active = item.key === selected;
      item.frame.classList.toggle('active', active);
      item.frame.setAttribute('aria-hidden', String(!active)); item.frame.inert = !active;
    }
    loading.hidden = entry.ready;
    document.title = run.title + ' · UI Atlas';
    remember(run, historyMode); prune();
  }
  window.addEventListener('message', event => {
    const message = event.data;
    if (message?.channel !== channel) return;
    const entry = [...mounted.values()].find(item => item.frame.contentWindow === event.source);
    if (!entry || message.atlasId !== entry.atlasId) return;
    if (message.type === 'ready') { connect(entry); return; }
    if (message.token !== entry.token || typeof message.dirty !== 'boolean') return;
    entry.dirty = message.dirty; entry.ready = true; clearTimeout(entry.timeout);
    if (entry.key === selected) loading.hidden = true;
    if (message.type === 'select' && runs.has(message.key)) open(runs.get(message.key));
    prune();
  });
  window.addEventListener('beforeunload', event => {
    if ([...mounted.values()].some(entry => entry.dirty === true)) { event.preventDefault(); event.returnValue = ''; }
  });
  const restore = () => open(initialRun(), 'none');
  window.addEventListener('popstate', restore);
  window.addEventListener('hashchange', restore);
  open(initialRun(), 'replace');
})();
