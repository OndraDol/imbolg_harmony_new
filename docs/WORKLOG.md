# Záznam práce

Každý skutečně provedený krok zapsat sem. Šablona: datum a fáze; činnost a účel; dotčené soubory/systém; výsledek a důkaz; omezení; další krok. Neuvádět přístupy ani soukromou poštu.

## 2026-10-06 / před A1 / plánovací průzkum

Provedeno read-only prohlédnutí veřejného webu, menu a sitemap.xml. Zjištěno deset veřejných URL. Texty byly přečteny přes webový nástroj a veřejný DOM v agent-browser; galerie vyžadují důkladnější rozbalení v A2. Jeden referenční screenshot úvodu byl pouze v dočasné složce Windows; projektový archiv zatím neexistuje. Nejde o hotovou kopii ani soupis všech médií.

Veřejné DNS čtení ukázalo MX `imap.mail.webnode.com` s prioritou 10 a NS `ns1.register.it`, `ns2.register.it`. Jde o pozorování, ne úplný export DNS ani důkaz konkrétní aktivní schránky. Žádný DNS záznam se nezměnil.

Podagent explorer_luna (GPT-5.6 Luna, medium) provedl veřejnou rešerši Webnode/Gigaserver. Hlavní agent ověřil rozhodující stránky a doplnil VEDOS. Původní domněnka pomocníka, že externí hosting vyžaduje Webnode Premium, nebyla doložená a byla odmítnuta; veřejná nápověda řeší připojení domény k projektu Webnode. Přesné zdroje a nejistoty jsou v MIGRATION.md.

Přímé Invoke-WebRequest selhalo na firemní proxy HTTP 407. Veřejné čtení přes agent-browser fungovalo. Jednorázový eval přes stdin vrátil null; přímý eval s Promise fungoval. Přihlášení přes skutečné UI Webnode skončilo obecným hlášením „Registraci se nepodařilo odeslat. Zkuste to prosím znovu.“ Nešlo o explicitní chybu hesla. Pokus otevřít login v Chrome přes CUA skončil timeoutem/resetem. Administrace nebyla prohlédnuta. Vlastní relace agent-browser byla uzavřena.

Uživatel rozhodl: správu obsahu přes AI, zachovat doménovou schránku, formulář doručovat na současný Seznam. Preferuje VEDOS + Gigaserver, pokud je převod bezpečný a rychlý. Plán byl odevzdán v chatu, v plánovacím režimu nebyly vytvořené soubory.

## 2026-10-06 / A1 / upřesnění rozsahu a kontrola prostředí

Po požadavku na realizaci uživatel výslovně upřesnil, že cílem této relace je především plán pro další model. Rozsah omezen na A1, žádný webový kód ani závislosti nebyly vytvořené. Načteny skilly ondra-delivery-loop, frontend-design, webapp-testing a Node dependency runbook; poslední dva implementační postupy zatím nebyly použité. Průzkum předchozí relace se neopakoval.

Ověřena absolutní pracovní složka `C:\Users\ondrej.dolejs\Desktop\Projekty\imbolg_harmony`. Byla prázdná. `git -C <projekt> rev-parse --show-toplevel` potvrdil, že složka ani její rodiče nejsou Git repozitář. Následuje vytvoření dokumentace a lokálního repozitáře.

## 2026-10-06 / A1 / základ dokumentace

Přes apply_patch vytvořeny .gitignore, README.md, AGENTS.md, STATUS.md a tento WORKLOG. AGENTS ukládá dokumentaci každého provedeného kroku, ochranu obsahu, hranice externích změn a práci pouze na objednané fázi. README rozlišuje současnou dokumentaci od budoucích npm příkazů. Následuje doplnění všech zadání fází a bezpečné uložení přístupů.

## 2026-10-06 / A1 / Git a přístupy

Založen lokální Git s větví main. Přístup Webnode uložen v ignorované `.secrets/webnode.credential.xml` jako Windows DPAPI PSCredential. Čerstvé načtení potvrdilo shodu údajů; kontrola potvrdila nepřítomnost otevřeného hesla v souboru. `git check-ignore -v` potvrdil pravidlo `.secrets/`. Heslo nebylo vloženo do dokumentace ani zdrojového souboru. Přihlášení Webnode se v A1 neopakovalo.

## 2026-10-06 / A1 / oprava zápisu dokumentace

Jedna dávka apply_patch pro rozšířené dokumenty selhala kvůli chybnému kontextu aktualizace WORKLOG. Kontrola adresáře potvrdila, že nové dokumenty nevznikly; nešlo o částečně uloženou realizaci. Dávka se rozděluje na samostatné dodatky s přesnými kontexty. Na webu ani v externích účtech se nic nezměnilo.

## 2026-10-06 / A1 / hlavní plán a předávací dokumenty

Vytvořeny PLAN, ARCHITECTURE, ACCESS, CONTENT-INVENTORY, MIGRATION, IMPROVEMENTS a CLAUDE-HANDOFF. Zdrojové ceny a DNS jsou označené jako dřívější průzkum, seznam médií a administrace jako neověřené. Handoff má výrazný stav NEPŘIPRAVENO. Návrh rozlišuje veřejnou archivaci od administrativní zálohy a blokuje migraci bez jejich dořešení. Další krok: samostatná podrobná zadání A1–C2, potom kontrola souborů a bezpečnosti.

## 2026-10-06 / A1 / podrobné fáze přípravy a redesignu

Vytvořena samostatná zadání A1–A6 a B1–B2 se vstupy, konkrétním postupem, ověřením a bodem zastavení. Obsahové testy musejí vycházet ze zdroje, ne z nové kopie. Formulář má lokální transport bez odesílání, přístupný chybový návrat a ochranu konfigurace. B1 výslovně patří Claude Opus a B2 odděluje technickou regresi od schválení majitelkou. Žádná z těchto implementací nebyla provedena. Následují detailní C1/C2 a závěrečná kontrola dokumentů.

## 2026-10-06 / A1 / migrační fáze

Doplněny C1 a C2. C1 je příprava a čtení účtů bez objednávky či přepnutí; povinně uzavírá administraci, kapacity a zálohy. C2 má oddělené kroky registrátora, DNS, webu a pošty, kontrolu po objednávce, ruční uživatelský test a rollback včetně zpráv doručených během přechodu. Sedmidenní souběh není slib automatického monitorování. Následuje kontrola odkazů, konzistence a úniku přístupů.

## 2026-10-06 / A1 / kontrola dokumentace a druhé čtení

Programově ověřeno 21 Markdown dokumentů, všech 10 zadání fází, lokální Markdown odkazy, přítomnost vstupů/postupu/DONE a UTF-8 bez náhradních znaků. Výsledek: 0 nalezených problémů. Ověřeno, že src, dist, package.json ani node_modules neexistují. Kontrola proti bezpečně načtené hodnotě přístupu nenašla heslo v žádném dokumentu; tajná hodnota nebyla vypsaná. Git nemá remote a ukazuje pouze nové dokumentační soubory.

Spuštěn cílený read-only reviewer_terra (GPT-5.6 Terra, high) pro materiální rozpory v návaznosti fází, zachování obsahu a externích oprávněních. Nemá číst .secrets ani cokoli upravovat. Výsledek druhého čtení bude doplněn před dokončením A1.

## 2026-10-06 / A1 / nálezy a jejich oprava

Reviewer našel dvě konkrétní vady: průběžný STATUS dosud uváděl Git/DPAPI jako budoucí krok a ARCHITECTURE neurčovala dostatečně přesný release strom. Stav byl aktualizován, aby nikdo neopakoval uložený přístup. Doplněna jediná kanonická mapa public/private, relativní cesta endpointu do bootstrapu, návaznost lokálních PHP testů a explicitní upload mapování. Odpovídající instrukce promítnuty do A5, A6 a C2. Žádný kód formuláře se nevytvořil.

Dokumentace byla explicitně přidána do Git indexu; `git diff --cached --check` prošel. Git hlásil pouze převod LF/CRLF podle existujícího nastavení Windows, nikoli chybu obsahu. Nebyl nastaven remote. Požadavek na otevření PLAN.md v Codexu nástroj přijal se stavem queued; skutečné zobrazení panelu tím není potvrzené. Následuje opakování dotčených dokumentačních kontrol a uzavření A1.

## 2026-10-06 / A1 / dokončení

Po opravách znovu ověřeno 21 dokumentů a přesná sada 10 fází: žádný neplatný lokální odkaz, chyba UTF-8 nebo chybějící zadání. Ověřena přítomnost přesné release smlouvy. Kontrola Git indexu a diff --cached --check prošla; soukromé adresáře v indexu nejsou. Neexistují src, server, dist, package.json ani node_modules. Tím je doloženo dodržení rozsahu pouze dokumentace.

STATUS přepnut na A1 DONE, všechny další fáze zůstávají TODO. Uzavření A1 zahrnuje lokální Git checkpoint dokumentace (identita v git log), bez remote a bez push. Připraven prompt pro samostatné zadání A2. Nic se neobjednalo, nenasadilo, nepřevádělo, neodesílalo a nezměnilo na zdrojovém webu. Neověřené účty, média a pošta zůstávají výslovně uvedené pro příslušné budoucí fáze.
