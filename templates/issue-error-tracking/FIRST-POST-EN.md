# Follow a problem from observation to tested repair
Keep issues, observed errors and fix trials as separate records. Record
expected behaviour, what happened, reproduction, possible causes and every
attempted fix. Keep unknowns visible.

A weighted score supports triage when its dimensions are recorded.
Confidence and verification cost stay separate. An update is not a new
incident. A synthetic pass does not establish a repair in actual use.

The Python checker validates the selected ledger's structure, references,
scores, declared test scope and recorded screening. The report builder makes
local reports. Neither proves complete history, true cause, semantic safety
or permission to publish.

~~~mermaid
flowchart TD
  A["Record an observation"] --> B["Triage the issue"]
  B --> C["Test each fix"]
  C --> D{"Acceptance scope met?"}
  D -->|Yes| E["Close or monitor with limits"]
  D -->|No or unknown| B
  E --> F["Review a safe public summary"]
  F --> G["Separate release check"]
~~~

Create an empty ledger, fill the forms and run check before rendering.
The optional example is fictional. Full open and lighter fixed reports keep
the same evidence boundaries.

Written 5 October 2026 for this repo's templates folder.

