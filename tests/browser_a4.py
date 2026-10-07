"""Browser proof of local A4 pages and all visible media with source CDN blocked."""

from __future__ import annotations

import json
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
PAGES = json.loads((ROOT / "evidence/pages.json").read_text(encoding="utf-8"))["pages"]
BASE = "http://127.0.0.1:8767"
SCREENSHOTS = ROOT / "artifacts/a4"


def browser_for(playwright):
    try:
        return playwright.chromium.launch(headless=True), "Playwright Chromium"
    except Exception as first_error:
        for candidate, label in (
            (Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"), "Google Chrome"),
            (Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"), "Microsoft Edge"),
            (Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"), "Microsoft Edge"),
        ):
            if candidate.is_file():
                return playwright.chromium.launch(headless=True, executable_path=str(candidate)), label
        raise RuntimeError("Není dostupný místní Chrome/Edge.") from first_error


def check(ok, message):
    if not ok:
        raise AssertionError(message)


with sync_playwright() as playwright:
    browser, browser_name = browser_for(playwright)
    SCREENSHOTS.mkdir(parents=True, exist_ok=True)
    requests_to_source = []
    page_count = image_count = gallery_count = 0
    try:
        for width in (390, 1440):
            context = browser.new_context(viewport={"width": width, "height": 900}, java_script_enabled=False)
            context.route("**/*", lambda route: (requests_to_source.append(route.request.url), route.abort())[1]
                          if "clvaw-cdnwnd.com" in route.request.url or "duyn491kcolsw.cloudfront.net" in route.request.url
                          else route.abort() if "google.com/maps/embed" in route.request.url else route.continue_())
            page = context.new_page()
            page.set_default_timeout(15000)
            page.set_default_navigation_timeout(15000)
            for source in PAGES:
                response = page.goto(BASE + source["path"], wait_until="domcontentloaded")
                check(response and response.status == 200, f"{width}px {source['path']}: HTTP není 200")
                check(page.title() == source["title"], f"{source['path']}: jiný title")
                check(page.locator("main [data-content-id]").count() == len(source["text_nodes"]),
                      f"{source['path']}: chybí obsahové uzly")
                check(page.evaluate("document.documentElement.scrollWidth <= innerWidth + 1"),
                      f"{width}px {source['path']}: vodorovné přetékání")
                images = page.locator("img[data-media-id]")
                check(images.count() == len(source["image_occurrences"]) + len([e for e in source["embedded_resources"] if e["kind"] == "svg"]),
                      f"{source['path']}: chybí obrazový výskyt")
                for i in range(images.count()):
                    image = images.nth(i)
                    image.scroll_into_view_if_needed()
                    image.evaluate("img => img.loading = 'eager'")
                    image.wait_for(state="visible")
                    check(image.evaluate("img => img.complete && img.naturalWidth > 0"),
                          f"{source['path']}: nenačtené médium {image.get_attribute('data-media-id')}")
                    image_count += 1
                gallery = page.locator("main a[data-gallery-id]")
                expected = [(g["id"], str(item["order"]), item["media_id"])
                            for g in source["galleries"] for item in g["items"]]
                actual = [(gallery.nth(i).get_attribute("data-gallery-id"),
                           gallery.nth(i).get_attribute("data-gallery-order"),
                           gallery.nth(i).get_attribute("data-media-id")) for i in range(gallery.count())]
                check(actual == expected, f"{source['path']}: galerie má jiné pořadí")
                for i in range(gallery.count()):
                    href = gallery.nth(i).get_attribute("href")
                    check(href.startswith("/assets/images/") and href.endswith(".jpg"),
                          f"{source['path']}: galerie nemá lokální plnou verzi")
                    response = context.request.get(BASE + href)
                    check(response.status == 200 and response.headers.get("content-type", "").startswith("image/jpeg"),
                          f"{source['path']}: plná položka galerie nejde otevřít")
                    gallery_count += 1
                if width == 1440:
                    name = "home" if source["path"] == "/" else source["path"].strip("/")
                    page.screenshot(path=str(SCREENSHOTS / f"{name}-desktop.png"), full_page=True)
                page_count += 1
            context.close()
        check(not requests_to_source, f"Web požádal o zdrojovou CDN: {requests_to_source[:3]}")
        print(json.dumps({"browser": browser_name, "pages": page_count, "images_loaded": image_count,
                          "gallery_full_opened": gallery_count, "source_cdn_requests": len(requests_to_source)},
                         ensure_ascii=False))
    finally:
        browser.close()
