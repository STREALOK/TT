# Issue ledger (local/private)

Reviewer attestations are recorded evidence, not authenticated authority.

Records: 3; error observation records: 1; observed occurrences: 1; unknown-count records: 0.
Trial tool/log events and manual transitions are separate from error occurrences. Audit coverage depends on supplied transition records.

Warning: ISS-example: unscored; missing impact, reach, recurrence, persistence, reversibility

## ISS-example

Status: open; classification: unknown; fix: none; weight: unscored.

> Example: record an observation

Owner:
> unassigned

Observed:
> Replace with a bounded observation\.

Expected:
> Replace with the expected behavior\.

First observed: None; earliest located: None; origin: unknown.
Fixed at: None; updated at: 2026-10-05T00:00:00Z; acceptance: none.
Confidence and verification cost: {"confidence": null, "verification_cost": {"level": "unknown", "estimate_minutes": null, "note": ""}}

Reproduction, cause, steps and hoped fix:
> \{"reproduction": \{"status": "unknown", "source": null\}, "cause": \{"status": "unknown", "description": null\}, "steps": \[\], "hoped\_fix": "To be investigated\.", "closed\_reason": null\}

Provenance:
> \[\]

Observation ERR-example:
> \{"revision": 1, "provenance": \[\], "issue\_id": "ISS\-example", "observed\_at": "2026\-10\-05T00:00:00Z", "recorded\_at": "2026\-10\-05T00:00:00Z", "count\_basis": "observed", "count\_source": "Fictional fixture, not workspace evidence\.", "window\_start": "2026\-10\-05T00:00:00Z", "window\_end": "2026\-10\-05T00:00:00Z", "type": "error", "id": "ERR\-example", "signature": "fictional\-example", "dedupe\_key": "fictional\-example\-v1", "grouping\_version": "example\-v1", "expectation": "unexpected", "transience": "unknown", "evidence": \["fictional://example"\], "occurrence\_count": 1\}

Observation TRY-example:
> \{"revision": 1, "provenance": \[\], "issue\_id": "ISS\-example", "observed\_at": "2026\-10\-05T00:00:00Z", "recorded\_at": "2026\-10\-05T00:00:00Z", "count\_basis": "observed", "count\_source": "Fictional fixture, not workspace evidence\.", "window\_start": "2026\-10\-05T00:00:00Z", "window\_end": "2026\-10\-05T00:00:00Z", "type": "trial", "id": "TRY\-example", "method": "Fictional synthetic check\.", "environment": "Fictional fixture\.", "duration\_seconds": null, "outcome": "pass", "result\_scope": "synthetic\-fixture", "use\_mode": "synthetic", "events\_observed": 0, "event\_kind": "behavior", "exposures": 1, "issue\_revision": 1, "artifact": \{"ref": "fictional://fixture", "sha256": null, "version": "fixture\-v1"\}, "scenario": "Fictional neutral test scenario\."\}
