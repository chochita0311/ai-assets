"""Capture two local review artifacts and compare the viewer itself.

Evaluation-only: requires Playwright and an installed Chromium browser. Pass the
preserved pre-change HTML and current HTML; the output embeds their screenshots
and works without the originals or a server. It records a local implemented
viewer change, with feedback enabled and adoption controls locked.
"""

import argparse
import hashlib
import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile

from playwright.sync_api import expect, sync_playwright


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--before-html", required=True, type=Path)
    parser.add_argument("--after-html", required=True, type=Path)
    parser.add_argument("--output", required=True, type=Path)
    parser.add_argument("--browser")
    args = parser.parse_args()
    sources = {"before": args.before_html.resolve(), "after": args.after_html.resolve()}
    if args.output.resolve() in sources.values():
        parser.error("Output must not overwrite an input review")
    owner = Path(__file__).resolve().parent
    helper = owner.parents[3] / "skills/design-deslop/scripts/review.py"
    components = [
        {"id": "canvas", "label": "비교 화면"},
        {"id": "choices", "label": "변경 목록"},
        {"id": "details", "label": "판단과 의견"},
    ]
    selectors = {"canvas": "#comparison-pair", "choices": "#proposal-list", "details": "#proposal-details"}
    captures, regions, metrics = {}, {}, {}
    with tempfile.TemporaryDirectory(prefix="viewer-review-") as temporary:
        work = Path(temporary)
        with sync_playwright() as playwright:
            browser = playwright.chromium.launch(executable_path=args.browser, headless=True)
            try:
                for side, source in sources.items():
                    captures[side], regions[side], metrics[side] = {}, {}, {}
                    for vid, width, height in [("desktop", 1440, 1000), ("phone", 390, 844)]:
                        page = browser.new_page(viewport={"width": width, "height": height}, device_scale_factor=1)
                        errors = []
                        page.on("pageerror", lambda error: errors.append(str(error)))
                        try:
                            page.goto(source.as_uri())
                            page.locator('button[data-proposal-id="N02-A"][data-action="preview"]').click()
                            if vid == "phone":
                                page.locator("#view-select").select_option("phone")
                            expect(page.locator("#before-image")).to_be_visible()
                            expect(page.locator("#after-image")).to_be_visible()
                            page.evaluate("() => { document.activeElement.blur(); window.scrollTo(0, 0); }")
                            page.evaluate("() => new Promise(requestAnimationFrame)")
                            assert not errors, errors
                            assert page.evaluate("() => document.documentElement.scrollWidth <= innerWidth")
                            path = work / f"{side}-{vid}.png"
                            page.screenshot(path=str(path), full_page=True)
                            captures[side][vid] = str(path)
                            regions[side][vid] = {}
                            for cid, selector in selectors.items():
                                box = page.locator(selector).bounding_box()
                                assert box, (side, vid, selector)
                                x, y = math.floor(box["x"]), math.floor(box["y"])
                                regions[side][vid][cid] = {
                                    "x": x, "y": y,
                                    "width": math.ceil(box["x"] + box["width"]) - x,
                                    "height": math.ceil(box["y"] + box["height"]) - y,
                                }
                            metrics[side][vid] = {"scale": page.locator("#scale-label").inner_text(), "page_errors": errors}
                        finally:
                            page.close()
            finally:
                browser.close()
        manifest = {
            "version": 1, "review_id": "viewer-component-workspace", "round": 1,
            "language": "ko", "stage": "applied", "title": "리뷰 도구의 변경 전후",
            "summary": "로컬 개발본에 반영한 리뷰 화면을 비교합니다. 영역을 골라 살펴보고 다음 수정 의견을 남길 수 있습니다.",
            "baseline": {
                "label": "이전 리뷰 화면",
                "description": "같은 가상 노트의 N02-A 변경을 보는 두 리뷰 도구입니다. 이전 도구는 전체 화면, 새 도구는 해당 노트 항목으로 시작합니다. 이는 새 컴포넌트 탐색 기능의 차이입니다. 원본 제품 화면의 디자인 선택과 리뷰 도구 자체의 변경을 구분합니다.",
                "files": {},
            },
            "components": components,
            "views": [
                {"id": vid, "label": label, "width": width, "height": height,
                 "conditions": f"리뷰 도구 {width}×{height} · N02-A 개별 미리보기 · 수락 항목 없음 · 피드백 없음 · 같은 제품 데이터 · 실제 전체 페이지 캡처",
                 "before": captures["before"][vid], "regions": regions["before"][vid]}
                for vid, label, width, height in [("desktop", "데스크톱", 1440, 1000), ("phone", "휴대폰", 390, 844)]
            ],
            "proposals": [{
                "id": "UI01", "title": "컴포넌트를 중심으로 비교하는 작업 화면",
                "observation": "이전 도구에서는 페이지 전체가 축소되고 안내와 반복된 버튼 테두리가 비교 대상과 경쟁했습니다. 개별 컴포넌트를 직접 크게 볼 수 없었습니다.",
                "benefit": "바뀐 노트 항목을 같은 배율로 가까이 비교하고, 전체 화면으로 돌아가 주변 영향을 확인할 수 있습니다. 확장 설명은 필요할 때 열어 읽습니다.",
                "tradeoff": "상세 근거와 검증 정보는 펼쳐 확인해야 합니다. 한 항목과 목록을 함께 바꾸는 제안은 컴포넌트별로 보더라도 하나의 변경 묶음입니다.",
                "question": "변경 목록에서 원하는 부분을 찾고, 무엇을 유지할지 판단하기가 이전보다 쉬운가요?",
                "scope": ["리뷰 도구의 탐색, 비교 영역, 설명·피드백 배치", "이 시안은 연결된 하나의 도구 구성입니다. 실제 사이트나 전역 설치에는 적용하지 않았습니다."],
                "preserved": ["좌측 원본·우측 변경안의 동시 비교", "수락·거절·보류·초기화와 개별·전체 의견", "실제 조합, 원본 상태 검사, 결정 내보내기·가져오기"],
                "checks": ["같은 제품 데이터와 제안 ID로 1440px·390px 실제 Chrome 캡처", "이 캡처에서 가로 넘침과 JavaScript 오류 없음; 인간 선호나 작업 시간은 미측정"],
                "components": [item["id"] for item in components],
                "evidence": "rendered", "captures": captures["after"], "regions": regions["after"],
            }],
            "applied": ["UI01"],
        }
        manifest_path = work / "manifest.json"
        manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
        args.output.parent.mkdir(parents=True, exist_ok=True)
        subprocess.run([sys.executable, str(helper), "build", str(manifest_path), "--output", str(args.output.resolve())], check=True)
    print(json.dumps({"viewer_metrics": metrics, "input_sha256": {key: hashlib.sha256(path.read_bytes()).hexdigest() for key, path in sources.items()}}, ensure_ascii=False))


if __name__ == "__main__":
    main()
