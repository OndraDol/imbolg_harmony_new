"""Prove the approved UX exceptions do not hide unrelated content changes."""
import json
from pathlib import Path
import shutil
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
import verify_content_a4 as contract


def main():
    source = next(p for p in contract.PAGES if p['path'] == '/')
    mapped = next(p for p in contract.SOURCE_MAP['pages'] if p['target_path'] == '/')
    media_by_id = {m['id']: m for m in contract.MEDIA}
    media_by_url = {v['url']: m for m in contract.MEDIA for v in m['variants']}
    original = (ROOT / 'dist/index.html').read_text(encoding='utf-8')
    mutations = {
        'wrong-whatsapp': ('https://wa.me/420775935130', 'https://wa.me/420111111111'),
        'unapproved-copy': ('data-content-id="home-node-001">„Naše pouto', 'data-content-id="home-node-001">„Jiný text'),
        'missing-text-marker': ('data-content-id="home-node-001"', ''),
        'hidden-privacy': ('<details class="form-privacy">', '<details class="form-privacy" hidden>'),
        'missing-privacy-text': ('Běžnou uzavřenou komunikaci uchováme nejdéle šest měsíců', 'Komunikaci uchováme navždy'),
        'missing-media-marker': ('data-media-order="2"', ''),
        'new-unapproved-addition': ('data-ux-addition="home-whatsapp"', 'data-ux-addition="unapproved"'),
    }
    with tempfile.TemporaryDirectory(prefix='imbolg-ux-contract-') as temporary:
        dist = Path(temporary) / 'dist'
        shutil.copytree(ROOT / 'dist', dist)
        results = []
        for name, (before, after) in mutations.items():
            assert original.count(before) == 1, name
            (dist / 'index.html').write_text(original.replace(before, after, 1), encoding='utf-8')
            contract.errors.clear()
            contract.verify_page(source, mapped, dist, media_by_id, media_by_url)
            assert contract.errors, f'Undetected mutation: {name}'
            results.append({'mutation': name, 'detected': True})
    output = ROOT / 'artifacts/ux-20261010'
    output.mkdir(parents=True, exist_ok=True)
    (output / 'content-mutations.json').write_text(json.dumps(results, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'status': 'PASS', 'mutations_rejected': len(results)}))


if __name__ == '__main__':
    main()
