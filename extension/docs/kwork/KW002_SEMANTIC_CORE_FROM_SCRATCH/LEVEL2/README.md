# KW-002 — LEVEL 2

Status: **ACTIVE UNIVERSAL ROADMAP/METHOD LAYER**

Level 2 contains only **universal rules and methodology for KW-002 roadmap steps**.

It must be executable for any eligible site/business without knowing the client/project that first revealed a lesson.

Mandatory architecture authority:

`../LEVEL1/ROADMAP_AND_METHOD_GENERALIZATION_RULE.md`

## What Level 2 contains

For each step:

```text
WHY the step exists
INPUT data layer
ENTRY gates
METHOD
applicable universal failure/root-cause controls
OUTPUT data layer/artifacts
full-volume/accounting requirements
semantic/method QA
PASS / FAIL / HOLD
next-step contract
```

## What Level 2 must NOT contain

```text
client/site/brand/product names
current job row counts
current family/query/queue IDs
provider request IDs
current job status
current owner execution approval
one project's defect examples as the rule itself
```

Those belong in `work/<JOB_ID>/`.

## Authorities

```text
STEP_RULES_INDEX.md
= canonical universal roadmap/navigation and input→output contract

INHERITED_KW001_STEP_RULES.md
= reusable rules transferred from KW-001, including WHY / root cause / control / PASS

dedicated STEP_<N>_*_METHOD/GATE files
= deeper universal method where a step requires more detail
```

Hard rule:

```text
"INHERITED FROM KW001" LABEL ALONE != RULE TRANSFER
JOB-SPECIFIC OWNER GATE != LEVEL2 METHOD
JOB-SPECIFIC EXAMPLE != UNIVERSAL ROOT CAUSE
```

Before executing a step:

```text
READ KW002 LEVEL1
→ READ ROADMAP_AND_METHOD_GENERALIZATION_RULE
→ READ STEP_RULES_INDEX
→ READ applicable inherited/dedicated Level2 method
→ READ current work/<JOB_ID>/ state/evidence
→ run required external-method review
→ perform job-specific owner disclosure/authorization where required
→ execute
```

Any current-job approval/status document must be stored under `work/<JOB_ID>/`, not here.
