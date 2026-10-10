"""A6 Chrome proof on the canonical PHP tree, offline external assets, no mail."""
from __future__ import annotations

import hashlib
import argparse
import json
from pathlib import Path
import sys
import traceback
import subprocess
from urllib.parse import urlparse, unquote
import xml.etree.ElementTree as ET

from bs4 import BeautifulSoup
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'scripts'))
from form_fixture_a5 import prepare_fixture, remove_fixture, running_server
from release_a6 import identity, digest

PAGES = json.loads((ROOT / 'evidence/pages.json').read_text(encoding='utf-8'))['pages']
ART = ROOT / 'artifacts/a6'
WIDTHS = (360, 390, 768, 1440)


def check(ok, message):
    if not ok:
        raise AssertionError(message)


def browser_for(p):
    candidates = (Path(r'C:\Program Files\Google\Chrome\Application\chrome.exe'),
                  Path(r'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe'))
    for candidate in candidates:
        if candidate.is_file():
            return p.chromium.launch(headless=True, executable_path=str(candidate)), str(candidate)
    return p.chromium.launch(headless=True), 'Playwright Chromium'


def geometry(page, label):
    data = page.evaluate('''() => {
      const outside = [...document.querySelectorAll('main *,header a,summary,input,textarea,button')]
        .filter(e => {const r=e.getBoundingClientRect(); const s=getComputedStyle(e);
          return r.width && r.height && s.visibility!=='hidden' &&
            (r.left < -1 || r.right > innerWidth+1);})
        .map(e=>({tag:e.tagName,id:e.id,text:e.textContent.slice(0,60)}));
      return {width:innerWidth,scroll:document.documentElement.scrollWidth,outside};
    }''')
    check(data['scroll'] <= data['width'] + 1 and not data['outside'], f'{label}: overflow {data}')
    check(page.evaluate('''() => {const header=document.querySelector('header');
      const m=document.querySelector('main').getBoundingClientRect();
      return !header || m.top>=header.getBoundingClientRect().bottom;}'''),
          f'{label}: header overlaps main')
    return data


def semantics(page, label):
    errors = page.evaluate('''() => {
      let errors=[]; const ids=[...document.querySelectorAll('[id]')].map(e=>e.id);
      if(new Set(ids).size!==ids.length) errors.push('duplicate IDs');
      if(document.documentElement.lang!=='cs') errors.push('language');
      if(document.querySelectorAll('main').length!==1) errors.push('main landmark');
      if(document.querySelectorAll('main h1').length!==1) errors.push('main heading');
      for(const img of document.images) if(!img.hasAttribute('alt')) errors.push('missing alt');
      for(const frame of document.querySelectorAll('iframe')) if(!frame.title) errors.push('iframe title');
      for(const a of document.querySelectorAll('a')) {
        if(!a.textContent.trim() && !a.getAttribute('aria-label') && !a.querySelector('img[alt]')) errors.push('unnamed link');
      }
      for(const e of document.querySelectorAll('input:not([type=hidden]),textarea')) {
        if(e.closest('[inert]')) continue;
        if(!e.labels.length && !e.getAttribute('aria-label')) errors.push('unnamed input');
        for(const id of (e.getAttribute('aria-describedby')||'').split(' ').filter(Boolean))
          if(!document.getElementById(id)) errors.push('broken describedby');
      }
      return errors;
    }''')
    check(not errors, f'{label}: accessibility {errors}')


def keyboard_menu(page, label):
    page.locator('.skip-link').focus()
    # Smooth scrolling is enabled by the site; focus may scroll asynchronously.
    page.wait_for_function("document.querySelector('.skip-link').getBoundingClientRect().top >= 0", timeout=5000)
    page.keyboard.press('Enter')
    check(page.locator('main').evaluate('e=>e===document.activeElement'), f'{label}: skip does not focus main')
    if page.locator('.mobile-menu').is_visible():
        summary = page.locator('.mobile-menu summary')
        summary.focus()
        page.keyboard.press('Enter')
        check(page.locator('.mobile-menu').get_attribute('open') is not None, f'{label}: menu does not open')
        links = page.locator('.mobile-menu nav a')
        check(links.count() == 10 and all(links.nth(i).is_visible() for i in range(10)), f'{label}: missing menu items')
        page.keyboard.press('Tab')
        check(links.first.evaluate('e=>e===document.activeElement'), f'{label}: keyboard menu focus')
        geometry(page, label + ' open menu')
        page.screenshot(path=str(ART / f'menu-{label}.png'), full_page=False)
        summary.focus()
        page.keyboard.press('Enter')
    else:
        check(page.locator('.desktop-nav a').count() == 10, f'{label}: desktop menu')


def check_lightbox(page, opener, href, label):
    dialog = page.locator('dialog.lightbox[open]')
    dialog.wait_for(state='visible')
    image = dialog.locator('img')
    page.wait_for_function('document.querySelector(".lightbox__image").complete && document.querySelector(".lightbox__image").naturalWidth > 0')
    check(image.get_attribute('src').endswith(href), label + ': correct lightbox image')
    check(image.evaluate('e=>getComputedStyle(e).objectFit') == 'contain', label + ': full uncropped image')
    group_id = opener.get_attribute('data-gallery-id')
    members = page.locator(f'a[data-gallery-id="{group_id}"]') if group_id else None
    if members and members.count() > 1:
        page.keyboard.press('ArrowRight')
        check(image.get_attribute('src').endswith(members.nth(1).get_attribute('href')), label + ': next photo in order')
        page.keyboard.press('ArrowLeft')
        check(image.get_attribute('src').endswith(href), label + ': previous photo')
    else:
        check(dialog.locator('.lightbox__next').is_disabled(), label + ': standalone photo')
    check(dialog.locator('.lightbox__original').get_attribute('href').endswith(href), label + ': original link')
    page.screenshot(path=str(ART / f'lightbox-{label}.png'), full_page=False)
    page.keyboard.press('Escape')
    page.locator('dialog.lightbox').wait_for(state='hidden')
    page.wait_for_function('(selector)=>document.querySelector(selector)===document.activeElement', arg=f'a[href="{href}"]')
    check(opener.evaluate('e=>e===document.activeElement'), label + ': lightbox restores focus')


def check_privacy(page, label):
    privacy = page.locator('.form-privacy')
    check(privacy.get_attribute('open') is None, label + ': privacy initially closed')
    check(page.locator('button[type=submit]').inner_text() == 'Odeslat zprávu', label + ': submit label')
    summary = privacy.locator('summary')
    summary.focus()
    page.keyboard.press('Enter')
    check(privacy.get_attribute('open') is not None and privacy.locator('p').first.is_visible(), label + ': privacy keyboard expand')
    geometry(page, label + '-privacy-open')
    page.keyboard.press('Enter')
    check(privacy.get_attribute('open') is None, label + ': privacy collapse')


def metadata_and_links(fixture):
    count = 0
    root = fixture / 'public'
    for source in PAGES:
        path = root / source['path'].strip('/') / 'index.html'
        soup = BeautifulSoup(path.read_text(encoding='utf-8'), 'html.parser')
        check(soup.title.string == source['title'], f'{source["path"]}: title')
        check(soup.select_one('meta[name=description]')['content'] == source['description'], f'{source["path"]}: description')
        check(soup.select_one('link[rel=canonical]')['href'] == source['canonical'], f'{source["path"]}: canonical')
        check(not soup.select_one('meta[name=robots]'), f'{source["path"]}: production noindex')
        for anchor in soup.select('a[href]'):
            url = urlparse(anchor['href'])
            if url.scheme in ('tel', 'mailto') or (url.netloc and url.netloc != 'www.imbolg-harmony.cz'):
                continue
            local = url.path or source['path']
            target = root / unquote(local).lstrip('/')
            if local.endswith('/'):
                target = target / 'index.html'
            check(target.is_file(), f'{source["path"]}: broken link {anchor["href"]}')
            if url.fragment:
                target_soup = BeautifulSoup(target.read_text(encoding='utf-8'), 'html.parser')
                check(target_soup.find(id=unquote(url.fragment)) is not None, f'broken fragment {anchor["href"]}')
            count += 1
        check([str(s) for s in soup.find_all('script')] == ['<script defer="" src="/assets/js/gallery.js"></script>'], 'unexpected script/tracking')
    tree = ET.parse(root / 'sitemap.xml')
    locations = [e.text for e in tree.findall('.//{http://www.sitemaps.org/schemas/sitemap/0.9}loc')]
    check(locations == [s['canonical'] for s in PAGES], 'sitemap mismatch')
    robots = (root / 'robots.txt').read_text()
    check('Disallow: /\n' not in robots and 'Sitemap: https://www.imbolg-harmony.cz/sitemap.xml' in robots, 'blocking robots')
    check('ErrorDocument 404 /404.html' in (root / '.htaccess').read_text(), '404 mapping absent')
    check('Stránka nenalezena' in (root / '404.html').read_text(encoding='utf-8'), '404 page absent')
    return count


def run(base, fixture, result, widths=WIDTHS, js_modes=(True, False)):
    result['internal_link_occurrences'] = metadata_and_links(fixture)
    result['checks'] = []
    result['external_requests'] = []
    result['console_errors'] = []
    result['page_errors'] = []
    result['failed_local_requests'] = []
    result['images_loaded'] = 0
    result['gallery_full_opened'] = 0
    result['form_scenarios'] = []
    with sync_playwright() as p:
        browser, executable = browser_for(p)
        result['browser'] = {'executable': executable, 'version': browser.version}
        try:
            for js in js_modes:
                for width in widths:
                    context = browser.new_context(viewport={'width': width, 'height': 900}, java_script_enabled=js)
                    form_scale = {'text200': False}
                    def route_external(route):
                        if urlparse(route.request.url).netloc != urlparse(base).netloc:
                            result['external_requests'].append(route.request.url)
                            # Do not load any third-party map resources or tracking; core must work offline.
                            route.fulfill(status=200, content_type='text/html', body='<!doctype html><html lang="cs"><title>Externí mapa offline</title></html>')
                        elif urlparse(route.request.url).path == '/assets/css/site.css' and form_scale['text200']:
                            # Same-origin stylesheet preserves the endpoint's CSP. No bypass or unsafe-inline.
                            css = (fixture / 'public/assets/css/site.css').read_text(encoding='utf-8')
                            route.fulfill(status=200, content_type='text/css', body=css+'\nhtml{font-size:200% !important}')
                        else:
                            route.continue_()
                    context.route('**/*', route_external)
                    page = context.new_page()
                    page.set_default_timeout(15000)
                    page.on('pageerror', lambda e: result['page_errors'].append(str(e)))
                    page.on('console', lambda m: result['console_errors'].append(m.text) if m.type == 'error' else None)
                    page.on('requestfailed', lambda r: result['failed_local_requests'].append(r.url) if r.url.startswith(base) else None)
                    for source in PAGES:
                        name = source['path'].strip('/') or 'home'
                        label = f'{name}-{width}-js{int(js)}'
                        response = page.goto(base + source['path'], wait_until='networkidle')
                        check(response.status == 200, label + ': HTTP')
                        check(page.title() == source['title'], label + ': title')
                        check(page.locator('[data-content-id]').count() == len(source['text_nodes']), label + ': node count')
                        semantics(page, label)
                        geometry(page, label)
                        if source['path'] == '/':
                            check_privacy(page, label)
                        keyboard_menu(page, label)
                        images = page.locator('img[data-media-id]')
                        for i in range(images.count()):
                            image = images.nth(i)
                            # Decode the real local image; an instant DOM scroll avoids
                            # Playwright's stability polling racing CSS smooth-scroll.
                            image.evaluate("e=>{e.loading='eager';e.scrollIntoView({behavior:'instant',block:'center'});return e.decode();}")
                            check(image.is_visible(), label + ': hidden image')
                            check(image.evaluate('e=>e.complete&&e.naturalWidth>0'), label + ': broken image')
                            result['images_loaded'] += 1
                        gallery = page.locator('a[data-gallery-id]')
                        actual = [(a.get_attribute('data-gallery-id'), a.get_attribute('data-gallery-order'), a.get_attribute('data-media-id'))
                                  for a in gallery.all()]
                        expected = [(g['id'], str(item['order']), item['media_id']) for g in source['galleries'] for item in g['items']]
                        check(actual == expected, label + ': gallery order')
                        for anchor in gallery.all():
                            href = anchor.get_attribute('href')
                            response = context.request.get(base + href)
                            check(response.status == 200 and response.headers.get('content-type','').startswith('image/jpeg'), label + ': full image')
                            check(hashlib.sha256(response.body()).hexdigest() == digest(fixture / 'public' / href.lstrip('/')), label + ': full image bytes')
                            result['gallery_full_opened'] += 1
                        if gallery.count():
                            href = gallery.first.get_attribute('href')
                            gallery.first.focus()
                            page.keyboard.press('Enter')
                            if js:
                                check_lightbox(page, gallery.first, href, label)
                            else:
                                page.wait_for_url(base + href)
                                check(page.locator('img').evaluate('e=>e.complete&&e.naturalWidth>0'), label + ': keyboard full image')
                                page.go_back(wait_until='networkidle')
                            check(page.title() == source['title'] and gallery.first.is_visible(), label + ': back to gallery')
                            # Without JS Browser Back need not restore focus; links stay focusable.
                            gallery.first.focus()
                            check(gallery.first.evaluate('e=>e===document.activeElement'), label + ': gallery focusable after Back')
                            check(gallery.first.evaluate('e=>e.getBoundingClientRect().height>=e.querySelector("img").getBoundingClientRect().height'),
                                  label + ': gallery focus box does not enclose image')
                        page.evaluate('scrollTo(0,0)')
                        page.screenshot(path=str(ART / f'{label}.png'), full_page=True)
                        result['checks'].append({'path':source['path'],'width':width,'js':js,'mode':'normal'})
                        if js:
                            for mode, css in (('text200', 'html { font-size:200% !important; }'),
                                              ('zoom200', 'html { zoom:2; }')):
                                sheet = page.add_style_tag(content=css)
                                geometry(page, label + '-' + mode)
                                semantics(page, label + '-' + mode)
                                if source['path'] == '/':
                                    check_privacy(page, label + '-' + mode)
                                keyboard_menu(page, label + '-' + mode)
                                # Actual text-size enlargement must be 32px or larger for body.
                                if mode == 'text200':
                                    check(page.evaluate("parseFloat(getComputedStyle(document.body).fontSize)>=32"), label + ': text not enlarged')
                                page.screenshot(path=str(ART / f'{name}-{width}-{mode}.png'), full_page=True)
                                sheet.evaluate('e=>e.remove()')
                                result['checks'].append({'path':source['path'],'width':width,'js':js,'mode':mode})
                    # Real synthetic POST, error+repair at every width, on/off JS.
                    page.goto(base, wait_until='networkidle')
                    for mode in ('normal','text200'):
                        # New fixture rate state, no personal data, keeps each scenario independent.
                        rate = fixture / 'private/var/rate.json'
                        if rate.is_file():
                            rate.unlink()
                        form_scale['text200'] = mode == 'text200'
                        page.goto(base, wait_until='networkidle')
                        page.locator('#contact-name').fill('   ')
                        page.locator('#contact-email').fill('a6@example.test')
                        page.locator('#contact-message').fill('Syntetická A6 kontrola česky.')
                        page.locator('button[type=submit]').click()
                        page.wait_for_load_state('networkidle')
                        check(page.locator('#contact-name').get_attribute('aria-invalid')=='true', 'server invalid field')
                        check(page.locator('#contact-email').input_value()=='a6@example.test', 'retained email')
                        if mode == 'text200':
                            check(page.evaluate('parseFloat(getComputedStyle(document.body).fontSize)>=32'), 'form error text not enlarged')
                        semantics(page, 'form-error')
                        geometry(page, 'form-error')
                        check_privacy(page, 'form-error')
                        page.screenshot(path=str(ART / f'form-error-{width}-js{int(js)}-{mode}.png'), full_page=True)
                        page.locator('#contact-name').focus()
                        page.locator('#contact-name').fill('A6 Kontrola')
                        page.keyboard.press('Tab')
                        check(page.locator('#contact-email').evaluate('e=>e===document.activeElement'), 'form keyboard sequence')
                        page.locator('button[type=submit]').click()
                        page.wait_for_load_state('networkidle')
                        check('Lokální test' in page.locator('main').inner_text(), 'capture success')
                        geometry(page, 'form-success')
                        page.screenshot(path=str(ART / f'form-success-{width}-js{int(js)}-{mode}.png'), full_page=True)
                        result['form_scenarios'].append({'width':width,'js':js,'mode':mode,'error_repair_capture':'PASS'})
                    form_scale['text200'] = False
                    page.goto(base + '/kontakt/', wait_until='networkidle')
                    check(page.locator('a[href="tel:+420775935130"]').count()==1, 'phone')
                    check(page.locator('a[href="mailto:kralovamarket@seznam.cz"]').count()==1, 'email')
                    for text in ('Markéta Kunešová','Myslbekova 559','407 21 Česká Kamenice'):
                        check(text in page.locator('main').inner_text(), 'contact '+text)
                    check(page.locator('a[href="https://www.facebook.com/profile.php?id=61571597523226"]').count()>=1, 'Facebook target')
                    response = page.goto(base + '/a6-nonexistent/', wait_until='networkidle')
                    check(response.status == 404 and page.title() == 'Stránka nenalezena | Imbolg Harmony', 'custom 404 response')
                    check('Stránka nenalezena' in page.locator('main').inner_text() and page.locator('main h1').is_visible(), 'visible custom 404 message')
                    semantics(page, '404')
                    geometry(page, '404')
                    page.screenshot(path=str(ART / f'404-{width}-js{int(js)}.png'), full_page=True)
                    context.close()
            # The local router emulates ErrorDocument; actual hosting/Apache support is a C1 gate.
            result['php_missing_url_status'] = browser.new_context().request.get(base+'/a6-nonexistent/').status
            check(result['php_missing_url_status']==404, 'unknown URL must return 404')
            # Chromium may report HTTP 404/422 in console; these are intentional responses,
            # never uncaught JS exceptions or failed local assets.
            unexpected = [e for e in result['console_errors'] if 'Failed to load resource: the server responded with a status of 404' not in e
                          and 'Failed to load resource: the server responded with a status of 422' not in e]
            result['unexpected_console_errors'] = unexpected
            check(not result['page_errors'] and not unexpected and not result['failed_local_requests'], 'console/network errors')
            allowed = {e['url'] for s in PAGES for e in s['embedded_resources'] if e['kind']=='iframe'}
            check(set(result['external_requests']) <= allowed, 'unexpected remote request/tracking')
            result['external_requests_unique'] = sorted(set(result['external_requests']))
            result['lightbox'] = ('PASS: native dialog, ordered arrow navigation, Escape and focus restoration.'
                                  if all(js_modes) else 'PASS: without JavaScript, original full-image links and browser Back remain usable.')
        finally:
            # Preserve a primary failure; driver loss during cleanup must not replace it.
            if browser.is_connected():
                try:
                    browser.close()
                except Exception:
                    if sys.exc_info()[0] is None:
                        raise


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--width', type=int, choices=WIDTHS)
    parser.add_argument('--js', type=int, choices=(0,1))
    args = parser.parse_args()
    ART.mkdir(parents=True, exist_ok=True)
    if args.width is None:
        # Bound Chromium/driver lifetime and memory; every group remains mandatory.
        parts = []
        version = identity()
        for js in (1,0):
            for width in WIDTHS:
                command = [sys.executable, str(Path(__file__)), '--width', str(width), '--js', str(js)]
                status = subprocess.run(command, cwd=ROOT).returncode
                part = json.loads((ART / f'browser-{width}-js{js}.json').read_text(encoding='utf-8'))
                check(status == 0 and part['status'] == 'PASS', f'{width}/js{js} group failed: {part.get("error")}')
                check(part['version_sha256'] == version['sha256'], 'different group version')
                parts.append(part)
        merged = dict(parts[0])
        for key in ('checks','form_scenarios','external_requests','console_errors','unexpected_console_errors','page_errors','failed_local_requests'):
            merged[key] = [v for part in parts for v in part[key]]
        for key in ('images_loaded','gallery_full_opened'):
            merged[key] = sum(part[key] for part in parts)
        merged['groups'] = [f'browser-{w}-js{j}.json' for j in (1,0) for w in WIDTHS]
        merged['external_requests_unique'] = sorted(set(merged['external_requests']))
        check(len(merged['checks']) == 160 and len(merged['form_scenarios']) == 16, 'incomplete aggregate')
        check(identity()['sha256'] == version['sha256'], 'changed aggregate version')
        (ART / 'browser-results.json').write_text(json.dumps(merged,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(json.dumps({'status':'PASS','groups':8,'page_checks':160,'form_scenarios':16,
                          'images_loaded':merged['images_loaded'],'gallery_full_opened':merged['gallery_full_opened']}))
        return
    check(args.js is not None, '--width requires --js')
    version = identity()
    result = {'version_sha256':version['sha256'],'status':'RUNNING'}
    fixture = prepare_fixture()
    try:
        # Compare canonical release bytes to the tested fixture before synthetic config/state exists.
        manifest = json.loads((ART / 'release-manifest.json').read_text())
        for record in manifest['files']:
            check(digest(fixture / record['path'])==record['sha256'], 'fixture/release mismatch '+record['path'])
        with running_server(fixture) as base:
            run(base, fixture, result, widths=(args.width,), js_modes=(bool(args.js),))
        check(identity()['sha256']==version['sha256'], 'version changed during browser verification')
        result['status']='PASS'
    except Exception as error:
        result['status']='FAIL'
        result['error']=str(error)
        traceback.print_exc()
        raise
    finally:
        remove_fixture(fixture)
        (ART / f'browser-{args.width}-js{args.js}.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
        print(json.dumps({k:v for k,v in result.items() if k not in ('checks','external_requests')},ensure_ascii=False))


if __name__=='__main__':
    main()
