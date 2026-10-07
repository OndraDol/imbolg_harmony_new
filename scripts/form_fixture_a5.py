"""Isolated A5 public/private fixtures. Always capture, always loopback, SMTP blocked."""
from __future__ import annotations

import argparse
from contextlib import contextmanager
import json
import os
from pathlib import Path
import shutil
import socket
import subprocess
import tempfile
import time
import urllib.request
from release_a6 import populate

ROOT = Path(__file__).resolve().parents[1]


def php_command():
    php = os.environ.get('IMBOLG_PHP') or str(ROOT / '.runtime/php83/php.exe')
    if not Path(php).is_file():
        php = shutil.which('php')
    if not php:
        raise RuntimeError('PHP 8.3 nenalezeno; nastavte IMBOLG_PHP na ověřené PHP.')
    # Ignore machine-wide php.ini; no SMTP sockets or mail() in local preview/tests.
    command = [php, '-n', '-d', f'extension_dir={Path(php).parent / "ext"}',
               '-d', 'extension=openssl', '-d', 'display_errors=0', '-d', 'log_errors=0',
               '-d', 'file_uploads=0', '-d', 'post_max_size=64K', '-d', 'expose_php=0',
               '-d', 'disable_functions=mail,fsockopen,pfsockopen,stream_socket_client']
    version = subprocess.check_output(command + ['-r', 'echo PHP_MAJOR_VERSION,".",PHP_MINOR_VERSION;'], text=True)
    if version != '8.3':
        raise RuntimeError(f'A5 vyžaduje PHP 8.3, nalezeno {version}')
    return command


def prepare_fixture():
    if not (ROOT / 'dist/index.html').is_file() or not (ROOT / 'server/vendor/autoload.php').is_file():
        raise RuntimeError('Nejdřív npm run build a Composer install dle README.')
    base = ROOT / 'private/a5'
    base.mkdir(parents=True, exist_ok=True)
    fixture = Path(tempfile.mkdtemp(prefix='fixture-', dir=base))
    populate(fixture)
    config = """<?php
return [
    'transport' => 'capture',
    'from' => 'form@example.invalid',
    'from_verified' => false,
    'rate_key' => '__KEY__',
    'rate_limit' => 5,
    'rate_window' => 600,
];
""".replace('__KEY__', os.urandom(32).hex())
    (fixture / 'private/config.php').write_text(config, encoding='utf-8')
    return fixture


def remove_fixture(fixture):
    fixture = fixture.resolve()
    parent = (ROOT / 'private/a5').resolve()
    if fixture.parent != parent or not fixture.name.startswith('fixture-') or fixture.is_symlink():
        raise RuntimeError('Odmítnut neověřený cíl úklidu fixture.')
    # Windows copies may carry ReadOnly; adjust only this verified temporary tree.
    def remove_readonly(func, path, exc):
        os.chmod(path, 0o700)
        func(path)
    shutil.rmtree(fixture, onexc=remove_readonly)


@contextmanager
def running_server(fixture):
    with socket.socket() as sock:
        sock.bind(('127.0.0.1', 0))
        port = sock.getsockname()[1]
    base = f'http://127.0.0.1:{port}'
    env = dict(os.environ, IMBOLG_LOCAL_CAPTURE='1')
    log = open(fixture / 'php-server.log', 'wb')
    process = subprocess.Popen(php_command() + ['-S', f'127.0.0.1:{port}', '-t', str(fixture / 'public'),
                                               str(ROOT / 'tests/php_router_a6.php')],
                               env=env, stdout=log, stderr=log,
                               creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
    try:
        opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        for attempt in range(50):
            if process.poll() is not None:
                raise RuntimeError('PHP server skončil před připraveností.')
            try:
                with opener.open(base, timeout=1) as response:
                    if response.status == 200:
                        break
            except (OSError, urllib.error.URLError):
                time.sleep(0.1)
        else:
            raise RuntimeError('PHP server není připravený.')
        yield base
    finally:
        process.terminate()
        process.wait(timeout=10)
        log.close()
        with socket.socket() as sock:
            if sock.connect_ex(('127.0.0.1', port)) == 0:
                raise RuntimeError('Po úklidu port stále poslouchá.')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--preview', action='store_true')
    args = parser.parse_args()
    if not args.preview:
        parser.error('Použijte --preview pro lokální capture náhled.')
    fixture = prepare_fixture()
    try:
        with running_server(fixture) as base:
            print(f'Capture náhled: {base}/; Ctrl+C ukončí server a odstraní syntetickou fixture.', flush=True)
            print('Nezadávejte osobní údaje, používejte pouze syntetické testy.', flush=True)
            while True:
                time.sleep(1)
    except KeyboardInterrupt:
        pass
    finally:
        remove_fixture(fixture)


if __name__ == '__main__':
    main()
