#!/usr/bin/env python3
"""Render a machine-local LaunchAgent; never install, load, or overwrite it."""

import argparse
import os
from pathlib import Path
import plistlib
import re


def absolute_path(value):
    path = Path(value).expanduser()
    if not path.is_absolute():
        raise argparse.ArgumentTypeError("use an absolute path")
    return path


def render(repo_root, codex_bin, codex_home, log_dir, label, exec_path):
    template = Path(__file__).resolve().parent.parent / "launchd/model-binding-audit.template.plist"
    values = {
        "@REPO_ROOT@": str(repo_root),
        "@CODEX_BIN@": str(codex_bin),
        "@CODEX_HOME@": str(codex_home),
        "@LOG_DIR@": str(log_dir),
        "@LABEL@": label,
        "@EXEC_PATH@": exec_path,
    }

    def substitute(value):
        if isinstance(value, dict):
            return {key: substitute(item) for key, item in value.items()}
        if isinstance(value, list):
            return [substitute(item) for item in value]
        if isinstance(value, str):
            return re.sub(r"@[A-Z_]+@", lambda match: values[match.group()], value)
        return value

    return substitute(plistlib.loads(template.read_bytes()))


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--repo-root", type=absolute_path, default=Path(__file__).resolve().parents[4])
    parser.add_argument("--codex-bin", type=absolute_path, required=True)
    parser.add_argument("--codex-home", type=absolute_path, required=True)
    parser.add_argument("--log-dir", type=absolute_path, required=True)
    parser.add_argument("--label", default="local.codex-model-binding-audit")
    parser.add_argument("--exec-path", default=os.environ.get("PATH", "/usr/bin:/bin"))
    parser.add_argument("--output", type=absolute_path, required=True)
    args = parser.parse_args()
    source_root = Path(__file__).resolve().parents[4]
    output = args.output.resolve()
    for checkout in (source_root, args.repo_root.resolve()):
        if output == checkout or checkout in output.parents:
            parser.error("machine-local output must be outside the source checkout")
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._-]*", args.label):
        parser.error("label must contain only letters, digits, dots, underscores, or hyphens")
    runner = args.repo_root / "agents/adapters/codex/scripts/run-model-binding-audit.sh"
    if not runner.is_file() or not args.codex_bin.is_file() or not os.access(args.codex_bin, os.X_OK):
        parser.error("repo runner and executable Codex path must exist")
    payload = plistlib.dumps(render(args.repo_root, args.codex_bin, args.codex_home,
                                   args.log_dir, args.label, args.exec_path), sort_keys=False)
    try:
        with args.output.open("xb") as destination:
            destination.write(payload)
    except OSError as error:
        parser.exit(1, f"Cannot create LaunchAgent: {error}\n")
    print(f"Rendered only; not installed or loaded: {args.output}")


if __name__ == "__main__":
    main()
