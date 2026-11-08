"""Own the local artifact directory and its generated run catalog, never app code."""
from datetime import datetime, timezone
from html import escape
import json
from pathlib import Path
from uuid import uuid4

from atlas import ID, STATUSES, read_json, require

SCHEMA = "ui-atlas.workspace/v1"


def initialize(source_root, location=None):
    root = Path(location or Path(source_root) / ".artifacts" / "ui-atlas").resolve()
    marker = root / "workspace.json"
    if root.exists() and any(root.iterdir()):
        require(marker.is_file() and read_json(marker).get("schema") == SCHEMA,
                f"Nonempty location is not an owned UI Atlas workspace: {root}")
    root.mkdir(parents=True, exist_ok=True)
    if not marker.exists():
        # Ignore observations before creating them. This does not untrack files
        # already committed, or authorize publishing recipes/data by force-add.
        (root / ".gitignore").write_text("*\n", encoding="utf-8")
        marker.write_text(json.dumps({"schema": SCHEMA}) + "\n", encoding="utf-8")
    require((root / ".gitignore").is_file(), "Workspace ignore file is missing; restore its local-only policy before capturing")
    for name in ("recipes", "runs", "notes", "tmp"):
        (root / name).mkdir(exist_ok=True)
    return root


def reserve(root, atlas_id):
    require(ID.fullmatch(atlas_id) is not None, "Invalid atlas ID")
    stamp = datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%S.%fZ")
    run = root / "runs" / f"{stamp}-{atlas_id}-{uuid4().hex[:8]}"
    run.mkdir()
    return run


def catalog(root):
    root = Path(root).resolve()
    require(read_json(root / "workspace.json").get("schema") == SCHEMA, "Not a UI Atlas workspace")
    groups, unfinished, unreadable = {}, [], []
    for run in sorted((root / "runs").iterdir(), reverse=True):
        if not run.is_dir():
            continue
        if not (run / "atlas.json").is_file() or not (run / "index.html").is_file():
            unfinished.append(run.name)
            continue
        try:
            data = read_json(run / "atlas.json")
            require(isinstance(data, dict) and isinstance(data.get("id"), str)
                    and ID.fullmatch(data["id"]), "Invalid atlas ID")
            require(isinstance(data.get("title"), str) and data["title"], "Missing title")
            require(isinstance(data.get("frames"), list) and data["frames"]
                    and all(isinstance(frame, dict) and frame.get("status") in STATUSES for frame in data["frames"]),
                    "Invalid frame status list")
            require(isinstance(data.get("journey_failures", []), list)
                    and isinstance(data.get("freshness", {}), dict), "Invalid run status")
            require(isinstance(data.get("freshness", {}).get("status", ""), str), "Invalid freshness status")
        except (OSError, ValueError, TypeError) as error:
            unreadable.append((run.name, str(error)))
            continue
        rendered = sum(frame["status"] == "rendered" for frame in data["frames"])
        failed = sum(frame["status"] == "render-failed" for frame in data["frames"])
        gaps = sum(frame["status"] not in ("rendered", "render-failed") for frame in data["frames"])
        incomplete = failed or data.get("journey_failures")
        status = "일부 실패" if incomplete else "실행 완료"
        freshness = {"matched": "생성 시 소스 일치", "changed": "소스 변경 · 갱신 필요", "unavailable": "소스 확인 불가"}.get(
            data.get("freshness", {}).get("status"), "생성 시 소스 검사 기록 없음")
        entry = (f'<a href="runs/{escape(run.name, quote=True)}/index.html">{escape(data["title"])}</a>'
                 f'<span>{status} · {rendered}개 장면 · 실패 {failed} · 범위 확인 {gaps}</span>'
                 f'<span>{freshness}</span>'
                 f'<small>{escape(run.name)}</small>')
        groups.setdefault(data["id"], []).append(entry)
    sections = []
    for atlas_id, entries in groups.items():
        history = '<details><summary>이전 실행</summary><ul>' + ''.join('<li>' + item + '</li>' for item in entries[1:]) + '</ul></details>' if len(entries) > 1 else ''
        sections.append(f'<section><h2>{escape(atlas_id)}</h2><p class="label">최근 열 수 있는 실행</p><div>{entries[0]}</div>{history}</section>')
    pending = ''.join('<li>' + escape(name) + '</li>' for name in unfinished)
    html = '''<!doctype html><html lang="ko"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1">
<title>UI Atlas</title><style>
body{font:14px/1.6 system-ui,sans-serif;background:#f4f4f6;color:#29292e;max-width:900px;margin:48px auto;padding:0 24px}
h1{font-size:24px}h2{font-size:16px}section{background:white;padding:20px 24px;margin:18px 0;border:1px solid #e5e5eb;border-radius:10px}
a{color:#6542cf}span,small{display:block}small,.label{color:#72727c;font-size:12px}details{margin-top:16px}li{margin:12px 0;list-style:none}summary{cursor:pointer}
</style><h1>UI Atlas</h1><p>최신 관찰과 이전 실행. 범위 확인에는 미확인·미구현·해당 없음 상태가 포함됩니다. 실행 완료는 앱 전체 검증을 뜻하지 않습니다.</p>'''
    html += ''.join(sections) or '<p>아직 생성된 전개도가 없습니다.</p>'
    if pending:
        html += '<section><h2>생성 중 또는 중단된 실행</h2><ul>' + pending + '</ul></section>'
    if unreadable:
        html += '<section><h2>읽을 수 없는 실행</h2><p>원본 파일은 보존했습니다. 다른 실행은 계속 열거나 생성할 수 있습니다.</p><ul>'
        html += ''.join('<li>' + escape(name) + '<small>' + escape(reason) + '</small></li>' for name, reason in unreadable)
        html += '</ul></section>'
    # Unique staging supports simultaneous writers without sharing a temp file.
    # A catalog refresh can always reconstruct the entry from retained runs.
    temporary = root / "tmp" / ("catalog-" + uuid4().hex + ".html")
    try:
        temporary.write_text(html, encoding="utf-8")
        temporary.replace(root / "index.html")
    finally:
        temporary.unlink(missing_ok=True)
    return root / "index.html"
