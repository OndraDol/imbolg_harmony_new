# Aktuální stav

Poslední aktualizace: 2026-10-07, zahájení založení soukromého GitHub repozitáře. Tento soubor je autoritativní pro stav; plán a zadání fází samy nejsou důkazem realizace.

## Rozsah aktuální relace

GitHub repozitář: IN_PROGRESS. Uživatel objednal soukromý `OndraDol/imbolg_harmony_new` včetně commitu a prvního push současného projektu a schválil realizaci navrženého plánu. Čerstvá kontrola potvrzuje místní větev `main`, existující necommitované změny, nepřítomnost remote a přihlášený GitHub CLI účet `OndraDol`; cílový repozitář vrací HTTP 404. Zatím nebyl založen ani nahrán. Přístupy, archiv, artefakty, závislosti a generované balíky zůstávají vyloučené podle `.gitignore`. B1 ani nasazení nejsou součástí tohoto zadání.

## Dokončená A6

Uživatel výslovně objednal pouze A6. Dokončená kontrola veřejného obsahu, metadat, odkazů, galerií, formuláře, čtyř šířek a 200% zvětšení, klávesnice a no-JS. Opravené zalamování, galerijní focus a nestabilní plynulé posouvání; obsah ani média se nemění. Lokální release a CLAUDE-HANDOFF mají konkrétní důkazy. Dosavadní necommitovaná práce je zachovaná. Žádný skutečný e-mail, změna externího systému, nové vlákno ani nasazení. B1 nezačala.

| Fáze | Stav | Důkaz / omezení |
|---|---|---|
| A1 Inicializace a plán | DONE | 21 dokumentů, 10 fází; odkazy a konzistence ověřené, dvě připomínky opravené; DPAPI a Git ignorování ověřené |
| A2 Soupis a archiv | DONE | Veřejný základ: `archive/2026-10-06T13-40-23Z/`, `evidence/pages.json`, `media.json`, `exclusions.json`; 10/10 URL, 26/26 položek galerií, 47 logických médií, 83 výskytů, 179 odkazů; `scripts/verify_a2.py` 0 chyb. Administrace není ověřená a není součástí zálohy účtu. |
| A3 Technický základ | DONE | `npm ci --ignore-scripts` a `npm run verify` prošly; 10 HTML + CSS v čistém `dist/`; `npm run dev` HTTP 200; headless Chrome 40 průchodů 10 cestami na 360/390/768/1440 px bez JS, funkční klávesnicové menu a skip link. Plný audit: 9 vývojových nálezů, produkční strom 0. Doplňkový test 200% textu nedokončen. |
| A4 Přenos obsahu | DONE | `evidence/source-map.json` mapuje 10 URL, 78 textových uzlů, 46 bloků, 47 médií, 83 výskytů, 26 galerijních položek a 179 odkazů. `npm run verify`: 0 chyb; mutační test odhalil vynechanou položku; Chrome: 20 průchodů, 114 načtených obrazových výskytů, 52 otevřených plných galerijních souborů a 0 požadavků na původní CDN. Neověřená práva a účet jsou oddělená omezení. |
| A5 Formulář | DONE | PHP 8.3.35, Composer 2.10.3 a PHPMailer 7.1.0; npm run verify skončil 0, obsah beze změn a 10 skupin A5 testů prošlo, včetně MIME capture, validation/XSS/CRLF/arrays/limitů, souběžného rate limitu, private HTTP 404, 503 a no-JS opravy chyby v Chrome. artifacts/a5/results.json a no-js snímky; PHP lint 5 souborů OK. Žádné skutečné e-maily, produkční SMTP a skutečné doručení neověřené. |
| A6 Kontrola a předání | DONE | A3/A4 bez rozdílu; konečná A5 regrese 10 skupin PASS. Browser 8/8 skupin, 160 režimů, 16 formulářových scénářů, 456 obrazových výskytů, 208 plných galerijních souborů, 266 interních odkazových výskytů, 0 nečekaných console/page/network chyb. Osobně posouzené snímky všech 10 stránek na 360/390/768/1440 a detaily zvětšení/formuláře/menu/404. Release 239 souborů / 50 406 788 B, manifest a verze v artifacts/a6; vyplněný CLAUDE-HANDOFF. Připraveno pro redesign, ne pro publikaci. |
| B1 Claude redesign | TODO | Vyhrazeno Claude Opus po A6 |
| B2 Regresní kontrola | TODO | Závisí na B1 |
| C1 Příprava migrace | TODO | Známé veřejné ceny; chybí ověření účtů a pošty |
| C2 Přepnutí | TODO | Vyžaduje nové explicitní oprávnění |

## Důležité neověřené skutečnosti

1. Přihlášení Webnode: předchozí pokus skončil obecnou chybou formuláře. Pokus A2 přes oficiální Webnode formulář stránku účtu ani projekt neotevřel; po něm zůstala veřejná stránka s nabídkou Login. Správnost hesla není vyvrácená. Neopakovat automaticky stejné pokusy.
2. Administrace: neznáme skryté stránky, koncepty, knihovnu, adresáta starého formuláře, aktivní balíček, expirace a přesnou cenu domény pro tento účet.
3. Pošta: uživatel potvrdil existenci používané doménové schránky, ale přesná adresa, objem, aliasy a historie nebyly ověřené. Veřejný MX ukazuje na Webnode.
4. Obsah: všech 10 URL ze sitemap/menu a interních obsahových odkazů je archivovaných, galerie prošly skutečným otevřením 8/8 a 18/18. Z veřejného DOM nevychází žádná chybějící položka. Neodkazované stránky a neveřejný obsah může odhalit jen přístup do administrace; dynamická externí mapa je doložená URL a screenshotem, ne lokální kopií mapové služby.
5. Práva a původ fotografií: existuje obecný kredit Pexels, přiřazení ke konkrétním souborům není ověřené.
6. Praktik: A6 ověřila celý webový balík včetně PHP na 50 406 788 B, pod interním limitem 80 000 000 B. Velikost pošty a hostingové podmínky stále neověřené. Žádný hosting není objednaný.
7. Převod domény: cesta přes CZ.NIC existuje obecně; držitel, kontaktní e-mail, blokace a DNSSEC konkrétní domény čekají na ověření.
8. A3: poslední plný npm audit hlásil 4 moderate a 5 high vývojových nálezů, produkční npm strom 0. Lock se od té doby nezměnil, databázový audit se v A6 neopakoval. Tehdy nedokončený test zvětšení A6 doplnila: všech 10 stránek ve všech čtyřech šířkách při skutečných 200% root fontech a CSS zoom:2 prošlo, body text200 má 32 px. Nejde o ručně nastavený UI zoom ani certifikaci WCAG/čteček.
9. A4: původní veřejné JPEG a SVG jsou převzaté doslovně; obecný Pexels kredit zůstává v patičce. Právo pro nový veřejný web ani přiřazení autora ke každému médiu nejsou doložené, takže místní kopie není souhlas k publikaci. Dynamická mapa Google zůstává externí službou, lokálně je zachovaná jen její URL a starší screenshot.
10. A5/A6: produkční SMTP a skutečné doručení neověřené. Není dodaná ověřená From schránka ani SMTP přístupy; vzor je disabled, testy používají syntetický capture s blokovanými poštovními síťovými funkcemi. Soukromí je pouze návrh v IMPROVEMENTS, před publikací doplnit a schválit údaje v C1. Composer strict validate má upozornění na záměrnou přesnou verzi PHPMailer 7.1.0; schéma je validní a audit při uzamčení balíku nenašel advisory. A6 vytvořila místní release bez config.php/var/přístupů; produkční konfigurace neexistuje.
11. A6: Google Maps je zachovaná externí služba, při testu nahrazená offline odpovědí. Původní Facebook URL je přesná; live fetch skončil Online fetch throttled, dostupnost profilu neověřená. Vlastní 404 je lokálně ověřená emulací ErrorDocument; skutečný Apache/AllowOverride, private HTTP ochranu a directory listing ověřit v C1. Příčina dřívějšího odpojení driveru není prokázaná; všech 8 finálních izolovaných procesů prošlo. Artefakty jsou ignorované Gitem a nezbytné k předání důkazů; samotný HEAD není finální verze.

## Následující krok

Dokončit kontrolu souborů a historie, commit aktuálního projektu, vytvoření soukromého repozitáře, první push a ověření shody GitHub větve `main` s místním HEAD. Každou dávku zapsat do WORKLOG; stav GitHub změnit na DONE až po ověření. Potom skončit.

A6 skončila. Následující plánovaná fáze B1 je redesign v Claude Opus pouze po samostatném zadání, podle CLAUDE-HANDOFF. Žádné nové vlákno ani redesign nebyly spuštěné. C1 později musí ověřit účet/poštu/hosting, změny od A2, práva médií a informaci o údajích; C2 vyžaduje nové explicitní oprávnění a ruční test skutečné pošty uživatelem. Místní capture náhled je npm run preview:form. Git init ani DPAPI uložení neopakovat.

Odkazy na skutečný výsledek A2 a jeho omezení jsou v `docs/CONTENT-INVENTORY.md` a chronologickém `docs/WORKLOG.md`.
