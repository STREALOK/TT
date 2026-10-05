# TT — the Three Tree Tenets

This repository holds the TT site: plain HTML and CSS in `public/`, with no build step and nothing to install.

## Where it lives

The site is served by Cloudflare Workers, and `wrangler.jsonc` holds its settings. Its public address comes later; until then, the first post can be read here as a PDF: [public/TT-first-post.pdf](public/TT-first-post.pdf).

The Norwegian edition («norsk utgave») lives beside it: the page [public/no/index.html](public/no/index.html), and the same four parts as one PDF, [public/no/TT-first-post.pdf](public/no/TT-first-post.pdf).

## Templates

Two of the systems TT runs on, shipped bare so anyone can copy and run them. Both are plain Python with nothing to install; each folder has its own README, a checker with a self-test, and an optional layer of worked examples kept apart from the bare files.

- [templates/dictionary/](templates/dictionary/): one vocabulary kept from three sides (human, formal, mathematical), one rule (a term is Confirmed only when its owner has stated it plainly), and `check_dictionary.py`, which proves the files are well formed and prints one digest two people can compare. The optional layer is a screened extract of TT's own dictionary.
- [templates/issue-error-tracking/](templates/issue-error-tracking/): issues, observed errors, fix trials and record changes kept as separate records, a weighted triage score with its dimensions in the open, and `track.py`, which validates a ledger and builds local or public reports. English and Norwegian forms (`ISSUE-RECORD.md`, `ERROR-RECORD.md`, `RAPPORTSKJEMA-NO.md`), the reporting policy (`ISSUE-POLICY.md`, `FEIL-OG-SAKSPOLITIKK-NO.md`), and a fictional example in `optional/`.

Norsk: to av systemene TT bygger på, levert nakne så hvem som helst kan kopiere og kjøre dem; hver mappe har sin egen README, en sjekker med selvtest, og et valgfritt lag med eksempler holdt adskilt fra de nakne filene. Ordboken: ett ordforråd fra tre sider, én regel (et ord er bekreftet først når eieren har sagt det rett ut). Feil- og sakssporing: saker, observerte feil, utbedringsforsøk og endringer som hver sin post, en vektet prioritering med dimensjonene i det åpne, og skjemaer og retningslinjer på norsk.

The issue forms also sit under `.github/ISSUE_TEMPLATE/`, so a report opened here starts on them.

## History

Every change is a git commit, so the site's history is its own record.

## Licence

The code (the page structure, stylesheets, scripts and `serve.py`) is licensed under the GNU Affero General Public License v3.0; see `LICENSE`. The writing (the words on the pages and in the posts) is licensed under Creative Commons Attribution-ShareAlike 4.0 International; see `LICENSES/CC-BY-SA-4.0.txt`.

In short: take anything, give credit, give back the same way.
