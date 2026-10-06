# Aktuální stav

Poslední aktualizace: 2026-10-06. Tento soubor je autoritativní pro stav; plán a zadání fází samy nejsou důkazem realizace.

## Rozsah aktuální relace

Uživatel upřesnil: „Nezapomeň, že máš primárně vytvořit plán fází pro horší model, ne to sám udělat.“ Dokončena pouze A1. Web nebyl implementován, zdrojový obsah nebyl archivován a externí systém se nezměnil.

| Fáze | Stav | Důkaz / omezení |
|---|---|---|
| A1 Inicializace a plán | DONE | 21 dokumentů, 10 fází; odkazy a konzistence ověřené, dvě připomínky opravené; DPAPI a Git ignorování ověřené |
| A2 Soupis a archiv | TODO | Existuje jen předběžný veřejný průzkum; chybí kompletní archiv |
| A3 Technický základ | TODO | Žádný package.json, kód webu ani projektové závislosti |
| A4 Přenos obsahu | TODO | Bez implementace |
| A5 Formulář | TODO | Bez implementace a bez SMTP konfigurace |
| A6 Kontrola a předání | TODO | Claude handoff je zatím jen zadání |
| B1 Claude redesign | TODO | Vyhrazeno Claude Opus po A6 |
| B2 Regresní kontrola | TODO | Závisí na B1 |
| C1 Příprava migrace | TODO | Známé veřejné ceny; chybí ověření účtů a pošty |
| C2 Přepnutí | TODO | Vyžaduje nové explicitní oprávnění |

## Důležité neověřené skutečnosti

1. Přihlášení Webnode: předchozí pokus skončil obecnou chybou formuláře, běžný Chrome pak timeoutem. Správnost hesla není vyvrácená. Neopakovat automaticky stejné pokusy.
2. Administrace: neznáme skryté stránky, koncepty, knihovnu, adresáta starého formuláře, aktivní balíček, expirace a přesnou cenu domény pro tento účet.
3. Pošta: uživatel potvrdil existenci používané doménové schránky, ale přesná adresa, objem, aliasy a historie nebyly ověřené. Veřejný MX ukazuje na Webnode.
4. Obsah: 10 veřejných URL bylo přečteno; úplný počet médií a souborů není stanoven. Textový výpis galerie není důkaz úplnosti.
5. Práva a původ fotografií: existuje obecný kredit Pexels, přiřazení ke konkrétním souborům není ověřené.
6. Praktik: použitelnost závisí na velikosti výsledného balíku a pošty. Žádný hosting není objednaný.
7. Převod domény: cesta přes CZ.NIC existuje obecně; držitel, kontaktní e-mail, blokace a DNSSEC konkrétní domény čekají na ověření.

## Následující krok

Po samostatném zadání začít A2 podle `docs/phases/A2.md`: nejdřív aktuální veřejný soupis a archiv, teprve dalšími fázemi webový kód. Git init ani DPAPI uložení neopakovat. Čtení dokumentace nesmí spustit další fáze automaticky.

Připravený prompt: `/goal Načti README.md, AGENTS.md, docs/STATUS.md a docs/phases/A2.md. Proveď pouze A2, průběžně dokumentuj kroky a ověř kritéria dokončení. Nepřecházej do A3 a neměň externí systémy.`
