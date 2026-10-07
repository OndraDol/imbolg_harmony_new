"""Compare selected JPEGs with published full-size WebP variants for crop drift.

Run: python scripts/compare_variants_a2.py archive/<timestamp>
Prints pairs needing visual inspection; never edits images or evidence.
"""

import argparse
import json
from pathlib import Path

from PIL import Image, ImageChops, ImageStat


ROOT = Path(__file__).resolve().parents[1]


def main(snapshot):
    media = json.loads((ROOT / "evidence/media.json").read_text(encoding="utf-8"))["media"]
    results = []
    for medium in media:
        original = medium["selected_original"]
        if original["format"] not in {"JPEG", "PNG"}:
            continue
        matching = [variant["archived"] for variant in medium["variants"]
                    if variant["archived"] and variant["archived"]["format"] == "WEBP"
                    and variant["archived"]["dimensions"] == original["dimensions"]]
        if not matching:
            continue
        webp = max(matching, key=lambda item: item["bytes"])
        with Image.open(snapshot / original["archive_file"]) as first:
            a = first.convert("RGB").resize((128, 128))
        with Image.open(snapshot / webp["archive_file"]) as second:
            b = second.convert("RGB").resize((128, 128))
        difference = ImageChops.difference(a, b)
        mean_difference = sum(ImageStat.Stat(difference).mean) / 3
        results.append((medium["id"], round(mean_difference, 2), original["archive_file"], webp["archive_file"]))
    print("compared", len(results), "full-size JPEG/WebP pairs")
    print("maximum_mean_difference", max((x[1] for x in results), default=None))
    print("pairs_over_15", [x for x in results if x[1] > 15])


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("snapshot", type=Path)
    main(parser.parse_args().snapshot.resolve())
