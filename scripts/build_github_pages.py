"""Create the explicitly approved static Pages copy; never change the PHP release."""
from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import re
import shutil
import stat
from xml.etree import ElementTree as ET

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "dist"
ARTIFACTS = ROOT / "artifacts/github-pages"
OUTPUT = ARTIFACTS / "preview/imbolg_harmony_new"
PREFIX = "/imbolg_harmony_new/"
SITE = "https://ondradol.github.io" + PREFIX
CONTACT = "kralovamarket@seznam.cz"
NOTE = "Formulář v této kopii webu zatím neodesílá. Napište na "
DISABLED_CSS = "\n/* Static Pages contact form */\n.pages-contact-note { margin-block: 1rem; }\n.contact-form button:disabled { cursor: not-allowed; opacity: .65; }\n"
EXTENSIONS = {".html", ".css", ".jpg", ".jpeg", ".png", ".webp", ".svg", ".gif", ".ico", ".woff", ".woff2"}


def safe_path(path):
    """Validate every existing component, including Windows junctions."""
    path = path.absolute()
    if path != ROOT and ROOT not in path.parents:
        raise ValueError(f"Outside workspace: {path}")
    for component in (path, *path.parents):
        if component.exists() or component.is_symlink():
            info = component.lstat()
            if stat.S_ISLNK(info.st_mode) or getattr(info, "st_file_attributes", 0) & stat.FILE_ATTRIBUTE_REPARSE_POINT:
                raise ValueError(f"Linked path is forbidden: {component}")
        if component == ROOT:
            break
    return path


def files_under(directory):
    safe_path(directory)
    result = []
    for path in directory.rglob("*"):
        safe_path(path)
        if path.is_file():
            result.append(path)
    return sorted(result)


def prefixed(url):
    return PREFIX + url[1:] if url.startswith("/") and not url.startswith("//") else url


def pages_html(text):
    soup = BeautifulSoup(text, "html.parser")
    for element in soup.find_all(True):
        for attribute in ("href", "src", "poster"):
            if element.has_attr(attribute):
                element[attribute] = prefixed(element[attribute])
        if element.has_attr("srcset"):
            candidates = []
            for candidate in element["srcset"].split(","):
                parts = candidate.strip().split()
                parts[0] = prefixed(parts[0])
                candidates.append(" ".join(parts))
            element["srcset"] = ", ".join(candidates)
    if not soup.select_one('meta[name="robots"]'):
        meta = soup.new_tag("meta", attrs={"name": "robots", "content": "noindex, follow", "data-pages-copy": "true"})
        soup.head.append(meta)
    forms = soup.select("form")
    for form in forms:
        if "contact-form" not in form.get("class", []):
            raise ValueError("Unexpected form in the static copy")
        form.attrs.pop("action", None)
        form.attrs.pop("method", None)
        form["data-pages-inactive"] = "true"
        form["aria-describedby"] = "pages-contact-note"
        for control in form.select("input, textarea, select, button"):
            control["disabled"] = ""
            if control.name == "button":
                control["type"] = "button"
        note = soup.new_tag("p", attrs={"id": "pages-contact-note", "class": "pages-contact-note", "data-pages-contact-note": "true"})
        note.append(NOTE)
        link = soup.new_tag("a", href="mailto:" + CONTACT)
        link.string = CONTACT
        note.append(link)
        note.append(".")
        form.insert_before(note)
    return str(soup)


def main():
    source_files = files_under(SOURCE)
    pages = json.loads((ROOT / "src/_data/sitePages.json").read_text(encoding="utf-8"))
    expected_html = {page["output"] for page in pages} | {"404.html"}
    actual_html = {p.relative_to(SOURCE).as_posix() for p in source_files if p.suffix == ".html"}
    if actual_html != expected_html:
        raise ValueError("The rebuilt source does not contain exactly the ten pages and 404")
    for path in source_files:
        relative = path.relative_to(SOURCE).as_posix()
        allowed = relative in expected_html | {"robots.txt", "sitemap.xml", ".htaccess"}
        allowed |= relative.startswith("assets/") and path.suffix.lower() in EXTENSIONS
        if not allowed:
            raise ValueError(f"Unexpected source file: {relative}")
    safe_path(OUTPUT)
    if OUTPUT.exists():
        files_under(OUTPUT)  # Refuse linked content before deleting this generated directory.
        if OUTPUT.resolve() != ROOT / "artifacts/github-pages/preview/imbolg_harmony_new":
            raise ValueError("Unexpected cleanup target")
        shutil.rmtree(OUTPUT, onexc=lambda function, path, error: (Path(path).chmod(0o700), function(path)))
    OUTPUT.mkdir(parents=True)
    for path in source_files:
        relative = path.relative_to(SOURCE)
        if relative.as_posix() == ".htaccess":
            continue
        target = OUTPUT / relative
        target.parent.mkdir(parents=True, exist_ok=True)
        if path.suffix == ".html":
            target.write_text(pages_html(path.read_text(encoding="utf-8")), encoding="utf-8", newline="\n")
        elif relative.as_posix() == "robots.txt":
            target.write_text("User-agent: *\nDisallow: /\nSitemap: " + SITE + "sitemap.xml\n", encoding="utf-8", newline="\n")
        elif relative.as_posix() == "sitemap.xml":
            namespace = "http://www.sitemaps.org/schemas/sitemap/0.9"
            ET.register_namespace("", namespace)
            sitemap = ET.Element(f"{{{namespace}}}urlset")
            for page in pages:
                url = ET.SubElement(sitemap, f"{{{namespace}}}url")
                ET.SubElement(url, f"{{{namespace}}}loc").text = SITE + page["path"].lstrip("/")
            target.write_bytes(ET.tostring(sitemap, encoding="utf-8", xml_declaration=True))
        elif path.suffix == ".css":
            css = path.read_text(encoding="utf-8")
            if re.search(r"url\(\s*['\"]?/(?!/)", css):
                raise ValueError("Root-relative CSS URL requires an explicit adaptation")
            target.write_text(css + (DISABLED_CSS if relative.as_posix() == "assets/css/site.css" else ""), encoding="utf-8", newline="\n")
        else:
            shutil.copyfile(path, target)
    (OUTPUT / ".nojekyll").write_bytes(b"")
    manifest = [{"path": p.relative_to(OUTPUT).as_posix(), "bytes": p.stat().st_size, "sha256": sha256(p.read_bytes()).hexdigest()} for p in files_under(OUTPUT)]
    receipt = {
        "created_utc": datetime.now(timezone.utc).isoformat(), "site": SITE, "prefix": PREFIX,
        "output": str(OUTPUT), "pages": len(pages), "files": manifest,
        "bytes": sum(p["bytes"] for p in manifest),
        "identity": sha256(json.dumps(manifest, sort_keys=True, separators=(",", ":")).encode()).hexdigest(),
        "form": "inactive", "canonical": "original domain", "robots": "noindex",
    }
    (ARTIFACTS / "build-manifest.json").write_text(json.dumps(receipt, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps({k: receipt[k] for k in ("pages", "bytes", "identity", "site", "form")} | {"files": len(manifest)}, ensure_ascii=False))


if __name__ == "__main__":
    main()
