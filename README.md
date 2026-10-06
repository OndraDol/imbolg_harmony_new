# Imbolg Harmony

Příprava úplné náhrady webu https://www.imbolg-harmony.cz/ a pozdějšího levného přesunu z Webnode. Obsah a současné menu zachovat; konečný redesign provede Claude Opus.

## Aktuální rozsah

Tento projekt nyní obsahuje dokumentaci a zadání fází. Web zatím není implementovaný. Poslední instrukce uživatele výslovně omezila tuto relaci na přípravu plánu pro další model a inicializaci A1. Nevyvozuj z existence plánu oprávnění provést všechny jeho fáze.

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

Příklad pro nejbližší fázi:

```text
/goal Načti README.md, AGENTS.md, docs/STATUS.md a docs/phases/A2.md. Proveď pouze fázi A2 podle jejích vstupů, kroků a kritérií. Každý provedený krok zdokumentuj v docs/WORKLOG.md, na konci aktualizuj docs/STATUS.md. Nezačínej A3, neměň zdrojový web ani DNS a nic neposílej.
```

U další fáze nahraď pouze její označení a cestu. Příkaz `/goal` zadává uživatel v Codexu; není to příkaz PowerShellu ani projektový skript. Pokud zadání fáze nebo její závislosti nejsou splněné, nejprve zjisti konkrétní překážku. Neoznačuj ji jako hotovou jen proto, že lze vytvořit další soubory.

## Dokumentace

| Dokument | Co obsahuje |
|---|---|
| [PLAN](docs/PLAN.md) | Rozsah, technologie, fáze a pravidla dokončení |
| [STATUS](docs/STATUS.md) | Jediné autoritativní místo pro aktuální stav |
| [WORKLOG](docs/WORKLOG.md) | Chronologický záznam provedené práce a ověření |
| [ARCHITECTURE](docs/ARCHITECTURE.md) | Navržené rozdělení kódu, dat a rozhraní |
| [CONTENT-INVENTORY](docs/CONTENT-INVENTORY.md) | Počáteční soupis a pravidla důkazu úplnosti |
| [MIGRATION](docs/MIGRATION.md) | Náklady, podmínky přechodu, pošta a návrat |
| [ACCESS](docs/ACCESS.md) | Bezpečné lokální přístupy a jejich omezení |
| [IMPROVEMENTS](docs/IMPROVEMENTS.md) | Návrhy mimo doslovný převod obsahu |
| [CLAUDE-HANDOFF](docs/CLAUDE-HANDOFF.md) | Budoucí předání redesignu; nyní ještě nepřipravené |

## Budoucí spuštění a kontrola

Následující příkazy jsou smluvené rozhraní budoucích fází, **v A1 ještě neexistují**. Není vytvořen `package.json` ani instalované projektové závislosti.

| Příkaz | Zavést ve fázi | Účel |
|---|---|---|
| `npm run dev` | A3 | Lokální náhled statické části |
| `npm run build` | A3 | Sestavení veřejných souborů do `dist/` |
| `npm run verify` | A3, rozšířit A4–A6 | Sestavení a všechny zavedené kontroly |
| `npm run verify:content` | A4 | Nezávislé porovnání zdrojového obsahu a výsledku |
| `npm run test:form` | A5 | PHP formulář bez odeslání e-mailů |
| `npm run verify:browser` | A6 | Kontrola vykreslení a ovládání v prohlížeči |

Přesné skutečně fungující příkazy, verze a postup přípravy prostředí musí implementující fáze zapsat zpět sem. Současné dostupné nástroje: Node.js 24.14.1, Git 2.53.0.windows.2, Python 3.14. PHP ani Composer nebyly nalezeny v PATH. To nevylučuje jejich existenci jinde.
