# KWORK PORTFOLIO — SERP MODE PRODUCTIZATION GATE

Date: 2026-09-10
Status: **OWNER-APPROVED / PERMANENT / PRODUCTIZATION-ONLY**
Applies to: KW-001..KW-008 and future Kwork products/versions that may use ordinary Yandex Search.

## Mandatory research authority

Before a Kwork product freezes its roadmap, read:

`KWORK_SERP_COVERAGE_MODE_RESEARCH_2026-09-10.md`

This is the portfolio-level method research comparing:

```text
FULL_SERP_COVERAGE
SELECTIVE_DECISION_SERP
HYBRID_SCOPED_FULL
NO_ORGANIC_SERP_BASE
```

## Core rule

SERP coverage mode is selected and justified **once during productization of a Kwork/version**.

It is NOT re-proved on every normal client order after the product roadmap/runbook is frozen.

```text
PRODUCTIZATION
-> PROVE/FREEZE SERP MODE
-> REHEARSE
-> FREEZE IN LEVEL-1 / RUNBOOK

NORMAL CLIENT JOB
-> READ FROZEN PRODUCT RULE
-> EXECUTE THAT MODE
```

A client job can still choose the exact Search phrases/batches/regions required by the frozen method. That operational selection is not a new debate over the product's SERP mode.

## Required local product authority

Before READY_TO_SELL every Kwork/version that might use Search must materialize an equivalent local Level-1 decision containing:

```text
SERP_COVERAGE_MODE
SOLD_RESULT_REQUIRING_OR_NOT_REQUIRING_SERP
WHY FULL/SELECTIVE/HYBRID/NONE IS APPROPRIATE
SEARCH_INPUT_SET DEFINITION
RAW/EXCLUDED/RESERVE BOUNDARY
EVIDENCE REUSE RULE
FRESH SEARCH TRIGGER
UNPROBED/FAILED RESULT STATE
PROVIDER/TRANSPORT MODE
COST/QUOTA ASSUMPTION
CLAIM BOUNDARY
REHEARSAL/VALIDATION EVIDENCE
```

Missing local decision = productization FAIL.

## Allowed modes

### FULL_SERP_COVERAGE
Every phrase in the declared Search-covered final set must have usable direct/reused current SERP evidence.

### SELECTIVE_DECISION_SERP
Search is acquired/reused only for product-defined decision-relevant queries/boundaries/controls. Unprobed rows are not called Search-confirmed.

### HYBRID_SCOPED_FULL
One declared product sub-universe receives FULL coverage; other parts use selective/no fresh Search.

### NO_ORGANIC_SERP_BASE
Ordinary organic Search is not a normal required evidence layer for the base sold result.

## Mode selection questions

During productization answer:

```text
1. What exactly is the client buying?
2. Is direct SERP compatibility for every final phrase part of the promise?
3. Is the site existing or is a new target architecture being designed?
4. Is clustering-by-TOP itself the product?
5. Is current page/history/business evidence stronger/more relevant than full fresh SERP for the sold question?
6. What direct Search blind spots would selective mode leave?
7. What extra decision value would FULL provide?
8. What provider/LLM/operator burden does each mode create?
9. Can current Bridge capabilities execute the chosen mode reliably?
10. Has the chosen mode been rehearsed before freeze?
```

Do not choose FULL only because it sounds more thorough. Do not choose SELECTIVE only because it is cheaper.

## Re-open triggers

Do not re-open the mode for each client. Re-open only when a product/version materially changes, for example:

```text
new commercial promise
existing-site -> greenfield mode or reverse
new full-TOP clustering promise
major provider/transport capability change
material price/limit change that changes executable evidence depth
new rehearsal exposes a mode-level defect
owner explicitly versions/reopens the product
```

## Current registry

Canonical current registry:

`KWORK_SERP_MODE_DECISION_REGISTRY_2026-09-10.md`

Current owner decisions:

```text
KW-001 = SELECTIVE_DECISION_SERP
KW-002 = FULL_SERP_COVERAGE
KW-003..KW-008 = PENDING_PRODUCTIZATION_DECISION
```

Do not infer future decisions from this list.

## Runbook requirement

Every final Kwork `RUNBOOK_FOR_CHATGPT.md` must state the already frozen local SERP mode and reference the local decision authority.

The runbook must NOT instruct a future executor to redesign/re-prove the SERP mode for every order.

## Marker

```text
KWORK_SERP_MODE_ONE_TIME_PRODUCTIZATION_DECISION_REQUIRED = true
KWORK_SERP_MODE_PER_CLIENT_REPROOF_REQUIRED = false
KWORK_SERP_MODE_RESEARCH_AUTHORITY = KWORK_SERP_COVERAGE_MODE_RESEARCH_2026-09-10.md
KW002_SERP_MODE = FULL_SERP_COVERAGE
```