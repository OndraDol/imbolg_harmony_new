# Imbolg Harmony

## Aktuální postup C2 (2026-10-10)

C2 je po dokončení technické přípravy BLOCKED na rozhodnutí o HTTPS/DNS a přijetí textu soukromí u formuláře. Praktik je objednaný a zaplacený do 10. 10. 2027. Nový public/private release má 239 souborů / 50 431 106 B; celý byl nahraný přes FTPES, každý soubor zpětně ověřený SHA-256. Všech deset stránek načtených z cílové IP bajtově souhlasí s releasem. PHP 8.3.33 běží a Seznam SMTP se ze serveru autentizoval bez odeslání zprávy. Konfigurace je mimo DocumentRoot a formulářový transport zůstává vypnutý. HTTPS, ruční doručení a změna veřejného DNS jsou otevřené; původní Webnode a pošta se nemění. Aktuální stav a důkazy jsou v [STATUS](docs/STATUS.md) a [WORKLOG](docs/WORKLOG.md).

Příprava úplné náhrady webu https://www.imbolg-harmony.cz/ a pozdějšího levného přesunu z Webnode. Obsah a současné menu jsou zachované; dodaný redesign od Claude je místně aplikovaný a ověřený.

## Stav před zahájením C2 (2026-10-07)

Tento projekt obsahuje veřejný zdrojový archiv A2 a lokální kopii deseti původních URL s převzatými texty, fotografiemi, galeriemi a odkazy. A4, lokální formulář A5, kontrola A6, aplikace redesignu B1 i regresní kontrola B2 jsou dokončené. Varianta 1B Fotka od Claude zachovává technologii i obsah; B2 opravila formulář při zvětšení a hover diplomů. Finální balík public/private má 50 430 699 B a browser prošel 8/8 skupinami na 360/390/768/1440 px. Majitelka prostřednictvím uživatele výslovně schválila verzi `B2-2026-10-07-ef779044` dne 2026-10-07 zprávou „Je to schváleno.“ Výsledky, konkrétní náhled a souhlas jsou v [B2-REVIEW](docs/B2-REVIEW.md), předání v [CLAUDE-HANDOFF](docs/CLAUDE-HANDOFF.md). Přesná varianta modelu Claude v dodaném ZIP není doložená. Uživatel 2026-10-07 potvrdil oprávnění k původním médiím. C1 ověřila Webnode, registr, DNS, fakturu, veřejné kontakty i obsah a připravila [MIGRATION](docs/MIGRATION.md) pro doménu u Webnode, web u Praktiku a Seznam SMTP. Jediný nalezený veřejný e-mail i příjemce původního formuláře jsou kralovamarket@seznam.cz. Nový účet imbolg.harmony.formular@seznam.cz je po ruční registraci uživatele skutečně ověřený a jeho DPAPI přístup uložený v ignorovaném .secrets. Správce/návrh soukromí připravené a skutečná místní šifrovaná záloha 3 074 souborů kompletně obnovená do oddělené složky a ověřená podle hashů a velikostí. C1 DONE po odpovědi Webnode; DNS správa bez Premium potvrzená, doménovou poštu ověřit před případným ukončením Standardu; přesný dopad je ve [STATUS](docs/STATUS.md). Produkční SMTP a cílový hosting se teprve ověří v autorizované C2, nynější PHP ještě Seznam From nepřijímá. Celý statický web je nyní zveřejněný na GitHub Pages s neaktivním formulářem podle samostatného zadání. Doménová C2 nezačala a vyžaduje nové zadání. Veřejný archiv a jeho omezení popisuje [CONTENT-INVENTORY](docs/CONTENT-INVENTORY.md).

Začni soubory [AGENTS.md](AGENTS.md), [stav](docs/STATUS.md) a [plán](docs/PLAN.md). Podrobné zadání jednotlivých fází je v [docs/phases](docs/phases/). Než začneš, ověř skutečný obsah složky a Git stav.

Na pozdější výslovný pokyn byl 2026-10-07 odeslaný jeden dotaz Webnode; uživatel nyní předal odpověď. Potvrdila DNS správu bez Premium při ponechání domény u Webnode, jeho doménové e-mailové služby Premium vyžadují. C1 DONE, C2 TODO. Před případným ukončením Standardu ověřit skutečné využití doménové pošty/přesměrování a zachovat příjem. Dokumentační push má historii v WORKLOG; samostatné pozdější zadání Pages povoluje i commit současné schválené B2 implementace a veřejnou statickou kopii. Přístupy, soukromé přílohy a ignorované důkazy se nepublikují.

Celý schválený web je zveřejněný na [GitHub Pages](https://ondradol.github.io/imbolg_harmony_new/). [Repozitář](https://github.com/OndraDol/imbolg_harmony_new) je public, main obsahuje schválenou B2 implementaci a dokumentaci, gh-pages pouze 148 veřejných statických souborů. Všech deset stránek, fotografie, galerie, menu a kontaktní mapa jsou dostupné; formulář je podle výslovné volby uživatele neaktivní a nabízí původní e-mail. HTTPS, shodné hashe 147 servírovaných souborů, vlastní 404 a vykreslení všech deseti stránek byly ověřené. Postup a návrat jsou v [PAGES](docs/PAGES.md), důkazy v STATUS/WORKLOG. Původní doména, DNS, Webnode a pošta se nemění, C2 nezačala.

## Rozhodnutí uživatele

- Obsah bude upravovat uživatel přes AI; administrace není požadovaná.
- Zachovat všech deset položek menu a původní URL.
- Texty převzít beze změn. Návrhy oprav předložit odděleně.
- Kontaktní formulář doručuje na `kralovamarket@seznam.cz`.
- Pokud původní web používá doménovou e-mailovou adresu, zachovat ji přeposíláním na Seznam; příjemkyně nemusí používat doménový webmail. Veřejný průzkum takovou adresu nenašel, neveřejné služby se tím nevylučují.
- Doména zůstane spravovaná u Webnode a později se prodlouží tam. Registrátor, NS a DNSSEC se nepřevádějí.
- Web plánovat u Gigaserveru Praktik, odesílání formuláře přes nový samostatný účet Seznam. Příjemcová schránka a její historie zůstávají na místě.
- Oprávnění k původním médiím uživatel výslovně potvrdil; původní kredity zachovat.
- Nejprve úplná funkční kopie, potom redesign v Claude Opus, až následně autorizovaná migrace.

## Pokračování v nové relaci

Příklad samostatného budoucího zadání další fáze, pouze pokud ji uživatel objedná:

```text
/goal Načti README.md, AGENTS.md, docs/STATUS.md a docs/phases/A3.md. Proveď pouze fázi A3 podle jejích vstupů, kroků a kritérií. Každý provedený krok zdokumentuj v docs/WORKLOG.md, na konci aktualizuj docs/STATUS.md. Nezačínej A4, neměň zdrojový web ani DNS a nic neposílej.
```

U další fáze nahraď pouze její označení a cestu. Příkaz `/goal` zadává uživatel v Codexu; není to příkaz PowerShellu ani projektový skript. Pokud zadání fáze nebo její závislosti nejsou splněné, nejprve zjisti konkrétní překážku. Neoznačuj ji jako hotovou jen proto, že lze vytvořit další soubory.

## Dokumentace

| Dokument | Co obsahuje |
|---|---|
| [PLAN](docs/PLAN.md) | Rozsah, technologie, fáze a pravidla dokončení |
| [STATUS](docs/STATUS.md) | Jediné autoritativní místo pro aktuální stav |
| [WORKLOG](docs/WORKLOG.md) | Chronologický záznam provedené práce a ověření |
| [ARCHITECTURE](docs/ARCHITECTURE.md) | Navržené rozdělení kódu, dat a rozhraní |
| [CONTENT-INVENTORY](docs/CONTENT-INVENTORY.md) | Ověřený veřejný soupis A2, umístění archivu a otevřené otázky |
| [MIGRATION](docs/MIGRATION.md) | Náklady, podmínky přechodu, pošta a návrat |
| [ACCESS](docs/ACCESS.md) | Bezpečné lokální přístupy a jejich omezení |
| [IMPROVEMENTS](docs/IMPROVEMENTS.md) | Návrhy mimo doslovný převod obsahu |
| [CLAUDE-HANDOFF](docs/CLAUDE-HANDOFF.md) | Předání redesignu s identitou verze, důkazy a otevřenými podmínkami |
| [B2-REVIEW](docs/B2-REVIEW.md) | Opravené regrese, finální kontroly, srovnávací náhled a výslovné schválení verze |

## Lokální spuštění a kontrola

Použitý Node.js: 24.14.1, npm: 11.11.0. Jediná přímá závislost je vývojový `@11ty/eleventy@3.1.6`, který obsahuje podporu Nunjucks. Přesné verze celého stromu jsou v `package-lock.json`. Instaluj bez lifecycle skriptů:

```text
npm ci --ignore-scripts --no-fund
npm run dev
```

Lokální náhled Eleventy je na `http://localhost:8080/`. Server zastaví Ctrl+C. Pro jednorázovou kontrolu použij `npm run verify`: sestaví pouze veřejné `dist/`, ověří A3 technické vlastnosti, porovná obsah A4 s neměnným veřejným archivem A2 a spustí izolované capture testy A5. Samostatně lze spustit `npm run verify:content` nad již sestaveným webem. Browserovou kontrolu A4 proveď v jednom terminálu přes `python -m http.server 8767 --directory dist`, ve druhém přes `python tests/browser_a4.py`; pak server ukonči. Test používá místní Chrome/Playwright, blokuje původní CDN a nic neodesílá. Statický server PHP formulář neobsluhuje; ten ověří pouze PHP náhled popsaný níže.

Poslední plný `npm audit` z A3 hlásil 9 nálezů ve vývojovém stromu (4 moderate, 5 high), `npm audit --omit=dev` 0. A6 neměnila lockfile ani nezopakovala databázový audit. Závislosti běží jen lokálně při sestavení a nejsou ve veřejném `dist/`. Před pozdějším updatem vyhodnoť nové bezpečné verze; nepoužívej automaticky `npm audit fix --force`.

| Příkaz | Zavést ve fázi | Účel |
|---|---|---|
| `npm run dev` | A3, hotovo | Lokální náhled statické kostry |
| `npm run build` | A3, hotovo | Sestavení veřejných souborů do `dist/` |
| `npm run verify` | A3–A5, hotovo | Sestavení, technický základ, obsah a lokální formulářové testy |
| `npm run verify:content` | A4, hotovo | Nezávislé porovnání zdrojového obsahu a výsledku |
| `npm run test:form` | A5, hotovo | PHP capture testy a Chrome bez JavaScriptu, bez odeslání e-mailů |
| `npm run preview:form` | A5, hotovo | Izolovaný lokální PHP capture náhled, Ctrl+C pro ukončení |
| `npm run verify:browser` | A6 | Build, A3/A4, release a Chrome na 360/390/768/1440 px, s JS i bez JS, 200% text a CSS zoom |
| `npm run release` | A6 | Build, A3/A4 a pouze místní balík public/private, bez přístupů a testovacích zpráv |
| `python tests/browser_b2.py` | B2 | Cílená kontrola hranic formuláře při zvětšení a contain fotografií při hover nad hotovým dist |

PHP ani Composer nejsou globálně v PATH; A5 připravila ověřené lokální PHP 8.3.35 v `.runtime/php83/php.exe` a Composer 2.10.3 v `.runtime/composer.phar`. PHPMailer 7.1.0 je uzamčený v `server/composer.lock`. Obnovení vendor, bezpečná konfigurace a přesné příkazy jsou v [FORM](docs/FORM.md).

Pro formulář spusť z kořene projektu `npm run test:form`, pro ruční syntetický náhled `npm run preview:form`. Náhled vypíše vlastní loopback URL s volným portem; Ctrl+C jej ukončí a uklidí fixture. Oba používají stejný strom public/private jako release a výhradně capture transport mimo veřejný adresář; PHP síťové poštovní funkce jsou zakázané. Místní router emuluje ErrorDocument 404; C1 připravila rozhodovací test a podporu Apache/.htaccess na skutečném cílovém hostingu ověří C2. Eleventy `npm run dev` PHP nespouští. Nezadávej osobní údaje do testovacího capture. Skutečné SMTP přístupy patří výhradně do private/config.php vedle DocumentRoot, vzor server/config.example.php je nefunkční. Produkční SMTP a skutečné doručení neověřené. Konkrétní návrh informace o údajích se správcem je připravený v IMPROVEMENTS; jeho přijetí a skutečné poskytovatelské podmínky se ověří před publikací.

Release builder odmítne přepsat neoznačený balík nebo balík se skutečným private/config.php. Kompletní seznam souborů, bajtů a SHA-256 zapisuje do artifacts/a6/release-manifest.json; identity zdrojů, evidence, dist a vendor do artifacts/a6/version.json. Autoritativní kopie schválené B2 jsou v artifacts/b2 spolu s readback-results.json. Na hosting později patří jen release/public a release/private podle ARCHITECTURE, žádný artifact ani značka .generated-a6. Zde uvedené příkazy nic nenahrávají. Náhled používej pouze na loopback; produkční robots je připravený pro indexování a místní náhled se nesmí bez ochrany zveřejnit.

Archivační a kontrolní příkazy A2 jsou uložené v `scripts/` a zdokumentované ve WORKLOG.
