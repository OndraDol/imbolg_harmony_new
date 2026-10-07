# Návrhy vylepšení

Návrh není schválení změny. Při A4 i B1 texty zůstávají doslovné. A2 doplní konkrétní ID a citace sporných bloků.

## Dodatečně schválené připomínky 2026-10-07

Uživatel výslovně objednal realizaci připomínek majitelky včetně GitHub Pages: celá obdélníková fotografie v záhlaví široká 112 px, odstranění čáry nad zdravotními testy Amy a přesná obsahová změna feny-node-010 z „BZ: 4x I. cena, CACT, res.CACT, Klubový vítěz“ na „BZ: 5x I. cena, CACT, res.CACT, Klubový vítěz“. Původní A2 archiv/evidence se nemění; jednotlivá odchylka je kontrolovaná ve verify_content_a4.py. Stav implementace a důkazy určuje STATUS/WORKLOG. Ostatní návrhy níže tím nejsou schválené.

## Součást technické kopie

Menší hlavička, čitelná sazba, přehledné rozestupy, kompletní mobilní menu, viditelný focus, responzivní fotografie, přístupné zvětšení galerií, klikací telefon/e-mail, srozumitelné chyby formuláře, zachování URL a metadat. Finální estetiku řeší Claude.

## Návrhy pro majitelku

### C1: připravená informace u formuláře, před publikací přijmout znění

„Správcem údajů z formuláře je Markéta Kunešová, Myslbekova 559, 407 21 Česká Kamenice, kontakt kralovamarket@seznam.cz. Jméno, e-mail a případnou zprávu použijeme k vyřízení vašeho dotazu. U poptávky koupě nebo služby jde o přípravu případné smlouvy na vaši žádost; u obecných dotazů o náš oprávněný zájem odpovědět na vámi zahájenou komunikaci. Formulář používá hosting Gigaserver a poštovní službu Seznam. Běžnou uzavřenou komunikaci uchováme nejdéle šest měsíců od vyřízení, poté ji odstraníme; pro zprávy potřebné ke smlouvě, zákonným povinnostem nebo konkrétnímu nároku platí odpovídající samostatný účel. Na uvedeném kontaktu můžete uplatnit svá práva na přístup, opravu, výmaz či omezení a podle podmínek zpracování přenositelnost nebo námitku. Můžete se také obrátit na Úřad pro ochranu osobních údajů.“

Toto je připravený návrh pro budoucí tok, nevkládá se automaticky do veřejného obsahu. Uživatel 2026-10-07 výslovně uložil určit správce. Markéta Kunešová je uvedená v původním veřejném Kontaktu a její přihlášený Webnode účet označuje tento projekt rolí VLASTNÍK; přiřazení vychází z těchto skutečných podkladů. IČO se nedoplňuje odhadem. Šest měsíců je navržené budoucí pravidlo pro vyřízené běžné dotazy a krátkou návaznost, není to zjištěné současné nastavení Seznamu nebo zákonem předepsaná jednotná lhůta. Dosavadní pošta se nemaže ani nemigruje; budoucí dodržování řeší majitelka. Při změně provozovatele musí být správce opravený podle skutečnosti.

Podklady byly přečtené v [příručce ÚOOÚ](https://uoou.gov.cz/verejnost/zakladni-prirucka-k-ochrane-udaju) a [zásadách Evropské komise](https://commission.europa.eu/law/law-topic/data-protection/information-business-and-organisations/principles-gdpr_en): správce odpovídá skutečnému účelu a prostředkům; smluvní poptávka a obecný dotaz se rozlišují a uchování má odpovídat potřebnému účelu. Před zveřejněním přijmout text a ověřit skutečné podmínky poskytovatelů/logy, které vydá konkrétní hostingový účet. Obecné pravidlo neslibuje délku každé technické zálohy Seznamu nebo Gigaserveru. Přesný způsob dodání informací návštěvníkovi připravit při povolené obsahové úpravě; nová stránka ani povinný souhlasový checkbox se zde nevytvářejí. From větev stále není implementovaná, produkční SMTP a doručení neověřené. Technické podklady jsou v FORM.md.

| Návrh | Důvod | Omezení |
|---|---|---|
| Sjednotit beagle / bígl | Jednotnější jazyk | Zatím nepřepisovat |
| Aktualizovat úvod galerie | Mluví o budoucích štěňatech, jiné části už o narozeném vrhu | Nové znění musí potvrdit majitelka |
| Prověřit popisy služeb | `sluzby-node-003` má nadpis „Péče o plemeno“, zatímco následující `sluzby-node-004` začíná „Výcvik pro beagly je skvělou příležitostí…“. Pod `sluzby-node-005` „Poradenství pro nové majitele“ začíná `sluzby-node-006` „Péče o plemeno zahrnuje…“. | Navrhnout nové přiřazení či znění majitelce; A4 zachovává zdroj beze změny. |
| Zdůraznit aktuální vrh a kontakt | Snazší orientace zájemce | Nevyvozovat dostupnost štěňat z existence stránky |
| Přidat zdravotní dokumenty | Doložení existujících údajů | Jen dodané podklady a oprávnění zveřejnit |
| Zpřesnit kredity fotografií | Pexels patička nepopisuje všechna média | Uživatel 2026-10-07 potvrdil oprávnění k původním médiím. Jednotlivé autory/přiřazení doplnit jen z důkazu; existující kredit zachovat. |

Bez nového zadání nepřidávat rezervace, platby, newsletter, blog, další jazyky ani analytiku. Zvyšovaly by rozsah, správu nebo provozní náklady.

## B1: návrhy mimo redesign (nic z toho není provedeno)

| Návrh | Důvod | Podmínka |
|---|---|---|
| Vlastní písmo loga (např. Lobster, OFL) uložené lokálně | Bližší původnímu psanému logu; B1 používá systémová písma, protože allowlist verify_a3 nepovoluje nové soubory v dist | Rozšířit allowlist a doložit licenci souboru |
| Prohlížeč fotografií (lightbox) jako progresivní vylepšení | Pohodlnější procházení galerií na mobilu | Vyžaduje JS soubor a úpravu kontrol A3/A6 (zákaz script, Enter otevírá plný soubor); bez JS zachovat odkaz |
| Nadpis h1 na úvodu, Službách, Fenách a Psech | Struktura pro čtečky a vyhledávače | Nový text nebo převzetí názvu stránky schválí majitelka |
| Uvozovky v nadpisech ("Péče o beagle", "Výcvik pro beagly"…) | Původní Webnode zápis působí jako placeholder | Rozhodne majitelka; B1 je zachovává |
| Datum Roxany a Lea s odrážkou • jednotně | Feny mají „• 30.5.2023“, Psi „3.3.2026“ bez odrážky | Jen se souhlasem |
