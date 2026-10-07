"""Audit an immutable A2 capture without changing its source files.

Run: python scripts/audit_public_a2.py archive/<timestamp>
"""

import argparse
import collections
import json
import sys
from pathlib import Path
from urllib.parse import urlparse

from bs4 import BeautifulSoup, NavigableString


BLOCKS = {"h1", "h2", "h3", "h4", "h5", "h6", "p", "li", "blockquote", "figcaption", "dt", "dd"}


def main(snapshot):
    sys.stdout.reconfigure(encoding="utf-8")
    data = json.loads((snapshot / "capture.json").read_text(encoding="utf-8"))
    print("pages", len(data["pages"]), "sitemap", len(data["sitemap_paths"]))
    print("paths", [page["path"] for page in data["pages"]])
    print("blocks", sum(len(p["blocks"]) for p in data["pages"]))
    print("image occurrences", sum(len(p["images"]) for p in data["pages"]))
    print("galleries", [(p["path"], [len(g["items"]) for g in p["galleries"]]) for p in data["pages"]])
    print("backgrounds", [(p["path"], len(p["backgrounds"])) for p in data["pages"]])
    print("links", sum(len(p["links"]) for p in data["pages"]))
    print("media URLs", len(data["media"]), "unique files", len(list((snapshot / "media").iterdir())))
    print("unique media bytes", sum(x.stat().st_size for x in (snapshot / "media").iterdir()))
    print("hosts", collections.Counter(urlparse(l["resolved"]).hostname for p in data["pages"] for l in p["links"]))
    internal = sorted({urlparse(l["resolved"]).path for p in data["pages"] for l in p["links"] if urlparse(l["resolved"]).hostname == "www.imbolg-harmony.cz"})
    print("internal paths", internal)
    print("errors", data["errors"])
    for page in data["pages"]:
        soup = BeautifulSoup((snapshot / page["rendered_dom"]).read_text(encoding="utf-8"), "html.parser")
        main_element = soup.find("main") or soup.body
        uncovered = []
        for node in main_element.descendants:
            if not isinstance(node, NavigableString) or not node.strip():
                continue
            if any(parent.name in BLOCKS for parent in node.parents):
                continue
            if any(parent.name in {"script", "style", "noscript"} for parent in node.parents):
                continue
            parent = node.parent
            uncovered.append({"tag": parent.name, "class": parent.get("class", []), "text": str(node).strip()[:220]})
        print("PAGE", page["path"], "uncovered text", uncovered[:30], "count", len(uncovered))
        print("  form", page["forms"])
        print("  outside link hosts", sorted({urlparse(l["resolved"]).hostname for l in page["links"] if urlparse(l["resolved"]).hostname not in {"www.imbolg-harmony.cz", None}}))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot", type=Path)
    main(parser.parse_args().snapshot.resolve())
