# FORMAL — the words a tool or a rule gives a fixed meaning to

Same grammar as HUMAN.md. Every entry says `where` its meaning executes (a script, a rule, a check), so the word can be
read against the thing that enforces it.

- **index line** (aka: entry line) [Confirmed] — the one-line grammar all three dictionaries share; a line that looks like an entry and does not parse is an error.
  - owner: "one grammar, one checker; an unreadable entry is an error, never a warning" (this template's README)
  - where: `check_dictionary.py` (the LINE pattern)
- **crosswalk** [Confirmed] — a field on each side of a look-alike pair that names the other term and says how the two differ.
  - owner: "keep look-alikes apart by writing the difference down on both sides" (this template's README)
  - where: `check_dictionary.py` (the look-alike check)
