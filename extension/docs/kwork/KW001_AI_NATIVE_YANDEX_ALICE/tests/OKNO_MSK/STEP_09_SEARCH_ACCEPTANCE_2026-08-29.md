# KW-001 / OKNO-MSK — STEP 09 ORDINARY YANDEX SEARCH ACCEPTANCE

Date: 2026-08-29
Status: **COMPLETE AFTER METHOD + EXECUTION + PERSISTENCE CORRECTIONS / R2 RAW-FIDELITY LIMITATION RECORDED**

## 1. Step goal

Collect bounded, reproducible ordinary Yandex Search evidence for material intent, result-type and page-boundary questions before Step 10 clustering and Step 11 page ownership, while keeping unresolved Search rows explicit and avoiding unsupported evidence transfer.

Step 09 is an evidence stage. It does not itself finalize clusters, assign pages, decide structural actions or diagnose cannibalization.

## 2. Method acceptance basis

Step 09 entered execution only after a job-specific pre-step method review with direct external sources and a source-to-method trace.

Direct sources preserved in the pre-step review include:

- Yandex user-need / relevance guidance: https://yandex.ru/support/webmaster/en/recommendations/targeting
- Yandex query/page evidence: https://yandex.ru/support/webmaster/ru/service/search-queries
- Yandex query selection / clustering context: https://yandex.ru/support/webmaster/ru/service/queries-selection
- Yandex ordinary Search API: https://aistudio.yandex.ru/docs/ru/search-api/concepts/web-search.html
- Yandex Search API reference: https://aistudio.yandex.ru/docs/ru/search-api/api-ref/WebSearch/search.html
- Yandex region reference: https://aistudio.yandex.ru/ru/docs/search-api/reference/regions
- Yandex Search API pricing: https://aistudio.yandex.ru/ru/docs/search-api/pricing
- Rush Analytics clustering practice: https://www.rush-analytics.ru/faq/klasterizaciya-zaprosov-semanticheskogo-yadra-rukovodstvo
- Rush Analytics marker-query warning: https://www.rush-analytics.ru/faq/kak-nayti-markernye-zaprosy
- Ahrefs keyword clustering: https://ahrefs.com/blog/keyword-clustering/
- Semrush keyword clustering: https://www.semrush.com/blog/keyword-clustering/

The method review explicitly avoided claiming a universal exact-URL overlap threshold.

Permanent product-method status remains separate:

```text
STEP_09_PERMANENT_METHOD = UNVALIDATED
JOB_SPECIFIC_STEP09_METHOD_REVIEW = COMPLETE
```

Completing this rehearsal does not silently promote the current job-specific method into a universal rule.

## 3. Corrected method boundary

The first manifest design incorrectly treated cleanup/acquisition metadata as transferable Search-intent authority. That assumption was corrected before provider execution:

```text
CLEANUP_REASON != SEARCH_INTENT_CLUSTER
ACQUISITION_SOURCE != SEARCH_INTENT_CLUSTER
LEXICAL_SIMILARITY != SERP_COMPATIBILITY
TRACEABILITY_COMPLETE != FULL_SERP_EVIDENCE_COVERAGE
```

The 75 queries were retained only as an `INITIAL_BOUNDED_SERP_TRANCHE`.

Their accepted roles were:

```text
REVIEW_STRATIFIED_SAMPLE = direct diagnostic only
NONEXACT_DUPLICATE_VARIANT = direct pairwise evidence
STEP1_BOUNDARY_OR_CORE_ANCHOR = direct contrast/control evidence
```

No pre-SERP transfer was allowed.

Authorities:

- `STEP_09_METHOD_POSTMORTEM_AND_CORRECTION_2026-08-29.md`
- `STEP_09_INITIAL_TRANCHE_SEMANTIC_QA.json`
- `STEP_09_SEARCH_PROBE_MANIFEST_RECONCILIATION.md`

## 4. Provider execution acceptance

```text
INITIAL_TRANCHE_PROBES = 75
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

Search profile remained ordinary Yandex Search in region `213` with the frozen TOP-10 flat-result profile.

No GenSearch call was introduced into Step 09.

## 5. Evidence persistence acceptance

Normalized repository evidence is complete for the bounded tranche:

```text
NORMALIZED_QUERIES = 75/75
NORMALIZED_RANKED_ROWS = 750/750
QUERY_INDEX_COVERAGE = 1..75 CONTIGUOUS
REPOSITORY_NORMALIZED_SERP_LEDGER_COMPLETE = true
```

The canary preserves its full available fields. The R2 recovery projection preserves normalized TOP-10 fields for queries 2..75.

## 6. Recorded persistence incident — no false raw-ledger PASS

A process error occurred during R2: paid work continued before each returned chunk had been copied and read back from the project repository. Bridge runtime persistence later allowed normalized recovery, but complete per-item R2 raw XML/provider request IDs were no longer exposed by the recovery projection.

Therefore:

```text
R2_NORMALIZED_TOP10_LEDGER_COMPLETE = true
R2_RAW_PER_ITEM_PROVIDER_XML_LEDGER_COMPLETE = false
R2_PER_ITEM_PROVIDER_REQUEST_ID_LEDGER_COMPLETE = false
```

The original pre-step gate requiring complete raw + normalized evidence for every successful item is **not retroactively claimed as PASS**.

The later active execution authority corrected the close procedure to reconcile all available durable evidence without replay. Repeating 74 paid provider calls solely to reconstruct bookkeeping that was lost by our persistence workflow would create new cost without being justified as new Search evidence.

This incident is accepted only as a recorded evidence-fidelity limitation of this rehearsal, with a mandatory non-repeat workflow:

```text
PROVIDER_RESULT_OR_NEXT_N_CHUNK_RECEIVED
-> PARSE_AND_ACCOUNT
-> IMMEDIATE_REPOSITORY_WRITE
-> GITHUB_READ_BACK_QA
-> COVERAGE_AND_COST_CHECKPOINT
-> ONLY_THEN_NEXT_PAID_CHUNK
```

Authority: `STEP_09_COLLECTION_METHOD_AND_IMMEDIATE_PERSISTENCE_POSTMORTEM_2026-08-29.md`.

## 7. Direct evidence decisions

```text
DIRECT_PROBE_DECISIONS = 75/75
MISSING_DIRECT_PROBE_DECISIONS = 0
```

Authority: `STEP_09_EVIDENCE_QUESTION_DECISIONS.tsv`.

These are evidence handoffs to Step 10. They are not final cluster/page decisions.

## 8. Non-exact duplicate evidence

All active Step-08 groups that required Search were directly compared:

```text
ACTIVE_NONEXACT_DUPLICATE_GROUPS_EXPECTED = 8
ACTIVE_NONEXACT_DUPLICATE_COMPARISONS = 8
MISSING = 0
AUTO_MERGED_IN_STEP09 = 0
```

Observed exact-URL overlaps:

```text
DUP-0001 = 7/10
DUP-0002 = 5/10
DUP-0003 = 5/10
DUP-0004 = 1/10
DUP-0005 = 5/10
DUP-0006 = 9/10
DUP-0007 = 7/10
DUP-0008 = 7/10
```

Seven comparisons are handed off as `CLUSTER_TOGETHER_CANDIDATE`; DUP-0004 is explicitly `DO_NOT_AUTO_MERGE__REVIEW_SEARCH_JOB_BOUNDARY`.

No universal numeric overlap threshold was used to assign a final cluster.

Authority: `STEP_09_SERP_COMPARISONS.tsv`.

## 9. REVIEW_SEARCH accounting acceptance

The Step-08 input contained 944 `REVIEW_SEARCH` rows.

Step-09 final accounting:

```text
DIRECT_REVIEW_SEARCH_ROWS = 45
UNRESOLVED_UNPROBED_REVIEW_SEARCH_ROWS = 899
TOTAL = 944
POST_SERP_AUTOMATIC_TRANSFER_ROWS = 0
SILENT_DROPS = 0
```

`899 UNRESOLVED_UNPROBED` is a deliberate truthful state, not a completeness bug. The bounded tranche was not approved to stand in for all 944 rows.

## 10. Corrected PASS gate

Latest Step-09 execution authority required the following before close:

```text
normalized SERP persistence for all 75 probes = PASS
attempted-provider accounting = PASS
available durable identifiers/raw evidence reconciled without replay = PASS_WITH_RECORDED_R2_FIDELITY_LIMITATION
8 active nonexact duplicate comparisons = PASS / 8 OF 8
declared direct evidence questions decided = PASS / 75 OF 75
944 REVIEW_SEARCH rows explicitly accounted = PASS / 45 + 899
semantic/accounting/normalized evidence QA = PASS
no Step-10 cluster/page-ownership action silently executed = PASS
```

Reconciliation authority: `STEP_09_SEARCH_RECONCILIATION.md`.

## 11. What Step 09 did NOT complete

```text
full direct SERP coverage of all 944 REVIEW_SEARCH rows = false
final user-task/SERP clusters = not decided
final duplicate merges = not decided
page ownership = not decided
structural actions = not decided
cannibalization = not decided
Search-only architecture = not frozen
AI-case selection = not started
AI-search evidence = not collected
```

Those boundaries are intentional.

## 12. Final acceptance verdict

```text
STEP09_PRE_STEP_METHOD_REVIEW = PASS
STEP09_SOURCE_TO_METHOD_TRACE = PASS
STEP09_OWNER_AUTHORIZATION = RECEIVED
STEP09_INITIAL_TRANCHE = PASS_AS_INITIAL_BOUNDED_TRANCHE_ONLY
STEP09_PROVIDER_ACCOUNTING = PASS
STEP09_PROVIDER_REQUESTS = 75
STEP09_PROVIDER_SUCCEEDED = 75
STEP09_PROVIDER_ESTIMATED_COST_RUB = 36.600
STEP09_NORMALIZED_SERP_PERSISTENCE = PASS / 75 QUERIES / 750 RANKED ROWS
STEP09_R2_RAW_FIDELITY = KNOWN_INCOMPLETE / INCIDENT RECORDED / NO FALSE PASS
STEP09_DIRECT_EVIDENCE_DECISIONS = PASS / 75 OF 75
STEP09_ACTIVE_DUPLICATE_COMPARISONS = PASS / 8 OF 8
STEP09_REVIEW_SEARCH_ACCOUNTING = PASS / 944 OF 944
STEP09_AUTOMATIC_EVIDENCE_TRANSFER = 0
STEP09_PREMATURE_CLUSTERING = 0
STEP09_PREMATURE_PAGE_OWNERSHIP = 0
STEP09_COMPLETE = true
STEP10_PRE_STEP_METHOD_RESEARCH_ALLOWED = true
STEP10_EXECUTION_ALLOWED_WITHOUT_ITS_OWN_METHOD_REVIEW = false
```

## 13. Next step

Next major stage: **Step 10 — user-task / SERP clustering**.

`STEP_RULES_INDEX.md` marks Step 10 methodology `UNVALIDATED`. Therefore the next action is not to cluster immediately. The next action is to perform Step-10 pre-step method research, source-to-method traceability, define the executable clustering decision model and PASS gate, then present that method for owner review before Step-10 execution.
