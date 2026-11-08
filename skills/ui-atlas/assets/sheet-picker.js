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
    this.select.addEventListener('change', () => {
      const key = this.select.value;
      this.select.value = this.context.current;
      if (key === '@catalog') { this.search.value = ''; this.renderCatalog(); this.dialog.showModal(); }
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
      const current = message.groups.flatMap(group => group.id === this.atlasId ? group.runs : [])
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
    this.select.replaceChildren(...this.context.groups.map(group => this.option(group.runs[0].key, group.runs[0].title)));
    const all = this.context.groups.flatMap(group => group.runs);
    const current = all.find(run => run.key === this.context.current);
    if (![...this.select.options].some(option => option.value === current.key)) {
      this.select.append(this.option(current.key, current.title + ' · 이전 실행'));
    }
    this.select.append(this.option('@catalog', '전체 시트 보기…'));
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
    for (const group of this.context.groups) {
      if (query && !group.runs.some(run => (run.title + ' ' + run.key + ' ' + group.id).toLocaleLowerCase().includes(query))) continue;
      const section = make('section', '', 'workspace-group'); section.append(runButton(group.runs[0]));
      if (group.runs.length > 1) {
        const history = document.createElement('details'); history.append(make('summary', '이전 실행'));
        for (const run of group.runs.slice(1)) history.append(runButton(run));
        section.append(history);
      }
      list.append(section);
    }
    if (!list.children.length) list.append(make('p', '일치하는 전개도가 없습니다.'));
    for (const [title, values] of [['생성 중 또는 중단된 실행', this.context.unfinished], ['읽을 수 없는 실행', this.context.unreadable]]) {
      if (!values.length) continue;
      const section = make('section', '', 'workspace-group'); section.append(make('h3', title));
      for (const value of values) section.append(make('p', typeof value === 'string' ? value : value.name + ' · ' + value.reason));
      list.append(section);
    }
  }
}
