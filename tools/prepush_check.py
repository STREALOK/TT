#!/usr/bin/env python3
"""prepush_check.py - read what is about to go public the way a stranger would, before it goes.

Run from the repository root before a push. It takes every line ADDED by the commits that are not yet on the
remote (origin/main..main; or every commit, when there is no remote yet) and reports two kinds of thing:

  STOP   a line that carries something project-internal: an internal identifier pattern, a machine path, a
         drive letter, a phrase about "this computer" or "this folder", or any term listed in the local marker
         file (see below). The check exits 1 and the push script stops. Nothing is sent.
  NUMBER a number in prose (a digit group of two or more, or a number word such as dozen, thirty, hundred, a
         "seventy-odd") in an added line of a text page, with no count note on the same line. These are listed,
         not refused: the person pushing reads the list and confirms each number is a counted one, not a guess.
         A line that says how the number was obtained ("counted on", "talt", "measured", "as of") is not listed.

Local marker file (never committed; add it to .gitignore): tools/prepush-markers.local.txt, one term or regular
expression per line, lines starting with # ignored. Optional mask module: if the environment variable
TT_PREPUSH_MASK_DIR names a folder holding a Python module `ns2` with a function mask(text) -> text, every added
line is passed through it, and a line the mask changes is a STOP. Both let a project keep its private names out
of this public file.

    python prepush_check.py                 # check the pending commits
    python prepush_check.py --files a.md b  # check whole files instead
    python prepush_check.py --selftest

Plain Python 3.8+, standard library only. Licence: AGPL-3.0-only.
"""
import os
import re
import subprocess
import sys

INTERNAL = [
    (r"\b[A-Z]{2,4}-20\d{6}-\d{3}\b", "dated internal id"),
    (r"\b(?:KT|LES|ISS|NUG|INC)-\d{2,3}\b", "internal id"),
    (r"\bT-\d{4}\b", "trail id"),
    (r"\b[A-Z]:\\", "drive path"),
    (r"\\Users\\|/Users/|/home/\w+/|/sessions/", "machine path"),
    (r"\bthis (?:computer|machine|folder|PC)\b", "machine phrase"),
    (r"\b(?:worktrees?|\.codex|\.claude)\b", "tool folder"),
]
NUMBER_WORDS = r"(?:dozen|dozens|eleven|twelve|thirteen|fourteen|fifteen|sixteen|seventeen|eighteen|nineteen|twenty|thirty|forty|fifty|sixty|seventy|eighty|ninety|hundred|hundreds|thousand|thousands|million|tusen|hundre|dusin|elleve|tolv|tretten|fjorten|femten|seksten|sytten|atten|nitten|tjue|tretti|førti|femti|seksti|sytti|åtti|nitti)"
NUMBER_RX = re.compile(r"(?<![\w.\-/#])\d{2,}(?:[.,]\d+)?(?![\w.\-/%])|\b" + NUMBER_WORDS + r"(?:-\w+)?\b", re.I)
COUNTED_RX = re.compile(r"\b(?:counted|measured|as of|talt|målt|per \d)|\(\d{1,2} \w+ 20\d\d\)", re.I)
SKIP_NUMBER_RX = re.compile(r"\b(?:Part|Del|Page|Side) \d+ (?:of|av) \d+|\b(?:19|20)\d\d\b|\d+\.\d+\.\d+|\bv\d|CC BY-SA \d|AGPL-?\d|\d{1,2} (?:January|February|March|April|May|June|July|August|September|October|November|December|januar|februar|mars|april|mai|juni|juli|august|september|oktober|november|desember)\b", re.I)
TEXT_EXT = (".md", ".html", ".txt")
SELF = "tools/prepush_check.py"  # exempt from its own scan (6 Oct 2026: v8 stopped on its own selftest lines)


def load_markers(root):
    path = os.path.join(root, "tools", "prepush-markers.local.txt")
    out = []
    if os.path.exists(path):
        for ln in open(path, encoding="utf-8"):
            ln = ln.strip()
            if ln and not ln.startswith("#"):
                try:
                    out.append((re.compile(ln, re.I), "local marker"))
                except re.error:
                    out.append((re.compile(re.escape(ln), re.I), "local marker"))
    return out


def load_mask():
    d = os.environ.get("TT_PREPUSH_MASK_DIR")
    if not d:
        return None
    sys.path.insert(0, d)
    try:
        import ns2  # noqa: F401
        return ns2.mask
    except Exception:  # noqa: BLE001
        return None


def added_lines(root):
    """[(path, line)] for lines added by the pending commits (origin/main..main), or all commits if no remote."""
    env = dict(os.environ, GIT_OPTIONAL_LOCKS="0")
    def git(*a):
        return subprocess.run(["git", "-C", root] + list(a), capture_output=True, text=True, encoding="utf-8", errors="replace", env=env)
    rng = "origin/main..main" if git("rev-parse", "--verify", "--quiet", "origin/main").returncode == 0 else "main"
    r = git("diff", "--cached" if False else rng, "--unified=0", "--no-color", "--diff-filter=AM", "--", ".") if rng != "main" else git("show", "--unified=0", "--no-color", "--format=", "main")
    out, path = [], None
    for ln in r.stdout.splitlines():
        if ln.startswith("+++ b/"):
            path = ln[6:]
        elif ln.startswith("+") and not ln.startswith("+++") and path:
            out.append((path, ln[1:]))
    return out


def check(lines, markers=(), mask=None):
    stops, numbers = [], []
    pats = INTERNAL + list(markers)
    for path, ln in lines:
        if path.replace("\\", "/").endswith(SELF):
            continue  # the checker's own text is made of the things it stops on (patterns, selftest lines); it is read by hand, not by itself
        for rx, why in pats:
            rx = re.compile(rx, re.I) if isinstance(rx, str) else rx
            if rx.search(ln):
                stops.append((path, why, ln.strip()[:120]))
                break
        else:
            if mask and mask(ln) != ln:
                stops.append((path, "masked term", "(line withheld: it carries a private term)"))
        if path.lower().endswith(TEXT_EXT) and not COUNTED_RX.search(ln):
            plain = re.sub(r"<[^>]+>", " ", ln)
            plain = SKIP_NUMBER_RX.sub(" ", plain)
            if NUMBER_RX.search(plain):
                numbers.append((path, ln.strip()[:120]))
    return stops, numbers


def report(stops, numbers):
    for path, why, ln in stops:
        print(f"STOP   {path}: {why}: {ln}")
    for path, ln in numbers:
        print(f"NUMBER {path}: {ln}")
    if stops:
        print(f"\n{len(stops)} line(s) carry something internal. Nothing should be sent until they are fixed.")
    if numbers:
        print(f"\n{len(numbers)} line(s) carry a number in prose. Confirm each is counted, not guessed, before sending.")
    if not stops and not numbers:
        print("pre-send read: nothing internal, no uncounted numbers in the added lines.")
    return 1 if stops else 0


def selftest():
    ok = 0
    s, n = check([("a.md", "see NUG-20261005-001 for the record")]); ok += bool(s) and s[0][1] == "dated internal id"; print("1 internal id stops", bool(s))
    s, n = check([("a.md", "files live at C:\\TT\\public")]); ok += bool(s); print("2 drive path stops", bool(s))
    s, n = check([("a.md", "some thirty skills and well over a hundred scripts")]); ok += (not s and len(n) == 1); print("3 number words are listed", not s and len(n) == 1)
    s, n = check([("a.md", "twelve plugins, counted on 5 October 2026")]); ok += (not s and not n); print("4 a counted line is not listed", not s and not n)
    s, n = check([("a.md", "Part 2 of 3 · 5 October 2026 · CC BY-SA 4.0 · AGPL-3.0 · v2.3")]); ok += (not n); print("5 parts, dates, licences and versions are not numbers", not n)
    s, n = check([("a.py", "x = 12345")]); ok += (not n); print("6 code files are not scanned for numbers", not n)
    s, n = check([("a.md", "the secret word is pineapple")], markers=[(re.compile("pineapple"), "local marker")]); ok += bool(s); print("7 a local marker stops", bool(s))
    s, n = check([("a.md", "hello ship")], mask=lambda t: t.replace("ship", "[x]")); ok += bool(s) and "withheld" in s[0][2]; print("8 a masked term stops and is not echoed", bool(s))
    s, n = check([("tools/prepush_check.py", "files live at C:\\TT\\public")]); ok += (not s); print("9 the checker's own file is exempt", not s)
    print(f"prepush_check selftest: {ok}/9")
    return 0 if ok == 9 else 1


def main(argv):
    if "--selftest" in argv:
        return selftest()
    root = os.getcwd()
    if "--files" in argv:
        lines = []
        for f in argv[argv.index("--files") + 1:]:
            lines += [(f, ln.rstrip("\n")) for ln in open(f, encoding="utf-8", errors="replace")]
    else:
        lines = added_lines(root)
    stops, numbers = check(lines, load_markers(root), load_mask())
    return report(stops, numbers)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
