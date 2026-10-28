import argparse
from datetime import datetime, timezone
from http.client import HTTPResponse
import importlib.util
from io import BytesIO
import json
from pathlib import Path
import sys
import tempfile
import unittest
from unittest.mock import patch
from urllib.error import URLError
from zoneinfo import ZoneInfo


SOURCE = Path(__file__).resolve().parents[1] / "reset_alert.py"
SPEC = importlib.util.spec_from_file_location("reset_alert", SOURCE)
monitor = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(monitor)
KST = ZoneInfo("Asia/Seoul")
NOW = datetime(2025, 1, 1, tzinfo=timezone.utc)


def state():
    return {"initialized": True, "seen": [], "failures": 0, "failure_notified": False}


def reset(identifier="example", kind="regular"):
    return {"id": identifier, "reset_type": kind, "announced_at": "2025-01-01T00:00:00Z"}


def scheduled(when="2025-01-01T02:55:00Z", kind="regular"):
    return dict(reset(kind=kind), status="scheduled", scheduled_for=when)


def snapshot(latest=None, pending=None, watch=None):
    return {"latest_reset": latest, "scheduled_reset": pending, "active_watch": watch}


class EventTests(unittest.TestCase):
    def test_scheduled_reset_uses_requested_title_and_timezone(self):
        event, = monitor.events_for(snapshot(pending=scheduled()), state(), NOW, KST)
        self.assertEqual(event[1:], ("Codex Reset", "01/01 11:55 KST"))

    def test_null_time_is_unknown_and_missing_field_is_invalid(self):
        event, = monitor.events_for(snapshot(pending=scheduled(None)), state(), NOW, KST)
        self.assertEqual(event[1:], ("Codex Reset", "시각 미정"))
        invalid = scheduled()
        del invalid["scheduled_for"]
        with self.assertRaises(ValueError):
            monitor.events_for(snapshot(pending=invalid), state(), NOW, KST)

    def test_banked_reset_is_not_reported_as_a_direct_reset(self):
        event, = monitor.events_for(snapshot(pending=scheduled(kind="banked")), state(), NOW, KST)
        self.assertEqual(event[2], "01/01 11:55 KST (리셋권)")
        event, = monitor.events_for(snapshot(latest=reset(kind="banked")), state(), NOW, KST)
        self.assertEqual(event[2], "01/01 09:00 KST (리셋권 확인)")

    def test_latest_timestamp_is_announcement_or_observation(self):
        event, = monitor.events_for(snapshot(latest=reset()), state(), NOW, KST)
        self.assertEqual(event[2], "01/01 09:00 KST (확인)")

    def test_existing_latest_is_baselined_but_pending_is_not(self):
        initial = state()
        initial["initialized"] = False
        events = monitor.events_for(snapshot(latest=reset("old"), pending=scheduled()), initial, NOW, KST)
        self.assertEqual([event[0] for event in events], ["scheduled:example:2025-01-01T02:55:00Z"])
        self.assertIn("latest:old", initial["seen"])
        monitor.remember(initial, events[0][0])
        self.assertEqual(monitor.events_for(snapshot(latest=reset("old"), pending=scheduled()), initial, NOW, KST), [])

    def test_changed_scheduled_time_triggers_an_update(self):
        current = state()
        event, = monitor.events_for(snapshot(pending=scheduled()), current, NOW, KST)
        monitor.remember(current, event[0])
        changed = scheduled("2025-01-01T03:00:00Z")
        event, = monitor.events_for(snapshot(pending=changed), current, NOW, KST)
        self.assertEqual(event[2], "01/01 12:00 KST")

    def test_watch_is_speculative_and_its_expiry_is_not_a_reset_time(self):
        watch = {
            "level": "elevated", "observed_at": "2024-12-31T23:00:00Z",
            "expires_at": "2025-01-01T02:55:00Z", "text": "example",
            "source": {"type": "x_post", "url": "https://example.com/post"},
        }
        event, = monitor.events_for(snapshot(watch=watch), state(), NOW, KST)
        self.assertEqual(event[2], "시각 미정 (가능성)")
        watch["expires_at"] = "2024-12-31T23:59:00Z"
        self.assertEqual(monitor.events_for(snapshot(watch=watch), state(), NOW, KST), [])

    def test_invalid_timestamp_or_kind_is_rejected(self):
        with self.assertRaises(ValueError):
            monitor.events_for(snapshot(pending=scheduled("2025-01-01T11:55:00")), state(), NOW, KST)
        with self.assertRaises(ValueError):
            monitor.events_for(snapshot(latest=reset(kind="unexpected")), state(), NOW, KST)

    def test_iana_zone_uses_daylight_saving_at_the_event_time(self):
        eastern = ZoneInfo("America/New_York")
        self.assertEqual(monitor.format_time("2025-07-01T00:00:00Z", eastern), "06/30 20:00 EDT")
        self.assertEqual(monitor.format_time("2025-12-01T00:00:00Z", eastern), "11/30 19:00 EST")

    def test_state_directory_must_be_absolute(self):
        with self.assertRaises(argparse.ArgumentTypeError):
            monitor.absolute_path("relative/state")

    def test_signal_types_are_pruned_with_seen_keys(self):
        current = state()
        for index in range(monitor.MAX_SEEN + 1):
            monitor.remember(current, f"latest:{index}", "regular")
        self.assertEqual(len(current["seen"]), monitor.MAX_SEEN)
        self.assertEqual(len(current["signal_types"]), monitor.MAX_SEEN)
        self.assertNotIn("latest:0", current["signal_types"])


class CheckTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="reset-alert-test-")
        self.addCleanup(self.temp.cleanup)
        self.directory = Path(self.temp.name)

    def test_three_failures_alert_once_then_recovery(self):
        with patch.object(monitor, "read_status", side_effect=[URLError("offline")] * 4 + [snapshot(latest=reset())]), patch.object(monitor, "notify") as notify:
            self.assertEqual([monitor.run_check(self.directory, KST) for _ in range(4)], [1, 1, 1, 1])
            self.assertEqual(notify.call_count, 1)
            self.assertIn("확인 필요", notify.call_args.args[0])
            self.assertEqual(monitor.run_check(self.directory, KST), 0)
            self.assertEqual(notify.call_count, 2)
            self.assertIn("복구", notify.call_args.args[0])
        saved = monitor.load_state(self.directory / "state.json")
        self.assertEqual(saved["failures"], 0)
        self.assertFalse(saved["failure_notified"])
        self.assertEqual(list(self.directory.glob(".state-*")), [])

    def test_truncated_chunked_response_counts_as_failure_and_recovers(self):
        class FakeSocket:
            def makefile(self, *args, **kwargs):
                return BytesIO(b"HTTP/1.1 200 OK\r\nTransfer-Encoding: chunked\r\n\r\n5\r\nab")

        def truncated_response(*args, **kwargs):
            response = HTTPResponse(FakeSocket())
            response.begin()
            return response

        with patch.object(monitor, "urlopen", side_effect=truncated_response), patch.object(monitor, "notify") as notify:
            self.assertEqual([monitor.run_check(self.directory, KST) for _ in range(3)], [1, 1, 1])
            saved = monitor.load_state(self.directory / "state.json")
            self.assertEqual(saved["failures"], 3)
            self.assertTrue(saved["failure_notified"])
            self.assertEqual(notify.call_count, 1)
            self.assertIn("확인 필요", notify.call_args.args[0])
            with patch.object(monitor, "read_status", return_value=snapshot()):
                self.assertEqual(monitor.run_check(self.directory, KST), 0)
            self.assertEqual(notify.call_count, 2)
            self.assertIn("복구", notify.call_args.args[0])
        saved = monitor.load_state(self.directory / "state.json")
        self.assertEqual(saved["failures"], 0)
        self.assertFalse(saved["failure_notified"])

    def test_truncated_content_length_counts_as_failure_even_when_json_is_valid(self):
        body = json.dumps({"data": snapshot()}).encode()

        class FakeSocket:
            def makefile(self, *args, **kwargs):
                headers = f"HTTP/1.1 200 OK\r\nContent-Length: {len(body) + 10}\r\n\r\n".encode()
                return BytesIO(headers + body)

        def truncated_response(*args, **kwargs):
            response = HTTPResponse(FakeSocket())
            response.begin()
            return response

        with patch.object(monitor, "urlopen", side_effect=truncated_response), patch.object(monitor, "notify") as notify:
            self.assertEqual([monitor.run_check(self.directory, KST) for _ in range(3)], [1, 1, 1])
            saved = monitor.load_state(self.directory / "state.json")
            self.assertEqual(saved["failures"], 3)
            self.assertTrue(saved["failure_notified"])
            self.assertEqual(notify.call_count, 1)
            self.assertIn("확인 필요", notify.call_args.args[0])

    def test_complete_content_length_response_is_accepted(self):
        data = snapshot(latest=reset())
        body = json.dumps({"data": data}).encode()

        class FakeSocket:
            def makefile(self, *args, **kwargs):
                headers = f"HTTP/1.1 200 OK\r\nContent-Length: {len(body)}\r\n\r\n".encode()
                return BytesIO(headers + body)

        response = HTTPResponse(FakeSocket())
        response.begin()
        with patch.object(monitor, "urlopen", return_value=response):
            self.assertEqual(monitor.read_status(), data)

    def test_legacy_state_baselines_kind_then_alerts_on_changes_and_reversions(self):
        latest_key = "latest:example"
        scheduled_key = "scheduled:example:2025-01-01T02:55:00Z"
        legacy = state()
        legacy["seen"] = [scheduled_key, latest_key]
        monitor.save_state(self.directory / "state.json", legacy)
        regular = snapshot(latest=reset(), pending=scheduled())
        banked = snapshot(latest=reset(kind="banked"), pending=scheduled(kind="banked"))
        with patch.object(monitor, "read_status", side_effect=[regular, banked, banked, regular]), patch.object(monitor, "notify") as notify:
            self.assertEqual(monitor.run_check(self.directory, KST), 0)
            notify.assert_not_called()
            saved = monitor.load_state(self.directory / "state.json")
            self.assertEqual(saved["seen"], legacy["seen"])
            self.assertEqual(saved["signal_types"], {scheduled_key: "regular", latest_key: "regular"})
            self.assertEqual(monitor.run_check(self.directory, KST), 0)
            self.assertEqual([call.args[1] for call in notify.call_args_list], [
                "01/01 11:55 KST (리셋권)", "01/01 09:00 KST (리셋권 확인)"
            ])
            self.assertEqual(monitor.run_check(self.directory, KST), 0)
            self.assertEqual(notify.call_count, 2)
            self.assertEqual(monitor.run_check(self.directory, KST), 0)
            self.assertEqual([call.args[1] for call in notify.call_args_list[-2:]], [
                "01/01 11:55 KST", "01/01 09:00 KST (확인)"
            ])

    def test_failed_reclassification_notification_preserves_old_type_for_retry(self):
        key = "scheduled:example:2025-01-01T02:55:00Z"
        existing = state()
        monitor.remember(existing, key, "banked")
        monitor.save_state(self.directory / "state.json", existing)
        response = snapshot(pending=scheduled())
        with patch.object(monitor, "read_status", return_value=response), patch.object(monitor, "notify", side_effect=OSError("unavailable")):
            with self.assertRaises(OSError):
                monitor.run_check(self.directory, KST)
        self.assertEqual(monitor.load_state(self.directory / "state.json")["signal_types"][key], "banked")
        with patch.object(monitor, "read_status", return_value=response), patch.object(monitor, "notify") as notify:
            self.assertEqual(monitor.run_check(self.directory, KST), 0)
            notify.assert_called_once_with("Codex Reset", "01/01 11:55 KST")
            self.assertEqual(monitor.run_check(self.directory, KST), 0)
            self.assertEqual(notify.call_count, 1)

    def test_failed_notification_is_retried_without_marking_it_sent(self):
        response = snapshot(pending=scheduled())
        with patch.object(monitor, "read_status", return_value=response), patch.object(monitor, "notify", side_effect=OSError("unavailable")):
            with self.assertRaises(OSError):
                monitor.run_check(self.directory, KST)
        saved = monitor.load_state(self.directory / "state.json")
        self.assertNotIn("scheduled:example:2025-01-01T02:55:00Z", saved["seen"])
        with patch.object(monitor, "read_status", return_value=response), patch.object(monitor, "notify") as notify:
            self.assertEqual(monitor.run_check(self.directory, KST), 0)
            notify.assert_called_once_with("Codex Reset", "01/01 11:55 KST")

    def test_osascript_treats_message_as_data(self):
        with patch.object(monitor.subprocess, "run") as run:
            monitor.notify('title "quoted"', 'body; do shell script "bad"')
        self.assertEqual(run.call_args.args[0][2:], ['title "quoted"', 'body; do shell script "bad"'])
        self.assertNotIn("do shell script", run.call_args.kwargs["input"])

    def test_status_response_needs_each_field(self):
        class Response:
            headers = {}

            def __enter__(self):
                return self

            def __exit__(self, *args):
                pass

            def read(self, limit):
                return json.dumps({"data": {"latest_reset": None}}).encode()

        with patch.object(monitor, "urlopen", return_value=Response()):
            with self.assertRaises(ValueError):
                monitor.read_status()

    def test_test_mode_needs_neither_state_nor_network(self):
        with patch.object(sys, "argv", ["reset_alert.py", "--test", "--timezone", "Asia/Seoul"]), patch.object(monitor, "notify") as notify, patch.object(monitor, "read_status", side_effect=AssertionError("unexpected network")):
            self.assertEqual(monitor.main(), 0)
        title, body = notify.call_args.args
        self.assertEqual(title, "Codex Reset")
        self.assertRegex(body, r"^\d{2}/\d{2} \d{2}:\d{2} KST$")

    def test_direct_cli_rejects_runtime_state_in_checkout(self):
        checkout = (self.directory / "checkout").resolve()
        checkout.mkdir()
        args = ["reset_alert.py", "--state-dir", str(checkout / "runtime")]
        with patch.object(sys, "argv", args), patch.object(monitor, "source_checkout", return_value=checkout), patch.object(monitor, "run_check") as run:
            with self.assertRaises(SystemExit):
                monitor.main()
        run.assert_not_called()


if __name__ == "__main__":
    unittest.main()
