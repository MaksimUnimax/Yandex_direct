# KW-002 JOB MANIFEST — BLOOD_SAND_GREENFIELD_2026-09-08

Status: **STEP04 W09 ACCEPTED / STEP05 W10 V2 PRE-ACQUISITION ACCEPTED / ONE FUTURE PROVIDER CANDIDATE / PROVIDER EXECUTION NOT RELEASED / STEP06 NOT STARTED**

## 1. Job identity

```text
KW_ID = KW-002
JOB_ID = BLOOD_SAND_GREENFIELD_2026-09-08
JOB_TYPE = PRODUCTIZATION_REHEARSAL
EXECUTION_MODE = CLEAN_FROM_SCRATCH
BUSINESS = Blood & Sand / «Кровь и Песок»
SITE = кровьипесок.рф
SITE_STATE = NEW_SITE
REGION = Russia
LANGUAGE = Russian
PRIMARY_SEARCH_ENGINE = Yandex
```

## 2. Frozen client truth

```text
Brand = «Кровь и Песок» / Blood & Sand
Business = product brand / seller
Client wording = амулеты, обереги и талисманы; в ассортименте есть в том числе товары для автомобиля
Sales channels = Ozon + Wildberries
Assortment authority = Ozon only
Primary market/search geography = Russia
New owned website planned = YES
OZON PRODUCT/LISTING ROWS = 76
WB PRODUCT/LISTING ROWS ACTIVE = 0
```

Frozen client/source authorities:

- `CLIENT_SUPPLIED_BRIEF.md`
- `CLIENT_SUPPLIED_ASSORTMENT_MANIFEST.md`
- `CLIENT_SUPPLIED_PRODUCT_CATALOG_OZON_76.csv`
- `ALLOWED_INPUTS_AND_SEALED_SOURCES.md`

## 3. Clean-baseline rule

```text
PRIOR BLOOD_SAND WORDSTAT/SEARCH/ALICE/COMPETITOR/CLUSTER/IA RESEARCH = SEALED / FORBIDDEN EXECUTION INPUT
```

Only explicitly allowed current-job sources may be used.

## 4. Current accepted upstream truth

```text
STEP00 = PASS / Ozon-only scope
STEP01 = PASS / 76 of 76
STEP02_V1 = SUPERSEDED
STEP02_V2 = PASS
STEP03 = PASS / 79 of 79 current durable provider outcomes
STEP03_RAW_RECOVERY = COMPLETE / PASS
STEP03A = PASS / 24576 normalized identities / 25979 RAW occurrences / lineage preserved
STEP03B_ORIGINAL = SUPERSEDED
STEP03B_CORRECTED = ACCEPTED
STEP03B_KEEP = 5100
STEP03B_HOLD = 13035
STEP03B_EXCLUDE = 6441
STEP04_W07_AUDIT = ACCEPTED / REWORK_REQUIRED / 255 material defect identities
STEP04_W08 = HISTORICAL / NOT CURRENT AUTHORITY
STEP04_W09 = MAIN CHATGPT REMOTE READBACK ACCEPTED
STEP04_CURRENT = ACCEPTED_W09_CURRENT_AUTHORITY
STEP04_W09_FAMILIES = 32
STEP04_W09_OBSERVED_FAMILIES = 29
STEP04_W09_QUEUE_ROWS = 13
STEP04_W09_RAW_LINEAGE_LOSS = 0
STEP04_W09_STEP03A_MUTATIONS = 0
STEP04_W09_STEP03B_MUTATIONS = 0
```

Current Step04 acceptance:

`STEP_04_W09_MAIN_CHATGPT_REMOTE_READBACK_ACCEPTANCE_2026-09-12.md`

Detailed historical Step02/03 acquisition/recovery evidence remains in the step-specific manifests, receipts, RAW carriers and QA files.

## 5. Historical Step05 evidence preserved

Exactly one historical Step05 provider request is durable and reusable:

```text
historical_queue_item = E013
phrase = !чётки
request_id = wordstat-132a43ff-7cf9-4544-a6e2-68da666c4813
results = 2000
associations = 19
raw_blob_sha = 550add6010ddbd10e0d807fd1a11046d2b782a4a
remote_readback = PASS
replay_required = false
```

Authority:

`STEP_05_E013_WORDSTAT_EVIDENCE_RECEIPT_2026-09-10.md`

## 6. Step05 preparation correction

The first W10 preparation was created before mandatory owner-facing pre-step disclosure and without an explicit frozen pre-handoff manifest. It is historical only and not execution authority.

Current corrected V2 package:

- `STEP_05_W10_PREPARATION_RULE_VIOLATION_AND_CORRECTION_2026-09-12.md`
- `STEP_05_W10_PRE_ACQUISITION_EXTERNAL_RESEARCH_V2_2026-09-12.md`
- `STEP_05_W10_PRE_HANDOFF_MANIFEST_V2_2026-09-12.md`
- `STEP_05_W10_PRE_ACQUISITION_WORK_PROMPT_V2_2026-09-12.md`
- `STEP_05_W10_PRE_ACQUISITION_EXECUTION_RELEASE_V2_2026-09-12.md`

The V1 W10 prompt/release/research files remain superseded.

## 7. Step05 W10 V2 accepted pre-acquisition authority

Main ChatGPT acceptance:

`STEP_05_W10_V2_MAIN_CHATGPT_REMOTE_READBACK_ACCEPTANCE_2026-09-12.md`

Accepted W10 V2 outputs:

1. `STEP_05_W10_V2_QUEUE_RECONCILIATION_WORK_2026-09-12.tsv`
2. `STEP_05_W10_V2_EXISTING_EVIDENCE_REUSE_REGISTER_2026-09-12.tsv`
3. `STEP_05_W10_V2_PROVIDER_CANDIDATE_MANIFEST_V1_2026-09-12.tsv`
4. `STEP_05_W10_V2_PRE_ACQUISITION_KNOWN_FAILURE_REGRESSION_MATRIX_2026-09-12.tsv`
5. `STEP_05_W10_V2_PRE_ACQUISITION_QA_2026-09-12.md`
6. `STEP_05_W10_V2_PRE_ACQUISITION_WORK_RETURN_2026-09-12.md`
7. `STEP_05_W10_V2_PRE_ACQUISITION_MATERIALIZER_2026-09-12.py`
8. `STEP_05_W10_V2_ARTIFACT_MANIFEST_2026-09-12.json`

Accepted counts/boundaries:

```text
QUEUE_RECONCILED = 13/13
REUSE_REGISTER_ROWS = 8
REGRESSION_MATRIX = 17/17 PASS
SURVIVING_NEW_PROVIDER_CANDIDATES = 1
DUPLICATE_REPROBES = 0
OWNER_FACT_BYPASSES = 0
PROVIDER_CALLS_IN_W10 = 0
STEP03A_MUTATIONS = 0
STEP03B_MUTATIONS = 0
W09_STEP04_MUTATIONS = 0
STEP06_STARTED = false
```

Accepted dispositions:

```text
PSQ001 = CLOSED BY Q001-Q003 / NO REPROBE
PSQ002 = OWNER FACT HOLD
PSQ003 = OWNER FACT HOLD
PSQ004 = CLOSED BY Q019 / NO REPROBE
PSQ005 = ONE FUTURE CANDIDATE W10C001 / NOT EXECUTED
PSQ006 = EXISTING EVIDENCE REUSE / NO REPROBE
PSQ007 = EXISTING EVIDENCE REUSE / NO REPROBE
PSQ008 = EXISTING EVIDENCE REUSE / NO REPROBE
PSQ009 = OWNER FACT HOLD
PSQ010 = E013 REUSE / NO REPLAY
PSQ011 = DEFER TO STEP10 OR LATER SERP/INTENT
PSQ012 = OWNER FACT ONLY
PSQ013 = OWNER FACT ONLY
```

## 8. Sole future provider candidate

```text
candidate_id = W10C001
source_queue_id = PSQ005
phrase = (амулет|оберег|талисман) Аум
regions = [225]
devices = [DEVICE_ALL]
requested_depth_if_bridge_supported = 2000
max_requests = 1
execution_status = NOT_EXECUTED
```

Evidence distinction preserved:

```text
S053 = broad Аум evidence
Q005 = qualified Ом evidence
W10C001 = qualified Аум question not yet acquired
Ом != Аум for evidence reuse
```

This candidate is not yet provider evidence and is not permission to make a request.

## 9. Current Step05 hard boundary

```text
STEP05_W10_V2_PRE_ACQUISITION = ACCEPTED
STEP05_PROVIDER_EXECUTION = NOT_RELEASED
WORDSTAT_CALLS_ALLOWED_NOW = 0
ORDINARY_SEARCH_CALLS_ALLOWED_NOW = 0
GENSEARCH_CALLS_ALLOWED_NOW = 0
AI_SEARCH_CALLS_ALLOWED_NOW = 0
STEP03A_MUTATION_ALLOWED = false
STEP03B_MUTATION_ALLOWED = false
STEP04_CURRENT_AUTHORITY_MUTATION_ALLOWED = false
STEP06_STARTED = false
```

## 10. Required gate before W10C001 execution

Before any provider command:

```text
FETCH CURRENT REMOTE HEAD
→ classify authority drift
→ recheck current Bridge Wordstat command schema
→ recheck current official provider price / applicable limits
→ issue separate W10C001 first-provider execution release
→ execute at most one request
→ persist complete RAW
→ remote readback
→ normalize/sanitize new rows through Step03A/Step03B
→ return to Main ChatGPT before any second provider action
```

## 11. Current next action

Prepare the separate Step05 first-provider execution gate for W10C001. Do not execute any provider call and do not start Step06 until that separate release exists.
