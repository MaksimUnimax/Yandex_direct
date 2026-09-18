# KW-002 / BLOOD & SAND — STEP07 FINAL WRAPPER-NOISE FULL-VOLUME CORRECTION QA

Date: 2026-09-18
Action: `STEP07_FINAL_WRAPPER_NOISE_FULL_VOLUME_CORRECTION`
Work start remote HEAD: `dedf5a4680c0c91f8ffb349c8260a9e150b4041a`
Pre-publication remote HEAD: `dedf5a4680c0c91f8ffb349c8260a9e150b4041a`
Authority drift: **NONE**
Overall hard QA: **PASS**
Step result: **PASS_FULL_VOLUME_WRAPPER_NOISE_CORRECTION**

## 1. Exact final report

```text
WORK_START_REMOTE_HEAD = dedf5a4680c0c91f8ffb349c8260a9e150b4041a
WORK_PRE_PUBLICATION_REMOTE_HEAD = dedf5a4680c0c91f8ffb349c8260a9e150b4041a
AUTHORITY_DRIFT_STATUS = NONE
STEP07_FINAL_WRAPPER_CORRECTION_STATUS = PASS_FULL_VOLUME_WRAPPER_NOISE_CORRECTION

TARGET_CANDIDATES_REVIEWED = 794/794
TARGET_PROVENANCE_REVIEWED = 1060/1060
TARGET_SILENT_SKIP = 0
OLD_STEP08_ELIGIBLE = 794
NEW_STEP08_ELIGIBLE = 794

TRANSFORMED_DERIVED_COUNT = 1
OUT_OF_SCOPE_DELTA = 0
AMBIGUOUS_DELTA = 0
ALREADY_PRESENT_DELTA = 0
NORMALIZED_DUPLICATE_DELTA = 0

LISTING_MANUAL_WORK_WRAPPER_HITS_AFTER = 0
LISTING_AVAILABILITY_WRAPPER_HITS_AFTER = 0
LISTING_PRICE_PHOTO_WRAPPER_HITS_AFTER = 0
LISTING_DIMENSION_NOISE_HITS_AFTER = 0
LISTING_CONDITION_NOISE_HITS_AFTER = 0
COMPETITOR_BRAND_WRAPPER_HITS_AFTER = 0

SCHEMA_COMPLIANCE = PASS
PRIMARY_KEYS_UNIQUE = PASS
FOREIGN_KEYS_RESOLVE = PASS
CANDIDATE_SOURCE_COUNTS_RECONCILE = PASS
STEP08_ROUTE_CONSISTENCY = PASS
DEMAND_VALIDATION_STATE = NOT_VALIDATED_STEP07 FOR ALL

HARD_GATE_FAILURES = 0
OPEN_CRITICAL_DEFECTS = 0
QUALITY_TOTAL = 99/100
QUALITY_SCORE = 9.9/10

NEW_BROWSER_CALLS = 0
NEW_CRAWL = 0
NEW_WORDSTAT_CALLS = 0
NEW_YANDEX_SEARCH_CALLS = 0
NEW_AI_SEARCH_OR_GENSEARCH_CALLS = 0
NEW_PROVIDER_CALLS = 0
STEP08_STARTED = false
WORK_GITHUB_COMMIT_PUSH_PR = false
MAIN_CHAT_ACCEPTANCE = PENDING
```

## 2. Full-volume correction accounting

```text
CURRENT_CANDIDATE_UNIVERSE_LOADED = 2172/2172
CURRENT_PROVENANCE_UNIVERSE_LOADED = 3948/3948
TARGET_CANDIDATES_REVIEWED = 794/794
TARGET_PROVENANCE_REVIEWED = 1060/1060
TARGET_CANDIDATES_SILENTLY_SKIPPED = 0
ALL_TARGET_PROVENANCE_REVIEWED = true

RETAINED_AS_IS = 793
TRANSFORMED_DERIVED = 1
RECLASSIFIED_OUT_OF_SCOPE = 0
RECLASSIFIED_AMBIGUOUS = 0
ALREADY_PRESENT_AFTER_RECONCILIATION = 0
NORMALIZED_DUPLICATE_AFTER_RECONCILIATION = 0
REMAINING_STEP08_ELIGIBLE = 794
```

Every current eligible identity received a new review receipt. Every linked raw
wording and source context row was read and hashed into that receipt. Source
multiplicity remained a confidence signal only.

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

## 3. Corrected false negative

| CANDIDATE_ID | BEFORE | AFTER | TRANSFORMATION | FINAL_STATUS | FINAL_ROUTE |
|---|---|---|---|---|---|
| `S07C000567` | Кулон кованый "Молот Тора" ручной работы | Кулон кованый "Молот Тора" | `UI_NOISE_REMOVAL` | `NEW_CANDIDATE` | `ELIGIBLE_NEW_CANDIDATE` |

The correction removes only the explicit trailing marketplace wrapper
`ручной работы`. The literal product phrase and the meaningful forged-product
attribute remain. The compact wording does not collide with any of the 2,172
current candidate identities or the accepted upstream semantic universe.

```text
S07C000567_RETAINED_AS_IS = false
S07C000567_RAW_WORDING_IMMUTABLE = true
UNSUPPORTED_DERIVATIONS = 0
EXISTING_IDENTITY_DUPLICATION = 0
```

## 4. Wrapper-signal decision accounting

The hard-gate hit counts below are semantic defect counts, not raw token counts.
All token matches were reviewed against wording plus every linked provenance row.

| DECISION_RULE | TARGETS | RESULT |
|---|---:|---|
| `LISTING_MANUAL_WORK_WRAPPER_REMOVAL` | 1 | S07C000567 compacted; PASS |
| `MATERIAL_SEMANTIC_ATTRIBUTE_RETAINED` | 4 | Handmade bronze product variants are explicit searchable attributes; PASS |
| `MATERIAL_SIZE_ATTRIBUTE_RETAINED` | 2 | Qualitative product-size variants, not numeric listing measurements; PASS |
| `PRODUCT_VARIANT_ATTRIBUTE_RETAINED` | 4 | Authentic/antique/used-horseshoe variant meaning retained; PASS |
| `TRANSACTIONAL_SEMANTIC_FORMULATION_RETAINED` | 8 | Independently meaningful transactional directions; no price/photo or brand wrapper; PASS |
| `NO_UNJUSTIFIED_WRAPPER_OR_LISTING_NOISE` | 775 | No removable wrapper/noise component found; PASS |

The four remaining literal `ручная работа` token rows are S07C001277,
S07C001280, S07C001282, and S07C001291. In each row the wording is an integrated
handmade bronze product variant, not a detachable seller suffix. This is the
contract's material-semantic-attribute exception, recorded explicitly rather
than a regex exemption.

## 5. Full-volume regression matrix

| REGRESSION_CLASS | EVIDENCE | RESULT |
|---|---|---|
| `LISTING_MANUAL_WORK_WRAPPER` | S07C000567 transformed; unresolved semantic hits=0 | PASS |
| `LISTING_AVAILABILITY_WRAPPER` | eligible hits=0 | PASS |
| `LISTING_PRICE_PHOTO_WRAPPER` | eligible price/photo wrapper hits=0 | PASS |
| `LISTING_DIMENSION_NOISE` | eligible numeric measurement-noise hits=0 | PASS |
| `LISTING_CONDITION_NOISE` | eligible condition/defect hits=0 | PASS |
| `LISTING_SELLER_FLUFF` | unresolved detachable seller-fluff hits=0 | PASS |
| `COMPETITOR_BRAND_WRAPPER` | eligible hits=0 | PASS |
| `OVERSPECIFIED_MARKETPLACE_TITLE` | unresolved wrapper-only titles=0 | PASS |
| `UNSUPPORTED_COMPACT_DERIVATION` | one literal derivation; unsupported=0 | PASS |
| `EXISTING_IDENTITY_DUPLICATION` | duplicate normalized keys=0 | PASS |
| `BUSINESS_SCOPE_LEAKAGE` | unrelated product/service routes=0 | PASS |
| `EFFICACY_CLAIM_COPY` | client-fact assertions=0 | PASS |

```text
LISTING_DIMENSION_CONDITION_NOISE_ELIGIBLE_HITS = 0
PAGE_WRAPPER_ELIGIBLE_HITS = 0
UNSUPPORTED_DERIVATIONS = 0
BUSINESS_SCOPE_LEAKAGE = 0
```

## 6. Independent mechanical and preservation QA

| INVARIANT | EVIDENCE | RESULT |
|---|---|---|
| `SCHEMA_COMPLIANCE` | exact 4/4 headers; required fields and enums valid | PASS |
| `PRIMARY_KEYS_UNIQUE` | 2,172 candidates; 1,976 URLs; 3,948 provenance rows | PASS |
| `NORMALIZED_COMPARISON_KEYS_UNIQUE` | 2,172/2,172 | PASS |
| `FOREIGN_KEYS_RESOLVE` | candidate, URL, and authority references | PASS |
| `CANDIDATE_SOURCE_COUNTS_RECONCILE` | 2,172/2,172 | PASS |
| `STEP08_ROUTE_CONSISTENCY` | 2,172/2,172 | PASS |
| `DEMAND_VALIDATION_STATE` | `NOT_VALIDATED_STEP07` for 2,172/2,172 | PASS |
| `RAW_WORDING_AND_CONTEXT_IMMUTABLE` | 3,948/3,948 | PASS |
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

`STEP07_SOURCE_URL_LEDGER.csv`, `STEP07_COMPETITOR_COVERAGE_LEDGER.csv`, and all
seven accepted browser-recovery evidence files remain byte-unchanged. Provenance
replacement is required because the corrected derivation and 794/1,060 review
receipts are materialized there; raw evidence fields did not change.

```text
COMPETITOR_GAP_CANDIDATES_SHA256 = 6e6f8593ff20c429e8377d29aba5445790e6cc8f0613e316c7a171e195443ee4
STEP07_CANDIDATE_PROVENANCE_LEDGER_SHA256 = 2b200b4d90e034f7fbdff8ea779187b279f5a130f2d3d90da4ba339fdccff53c
STEP07_SOURCE_URL_LEDGER_SHA256 = f923c412f00fdb318bd57c0610ca404d8093a3a7cad4d7c71e2c31e86de568f7
STEP07_COMPETITOR_COVERAGE_LEDGER_SHA256 = 0ee233a792d9e97b1b3d45fe051ce2068f261fd0b53dc1408b6cd7345483c898
```

## 9. Universal quality score

| DIMENSION | SCORE / 10 | BASIS |
|---|---:|---|
| Goal and output completeness | 10 | All 794 targets and 1,060 linked evidence rows reviewed. |
| Method and source support | 10 | Frozen business authority and accepted Step07 corpus only. |
| Input evidence and provenance integrity | 10 | Raw wording/context immutable; explicit transformation ledgered. |
| Coverage and completeness | 10 | Zero silent skips; complete candidate/provenance universes reconciled. |
| Analytical correctness and claim boundaries | 10 | Wrapper removal is minimal; material attributes preserved; claims remain competitor evidence. |
| Adversarial QA quality | 10 | 12/12 required full-volume regression classes pass. |
| Persistence/readback/reproducibility | 10 | Decision rules, evidence hashes, stable IDs, and transition matrix recorded. |
| Owner/client usability/plain language | 9 | Four-file atomic replacement package and one transport ZIP. |
| Information gain/cost/execution efficiency | 10 | No acquisition/provider calls; accepted corpus reused. |
| Downstream readiness | 10 | Corrected 794-candidate Step08 queue; Step08 not started. |

```text
QUALITY_TOTAL = 99 / 100
QUALITY_SCORE = 9.9 / 10
PASS_THRESHOLD_MET = true
HARD_FAILURE_OVERRIDE = false
```

## 10. Stop boundaries

```text
NEW_BROWSER_CALLS = 0
NEW_CRAWL = 0
NEW_WORDSTAT_CALLS = 0
NEW_YANDEX_SEARCH_CALLS = 0
NEW_AI_SEARCH_OR_GENSEARCH_CALLS = 0
NEW_PROVIDER_CALLS = 0
STEP08_STARTED = false
FINAL_INTENT_DECISIONS = NONE
FINAL_CLUSTER_DECISIONS = NONE
FINAL_PAGE_DECISIONS = NONE
WORK_GITHUB_COMMIT_PUSH_PR = false
OWNER_UPLOAD_COMPLETE = false
REMOTE_READBACK_PASS = false
MAIN_CHAT_ACCEPTANCE = PENDING
```
