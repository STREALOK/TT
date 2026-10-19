# TT — the Three Tree Tenets

[Norsk](#norsk)

This repository holds TT's site: the posts as pages and PDFs, some of the systems TT runs on as templates, and the small tools that keep them in order.

# Licence
### The code:
(the page structure, stylesheets, scripts and [`serve.py`](serve.py))
is licensed under the GNU Affero General Public License, version 3; see [`LICENSE`](LICENSE).
### The writing:
(the words on the pages and in the posts)
is licensed under Creative Commons Attribution-ShareAlike 4.0 International; see [`LICENSES/CC-BY-SA-4.0.txt`](LICENSES/CC-BY-SA-4.0.txt).

In short: take anything, give credit, give back the same way. (Open-Source)

(Note from Me Myself: personally, imo, if you want to share this personally/privately to anyone, no restriction, no credit needed either ofc.. :p really just if you repost/remake/republish it anywhere would i prefer credit where credit is due please, thank you for your time <3 TT <3)

## What TT is

In the first post's own words:

> TT is a developing way for people and AI systems to investigate, make, correct and share work together. Its philosophical and social name is the Prime Directives.

> The three tenets:
>
> 1. "Do unto others, as you wish done to yourself", considered from more than one thing's position, and in every literal, semantic and philosophical sense.
> 2. Interconnectivity.
> 3. Awareness plus Retention.

> Its effectiveness, novelty and influence are open questions. … Independent tests, counterexamples and corrections are welcome.

To report something, open an issue here: GitHub offers TT's issue and error forms.

## Read the posts

| Post | Date | PDF |
|---|---|---|
| TT: a living method for keeping people, systems and evidence connected. | 27 September 2026 | [PDF](public/TT-first-post-EN.pdf) |
| Second post: two of TT's own systems, shipped bare, so you can run them. | 5 October 2026 | [PDF](public/second-post/TT-second-post-EN.pdf) |
| Third post: the three tenets in a life, and what straying from them seems to cost. | 7 October 2026 | [PDF](public/third-post/TT-third-post-EN.pdf) |
| Fourth post: two receipts for the first tenet. | 8 October 2026 | [PDF](public/fourth-post/TT-fourth-post-EN.pdf) |
| Fifth post: Dante's Inferno, read through the three tenets. | 15 October 2026 | [PDF](public/fifth-post/TT-5-dantes-inferno-EN.pdf) |
| Sixth post: the religious connection. | 15 October 2026 | [PDF](public/sixth-post/TT-6-the-religious-connection-EN.pdf) |

Each post is also an HTML page in [`public/`](public/); [`serve.py`](serve.py) shows them on your own computer.

## Templates

Two of the systems TT runs on, shipped bare so anyone can copy and run them. Both are plain Python with nothing to install; each folder has its own README, a checker with a self-test, and an optional layer of worked examples kept apart from the bare files.

- [templates/dictionary/](templates/dictionary/): one vocabulary kept from three sides (human, formal, mathematical), one rule (a term is Confirmed only when its owner has stated it plainly), and `check_dictionary.py`, which proves the files are well formed and prints one digest two people can compare. The optional layer is a screened extract of TT's own dictionary.
- [templates/issue-error-tracking/](templates/issue-error-tracking/): issues, observed errors, fix trials and record changes kept as separate records, a weighted triage score with its dimensions in the open, and `track.py`, which validates a ledger and builds local or public reports. English and Norwegian forms (`ISSUE-RECORD.md`, `ERROR-RECORD.md`, `RAPPORTSKJEMA-NO.md`), the reporting policy (`ISSUE-POLICY.md`, `FEIL-OG-SAKSPOLITIKK-NO.md`), and a fictional example in `optional/`.

## The matrix at a glance

### Claude-side register

Every problem met while TT was run day to day, sorted by where it came from. Counted on 10 October 2026: 481 problems logged since 18 September 2026, 345 still open or being watched, 132 fixed, and 35 more slips caught by the checks before they landed. The full breakdown puts problems of the same kind on one line, each with the date it was first confirmed: [docs/matrix-by-category-EN.md](docs/matrix-by-category-EN.md).

| Where it came from | Logged | Still open | Fixed | First confirmed |
|---|---|---|---|---|
| Connections and safety gates (bridges, plugins, filters, pushing) | 160 | 107 | 52 | 18 September 2026 |
| The host app (Claude Cowork: sessions, compaction, model switching) | 125 | 102 | 22 | 18 September 2026 |
| Home-made tools and checkers | 86 | 55 | 30 | 18 September 2026 |
| Working rules and projects | 40 | 28 | 11 | 18 September 2026 |
| The Codex side (OpenAI's Codex, across the bridge) | 35 | 25 | 10 | 18 September 2026 |
| The AI's own reasoning | 29 | 24 | 5 | 18 September 2026 |
| Official documentation against the real app | 6 | 4 | 2 | 18 September 2026 |

A first-confirmed date is the earliest the register can show, not proof of the very first time a problem happened.

### Codex records: a separate scope

The matrix above describes the Claude-side register. Codex records are kept in separate files and separate entries: [Codex matrix overview](docs/codex-matrix-overview-EN.md).

The Codex catalogue contains **287 catalogue headings**: **195 legacy source-defined families**, preserving **708 source rows**, plus **92 later entries**.

By category, counted on 10 October 2026:

| Category | Catalog headings | Older families | Later additions |
|---|---:|---:|---:|
| Host and app | 25 | 18 | 7 |
| Cloud and transport | 4 | 2 | 2 |
| Execution tools | 158 | 104 | 54 |
| Context and continuity | 19 | 5 | 14 |
| Workflow and authority | 33 | 31 | 2 |
| Model and tool use | 8 | 1 | 7 |
| Documentation and state | 31 | 26 | 5 |
| Project and content | 9 | 8 | 1 |
| **Total** | **287** | **195** | **92** |

Verified current totals of open or fixed problems are not yet established for this catalogue.

These counts use different units: catalogue headings, source rows and later entries. Their overlap with each other and with the Claude-side register is unresolved. They do not establish independently confirmed incident counts, and there is no combined total.

**Why consolidation is waiting:** This work is funded through personal subscriptions. Intensive work with frontier models, recovery and documentation all consume the subscriptions' usage allowances. On 10 October 2026, the maintainer reported that a 5× Codex subscription plus one usage reset in the same week had still not covered a full week of work. A 20× Claude subscription had reached 99% of its overall weekly allowance roughly 12–24 hours before its next reset. Consolidation is waiting for enough usage capacity to review both catalogues together; subscription costs also constrain this personally funded work.

Consolidation will follow a later reconciliation of provenance, counting units and overlapping records. The separate catalogues preserve their own evidence and scope until that work is complete.

## What is in this repository

| Path | What it is |
|---|---|
| [`public/`](public/) | The site: plain HTML, CSS and a little JavaScript, no build step and nothing to install. Every post is a page and a PDF; each translation sits in its own folder, such as [`public/no/`](public/no/), and each PDF linked here carries its language in its name (`-EN`, `-NO`). |
| [`templates/`](templates/) | Some of the systems TT runs on, shipped bare (see Templates). |
| [`docs/`](docs/) | Documentation: the matrix, every problem met while running TT, sorted by where it came from (see The matrix at a glance). |
| [`tools/`](tools/) | `prepush_check.py`: run before a push, it lists every added line that looks project-internal, and every number in prose, for a person to check. |
| [`.github/`](.github/) | The issue and error report forms GitHub offers when an issue is opened here, and a workflow, run by hand, that publishes chosen files as a Release with a sha256 manifest. |
| [`serve.py`](serve.py) | Serves [`public/`](public/) on your own computer and reloads an open page when a file is saved; nothing outside your computer can reach it. |
| [`wrangler.jsonc`](wrangler.jsonc) | The settings for serving [`public/`](public/) with Cloudflare Workers. |
| [`LICENSE`](LICENSE) | The GNU Affero General Public License, version 3, for the code. |
| [`LICENSES/`](LICENSES/) | [`CC-BY-SA-4.0.txt`](LICENSES/CC-BY-SA-4.0.txt), for the writing. |

## History

Every change is a git commit, so the site's history is its own record.

# Norsk

Dette kodelageret inneholder TTs nettsted: innleggene som sider og PDF-er, noen av systemene TT bygger på som maler, og de små verktøyene som holder dem i orden.

# Lisens
### Koden:
(sidestrukturen, stilarkene, skriptene og [`serve.py`](serve.py))
er lisensiert under GNU Affero General Public License, version 3; se [`LICENSE`](LICENSE).
### Teksten:
(ordene på sidene og i innleggene)
er lisensiert under Creative Commons Attribution-ShareAlike 4.0 International; se [`LICENSES/CC-BY-SA-4.0.txt`](LICENSES/CC-BY-SA-4.0.txt).

Kårt sakt: ta hva du vill, gi navngitt kreditering, gi tilbake på samme vis. (Open-Source)

(Notat fra Meg Selv: personlig, såvidt jeg bryr meg, hvis du vil dele dette personlig/privat med hvem som helst, ingen begrensning, trengs ingen kreditt heller selvfølgelig.. :p det er egentlig bare hvis du poster/lager om TT og/eller re-publiserer det på nytt et sted at jeg helst vil ha kreditt der kreditt er fortjent, takk for din tid <3 TT <3)

## Hva TT er

Med det første innleggets egne ord:

> TT er en metode under utvikling for at mennesker og KI-systemer skal kunne undersøke, lage, rette og dele arbeid sammen. Dens filosofiske og sosiale navn er Primærdirektivene.

> The three tenets (de tre trådene):
>
> 1. «Gjør mot andre, slik du ønsker det gjort mot deg selv», sett fra mer enn én tings ståsted, og i enhver bokstavelig, semantisk og filosofisk betydning.
> 2. Sammenheng.
> 3. Bevissthet/oppmerksomhet + bevaring/bevarelse.

> Hvor virksomt, nytt og innflytelsesrikt det er, er åpne spørsmål. … Uavhengige tester, moteksempler og rettelser er velkomne.

Vil du melde fra om noe, åpner du en sak her: GitHub tilbyr TTs skjemaer for saker og feil.

## Les innleggene

| Innlegg | Dato | PDF |
|---|---|---|
| TT: en levende metode for å holde mennesker, systemer og bevis forbundet. | 27. september 2026 | [PDF](public/no/TT-first-post-NO.pdf) |
| Andre innlegg: to av TTs egne systemer, levert nakne, så du kan kjøre dem. | 5. oktober 2026 | [PDF](public/no/second-post/TT-second-post-NO.pdf) |
| Tredje innlegg: de tre trådene i et liv, og hva det ser ut til å koste å komme bort fra dem. | 7. oktober 2026 | [PDF](public/no/third-post/TT-third-post-NO.pdf) |
| Fjerde innlegg: to belegg for den første grunnsetningen. | 8. oktober 2026 | [PDF](public/no/fourth-post/TT-fourth-post-NO.pdf) |
| Femte innlegg: Dantes Inferno, lest gjennom de tre grunnsetningene. | 15. oktober 2026 | [PDF](public/no/fifth-post/TT-5-dantes-inferno-NO.pdf) |
| Sjette innlegg: den religiøse forbindelsen. | 15. oktober 2026 | [PDF](public/no/sixth-post/TT-6-den-religiose-forbindelsen-NO.pdf) |

Hvert innlegg er også en HTML-side i [`public/`](public/); [`serve.py`](serve.py) viser dem på din egen datamaskin.

Hver norsk utgave har en egen del om hvordan den ble oversatt.

## Maler

To av systemene TT bygger på, levert nakne så hvem som helst kan kopiere og kjøre dem. Begge er ren Python uten noe å installere; hver mappe har sin egen README, en sjekker med selvtest og et valgfritt lag med gjennomarbeidede eksempler, holdt adskilt fra de nakne filene.

- [templates/dictionary/](templates/dictionary/): ett ordforråd holdt fra tre sider (menneskelig, formell, matematisk), én regel (et ord er bekreftet først når eieren har sagt det rett ut), og `check_dictionary.py`, som beviser at filene er riktig formet og skriver ut én kontrollsum to personer kan sammenligne. Det valgfrie laget er et filtrert utdrag av TTs egen ordbok.
- [templates/issue-error-tracking/](templates/issue-error-tracking/): saker, observerte feil, utbedringsforsøk og endringer i registeret holdt som hver sin post, en vektet prioritering med dimensjonene i det åpne, og `track.py`, som kontrollerer en logg og bygger lokale eller offentlige rapporter. Skjemaer på engelsk og norsk (`ISSUE-RECORD.md`, `ERROR-RECORD.md`, `RAPPORTSKJEMA-NO.md`), retningslinjene for rapportering (`ISSUE-POLICY.md`, `FEIL-OG-SAKSPOLITIKK-NO.md`), og et oppdiktet eksempel i `optional/`.

## Matrisen i korte trekk

### Claude-sidens register

Alle problemer som dukket opp mens TT ble brukt fra dag til dag, sortert etter hvor de kom fra. Talt 10. oktober 2026: 481 problemer ført opp siden 18. september 2026, 345 fortsatt åpne eller under oppsyn, 132 fikset, og 35 glipper til som sjekkene fanget før de slapp gjennom. Hele oversikten, med hver gruppe av samme slag på én linje og datoen den først ble bekreftet, ligger på engelsk i [docs/matrix-by-category-EN.md](docs/matrix-by-category-EN.md).

| Hvor det kom fra | Ført opp | Fortsatt åpne | Fikset | Først bekreftet |
|---|---|---|---|---|
| Forbindelser og sikkerhetssperrer (broer, tillegg, filtre, opplasting) | 160 | 107 | 52 | 18. september 2026 |
| Vertsappen (Claude Cowork: økter, komprimering, modellbytte) | 125 | 102 | 22 | 18. september 2026 |
| Hjemmelagde verktøy og sjekkere | 86 | 55 | 30 | 18. september 2026 |
| Arbeidsregler og prosjekter | 40 | 28 | 11 | 18. september 2026 |
| Codex-siden (OpenAIs Codex, over broen) | 35 | 25 | 10 | 18. september 2026 |
| KI-ens egen tenkning | 29 | 24 | 5 | 18. september 2026 |
| Offisiell dokumentasjon mot den faktiske appen | 6 | 4 | 2 | 18. september 2026 |

En dato for første bekreftelse er det tidligste registeret kan vise, ikke bevis for første gang problemet oppsto.

### Codex-postene: et eget omfang

Matrisen over beskriver Claude-sidens register. Codex-postene holdes i egne filer og egne oppføringer: [Codex-matrisen i oversikt](docs/codex-matrix-overview-EN.md) (på engelsk).

Codex-katalogen har **287 katalogoverskrifter**: **195 eldre familier definert av kildene**, som bevarer **708 kilderader**, pluss **92 senere oppføringer**.

Etter kategori, talt 10. oktober 2026:

| Kategori | Katalogoverskrifter | Eldre familier | Senere tillegg |
|---|---:|---:|---:|
| Vert og app | 25 | 18 | 7 |
| Sky og transport | 4 | 2 | 2 |
| Kjøreverktøy | 158 | 104 | 54 |
| Kontekst og kontinuitet | 19 | 5 | 14 |
| Arbeidsflyt og myndighet | 33 | 31 | 2 |
| Modell- og verktøybruk | 8 | 1 | 7 |
| Dokumentasjon og tilstand | 31 | 26 | 5 |
| Prosjekt og innhold | 9 | 8 | 1 |
| **Totalt** | **287** | **195** | **92** |

Bekreftede, oppdaterte tall for åpne eller fiksede problemer er ennå ikke fastsatt for denne katalogen.

Disse tallene bruker ulike enheter: katalogoverskrifter, kilderader og senere oppføringer. Hvor mye de overlapper med hverandre og med Claude-sidens register, er uavklart. De gir ikke uavhengig bekreftede antall hendelser, og det finnes ingen samlet sum.

**Hvorfor sammenslåingen venter:** Dette arbeidet er finansiert gjennom private abonnementer. Intensivt arbeid med de fremste modellene, gjenoppretting og dokumentasjon bruker alt av abonnementenes bruksgrenser. 10. oktober 2026 meldte vedlikeholderen at et 5× Codex-abonnement pluss én nullstilling av bruksgrensen samme uke fortsatt ikke hadde dekket en full arbeidsuke. Et 20× Claude-abonnement hadde nådd 99 % av sin samlede ukegrense omtrent 12–24 timer før neste nullstilling. Sammenslåingen venter på nok brukskapasitet til å gå gjennom begge katalogene samlet; abonnementskostnadene setter også grenser for dette privatfinansierte arbeidet.

Sammenslåingen kommer etter en senere avstemming av opphav, telleenheter og overlappende poster. Til det arbeidet er ferdig, bevarer de separate katalogene sine egne belegg og sitt eget omfang.

## Hva som ligger i dette kodelageret

| Sti | Hva det er |
|---|---|
| [`public/`](public/) | Nettstedet: ren HTML, CSS og litt JavaScript, uten byggetrinn og uten noe å installere. Hvert innlegg er en side og en PDF; hver oversettelse ligger i sin egen mappe, som [`public/no/`](public/no/), og hver PDF som lenkes her, har språket sitt i navnet (`-EN`, `-NO`). |
| [`templates/`](templates/) | Noen av systemene TT bygger på, levert nakne (se Maler). |
| [`docs/`](docs/) | Dokumentasjon: matrisen, hvert problem som dukket opp mens TT ble brukt, sortert etter hvor det kom fra (se Matrisen i korte trekk). |
| [`tools/`](tools/) | `prepush_check.py`: kjørt før en opplasting lister den opp hver tilføyde linje som ser prosjektintern ut, og hvert tall i løpende tekst, så et menneske kan sjekke dem. |
| [`.github/`](.github/) | Skjemaene for saks- og feilrapporter som GitHub tilbyr når en sak åpnes her, og en arbeidsflyt, kjørt for hånd, som publiserer utvalgte filer som en Release med et sha256-manifest. |
| [`serve.py`](serve.py) | Viser [`public/`](public/) på din egen datamaskin og laster en åpen side på nytt når en fil lagres; ingenting utenfor datamaskinen din kan nå den. |
| [`wrangler.jsonc`](wrangler.jsonc) | Innstillingene for å vise [`public/`](public/) med Cloudflare Workers. |
| [`LICENSE`](LICENSE) | GNU Affero General Public License, version 3, for koden. |
| [`LICENSES/`](LICENSES/) | [`CC-BY-SA-4.0.txt`](LICENSES/CC-BY-SA-4.0.txt), for teksten. |

## Historikk

Hver endring er en git-commit, så nettstedets historikk er sin egen journal.
