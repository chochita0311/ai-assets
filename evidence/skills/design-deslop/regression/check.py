"""Exercise the synthetic pages through a real local browser.

This is evaluation material, not a dependency of the design-deslop skill.
Selectors identify this corpus; adapt them if a valid redesign changes markup.
Passing these checks does not establish visual quality or scope isolation.
"""

import argparse
from contextlib import contextmanager
import functools
import http.server
import json
from pathlib import Path
import threading

from playwright.sync_api import sync_playwright


class QuietHandler(http.server.SimpleHTTPRequestHandler):
    def log_message(self, *_args):
        pass


@contextmanager
def serve(root):
    handler = functools.partial(QuietHandler, directory=str(root))
    server = http.server.ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        yield f"http://127.0.0.1:{server.server_port}"
    finally:
        server.shutdown()
        server.server_close()
        thread.join()


def check_notebook(page, check):
    check(page.locator("#note-list article").count() == 8, "eight notes")
    for note_id, date in [("n1", "2026-05-15"), ("n3", "2026-05-12"), ("n6", "2026-05-14")]:
        check(date in page.locator(f"#{note_id}").inner_text(), f"review deadline {note_id}")
    check("Edited" in page.locator("#n1").inner_text(), "edited date distinct")
    page.locator("#reading-board input[type=checkbox]").first.check()
    page.locator("#note-category").select_option("Research")
    page.locator("#note-tag").select_option("interviews")
    check(page.locator("#note-list article").count() == 3, "category and tag intersection")
    page.locator("#note-search").fill("keyboard")
    check(page.locator("#note-list article").count() == 1 and page.locator("#n4").is_visible(), "search intersection")
    check(page.locator("#reading-progress").inner_text() == "1 of 3 read", "independent reading state")
    # A real fill followed by a pointer click catches blur-triggered rerender loss.
    page.locator("#n4 summary").click()
    check(page.locator("#n4 details").get_attribute("open") is not None, "disclosure after search blur")
    page.locator("#note-search").fill("no-match-phrase")
    check(page.locator("#note-empty").is_visible(), "empty state")
    page.locator("#note-filters button[type=reset]").click()
    page.wait_for_function("document.querySelectorAll('#note-list article').length === 8")
    check(page.locator("#reading-progress").inner_text() == "1 of 3 read", "reset preserves reading state")
    page.locator("#note-tag").select_option("accessibility")
    check(page.locator("#note-list article").evaluate_all("els => els.map(el => el.id)") == ["n2", "n4", "n6"], "tag crosses categories")
    page.locator("#note-tag").select_option("release")
    page.locator("#note-category").select_option("Draft")
    check(page.locator("#note-list article").evaluate_all("els => els.map(el => el.id)") == ["n3", "n8"], "draft and release intersection")
    page.locator("#note-filters button[type=reset]").click()
    page.wait_for_function("document.querySelectorAll('#note-list article').length === 8")
    page.locator("#note-order").select_option("title")
    check(page.locator("#note-list article").first.get_attribute("id") == "n1", "title ordering")


def check_galaxy(page, check):
    check(page.locator("#sky-list article").count() == 4, "four entries")
    page.locator("[data-save=s2]").click()
    check(page.locator("[data-save=s2]").get_attribute("aria-pressed") == "true", "save state")
    check(page.evaluate("document.activeElement.dataset.save") == "s2", "save focus retained")
    page.locator("#sky-saved").check()
    check(page.locator("#sky-list article").count() == 1, "saved-only filter")
    page.locator("#sky-search").fill("sketch")
    check(page.locator("#s2").is_visible(), "field note searchable")
    page.locator("#sky-type").select_option("Cloud")
    check(page.locator("#sky-empty").is_visible(), "filter intersection empty state")
    page.locator("#bulletin-month").select_option("april")
    check("Paper lantern evening" in page.locator("#bulletin-list").inner_text(), "independent bulletin")
    page.locator("#sky-type").select_option("")
    check(page.locator("#sky-list article").count() == 1, "bulletin preserves saved state")
    page.locator("#sky-saved").uncheck()
    page.locator("#sky-search").fill("")
    check(page.locator("#sky-list article").count() == 4, "restore all entries")
    page.locator("#s1 summary").click()
    check(page.locator("#s1 details").get_attribute("open") is not None, "field note disclosure")


def check_queue(page, check):
    check(page.locator("#queue-list tr").count() == 5, "five items")
    check(all(word in page.locator("#queue-list").inner_text() for word in ["Ready", "Needs info", "Scheduled"]), "written statuses")
    page.locator("#queue-mine").check()
    page.locator("#queue-status").select_option("Ready")
    check(page.locator("#queue-list tr").count() == 2, "assignee and status intersection")
    page.locator("#queue-search").fill("handoff")
    check(page.locator("#queue-list tr").count() == 1, "search intersection")
    page.locator("#q1 summary").click()
    check(page.locator("#q1 details").get_attribute("open") is not None, "review disclosure")
    page.locator("#queue-search").fill("no-match-phrase")
    check(page.locator("#queue-empty").is_visible(), "empty state")
    page.locator("#queue-filters button[type=reset]").click()
    page.wait_for_function("document.querySelectorAll('#queue-list tr').length === 5")
    check(page.locator("#queue-list tr").count() == 5, "clear filters")


CHECKS = {"notebook": check_notebook, "galaxy": check_galaxy, "queue": check_queue}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, required=True, help="Isolated project copy to check")
    parser.add_argument("--out", type=Path, required=True, help="Task-owned output directory")
    parser.add_argument("--browser", help="Installed Chromium/Chrome executable; otherwise Playwright's browser")
    parser.add_argument("--pages", nargs="+", choices=CHECKS, default=list(CHECKS))
    args = parser.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    observations = []
    result = {"result": "FAIL", "observations": observations, "limits": "Named flows at two widths only; inspect content, unselected scope and visual quality separately."}
    try:
        with serve(args.root.resolve()) as base_url, sync_playwright() as playwright:
            browser = playwright.chromium.launch(executable_path=args.browser, headless=True)
            try:
                for name in args.pages:
                    for width, height in [(1440, 1000), (390, 844)]:
                        page = browser.new_page(viewport={"width": width, "height": height})
                        page.set_default_timeout(5000)
                        errors = []
                        page.on("pageerror", lambda error: errors.append(str(error)))
                        observation = {"page": name, "width": width, "passed": []}
                        observations.append(observation)

                        def check(condition, label):
                            if not condition:
                                raise AssertionError(f"{name} at {width}: {label}")
                            observation["passed"].append(label)

                        try:
                            page.goto(f"{base_url}/{name}.html", wait_until="networkidle")
                            CHECKS[name](page, check)
                            check(page.evaluate("document.documentElement.scrollWidth <= innerWidth"), "no document overflow")
                            page.keyboard.press("Tab")
                            check(page.evaluate("document.activeElement.tagName") != "BODY", "keyboard reaches a control")
                            check(not errors, "no page script errors")
                            page.screenshot(path=str(args.out / f"{name}-{width}.png"), full_page=True)
                        finally:
                            page.close()
                result["result"] = "PASS"
            finally:
                browser.close()
    except Exception as error:
        result["failure"] = str(error)
        raise
    finally:
        (args.out / "result.json").write_text(json.dumps(result, indent=2) + "\n")
    print(json.dumps({"result": result["result"], "browser_runs": len(observations)}))


if __name__ == "__main__":
    main()
