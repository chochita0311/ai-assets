"""Synthetic checks for topic ownership, evidence identity and safe composition."""
import json
from pathlib import Path
import re
import tempfile
import unittest

import atlas
import topics
import workspace
from capture import Responses


class TopicTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.source = Path(self.temporary.name)
        self.root = workspace.initialize(self.source)
        (self.source / 'app.txt').write_text('synthetic app')
        self.recipe = self.source / 'recipe.json'
        self.recipe.write_text('{}')

    def observation(self, owner, frame='entry', stamp='20260101', gap=False):
        run = self.root / 'runs' / (stamp + '-' + owner)
        run.mkdir()
        (run / 'frames').mkdir()
        document = '<!doctype html><html><head></head><body><button id="open" data-atlas-node="e1">Open</button></body></html>'
        (run / 'frames' / 'entry.html').write_text(document)
        state = {'id': frame, 'label': 'Open', 'surface': 'Synthetic settings', 'journey': 'entry',
                 'status': 'rendered', 'evidence': 'synthetic', 'viewport': {'width': 800, 'height': 600},
                 'locale': 'en-US', 'theme': 'light', 'regions': [], 'texts': [],
                 'elements': [{'id': 'e1', 'parent': None, 'tag': 'button', 'selector': '#open',
                               'label': 'Open', 'text': 'Open', 'visible': True,
                               'rect': {'x': 0, 'y': 0, 'width': 100, 'height': 30}}],
                 'document': 'frames/entry.html', 'payload': {'steps': [{'action': 'frame', 'id': frame}]}}
        manifest = {'schema': 'ui-atlas/v2', 'id': owner, 'title': owner, 'captured_at': stamp,
                    'source': atlas.source_identity(self.source, ['app.txt']),
                    'recipe': {'path': str(self.recipe), 'sha256': atlas.digest(self.recipe.read_bytes()), 'files': {}},
                    'frames': [state], 'replay': 'synthetic STATE_ID'}
        if gap:
            manifest['frames'].append({'id': 'native', 'label': 'Native chooser', 'surface': 'Settings',
                                      'journey': 'native', 'status': 'unverified', 'reason': 'Host not exercised'})
        atlas.write_json(run / 'atlas.json', manifest)
        atlas.package(run / 'atlas.json', run / 'index.html')
        return run

    def configure(self, definitions):
        (self.root / 'navigation.json').write_text(json.dumps({'schema': 'ui-atlas.navigation/v1', 'topics': definitions}))

    def definition(self, id, selections):
        return {'id': id, 'label': id, 'group': 'App', 'features': [{'id': 'general', 'label': 'General', 'select': selections}]}

    def payload(self, file):
        return json.loads(re.search(r'<script type="application/json" id="atlas-data">(.*?)</script>', file.read_text(), re.S)[1])

    def test_combines_duplicate_state_ids_without_changing_original_evidence(self):
        first, second = self.observation('alpha'), self.observation('beta')
        before = {p: p.read_bytes() for p in (first / 'atlas.json', second / 'atlas.json')}
        original = atlas.prepare(first / 'atlas.json')['frames'][0]['identity']
        self.configure([self.definition('settings', [{'atlas': 'alpha', 'frames': ['*']}, {'atlas': 'beta', 'frames': ['*']}])])
        workspace.catalog(self.root)
        view = self.payload(self.root / 'topics/settings.html')
        self.assertEqual({f['id'] for f in view['frames']}, {'alpha::entry', 'beta::entry'})
        self.assertEqual(view['frames'][0]['identity'], original)
        self.assertEqual(view['frames'][0]['origin']['frame'], 'entry')
        self.assertEqual(view['frames'][0]['origin']['atlas'], 'alpha')
        self.assertTrue(all(p.read_bytes() == value for p, value in before.items()))

    def test_menu_order_is_independent_of_capture_dates_and_keeps_history(self):
        self.observation('alpha', stamp='20260101')
        self.observation('beta', stamp='20261231')
        self.configure([self.definition('first', [{'atlas': 'alpha', 'frames': ['*']}]),
                        self.definition('second', [{'atlas': 'beta', 'frames': ['*']}])])
        workspace.catalog(self.root)
        html = (self.root / 'index.html').read_text()
        data = json.loads(re.search(r'id="workspace-data">(.*?)</script>', html, re.S)[1])
        self.assertEqual([topic['id'] for topic in data['topics']], ['first', 'second'])
        self.assertEqual(len(data['groups']), 2)
        self.assertEqual(data['unassigned'], [])

    def test_unknown_or_unmatched_states_stop_before_replacing_entry(self):
        self.observation('alpha')
        workspace.catalog(self.root)
        previous = (self.root / 'index.html').read_bytes()
        for selection in ({'atlas': 'missing', 'frames': ['*']}, {'atlas': 'alpha', 'frames': ['missing']}):
            self.configure([self.definition('settings', [selection])])
            with self.assertRaises(ValueError): workspace.catalog(self.root)
            self.assertEqual((self.root / 'index.html').read_bytes(), previous)

    def test_duplicate_primary_ownership_is_refused(self):
        self.observation('alpha')
        selection = [{'atlas': 'alpha', 'frames': ['*']}]
        self.configure([self.definition('first', selection), self.definition('second', selection)])
        with self.assertRaisesRegex(ValueError, 'more than one primary'): workspace.catalog(self.root)

    def test_link_trigger_must_match_exactly_one_visible_element(self):
        self.observation('alpha')
        self.observation('beta')
        definition = self.definition('settings', [{'atlas': 'alpha', 'frames': ['*']}, {'atlas': 'beta', 'frames': ['*']}])
        definition['links'] = [{'from': ['alpha', 'entry'], 'to': ['beta', 'entry'], 'label': 'Open next', 'element_selector': '#open', 'focus_selector': '#open'}]
        self.configure([definition]); workspace.catalog(self.root)
        view = self.payload(self.root / 'topics/settings.html')
        self.assertEqual(view['frames'][0]['transitions'][0]['target'], 'beta::entry')
        self.assertEqual(view['frames'][0]['transitions'][0]['target_node'], 'e1')
        definition['links'][0]['element_label'] = 'Missing'
        definition['links'][0].pop('element_selector')
        self.configure([definition])
        with self.assertRaisesRegex(ValueError, 'missing or ambiguous'): workspace.catalog(self.root)

    def test_unassigned_and_unverified_states_are_not_silently_lost(self):
        self.observation('alpha', gap=True)
        self.configure([self.definition('settings', [{'atlas': 'alpha', 'frames': ['entry']}])])
        workspace.catalog(self.root)
        data = json.loads(re.search(r'id="workspace-data">(.*?)</script>', (self.root / 'index.html').read_text(), re.S)[1])
        self.assertEqual(data['unassigned'][0]['frame'], 'native')
        self.configure([self.definition('settings', [{'atlas': 'alpha', 'frames': ['*']}])])
        workspace.catalog(self.root)
        view = self.payload(self.root / 'topics/settings.html')
        self.assertEqual(view['frames'][1]['status'], 'unverified')

    def test_failed_link_endpoint_stays_a_gap_without_blocking_other_states(self):
        for failed_owner in ('alpha', 'beta'):
            with self.subTest(failed_owner=failed_owner), tempfile.TemporaryDirectory() as temporary:
                old_root = self.root
                self.root = workspace.initialize(self.source, Path(temporary) / 'workspace')
                try:
                    runs = {owner: self.observation(owner) for owner in ('alpha', 'beta')}
                    path = runs[failed_owner] / 'atlas.json'
                    manifest = atlas.read_json(path)
                    manifest['frames'][0] = {'id': 'entry', 'label': 'Capture failed', 'surface': 'Settings',
                        'journey': 'entry', 'status': 'render-failed', 'reason': 'Synthetic unsupported renderer'}
                    atlas.write_json(path, manifest); atlas.package(path, path.parent / 'index.html')
                    definition = self.definition('settings', [{'atlas': owner, 'frames': ['*']} for owner in runs])
                    definition['links'] = [{'from': ['alpha', 'entry'], 'to': ['beta', 'entry'],
                        'label': 'Open', 'element_selector': '#open', 'focus_selector': '#open'}]
                    self.configure([definition]); workspace.catalog(self.root)
                    view = self.payload(self.root / 'topics/settings.html')
                    self.assertEqual(sum(frame['status'] == 'rendered' for frame in view['frames']), 1)
                    self.assertEqual(view['frames'][0]['transitions'][0]['unavailable'], True)
                    self.assertEqual(view['frames'][0]['transitions'][0]['selector'], '')
                finally:
                    self.root = old_root

    def test_source_drift_is_qualified_per_original_observation(self):
        self.observation('alpha')
        (self.source / 'app.txt').write_text('changed synthetic app')
        self.configure([self.definition('settings', [{'atlas': 'alpha', 'frames': ['*']}])])
        workspace.catalog(self.root)
        view = self.payload(self.root / 'topics/settings.html')
        self.assertEqual(view['freshness']['status'], 'changed')
        self.assertEqual(view['frames'][0]['origin']['freshness']['status'], 'changed')

    def test_topic_id_cannot_escape_its_output_owner(self):
        self.observation('alpha')
        self.configure([self.definition('../outside', [{'atlas': 'alpha', 'frames': ['*']}])])
        with self.assertRaises(ValueError): workspace.catalog(self.root)

    def test_unobserved_topic_is_visible_without_claiming_matching_source(self):
        self.observation('alpha')
        self.configure([{'id': 'native', 'label': 'Native', 'group': 'App', 'features': [
            {'id': 'chooser', 'label': 'Chooser', 'missing': [{'label': 'Open chooser', 'reason': 'Host not exercised'}]}
        ]}])
        workspace.catalog(self.root)
        view = self.payload(self.root / 'topics/native.html')
        self.assertEqual(view['schema'], 'ui-atlas.topic/v1')
        self.assertEqual(view['freshness']['status'], 'unavailable')
        self.assertEqual(view['frames'][0]['status'], 'unverified')

    def test_url_escaped_capture_directory_is_resolved_as_a_file_path(self):
        self.observation('alpha', stamp='20260101 synthetic')
        self.configure([self.definition('settings', [{'atlas': 'alpha', 'frames': ['*']}])])
        workspace.catalog(self.root)
        view = self.payload(self.root / 'topics/settings.html')
        self.assertIn('20260101 synthetic', view['frames'][0]['origin']['manifest'])

    def test_compound_gesture_does_not_become_a_single_control_jump(self):
        first = {'id': 'a::one', 'origin': {'atlas': 'a'}, 'journey': 'flow', 'label': 'Before',
                 'payload': {'steps': [{'action': 'frame', 'id': 'one'}]},
                 'transitions': [{'target': 'a::two', 'selector': '#open', 'label': 'Canceled'}]}
        second = {'id': 'a::two', 'origin': {'atlas': 'a'}, 'journey': 'flow', 'label': 'Canceled',
                  'payload': {'steps': first['payload']['steps'] + [{'action': 'click', 'selector': '#open'},
                              {'action': 'press', 'key': 'Escape'}, {'action': 'frame', 'id': 'two'}]}}
        topics.infer_links([first, second])
        self.assertEqual(first['transitions'][0]['selector'], '')
        self.assertEqual(first['transitions'][0]['action'], 'sequence')

    def test_response_only_result_is_a_frame_link_with_no_invented_trigger(self):
        first = {'id': 'a::one', 'origin': {'atlas': 'a'}, 'journey': 'flow', 'label': 'Pending',
                 'payload': {'steps': [{'action': 'frame', 'id': 'one'}]}}
        second = {'id': 'a::two', 'origin': {'atlas': 'a'}, 'journey': 'flow', 'label': 'Ready',
                  'payload': {'steps': first['payload']['steps'] + [{'action': 'respond', 'route': 'settings'}, {'action': 'frame', 'id': 'two'}]}}
        topics.infer_links([first, second])
        self.assertEqual(first['transitions'][0]['selector'], '')
        self.assertEqual(first['transitions'][0]['action'], 'respond')

    def test_control_after_response_or_navigation_is_not_anchored_to_earlier_state(self):
        for action in ('respond', 'goto'):
            first = {'id': 'a::one', 'origin': {'atlas': 'a'}, 'journey': 'flow', 'label': 'Before',
                     'payload': {'steps': [{'action': 'frame', 'id': 'one'}]},
                     'transitions': [{'target': 'a::two', 'selector': '#later', 'label': 'After'}]}
            second = {'id': 'a::two', 'origin': {'atlas': 'a'}, 'journey': 'flow', 'label': 'After',
                      'payload': {'steps': first['payload']['steps'] + [{'action': action},
                                  {'action': 'click', 'selector': '#later'}, {'action': 'frame', 'id': 'two'}]}}
            topics.infer_links([first, second])
            self.assertEqual(first['transitions'][0]['selector'], '')


class MergeTests(unittest.TestCase):
    def test_array_override_preserves_the_unmodified_synthetic_fields(self):
        class Request: method = 'GET'; url = 'http://example.test/api/settings'
        class Response:
            def json(self): return {'sources': [{'id': 1, 'color': 'green', 'root': '/synthetic'}]}
        class Route:
            request = Request()
            def fetch(self, **kwargs): return Response()
            def fulfill(self, **kwargs): self.result = kwargs['json']
        responses = Responses([], ('http', 'example.test'), Path('.'))
        route = Route()
        responses.fulfill(route, {'forward': True, 'merge': {'sources': {'0': {'color': 'blue'}}}})
        self.assertEqual(route.result, {'sources': [{'id': 1, 'color': 'blue', 'root': '/synthetic'}]})
        with self.assertRaisesRegex(ValueError, 'out of range'):
            responses.fulfill(route, {'forward': True, 'merge': {'sources': {'4': {'color': 'blue'}}}})


if __name__ == '__main__': unittest.main()
