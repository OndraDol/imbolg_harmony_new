# Soupis obsahu a zdrojový archiv A2

Stav: veřejný základ A2 po archivaci 2026-10-06 od 13:40:23 UTC. Níže uvedený původní průzkum je doplněný skutečným archivem a strojovou evidencí. Účet Webnode ani neveřejný obsah nejsou ověřené.

## Archiv a rozsah důkazu

Archiv je v `archive/2026-10-06T13-40-23Z/` (ignorovaný Gitem), soupis v `evidence/pages.json`, `evidence/media.json` a `evidence/exclusions.json`. Archiv obsahuje veřejnou sitemap, raw odpověď HTML a vykreslený DOM každé stránky, 20 celostránkových screenshotů při viewportech 1440 × 900 a 390 × 844, snímky obou otevřených galerií, 109 jedinečných rastrových souborů pro 112 pozorovaných URL a dodatek čtyř SVG ikon. `capture.json` zachovává původní pořadí i úplné URL; `gallery-browser-check.json` dokládá průchod galeriemi; `supplement-embeds.json` dokládá ikony a externí mapu. Celý archiv má 95 029 701 bajtů v 160 souborech; rastrová média zaujímají 56 259 635 bajtů a SVG 8 345 bajtů. Ze 43 rastrových zdrojových položek pochází 42 obsahově různých největších dostupných veřejných JPEG souborů o 30 315 841 bajtech. Jsou to veřejné plné varianty Webnode, ne ověřené originály přímo z fotoaparátu.

| Cesta | Textové kontejnery | Neprázdné textové uzly | Výskyty `img` | Položky galerie | Výskyty odkazů `a[href]` |
|---|---:|---:|---:|---:|---:|
| `/` | 10 | 20 | 15 | 8 | 26 |
| `/o-nas/` | 3 | 7 | 3 | 0 | 15 |
| `/sluzby/` | 6 | 6 | 3 | 0 | 15 |
| `/nase-prace/` | 2 | 2 | 1 | 0 | 15 |
| `/fotogalerie/` | 4 | 4 | 22 | 18 | 33 |
| `/cenik/` | 9 | 10 | 1 | 0 | 15 |
| `/kontakt/` | 5 | 8 | 1 | 0 | 15 |
| `/vrh-a/` | 1 | 2 | 2 | 0 | 15 |
| `/feny/` | 4 | 16 | 3 | 0 | 15 |
| `/psi/` | 2 | 3 | 2 | 0 | 15 |
| **Celkem** | **46** | **78** | **53** | **26** | **179** |

Z 47 evidovaných logických médií je 43 rastrových zdrojových URL a čtyři SVG ikony kontaktu. Dohromady mají 83 výskytů: 53 v `img`, 26 v galeriích a čtyři `embed`; opakované logo se nepovažuje za ztrátu ani za nový soubor. K 78 obsahovým textovým uzlům v `main` je evidováno dalších 230 neprázdných uzlů z hlavičky, patičky a ostatních částí každé stránky včetně opakování, kreditu a technického cookie textu. Původ a práva jsou u každé mediální položky označené jako otevřené. Obecný kredit Pexels v patičce zůstává zachovaný, nelze jej bez důkazu přiřadit ke všem snímkům.

Veřejná sitemap, všech deset položek menu a interní odkazy se shodují na stejných deseti obsahových cestách. Existuje 179 výskytů klasických odkazů `a[href]` a 48 odlišných úplných cílů včetně fragmentů a 26 mediálních odkazů galerie. Navíc je samostatně evidovaný jeden externí iframe Google Maps na `/kontakt/` a čtyři URL SVG ikon. Mezi veřejnými odkazy se neobjevila samostatná PDF, DOC, ZIP, video ani audio příloha. Raw DOM mapu a její URL zachovává, screenshot kontaktu dokládá vykreslení; obsah externí dynamické mapové služby není lokální záloha.

`scripts/verify_a2.py` ověřil shodu sitemap, URL, pořadí galerie v DOM, všech obsahových i mimohlavních textových uzlů, pořadí odkazů, počty obrázků, hashe HTML/DOM a všech uložených médií, čitelnost souborů a screenshotů, SVG XML i odkazy na mapu: **0 chyb**. `scripts/check_galleries_a2.py` navíc prošel skutečný browserový overlay v pořadí 8/8 na úvodu a 18/18 na Fotogalerii; všech 26 obrazů se načetlo. Seznam chybějícího obsahu v takto vymezeném veřejném základu je prázdný. Neodkazovanou stránku mimo sitemap/menu/crawl nelze vyloučit bez přístupu do administrace. Přihlášení účet neotevřelo; neveřejné koncepty, knihovna a úplnost účtu zůstávají pro C1 neověřené.

U všech 43 veřejných párů plného JPEG/WebP se shodovaly rozměry a poměr stran. Zmenšené pixelové porovnání v `scripts/compare_variants_a2.py` mělo nejvyšší průměrný rozdíl 0,93 z 255, bez případu nad mezí 15; žádný odlišný ořez se tímto testem neukázal. Původ fotografie ani její licence z této podobnosti neplynou.

## Opakovatelné příkazy

Skripty použily existující lokální Python knihovny Playwright, Pillow a BeautifulSoup. Browserové příkazy potřebují čerstvé CDP URL vlastní relace `agent-browser`; starý port může přestat fungovat. Nový průchod vytvoří nový časový adresář a nepřepíše zde uvedený snímek.

```text
agent-browser session id --scope worktree --prefix imbolg-a2
agent-browser --session <vlastní-relace> open https://www.imbolg-harmony.cz/
agent-browser --session <vlastní-relace> get cdp-url
python scripts/archive_public_a2.py --cdp <čerstvé-CDP-URL>
python scripts/archive_embeds_a2.py --cdp <čerstvé-CDP-URL> --snapshot archive/<nový-snímek>
python scripts/build_a2_evidence.py archive/<nový-snímek>
python scripts/check_galleries_a2.py --cdp <čerstvé-CDP-URL> --snapshot archive/<nový-snímek>
python scripts/verify_a2.py archive/<nový-snímek>
python scripts/compare_variants_a2.py archive/<nový-snímek>
```

Všechny uvedené typy kroků byly v A2 skutečně provedené pro `archive/2026-10-06T13-40-23Z/`; obnovovat evidenci z jiného snímku jen s vědomým doložením změny zdroje. Skript přihlášení `check_webnode_login_a2.py` je samostatný jednorázový diagnostický pokus; bez změněné situace jej neopakovat.

Při A4 použít `pages.json` jako zdrojovou mapu bloků, uzlů, odkazů, formuláře, galerií a mediálních výskytů; neposuzovat úplnost podle pouhého počtu souborů. Otevřenou provenienci médií vyřešit před veřejným použitím. Před přepnutím webu ověřit změny veřejného zdroje od tohoto snímku.

## Původní předběžný průzkum před A2

| Pořadí | Menu | Cesta | Pozorovaný obsah / riziko |
|---:|---|---|---|
| 1 | Úvod | `/` | Název, logo-fotografie, citát, Péče o beagle, Beagle Chov & Výcvik, Krásy beagle chovu, fotografie, formulář a Facebook |
| 2 | O nás | `/o-nas/` | Citát, historie se Samem a Amy, filozofie chovu, fotografie |
| 3 | Služby | `/sluzby/` | Tři bloky Výcvik pro beagly, Péče o plemeno, Poradenství pro nové majitele; možné nesoulady nadpisů a popisů jen evidovat |
| 4 | Naše práce | `/nase-prace/` | Chov, péče, výstavy a zkoušky |
| 5 | Fotogalerie | `/fotogalerie/` | Úvod, Amy od štěněte, ANIMA vrh; nutná kontrola načtených a rozbalených galerií |
| 6 | Ceník | `/cenik/` | Individuální cena štěňat, lekce, výstavní příprava a péče; nevymýšlet částky |
| 7 | Kontakt | `/kontakt/` | Jméno, adresa, telefon, e-mail, Facebook; ověřit zalomení adresy |
| 8 | Vrh A | `/vrh-a/` | Vrh A... ANIMA a obrazový obsah; krátký text neznamená prázdnou stránku |
| 9 | Feny | `/feny/` | Imbolg Cernunnos Mawr (Amy), Anima Roxana Imbolg Harmony, data, výsledky a genetické údaje |
| 10 | Psi | `/psi/` | Anima Leo Imbolg Harmony, datum, genetické údaje a fotografie |

Sitemap.xml obsahovala těchto deset cest. Aktuální A2 potvrdila shodu se seznamem veřejně odkazovaných obsahových cest; další neodkazované stránky může ukázat teprve administrace.

## Pozorované kontakty

Markéta Kunešová, telefon +420 775 935 130, e-mail kralovamarket@seznam.cz. Adresa se v textovém výpisu sloučila na „Myslbekova 559407 21 Česká Kamenice“; před převzetím ověřit DOM a skutečné zalomení, nevymýšlet opravu.

Facebook: https://www.facebook.com/profile.php?id=61571597523226 . Zachovat přesný cíl.

Formulář na úvodu má Jméno a příjmení, E-mail, Zpráva, Odeslat. DOM ukazoval required jen u jména a e-mailu. Formulář nebyl odeslán. Seznam je uživatelem zvolený nový příjemce, příjemce původního formuláře není ověřený.

## Média a technické části

Pozorovaná CDN: `454501af52.clvaw-cdnwnd.com`. Různé velikosti a WebP/JPEG varianty nejsou automaticky různé fotografie. Galerie mohou používat JavaScript, datové atributy a CSS pozadí. Soupis nesmí vzniknout jen počítáním img tagů nebo textových značek Image.

Patička obsahuje obecný kredit Pexels. Autorství a oprávnění každého souboru nejsou doložené; nepřisuzovat automaticky všechny fotografie majitelce. Nejasnosti vést jednotlivě.

Byl pozorovaný GTM iframe a cookie dialog. Tyto technické prvky se nepřebírají automaticky a patří do evidence výluk. Kredit a skutečnou informaci o soukromí neodstraňovat spolu s technickou patičkou.

## Navazující kontrola A4

A4 doplnila `evidence/source-map.json`: všech deset URL, 78 textových uzlů, 46 editorových bloků, 47 logických médií, 83 výskytů, 26 položek galerií a všech 179 zdrojových odkazů má jednotlivé mapování. Z nich 149 vede na cílový obsah a 30 technických ovládacích odkazů Webnode (`#`: zavření/menu/cookie ovládání) je označených jako výluka. Původní pořadí a opakované položky zůstaly zachované. Text a struktura jsou v `src/content/pages.json`, technické alty v `src/content/media-alt.json`, 43 plných JPEG a jejich dvě WebP varianty spolu se čtyřmi SVG v `src/assets/images/`. Plné JPEG a SVG jsou bytově stejné jako veřejný archiv; varianty jsou běžné zmenšení a komprese. Formulářová slova na úvodu jsou viditelná, přenosové chování patří A5.

`npm run verify` porovnalo skutečný build s nezměněnou evidencí A2: jednotlivé ID, přesný text po povolené normalizaci mezer, pořadí bloků, médií a galerií, cíle odkazů, hashe plných obrazů, SVG a vloženou URL mapy. Výsledek: 0 chyb. `tests/mutation_a4.py` na dočasné kopii odstranil značku `home-node-001` a kontrola chybu výslovně ohlásila; testovací kopie byla odstraněna. Headless Google Chrome otevřel deset stránek při 390 a 1440 px, načetl 114 obrazových výskytů (dvě šířky) a ověřil otevření 52 plných galerijních souborů. Při zablokované původní CDN nevznikl žádný požadavek na ni. Vizuálně prošly screenshoty všech deseti stránek, kontaktní ikony a přehled všech 43 fotografií; plné soubory s textem diplomů zůstaly čitelné. Veřejný `dist/` má 49 867 098 bajtů a neobsahuje JSON evidenci, archiv ani soukromé soubory.

„Obsah převzat“ zde znamená přesně vymezený veřejný základ A2. Neodkazované a neveřejné stránky účtu nebylo možné potvrdit bez administrace. Původ a oprávnění všech jednotlivých fotografií a ikon zůstávají otevřené; obecný původní kredit Pexels je zachovaný, ale není přiřazen jednotlivým souborům. Místní import nedává souhlas k veřejnému použití. Google Maps je externí dynamický iframe, jeho URL a archivní screenshot se zachovaly, samotná mapa není lokální kopie. Na původním webu nebylo nic změněno a nic nebylo nasazeno.

## Navazující konečná kontrola A6

A6 zachovala nezávislý A2 základ i source-map. Poslední A3/A4 kontrola nad finálním dist má stejné počty 10 URL / 78 uzlů / 46 bloků / 47 médií / 83 zdrojových výskytů / 26 galerijních položek / 179 původních odkazů a 0 chyb. Metadata description/canonical se doplnila doslovně z evidence, stejně jako původní titulky. Nové jsou jen technické sitemap, robots, 404 a serverová mapa; do autorského obsahu se nezasahovalo. Plné JPEG/SVG jsou bytově shodné s archivem. Původní A4 neaktivní formulář byl v A5 nahrazen aktivním se zachovanými popisky a povinnými poli, nyní má 10 skupin A5 a 16 A6 capture scénářů PASS.

Browser A6: Chrome 154.0.8037.98, osm samostatných procesů 360/390/768/1440 × JS on/off, souhrnný PASS v artifacts/a6/browser-results.json. 160 stránkových režimů včetně 200% textu a CSS zoom:2, 456 načtených obrazových výskytů a 208 otevření plných galerijních souborů, 266 interních odkazových výskytů (včetně obou navigací a technických kontaktů), žádné nečekané runtime/console/local-network chyby. Všech 10 stránek na každé šířce prošlo i osobním posouzením přehledů skutečných plných snímků; navíc detaily zvětšení, formuláře, otevřeného menu a 404. Galerie má správný focus box, dlouhé URL/název se zalamují a focus/click nečeká na plynulé posouvání. Snímky a kontrolní výsledky jsou v artifacts/a6, konkrétní vzory a omezení v CLAUDE-HANDOFF.

Celý místní nasazovací balík public/private má 239 souborů a 50 406 788 B, tedy méně než 80 000 000 B. Manifest všech souborů/velikostí/hashů je artifacts/a6/release-manifest.json, package SHA-256 719e6da0f1ceb81a1c7b2547f719f6da51132bd543b469c8c9692fb8fa415ea9. Identita zdrojů, skutečného dist, produkčního vendor a evidencí je 5f0a89085b9cc41e7062537f8164a369a191861b929f259771449475927e1fec v artifacts/a6/version.json. Balík obsahuje endpoint a soukromý runtime/vzor, žádnou produkční konfiguraci, capture, archiv, docs nebo Node závislosti.

Účet Webnode, jednotlivá práva médií, skutečné SMTP/doručení a schránky stále nejsou ověřené. Live Facebook fetch byl omezen nástrojem; přesný původní cíl je ověřený, dostupnost profilu není PASS. Google Maps zůstává původní externí volitelný iframe; core prošel při offline odpovědi mapy a bez CDN/tracking požadavků. 404 je skutečně viditelná na neznámé lokální URL se stavem404 přes testovou emulaci; Apache/AllowOverride cílového hostingu je C1 brána. A6 je DONE pro místní funkční základ a předání redesignu, ne pro publikaci či zrušení Webnode.
