# KW-002 — LEVEL 1 JOB DATA SEPARATION AND LIFECYCLE

Status: **ACTIVE / OWNER-AUTHORIZED / UNIVERSAL**

Canonical generalization authority:

`ROADMAP_AND_METHOD_GENERALIZATION_RULE.md`

## 1. Three stores, three purposes

```text
LEVEL1/
= universal cross-step rules + universal root causes

LEVEL2/
= universal roadmap step methods executable for any eligible site/business

work/<JOB_ID>/
= one concrete order only
```

No concrete client/order data is allowed to become permanent Level1/Level2 methodology merely because it was useful in one execution.

## 2. Required job workspace

At job creation, materialize at minimum:

```text
JOB_MANIFEST.md
JOB_FLOW.md
frozen client brief/scope
ALLOWED_INPUTS_AND_SEALED_SOURCES.md
SOURCE_MANIFEST.md
WORK_HANDOFF_LOG.md when Work is used
```

Then add step evidence/artifacts as required.

## 3. Job data may contain

```text
client/test identity
business/product/service vocabulary
region
assortment inputs
current queries/seeds
provider results
SERP results
competitor URLs
family/cluster/page IDs
job-specific thresholds/heuristics
counts/costs/request IDs
current status
open questions
HOLD/REJECT/KEEP rows
owner approvals
Work handoffs
client deliverables
revision records
productization measurements
```

## 4. Level1/Level2 contamination is forbidden

Forbidden permanent contamination includes:

```text
client brand/domain as universal input
one site's product/family/query IDs in a universal rule
current-job row counts as permanent thresholds
current-job competitor names as required future competitors
current-job URL structure as a template for all sites
current-job provider cost/request count as a universal constant
current-job cluster split as a universal rule
current owner execution approval/status in Level2
```

## 5. How a concrete failure becomes universal

A reusable lesson may be promoted only through:

```text
concrete incident
→ underlying root cause/mechanism
→ proof the mechanism can recur outside this client
→ parameterized universal control
→ generic PASS/FAIL gate
→ mapping to applicable roadmap steps
```

The concrete example/counts remain in `work/<JOB_ID>/` as provenance.

Forbidden:

```text
ONE BAD PHRASE -> UNIVERSAL SPECIAL CASE
ONE FAMILY ID -> PERMANENT TAXONOMY
ONE CLIENT VOCABULARY -> GLOBAL LEXICAL RULE
```

## 6. Job lifecycle

```text
CREATE work/<JOB_ID>/
→ freeze brief / sources / scope
→ execute universal Level2 steps in order
→ persist complete evidence after each step
→ update JOB_FLOW
→ build final deliverables
→ revision rehearsal / real revision if applicable
→ productization measurement
→ final handoff / owner review
→ close job
```

## 7. Clean-context rule

When a business has prior internal research and the current job is FROM_SCRATCH:

```text
NEW EXECUTION CONTEXT
MUST RECEIVE ONLY
LEVEL1 + LEVEL2 + EXPLICITLY ALLOWED work/<JOB_ID>/ INPUTS
```

Do not rely on assistant memory of prior research.

If a conversation contains old conclusions, they are not execution evidence unless explicitly whitelisted.

## 8. Regression comparison is downstream only

After a new result is frozen, prior research may be opened under a separated comparison gate to measure what was reproduced, missed or improved.

Comparison may improve universal methodology only after the generalization test in `ROADMAP_AND_METHOD_GENERALIZATION_RULE.md` passes. It may not retroactively contaminate the from-scratch result.

## 9. Universal-layer acceptance gate

Before accepting a Level1/Level2 edit:

```text
JOB_SPECIFIC_CLIENT_NAMES_IN_METHOD = 0
JOB_SPECIFIC_IDS_IN_METHOD = 0
JOB_SPECIFIC_COUNTS_AS_UNIVERSAL_THRESHOLDS = 0
CURRENT_JOB_STATUS_IN_LEVEL2 = 0
ROOT_CAUSE_GENERALIZED_WHERE_LESSON_DERIVED = true
ANY_SITE_EXECUTABILITY_TEST = PASS
```
