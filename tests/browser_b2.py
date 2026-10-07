"""B2 regressions: form card bounds at enlargement and uncropped contain hover."""
from __future__ import annotations
import json
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / 'artifacts/b2'
sys.path.insert(0, str(ROOT / 'scripts'))
from form_fixture_a5 import prepare_fixture, remove_fixture, running_server
from release_a6 import identity
from browser_a6 import browser_for, geometry, semantics, WIDTHS


def form_bounds(page):
    result = page.locator('.contact-form').evaluate('''f=>{
      const b=f.getBoundingClientRect(),s=getComputedStyle(f),z=b.width/f.offsetWidth;
      const left=b.left+parseFloat(s.paddingLeft)*z,right=b.right-parseFloat(s.paddingRight)*z;
      return {left,right,fields:[...f.querySelectorAll('input,textarea,button')]
        .filter(e=>e.getClientRects().length).map(e=>{const r=e.getBoundingClientRect();
          return {id:e.id||e.tagName,left:r.left,right:r.right,inside:r.left>=left-1&&r.right<=right+1}})};
    }''')
    assert len(result['fields']) == 4
    assert all(f['inside'] for f in result['fields']), result
    return result


def main():
    version = identity()['sha256']
    result = {'version_sha256': version, 'status': 'RUNNING', 'forms': [], 'hovers': []}
    fixture = prepare_fixture()
    try:
        with running_server(fixture) as base, sync_playwright() as pw:
            browser, executable = browser_for(pw)
            result['browser'] = executable
            for js in (True, False):
                for width in WIDTHS:
                    context = browser.new_context(java_script_enabled=js, viewport={'width': width, 'height': 900})
                    scale = {'css': ''}
                    def route(r):
                        if r.request.url == base + '/assets/css/site.css':
                            r.fulfill(status=200, content_type='text/css', body=(fixture / 'public/assets/css/site.css').read_text(encoding='utf-8') + scale['css'])
                        elif r.request.url.startswith(base + '/'): r.continue_()
                        else: r.fulfill(status=200, body='')
                    context.route('**/*', route)
                    page = context.new_page()
                    for mode, css in [('normal',''), ('text200','\nhtml{font-size:200% !important}'), ('zoom200','\nhtml{zoom:2}')]:
                        rate = fixture / 'private/var/rate.json'
                        if rate.is_file():
                            rate.unlink()
                        scale['css'] = css
                        page.goto(base, wait_until='networkidle')
                        home_bounds = form_bounds(page)
                        page.locator('#contact-name').fill('   ')
                        page.locator('#contact-email').fill('b2@example.test')
                        page.locator('#contact-message').fill('Syntetická kontrola B2.')
                        page.locator('button[type=submit]').click()
                        page.wait_for_load_state('networkidle')
                        assert page.locator('#contact-name').get_attribute('aria-invalid') == 'true'
                        assert page.locator('#contact-email').input_value() == 'b2@example.test'
                        error_bounds = form_bounds(page)
                        geometry(page, f'B2 {width}/{js}/{mode}')
                        semantics(page, 'B2 form error')
                        page.screenshot(path=str(ART / f'fixed-form-{width}-js{int(js)}-{mode}.png'), full_page=True)
                        result['forms'].append({'width':width, 'js':js, 'mode':mode, 'home':home_bounds, 'error':error_bounds})
                    scale['css'] = ''
                    if js:
                        for path, ids in [('/', [6,7,8,9,12]), ('/fotogalerie/', [20,26,27,37,38])]:
                            page.goto(base + path, wait_until='networkidle')
                            for number in ids:
                                img = page.locator(f'main img[data-media-id="media-{number:03d}"]')
                                img.hover()
                                props = img.evaluate('e=>({fit:getComputedStyle(e).objectFit,transform:getComputedStyle(e).transform})')
                                assert props == {'fit':'contain', 'transform':'none'}, (width, number, props)
                                if number in (6,12):
                                    img.screenshot(path=str(ART / f'fixed-hover-{width}-media-{number:03d}.png'))
                                result['hovers'].append({'width':width, 'media':number, **props})
                    context.close()
            browser.close()
        assert identity()['sha256'] == version
        assert len(result['forms']) == 24 and len(result['hovers']) == 40
        result['status'] = 'PASS'
    finally:
        remove_fixture(fixture)
        ART.mkdir(exist_ok=True)
        (ART / 'regressions.json').write_text(json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps({'status':result['status'], 'form_modes':len(result['forms']), 'form_states':len(result['forms'])*2, 'contain_hovers':len(result['hovers']), 'version_sha256':version}))


if __name__ == '__main__':
    main()
