# KW-002 / BLOOD & SAND — STEP07 FINAL MANUAL-WORK WRAPPER FULL-VOLUME CORRECTION R2 QA

Date: 2026-09-18
Action: `STEP07_FINAL_MANUAL_WORK_WRAPPER_FULL_VOLUME_CORRECTION_R2`
Work start remote HEAD: `2a266dec29c01bf6d7d15e34ed55cdd6ff28be42`
Pre-publication remote HEAD: `2a266dec29c01bf6d7d15e34ed55cdd6ff28be42`
Authority drift: **NONE**
Overall hard QA: **PASS**
Step result: **PASS_FULL_VOLUME_MANUAL_WORK_WRAPPER_CORRECTION_R2**

## 1. Exact final report

```text
WORK_START_REMOTE_HEAD = 2a266dec29c01bf6d7d15e34ed55cdd6ff28be42
WORK_PRE_PUBLICATION_REMOTE_HEAD = 2a266dec29c01bf6d7d15e34ed55cdd6ff28be42
AUTHORITY_DRIFT_STATUS = NONE
STEP07_FINAL_MANUAL_WORK_WRAPPER_STATUS = PASS_FULL_VOLUME_MANUAL_WORK_WRAPPER_CORRECTION_R2

TARGET_CANDIDATES_REVIEWED = 794/794
TARGET_PROVENANCE_REVIEWED = 1060/1060
TARGET_SILENT_SKIP = 0
OLD_STEP08_ELIGIBLE = 794
NEW_STEP08_ELIGIBLE = 794

TRANSFORMED_DERIVED_COUNT = 5
OUT_OF_SCOPE_DELTA = 0
AMBIGUOUS_DELTA = 0
ALREADY_PRESENT_DELTA = 0
NORMALIZED_DUPLICATE_DELTA = 0

KNOWN_MANUAL_WORK_REGRESSION_ROWS_CORRECTED = 4/4
GENERIC_MANUAL_WORK_WRAPPER_HITS_AFTER = 0
DELIBERATELY_RETAINED_MANUAL_WORK_SEMANTIC_ROWS = 0

HARD_GATE_FAILURES = 0
OPEN_CRITICAL_DEFECTS = 0
QUALITY_TOTAL = 99/100
QUALITY_SCORE = 9.9/10

NEW_BROWSER_CALLS = 0
NEW_PROVIDER_CALLS = 0
STEP08_STARTED = false
WORK_GITHUB_COMMIT_PUSH_PR = false
MAIN_CHAT_ACCEPTANCE = PENDING
```

## 2. Full-volume execution accounting

```text
CURRENT_CANDIDATE_UNIVERSE_LOADED = 2172/2172
CURRENT_PROVENANCE_UNIVERSE_LOADED = 3948/3948
TARGET_CANDIDATES_REVIEWED = 794/794
TARGET_PROVENANCE_REVIEWED = 1060/1060
TARGET_CANDIDATES_SILENTLY_SKIPPED = 0
ALL_TARGET_PROVENANCE_REVIEWED = true

RETAINED_AS_IS = 789
TRANSFORMED_DERIVED = 5
RECLASSIFIED_OUT_OF_SCOPE = 0
RECLASSIFIED_AMBIGUOUS = 0
ALREADY_PRESENT_AFTER_RECONCILIATION = 0
NORMALIZED_DUPLICATE_AFTER_RECONCILIATION = 0
REMAINING_STEP08_ELIGIBLE = 794
```

All 794 eligible identities and all 1,060 linked evidence rows received an R2
review receipt. The full manual-work lexical family was tested against candidate
wording and immutable provenance evidence. Source multiplicity remained a
confidence signal only.

Review-register SHA-256: `3a497e5f5379bb98f78663f9ef695481dfe0e2f7909bc6aa59d3ca2ed2d0483a`
Linked-provenance-register SHA-256: `88af1430f8b7e24fe3aa207321c43519523f9d5e8cc034faf93574d621d9adf5`

### Old 794 → new status transition matrix

| FROM_STATUS | TO_STATUS | ROW_COUNT |
|---|---|---:|
| `NEW_CANDIDATE` | `NEW_CANDIDATE` | 787 |
| `POSSIBLE_VARIANT` | `POSSIBLE_VARIANT` | 7 |

### Final Step08-eligible candidates by type

| CANDIDATE_TYPE | COUNT |
|---|---:|
| `ATTRIBUTE` | 8 |
| `INFORMATIONAL_FORMULATION` | 55 |
| `PRODUCT_NAME` | 411 |
| `SUBCATEGORY` | 74 |
| `TERMINOLOGY` | 236 |
| `USE_CASE` | 10 |

### Final Step08-eligible candidates by source-count band

| DISTINCT COMPETITOR SOURCES | COUNT |
|---|---:|
| 1 | 756 |
| 2 | 22 |
| 3 | 14 |
| 4+ | 2 |

```text
SINGLE_SOURCE_FINAL = 756
MULTI_SOURCE_FINAL = 38
```

## 3. Corrected wrapper rows

| CANDIDATE_ID | BEFORE | AFTER | TRANSFORMATION | FINAL_STATUS | FINAL_ROUTE |
|---|---|---|---|---|---|
| `S07C001277` | Славянский оберег "Велес" ручная работа, бронза | Славянский оберег "Велес", бронза | `LISTING_MANUAL_WORK_WRAPPER_REMOVAL` | `NEW_CANDIDATE` | `ELIGIBLE_NEW_CANDIDATE` |
| `S07C001280` | Славянский оберег "Звезда Инглии" ручная работа, бронза | Славянский оберег "Звезда Инглии", бронза | `LISTING_MANUAL_WORK_WRAPPER_REMOVAL` | `NEW_CANDIDATE` | `ELIGIBLE_NEW_CANDIDATE` |
| `S07C001282` | Славянский оберег "Звезда Лады" ручная работа, бронза | Славянский оберег "Звезда Лады", бронза | `LISTING_MANUAL_WORK_WRAPPER_REMOVAL` | `NEW_CANDIDATE` | `ELIGIBLE_NEW_CANDIDATE` |
| `S07C001291` | Славянский оберег "Лунница" малая, ручная работа, бронза | Славянский оберег "Лунница" малая, бронза | `LISTING_MANUAL_WORK_WRAPPER_REMOVAL` | `NEW_CANDIDATE` | `ELIGIBLE_NEW_CANDIDATE` |
| `S07C001541` | Талисман «Ловец удачи» Автор – Natalie | Талисман «Ловец удачи» | `LISTING_SELLER_ATTRIBUTION_REMOVAL` | `NEW_CANDIDATE` | `ELIGIBLE_NEW_CANDIDATE` |

The four required manual-work regressions were reduced by deleting only the
detachable `ручная работа` wrapper. Bronze remains as a supported material
attribute; `малая` remains for the explicit qualitative size variant. The
full-volume pass also found and removed one seller attribution from
`S07C001541`. All five compact forms are literal source-supported reductions,
remain within the frozen business scope, and collide with neither the complete
2,172-candidate universe nor the accepted upstream semantic universe.

```text
KNOWN_MANUAL_WORK_REGRESSION_ROWS = 4/4 CORRECTED
ADDITIONAL_SELLER_WRAPPER_ROWS_CORRECTED = 1
UNSUPPORTED_DERIVATIONS = 0
EXISTING_IDENTITY_DUPLICATION = 0
```

## 4. Deliberately retained manual-work semantic rows

None.

```text
DELIBERATELY_RETAINED_MANUAL_WORK_SEMANTIC_ROWS = 0
GENERIC_MANUAL_WORK_WRAPPER_HITS_AFTER = 0
UNJUSTIFIED_MANUAL_WORK_RETAINED = 0
```

Manual-work wording still occurs only in immutable raw/source evidence or in
already excluded audit rows; it does not survive in any Step08-eligible
candidate wording.

## 5. Full-volume regression matrix

| REGRESSION_CLASS | EVIDENCE | RESULT |
|---|---|---|
| `LISTING_MANUAL_WORK_WRAPPER` | Full lexical family; eligible hits after=0 | PASS |
| `LISTING_SELLER_FLUFF` | Author/seller attribution eligible hits after=0 | PASS |
| `LISTING_AVAILABILITY_WRAPPER` | eligible hits after=0 | PASS |
| `LISTING_PRICE_PHOTO_WRAPPER` | eligible hits after=0 | PASS |
| `LISTING_DIMENSION_NOISE` | numeric listing-measurement hits after=0 | PASS |
| `LISTING_CONDITION_NOISE` | condition/defect hits after=0 | PASS |
| `COMPETITOR_BRAND_WRAPPER` | eligible hits after=0 | PASS |
| `OVERSPECIFIED_MARKETPLACE_TITLE` | unresolved wrapper-only title hits after=0 | PASS |
| `UNSUPPORTED_COMPACT_DERIVATION` | five literal reductions; unsupported=0 | PASS |
| `EXISTING_IDENTITY_DUPLICATION` | normalized comparison keys unique=2,172/2,172 | PASS |
| `BUSINESS_SCOPE_LEAKAGE` | newly introduced or retained unrelated routes=0 | PASS |
| `EFFICACY_CLAIM_COPY` | client-fact assertions introduced=0 | PASS |

```text
LISTING_MANUAL_WORK_WRAPPER_HITS_AFTER = 0
LISTING_SELLER_FLUFF_HITS_AFTER = 0
LISTING_AVAILABILITY_WRAPPER_HITS_AFTER = 0
LISTING_PRICE_PHOTO_WRAPPER_HITS_AFTER = 0
LISTING_DIMENSION_NOISE_HITS_AFTER = 0
LISTING_CONDITION_NOISE_HITS_AFTER = 0
COMPETITOR_BRAND_WRAPPER_HITS_AFTER = 0
BUSINESS_SCOPE_LEAKAGE = 0
UNSUPPORTED_DERIVATIONS = 0
EXISTING_IDENTITY_DUPLICATION = 0
CLAIM_LANGUAGE_TREATED_AS_CLIENT_FACT = 0
```

## 6. Independent mechanical and preservation QA

| INVARIANT | EVIDENCE | RESULT |
|---|---|---|
| `SCHEMA_COMPLIANCE` | exact four canonical headers; required fields/enums valid | PASS |
| `PRIMARY_KEYS_UNIQUE` | 2,172 candidates; 1,976 URLs; 3,948 provenance rows | PASS |
| `NORMALIZED_COMPARISON_KEYS_UNIQUE` | 2,172/2,172 | PASS |
| `FOREIGN_KEYS_RESOLVE` | candidate, URL, and authority references | PASS |
| `CANDIDATE_SOURCE_COUNTS_RECONCILE` | 2,172/2,172 | PASS |
| `STEP08_ROUTE_CONSISTENCY` | 2,172/2,172 | PASS |
| `DEMAND_VALIDATION_STATE` | `NOT_VALIDATED_STEP07` for 2,172/2,172 | PASS |
| `RAW_WORDING_IMMUTABLE` | 3,948/3,948 | PASS |
| `SOURCE_CONTEXT_IMMUTABLE` | 3,948/3,948 | PASS |
| `NON_TARGET_CANDIDATES_UNCHANGED` | 1,378/1,378 | PASS |
| `NON_TARGET_PROVENANCE_UNCHANGED` | 2,888/2,888 | PASS |
| `SOURCE_URL_LEDGER_UNCHANGED` | SHA-256 exact | PASS |
| `COMPETITOR_COVERAGE_LEDGER_UNCHANGED` | SHA-256 exact | PASS |
| `NEW_BROWSER_OR_PROVIDER_CALLS` | 0 | PASS |
| `STEP08_STARTED` | false | PASS |

```text
SCHEMA_COMPLIANCE = PASS
PRIMARY_KEYS_UNIQUE = PASS
FOREIGN_KEYS_RESOLVE = PASS
CANDIDATE_SOURCE_COUNTS_RECONCILE = PASS
STEP08_ROUTE_CONSISTENCY = PASS
DEMAND_VALIDATION_STATE = NOT_VALIDATED_STEP07 FOR ALL
RAW_WORDING_IMMUTABLE = true
SOURCE_CONTEXT_IMMUTABLE = true
HARD_GATE_FAILURES = 0
OPEN_CRITICAL_DEFECTS = 0
```

## 7. Top eligible competitor sources after correction

| RANK | COMPETITOR_DOMAIN | DISTINCT ELIGIBLE CANDIDATES |
|---:|---|---:|
| 1 | `livemaster.ru` | 307 |
| 2 | `slavyanskieoberegi.ru` | 90 |
| 3 | `avito.ru` | 84 |
| 4 | `xn--80aejvmu5h.xn--80aswg` | 65 |
| 5 | `kartaslov.ru` | 39 |
| 6 | `wildberries.ru` | 34 |
| 7 | `ru.wikipedia.org` | 34 |
| 8 | `happywitch.ru` | 33 |
| 9 | `simvolroda.ru` | 27 |
| 10 | `actro.online` | 26 |
| 11 | `lunaro.ru` | 16 |
| 12 | `goroskop365.ru` | 15 |

## 8. Changed and immutable artifacts

Changed canonical files:

- `COMPETITOR_GAP_CANDIDATES.csv`
- `STEP07_CANDIDATE_PROVENANCE_LEDGER.csv`
- `STEP07_EXECUTION_QA.md`
- `STEP07_EXECUTION_HANDOFF_MANIFEST.json`

`STEP07_SOURCE_URL_LEDGER.csv`, `STEP07_COMPETITOR_COVERAGE_LEDGER.csv`, all
browser-recovery evidence, `JOB_FLOW.md`, and execution cursors remain unchanged.

```text
COMPETITOR_GAP_CANDIDATES_SHA256 = 706ef4b08b25807840427b53ac6a8222bd49fd8b3752a732e319fd39823f6eef
STEP07_CANDIDATE_PROVENANCE_LEDGER_SHA256 = d50bab24c96f7cf715197ca5c8ace65dc4c976945826521808bba64734cb789c
STEP07_SOURCE_URL_LEDGER_SHA256 = f923c412f00fdb318bd57c0610ca404d8093a3a7cad4d7c71e2c31e86de568f7
STEP07_COMPETITOR_COVERAGE_LEDGER_SHA256 = 0ee233a792d9e97b1b3d45fe051ce2068f261fd0b53dc1408b6cd7345483c898
```

## 9. Universal quality score

| DIMENSION | SCORE / 10 | BASIS |
|---|---:|---|
| Goal and output completeness | 10 | All required canonical outputs materialized. |
| Method and source support | 10 | Frozen business authority and accepted Step07 corpus only. |
| Input evidence and provenance integrity | 10 | Raw wording and context immutable; transformations explicit. |
| Coverage and completeness | 10 | 794/794 and 1,060/1,060 reviewed; zero silent skips. |
| Analytical correctness and claim boundaries | 10 | Minimal literal reductions; no efficacy claim promoted to client fact. |
| Adversarial QA quality | 10 | Manual family and all active wrapper gates rerun. |
| Persistence/readback/reproducibility | 10 | Stable IDs, evidence hashes, transition matrix, and exact hashes recorded. |
| Owner/client usability/plain language | 9 | One atomic four-file package and one transport ZIP. |
| Information gain/cost/execution efficiency | 10 | No acquisition or provider calls. |
| Downstream readiness | 10 | Corrected 794-candidate queue; Step08 not started. |

```text
QUALITY_TOTAL = 99/100
QUALITY_SCORE = 9.9/10
PASS_THRESHOLD = >=90/100 AND ALL HARD GATES PASS
QUALITY_GATE = PASS
```
