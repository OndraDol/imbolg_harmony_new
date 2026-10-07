"""Verify A2 evidence against the independent archived source files.

Run: python scripts/verify_a2.py archive/<timestamp>
"""

import argparse
import hashlib
import io
import json
from pathlib import Path
from urllib.parse import urlparse
from xml.etree import ElementTree

from bs4 import BeautifulSoup, NavigableString
from PIL import Image, ImageChops


ROOT = Path(__file__).resolve().parents[1]


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main(snapshot):
    capture = json.loads((snapshot / "capture.json").read_text(encoding="utf-8"))
    pages = json.loads((ROOT / "evidence/pages.json").read_text(encoding="utf-8"))["pages"]
    media = json.loads((ROOT / "evidence/media.json").read_text(encoding="utf-8"))["media"]
    errors = list(capture["errors"])
    sitemap = set(capture["sitemap_paths"])
    crawled = {page["path"] for page in pages}
    if sitemap != crawled:
        errors.append({"sitemap_difference": sorted(sitemap ^ crawled)})
    internal = set()
    gallery_items = 0
    for page in pages:
        original = next(x for x in capture["pages"] if x["path"] == page["path"])
        for kind, expected in (("raw_html", "raw_sha256"), ("rendered_dom", "rendered_sha256")):
            path = ROOT / page["archive"][kind]
            if not path.is_file() or sha(path) != page["archive"][expected]:
                errors.append({"page": page["path"], "archive_integrity": kind})
        for kind in ("desktop_screenshot", "mobile_screenshot"):
            path = ROOT / page["archive"][kind]
            try:
                with Image.open(path) as picture:
                    picture.verify()
                with Image.open(path) as picture:
                    expected_width = 1440 if kind == "desktop_screenshot" else 390
                    if picture.width != expected_width:
                        errors.append({"page": page["path"], "screenshot_width": [kind, picture.width]})
            except Exception as exc:
                errors.append({"page": page["path"], "screenshot": kind, "error": str(exc)})
        soup = BeautifulSoup((ROOT / page["archive"]["rendered_dom"]).read_text(encoding="utf-8"), "html.parser")
        main_element = soup.find("main") or soup.body
        dom_text = [str(node) for node in main_element.descendants if isinstance(node, NavigableString)
                    and str(node).strip() and not any(ancestor.name in {"script", "style", "noscript"} for ancestor in node.parents)]
        if dom_text != [node["raw_text"] for node in page["text_nodes"]]:
            errors.append({"page": page["path"], "text_node_order_mismatch": True})
        shell_text = [str(node) for node in soup.body.descendants if isinstance(node, NavigableString)
                      and str(node).strip() and main_element not in node.parents
                      and not any(ancestor.name in {"script", "style", "noscript"} for ancestor in node.parents)]
        if shell_text != [node["raw_text"] for node in page["shell_text_nodes"]]:
            errors.append({"page": page["path"], "shell_text_node_order_mismatch": True})
        dom_blocks = [element.decode_contents() for element in main_element.select(".b-text-c")]
        if dom_blocks != [block["html"] for block in page["content_blocks"]]:
            errors.append({"page": page["path"], "content_block_mismatch": True})
        if [element.get("href") for element in soup.select("a[href]")] != [link["href"] for link in page["links"]]:
            errors.append({"page": page["path"], "link_order_mismatch": True})
        dom_images = soup.find_all("img")
        if len(dom_images) != len(page["image_occurrences"]):
            errors.append({"page": page["path"], "img_count": [len(dom_images), len(page["image_occurrences"])]})
        dom_gallery = soup.select("a.b-gal-a")
        listed_gallery = [item for gal in page["galleries"] for item in gal["items"]]
        gallery_items += len(listed_gallery)
        if [a.get("href") for a in dom_gallery] != [item["href"] for item in listed_gallery]:
            errors.append({"page": page["path"], "gallery_order_mismatch": True})
        if len(page["text_nodes"]) == 0 or len(page["content_blocks"]) == 0:
            errors.append({"page": page["path"], "text_missing": True})
        dom_svg = [x["src"] for x in soup.select("embed[src]")]
        listed_svg = [x["url"] for x in page["embedded_resources"] if x["kind"] == "svg"]
        if dom_svg != listed_svg:
            errors.append({"page": page["path"], "embedded_svg_mismatch": True})
        dom_iframe = [x["src"] for x in soup.select("iframe[src]") if "googletagmanager.com" not in x["src"]]
        listed_iframe = [x["url"] for x in page["embedded_resources"] if x["kind"] == "iframe"]
        if dom_iframe != listed_iframe:
            errors.append({"page": page["path"], "embedded_iframe_mismatch": True})
        for link in page["links"]:
            parsed = urlparse(link["resolved"])
            if parsed.hostname == "www.imbolg-harmony.cz" and parsed.path.endswith("/"):
                internal.add(parsed.path)
        if original["status"] != 200:
            errors.append({"page": page["path"], "http": original["status"]})
    if internal != sitemap:
        errors.append({"internal_links_sitemap_difference": sorted(internal ^ sitemap)})
    media_urls = {record["url"] for record in capture["media"]}
    for medium in media:
        original = medium["selected_original"]
        if not original or (original["url"] not in media_urls and original.get("format") != "SVG"):
            errors.append({"media": medium["id"], "missing_original": True})
            continue
        image_file = snapshot / original["archive_file"]
        if not image_file.is_file() or sha(image_file) != original["sha256"]:
            errors.append({"media": medium["id"], "file_integrity": True})
            continue
        try:
            if original.get("format") == "SVG":
                if ElementTree.parse(image_file).getroot().tag.rsplit("}", 1)[-1].lower() != "svg":
                    errors.append({"media": medium["id"], "format": "not_svg"})
            else:
                with Image.open(image_file) as picture:
                    picture.verify()
                with Image.open(image_file) as picture:
                    if list(picture.size) != original["dimensions"] or picture.format != original["format"]:
                        errors.append({"media": medium["id"], "dimensions_or_format": True})
        except Exception as exc:
            errors.append({"media": medium["id"], "unreadable": str(exc)})
        if original["status"] != 200:
            errors.append({"media": medium["id"], "http": original["status"]})
        # A variant with a different aspect ratio may be a different crop and needs visual review.
        for variant in medium["variants"]:
            archived = variant["archived"]
            if not archived or original.get("format") == "SVG":
                continue
            width, height = archived["dimensions"]
            ow, oh = original["dimensions"]
            if abs(width / height - ow / oh) > 0.015:
                errors.append({"media": medium["id"], "variant_crop": variant["url"]})
    for record in capture["media"]:
        path = snapshot / record["archive_file"]
        if not path.is_file() or sha(path) != record["sha256"] or path.stat().st_size != record["bytes"]:
            errors.append({"media_url": record["url"], "archive_integrity": True})
    gallery_check = snapshot / "gallery-browser-check.json"
    if not gallery_check.is_file():
        errors.append({"gallery_browser_check": "missing"})
    else:
        checks = json.loads(gallery_check.read_text(encoding="utf-8"))
        for check in checks:
            if check["counters"] != [f"{i} / {check['dom_items']}" for i in range(1, check["dom_items"] + 1)] or not check["all_images_loaded"]:
                errors.append({"gallery_browser_check": check["gallery_id"]})
    print(json.dumps({"pages": len(pages), "sitemap_paths": len(sitemap),
                      "text_nodes": sum(len(page["text_nodes"]) for page in pages),
                      "shell_text_nodes": sum(len(page["shell_text_nodes"]) for page in pages),
                      "content_blocks": sum(len(page["content_blocks"]) for page in pages),
                      "links": sum(len(page["links"]) for page in pages),
                      "gallery_items": gallery_items, "logical_media": len(media),
                      "svg_embeds": sum(1 for medium in media if medium["selected_original"].get("format") == "SVG"),
                      "external_iframes": sum(1 for page in pages for item in page["embedded_resources"] if item["kind"] == "iframe"),
                      "media_occurrences": sum(len(medium["occurrences"]) for medium in media),
                      "media_urls": len(capture["media"]), "errors": errors}, ensure_ascii=False, indent=2))
    if errors:
        raise SystemExit(1)


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot", type=Path)
    main(parser.parse_args().snapshot.resolve())
