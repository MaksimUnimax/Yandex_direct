# KW-002 — LEVEL 1 JOB DATA SEPARATION AND LIFECYCLE

Status: **ACTIVE / OWNER-AUTHORIZED SCAFFOLD**

## 1. Three stores, three purposes

```text
LEVEL1/
= universal cross-step rules

LEVEL2/
= universal step methods

work/<JOB_ID>/
= one concrete order only
```

No concrete client/order data is allowed to become a permanent Level 1 or Level 2 input merely because it was useful in one test.

## 2. work/<JOB_ID>/ required files

At job creation, materialize at minimum:

```text
JOB_MANIFEST.md
JOB_FLOW.md
CLIENT_BRIEF_FROZEN.md or equivalent section in manifest
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
cluster/page IDs
job-specific thresholds/heuristics
counts/costs/request ids
current status
open questions
HOLD/REJECT/KEEP rows
Work handoff manifests/results
client deliverables
revision records
productization measurements
```

## 4. Level 1 and Level 2 must not absorb job facts

Forbidden permanent contamination includes:

```text
client brand/domain used as universal input
exact current-job query/page counts as permanent thresholds
current-job competitor names as required future competitors
current-job URL structure as a template for all sites
current-job provider cost/request count as a universal constant
current-job cluster split as a universal rule
```

A reusable lesson may be proposed only as:

```text
failure class
→ root cause
→ general control
→ parameterized rule
→ generic pass gate
```

Owner authorization is required before permanent promotion.

## 5. Job flow

```text
CREATE work/<JOB_ID>/
→ freeze brief / sources / scope
→ execute Level 2 steps in order
→ persist complete evidence after each step
→ update JOB_FLOW
→ build final deliverables
→ revision rehearsal / real revision if applicable
→ productization measurement
→ final handoff / owner review
→ close job
```

For test/demo jobs, the workspace may be retained until portfolio/sample acceptance is complete. Do not delete evidence needed to prove the productization test.

## 6. Clean-context rule for seeded internal projects

When the business has prior internal research and the test goal is FROM_SCRATCH:

```text
NEW EXECUTION CONTEXT
MUST RECEIVE ONLY
LEVEL1 + LEVEL2 + ALLOWED work/<JOB_ID>/ INPUTS
```

Do not rely on assistant memory of prior research.

If the current conversation already contains old conclusions, those conclusions are not execution evidence and must not be passed into the clean execution unit.

Where necessary, use a clean ChatGPT Work run with an explicit source whitelist.

## 7. Regression comparison is downstream only

After the new final result is frozen, prior research may be opened under a separate comparison gate to answer:

```text
what the new method independently reproduced
what it found that old work missed
what old work found that new method missed
where conclusions differ and why
whether the product needs correction before sale
```

The comparison may improve product methodology only after owner review; it may not retroactively contaminate the frozen from-scratch result.
