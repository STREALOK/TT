# Weighted triage
Model: TT-compatible weighted-issue/1.
W = 3 × impact + 2 × reach + 2 × recurrence + persistence + 2 × reversibility.

Dimensions are integers 1–5 or null. The fully scored range is 10–50.
A missing dimension leaves the score unscored; a boolean is invalid.
Confidence and verification cost are separate. No priority bands are imposed.

The compatibility field reversibility means rollback difficulty: higher
means harder to undo. Always explain this alongside the score.

| Dimension | 1 | 3 | 5 |
|---|---|---|---|
| Impact | Contained inconvenience | Material interruption | Severe or durable loss |
| Reach | One bounded case | Several operations/people | Many connected systems/people |
| Recurrence | One case in a stated window | Repeated in a stated window | Frequent in a stated window |
| Persistence | Clears within the attempt | Persists until intervention | Persists across attempts/sessions |
| Rollback difficulty | Readily reversible | Restoration costs effort | Restoration very difficult/unavailable |

Values 2/4 express documented intermediate judgements. These are proposed
reusable anchors, not retrospective grades for live issues. Record the basis,
observation window, coverage and any denominator.

Updates, retries and copied reports are not automatically new occurrences.
A report of 8–12 windows is a human range, not twelve measured process events.
Unknown is not zero or 1. A legacy score using defaults can be retained only
as a visibly provisional value with every imputed dimension listed.

