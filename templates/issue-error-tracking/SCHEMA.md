# JSONL schema and command reference
Template format version 1, bundled with track.py 0.1 candidate.
One UTF-8 JSON object per nonblank line. Exact fields are required: unknown
keys, duplicate keys, malformed rows and nonfinite numbers are refused.

Limits: 1 MiB per selected file, 1,000 records, 4,096 characters per text value.
IDs are unique across the file: ISS-, ERR-, TRY- or CHG-, followed by a bounded
letter/digit/underscore/hyphen identifier. Revisions are positive integers.
Times are UTC YYYY-MM-DDTHH:MM:SSZ; calendar validity is checked. Unknown
observation time is null. Import/record time must not replace it.

## Common fields
Every record has type, id, revision, provenance, screening.
provenance is a list of objects with exactly:
- ref: bounded text; sha256: lowercase SHA-256 or null
- rights: owned / licensed / permission / restricted / unknown
- redaction: none / partial / complete / unknown
- public_excerpt: bounded text or null
- privacy_flags: bounded list of declared flags

screening has status (pending/approved/rejected), reviewer (text/null),
date (YYYY-MM-DD/null), revision (integer/null), text_digest (SHA-256/null).
Approved requires all fields. A current decision must match the record revision
and computed payload digest. Issue digests include the payload of every linked
error, trial and change record, sorted by ID. Screening metadata itself is
excluded to avoid circular hashing. Every linked record needs its own current
decision for the issue to qualify for public export.

A changed declared source hash invalidates screening; the checker does not
open the reference to authenticate its current bytes or rights.

## Issue (type issue)
Required additional fields:
~~~text
title, owner, kind, system_side, status, classification, fix_state,
created_at, updated_at, first_observed, earliest_located, origin, fixed_at,
closed_reason, supersedes, observed, expected, steps, reproduction, cause,
hoped_fix, acceptance_scope, confidence, verification_cost, weights,
public_summary
~~~
- kind: issue/error/suspicion/process/documentation
- system_side: root_app/cloud/model/mechanical/human/workflow/documentation
- status: open/fixed/wontfix/superseded/monitoring
- classification: confirmed/repaired/suspicion/unknown
- fix_state: none/proposed/applied/synthetic-pass/live-verified
- origin: unknown/proven; proven requires declared provenance
- acceptance_scope: none/synthetic/in-use/document
- first_observed, earliest_located, fixed_at: UTC or null
- closed_reason and public_summary: text or null
- supersedes: prior issue ID or null; a superseded issue needs a successor,
  and cycles are refused
- steps: bounded text list
- reproduction: exactly status (reproduced/not-reproduced/unknown), source(text/null)
- cause: exactly status (proven/suspected/unknown), description(text/null)
- confidence: finite 0–1 or null; this is a declared template scale
- verification_cost: level(low/medium/high/unknown), estimate_minutes(number/null), note
- weights: impact,reach,recurrence,persistence,reversibility, each integer1–5/null

Fixed requires explicit time, reason, applied fix and matching acceptance
trial. Live-verified requires current passing in-use evidence. Do not map
legacy confidence values into a new scale without a recorded interpretation.

## Error observation (type error)
Required additional fields:
~~~text
issue_id, observed_at, recorded_at, signature, dedupe_key, grouping_version,
expectation, transience, evidence, occurrence_count, count_basis, count_source,
window_start, window_end
~~~
issue_id is a valid issue ID or null. expectation is expected/unexpected/unknown;
transience is transient/persistent/unknown. evidence is a bounded text list.
occurrence_count is integer>=1 or null; count_basis is observed/unknown.
Known counts require count_source and both ordered UTC window endpoints.
Unknown counts remain null, not zero. recorded_at is required; observed_at
can be null. Deduplication uses the declared grouping-version/key pair.

## Fix trial (type trial)
Required additional fields:
~~~text
issue_id, issue_revision, artifact, scenario, observed_at, recorded_at,
method, environment, duration_seconds, outcome, result_scope, use_mode,
events_observed, event_kind, exposures, count_basis, count_source,
window_start, window_end
~~~
- artifact: exactly ref,sha256,version; each can be null for an unverified trial
- outcome: pass/fail/inconclusive
- use_mode/result_scope: synthetic/synthetic-fixture,
  in-use/in-use-observation, document/document-review
- event_kind: behavior/tool/log/unknown
- duration_seconds: nonnegative finite number or null
- events_observed and exposures: nonnegative integers or null

Verification claims need the current issue revision, an observed time,
known artifact reference plus hash/version, and the latest passing trial
for the claimed mode before the relevant update/closure time. Old trials
remain historical evidence. A new issue revision does not reuse them.
For behavior-event counts, events cannot exceed known exposures.
Tool/log counts remain separate from error occurrences.

## Manual change record (type transition)
Required additional fields:
~~~text
issue_id, recorded_at, field, before, after, reason
~~~
field is status/fix_state/classification/revision, with valid before/after
values. Revision changes increase. Supplied chains must be continuous and
end at the current issue snapshot. Changes are not automatically discovered.
Audit coverage is exactly the history supplied, not a complete hidden journal.

## Commands
init FILE creates a new empty ledger; parent must already exist and an
existing file is refused. example prints a blank issue record; example
--bundle adds fictional error/trial records. check FILE validates; optional
--baseline FILE also rejects deletion or payload modification of old error,
trial and change records, and issue edits without an increased revision.
score FILE reports weights/unknowns; digest FILE prints review digests.
report FILE creates local/private Markdown; --public selects currently
screened issues and rejects blocked linked provenance. --output FILE refuses
an existing destination. No command commits, pushes, scans history or runs
a target application.

The renderer quotes supplied text as inert Markdown. Public output selects
the newly authored public_summary and permitted excerpts; it does not print
private owner/title/steps/origin. Fixed issue excerpts are omitted. Human
review of public_summary is still necessary; quotation/origin omission cannot
be inferred from its semantic content by this tool.

