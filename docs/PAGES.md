# GitHub Pages

Samostatné zadání 2026-10-07 bylo dokončené: [celý schválený web](https://ondradol.github.io/imbolg_harmony_new/) je veřejný, formulář zatím neaktivní. Zdroj main při prvním zveřejnění cd6695d95eca6ceda5afb70838bac71e6ca2cc9a, veřejný gh-pages commit 65b49c898fe8b3c628a69e721470839ea60d5577. [Workflow 37630497020](https://github.com/OndraDol/imbolg_harmony_new/actions/runs/37630497020) dokončil build i deploy úspěšně; Pages API status built, HTTPS vynucené, CNAME prázdné. Výstup má 148 souborů / 49 903 735 B, identitu 0ad525d0c40d739daeeba32cb463316e812d5529fda0858d5f66057139f634d9. HTTPS kontrola 147 servírovaných souborů i vlastní 404 PASS, všechny stránky vykreslené v Chromu a ověřené mobilní menu/galerie/formulář; živá kontaktní mapa načtená. Důkazy v artifacts/github-pages, historie ve WORKLOG. Původní doména a pošta se nepřepínají, C2 nezačala.

## Připomínky majitelky, 2026-10-07

Zpracované a zveřejněné: celá obdélníková fotografie v záhlaví přibližně 112 × 149 px, odstraněná čára nad zdravotními testy Amy a BZ 5x I. cena. Při zvětšení se název značky zalamuje po celých slovech. Zdrojový commit d83284995268f9ea8bbde2f0233afbb1d316f1b1, veřejný gh-pages d0b8ba65f000caee8cf175f325c5c1562a7fa917, [workflow 37663896105](https://github.com/OndraDol/imbolg_harmony_new/actions/runs/37663896105) success. Aktuální manifest: 148 souborů / 49 903 817 B, identita 70f19ad2a7c331a7ea5d765676d22d0161a7720d2e6c3c4843f3fbdabbfbe5d8. HTTPS readback všech 147 servírovaných souborů a vlastní 404 PASS, skutečné vykreslení všech deseti stránek na 390/1440 px i cílené Feny na čtyřech šířkách PASS. Místní A6 8/8 skupin a cílená Pages kontrola 24/24 režimů PASS. Důkazy v artifacts/feedback-2026-10-07, původní vydání z úvodu zůstává historickým záznamem. Archiv/evidence se nepřepisovaly, formulář je dál neaktivní.

## Obsah a formulář

Výstup obsahuje všech deset původních cest, 404, kompletní veřejná média, CSS, robots a sitemap. Původní obsahové texty, média, popisky, kredity, menu, pořadí galerií a externí odkazy jsou zachované. Kořenové interní URL a srcset získávají prefix /imbolg_harmony_new/. Kanonické adresy zůstávají na původní doméně, kopie má noindex. Apache .htaccess se nepoužívá; .nojekyll umožňuje publikaci hotových statických souborů.

Kontaktní formulář má viditelné upozornění a mailto:kralovamarket@seznam.cz. Všechna pole a tlačítko jsou disabled, tlačítko má type=button a formulář nemá action/method. Nic neodesílá ani nezobrazuje falešné potvrzení. PHP, SMTP, server, konfigurace, přístupy, historie pošty, archiv, dokumentace a soukromé přílohy do této větve nevstupují. Původní PHP šablona a produkční plán zůstávají oddělené; skutečné doručení patří do samostatně autorizovaného zprovoznění formuláře.

## Sestavení a ověření

`npm run verify:pages` vždy nejprve sestaví aktuální Eleventy zdroje a oddělený Pages výstup. Potom provede A3 a A4 kontroly proti původní evidenci a porovnání celého HTML/assetů s dist. A4 od 2026-10-07 přijímá jedinou výslovně autorizovanou obsahovou změnu feny-node-010: BZ 4x → 5x I. cena. Kontroluje celé původní a nové znění uzlu, odpovídající blok i main; archiv/evidence se nepřepisují. Pages porovnání dovoluje pouze uvedené technické změny a doplnění stavu formuláře. Výstup je v artifacts/github-pages/preview/imbolg_harmony_new, manifest a receipty mimo publikovaný strom v artifacts/github-pages. Úklid ověřeného generovaného exportu podporuje i read-only položky na Windows.

`python scripts/prepare_github_pages.py` pouze připraví místní gh-pages commit. Použije oddělený Git index, předem ověří úspěšnou kontrolu i každý veřejný soubor a porovná přesné Git blob hashe se schváleným manifestem. Nezahrnuje hlavní pracovní index. První commit je bez rodiče, další navazuje na místní gh-pages. Neprovádí push, neobjednává služby a nekonfiguruje hosting. Budoucí publikaci provést jen na výslovné zadání; bez force push.

GitHub Pages používá větev gh-pages a její kořen, bez vlastní domény/CNAME. Zdrojová main obsahuje schválenou B2 implementaci, pomocné skripty a dokumentaci. Po publikaci `python scripts/verify_github_pages.py --live` ověří shodné hashe všech veřejně servírovaných souborů přes HTTPS; .nojekyll se dokládá stromem větve. Skutečné vykreslení, mobilní menu a stav formuláře se ověřují také v Chromu.

## Návrat

Při chybném budoucím Pages vydání zachovat předchozí gh-pages commit a z něj vytvořit nový navazující commit s jeho ověřeným stromem. Publikovat běžným push, vyčkat na dokončení a zopakovat veřejný readback. Main, zdrojové doklady a staré release identity se kvůli tomu nepřepisují. Původní Webnode, DNS a pošta nejsou Pages publikací dotčené a zůstávají dostupné podle svých dosavadních služeb.
