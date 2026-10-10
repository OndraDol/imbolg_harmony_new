"""Focused browser regression for the approved UX additions and lightbox."""
from __future__ import annotations

from pathlib import Path
import json
import sys
from urllib.parse import urlparse

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "artifacts" / "ux-20261010"
sys.path.insert(0, str(ROOT / "scripts"))

from form_fixture_a5 import prepare_fixture, remove_fixture, running_server
from browser_a6 import browser_for


def check(condition, message):
    if not condition:
        raise AssertionError(message)


def no_horizontal_overflow(page, label):
    metrics = page.evaluate("""() => ({
      viewport: innerWidth,
      document: document.documentElement.scrollWidth,
      dialog: document.querySelector('.lightbox')?.scrollWidth || 0,
      dialogBox: document.querySelector('.lightbox')?.getBoundingClientRect().width || 0
    })""")
    check(metrics["document"] <= metrics["viewport"] + 1, f"{label}: viewport overflow {metrics}")
    check(metrics["dialogBox"] <= metrics["viewport"] + 1, f"{label}: dialog wider than viewport {metrics}")


def wait_for_image(page):
    page.wait_for_function("""() => {
      const image = document.querySelector('.lightbox__image');
      return image && image.complete && image.naturalWidth > 0;
    }""")


def visible_focus_stays_in_dialog(page, dialog, label):
    focusable = dialog.locator("button:not([disabled]), a[href], [tabindex]:not([tabindex='-1'])")
    check(focusable.count() >= 3, f"{label}: missing lightbox controls")
    focusable.last.focus()
    page.keyboard.press("Tab")
    check(page.evaluate("e => e.contains(document.activeElement)", arg=dialog.element_handle()),
          f"{label}: Tab leaves dialog")
    focusable.first.focus()
    page.keyboard.press("Shift+Tab")
    check(page.evaluate("e => e.contains(document.activeElement)", arg=dialog.element_handle()),
          f"{label}: Shift+Tab leaves dialog")


def open_gallery(page, opener, label):
    opener.scroll_into_view_if_needed()
    opener.focus()
    before = page.evaluate("() => ({x: scrollX, y: scrollY})")
    opener.click()
    dialog = page.locator("dialog.lightbox[open]")
    dialog.wait_for(state="visible")
    wait_for_image(page)
    check(page.locator("dialog.lightbox .lightbox__close").evaluate("e => e === document.activeElement"),
          f"{label}: close control does not receive focus")
    return dialog, before


def exercise_gallery(page, base, label, scale_css=""):
    page.goto(base + "/fotogalerie/", wait_until="networkidle")
    if scale_css:
        page.add_style_tag(content=scale_css)
    opener = page.locator("main a[data-gallery-id]").first
    first_href = opener.get_attribute("href")
    check(first_href and first_href.startswith("/assets/images/"), f"{label}: gallery link is not a plain local image link")
    dialog, before = open_gallery(page, opener, label)
    image = dialog.locator(".lightbox__image")
    next_button = dialog.locator(".lightbox__next")
    previous_button = dialog.locator(".lightbox__previous")
    members = page.locator(f'a[data-gallery-id="{opener.get_attribute("data-gallery-id")}"]')
    second_href = members.nth(1).get_attribute("href")

    next_button.click()
    check(image.get_attribute("src").endswith(second_href), f"{label}: next button")
    previous_button.click()
    check(image.get_attribute("src").endswith(first_href), f"{label}: previous button")
    page.keyboard.press("ArrowRight")
    check(image.get_attribute("src").endswith(second_href), f"{label}: ArrowRight")
    page.keyboard.press("ArrowLeft")
    check(image.get_attribute("src").endswith(first_href), f"{label}: ArrowLeft")
    visible_focus_stays_in_dialog(page, dialog, label)
    no_horizontal_overflow(page, label)
    if label.endswith("-normal"):
        page.screenshot(path=str(ART / f"lightbox-{label}.png"), full_page=False)

    page.keyboard.press("Escape")
    dialog.wait_for(state="hidden")
    page.wait_for_function("element => element === document.activeElement", arg=opener.element_handle())
    restored = page.evaluate("() => ({x: scrollX, y: scrollY})")
    check(abs(restored["x"] - before["x"]) <= 2 and abs(restored["y"] - before["y"]) <= 2,
          f"{label}: scroll was not restored {before} -> {restored}")

    page.goto(base + "/", wait_until="networkidle")
    logo = page.locator("header .site-brand")
    logo.click()
    check(page.locator("dialog.lightbox[open]").count() == 0, f"{label}: header logo opened lightbox")

    standalone = page.locator('main a[href="/assets/images/media-012.jpg"]')
    dialog, _ = open_gallery(page, standalone, label + " standalone")
    check(dialog.locator(".lightbox__next").is_disabled(), f"{label}: standalone next enabled")
    check(dialog.locator(".lightbox__previous").is_disabled(), f"{label}: standalone previous enabled")
    dialog.locator(".lightbox__close").click()
    dialog.wait_for(state="hidden")


def exercise_error_link(page, base, label):
    page.goto(base + "/fotogalerie/", wait_until="networkidle")
    opener = page.locator("main a[data-gallery-id]").first
    href = opener.get_attribute("href")
    page.context.route(f"**{href}", lambda route: route.abort())
    opener.click()
    dialog = page.locator("dialog.lightbox[open]")
    dialog.wait_for(state="visible")
    error = dialog.locator(".lightbox__error")
    error.wait_for(state="visible")
    original = dialog.locator(".lightbox__original")
    check(original.is_visible() and original.get_attribute("href").endswith(href),
          f"{label}: failed image has no usable original link")
    page.context.unroute(f"**{href}")


def exercise_no_js(base, browser):
    context = browser.new_context(viewport={"width": 390, "height": 900}, java_script_enabled=False)
    try:
        context.route("**/*", lambda route: route.abort()
                      if urlparse(route.request.url).netloc != urlparse(base).netloc else route.continue_())
        page = context.new_page()
        page.goto(base + "/fotogalerie/", wait_until="networkidle")
        opener = page.locator("main a[data-gallery-id]").first
        href = opener.get_attribute("href")
        check(href and href.startswith("/assets/images/"), "no-js: missing plain image href")
        opener.click()
        page.wait_for_url(base + href)
        check(page.locator("img").evaluate("image => image.complete && image.naturalWidth > 0"),
              "no-js: full image navigation failed")
    finally:
        context.close()


def run():
    ART.mkdir(parents=True, exist_ok=True)
    fixture = prepare_fixture()
    try:
        with running_server(fixture) as base, sync_playwright() as playwright:
            browser, executable = browser_for(playwright)
            try:
                for width in (390, 1440):
                    for mode, css in (("normal", ""), ("text200", "html { font-size: 200% !important; }"),
                                      ("zoom200", "html { zoom: 2; }")):
                        context = browser.new_context(viewport={"width": width, "height": 900})
                        try:
                            context.route("**/*", lambda route: route.abort()
                                          if urlparse(route.request.url).netloc != urlparse(base).netloc else route.continue_())
                            page = context.new_page()
                            page.set_default_timeout(15000)
                            print(f"Checking {width}-{mode}", flush=True)
                            try:
                                exercise_gallery(page, base, f"{width}-{mode}", css)
                            except Exception:
                                page.screenshot(path=str(ART / f"failure-{width}-{mode}.png"))
                                print(page.evaluate('''() => [...document.querySelectorAll('.lightbox, .lightbox button')].map(e => ({class:e.className, rect:e.getBoundingClientRect().toJSON(), scrollHeight:e.scrollHeight, clientHeight:e.clientHeight}))'''), flush=True)
                                raise
                            if mode == "normal" and width == 390:
                                page.goto(base, wait_until="networkidle")
                                page.locator(".form-privacy summary").click()
                                page.locator('.contact-form').screenshot(path=str(ART / "home-form-details-390.png"))
                                page.locator(".form-privacy summary").click()
                                page.locator('.contact-form').screenshot(path=str(ART / "home-form-390.png"))
                                page.goto(base + "/kontakt/", wait_until="networkidle")
                                page.screenshot(path=str(ART / "contact-390.png"), full_page=True)
                        finally:
                            context.close()

                error_context = browser.new_context(viewport={"width": 390, "height": 900})
                try:
                    error_context.route("**/*", lambda route: route.abort()
                                        if urlparse(route.request.url).netloc != urlparse(base).netloc else route.continue_())
                    error_page = error_context.new_page()
                    exercise_error_link(error_page, base, "image-error")
                finally:
                    error_context.close()
                exercise_no_js(base, browser)
            finally:
                browser.close()
            (ART / 'browser-results.json').write_text(json.dumps({'status': 'PASS', 'browser': executable, 'widths': [390, 1440], 'modes': ['normal', 'text200', 'zoom200'], 'scenarios': ['focus-trap', 'scroll-restore', 'buttons-arrows', 'standalone', 'logo-excluded', 'image-error', 'no-js']}, indent=2)+'\n', encoding='utf-8')
            print(f"PASS browser UX regression ({executable})")
    finally:
        remove_fixture(fixture)


if __name__ == "__main__":
    run()
