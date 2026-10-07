"""A5 form integration proof using only the local capture fixture.

This script deliberately exercises the public HTTP endpoint.  It never calls a
production SMTP server: the fixture permits only loopback capture and starts
PHP with mail and socket functions disabled.
"""

from __future__ import annotations

from contextlib import ExitStack
from email import policy
from email.parser import BytesParser
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import urllib.error
import urllib.parse
import urllib.request

from playwright.sync_api import sync_playwright


ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from form_fixture_a5 import php_command, prepare_fixture, remove_fixture, running_server  # noqa: E402


ARTIFACTS = ROOT / "artifacts" / "a5"


def check(condition: bool, detail: str) -> None:
    if not condition:
        raise AssertionError(detail)


def chrome_for(playwright):
    try:
        return playwright.chromium.launch(headless=True), "Playwright Chromium"
    except Exception as first_error:
        for candidate, label in (
            (Path(r"C:\Program Files\Google\Chrome\Application\chrome.exe"), "Google Chrome"),
            (Path(r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe"), "Microsoft Edge"),
            (Path(r"C:\Program Files\Microsoft\Edge\Application\msedge.exe"), "Microsoft Edge"),
        ):
            if candidate.is_file():
                return playwright.chromium.launch(headless=True, executable_path=str(candidate)), label
        raise RuntimeError("Není dostupný místní Chrome/Edge pro kontrolu A5.") from first_error


class FormProof:
    def __init__(self) -> None:
        self.fixture = prepare_fixture()
        self.stack = ExitStack()
        try:
            self.base = self.stack.enter_context(running_server(self.fixture))
        except BaseException:
            self.stack.close()
            remove_fixture(self.fixture)
            raise
        self.opener = urllib.request.build_opener(urllib.request.ProxyHandler({}))
        self.results: dict[str, object] = {"base": self.base, "checks": []}
        self.write_config(rate_limit=100)

    @property
    def private(self) -> Path:
        return self.fixture / "private"

    def close(self) -> None:
        self.stack.close()
        remove_fixture(self.fixture)

    def write_config(self, *, rate_limit: int = 100, transport: str = "capture") -> None:
        config = f"""<?php
return [
    'transport' => '{transport}',
    'from' => 'form@example.invalid',
    'from_verified' => false,
    'rate_key' => '0123456789abcdef0123456789abcdef0123456789abcdef0123456789abcdef',
    'rate_limit' => {rate_limit},
    'rate_window' => 600,
];
"""
        (self.private / "config.php").write_text(config, encoding="utf-8")

    def reset_var(self) -> None:
        var = self.private / "var"
        if var.exists():
            self.remove_fixture_tree(var)

    def remove_fixture_tree(self, path: Path) -> None:
        """Delete only a real temporary tree below this fixture's private/var."""
        root = self.fixture.resolve()
        allowed = (self.private / "var").resolve()
        target = path.resolve()
        try:
            target.relative_to(allowed)
            allowed.relative_to(root)
        except ValueError as error:
            raise RuntimeError("Odmítnut úklid mimo private/var této fixture.") from error
        if path.is_symlink() or target.is_symlink():
            raise RuntimeError("Odmítnut úklid symlinku ve fixture.")
        shutil.rmtree(target)

    def captures(self) -> list[Path]:
        return sorted((self.private / "var" / "capture").glob("*.eml")) if (self.private / "var" / "capture").is_dir() else []

    def request(self, method: str, path: str = "/api/contact.php", data=None, headers=None):
        payload = None
        request_headers = {"Accept": "text/html"}
        if headers:
            request_headers.update(headers)
        if data is not None:
            payload = urllib.parse.urlencode(data, doseq=True).encode("utf-8") if not isinstance(data, bytes) else data
            request_headers.setdefault("Content-Type", "application/x-www-form-urlencoded")
        request = urllib.request.Request(self.base + path, data=payload, headers=request_headers, method=method)
        try:
            with self.opener.open(request, timeout=10) as response:
                return response.status, dict(response.headers.items()), response.read()
        except urllib.error.HTTPError as error:
            return error.code, dict(error.headers.items()), error.read()

    def record(self, name: str) -> None:
        self.results["checks"].append(name)

    def test_success_and_mime(self) -> None:
        self.reset_var()
        status, _, body = self.request("POST", data={"name": "Hana Žížalová", "email": "hana@example.test", "message": "Dobrý den, zkouška s diakritikou."})
        check(status == 200 and "Lokální test" in body.decode("utf-8"), "validní capture nevrátila pravdivý úspěch")
        captures = self.captures()
        check(len(captures) == 1, "validní zpráva nevytvořila právě jeden lokální MIME soubor")
        mail = BytesParser(policy=policy.default).parsebytes(captures[0].read_bytes())
        check(mail["To"].addresses[0].addr_spec == "kralovamarket@seznam.cz", "příjemce není pevný Seznam")
        check(mail["From"].addresses[0].addr_spec == "form@example.invalid", "From není konfigurace fixture")
        check(mail["Reply-To"].addresses[0].addr_spec == "hana@example.test", "Reply-To není návštěvník")
        text = mail.get_body(preferencelist=("plain",)).get_content()
        check("Hana Žížalová" in text and "zkouška s diakritikou" in text, "MIME nezachovalo Unicode obsah")
        self.record("valid-capture-mime")

    def test_optional_empty_message(self) -> None:
        before = set(self.captures())
        status, _, _ = self.request("POST", data={"name": "Prázdná Zpráva", "email": "empty@example.test", "message": ""})
        created = set(self.captures()) - before
        check(status == 200 and len(created) == 1, "nepovinná prázdná zpráva neprošla do capture")
        mail = BytesParser(policy=policy.default).parsebytes(created.pop().read_bytes())
        text = mail.get_body(preferencelist=("plain",)).get_content().replace("\r\n", "\n")
        check(text.endswith("\n\n"), "prázdná zpráva změnila formát těla")
        self.record("optional-empty-message")

    def test_query_overrides_are_ignored(self) -> None:
        before = set(self.captures())
        status, _, _ = self.request(
            "POST",
            "/api/contact.php?recipient=attacker%40example.test&transport=smtp&host=mail.attacker.invalid",
            {"name": "Pevný Příjemce", "email": "query@example.test", "message": "x"},
        )
        created = set(self.captures()) - before
        check(status == 200 and len(created) == 1, "query parametry změnily či zablokovaly lokální capture")
        mail = BytesParser(policy=policy.default).parsebytes(created.pop().read_bytes())
        check(mail["To"].addresses[0].addr_spec == "kralovamarket@seznam.cz", "query parametr změnil pevného příjemce")
        self.record("query-overrides-ignored-fixed-recipient")

    def test_validation_and_escaping(self) -> None:
        before = len(self.captures())
        status, _, body = self.request("POST", data={"name": "", "email": "wrong", "message": "x"})
        text = body.decode("utf-8")
        check(status == 422 and "Vyplňte prosím" in text and "platnou e-mailovou" in text, "chybějící jméno a e-mail nemají chybu")
        check(len(self.captures()) == before, "neplatná data byla předána transportu")
        status, _, body = self.request("POST", data={"name": "<script>window.bad=1</script>", "email": "bad", "message": "<b>text</b>"})
        text = body.decode("utf-8")
        check(status == 422 and "&lt;script&gt;window.bad=1&lt;/script&gt;" in text and "<script>window.bad" not in text,
              "vratný HTML obsah není escapovaný")
        status, _, _ = self.request("POST", data=[("name[]", "pole"), ("email", "array@example.test"), ("message", "x")])
        check(status == 422 and len(self.captures()) == before, "array pole bylo přijato nebo odesláno")
        status, _, _ = self.request("POST", data={"name": "Jméno", "email": "attacker@example.test\r\nBcc: evil@example.test", "message": "x"})
        check(status == 422 and len(self.captures()) == before, "CRLF v e-mailu nebylo odmítnuto")
        self.record("validation-array-crlf-escaping")

    def test_size_honeypot_and_protocol(self) -> None:
        before = len(self.captures())
        status, _, _ = self.request("POST", data={"name": "A" * 801, "email": "long@example.test", "message": "x"})
        check(status == 422 and len(self.captures()) == before, "nadměrné pole nebylo odmítnuto")
        status, _, _ = self.request("POST", data={"name": "Velká", "email": "large@example.test", "message": "x" * 66000})
        check(status == 413 and len(self.captures()) == before, "nadměrný request nebyl odmítnut")
        status, _, _ = self.request("POST", data={"name": "Bot", "email": "bot@example.test", "message": "x", "website": "https://spam.invalid"})
        check(status == 422 and len(self.captures()) == before, "honeypot odeslal zprávu")
        status, headers, _ = self.request("GET")
        check(status == 405 and headers.get("Allow") == "POST" and len(self.captures()) == before, "GET není bezpečně odmítnut")
        status, _, _ = self.request("POST", data=b'{"name":"json"}', headers={"Content-Type": "application/json"})
        check(status == 415 and len(self.captures()) == before, "cizí Content-Type není odmítnut")
        self.record("limits-honeypot-method-content-type")

    def test_rate_proxy_and_private_http(self) -> None:
        self.reset_var()
        self.write_config(rate_limit=1)
        status, _, _ = self.request("POST", data={"name": "Limit", "email": "one@example.test", "message": "x"})
        check(status == 200, "první požadavek rate testu neprošel")
        status, headers, _ = self.request("POST", data={"name": "Limit", "email": "two@example.test", "message": "x"}, headers={"X-Forwarded-For": "203.0.113.9"})
        check(status == 429 and "Retry-After" in headers, "falešný XFF obešel rate limit")
        for path in ("/private/config.php", "/config.php", "/vendor/autoload.php"):
            status, _, body = self.request("GET", path)
            check(status == 404 and b"form@example.invalid" not in body, f"{path} je veřejně dostupné")
        self.write_config(rate_limit=100)
        self.reset_var()
        self.record("rate-xff-private-boundary")

    def test_missing_disabled_and_capture_failure(self) -> None:
        config = self.private / "config.php"
        config_bytes = config.read_bytes()
        config.unlink()
        try:
            status, _, body = self.request("POST", data={"name": "Bez configu", "email": "missing@example.test", "message": "x"})
            check(status == 503 and "nepodařilo předat" in body.decode("utf-8"), "chybějící config hlásí úspěch nebo jinou chybu")
        finally:
            config.write_bytes(config_bytes)
        self.write_config(transport="disabled")
        status, _, body = self.request("POST", data={"name": "Zakázáno", "email": "disabled@example.test", "message": "x"})
        check(status == 503 and "Lokální test" not in body.decode("utf-8"), "disabled transport hlásí lokální nebo falešný úspěch")
        self.write_config(rate_limit=100)
        self.reset_var()
        var = self.private / "var"
        var.mkdir(parents=True)
        (var / "capture").write_text("blokace", encoding="utf-8")
        status, _, body = self.request("POST", data={"name": "Capture", "email": "capture@example.test", "message": "x"})
        check(status == 503 and "nepodařilo předat" in body.decode("utf-8"), "chyba capture hlásí falešný úspěch")
        self.reset_var()
        self.record("missing-disabled-capture-failure")

    def test_rate_concurrency_and_cleanup(self) -> None:
        rate = self.private / "app" / "rate.php"
        state = self.private / "var" / "rate-cli"
        state.mkdir(parents=True)
        code = "require $argv[1]; echo \\Imbolg\\rateAllowed($argv[2], '127.0.0.1', 'local-secret', 5, 60) ? '1' : '0';"
        commands = [php_command() + ["-r", code, str(rate), str(state)] for _ in range(12)]
        processes = [subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) for command in commands]
        outputs = [process.communicate(timeout=20) for process in processes]
        check(all(process.returncode == 0 for process in processes), "souběžný PHP rate test skončil chybou")
        allowed = sum(out.strip() == "1" for out, _ in outputs)
        check(allowed == 5, f"souběžný rate limit povolil {allowed} místo 5 požadavků")
        # Start the expiry proof from its own state, otherwise present-time
        # concurrent buckets would correctly survive the artificial timestamp.
        (state / "rate.json").unlink()
        expiry_code = ("require $argv[1]; $d=$argv[2]; "
                       "\\Imbolg\\rateAllowed($d,'192.0.2.1','local-secret',5,60,1000); "
                       "\\Imbolg\\rateAllowed($d,'192.0.2.2','local-secret',5,60,1061); "
                       "echo file_get_contents($d.'/rate.json');")
        expiry = subprocess.run(php_command() + ["-r", expiry_code, str(rate), str(state)], text=True, capture_output=True, timeout=20)
        check(expiry.returncode == 0, "rate cleanup CLI skončil chybou")
        state_json = json.loads(expiry.stdout)
        check(len(state_json) == 1 and all(isinstance(item, list) and len(item) == 1 for item in state_json.values()),
              "rate cleanup neodstranil expirované bucket")
        serialized = (state / "rate.json").read_text(encoding="utf-8")
        check("@" not in serialized and "message" not in serialized and "192.0.2." not in serialized,
              "rate stav obsahuje soukromá vstupní data nebo IP")
        self.remove_fixture_tree(state)
        self.record("rate-concurrency-expiry-privacy")

    def test_capture_and_smtp_failure_boundaries_cli(self) -> None:
        transport = self.private / "app" / "transport.php"
        autoload = self.private / "vendor" / "autoload.php"
        refusal = """
require $argv[1]; require $argv[2];
$c=['transport'=>'capture','from'=>'form@example.invalid','rate_key'=>str_repeat('a',32),'rate_limit'=>1,'rate_window'=>60];
$caught=0;
try { \\Imbolg\\configuration($c, '127.0.0.1'); } catch (\\Throwable $e) { $caught++; }
putenv('IMBOLG_LOCAL_CAPTURE=1');
try { \\Imbolg\\configuration($c, '203.0.113.7'); } catch (\\Throwable $e) { $caught++; }
echo $caught;
"""
        safe_env = {key: value for key, value in os.environ.items() if key != "IMBOLG_LOCAL_CAPTURE"}
        result = subprocess.run(php_command() + ["-r", refusal, str(autoload), str(transport)], text=True,
                                capture_output=True, timeout=20, env=safe_env)
        check(result.returncode == 0 and result.stdout == "2", "capture lze aktivovat bez env nebo mimo loopback")
        smtp_failure = """
require $argv[1]; require $argv[2];
class ThrowMailer extends \\PHPMailer\\PHPMailer\\PHPMailer { public function send() { throw new \\RuntimeException('synthetic'); } }
class FalseMailer extends \\PHPMailer\\PHPMailer\\PHPMailer { public function send() { return false; } }
$c=['transport'=>'smtp','smtp'=>['host'=>'mail.example.invalid','port'=>587,'encryption'=>'tls','username'=>'x','password'=>'y']];
$caught=0;
foreach ([new ThrowMailer(true), new FalseMailer(true)] as $mailer) { try { \\Imbolg\\deliver($mailer, $c, 'unused'); } catch (\\RuntimeException $e) { $caught++; } }
echo $caught;
"""
        result = subprocess.run(php_command() + ["-r", smtp_failure, str(autoload), str(transport)], text=True,
                                capture_output=True, timeout=20, env=safe_env)
        check(result.returncode == 0 and result.stdout == "2", "SMTP výjimka nebo false send nevede k chybě")
        self.record("capture-loopback-env-refusal-and-smtp-send-failures")

    def test_browser_without_javascript(self) -> None:
        ARTIFACTS.mkdir(parents=True, exist_ok=True)
        with sync_playwright() as playwright:
            browser, browser_name = chrome_for(playwright)
            try:
                context = browser.new_context(java_script_enabled=False, viewport={"width": 390, "height": 900})
                page = context.new_page()
                errors: list[str] = []
                page.on("pageerror", lambda error: errors.append(str(error)))
                response = page.goto(self.base + "/", wait_until="domcontentloaded")
                check(response is not None and response.status == 200, "browser nenahrál úvod")
                page.locator("#contact-name").fill("   ")
                page.locator("#contact-email").fill("browser@example.test")
                page.locator("#contact-message").fill("Bez JavaScriptu")
                page.locator(".contact-form button[type=submit]").click()
                page.wait_for_load_state("domcontentloaded")
                check("Zkontrolujte prosím označená pole." in page.locator(".form-summary").inner_text(),
                      "browser nevidí souhrn serverové chyby")
                check("Vyplňte prosím toto pole." in page.locator("#name-error").inner_text(),
                      "browser nevidí konkrétní chybu jména")
                check(page.locator("#contact-email").input_value() == "browser@example.test", "chybový návrat nezachoval e-mail")
                check(page.locator("#contact-message").input_value() == "Bez JavaScriptu", "chybový návrat nezachoval zprávu")
                page.screenshot(path=str(ARTIFACTS / "no-js-error.png"), full_page=True)
                page.locator("#contact-name").fill("Browser Hana")
                page.locator(".contact-form button[type=submit]").click()
                page.wait_for_load_state("domcontentloaded")
                check("Lokální test" in page.locator("main").inner_text(), "opravený browser formulář neprošel capture")
                page.screenshot(path=str(ARTIFACTS / "no-js-success.png"), full_page=True)
                check(not errors, f"browser hlásil pageerror: {errors}")
                context.close()
                self.results["browser"] = browser_name
            finally:
                browser.close()
        self.record("browser-no-javascript-error-repair")


def main() -> None:
    proof = FormProof()
    try:
        proof.test_success_and_mime()
        proof.test_optional_empty_message()
        proof.test_query_overrides_are_ignored()
        proof.test_validation_and_escaping()
        proof.test_size_honeypot_and_protocol()
        proof.test_rate_proxy_and_private_http()
        proof.test_missing_disabled_and_capture_failure()
        proof.test_rate_concurrency_and_cleanup()
        proof.test_capture_and_smtp_failure_boundaries_cli()
        proof.test_browser_without_javascript()
        ARTIFACTS.mkdir(parents=True, exist_ok=True)
        (ARTIFACTS / "results.json").write_text(json.dumps(proof.results, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
        print(json.dumps(proof.results, ensure_ascii=False))
    finally:
        proof.close()


if __name__ == "__main__":
    main()
