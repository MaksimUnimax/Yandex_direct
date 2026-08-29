# KW-001 / OKNO-MSK — STEP 09 ORDINARY YANDEX SEARCH RECONCILIATION

Date: 2026-08-29
Status: **RECONCILED AFTER METHOD + PERSISTENCE CORRECTIONS / READY FOR ACCEPTANCE**

## 1. Authority chain

This reconciliation closes the job-specific Step-09 evidence/accounting work using the latest correction authorities, in this order where statements conflict:

1. `STEP_09_CURRENT_STATE_AND_EXECUTION_PROTOCOL_2026-08-29.md`
2. `STEP_09_COLLECTION_METHOD_AND_IMMEDIATE_PERSISTENCE_POSTMORTEM_2026-08-29.md`
3. `STEP_09_NEXTN_LIVE_CHUNK_VALIDATION_2026-08-29.md`
4. `STEP_09_METHOD_POSTMORTEM_AND_CORRECTION_2026-08-29.md`
5. `STEP_09_ORDINARY_YANDEX_SEARCH_PRE_STEP_REVIEW_2026-08-29.md`

The pre-step review remains the source/method basis. Later correction authorities supersede two failed assumptions discovered during execution:

```text
TRACEABILITY_COMPLETE != FULL_SERP_EVIDENCE_COVERAGE
BRIDGE_INTERNAL_DURABILITY != PROJECT_EVIDENCE_DURABILITY
```

No provider replay is performed for reconciliation.

## 2. Frozen Step-09 scope

```text
provider = ordinary Yandex Search
GenSearch = forbidden in Step 09
region = 213 / Moscow
page = 0
groupsOnPage = 10
docsInGroup = 1
groupMode = GROUP_MODE_FLAT
sortMode = SORT_MODE_BY_RELEVANCE
response format at provider boundary = FORMAT_XML
initial bounded tranche probes = 75
authorized max requests = 80
authorized max cost = 39.04 RUB
unit cost = 0.488 RUB/request
```

The 75 queries were accepted only as an `INITIAL_BOUNDED_SERP_TRANCHE`, not as evidence for all 944 `REVIEW_SEARCH` rows.

## 3. Manifest and semantic QA reconciliation

```text
REVIEW_SEARCH_TOTAL = 944
REVIEW_SEARCH_REASONS = 23
REVIEW_SAMPLING_STRATA = 40
ACTIVE_NONEXACT_DUPLICATE_GROUPS = 8
INITIAL_TRANCHE_PROBES = 75
DIRECT_REVIEW_SEARCH_ROWS = 45
UNRESOLVED_UNPROBED_REVIEW_SEARCH_ROWS = 899
TRACEABILITY_ROWS = 944
TRACEABILITY_COMPLETE = true
FULL_SERP_EVIDENCE_COVERAGE = false
PRE_SERP_TRANSFER_LINKS = 0
INITIAL_TRANCHE_SEMANTIC_QA = PASS_AS_INITIAL_BOUNDED_TRANCHE_ONLY
```

Arithmetic:

```text
45 DIRECT_PROBE + 899 UNRESOLVED_UNPROBED = 944 REVIEW_SEARCH
```

No non-probed row is silently promoted by cleanup reason, Wordstat source/provenance, lexical similarity or absence of contradiction.

Frozen ordered query list SHA-256:

```text
ce2ca4f1220873416f621047b0256e8a1e3c18e633c11b326823ae7e0de0cecb
```

Authorities:

- `STEP_09_SEARCH_PROBE_MANIFEST.tsv`
- `STEP_09_SEARCH_PROBE_MANIFEST_QA.json`
- `STEP_09_SEARCH_PROBE_MANIFEST_RECONCILIATION.md`
- `STEP_09_INITIAL_TRANCHE_SEMANTIC_QA.json`
- `STEP_09_REVIEW_SEARCH_COVERAGE.tsv`

## 4. Provider execution reconciliation

Initial canary:

```text
job_id = kw001-okno-msk-search-step09-20260829
successful provider requests = 1
estimated cost = 0.488 RUB
normalized ranked rows = 10
```

R2:

```text
job_id = kw001-okno-msk-search-step09-20260829-r2
status = COMPLETED
provider requests = 74
succeeded = 74
failed_terminal = 0
outcome_unknown = 0
estimated cost = 36.112 RUB
normalized ranked rows recovered by projection = 740
```

Combined:

```text
PROVIDER_REQUESTS = 75
PROVIDER_SUCCEEDED = 75
PROVIDER_FAILED_TERMINAL = 0
PROVIDER_OUTCOME_UNKNOWN = 0
PROVIDER_ESTIMATED_COST_RUB = 36.600
AUTHORIZED_MAX_REQUESTS = 80
AUTHORIZED_MAX_COST_RUB = 39.04
REQUEST_CAP = PASS
COST_CAP = PASS
```

No blind replay was performed after unknown outcome because there were zero unknown outcomes.

## 5. Normalized SERP persistence reconciliation

Repository evidence:

```text
query index 1 = canary / 10 rows
query indexes 2..75 = R2 projection / 740 rows
combined query coverage = 1..75 contiguous
combined normalized ranked rows = 750
expected TOP-10 rows = 75 * 10 = 750
missing normalized query indexes = 0
missing normalized ranked rows = 0
```

R2 file split:

```text
part 01: indexes 2..20 = 19 queries = 190 rows
part 02: indexes 21..39 = 19 queries = 190 rows
part 03: indexes 40..58 = 19 queries = 190 rows
part 04: indexes 59..75 = 17 queries = 170 rows
R2 total = 74 queries = 740 rows
```

Result:

```text
REPOSITORY_NORMALIZED_SERP_LEDGER_COMPLETE = true
COMBINED_75_QUERY_NORMALIZED_SERP_PERSISTENCE = PASS
```

Authorities:

- `STEP_09_SERP_RESULTS.tsv`
- `STEP_09_SERP_R2_PROJECTION_RAW_PART_01.tsv`
- `STEP_09_SERP_R2_PROJECTION_RAW_PART_02.tsv`
- `STEP_09_SERP_R2_PROJECTION_RAW_PART_03.tsv`
- `STEP_09_SERP_R2_PROJECTION_RAW_PART_04.tsv`
- `STEP_09_SERP_R2_PROJECTION_INDEX.md`

## 6. Raw-evidence fidelity limitation

The initial pre-step PASS gate required complete raw + normalized evidence for every successful item. That condition was **not met as written** for the 74 R2 requests because project-level persistence was delayed until the recovery projection.

Known boundary:

```text
CANARY_FULL_AVAILABLE_FIELDS_PERSISTED = true
R2_NORMALIZED_TOP10_LEDGER_COMPLETE = true
R2_RAW_PER_ITEM_PROVIDER_XML_LEDGER_COMPLETE = false
R2_PER_ITEM_PROVIDER_REQUEST_ID_LEDGER_COMPLETE = false
```

Unavailable R2 fields were not invented.

The incident and non-repeat control are explicitly recorded in:

`STEP_09_COLLECTION_METHOD_AND_IMMEDIATE_PERSISTENCE_POSTMORTEM_2026-08-29.md`.

The later Step-09 current-state authority replaces impossible retrospective replay with the corrected close condition:

```text
available durable per-item identifiers/raw evidence are reconciled without provider replay
```

That corrected condition is satisfied here. This reconciliation therefore does **not** claim that the original full-raw gate passed. It records the fidelity defect and prevents paying for the same evidence again solely to repair project bookkeeping.

## 7. Direct evidence-question decisions

`STEP_09_EVIDENCE_QUESTION_DECISIONS.tsv` contains one direct decision for each frozen probe:

```text
SP09-001 .. SP09-075 = 75/75 direct evidence decisions
missing direct probe decisions = 0
```

The decisions remain Step-09 evidence handoffs. They do not themselves assign final clusters, final page ownership or structural actions.

## 8. Active non-exact duplicate comparisons

All 8 active groups routed from Step 08 to ordinary Search have direct pairwise SERP comparisons:

```text
CMP-0001 / DUP-0001 = 7/10 exact URL overlap -> cluster-together candidate
CMP-0002 / DUP-0002 = 5/10 -> cluster-together candidate
CMP-0003 / DUP-0003 = 5/10 -> cluster-together candidate
CMP-0004 / DUP-0004 = 1/10 -> DO NOT AUTO MERGE / Step-10 boundary review
CMP-0005 / DUP-0005 = 5/10 -> cluster-together candidate
CMP-0006 / DUP-0006 = 9/10 -> cluster-together candidate
CMP-0007 / DUP-0007 = 7/10 -> cluster-together candidate
CMP-0008 / DUP-0008 = 7/10 -> cluster-together candidate
```

Reconciliation:

```text
ACTIVE_DUPLICATE_GROUPS_EXPECTED = 8
ACTIVE_DUPLICATE_COMPARISONS_WRITTEN = 8
MISSING_ACTIVE_DUPLICATE_COMPARISONS = 0
AUTOMATIC_MERGES_PERFORMED_IN_STEP09 = 0
UNIVERSAL_NUMERIC_OVERLAP_THRESHOLD_USED = false
```

The seven `CLUSTER_TOGETHER_CANDIDATE` labels are handoffs to Step 10, not completed cluster decisions.

Authority: `STEP_09_SERP_COMPARISONS.tsv`.

## 9. 944-row coverage accounting

Step 09 intentionally does not claim full direct Search coverage of all 944 `REVIEW_SEARCH` rows.

Final Step-09 coverage accounting:

```text
DIRECT_REVIEW_SEARCH_ROWS_WITH_DIRECT_PROBE = 45
UNRESOLVED_UNPROBED_REVIEW_SEARCH_ROWS = 899
POST_SERP_AUTOMATIC_TRANSFER_ROWS = 0
TOTAL_ACCOUNTED_REVIEW_SEARCH_ROWS = 944
SILENT_DROPS = 0
```

The 899 rows remain explicit unresolved input for downstream governed analysis. Their existence does not invalidate the bounded Step-09 tranche; it prevents false evidence-transfer claims.

## 10. Corrected Step-09 close gate

The latest execution authority says Step 09 remains blocked until eight conditions are satisfied. Reconciliation result:

```text
1. normalized SERP persistence for all 75 probes = PASS
2. attempted-provider accounting reconciled = PASS
3. available durable identifiers/raw evidence reconciled without replay = PASS_WITH_RECORDED_R2_FIDELITY_LIMITATION
4. eight active nonexact duplicate comparisons = PASS / 8 OF 8
5. declared boundary/evidence questions decided = PASS / 75 OF 75 DIRECT PROBES
6. all 944 REVIEW_SEARCH rows explicitly accounted = PASS / 45 DIRECT + 899 UNRESOLVED
7. semantic and provider QA = PASS FOR ACCOUNTING + NORMALIZED EVIDENCE; RAW-R2 FIDELITY LIMITATION RECORDED
8. no Step-10 clustering/page-ownership decision silently performed = PASS
```

## 11. Reconciliation verdict

```text
STEP09_METHOD_RESEARCH_AND_TRACE = PASS
STEP09_OWNER_AUTHORIZATION = RECEIVED
STEP09_INITIAL_TRANCHE_SEMANTIC_QA = PASS_AS_INITIAL_BOUNDED_TRANCHE_ONLY
STEP09_PROVIDER_ACCOUNTING = PASS
STEP09_PROVIDER_REQUESTS = 75
STEP09_PROVIDER_SUCCEEDED = 75
STEP09_PROVIDER_FAILED_TERMINAL = 0
STEP09_PROVIDER_OUTCOME_UNKNOWN = 0
STEP09_PROVIDER_ESTIMATED_COST_RUB = 36.600
STEP09_NORMALIZED_QUERY_COVERAGE = 75/75
STEP09_NORMALIZED_RANKED_ROWS = 750/750
STEP09_R2_FULL_RAW_LEDGER = INCOMPLETE_RECORDED_INCIDENT
STEP09_DIRECT_EVIDENCE_DECISIONS = 75/75
STEP09_ACTIVE_DUPLICATE_COMPARISONS = 8/8
STEP09_REVIEW_SEARCH_ACCOUNTING = 944/944
STEP09_REVIEW_SEARCH_DIRECT = 45
STEP09_REVIEW_SEARCH_UNRESOLVED = 899
STEP09_AUTOMATIC_TRANSFER = 0
STEP09_PREMATURE_FINAL_CLUSTERING = 0
STEP09_PREMATURE_PAGE_OWNERSHIP = 0
STEP09_RECONCILIATION = PASS_AFTER_CORRECTIONS_WITH_RECORDED_R2_RAW_FIDELITY_LIMITATION
STEP10_EXECUTION_NOT_AUTHORIZED_BY_RECONCILIATION_ALONE = true
```
