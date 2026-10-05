# MATH — the words with a number or a test behind them

Same grammar. Every entry says how it is `measure`d, so a claim about the dictionary can be counted rather than argued.

- **digest** [Confirmed] — one short string computed from every entry of all three files; two people holding the same dictionary get the same digest.
  - owner: "a digest, so two people can confirm in one line that they hold the same dictionary" (this template's README)
  - measure: SHA-256 over the sorted, normalised entry lines of HUMAN.md, FORMAL.md and MATH.md, first 16 hex characters; `check_dictionary.py --digest`
- **confirmed ratio** [Confirmed] — the share of entries that are Confirmed, across the three files.
  - owner: "how much of the vocabulary its owners have actually stated" (this template's README)
  - measure: Confirmed entries divided by all entries; printed by the checker as `confirmed N/M`
