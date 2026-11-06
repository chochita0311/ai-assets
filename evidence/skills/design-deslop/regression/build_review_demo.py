"""Build a DOM-only synthetic review and verify source/snapshot geometry and styles.

Evaluation-only dependencies: Playwright and an available Chromium executable.
The runtime skill's review helper uses only Python's standard library.
"""

import argparse
import functools
import hashlib
import http.server
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import threading

from playwright.sync_api import sync_playwright


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


def shorten_header(site):
    html = site / "notebook.html"
    updated, count = re.subn(
        r'<header class="notebook-hero surface">.*?</header>',
        '<header class="notebook-hero surface"><h1>Your notebook</h1>'
        '<p>Find notes by text, category, and topic.</p></header>',
        html.read_text(), flags=re.S,
    )
    assert count == 1, "Fixture header changed; update this demo transformation."
    html.write_text(updated)
    with (site / "notebook.css").open("a") as stream:
        stream.write("\n.notebook-hero { text-align: left; background: transparent; padding: 1rem 0 1.5rem; border: 0; border-bottom: 2px solid #8b78ba; border-radius: 0; box-shadow: none; }\n.notebook-hero h1 { font-size: 2rem; }\n.notebook-hero > p { margin-bottom: 0; }\n")


def quiet_cards(site):
    script = site / "notebook.js"
    updated, count = re.subn(r'<div class="note-topline">.*?</div>', "", script.read_text())
    assert count == 1, "Fixture note decoration changed; update this transformation."
    script.write_text(updated)
    with (site / "notebook.css").open("a") as stream:
        stream.write("\n.note-card { background: white; box-shadow: none; border-radius: 8px; }\n")


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--browser", help="Installed Chrome/Chromium executable")
    parser.add_argument("--verify-raster", action="store_true",
                        help="Also require byte-identical temporary PNG captures in this browser environment")
    args = parser.parse_args()
    owner = Path(__file__).resolve().parent
    repo = owner.parents[3]
    helper = repo / "skills/design-deslop/scripts/review.py"
    snapshot_script = (repo / "skills/design-deslop/assets/snapshot.js").read_text()
    source = owner / "inputs"
    args.output.parent.mkdir(parents=True, exist_ok=True)

    with tempfile.TemporaryDirectory(prefix="design-review-demo-") as temporary:
        work = Path(temporary)
        names = ["original", "header", "cards", "rows", "header-cards", "header-rows"]
        for name in names:
            site = work / name
            shutil.copytree(source, site)
            if "rows" in name:
                subprocess.run(
                    ["patch", "-p1", "-i", str(owner / "observed/selected.patch")],
                    cwd=site, capture_output=True, check=True,
                )
            if "cards" in name:
                quiet_cards(site)
            if "header" in name:
                shorten_header(site)

        documents = {name: {} for name in names}
        snapshot_parity = []
        components = [
            {"id": "intro", "label": "도입부"},
            {"id": "note", "label": "노트 항목"},
            {"id": "notes", "label": "노트 목록"},
        ]
        selectors = {"intro": ".notebook-hero", "note": "#n1", "notes": "#note-list"}
        server = http.server.ThreadingHTTPServer(
            ("127.0.0.1", 0), functools.partial(QuietHandler, directory=str(work))
        )
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with sync_playwright() as playwright:
                browser = playwright.chromium.launch(executable_path=args.browser, headless=True)
                try:
                    for name in names:
                        for view, width, height in [("desktop", 1440, 1000), ("phone", 390, 844)]:
                            page = browser.new_page(viewport={"width": width, "height": height})
                            errors = []
                            page.on("pageerror", lambda error: errors.append(str(error)))
                            try:
                                page.goto(f"http://127.0.0.1:{server.server_port}/{name}/notebook.html", wait_until="networkidle")
                                page.evaluate("document.fonts.ready")
                                assert not errors, (name, view, errors)
                                assert page.locator("#note-list article").count() == 8
                                assert page.evaluate("document.documentElement.scrollWidth <= innerWidth")
                                image = page.screenshot(full_page=True) if args.verify_raster else None
                                for component, selector in selectors.items():
                                    box = page.locator(selector).bounding_box()
                                    assert box, (name, view, selector)
                                snapshot = page.evaluate(snapshot_script)
                                document = work / f"{name}-{view}.html"
                                document.write_text(snapshot, encoding="utf-8")
                                documents[name][view] = {"html": str(document), "selectors": dict(selectors)}
                                restored = browser.new_page(viewport={"width": width, "height": height})
                                try:
                                    restored.set_content(snapshot, wait_until="load")
                                    restored.evaluate("document.fonts.ready")
                                    for selector in selectors.values():
                                        original_box = page.locator(selector).bounding_box()
                                        restored_box = restored.locator(selector).bounding_box()
                                        assert all(abs(original_box[key] - restored_box[key]) < 0.1 for key in original_box), (name, view, selector, original_box, restored_box)
                                        assert page.locator(selector).inner_text() == restored.locator(selector).inner_text()
                                    # Compare the rendered properties that this fixture's
                                    # proposals change, including their nested text/controls.
                                    appearance = """() => [...document.querySelectorAll('header, h1, h2, h3, article, input, select, button, .tag, .note-list')].map(el => {
                                        const style = getComputedStyle(el);
                                        return Object.fromEntries(['display', 'color', 'backgroundColor', 'backgroundImage',
                                          'fontFamily', 'fontSize', 'fontWeight', 'lineHeight', 'letterSpacing',
                                          'textAlign', 'padding', 'margin', 'borderRadius', 'borderColor', 'borderWidth',
                                          'boxShadow', 'gap', 'gridTemplateColumns'].map(key => [key, style[key]]));
                                    })"""
                                    assert page.evaluate(appearance) == restored.evaluate(appearance), (name, view, "DOM snapshot styles differ")
                                    if args.verify_raster:
                                        assert restored.screenshot(full_page=True) == image, (name, view, "Strict PNG parity differs in this environment")
                                    snapshot_parity.append(f"{name}/{view}")
                                finally:
                                    restored.close()
                            finally:
                                page.close()
                finally:
                    browser.close()
        finally:
            server.shutdown()
            server.server_close()
            thread.join()

        def proposal(key, group, title, observation, benefit, tradeoff, question, image_set, scope):
            affected = ["intro"] if image_set == "header" else ["note", "notes"]
            return {
                "id": key, "group": group, "title": title,
                "observation": observation, "benefit": benefit, "tradeoff": tradeoff,
                "question": question, "scope": scope,
                "preserved": ["노트 8개와 분류·태그·날짜", "검색·정렬과 독립된 읽기 체크리스트"],
                "checks": ["실제 Chrome에서 데스크톱·휴대폰 DOM 비교", "초기 노트 수와 가로 넘침 확인; 사용자 성과는 미측정"],
                "requires": [], "conflicts": [], "evidence": "rendered",
                "components": affected,
                "documents": {
                    view: {"html": document["html"], "selectors": {cid: selectors[cid] for cid in affected}}
                    for view, document in documents[image_set].items()
                },
            }

        manifest = {
            "version": 1, "review_id": "fieldbook-dom-review-demo", "round": 4,
            "language": "ko", "stage": "proposal", "title": "Fieldbook · 디자인 변경 검토",
            "summary": "변경안마다 전체 채택·일부 차용·제외를 선택하고, 의견을 대화로 전달합니다. 선택 조합은 전체 채택한 항목의 통합 화면입니다.",
            "components": components,
            "baseline": {
                "label": "현재 화면",
                "description": "가상 Fieldbook의 기본 목록. 같은 데이터·테마·뷰포트의 DOM으로 비교합니다.",
                "files": {name: hashlib.sha256((source / name).read_bytes()).hexdigest() for name in ["notebook.html", "notebook.css", "notebook.js", "tokens.css", "DESIGN.md"]},
            },
            "views": [
                {"id": view, "label": label, "width": width, "height": height,
                 "conditions": "/notebook.html · 기본 목록 · 밝은 테마 · 필터 없음 · 접힌 본문",
                 "document": documents["original"][view]}
                for view, label, width, height in [("desktop", "데스크톱", 1440, 1000), ("phone", "휴대폰", 390, 844)]
            ],
            "proposals": [
                proposal("N01", "header", "도입부를 짧게", "큰 홍보 문구와 배지가 노트보다 먼저 보입니다.", "목록에 더 일찍 도달할 수 있는 구성입니다.", "홍보성 분위기는 줄어듭니다.", "이 노트장에는 짧은 안내가 더 어울리나요?", "header", ["notebook.html: 도입부", "notebook.css: 도입부 스타일"]),
                proposal("N02-A", "notes", "카드를 유지하며 장식 줄이기", "모든 노트에 같은 별과 문구가 반복됩니다.", "각 노트 제목이 먼저 보입니다.", "기존 장식의 따뜻한 느낌은 줄어듭니다.", "노트를 카드 단위로 구분하는 편이 좋은가요?", "cards", ["notebook.js: 노트 표현", "notebook.css: 카드 스타일"]),
                proposal("N02-B", "notes", "노트를 정렬된 행으로", "두 열 카드에서 제목과 날짜 위치가 반복해서 바뀝니다.", "제목·분류·날짜를 일정한 축으로 비교할 수 있습니다.", "개별 카드의 구분감이 줄며, 데스크톱에서 더 촘촘하다는 뜻은 아닙니다.", "카드의 독립성보다 행의 정렬이 더 유용한가요?", "rows", ["notebook.html: 노트 목록", "notebook.js: 노트 표현", "notebook.css: 목록 스타일"]),
            ],
            "combinations": [
                {"id": "C-A", "proposals": ["N01", "N02-A"], "evidence": "rendered", "documents": documents["header-cards"]},
                {"id": "C-B", "proposals": ["N01", "N02-B"], "evidence": "rendered", "documents": documents["header-rows"]},
            ],
            "applied": [],
        }
        manifest_path = work / "manifest.json"
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2))
        subprocess.run([sys.executable, str(helper), "build", str(manifest_path), "--output", str(args.output.resolve())], check=True)
    evidence = "geometry, text and styles" + (" plus exact PNGs" if args.verify_raster else "")
    print(f"Built {args.output}; {len(snapshot_parity)} DOM snapshots match source {evidence}; temporary sources removed.")


if __name__ == "__main__":
    main()
