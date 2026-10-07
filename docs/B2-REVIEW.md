# B2: regresní kontrola a schválení

Datum: 2026-10-07. Stav: DONE. Technické ověření je dokončené a majitelka schválila konkrétní verzi prostřednictvím uživatele zprávou „Je to schváleno.“ C1 ani C2 nezačaly, nic není nasazené.

Předchozí odstavec zaznamenává okamžik uzávěrky B2. Následný průzkum C1, odeslaný dotaz Webnode a dokumentační commit/push jsou v [STATUS](STATUS.md) a [WORKLOG](WORKLOG.md); nyní C1 BLOCKED čeká na poskytovatelskou odpověď a C2 zůstává TODO. Tento dokument je schválení konkrétní místní B2, nikde netvrdí její nasazení nebo commit implementace.

## Konkrétní verze

Redesign je dodaná varianta 1B Fotka s opravami B1 a dvěma níže uvedenými opravami B2. Identita finálních zdrojů, evidence, dist a vendor: `ef7790446ba6470d3cee43694c399722296831a98176af803efc7a08e6fdb820`. Označení schváleného náhledu: `B2-2026-10-07-ef779044`.

Ověřený původní základ A6 má identitu `5f0a89085b9cc41e7062537f8164a369a191861b929f259771449475927e1fec`, předaná B1 `57dd03c08304df612f112ccc11209eac7660fd35032eca498c53bca71e45f17e`. Git HEAD samotný tyto místní necommitované verze neidentifikuje.

## Porovnání a opravy

Přepočet proti A6 potvrdil, že B1 změnila pouze CSS, atribut `data-page` společné šablony a odpovídající sestavené výstupy. Nezávislý základ A2, texty, pořadí menu a galerií, všechny soubory fotografií, URL, metadata, kontakty, příjemce, SMTP rozhraní a serverová validace jsou zachované. Technické výluky Webnode zůstávají stejné. Důkaz: `artifacts/b2/preflight.json` a `a6-to-b1.diff`.

| Regrese | Důkaz | Oprava |
|---|---|---|
| Formulář při 200% textu na 360 px přesahoval kartu | Pravý okraj polí 329,375 px proti vnitřnímu limitu 280 px; A6 měla všechna pole uvnitř. `form-layout-diagnosis.json` a snímky A6/B1/kandidáta. | Sloupec `minmax(0,1fr)`, omezení šířky tlačítka a jeho responzivní vodorovný padding. Pole po opravě končí přesně na 280 px. |
| Hover na diplomech úvodní galerie přebíjel zákaz ořezu | `check_preview.py` zaznamenal na media-006 `matrix(1.04,0,0,1.04,0,0)` místo `none`. Starší B1 kontrola zkoušela pouze contain fotografie na stránce Fotogalerie. | `:where()` snižuje specificitu stejného homepage selektoru; contain výjimky nyní platí i při hover. |

Vlastní zásah B2 do webu jsou tři řádky `src/assets/css/site.css`. Přidaný `tests/browser_b2.py` kontroluje obě nalezené vady skutečným Chromem; žádný původní test ani baseline nebyl oslabený. Obsahové návrhy v IMPROVEMENTS se neprováděly.

## Ověření

| Oblast | Výsledek a důkaz |
|---|---|
| Nezávislý obsah | PASS, 0 rozdílů: 10 URL, 78 textových uzlů, 46 bloků, 47 médií, 83 výskytů, 26 galerijních položek, 179 původních odkazů. `release-final.log`. |
| Formulářová logika | PASS, všech 10 skupin A5 nad opraveným dist. `form-final.log`. Pouze capture, žádná skutečná pošta. |
| Obě B2 regrese | PASS, 48 stavů formuláře ve 24 kombinacích šířky/JS/zvětšení, 40 contain hover kontrol. `regressions.json`. |
| Úplný browser finální verze | PASS, 8/8 skupin: 160 stránkových režimů, 16 formulářových scénářů, 456 načtených obrazových výskytů, 208 otevření plné galerie, 266 interních odkazových výskytů, 0 nečekaných console/page/network chyb. `browser-final.log`, `browser-results.json` a osm dílčích JSON. |
| Vizuální posouzení | PASS, 120 režimů viditelnosti textu, 228 obrazových boxů a 40 čerstvých čistých stránek. Osobně všechny stránky včetně konců a všechny ořezy na 360/390/768/1440 px, po opravě dotčený formulář při 200% textu/zoom a hover diplomů; čerstvý úvod 390/1440. `visual-results.json` a snímky. |
| Public/private release | PASS, 239 souborů, 50 430 699 B, limit 80 000 000 B splněný. Package SHA-256 `eaa15904b8bc65dc169069dffa13d7a6a7661aedacd1e639cb0678145042527e`. `readback-results.json` propojuje skutečné soubory, testy, snímky a přenositelný náhled se stejnou finální identitou. |

## Náhled a schválení majitelkou

Hotový [srovnávací náhled](../artifacts/b2/nahled/index.html) a [přenositelný ZIP](../artifacts/b2/B2-2026-10-07-ef779044-nahled.zip) obsahují všech deset stránek A6 i B2 ve čtyřech šířkách, celkem 80 snímků. ZIP lze rozbalit a otevřít `index.html` bez připojení k internetu; složka `snimky` musí zůstat vedle něj. Browser ověřil všech 40 dvojic, jejich no-JS zobrazení a mobilní náhled bez přesahu. Webové menu a formulář uvnitř snímků nejsou interaktivní. Pracovní ZIP s identitou 57dd03c0 vznikl před opravami a není schválenou verzí.

Srovnávací A6 snímky pocházejí z dočasně obnoveného veřejného stromu, jehož všech 148 souborů bylo před snímáním ověřeno proti původním A6 hashům. Nejde o rekonstrukci baseline z nového webu. Snímky jsou včetně všech dekódovaných fotografií a konců stránek. Mapová služba je během snímání vypnutá, což náhled výslovně uvádí.

| Záznam souhlasu | Stav |
|---|---|
| Schválená verze | `B2-2026-10-07-ef779044` |
| Souhlas majitelky zprostředkovaný uživatelem | Výslovná zpráva uživatele v této relaci po uvedení finální verze náhledu |
| Datum a přesné znění souhlasu | 2026-10-07: „Je to schváleno.“ |
| Stav celé B2 | DONE, technické důkazy i konkrétní souhlas jsou zaznamenané |

Souhlas je zaznamenaný také v `artifacts/b2/approval.json` a WORKLOG. Po souhlasu se mění jen dokumentační informace o schválení v náhledu, jeho 80 snímků a identita webu zůstávají stejné. Schválení vzhledu neopravňuje k nasazení ani automatickému zahájení C1. B2 zde končí.

## Omezení

Ověření se týká místního Chromu, PHP capture a zachovaného veřejného základu A2. Živá Google Maps, dostupnost Facebook profilu, skutečné SMTP/doručení, hostingové chování, neveřejný obsah Webnode a práva jednotlivých médií se tím neprokazují. Původní obecný kredit Pexels je zachovaný. Neproběhlo nasazení, změna DNS, skutečný e-mail, commit ani push. Artefakty jsou mimo veřejný build a ignorované Gitem; pro zachování důkazů je potřeba tento místní workspace.

## Reprodukce

Z ověřeného kořene projektu: `npm run verify:browser` pro standardní úplnou suite, `python tests/browser_b2.py` pro obě regrese, `python tests/test_form_a5.py` pro capture scénáře. Závěrečný běh používá stejné nezměněné skupiny A6 po dvou izolovaných procesech přes `artifacts/b2/run_browser_final.py`. `artifacts/b2/readback.py` následně propojí identity, manifest, snímky, výsledky a náhled. Všechny uvedené kroky jsou místní.
