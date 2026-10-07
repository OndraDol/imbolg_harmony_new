# GitHub Pages

Samostatné zadání 2026-10-07 povoluje publikaci celého schváleného webu na https://ondradol.github.io/imbolg_harmony_new/ s formulářem zatím neaktivním. Aktuální stav a důkaz publikace jsou v STATUS/WORKLOG. Tento výstup nepřepíná původní doménu u Webnode a není doménová migrace C2.

## Obsah a formulář

Výstup obsahuje všech deset původních cest, 404, kompletní veřejná média, CSS, robots a sitemap. Původní obsahové texty, média, popisky, kredity, menu, pořadí galerií a externí odkazy jsou zachované. Kořenové interní URL a srcset získávají prefix /imbolg_harmony_new/. Kanonické adresy zůstávají na původní doméně, kopie má noindex. Apache .htaccess se nepoužívá; .nojekyll umožňuje publikaci hotových statických souborů.

Kontaktní formulář má viditelné upozornění a mailto:kralovamarket@seznam.cz. Všechna pole a tlačítko jsou disabled, tlačítko má type=button a formulář nemá action/method. Nic neodesílá ani nezobrazuje falešné potvrzení. PHP, SMTP, server, konfigurace, přístupy, historie pošty, archiv, dokumentace a soukromé přílohy do této větve nevstupují. Původní PHP šablona a produkční plán zůstávají oddělené; skutečné doručení patří do samostatně autorizovaného zprovoznění formuláře.

## Sestavení a ověření

`npm run verify:pages` vždy nejprve sestaví aktuální Eleventy zdroje a oddělený Pages výstup. Potom provede nezměněné A3/A4 kontroly proti původní evidenci a nové porovnání celého HTML/assetů s dist. Nová kontrola dovoluje pouze uvedené technické změny a doplnění stavu formuláře; původní kontrolní základ se nemění. Výstup je v artifacts/github-pages/preview/imbolg_harmony_new, manifest a receipty mimo publikovaný strom v artifacts/github-pages.

`python scripts/prepare_github_pages.py` pouze připraví místní gh-pages commit. Použije oddělený Git index, předem ověří úspěšnou kontrolu i každý veřejný soubor a porovná přesné Git blob hashe se schváleným manifestem. Nezahrnuje hlavní pracovní index. První commit je bez rodiče, další navazuje na místní gh-pages. Neprovádí push, neobjednává služby a nekonfiguruje hosting. Budoucí publikaci provést jen na výslovné zadání; bez force push.

GitHub Pages používá větev gh-pages a její kořen, bez vlastní domény/CNAME. Zdrojová main obsahuje schválenou B2 implementaci, pomocné skripty a dokumentaci. Po publikaci `python scripts/verify_github_pages.py --live` ověří shodné hashe všech veřejně servírovaných souborů přes HTTPS; .nojekyll se dokládá stromem větve. Skutečné vykreslení, mobilní menu a stav formuláře se ověřují také v Chromu.

## Návrat

Při chybném budoucím Pages vydání zachovat předchozí gh-pages commit a z něj vytvořit nový navazující commit s jeho ověřeným stromem. Publikovat běžným push, vyčkat na dokončení a zopakovat veřejný readback. Main, zdrojové doklady a staré release identity se kvůli tomu nepřepisují. Původní Webnode, DNS a pošta nejsou Pages publikací dotčené a zůstávají dostupné podle svých dosavadních služeb.
