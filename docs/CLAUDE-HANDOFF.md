# Předání redesignu Claude Opus

**A6 DONE: připraveno pro redesign.** Místní veřejný obsah, formulář, viewporty a balík jsou ověřené níže uvedenými důkazy. B1 smí začít jen po výslovném zadání uživatele. Toto předání nespouští Claude ani nové vlákno. Web není připravený k publikaci, dokud nejsou vyřešené níže uvedené podmínky C1/C2.

## Identita a skutečné podklady A6

| Podklad | Důkaz / výsledek |
|---|---|
| Commit / identita | HEAD `5236f348a5753ec651b223184cd9e2da4aef3821` je pouze předchozí commit. A2–A6 jsou necommitované. Autoritativní identita 415 zdrojových, buildových a vendor souborů + 4 evidencí: SHA-256 `5f0a89085b9cc41e7062537f8164a369a191861b929f259771449475927e1fec`, jednotlivé cesty/hashe v `artifacts/a6/version.json`. |
| Náhled | `npm run preview:form` z ověřeného kořene, vlastní loopback port, capture bez odesílání a Ctrl+C úklid. `npm run dev` je pouze statický náhled. |
| Nezávislý obsah | A2 `archive/2026-10-06T13-40-23Z/`, `evidence/pages.json`, `media.json`, `source-map.json`, `exclusions.json`; poslední A4 ověření má 10/10 URL, 78 textových uzlů, 46 bloků, 47 médií, 83 výskytů, 26 galerijních položek a 179 původních odkazů, 0 chyb. |
| Formulář | Finální `python tests/test_form_a5.py`: exit 0, 10 skupin v `artifacts/a5/results.json`, no-JS snímky ve stejné složce. Server testuje stejný public/private strom jako release, síťové poštovní funkce vypnuté. Produkční SMTP a skutečné doručení nejsou ověřené. |
| Browser | `python tests/browser_a6.py` exit 0; 8/8 samostatných procesů a souhrnný PASS v `artifacts/a6/browser-results.json`, všechny s výše uvedeným version SHA. Google Chrome 154.0.8037.98; 160 stránkových režimů, 16 formulářových scénářů, 456 načtených obrazových výskytů, 208 otevřených plných galerijních souborů a 266 interních odkazových výskytů. 0 pageerror, 0 nečekaných console chyb a 0 selhaných lokálních requestů. |
| Původ a práva médií | Zachované původní 43 JPEG + 4 SVG a WebP deriváty. Žádné nové AI obrazy. Obecný kredit Pexels zachovaný, jednotlivé původy/oprávnění neověřené, publikace blokovaná do vyřešení v C1. |
| Kompletní balík | `release/public` + `release/private`: 239 souborů, **50 406 788 B = 50,406788 MB**, public 49 874 958 B, private 531 830 B; limit 80 000 000 B splněn, rezerva 29 593 212 B. Každý soubor, bajty a SHA-256 v `artifacts/a6/release-manifest.json`. Package SHA-256 `719e6da0f1ceb81a1c7b2547f719f6da51132bd543b469c8c9692fb8fa415ea9`. |
| Konečný readback | `artifacts/a6/readback-results.json` PASS: přepočtená identita odpovídá browser důkazům, všech 239 souborů odpovídá manifestu, 200 povinných snímků je čerstvých a neprázdných. Jejich jednotlivé velikosti a SHA-256 jsou v `artifacts/a6/screenshot-index.json`. Testovací private fixture je prázdná, skutečný config a capture soubory chybějí. |
| Administrace Webnode | Neověřená; veřejný archiv není záloha účtu. Neveřejné/neodkazované stránky, koncepty, balíček a pošta čekají na C1. Neopakovat neúspěšné přihlašovací pokusy bez změny situace. |

Všechny cesty jsou relativní ke kořeni `C:\Users\ondrej.dolejs\Desktop\Projekty\imbolg_harmony`. Archiv a artifacts jsou záměrně ignorované Gitem: samotný checkout ani HEAD je neobsahuje. Claude potřebuje tentýž lokální workspace, nebo výslovně připravené předání veřejné evidence a výše uvedených důkazů. Nikdy nepředávat `.secrets`, skutečnou SMTP konfiguraci, sessions, testovací zprávy ani poštu.

## Ověřené příkazy a reprodukce

```text
npm run verify:browser
python scripts/release_a6.py
python tests/browser_a6.py
python tests/test_form_a5.py
```

Při posledním běhu prvního příkazu prošel build, A3 a verify:content, browser se potom odpojil. Po opravě pouze kontrolního harnessu se neopakoval nezměněný úspěšný build: druhý příkaz zaznamenal novou identitu a tentýž balík, třetí dokončil 8/8 browser skupin s exit 0. Poslední příkaz dokončil 10 A5 skupin s exit 0 nad týmž finálním dist; od tohoto formulářového PASS se měnil jen browser harness, žádný soubor v balíku. Celou browser kontrolu lze reprodukovat prvním npm příkazem, který dnes obsahuje stejný finální dělený harness. Běžný `npm run verify` sestaví web a provede A3/A4/A5; samostatné `npm run test:form` nejprve sestavuje. Lokální balení lze zopakovat přes `npm run release`. Žádný z příkazů neprovádí upload, DNS, objednávku ani skutečný e-mail.

## Snímky a osobní vizuální posouzení

`artifacts/a6/{home,o-nas,sluzby,nase-prace,fotogalerie,cenik,kontakt,vrh-a,feny,psi}-{360,390,768,1440}-js{0,1}.png` jsou skutečné plné snímky všech deseti stránek. Další `*-text200.png` a `*-zoom200.png` dokládají zvětšení, `menu-*.png` otevřené klávesnicové menu, `form-{error,success}-*.png` chybový návrat a capture, `404-*-js*.png` neznámou URL. Snímky zachycují i aktivní focus po testu; nejde vždy o výchozí pozici stránky před interakcí. U CSS zoom v malé šířce může focus posunout horní část záběru; úplnou značku dokládají normální a text200 snímky a zvlášť otevřené menu.

Hlavní agent prohlédl celé přehledy všech deseti stránek ve všech čtyřech šířkách (`review-normal-*-{1,2}.png`), detaily home/galerie/kontaktu v obou zvětšeních (`review-enlarged-*.png`), formulář normal/text200, zvětšené otevřené menu a mobilní/desktopovou vlastní 404. Bez chybějícího obsahu, přetékání, překryvu či ztráty motivu ve vlastních obrázcích. Offline mapa je záměrně prázdná testová odpověď, ne chybějící autorský obsah. Galerijní focus nyní obepíná snímek, dlouhé URL/název se zalamují a posouvání je okamžité. Převzaté obrázky se neupravovaly. Výsledné CSS kontrasty v `artifacts/a6/contrast.json`: body 14,90:1, odkazy 7,43:1, patička 6,27:1, chyby 7,86:1, aktivní menu 6,56:1.

Read-only reviewer_terra (GPT-5.6 Terra, high) posoudil balení a důkazy. Dvě materiální mezery byly opravené: hash identity zahrnuje skutečný dist/vendor a instalovaná PHP verze/reference se porovnává s lockem. Doporučení pro viditelný 404 main/h1 bylo rovněž doplněné a prošlo. Příčina někdejšího odpojení driveru nebyla prokázaná; osm samostatných procesů odstranilo provozní překážku. Neúspěšné pokusy a opravy jsou v WORKLOG, nejsou započtené jako PASS.

Python potřebuje již přítomné Playwright, BeautifulSoup a Pillow; PHP 8.3.35 je v `.runtime/php83/php.exe`, PHPMailer 7.1.0 v produkčním `server/vendor` podle `server/composer.lock`. Obnovení prostředí je v README a FORM. Browser test používá skutečný systémový Google Chrome v headless režimu, vlastní kontexty a loopback PHP; uživatelské karty ani přihlášení nepřebírá.

Metadata jsou převzatá read-only z A2: titulky, description i canonical. Sitemap zachovává deset URL s koncovými lomítky, robots neblokuje veřejný obsah. 404 má vlastní stránku a noindex; `.htaccess` obsahuje ErrorDocument, DirectoryIndex a zákaz výpisu adresářů. Lokální PHP router emuluje ErrorDocument a do balíku se nekopíruje. C1 musí na skutečném hostingu ověřit Apache/AllowOverride, HTTP 404 s vlastním viditelným tělem, private HTTP nedostupnost a directory listing.

## Chráněné části a hranice B1

| Část | Pravidlo |
|---|---|
| `evidence/*.json`, archiv A2 | Nezávislý kontrolní základ. Neodvozovat z nového webu, nepřepisovat kvůli testu. |
| `src/content/pages.json` | Každý text, opakování, datum, číslo, emoji a původní pořadí jsou chráněné. |
| `src/content/media-alt.json`, `src/assets/images/` | Zachovat identitu, původní plné fotografie a čitelnost diplomů; nevynechat položku ani výskyt. Změny ořezu vyžadují kontrolu skutečného obrazu. |
| `src/_data/sitePages.json`, metadata | Všech deset položek menu a URL v původním pořadí, původní titulky a popisy. |
| `server/`, formulářový partial, FORM | POST smlouva, povinné jméno/e-mail, nepovinná zpráva, fixed recipient, From/Reply-To, CSP, rate limit a bezpečné chyby. Nezasahovat do SMTP ani validace kvůli vzhledu. |
| Release mapa | Pouze public je DocumentRoot; app/vendor/config/var jsou v sourozeneckém private. Žádné přístupy, archiv, docs, node_modules nebo testovací capture v uploadu. `.generated-a6` je lokální ochranná značka, nenahrávat. |
| Šablony/CSS/prezentační JS | Prostor B1 po objednání. Zachovat landmarky, focus, no-JS menu/formulář, technická metadata a 404. Žádný nový framework, tracking, placená služba ani AI náhrada psů. |

## Otevřené podmínky publikace a rozsah ověření

Převzatý je přesně veřejný základ A2, ne účet Webnode. Před přepnutím ověřit změny od archivu, skryté stránky a soukromé koncepty. Rozhodnout a doložit jednotlivá práva fotografií/ikon; veřejný obecný Pexels kredit sám licenci nedokazuje.

Produkční From/SMTP přístupy nejsou dodané. Release obsahuje jen disabled vzor a žádný `private/config.php` ani `var`. Místní capture PASS nepotvrzuje SMTP ani doručení do Seznamu. Doplnění informace o osobních údajích čeká na skutečné údaje a schválení v C1; návrh v IMPROVEMENTS se automaticky nevkládá.

Google Maps je zachovaná externí volitelná mapa s původní URL. Browser test ji nahrazuje offline odpovědí a vyžaduje vykreslení všech vlastních textů a fotografií bez jakékoli CDN; samotnou živou mapovou službu netestuje. Facebook má přesně původní URL a text, živý fetch byl omezen (`Online fetch throttled`), takže dostupnost profilu není PASS. Pexels cíl byl čitelný. Telefony/e-maily jsou přesné linkové cíle, test nespouští hovory ani mail klienta.

Testy přístupnosti jsou konkrétní lokální geometrické, sémantické, klávesnicové a obrazové kontroly, ne certifikace celého WCAG ani čtečky obrazovky. Zvětšení zahrnuje skutečné 32px body přes 200% root text a `zoom:2` v Chrome; nejde o ručně kliknutý zoom v uživatelském Chrome. Galerie používá nativní místní plný soubor, žádný modal lightbox. Enter/Back a opětovný focus se testují; Escape/focus trap lightboxu je N/A. Automatické obnovení activeElement nativním browser Back není garantované.

Plný npm audit má dřívějších 9 vývojových nálezů (4 moderate, 5 high), produkční npm strom 0; Node běží pouze místně a žádné node_modules nejsou v release. V A6 se verze závislostí neměnily. Náklady/tarif, konkrétní hostingové cesty, doména, DNS a doménová pošta patří až C1/C2. Nic není nasazené a vzhled není schválený majitelkou.

## Zadání pro Claude

Pracuješ ve fázi B1. Načti README, AGENTS, STATUS, ARCHITECTURE a toto předání. Implementuj vizuální redesign chovatelské stanice Imbolg Harmony. Majitelka je spokojená s obsahem a rozdělením webu; zlepši vzhled, přehlednost a využití autentických fotografií na mobilu a PC.

Zachovej deset položek menu, původní URL, každý textový blok, média, galerie, odkazy a formulářovou smlouvu. Texty nekrátit a neparafrázovat, neměnit fakta ani emoji. Nepřidávat zdravotní/chovatelské sliby nebo AI náhrady skutečných psů. Nepředpokládat autorství majitelky jen podle umístění souboru na webu.

Měň především šablony, CSS a prezentační JavaScript. Zdrojový základ, obsahová data, SMTP a bezpečnost formuláře jsou chráněné. Nezaváděj nový framework, databázi, serverový Node ani placené služby. Každý krok zdokumentuj.

Použij existující kontroly. Rozbitý obsahový test oprav úpravou výsledku, ne baseline. Při změně ořezu ověř motiv a případné údaje v obrazu. Zachovej čtení, navigaci a formulář bez JS. Návrhy textových změn zapiš odděleně do IMPROVEMENTS.

Výstup: návrh vzhledu, kontrolní výsledky, skutečné screenshoty čtyř šířek a otevřené otázky. Nic nepublikuj. Schválení majitelkou a finální regresi řeší B2.
