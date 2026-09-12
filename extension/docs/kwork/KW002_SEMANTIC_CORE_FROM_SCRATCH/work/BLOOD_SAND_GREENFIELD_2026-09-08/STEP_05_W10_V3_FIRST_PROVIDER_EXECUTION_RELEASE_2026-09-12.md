# KW-002 Blood & Sand — Step05 W10 V3 first-provider execution release

Date: 2026-09-12
Status: **RELEASED FOR EXACTLY ONE W10C001 WORDSTAT GETTOP REQUEST / NOT YET EXECUTED**

Release base HEAD checked immediately before publication:

`ba1709a0fde68ae8671355924e210deda1985054`

Required prior authorities:

- `STEP_05_W10_V3_PROVIDER_CANDIDATE_MANIFEST_2026-09-12.tsv`
- `STEP_05_W10_V3_FIRST_PROVIDER_EXTERNAL_RESEARCH_2026-09-12.md`
- `STEP_05_W10_V3_FIRST_PROVIDER_EXECUTION_GATE_2026-09-12.md`
- `../../LEVEL2/STEP_05_TARGETED_EXPANSION_AND_PROVIDER_EXECUTION_GATE.md`
- `../../LEVEL2/STEP_03_WORDSTAT_DEPTH_JUSTIFICATION_GATE.md`
- `../../LEVEL2/STEP_03_WORDSTAT_RAW_PERSISTENCE_GATE.md`

The separate first-provider gate passed and was remotely read back before this release. This file is the only authority that changes W10C001 from `NOT RELEASED` to `ONE REQUEST RELEASED`.

## Exact released provider action

```text
SERVICE = wordstat
PREFIX = WORDSTAT_API_V1
METHOD = getTop
PHRASE = (амулет|оберег|талисман) Аум
NUM_PHRASES = 2000
REGIONS = ["225"]
DEVICES = ["DEVICE_ALL"]
MAX_PROVIDER_REQUESTS_THIS_RELEASE = 1
CURRENT_ESTIMATED_COST_RUB = 0.02
```

Exact Bridge command envelope:

```text
WORDSTAT_API_V1 {"method":"getTop","phrase":"(амулет|оберег|талисман) Аум","numPhrases":2000,"regions":["225"],"devices":["DEVICE_ALL"]}
```

No alternative phrase, morphology-fixed variant, different depth, region, device, method or batch request is released.

## Released scope and hard exclusions

```text
W10C001_WORDSTAT_GETTOP_CALLS_ALLOWED_NOW = 1
ORDINARY_SEARCH_CALLS_ALLOWED_NOW = 0
GENSEARCH_CALLS_ALLOWED_NOW = 0
AI_SEARCH_CALLS_ALLOWED_NOW = 0
STEP06_START_ALLOWED = false
SECOND_WORDSTAT_CALL_ALLOWED_BEFORE_CURRENT_RAW_READBACK = false
```

A returned depth boundary, technical failure, zero result, incomplete evidence or unknown outcome does NOT authorize another call.

## Mandatory immediate stop after first provider delivery

After the one released command is executed:

```text
STOP PROVIDER EXECUTION
-> CLASSIFY OUTCOME
-> PERSIST COMPLETE RETURNED BRIDGE/PROVIDER ENVELOPE
-> PERSIST REQUEST/PROVENANCE RECEIPT
-> GITHUB REMOTE READBACK
-> RECONCILE REQUEST CONFIG + REQUEST ID + STATUS + ROWS + FIELDS
```

Only after current RAW readback PASS may downstream semantic processing continue. No second provider request is authorized by this release.

## Durable RAW destination

Complete returned factual evidence belongs under the existing inherited Wordstat RAW authority directory:

```text
STEP_03_WORDSTAT_RAW/STEP05__W10C001__<request_id>.txt
```

The RAW artifact must preserve the complete Bridge/provider envelope and every returned factual field/body element, including where present:

```text
request_id
status
reason
cost_estimate
policy
command
http_status
elapsed_ms
request_executed
automatic_retry
result.results[]
result.associations[]
result.totalCount
complete error body when applicable
```

Do not save only counts, examples or summaries.

## Receipt destination

After execution create/update:

`STEP_05_W10_V3_PROVIDER_RECEIPT_2026-09-12.json`

Minimum receipt fields:

```text
candidate_id
phrase
method
numPhrases
regions
devices
request_id
http_status
status
request_executed
automatic_retry
results_rows
association_rows
total_count
outcome_class
depth_boundary_reached
raw_file
raw_blob_sha/readback_locator
cost_estimate
remote_readback
notes
```

## Pre-declared outcome semantics

```text
SUCCESS_WITH_ROWS
-> bounded positive evidence only
-> full RAW/readback
-> Step03A-compatible normalization
-> Step03B-compatible sanitation
-> Step05 reconciliation

SUCCESS_WITH_ZERO_ROWS
-> bounded zero observation for this exact provider/query/operator/region/device/current snapshot only
-> full RAW/readback
-> may close current snapshot branch
-> MUST NOT become universal zero-demand claim

SUCCESS_BUT_EVIDENCE_INCOMPLETE
-> branch UNRESOLVED
-> preserve returned evidence
-> no semantic closure
-> no follow-up without separate release

VALIDATION_FAILURE
-> no semantic answer
-> preserve failure evidence
-> branch UNRESOLVED
-> corrected request requires separate release

PROVIDER_FAILURE
-> no semantic answer
-> preserve failure evidence
-> branch UNRESOLVED
-> follow-up requires separate release

OUTCOME_UNKNOWN
-> no semantic answer
-> preserve receipt/evidence
-> duplicate-execution risk
-> blind retry forbidden
-> separate recovery/release required
```

Hard invariant:

`NO_RETRY != NEGATIVE_EVIDENCE`

## Depth-boundary rule

```text
RETURNED_RESULTS_ROWS == 2000
=> DEPTH_BOUNDARY_REACHED = true
=> SEMANTIC_UNIVERSE_COMPLETE = false
=> SECOND_CALL_AUTOMATICALLY_AUTHORIZED = false
```

## Downstream processing rule

Any new rows must follow:

```text
COMPLETE RAW + REMOTE READBACK
-> STEP03A-COMPATIBLE NORMALIZATION
-> STEP03B-COMPATIBLE SANITATION
-> UNION / RECONCILIATION
-> STEP05 FINAL DECISION
```

RAW rows cannot be injected directly into accepted family/semantic/page authorities.

If the returned full-volume result is too large to process losslessly in ordinary chat, that later 03A/03B transformation activates the large-data Work rule. Work is not needed for this release or for the one provider request itself.

## Release verdict

```text
W10C001_FIRST_PROVIDER_GATE = PASS
W10C001_PROVIDER_EXECUTION_RELEASED = true
W10C001_EXECUTION_STATUS = NOT_EXECUTED
WORDSTAT_CALLS_ALLOWED_NOW = 1 / W10C001 ONLY
SEARCH_CALLS_ALLOWED_NOW = 0
GENSEARCH_CALLS_ALLOWED_NOW = 0
STEP05_FINAL_COMPLETE = false
STEP06_STARTED = false
```

This release expires immediately after the first provider execution attempt, regardless of outcome. Any further provider action requires a new explicit authority after the first result is durably persisted and reconciled.