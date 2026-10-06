# Přístupy

Přístup Webnode je lokálně uložen v `.secrets/webnode.credential.xml` jako Windows DPAPI PSCredential. Soubor ignoruje Git. Není určený do veřejného webu ani pro předání Claude. Žádná přístupová hodnota se nesmí objevit v dokumentaci.

## Použití a ověření

Načti PowerShell příkazem `Import-Clixml -LiteralPath <absolutní cesta k souboru>` do lokální proměnné. Nevypisuj objekt ani jeho heslo. Dešifrovanou hodnotu použij pouze bezprostředně pro ověřené přihlašovací pole Webnode a pak proměnnou odstraň. Nevytvářej plaintext mezisoubor a nezahrnuj hodnoty do logů/screenshotů.

Windows DPAPI je vázané na účet a prostředí, které soubor vytvořilo. Přenos na jiný počítač nebo spuštění pod jiným uživatelem nemusí fungovat; v takovém případě vyžádat nové bezpečné předání. Nesnažit se obnovit heslo z historie výpisů.

A1 ověřila čerstvé načtení a shodu se vstupem, nepřítomnost otevřeného hesla v souboru a Git ignorování. To potvrzuje uložení, ne přihlášení do služby.

## Stav systémů

| Systém | Stav |
|---|---|
| Webnode | Uloženo lokálně, přihlášení zatím nepotvrzené |
| VEDOS | Přístup nebyl dodán, žádný účet ani převod se nezaložil |
| Gigaserver | Přístup nebyl dodán, žádná služba se neobjednala |
| Doménová pošta | Adresa, přístupy a velikost neověřené |
| Seznam | Známý příjemce formuláře; přihlášení pro vývoj není potřeba |

Předchozí Webnode login skončil obecným hlášením, ne explicitním odmítnutím hesla. Při opakovaném selhání změň přístup nebo požádej o ruční přihlášení. Neobcházej CAPTCHA a nespouštěj reset hesla bez zadání.

Pošta, privátní archiv administrace a SMTP konfigurace patří mimo Git a veřejný adresář. Bezpečné umístění zálohy pošty stanovit v C1 s uživatelem. A1 žádnou poštu nečte a nezálohuje. Před commitem i uploadem kontrolovat skutečný seznam souborů: .gitignore sám nezabrání chybnému FTP uploadu.
