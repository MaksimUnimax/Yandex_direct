# KW-002 Blood & Sand — corrected Step03B sanitation QA

Date: 2026-09-11
Status: **COMPLETE / PASS CANDIDATE / MAIN CHATGPT RETURN QA REQUIRED**

## Authority and method boundary

- The owner/Main ChatGPT accepted the independent full-volume audit and revoked the original Step03B semantic PASS candidate.
- The executable classifier applies the accepted corrected rule order to all 24,576 frozen Step03A identities.
- The audit overlay is used only as a post-classification row-level regression oracle.
- External-method support and source disclosure are preserved in `KW002_STEP03A_03B_INDEPENDENT_FULL_VOLUME_AUDIT_REPORT_2026-09-11.md`, sections B-D; no new method was invented in this correction.
- No provider, Search, GenSearch, AI-search, Step05, sealed research, final intent, clustering, or page mapping was used.

## Frozen-input integrity

```text
STEP03A_NORMALIZED_POOL_SHA256 = b30c29ff66a56d80bc1aa9ff6b2eade522b27d1e167cbd636ac72fbff211f2a8
STEP03A_NORMALIZATION_LEDGER_SHA256 = 28205ca64f26d219d489b36f102a8923b4a4b635c8b213179bca4a188b24c3df
STEP03A_BYTE_IDENTITY = PASS
AUDIT_OVERLAY_SHA256 = db9b79dda64b205f0b0bef273f70f221f183d9389eca3e67e651e93ea269d669
AUDIT_REASON_REGISTER_SHA256 = 050af71b8e431408c2f406e984416dc4c605038a5ad9f0ac103772f2f9310b31
```

## Full-volume accounting

```text
NORMALIZED_IDENTITIES = 24576
RAW_OCCURRENCES = 25979
UNIQUE_RAW_OCCURRENCE_IDS = 25979

CORRECTED_KEEP = 5100
CORRECTED_HOLD = 13035
CORRECTED_EXCLUDE = 6441
NORMALIZED_TOTAL = 24576

CORRECTED_KEEP_RAW = 5263
CORRECTED_HOLD_RAW = 13823
CORRECTED_EXCLUDE_RAW = 6893
RAW_TOTAL = 25979

CHANGED_IDENTITIES = 1710
CHANGED_RAW_OCCURRENCES = 1761
```

## Accepted transition regression

| current → corrected | normalized identities | RAW occurrences |
|---|---:|---:|
| KEEP → KEEP | 4788 | 4945 |
| KEEP → HOLD | 207 | 211 |
| KEEP → EXCLUDE | 79 | 80 |
| HOLD → KEEP | 298 | 304 |
| HOLD → HOLD | 12084 | 12828 |
| HOLD → EXCLUDE | 368 | 368 |
| EXCLUDE → KEEP | 14 | 14 |
| EXCLUDE → HOLD | 744 | 784 |
| EXCLUDE → EXCLUDE | 5994 | 6445 |

```text
EXCLUDE_TO_KEEP_MATCH = 14/14
EXCLUDE_TO_HOLD_MATCH = 744/744
KEEP_TO_HOLD_MATCH = 207/207
KEEP_TO_EXCLUDE_MATCH = 79/79
HOLD_TO_KEEP_MATCH = 298/298
HOLD_TO_EXCLUDE_MATCH = 368/368
TOTAL_CHANGED_IDENTITIES_MATCH = 1710/1710
OVERLAY_STATE_MISMATCHES = 0
```

## Corrected reason-code accounting

| state | corrected reason code | normalized identities | RAW occurrences | confidence |
|---|---|---:|---:|---|
| EXCLUDE | `EXCLUDE_CLEAR_LEXICAL_GARBAGE` | 1197 | 1201 | high |
| EXCLUDE | `EXCLUDE_EXPLICIT_ALATYR_PLACE_OR_LOCAL_ENTITY_CONTEXT` | 448 | 448 | high |
| EXCLUDE | `EXCLUDE_EXPLICIT_ASTROLOGY_INFORMATION_TASK` | 1900 | 2319 | high |
| EXCLUDE | `EXCLUDE_EXPLICIT_DIGITAL_MEDIA_CONSUMPTION_CONTEXT` | 167 | 167 | high |
| EXCLUDE | `EXCLUDE_EXPLICIT_DIGITAL_MEDIA_TITLE_CONTEXT` | 17 | 17 | high |
| EXCLUDE | `EXCLUDE_EXPLICIT_GAME_OR_GAME_ITEM_CONTEXT` | 292 | 296 | high |
| EXCLUDE | `EXCLUDE_EXPLICIT_INDUSTRIAL_AUMA_CONTEXT` | 66 | 66 | high |
| EXCLUDE | `EXCLUDE_EXPLICIT_MEDIA_WORK_OR_EPISODE_CONTEXT` | 1200 | 1210 | high |
| EXCLUDE | `EXCLUDE_EXPLICIT_PERSON_OR_FOREIGN_ENTITY_CONTEXT` | 31 | 32 | high |
| EXCLUDE | `EXCLUDE_EXPLICIT_PLACE_OR_ORGANIZATION_CONTEXT` | 206 | 206 | high |
| EXCLUDE | `EXCLUDE_EXPLICIT_REAL_ESTATE_CONTEXT` | 8 | 8 | high |
| EXCLUDE | `EXCLUDE_EXPLICIT_RELIGIOUS_PRACTICE_WITHOUT_PRODUCT` | 124 | 131 | high |
| EXCLUDE | `EXCLUDE_EXPLICIT_SPORT_TEAM_EVENT_OR_MASCOT_CONTEXT` | 19 | 19 | high |
| EXCLUDE | `EXCLUDE_EXPLICIT_UNSUPPORTED_CLOTHING_PRODUCT` | 12 | 12 | high |
| EXCLUDE | `EXCLUDE_EXPLICIT_UNSUPPORTED_PRODUCT_OR_LOCAL_ENTITY_CONTEXT` | 215 | 217 | high |
| EXCLUDE | `EXCLUDE_EXPLICIT_VEHICLE_BRAND_OR_MODEL_CONTEXT` | 41 | 41 | high |
| EXCLUDE | `EXCLUDE_EXPLICIT_VEHICLE_MODEL_OR_PART_CONTEXT` | 498 | 503 | high |
| HOLD | `HOLD_AUTOMOBILE_USE_WITHOUT_SUPPORTED_PRODUCT_NOUN` | 23 | 36 | medium |
| HOLD | `HOLD_CATALOG_NAME_VERSUS_VEHICLE_COLLISION` | 24 | 27 | medium |
| HOLD | `HOLD_CATALOG_PRODUCT_NAME_VERSUS_RELIGIOUS_TEXT` | 28 | 28 | medium |
| HOLD | `HOLD_FROZEN_CATALOG_NAME_REFERENT_UNRESOLVED` | 2713 | 2740 | medium |
| HOLD | `HOLD_GENERIC_GAME_OR_MODEL_TOKEN_NEEDS_CONTEXT` | 45 | 46 | medium |
| HOLD | `HOLD_GENERIC_MEDIA_ACTION_MAY_BE_INFORMATIONAL_PRODUCT_RESEARCH` | 306 | 311 | medium |
| HOLD | `HOLD_GENERIC_TEAM_OR_MASCOT_CONTEXT` | 2 | 2 | medium |
| HOLD | `HOLD_INSUFFICIENT_CONTEXT_FOR_KEEP_OR_EXCLUDE` | 1365 | 1525 | medium |
| HOLD | `HOLD_MEDIA_TITLE_VERSUS_PRODUCT_COLLISION` | 48 | 48 | medium |
| HOLD | `HOLD_PHYSICAL_PRODUCT_VERSUS_RELIGIOUS_PRACTICE` | 147 | 148 | medium |
| HOLD | `HOLD_POSSIBLE_ROSARY_MORPHOLOGY_OR_TYPO` | 33 | 33 | medium |
| HOLD | `HOLD_PRODUCT_NAME_VERSUS_VEHICLE_PAINT_COLLISION` | 3 | 3 | medium |
| HOLD | `HOLD_PRODUCT_OR_CATALOG_NAME_WITH_PERSON_ENTITY_CONTEXT` | 5 | 5 | medium |
| HOLD | `HOLD_PRODUCT_OR_CATALOG_NAME_WITH_PLACE_OR_ORGANIZATION` | 140 | 140 | medium |
| HOLD | `HOLD_PRODUCT_VERSUS_ASTROLOGY_INFORMATION` | 132 | 137 | medium |
| HOLD | `HOLD_SEARCH_PLATFORM_OR_MEDIA_CONTEXT_UNRESOLVED` | 8 | 8 | medium |
| HOLD | `HOLD_TITLE_LIKE_PRODUCT_WORD_COLLISION` | 168 | 173 | medium |
| HOLD | `HOLD_ZODIAC_OR_STONE_PRODUCT_COLLISION` | 7845 | 8413 | medium |
| KEEP | `KEEP_CATALOG_NAME_WITH_COMMERCE` | 1 | 1 | high |
| KEEP | `KEEP_FROZEN_CATALOG_NAME_WITH_COMMERCE_OR_OBJECT_FORM` | 76 | 76 | high |
| KEEP | `KEEP_FROZEN_CLIENT_PRODUCT_CLASS_WITHOUT_FOREIGN_CONTEXT` | 4706 | 4863 | high |
| KEEP | `KEEP_SUPPORTED_AUTOMOBILE_USE_PRODUCT_CONTEXT` | 1 | 1 | high |
| KEEP | `KEEP_SUPPORTED_PRODUCT_PLUS_ZODIAC_TITLE` | 114 | 119 | high |
| KEEP | `KEEP_SUPPORTED_PRODUCT_WITH_COMMERCE_AND_GEO_CHANNEL` | 5 | 5 | high |
| KEEP | `KEEP_ZODIAC_TITLE_WITH_COMMERCE_OR_OBJECT_FORM` | 197 | 198 | high |

## Hard gates

```text
STATE_PARTITION_EXHAUSTIVE = PASS
STATE_PARTITION_MUTUALLY_EXCLUSIVE = PASS
RAW_LINEAGE_LOSS = 0
UNMAPPED_RAW_OCCURRENCES = 0
DUPLICATE_RAW_OCCURRENCE_IDS = 0
FREQUENCY_ONLY_EXCLUSIONS = 0
HIGH_FREQUENCY_ONLY_KEEPS = 0
SINGLE_AMBIGUOUS_TOKEN_AUTO_EXCLUSIONS = 0
SEALED_SOURCE_VIOLATIONS = 0
NEW_WORDSTAT_CALLS = 0
NEW_SEARCH_CALLS = 0
NEW_GENSEARCH_CALLS = 0
NEW_AI_SEARCH_CALLS = 0
STEP05_USED_AS_BACKFILL = false
STEP05_STARTED = false
FALSE_EXCLUSION_REGRESSION = PASS
FALSE_KEEP_REGRESSION = PASS
BUSINESS_COLLISION_REGRESSION = PASS
STEP04_RECONCILIATION = PASS
DEDICATED_POST_SANITATION_STEP04_WORK_PASS_REQUIRED = true
ALL_HARD_GATES = PASS
OPEN_CRITICAL_SEMANTIC_DEFECTS = 0
```

## Fresh quality score

The revoked 96/100 and audit 75/100 scores are not reused. Thirteen correction-specific dimensions are independently scored on the 0-10 scale; the /100 score is the arithmetic mean multiplied by ten.

| dimension | score | evidence / limitation |
|---|---:|---|
| NORMALIZATION_SAFETY | 10.0/10 | No points lost: both frozen Step03A files are byte-identical to live base and the correction does not write them. |
| RAW_LINEAGE_INTEGRITY | 10.0/10 | No points lost: 25,979 unique RAW IDs occur exactly once across corrected lineage and all join to Step04. |
| SANITATION_RULE_PRECISION | 9.8/10 | 0.2 lost because Step03B remains a conservative lexical/catalog pre-filter rather than final SERP intent evidence. This does not block Step03B PASS; later SERP work can only resolve HOLD, not justify destructive pre-filtering. |
| FALSE_EXCLUSION_CONTROL | 9.8/10 | 0.2 lost pending independent Main ChatGPT return QA/remote readback. All 758 unsafe exclusions identified by the accepted audit now match the row oracle, so no critical defect remains locally. |
| FALSE_KEEP_CONTROL | 9.8/10 | 0.2 lost pending independent Main ChatGPT return QA/remote readback. All 286 unsafe keeps identified by the audit now match the row oracle, so no critical defect remains locally. |
| AMBIGUITY_HANDLING | 9.8/10 | 0.2 lost because 13,035 identities intentionally remain HOLD for later evidence. This is governed uncertainty, not a Step03B blocker; later Step10/SERP evidence is required to raise resolution coverage. |
| BUSINESS_ASSORTMENT_ALIGNMENT | 9.8/10 | 0.2 lost because the frozen business authority is a 76-row title catalog rather than full product-content evidence. All accepted zodiac, religious, automobile-use, and catalog-name collision regressions pass. |
| LOW_FREQUENCY_BIAS_CONTROL | 10.0/10 | No points lost: the classifier never reads observed count values when assigning state. |
| REASON_CODE_QUALITY | 9.6/10 | 0.4 lost because 42 machine-oriented reason codes are intentionally granular and not client wording. This does not block the analytical authority; a later recipient layer may consolidate display labels without changing states. |
| FULL_VOLUME_COVERAGE | 10.0/10 | No points lost: all 24,576 identities and all 25,979 RAW links were processed with no sample or truncation. |
| REPRODUCIBILITY | 9.8/10 | 0.2 lost because remote readback is still pending. Local rerun is byte-deterministic and the executable materializer plus exact audit hashes are preserved. |
| DOWNSTREAM_SAFETY | 9.5/10 | 0.5 lost because the dedicated post-sanitation Step04 semantic rewrite is deliberately not executed and Step05 remains blocked. The one-to-one Step04 reconciliation itself passes. |
| METHOD_SOURCE_SUPPORT | 9.8/10 | 0.2 lost because this materialization reuses the accepted same-day independent audit source trace rather than performing a second redundant web review. No new method element was introduced and the owner explicitly accepted that audit. |

```text
QUALITY_SCORE_100 = 98.23
QUALITY_SCORE_10 = 9.82
STEP03B_CORRECTION = PASS_CANDIDATE
MAIN_CHATGPT_RETURN_QA_REQUIRED = true
STEP05_ALLOWED = false
```
