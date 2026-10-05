# Issue and error tracking template
Version 0.1 candidate, prepared 5 October 2026 for TT First Post.

An empty reusable tracking system, a local checker/report builder, report forms,
and optional fictional examples. Issues, observed errors, fix trials and record
changes are separate. Nothing imports private records or publishes a site.

Python 3.12+, standard library only. From this folder:
~~~text
python track.py init ledger.jsonl
python track.py check ledger.jsonl
python track.py score ledger.jsonl
python track.py digest ledger.jsonl
python track.py report ledger.jsonl
python -m unittest -v test_track.py
~~~
Initialization creates one empty ledger file; its parent must already exist.
It refuses an existing destination. Prepare records explicitly,
retain a previous baseline, and validate before rendering:
~~~text
python track.py check ledger.jsonl --baseline previous.jsonl
python track.py report ledger.jsonl --public --output approved-report.md
~~~
Public report generation writes a local file. It requires current recorded
screening, which is evidence of review, not authenticated human authority.

## Files
SCHEMA.md gives exact fields and CLI. ISSUE-RECORD.md and ERROR-RECORD.md are
complete English forms; RAPPORTSKJEMA-NO.md supplies Norwegian forms.
SCORING.md, WORKFLOW.md and PUBLICATION-SCREENING.md explain the lifecycle.
FIRST-POST-EN.md and FIRST-POST-NO.md are prepared explanatory copy.
optional/ holds only fictional examples. tests/ holds root's actual test
results and sample reports once verified.

For this template, ledger.jsonl is the chosen structured source; reports are
derived. Use one writer and retained baselines. This version supplies validation
and reporting; editing records is explicit. It installs no global error hook,
automatic observer or deployment service.

This template is the reusable system on its own. A project that already keeps
an issue register maps its fields onto this ledger explicitly, or leaves them
unknown; nothing here replaces an existing record.

Full open reports retain origin and evidence. Lighter fixed-public reports
omit quotes and absolute origin pointers, retaining fix trials, validation
scope, uncertainty and reopening conditions.

Checks establish declared structure and consistency in selected files. They
do not prove complete history, true cause, total incident counts, human
authority, semantic reading, live operation or publication.

License: SPDX AGPL-3.0-only, matching the planned TT template release.
Carry the site's existing LICENSE into the adopted release folder.

