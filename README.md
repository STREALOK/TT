# TT — the Three Tree Tenets

[Norsk](#norsk)

This repository holds TT's site: the posts as pages and PDFs, some of the systems TT runs on as templates, and the small tools that keep them in order.

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

Each post is also an HTML page in `public/`; `serve.py` shows them on your own computer.

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
| [`public/`](public/) | The site: plain HTML, CSS and a little JavaScript, no build step and nothing to install. Every post is a page and a PDF; each translation sits in its own folder, such as `public/no/`, and each PDF linked here carries its language in its name (`-EN`, `-NO`). |
| [`templates/`](templates/) | Some of the systems TT runs on, shipped bare (see Templates). |
| [`docs/`](docs/) | Documentation: the matrix, every problem met while running TT, sorted by where it came from (see The matrix at a glance). |
| [`tools/`](tools/) | `prepush_check.py`: run before a push, it lists every added line that looks project-internal, and every number in prose, for a person to check. |
| [`.github/`](.github/) | The issue and error report forms GitHub offers when an issue is opened here, and a workflow, run by hand, that publishes chosen files as a Release with a sha256 manifest. |
| [`serve.py`](serve.py) | Serves `public/` on your own computer and reloads an open page when a file is saved; nothing outside your computer can reach it. |
| [`wrangler.jsonc`](wrangler.jsonc) | The settings for serving `public/` with Cloudflare Workers. |
| [`LICENSE`](LICENSE) | The GNU Affero General Public License, version 3, for the code. |
| [`LICENSES/`](LICENSES/) | `CC-BY-SA-4.0.txt`, for the writing. |

## History

Every change is a git commit, so the site's history is its own record.

## Licence

The code (the page structure, stylesheets, scripts and `serve.py`) is licensed under the GNU Affero General Public License, version 3; see `LICENSE`. The writing (the words on the pages and in the posts) is licensed under Creative Commons Attribution-ShareAlike 4.0 International; see `LICENSES/CC-BY-SA-4.0.txt`.

In short: take anything, give credit, give back the same way.

## Norsk

Med det første innleggets egne ord:

> TT er en metode under utvikling for at mennesker og KI-systemer skal kunne undersøke, lage, rette og dele arbeid sammen. Dens filosofiske og sosiale navn er Primærdirektivene.

> The three tenets (de tre trådene):
>
> 1. «Gjør mot andre, slik du ønsker det gjort mot deg selv», sett fra mer enn én tings ståsted, og i enhver bokstavelig, semantisk og filosofisk betydning.
> 2. Sammenheng.
> 3. Bevissthet/oppmerksomhet + bevaring/bevarelse.

> Hvor virksomt, nytt og innflytelsesrikt det er, er åpne spørsmål. … Uavhengige tester, moteksempler og rettelser er velkomne.

### Les innleggene

| Innlegg | Dato | PDF |
|---|---|---|
| TT: en levende metode for å holde mennesker, systemer og bevis forbundet. | 27. september 2026 | [PDF](public/no/TT-first-post-NO.pdf) |
| Andre innlegg: to av TTs egne systemer, levert nakne, så du kan kjøre dem. | 5. oktober 2026 | [PDF](public/no/second-post/TT-second-post-NO.pdf) |
| Tredje innlegg: de tre trådene i et liv, og hva det ser ut til å koste å komme bort fra dem. | 7. oktober 2026 | [PDF](public/no/third-post/TT-third-post-NO.pdf) |
| Fjerde innlegg: to belegg for den første grunnsetningen. | 8. oktober 2026 | [PDF](public/no/fourth-post/TT-fourth-post-NO.pdf) |

Hver norsk utgave har en egen del om hvordan den ble oversatt.

### Maler

To av systemene TT bygger på, levert nakne så hvem som helst kan kopiere og kjøre dem; hver mappe har sin egen README, en sjekker med selvtest og et valgfritt lag med eksempler holdt adskilt fra de nakne filene. [Ordboken](templates/dictionary/): ett ordforråd fra tre sider, én regel (et ord er bekreftet først når eieren har sagt det rett ut). [Feil- og sakssporing](templates/issue-error-tracking/): saker, observerte feil, utbedringsforsøk og endringer som hver sin post, en vektet prioritering med dimensjonene i det åpne, og skjemaer og retningslinjer på norsk.

### Matrisen i korte trekk

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
