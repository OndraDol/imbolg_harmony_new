# Schválený plán: Imbolg Harmony

Aktuální stav k 2026-10-10: C1 DONE, C2 po technické přípravě BLOCKED na rozhodnutí o HTTPS/DNS a přijetí textu soukromí. Níže uvedený úvodní stav C1 BLOCKED/C2 TODO je historický text plánu ze 2026-10-07; autoritativní průběh a důkazy jsou v [STATUS](STATUS.md) a [WORKLOG](WORKLOG.md).

Zadání a rozhodnutí: 2026-10-06, provozní volby upřesněné 2026-10-07. Plán popisuje celý projekt. Aktuální oprávnění a stav určují poslední zadání uživatele a [STATUS](STATUS.md). A1, veřejná A2, technická A3, veřejný obsah A4, lokální formulář A5, kontrola/předání A6, aplikace dodaného redesignu B1 a regresní kontrola B2 jsou dokončené. Verze B2-2026-10-07-ef779044 je technicky ověřená a výslovně schválená majitelkou prostřednictvím uživatele. C1 má skutečný účetní/DNS průzkum, veřejné kontakty a konkrétní MIGRATION pro ponechání domény u Webnode a Seznam SMTP. Správce/návrh soukromí a nový účet imbolg.harmony.formular@seznam.cz s DPAPI přístupem jsou připravené, skutečná místní šifrovaná záloha 3 074 souborů kompletně obnovená do oddělené složky a ověřená podle hashů a velikostí. C1 BLOCKED pouze na potvrzení DNS/editace po Standardu, C2 je TODO. Oprávnění k původním médiím uživatel potvrdil. Produkční SMTP a skutečné doručení neověřené. Původ návrhu od Claude potvrzuje uživatel, přesná varianta modelu v ZIP není doložená.

## Cíl a rozsah

Nahradit webovou část Webnode samostatným levně provozovatelným webem, zachovat 100 % veřejného autorského obsahu, deset položek menu a původní URL. Zlepšit použitelnost na PC i mobilu. Nejprve úplný funkční základ, potom redesign v Claude Opus, až následně autorizovaný přesun webu a zapojení nového odesílacího účtu. Správa domény a příjemcová schránka zůstávají na místě.

Obsah spravuje uživatel přes AI. Bez administrace, databáze a placeného formulářového SaaS. Texty převzít doslovně; návrhy změn evidovat zvlášť. Fotografie nesmějí zmizet kvůli prostoru hostingu. Originály archivovat a pro veřejný web připravit věrné optimalizované varianty.

## Rozhodnuté technologie a provoz

Eleventy + Nunjucks, běžné CSS, minimum JavaScriptu. Node jen lokálně při sestavení. PHP 8.3 + PHPMailer přes SMTP pouze pro formulář. Příjemce: `kralovamarket@seznam.cz`, shodný s původním formulářem. Nový samostatný Seznam účet bude autentizovaným From, návštěvník patří do Reply-To. Současné PHP tuto variantu ještě nepodporuje; úprava a nový ověřený release patří až do samostatně autorizované C2. Pokud se prokáže používaná doménová adresa, zachovat její přeposílání na Seznam bez požadavku běžného webmailu; veřejný průzkum takovou adresu nenašel. Soukromá konfigurace, PHP závislosti a zálohy mimo veřejný adresář. Podrobnosti: [ARCHITECTURE](ARCHITECTURE.md).

Vybraná kombinace: doména a DNS u Webnode, web u Gigaserveru Praktik a nový běžný účet Email.cz pro SMTP. Registrátor, NS/DS a nynější MX/DKIM/DMARC zůstávají. Nabídka prodloužení Webnode domény včetně stávající skryté registrace 964,37 Kč + Praktik 181,50 Kč + Email.cz 0 Kč dává 1 145,87 Kč ročně za uvedené služby včetně DPH. Není započtená případná další úhrada Standardu; DNS po jeho skončení dosud nepotvrzené. Vypnutí skryté registrace nebo převod k VEDOS nebyly zvolené. Praktik má 100 MB pro web; interní limit celého balíku je 80 MB a schválená B2 má 50 430 699 B. Gigaserver mailová kapacita ani její navýšení nejsou potřebné pro zvolené Seznam SMTP. Smart má jen 15 MB, proto nepojme tento balík.

Webnode Standard byl zaplacený na 1 808 Kč za rok do 12. 11. 2026, další automatická obnova 28. 10. 2026 má neověřenou cenu. Doménová služba podle Webnode končí již 8. 11. 2026; registr CZ.NIC uvádí 13. 11. 2026. Doména se později prodlouží u Webnode, agent nic neplatí ani nemění předplatné. Přesun webových A/www je podporovaný bez převodu domény. Pro ukončení Standardu chybí potvrzení pokračující autoritativní DNS služby a správy; jeho nutnost ani bezplatné pokračování se neodhadují. V přechodovém okně původní projekt a Premium zachovat, aby šel web i formulář vrátit na Webnode. [MIGRATION](MIGRATION.md) obsahuje zdroje, přesné mezery a návrat.

## Fáze a závislosti

| Fáze | Výsledek | Vstup |
|---|---|---|
| [A1](phases/A1.md) | Git, dokumentace, detailní fáze, bezpečné přístupy | Schválený plán |
| [A2](phases/A2.md) | Soupis a archiv veřejného webu | A1 |
| [A3](phases/A3.md) | Technický základ a základní responzivní vzhled | Veřejný obsahový základ A2 |
| [A4](phases/A4.md) | Převzetí všech textů, médií, galerií a odkazů | A2 a A3 |
| [A5](phases/A5.md) | Formulář a lokální testy bez odesílání | A4 |
| [A6](phases/A6.md) | Kontrola a vyplněné předání Claude | A4 a A5 |
| [B1](phases/B1.md) | Redesign v Claude Opus | A6 a zadání Claude |
| [B2](phases/B2.md) | Regrese a schválení majitelkou | B1 |
| [C1](phases/C1.md) | Konkrétní migrační postup | B2; dílčí read-only zjištění lze získat dřív při zadaném průzkumu |
| [C2](phases/C2.md) | Autorizované přepnutí a ověřený provoz | C1 a nové explicitní oprávnění |

Fáze má samostatné vstupy, kroky, výstupy, kontroly a bod zastavení. Neprovádět následující fázi „pro úplnost“. A1 a A2 nevytvořily webový kód ani nenakoupily služby. A3 vytvořila pouze technickou kostru a nic nenasadila.

## Co znamená zachovat 100 %

Všechny veřejné autorské texty a jejich opakování, nadpisy, popisky, média, položky galerií, soubory a cíle odkazů k zaznamenanému okamžiku archivace. Zachovat emoji a podstatné údaje uvnitř obrázků, které musejí zůstat čitelné při zvětšení. Žádné sloučení stránek do landing page a žádné odstranění opakování bez zadání.

Interní Webnode skripty a tracking nejsou autorský obsah k převzetí, ale jejich vypuštění zaznamenat. U patičky rozliš techniku od kreditů a právních údajů. Neodstraňovat obecný kredit Pexels bez vyřešení jeho významu.

Veřejný soupis není záloha administrace. Pokud administrace není dostupná, může A2 doložit jen veřejnou archivaci s výslovným omezením „administrace neověřena“. Porovnání administrace pak zůstává povinnou bránou C1. To neumožňuje vynechat žádný nalezený veřejný obsah ani tvrdit, že je bezpečné zrušit Webnode. Neveřejné koncepty evidovat odděleně, nezveřejňovat automaticky. Před přepnutím prověřit změny od A2.

## Důkazy a dokončení

Úplnost dokládá nezávislý zdrojový základ a mapa zdroj → cíl. Použitelnost dokládá skutečný browser na šířkách 360, 390, 768 a 1440 px, klávesnice a zvětšení textu. Formulář dokládají pozitivní i negativní lokální testy; skutečné doručení až ruční test uživatele. Migraci dokládá čerstvé DNS/HTTP čtení, kontrola schránek a potvrzený provoz.

Zelený build, první návrh, upload ani SMTP přijetí samy nedokazují úplné dokončení. Rozlišovat kopii, redesign, nasazení a poštu. Každý krok zapsat do WORKLOG a konec fáze do STATUS. Návrhy nad rámec kopie jsou v [IMPROVEMENTS](IMPROVEMENTS.md).
