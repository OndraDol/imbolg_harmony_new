# Provoz a budoucí migrace

Stav k 2026-10-07: C1 BLOCKED po dokončení dostupného průzkumu, nového Seznam účtu a skutečné místní zálohy. Jediná zbývající poskytovatelská podmínka konečné varianty je zachování DNS/editace po skončení Standardu. Aktivní plán je doména a DNS u Webnode, web u Gigaserveru Praktik a formulář přes nový samostatný účet Seznam. Správce podle výslovného pověření určený a text soukromí připravený. Účet imbolg.harmony.formular@seznam.cz má čerstvý readback a DPAPI přístup v ignorovaném .secrets; místní snímek 3 074 souborů má úspěšnou hashovou kontrolu všech 12 dílů a kompletní ověřenou obnovu na disk do oddělené složky. C2 je TODO a vyžaduje samostatné zadání. Nic nebylo zaplaceno, potvrzeno jako objednávka, nahráno na hosting, přepnuto ani zrušeno. Dřívější otevření cenové nabídky Webnode vytvořilo neodeslaný checkout; nebyla potvrzena platba ani změna předplatného.

## Skutečné služby a obsah

| Oblast | Doložený stav | Omezení a důsledek |
|---|---|---|
| Webnode | Přístup v již přihlášeném Chrome fungoval 2026-10-07; projekt imbolg-harmony8, primární imbolg-harmony.cz | Samotný login nepotvrzuje právního držitele nebo jeho kontaktní e-mail |
| Standard | Zaplacené období 12. 11. 2025 až 12. 11. 2026; automatická obnova 28. 10. 2026 | Cena příští obnovy neověřená; předplatné zůstalo beze změny |
| Doména a skrytá registrace u Webnode | Služby do 8. 11. 2026; uživatel požaduje ponechání a pozdější prodloužení u Webnode | Pro provozní plán použít dřívější termín služby, ne až expiraci registru |
| Registr CZ.NIC | Registrace 13. 11. 2025, expirace 13. 11. 2026, REG-MEDIA4WEB / Media4Web s.r.o. | Webnode je správce pro uživatele; registrátora ani doménové kontakty neměnit |
| Držitel a kontakty | Anonymouse Domains s.r.o., M4WR-29D9C; administrativní kontakt WEBNODE | Skrytá registrace; skutečný kontakt nebyl zjištěný. Bez transferu není AuthInfo nebo odstranění proxy podmínkou tohoto webového přesunu |
| Správce formulářových údajů | Na pokyn uživatele určená Markéta Kunešová, Myslbekova 559, 407 21 Česká Kamenice, kralovamarket@seznam.cz; původní Kontakt a stejná osoba s rolí VLASTNÍK projektu Webnode | Konkrétní návrh účelu, právního základu a uchování je v IMPROVEMENTS; šest měsíců pro běžné vyřízené dotazy je budoucí návrh, ne zjištěné nastavení schránky. Text se před publikací přijme |
| DNS a DNSSEC | NSSET WEBNODE-TB, ns1/ns2.register.it; KEYSET M4WK-29D9C, DNSKEY a parent DS | Osm viditelných záznamů a systémové údaje zachycené. NS/KEYSET/DS zůstávají; žádná delegace k jinému poskytovateli |
| Webový prostor | 34 MB z 10 GB, přenos 162 MB z 10 GB podle editoru | Období přenosu nezobrazené; nejde o velikost nového balíku |
| Doménové schránky | UI uvádí žádný účet, 0 z 20; MX Webnode | Neprokazuje nulovou historii ani absenci neveřejného přeposílání. Žádná schránka ani zpráva nebyla čtená |
| Veřejné e-mailové adresy | Čerstvý Chrome průchod všech deseti stránek: pouze Kontakt uvádí kralovamarket@seznam.cz; žádná @imbolg-harmony.cz v textu nebo mailto. Ve všech 47 logických médiích A2 nebyl nalezený čitelný e-mail | JPEG pixely vizuálně zkontrolované, čtyři SVG přečtené celé. Archivní bajty, bez OCR drobného pozadí a bez nového binárního stažení; neveřejné služby se tím nevylučují. Pro nalezený veřejný kontakt nový doménový forward není potřeba |
| Původní formulář | Vizuálně ověřené upozornění na kralovamarket@seznam.cz | Může vysvětlovat hlášený příjem z webu, konkrétní hlášená zpráva ověřená není |
| Zálohy Webnode | 0 manuálních záloh z 5 | Rozsah automatických záloh/obnova pro účet nepotvrzené; místní kopie projektu je samostatná záloha s vymezeným rozsahem níže |
| Stránky a knihovna | Deset stránek, všechny show_in_menu true a private_access false; panel galerie ukázal osm používaných obrázků | Kompletní nepoužitá knihovna nebyla inventarizovaná ani exportovaná |
| Aktuální veřejný obsah | 10/10 URL odpovídá A2 v autorském textu, pořadí/identitě hlavních obrazů, galeriích/popiscích a odkazech | Nové binární porovnání médií neproběhlo; živý sitemap blokoval klient |
| Původní média | Uživatel 2026-10-07: „Potvrzuji oprávnění k původním médiím“ | Oprávnění pro převzetí původních médií potvrzené; zachovat Pexels kredit, neodvozovat nové autorství jednotlivých souborů |
| Gigaserver | Přístup nedodaný/neověřený; služba nevytvořená | Konkrétní IP a cesty se nevymýšlejí; doplnění a test jsou první brány autorizované C2 |
| Nový Seznam účet | Uživatel dokončil registraci a čerstvé přihlášené menu potvrzuje imbolg.harmony.formular@seznam.cz | Přístup v .secrets/seznam-smtp.credential.xml šifrovaný DPAPI, import/shoda/absence plaintextu/Git ignorování/ACL ověřené. Přihlášení ze serveru, 2FA konfigurace a skutečné doručení zatím neověřené |

Důkazy: [sanitizované pozorování účtu](../artifacts/c1/account-observations.json), [nové poštovní ověření a volby](../artifacts/c1/mail-scope-2026-10-07.json), [adresy v archivních médiích](../artifacts/c1/public-media-email-check-2026-10-07.json), [čerstvý vlastník, DNS a registrace](../artifacts/c1/completion-observations-2026-10-07.json), [CZ.NIC WHOIS](https://www.nic.cz/whois/domain/imbolg-harmony.cz/) a [WORKLOG](WORKLOG.md). Žádné heslo, neveřejný vlastnický e-mail, zpráva nebo platební údaje nejsou v dokumentaci.

Nezávislý A2 základ zůstává archive/2026-10-06T13-40-23Z/. [Veřejné porovnání](../artifacts/c1/public-comparison.json) má deset průchodů bez rozdílu. Nepoužité soubory musí zůstat u majitelky nebo být obnovitelně uchované před zrušením projektu či zásahem do jeho dat. Projekt se zde neruší. Externí mapový widget se v editoru nenačetl; dostupnost živé mapy tím není potvrzená.

Schválený vstup B2-2026-10-07-ef779044: souhlas „Je to schváleno.“ z 2026-10-07, identita ef7790446ba6470d3cee43694c399722296831a98176af803efc7a08e6fdb820. Release 239 souborů / 50 430 699 B, public 49 898 869 B a private 531 830 B; package SHA-256 eaa15904b8bc65dc169069dffa13d7a6a7661aedacd1e639cb0678145042527e. [C1 readback](../artifacts/c1/readback-results.json) doložil kontinuitu bez buildu. Nová volba Seznam From zatím není implementovaná v tomto releasu.

## Doložené ceny

Odečet 2026-10-07. Faktura, nabídka pro účet a veřejná opakovaná cena mají odlišný význam.

| Položka | Cena včetně DPH | Povaha a důkaz |
|---|---:|---|
| Webnode Standard, 1 rok | 1 808 Kč | Zaplaceno podle WI0004044001.pdf, 12. 11. 2025 až 12. 11. 2026; základ 1 494 Kč, DPH na faktuře 314 Kč |
| Webnode doména, prodloužení 1 rok | 603,79 Kč | Neodeslaná nabídka účtu pro 8. 11. 2026 až 8. 11. 2027, 499 Kč bez DPH |
| Webnode skrytá registrace, 1 rok | 360,58 Kč | Součást nynějšího nastavení, 298 Kč bez DPH; její vypnutí uživatel nezadal |
| Webnode doména a skrytá registrace | 964,37 Kč | Celá neodeslaná nabídka: základ 797 Kč, DPH 167,37 Kč; neuhrazeno |
| Praktik, opakovaně ročně | 181,50 Kč | 150 Kč bez DPH, [tarify Gigaserver](https://www.gigaserver.cz/webhosting/porovnani-tarifu) |
| Nový běžný Email.cz pro SMTP | 0 Kč za službu | [Podmínky Email.cz](https://o-seznam.cz/napoveda/email/smluvni-podminky/), bezúplatná služba; nejde o garanci odesílací kvóty |
| Let's Encrypt | 0 Kč za certifikát | [Nápověda Gigaserver](https://kb.gigaserver.cz/co-je-lets-encrypt-a-jak-jej-nainstalovat/); certifikát dosud neaktivovaný |
| Vybraná kombinace Webnode doména včetně skrytí + Praktik + Seznam | 1 145,87 Kč ročně za uvedené služby | 964,37 + 181,50 + 0; bez případné další úhrady Standardu. Konečný provoz bez Standardu závisí na potvrzené DNS službě |
| Stejná kombinace bez skryté registrace | 785,29 Kč ročně za uvedené služby | Pouze vysvětlení doplatku 360,58 Kč; není zvolené vypnutí skrytí ani změna kontaktů |

Faktura je [lokální soukromý podklad](C:/Users/ondrej.dolejs/Desktop/WI0004044001.pdf), SHA-256 e5347f89d18b28cf116010ca53d33bf996732da86b0ab2b0765a10c665897b13. Do repo se nekopíruje. Budoucí cena Standardu, dřívější zaplacená doména a případné jiné služby nejsou doložené; přesný současný opakovaný součet ani skutečnou úsporu nelze uvést. Zaplacený Standard je náklad původního období a v souběhu se neplatí automaticky znovu. Další obnovu může provést stávající předplatné 28. 10.; agent je nemění.

Dřívější cenové varianty VEDOS nebo doména u Gigaserveru nejsou aktivní plán po uživatelově rozhodnutí. U Praktiku není kvůli zvolenému SMTP na Seznamu potřebná nová mailová kapacita nebo placené navýšení. Veřejný základ Praktiku pro případnou jinou schránku je 200 MB, navýšení na 500 MB 302,50 Kč a 1000 MB 605 Kč jednorázově; tyto nezvolené služby se do rozpočtu nepřičítají. Přesná velikost cílového účtu a logů se ověří v C2.

## Doména zůstává u Webnode

Uživatel určil ponechání domény u Webnode a pozdější úhradu její obnovy tam. Registr zůstává REG-MEDIA4WEB, správa pro uživatele u Webnode, NS ns1/ns2.register.it a nynější DNSSEC. C1 ani plán C2 neobsahují AuthInfo, převod registrátora, změnu držitele, kontaktů, NSSET nebo KEYSET. Historické transferové úvahy zůstávají pouze ve WORKLOG.

Webnode [výslovně odkazuje na nasměrování jinam pomocí DNS](https://www.webnode.com/cs/support/prevest-domenu-pryc/) a [návod DNS](https://www.webnode.com/cs/support/nastavit-dns-u-domeny/) popisuje A/CNAME/MX/TXT. Gigaserver [umožňuje hosting s doménou jinde](https://kb.gigaserver.cz/mohu-mit-hosting-u-gigaserveru-a-pritom-domenu-jinde/). Změna webového cíle tedy nevyžaduje transfer domény.

Není dosud potvrzené, zda tento konkrétní Webnode účet zachová DNS i jeho správu po konci Standardu při placené doméně a skryté registraci. [FAQ](https://www.webnode.com/cs/support/placene-a-neplacene-sluzby/) rozlišuje doménu a Premium, ale podmínku samostatného DNS jednoznačně neřeší. Nepřisuzovat tím externímu hostingu povinný Standard ani slíbit, že jeho ukončení služby neovlivní.

Nová kontrola skutečné správy domén 2026-10-07 ukazuje „Správa DNS záznamů Aktivní“ a podmínku „Pokud je tato doména registrovaná u Webnode, můžete zde spravovat její DNS záznamy.“ Osm záznamů stále odpovídá snímku. [Aktuální podmínky](https://www.webnode.com/terms-and-conditions/) s účinností 14. 8. 2026 a [doménové podmínky](https://www.webnode.com/domain-names-policies/) oddělují doménovou a Premium službu. Je to podklad pro předpoklad samostatné DNS správy, ale výslovný příslib jejího pokračování po Standardu v přečtených dokumentech není. Nynější aktivní tarif budoucí stav neprokazuje; kvůli testu se předplatné nemění. Připravený dotaz níže je poslední konkrétní mezera konečné varianty bez Standardu.

Nejmenší potřebné potvrzení pro zvolený konečný provoz zní: „Doména imbolg-harmony.cz zůstane u Webnode a bude prodloužená; web bude jinde přes upravené A a www. Zůstanou po skončení Standardu aktivní ns1/ns2.register.it, vlastní DNS záznamy a přístup k jejich správě? Změní se nějak stávající MX nebo případné e-mailové služby?“ Potvrzení musí pocházet z účtové dokumentace nebo od Webnode; aktuálně zapnuté Premium budoucí stav nedokazuje.

Uživatel 2026-10-07 výslovně povolil odeslat tento jediný dotaz jménem majitelky. Přes kontaktní formulář přihlášeného účtu Markéty Kunešové byl odeslaný dotaz pro imbolg-harmony.cz a projekt imbolg-harmony8, téma Domény / Nastavení domény. Obsah zahrnul zachování DNSSEC, možnost editace A/CNAME/MX/TXT, existenci stávajícího přeposílání nebo přijímací služby a případnou další nutnou úhradu; výslovně bez žádosti o změnu, zrušení nebo objednávku. Webnode zobrazil ?sent=1 a „Děkujeme za váš dotaz“, s odpovědí na kralovamarket@seznam.cz podle jeho odhadu během následujících 48 hodin. Ticket ID nebylo zobrazené. [Záznam přijetí](../artifacts/c1/webnode-support-submission-2026-10-07.json) a [snímek](../artifacts/c1/webnode-support-sent-2026-10-07.jpg) dokládají odeslání, vlastní technickou odpověď zatím nemáme. C1 zůstává BLOCKED; po ručním předání odpovědi uživatelem ověřit jednotlivé podmínky a aktualizovat plán i rozpočet. Další dotaz nebo změna služby tím nejsou automaticky povolené.

Standard a původní projekt zachovat pro ověřený návrat v přechodovém okně. Vlastní doména na projektu Webnode vyžaduje Premium; po jeho skončení není návrat na původní doméně jen vrácením A zaručený. Obnova původního projektu je jiná věc než obnova registrace domény. Pozdější vypnutí obnovy/ukončení Standardu vyžaduje samostatné zadání a splněné podmínky, doménová služba se neruší.

## Výchozí DNS pozorování

Snímek 2026-10-07 08:22:29 UTC: [dns-snapshot.json](../artifacts/c1/dns-snapshot.json), SHA-256 8e90ad1ed8ae66034a6c1fa0b89bd437c843b231c05c750b15b8a0f6a6193486. Obsahuje 25 veřejných dotazů, oba autoritativní servery, parent DS přes 1.1.1.1 a všech osm záznamů z UI. Není to AXFR nebo důkaz absence libovolných dalších subdomén. Před změnou znovu načíst UI a relevantní autoritativní hodnoty; neodstraňovat jiné služby nebo celou zónu.

| Jméno v imbolg-harmony.cz | Typ | Původní hodnota | Autoritativní TTL | Vybraný cílový stav, nyní neprovedený |
|---|---|---|---:|---|
| @ | A | 3.73.27.108 | 3600 | Nahradit potvrzenou cílovou sadou IPv4 Gigaserveru až po připraveném HTTPS |
| @ | A | 3.125.172.46 | 3600 | Druhou starou A zahrnout do stejné změny; cílová IP zatím nedodaná |
| www | CNAME | imbolg-harmony8.webnode.cz. | 3600 | Nahradit přesným doporučením cílového účtu; typ nelze v UI jen přepsat, případnou změnu CNAME na A provést jako koordinované odstranění/přidání po vlastní autorizaci |
| @ | MX 10 | imap.mail.webnode.com. | 3600 | Ponechat stávající hodnotu; příchozí doménová pošta se podle tohoto plánu nepřesouvá |
| @ | TXT | v=spf1 a mx include:spfuser.webnode.com -all | 3600 | Nevkládat Seznam include jen kvůli From @seznam.cz. Před změnou A vyhodnotit mechanismus a pro případné skutečné doménové odesílatele; změna TXT není automaticky schválená |
| _dmarc | CNAME | _dmarc-user.webnode.com. | 3600 | Zachovat, nový Seznam From nepotřebuje DMARC změnu imbolg-harmony.cz |
| key-wb001._domainkey | CNAME | key-wb001._domainkey.webnode.com. | 3600 | Zachovat |
| key-wb002._domainkey | CNAME | key-wb002._domainkey.webnode.com. | 3600 | Zachovat |

Apex AAAA a CAA: oba servery vracejí autoritativní NOERROR/NODATA se SOA. Nepřidávat AAAA bez ověřeného IPv6 a stejného HTTPS. NS ns1.register.it. a ns2.register.it., TTL 3600. SOA ns1.register.it. / hostmaster.register.it., serial 2025111202, refresh 10800, retry 3600, expire 604800, minimum 86400; pozorované negativní TTL 3600. Tyto systémové hodnoty se v plánu nemění.

SPF závislost trvá i bez změny mailových TXT: mechanismus a bere IP apexu, takže změna webového A mění oprávnění pro případný doménový From. Neodvozovat skutečné odesílatele z MX nebo IP webu. Seznam Form From bude @seznam.cz a používá autorizační nastavení Seznamu; SPF imbolg-harmony.cz jej neřídí. Pro případnou jinou doménovou poštu musí zůstat doložená správná autorizace po změně A i během cache. Pokud je potřeba jediný SPF upravit, vyžádat konkrétní změnu podle skutečné služby, ne vymyšlený include. Není důvod kvůli formuláři převádět MX, DKIM nebo DMARC.

DNSKEY flags 257, protocol 3, algoritmus 13, TTL 86400; úplný veřejný klíč je v JSON. Parent DS tag 2997, algoritmus 13, digest typ 2, TTL 3600; digest 1456E2861210F69CBDD9EB3C4004184FD54323F2177B14984D858C78EA99FC5A. Readback potvrzuje shodu obou NS a digest/tag, ne celou kryptografickou validační cestu RRSIG. NS/DS/KEYSET se nemění, proto se neplánuje rekey nebo převzetí podpisových klíčů.

## Pošta a soukromé zálohy

Podmíněné zadání uživatele je zachovat veřejnou doménovou adresu přeposíláním, pokud ji web používá. Read-only průchod všech deseti stránek takovou adresu nenašel; nalezený kontakt i příjemce původního formuláře jsou kralovamarket@seznam.cz. Vizuální kontrola všech 42 jedinečných archivních JPEGů a celé zdroje čtyř SVG také neukázaly čitelný e-mail. Není to OCR nečitelných nápisů ani nový download aktuálních médií. Před C2 zopakovat dotčenou kontrolu, pokud přibude nebo se změní obsah či média. Pro nyní doložený veřejný tok není potřeba vytvořit doménovou schránku, nový forward nebo přesouvat historii Seznamu. Pošta zůstává v dosavadní příjemcové schránce.

0/20 účtů v Webnode není důkaz „e-mail nefunguje“. Neveřejnou adresu nebo přesměrování jsme nepotvrdili ani nevyloučili. Pokud majitelka takovou adresu používá, stačí její přesný název a potvrzený poskytovatel/cíl přeposílání; není požadované její běžné používání přes webmail. Dokud tato služba není doložená, její MX a další mailová DNS se zachovají. Před ukončením původních e-mailových služeb je nutné tuto nejasnost vyřešit.

[Webnode přeposílání](https://www.webnode.com/cs/support/preposilani-emailovych-zprav-nove-rozhrani/) vychází z vytvořené schránky nebo filtru. Samostatný bezplatný forward při 0 účtech či po konci Premium není potvrzený. Jestli se později prokáže potřebná doménová adresa, vybrat její skutečně dostupné přeposílání na Seznam a cenu před jakoukoli mailovou změnou. Nehádat info@ a nerozšiřovat nynější objednávku C1 o tuto realizaci.

### Nový odesílací účet na Seznamu

Nový samostatný technický účet Email.cz odpovídá uživatelově volbě a jeho bezplatné vytvoření bylo povolené v C1. Uživatel ručně dokončil registraci a čerstvé osobní menu v Chrome potvrzuje skutečnou adresu imbolg.harmony.formular@seznam.cz. Agent nezadával nové heslo ani nepřijal registrační podmínky. Na následné výslovné zadání uložil poskytnutý přístup do .secrets/seznam-smtp.credential.xml přes DPAPI CurrentUser; import/shoda/absence plaintextu/Git ignorování a chráněné ACL ověřené. Schránka příjemkyně se k odesílání nepoužije. Veřejné parametry podle [Seznam nápovědy](https://o-seznam.cz/napoveda/email/mohlo-by-se-hodit/postovni-programy-a-aplikace/): smtp.seznam.cz, port 465, implicitní TLS, PHPMailer encryption ssl, povinná autentifikace. Username a From budou přesně imbolg.harmony.formular@seznam.cz. Při 2FA majitelka nastaví [heslo pro aplikace](https://o-seznam.cz/napoveda/ucet/dvoufazove-overeni/postovni-programy/) bezpečným postupem; hlavní heslo se do dokumentace nebo veřejného webu nedává. Aktuální webové přihlášení neprokazuje SMTP autentifikaci.

Pevný To zůstává kralovamarket@seznam.cz a Reply-To validovaná adresa návštěvníka. [Seznam odmítá nepovolený cizí From](https://o-seznam.cz/napoveda/email/mohlo-by-se-hodit/chyby-v-postovnich-programech/use-your-own/). Pro zvolený Seznam From není potřeba ověřovat doménový alias ani měnit MX/NS této domény. Chceme běžné jednotlivé zprávy kontaktního formuláře, ne rozesílací službu.

[Email.cz je bezplatný](https://o-seznam.cz/napoveda/email/smluvni-podminky/). [Nápověda limitů](https://o-seznam.cz/napoveda/email/mohlo-by-se-hodit/limity-schranky/) uvádí základní počet 120 000 zpráv s možností navýšení; přesné kvóty odesílání za období veřejné nejsou. Příjemcová schránka nebyla otevřená a její zaplnění není doložené. Účet není záruka doručení. Samostatný přepínač povolení SMTP nebyl ve veřejné dokumentaci doložený. Majitelka bude vlastníkem nového účtu, nastaví obnovu přístupu a bude ho udržovat aktivní; podmínky připouštějí omezení počátečně nepoužitého účtu po 14 dnech nebo po více než šesti měsících bez přihlášení. Skutečné spojení ze serveru, autentifikace a doručení se ověří až v C2; agent žádný e-mail neposílá.

### Zjištěná nutná lokální úprava formuláře

Současný [transport.php](../server/app/transport.php) na řádku 30 povoluje v produkci pouze From @imbolg-harmony.cz. Config se Seznam adresou by skončil bezpečnou 503. PHP/PHPMailer port a TLS již umí; nestačí pouze vložit heslo do konfigurace.

Přesné zadání pozdější lokální úpravy: povolit soukromě konfigurovaný, potvrzený Seznam From jen s odpovídající SMTP identitou, zachovat syntaktickou validaci/odmítnutí řídicích znaků, from_verified, pevný To, návštěvnický Reply-To, TLS ověření, rate limit a disabled default. Pro novou větev ověřit shodu From a SMTP username a potvrzený smtp.seznam.cz:465/ssl. Neotevřít libovolný From z POST. Zachovat izolovaný capture @example.invalid; žádné skutečné SMTP v lokálních testech. Dotčené testy musí prokázat povolenou synteticky konfigurovanou Seznam větev, odmítnutí jiné identity/visitor From, pevný To/Reply-To, chybějící konfiguraci 503 a bezezměnné capture omezení. Po implementaci vznikne nová identita releasu; stará B2 se nesmí vydávat za otestovanou Seznam verzi. C1 připravuje zadání, kód nezměnila.

### Co skutečně zálohovat

Před C1 vznikly veřejný archiv A2 a schválený release; C1 doplnila DNS snímek. Samostatná obnovená soukromá záloha pošty nevznikla. Historie stávajícího Seznamu se při přesunu webu nemigruje, proto její export není vstupem tohoto postupu. Pro celkovou osobní obnovu si ji majitelka může zálohovat, agent ji zde nečte ani nekopíruje.

Uživatel výslovně určil místní PC. Konkrétní místo je C:\Users\ondrej.dolejs\Documents\Imbolg-Harmony-Backups mimo repo a hosting; obnovu spravuje místní Windows uživatel ondrej.dolejs. Skutečný snímek 2026-10-07 10:54:04 UTC zahrnuje 3 074 souborů / 1 462 841 611 B zdrojů, evidence, archivů/artefaktů, tehdejší dokumentace, root konfigurací a celého schváleného public/private releasu. Dvanáct dílů má celkem 1 445 286 380 B ciphertextu. Každý díl byl autentizovaný, dešifrovaný v RAM a všechny položky ověřené SHA-256 i počtem bajtů. [Receipt](../artifacts/c1/local-backup-receipt-2026-10-07.json) obsahuje identity dílů a rozsah; jeho kopie a shodný helper jsou také u zálohy. Následná skutečná obnova do C:\Users\ondrej.dolejs\Documents\Imbolg-Harmony-Restore-20261007T105404Z prošla pro všech 3 074 souborů a přesně 1 462 841 611 B. Každý zapsaný soubor má shodnou velikost a SHA-256, oba DPAPI credentialy zůstaly šifrované. Nový cíl má ACL pouze pro současný účet a SYSTEM; původní projekt/archivy/klíč se nepřepisovaly. [Protokol obnovy](../artifacts/c1/local-restore-receipt-2026-10-07.json) je samostatný důkaz, původní receipt zachovává stav v době vytvoření zálohy. Jiný PC/profil se netestoval.

DPAPI přístupy Webnode a nového Seznamu vstoupily pouze v původních šifrovaných souborech uvnitř šifrované zálohy, ne jako hesla. Produkční SMTP config zatím nevznikl. Git, node_modules, runtime, skutečný private config/stav/pošta, server/config.local.php/.env a jiná osobní data do snímku nevstoupily. Pozdější závěrečné doplnění dokumentace/receiptu není vydávané za obsah dřívějšího snímku; základní archiv/release a přístupy v něm jsou. Původní ignored artifacts/c1/local-backup.ps1 a jeho shodná kopie u zálohy jsou nezměněné. Nový local-restore.ps1 i vlastní restore receipt jsou také u zálohy, helper SHA-256 f9c75db415f82b0469dff59184c0982749a7a922fed27214ee0e46f65d7cdf59. Úplná zkušební obnova na disk už proběhla; původní receipt se zpětně nepřepisuje. Budoucí produkční config bude vyžadovat vlastní novou šifrovanou zálohu a obnovu.

Pro samostatné ověření prvního dílu použij existující klíč. Nevytvářej nový a nic nepřepisuj:

```powershell
pwsh -NoProfile -File "C:\Users\ondrej.dolejs\Documents\Imbolg-Harmony-Backups\local-backup.ps1" -Verify -ArchivePath "C:\Users\ondrej.dolejs\Documents\Imbolg-Harmony-Backups\imbolg-c1-20261007T105404Z-vol0001.ihb" -TargetFolder "C:\Users\ondrej.dolejs\Documents\Imbolg-Harmony-Backups"
```

Pro další úplnou obnovu použij novou dosud neexistující cílovou složku. Následující příklad nebyl spuštěný; již ověřená obnova je v cestě končící Restore-20261007T105404Z. Nástroj přijímá pouze běžné absolutní C: cesty, odmítá aliasy/reparse, existující cíl a překryv se zdrojem nebo archivy. Běží pod stejným Windows účtem v existujícím PowerShell 7 a credential XML pouze kopíruje:

```powershell
pwsh -NoProfile -File "C:\Users\ondrej.dolejs\Documents\Imbolg-Harmony-Backups\local-restore.ps1" -ReceiptPath "C:\Users\ondrej.dolejs\Documents\Imbolg-Harmony-Backups\snapshot-20261007T105404Z-receipt.json" -ArchiveFolder "C:\Users\ondrej.dolejs\Documents\Imbolg-Harmony-Backups" -RestoreFolder "C:\Users\ondrej.dolejs\Documents\Imbolg-Harmony-Restore-Dalsi" -ProtectedSourceRoot "C:\Users\ondrej.dolejs\Desktop\Projekty\imbolg_harmony"
```

Klíč je samostatný soubor chráněný Windows DPAPI CurrentUser, složka má omezené ACL. Tato místní kopie nechrání před ztrátou PC nebo Windows profilu a není ověřeně přenosná na jiný počítač. Při pozdější konfiguraci doplnit její novou šifrovanou zálohu a obnovu. GitHub nezahrnuje ignorované A2/artifacts. Před odstraněním starého projektu nebo dat doložit také nepoužitou knihovnu a její obnovu; lokální snímek současného projektu ji nenahrazuje. Pokud se později opravdu přesouvá doménová pošta, je to samostatná autorizovaná změna se soupisem adres/filtrů, metadata historií, šifrovanou kopií, obnovou a zachováním přírůstků; přeposílání nesmí bez rozhodnutí smazat původní historii.

## Cílový hosting a ověření kompatibility

| Podmínka | Doložené veřejné informace | Povinná brána konkrétního účtu před DNS |
|---|---|---|
| Kapacita | Praktik 100 MB web, B2 50 430 699 B, interní strop 80 000 000 B | Ověřit reálnou kvótu a public/private/config/stav/logy; neukládat druhý celý release nebo archivy na tento prostor |
| PHP | PHP 8.3 v [tarifech](https://www.gigaserver.cz/webhosting/porovnani-tarifu) | Skutečně běžící verze, rozšíření, zapisovatelný rate stav a SMTP spojení |
| Neveřejné soubory | [Obecná cesta](https://kb.gigaserver.cz/jaka-je-absolutni-cesta-na-serveru/) /www/doména/doména/ | Potvrzený DocumentRoot a sourozenecký private, PHP přístup/open_basedir a HTTP nedostupnost |
| SMTP | smtp.seznam.cz:465/ssl, nový samostatný Seznam účet | Povolený TCP/TLS přístup ze skutečného hostingu, platný certifikát a autentifikace; heslo jen v soukromé konfiguraci |
| HTTPS | [Let's Encrypt](https://kb.gigaserver.cz/co-je-lets-encrypt-a-jak-jej-nainstalovat/) zdarma pro www/apex, přesměrování se samo nezapne | Platný certifikát obou jmen a jeho obnova; konkrétní způsob vydání před změnou DNS je nutné potvrdit |
| Náhled | [Hosts před DNS](https://kb.gigaserver.cz/41/) | Přidělená IP pro obě jména jen místně, následně odstranit; neobcházet varování certifikátu, HTTP není důkaz HTTPS |
| Zálohy | [FTP jednou za 7 dní](https://kb.gigaserver.cz/jak-probiha-zalohovani-dat-a-jak-mohu-zalohu-ziskat/), [dvě FTP kopie](https://kb.gigaserver.cz/jak-se-zalohuji-data-na-vasich-serverech/), bezplatný archiv | Ověřit dostupnou zálohu a izolovanou obnovu; poskytovatelská FTP kopie není jediná off-host záloha |
| 404 a výpis složek | [ErrorDocument](https://kb.gigaserver.cz/errordocument-404/) podporovaný; [návod chyby 500](https://kb.gigaserver.cz/internal-server-error-chyba-serveru-500/) varuje před Options | Skutečný webserver musí projít rozhodovacím testem níže |

Na „ověř, jestli je kompatibilní řešení vůbec potřeba“: veřejné varování před Options není důkaz selhání Options -Indexes na konkrétním serveru. Výchozí AutoIndex stav není potvrzený. Preventivní změna .htaccess není doloženě potřebná a nebyla provedena.

První hostovací test C2 použije původní .htaccess: Options -Indexes, DirectoryIndex index.html, ErrorDocument 404 /404.html. Požadovat stránky 200, neznámou URL skutečně 404 s vlastním tělem a existující složku bez indexu 403/404 bez výpisu. Současně config/vendor/private/stav/dotfiles/záložní archivy musí být HTTP nedostupné. Jestli vše projde, změna není potřeba. Při 500 zjistit konkrétní příčinu z bezpečného logu. Jestli je příčinou Options, odstranit jen tento řádek až po prokázaném vypnutí AutoIndex na úrovni hostingu a zopakovat adresářový test. Bez ochrany nepokračovat. Každá změna releasu vyžaduje novou identitu a dotčené kontroly.

Pevná nasazovací mapa: release/public do potvrzeného DocumentRoot, release/private do sourozence private pod stejným rodičem. api/contact.php hledá bootstrap právě tam. Obecný návod neprokazuje zápis v rodiči nebo open_basedir; tyto podmínky musí potvrdit účet a test. Pokud vztah není možný, nejdřív připravit konkrétní ověřenou mapu, až potom povolit produkční upload.

## Význam překážek a rozhodnutí

Uživatel rozhodl o požadovaném chování. Fakta o službách se ověřují; nemusí vybírat DNS IP nebo potvrzovat skutečnost, kterou lze přečíst. Práva původních médií jsou vyřešená jeho výslovným potvrzením. Převodní AuthInfo/proxy kontakt, nový doménový From a export historie Seznamu nejsou brány zvolené varianty.

| Bod | Co přesně brzdí | Nejmenší další důkaz |
|---|---|---|
| DNS u Webnode po Premium | Uzavření konečného provozu jen s placenou doménou a bezpečné ukončení Standardu; při dosud aktivním Standardu technická možnost změny A doložená je | Konkrétní potvrzení pokračování DNS a editace při placené doméně, případného vlivu na mail |
| Soukromí formuláře | Zveřejnění nové informace; správce a konkrétní návrh jsou už připravené | Markéta Kunešová a původní kontakt doložené; přijmout text IMPROVEMENTS a před provozem ověřit skutečné podmínky poskytovatelů/logů. Šest měsíců je návrh pro běžné dotazy, ne zjištěná konfigurace |
| Soukromá záloha a nepoužitá knihovna | Zálohu nové produkční konfigurace a pozdější odstranění starého účtu/dat | Místo, správce, skutečný snímek i kompletní obnova všech 3 074 souborů na disk doložené samostatnými receipty. Budoucí SMTP config do dřívějšího snímku nepatří; jeho záloha/obnova a soupis/uchování nepoužité Webnode knihovny zůstávají před příslušným zásahem |
| Případná neveřejná doménová pošta | Zásah do MX/SPF nebo ukončení původního mailového poskytovatele | Pokud se používá, přesná adresa, provider a cíl přeposílání, nutná metadata; běžný login příjemkyně do doménové schránky není požadovaný |
| Seznam úprava PHP a provozní test | Pozdější spuštění formuláře; nový účet je už dokončený | Lokální úprava s testy, bezpečný config, přístup ze serveru a ruční doručení zůstávají C2. Aktuální B2 nepřijme Seznam From |
| Cílový hosting/HTTPS/private/Options | Produkční upload a DNS po objednání | Skutečné údaje a testy z první autorizované C2; veřejný ceník se nevydává za přístup k účtu |
| Cena dalšího Standardu | Přesný součet současných nákladů/úsporu a rozhodnutí o jeho obnově | Cena pro konkrétní účet; faktura minulého období ji nenahrazuje |

C1 se nesmí označit DONE, dokud chybí potřebná dostupnost/obnova nebo schválení. Rozsah potřebných záloh se řídí skutečně měněnými službami. Otevřená možnost neveřejné pošty není důvod migrace historie Seznamu. Neúplná soukromá knihovna nevyvrací úplnost veřejné kopie 10/10; zároveň neopravňuje mazat starý projekt.

Při tomto přerušení jsou účet, přiřazení správce a potřebné místní místo/snímek vyřešené. C1 podle vlastního kritéria zůstává BLOCKED výhradně na poskytovatelském potvrzení DNS po Standardu. Brány konkrétního dosud neobjednaného hostingu, lokální From změny, obnovy budoucí konfigurace, přijetí soukromí a uživatelova doručení nejsou označené jako provedené; nastanou až před příslušnými změnami C2. Bez potvrzení DNS není bezpečně připravené ukončení Standardu ani bezpodmínečný konečný roční součet bez něj.

## Povinné vstupy C1

| Zbývající vstup | Dopad a přesný další krok |
|---|---|
| Podmínky DNS po konci Standardu | Získat výše formulované konkrétní potvrzení. Do té doby neuzavírat cenu celého provozu bez Premium ani nenavrhovat jeho ukončení jako bezpečně připravené |
| Nový účet | Splněno ruční registrací uživatele a čerstvým readbackem; přístup bezpečně uložený. SMTP/doručení zůstává samostatná brána C2 |
| Místní kopie projektu | Splněno snímkem i kompletní obnovou všech 3 074 souborů ve 12 dílech do odděleného cíle s kontrolou každého hashe/velikosti. Záloha a obnova budoucího SMTP configu zůstávají C2; nepoužitá Webnode knihovna před odstraněním |
| Skutečné neveřejné mailové použití, pouze je-li přítomné | Doplnit adresu a poskytovatele před zásahem do jeho služeb. Není potřeba číst těla pošty nebo migrovat neměněný Seznam |
| Budoucí ruční test a okno | Určit osobu pro skutečný formulář/případné forwardy a přijetí výsledku; datum až při objednání C2 |

Konkrétní hostingová IP a cesty se doplní po samostatně autorizovaném objednání; tajné hodnoty pouze bezpečným postupem mimo dokumentaci. Jejich absence zde není důkaz chyby webu. C2 musí mít před každým nevratným krokem příslušnou bránu. Nový Seznam účet vznikl ručně uživatelem v C1 a má readback; žádný skutečný SMTP test neproběhl. Jediná komunikační výjimka je již odeslaný dotaz Webnode výše.

## Pořadí a návrat

Následující kroky jsou plán C2 a pozdějšího samostatného ukončení nepotřebného Standardu. Nejsou provedené.

1. **Uzavřít podmínky a určit okno.** Získat DNS/Premium potvrzení, přijmout připravené soukromí a ověřit aktuální zálohu. Ruční test formuláře provede uživatel, příjem na kralovamarket@seznam.cz potvrdí majitelka Markéta Kunešová prostřednictvím uživatele; termín se určí při zadání C2. Zkontrolovat změny původního webu a čerstvé DNS před krokem; potvrdit konkrétní schválený release. Původní Standard a projekt ponechat pro návrat. Zohlednit automatickou obnovu 28. 10., doménovou službu do 8. 11. a Standard do 12. 11. 2026; DNS neuspěchat kvůli termínu.
2. **Nové explicitní zadání C2.** Objednat pouze zvolený Praktik pro existující doménu spravovanou u Webnode, případné existující účty nejprve využít. Žádná nová registrace stejné domény, transfer nebo delegace NS. Z účtu zaznamenat skutečnou IP, kvótu, PHP, cesty/private a podmínky předběžného HTTPS; odmítnout automatické přepsání DNS bez vlastního kroku.
3. **Připravit Seznam a lokální formulář.** Použít skutečný nový účet po readbacku registrace povolené v C1; nezakládat zbytečně druhý. Majitelka bude vlastník/udržovatel účtu a bezpečně nastaví autentifikaci včetně případné 2FA. Implementovat výše vymezenou From změnu a testy bez síťového odesílání. Příjemce a původní veřejné texty zachovat. Novou identitu/release nechat přijmout pro tuto technickou změnu; B2 vzhled se nereviduje automaticky.
4. **Zálohy a izolovaný náhled.** Uchovat obnovitelné kopie zdrojů/evidence, starého i nového releasu a DNS mimo hosting. Tajné konfigurace pouze šifrovaně mimo Git a ve skutečném private mimo DocumentRoot. Provést public/private mapu, kapacitu, PHP, 200/404, index/private testy, všech deset URL/médií/galerií a capture. Options změnit jen podle konkrétního prokázaného selhání a zachované ochrany.
5. **HTTPS a SMTP před DNS.** Ověřit certifikát pro www/apex na nové IP a budoucí obnovu. Získat konkrétní způsob vydání před DNS; hosts ani ignorování varování jej nenahradí. Ověřit TCP/TLS a přihlášení nového Seznam účtu bez odeslání, je-li pro tuto kontrolu oprávnění; samotné ověření autentifikace neznamená doručení. Uživatel ručně odešle skutečný formulář přes izolovaný náhled a zkontroluje příjem/spam a odpověď na návštěvníka. Agent neposílá.
6. **Přepnout pouze webové DNS.** Po splnění předchozích bran v účtu Webnode změnit celou apex A sadu a www podle potvrzené mapy. Předem vyhodnotit mechanismus a ve SPF, případnou nutnou změnu autorizovat zvlášť. Zachovat MX/DKIM/DMARC, NS/KEYSET/DS a doménové kontakty. Případnou změnu typu www připravit koordinovaně, ne ponechat současně CNAME a A. Pozorované TTL je 3600; snížení není v UI doložené a propagace není garantované okamžité přepnutí všech cache.
7. **Ověřit a přijmout.** Oba autoritativní NS a nezávislé resolvery musí ukázat cílový web a zachované mailové záznamy. Pro www i apex ověřit HTTPS, HTTP/apex přesměrování na https://www.imbolg-harmony.cz se zachováním cesty/query, všech deset starých URL, 404, galerie/média a HTTP nedostupnost private. Uživatel zopakuje skutečný formulář a potvrdí doručení na Seznam. Případnou prokázanou doménovou adresu otestuje ručně v její nezměněné příjmové cestě.
8. **Souběh a pozdější uzávěrka.** Alespoň sedm dní ponechat dostupný nový hosting i původní Webnode s aktivním Premium/doménovou vazbou a platným TLS. Historie Seznamu se nepřesouvá ani nedorovnává mezi servery. Zálohu nové konfigurace a obnovu ověřit. Teprve po přijetí provozu a potvrzení samostatného DNS/mailu může samostatné zadání řešit obnovu/ukončení Standardu. Doménu dál prodlužovat u Webnode, projekt/data bez potřebné kopie nerušit.

### Návrat webu při zachovaném Webnode

Před webovým přepnutím potvrdit původní projekt, jeho doménovou vazbu, aktivní Premium a platný certifikát na staré sadě IP. Neúspěch TLS, 500, ztráta obsahu, chybné přesměrování, zpřístupněné private nebo nedoručený ruční formulář zastaví přijetí a další kroky.

Vrátit obě A 3.73.27.108 a 3.125.172.46 a www CNAME imbolg-harmony8.webnode.cz. podle čerstvého snímku v Webnode. Pokud se typ www změnil na A, vrátit jej koordinovaným odstraněním/přidáním bez souběžného CNAME+A. Znovu posoudit a ve SPF a autorizaci skutečně aktivních doménových odesílatelů během cache; případný TXT nevracet naslepo. MX/DKIM/DMARC, registrar, NS a DS tento webový návrat nemění.

Ověřit oba NS/nezávislé resolvery, www/apex HTTPS, původní cesty a formulář Webnode. Nový hosting ponechat dostupný pro starou cache. TTL 3600 znamená zpoždění, ne pevnou horní mez celého návratu. Přechodovou Seznam konfiguraci uchovat bezpečně; zprávy už doručené do příjemcového Seznamu tam zůstávají. Agent je nečte ani nepřesouvá.

Po skončení Premium není tato návratová větev na vlastní doméně ověřená. Proto má proběhnout přijetí a souběh ještě při aktivním původním Standardu. Pozdější návrat by vyžadoval předem potvrzené obnovení doménové vazby/Premium a HTTPS; projektová adresa je jen nouzový odkaz.

### Návrat formuláře a případného přeposílání

Příjemcová schránka zůstává stejná a MX domény se v tomto plánu nepřepíná, proto se neprovádí zpětný IMAP přenos historie. Při nedoručení nepovažovat SMTP odpověď za úspěšný provoz a nepokračovat s přijetím. Nejbezpečnější připravená cesta během souběhu je výše uvedený návrat celého webu na funkční původní formulář Webnode.

Samotnou novou SMTP konfiguraci lze vrátit jen na předem skutečně otestovanou konfiguraci kompatibilní s odpovídajícím releasem; schválená B2 bez funkčních SMTP přístupů není funkční produkční mailová záloha. Není-li taková konfigurace, bezpečný disabled stav vrací 503 a nehlásí odeslání. Zprávy už předané Seznamu nemažou žádné návratové kroky; při ručním opakování počítat s možnou duplicitou.

Pokud se později prokáže a samostatně mění forward doménové adresy, předem uložit přesnou původní adresu/cíl, ukládání místní kopie a ověřit funkčnost staré přijímací služby. Návrat obnoví tuto konfiguraci a uživatel ručně ověří doručení; případné zprávy přijaté v jiném úložišti se uchovají a beze smazání předají majitelce. Bez existující ověřené přijímací služby nevracet MX naslepo. Tento podmíněný postup není provedená mailová migrace.
