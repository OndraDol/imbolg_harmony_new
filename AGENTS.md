# Práce v projektu Imbolg Harmony

## Začni zde

Přečti `README.md`, `docs/STATUS.md`, `docs/PLAN.md` a zadání aktuálně objednané fáze v `docs/phases/`. Pro kód načti i `docs/ARCHITECTURE.md`. Při novém zahájení práce ověř absolutní pracovní adresář a Git stav. Projekt: `C:\Users\ondrej.dolejs\Desktop\Projekty\imbolg_harmony`.

Uživatel primárně objednal podrobný plán pro další model. A1 byla inicializace dokumentace. Žádná další fáze není automaticky autorizovaná jen tím, že je zde popsaná. Proveď fázi výslovně zadanou uživatelem a na jejím konci skonči; nepřecházej samovolně na další.

## Povinná dokumentace každého kroku

Každý provedený pracovní krok musí mít záznam v `docs/WORKLOG.md`: datum a fáze, co a proč se provedlo, dotčené soubory nebo systém, výsledek, konkrétní důkaz, případná překážka a následující krok. Dokumentuj i neúspěšné pokusy, přístupová omezení a rozhodnutí. Související čtení nebo dávku kontrol lze zapsat společně, nesmí se tím ztratit podstatný krok.

Záznam proveď bezprostředně po kroku nebo dávce, ne až při odevzdání celé fáze. Hesla, cookies, tokeny, soukromé zprávy a osobní obsah pošty nikdy nevkládej do záznamu. Neoznačuj plánované kroky jako provedené.

Při začátku, dokončení i přerušení aktualizuj `docs/STATUS.md`. Používej `TODO`, `IN_PROGRESS`, `BLOCKED`, `DONE`. `DONE` vyžaduje splnění všech kritérií fáze a uvedení důkazu. Při přerušení popiš přesný bod pokračování, ne pouze „pokračovat v práci“.

## Obsah a autorská ochrana

Zachovej všechny texty, média, popisky, odkazy, autorské emoji, pořadí položek galerií a členění menu. Původní opakování není chyba k automatickému odstranění. Neměň odborné údaje, výsledky, data, kontakty ani tvrzení o zdraví psů.

Návrhy obsahových změn patří do `docs/IMPROVEMENTS.md`. Jejich provedení vyžaduje samostatné zadání; migrace a redesign je samy nepovolují. Odchylky od zdrojového základu eviduj jednotlivě a dolož autorizaci.

Úplnost musí být doložená mapou zdroj → cíl a skutečným vykreslením. Kontrolní základ se nesmí generovat z nového webu ani přepsat jen proto, aby kontrola prošla. Samotný počet obrázků nebo zelený build úplnost nedokazuje. Částečné výsledky označ jako částečné.

Neznámý původ obrázku není důvod vymyslet kredit. Zachovej doložené kredity a veď otevřené otázky k právům. Nezaváděj nové AI obrázky. Při práci s médii načti uživatelský runbook `C:/Users/ondrej.dolejs/.codex/runbooks/editorial-media-quality.md`.

## Technologie a změny

Drž Eleventy + Nunjucks, běžné CSS a minimum JavaScriptu. PHP 8.3 + PHPMailer slouží pouze formuláři. Bez samostatného rozhodnutí nezaváděj React, WordPress, databázi, placené SaaS ani serverový Node provoz.

Obsah musí být oddělený od šablon a vzhledu. Zachovej původní URL s koncovými lomítky. Veřejný build obsahuje jen veřejné soubory; archiv, dokumentace, Git, přístupy, SMTP konfigurace a historie pošty do něj nesmí vstoupit.

Záměrné textové úpravy prováděj přes `apply_patch`. Před novými Node závislostmi načti `C:/Users/ondrej.dolejs/.codex/runbooks/node-dependency-safety.md`, ověř původ/verzi, použij lockfile a neprováděj neprověřené instalační skripty. Respektuj zavedené npm příkazy; nepřidávej další správce balíků.

## Externí hranice

Bez samostatného explicitního oprávnění neobjednávej, neplať, neměň DNS, registrátora, doménové kontakty, přístupy ani produkční hosting. Nenahrávej nový web na veřejný server a neruš Webnode. Zadání fáze C1 neopravňuje k C2.

E-maily neodesílej, neodpovídej na ně ani je nepřeposílej. Platí to také pro testovací zprávu z formuláře a zprávy podpoře. Lokální testy používají zachytávací transport; skutečné odeslání testu provede uživatel. Přihlašovací formulář není kontaktní zpráva, read-only přihlášení v objednaném průzkumu je možné.

Nečti obsah pošty, pokud k ověření stačí seznam složek, počty a velikosti. Přesun historie pošty patří až do výslovně autorizované migrace a soukromé zálohy musí zůstat mimo repozitář i veřejný web.

Přístupy používej podle `docs/ACCESS.md`. Neexportuj je do plaintextu, výpisů, browser snímků, Git historie ani předání Claude. Bezpečné úložiště `.secrets/` není distribuční balík.

## Ověření a odevzdání

Každá kontrola musí ověřit konkrétní kritérium. Po chybě uprav hypotézu; po dvou neproduktivních pokusech změň přístup. Neoslabuj kontrolu kvůli zelenému výsledku. Neskrývej nesplněné podmínky za `DONE`.

Odevzdání obsahuje skutečně dokončenou fázi, důkazy, zbývající omezení a označení příští fáze. Rozlišuj „obsah převzat“, „vzhled schválen“, „nasazeno“ a „ověřena pošta“. Nepoužívej nové vlákno ani podagenta pro autorství nebo redesign bez potřebného zadání. Cílená pomoc s technickým problémem musí mít vymezené soubory a hranice; jeden soubor upravuje jeden agent.
