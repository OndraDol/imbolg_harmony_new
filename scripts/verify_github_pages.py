"""Compare the Pages copy to the unchanged source, then optionally to public HTTPS."""
import argparse
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import re
from urllib.parse import quote, unquote, urlsplit
from urllib.error import HTTPError
from urllib.request import Request, urlopen
from xml.etree import ElementTree as ET

from bs4 import BeautifulSoup, NavigableString, Tag

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "dist"
ARTIFACTS = ROOT / "artifacts/github-pages"
OUTPUT = ARTIFACTS / "preview/imbolg_harmony_new"
PREFIX = "/imbolg_harmony_new/"
SITE = "https://ondradol.github.io" + PREFIX


def require(condition, message):
    if not condition:
        raise AssertionError(message)


def normalized_node(node):
    if isinstance(node, NavigableString):
        text = re.sub(r"\s+", " ", str(node)).strip()
        return text or None
    if isinstance(node, Tag):
        attributes = sorted((k, tuple(v) if isinstance(v, list) else v) for k, v in node.attrs.items())
        children = [value for child in node.children if (value := normalized_node(child)) is not None]
        return [node.name, attributes, children]
    return None


def original_url(url):
    return "/" + url[len(PREFIX):] if url.startswith(PREFIX) else url


def check_html(relative, expected_files):
    original = BeautifulSoup((SOURCE / relative).read_text(encoding="utf-8"), "html.parser")
    copy = BeautifulSoup((OUTPUT / relative).read_text(encoding="utf-8"), "html.parser")
    require(copy.select_one('meta[name="robots"]') is not None, f"Missing noindex: {relative}")
    require("noindex" in copy.select_one('meta[name="robots"]').get("content", ""), f"Indexable duplicate: {relative}")
    for element in copy.find_all(True):
        urls = [element[attr] for attr in ("href", "src", "poster") if element.has_attr(attr)]
        urls += [value.strip().split()[0] for value in element.get("srcset", "").split(",") if value.strip()]
        for url in urls:
            parsed = urlsplit(url)
            if parsed.path.startswith("/") and not parsed.netloc:
                require(parsed.path.startswith(PREFIX), f"Unprefixed local URL: {relative}: {url}")
                path = unquote(parsed.path[len(PREFIX):])
                path = path + "index.html" if not path or path.endswith("/") else path
                require(path in expected_files, f"Broken local URL: {relative}: {url}")
                if parsed.fragment and path.endswith(".html"):
                    target = BeautifulSoup((OUTPUT / path).read_text(encoding="utf-8"), "html.parser")
                    require(target.find(id=unquote(parsed.fragment)) is not None, f"Missing anchor: {relative}: {url}")
        for attribute in ("href", "src", "poster"):
            if element.has_attr(attribute):
                element[attribute] = original_url(element[attribute])
        if element.has_attr("srcset"):
            values = []
            for value in element["srcset"].split(","):
                parts = value.strip().split()
                parts[0] = original_url(parts[0])
                values.append(" ".join(parts))
            element["srcset"] = ", ".join(values)
    for meta in copy.select("meta[data-pages-copy]"):
        require(meta.get("name") == "robots", "Unexpected extra metadata")
        meta.decompose()
    original_forms, copy_forms = original.select("form"), copy.select("form")
    require(len(original_forms) == len(copy_forms), f"Missing form: {relative}")
    notes = copy.select("[data-pages-contact-note]")
    require(len(notes) == len(copy_forms), f"Missing inactive notice: {relative}")
    for note in notes:
        require(note.get_text(" ", strip=True) == "Formulář v této kopii webu zatím neodesílá. Napište na kralovamarket@seznam.cz .", "Unexpected contact notice")
        require(note.select_one('a[href="mailto:kralovamarket@seznam.cz"]') is not None, "Missing usable e-mail link")
        note.decompose()
    for before, after in zip(original_forms, copy_forms):
        require(not after.has_attr("action") and not after.has_attr("method"), "Form still has a submission endpoint")
        require(after.get("data-pages-inactive") == "true" and after.get("aria-describedby") == "pages-contact-note", "Form status missing")
        after.attrs = dict(before.attrs)
        old_controls, new_controls = before.select("input, textarea, select, button"), after.select("input, textarea, select, button")
        require(len(old_controls) == len(new_controls), "Form controls changed")
        for old, new in zip(old_controls, new_controls):
            require(new.has_attr("disabled"), "Active input in the static form")
            if not old.has_attr("disabled"):
                new.attrs.pop("disabled")
            if new.name == "button":
                require(new.get("type") == "button", "Submit button is still active")
                new["type"] = old.get("type", "submit")
    require(normalized_node(original.html) == normalized_node(copy.html), f"Unauthorized HTML/content/layout difference: {relative}")


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--live", action="store_true", help="Check the deployed public files through HTTPS")
    args = parser.parse_args()
    manifest = json.loads((ARTIFACTS / "build-manifest.json").read_text(encoding="utf-8"))
    expected = {p.relative_to(SOURCE).as_posix() for p in SOURCE.rglob("*") if p.is_file()} - {".htaccess"} | {".nojekyll"}
    actual = {p.relative_to(OUTPUT).as_posix() for p in OUTPUT.rglob("*") if p.is_file()}
    require(actual == expected == {f["path"] for f in manifest["files"]}, "Missing or unexpected public file")
    require(manifest["site"] == SITE and manifest["form"] == "inactive", "Wrong deployment destination")
    for item in manifest["files"]:
        data = (OUTPUT / item["path"]).read_bytes()
        require(sha256(data).hexdigest() == item["sha256"] and len(data) == item["bytes"], f"Manifest mismatch: {item['path']}")
        require(not re.search(r"(?:^|/)(?:\.git|\.secrets|private|server|docs|archive|artifacts)(?:/|$)|\.php$|credential|CNAME", item["path"], re.I), "Nonpublic file in deployment")
        if item["path"].endswith(".html"):
            check_html(item["path"], expected)
        elif item["path"] not in {".nojekyll", "robots.txt", "sitemap.xml", "assets/css/site.css"}:
            require(data == (SOURCE / item["path"]).read_bytes(), f"Public asset changed: {item['path']}")
    source_css = (SOURCE / "assets/css/site.css").read_text(encoding="utf-8")
    copy_css = (OUTPUT / "assets/css/site.css").read_text(encoding="utf-8")
    require(copy_css == source_css + "\n/* Static Pages contact form */\n.pages-contact-note { margin-block: 1rem; }\n.contact-form button:disabled { cursor: not-allowed; opacity: .65; }\n", "Unapproved CSS difference")
    require((OUTPUT / ".nojekyll").stat().st_size == 0, "Jekyll marker missing")
    require((OUTPUT / "robots.txt").read_text() == "User-agent: *\nDisallow: /\nSitemap: " + SITE + "sitemap.xml\n", "Wrong robots")
    pages = json.loads((ROOT / "src/_data/sitePages.json").read_text(encoding="utf-8"))
    sitemap = ET.parse(OUTPUT / "sitemap.xml")
    require([e.text for e in sitemap.findall(".//{*}loc")] == [SITE + page["path"].lstrip("/") for page in pages], "Sitemap is incomplete")
    live = []
    not_found = None
    if args.live:
        def fetch(item):
            request = Request(SITE + quote(item["path"], safe="/"), headers={"User-Agent": "Imbolg-Harmony-release-verification"})
            with urlopen(request, timeout=45) as response:
                data = response.read()
                require(response.status == 200, f"Public HTTP failure: {item['path']}")
                require(sha256(data).hexdigest() == item["sha256"] and len(data) == item["bytes"], f"Deployed file differs: {item['path']}")
            return {"path": item["path"], "status": 200, "sha256": item["sha256"]}
        with ThreadPoolExecutor(max_workers=6) as pool:
            live = list(pool.map(fetch, [item for item in manifest["files"] if item["path"] != ".nojekyll"]))
        try:
            with urlopen(SITE + "__pages-not-found-check__/", timeout=30):
                raise AssertionError("Unknown route did not return HTTP 404")
        except HTTPError as error:
            require(error.code == 404, "Wrong error status for an unknown route")
            require(sha256(error.read()).hexdigest() == sha256((OUTPUT / "404.html").read_bytes()).hexdigest(), "Custom 404 differs from the verified page")
            not_found = {"status": 404, "custom_page": True}
    receipt = {"verified_utc": datetime.now(timezone.utc).isoformat(), "result": "PASS", "identity": manifest["identity"], "files": len(actual), "pages": len(pages), "html": sum(p.endswith(".html") for p in actual), "form": "inactive", "live_files": live, "not_found": not_found}
    name = "live-verification.json" if args.live else "local-verification.json"
    (ARTIFACTS / name).write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(receipt | {"live_files": len(live)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
