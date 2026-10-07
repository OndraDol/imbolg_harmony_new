"""Lokální browser kontrola technické kostry A3 bez odesílání dat."""

import json
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
PAGES = json.loads((ROOT / "src/_data/sitePages.json").read_text(encoding="utf-8"))
BASE = "http://127.0.0.1:8765"
SCREENSHOTS = ROOT / "artifacts/a3"


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
        raise RuntimeError("Není dostupný Playwright Chromium ani systémový Chrome/Edge.") from first_error


def check(condition, detail):
    if not condition:
        raise AssertionError(detail)


with sync_playwright() as playwright:
    browser, browser_name = browser_for(playwright)
    try:
        SCREENSHOTS.mkdir(parents=True, exist_ok=True)
        checked = 0
        for width in (360, 390, 768, 1440):
            context = browser.new_context(viewport={"width": width, "height": 900}, java_script_enabled=False)
            page = context.new_page()
            page.set_default_timeout(10000)
            page.set_default_navigation_timeout(10000)
            errors = []
            page.on("pageerror", lambda error: errors.append(str(error)))
            for item in PAGES:
                response = page.goto(BASE + item["path"], wait_until="networkidle")
                check(response is not None and response.status == 200, f"{width}px {item['path']}: HTTP není 200")
                check(page.title() == item["title"], f"{width}px {item['path']}: nesprávný titulek")
                check(page.locator("main h1").inner_text() == item["heading"], f"{width}px {item['path']}: nesprávný nadpis")
                check(page.evaluate("document.documentElement.scrollWidth <= innerWidth"), f"{width}px {item['path']}: vodorovné přetékání")
                mobile = width <= 768
                nav = page.locator(".mobile-menu nav" if mobile else ".desktop-nav")
                check(page.locator(".mobile-menu summary").is_visible() == mobile, f"{width}px {item['path']}: chybný stav mobilního menu")
                if mobile:
                    check(not nav.is_visible(), f"{width}px {item['path']}: zavřené menu je viditelné")
                    page.locator(".mobile-menu summary").click()
                check(nav.is_visible(), f"{width}px {item['path']}: menu nelze otevřít bez JS")
                links = nav.locator("a")
                check(links.count() == 10, f"{width}px {item['path']}: menu nemá 10 položek")
                check([links.nth(i).get_attribute("href") for i in range(10)] == [source["path"] for source in PAGES], f"{width}px {item['path']}: špatné pořadí menu")
                current = nav.locator('a[aria-current="page"]')
                check(current.count() == 1 and current.get_attribute("href") == item["path"], f"{width}px {item['path']}: chybná aktivní položka")
                checked += 1
            page.goto(BASE, wait_until="networkidle")
            page.screenshot(path=str(SCREENSHOTS / f"home-{width}.png"), full_page=True)
            if width == 360:
                page.keyboard.press("Tab")
                check(page.evaluate("document.activeElement.classList.contains('skip-link')"), "Skip link není první v pořadí klávesnice")
                check(page.locator(".skip-link").is_visible(), "Skip link není při focusu viditelný")
                page.keyboard.press("Enter")
                check(page.evaluate("document.activeElement.id === 'hlavni-obsah'"), "Skip link nepřesunul focus do main")
                summary = page.locator(".mobile-menu summary")
                summary.focus()
                page.keyboard.press("Enter")
                check(page.locator(".mobile-menu").get_attribute("open") is not None, "Mobilní menu nejde otevřít klávesnicí")
                summary.focus()
                page.keyboard.press("Enter")
                check(page.locator(".mobile-menu").get_attribute("open") is None, "Mobilní menu nejde zavřít klávesnicí")
                summary.focus()
                page.keyboard.press("Enter")
                page.locator('.mobile-menu a[href="/kontakt/"]').click()
                check(page.url.endswith("/kontakt/"), "Mobilní odkaz nepřešel na původní URL")
            check(not errors, f"{width}px: chyba stránky: {errors}")
            context.close()
        print(f"A3 browser: {checked} HTTP průchodů, 4 šířky, JS vypnutý, menu, klávesnice a skip link OK ({browser_name}).")
    finally:
        browser.close()
