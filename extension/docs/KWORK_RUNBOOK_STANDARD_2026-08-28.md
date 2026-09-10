# KWORK RUNBOOK STANDARD

Date: 2026-08-28
Updated: 2026-09-10
Status: **PERMANENT PRODUCTIZATION CONTRACT**

## Purpose

Every sellable Kwork must end with a self-contained `RUNBOOK_FOR_CHATGPT.md` that can be opened in a clean conversation and used immediately to execute a real client order without relying on remembered chat context.

The runbook is an operating manual for ChatGPT, not marketing copy.

## Mandatory portfolio dependencies

Before a Kwork/version is frozen, its productization must obey:

- `KWORK_SERP_MODE_PRODUCTIZATION_GATE_2026-09-10.md` when ordinary Yandex Search may be relevant;
- `KWORK_SERP_COVERAGE_MODE_RESEARCH_2026-09-10.md` as the portfolio research authority for FULL vs SELECTIVE vs HYBRID vs NO-ORGANIC-SERP mode selection.

The SERP mode is proved once during productization and frozen in the product Level-1 authority. A normal future client order executes that frozen mode and does not repeat the portfolio methodology proof.

## Required sections

Every final runbook must contain, in this order:

```text
1. Service identity
2. Client-facing promise
3. Exact inclusions
4. Exact exclusions / forbidden promises
5. Package limits and price assumptions
6. Required client inputs
7. Intake questionnaire
8. Preflight / access / credentials
9. Evidence-source map
10. Exact execution sequence
11. Bridge command/protocol templates where applicable
12. Provider request/cost rules
13. Decision logic owned by ChatGPT
14. Branching rules for missing/ambiguous evidence
15. Checkpoint/recovery rules
16. Deliverable schemas
17. QA checklist
18. Client delivery message template
19. Revision workflow
20. Failure/escalation cases requiring owner action
21. Worked example from accepted test run
22. Known limitations
23. Version / accepted source authority
24. Frozen SERP coverage mode + local decision authority when ordinary Search is relevant
```

## SERP-mode runbook rule

For products that may use ordinary Yandex Search, the final runbook must state the frozen product-level value:

```text
SERP_COVERAGE_MODE = FULL_SERP_COVERAGE | SELECTIVE_DECISION_SERP | HYBRID_SCOPED_FULL | NO_ORGANIC_SERP_BASE
```

and link the product-local Level-1 decision authority.

The runbook must define:

```text
SEARCH_INPUT_SET
REUSE RULE
FRESH SEARCH TRIGGER
WHAT COUNTS AS COVERED
UNPROBED / FAILED BEHAVIOR
PROVIDER / COST ROUTE
CLAIM BOUNDARY
```

Forbidden normal-job instruction:

```text
"Decide again whether this client should use full or selective SERP."
```

That is a productization/versioning decision unless the product-local method itself explicitly contains a scoped hybrid branch.

## Clean-context requirement

The runbook must not use instructions such as:

```text
as we discussed before
use the usual method
same as last time
remember the blood_sand rules
use the settings we already chose
```

Every required rule must be present directly or linked to a canonical repository document that the runbook explicitly tells ChatGPT to open.

## Worker separation

The runbook must explicitly separate:

```text
CHATGPT = reasoning / interpretation / semantic judgment / artifacts / QA
BRIDGE = deterministic provider evidence acquisition / persistence / safe execution
OWNER = authorization / local access / irreducible live action
```

Do not move subjective SEO/marketing judgment into Bridge merely to make the runbook look automated.

## Evidence truth

The runbook must preserve provider/source provenance and must never relabel one evidence surface as another.

If a promised fact cannot be obtained from current accepted hands, the runbook must either:

```text
remove that promise from the Kwork
OR
mark the Kwork NOT_READY_TO_SELL pending capability work
```

## Test-derived only

The final runbook must reflect what was actually exercised during productization.

Untested theoretical steps may be included only as explicit optional/untested extensions and cannot be required for the base package.

A FULL_SERP_COVERAGE product cannot become READY_TO_SELL merely because full coverage exists in theory; its provider/processing/recovery path must be rehearsed at the declared product scale or under an accepted scalable-equivalence test.

## Acceptance rehearsal

Before the runbook is frozen:

```text
open a clean context
open only the runbook + its declared canonical dependencies
present a representative client brief
execute/reconstruct the job plan from those files alone
verify no missing hidden assumption
verify the frozen SERP mode is executable without redesigning it
```

Acceptance marker:

```text
CLEAN_CONTEXT_RUNBOOK_REHEARSAL_PASS
```

Without this marker the Kwork is not `READY_TO_SELL`.
