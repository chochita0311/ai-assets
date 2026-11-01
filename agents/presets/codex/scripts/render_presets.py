#!/usr/bin/env python3
"""Render all or selected prompt presets without writing local configuration."""

import argparse
import json
from pathlib import Path
import re
import sys


PACKAGE_DIR = Path(__file__).resolve().parents[1]


def _unique_object(pairs):
    result = {}
    for key, value in pairs:
        if key in result:
            raise ValueError(f"duplicate catalog key: {key}")
        result[key] = value
    return result


def _toml_string(value):
    # JSON string escapes also work in TOML; DEL must additionally be escaped.
    return json.dumps(value, ensure_ascii=False).replace("\x7f", "\\u007f")


def render_presets(package_dir, numbers):
    """Validate a selection completely, then return its lossless TOML fragment."""
    package_dir = package_dir.resolve()
    catalog = json.loads(
        (package_dir / "catalog.json").read_text(encoding="utf-8"),
        object_pairs_hook=_unique_object,
    )
    if not isinstance(catalog, dict) or not catalog:
        raise ValueError("catalog must be a nonempty object")
    if any(not re.fullmatch(r"[1-9][0-9]*", key) for key in catalog):
        raise ValueError("catalog numbers must be positive decimals without leading zeroes")

    selected = list(dict.fromkeys(numbers)) if numbers else sorted(catalog, key=int)
    unknown = [number for number in selected if number not in catalog]
    if unknown:
        raise ValueError(f"unknown preset numbers: {', '.join(unknown)}")

    fragments = []
    for number in selected:
        entry = catalog[number]
        if not isinstance(entry, dict) or set(entry) != {"label", "prompt_file"}:
            raise ValueError(f"preset {number} must contain label and prompt_file")
        label, filename = entry["label"], entry["prompt_file"]
        if not isinstance(label, str) or not label.strip():
            raise ValueError(f"preset {number} must have a nonempty label")
        if not isinstance(filename, str) or not filename:
            raise ValueError(f"preset {number} must have a prompt_file path")
        prompt_path = (package_dir / filename).resolve()
        if not prompt_path.is_relative_to(package_dir) or prompt_path.suffix != ".md":
            raise ValueError(f"preset {number} prompt_file must be Markdown inside this package")
        prompt = prompt_path.read_bytes().decode("utf-8")
        if not prompt.strip():
            raise ValueError(f"preset {number} prompt must not be empty")
        fragments.append(
            f"[tui.presets.{number}]\n"
            f"label = {_toml_string(label)}\n"
            f"input = {_toml_string(prompt)}\n"
        )
    return "\n".join(fragments)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("numbers", nargs="*", metavar="NUMBER", help="catalog numbers; default: all")
    args = parser.parse_args()
    try:
        fragment = render_presets(PACKAGE_DIR, args.numbers)
    except (OSError, UnicodeError, ValueError) as exc:
        parser.error(str(exc))
    sys.stdout.buffer.write(fragment.encode("utf-8"))


if __name__ == "__main__":
    main()
