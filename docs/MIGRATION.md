# Provoz a budoucí migrace

Stav: plán a veřejná rešerše z 2026-10-06. Nic nebylo objednané, převedené, nasazené nebo zrušené. Před změnou ověřit aktuální ceny a konkrétní účet.

## Doložené ceny

| Položka | Ročně včetně DPH | Zdroj |
|---|---:|---|
| Praktik, opakovaná cena | 181,50 Kč | [Gigaserver tarify](https://www.gigaserver.cz/webhosting/porovnani-tarifu), 150 Kč bez DPH |
| .cz prodloužení VEDOS | 193,60 Kč | [VEDOS domény](https://hosting.vedos.cz/domeny/), 160 Kč bez DPH |
| Preferovaná kombinace | 375,10 Kč | Součet, bez případného navýšení prostoru a dalších služeb |
| .cz prodloužení Gigaserver | 264,99 Kč | [Ceník domén](https://www.gigaserver.cz/ceniky/ceny-domen), 219 Kč bez DPH; web zaokrouhluje na 265 Kč |
| Vše u Gigaserveru | přibližně 447 Kč | Přesný součet výše je 446,49 Kč |
| Doména Webnode | Neověřeno pro účet | [Ceník](https://www.webnode.com/cs/domeny-cenik/) nedodal spolehlivou cenu v Kč pro tento účet |

Praktik: 100 MB pro web, PHP včetně 8.3, SMTP/IMAP/POP3 a základně 200 MB na schránku. Dostatečnost prostoru, případné navýšení, SMTP limity, zálohy, HTTPS a neveřejné složky potvrdit v C1. [Parametry](https://www.gigaserver.cz/webhosting/zakladni-webhostingove-tarify), [kapacita pošty](https://kb.gigaserver.cz/velikost-e-mailove-schranky-a-jeji-navyseni/).

Gigaserver podporuje doménu registrovanou jinde: [externí doména](https://www.gigaserver.cz/webhosting/hosting-a-domena). Neobjednávat novou doménu namísto připojení existující.

## Převod a Webnode

[CZ.NIC](https://podpora.nic.cz/cs/domeny/) umožňuje získat AuthInfo přes stávajícího či nového registrátora, vlastním formulářem nebo Doménovým prohlížečem u MojeID kontaktu. Uvádí platnost 14 dní. Nežádat heslo týdny předem. Žádný požadavek o heslo nebyl odeslaný.

Pro konkrétní doménu je třeba ověřit držitele, e-mail, blokace, stav registru a DNSSEC. Převod registrátora není změna hostingu ani nameserverů. Zjistit, zda současný provozovatel zachová DNS zónu po odchodu; nepředpokládat to.

[Webnode DNS](https://www.webnode.com/cs/support/nastavit-dns-u-domeny/) dovoluje A/CNAME/MX/TXT. Nápověda Premium řeší připojení domény k projektu Webnode; nedokládá povinnost Premium pro pouhou registraci s externím webem. Dostupnost DNS správy po skončení balíčku není potvrzená. Pokud by doména zůstala, tuto vlastnost i cenu ověřit pro účet. Agent může připravit text dotazu podpoře, nesmí jej odeslat.

## Výchozí DNS pozorování

2026-10-06: MX `imap.mail.webnode.com`, priorita 10; NS `ns1.register.it`, `ns2.register.it`. Toto není úplná zóna. Před migrací exportovat A, AAAA, CNAME, MX, TXT, CAA a další skutečné záznamy, TTL a DNSSEC/DS. IP, DKIM ani SPF nového poskytovatele nevymýšlet podle obecných příkladů.

## Povinné vstupy C1

Funkční přístupy a expirace, držitel/kontakt/blokace domény, úplná DNS zóna a návaznost nameserverů; používané schránky, aliasy, přeposílání, objemy a složky; bezpečné místo soukromé zálohy; nový hosting s dostatečnou kapacitou; potvrzené PHP, HTTPS a neveřejné umístění konfigurace; doménový From a SMTP; schválený release po B2; rozdíly obsahu od A2; uživatel pro ruční test pošty a termín změny.

## Pořadí a návrat

Nejdřív zálohy a konkrétní rollback, potom připravený hosting a schránky, náhled a autorizované přepnutí. Převod registrátora samostatně, s zachovanou nebo připravenou DNS správou. Nepřijímat automatické DNS z objednávky bez porovnání staré zóny.

Před změnou zaznamenat staré hodnoty a TTL; případné snížení TTL jen v autorizovaném okně. Ověřit HTTPS pro www i apex, kanonické přesměrování a zapomenutý AAAA na starý server. DNSSEC měnit koordinovaně, ne pouhým přepsáním NS.

Poštu předkopírovat, při přepnutí dorovnat a během souběhu kontrolovat oba servery. Změna MX sama nepřenese historii. Porovnat složky a počty s rozlišením nových zpráv a duplicit. Návrat MX nevrátí zprávy doručené novému serveru; rollback musí pokrýt i je. Nevytvářet dva samostatné SPF záznamy.

Uživatel ručně ověří příjem/odeslání pošty a formulář na Seznamu včetně spamu. SMTP přijetí není inbox receipt. Po úspěšném přepnutí nejméně sedm dní souběhu. Zrušení Webnode až po kontrole a samostatném souhlasu; nesmí omylem zrušit doménu, poštu ani potřebná data.
