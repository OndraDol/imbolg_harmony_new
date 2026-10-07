"""One read-only Webnode login attempt with the locally stored DPAPI credential.

Run: python scripts/check_webnode_login_a2.py --cdp <URL>
No credential value, session data, page HTML, or screenshot is written or printed.
"""

import argparse
import base64
import subprocess
from pathlib import Path

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
CREDENTIAL = ROOT / ".secrets" / "webnode.credential.xml"


def read_credential():
    script = (
        "$c=Import-Clixml -LiteralPath '" + str(CREDENTIAL).replace("'", "''") + "';"
        "$u=[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($c.UserName));"
        "$p=$c.GetNetworkCredential().Password;"
        "$q=[Convert]::ToBase64String([Text.Encoding]::UTF8.GetBytes($p));"
        "[Console]::WriteLine($u);[Console]::WriteLine($q);"
        "Remove-Variable c,u,p,q"
    )
    result = subprocess.run(["powershell", "-NoProfile", "-Command", script],
                            capture_output=True, check=True, text=True)
    lines = result.stdout.splitlines()
    if len(lines) != 2:
        raise RuntimeError("DPAPI credential could not be read in the expected format")
    return tuple(base64.b64decode(line).decode("utf-8") for line in lines)


def main(cdp):
    username, password = read_credential()
    with sync_playwright() as pw:
        browser = pw.chromium.connect_over_cdp(cdp)
        pages = [p for context in browser.contexts for p in context.pages if p.url.startswith("https://www.webnode.com/")]
        if len(pages) != 1:
            raise RuntimeError(f"Expected one already-open official Webnode login page; found {len(pages)}")
        page = pages[0]
        email = page.get_by_role("textbox", name="Email address")
        secret = page.get_by_role("textbox", name="Password")
        submit = page.get_by_role("button", name="Log in", exact=True)
        if not (email.is_visible() and secret.is_visible() and submit.is_visible()):
            raise RuntimeError("Expected Webnode login form is not visible")
        email.fill(username)
        secret.fill(password)
        submit.click()
        page.wait_for_timeout(5000)
        body = page.locator("body").inner_text(timeout=10000)
        if "Registraci se nepodařilo odeslat" in body:
            status = "generic_registration_error"
        elif "přihlášení" in body.lower() and "nepodařilo" in body.lower():
            status = "generic_login_error"
        elif "imbolg" in body.lower():
            status = "project_visible"
        elif not page.get_by_role("textbox", name="Password").is_visible():
            status = "login_form_closed_or_navigated"
        else:
            status = "unverified"
        print(f"WEBNODE_LOGIN_STATUS {status}")
        print(f"WEBNODE_PAGE_HOST {page.url.split('/')[2] if '://' in page.url else 'unknown'}")
        browser.close()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cdp", required=True)
    main(parser.parse_args().cdp)
