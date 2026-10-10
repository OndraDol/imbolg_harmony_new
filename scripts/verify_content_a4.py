"""Check content against untouched A2 with individually authorized text changes."""

from __future__ import annotations

import argparse
import copy
import hashlib
import json
import re
import sys
from pathlib import Path

from bs4 import BeautifulSoup
from PIL import Image


ROOT = Path(__file__).resolve().parents[1]
PAGES = json.loads((ROOT / "evidence/pages.json").read_text(encoding="utf-8"))["pages"]
MEDIA = json.loads((ROOT / "evidence/media.json").read_text(encoding="utf-8"))["media"]
ALT = json.loads((ROOT / "src/content/media-alt.json").read_text(encoding="utf-8"))
SOURCE_MAP = json.loads((ROOT / "evidence/source-map.json").read_text(encoding="utf-8"))
BASE = "https://www.imbolg-harmony.cz"
errors = []

# Owner feedback supplied by the user on 2026-10-07; implementation and Pages
# publication explicitly authorized. Never replace the independent A2 evidence.
APPROVED_TEXT_CHANGES = {
    "feny-node-010": {
        "path": "/feny/",
        "block_id": "feny-block-002",
        "before": "BZ: 4x I. cena, CACT, res.CACT, Klubový vítěz\u00a0",
        "after": "BZ: 5x I. cena, CACT, res.CACT, Klubový vítěz\u00a0",
    },
}

# Exact user-approved UX text changes, 2026-10-10. A2 stays immutable.
APPROVED_TEXT_CHANGES.update({'home-node-003': {'path': '/',
                   'block_id': 'home-block-002',
                   'before': '"Péče o beagle"',
                   'after': 'Péče o beagle'},
 'home-node-005': {'path': '/',
                   'block_id': 'home-block-004',
                   'before': '"Výcvik pro beagly"',
                   'after': 'Výcvik pro beagly'},
 'home-node-006': {'path': '/',
                   'block_id': 'home-block-004',
                   'before': '"Péče o plemeno"',
                   'after': 'Péče o plemeno'},
 'home-node-007': {'path': '/',
                   'block_id': 'home-block-004',
                   'before': '"Poradenství pro nové majitele"',
                   'after': 'Poradenství pro nové majitele'},
 'home-node-018': {'path': '/', 'block_id': None, 'before': 'Odeslat', 'after': 'Odeslat zprávu'},
 'home-node-020': {'path': '/',
                   'block_id': None,
                   'before': 'www.facebook.com/profile.php?id=61571597523226',
                   'after': 'Imbolg Harmony na Facebooku'},
 'sluzby-node-001': {'path': '/sluzby/',
                     'block_id': 'sluzby-block-001',
                     'before': '"Výcvik pro beagly"',
                     'after': 'Chov a péče o beagle'},
 'sluzby-node-003': {'path': '/sluzby/',
                     'block_id': 'sluzby-block-003',
                     'before': '"Péče o plemeno"',
                     'after': 'Výcvik pro beagly'},
 'sluzby-node-005': {'path': '/sluzby/',
                     'block_id': 'sluzby-block-005',
                     'before': '"Poradenství pro nové majitele"',
                     'after': 'Péče o plemeno'},
 'kontakt-node-008': {'path': '/kontakt/',
                      'block_id': 'kontakt-block-005',
                      'before': 'https://www.facebook.com/profile.php?id=61571597523226',
                      'after': 'Imbolg Harmony na Facebooku'}})

# User-approved C2 notice is an addition inside the existing form, not a
# replacement for independent A2 page evidence.
APPROVED_FORM_NOTICE = (
    "Správcem údajů z formuláře je Markéta Kunešová, Myslbekova 559, 407 21 Česká Kamenice, kontakt kralovamarket@seznam.cz. "
    "Jméno, e-mail a případnou zprávu použijeme k vyřízení vašeho dotazu. "
    "U poptávky koupě nebo služby jde o přípravu případné smlouvy na vaši žádost; u obecných dotazů o náš oprávněný zájem odpovědět na vámi zahájenou komunikaci. "
    "Formulář používá hosting Gigaserver a poštovní službu Seznam. "
    "Běžnou uzavřenou komunikaci uchováme nejdéle šest měsíců od vyřízení, poté ji odstraníme; pro zprávy potřebné ke smlouvě, zákonným povinnostem nebo konkrétnímu nároku platí odpovídající samostatný účel. "
    "Na uvedeném kontaktu můžete uplatnit svá práva na přístup, opravu, výmaz či omezení a podle podmínek zpracování přenositelnost nebo námitku. "
    "Můžete se také obrátit na Úřad pro ochranu osobních údajů."
)


def check(condition: bool, message: str) -> None:
    if not condition:
        errors.append(message)


def hash_of(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def norm(value: str) -> str:
    return re.sub(r"\s+", " ", value.replace("\u00a0", " ")).strip()



def verify_ux_additions(main, route):
    """Validate each exact addition and its location before comparing unchanged A2 text."""
    expected = {}
    headings = {"/": "Imbolg Harmony", "/sluzby/": "Služby", "/feny/": "Feny", "/psi/": "Psi"}
    if route in headings:
        expected["page-heading"] = (f'<h1 class="visually-hidden" data-ux-addition="page-heading">{headings[route]}</h1>', "main")
    wa = 'href="https://wa.me/420775935130">Napsat na WhatsApp</a>'
    if route == "/":
        expected["home-whatsapp"] = ('<a class="contact-action" data-ux-addition="home-whatsapp" '+wa, '[data-block-id="home-block-009"]')
        expected["form-intro"] = ('<p data-ux-addition="form-intro">Údaje z formuláře použijeme k vyřízení vašeho dotazu.</p>', 'form.contact-form')
        expected["form-summary"] = ('<summary data-ux-addition="form-summary">Informace o zpracování údajů</summary>', 'details.form-privacy')
    if route == "/kontakt/":
        expected["contact-whatsapp"] = ('<a class="contact-action" data-ux-addition="contact-whatsapp" '+wa, '[data-block-id="kontakt-block-003"]')
        expected["contact-map"] = ('<a class="contact-action" data-ux-addition="contact-map" href="https://www.google.com/maps/search/?api=1&amp;query=Myslbekova%20559%2C%20407%2021%20%C4%8Cesk%C3%A1%20Kamenice">Otevřít v mapách</a>', '[data-block-id="kontakt-block-002"]')
    if route == "/cenik/":
        expected["price-contact"] = ('<a class="contact-action" data-ux-addition="price-contact" href="/kontakt/">Domluvit cenu</a>', '[data-block-id="cenik-block-003"]')
    actual = main.select("[data-ux-addition]")
    check(sorted(n["data-ux-addition"] for n in actual) == sorted(expected), f"{route}: nesprávné UX doplňky.")
    for node in actual:
        item = expected.get(node["data-ux-addition"])
        if item:
            markup, parent = item
            check(str(node) == str(BeautifulSoup(markup, "html.parser").find()), f"{route}: změněný UX doplněk {node['data-ux-addition']}.")
            container = main if parent == "main" else main.select_one(parent)
            check(node.parent is container, f"{route}: chybné umístění UX doplňku {node['data-ux-addition']}.")
        node.decompose()

def approved_expected_text(value: str, changes: list[dict], label: str) -> str:
    """Apply exact changes to expected text only, rejecting a changed baseline."""
    text = norm(value)
    for change in changes:
        before, after = norm(change["before"]), norm(change["after"])
        check(text.count(before) == 1, f"{label}: schválená změna nemá právě jeden původní výskyt.")
        text = text.replace(before, after, 1)
    return text


def image_urls(medium: dict) -> dict:
    stem = f"/assets/images/{medium['id']}"
    if medium["selected_original"]["format"] == "SVG":
        return {"full": stem + ".svg", "src": stem + ".svg"}
    return {"full": stem + ".jpg", "src": stem + "-700.webp"}


def expected_href(href: str, media_by_url: dict) -> str:
    if href in media_by_url:
        return image_urls(media_by_url[href])["full"]
    if href.startswith(BASE + "/"):
        return href.removeprefix(BASE)
    return href


def verify_media(dist: Path, mapped_media: dict) -> None:
    check(len(MEDIA) == 47, "A2 nemá očekávaných 47 logických médií.")
    check(set(mapped_media) == {m["id"] for m in MEDIA}, "source-map: seznam médií není shodný s A2.")
    for medium in MEDIA:
        mid = medium["id"]
        original = medium["selected_original"]
        source = ROOT / "archive/2026-10-06T13-40-23Z" / original["archive_file"]
        check(source.is_file(), f"{mid}: chybí archivní zdroj.")
        if source.is_file():
            check(hash_of(source) == original["sha256"], f"{mid}: změnil se archivní hash.")
        mapped = mapped_media.get(mid, {})
        urls = image_urls(medium)
        check(mapped.get("source_sha256") == original["sha256"], f"{mid}: mapa má jiný zdrojový hash.")
        check(mapped.get("public", {}).get("full") == urls["full"], f"{mid}: mapa vede na jiný plný soubor.")
        full = dist / urls["full"].lstrip("/")
        check(full.is_file(), f"{mid}: chybí lokální plný soubor.")
        if not full.is_file():
            continue
        check(hash_of(full) == original["sha256"], f"{mid}: plný soubor se liší od A2.")
        check(mapped.get("public_sha256") == hash_of(full), f"{mid}: mapa má jiný výstupní hash.")
        if original["format"] == "SVG":
            continue
        with Image.open(full) as photo:
            check(list(photo.size) == original["dimensions"], f"{mid}: jiné rozměry plného snímku.")
        for width in (700, 1400):
            variant = dist / f"assets/images/{mid}-{width}.webp"
            check(variant.is_file(), f"{mid}: chybí varianta {width}.")
            if variant.is_file():
                with Image.open(variant) as image:
                    check(image.format == "WEBP" and image.width <= width and image.height > 0,
                          f"{mid}: vadná varianta {width}.")


def verify_page(page: dict, mapped: dict, dist: Path, media_by_id: dict, media_by_url: dict) -> None:
    route = page["path"]
    output = dist / ("index.html" if route == "/" else route.strip("/") + "/index.html")
    if not output.is_file():
        errors.append(f"{route}: chybí HTML.")
        return
    html = output.read_text(encoding="utf-8")
    soup = BeautifulSoup(html, "html.parser")
    main = soup.find("main")
    if not main:
        errors.append(f"{route}: chybí main.")
        return
    check("clvaw-cdnwnd.com" not in html and "duyn491kcolsw.cloudfront.net" not in html,
          f"{route}: zůstal vzdálený zdroj fotografie nebo ikony.")
    check(mapped.get("source_page_id") == page["id"] and mapped.get("target_path") == route,
          f"{route}: chybná mapa stránky.")
    check(len(mapped.get("text_nodes", [])) == len(page["text_nodes"]), f"{route}: mapa textových uzlů není úplná.")
    verify_ux_additions(main, route)
    actual_nodes = main.select("[data-content-id]")
    expected_ids = [n["id"] for n in page["text_nodes"]]
    changes = {node_id: change for node_id, change in APPROVED_TEXT_CHANGES.items()
               if change["path"] == route}
    for node_id, change in changes.items():
        source_nodes = [n for n in page["text_nodes"] if n["id"] == node_id]
        check(len(source_nodes) == 1 and source_nodes[0]["raw_text"] == change["before"],
              f"{node_id}: původní text schválené změny neodpovídá A2.")
        check(sum(b["id"] == change["block_id"] for b in page["content_blocks"]) == (1 if change["block_id"] else 0),
              f"{node_id}: původní blok schválené změny není jednoznačný.")
    check([n.get("data-content-id") for n in actual_nodes] == expected_ids,
          f"{route}: textové uzly chybí nebo mají jiné pořadí.")
    for actual, expected in zip(actual_nodes, page["text_nodes"]):
        target_text = changes.get(expected["id"], {}).get("after", expected["raw_text"])
        check(norm(actual.get_text()) == norm(target_text), f"{expected['id']}: rozdíl textu.")
    actual_blocks = main.select("[data-block-id]")
    expected_blocks = page["content_blocks"]
    check([b.get("data-block-id") for b in actual_blocks] == [b["id"] for b in expected_blocks],
          f"{route}: editorové bloky chybí nebo mají jiné pořadí.")
    for actual, expected in zip(actual_blocks, expected_blocks):
        block_changes = [c for c in changes.values() if c["block_id"] == expected["id"]]
        target_text = approved_expected_text(expected["text"], block_changes, expected["id"])
        check(norm(actual.get_text("\n")) == target_text, f"{expected['id']}: rozdíl bloku.")

    original_main = BeautifulSoup((ROOT / Path(page["archive"]["rendered_dom"])).read_text(encoding="utf-8"), "html.parser").find("main")
    target_main = approved_expected_text(original_main.get_text(" "), list(changes.values()), route)
    main_without_notice = copy.deepcopy(main)
    notices = main_without_notice.select(".form-privacy")
    check(len(notices) == (1 if route == "/" else 0), f"{route}: nesprávný počet informací u formuláře.")
    if route == "/" and len(notices) == 1:
        notice = notices[0]
        form = notice.find_parent("form")
        check(form is not None and form.get("action") == "/api/contact.php"
              and notice.find_next_sibling("button") is not None,
              "Úvod: informace není před tlačítkem kontaktního formuláře.")
        check(notice.name == "details" and notice.attrs == {"class": ["form-privacy"]},
              "Informace musí být dostupné nativní zavřené details bez skrytí.")
        check(len(notice.find_all("p", recursive=False)) == 2
              and norm(notice.get_text(" ")) == norm(APPROVED_FORM_NOTICE),
              "Úvod: informace u formuláře není přesné schválené znění.")
    for notice in notices:
        notice.decompose()
    check(norm(main_without_notice.get_text(" ")) == target_main,
          f"{route}: celkový viditelný text main se liší od A2.")
    expected_images = page["image_occurrences"]
    actual_images = soup.select("img[data-media-order]")
    check([(i.get("data-media-id"), int(i.get("data-media-order", 0))) for i in actual_images]
          == [(i["media_id"], i["order"]) for i in expected_images],
          f"{route}: obrázkové výskyty nebo pořadí nejsou shodné s A2.")
    for image in actual_images:
        mid = image["data-media-id"]
        check(image.get("src") == image_urls(media_by_id[mid])["src"], f"{route}: {mid} má chybný lokální src.")
        if image.find_parent("main"):
            check(image.get("alt") == ALT[mid], f"{route}: {mid} nemá ověřený technický alt.")

    expected_gallery = [(g["id"], item["order"], item["media_id"])
                        for g in page["galleries"] for item in g["items"]]
    actual_gallery = [(a.get("data-gallery-id"), int(a.get("data-gallery-order", 0)), a.get("data-media-id"))
                      for a in main.select("a[data-gallery-id]")]
    check(actual_gallery == expected_gallery, f"{route}: položky galerie nebo pořadí se liší.")
    for anchor in main.select("a[data-gallery-id]"):
        mid = anchor["data-media-id"]
        check(anchor.get("href") == image_urls(media_by_id[mid])["full"],
              f"{route}: {mid} neotvírá lokální plnou fotografii.")

    expected_main_links = [l for l in page["links"] if l["in_main"]]
    actual_main_links = main.select("a[data-link-id]")
    check([a.get("data-link-id") for a in actual_main_links]
          == [f"{page['id']}-link-{l['order']:03d}" for l in expected_main_links],
          f"{route}: obsahové odkazy chybí nebo mají jiné pořadí.")
    for anchor, source in zip(actual_main_links, expected_main_links):
        target = expected_href(source["href"], media_by_url)
        check(anchor.get("href") == target, f"{route}: odkaz #{source['order']} má jiný cíl.")
        link_changes = [c for c in changes.values() if norm(c["before"]) == norm(source["text"])]
        check(norm(anchor.get_text(" ")) == approved_expected_text(source["text"], link_changes, f"link {source['order']}"),
              f"{route}: odkaz #{source['order']} má jiný text.")

    mapped_links = mapped.get("links", [])
    check(len(mapped_links) == len(page["links"]), f"{route}: mapa odkazů není úplná.")
    for link, source in zip(mapped_links, page["links"]):
        excluded = not source["in_main"] and source["href"] == "#"
        check(link.get("source_href") == source["href"] and link.get("source_order") == source["order"],
              f"{route}: mapa odkazu #{source['order']} neodpovídá A2.")
        check(link.get("excluded_technical") == excluded, f"{route}: chybná výluka odkazu #{source['order']}.")
        check(link.get("target_href") == (None if excluded else expected_href(source["href"], media_by_url)),
              f"{route}: mapa cíle odkazu #{source['order']} nesouhlasí.")
    pexels = soup.select('footer a[href="https://pexels.com"]')
    check(len(pexels) == 1 and norm(pexels[0].get_text()) == "Pexels", f"{route}: chybí původní kredit Pexels.")
    for anchor in soup.select("a[href]"):
        href = anchor["href"]
        if not href.startswith("/"):
            continue
        local = dist / href.split("#", 1)[0].split("?", 1)[0].lstrip("/")
        expected_file = local / "index.html" if href.endswith("/") else local
        check(expected_file.is_file(), f"{route}: interní odkaz má chybějící cíl {href}.")

    expected_svg = [e for e in page["embedded_resources"] if e["kind"] == "svg"]
    actual_svg = main.select("img[data-embed-order]")
    check([(i.get("data-media-id"), int(i.get("data-embed-order", 0))) for i in actual_svg]
          == [(e["media_id"], e["order"]) for e in expected_svg],
          f"{route}: SVG ikony kontaktu nejsou úplné.")
    expected_iframe = [e["url"] for e in page["embedded_resources"] if e["kind"] == "iframe"]
    check([i.get("src") for i in main.select("iframe")] == expected_iframe,
          f"{route}: URL vložené mapy se liší.")
    if page["forms"]:
        forms = main.select('form[action="/api/contact.php"][method="post"]')
        check(len(forms) == len(page["forms"]), f"{route}: chybí formulář A5.")
        if forms:
            fields = [forms[0].select_one(f'[name="{name}"]') for name in ("name", "email", "message")]
            expected = page["forms"][0]["fields"][:3]
            for field, source in zip(fields, expected):
                check(field is not None and field.has_attr("required") == source["required"]
                      and not field.has_attr("disabled"), f"{route}: pole či required formuláře se liší od A2.")
    if route == "/kontakt/":
        check(len(main.select('a[href="tel:+420775935130"]')) == 1, "Kontakt: telefon není dostupný přes tel.")
        check(len(main.select('a[href="mailto:kralovamarket@seznam.cz"]')) == 1,
              "Kontakt: e-mail není dostupný přes mailto.")


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dist", type=Path, default=ROOT / "dist")
    args = parser.parse_args()
    dist = args.dist.resolve()
    media_by_id = {m["id"]: m for m in MEDIA}
    media_by_url = {v["url"]: m for m in MEDIA for v in m["variants"]}
    mapped_media = {m["id"]: m for m in SOURCE_MAP["media"]}
    mapped_pages = {p["target_path"]: p for p in SOURCE_MAP["pages"]}
    check(SOURCE_MAP.get("source_snapshot") == "archive/2026-10-06T13-40-23Z",
          "source-map: jiný snímek A2.")
    check(set(mapped_pages) == {p["path"] for p in PAGES}, "source-map: chybí stránka nebo přebývá jiná.")
    check({c["path"] for c in APPROVED_TEXT_CHANGES.values()} <= {p["path"] for p in PAGES},
          "Schválená textová změna míří na chybějící stránku.")
    verify_media(dist, mapped_media)
    for page in PAGES:
        verify_page(page, mapped_pages.get(page["path"], {}), dist, media_by_id, media_by_url)
    counts = {"pages": len(PAGES), "text_nodes": sum(len(p["text_nodes"]) for p in PAGES),
              "blocks": sum(len(p["content_blocks"]) for p in PAGES), "media": len(MEDIA),
              "occurrences": sum(len(m["occurrences"]) for m in MEDIA),
              "gallery_items": sum(len(g["items"]) for p in PAGES for g in p["galleries"]),
              "links": sum(len(p["links"]) for p in PAGES)}
    print(json.dumps({**counts, "approved_text_changes": list(APPROVED_TEXT_CHANGES), "errors": errors}, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
