# KW-002 Blood & Sand — Step05 W10 V2 pre-handoff manifest

Date: 2026-09-12
Status: **FROZEN PRE-HANDOFF MANIFEST / NO PROVIDER EXECUTION AUTHORIZED**

## JOB_ID

`BLOOD_SAND_GREENFIELD_2026-09-08`

## STEP_ID

`STEP05_W10_PRE_ACQUISITION_RECONCILIATION_V2`

## WHY_WORK_REQUIRED

Step05 must reconcile a 13-row queue against the complete durable Step02/Step03/Step05 evidence universe and current W09 Step04 authorities. The decision is global, not sample-based: a family-local zero can be a false gap when equivalent evidence already exists under another acquisition route. Work is required so the complete evidence universe is processed without sampling/truncation.

## ALLOWED_INPUT_FILES / SOURCES

Current universal rules:

- `LEVEL1/ROADMAP_AND_METHOD_GENERALIZATION_RULE.md`
- `LEVEL1/EXECUTION_FAILURE_LEDGER_AND_ANTI_REGRESSION_RULE.md`
- `LEVEL1/PRE_STEP_EXTERNAL_RESEARCH_AND_SOURCE_DISCLOSURE_RULE.md`
- `LEVEL1/WORK_HANDOFF_RULE.md`
- `LEVEL1/WORK_BASE_FRESHNESS_AND_AUTHORITY_DRIFT_RULE.md`
- `LEVEL1/DATA_VOLUME_SANITATION_AND_DELIVERY_SCOPE_RULE.md`
- `LEVEL1/JOB_DATA_SEPARATION_AND_LIFECYCLE.md`
- `LEVEL2/STEP_RULES_INDEX.md`

Current job authorities:

- `KW002_EXECUTION_CURSOR_2026-09-11.json` current live version at Work start;
- `STEP_04_W09_MAIN_CHATGPT_REMOTE_READBACK_ACCEPTANCE_2026-09-12.md`;
- all accepted W09 `STEP_04_CURRENT_AUTHORITY_*` artifacts;
- `STEP_05_W10_PRE_ACQUISITION_EXTERNAL_RESEARCH_V2_2026-09-12.md`;
- corrected W10 V2 prompt/release;
- `STEP_02_PRIMARY_ACQUISITION_MANIFEST_V2.csv` and relevant Step02 evidence;
- complete durable Step03 execution/RAW/receipt authorities;
- accepted Step03A and corrected Step03B authorities;
- historical Step05 E013 receipt, cursor and RAW artifact;
- frozen client brief/assortment/allowed-source authorities.

Current external sources are only methodological/provider support; they do not become client truth.

## PROHIBITED INPUT_FILES / SOURCES

- SEALED prior Blood & Sand SEO/research except explicit whitelist;
- superseded Step04/W08 family/queue outputs as current truth;
- old pre-W09 Step05 queue split as current authority;
- stale `JOB_FLOW.md` / `JOB_MANIFEST.md` status text as current execution authority until reconciled;
- assistant memory as evidence;
- arbitrary web keyword databases as project evidence;
- any new provider response during this V2 reconciliation pass.

## CURRENT AUTHORITATIVE UPSTREAM ARTIFACTS

Step04 current authority is W09 accepted.

Key accepted counts:

```text
NORMALIZED_IDENTITIES = 24576
RAW_OCCURRENCES = 25979
KEEP = 5100
HOLD = 13035
EXCLUDE = 6441
STEP04_QUEUE_ROWS = 13
STEP04_PROVIDER_READY_NOW = 0
```

Current queue classification entering W10 V2:

```text
SEARCH_GAP_CANDIDATES_TO_CHALLENGE = PSQ001, PSQ004, PSQ005
OWNER_FACT_FIRST_OR_ONLY = PSQ002, PSQ003, PSQ009, PSQ012, PSQ013
EXISTING_EVIDENCE_REUSE = PSQ006, PSQ007, PSQ008, PSQ010
DEFERRED = PSQ011
```

Historical E013 `!чётки` is durable evidence and blind replay is forbidden.

## EXACT EXECUTION GOAL

Reconcile every current queue row against all durable evidence and determine the smallest safe Step05 acquisition plan. The pass may select at most one future first provider candidate, but must execute zero provider calls.

For each possible new candidate prove:

- exact unresolved search-demand question;
- no literal duplicate;
- no semantically equivalent prior probe without scope/operator gain;
- no unresolved owner-fact dependency;
- explicit incremental information gain;
- explicit useful negative-result value;
- explicit stop condition;
- bounded request design;
- current Bridge schema compatibility.

## REQUIRED OUTPUT FILES / TABLES

1. `STEP_05_W10_V2_QUEUE_RECONCILIATION_WORK_2026-09-12.tsv`
2. `STEP_05_W10_V2_EXISTING_EVIDENCE_REUSE_REGISTER_2026-09-12.tsv`
3. `STEP_05_W10_V2_PROVIDER_CANDIDATE_MANIFEST_V1_2026-09-12.tsv`
4. `STEP_05_W10_V2_PRE_ACQUISITION_KNOWN_FAILURE_REGRESSION_MATRIX_2026-09-12.tsv`
5. `STEP_05_W10_V2_PRE_ACQUISITION_QA_2026-09-12.md`
6. `STEP_05_W10_V2_PRE_ACQUISITION_WORK_RETURN_2026-09-12.md`
7. deterministic materializer/source if nontrivial programmatic reconciliation is used;
8. `STEP_05_W10_V2_ARTIFACT_MANIFEST_2026-09-12.json`.

## MANDATORY FIELDS

Queue reconciliation minimum:

```text
queue_id
family_id
current_problem
current_w09_gate
prior_acquisition_overlap
existing_evidence_locator
owner_fact_dependency
search_demand_question
recommended_disposition
candidate_id_or_none
candidate_phrase_or_none
operator_or_scope_gain
positive_information_gain
negative_result_value
stop_condition
literal_duplicate_check
semantic_duplicate_check
collision_risk
later_route
confidence
```

Provider candidate manifest minimum:

```text
candidate_id
source_queue_id
unresolved_question
phrase
regions
devices
requested_depth_if_bridge_supported
operator_usage
prior_probe_difference
expected_information_gain
negative_result_value
collision_guard
stop_condition
max_requests
estimated_cost_rub
execution_status
```

Required: `execution_status = NOT_EXECUTED`.

## ROW / COUNT / JOIN EXPECTATIONS

```text
CURRENT_QUEUE_ROWS = 13
QUEUE_RECONCILED = 13
MISSING_QUEUE_ROWS = 0
DUPLICATE_QUEUE_ROWS = 0
CURRENT_W09_QUEUE_IDENTITY = EXACT
HISTORICAL_E013_FOUND = true
BLIND_E013_REPLAY = false
FIRST_EXECUTION_CANDIDATES <= 1
PROVIDER_CALLS = 0
```

## CLAIM BOUNDARIES

Step05 may establish whether a targeted search-vocabulary gap has useful current Yandex demand evidence.

Step05 may NOT establish:

- client inventory/product form/material/claim truth from search demand;
- final relevance/intent;
- final cluster;
- query→page ownership;
- site architecture;
- competitor authority;
- AI-search conclusions.

## QA / ACCEPTANCE CHECKS

Mandatory universal regression classes:

- F03 provider success != durable completion;
- F03B-1 lexical/operator shortcut != semantic truth;
- F03B-4 uncertainty preservation;
- F04-3 upstream authority propagation;
- F05-1 duplicate durable evidence prevention;
- F05-2 owner-fact/search-demand separation;
- F06+ preliminary family != final cluster/page;
- Work base freshness / authority drift.

Job regressions:

```text
PSQ006_REPROBE = false
PSQ007_REPROBE = false
PSQ008_REPROBE = false
PSQ010_REPROBE = false
E013_BLIND_REPLAY = false
OWNER_FACT_ROWS_PROVIDER_CANDIDATES = 0
PSQ011_PROVIDER_CANDIDATE = false unless genuinely new current authority proves a concrete collision
PROVIDER_CALLS = 0
```

## STOP CONDITIONS

Stop immediately after the V2 reconciliation artifacts and QA are complete and publication/owner relay is prepared.

Do not execute a provider command.
Do not start Step06.
Return to Main ChatGPT for remote readback and a separate provider-execution decision.

## ARTIFACT_PUBLICATION_POLICY

```text
ARTIFACT_PUBLICATION_POLICY = NATIVE_GIT_IF_ALREADY_AUTHENTICATED | OWNER_RELAY_IF_MORE_EFFICIENT
LARGE_ARTIFACT_MODEL_TRANSPORT = FORBIDDEN_BY_DEFAULT
OWNER_RELAY_ALLOWED = true
REMOTE_READBACK_REQUIRED = true
```

If owner relay is used, provide individual files + transport ZIP + direct GitHub Upload-files link for the exact job directory. Do not include stale mutable current-state files unless freshly reconciled immediately before packaging.

## HANDOFF GATE

This manifest is frozen before the corrected V2 Work prompt/release.

Actual Work execution remains blocked until the required owner-facing pre-step disclosure has been shown in chat and the owner then relays the corrected V2 handoff.
