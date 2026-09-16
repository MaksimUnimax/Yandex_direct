# KW-002 — LEVEL 2

Status: **ACTIVE UNIVERSAL ROADMAP/METHOD LAYER**

Level 2 contains only **universal rules and methodology for KW-002 roadmap steps**.

It must be executable for any eligible site/business without knowing the client/project that first revealed a lesson.

Mandatory architecture authority:

`../LEVEL1/ROADMAP_AND_METHOD_GENERALIZATION_RULE.md`

Mandatory Yandex Marketing Bridge execution authority:

`../LEVEL1/YANDEX_MARKETING_BRIDGE_EXECUTION_RULE.md`

## Canonical roadmap

`STEP_RULES_INDEX.md`

This is the universal Step00–22 input→method→output roadmap.

Any roadmap step that uses Yandex Marketing Bridge/provider execution must additionally pass:

`YANDEX_MARKETING_BRIDGE_PROVIDER_EXECUTION_GATE.md`

This currently applies at minimum to Step03, Step05 where provider acquisition is used, Step06, Step08, Step12 and Step16, including corrective/re-acquisition branches.

## Dedicated universal step gates currently active

```text
STEP_02_SEED_ACQUISITION_QUALITY_GATE.md
STEP_03_WORDSTAT_DEPTH_JUSTIFICATION_GATE.md
STEP_03_WORDSTAT_RAW_PERSISTENCE_GATE.md
STEP_04_PRELIMINARY_FAMILY_TRIAGE_QUALITY_GATE.md
STEP_05_TARGETED_EXPANSION_AND_PROVIDER_EXECUTION_GATE.md
YANDEX_MARKETING_BRIDGE_PROVIDER_EXECUTION_GATE.md
```

These deepen the corresponding roadmap step without introducing client-specific data.

The YMB gate is cross-step and controls **how a provider command is actually rendered, triggered and proven**. In particular:

```text
ONE COMMAND = ONE STANDALONE FENCED MARKDOWN CODE BLOCK
ASSISTANT RENDERED COMMAND != EXECUTED COMMAND
EXECUTION REQUIRES YMB `Яндекс` ACTION
NO ACTUAL *_RESULT_V1 = NO EXECUTION CLAIM
```

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

## Reusable inherited authorities

```text
INHERITED_KW001_STEP_RULES.md
= reusable rules transferred from KW-001, including WHY / root cause / control / PASS

INHERITED_KW001_RULES_MAP.md
= mapping/index only; it does not override current KW-002 dedicated gates
```

Where a current dedicated KW-002 gate is stricter or newer, the dedicated gate controls that step.

Hard rules:

```text
"INHERITED FROM KW001" LABEL ALONE != RULE TRANSFER
JOB-SPECIFIC OWNER GATE != LEVEL2 METHOD
JOB-SPECIFIC EXAMPLE != UNIVERSAL ROOT CAUSE
CURRENT JOB STATUS != ROADMAP DEFINITION
PRINTED BRIDGE COMMAND != EXECUTED BRIDGE COMMAND
```

Before executing a step:

```text
READ KW002 LEVEL1
→ READ ROADMAP_AND_METHOD_GENERALIZATION_RULE
→ READ YANDEX_MARKETING_BRIDGE_EXECUTION_RULE when Bridge/provider work is possible
→ READ STEP_RULES_INDEX
→ READ YANDEX_MARKETING_BRIDGE_PROVIDER_EXECUTION_GATE for Bridge/provider steps
→ READ applicable dedicated/inherited Level2 method
→ READ current work/<JOB_ID>/ state/evidence
→ run required external-method review
→ perform job-specific owner disclosure/authorization where required
→ execute
```

Any current-job approval/status document must be stored under `work/<JOB_ID>/`, not here.
