"""Add observed public SVG embeds and iframe references to an existing A2 snapshot.

Run: python scripts/archive_embeds_a2.py --cdp <URL> --snapshot archive/<timestamp>
Only appends new supplement files; does not rewrite the initial capture.
"""

import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import urlparse
from xml.etree import ElementTree

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
ALLOWED_SVG_HOST = "duyn491kcolsw.cloudfront.net"


def main(cdp, snapshot):
    capture = json.loads((snapshot / "capture.json").read_text(encoding="utf-8"))
    embeds = {}
    iframes = []
    for page in capture["pages"]:
        soup = BeautifulSoup((snapshot / page["rendered_dom"]).read_text(encoding="utf-8"), "html.parser")
        for index, element in enumerate(soup.select("embed[src]"), 1):
            url = element["src"]
            if urlparse(url).hostname == ALLOWED_SVG_HOST and urlparse(url).path.endswith(".svg"):
                embeds.setdefault(url, []).append({"page": page["path"], "order": index,
                                                     "type": element.get("type"), "outer_html": str(element)})
        for index, element in enumerate(soup.select("iframe[src]"), 1):
            url = element["src"]
            if urlparse(url).hostname != "www.googletagmanager.com":
                iframes.append({"page": page["path"], "order": index, "url": url,
                                "title": element.get("title"), "outer_html": str(element),
                                "archive_status": "external_dynamic_embed_url_and_screenshot_only"})
    records = []
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp(cdp)
        context = browser.contexts[0]
        tab = context.new_page()
        for index, (url, occurrences) in enumerate(embeds.items(), 1):
            response = tab.goto(url, wait_until="commit", timeout=30000)
            content = response.body()
            root = ElementTree.fromstring(content)
            if root.tag.rsplit("}", 1)[-1].lower() != "svg":
                raise RuntimeError(f"Not SVG: {url}")
            if response.status != 200:
                raise RuntimeError(f"HTTP {response.status}: {url}")
            sha = hashlib.sha256(content).hexdigest()
            local = Path("supplemental-media") / f"{sha}.svg"
            path = snapshot / local
            path.parent.mkdir(exist_ok=True)
            if not path.exists():
                with path.open("xb") as file:
                    file.write(content)
            records.append({"id": f"embed-svg-{index:03d}", "url": url, "status": response.status,
                            "content_type": response.headers.get("content-type"),
                            "archive_file": str(local).replace("\\", "/"), "bytes": len(content),
                            "sha256": sha, "format": "SVG", "occurrences": occurrences,
                            "source_credit": "open", "rights": "open"})
            print(f"SVG {index}/{len(embeds)} HTTP {response.status} {len(content)} bytes", flush=True)
        tab.close()
        browser.close()
    result = {"snapshot": str(snapshot.relative_to(ROOT)).replace("\\", "/"),
              "svg_embeds": records, "external_iframes": iframes}
    with (snapshot / "supplement-embeds.json").open("x", encoding="utf-8", newline="\n") as file:
        json.dump(result, file, ensure_ascii=False, indent=2)
        file.write("\n")
    print(f"SUPPLEMENT SVG={len(records)} external_iframes={len(iframes)}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cdp", required=True)
    parser.add_argument("--snapshot", type=Path, required=True)
    args = parser.parse_args()
    main(args.cdp, args.snapshot.resolve())
