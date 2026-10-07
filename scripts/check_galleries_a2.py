"""Exercise every public gallery item in the real browser without submitting forms.

Run: python scripts/check_galleries_a2.py --cdp <URL> --snapshot archive/<timestamp>
"""

import argparse
import json
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
BASE = "https://www.imbolg-harmony.cz"


def main(cdp, snapshot):
    evidence = json.loads((ROOT / "evidence/pages.json").read_text(encoding="utf-8"))
    results = []
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp(cdp)
        context = browser.contexts[0]
        page = context.new_page()
        page.set_viewport_size({"width": 1440, "height": 900})
        for record in evidence["pages"]:
            for gallery in record["galleries"]:
                path = record["path"]
                expected = len(gallery["items"])
                page.goto(BASE + path, wait_until="networkidle")
                cookie = page.get_by_role("button", name="Přijmout nezbytné")
                if cookie.is_visible():
                    cookie.click()
                links = page.locator("a.b-gal-a")
                actual = links.count()
                if actual != expected:
                    raise RuntimeError(f"{path}: DOM gallery {actual}, evidence {expected}")
                links.first.click()
                page.locator(".pswp__counter").wait_for(state="visible")
                counters = []
                for number in range(1, expected + 1):
                    page.wait_for_function("expected => document.querySelector('.pswp__counter')?.textContent?.trim() === expected", arg=f"{number} / {expected}")
                    counter = page.locator(".pswp__counter").inner_text().strip()
                    loaded = page.evaluate("[...document.querySelectorAll('.pswp__img')].some(x => x.complete && x.naturalWidth > 0)")
                    if not loaded:
                        page.wait_for_function("[...document.querySelectorAll('.pswp__img')].some(x => x.complete && x.naturalWidth > 0)")
                    counters.append(counter)
                    if number == 1:
                        page.screenshot(path=str(snapshot / "screenshots" / f"{record['id']}-gallery-open.png"), animations="disabled")
                    if number < expected:
                        page.get_by_role("button", name="Next").click()
                results.append({"path": path, "gallery_id": gallery["id"], "dom_items": actual,
                                "counters": counters, "all_images_loaded": True})
                print(f"GALLERY {path}: {len(counters)}/{expected} counters and images loaded", flush=True)
        with (snapshot / "gallery-browser-check.json").open("x", encoding="utf-8", newline="\n") as file:
            json.dump(results, file, ensure_ascii=False, indent=2)
            file.write("\n")
        page.close()
        browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cdp", required=True)
    parser.add_argument("--snapshot", type=Path, required=True)
    args = parser.parse_args()
    main(args.cdp, args.snapshot.resolve())
