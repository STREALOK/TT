#!/usr/bin/env python3
"""check_dictionary.py - prove a three-file dictionary is well formed, and print one digest for it.

Reads HUMAN.md, FORMAL.md and MATH.md from the folder it sits in (or --dir), each written in one grammar:

    - **term** (aka: alias, alias) [Confirmed|Unresolved] — one-line meaning
      - field: value

What it checks (each failure is listed; exit code 1 if any):
  1. every line that looks like an entry parses (the separator is an em dash);
  2. no term or alias is declared twice across the three files;
  3. a Confirmed term carries an `owner` statement (the one rule);
  4. a FORMAL entry carries `where`; a MATH entry carries `measure`;
  5. a look-alike pair (two entries whose names share a stem) carries a `crosswalk` on both sides.

What it cannot check: that a meaning is true. That is the owner's.

    python3 check_dictionary.py                       # check the three files beside this script
    python3 check_dictionary.py --digest              # the digest only
    python3 check_dictionary.py --with extra.md         # also read an extra file in the same grammar, with the three
    python3 check_dictionary.py --only optional/TT-COLLECTED.md   # check one file on its own (the optional layer
                                                        #   repeats three of the template's examples on purpose)
    python3 check_dictionary.py --selftest

Plain Python 3.8+, standard library only. Licence: AGPL-3.0-only.
"""
import hashlib
import os
import re
import sys

FILES = (("H", "HUMAN.md"), ("F", "FORMAL.md"), ("M", "MATH.md"))
LINE = re.compile(r"^- \*\*(.+?)\*\*(?:\s*\(aka:\s*(.*?)\))?\s*\[(Confirmed|Unresolved)\]\s*—\s*(.*)$")
LOOKS_LIKE = re.compile(r"^- \*\*")
FIELD = re.compile(r"^\s{2,}- ([A-Za-z][\w -]*?):\s*(.*)$")
REQUIRED = {"F": "where", "M": "measure"}


def read(path, letter):
    """Entries of one file: dicts with term, aliases, status, meaning, fields, file, line; plus a list of errors."""
    entries, errors = [], []
    cur = None
    try:
        lines = open(path, encoding="utf-8").read().splitlines()
    except OSError as exc:
        return [], [f"{os.path.basename(path)}: cannot read ({exc.__class__.__name__})"]
    for n, raw in enumerate(lines, 1):
        m = LINE.match(raw)
        if m:
            cur = {"term": m.group(1).strip(), "aliases": [a.strip() for a in (m.group(2) or "").split(",") if a.strip()],
                   "status": m.group(3), "meaning": m.group(4).strip(), "fields": {}, "file": letter, "line": n}
            entries.append(cur)
            continue
        if LOOKS_LIKE.match(raw):
            errors.append(f"{os.path.basename(path)}:{n}: looks like an entry and does not parse (is the separator an em dash?)")
            cur = None
            continue
        f = FIELD.match(raw)
        if f and cur is not None:
            cur["fields"][f.group(1).strip().lower()] = f.group(2).strip()
    return entries, errors


def stem(term):
    """A crude shared-stem key for look-alikes: the first five letters of the term, lower-cased, letters only."""
    return re.sub(r"[^a-z]", "", term.lower())[:5]


def check(entries, errors):
    problems = list(errors)
    seen = {}
    for e in entries:
        for key in [e["term"]] + e["aliases"]:
            k = key.lower()
            if k in seen:
                problems.append(f"{e['file']}:{e['line']}: '{key}' is already declared at {seen[k]}")
            else:
                seen[k] = f"{e['file']}:{e['line']}"
        if e["status"] == "Confirmed" and not e["fields"].get("owner"):
            problems.append(f"{e['file']}:{e['line']}: Confirmed '{e['term']}' has no owner statement")
        need = REQUIRED.get(e["file"])
        if need and not e["fields"].get(need):
            problems.append(f"{e['file']}:{e['line']}: '{e['term']}' lacks the '{need}' field its file requires")
    by_stem = {}
    for e in entries:
        by_stem.setdefault(stem(e["term"]), []).append(e)
    for group in by_stem.values():
        if len(group) < 2:
            continue
        for e in group:
            if not e["fields"].get("crosswalk"):
                others = ", ".join(x["term"] for x in group if x is not e)
                problems.append(f"{e['file']}:{e['line']}: '{e['term']}' looks like {others} and has no crosswalk")
    return problems


def digest(entries):
    norm = sorted(f"{e['file']}|{e['term'].lower()}|{e['status']}|{e['meaning']}" for e in entries)
    return hashlib.sha256("\n".join(norm).encode("utf-8")).hexdigest()[:16]


def run(folder, extra=(), only=None):
    entries, errors = [], []
    if only:
        es, errs = read(only if os.path.isabs(only) else os.path.join(folder, only), "X1")
        return es, check(es, errs)
    for letter, name in FILES:
        es, errs = read(os.path.join(folder, name), letter)
        entries += es
        errors += errs
    for i, path in enumerate(extra):
        es, errs = read(path if os.path.isabs(path) else os.path.join(folder, path), f"X{i + 1}")
        entries += es
        errors += errs
    return entries, check(entries, errors)


def selftest():
    import tempfile
    d = tempfile.mkdtemp()
    ok = 0
    good = ("- **alpha** (aka: a) [Confirmed] — first.\n  - owner: \"first\"\n"
            "- **beta** [Unresolved] — reading: second.\n")
    open(os.path.join(d, "HUMAN.md"), "w", encoding="utf-8").write(good)
    open(os.path.join(d, "FORMAL.md"), "w", encoding="utf-8").write("- **gamma** [Confirmed] — g.\n  - owner: \"g\"\n  - where: here\n")
    open(os.path.join(d, "MATH.md"), "w", encoding="utf-8").write("- **delta** [Confirmed] — d.\n  - owner: \"d\"\n  - measure: count\n")
    e, p = run(d)
    t = (len(e) == 4 and p == []); ok += t; print("1 a clean triple passes", t)
    d1 = digest(e)
    open(os.path.join(d, "HUMAN.md"), "a", encoding="utf-8").write("- **epsilon** [Confirmed] — no owner.\n")
    e, p = run(d); t = any("no owner statement" in x for x in p); ok += t; print("2 a Confirmed term without an owner is refused", t)
    open(os.path.join(d, "HUMAN.md"), "a", encoding="utf-8").write("- **a** [Unresolved] — clashes with alpha's alias.\n")
    e, p = run(d); t = any("already declared" in x for x in p); ok += t; print("3 a duplicate name or alias is refused", t)
    open(os.path.join(d, "HUMAN.md"), "a", encoding="utf-8").write("- **zeta** [Confirmed] - a hyphen, not an em dash.\n")
    e, p = run(d); t = any("does not parse" in x for x in p); ok += t; print("4 an unparsed entry is an error", t)
    open(os.path.join(d, "FORMAL.md"), "w", encoding="utf-8").write("- **gamma** [Confirmed] — g.\n  - owner: \"g\"\n")
    e, p = run(d); t = any("lacks the 'where'" in x for x in p); ok += t; print("5 a FORMAL entry without 'where' is flagged", t)
    open(os.path.join(d, "HUMAN.md"), "w", encoding="utf-8").write(good + "- **alphabet** [Confirmed] — looks like alpha.\n  - owner: \"x\"\n")
    open(os.path.join(d, "FORMAL.md"), "w", encoding="utf-8").write("- **gamma** [Confirmed] — g.\n  - owner: \"g\"\n  - where: here\n")
    e, p = run(d); t = any("has no crosswalk" in x for x in p); ok += t; print("6 a look-alike pair without a crosswalk is flagged", t)
    open(os.path.join(d, "HUMAN.md"), "w", encoding="utf-8").write(good)
    e, p = run(d); t = (digest(e) == d1); ok += t; print("7 the digest is stable for the same entries", t)
    print(f"check_dictionary selftest: {ok}/7")
    return 0 if ok == 7 else 1


def main(argv):
    if "--selftest" in argv:
        return selftest()
    folder = os.path.dirname(os.path.abspath(__file__))
    if "--dir" in argv:
        folder = argv[argv.index("--dir") + 1]
    extra = [argv[i + 1] for i, a in enumerate(argv) if a == "--with"]
    only = argv[argv.index("--only") + 1] if "--only" in argv else None
    entries, problems = run(folder, extra, only)
    if "--digest" in argv:
        print(digest(entries))
        return 0
    conf = sum(1 for e in entries if e["status"] == "Confirmed")
    files = (os.path.basename(only) if only else ", ".join(f"{n} {sum(1 for e in entries if e['file'] == l)}" for l, n in FILES)
             + (f", extra {sum(1 for e in entries if e['file'].startswith('X'))}" if extra else ""))
    print(f"dictionary: {len(entries)} entries ({files}); confirmed {conf}/{len(entries)}; digest {digest(entries)}")
    for p in problems:
        print("  PROBLEM " + p)
    print("OK: every entry parses, no duplicates, every Confirmed term has its owner, every look-alike has its crosswalk"
          if not problems else f"FAILED: {len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
