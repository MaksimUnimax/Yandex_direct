# STEP 05A.8 — INFORMATION GAIN AND FIRST-EXECUTION VALIDATION REPORT

Date: 2026-09-08  
Status: **DETERMINISTIC TECHNICAL QA PASS / OWNER REVIEW REQUIRED / METHOD NOT PROMOTED**

## 1. Executive result

The full preserved Step 5A.1–5A.7 chain produced material positive information gain with strong filtering value. Seven new in-scope directions survived Wordstat and current exact-query Search checks, yielding 16 union-compatible acquisition rows with zero normalized overlap against the live frozen 2,840-phrase baseline.

Technical execution supports **RECOMMEND_VALIDATE_AFTER_OWNER_REVIEW**. This is a recommendation only: **PROJECT_TEST_VALIDATED** remains false/pending owner review, Level 1 remains not promoted, and the client-usefulness gate is not self-certified.

## 2. Quantitative funnel

- Discovery: 75 preserved queries / 750 TOP10 rows / 237 normalized domains.
- Selection and inspection: 9 competitors / 44 target pages / 43 direct + 1 redirected accessible / 0 inaccessible.
- Page evidence: 92 candidate occurrences → 43 directions (46.74% consolidation yield; 49 repeat-support occurrences retained without inflating direction count).
- Page-level routing: 22/43 already covered; 14/43 Wordstat seeds; 3/43 off-scope; 4/43 held.
- Wordstat: 14/14 executions; 160 actual rows; 20/160 potentially new Search-recheck occurrences (12.50%).
- Search: 9 requirements; 7 successful; 2 outcome unknown and unretried.
- Direction decisions: 7/9 **ADD_TO_PIPELINE** (77.78%); 2/9 **HOLD_EVIDENCE** (22.22%).
- Phrase merge: 20 = 16 accepted + 3 close variants suppressed + 1 held; acceptance yield 80.00%.

Every percentage above is persisted with its named numerator and denominator in the metrics JSON and funnel TSV.

## 3. Expansion against the live frozen baseline

Verified directly against the current Stage-5 authority:

- unique phrases = 2,840;
- active phrases = 2,332;
- assigned phrases = 2,313;
- Search-required phrases = 19;
- canonical structural units = 168;
- accepted delta rows = 16;
- normalized exact overlap between delta and baseline = 0;
- duplicate normalized phrases inside delta = 0.

The 16-row delta equals 0.5634% of the unique baseline and 0.6861% of the active baseline. A simple projected total of 2,856 is arithmetic context only and applies only if all 16 rows survive the normal downstream pipeline. The delta remains **PROPAGATION_REQUIRED_BEFORE_NEXT_REAL_RELEASE**; it is not frozen truth yet.

## 4. Provider-cost efficiency

Preserved raw envelopes confirm:

- Wordstat = 0.280 RUB;
- Search = 4.392 RUB;
- total incremental provider cost = 4.672 RUB;
- total cost per final added direction = 0.6674 RUB;
- total cost per accepted delta row = 0.292 RUB;
- total cost per successfully resolved Search requirement = 0.6674 RUB;
- Search-only cost per successful requirement = 0.6274 RUB.

These are descriptive incremental COGS. They exclude any cost not preserved in the Step 5A Wordstat/Search envelopes and are not a quality target or a reason to reject useful evidence.

## 5. Filtering and de-risking value

- 29/43 directions (67.44%) were already covered, off-scope, or held before Wordstat.
- 140/160 Wordstat rows (87.50%) were covered, noise, off-scope, or held rather than sent to Search.
- 4/20 potentially new occurrences (20.00%) were suppressed or held instead of inflating the delta.
- Two unknown Search outcomes remained holds; they were not converted to empty/failed SERPs.
- Website-text-as-ranking overclaim = 0.
- Full-competitor-keyword-universe overclaim = 0.

Therefore the method's value is not only the 16 additions: it also prevents duplicate, off-scope, noisy and unsupported promotion.

## 6. Selected-competitor visibility gain

- visible selected-competitor cells = 11/81 (13.58%);
- selected-competitor ranking rows = 12;
- unique selected competitors visible = 7/9 (77.78%): elit-balkon.ru, fabrikaokon.ru, i-okna.ru, mosokna.ru, msk.okna-servise.com, okna-germany.ru, oknafactoria.ru;
- selected competitors not observed in the seven successful exact rechecks: aluminarium.ru, okna-moskva.ru;
- exact matches to the 44 earlier inspected URLs = 0;
- same-domain/different-URL visible cells = 11 and ranking rows = 12;
- one added direction, “гидроизоляция для открытого балкона”, had zero selected competitors visible but still passed because Wordstat demand, current SERP intent/page mix, frozen business fit and semantic novelty jointly supported it.

The earlier page supplied topic/seed lineage only. Exact-query visibility claims come only from successful current Search rows.

## 7. Diminishing-information-gain assessment

1. Material new information: **YES** — 7 confirmed directions and 16 accepted occurrences.
2. Evidence mix: strong filtering (22/43 directions already covered; 140/160 Wordstat rows did not advance) with still-material in-scope novelty.
3. Permanent reusable saturation threshold: **NO** — one execution cannot establish a universal number of competitors/pages/seeds.
4. Stop this bounded rehearsal: **YES** — the authorized chain is complete, material additions are captured, two unresolved directions are safely held, and recursive expansion is not authorized.
5. Future varied rehearsal: measure marginal accepted directions/occurrences per additional bounded domain/page batch together with covered/noise/off-scope/hold shares and cost. Extend when a distinct batch still yields material in-scope additions; consider stopping earlier only after varied consecutive batches predominantly repeat or add noise.

**STOP_THIS_REHEARSAL = true** does not mean **PERMANENT_DIMINISHING_GAIN_THRESHOLD_VALIDATED = true**.

## 8. Level-1 Section 11 validation gates

| # | Gate | Status | Evidence fact |
|---:|---|---|---|
| 1 | `REAL_SEARCH_COMPETITOR_DISCOVERY_WORKS_IN_TARGET_REGION` | PASS | region=213; 75 queries; 750 TOP10 rows; 237 normalized domains; 9 selected competitors |
| 2 | `COMPETITOR_PAGE_TO_SEED_LINEAGE_IS_DURABLE` | PASS | 44/44 targets; 92 candidate occurrences; every candidate has page/evidence lineage; 43 deduplicated directions |
| 3 | `WORDSTAT_EXPANSION_ADDS_MEASURABLE_COVERAGE_OR_PROVES_NO_MATERIAL_GAP` | PASS | 14 executions; 160 returned rows; 20 potentially new occurrences; 7 Search-confirmed directions; 16 accepted delta rows |
| 4 | `RETURNED_WORDSTAT_ROWS_FULLY_PRESERVED_UNDER_STEP3_STEP5_SCHEMA` | PASS | 160/160 rows; 21 direct + 139 association; 0 fabricated rows; empty and totalCount-only shapes preserved |
| 5 | `MATERIAL_NEW_CANDIDATES_RECEIVE_CORRECT_SEARCH_CONFIRMATION_OR_HOLD_ROUTING` | PASS | 9/9 requirements; 7 successful -> ADD_TO_PIPELINE; 2 OUTCOME_UNKNOWN -> HOLD_EVIDENCE; 0 retries |
| 6 | `WEBSITE_TEXT_AS_RANKING_OVERCLAIM_EQUALS_0` | PASS | overclaims=0; 11 visible cells and 12 ranking rows trace only to successful exact-query Search rows |
| 7 | `FULL_COMPETITOR_KEYWORD_UNIVERSE_OVERCLAIM_EQUALS_0` | PASS | overclaims=0; evidence limited to 75 discovery queries and 7 successful exact-query rechecks |
| 8 | `MERGE_COUNTS_RECONCILE` | PASS | 20 = 16 MERGE_ACCEPTED + 3 close-variant suppressions + 1 retained hold + 0 rejected; delta rows=16 |
| 9 | `EXTERNAL_REVERSE_DOMAIN_PROVIDER_REQUIRED_FOR_BASE_EXECUTION_EQUALS_FALSE` | PASS | Complete 5A.1-5A.7 rehearsal executed with preserved Yandex Search, public-page evidence and Wordstat; reverse-domain provider calls=0 |
| 10 | `CLIENT_FACING_COMPETITOR_GAP_RESULT_IS_UNDERSTANDABLE_AND_MATERIALLY_USEFUL` | OWNER_REVIEW_REQUIRED | Plain-Russian preview contains all 16 accepted phrases in 7 directions; 7 exact-query checks; 11 visible query-domain cells; 12 ranking rows; explicit zero-selected-competitor case; 2 unresolved directions; no-new-page boundary |

Nine deterministic technical gates pass. Gate 10 remains **OWNER_REVIEW_REQUIRED**; Work verified that the preview is complete and plain-language, but only the owner/recipient may decide whether it is understandable and materially useful.

## 9. Separated verdicts

~~~text
FIRST_EXECUTION_TECHNICAL_VALIDATION = PASS_9_OF_9_DETERMINISTIC_GATES
FIRST_EXECUTION_INFORMATION_GAIN_VERDICT = MATERIAL_POSITIVE_GAIN_WITH_STRONG_FILTERING_VALUE
CLIENT_FACING_USEFULNESS_GATE = OWNER_REVIEW_REQUIRED
RECOMMENDED_PROJECT_TEST_VALIDATION = RECOMMEND_VALIDATE_AFTER_OWNER_REVIEW
ACTUAL_PROJECT_TEST_VALIDATED_STATE = false / PENDING_OWNER_REVIEW
LEVEL1_METHOD_PROMOTION_STATE = NOT_PROMOTED
PERMANENT_DIMINISHING_GAIN_THRESHOLD_STATE = NOT_VALIDATED_SINGLE_REHEARSAL
~~~

## 10. Protection and provider boundary

- New provider or substitute web calls by Work: 0.
- Raw provider envelopes modified: false.
- Frozen Stage-5 semantic master modified: false.
- Canonical unit authority modified: false.
- Corrected client release / Documents 01–03 / semantic-core XLSX modified: false.
- Page ownership, creation, deletion, split/merge or implementation action created: false.

## 11. Next actions

1. **OWNER_REVIEW_REVISED_STEP_5A_CLIENT_FACING_PREVIEW_AND_EXPLICITLY_ACCEPT_OR_REJECT_GATE_10**
2. Independently before any next real release: **PROPAGATE_STEP_5A_ACCEPTED_SEMANTIC_PIPELINE_DELTA_THROUGH_NORMAL_DOWNSTREAM_PIPELINE**

Neither action is executed in this task.
