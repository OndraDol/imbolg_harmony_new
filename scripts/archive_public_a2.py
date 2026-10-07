"""Read-only A2 capture of the public Imbolg Harmony site via an existing Chrome CDP session.

Run: python scripts/archive_public_a2.py --cdp <agent-browser get cdp-url>
The script creates a new timestamped snapshot; it never overwrites an older one.
Only public page responses and public image URLs are saved. No browser storage is exported.
"""

import argparse
import hashlib
import io
import json
import re
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urljoin, urlparse
from xml.etree import ElementTree

from bs4 import BeautifulSoup
from PIL import Image
from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
BASE = "https://www.imbolg-harmony.cz"
ALLOWED_MEDIA_HOSTS = {"454501af52.clvaw-cdnwnd.com", "www.imbolg-harmony.cz"}
BLOCK_TAGS = "h1,h2,h3,h4,h5,h6,p,li,blockquote,figcaption,dt,dd"


def digest(data):
    return hashlib.sha256(data).hexdigest()


def write_new(path, data):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("xb") as file:
        file.write(data)


def save_json(path, value):
    write_new(path, (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8"))


def slug(path):
    return "home" if path == "/" else path.strip("/").replace("/", "-")


def source_data(page):
    return page.evaluate("""({blockTags}) => {
      const main = document.querySelector('main') || document.body;
      const blocks = [...main.querySelectorAll(blockTags)].map((el, i) => ({
        id: location.pathname === '/' ? `home-text-${String(i+1).padStart(3,'0')}` : `${location.pathname.replaceAll('/','')}-text-${String(i+1).padStart(3,'0')}`,
        tag: el.tagName.toLowerCase(), html: el.innerHTML, text: el.innerText,
        outer_html: el.outerHTML
      }));
      const links = [...document.querySelectorAll('a[href]')].map((el, i) => ({
        order: i+1, href: el.getAttribute('href'), resolved: el.href,
        text: el.innerText, title: el.getAttribute('title'),
        in_main: main.contains(el), class_name: el.className
      }));
      const imageOccurrences = [...document.querySelectorAll('img')].map((el, i) => ({
        order: i+1, src: el.getAttribute('src'), current_src: el.currentSrc,
        alt: el.getAttribute('alt'), width: el.getAttribute('width'), height: el.getAttribute('height'),
        loading: el.getAttribute('loading'), outer_html: el.outerHTML,
        picture: el.closest('picture')?.outerHTML || null,
        in_main: main.contains(el)
      }));
      const backgrounds = [...document.querySelectorAll('*')].map((el, i) => ({
        dom_order: i+1, tag: el.tagName.toLowerCase(), class_name: String(el.className).slice(0,200),
        inline: el.style.backgroundImage, computed: getComputedStyle(el).backgroundImage
      })).filter(x => (x.inline && x.inline !== 'none') || (x.computed && x.computed !== 'none'));
      const galleries = [...document.querySelectorAll('.b-gal')].map((gal, i) => ({
        id: `${location.pathname.replaceAll('/','') || 'home'}-gallery-${String(i+1).padStart(2,'0')}`,
        order: i+1, items: [...gal.querySelectorAll('a.b-gal-a')].map((el, j) => ({
          order: j+1, href: el.href, raw_href: el.getAttribute('href'),
          caption: el.dataset.liteboxText || '', group: el.dataset.liteboxGroup || '',
          image: el.querySelector('img')?.outerHTML || null
        }))
      }));
      const forms = [...document.forms].map((el, i) => ({
        order: i+1, action: el.getAttribute('action'), method: el.getAttribute('method'),
        fields: [...el.querySelectorAll('input,textarea,select,button')].map(x => ({
          tag: x.tagName.toLowerCase(), type: x.getAttribute('type'), name: x.getAttribute('name'),
          label: x.labels ? [...x.labels].map(y=>y.innerText) : [], placeholder: x.getAttribute('placeholder'),
          required: x.required, text: x.tagName === 'BUTTON' ? x.innerText : null
        }))
      }));
      return {
        title: document.title, lang: document.documentElement.lang,
        description: document.querySelector('meta[name="description"]')?.content || null,
        canonical: document.querySelector('link[rel="canonical"]')?.href || null,
        main_text: main.innerText, blocks, links, images: imageOccurrences,
        backgrounds, galleries, forms,
        menu: [...document.querySelectorAll('[role="menuitem"],nav a')].map(x=>({text:x.innerText,href:x.href || null})),
        rendered_html: document.documentElement.outerHTML
      };
    }""", {"blockTags": BLOCK_TAGS})


def scroll_all(page):
    page.evaluate("window.scrollTo(0, 0)")
    height = page.evaluate("document.documentElement.scrollHeight")
    for y in range(0, height + 1000, 650):
        page.evaluate("y => window.scrollTo(0, y)", y)
        page.wait_for_timeout(100)
    page.wait_for_timeout(400)
    page.evaluate("window.scrollTo(0, 0)")


def media_urls(page_record):
    urls = []
    for img in page_record["images"]:
        for value in (img["src"], img["current_src"]):
            if value:
                urls.append(urljoin(BASE, value))
        if img["picture"]:
            picture = BeautifulSoup(img["picture"], "html.parser")
            for source in picture.select("source[srcset]"):
                candidates = [part.strip().split()[0] for part in source["srcset"].split(",") if part.strip()]
                if candidates:
                    urls.append(urljoin(BASE, candidates[-1]))
    for bg in page_record["backgrounds"]:
        for value in (bg["inline"], bg["computed"]):
            urls.extend(re.findall(r'url\(["\']?([^"\')]+)', value or ""))
    for gallery in page_record["galleries"]:
        urls.extend(item["href"] for item in gallery["items"])
    return list(dict.fromkeys(u for u in urls if urlparse(u).hostname in ALLOWED_MEDIA_HOSTS))


def main(cdp):
    started = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H-%M-%SZ")
    snapshot = ROOT / "archive" / started
    if snapshot.exists():
        raise FileExistsError(snapshot)
    snapshot.mkdir(parents=True)
    (snapshot / "screenshots").mkdir()
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp(cdp)
        context = browser.contexts[0]
        page = context.new_page()
        page.set_viewport_size({"width": 1440, "height": 900})
        sitemap_response = page.goto(BASE + "/sitemap.xml", wait_until="domcontentloaded")
        sitemap_bytes = sitemap_response.body()
        write_new(snapshot / "sitemap.xml", sitemap_bytes)
        sitemap_paths = [urlparse(el.text).path for el in ElementTree.fromstring(sitemap_bytes).iter() if el.tag.endswith("loc") and el.text]
        queue = list(dict.fromkeys(sitemap_paths))
        pages = []
        seen = set()
        errors = []
        all_media_urls = []
        while queue:
            path = queue.pop(0)
            if path in seen:
                continue
            seen.add(path)
            url = BASE + path
            try:
                response = page.goto(url, wait_until="domcontentloaded", timeout=30000)
                page.wait_for_load_state("networkidle", timeout=15000)
                scroll_all(page)
                record = source_data(page)
                raw = response.body()
                name = slug(path)
                write_new(snapshot / "raw-html" / f"{name}.html", raw)
                rendered = record.pop("rendered_html").encode("utf-8")
                write_new(snapshot / "rendered-dom" / f"{name}.html", rendered)
                page.screenshot(path=str(snapshot / "screenshots" / f"{name}-desktop.png"), full_page=True, animations="disabled")
                page.set_viewport_size({"width": 390, "height": 844})
                page.screenshot(path=str(snapshot / "screenshots" / f"{name}-mobile.png"), full_page=True, animations="disabled")
                page.set_viewport_size({"width": 1440, "height": 900})
                record.update({"url": url, "path": path, "status": response.status,
                               "raw_html": f"raw-html/{name}.html", "raw_sha256": digest(raw),
                               "rendered_dom": f"rendered-dom/{name}.html", "rendered_sha256": digest(rendered)})
                pages.append(record)
                for link in record["links"]:
                    parsed = urlparse(link["resolved"])
                    if parsed.hostname == "www.imbolg-harmony.cz" and parsed.path.endswith("/") and parsed.path not in seen and parsed.path not in queue:
                        queue.append(parsed.path)
                all_media_urls.extend(media_urls(record))
                print(f"PAGE {path}: HTTP {response.status}; {len(record['blocks'])} blocks, {len(record['images'])} img, {sum(len(g['items']) for g in record['galleries'])} gallery items", flush=True)
            except Exception as exc:
                errors.append({"page": url, "error": str(exc)})
                print(f"ERROR {url}: {exc}", flush=True)
        # Close after capture; image downloads use the same browser transport in a fresh tab.
        image_page = context.new_page()
        image_page.set_default_timeout(30000)
        media = []
        hashes = {}
        for index, url in enumerate(dict.fromkeys(all_media_urls), 1):
            parsed = urlparse(url)
            if parsed.hostname not in ALLOWED_MEDIA_HOSTS:
                continue
            try:
                response = image_page.goto(url, wait_until="commit", timeout=30000)
                content = response.body()
                with Image.open(io.BytesIO(content)) as picture:
                    picture.verify()
                with Image.open(io.BytesIO(content)) as picture:
                    fmt = picture.format
                    dimensions = list(picture.size)
                sha = digest(content)
                extension = {"JPEG": ".jpg", "WEBP": ".webp", "PNG": ".png", "GIF": ".gif"}.get(fmt, ".bin")
                local = hashes.get(sha)
                if local is None:
                    local = f"media/{sha}{extension}"
                    write_new(snapshot / local, content)
                    hashes[sha] = local
                media.append({"url": url, "status": response.status, "content_type": response.headers.get("content-type"),
                              "archive_file": local, "bytes": len(content), "sha256": sha, "format": fmt, "dimensions": dimensions})
                print(f"MEDIA {index}/{len(set(all_media_urls))}: {response.status} {dimensions[0]}x{dimensions[1]} {url}", flush=True)
            except Exception as exc:
                errors.append({"media": url, "error": str(exc)})
                print(f"ERROR MEDIA {url}: {exc}", flush=True)
        save_json(snapshot / "capture.json", {"captured_utc": started, "sitemap_paths": sitemap_paths,
                                               "pages": pages, "media": media, "errors": errors})
        image_page.close()
        page.close()
        browser.close()
    print(f"SNAPSHOT {snapshot}")
    print(f"SUMMARY pages={len(pages)} media_urls={len(media)} unique_files={len(hashes)} errors={len(errors)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cdp", required=True)
    main(parser.parse_args().cdp)
