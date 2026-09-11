# KW-002 Blood & Sand — post-sanitation Step04 QA

Date: 2026-09-11
Status: **COMPLETE / PASS CANDIDATE / MAIN CHATGPT RETURN QA REQUIRED**

## Scope and method boundary

The full accepted corrected Step03B universe was processed. New family assignment used only canonical phrase text, corrected Step03B state/reason and frozen business/catalog authority. Historical Step04 was joined **after** each new primary family had been assigned and was used only for comparison.

No Wordstat, Search, GenSearch, AI-search, Step05, sealed Blood & Sand research, final row cleanup, final intent classification, SERP clustering, query-to-page mapping, IA or Page Jobs were used.

## Full-volume accounting

```text
TOTAL_NORMALIZED_IDENTITIES = 24576
TOTAL_RAW_OCCURRENCES = 25979
KEEP_IDENTITIES = 5100
HOLD_IDENTITIES = 13035
EXCLUDE_IDENTITIES = 6441
ACTIVE_PLUS_HOLD_IDENTITIES_TRIAGED = 18135
EXCLUDED_IDENTITIES_PRESERVED_AS_HISTORY = 6441
KEEP_RAW_OCCURRENCES = 5263
HOLD_RAW_OCCURRENCES = 13823
EXCLUDE_RAW_OCCURRENCES = 6893
ACTIVE_PLUS_HOLD_RAW_OCCURRENCES = 19086
OCCURRENCE_LEDGER_ROWS = 25979
UNIQUE_OCCURRENCE_IDS = 25979
UNASSIGNED_OCCURRENCE_IDS = 0
UNEXPECTED_DUPLICATE_OCCURRENCE_IDS = 0
RAW_LINEAGE_LOSS = 0
OVERLAY_STATE_MISMATCHES = 0
```

## New preliminary family authority

Family rows include 26 total concepts: 24 observed families and 2 zero-observation coverage-gap families. Family count was not forced to historical 25/31.

| family | plain label | triage | identities | RAW | KEEP | HOLD |
|---|---|---|---:|---:|---:|---:|
| PSF001 | Общие названия товара без уточнения | PLAUSIBLE_IN_SCOPE | 2953 | 3031 | 2953 | 0 |
| PSF002 | Общие товарные запросы с покупкой | STRONG_IN_SCOPE | 70 | 70 | 70 | 0 |
| PSF003 | Товары для автомобиля | STRONG_IN_SCOPE | 151 | 161 | 151 | 0 |
| PSF004 | Чётки как физический предмет | PLAUSIBLE_IN_SCOPE | 670 | 671 | 670 | 0 |
| PSF005 | Каталожное имя с товаром, формой или покупкой | PLAUSIBLE_IN_SCOPE | 498 | 538 | 366 | 132 |
| PSF006 | Каталожное имя без достаточного уточнения | MIXED_AMBIGUOUS | 2109 | 2131 | 0 | 2109 |
| PSF007 | Значение, история и трактовка каталожных символов | MIXED_AMBIGUOUS | 360 | 377 | 166 | 194 |
| PSF008 | Визуальные символы, руны и body-art | MIXED_AMBIGUOUS | 336 | 336 | 86 | 250 |
| PSF009 | Каталожные имена с омонимами | MIXED_AMBIGUOUS | 336 | 338 | 0 | 336 |
| PSF010 | Форма или материал вне подтверждённых фактов | MIXED_AMBIGUOUS | 94 | 102 | 78 | 16 |
| PSF011 | Эффекты, защита и аудитории | MIXED_AMBIGUOUS | 159 | 173 | 151 | 8 |
| PSF012 | Зодиак с товаром, формой или покупкой | PLAUSIBLE_IN_SCOPE | 608 | 620 | 313 | 295 |
| PSF013 | Камни, каталожные символы и зодиак: товарно-информационная коллизия | MIXED_AMBIGUOUS | 339 | 370 | 0 | 339 |
| PSF014 | Знак зодиака без товарного уточнения | MIXED_AMBIGUOUS | 6540 | 7038 | 0 | 6540 |
| PSF015 | Зодиакальная информация внутри HOLD | SANITATION_LEAKAGE_REVIEW | 543 | 580 | 0 | 543 |
| PSF016 | Зодиакальные изображения и символика | MIXED_AMBIGUOUS | 275 | 277 | 0 | 275 |
| PSF017 | Религиозный предмет, текст или практика | MIXED_AMBIGUOUS | 234 | 236 | 43 | 191 |
| PSF018 | Медиа, заголовок и цифровое действие | SANITATION_LEAKAGE_REVIEW | 558 | 568 | 25 | 533 |
| PSF019 | Игра, игровой предмет или model-token | SANITATION_LEAKAGE_REVIEW | 96 | 97 | 22 | 74 |
| PSF020 | Автомодель, деталь, краска или товар для машины | SANITATION_LEAKAGE_REVIEW | 57 | 76 | 2 | 55 |
| PSF021 | Место, человек, организация или платформа | SANITATION_LEAKAGE_REVIEW | 168 | 168 | 4 | 164 |
| PSF022 | Возможная форма слова «чётки» или опечатка | SANITATION_LEAKAGE_REVIEW | 33 | 33 | 0 | 33 |
| PSF023 | Общее товарное слово с неразрешённым референтом | MIXED_AMBIGUOUS | 240 | 240 | 0 | 240 |
| PSF024 | Остаточный недостаточный контекст | SANITATION_LEAKAGE_REVIEW | 708 | 855 | 0 | 708 |
| PSF025 | Точные каталожные названия без текущей наблюдаемой ветви | COVERAGE_GAP | 0 | 0 | 0 | 0 |
| PSF026 | Бренд «Кровь и Песок» с товарным уточнением | COVERAGE_GAP | 0 | 0 | 0 | 0 |

The 18,135 identity and 19,086 RAW active/HOLD totals reconcile exactly across these rows. No family verdict changes a corrected Step03B state. Every HOLD occurrence keeps a later-evidence route and every observed family has deterministic representative phrases.

## Semantic adversarial scans

```json
{
  "ACTIVE_ROWS_ASSIGNED_TO_EXCLUDED_MARKER": 0,
  "EXCLUDED_ROWS_ASSIGNED_ACTIVE_FAMILY": 0,
  "HOLD_WITH_FINAL_NONE_EVIDENCE": 0,
  "FREQUENCY_USED_FOR_ASSIGNMENT": 0,
  "STRONG_FAMILY_HOLD_SHARE_OVER_20_PERCENT": 0,
  "COVERAGE_GAP_WITH_OBSERVED_IDENTITIES": 0,
  "OBSERVED_FAMILY_WITHOUT_EXAMPLES": 0,
  "QUEUE_EXECUTED_ROWS": 0,
  "FEEDBACK_STATE_MUTATIONS": 0,
  "GENERIC_PRODUCT_FAMILY_WITH_FOREIGN_COLLISION_SIGNAL": 0,
  "COMMERCIAL_FAMILY_WITH_FOREIGN_COLLISION_SIGNAL": 0,
  "STRONG_AUTO_FAMILY_WITH_GAME_MEDIA_ENTITY_SIGNAL": 0,
  "OBSERVED_FEEDBACK_FAMILY_WITHOUT_FEEDBACK_ROW": 0
}
```

All values are zero. `assign_family()` does not accept historical family fields or frequency values. Bounded collision families take precedence over generic product grouping for HOLD identities. Coverage-gap families contain no invented observation.

During adversarial development, whole-volume inspection caught unsafe substring
collisions (`лев` in `королева`, `рак` in `тракт`, `игра` in `тигра`, `город`
in `богородица`, `краска` in `раскраска`) and the catalog/vehicle boundary for
`звезды Лады`. Final rules use bounded tokens or contextual reason codes, and
all six cases are blocking phrase assertions in every rerun.

## Mandatory known examples

| phrase | regression |
|---|---|
| `оберег дома купить` | PASS |
| `четки в машину знак lada` | PASS |
| `звезда лада купить` | PASS |
| `кулон дева знак зодиака с камнем` | PASS |
| `амулет читать` | PASS |
| `серия амулет` | PASS |
| `талисман команды` | PASS |
| `звезда лада значение` | PASS |
| `hollow knight амулеты` | PASS |
| `датчик температуры амулет` | PASS |
| `оберег для водителя и автомобиля` | PASS |
| `счастливый амулет` | PASS |
| `королева четок` | PASS |
| `тракт` | PASS |
| `талисман тигра` | PASS |
| `обереги богородицы` | PASS |
| `раскраска талисманы` | PASS |
| `амулет звезды лады` | PASS |

Additional class controls cover zodiac product vs astrology, religious product vs practice, car-use vs vehicle part/model, media title/action, game/item, entity/place/organization, rosary morphology, and home/product vs real-estate interpretation. The tests are assertions over the full rerun, not row patches.

## Sanitation feedback

| feedback | family | class | identities | RAW |
|---|---|---|---:|---:|
| PSFB001 | PSF015 | POSSIBLE_UNDER_EXCLUSION | 543 | 580 |
| PSFB002 | PSF018 | MEDIA_REFERENT_BOUNDARY | 558 | 568 |
| PSFB003 | PSF019 | GAME_REFERENT_BOUNDARY | 96 | 97 |
| PSFB004 | PSF020 | AUTOMOTIVE_COLLISION_BOUNDARY | 57 | 76 |
| PSFB005 | PSF021 | ENTITY_COLLISION_BOUNDARY | 168 | 168 |
| PSFB006 | PSF022 | ROSARY_MORPHOLOGY_BOUNDARY | 33 | 33 |
| PSFB007 | PSF005 | POSSIBLE_OVER_HOLD | 132 | 134 |
| PSFB008 | PSF017 | RELIGIOUS_PRODUCT_BOUNDARY | 234 | 236 |
| PSFB009 | PSF024 | RESIDUAL_LEXICAL_OR_REFERENT_GAP | 708 | 855 |
| PSFB010 | PSF011 | EFFECT_OR_AUDIENCE_CLAIM_BOUNDARY | 159 | 173 |

Feedback is non-destructive. `STEP03B_STATE_CHANGED_IN_STEP04 = 0`. These rows document possible over-HOLD/under-exclusion or unresolved collision boundaries for later independent adjudication.

## Expansion queue

```text
NEW_QUEUE_ROWS = 13
PROVIDER_NEEDED_LATER = 11
OWNER_FACT_FIRST_OR_ONLY = 5
QUEUE_ACTIONS_EXECUTED_NOW = 0
HISTORICAL_E001_E002_E003_MERGED = 1 bounded current item
PRAYER_DUPLICATION = 0
AUTOMOTIVE_DUPLICATION = 0
```

Every queue item cites current corrected-universe evidence, expected information gain, a stopping rule and a Step03B collision risk. Frequency and delivery cap are not queue reasons.

## Historical comparison

```text
HISTORICAL_FAMILY_COUNT = 31
HISTORICAL_OBSERVED_FAMILY_COUNT = 25
NEW_FAMILY_COUNT = 26
NEW_OBSERVED_FAMILY_COUNT = 24
FAMILIES_PRESERVED_SEMANTICALLY = 2
FAMILIES_SPLIT = 0
FAMILIES_MERGED = 17
FAMILIES_REDEFINED = 23
HISTORICAL_FAMILIES_RETIRED = 0
NEW_FAMILIES_CREATED = 0
IDENTITIES_MOVED_BETWEEN_FAMILY_MEANINGS = 1875
RAW_OCCURRENCES_MOVED_BETWEEN_FAMILY_MEANINGS = 1983
HISTORICAL_QUEUE_ROWS = 15
NEW_QUEUE_ROWS = 13
QUEUE_ROWS_PRESERVED = 12
QUEUE_ROWS_RETIRED = 0
QUEUE_ROWS_MERGED = 3
NEW_QUEUE_ROWS_CREATED = 0
```

The comparison table defines movement as a current active/HOLD occurrence whose new primary family falls outside the declared semantic refinement set for its historical occurrence family. This is a traceability metric, not a defect count. Excluded rows remain `EXCLUDED_HISTORY` and are not counted as active semantic moves.

## Known-failure regression

All 15 rows in `STEP_04_POST_SANITATION_KNOWN_FAILURE_REGRESSION_MATRIX_2026-09-11.tsv` are PASS and blocking if failed. In particular:

```text
F03B_COLLISION_REGRESSION = PASS
F04_OCCURRENCE_REPRODUCIBILITY = PASS
F04_RULE_LEVEL_RERUN = PASS
UPSTREAM_INVALIDATION_HANDLED = PASS
KNOWN_FAILURE_REGRESSION = PASS
```

## Quality score

Sixteen Step04-specific dimensions are scored independently on 0-10. The normalized /100 result is the arithmetic mean multiplied by ten.

| dimension | score | evidence / points lost |
|---|---:|---|
| SOURCE_BOUNDARY_INTEGRITY | 10.0/10 | Only Ozon-only frozen scope and prompt-whitelisted authorities were used. |
| CORRECTED_STEP03B_ALIGNMENT | 10.0/10 | 24,576/24,576 identities match the accepted audit state; no state mutation. |
| FULL_VOLUME_COVERAGE | 10.0/10 | 18,135 active/HOLD identities semantically triaged and 6,441 excluded identities preserved. |
| OCCURRENCE_REPRODUCIBILITY | 10.0/10 | 25,979 unique RAW occurrence ids map one-to-one with zero loss. |
| FAMILY_COHERENCE | 9.4/10 | 0.6 lost because preliminary lexical/context families intentionally await Step10/SERP refinement; no blocking incoherence found. |
| FAMILY_BOUNDARY_PRECISION | 9.3/10 | 0.7 lost for mixed catalog/zodiac/religious collision boundaries that cannot be finalized without later evidence. |
| AMBIGUITY_HANDLING | 9.8/10 | 0.2 lost because large governed HOLD zones remain; none was silently resolved. |
| BUSINESS_ASSORTMENT_ALIGNMENT | 9.5/10 | 0.5 lost because most Ozon titles omit physical form/material facts. |
| FREQUENCY_BIAS_CONTROL | 10.0/10 | Frequency is descriptive only and absent from family assignment logic. |
| COVERAGE_GAP_QUALITY | 9.4/10 | 0.6 lost because gap hypotheses still require owner fact or later provider evidence. |
| EXPANSION_QUEUE_QUALITY | 9.5/10 | 0.5 lost because 11 of 13 rows are conditional later provider opportunities, not current observations. |
| SANITATION_FEEDBACK_QUALITY | 9.5/10 | 0.5 lost because feedback is class-level and awaits separate adjudication; Step03B remains unchanged. |
| KNOWN_FAILURE_REGRESSION | 10.0/10 | All 15 blocking matrix rows and representative collision cases pass. |
| HISTORICAL_COMPARISON_TRACEABILITY | 9.7/10 | 0.3 lost because different taxonomy granularity makes semantic-move counts definition-dependent; definition is explicit. |
| DOWNSTREAM_SAFETY | 9.7/10 | 0.3 lost pending Main ChatGPT return QA; Step05 remains blocked. |
| METHOD_SOURCE_SUPPORT | 9.8/10 | 0.2 lost because sources support staged family/intent practice, not this project-specific taxonomy itself. |

```text
QUALITY_SCORE_100 = 97.20
QUALITY_SCORE_10 = 9.72
MIN_CRITICAL_DIMENSION = 9.3
ALL_BLOCKING_REGRESSIONS = PASS
OPEN_CRITICAL_DEFECTS = 0
STEP04_POST_SANITATION_VERDICT = PASS_CANDIDATE
```

## Hard boundaries and stop

```text
NEW_WORDSTAT_CALLS = 0
NEW_SEARCH_CALLS = 0
NEW_GENSEARCH_CALLS = 0
NEW_AI_SEARCH_CALLS = 0
SEALED_SOURCE_VIOLATIONS = 0
FINAL_ROW_CLEANUP_PERFORMED = false
FINAL_INTENT_CLASSIFICATION_PERFORMED = false
SERP_CLUSTERING_PERFORMED = false
QUERY_TO_PAGE_MAPPING_PERFORMED = false
IA_PAGE_JOBS_INTERNAL_LINKS_PERFORMED = false
STEP05_STARTED = false
STEP05_ALLOWED = false
```

## ПРОСТЫМИ СЛОВАМИ

Старую группировку нельзя было просто оставить: после исправления фильтра 1 710 фраз сменили статус, поэтому состав почти всех прежних групп перестал быть надёжной текущей картиной. Мы заново распределили все 18 135 актуальных и спорных фраз по предварительным смысловым семьям, а все 25 979 исходных появлений сохранили в проверяемой таблице.

Новые семьи показывают отдельно общий товарный спрос, покупки, автомобильное использование, чётки, конкретные названия, зодиакальные товары, камни, религиозные темы и зоны смешения с медиа, играми, машинами и чужими сущностями. Спорные фразы не объявлены окончательно подходящими или неподходящими: они остались спорными и получили понятный маршрут дальнейшей проверки. Доказательства и связи с исходными данными не потеряны.

Локально шаг проходит все обязательные проверки и является кандидатом на принятие. Дальше всё ещё нельзя запускать Step05: сначала Main ChatGPT должен независимо проверить этот возврат и принять новую семейную модель.
