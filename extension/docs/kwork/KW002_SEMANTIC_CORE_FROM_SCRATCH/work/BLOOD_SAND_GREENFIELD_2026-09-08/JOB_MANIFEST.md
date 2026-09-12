# KW-002 JOB MANIFEST — BLOOD_SAND_GREENFIELD_2026-09-08

Status: **STEP04 W09 ACCEPTED / STEP05 W10 V2 PRE-ACQUISITION PREPARED / WORK NOT STARTED / PROVIDER EXECUTION NOT RELEASED**

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
STEP04_W09_PROVIDER_READY_NOW = 0
STEP04_W09_RAW_LINEAGE_LOSS = 0
STEP04_W09_STEP03A_MUTATIONS = 0
STEP04_W09_STEP03B_MUTATIONS = 0
```

Current Step04 acceptance:

`STEP_04_W09_MAIN_CHATGPT_REMOTE_READBACK_ACCEPTANCE_2026-09-12.md`

Current analytical authority:

`STEP_04_CURRENT_AUTHORITY_*`

Detailed historical Step02/03 acquisition/recovery evidence remains in the step-specific manifests, receipts, RAW carriers and QA files. This current manifest does not replace those evidence artifacts.

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

## 6. Current Step05 entry contract

Universal Step05 purpose:

```text
close material search-vocabulary gaps
without duplicate acquisition
without asking search demand to prove owner/business facts
without recursive expansion lacking information gain
```

Current W09 queue classification entering the corrected W10 V2 reconciliation:

```text
SEARCH_GAP_CANDIDATES_TO_CHALLENGE = PSQ001, PSQ004, PSQ005
OWNER_FACT_FIRST_OR_ONLY = PSQ002, PSQ003, PSQ009, PSQ012, PSQ013
EXISTING_EVIDENCE_REUSE_NO_REPROBE = PSQ006, PSQ007, PSQ008, PSQ010
DEFERRED_TO_LATER_INTENT/SERP = PSQ011
PROVIDER_READY_NOW = 0
```

## 7. Corrected W10 V2 preparation authority

The first W10 preparation was created before the mandatory owner-facing pre-step disclosure and without an explicit frozen pre-handoff manifest. It is historical only.

Current corrected package:

- `STEP_05_W10_PREPARATION_RULE_VIOLATION_AND_CORRECTION_2026-09-12.md`
- `STEP_05_W10_PRE_ACQUISITION_EXTERNAL_RESEARCH_V2_2026-09-12.md`
- `STEP_05_W10_PRE_HANDOFF_MANIFEST_V2_2026-09-12.md`
- `STEP_05_W10_PRE_ACQUISITION_WORK_PROMPT_V2_2026-09-12.md`
- `STEP_05_W10_PRE_ACQUISITION_EXECUTION_RELEASE_V2_2026-09-12.md`

The V1 W10 prompt/release/research files are superseded for execution.

## 8. Step05 current boundaries

```text
STEP05_WORK_EXECUTION = NOT_STARTED
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

Actual Work execution becomes eligible only after Main ChatGPT has shown the required owner-facing pre-step disclosure in chat and the owner relays the exact W10 V2 handoff.

## 9. Step05 Work output contract

W10 V2 Work must reconcile all 13 queue rows and create:

1. `STEP_05_W10_V2_QUEUE_RECONCILIATION_WORK_2026-09-12.tsv`
2. `STEP_05_W10_V2_EXISTING_EVIDENCE_REUSE_REGISTER_2026-09-12.tsv`
3. `STEP_05_W10_V2_PROVIDER_CANDIDATE_MANIFEST_V1_2026-09-12.tsv`
4. `STEP_05_W10_V2_PRE_ACQUISITION_KNOWN_FAILURE_REGRESSION_MATRIX_2026-09-12.tsv`
5. `STEP_05_W10_V2_PRE_ACQUISITION_QA_2026-09-12.md`
6. `STEP_05_W10_V2_PRE_ACQUISITION_WORK_RETURN_2026-09-12.md`
7. deterministic materializer/source if needed;
8. `STEP_05_W10_V2_ARTIFACT_MANIFEST_2026-09-12.json`.

Provider execution remains `NOT_EXECUTED` in this pass.

## 10. Current next action

```text
MAIN CHATGPT OWNER-FACING PRE-STEP DISCLOSURE
→ OWNER RELAYS W10 V2 PROMPT
→ WORK FULL RECONCILIATION / ZERO PROVIDER CALLS
→ PUBLICATION OR OWNER RELAY
→ MAIN CHATGPT REMOTE READBACK / RETURN QA
→ SEPARATE DECISION ON WHETHER ONE NEW PROVIDER CALL IS JUSTIFIED
```

## 11. Current mutable-state authority

Current execution cursor remains the machine-readable current-state authority. `JOB_FLOW.md` is the human-readable roadmap/status view and must remain consistent with it.
