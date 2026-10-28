#!/usr/bin/env python3
"""Check a public reset tracker and notify the logged-in macOS user."""

import argparse
from datetime import datetime, timedelta, timezone
import fcntl
from http.client import HTTPException
import json
import logging
from logging.handlers import RotatingFileHandler
import os
from pathlib import Path
import subprocess
import tempfile
from urllib.error import HTTPError, URLError
from urllib.request import Request, urlopen
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


API_URL = "https://codex-resets.com/api/v1/status"
MAX_RESPONSE_BYTES = 1024 * 1024
MAX_SEEN = 100
LOG = logging.getLogger("codex-reset-alert")
APPLE_SCRIPT = '''on run argv
    display notification (item 2 of argv) with title (item 1 of argv) sound name "Glass"
end run
'''


def parse_time(value):
    if not isinstance(value, str):
        raise ValueError("invalid timestamp")
    parsed = datetime.fromisoformat(value.replace("Z", "+00:00"))
    if parsed.tzinfo is None:
        raise ValueError("timestamp has no timezone")
    return parsed.astimezone(timezone.utc)


def format_time(value, display_timezone):
    # astimezone(None) applies the system's rules for the timestamp, including DST.
    local = parse_time(value).astimezone(display_timezone)
    zone = local.tzname() or local.strftime("UTC%z")
    return local.strftime("%m/%d %H:%M ") + zone


def read_status():
    request = Request(
        API_URL,
        headers={"Accept": "application/json", "User-Agent": "CodexResetAlert/1.0"},
    )
    with urlopen(request, timeout=20) as response:
        raw = response.read(MAX_RESPONSE_BYTES + 1)
        content_length = response.headers.get("Content-Length")
        transfer_encoding = response.headers.get("Transfer-Encoding")
    if len(raw) > MAX_RESPONSE_BYTES:
        raise ValueError("status response is too large")
    if content_length is not None and transfer_encoding is None:
        try:
            expected_length = int(content_length)
        except ValueError as exc:
            raise HTTPException("invalid status Content-Length") from exc
        if expected_length < 0 or len(raw) != expected_length:
            raise HTTPException("incomplete status response")
    body = json.loads(raw)
    if not isinstance(body, dict) or not isinstance(body.get("data"), dict):
        raise ValueError("invalid status response")
    data = body["data"]
    for key in ("latest_reset", "scheduled_reset", "active_watch"):
        if key not in data or (data[key] is not None and not isinstance(data[key], dict)):
            raise ValueError("missing or invalid " + key)
    return data


def reset_info(item):
    if not isinstance(item.get("id"), str) or not item["id"]:
        raise ValueError("reset has no id")
    if item.get("reset_type") not in ("regular", "banked"):
        raise ValueError("reset has unknown type")
    parse_time(item.get("announced_at"))


def remember(state, key, kind=None):
    if key not in state["seen"]:
        state["seen"].append(key)
        state["seen"] = state["seen"][-MAX_SEEN:]
    types = state.setdefault("signal_types", {})
    if kind is not None:
        types[key] = kind
    state["signal_types"] = {item: value for item, value in types.items() if item in state["seen"]}


def reset_is_new(state, key, kind):
    if key not in state["seen"]:
        return True
    types = state.setdefault("signal_types", {})
    if key not in types:
        # Old state did not record reset types; adopt the current type silently.
        types[key] = kind
        return False
    return types[key] != kind


def events_for(data, state, now, display_timezone):
    """Return new notifications; baseline the previous latest reset silently."""
    latest = data["latest_reset"]
    scheduled = data["scheduled_reset"]
    watch = data["active_watch"]
    if latest is not None:
        reset_info(latest)
    if scheduled is not None:
        reset_info(scheduled)
        if scheduled.get("status") != "scheduled" or "scheduled_for" not in scheduled:
            raise ValueError("invalid scheduled reset")
        if scheduled["scheduled_for"] is not None:
            parse_time(scheduled["scheduled_for"])
    if watch is not None:
        if watch.get("level") not in ("elevated", "strong"):
            raise ValueError("unknown watch level")
        parse_time(watch.get("observed_at"))
        parse_time(watch.get("expires_at"))
        if not isinstance(watch.get("source"), dict) or not isinstance(watch.get("text"), str):
            raise ValueError("invalid watch source or text")

    if not state["initialized"]:
        if latest is not None:
            remember(state, "latest:" + latest["id"], latest["reset_type"])
        state["initialized"] = True
    seen = state["seen"]
    events = []

    if scheduled is not None:
        when = scheduled["scheduled_for"]
        key = "scheduled:" + scheduled["id"] + ":" + (when or "unknown")
        if reset_is_new(state, key, scheduled["reset_type"]):
            message = format_time(when, display_timezone) if when else "시각 미정"
            if scheduled["reset_type"] == "banked":
                message += " (리셋권)"
            events.append((key, "Codex Reset", message))

    if watch is not None and parse_time(watch["expires_at"]) > now:
        source = watch["source"].get("url") or watch["text"] or "unknown"
        key = "watch:" + str(source) + ":" + watch["level"]
        if key not in seen:
            events.append((key, "Codex Reset", "시각 미정 (가능성)"))

    if latest is not None:
        key = "latest:" + latest["id"]
        if reset_is_new(state, key, latest["reset_type"]):
            label = "리셋권 확인" if latest["reset_type"] == "banked" else "확인"
            message = format_time(latest["announced_at"], display_timezone) + " (" + label + ")"
            events.append((key, "Codex Reset", message))
    return events


def load_state(state_file):
    if not state_file.exists():
        return {"initialized": False, "seen": [], "failures": 0, "failure_notified": False, "signal_types": {}}
    with state_file.open(encoding="utf-8") as source:
        state = json.load(source)
    if (
        not isinstance(state, dict)
        or not isinstance(state.get("initialized"), bool)
        or not isinstance(state.get("seen"), list)
        or not all(isinstance(item, str) for item in state["seen"])
    ):
        raise ValueError("invalid state file")
    state.setdefault("failures", 0)
    state.setdefault("failure_notified", False)
    state.setdefault("signal_types", {})
    if (
        isinstance(state["failures"], bool)
        or not isinstance(state["failures"], int)
        or state["failures"] < 0
        or not isinstance(state["failure_notified"], bool)
    ):
        raise ValueError("invalid failure state")
    if not isinstance(state["signal_types"], dict) or not all(
        isinstance(key, str) and value in ("regular", "banked") for key, value in state["signal_types"].items()
    ):
        raise ValueError("invalid signal type state")
    return state


def save_state(state_file, state):
    temp_name = None
    try:
        with tempfile.NamedTemporaryFile(
            mode="w", encoding="utf-8", dir=str(state_file.parent), prefix=".state-", delete=False
        ) as destination:
            temp_name = destination.name
            os.fchmod(destination.fileno(), 0o600)
            json.dump(state, destination, ensure_ascii=False, indent=2)
            destination.write("\n")
        os.replace(temp_name, state_file)
    finally:
        if temp_name and os.path.exists(temp_name):
            os.unlink(temp_name)


def notify(title, message):
    # Arguments are separate from the AppleScript source; remote text is never code.
    subprocess.run(
        ["/usr/bin/osascript", "-", title, message],
        input=APPLE_SCRIPT,
        text=True,
        check=True,
        capture_output=True,
        timeout=20,
    )


def setup_logging(state_dir):
    LOG.setLevel(logging.INFO)
    handler = RotatingFileHandler(
        state_dir / "monitor.log", maxBytes=262144, backupCount=2, encoding="utf-8"
    )
    handler.setFormatter(logging.Formatter("%(asctime)s %(levelname)s %(message)s"))
    LOG.addHandler(handler)
    return handler


def run_check(state_dir, display_timezone):
    state_dir.mkdir(mode=0o700, parents=True, exist_ok=True)
    handler = setup_logging(state_dir)
    try:
        with (state_dir / "monitor.lock").open("a+") as lock:
            try:
                fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
            except BlockingIOError:
                LOG.info("Skipped: another check is running")
                return 0
            try:
                state_file = state_dir / "state.json"
                state = load_state(state_file)
                try:
                    data = read_status()
                    events = events_for(data, state, datetime.now(timezone.utc), display_timezone)
                except (HTTPError, URLError, HTTPException, TimeoutError, OSError, ValueError, KeyError, TypeError) as exc:
                    state["failures"] += 1
                    LOG.warning("API check failed (%d consecutive): %s", state["failures"], exc)
                    if state["failures"] >= 3 and not state["failure_notified"]:
                        try:
                            notify("Codex 리셋 알림 확인 필요", "API를 3회 연속 확인하지 못했습니다. 연결과 로그를 확인하세요.")
                            state["failure_notified"] = True
                        except (OSError, subprocess.SubprocessError) as notify_exc:
                            LOG.error("Could not display error notification: %s", notify_exc)
                    save_state(state_file, state)
                    return 1
                if state["failure_notified"]:
                    notify("Codex 리셋 알림 복구", "API 조회가 다시 정상 작동합니다.")
                state["failures"] = 0
                state["failure_notified"] = False
                save_state(state_file, state)
                for key, title, message in events:
                    notify(title, message)
                    if key.startswith("scheduled:"):
                        kind = data["scheduled_reset"]["reset_type"]
                    elif key.startswith("latest:"):
                        kind = data["latest_reset"]["reset_type"]
                    else:
                        kind = None
                    remember(state, key, kind)
                    save_state(state_file, state)
                    LOG.info("Notification sent: %s", title)
                LOG.info("Check succeeded; %d new notification(s)", len(events))
                print("Codex reset check succeeded; new notifications:", len(events))
                return 0
            except Exception:
                LOG.exception("Check could not finish")
                raise
    finally:
        LOG.removeHandler(handler)
        handler.close()


def absolute_path(value):
    path = Path(value).expanduser()
    if not path.is_absolute():
        raise argparse.ArgumentTypeError("use an absolute path")
    return path


def timezone_arg(value):
    try:
        return ZoneInfo(value)
    except (ZoneInfoNotFoundError, ValueError) as exc:
        raise argparse.ArgumentTypeError("use an available IANA time zone") from exc


def source_checkout():
    # Also handles worktrees where .git is a file rather than a directory.
    for parent in Path(__file__).resolve().parents:
        if (parent / ".git").exists():
            return parent
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--state-dir", type=absolute_path, help="dedicated runtime directory outside the checkout")
    parser.add_argument("--timezone", type=timezone_arg, help="IANA time zone; defaults to the system's local zone")
    parser.add_argument("--test", action="store_true", help="send a simulated macOS notification without fetching data")
    args = parser.parse_args()
    if args.test:
        example = datetime.now(timezone.utc) + timedelta(hours=2)
        notify("Codex Reset", format_time(example.isoformat(), args.timezone))
        print("Test notification requested; its time is an example, not a real reset.")
        return 0
    if args.state_dir is None:
        parser.error("--state-dir is required unless --test is used")
    checkout = source_checkout()
    state_dir = args.state_dir.resolve()
    if checkout is not None and (state_dir == checkout or checkout in state_dir.parents):
        parser.error("--state-dir must be outside the source checkout")
    return run_check(args.state_dir, args.timezone)


if __name__ == "__main__":
    raise SystemExit(main())
