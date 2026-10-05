# Dictionary template — three views of one vocabulary, and a checker anyone can run

This is the bare template of the dictionary TT keeps for itself: three small files that hold one vocabulary from
three sides, and one script that proves the files are well formed. It ships empty but for examples. Copy the folder,
replace the examples with your own terms, run the checker, and you have a dictionary that cannot silently drift.

## The one rule

A term is **Confirmed** only when its owner has stated its meaning plainly, in their own words, and that statement is
on the entry. Until then it is **Unresolved**: a meaning someone inferred, written down so it can be checked, never
promoted by habit. The checker refuses a Confirmed term that has no owner statement.

## The three files

| file | what it holds | what every entry must carry |
|---|---|---|
| `HUMAN.md` | the words people use, as they use them | `owner` (the statement, as said) for a Confirmed term |
| `FORMAL.md` | the words a tool or a rule gives a fixed meaning to | `where` (what executes the meaning) |
| `MATH.md` | the words with a number or a test behind them | `measure` (how it is counted or tested) |

All three share one line grammar, so one checker reads them all:

```
- **term** (aka: alias, alias) [Confirmed] — one-line meaning
  - owner: the owner's own words, as said
  - crosswalk: other-term — how the two differ
```

The separator after the status is an em dash (—). A line that looks like an entry and does not parse is an error,
not a warning: a dictionary with one unreadable entry is a dictionary you cannot trust.

## Look-alikes

Two terms can share an outward shape (the same act, the same first letters, the same sound) and mean different things
underneath. The template calls those a **look-alike pair** and keeps them apart with a `crosswalk` field on each side
that names the other and says how they differ. The checker flags a pair of entries whose names share a stem but carry
no crosswalk, so the difference is written down before someone assumes it away.

## The checker

```
python3 check_dictionary.py            # checks HUMAN.md, FORMAL.md and MATH.md beside it
python3 check_dictionary.py --digest   # one short digest of the whole dictionary
python3 check_dictionary.py --selftest
```

What it proves: every entry parses; no term or alias is declared twice across the three files; every Confirmed term
has its owner statement; every Formal entry says where it executes and every Math entry how it is measured; every
look-alike pair has its crosswalk; and a digest, so two people can confirm in one line that they hold the same
dictionary. What it cannot prove: that a meaning is true. That is the owner's, and only the owner's.

`EXPECTED-OUTPUT.txt` beside this file is what the checker prints on this template as shipped. Run it and compare.

## The optional layer

`optional/TT-COLLECTED.md` is not part of the template. It is a short, screened extract of TT's own dictionary, in the
same grammar, so you can see the template carrying real terms. Three of its entries (working map, handoff, dropoff) are
the same terms the bare template uses as examples, on purpose, so you can hold the example and the real entry side by
side; that is also why the checker reads it on its own (`--only optional/TT-COLLECTED.md`) and would rightly refuse the
duplicates if you loaded both. Delete it, or keep it as a worked example.

Plain Python, nothing to install. Licence: AGPL-3.0 for the code, CC BY-SA 4.0 for the text, as the rest of this repo.
