# KW-002 Blood & Sand — STEP05 W10 PRE-ACQUISITION WORK PROMPT

Date: 2026-09-12  
Handoff ID: `KW002-BS-W10`  
Status: **CANONICAL CURRENT-AUTHORITY WORK PROMPT / NO PROVIDER CALLS IN THIS PASS**

## 0. Mission

Continue the existing KW-002 Blood & Sand greenfield semantic-core rehearsal.

THIS IS AN EXECUTION TASK, but it is a **PRE-ACQUISITION RECONCILIATION PASS**.

This is NOT a new project.  
This is NOT Step04.  
This is NOT Step06.  
This is NOT permission to call Wordstat/Search/GenSearch/AI-search.

The purpose is to take the accepted W09 Step04 queue, reconcile every row against all durable acquisition evidence and owner-fact boundaries, and produce the smallest safe Step05 provider-candidate manifest for a later separate Main ChatGPT release.

Repository:

`MaksimUnimax/Yandex_direct`

Branch:

`roadmap/kwork-productization-2026-08-28`

Job root:

`extension/docs/kwork/KW002_SEMANTIC_CORE_FROM_SCRATCH/work/BLOOD_SAND_GREENFIELD_2026-09-08`

## 1. Fresh-base gate — mandatory before reading job state

Do not work from a cached checkout.

At start:

```text
fetch current remote branch
record actual remote HEAD
verify working tree/base is that current authority
classify any branch changes after the release base
read current governing authorities from the fetched branch
```

Historical preparation base for W10 was:

`ea2707f757475f24550f5b89b1e453e44631abe3`

That SHA is **not** permission to use a stale checkout. Fetch again yourself.

Obey in full:

- `LEVEL1/WORK_BASE_FRESHNESS_AND_AUTHORITY_DRIFT_RULE.md`
- `LEVEL1/ROADMAP_AND_METHOD_GENERALIZATION_RULE.md`
- `LEVEL1/EXECUTION_FAILURE_LEDGER_AND_ANTI_REGRESSION_RULE.md`
- `LEVEL1/PRE_STEP_EXTERNAL_RESEARCH_AND_SOURCE_DISCLOSURE_RULE.md`
- `LEVEL1/DATA_VOLUME_SANITATION_AND_DELIVERY_SCOPE_RULE.md`
- `LEVEL1/JOB_DATA_SEPARATION_AND_LIFECYCLE.md`
- `LEVEL2/STEP_RULES_INDEX.md`

## 2. Current Step04 authority — read in full

Read and treat as current:

- `STEP_04_W09_MAIN_CHATGPT_REMOTE_READBACK_ACCEPTANCE_2026-09-12.md`
- `STEP_04_CURRENT_AUTHORITY_ARTIFACT_MANIFEST_2026-09-11.json`
- `STEP_04_CURRENT_AUTHORITY_TARGETED_EXPANSION_QUEUE_2026-09-11.tsv`
- `STEP_04_CURRENT_AUTHORITY_FAMILY_TRIAGE_2026-09-11.tsv`
- `STEP_04_CURRENT_AUTHORITY_IDENTITY_SIGNAL_LEDGER_2026-09-11.tsv`
- `STEP_04_CURRENT_AUTHORITY_OCCURRENCE_FAMILY_LEDGER_2026-09-11.tsv`
- `STEP_04_CURRENT_AUTHORITY_INDEPENDENT_TAXONOMY_AUDIT_2026-09-11.tsv`
- `STEP_04_CURRENT_AUTHORITY_SANITATION_FEEDBACK_REGISTER_2026-09-11.tsv`

Read W10 preparation authorities:

- `STEP_05_W10_PRE_ACQUISITION_EXTERNAL_RESEARCH_2026-09-12.md`
- `STEP_05_W10_CURRENT_AUTHORITY_QUEUE_GATE_2026-09-12.tsv`

Older Step05 queue gates/prompts are historical only. Do not use their candidate split as current authority.

## 3. Historical Step05 evidence — must reconcile, never replay blindly

Read in full:

- `STEP_05_E013_WORDSTAT_EVIDENCE_RECEIPT_2026-09-10.md`
- the exact durable E013 RAW artifact under `STEP_05_WORDSTAT_RAW/`
- `STEP_05_EXECUTION_CURSOR_2026-09-10.json`
- any prior Step05 source trace / queue artifacts necessary to understand acquisition history.

E013 current safety rule:

```text
PHRASE = !чётки
REQUEST_ID = wordstat-132a43ff-7cf9-4544-a6e2-68da666c4813
RESULT_ROWS = 2000
ASSOCIATIONS = 19
RAW_BLOB_SHA = 550add6010ddbd10e0d807fd1a11046d2b782a4a
REMOTE_READBACK = PASS
REPLAY_ALLOWED = false unless a materially different later question is separately authorized
```

Do not treat chat/context loss as evidence loss.

## 4. Prior acquisition universe — mandatory global reconciliation

Before declaring any provider candidate, inspect the durable search-acquisition authorities, including at least:

- `STEP_02_PRIMARY_ACQUISITION_MANIFEST_V2.csv`
- applicable Step02 probe maps / additional probes / decision overlays;
- `STEP_03_WORDSTAT_EXECUTION_MANIFEST_V1.csv`
- `STEP_03_WORDSTAT_ACQUISITION_RECEIPTS.csv`
- complete `STEP_03_WORDSTAT_RAW/` evidence tree as needed;
- accepted Step03A normalized authorities;
- accepted corrected Step03B authorities;
- current W09 Step04 queue and signal authority;
- historical E013 evidence.

Do not infer “gap” merely because a family-local view is empty.

Mandatory rule:

```text
LOCAL STEP04 GAP
!=
GLOBAL ACQUISITION GAP
```

## 5. Current 13-row queue contract

Account for all 13 rows exactly once.

### Search-gap candidates to CHALLENGE, not authorize automatically

```text
PSQ001
PSQ004
PSQ005
```

For each, prove or reject:

1. exact unresolved search-vocabulary question;
2. why all durable prior evidence does not already answer it;
3. semantic and literal duplicate checks;
4. whether operator/qualification creates real scope gain rather than cosmetic wording change;
5. expected positive information gain;
6. useful negative-result value;
7. exact stop condition;
8. why the proposed request is minimal.

A candidate may be downgraded to reuse/defer/owner-fact/HOLD. Do not preserve three candidates by force.

### Owner-fact rows

```text
PSQ002
PSQ003
PSQ009
PSQ012
PSQ013
```

Search demand cannot establish inventory, physical form, materials or effect/audience claim truth.

Classify each as OWNER_FACT_FIRST or OWNER_FACT_ONLY and preserve the exact unknown. Provider candidate = NO unless a later owner fact legitimately creates a new demand question and Main ChatGPT separately releases it.

### Existing-evidence reuse rows

```text
PSQ006
PSQ007
PSQ008
PSQ010
```

Map the durable evidence that closes each current acquisition question. Do not execute or plan a cosmetic duplicate.

PSQ010 must explicitly link to E013 and record `BLIND_REPLAY = false`.

### Deferred row

```text
PSQ011
```

Keep it deferred to Step10/later SERP unless a concrete named collision now exists in current authority. Do not create a provider call merely to avoid carrying a HOLD/deferred question.

## 6. Current provider + Bridge contract review

Read current repository implementation before writing any candidate command:

- `extension/src/shared/wordstat_protocol.js`
- relevant `extension/src/service_worker.js`
- `extension/src/shared/product.js`
- current policy/cost model files used by Wordstat.

Use `STEP_05_W10_PRE_ACQUISITION_EXTERNAL_RESEARCH_2026-09-12.md` for the current external source trace.

Hard distinction:

```text
OFFICIAL PROVIDER DOCS -> method meaning, operators, quota, current price
CURRENT BRIDGE CODE -> executable envelope and field validation
HISTORICAL SUCCESS -> project-tested evidence only
```

Do not claim that a Bridge-only field is an official public API field unless current official docs support that claim.

Do not apply a general Search API result-depth limit to Wordstat GetTop unless the current Wordstat provider contract explicitly says it applies.

## 7. Candidate design rules

If one or more new search-gap candidates survive reconciliation, materialize a provider candidate manifest but DO NOT EXECUTE IT.

For every surviving candidate include at least:

```text
candidate_id
source_queue_id
unresolved_question
why_existing_evidence_is_insufficient
exact_phrase_or_operator_design
operator_purpose
regions
devices
requested_depth_if_bridge_supports_it
current_bridge_contract_reference
current_provider_semantics_reference
estimated_cost_rub_from_current_source_trace
positive_information_gain
negative_result_value
stop_condition
semantic_duplicate_check
literal_duplicate_check
owner_fact_dependency
provider_execution_status = NOT_EXECUTED
```

### Selection rule

Select **at most one** `FIRST_EXECUTION_CANDIDATE` for the later Main ChatGPT release.

Selection is based on marginal information gain / ambiguity reduction / downstream usefulness, not queue order or convenience.

If no candidate survives, state `NO_NEW_PROVIDER_CALL_NEEDED` and Step05 may close acquisition without spending money.

Do not invent a call just because Step05 exists.

## 8. No provider calls in W10

Hard zero-call gate:

```text
WORDSTAT_CALLS = 0
ORDINARY_SEARCH_CALLS = 0
GENSEARCH_CALLS = 0
AI_SEARCH_CALLS = 0
```

Do not output an executable command into a channel that the Bridge can consume during this pass.

A command specimen, if needed for the manifest, must be stored as inert data and marked `NOT_EXECUTED`.

## 9. No upstream mutation

Do not modify:

- Step00–03B accepted data;
- current W09 Step04 analytical payload;
- historical E013 RAW evidence.

Step05 planning may add reconciliation/manifest artifacts only.

## 10. Required outputs

Materialize in the job root:

1. `STEP_05_W10_QUEUE_RECONCILIATION_WORK_2026-09-12.tsv`
2. `STEP_05_W10_EXISTING_EVIDENCE_REUSE_REGISTER_2026-09-12.tsv`
3. `STEP_05_W10_PROVIDER_CANDIDATE_MANIFEST_V1_2026-09-12.tsv`
4. `STEP_05_W10_PRE_ACQUISITION_KNOWN_FAILURE_REGRESSION_MATRIX_2026-09-12.tsv`
5. `STEP_05_W10_PRE_ACQUISITION_QA_2026-09-12.md`
6. `STEP_05_W10_PRE_ACQUISITION_WORK_RETURN_2026-09-12.md`
7. deterministic materializer/source if nontrivial programmatic reconciliation is used;
8. artifact manifest with row counts/hashes/provenance.

The queue reconciliation must contain all 13 W09 rows exactly once.

## 11. Minimum known-failure regression matrix

Test at least:

```text
F03 provider success != durable completion
F03B-1 lexical/operator shortcut != semantic truth
F03B-4 ambiguity preserved
F04-3 current upstream authority propagated
F05-1 durable evidence duplication prevention
F05-2 owner/business fact never delegated to demand provider
F06+ preliminary family not promoted to final cluster/page
WORK_BASE_FRESHNESS / authority drift
```

Also explicit job regressions:

```text
E013_BLIND_REPLAY = false
PSQ006_REPROBE = false
PSQ007_REPROBE = false
PSQ008_REPROBE = false
PSQ010_REPROBE = false
OWNER_FACT_ROWS_PROVIDER_CANDIDATES = 0
PSQ011_PROVIDER_CANDIDATE = false unless concrete new authority proves otherwise
PROVIDER_CALLS = 0
```

## 12. PASS gates for W10 pre-acquisition

W10 may return PASS_CANDIDATE only if:

```text
LIVE_BASE_HEAD_RECORDED = true
CURRENT_W09_AUTHORITY_USED = true
QUEUE_ROWS_RECONCILED = 13
QUEUE_ROWS_MISSING = 0
QUEUE_ROWS_DUPLICATED = 0
PROVIDER_READY_AT_START = 0
EQUIVALENT_DURABLE_EVIDENCE_REPROBES = 0
OWNER_FACT_GATED_SENT_TO_PROVIDER = 0
LITERAL_DUPLICATE_CANDIDATES = 0
SEMANTIC_DUPLICATE_CANDIDATES_WITHOUT_SCOPE_GAIN = 0
EVERY_SURVIVING_CANDIDATE_HAS_INCREMENTAL_GAIN = true
EVERY_SURVIVING_CANDIDATE_HAS_NEGATIVE_RESULT_VALUE = true
EVERY_SURVIVING_CANDIDATE_HAS_STOP_CONDITION = true
FIRST_EXECUTION_CANDIDATES <= 1
PROVIDER_EXECUTION_STATUS = NOT_EXECUTED
PROVIDER_CALLS = 0
STEP06_STARTED = false
```

Quality scores never override a failed hard gate.

## 13. Pre-publication authority drift gate

Immediately before publication/owner relay:

```text
fetch remote branch again
compare current HEAD to Work start HEAD
classify changed paths
if Level1/Level2/current upstream authority changed -> reconcile before publication
never overwrite a newer mutable cursor/JOB_FLOW/JOB_MANIFEST from stale state
```

Do not include mutable current-state files in an owner relay unless they were freshly reconciled against the immediate pre-publication HEAD.

## 14. STOP condition

After the seven required W10 artifacts are materialized and QA passes:

STOP.

Return for Main ChatGPT remote readback and acceptance.

Do not execute the selected Wordstat candidate.
Do not start Step06.
Do not proceed to downstream clustering/intent/page work.
