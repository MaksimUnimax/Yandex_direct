# KW-002 Blood & Sand — JOB FLOW

Status: **STEP 03 CURRENT / Q001 RAW PERSISTED / ITEM 2 PIPELINE CONTROL NEXT / MASS CONTINUATION BLOCKED**

## Whole-job goal

```text
semantic core
→ user tasks / intent
→ Yandex-SERP-backed clusters
→ query→page ownership
→ Search-only site architecture
→ AI-search reconciliation
→ final IA / Page Jobs / internal-link model
→ client-ready deliverables
```

No prior Blood & Sand analytical research is an execution input before final freeze.

## Current client-input state

```text
CLIENT_SUPPLIED_BRIEF = FROZEN
ASSORTMENT AUTHORITY = Ozon only
OZON PRODUCT/LISTING ROWS = 76
WB PRODUCT/LISTING ROWS ACTIVE = 0
CLIENT-SUPPLIED COMPETITORS = NONE
EXISTING SEMANTIC CORE = NONE
EXISTING SITE ARCHITECTURE = NONE
OLD BLOOD_SAND ANALYTICAL SOURCES = SEALED
WORK HANDOFFS EXECUTED = 1
```

## Full roadmap / current status

| Step | Purpose | Status |
|---|---|---|
| 00 | Freeze order/scope/source boundary | ✅ COMPLETE / corrected to Ozon-only |
| 01 | Build factual business + complete assortment model | ✅ COMPLETE / PASS / MAIN RETURN QA PASS |
| 02 | Build seed/acquisition map | ✅ COMPLETE / V2 REWORK PASS / **93/100 = 9.3/10** |
| 03 | Primary Wordstat acquisition | 🟡 CURRENT / Q001 persisted / item 2 diagnostic next |
| 04 | First family triage | ⬜ NOT STARTED |
| 05 | Targeted expansion / coverage | ⬜ NOT STARTED |
| 06 | Current Yandex competitor discovery | ⬜ NOT STARTED |
| 07 | Competitor semantic expansion | ⬜ NOT STARTED |
| 08 | Competitor-derived Wordstat expansion | ⬜ NOT STARTED |
| 09 | Candidate semantic master freeze | ⬜ NOT STARTED |
| 10 | Row-level cleanup / intent / user job | ⬜ NOT STARTED |
| 11 | Search-stage semantic freeze | ⬜ NOT STARTED |
| 12 | Ordinary Yandex Search batch | ⬜ NOT STARTED |
| 13 | SERP + task-first clustering | ⬜ NOT STARTED |
| 14 | Query→page ownership + Search-only IA | ⬜ NOT STARTED |
| 15 | AI-search diagnostic selection | ⬜ NOT STARTED |
| 16 | AI-search evidence acquisition | ⬜ NOT STARTED |
| 17 | Search-vs-AI reconciliation | ⬜ NOT STARTED |
| 18 | Final semantic core + IA + Page Jobs | ⬜ NOT STARTED |
| 19 | Client deliverables | ⬜ NOT STARTED |
| 20 | Final QA / recipient acceptance | ⬜ NOT STARTED |
| 21 | Revision rehearsal + Kwork measurement | ⬜ NOT STARTED |
| 22 | Job close | ⬜ NOT STARTED |

## Completed work

```text
Step 00 scope/source freeze = PASS after Ozon-only correction
Step 01 Ozon 76-row factual assortment model = PASS
Step 01 main ChatGPT return QA = PASS
Step 02 V1 = 97 probes / 65/100 = 6.5/10 / SUPERSEDED
Step 02 external method audit = COMPLETE
Step 02 permanent Level-2 quality gate = ACTIVE
Level-1 per-criterion 0–10 scoring rule = ACTIVE
Level-1 fresh internet research + clickable source disclosure rule = ACTIVE
Step 02 V2 primary manifest = 79
Step 02 V2 deferred/control = 49
Step 02 V2 QA = PASS / 93/100 = 9.3/10
Step 03 external-source disclosure = PASS
Step 03 live Bridge/Wordstat capability review = COMPLETE
Step 03 pre-step/provider gate = COMPLETE
Step 03 execution manifest = 79 rows / Q001 reordered to item 1 for OR check
Step 03 batch.start = PASS / 79 pending / 0 provider calls
Step 03 Q001 provider request = HTTP 200 / SUCCEEDED / request executed
Step 03 Q001 raw payload = exact persisted + remote readback PASS
Step 03 Q001 provider result body = {}
Step 03 Q001 results_rows / associations / totalCount = UNRESOLVED, not synthesized as zero
Step 03 Q001 investigation = CURRENT
```

## Current diagnostic state

Official current Yandex GetTop documentation describes HTTP-200 response fields:

```text
totalCount
results[]
associations[]
```

but does not explicitly document whether a zero-result response may be serialized as `{}`.

Therefore:

```text
Q001_HTTP_200 = true
Q001_PROVIDER_ERROR = false
Q001_SYNTAX_REJECTED = false
Q001_RESULT_OBJECT = {}
Q001_RESULTS_ROWS = UNKNOWN
Q001_ASSOCIATION_ROWS = UNKNOWN
Q001_TOTAL_COUNT = UNKNOWN
Q001_EVIDENCE_INTERPRETATION = UNRESOLVED
```

Do not infer `0` for missing provider fields.

## Highest-information next action

Run exactly one already-planned item through the same runtime path:

```text
ITEM 2 = S001 = амулет
```

Purpose: distinguish an OR/no-data outcome from a general Bridge/runtime payload problem.

```text
IF S001 returns populated GetTop fields
→ pipeline works for ordinary phrase
→ Q001 empty object is localized to Q001/operator/no-data behavior
→ compare and define governed interpretation before mass continuation

IF S001 also returns {}
→ STOP
→ suspect Bridge 0.1.4/provider normalization path
→ debug before spending more requests
```

This control is not an additional provider cost outside the plan: `амулет` is already primary item 2.

## Provider/accounting truth

```text
WORDSTAT_BATCH_STARTED = true
WORDSTAT_BATCH_STATUS = RUNNING
WORDSTAT_BATCH_TOTAL = 79
WORDSTAT_BATCH_PENDING = 78
WORDSTAT_BATCH_SUCCEEDED_ITEMS = 1
WORDSTAT_BATCH_TERMINAL = 1
WORDSTAT_BATCH_DUPLICATE_INPUTS = 0
WORDSTAT_REQUESTS_STARTED = 1
WORDSTAT_ESTIMATED_COST_RUB = 0.02
Q001_RAW_READBACK = PASS
SEARCH_REQUESTS_STARTED = 0
AI_SEARCH_REQUESTS_STARTED = 0
WORDSTAT_EXPECTED_REQUESTS_CURRENT_MANIFEST = 79
WORDSTAT_BATCH_HARD_MAX_COST_RUB = 2.00
WORK_HANDOFFS_EXECUTED = 1
```

## Current Step-03 authorities

```text
STEP_03_PRE_STEP_EXTERNAL_RESEARCH_AND_SOURCE_DISCLOSURE_2026-09-09.md
STEP_03_PRE_STEP_PROVIDER_GATE_2026-09-09.md
STEP_03_WORDSTAT_EXECUTION_MANIFEST_V1.csv
STEP_03_WORDSTAT_BATCH_START_RESULT_2026-09-09.txt
STEP_03_WORDSTAT_RAW/001__Q001__wordstat-batch-9292c032-e48e-443e-8576-a51ad4b2c8cc.txt
STEP_03_WORDSTAT_ACQUISITION_RECEIPTS.csv
STEP_03_Q001_EMPTY_PAYLOAD_INVESTIGATION_2026-09-09.md
```

Upstream seed authority remains:

```text
STEP_02_PRIMARY_ACQUISITION_MANIFEST_V2.csv
```

## Current exact action

```text
STEP_03_STARTED = true
STEP_03_BATCH_STARTED = true
STEP_03_RUNTIME_BRIDGE_VERSION_OBSERVED = 0.1.4
STEP_03_PROVIDER_REQUESTS_STARTED = 1
STEP_03_Q001_RAW_PERSISTED = true
STEP_03_Q001_RAW_READBACK = PASS
STEP_03_Q001_EVIDENCE_INTERPRETATION = UNRESOLVED
STEP_03_MASS_CONTINUATION_ALLOWED = false
STEP_03_CONTROL_ITEM_2_ALLOWED = true
STEP_03_NEXT_ITEM = S001_АМУЛЕТ_PIPELINE_CONTROL
STEP_03_COMPLETE = false
NEXT_STEP_ALLOWED = false
NEXT_ACTION = EXECUTE_ONE_BATCH_NEXT_FOR_S001_PIPELINE_CONTROL
```

No third provider request is allowed until item 2 is fully persisted/read back and compared with Q001.
