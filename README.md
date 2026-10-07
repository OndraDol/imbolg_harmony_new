# Imbolg Harmony

Příprava úplné náhrady webu https://www.imbolg-harmony.cz/ a pozdějšího levného přesunu z Webnode. Obsah a současné menu zachovat; konečný redesign provede Claude Opus.

## Aktuální rozsah

Tento projekt obsahuje veřejný zdrojový archiv A2 a lokální kopii deseti původních URL s převzatými texty, fotografiemi, galeriemi a odkazy. A4, lokální formulář A5 a kontrola A6 jsou dokončené. Web je připravený pro objednaný redesign, balík public/private má 50 406 788 B a browser prošel 8/8 skupinami. Předání s identitou a důkazy je v [CLAUDE-HANDOFF](docs/CLAUDE-HANDOFF.md). Produkční SMTP a skutečné doručení neověřené; práva médií, účet a hosting jsou otevřené podmínky před publikací. Žádná další fáze není automaticky autorizovaná. Důkazy a omezení jsou v [STATUS](docs/STATUS.md) a [CONTENT-INVENTORY](docs/CONTENT-INVENTORY.md).

Začni soubory [AGENTS.md](AGENTS.md), [stav](docs/STATUS.md) a [plán](docs/PLAN.md). Podrobné zadání jednotlivých fází je v [docs/phases](docs/phases/). Než začneš, ověř skutečný obsah složky a Git stav.

## Rozhodnutí uživatele

- Obsah bude upravovat uživatel přes AI; administrace není požadovaná.
- Zachovat všech deset položek menu a původní URL.
- Texty převzít beze změn. Návrhy oprav předložit odděleně.
- Kontaktní formulář doručuje na `kralovamarket@seznam.cz`.
- Existující doménovou schránku zachovat. Přesná adresa a velikost nejsou ověřené.
- Preferovat doménu u VEDOS a web i poštu u Gigaserveru Praktik, pokud bude převod bezpečný a bez zbytečných komplikací.
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

PHP ani Composer nejsou globálně v PATH; A5 připravila ověřené lokální PHP 8.3.35 v `.runtime/php83/php.exe` a Composer 2.10.3 v `.runtime/composer.phar`. PHPMailer 7.1.0 je uzamčený v `server/composer.lock`. Obnovení vendor, bezpečná konfigurace a přesné příkazy jsou v [FORM](docs/FORM.md).

Pro formulář spusť z kořene projektu `npm run test:form`, pro ruční syntetický náhled `npm run preview:form`. Náhled vypíše vlastní loopback URL s volným portem; Ctrl+C jej ukončí a uklidí fixture. Oba používají stejný strom public/private jako release a výhradně capture transport mimo veřejný adresář; PHP síťové poštovní funkce jsou zakázané. Místní router emuluje ErrorDocument 404; podporu Apache/.htaccess na cílovém hostingu musí ověřit C1. Eleventy `npm run dev` PHP nespouští. Nezadávej osobní údaje do testovacího capture. Skutečné SMTP přístupy patří výhradně do private/config.php vedle DocumentRoot, vzor server/config.example.php je nefunkční. Produkční SMTP a skutečné doručení neověřené. Návrh informace o údajích čeká na doplnění a schválení v C1.

Release builder odmítne přepsat neoznačený balík nebo balík se skutečným private/config.php. Kompletní seznam souborů, bajtů a SHA-256 je v artifacts/a6/release-manifest.json; identity zdrojů, evidence, dist a vendor v artifacts/a6/version.json. Na hosting později patří jen release/public a release/private podle ARCHITECTURE, žádný artifact ani značka .generated-a6. Zde uvedené příkazy nic nenahrávají. Náhled používej pouze na loopback; produkční robots je připravený pro indexování a místní náhled se nesmí bez ochrany zveřejnit.

Archivační a kontrolní příkazy A2 jsou uložené v `scripts/` a zdokumentované ve WORKLOG.
