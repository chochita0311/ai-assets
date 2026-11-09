class AtlasSheetPicker {
  constructor(atlasId, hasUnsavedWork) {
    this.atlasId = atlasId;
    this.hasUnsavedWork = hasUnsavedWork;
    this.channel = 'ui-atlas-workspace/v1';
    this.context = null;
    this.token = null;
    this.lastDirty = null;
    if (window.parent === window) return;
    this.picker = document.querySelector('#sheet-picker');
    this.select = document.querySelector('#sheet-select');
    this.dialog = document.querySelector('#workspace-catalog');
    this.search = document.querySelector('#workspace-search');
    this.edition = document.querySelector('#edition-select');
    const openMap = () => { this.search.value = ''; this.renderCatalog(); this.dialog.showModal(); };
    document.querySelector('#workspace-map').onclick = openMap;
    this.edition.onchange = () => this.choose(this.context.topics.find(topic => topic.group === this.edition.value).key);
    this.select.addEventListener('change', () => {
      const key = this.select.value;
      this.select.value = this.context.current;
      if (key === '@catalog') openMap();
      else this.choose(key);
    });
    this.search.addEventListener('input', () => this.renderCatalog());
    document.querySelector('#close-workspace-catalog').onclick = () => this.dialog.close();
    for (const name of ['input', 'change', 'submit']) document.addEventListener(name, () => queueMicrotask(() => this.changed()));
    window.addEventListener('message', event => {
      const message = event.data;
      if (event.source !== window.parent || message?.channel !== this.channel || message.type !== 'connect') return;
      if (this.token && message.token !== this.token) return;
      if (!Array.isArray(message.groups) || typeof message.token !== 'string') return;
      const current = [...message.groups.flatMap(group => group.id === this.atlasId ? group.runs : []),
        ...(message.topics || []).filter(topic => topic.atlasId === this.atlasId)]
        .find(run => run.key === message.current);
      if (!current) return;
      this.token = message.token; this.context = message;
      this.renderPicker(); this.picker.hidden = false; this.changed(true);
    });
    window.parent.postMessage({channel: this.channel, type: 'ready', atlasId}, '*');
  }
  send(type, detail = {}) {
    if (!this.context) return;
    const dirty = this.hasUnsavedWork(); this.lastDirty = dirty;
    window.parent.postMessage({channel: this.channel, type, atlasId: this.atlasId, token: this.token, dirty, ...detail}, '*');
  }
  changed(force = false) {
    if (this.context && (force || this.hasUnsavedWork() !== this.lastDirty)) this.send('status');
  }
  choose(key) {
    if (this.dialog.open) this.dialog.close();
    this.send('select', {key});
  }
  option(key, title) {
    const option = document.createElement('option'); option.value = key; option.textContent = title; return option;
  }
  renderPicker() {
    const topics = this.context.topics || [];
    const selectedTopic = topics.find(topic => topic.key === this.context.current);
    const group = selectedTopic?.group || topics[0]?.group;
    const editions = [...new Set(topics.map(topic => topic.group))];
    this.edition.replaceChildren(...editions.map(label => this.option(label, label)));
    this.edition.value = group;
    this.edition.hidden = document.querySelector('#edition-label').hidden = !topics.length;
    this.select.replaceChildren(...(topics.length ? topics.filter(topic => topic.group === group).map(topic => this.option(topic.key, topic.title)) :
      this.context.groups.map(group => this.option(group.runs[0].key, group.runs[0].title))));
    const all = this.context.groups.flatMap(group => group.runs);
    const current = selectedTopic || all.find(run => run.key === this.context.current);
    if (![...this.select.options].some(option => option.value === current.key)) {
      this.select.append(this.option(current.key, current.title + (topics.length ? ' · 원본 캡처' : ' · 이전 실행')));
    }
    this.select.append(this.option('@catalog', topics.length ? '전체 메뉴 지도…' : '전체 시트 보기…'));
    this.select.value = current.key; this.select.title = current.title;
  }
  renderCatalog() {
    const list = document.querySelector('#workspace-list'); list.replaceChildren();
    const query = this.search.value.trim().toLocaleLowerCase();
    const make = (tag, text, className) => {
      const element = document.createElement(tag); element.textContent = text;
      if (className) element.className = className; return element;
    };
    const runButton = run => {
      const control = make('button', '', 'workspace-run'); control.type = 'button'; control.dataset.run = run.key;
      control.append(make('strong', run.title), make('small', run.status + ' · ' + run.rendered + '개 장면 · 실패 ' + run.failed + ' · 범위 확인 ' + run.gaps),
        make('small', run.freshness), make('small', run.key));
      if (run.key === this.context.current) control.append(make('small', '현재 시트', 'current-sheet'));
      control.onclick = () => this.choose(run.key); return control;
    };
    const activeGroup = this.context.topics?.find(topic => topic.key === this.context.current)?.group || this.context.topics?.[0]?.group;
    for (const group of [...new Set((this.context.topics || []).map(topic => topic.group))]) {
      const section = make('details', '', 'workspace-group product-map-group');
      section.open = !!query || group === activeGroup; section.append(make('summary', group));
      const grid = make('div', '', 'topic-grid');
      for (const topic of this.context.topics.filter(topic => topic.group === group)) {
        if (query && !(topic.title + ' ' + topic.description).toLocaleLowerCase().includes(query)) continue;
        const control = make('button', '', 'workspace-topic'); control.type = 'button'; control.dataset.topic = topic.id;
        control.append(make('strong', topic.title), make('small', `${topic.features}개 기능 · ${topic.rendered}개 장면` + (topic.gaps ? ` · 범위 확인 ${topic.gaps}` : '')),
          make('small', topic.description));
        control.onclick = () => this.choose(topic.key); grid.append(control);
      }
      if (grid.children.length) { section.append(grid); list.append(section); }
    }
    const hasTopics = !!this.context.topics?.length;
    const unassigned = new Set((this.context.unassigned || []).map(state => state.atlas));
    const history = document.createElement('details'); history.className = 'capture-history';
    const hasHistory = this.context.groups.some(group => group.runs.length > 1);
    history.append(make('summary', unassigned.size ? (hasHistory ? '미분류 캡처·이전 실행' : '미분류 캡처') : '이전 실행'));
    for (const group of this.context.groups) {
      // A fully assigned latest capture backs the topic; listing it again adds
      // no navigation. Retained history and unassigned observations stay reachable.
      const runs = hasTopics && !unassigned.has(group.id) ? group.runs.slice(1) : group.runs;
      if (!runs.length || query && !runs.some(run => (run.title + ' ' + run.key + ' ' + group.id).toLocaleLowerCase().includes(query))) continue;
      const section = make('section', '', 'workspace-group'); section.append(runButton(runs[0]));
      if (runs.length > 1) {
        const history = document.createElement('details'); history.append(make('summary', '이전 실행'));
        for (const run of runs.slice(1)) history.append(runButton(run));
        section.append(history);
      }
      (hasTopics ? history : list).append(section);
    }
    if (hasTopics && history.children.length > 1) list.append(history);
    if (this.context.unassigned?.length) list.append(make('p', `주제에 아직 배치하지 않은 관찰 ${this.context.unassigned.length}개 · 원본 캡처에서 확인할 수 있습니다.`, 'stale'));
    if (!list.children.length) list.append(make('p', '일치하는 전개도가 없습니다.'));
    for (const [title, values] of [['생성 중 또는 중단된 실행', this.context.unfinished], ['읽을 수 없는 실행', this.context.unreadable]]) {
      if (!values.length) continue;
      const section = make('section', '', 'workspace-group'); section.append(make('h3', title));
      for (const value of values) section.append(make('p', typeof value === 'string' ? value : value.name + ' · ' + value.reason));
      list.append(section);
    }
  }
}
