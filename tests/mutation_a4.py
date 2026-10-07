"""Confirm A4 verifier fails when an item is missing from a disposable build copy."""

import shutil
import os
import stat
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "artifacts/a4/negative-fixture"
if not FIXTURE.resolve().is_relative_to((ROOT / "artifacts/a4").resolve()):
    raise RuntimeError("Fixture path outside intended artifacts directory")
def clear_read_only(function, path, error):
    os.chmod(path, stat.S_IREAD | stat.S_IWRITE | stat.S_IEXEC)
    function(path)

if FIXTURE.exists():
    old_home = FIXTURE / "index.html"
    if FIXTURE.is_symlink() or not old_home.is_file() or 'data-content-id="home-node-001"' in old_home.read_text(encoding="utf-8"):
        raise RuntimeError("Existing fixture is not the disposable mutated copy")
    shutil.rmtree(FIXTURE, onexc=clear_read_only)

try:
    shutil.copytree(ROOT / "dist", FIXTURE)
    home = FIXTURE / "index.html"
    html = home.read_text(encoding="utf-8")
    needle = 'data-content-id="home-node-001"'
    if html.count(needle) != 1:
        raise RuntimeError("Expected one target marker before mutation")
    home.write_text(html.replace(needle, "", 1), encoding="utf-8")
    result = subprocess.run([sys.executable, str(ROOT / "scripts/verify_content_a4.py"),
                             "--dist", str(FIXTURE)], capture_output=True, text=True, encoding="utf-8")
    if result.returncode == 0 or "textové uzly chybí" not in result.stdout:
        raise RuntimeError(f"Verifier failed to identify the missing item: {result.stdout} {result.stderr}")
    print("Mutation test: removing home-node-001 is detected in the disposable copy.")
finally:
    if FIXTURE.exists():
        shutil.rmtree(FIXTURE, onexc=clear_read_only)
