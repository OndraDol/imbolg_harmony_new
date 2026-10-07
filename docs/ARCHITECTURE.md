# Technické zadání budoucí implementace

Stav: A3–A6, aplikace redesignu B1 a regresní kontrola B2 jsou dokončené v místním rozsahu. A6 přidala release builder, společnou public/private fixture a browser audit v osmi samostatných procesech; stejný nezměněný harness nad finální B2 prošel 8/8. B1 mění pouze CSS a atribut data-page společného layoutu; B2 doplňuje tři řádky CSS pro šířku formuláře a contain hover a cílený tests/browser_b2.py. Obsah, serverová rozhraní a technologie se nemění. Eleventy 3.1.6 je uzamčené v `package-lock.json`, PHPMailer 7.1.0 v `server/composer.lock`. Důkazy jsou v STATUS, FORM, B2-REVIEW a CLAUDE-HANDOFF, finální B2 readback v artifacts/b2. Vzhled B2-2026-10-07-ef779044 je schválený majitelkou prostřednictvím uživatele. C1 připravila MIGRATION, skutečný Seznam účet/DPAPI přístup a správce/návrh soukromí, vytvořila místní šifrovaný snímek a ověřila jeho kompletní obnovu do odděleného cíle. C1 DONE po odpovědi Webnode; DNS správa bez Premium potvrzená, doménovou poštu ověřit před případným ukončením Standardu. C2 ani nasazení nezačaly. Hashový readback C1 potvrzuje nezměněnou B2.

## Rozdělení souborů

```text
src/_data/           společné kontakty, navigace a galerie
src/_includes/       Nunjucks layouty a komponenty
src/content/         doslovné obsahové fragmenty po stránkách
src/pages/           vstupy s pevnými permalinky
src/assets/          CSS, minimální JS, optimalizované fotografie
evidence/pages.json  nezávislý zdrojový základ stránek z A2
evidence/media.json  logická média, zdrojové varianty a všechny výskyty
evidence/source-map.json  zdroj → výsledné HTML/média, doplní A4
evidence/exclusions.json  zdůvodněné technické výluky Webnode
server/public/api/contact.php  veřejný vstup formuláře
server/app/          serverová validace, transport, odpovědi
server/config.example.php     nefunkční vzor bez přístupů
server/vendor/       závislosti PHP, ignorované Gitem
scripts/             build, verifikace, balení
tests/               obsahové, formulářové a browser kontroly
archive/             raw zdroje a originály, ignorované Gitem
artifacts/           screenshoty a výsledky, ignorované Gitem
private/             lokální konfigurace a zachycené testy, ignorované
dist/                jen generovaný veřejný web
release/             budoucí nasazovací balík public + private
```

Soukromá data nikdy nedávat do src. Skutečné schéma přizpůsobit archivovanému obsahu při zachování těchto rozhraní; změny popsat, neimprovizovat nový framework.

## Obsahová smlouva

pages.json: původní URL, title a metadata, čas snímku, cesta/hash archivního HTML a bloky v původním pořadí. Blok má stabilní ID, typ, přesný text nebo odkazy na média a cíle odkazů. Například ID `feny-text-001` zůstává stabilní po redesignu.

media.json: stabilní ID logického média, všechny nalezené URL variant, vybraný originál, rozměry, bajty, SHA-256, původ/kredit/nejistota, galerie a všechny výskyty. Jedna fotografie může mít více výskytů; deduplikace nesmí odstranit výskyty. Stejný název neprokazuje stejnou fotku. Různé ořezy posoudit vizuálně.

source-map.json: ID bloku → cílová URL a DOM značka `data-content-id`; média → veřejné soubory a výskyty `data-media-id`. Kontrola musí ověřit i původní a výsledné cíle odkazů a pořadí galerie. Originály mohou zůstat jen v archivu, veřejné optimalizované deriváty se mapují zpět na jejich ID.

Baseline pochází z původního webu, nikdy z nového výstupu. Povolena je normalizace konců řádků, HTML entit a technických mezer včetně NBSP; není povoleno odstranit interpunkci, slova, diakritiku, čísla nebo emoji. Změny baseline vyžadují doloženou změnu zdroje nebo schválení, ne potřebu zeleného testu.

## Základní vzhled A3

Funkční klidný základ, finální styl až B1. Bílé pozadí, tmavý text, tlumené modré akcenty navazující na původní web, systémové fonty bez externího načítání. Hlavní vizuální obsah jsou původní fotografie. Bez nových sloganů, AI ilustrací, animovaného hero a automatických sliderů.

Barvy, šířky, fonty a rozestupy jako samostatné CSS proměnné. Obsahové fragmenty bez designových tříd. Desktop menu smí přehledně zalamovat; mobilní má všech deset položek a musí být dostupné i bez JS, např. nativní details/summary.

Fotografie mají rozměry, srcset a lazy loading mimo první viditelný obraz. Zvětšení odkazuje na lokální plnou variantu i bez JS. Lightbox, pokud vznikne, ovládání klávesnicí, Escape, návrat focusu a přístupné názvy.

## Aktuální vzhled B1

Aktuální vizuální vrstva B1 je dodaná varianta 1B Fotka: tmavá pozadí, teplý oranžový akcent, systémové písmo a Palatino/Georgia pro nadpisy. Původní fotografie a nativní mobilní details/summary zůstávají. Stránkové layouty vybírá atribut data-page; obsahové fragmenty neobsahují nové designové třídy. U fotografií s motivem u okraje a diplomů je contain bez zvětšování při hover. Výše uvedený světlý vzhled popisuje historický základ A3.

## Formulářové rozhraní A5

`POST /api/contact.php`, standardní HTML formulář, application/x-www-form-urlencoded, bez příloh. Pole `name`, `email`, `message` a skryté `website`. Jméno a e-mail povinné. Povinnost zprávy zachovat podle skutečně archivovaného formuláře; v předběžném průzkumu povinná nebyla. Potichu ji nezpřísnit.

Server omezuje velikost požadavku a polí, odmítá neplatný e-mail, pole typu array, hlavičkové řídicí znaky a jiné HTTP metody. Příjemce je pevný Seznam, nikdy parametr od návštěvníka. Současná A5/B2 vyžaduje ověřený From na @imbolg-harmony.cz z neveřejné konfigurace; návštěvník patří do Reply-To. SMTP přístupy jsou pouze neveřejné.

Provozní volba uživatele z 2026-10-07 mění budoucí konfiguraci: doména/DNS zůstanou u Webnode, web u Praktiku a From má být nový samostatný účet Seznam. Veřejná nápověda uvádí smtp.seznam.cz:465 s implicitním TLS a autentifikací. Ochrana v server/app/transport.php zatím Seznam From odmítne; její vymezená úprava, relevantní capture/negativní testy a nový release patří až do autorizované C2 podle [MIGRATION](MIGRATION.md) a [FORM](FORM.md). Pevný příjemce, validovaný Reply-To, TLS, zakázaný výchozí transport a rate limit zůstávají požadované. Seznam konfigurace není ověřená tímto popisem ani stávajícím B2 testem.

Rate limit používá krátkodobý stav mimo DocumentRoot bez textů zpráv. Limit konfigurovatelný a zdůvodněný v A5. Nedůvěřovat libovolnému X-Forwarded-For. Chyby jsou české a s bezpečně escapovanými vstupy fungují bez JS. Chyba serveru nebo chybějící SMTP nesmí hlásit úspěch. SMTP úspěch znamená předání k odeslání, ne doložené doručení.

Výchozí produkční transport je zakázaný do dodání validní konfigurace. Testy používají pouze explicitní capture/fake SMTP bez síťového odeslání. Capture odpověď říká, že jde o lokální zachycení. Návštěvník nemůže režim přepnout URL parametrem. Eleventy dev server PHP nespouští; A5 musí zdokumentovat samostatný lokální PHP náhled a testovací příkaz.

## Build a nasazení

Build do dist kopíruje jen schválené veřejné soubory; ne celý projekt nebo server. Budoucí release má public a private. PHPMailer, aplikační kód a konfigurace jsou mimo DocumentRoot; konkrétní hostingové cesty dodá až samostatně objednaný účet, ověřit je v C2 před uploadem. Pokud to hosting neumožní, návrh bezpečného uložení předložit před uploadem, ne improvizovat s heslem ve veřejné složce.

Kanonický sestavený strom, který se použije i v lokálním PHP testu:

```text
release/
  public/                  DocumentRoot; obsah dist/ (HTML, média, CSS, JS)
    api/contact.php        kopie server/public/api/contact.php
  private/                 sourozenec DocumentRoot, nikdy uvnitř něj
    app/bootstrap.php      vstup serverové aplikace ze server/app/
    app/                   další serverové aplikační soubory
    vendor/                produkční Composer závislosti ze server/vendor/
    config.example.php     bezpečný vzor ze server/config.example.php
    config.php             doplněno pouze lokálně/na hostingu, ne z veřejného buildu
    var/                   neveřejný dočasný stav rate limitu; test capture jen lokálně
```

Endpoint má relativní smlouvu načtení `dirname(__DIR__, 2) . '/private/app/bootstrap.php'`. Bootstrap pak načítá konfiguraci a autoloader z rodičovského private. Žádné hledání konfigurace ve veřejném adresáři a žádné předání absolutní cesty návštěvníkem.

Nasazovací mapa: obsah release/public nahrát do potvrzeného DocumentRoot; obsah release/private do adresáře private vedle DocumentRoot pod stejným rodičem. Samotný webový adresář na hostingu se může jmenovat jinak než public, vzájemná poloha však musí zůstat stejná. C1 připravila tuto mapu a bránu; přístup k oběma místům a absenci kolize s cizími soubory ověří první kroky samostatně autorizované C2 v konkrétním účtu. Pokud host tuto polohu neumožňuje, C2 nesmí pokračovat bez konkrétně opravené a otestované mapy.

A5 a A6 testují stejný strom v oddělené lokální fixture přes společnou funkci populate v scripts/release_a6.py. DocumentRoot je výhradně public, config používá jen syntetický capture transport. A6 sestavuje release bez skutečných přístupů a bez testovacích zpráv; config.php pro produkci doplní až C2 bezpečně mimo veřejný prostor. Nejde o oprávnění balík v A6 nahrát. Builder porovná instalovaný PHP package name/version/reference s lockfilem, odmítá symlinky/junctions a nepřepisuje konfigurovaný release. Značka release/.generated-a6 nepatří do uploadu; manifest je mimo release v artifacts/a6.

Produkční dist obsahuje .htaccess s Options -Indexes, DirectoryIndex index.html a ErrorDocument 404 /404.html, samostatnou 404 stránku s noindex, sitemap deseti obsahových URL a robots bez blokace veřejného obsahu. Testový tests/php_router_a6.php emuluje 404 pouze v lokálním PHP serveru a není v balíku. C1 zjistila veřejné varování Gigaserveru před Options s možným HTTP 500; konkrétní nutnost úpravy dosud neověřená a schválený B2 se nemění. MIGRATION určuje první hostovací test po samostatné autorizaci C2: povolení direktiv, vlastní HTTP 404, nepřístupnost private a nepřítomnost výpisu složek musí být prokázané před DNS. Odstranění Options -Indexes vyžaduje nejprve doložené vypnutí AutoIndex na úrovni hostingu a stejný test. Browserová emulace sama podporu hostingu nedokazuje.

Limit 80 MB zahrnuje celý skutečně nahrávaný balík včetně PHP závislostí. Originální archiv na hosting nepatří. Kanonický host je `https://www.imbolg-harmony.cz`. Náhled chránit před indexací, produkční release nesmí omylem obsahovat náhledové noindex nebo blokující robots.
