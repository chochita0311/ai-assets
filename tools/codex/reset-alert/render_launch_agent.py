#!/usr/bin/env python3
"""Render, but do not install or load, a macOS hourly LaunchAgent."""

import argparse
import os
from pathlib import Path
import plistlib
import re
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


def absolute_path(value):
    path = Path(value).expanduser()
    if not path.is_absolute():
        raise argparse.ArgumentTypeError("use an absolute path")
    return path


def timezone_arg(value):
    try:
        ZoneInfo(value)
    except (ZoneInfoNotFoundError, ValueError) as exc:
        raise argparse.ArgumentTypeError("use an available IANA time zone") from exc
    return value


def make_job(label, python, monitor, state_dir, display_timezone=None):
    arguments = [str(python), "-B", str(monitor), "--state-dir", str(state_dir)]
    if display_timezone:
        arguments.extend(["--timezone", display_timezone])
    return {
        "Label": label,
        "ProgramArguments": arguments,
        "StartCalendarInterval": {"Minute": 0},
    }


def source_checkout(path):
    # Also handles worktrees where .git is a file rather than a directory.
    for parent in path.resolve().parents:
        if (parent / ".git").exists():
            return parent
    return None


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--python", type=absolute_path, required=True)
    parser.add_argument("--monitor", type=absolute_path, default=Path(__file__).resolve().with_name("reset_alert.py"))
    parser.add_argument("--state-dir", type=absolute_path, required=True)
    parser.add_argument("--timezone", type=timezone_arg, help="IANA display time zone; defaults to system local time")
    parser.add_argument("--label", default="local.codex-reset-alert")
    parser.add_argument("--output", type=absolute_path, required=True)
    args = parser.parse_args()

    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", args.label):
        parser.error("label must contain only letters, digits, dots, underscores, or hyphens")
    if not args.python.is_file() or not os.access(args.python, os.X_OK):
        parser.error("--python must be an existing executable")
    if not args.monitor.is_file():
        parser.error("--monitor must be an existing file")
    if args.state_dir.exists() and not args.state_dir.is_dir():
        parser.error("--state-dir must be a directory")
    checkouts = {source_checkout(Path(__file__)), source_checkout(args.monitor)} - {None}
    for checkout in checkouts:
        for label, path in (("--output", args.output), ("--state-dir", args.state_dir)):
            resolved = path.resolve()
            if resolved == checkout or checkout in resolved.parents:
                parser.error(label + " must be outside the renderer and monitor source checkouts")

    job = make_job(args.label, args.python, args.monitor, args.state_dir, args.timezone)
    try:
        with args.output.open("xb") as destination:
            plistlib.dump(job, destination, sort_keys=False)
    except OSError as error:
        parser.exit(1, f"Cannot create LaunchAgent: {error}\n")
    print(f"Rendered only; not installed or loaded: {args.output}")


if __name__ == "__main__":
    main()
