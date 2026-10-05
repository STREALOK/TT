# Error observation — empty form
An observation can link to an issue, or remain untriaged.

## Group and occurrence
- Safe signature, grouping-rule version and distinct-group criteria:
- Operation and expected outcome:
- Expectation: expected / unexpected / unknown:
- Transience: transient / persistent / unknown:
- Unique event ID, attempt/run reference and linked issue or none:
- Observed time or unknown; recorded time:
- Safe environment/version and bounded description:
- Outcome; evidence reference and scope:
- Deduplication key and count basis:
- Occurrences or unknown; window, exposures/attempts and coverage:
- Privacy, rights and screening:

Do not collect whole environment dumps or exception bodies by default.
Never fetch a reasoning transcript to complete an observation.

## Distinct totals
Error records count stored observations. Signature groups depend on the
declared normalization/version. Known occurrences sum measured counts only
after deduplication; report unknown-count records separately.
Issue records are problems; trials are checks; transition events are record
changes. Journal length or the word again is not an incident count.
Import date is not observation date.

## Change-event form
- Event ID, entity ID, recorded time and actor role:
- Changed field, prior value, new value:
- Reason/evidence and revision before/after:
- Effect on acceptance and screening:
- Linked new observation/trial, if any:

SCHEMA.md specifies executable transition fields and limits.
Existing external audit history remains separate during adoption.

