# KW-002 / BLOOD & SAND — STEP07 FULL-VOLUME REWORK EXECUTION QA

Date: 2026-09-18
Action: `ACTUAL_STEP07_FULL_VOLUME_CORRECTIVE_REWORK`
Work start remote HEAD: `90d0755a497bd23c25ea14fd3d5fcae967bd12c3`
Pre-publication remote HEAD: `90d0755a497bd23c25ea14fd3d5fcae967bd12c3`
Authority drift: **NONE MATERIAL; ONE ACCEPTANCE SHA METADATA TYPO RECONCILED BY EXACT ACCEPTED GIT BLOB**
Overall hard QA: **PASS**
Step result: **COMPLETE_WITH_ACCEPTED_TARGET_BLOCK_EVIDENCE**

## 1. Executive result

The complete affected Attempt-1 semantic universe and the complete canonically
accepted browser-recovery evidence set were reprocessed under one corrected
candidate-eligibility producer. Raw BODY_TEXT, literary examples, citations,
broken fragments and generic UI are no longer promoted merely because they
contain an in-scope token. BODY_TEXT remains provenance for the 1,417 preserved
Attempt-1 rows. New identities are produced only from compact, independently
meaningful structured page fields.

```text
WORK_START_REMOTE_HEAD = 90d0755a497bd23c25ea14fd3d5fcae967bd12c3
WORK_PRE_PUBLICATION_REMOTE_HEAD = 90d0755a497bd23c25ea14fd3d5fcae967bd12c3
AUTHORITY_DRIFT_STATUS = NONE_MATERIAL__ACCEPTANCE_SHA_METADATA_TYPO_RECONCILED_BY_EXACT_GIT_BLOB
STEP07_REWORK_STATUS = PASS_COMPLETE_WITH_ACCEPTED_TARGET_BLOCK_EVIDENCE

AUTHORIZED_COMPETITORS = 32
SOURCE_URL_ROWS = 1976
PAGE_EVIDENCE_ROWS_CONSUMED = 725
FULL_EXISTING_CANDIDATE_IDENTITIES_REEVALUATED = 686
FULL_EXISTING_PROVENANCE_ROWS_REEVALUATED = 1417
NEW_PROVENANCE_ROWS_ADDED = 2531
TOTAL_PROVENANCE_ROWS = 3948
CANDIDATE_IDENTITIES = 2172
NEW_RECOVERY_IDENTITY_DELTA = 1486
```

## 2. Accepted browser-recovery accounting consumed

| Terminal state | Attempt 1 | Rework / accepted recovery |
|---|---:|---:|
| Inspected | 24 | 432 |
| Redirected in scope | 0 | 293 |
| Excluded out of scope | 1201 | 1201 |
| Excluded duplicate | 0 | 24 |
| Target CAPTCHA / anti-bot | 12 | 26 |
| Execution-environment failure | 561 proxy/network rows | 0 |
| Unresolved dynamic content | 0 | 0 |
| Total source URLs | 1976 | 1976 |

```text
DISCOVERED_URLS: 1976 -> 1976
INSPECTED_URLS: 24 -> 432
EXCLUDED_URLS: 1201 -> 1225
INACCESSIBLE_URLS: 751 -> 26
REDIRECTED_TERMINAL_URLS: 0 -> 293
UNRESOLVED_URLS: 0 -> 0
ERROR_URLS: 0 -> 0

COVERAGE_COMPLETE = 29
COVERAGE_COMPLETE_WITH_INACCESSIBLE_EVIDENCE = 3
COVERAGE_INCOMPLETE_OR_BLOCKED_OR_ERROR = 0
INSPECTED_CANDIDATE_YIELD_URLS = 191
INSPECTED_NO_CANDIDATE_URLS = 241
```

The 26 target blocks are accepted target-side evidence. No bypass or new
navigation was attempted. All 32 competitors reconcile; no Attempt-1 proxy
failure survives as current source-level closure.

One non-material acceptance-metadata typo was found and bounded during
preflight: the recorded residual-retry SHA contains `...37f...`, while the
accepted/current Git blob `440e4df546720e2dfd7f6ed4a36ab5394f55dca1`
computes `ad77bad53a960c6ea37c4689f556e2f92f17bc5a57fcdd0dfaa0d7b6a03faf3d`.
The Git blob identity matches the canonical remote-acceptance record exactly;
the immutable file was not changed.

## 3. Corrected producer full-volume accounting

| Structured evidence field | Occurrences evaluated |
|---|---:|
| `page_title` | 725 |
| `h1` | 706 |
| `headings_h2_h6` | 11225 |
| `breadcrumbs` | 7 |
| `navigation_labels` | 1919 |
| `category_labels` | 14 |
| `product_or_service_names` | 920 |
| `faq_questions` | 0 |
| `glossary_terms` | 102 |

```text
STRUCTURED_OCCURRENCES_EVALUATED = 15618
STRUCTURED_OCCURRENCES_PROMOTED = 2531
STRUCTURED_OCCURRENCES_REJECTED_BEFORE_IDENTITY = 13087
PROMOTED_VALID = 2515
PROMOTED_AMBIGUOUS = 16
```

Rejected producer classes:

| Producer reason | Rows/identities |
|---|---:|
| `NO_INDEPENDENT_IN_SCOPE_SEMANTIC_DIRECTION` | 7252 |
| `NAVIGATION_IS_CONTEXT_NOT_CANDIDATE_IDENTITY` | 1730 |
| `LITERARY_OR_SENTENCE_CORPUS_SURFACE` | 1656 |
| `GENERIC_UI_OR_NAVIGATION_NOISE` | 1513 |
| `EMPTY_STRUCTURED_FIELD` | 488 |
| `RAW_BODY_PROSE_IS_PROVENANCE_NOT_IDENTITY` | 249 |
| `RAW_PROSE_OR_CLAIM_NOT_STABLE_SEMANTIC_DIRECTION` | 154 |
| `CONCATENATED_NAVIGATION_OR_CATEGORY_TEXT` | 117 |
| `PRODUCT_LISTING_OUTSIDE_FROZEN_SEMANTIC_SCOPE` | 113 |
| `BROKEN_OR_CONTEXT_DEPENDENT_FRAGMENT` | 87 |
| `LONG_FORM_NOT_INDEPENDENT_CANDIDATE` | 31 |
| `PUBLIC_PAGE_ERROR_UI_TEXT` | 27 |
| `DICTIONARY_WRAPPER_TARGET_OUTSIDE_INDEPENDENT_CORE_SCOPE` | 27 |
| `CONCATENATED_PAGE_UI_OR_TOC` | 24 |
| `STORE_BRAND_WRAPPER_NOT_SEMANTIC_IDENTITY` | 22 |
| `BIBLIOGRAPHIC_OR_CITATION_METADATA` | 20 |
| `AUTHOR_WRAPPER_OR_BIBLIOGRAPHIC_TITLE` | 19 |
| `FOREIGN_MEDIA_OR_TOY_COLLISION` | 16 |
| `NON_COMPACT_OR_NON_TOPICAL_BREADCRUMB` | 10 |
| `PROMOTIONAL_OR_SUBSCRIPTION_UI` | 4 |
| `SITE_OR_BRAND_WRAPPER_NOT_SEMANTIC_IDENTITY` | 1 |
| `SENTENCE_OR_CLAIM_NOT_STABLE_SEMANTIC_DIRECTION` | 1 |

`body_text_blocks` and `full_visible_main_text` were read as evidence context,
not iterated as automatic candidate sources. This is the producer correction:
raw page prose is not itself a candidate stream. The immutable page evidence
remains the source authority.

## 4. Candidate reconciliation totals

| Reconciliation status | Identities |
|---|---:|
| `ALREADY_PRESENT` | 52 |
| `AMBIGUOUS` | 98 |
| `NEW_CANDIDATE` | 1540 |
| `OUT_OF_SCOPE` | 474 |
| `POSSIBLE_VARIANT` | 8 |

| Step08 route label | Identities |
|---|---:|
| `AUDIT_ONLY_ALREADY_PRESENT` | 52 |
| `ELIGIBLE_NEW_CANDIDATE` | 1540 |
| `ELIGIBLE_POSSIBLE_VARIANT` | 8 |
| `EXCLUDED_OUT_OF_SCOPE` | 474 |
| `HOLD_AMBIGUOUS` | 98 |

Step08 route is declarative only. No candidate is claimed as proven demand.

Candidate/source/provenance reconciliation:

```text
UNIQUE_CANDIDATE_IDS = 2172 / 2172
UNIQUE_SOURCE_URL_IDS = 1976 / 1976
UNIQUE_PROVENANCE_IDS = 3948 / 3948
EVERY_CANDIDATE_HAS_PROVENANCE = true
CANDIDATE_DISTINCT_AUTHORITY_COUNTS_RECONCILE = true
CANDIDATE_DISTINCT_SOURCE_URL_COUNTS_RECONCILE = true
CANDIDATE_PROVENANCE_ROW_COUNTS_RECONCILE = true
PROVENANCE_SOURCE_URL_FOREIGN_KEYS_RESOLVE = 3948 / 3948
PROVENANCE_CANDIDATE_FOREIGN_KEYS_RESOLVE = 3948 / 3948
```

## 5. Existing 686-identity old→new transition matrix

| FROM_STATUS | TO_STATUS | ROW_COUNT |
|---|---|---:|
| `ALREADY_PRESENT` | `ALREADY_PRESENT` | 10 |
| `AMBIGUOUS` | `AMBIGUOUS` | 23 |
| `AMBIGUOUS` | `OUT_OF_SCOPE` | 43 |
| `NEW_CANDIDATE` | `AMBIGUOUS` | 6 |
| `NEW_CANDIDATE` | `NEW_CANDIDATE` | 110 |
| `NEW_CANDIDATE` | `OUT_OF_SCOPE` | 284 |
| `OUT_OF_SCOPE` | `AMBIGUOUS` | 61 |
| `OUT_OF_SCOPE` | `OUT_OF_SCOPE` | 146 |
| `POSSIBLE_VARIANT` | `AMBIGUOUS` | 2 |
| `POSSIBLE_VARIANT` | `OUT_OF_SCOPE` | 1 |

```text
EXISTING_NORMALIZED_IDENTITIES_RETAINED = 686
EXISTING_STATUS_UNCHANGED = 289
EXISTING_STATUS_RECLASSIFIED = 397
EXISTING_IDENTITIES_SUPERSEDED = 0
EXISTING_IDS_UNCHANGED_AFTER_DETERMINISTIC_RESORT = 0
EXISTING_IDS_REGENERATED_AFTER_DETERMINISTIC_RESORT = 686
SILENT_EXISTING_PROVENANCE_LOSS = 0
```

## 6. Known producer-regression examples

| Candidate | Attempt 1 | Rework | Route |
|---|---|---|---|
| 10 схем вышивки крестиком для дизайна детской | `NEW_CANDIDATE` | `OUT_OF_SCOPE` | `EXCLUDED_OUT_OF_SCOPE` |
| [Муров:] Добрые люди обещали мне никогда не снимать с него [сына] медальона. | `NEW_CANDIDATE` | `OUT_OF_SCOPE` | `EXCLUDED_OUT_OF_SCOPE` |
| amuletum, с араб.]. | `NEW_CANDIDATE` | `OUT_OF_SCOPE` | `EXCLUDED_OUT_OF_SCOPE` |
| amuletum] | `NEW_CANDIDATE` | `OUT_OF_SCOPE` | `EXCLUDED_OUT_OF_SCOPE` |
| А на груди висел серебряный медальон в виде перевёрнутой пентаграммы. | `NEW_CANDIDATE` | `OUT_OF_SCOPE` | `EXCLUDED_OUT_OF_SCOPE` |
| Антон Платов, «Славянские руны», 2001 г. | `NEW_CANDIDATE` | `OUT_OF_SCOPE` | `EXCLUDED_OUT_OF_SCOPE` |

These examples are assertions over the general producer rules; they were not
used as a manual patch list.

## 7. Hard QA

| # | Invariant | Result | Evidence |
|---:|---|---|---|
| 1 | `ONLY_AUTHORIZED_COMPETITORS` | **PASS** | All URL/provenance/coverage authority IDs resolve to the frozen 32-row universe. |
| 2 | `ALL_32_COMPETITORS_ACCOUNTED` | **PASS** | coverage rows=32; exact S07A001..S07A032 set. |
| 3 | `ARBITRARY_TOP_N_OR_SAMPLE` | **PASS** | 0; all 1,976 URLs and 725 page-evidence rows processed. |
| 4 | `RUNTIME_PROXY_FAILURE_MISTAKEN_FOR_SOURCE_CLOSURE` | **PASS** | 0; canonical recovery supersedes Attempt-1 runtime failures. |
| 5 | `CANONICAL_BROWSER_RECOVERY_REMOTE_ACCEPTANCE` | **PASS** | Five recorded SHA-256 identities match; the residual file matches the exact accepted Git blob and its one-nibble SHA metadata typo is disclosed above. |
| 6 | `FULL_EXISTING_686_CANDIDATE_UNIVERSE_REEVALUATED` | **PASS** | 686/686 identities transition-accounted. |
| 7 | `FULL_EXISTING_1417_PROVENANCE_UNIVERSE_REEVALUATED` | **PASS** | 1,417/1,417 rows preserved and reclassified. |
| 8 | `KNOWN_BAD_EXAMPLES_NO_LONGER_ROUTE_AS_NEW_CANDIDATE` | **PASS** | 6/6 assertions pass; eligible routes=0. |
| 9 | `GENERIC_UI_NOISE_ROUTED_AS_STEP08_CANDIDATE` | **PASS** | 0 by producer rule and regression scan. |
| 10 | `BIBLIOGRAPHIC_METADATA_ROUTED_AS_STEP08_CANDIDATE` | **PASS** | 0 by producer rule and regression scan. |
| 11 | `LITERARY_EXAMPLE_SENTENCE_ROUTED_AS_STEP08_CANDIDATE` | **PASS** | 0 by producer rule and regression scan. |
| 12 | `BROKEN_TEXT_FRAGMENT_ROUTED_AS_STEP08_CANDIDATE` | **PASS** | 0 by producer rule and regression scan. |
| 13 | `LONG_FORM_DERIVED_CANDIDATES_HAVE_EXPLICIT_REPRODUCIBLE_TRANSFORMATION` | **PASS** | Every promoted occurrence records exact field, ordinal, rule and detail. |
| 14 | `RAW_WORDING_SOURCE_CONTEXT_PRESERVED` | **PASS** | Old 1,417 raw rows retained; every new provenance row stores raw field wording and evidence locator. |
| 15 | `OLD_TO_NEW_STATUS_TRANSITION_MATRIX_PRESENT` | **PASS** | Complete 686-row matrix above. |
| 16 | `SILENT_PROVENANCE_LOSS` | **PASS** | 0; total provenance=1,417+2531. |
| 17 | `SCHEMA_REQUIRED_FIELD_COMPLIANCE` | **PASS** | All four CSVs emitted in exact frozen field order with nonblank fallbacks. |
| 18 | `PRIMARY_AND_COMPARISON_KEYS_UNIQUE` | **PASS** | candidates=2172; URLs=1,976; provenance=3948. |
| 19 | `ALL_FOREIGN_KEYS_RESOLVE` | **PASS** | Candidate, source URL and authority references resolve. |
| 20 | `CANDIDATE_SOURCE_COUNTS_EQUAL_PROVENANCE` | **PASS** | Counts regenerated from final occurrence ledger. |
| 21 | `DISCOVERED_URL_TERMINAL_RECONCILIATION` | **PASS** | 32/32 equalities; unresolved=0; execution-environment failure=0. |
| 22 | `STEP08_ELIGIBILITY_STATUS_CONSISTENCY` | **PASS** | Only NEW_CANDIDATE/POSSIBLE_VARIANT have eligible route labels. |
| 23 | `DEMAND_NOT_ASSERTED` | **PASS** | All candidates are NOT_VALIDATED_STEP07. |
| 24 | `NO_FINAL_INTENT_CLUSTER_OR_PAGE_DECISIONS` | **PASS** | Frozen stop-state fields and no page decision fields. |
| 25 | `STEP08_PROVIDER_CALLS` | **PASS** | 0. |
| 26 | `ACCEPTED_BROWSER_RECOVERY_FILES_UNCHANGED` | **PASS** | Exact preflight SHA-256 identities rechecked before materialization. |
| 27 | `QA_SELF_CONSISTENCY_SIX_FILE_HANDOFF` | **PASS** | Exactly six replacement files; no stale seven-file wording. |

```text
HARD_GATE_FAILURES = 0
NO_OPEN_CRITICAL_DEFECT = true
```

## 8. Universal quality score

| Dimension | Score /10 | Basis |
|---|---:|---|
| Goal and output completeness | 10 | Full affected universe and accepted recovery unit processed. |
| Method and source support | 10 | Frozen authority, schema and canonical recovery used without acquisition. |
| Input evidence and provenance integrity | 10 | Immutable raw wording and exact recovery hashes retained. |
| Coverage and completeness | 10 | 32/32 competitors, 1,976/1,976 URLs, 725/725 evidence rows. |
| Analytical correctness and claim boundaries | 9 | Strict independent-direction producer; claims remain competitor language only. |
| Adversarial QA quality | 10 | Producer regressions, transitions, schema, FK and accounting gates pass. |
| Persistence/readback/reproducibility | 10 | Deterministic sort/IDs and exact evidence locators. |
| Owner/client usability/plain language | 9 | Single six-file replacement package and explicit boundary report. |
| Information gain/cost/execution efficiency | 10 | Zero provider/browser calls; accepted evidence reused once. |
| Downstream readiness | 10 | Step08 queue is cleanly bounded but not executed. |

```text
QUALITY_TOTAL = 98 / 100
QUALITY_SCORE = 9.8 / 10
HARD_FAILURE_OVERRIDE = false
```

## 9. Stop boundaries

```text
NEW_WORDSTAT_CALLS = 0
NEW_YANDEX_SEARCH_CALLS = 0
NEW_AI_SEARCH_OR_GENSEARCH_CALLS = 0
STEP08_STARTED = false
FINAL_INTENT_DECISIONS = NONE
FINAL_CLUSTER_DECISIONS = NONE
FINAL_PAGE_DECISIONS = NONE
WORK_GITHUB_COMMIT_PUSH_PR = false
OWNER_UPLOAD_COMPLETE = false
REMOTE_READBACK_PASS = false
MAIN_CHAT_ACCEPTANCE = PENDING
```
