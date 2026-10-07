"""Canonical public/private release; explicit inputs, no credentials or captures."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PROOF = ROOT / 'artifacts/a6'
LIMIT = 80_000_000  # decimal MB; stricter than 80 MiB


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def identity():
    files = []
    for directory in ('src', 'server/app', 'server/public', 'scripts', 'tests', 'dist', 'server/vendor'):
        files += [p for p in (ROOT / directory).rglob('*')
                  if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc']
    files += [ROOT / p for p in ('.eleventy.cjs', 'package.json', 'package-lock.json',
                                'server/composer.json', 'server/composer.lock', 'server/config.example.php')]
    records = [{'path': p.relative_to(ROOT).as_posix(), 'sha256': digest(p)} for p in sorted(files)]
    baseline = [{'path': 'evidence/' + p, 'sha256': digest(ROOT / 'evidence' / p)}
                for p in ('pages.json', 'media.json', 'source-map.json', 'exclusions.json')]
    return {'git_head': subprocess.check_output(['git', '-C', str(ROOT), 'rev-parse', 'HEAD'], text=True).strip(),
            'working_tree': 'uncommitted; file hashes are authoritative', 'files': records,
            'baseline': baseline,
            'sha256': hashlib.sha256(json.dumps(records + baseline, sort_keys=True).encode()).hexdigest()}


def copy_tree(source, target):
    # Reject symlinks/junctions anywhere, including a root directory.
    for item in [source, *source.rglob('*')]:
        if item.is_symlink() or item.is_junction():
            raise RuntimeError(f'Link/junction is not an allowed release input: {item}')
    shutil.copytree(source, target)


def populate(target):
    """Shared by release and PHP capture fixture; target must be fresh."""
    if (target / 'public').exists() or (target / 'private').exists():
        raise RuntimeError('Release target must be fresh.')
    installed = json.loads((ROOT / 'server/vendor/composer/installed.json').read_text(encoding='utf-8'))
    locked = json.loads((ROOT / 'server/composer.lock').read_text(encoding='utf-8'))['packages']
    installed_packages = installed['packages']
    if installed.get('dev') or {p['name'] for p in installed_packages} != {'phpmailer/phpmailer'}:
        raise RuntimeError('Vendor is not the locked production-only PHPMailer tree.')
    package_keys = lambda packages: {(p['name'], p['version'], p['source']['reference'], p['dist']['reference']) for p in packages}
    if package_keys(installed_packages) != package_keys(locked):
        raise RuntimeError('Installed PHP package version/reference does not match composer.lock.')
    copy_tree(ROOT / 'dist', target / 'public')
    copy_tree(ROOT / 'server/public/api', target / 'public/api')
    copy_tree(ROOT / 'server/app', target / 'private/app')
    copy_tree(ROOT / 'server/vendor', target / 'private/vendor')
    shutil.copyfile(ROOT / 'server/config.example.php', target / 'private/config.example.php')


def remove_generated(target):
    # Only our marked, non-reparse generated root. Never delete a user config.
    if target.absolute() != ROOT / 'release' or target.is_symlink() or target.is_junction():
        raise RuntimeError('Unverified release cleanup target.')
    if not target.exists():
        return
    if not (target / '.generated-a6').is_file() or (target / 'private/config.php').exists():
        raise RuntimeError('Refusing to replace an unmarked release or a configured release.')
    for item in target.rglob('*'):
        if item.is_symlink() or item.is_junction():
            raise RuntimeError('Release contains a reparse point; cleanup refused.')
    shutil.rmtree(target, onexc=lambda function, path, error: (Path(path).chmod(0o700), function(path)))


def build_release():
    target = ROOT / 'release'
    remove_generated(target)
    target.mkdir()
    (target / '.generated-a6').write_text('Generated local A6 package. Only public/private are upload inputs.\n')
    populate(target)
    files = [{'path': p.relative_to(target).as_posix(), 'bytes': p.stat().st_size, 'sha256': digest(p)}
             for folder in ('public', 'private') for p in sorted((target / folder).rglob('*')) if p.is_file()]
    for item in files:
        parts = Path(item['path']).parts
        if any(part in ('archive', 'artifacts', 'node_modules', '.git', '.secrets', 'docs', 'var') for part in parts):
            raise RuntimeError(f'Excluded input in release: {item["path"]}')
    total = sum(f['bytes'] for f in files)
    manifest = {'limit_bytes': LIMIT, 'total_bytes': total, 'files_count': len(files),
                'public_bytes': sum(f['bytes'] for f in files if f['path'].startswith('public/')),
                'private_bytes': sum(f['bytes'] for f in files if f['path'].startswith('private/')),
                'package_sha256': hashlib.sha256(json.dumps(files, sort_keys=True).encode()).hexdigest(),
                'files': files}
    PROOF.mkdir(parents=True, exist_ok=True)
    (PROOF / 'release-manifest.json').write_text(json.dumps(manifest, indent=2) + '\n', encoding='utf-8')
    (PROOF / 'version.json').write_text(json.dumps(identity(), indent=2) + '\n', encoding='utf-8')
    if total > LIMIT:
        raise RuntimeError(f'Release is over 80 MB: {total} bytes')
    print(json.dumps({k: v for k, v in manifest.items() if k != 'files'}))


if __name__ == '__main__':
    argparse.ArgumentParser(description=__doc__).parse_args()
    build_release()
