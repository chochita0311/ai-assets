#!/usr/bin/env python3
"""Build a portable design review and validate submitted decision receipts.

Python 3.9+; standard library only. Neither command applies design changes.
"""

from __future__ import annotations

import argparse
import base64
import binascii
from datetime import datetime
import hashlib
from html.parser import HTMLParser
import json
import math
from pathlib import Path
import re
import struct
import sys
from typing import Any, Callable, Optional
from urllib.parse import unquote_to_bytes, urlsplit
import zlib


MARKER = "__REVIEW_DATA__"
DOM_MARKER = "__DOM_PREVIEW__"
DATA_PREFIX = "data:image/png;base64,"
IDENTIFIER = re.compile(r"[A-Za-z0-9_-]+\Z")
SHA256 = re.compile(r"[0-9a-f]{64}\Z")
TEMPLATE_PATH = Path(__file__).resolve().parent.parent / "assets" / "review.html"
DOM_PREVIEW_PATH = TEMPLATE_PATH.with_name("dom-preview.js")


class ReviewError(ValueError):
    """An input cannot safely represent the requested review or decision."""


def fail(message: str) -> None:
    raise ReviewError(message)


def object_fields(value: Any, label: str, required: set, optional: set = frozenset()) -> dict:
    if not isinstance(value, dict):
        fail(f"{label} must be an object")
    missing, extra = required - value.keys(), value.keys() - required - optional
    if missing:
        fail(f"{label} is missing fields: {', '.join(sorted(missing))}")
    if extra:
        fail(f"{label} has unknown fields: {', '.join(sorted(extra))}")
    return value


def text(value: Any, label: str, allow_empty: bool = False) -> str:
    if not isinstance(value, str) or (not allow_empty and not value.strip()):
        fail(f"{label} must be {'a' if allow_empty else 'a nonempty'} string")
    return value


def identifier(value: Any, label: str) -> str:
    if not isinstance(value, str) or not IDENTIFIER.fullmatch(value):
        fail(f"{label} must contain only letters, digits, hyphens and underscores")
    return value


def integer(value: Any, label: str, minimum: int = 1) -> int:
    if type(value) is not int or value < minimum:
        fail(f"{label} must be an integer >= {minimum}")
    return value


def choice(value: Any, label: str, choices: set) -> str:
    if not isinstance(value, str) or value not in choices:
        fail(f"{label} must be one of: {', '.join(sorted(choices))}")
    return value


def array(value: Any, label: str) -> list:
    if not isinstance(value, list):
        fail(f"{label} must be an array")
    return value


def string_list(value: Any, label: str, ids: bool = False) -> list:
    validator = identifier if ids else text
    result = [validator(item, f"{label}[{i}]") for i, item in enumerate(array(value, label))]
    if ids and len(result) != len(set(result)):
        fail(f"{label} contains duplicate IDs")
    return result


def source_path(value: Any, label: str) -> str:
    path = text(value, label)
    if "\\" in path or "\x00" in path or any(part in {"", ".", ".."} for part in path.split("/")):
        fail(f"{label} must be a relative POSIX path without traversal: {path!r}")
    # A drive prefix is not relative on Windows, even when authored on POSIX.
    if re.match(r"^[A-Za-z]:", path):
        fail(f"{label} must not have a drive prefix: {path!r}")
    return path


def canonical_json(value: Any) -> str:
    return json.dumps(value, sort_keys=True, separators=(",", ":"), ensure_ascii=True, allow_nan=False)


def parse_json(data: str, label: str) -> Any:
    def unique_object(pairs: list) -> dict:
        result = {}
        for key, value in pairs:
            if key in result:
                fail(f"{label} contains duplicate object key {key!r}")
            result[key] = value
        return result

    def invalid_constant(value: str) -> None:
        fail(f"{label} contains invalid JSON number {value}")

    try:
        return json.loads(data, object_pairs_hook=unique_object, parse_constant=invalid_constant)
    except (json.JSONDecodeError, RecursionError) as exc:
        fail(f"{label} is not valid JSON: {exc}")


def read_utf8(path: Path, label: str) -> str:
    try:
        return path.read_bytes().decode("utf-8")
    except (OSError, UnicodeError) as exc:
        fail(f"Cannot read {label} {str(path)!r}: {exc}")


def png_dimensions(data: bytes, label: str) -> tuple:
    """Check PNG structure, CRCs and scanline data without a raster dependency."""
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        fail(f"{label} is not a PNG image")
    offset, dimensions, palette = 8, None, None
    idat, ended_idat, finished = [], False, False
    while offset < len(data):
        if offset + 12 > len(data):
            fail(f"{label} has a truncated PNG chunk")
        length = struct.unpack_from(">I", data, offset)[0]
        tag = data[offset + 4:offset + 8]
        end = offset + 12 + length
        if length > 0x7FFFFFFF or end > len(data) or not re.fullmatch(rb"[A-Za-z]{4}", tag):
            fail(f"{label} has an invalid PNG chunk")
        chunk = data[offset + 8:end - 4]
        crc = struct.unpack_from(">I", data, end - 4)[0]
        if binascii.crc32(tag + chunk) & 0xFFFFFFFF != crc:
            fail(f"{label} has a PNG checksum error in {tag.decode('ascii')}")
        if dimensions is None and tag != b"IHDR":
            fail(f"{label} must start with a PNG IHDR chunk")
        if tag == b"IHDR":
            if dimensions is not None or length != 13:
                fail(f"{label} has an invalid PNG IHDR chunk")
            width, height, depth, color, compression, filtering, interlace = struct.unpack(">IIBBBBB", chunk)
            valid_depths = {0: {1, 2, 4, 8, 16}, 2: {8, 16}, 3: {1, 2, 4, 8}, 4: {8, 16}, 6: {8, 16}}
            if not (0 < width <= 0x7FFFFFFF and 0 < height <= 0x7FFFFFFF):
                fail(f"{label} has invalid PNG dimensions")
            if depth not in valid_depths.get(color, set()) or compression or filtering or interlace not in {0, 1}:
                fail(f"{label} has unsupported or invalid PNG image metadata")
            dimensions = width, height
        elif tag == b"PLTE":
            if palette is not None or idat or not length or length % 3 or length > 768 or color in {0, 4}:
                fail(f"{label} has an invalid PNG palette")
            palette = length // 3
        elif tag == b"IDAT":
            if ended_idat:
                fail(f"{label} has nonconsecutive PNG image chunks")
            idat.append(chunk)
        elif tag == b"IEND":
            if length or not idat or end != len(data):
                fail(f"{label} has an invalid PNG end chunk")
            finished = True
            break
        elif tag[0] < 97:
            fail(f"{label} contains an unknown critical PNG chunk")
        if idat and tag != b"IDAT":
            ended_idat = True
        offset = end
    if not finished or dimensions is None:
        fail(f"{label} is an incomplete PNG image")
    if color == 3 and (palette is None or palette > 2 ** depth):
        fail(f"{label} has no valid indexed PNG palette")

    channels = {0: 1, 2: 3, 3: 1, 4: 2, 6: 4}[color]
    passes = [(0, 0, 1, 1)] if interlace == 0 else [
        (0, 0, 8, 8), (4, 0, 8, 8), (0, 4, 4, 8), (2, 0, 4, 4),
        (0, 2, 2, 4), (1, 0, 2, 2), (0, 1, 1, 2),
    ]
    rows = []
    for x, y, dx, dy in passes:
        columns = max(0, (width - x + dx - 1) // dx)
        count = max(0, (height - y + dy - 1) // dy)
        if columns and count:
            rows.append(((columns * channels * depth + 7) // 8 + 1, count))
    expected = sum(stride * count for stride, count in rows)
    decompressor = zlib.decompressobj()
    consumed, next_filter, pass_index, row_index = 0, 0, 0, 0
    try:
        for compressed in idat:
            pending = compressed
            while pending:
                decoded = decompressor.decompress(pending, 65536)
                pending = decompressor.unconsumed_tail
                if decompressor.unused_data or consumed + len(decoded) > expected:
                    fail(f"{label} has excess PNG image data")
                while next_filter < consumed + len(decoded):
                    if decoded[next_filter - consumed] > 4:
                        fail(f"{label} has an invalid PNG scanline filter")
                    stride, count = rows[pass_index]
                    next_filter += stride
                    row_index += 1
                    if row_index == count:
                        pass_index += 1
                        row_index = 0
                consumed += len(decoded)
    except zlib.error as exc:
        fail(f"{label} has unreadable PNG image data: {exc}")
    if not decompressor.eof or consumed != expected:
        fail(f"{label} has incomplete PNG image data")
    return dimensions


def capture_reader(manifest_path: Path, input_paths: set) -> Callable:
    cache = {}

    def load(value: Any, width: int, label: str) -> Optional[tuple]:
        if value is None:
            return None
        path_text = text(value, label)
        try:
            parsed = urlsplit(path_text)
        except ValueError as exc:
            fail(f"{label} must be a local PNG path: {exc}")
        if parsed.scheme or parsed.netloc or "\x00" in path_text:
            fail(f"{label} must be a local PNG path, not a URL")
        try:
            path = (manifest_path.parent / path_text).resolve(strict=True)
            if not path.is_file():
                fail(f"{label} must name a PNG file: {path_text!r}")
            if path not in cache:
                data = path.read_bytes()
                dimensions = png_dimensions(data, label)
                cache[path] = (DATA_PREFIX + base64.b64encode(data).decode("ascii"), dimensions)
        except (OSError, RuntimeError) as exc:
            fail(f"Cannot read {label} {path_text!r}: {exc}")
        input_paths.add(path)
        uri, dimensions = cache[path]
        if dimensions[0] != width:
            fail(f"{label} width is {dimensions[0]}; declared view width is {width}")
        return uri, dimensions

    return load


def embedded_capture_reader() -> Callable:
    cache = {}

    def load(value: Any, width: int, label: str) -> Optional[tuple]:
        if value is None:
            return None
        if not isinstance(value, str) or not value.startswith(DATA_PREFIX):
            fail(f"{label} must be an embedded PNG data URI or null")
        if value not in cache:
            encoded = value[len(DATA_PREFIX):]
            try:
                data = base64.b64decode(encoded, validate=True)
            except (binascii.Error, ValueError) as exc:
                fail(f"{label} has invalid PNG base64: {exc}")
            if base64.b64encode(data).decode("ascii") != encoded:
                fail(f"{label} uses noncanonical PNG base64")
            cache[value] = png_dimensions(data, label)
        if cache[value][0] != width:
            fail(f"{label} width is {cache[value][0]}; declared view width is {width}")
        return value, cache[value]

    return load


def snapshot_asset(value: str, label: str) -> None:
    """Allow embedded image/font bytes and in-document SVG references only."""
    value = value.strip()
    if value.startswith("#") and len(value) > 1:
        return
    if not value.lower().startswith("data:") or "," not in value:
        fail(f"{label} must embed its asset as a data URI; external/local resource URLs are not portable")
    header, encoded = value[5:].split(",", 1)
    mime = header.split(";", 1)[0].lower()
    allowed = {"image/png", "image/jpeg", "image/webp", "image/svg+xml",
               "font/woff", "font/woff2", "font/ttf", "font/otf", "application/font-woff",
               "application/x-font-woff", "application/x-font-ttf", "application/x-font-opentype"}
    if mime not in allowed or not encoded:
        fail(f"{label} has an unsupported or empty embedded asset: {mime!r}")
    try:
        data = base64.b64decode(encoded, validate=True) if header.lower().endswith(";base64") else unquote_to_bytes(encoded)
    except (ValueError, binascii.Error) as exc:
        fail(f"{label} has invalid embedded asset data: {exc}")
    if not data:
        fail(f"{label} has an empty embedded asset")
    if mime == "image/svg+xml":
        try:
            svg = data.decode("utf-8")
        except UnicodeError as exc:
            fail(f"{label} has unreadable SVG data: {exc}")
        SnapshotHTMLParser(svg, label, svg_only=True).validate()


def snapshot_css(value: str, label: str) -> None:
    # Decode CSS escapes before checking resource-bearing tokens. This is a
    # portability boundary, not a CSS grammar/selector validator.
    value = re.sub(r"/\*.*?\*/", "", value, flags=re.S)
    value = re.sub(r"\\(?:\r\n|[\r\n\f])", "", value)

    def unescape(match: re.Match) -> str:
        if match.group(1):
            codepoint = int(match.group(1), 16)
            return chr(codepoint) if 0 < codepoint <= 0x10FFFF else "\ufffd"
        return match.group(2)

    value = re.sub(r"\\([0-9a-fA-F]{1,6})(?:\r\n|[ \t\r\n\f])?|\\([^\r\n\f])", unescape, value)
    if re.search(r"@import\b|\b(?:image-set|-webkit-image-set|paint|element|-webkit-canvas|local|expression)\s*\(", value, re.I):
        fail(f"{label} contains unsupported CSS imports, dynamic assets, or local-only font sources")
    urls = list(re.finditer(r"\burl\s*\(\s*(?:\"([^\"]*)\"|'([^']*)'|([^)]*?))\s*\)", value, re.I))
    if len(urls) != len(re.findall(r"\burl\s*\(", value, re.I)):
        fail(f"{label} contains an unparseable CSS resource URL")
    for match in urls:
        snapshot_asset(next(group for group in match.groups() if group is not None).strip(), label)


class SnapshotHTMLParser(HTMLParser):
    """Validate the deliberately bounded, inert HTML snapshot interchange."""

    VOID = {"area", "br", "col", "hr", "img", "input", "meta", "param", "source", "track", "wbr"}
    UNSUPPORTED = {"script", "iframe", "frame", "frameset", "object", "embed", "portal", "base",
                   "canvas", "video", "audio", "link", "template", "noscript", "marquee", "animate", "animatemotion",
                   "animatetransform", "set"}

    def __init__(self, document: str, label: str, svg_only: bool = False):
        super().__init__(convert_charrefs=True)
        self.document, self.label, self.svg_only = document, label, svg_only
        self.stack, self.counts, self.roots = [], {}, 0
        self.doctype_seen = False

    def handle_starttag(self, tag: str, attrs: list) -> None:
        if tag in self.UNSUPPORTED or "-" in tag:
            fail(f"{self.label} contains unsupported or active <{tag}> content")
        if len({key for key, _ in attrs}) != len(attrs):
            fail(f"{self.label} has duplicate attributes on <{tag}>")
        attributes = dict(attrs)
        for name, raw_value in attrs:
            value = raw_value or ""
            if name.startswith("on") or name in {"is", "srcdoc", "action", "formaction", "ping", "autofocus",
                                                   "http-equiv", "shadowrootmode", "srcset", "imagesrcset", "xml:base", "manifest"}:
                fail(f"{self.label} contains active or unsupported attribute {name!r}")
            if name == "style":
                snapshot_css(value, f"{self.label} style")
            elif name in {"fill", "stroke", "filter", "clip-path", "mask", "cursor", "marker", "marker-start",
                          "marker-mid", "marker-end"} or re.search(r"\burl\s*\(", value, re.I):
                snapshot_css(value, f"{self.label} {name}")
            if name in {"src", "href", "xlink:href", "poster", "background", "data"}:
                snapshot_asset(value, f"{self.label} {name}")
        if tag == "style" and attributes.get("type", "text/css").lower() != "text/css":
            fail(f"{self.label} contains a non-CSS style element")
        if tag in {"html", "head", "body"}:
            self.counts[tag] = self.counts.get(tag, 0) + 1
            expected_parent = None if tag == "html" else "html"
            if (self.stack[-1] if self.stack else None) != expected_parent:
                fail(f"{self.label} has misplaced <{tag}> markup")
            if tag == "body" and self.counts.get("head") != 1:
                fail(f"{self.label} must place head before body")
        if not self.stack and tag != ("svg" if self.svg_only else "html"):
            fail(f"{self.label} must be a complete {'SVG' if self.svg_only else 'HTML'} document")
        if not self.stack:
            self.roots += 1
        if tag not in self.VOID:
            self.stack.append(tag)

    def handle_startendtag(self, tag: str, attrs: list) -> None:
        self.handle_starttag(tag, attrs)
        if tag not in self.VOID:
            self.handle_endtag(tag)

    def handle_endtag(self, tag: str) -> None:
        if not self.stack or self.stack[-1] != tag:
            fail(f"{self.label} has unbalanced markup at </{tag}>")
        self.stack.pop()

    def handle_data(self, data: str) -> None:
        if not self.stack and data.strip():
            fail(f"{self.label} contains text outside its root element")
        if self.stack and self.stack[-1] == "style":
            snapshot_css(data, f"{self.label} stylesheet")

    def handle_decl(self, decl: str) -> None:
        if decl.lower() != "doctype html" or self.svg_only or self.doctype_seen or self.roots:
            fail(f"{self.label} contains an unsupported document declaration")
        self.doctype_seen = True

    def unknown_decl(self, data: str) -> None:
        fail(f"{self.label} contains unsupported declaration markup")

    def validate(self) -> None:
        if not self.document.strip() or "\x00" in self.document:
            fail(f"{self.label} must contain nonempty, well-formed snapshot HTML")
        try:
            self.feed(self.document)
            self.close()
        except (RecursionError, AssertionError) as exc:
            fail(f"{self.label} has unreadable snapshot markup: {exc}")
        if self.stack or self.roots != 1 or (not self.svg_only and
                (not self.doctype_seen or self.counts != {"html": 1, "head": 1, "body": 1})):
            fail(f"{self.label} must contain <!doctype html> and complete, balanced html/head/body markup")


def embedded_document_reader(value: Any, label: str) -> str:
    document = text(value, label)
    SnapshotHTMLParser(document, label).validate()
    return document


def document_reader(manifest_path: Path, input_paths: set) -> Callable:
    cache = {}

    def load(value: Any, label: str) -> str:
        path_text = text(value, label)
        try:
            parsed = urlsplit(path_text)
        except ValueError as exc:
            fail(f"{label} must be a local HTML path: {exc}")
        if parsed.scheme or parsed.netloc or "\x00" in path_text:
            fail(f"{label} must be a local HTML path, not a URL")
        try:
            path = (manifest_path.parent / path_text).resolve(strict=True)
            if not path.is_file():
                fail(f"{label} must name an HTML file: {path_text!r}")
            if path not in cache:
                cache[path] = embedded_document_reader(read_utf8(path, label), label)
        except (OSError, RuntimeError) as exc:
            fail(f"Cannot read {label} {path_text!r}: {exc}")
        input_paths.add(path)
        return cache[path]

    return load


def document_descriptor(value: Any, label: str, component_ids: set, load_document: Callable) -> Optional[dict]:
    if value is None:
        return None
    descriptor = object_fields(value, label, {"html", "selectors"})
    selectors = object_fields(descriptor["selectors"], f"{label}.selectors", set(), component_ids)
    return {"html": load_document(descriptor["html"], f"{label}.html"),
            "selectors": {cid: text(selector, f"{label}.selectors.{cid}") for cid, selector in selectors.items()}}


def component_regions(value: Any, label: str, component_ids: set,
                      dimensions: Optional[tuple]) -> dict:
    mapping = object_fields(value, label, set(), component_ids)
    result = {}
    for cid, value in mapping.items():
        region_label = f"{label}.{cid}"
        if value is None:
            result[cid] = None
            continue
        rect = object_fields(value, region_label, {"x", "y", "width", "height"})
        for key, number in rect.items():
            if type(number) not in {int, float} or (type(number) is float and not math.isfinite(number)):
                fail(f"{region_label}.{key} must be a finite number")
            if number < 0 or (key in {"width", "height"} and number == 0):
                fail(f"{region_label}.{key} must be {'positive' if key in {'width', 'height'} else 'nonnegative'}")
        if dimensions is None:
            fail(f"{region_label} requires a corresponding PNG capture")
        width, height = dimensions
        # Check individual bounds first so arbitrarily large JSON integers do
        # not overflow when mixed with floating-point coordinates in the sums.
        if (rect["x"] > width or rect["width"] > width or rect["y"] > height or rect["height"] > height
                or rect["x"] + rect["width"] > width or rect["y"] + rect["height"] > height):
            fail(f"{region_label} exceeds the actual PNG bounds {width} x {height}")
        result[cid] = dict(rect)
    return result


def selection_errors(payload: dict, selected: list) -> list:
    proposals = {item["id"]: item for item in payload["proposals"]}
    chosen, groups, problems = set(selected), {}, []
    for pid in selected:
        proposal = proposals[pid]
        group = proposal["group"]
        if group in groups:
            problems.append(f"{pid} and {groups[group]} are alternatives in group {group}")
        groups[group] = pid
        for required in proposal["requires"]:
            if required not in chosen:
                problems.append(f"{pid} requires {required}")
        for conflict in proposal["conflicts"]:
            if conflict in chosen:
                problems.append(f"{pid} conflicts with {conflict}")
    return problems


def exact_preview(payload: dict, selected: list, preview_id: Any = None) -> Optional[dict]:
    candidates = payload["proposals"] + payload["combinations"]
    for item in candidates:
        members = item.get("proposals", [item["id"]])
        if set(members) == set(selected) and (preview_id is None or item["id"] == preview_id):
            return item
    return None


def rendered_errors(payload: dict, preview: Optional[dict]) -> list:
    problems = []
    # An explicitly declared DOM descriptor is authoritative, including null.
    for view in payload["views"]:
        if "document" in view:
            if view["document"] is None:
                problems.append(f"baseline DOM document is missing for view {view['id']}")
        elif view["before"] is None:
            problems.append(f"baseline capture is missing for view {view['id']}")
    if preview is None:
        problems.append("there is no exact selected preview")
    else:
        if preview["evidence"] != "rendered":
            problems.append(f"preview {preview['id']} is not rendered evidence")
        documents = preview.get("documents", {})
        for vid, capture in preview["captures"].items():
            if vid in documents:
                if documents[vid] is None:
                    problems.append(f"preview {preview['id']} DOM document is missing for view {vid}")
            elif capture is None:
                problems.append(f"preview {preview['id']} capture is missing for view {vid}")
    return problems


def normalize_manifest(raw: Any, load_capture: Callable,
                       load_document: Callable = embedded_document_reader) -> dict:
    required = {"version", "review_id", "round", "title", "summary", "baseline", "views", "proposals"}
    source = object_fields(raw, "manifest", required, {"language", "stage", "combinations", "applied", "components"})
    if integer(source["version"], "version") != 1:
        fail("Unsupported manifest version; expected 1")
    payload = {
        "version": 1,
        "review_id": identifier(source["review_id"], "review_id"),
        "round": integer(source["round"], "round"),
        "language": choice(source.get("language", "en"), "language", {"en", "ko"}),
        "stage": choice(source.get("stage", "proposal"), "stage", {"proposal", "applied", "retained"}),
        "title": text(source["title"], "title"),
        "summary": text(source["summary"], "summary", allow_empty=True),
    }
    baseline = object_fields(source["baseline"], "baseline", {"label", "description", "files"})
    if not isinstance(baseline["files"], dict):
        fail("baseline.files must be an object of relative paths and SHA-256 hashes")
    files = {}
    for name, digest in baseline["files"].items():
        source_path(name, "baseline.files path")
        if not isinstance(digest, str) or not SHA256.fullmatch(digest):
            fail(f"baseline.files[{name!r}] must be a lowercase SHA-256 hash")
        files[name] = digest
    payload["baseline"] = {"label": text(baseline["label"], "baseline.label"),
                           "description": text(baseline["description"], "baseline.description"), "files": files}
    component_ids = set()
    if "components" in source:
        components = []
        for index, raw_component in enumerate(array(source["components"], "components")):
            label = f"components[{index}]"
            component = object_fields(raw_component, label, {"id", "label"})
            cid = identifier(component["id"], f"{label}.id")
            if cid in component_ids:
                fail(f"Duplicate component ID: {cid}")
            component_ids.add(cid)
            components.append({"id": cid, "label": text(component["label"], f"{label}.label")})
        payload["components"] = components

    capture_dimensions = {}

    def capture(value: Any, width: int, label: str) -> Optional[str]:
        loaded = load_capture(value, width, label)
        if loaded is None:
            return None
        uri, dimensions = loaded
        capture_dimensions[uri] = dimensions
        return uri

    views, view_ids = [], set()
    for index, raw_view in enumerate(array(source["views"], "views")):
        label = f"views[{index}]"
        view = object_fields(raw_view, label, {"id", "label", "width", "height", "conditions"}, {"before", "regions", "document"})
        vid = identifier(view["id"], f"{label}.id")
        if vid in view_ids:
            fail(f"Duplicate view ID: {vid}")
        view_ids.add(vid)
        width = integer(view["width"], f"{label}.width")
        normalized_view = {"id": vid, "label": text(view["label"], f"{label}.label"), "width": width,
                           "height": integer(view["height"], f"{label}.height"),
                           "conditions": text(view["conditions"], f"{label}.conditions"),
                           "before": capture(view.get("before"), width, f"{label}.before")}
        if "regions" in view:
            normalized_view["regions"] = component_regions(
                view["regions"], f"{label}.regions", component_ids,
                capture_dimensions.get(normalized_view["before"]))
        if "document" in view:
            normalized_view["document"] = document_descriptor(view["document"], f"{label}.document",
                                                              component_ids, load_document)
        views.append(normalized_view)
    if not views:
        fail("views must contain at least one comparison view")
    payload["views"] = views

    def captures(value: Any, label: str) -> dict:
        mapping = object_fields(value, label, view_ids)
        return {view["id"]: capture(mapping[view["id"]], view["width"], f"{label}.{view['id']}") for view in views}

    def preview_regions(value: Any, label: str, allowed_components: set, capture_map: dict) -> dict:
        mapping = object_fields(value, label, set(), view_ids)
        return {vid: component_regions(regions, f"{label}.{vid}", allowed_components,
                                       capture_dimensions.get(capture_map[vid]))
                for vid, regions in mapping.items()}

    def documents(value: Any, label: str, allowed_components: set) -> dict:
        mapping = object_fields(value, label, set(), view_ids)
        return {vid: document_descriptor(descriptor, f"{label}.{vid}", allowed_components, load_document)
                for vid, descriptor in mapping.items()}

    proposals, proposal_ids = [], set()
    required = {"id", "title", "observation", "benefit", "tradeoff", "question", "scope", "evidence"}
    optional = {"group", "requires", "conflicts", "preserved", "checks", "components", "captures", "regions", "documents"}
    for index, raw_proposal in enumerate(array(source["proposals"], "proposals")):
        label = f"proposals[{index}]"
        item = object_fields(raw_proposal, label, required, optional)
        pid = identifier(item["id"], f"{label}.id")
        if pid in proposal_ids:
            fail(f"Duplicate proposal ID: {pid}")
        proposal_ids.add(pid)
        proposal = {"id": pid, "group": identifier(item.get("group", pid), f"{label}.group")}
        for key in ("title", "observation", "benefit", "tradeoff", "question"):
            proposal[key] = text(item[key], f"{label}.{key}")
        for key in ("scope", "preserved", "checks", "requires", "conflicts"):
            proposal[key] = string_list(item.get(key, []), f"{label}.{key}", ids=key in {"requires", "conflicts"})
        proposal["evidence"] = choice(item["evidence"], f"{label}.evidence", {"rendered", "concept", "unavailable"})
        proposal["captures"] = captures(item.get("captures", dict.fromkeys(view_ids)), f"{label}.captures")
        if "components" in item:
            proposal["components"] = string_list(item["components"], f"{label}.components", ids=True)
            if not set(proposal["components"]) <= component_ids:
                fail(f"{label}.components contains unknown component IDs")
        if "regions" in item:
            proposal["regions"] = preview_regions(item["regions"], f"{label}.regions",
                                                  set(proposal.get("components", [])), proposal["captures"])
        if "documents" in item:
            proposal["documents"] = documents(item["documents"], f"{label}.documents", set(proposal.get("components", [])))
        proposals.append(proposal)
    payload["proposals"] = proposals
    by_id = {item["id"]: item for item in proposals}
    for item in proposals:
        for edge in ("requires", "conflicts"):
            for target in item[edge]:
                if target not in proposal_ids:
                    fail(f"Proposal {item['id']} {edge} unknown proposal {target}")
                if target == item["id"]:
                    fail(f"Proposal {item['id']} has a self edge in {edge}")
                if edge == "requires" and item["group"] == by_id[target]["group"]:
                    fail(f"Proposal {item['id']} requires same-group alternative {target}")
    # The explicit stack avoids a recursion limit for otherwise valid large reviews.
    closures = {}
    for pid in by_id:
        pending, visiting = [(pid, False)], set()
        while pending:
            current, returning = pending.pop()
            if current in closures:
                continue
            if returning:
                closure = {current}
                for target in by_id[current]["requires"]:
                    closure.update(closures[target])
                closures[current] = closure
                visiting.remove(current)
            else:
                if current in visiting:
                    fail(f"Dependency cycle in requires at proposal {current}")
                visiting.add(current)
                pending.append((current, True))
                pending.extend((target, False) for target in by_id[current]["requires"])
        problems = selection_errors(payload, sorted(closures[pid]))
        if problems:
            fail(f"Proposal {pid} has impossible requirements: {'; '.join(problems)}")

    combinations, combined_ids = [], set(proposal_ids)
    for index, raw_combination in enumerate(array(source.get("combinations", []), "combinations")):
        label = f"combinations[{index}]"
        item = object_fields(raw_combination, label, {"id", "proposals", "evidence"}, {"captures", "regions", "documents"})
        cid = identifier(item["id"], f"{label}.id")
        if cid in combined_ids:
            fail(f"Duplicate proposal or combination ID: {cid}")
        combined_ids.add(cid)
        members = string_list(item["proposals"], f"{label}.proposals", ids=True)
        if len(members) < 2 or not set(members) <= proposal_ids:
            fail(f"Combination {cid} must contain at least two existing proposal IDs")
        problems = selection_errors(payload, members)
        if problems:
            fail(f"Combination {cid} is impossible: {'; '.join(problems)}")
        combination = {"id": cid, "proposals": members,
                       "evidence": choice(item["evidence"], f"{label}.evidence", {"rendered", "concept", "unavailable"}),
                       "captures": captures(item.get("captures", dict.fromkeys(view_ids)), f"{label}.captures")}
        affected = {cid for pid in members for cid in by_id[pid].get("components", [])}
        if "regions" in item:
            combination["regions"] = preview_regions(item["regions"], f"{label}.regions", affected,
                                                     combination["captures"])
        if "documents" in item:
            combination["documents"] = documents(item["documents"], f"{label}.documents", affected)
        combinations.append(combination)
    payload["combinations"] = combinations
    applied = string_list(source.get("applied", []), "applied", ids=True)
    if not set(applied) <= proposal_ids:
        fail("applied contains unknown proposal IDs")
    if payload["stage"] != "applied" and applied:
        fail("applied must be empty outside the applied stage")
    if payload["stage"] == "applied":
        if not applied:
            fail("applied stage requires a nonempty applied selection")
        problems = selection_errors(payload, applied) + rendered_errors(payload, exact_preview(payload, applied))
        if problems:
            fail(f"Invalid applied selection: {'; '.join(problems)}")
    payload["applied"] = applied
    return payload


class ReviewDataParser(HTMLParser):
    """Locate the data script precisely, retaining byte-for-byte template text."""

    def __init__(self, document: str):
        super().__init__(convert_charrefs=False)
        self.document = document
        self.line_offsets = [0]
        self.line_offsets.extend(match.end() for match in re.finditer("\n", document))
        self.start = self.end = None
        self.open_data = False

    def character_offset(self) -> int:
        line, column = self.getpos()
        return self.line_offsets[line - 1] + column

    def handle_starttag(self, tag: str, attrs: list) -> None:
        matching = [value for key, value in attrs if key == "id" and value == "review-data"]
        if not matching:
            return
        if self.start is not None or tag != "script" or len({key for key, _ in attrs}) != len(attrs):
            fail("HTML must contain exactly one review-data JSON script")
        if dict(attrs).get("type") != "application/json":
            fail("review-data script must have type application/json")
        self.start = self.character_offset() + len(self.get_starttag_text())
        self.open_data = True

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self.open_data:
            self.end = self.character_offset()
            self.open_data = False

    def span(self) -> tuple:
        self.feed(self.document)
        self.close()
        if self.start is None or self.end is None or self.open_data:
            fail("HTML has no complete review-data JSON script")
        return self.start, self.end


def fingerprint(payload: dict, template: str) -> str:
    return hashlib.sha256(canonical_json(payload).encode("utf-8") + template.encode("utf-8")).hexdigest()


def build(manifest_path: Path, output_path: Path) -> dict:
    manifest_path = manifest_path.resolve()
    input_paths = {manifest_path, TEMPLATE_PATH.resolve()}
    payload = normalize_manifest(parse_json(read_utf8(manifest_path, "manifest"), "manifest"),
                                 capture_reader(manifest_path, input_paths), document_reader(manifest_path, input_paths))
    input_paths.update((manifest_path.parent / name).resolve() for name in payload["baseline"]["files"])
    template = read_utf8(TEMPLATE_PATH, "review template")
    if DOM_MARKER in template:
        if template.count(DOM_MARKER) != 1:
            fail("Review template must contain at most one DOM preview marker")
        input_paths.add(DOM_PREVIEW_PATH.resolve())
        bridge = read_utf8(DOM_PREVIEW_PATH, "DOM preview resource")
        if re.search(r"</script", bridge, re.I):
            fail("DOM preview resource contains an unsafe closing script sequence")
        template = template.replace(DOM_MARKER, bridge)
    start, end = ReviewDataParser(template).span()
    if template.count(MARKER) != 1 or template[start:end] != MARKER:
        fail("Review template must contain exactly one marker inside its review-data script")
    digest = fingerprint(payload, template)
    payload["review_fingerprint"] = digest
    embedded = canonical_json(payload).replace("&", "\\u0026").replace("<", "\\u003c").replace(">", "\\u003e")
    document = template[:start] + embedded + template[end:]
    output_path = output_path.resolve()
    if output_path in input_paths or any(output_path.exists() and path.exists() and output_path.samefile(path) for path in input_paths):
        fail("Output must not overwrite the manifest, template, capture, DOM resource or a known baseline source")
    try:
        output_path.write_bytes(document.encode("utf-8"))
    except OSError as exc:
        fail(f"Cannot write review HTML {str(output_path)!r}: {exc}")
    return {"result": "built", "output": str(output_path), "review_id": payload["review_id"],
            "round": payload["round"], "review_fingerprint": digest}


def load_review(path: Path) -> dict:
    document = read_utf8(path, "review HTML")
    start, end = ReviewDataParser(document).span()
    embedded = parse_json(document[start:end], "review-data")
    if not isinstance(embedded, dict):
        fail("review-data must be an object")
    digest = embedded.pop("review_fingerprint", None)
    if not isinstance(digest, str) or not SHA256.fullmatch(digest):
        fail("review-data has no valid review_fingerprint")
    payload = normalize_manifest(embedded, embedded_capture_reader())
    if canonical_json(payload) != canonical_json(embedded):
        fail("review-data is not a normalized manifest")
    template = document[:start] + MARKER + document[end:]
    if fingerprint(payload, template) != digest:
        fail("Review fingerprint mismatch: embedded data or viewer HTML changed")
    payload["review_fingerprint"] = digest
    return payload


def validate_receipt(raw: Any, payload: dict) -> dict:
    required = {"format", "version", "review_id", "round", "review_fingerprint", "intent",
                "preview_id", "selected", "decisions", "review_note", "exported_at"}
    receipt = object_fields(raw, "decision receipt", required)
    if receipt["format"] != "design-deslop-decisions" or type(receipt["version"]) is not int or receipt["version"] != 1:
        fail("Unsupported decision receipt format or version")
    for key in ("review_id", "round", "review_fingerprint"):
        if type(receipt[key]) is not type(payload[key]) or receipt[key] != payload[key]:
            fail(f"Decision receipt {key} does not match this review")
    choice(receipt["intent"], "intent", {"review-feedback", "apply-selected", "retain-original"})
    proposal_ids = {item["id"] for item in payload["proposals"]}
    selected = string_list(receipt["selected"], "selected", ids=True)
    if not set(selected) <= proposal_ids:
        fail("selected contains unknown proposal IDs")
    decisions = object_fields(receipt["decisions"], "decisions", proposal_ids)
    accepted = set()
    for pid, raw_decision in decisions.items():
        decision = object_fields(raw_decision, f"decisions.{pid}", {"status", "note"})
        status = choice(decision["status"], f"decisions.{pid}.status", {"pending", "accept", "reject", "defer", "revise"})
        text(decision["note"], f"decisions.{pid}.note", allow_empty=True)
        if status == "accept":
            accepted.add(pid)
    if accepted != set(selected):
        fail("selected must exactly match the accepted decision statuses")
    preview_ids = proposal_ids | {item["id"] for item in payload["combinations"]}
    if receipt["preview_id"] is not None:
        identifier(receipt["preview_id"], "preview_id")
        if receipt["preview_id"] not in preview_ids:
            fail("preview_id is unknown to this review")
    text(receipt["review_note"], "review_note", allow_empty=True)
    timestamp = text(receipt["exported_at"], "exported_at")
    try:
        if "T" not in timestamp:
            raise ValueError("must include a date and time")
        datetime.fromisoformat(timestamp.replace("Z", "+00:00"))
    except ValueError as exc:
        fail(f"exported_at must be an ISO timestamp: {exc}")
    return receipt


def check_sources(payload: dict, source_root: Optional[Path]) -> list:
    if source_root is None:
        fail("apply-selected requires --source-root")
    if not payload["baseline"]["files"]:
        fail("apply-selected requires baseline source file fingerprints")
    try:
        root = source_root.resolve(strict=True)
        if not root.is_dir():
            fail("--source-root must name a directory")
    except (OSError, RuntimeError) as exc:
        fail(f"Cannot resolve source root: {exc}")
    checked = []
    for name, expected in payload["baseline"]["files"].items():
        try:
            path = root.joinpath(*name.split("/")).resolve(strict=True)
            try:
                path.relative_to(root)
            except ValueError:
                fail(f"Source path escapes --source-root, including through a symlink: {name!r}")
            if not path.is_file():
                fail(f"Baseline source is not a regular file: {name!r}")
            digest = hashlib.sha256()
            with path.open("rb") as stream:
                for block in iter(lambda: stream.read(1024 * 1024), b""):
                    digest.update(block)
            if digest.hexdigest() != expected:
                fail(f"Stale baseline source: {name!r}; refresh the review before applying")
        except (OSError, RuntimeError) as exc:
            fail(f"Cannot read baseline source {name!r}: {exc}")
        checked.append(name)
    return checked


def check(review_path: Path, decisions_path: Path, source_root: Optional[Path]) -> dict:
    payload = load_review(review_path)
    receipt = validate_receipt(parse_json(read_utf8(decisions_path, "decision receipt"), "decision receipt"), payload)
    intent, selected = receipt["intent"], receipt["selected"]
    summary = {"result": "feedback-valid", "intent": intent, "review_id": payload["review_id"],
               "round": payload["round"], "review_fingerprint": payload["review_fingerprint"],
               "selected": selected, "source_files_checked": [],
               "notice": "Read-only validation; no source changes. A receipt is not proof of the user's submission."}
    if intent == "apply-selected":
        if payload["stage"] != "proposal":
            fail("apply-selected is allowed only in proposal stage")
        if not selected:
            fail("apply-selected requires a nonempty selection")
        if receipt["preview_id"] is None:
            fail("apply-selected requires the exact selected preview_id")
        preview = exact_preview(payload, selected, receipt["preview_id"])
        problems = selection_errors(payload, selected) + rendered_errors(payload, preview)
        if problems:
            fail(f"Selection cannot be applied: {'; '.join(problems)}")
        summary["source_files_checked"] = check_sources(payload, source_root)
        summary["result"] = "application-ready"
        summary["notice"] = "Read-only validation; nothing applied. Apply only after the user's actual submission, then recheck source freshness."
    elif intent == "retain-original":
        if selected:
            fail("retain-original requires no accepted proposals")
        if payload["stage"] != "proposal":
            fail("retain-original is an adoption action available only in proposal stage")
        summary["result"] = "retain-valid"
    return summary


def main(argv: Optional[list] = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    commands = parser.add_subparsers(dest="command", required=True)
    build_parser = commands.add_parser("build", help="Build one self-contained HTML review")
    build_parser.add_argument("manifest", type=Path)
    build_parser.add_argument("--output", required=True, type=Path)
    check_parser = commands.add_parser("check", help="Validate submitted decisions and source freshness without editing source")
    check_parser.add_argument("review_html", type=Path)
    check_parser.add_argument("decisions_json", type=Path)
    check_parser.add_argument("--source-root", type=Path, help="Required for apply-selected; current baseline source directory")
    args = parser.parse_args(argv)
    try:
        if args.command == "build":
            result = build(args.manifest, args.output)
        else:
            result = check(args.review_html, args.decisions_json, args.source_root)
    except (ReviewError, OSError, RuntimeError, UnicodeError) as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, ensure_ascii=True, sort_keys=True, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
