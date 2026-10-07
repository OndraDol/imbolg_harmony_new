# Schválený plán: Imbolg Harmony

Zadání a rozhodnutí: 2026-10-06. Plán popisuje celý projekt. Aktuální oprávnění a stav určují poslední zadání uživatele a [STATUS](STATUS.md). A1, veřejná A2, technická A3, veřejný obsah A4, lokální formulář A5 a kontrola/předání A6 jsou dokončené. B1 čeká na samostatné zadání; produkční SMTP a skutečné doručení neověřené.

## Cíl a rozsah

Nahradit Webnode samostatným levně provozovatelným webem, zachovat 100 % veřejného autorského obsahu, deset položek menu a původní URL. Zlepšit použitelnost na PC i mobilu. Nejprve úplný funkční základ, potom redesign v Claude Opus, až následně autorizovaná migrace webu, domény a pošty.

Obsah spravuje uživatel přes AI. Bez administrace, databáze a placeného formulářového SaaS. Texty převzít doslovně; návrhy změn evidovat zvlášť. Fotografie nesmějí zmizet kvůli prostoru hostingu. Originály archivovat a pro veřejný web připravit věrné optimalizované varianty.

## Rozhodnuté technologie a provoz

Eleventy + Nunjucks, běžné CSS, minimum JavaScriptu. Node jen lokálně při sestavení. PHP 8.3 + PHPMailer přes SMTP pouze pro formulář. Příjemce: `kralovamarket@seznam.cz`. Doménovou schránku zachovat; adresu, objem a historii zjistit v C1. Soukromá konfigurace, PHP závislosti a zálohy mimo veřejný adresář. Podrobnosti: [ARCHITECTURE](ARCHITECTURE.md).

Preferovaná kombinace: doména VEDOS, web a pošta Gigaserver Praktik, pokud je převod bezpečný a rychlý. Veřejně ověřené opakované ceny: 193,60 + 181,50 = 375,10 Kč ročně včetně DPH. Nejvýhodnější ověřená varianta není důkaz absolutního minima trhu. Praktik má 100 MB pro web; interní limit celého balíku je 80 MB. Schránka má základně 200 MB; navýšení a případnou cenu ověřit. Smart má jen 15 MB, proto jej neplánovat kvůli úspoře 36,30 Kč ročně.

Doména i Praktik u Gigaserveru jsou alternativa přibližně za 447 Kč ročně. Ponechání domény u Webnode vyžaduje ověřit skutečnou cenu účtu a samostatnou DNS správu po Premium. Netvrdit, že pro externí hosting musí Premium zůstat placené: to veřejné podklady nedoložily. [MIGRATION](MIGRATION.md) obsahuje zdroje, nejistoty i návratový postup.

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
