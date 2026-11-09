"""Compose menu topics from retained observations without moving their evidence."""
from copy import deepcopy
from fnmatch import fnmatchcase
from pathlib import Path
from urllib.parse import quote, unquote

from atlas import ID, now, prepare, read_json, render, require


def frame_key(atlas_id, state_id):
    return atlas_id + '::' + state_id


def infer_links(frames):
    """Connect observed checkpoints, keeping compound gestures at frame level."""
    previous = {}
    for frame in frames:
        key = (frame['origin']['atlas'], frame['journey'])
        before = previous.get(key)
        if before:
            old = before.get('payload', {}).get('steps', [])
            new = frame.get('payload', {}).get('steps', [])
            if new[:len(old)] == old:
                actions = [step for step in new[len(old):]
                           if step['action'] in ('click', 'fill', 'press', 'hover', 'focus', 'scroll', 'goto', 'respond', 'advance-clock')]
                if actions:
                    controls = [step for step in actions if step['action'] not in ('goto', 'respond', 'advance-clock')]
                    link = next((item for item in before.get('transitions', []) if item['target'] == frame['id']), None)
                    if link is None:
                        action = actions[0]
                        link = {'target': frame['id'], 'label': frame['label'], 'selector': action.get('selector', ''), 'action': action['action']}
                        before.setdefault('transitions', []).append(link)
                    if len(controls) != 1 or actions[0] is not controls[0]:
                        link['selector'] = ''
                        link['action'] = 'sequence' if controls else actions[0]['action']
        previous[key] = frame


def build_topics(root, groups):
    """navigation.json owns product order; capture names and dates do not."""
    path = root / 'navigation.json'
    if not path.exists():
        return [], []
    navigation = read_json(path)
    require(navigation.get('schema') == 'ui-atlas.navigation/v1', 'Invalid navigation schema')
    require(isinstance(navigation.get('topics'), list) and navigation['topics'], 'Navigation needs topics')
    sources = {}
    loaded = {}
    for atlas_id, runs in groups.items():
        manifest = root / Path(unquote(runs[0]['url'])).parent / 'atlas.json'
        sources[atlas_id] = manifest

    def source(atlas_id):
        require(atlas_id in sources, 'Unknown observation atlas: ' + atlas_id)
        if atlas_id not in loaded:
            loaded[atlas_id] = prepare(sources[atlas_id])
        return loaded[atlas_id]

    topics, compositions, claimed, seen = [], [], set(), set()
    for definition in navigation['topics']:
        topic_id = definition.get('id', '')
        require(ID.fullmatch(topic_id) and topic_id not in seen, 'Invalid or duplicate topic ID')
        seen.add(topic_id)
        require(bool(definition.get('label')) and bool(definition.get('group')), 'Topic needs label and group')
        frames, resources, observations = [], {}, {}
        feature_ids = set()
        for feature in definition.get('features', []):
            feature_id = feature.get('id', '')
            require(ID.fullmatch(feature_id) and feature_id not in feature_ids and feature.get('label'),
                    'Invalid or duplicate feature')
            feature_ids.add(feature_id)
            for selection in feature.get('select', []):
                atlas_id = selection['atlas']
                original = source(atlas_id)
                patterns = selection.get('frames', [])
                require(patterns and all(isinstance(pattern, str) for pattern in patterns), 'Select explicit state patterns')
                matches = [frame for frame in original['frames']
                           if any(fnmatchcase(frame['id'], pattern) for pattern in patterns)]
                require(matches, 'No states matched: ' + atlas_id + ' / ' + repr(patterns))
                observations[atlas_id] = {key: original.get(key) for key in ('source', 'freshness', 'replay')}
                observations[atlas_id]['recipe'] = original.get('recipe', {})
                observations[atlas_id]['captured_at'] = original.get('captured_at') or 'unknown'
                observations[atlas_id]['states'] = [frame['id'] for frame in original['frames']]
                resources.update(original.get('resources', {}))
                for item in matches:
                    identity = (atlas_id, item['id'])
                    require(identity not in claimed, 'State has more than one primary topic: ' + repr(identity))
                    claimed.add(identity)
                    frame = deepcopy(item)
                    frame['origin'] = {'atlas': atlas_id, 'frame': item['id'],
                                       'manifest': str(sources[atlas_id].relative_to(root)),
                                       'replay': original['replay'], 'freshness': original['freshness'], 'captured_at': original.get('captured_at') or 'unknown'}
                    frame['id'] = frame_key(*identity)
                    frame['origin']['surface'] = item['surface']
                    frame['surface'] = definition['label']
                    frame['label'] = selection.get('labels', {}).get(item['id'], item['label'])
                    frame['feature'] = {'id': feature_id, 'label': feature['label'], 'description': feature.get('description', '')}
                    frame['flow_label'] = selection.get('flow_label', frame.get('journey_label', item['journey']))
                    frame['variant'] = selection.get('variant') or ('narrow' if frame.get('viewport', {}).get('width', 1440) <= 600 else 'wide')
                    for link in frame.get('transitions', []):
                        link['target'] = frame_key(atlas_id, link['target'])
                    frames.append(frame)
            for index, gap in enumerate(feature.get('missing', [])):
                require(gap.get('label') and gap.get('reason'), 'Missing states need their reason')
                frames.append({'id': topic_id + '.' + feature_id + '.missing-' + str(index),
                    'label': gap['label'], 'surface': definition['label'], 'journey': feature_id,
                    'feature': {'id': feature_id, 'label': feature['label']},
                    'status': 'unverified', 'reason': gap['reason']})
        require(frames, 'Empty topic: ' + topic_id)
        infer_links([frame for frame in frames if frame['status'] == 'rendered'])
        by_origin = {(frame['origin']['atlas'], frame['origin']['frame']): frame for frame in frames if 'origin' in frame}
        for relation in definition.get('links', []):
            before = by_origin.get(tuple(relation['from']))
            after = by_origin.get(tuple(relation['to']))
            require(before is not None and after is not None, 'Topic link has an unknown endpoint')
            if before['status'] != 'rendered' or after['status'] != 'rendered':
                # A failed capture is evidence of a gap, not a bad menu map or
                # permission to invent its trigger/focus from an older state.
                before.setdefault('transitions', []).append({'target': after['id'],
                    'label': relation['label'], 'selector': '', 'unavailable': True})
                continue
            element_label = relation.get('element_label')
            element_selector = relation.get('element_selector')
            matches = [element for element in before.get('elements', [])
                       if element.get('visible') and ((element_label and element.get('label') == element_label) or (element_selector and element.get('selector') == element_selector))] if element_label or element_selector else []
            require(not (element_label or element_selector) or len(matches) == 1, 'Topic link trigger is missing or ambiguous: ' + str(element_label))
            link = {'target': after['id'], 'label': relation['label'],
                    'selector': matches[0]['selector'] if matches else '', 'action': relation.get('action', 'click')}
            if relation.get('focus_selector'):
                targets = [element for element in after.get('elements', [])
                           if element.get('visible') and element['selector'] == relation['focus_selector']]
                require(len(targets) == 1, 'Linked result focus is missing or ambiguous')
                link['target_node'] = targets[0]['id']
            existing = next((item for item in before.get('transitions', [])
                             if item['target'] == link['target'] and item.get('selector') == link['selector']), None)
            if existing is None:
                before.setdefault('transitions', []).append(link)
            else:
                existing.update(link)
        states = {frame['id'] for frame in frames}
        for frame in frames:
            frame['transitions'] = [link for link in frame.get('transitions', []) if link['target'] in states]
        statuses = [item['freshness']['status'] for item in observations.values()]
        freshness = {'status': 'unavailable' if not statuses or 'unavailable' in statuses else 'changed' if 'changed' in statuses else 'matched',
                     'checked_at': now(), 'changed': [], 'unavailable': []}
        if not observations:
            freshness['unavailable'].append('This topic has no observed source state yet.')
        for atlas_id, evidence in observations.items():
            for key in ('changed', 'unavailable'):
                freshness[key].extend(atlas_id + ': ' + item for item in evidence['freshness'][key])
        atlas = {'schema': 'ui-atlas.topic/v1', 'id': topic_id, 'title': definition['label'],
                 'scope': definition.get('description', 'Recorded states grouped by their product menu.'),
                 'captured_at': max((item['captured_at'] for item in observations.values()), default='unobserved'),
                 'frames': frames, 'resources': resources, 'freshness': freshness,
                 'composition': {'observations': observations},
                 'replay': '', 'limitations': navigation.get('limitations', []), 'journey_failures': []}
        url = 'topics/' + quote(topic_id, safe='') + '.html'
        compositions.append((atlas, root / url))
        topics.append({'key': 'topic:' + topic_id, 'atlasId': topic_id, 'id': topic_id,
                       'title': definition['label'], 'group': definition['group'], 'url': url,
                       'description': atlas['scope'], 'features': len(feature_ids),
                       'rendered': sum(frame['status'] == 'rendered' for frame in frames),
                       'gaps': sum(frame['status'] != 'rendered' for frame in frames),
                       'origins': [{'atlas': key[0], 'frame': key[1]} for key in by_origin],
                       'freshness': freshness['status']})
    unassigned = []
    for atlas_id, manifest in sources.items():
        for frame in read_json(manifest)['frames']:
            if (atlas_id, frame['id']) not in claimed:
                unassigned.append({'atlas': atlas_id, 'frame': frame['id'], 'label': frame['label']})
    for atlas, output in compositions:
        render(atlas, output)
    return topics, unassigned
