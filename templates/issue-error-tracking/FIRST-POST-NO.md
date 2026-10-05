# Følg et avvik fra observasjon til kontrollert tiltak
Hold avviket, feilhendelsen og hvert forsøk på et tiltak adskilt.
Skriv hva du forventet, hva som skjedde, hvordan feilen kan gjenskapes,
mulige årsaker og hvordan hvert tiltak ble prøvd. Behold det ukjente.

En vektet skår støtter prioritering når grunnlaget er registrert.
Tillit til grunnlaget og kostnaden ved å kontrollere står separat.
En loggoppdatering er ikke en ny feilhendelse. Bestått kunstig test
beviser ikke at tiltaket virker i faktisk bruk.

Python-kontrollen sjekker struktur, koblinger mellom postene, skårer,
oppgitt testomfang og registrerte kontrollbeslutninger. Rapportbyggeren lager
lokale rapporter. Ingen av dem beviser fullstendig historikk, riktig årsak,
trygg tekst eller tillatelse til å publisere.

~~~mermaid
flowchart TD
  A["Registrer en observasjon"] --> B["Vurder avviket"]
  B --> C["Prøv hvert tiltak"]
  C --> D{"Godkjenningskriteriene oppfylt?"}
  D -->|Ja| E["Avslutt eller følg videre"]
  D -->|Nei eller ukjent| B
  E --> F["Kontroller en trygg offentlig tekst"]
  F --> G["Egen kontroll før publisering"]
~~~

Opprett en tom registreringsfil, fyll skjemaene og kjør check før rapporten
lages. Det valgfrie eksemplet er oppdiktet. Full rapport for åpne avvik og
kortere rapport for løste avvik følger samme grenser for kildegrunnlaget.

Skrevet 5. oktober 2026 for mappen templates i dette repoet.
