"""Own the local artifact directory and its generated run catalog, never app code."""
from datetime import datetime, timezone
from html import escape
import json
from pathlib import Path
from uuid import uuid4
from urllib.parse import quote

from atlas import ASSETS, ID, STATUSES, read_json, require

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
        entry = {"key": run.name, "url": f"runs/{quote(run.name, safe='')}/index.html",
                 "title": data["title"], "status": status, "rendered": rendered,
                 "failed": failed, "gaps": gaps, "freshness": freshness}
        groups.setdefault(data["id"], []).append(entry)

    def entry_html(entry):
        return (f'<a href="{escape(entry["url"], quote=True)}">{escape(entry["title"])}</a>'
                f'<span>{entry["status"]} · {entry["rendered"]}개 장면 · 실패 {entry["failed"]} · 범위 확인 {entry["gaps"]}</span>'
                f'<span>{entry["freshness"]}</span><small>{escape(entry["key"])}</small>')

    sections = []
    for atlas_id, entries in groups.items():
        history = '<details><summary>이전 실행</summary><ul>' + ''.join('<li>' + entry_html(item) + '</li>' for item in entries[1:]) + '</ul></details>' if len(entries) > 1 else ''
        sections.append(f'<section><h2>{escape(atlas_id)}</h2><p class="label">최근 열 수 있는 실행</p><div>{entry_html(entries[0])}</div>{history}</section>')
    pending = ''.join('<li>' + escape(name) + '</li>' for name in unfinished)
    catalog_html = ''.join(sections) or '<p>아직 생성된 전개도가 없습니다.</p>'
    if pending:
        catalog_html += '<section><h2>생성 중 또는 중단된 실행</h2><ul>' + pending + '</ul></section>'
    if unreadable:
        catalog_html += '<section><h2>읽을 수 없는 실행</h2><p>원본 파일은 보존했습니다. 다른 실행은 계속 열거나 생성할 수 있습니다.</p><ul>'
        catalog_html += ''.join('<li>' + escape(name) + '<small>' + escape(reason) + '</small></li>' for name, reason in unreadable)
        catalog_html += '</ul></section>'
    payload = json.dumps({"groups": [{"id": key, "runs": entries} for key, entries in groups.items()],
                          "unfinished": unfinished,
                          "unreadable": [{"name": name, "reason": reason} for name, reason in unreadable]},
                         ensure_ascii=False).replace('<', '\\u003c').replace('\u2028', '\\u2028').replace('\u2029', '\\u2029')
    html = (ASSETS / 'workspace.html').read_text(encoding='utf-8')
    html = html.replace('ATLAS_CATALOG', catalog_html).replace('WORKSPACE_PAYLOAD', payload)
    html = html.replace('/* ATLAS_WORKSPACE */', (ASSETS / 'workspace.js').read_text(encoding='utf-8'))
    # Unique staging supports simultaneous writers without sharing a temp file.
    # A catalog refresh can always reconstruct the entry from retained runs.
    temporary = root / "tmp" / ("catalog-" + uuid4().hex + ".html")
    try:
        temporary.write_text(html, encoding="utf-8")
        temporary.replace(root / "index.html")
    finally:
        temporary.unlink(missing_ok=True)
    return root / "index.html"
