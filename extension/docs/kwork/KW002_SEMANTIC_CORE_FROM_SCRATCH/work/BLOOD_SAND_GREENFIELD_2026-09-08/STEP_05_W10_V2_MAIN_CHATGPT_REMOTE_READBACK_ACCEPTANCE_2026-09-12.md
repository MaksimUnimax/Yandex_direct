# KW-002 Blood & Sand — Step05 W10 V2 Main ChatGPT remote readback acceptance

Date: 2026-09-12
Status: **REMOTE READBACK PASS / W10 V2 PRE-ACQUISITION ACCEPTED / PROVIDER EXECUTION NOT RELEASED**

## Verdict

```text
HANDOFF_ID = KW002-BS-W10-V2
OWNER_UPLOAD_HEAD = f4f46d6eb8f40541ec742f36173d72237027dacb
MAIN_CHATGPT_REMOTE_READBACK = PASS
MAIN_CHATGPT_ACCEPTANCE = PASS
QUEUE_RECONCILIATION = 13/13
SURVIVING_NEW_PROVIDER_CANDIDATES = 1
FIRST_FUTURE_CANDIDATE = W10C001
FIRST_FUTURE_CANDIDATE_SOURCE = PSQ005
FIRST_FUTURE_CANDIDATE_EXECUTION_STATUS = NOT_EXECUTED
PROVIDER_EXECUTION_RELEASED_BY_THIS_ACCEPTANCE = false
WORDSTAT_CALLS = 0
ORDINARY_SEARCH_CALLS = 0
GENSEARCH_CALLS = 0
AI_SEARCH_CALLS = 0
STEP03A_MUTATIONS = 0
STEP03B_MUTATIONS = 0
W09_STEP04_MUTATIONS = 0
STEP06_STARTED = false
```

## Publication readback

Remote compare from the W10 V2 preparation head `7ceec096dad6703b5dffede3271019f55946d75d` to owner-upload head `f4f46d6eb8f40541ec742f36173d72237027dacb` is exactly one commit and adds exactly the eight expected W10 V2 artifacts in the canonical job root:

1. `STEP_05_W10_V2_ARTIFACT_MANIFEST_2026-09-12.json`
2. `STEP_05_W10_V2_EXISTING_EVIDENCE_REUSE_REGISTER_2026-09-12.tsv`
3. `STEP_05_W10_V2_PRE_ACQUISITION_KNOWN_FAILURE_REGRESSION_MATRIX_2026-09-12.tsv`
4. `STEP_05_W10_V2_PRE_ACQUISITION_MATERIALIZER_2026-09-12.py`
5. `STEP_05_W10_V2_PRE_ACQUISITION_QA_2026-09-12.md`
6. `STEP_05_W10_V2_PRE_ACQUISITION_WORK_RETURN_2026-09-12.md`
7. `STEP_05_W10_V2_PROVIDER_CANDIDATE_MANIFEST_V1_2026-09-12.tsv`
8. `STEP_05_W10_V2_QUEUE_RECONCILIATION_WORK_2026-09-12.tsv`

No cursor/JOB_FLOW/JOB_MANIFEST or unrelated path was included in the owner upload.

## Full-volume and freshness acceptance

The published QA and materializer prove and remotely expose:

```text
W09_NORMALIZED_IDENTITIES = 24576 / PASS
W09_RAW_OCCURRENCES = 25979 / PASS
STEP03A_NORMALIZATION_ROWS = 25979 / PASS
STEP03B_KEEP = 5100 / PASS
STEP03B_HOLD = 13035 / PASS
STEP03B_EXCLUDE = 6441 / PASS
ACTIVE_PLUS_HOLD_IDENTITIES = 18135 / PASS
ACTIVE_PLUS_HOLD_RAW = 19086 / PASS
W09_FAMILIES = 32 / PASS
W09_INDEPENDENT_ROWS = 24576 / PASS
STEP02_ROWS = 79 / PASS
STEP03_ROWS = 79 / PASS
STEP03_RAW_TREE_FILES_BYTE_READ = 96 / PASS
QUEUE_ROWS = 13 / PASS
```

Work start and pre-publication remote heads were both `7ceec096dad6703b5dffede3271019f55946d75d`, so Work correctly classified no remote drift. The owner upload itself is a separate later publication event and contains only the frozen analytical payload.

## Queue reconciliation accepted

Accepted current dispositions:

```text
PSQ001 = CLOSED_EXISTING_DURABLE_EVIDENCE_NO_REPROBE
PSQ002 = OWNER_FACT_HOLD_NO_PROVIDER
PSQ003 = OWNER_FACT_HOLD_NO_PROVIDER
PSQ004 = CLOSED_EXISTING_DURABLE_EVIDENCE_NO_REPROBE
PSQ005 = SURVIVES_AS_W10C001_NOT_EXECUTED
PSQ006 = CLOSED_EXISTING_DURABLE_EVIDENCE_NO_REPROBE
PSQ007 = CLOSED_EXISTING_DURABLE_EVIDENCE_NO_REPROBE
PSQ008 = CLOSED_EXISTING_DURABLE_EVIDENCE_NO_REPROBE
PSQ009 = OWNER_FACT_HOLD_NO_PROVIDER
PSQ010 = CLOSED_REUSE_E013_NO_REPLAY
PSQ011 = DEFER_TO_STEP10_OR_LATER_SERP_INTENT
PSQ012 = OWNER_FACT_ONLY_NO_PROVIDER_ROUTE
PSQ013 = OWNER_FACT_ONLY_NO_PROVIDER_ROUTE
```

## Independent check of the two closed search-gap candidates

Main ChatGPT independently read back the underlying durable acquisition evidence.

### PSQ001

The Step02/Step03 manifests contain the exact product-qualified probes:

- `Q001 = (амулет|оберег|талисман) RSOTM`
- `Q002 = (амулет|оберег|талисман) Soldier Of Fortune`
- `Q003 = (амулет|оберег|талисман) Бусидо Путь Воина`

Q001 remote RAW is HTTP 200 with `result={}`. Q002 and Q003 preserved durable equivalents are HTTP 200, zero results, zero associations, and explicitly do not fabricate a missing `totalCount` as zero. Therefore replaying the same bounded question has no incremental information gain.

### PSQ004

`Q019 = Кровь и Песок (амулет|оберег|талисман)` is the same bounded brand+product question. Its durable remote RAW is HTTP 200 with `totalCount=1` and no materialized result/association rows. This closes the identical acquisition round without making a global claim of zero demand.

## W10C001 accepted as future candidate only

The sole surviving future candidate is:

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

The current 79-row acquisition manifest contains broad `S053 = Аум` and qualified `Q005 = (амулет|оберег|талисман) Ом`, but no qualified `Аум` probe. Work preserves `Ом != Аум` for evidence purposes and explicitly guards religious/media/AUMA-industrial collisions. The candidate therefore has a genuine spelling+scope information gain and is not a cosmetic replay.

This acceptance does **not** authorize execution. Immediately before any later provider command, the current remote branch, current Bridge schema and current provider price must be rechecked and a separate execution release must be issued.

## Existing evidence reuse accepted

The eight-row reuse register correctly prevents replay of existing durable evidence, including:

- PSQ001 via Q001/Q002/Q003;
- PSQ004 via Q019;
- PSQ005 broad Aum / qualified Om as comparison evidence only;
- PSQ006 existing Gungnir/Odin-spear evidence;
- PSQ007 named-entity collision evidence;
- PSQ008 Belobog/Chernobog/Mara evidence;
- PSQ010 historical E013 `!чётки` with 2000 results + 19 associations and replay=false.

## Regression acceptance

All 17 blocking W10 V2 regressions are PASS. Main readback confirms the key hard boundaries:

```text
DUPLICATE_REPROBES = 0
OWNER_FACT_BYPASSES = 0
E013_BLIND_REPLAY = false
PSQ006_REPROBE = false
PSQ007_REPROBE = false
PSQ008_REPROBE = false
PSQ010_REPROBE = false
PSQ011_PROVIDER_CANDIDATE = false
PROVIDER_CALLS = 0
STEP06_STARTED = false
```

The materializer is inert: it imports only local processing libraries (`csv`, `hashlib`, `json`, `collections`, `pathlib`) and contains no network/provider execution path. It asserts the accepted full-volume counts, W09 hashes, 79/79 acquisition-manifest alignment, candidate `NOT_EXECUTED`, and `PROVIDER_CALLS = 0`.

## Accepted state transition

```text
STEP05_W10_V2_PRE_ACQUISITION = ACCEPTED
STEP05_QUEUE_RECONCILIATION = ACCEPTED_13_OF_13
STEP05_NEW_PROVIDER_CANDIDATES = 1
STEP05_FIRST_FUTURE_CANDIDATE = W10C001
STEP05_PROVIDER_EXECUTION = NOT_RELEASED
STEP05_PROVIDER_CALLS_TOTAL_IN_W10 = 0
STEP06 = NOT_STARTED
```

Next allowed action is a **separate Step05 first-provider execution gate** for W10C001, with immediate current price/schema/freshness recheck. No provider call is authorized by this acceptance file itself.
