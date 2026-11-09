class AtlasCatalog {
  constructor(frames) {
    this.frames = frames;
    this.byFrame = new Map(frames.map(frame => [frame.id, frame]));
    this.indices = new Map();
    this.sections = new Map();
    for (const frame of frames) {
      // Older inventories did not record overflow clipping. At least reject
      // viewport-external targets; the bridge checks actual clipping on selection.
      for (const element of frame.elements) {
        if ('visibleRect' in element) element.visible = !!element.visibleRect;
        else if (element.rect) {
          const r = element.rect;
          element.visible = element.visible && r.x + r.width > 0 && r.y + r.height > 0 &&
            r.x < frame.viewport.width && r.y < frame.viewport.height;
        }
      }
      const key = this.sectionKey(frame);
      if (!this.sections.has(key)) this.sections.set(key, {id: key, surface: frame.surface,
        label: frame.feature?.label || frame.journey_label || frame.journey, frames: []});
      this.sections.get(key).frames.push(frame);
      const elements = new Map(frame.elements.map(element => [element.id, element]));
      const children = new Map();
      for (const element of frame.elements) {
        const parent = element.parent ?? null;
        if (!children.has(parent)) children.set(parent, []);
        children.get(parent).push(element);
      }
      const regions = new Map();
      for (const region of frame.regions) {
        if (!region.rect) continue;
        const roots = frame.elements.filter(element => element.regions?.includes(region.id) &&
          !elements.get(element.parent)?.regions?.includes(region.id));
        if (roots.length === 1) regions.set(region.id, roots[0]);
      }
      this.indices.set(frame.id, {elements, children, regions});
    }
    this.allSections = this.sections;
  }
  sectionKey(frame) { return frame.feature?.id || frame.surface + '\n' + frame.journey; }
  filter(variant) {
    this.sections = new Map([...this.allSections].map(([id, section]) => [id, {...section, frames: section.frames.filter(frame => variant === 'all' || frame.variant === variant)}]).filter(([, section]) => section.frames.length));
  }
  section(frame) { return this.sections.get(this.sectionKey(frame)) || this.allSections.get(this.sectionKey(frame)); }
  flow(frame) { return frame.origin ? this.frames.filter(other => other.journey === frame.journey && other.origin?.atlas === frame.origin.atlas) : this.section(frame).frames; }
  index(frame) { return this.indices.get(frame.id); }
  name(frame, element) {
    const region = frame.regions.find(region => this.index(frame).regions.get(region.id)?.id === element.id);
    if (region) return region.label;
    if (element.label && element.label !== element.tag && !element.label.startsWith(element.tag + '#')) return element.label;
    const names = {html: '문서', body: '화면', div: '영역', span: '텍스트 영역', p: '문단', button: '버튼',
      input: '입력', select: '선택 입력', svg: '아이콘', path: '아이콘 경로', dialog: '대화상자', a: '링크',
      section: '섹션', header: '머리글', footer: '바닥글', nav: '탐색', main: '본문', ul: '목록', li: '목록 항목'};
    return (names[element.tag] || element.tag) + (element.label?.startsWith(element.tag + '#') ? ' · ' + element.label.slice(element.tag.length + 1) : '');
  }
  ancestors(frame, element) {
    const result = [], seen = new Set();
    while (element && !seen.has(element.id)) {
      seen.add(element.id); result.unshift(element); element = this.index(frame).elements.get(element.parent);
    }
    return result;
  }
  search(query, frame = null) {
    query = query.trim().toLocaleLowerCase();
    if (!query) return [];
    const results = [];
    for (const current of frame ? [frame] : this.frames) {
      if ([current.label, current.surface, current.journey_label].join(' ').toLocaleLowerCase().includes(query)) results.push({frame: current});
      for (const element of current.elements) {
        if (element.visible && [this.name(current, element), element.text].join(' ').toLocaleLowerCase().includes(query)) results.push({frame: current, element});
      }
    }
    return results;
  }
  match(from, element, target) {
    const index = this.index(target);
    const region = from.regions.find(region => this.index(from).regions.get(region.id)?.id === element.id);
    if (region) {
      const match = index.regions.get(region.id);
      return match?.visible ? match : null;
    }
    // Positional selectors and sequential inventory IDs are not cross-state identities.
    if (!/:nth-|:first-|:last-/.test(element.selector) && (element.selector.includes('#') || ['html', 'body'].includes(element.tag))) {
      const exact = target.elements.filter(other => other.visible && other.selector === element.selector && other.tag === element.tag);
      if (exact.length === 1) return exact[0];
    }
    const meaningful = element.text || (element.label !== element.tag && !element.label?.startsWith(element.tag + '#') ? element.label : '');
    if (!meaningful) return null;
    const equivalent = other => other.visible && other.tag === element.tag &&
      (other.text || other.label) === meaningful &&
      (element.regions || []).every(region => other.regions?.includes(region));
    if (from.elements.filter(equivalent).length !== 1) return null;
    const matches = target.elements.filter(equivalent);
    if (matches.length !== 1) return null;
    const match = matches[0];
    // A label change must not transfer identity to an already-distinct control.
    const knownOther = from.elements.some(other => other.id !== element.id &&
      other.tag === match.tag && other.selector === match.selector &&
      !/:nth-|:first-|:last-/.test(other.selector) && other.selector.includes('#'));
    const targetRegion = target.regions.find(region => index.regions.get(region.id)?.id === match.id);
    const previousRoot = targetRegion && this.index(from).regions.get(targetRegion.id);
    return knownOther || previousRoot && previousRoot.id !== element.id ? null : match;
  }
  noteTarget(frame, note) {
    if (note.identity === frame.identity) {
      const node = this.index(frame).elements.get(note.node);
      if (node?.visible) return node;
    }
    const matches = frame.elements.filter(element => element.visible && element.selector === note.selector &&
      (!note.quote || element.text === note.quote));
    return matches.length === 1 && !/:nth-|:first-|:last-/.test(note.selector || '') ? matches[0] : null;
  }
  description(section) {
    const first = section.frames[0], last = section.frames.at(-1);
    if (first.feature) return [
      ['목적', first.feature.description || first.feature.label + '의 화면과 세부 상태 검토'],
      ['조건', '장면별 조건과 조작 기록은 Payload에서 확인합니다.'],
      ['동작', '연결된 상태로 이동하거나 요소를 선택해 의견을 남깁니다.'],
      ['관찰 결과', section.frames.map(frame => frame.label).join(' · ')],
      ['예외', '미관찰 상태와 실제 앱의 재현 실행은 관찰 범위에서 구분합니다.']
    ];
    const authored = first.description || {};
    const steps = last.payload?.steps || [];
    const actions = steps.filter(step => ['goto', 'click', 'hover', 'focus', 'fill', 'press', 'scroll'].includes(step.action));
    const verbs = {goto: '화면 열기', click: '클릭', hover: '호버', focus: '포커스', fill: '입력', press: '키 입력', scroll: '스크롤'};
    const actionLabels = actions.map(step => {
      const element = section.frames.flatMap(frame => {
        const item = frame.elements.find(item => item.selector === step.selector);
        return item ? [this.name(frame, item)] : [];
      })[0];
      return [element || (step.action === 'press' ? step.key : ''), verbs[step.action]].filter(Boolean).join(' · ');
    });
    return [
      [authored.purpose ? '목적' : '흐름', authored.purpose || section.label],
      ['조건', first.conditions || '별도 조건 설명 없음'],
      ['동작', authored.action || actionLabels.join(' → ') || '기록된 사용자 동작 없음'],
      ['관찰 결과', authored.result || section.frames.map(frame => frame.label).join(' → ')],
      ['예외', authored.exceptions || '별도 예외 설명 없음']
    ];
  }
}
