# Formulář A5

Implementace používá PHP 8.3 a PHPMailer 7.1.0. A5 místně DONE: npm run verify prošel včetně deseti skupin A5 testů a skutečné opravy chyby/odeslání do capture v Chrome bez JavaScriptu. Důkazy: artifacts/a5/results.json, no-js-error.png, no-js-success.png a WORKLOG. POST /api/contact.php přijímá pouze application/x-www-form-urlencoded bez příloh. Jméno (200 Unicode znaků) a e-mail (254 bajtů) jsou povinné; zpráva (10 000 Unicode znaků) je volitelná podle A2. Limit celého zakódovaného těla je 64 KiB, takže velká zpráva se může do limitu těla nevejít. Stejný HTML partial v server/app/templates/contact-form.html používá statický úvod i PHP chybový návrat. Vstupy v návratu jsou escapované, transport vytváří prostý text. Nové required ani změny původních popisků nebyly přidány.

## Lokální prostředí

Na tomto Windows je ověřené izolované PHP v `.runtime/php83/php.exe` (8.3.35 NTS x64) a Composer v `.runtime/composer.phar` (2.10.3). Ani jeden není globálně instalovaný. Oficiální downloady a ověřené SHA-256 jsou ve WORKLOG. Runtime je ignorovaný Gitem. Na jiném stroji použij ověřenou PHP 8.3 distribuci a nastav `IMBOLG_PHP` na absolutní cestu binárního souboru; fixture ověřuje hlavní a vedlejší verzi. Lokální helper nečte globální php.ini, načte openssl a blokuje mail, fsockopen, pfsockopen a stream_socket_client.

Obnovení produkčních PHP závislostí z lockfile (pouze místně, ne na hostingu):

```powershell
& 'C:\Users\ondrej.dolejs\Desktop\Projekty\imbolg_harmony\.runtime\php83\php.exe' 'C:\Users\ondrej.dolejs\Desktop\Projekty\imbolg_harmony\.runtime\composer.phar' install --working-dir='C:\Users\ondrej.dolejs\Desktop\Projekty\imbolg_harmony\server' --no-dev --no-scripts --no-plugins --prefer-dist --no-interaction
```

Pokud systémová proxy vrací 407, použij v daném procesu funkční přímé HTTPS, bez vypnutí ověřování certifikátů. Strom obsahuje jediný runtime balík PHPMailer. Jeho vlastní require-dev/scripts se nespouštějí; kořen má allow-plugins false, žádné scripts. Vendor nikdy nekopíruj do veřejného adresáře.

Z ověřeného kořene projektu spusť `npm run test:form`. Příkaz nejprve sestaví statický web, vytvoří novou fixture pod private/a5 a spustí její PHP server pouze na 127.0.0.1 s DocumentRoot public. Fixture má public/api/contact.php a sourozence private/app, private/vendor, private/config.php. Konfigurace obsahuje jen náhodný lokální rate klíč a syntetický From form@example.invalid. Po testu se server zastaví a fixture i zachycené syntetické zprávy odstraní. Souhrnný důkaz a snímky patří do artifacts/a5, bez produkčních přístupů a osobních údajů.

`npm run preview:form` spustí stejný izolovaný capture náhled a vypíše skutečnou lokální URL s volným portem. Používej pouze smyšlené kontakty a zprávy. Ctrl+C server ukončí a fixture odstraní. Nespouštěj PHP server nad kořenem repozitáře ani nad rodičem public/private. Eleventy `npm run dev` PHP nespouští; jeho statický formulář nemůže potvrdit odeslání. API PHP není součástí statického dist, do public se dosadí až ve fixture a pozdějším balíku.

## Konfigurace a produkční hranice

`server/config.example.php` je nefunkční vzor. Skutečný config.php se načítá výhradně z private vedle DocumentRoot; bootstrap nikde nehledá veřejný config. Doménové SMTP přístupy nejsou dodané a nebyly vymyšlené. SMTP vyžaduje transport smtp, enabled true, from_verified true, ověřenou adresu @imbolg-harmony.cz, přístupové údaje a TLS/SSL na 587/465. From_verified je potvrzení správce, kód vlastnictví schránky sám neověří. Nastavení TLS ověřování certifikátů PHPMailer zůstává výchozí, žádný debug s přístupy se nevypisuje. Návštěvník nemůže měnit recipient, server, transport ani cestu.

Příjemce je pevně kralovamarket@seznam.cz. From pochází výhradně z config; návštěvník je pouze Reply-To. Výchozí disabled nebo chybějící config vrací bezpečnou HTTP 503. Chyby nikdy nevypisují výjimku ani přístupy a nikdy nehlásí úspěch. SMTP úspěch říká pouze předání k odeslání, ne skutečné doručení.

Capture se aktivuje výhradně soukromou konfigurací spolu s environment IMBOLG_LOCAL_CAPTURE=1, loopback REMOTE_ADDR a syntetickým From @example.invalid. HTTP ani pole formuláře tyto přepínače neurčují. Capture používá PHPMailer preSend pro skutečný MIME, žádné send/mail ani SMTP, a ukládá .eml pouze do private/var/capture. Pro budoucí produkční balení nepřevzít testovací config, var ani capture environment; A6 musí kopírovat jen čistý vzor a runtime podle mapy. A5 žádný release ani veřejný upload nevytvořila.

## Omezení zneužití

Výchozí limit je pět pokusů z jedné REMOTE_ADDR za deset minut. Pro malý kontaktní web omezuje automatické opakování a dovoluje opravu chyby; počítá i nevalidní pokusy po načtení konfigurace. Sdílená IP může limit sdílet mezi návštěvníky. Limity jsou konfigurovatelné (1–100 pokusů, okno 1–86 400 sekund). X-Forwarded-For se ignoruje; případný důvěryhodný reverse proxy vyžaduje zvláštní ověřenou konfiguraci později.

Rate stav je jeden flock chráněný private/var/rate.json: HMAC IP pomocí neveřejného náhodného rate_key a časová razítka. Neukládá jména, e-maily ani zprávy. Při každém dalším pokusu se odstraní starší časy i prázdné klíče, maximálně 10 000 současných IP klíčů. Při absenci provozu fyzický soubor zůstává, obsah se pro rozhodování po expiraci už nepoužije a při příštím pokusu se vyčistí. Nemožnost zápisu či poškozený JSON vrací 503, nemůže obejít limit. Nepřevádět var do veřejných souborů ani jej používat pro historii komunikace.

## Soukromí a neověřené skutečnosti

Pracovní návrh krátké informace je v IMPROVEMENTS; není vložený do veřejného textu ani schválený. Před publikací v C1 doplnit skutečného správce, právní základ, dobu uchování, podmínky hostingu/Seznamu, informace o právech a kontakt pro jejich uplatnění. Identitu, IČO ani dobu uchování nevymýšlet. Tok: prohlížeč → PHP validace → TLS SMTP hostingu → pevný příjemce Seznam; návštěvnické údaje jsou v těle a Reply-To. Aplikace mimo testovací capture nearchivuje zprávy; poskytovatelé či schránka je mohou uchovávat dle skutečných nastavení. Stav ochrany formuláře je oddělený krátkodobý HMAC stav. A5 nepřidala analytiku, CAPTCHA ani cookies.

Produkční SMTP a skutečné doručení neověřené. Žádná skutečná testovací zpráva se neodesílá; případný ruční test produkce provede uživatel v samostatně objednané fázi. A6 používá společný release populate pro fixture i balík. Její browser test dočasně zvětší text přes same-origin CSS odpověď, takže původní CSP zůstává zapnutá. Lokální router je pouze test/preview nástroj a do release nepatří.
