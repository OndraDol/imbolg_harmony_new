# Předání redesignu Claude Opus

## Dokončená B2 a schválení / 2026-10-07

**B2 DONE:** finální varianta 1B Fotka je porovnaná s ověřenou A6, lokální regrese jsou opravené a majitelka prostřednictvím uživatele výslovně schválila konkrétní verzi. Po uvedení označení `B2-2026-10-07-ef779044` uživatel napsal „Je to schváleno.“ Záznam souhlasu a podrobný přehled jsou v [B2-REVIEW](B2-REVIEW.md), WORKLOG a `artifacts/b2/approval.json`. Souhlas se týká vzhledu, ne nasazení nebo zahájení C1/C2.

Aktuální identita je `ef7790446ba6470d3cee43694c399722296831a98176af803efc7a08e6fdb820`. Místní release obsahuje 239 souborů / 50 430 699 B, public 49 898 869 B a private 531 830 B. Package SHA-256 `eaa15904b8bc65dc169069dffa13d7a6a7661aedacd1e639cb0678145042527e`. Autoritativní manifest, verze a výsledky jsou v `artifacts/b2`; `readback-results.json` PASS propojuje aktuální soubory, všechny kontroly, snímky a náhled. Výchozí Git HEAD před dokumentační uzávěrkou byl `c85e298300508adb53c5938df8ee4f9105c4dab6`; nový povolený commit/push se týká dokumentace a historie, implementace B1/B2 zůstává místní a necommitovaná. Skutečný Git readback je ve WORKLOG/STATUS.

Proti B1 se změnily pouze tři řádky CSS a přidal se `tests/browser_b2.py`. Opravený formulář se při 200% textu vejde do své karty a hover na diplomech úvodní galerie nepřebíjí contain výjimky. Nezávislé porovnání s A2 má 0 rozdílů: 10 URL, 78 textových uzlů, 46 bloků, 47 médií, 83 výskytů, 26 galerijních položek a 179 původních odkazů. Chráněné baseline, obsah, fotografie, pořadí, metadata, recipient, SMTP, serverová validace i původní testy zůstávají stejné.

Finální browser prošel 8/8 skupinami, 160 stránkovými režimy včetně JS/no-JS a 200% textu/zoom na 360/390/768/1440 px, 16 formulářovými scénáři, 456 obrazovými výskyty, 208 otevřeními plné galerie a 266 interními odkazovými výskyty. Nečekané console/page/network chyby: 0. Deset A5 skupin PASS používá pouze místní syntetický capture. Cílené nové kontroly mají 48 formulářových stavů a 40 contain hover PASS. Vizuální evidence má 120 režimů viditelnosti textu, 228 obrazových screenshotů a 40 čistých plných stránek; osobní prohlídka pokryla všechny stránky a ořezy, po opravách znovu dotčené části.

Hotový [náhled A6/B2](../artifacts/b2/nahled/index.html) a [přenositelný ZIP](../artifacts/b2/B2-2026-10-07-ef779044-nahled.zip) obsahují 80 snímků deseti stránek ve čtyřech šířkách. Srovnávací A6 se před snímáním shodovala ve všech 148 veřejných souborech s původními hashi. Browser ověřil všech 40 dvojic, no-JS režim a mobil bez přesahu. Jde o snímky, ne interaktivní web; živá mapa je v nich vypnutá. Náhled ani balík nebyly zveřejněné nebo odeslané třetí osobě.

Skutečné SMTP/doručení, živá Google Maps, dostupnost Facebook profilu a cílový hosting nejsou místními testy prokázané. Uživatel 2026-10-07 výslovně potvrdil oprávnění k původním médiím; kredity se zachovávají a jednotlivé autory z toho neodvozujeme. C1 ověřila Webnode administraci, registr, DNS, fakturu, veřejné kontakty i obsah; schválená B2 se nezměnila. Vybraný plán je doména/DNS u Webnode, web u Praktiku a Seznam SMTP; nynější PHP Seznam From ještě nepřijímá. Účet imbolg.harmony.formular@seznam.cz má ruční registraci uživatele a skutečný readback, přístup DPAPI v .secrets se do předání nekopíruje. Správce/návrh soukromí jsou připravené a skutečná místní šifrovaná záloha kompletně obnovená s kontrolou každého souboru; C1 BLOCKED pouze na DNS/editaci po Standardu podle STATUS. Obnova 3 074 souborů na disk je ověřená, jiný PC/profil se netestoval. Příjemce a historie Seznamu zůstávají, veřejná doménová adresa nebyla nalezená. Na nový výslovný pokyn byl odeslaný jeden dotaz Webnode jménem majitelky; přijetí doložené, vlastní technická odpověď dosud chybí. Konkrétní postup/návrat je v MIGRATION, přístupy v ACCESS. Nasazení, změna DNS/registrátora ani skutečný SMTP test neproběhly; dokumentační commit/push je nově povolený, C2 vyžaduje nové zadání. Po uzávěrce dokumentace čekat na odpověď Webnode, další zprávu neposílat. Následující oddíly zachovávají historický stav B1 a A6, jejich tehdejší omezení a identity nejsou aktuálním stavem C1 nebo schválenou B2.

## Dokončená aplikace B1 / 2026-10-07

**B1 DONE v aktuálně objednaném rozsahu:** návrh varianty 1B Fotka z `C:\Users\ondrej.dolejs\Desktop\Imbolg Harmony redesign.zip` je aplikovaný a místně ověřený. Uživatel potvrdil práci Claude a výslovně objednal její aplikaci; přesný model v ZIP není doložený. Tato relace nespouštěla Claude ani nepřebírala autorství původního návrhu. Původní A6 před aplikací prošla hashovým ověřením v `artifacts/b1/a6-precheck.json`. Dodané dokumenty se sloučily, původní historie a obsahové návrhy zůstávají zachované. Místní opravy uzavírají zavřené mobilní menu a čtyři ořezy fotografií; texty, menu, galerie, URL, formulářová logika a technologie jsou beze změny.

Finální identita `57dd03c08304df612f112ccc11209eac7660fd35032eca498c53bca71e45f17e` je v `artifacts/b1/version.json`. Package SHA-256 `bade1c15ae78f5843da9d4d94d365239a7438dcb40177cce6908aacc0c9bfc88`, manifest v `artifacts/b1/release-manifest.json`: 239 souborů / 50 430 625 B, public 49 898 795 B a private 531 830 B. `artifacts/b1/readback-results.json` PASS přepočítal všechny soubory, nezměněné chráněné vstupy, identity důkazů a hashové indexy snímků. V balíku není config ani zachycená zpráva, testovací private fixture je prázdná. Důkazy a archivy zůstávají mimo veřejný build a jsou ignorované Gitem.

Předepsané `npm run verify` a závěrečné `npm run verify:browser` skončily exit 0, výstupy `artifacts/b1/verify.log` a `browser-final.log`. Finální formulářová regrese `python tests/test_form_a5.py` exit 0 je v `form-final.log`. Obsahová kontrola: 10 URL, 78 textových uzlů, 46 bloků, 47 médií, 83 výskytů, 26 galerijních položek a 179 původních odkazů, 0 rozdílů. Browser Chrome 154.0.8037.98: 8/8 skupin JS/no-JS na 360/390/768/1440 px, 160 stránkových režimů včetně 200% textu/zoom, 16 formulářových scénářů, 456 načtených obrazových výskytů, 208 plných galerijních souborů, 0 nečekaných console/page/network chyb. Formulář všech deset skupin PASS s lokálním syntetickým capture a blokovaným poštovním síťovým transportem.

Dodatečně ověřená skutečná viditelnost původních textů ve 120 režimech a 228 obrazových boxů v `artifacts/b1/visual-results.json`; contain při hover v `hover-results.json`. Hlavní agent osobně prohlédl všechny ořezy na čtyřech šířkách a všechny finální stránky v osmi přehledech `pages-{360,390,768,1440}-{1,2}.jpg`, včetně samostatné galerie na 390 px, formulářových odpovědí, otevřeného menu a 404. Čtyřicet čistých snímků je v `artifacts/b1/{home,o-nas,sluzby,nase-prace,fotogalerie,cenik,kontakt,vrh-a,feny,psi}-{360,390,768,1440}.png`, index `clean-screenshot-index.json`. Nezávisle zachovaných 200 povinných snímků původního harnessu indexuje `artifacts/b1/screenshot-index.json`; screenshot po BrowserBack může znovu odložit lazy obraz mimo viewport, proto čisté náhledy vznikly přímým otevřením a decode všech místních fotografií. Testy se kvůli tomu neměnily.

Při uzávěrce B1 ještě B2 nezačala a schválení majitelkou nebylo doložené; aktuální dokončení a souhlas zaznamenává úvodní oddíl B2. Produkční SMTP, skutečná pošta, živá Google Maps, účty, práva médií a hostingové podmínky zůstávaly neověřené. Nedošlo k uploadu, publikaci, DNS změně, commitu, push ani externímu zápisu. Obsahové návrhy jsou v IMPROVEMENTS a nebyly provedené.

## Historické předání A6

Následující text zachovává původní předání před redesignem a tehdejší Git stav. Původní odkazy `artifacts/a6/*` a `artifacts/a5/*` v této historické části nyní čti ze zachovaných `artifacts/b1/a6-before/*` a `artifacts/b1/a5-before/*`; původní harness stejné pracovní složky znovu použil pro B1/B2. Historické B1 důkazy jsou v `artifacts/b1`, aktuální B2 důkazy v `artifacts/b2`, aktuální Git kontext v STATUS.

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
