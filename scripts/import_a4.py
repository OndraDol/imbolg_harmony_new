"""One-way A4 import from the immutable A2 public archive into local content."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString
from PIL import Image, ImageOps


ROOT = Path(__file__).resolve().parents[1]
PAGES = json.loads((ROOT / "evidence/pages.json").read_text(encoding="utf-8"))["pages"]
MEDIA = json.loads((ROOT / "evidence/media.json").read_text(encoding="utf-8"))["media"]
ALT = json.loads((ROOT / "src/content/media-alt.json").read_text(encoding="utf-8"))
CONTENT = ROOT / "src/content"
IMAGES = ROOT / "src/assets/images"
MAP = ROOT / "evidence/source-map.json"
BASE = "https://www.imbolg-harmony.cz"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def image_urls(medium: dict) -> dict:
    stem = f"/assets/images/{medium['id']}"
    if medium["selected_original"]["format"] == "SVG":
        return {"full": stem + ".svg", "src": stem + ".svg", "srcset": ""}
    return {"full": stem + ".jpg", "src": stem + "-700.webp",
            "srcset": f"{stem}-700.webp 700w, {stem}-1400.webp 1400w"}


def import_media() -> list[dict]:
    IMAGES.mkdir(parents=True, exist_ok=True)
    result = []
    for medium in MEDIA:
        original = medium["selected_original"]
        source = ROOT / "archive/2026-10-06T13-40-23Z" / original["archive_file"]
        if sha256(source) != original["sha256"]:
            raise ValueError(f"Invalid archived media: {medium['id']}")
        urls = image_urls(medium)
        full = ROOT / "src" / urls["full"].lstrip("/")
        if medium["selected_original"]["format"] == "SVG":
            if not full.is_file() or sha256(full) != original["sha256"]:
                full.write_bytes(source.read_bytes())
            dimensions = None
        else:
            with Image.open(source) as source_image:
                photo = ImageOps.exif_transpose(source_image).convert("RGB")
                dimensions = list(photo.size)
                # The full-sized locally served JPEG keeps the public source pixels.
                if not full.is_file() or sha256(full) != original["sha256"]:
                    full.write_bytes(source.read_bytes())
                for width in (700, 1400):
                    target = IMAGES / f"{medium['id']}-{width}.webp"
                    if target.is_file():
                        continue
                    variant = photo.copy()
                    variant.thumbnail((width, width * 4), Image.Resampling.LANCZOS)
                    variant.save(target, "WEBP", quality=82, method=6)
        result.append({"id": medium["id"], "source_url": medium["source_url"],
                       "archive_file": str(source.relative_to(ROOT)).replace("\\", "/"),
                       "source_sha256": original["sha256"], "public": urls,
                       "public_sha256": sha256(full), "dimensions": dimensions,
                       "source_credit": medium["source_credit"], "rights": medium["rights"],
                       "rights_note": medium["rights_note"]})
    return result


def expected_href(href: str, media_by_url: dict) -> str:
    if href in media_by_url:
        return image_urls(media_by_url[href])["full"]
    if href.startswith(BASE + "/"):
        return href.removeprefix(BASE)
    return href


def annotate_page(page: dict, media_by_id: dict, media_by_url: dict) -> tuple[str, dict]:
    dom = ROOT / Path(page["archive"]["rendered_dom"])
    if sha256(dom) != page["archive"]["rendered_sha256"]:
        raise ValueError(f"Invalid archived DOM: {page['path']}")
    soup = BeautifulSoup(dom.read_text(encoding="utf-8"), "html.parser")
    main = soup.find("main")
    if not main:
        raise ValueError(f"No main: {page['path']}")

    text_nodes = [node for node in main.descendants if isinstance(node, NavigableString)
                  and str(node).strip() and not any(a.name in {"script", "style", "noscript"} for a in node.parents)]
    if len(text_nodes) != len(page["text_nodes"]):
        raise ValueError(f"Text node count changed: {page['path']}")
    for node, evidence in zip(text_nodes, page["text_nodes"]):
        if str(node) != evidence["raw_text"]:
            raise ValueError(f"Text node differs: {evidence['id']}")
        marker = soup.new_tag("span")
        marker["data-content-id"] = evidence["id"]
        marker.string = str(node)
        node.replace_with(marker)
    blocks = main.select(".b-text-c")
    if len(blocks) != len(page["content_blocks"]):
        raise ValueError(f"Block count changed: {page['path']}")
    for block, evidence in zip(blocks, page["content_blocks"]):
        block["data-block-id"] = evidence["id"]

    links = soup.select("a[href]")
    if len(links) != len(page["links"]):
        raise ValueError(f"Link count changed: {page['path']}")
    link_map = []
    for anchor, evidence in zip(links, page["links"]):
        if anchor.get("href") != evidence["href"]:
            raise ValueError(f"Link differs: {page['path']} #{evidence['order']}")
        excluded = not evidence["in_main"] and (evidence["href"] == "#")
        target = expected_href(evidence["href"], media_by_url)
        link_id = f"{page['id']}-link-{evidence['order']:03d}"
        link_map.append({"id": link_id, "source_href": evidence["href"],
                         "target_href": None if excluded else target,
                         "source_order": evidence["order"], "in_main": evidence["in_main"],
                         "excluded_technical": excluded})
        if evidence["in_main"]:
            anchor["data-link-id"] = link_id
            anchor["href"] = target

    if page["path"] == "/kontakt/":
        for node_id, href in (("kontakt-node-006", "tel:+420775935130"),
                              ("kontakt-node-007", "mailto:kralovamarket@seznam.cz"),
                              ("kontakt-node-008", "https://www.facebook.com/profile.php?id=61571597523226")):
            marker = main.select_one(f'[data-content-id="{node_id}"]')
            marker.wrap(soup.new_tag("a", href=href))

    image_map = []
    images = soup.select("img")
    if len(images) != len(page["image_occurrences"]):
        raise ValueError(f"Image count changed: {page['path']}")
    for image, occurrence in zip(images, page["image_occurrences"]):
        medium = media_by_id[occurrence["media_id"]]
        public = image_urls(medium)
        image["data-media-id"] = medium["id"]
        image["data-media-order"] = str(occurrence["order"])
        image["src"] = public["src"]
        if public["srcset"]:
            image["srcset"] = public["srcset"]
            image["sizes"] = "(max-width: 48rem) 100vw, 48rem"
        image["width"], image["height"] = medium["selected_original"]["dimensions"]
        image["loading"] = "eager" if occurrence["order"] == 1 else "lazy"
        if main in image.parents:
            image["alt"] = ALT[medium["id"]]
        image_map.append({"media_id": medium["id"], "kind": "img", "order": occurrence["order"],
                          "target_src": public["src"], "region": "main" if main in image.parents else "header"})
        if main in image.parents and not image.find_parent("a"):
            enlargement = soup.new_tag("a", href=public["full"])
            enlargement["aria-label"] = "Zvětšit fotografii"
            image.wrap(enlargement)

    galleries = []
    for gallery in page["galleries"]:
        for item in gallery["items"]:
            candidates = main.find_all("a", href=image_urls(media_by_id[item["media_id"]])["full"])
            unused = [a for a in candidates if not a.has_attr("data-gallery-id")]
            if not unused:
                raise ValueError(f"Gallery item missing: {gallery['id']} #{item['order']}")
            anchor = unused[0]
            anchor["data-gallery-id"] = gallery["id"]
            anchor["data-gallery-order"] = str(item["order"])
            anchor["data-media-id"] = item["media_id"]
            grid = anchor.find_parent(class_="b-gal-grid")
            if grid:
                grid["data-gallery-grid"] = gallery["id"]
                anchor.parent["data-gallery-item"] = str(item["order"])
            galleries.append({"gallery_id": gallery["id"], "order": item["order"],
                              "media_id": item["media_id"], "target_href": anchor["href"]})

    embeds = []
    for embed, evidence in zip(main.select("embed"), [e for e in page["embedded_resources"] if e["kind"] == "svg"]):
        medium = media_by_id[evidence["media_id"]]
        if embed.get("src") != evidence["url"]:
            raise ValueError(f"SVG embed differs: {medium['id']}")
        image = soup.new_tag("img", src=image_urls(medium)["src"], alt="")
        image["data-media-id"] = medium["id"]
        image["data-embed-order"] = str(evidence["order"])
        embed.replace_with(image)
        embeds.append({"kind": "svg", "media_id": medium["id"], "order": evidence["order"],
                       "target_src": image["src"]})
    source_iframes = [e for e in page["embedded_resources"] if e["kind"] == "iframe"]
    for iframe, evidence in zip(main.select("iframe"), source_iframes):
        if iframe.get("src") != evidence["url"]:
            raise ValueError(f"Iframe differs: {page['path']}")
        iframe["title"] = "Mapa kontaktu"
        iframe["loading"] = "lazy"
        embeds.append({"kind": "iframe", "source_url": evidence["url"], "target_url": evidence["url"]})

    # The contact form transport is A5. Keep its visible wording without a live Webnode action.
    for form in main.select("form"):
        form.name = "div"
        form["data-form-pending"] = "A5"
        for button in form.select("button"):
            button["type"] = "button"
            button["disabled"] = ""

    for tag in list(main.find_all(["script", "style", "noscript", "source", "svg", "object"])):
        tag.decompose()
    for picture in list(main.find_all("picture")):
        picture.unwrap()
    allowed = {"href", "src", "srcset", "sizes", "width", "height", "alt", "loading", "title",
               "type", "name", "required", "disabled", "placeholder", "aria-label", "referrerpolicy",
               "data-content-id", "data-block-id", "data-link-id", "data-media-id", "data-media-order",
               "data-gallery-id", "data-gallery-order", "data-embed-order", "data-form-pending"}
    allowed.update({"data-gallery-grid", "data-gallery-item"})
    for tag in main.find_all(True):
        for key in list(tag.attrs):
            if key not in allowed:
                del tag[key]
        if tag.name == "a" and tag.get("href", "").startswith("https://454501af52.clvaw-cdnwnd.com"):
            raise ValueError(f"Remote image link remains: {page['path']}")
    for tag in main.find_all(["input", "textarea"]):
        tag["disabled"] = ""

    result = {"source_page_id": page["id"], "target_path": page["path"],
              "text_nodes": [{"id": n["id"], "target_selector": f'[data-content-id="{n["id"]}"]'} for n in page["text_nodes"]],
              "content_blocks": [{"id": b["id"], "target_selector": f'[data-block-id="{b["id"]}"]'} for b in page["content_blocks"]],
              "links": link_map, "images": image_map, "galleries": galleries, "embeds": embeds}
    return main.decode_contents(), result


def main() -> None:
    CONTENT.mkdir(parents=True, exist_ok=True)
    media_by_id = {m["id"]: m for m in MEDIA}
    media_by_url = {v["url"]: m for m in MEDIA for v in m["variants"]}
    media_map = import_media()
    page_map = []
    content = {}
    for page in PAGES:
        html, mapped = annotate_page(page, media_by_id, media_by_url)
        content[page["id"].removesuffix("-page")] = html
        page_map.append(mapped)
    (CONTENT / "pages.json").write_text(json.dumps(content, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    MAP.write_text(json.dumps({"source_snapshot": "archive/2026-10-06T13-40-23Z",
                               "pages": page_map, "media": media_map}, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(f"Imported {len(page_map)} pages, {len(media_map)} media, {sum(len(p['text_nodes']) for p in page_map)} text nodes")


if __name__ == "__main__":
    main()
