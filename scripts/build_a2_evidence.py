"""Build public A2 evidence from an immutable browser capture.

Run: python scripts/build_a2_evidence.py archive/<timestamp>
Never changes the captured source. Refuses to overwrite evidence files.
"""

import argparse
import hashlib
import json
from pathlib import Path
from urllib.parse import urljoin

from bs4 import BeautifulSoup, NavigableString


ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / "evidence"
BASE = "https://www.imbolg-harmony.cz"


def write_json_new(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("x", encoding="utf-8", newline="\n") as file:
        json.dump(value, file, ensure_ascii=False, indent=2)
        file.write("\n")


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def page_prefix(path):
    return "home" if path == "/" else path.strip("/").replace("/", "-")


def split_srcset(value):
    return [part.strip().split()[0] for part in (value or "").split(",") if part.strip()]


def main(snapshot):
    capture = json.loads((snapshot / "capture.json").read_text(encoding="utf-8"))
    supplement_path = snapshot / "supplement-embeds.json"
    supplement = json.loads(supplement_path.read_text(encoding="utf-8")) if supplement_path.is_file() else {"svg_embeds": [], "external_iframes": []}
    downloaded = {item["url"]: item for item in capture["media"]}
    pages = []
    logical_media = {}
    media_order = []

    def media_for(url):
        if url not in logical_media:
            media_id = f"media-{len(logical_media)+1:03d}"
            logical_media[url] = {"id": media_id, "source_url": url, "variants": [],
                                  "selected_original": downloaded.get(url), "occurrences": [],
                                  "source_credit": "open", "rights": "open",
                                  "rights_note": "Veřejný web uvádí obecný kredit Pexels; přiřazení ke konkrétnímu souboru není doložené."}
            media_order.append(url)
        return logical_media[url]

    for page in capture["pages"]:
        prefix = page_prefix(page["path"])
        dom_path = snapshot / page["rendered_dom"]
        soup = BeautifulSoup(dom_path.read_text(encoding="utf-8"), "html.parser")
        main_element = soup.find("main") or soup.body
        elements = {id(el): index + 1 for index, el in enumerate(main_element.find_all(True))}
        content_blocks = []
        for index, element in enumerate(main_element.select(".b-text-c"), 1):
            content_blocks.append({"id": f"{prefix}-block-{index:03d}",
                                   "dom_order": elements.get(id(element)), "html": element.decode_contents(),
                                   "text": element.get_text("\n", strip=False)})
        text_nodes = []
        for node in main_element.descendants:
            if not isinstance(node, NavigableString) or not str(node).strip():
                continue
            if any(ancestor.name in {"script", "style", "noscript"} for ancestor in node.parents):
                continue
            parent = node.parent
            text_nodes.append({"id": f"{prefix}-node-{len(text_nodes)+1:03d}",
                               "dom_order": elements.get(id(parent)), "parent_tag": parent.name,
                               "parent_class": parent.get("class", []), "raw_text": str(node)})
        shell_text_nodes = []
        for node in soup.body.descendants:
            if not isinstance(node, NavigableString) or not str(node).strip() or main_element in node.parents:
                continue
            if any(ancestor.name in {"script", "style", "noscript"} for ancestor in node.parents):
                continue
            parent = node.parent
            region = "header" if parent.find_parent("header") else "footer" if parent.find_parent("footer") else "other"
            shell_text_nodes.append({"id": f"{prefix}-shell-{len(shell_text_nodes)+1:03d}",
                                     "region": region, "parent_tag": parent.name,
                                     "parent_class": parent.get("class", []), "raw_text": str(node)})
        image_occurrences = []
        for image in page["images"]:
            url = urljoin(BASE, image["src"] or image["current_src"] or "")
            if not url.startswith("http"):
                continue
            medium = media_for(url)
            variants = [url]
            if image["current_src"]:
                variants.append(image["current_src"])
            if image["picture"]:
                picture = BeautifulSoup(image["picture"], "html.parser")
                for source in picture.select("source[srcset]"):
                    variants.extend(urljoin(BASE, item) for item in split_srcset(source["srcset"]))
            medium["variants"] = list(dict.fromkeys(medium["variants"] + variants))
            occurrence = {"page": page["path"], "kind": "img", "order": image["order"],
                          "alt": image["alt"], "loading": image["loading"],
                          "html": image["outer_html"]}
            medium["occurrences"].append(occurrence)
            image_occurrences.append({"media_id": medium["id"], **occurrence})
        galleries = []
        for gallery in page["galleries"]:
            items = []
            for item in gallery["items"]:
                medium = media_for(item["href"])
                medium["occurrences"].append({"page": page["path"], "kind": "gallery",
                                              "gallery_id": gallery["id"], "order": item["order"],
                                              "caption": item["caption"]})
                items.append({"order": item["order"], "media_id": medium["id"],
                              "href": item["href"], "caption": item["caption"], "group": item["group"]})
            galleries.append({"id": gallery["id"], "order": gallery["order"], "items": items})
        pages.append({"id": f"{prefix}-page", "url": page["url"], "path": page["path"],
                      "captured_utc": capture["captured_utc"], "status": page["status"],
                      "title": page["title"], "description": page["description"],
                      "canonical": page["canonical"], "lang": page["lang"],
                      "archive": {"raw_html": str(snapshot.relative_to(ROOT) / page["raw_html"]),
                                  "raw_sha256": page["raw_sha256"],
                                  "rendered_dom": str(snapshot.relative_to(ROOT) / page["rendered_dom"]),
                                  "rendered_sha256": page["rendered_sha256"],
                                  "desktop_screenshot": str(snapshot.relative_to(ROOT) / "screenshots" / f"{prefix}-desktop.png"),
                                  "mobile_screenshot": str(snapshot.relative_to(ROOT) / "screenshots" / f"{prefix}-mobile.png")},
                      "main_text": page["main_text"], "content_blocks": content_blocks,
                      "text_nodes": text_nodes, "shell_text_nodes": shell_text_nodes,
                      "links": page["links"], "forms": page["forms"],
                      "menu": page["menu"], "galleries": galleries,
                      "image_occurrences": image_occurrences, "backgrounds": page["backgrounds"],
                      "embedded_resources": []})

    page_by_path = {page["path"]: page for page in pages}
    for embed in supplement["svg_embeds"]:
        medium = media_for(embed["url"])
        medium["selected_original"] = embed
        medium["variants"] = [embed["url"]]
        medium["rights_note"] = "Veřejně vložená SVG ikona Webnode; původ a právo pro nový web nejsou doložené."
        for occurrence in embed["occurrences"]:
            ref = {"page": occurrence["page"], "kind": "embed", "order": occurrence["order"]}
            medium["occurrences"].append(ref)
            page_by_path[occurrence["page"]]["embedded_resources"].append({"kind": "svg", "media_id": medium["id"],
                                                                               "url": embed["url"], "order": occurrence["order"]})
    for iframe in supplement["external_iframes"]:
        page_by_path[iframe["page"]]["embedded_resources"].append({"kind": "iframe", "url": iframe["url"],
                                                                      "order": iframe["order"],
                                                                      "archive_status": iframe["archive_status"]})

    for url in media_order:
        medium = logical_media[url]
        medium["variants"] = [{"url": variant, "archived": downloaded.get(variant) or (
            medium["selected_original"] if medium["selected_original"] and medium["selected_original"]["url"] == variant else None
        )} for variant in medium["variants"]]

    write_json_new(EVIDENCE / "pages.json", {"snapshot": str(snapshot.relative_to(ROOT)),
                                             "sitemap_paths": capture["sitemap_paths"], "pages": pages})
    write_json_new(EVIDENCE / "media.json", {"snapshot": str(snapshot.relative_to(ROOT)),
                                             "media": [logical_media[url] for url in media_order]})
    write_json_new(EVIDENCE / "exclusions.json", {
        "snapshot": str(snapshot.relative_to(ROOT)),
        "technical_exclusions": [
            {"item": "Webnode JavaScript a provozní skripty", "reason": "Provozní technika zdrojového systému; není autorský obsah."},
            {"item": "Cookie dialog a jeho technické ovládání", "reason": "Ovládací vrstva Webnode; právní texty a veřejné odkazy zůstávají v raw HTML a pages.json."},
            {"item": "GTM iframe a měřicí skripty", "reason": "Měřicí technika; archivovaný raw HTML dokládá přítomnost, nepřenáší se automaticky."}
        ],
        "preserved_public_material": ["Pexels kredit v patičce", "Veřejné odkazy a jejich cíle", "Formulářová pole a povinnost vyplnění", "Čtyři SVG ikony kontaktu", "URL a vykreslený snímek vložené mapy Google"],
        "note": "Výluky se týkají budoucí implementace; tento A2 archiv uchovává raw HTML včetně technických částí."
    })
    print("evidence pages", len(pages), "blocks", sum(len(p["content_blocks"]) for p in pages),
          "text nodes", sum(len(p["text_nodes"]) for p in pages),
          "shell text nodes", sum(len(p["shell_text_nodes"]) for p in pages),
          "logical media", len(logical_media), "media occurrences", sum(len(m["occurrences"]) for m in logical_media.values()))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot", type=Path)
    main(parser.parse_args().snapshot.resolve())
