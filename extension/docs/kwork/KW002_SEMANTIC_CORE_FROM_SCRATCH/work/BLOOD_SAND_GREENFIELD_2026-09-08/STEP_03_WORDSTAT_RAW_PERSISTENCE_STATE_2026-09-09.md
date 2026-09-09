# STEP 03 — WORDSTAT RAW PERSISTENCE STATE

Date: 2026-09-09
Job: `BLOOD_SAND_GREENFIELD_2026-09-08`

## Owner rule activation

The owner explicitly required that Wordstat factual results no longer be kept only in chat. From the activation point onward every provider result must be persisted in full factual form before the next provider block is issued.

```text
PERSISTENCE_ENFORCEMENT_START = M012
CURRENT_POLICY = FULL_RAW_BEFORE_NEXT_BLOCK
```

## Historical provenance boundary

The original historical M001–M011 request-specific bodies were not durably persisted under their original request IDs. They remain historical missing-original evidence and are not relabelled or overwritten.

The owner later explicitly allowed provider re-query when needed. Current-provider re-query data for the affected probes was persisted under new request IDs. M012–M021 retained their request-specific raw evidence. Later canonical-primary probes were collected and persisted prospectively under the same full-raw-before-next-block rule.

```text
ORIGINAL_M001_M011_REQUEST_BODIES_RECOVERED = false
ORIGINAL_M001_M011_HISTORY_OVERWRITTEN = false
CURRENT_REQUERY_DATA_FOR_PRE_GATE_PROBES = PRESERVED
M012_M021_REQUEST_SPECIFIC_RAW = PRESERVED
```

## Final canonical acquisition closure

Canonical primary authority:

`STEP_02_PRIMARY_ACQUISITION_MANIFEST_V2.csv`

```text
CANONICAL_PRIMARY_MANIFEST_ROWS = 79
CANONICAL_PRIMARY_RUN_ORDER = 1..79
CANONICAL_PRIMARY_PROBES_WITH_CURRENT_ACQUISITION_EVIDENCE = 79
CANONICAL_PRIMARY_COVERAGE = 79/79
STEP03_ACQUISITION_PERSISTENCE = COMPLETE / PASS
```

The final missing canonical primary probe was run_order 1, `амулет`. It was re-queried as a new current-provider request and persisted separately without rewriting the historical OUTCOME_UNKNOWN record.

```text
FINAL_S001_PHRASE = амулет
FINAL_S001_REQUEST_ID = wordstat-86e7b86f-b118-4a08-b4bf-564b053de070
FINAL_S001_HTTP_STATUS = 200
FINAL_S001_PROVIDER_STATUS = OK
FINAL_S001_TOTALCOUNT = 478857
FINAL_S001_RESULTS_ROWS = 2000
FINAL_S001_ASSOCIATIONS_ROWS = 20
FINAL_S001_REQUEST_EXECUTED = true
FINAL_S001_AUTOMATIC_RETRY = false
FINAL_S001_RAW_PATH = STEP_03_WORDSTAT_RAW/MANUAL__001_CURRENT_REQUERY__wordstat-86e7b86f-b118-4a08-b4bf-564b053de070.raw.txt
FINAL_S001_RAW_GIT_BLOB = 1a8b027853f6a1c89fc7cb3cdcdd4949e3ab195a
FINAL_S001_REMOTE_READBACK = PASS
```

The remote readback verified the request ID, complete response tail, exactly 2000 `results[]` rows, exactly 20 `associations[]` rows, and `totalCount=478857`.

## What COMPLETE means here

This closure is deliberately narrow:

```text
STEP03 = ACQUISITION / PERSISTENCE
STEP03 != CLEANUP
STEP03 != KEEP/REJECT
STEP03 != CLUSTERING
STEP03 != PAGE DESIGN
SEMANTIC_ANALYSIS_PERFORMED_IN_MAIN_CHAT = false
```

Noise, duplicates, low-frequency rows, provider morphology, and associations remain preserved as acquisition evidence. Their later treatment belongs to downstream methodology, not to Step03 persistence.

## Next transition

The large Wordstat corpus must not be semantically processed in normal chat. Per the owner instruction and `LEVEL1/WORK_HANDOFF_RULE.md`, the next action is a frozen pre-handoff manifest and canonical Work prompt for downstream expansion-family triage. Actual Step04 execution remains subject to the current Level-2 step gate and pre-step external-research/source-disclosure requirements.

```text
PERSISTENCE_GATE_NEXT_PROVIDER_BLOCK_ALLOWED = true
WORDSTAT_PRIMARY_COLLECTION_COMPLETE = true
NEXT_ACTION = PREPARE_WORK_HANDOFF_FOR_STEP04_SUBJECT_TO_METHOD_GATE
```
