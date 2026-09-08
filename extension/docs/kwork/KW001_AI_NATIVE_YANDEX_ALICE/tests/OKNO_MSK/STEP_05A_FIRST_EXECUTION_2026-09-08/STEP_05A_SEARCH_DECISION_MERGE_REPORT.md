# STEP 05A.6 SEARCH RECONCILIATION + STEP 05A.7 DECISION / MERGE REPORT

Date: 2026-09-08

Status: **ANALYST QA PASS / OWNER REVIEW PENDING**

## Outcome

The bounded preserved Search acquisition is fully reconciled: all 9 requirements are accounted across three durable job lifecycles, all 70 actually returned TOP10 rows are preserved, and both outcome-unknown requests remain unknown without retry or invented evidence.

`ADD_TO_PIPELINE` means acquisition-pipeline inclusion only. It does **not** mean a new page, page owner, split/merge, architecture, or implementation action. The corrected client release and frozen Stage-5 authorities were not changed.

## Exact counts

- SEARCH_REQUIREMENTS = 9
- SEARCH_SUCCEEDED = 7
- SEARCH_OUTCOME_UNKNOWN = 2
- SEARCH_SERP_ROWS = 70
- SELECTED_COMPETITOR_VISIBILITY_OBSERVATIONS = 11
- SELECTED_COMPETITOR_RANKING_ROWS = 12
- FINAL_ADD_TO_PIPELINE = 7
- FINAL_ALREADY_COVERED = 0
- FINAL_REJECT_OFF_SCOPE = 0
- FINAL_HOLD_EVIDENCE = 2
- POTENTIALLY_NEW_WORDSTAT_OCCURRENCES_RECONCILED = 20
- MERGE_ACCEPTED_PHRASE_OCCURRENCES = 16
- SUPPRESSED_AS_CLOSE_VARIANT_DUPLICATE = 3
- RETAIN_HOLD = 1
- REJECT_AFTER_SEARCH = 0
- SEMANTIC_PIPELINE_DELTA_ROWS = 16
- UNKNOWN_RETRIES = 0
- NEW_PROVIDER_CALLS_BY_WORK = 0
- WEBSITE_TEXT_AS_RANKING_OVERCLAIM = 0
- FULL_COMPETITOR_KEYWORD_UNIVERSE_OVERCLAIM = 0
- CLIENT_DELIVERABLES_MODIFIED = false
- LEVEL1_METHOD_PROMOTED = false
- PROJECT_TEST_VALIDATED = false

Upstream bounded impact input retained for Step 5A.8: 75 preserved queries / 750 ranking rows; 9 selected domains; 44 inspected targets (43 accessible at the requested URL, 1 accessible after redirect, 0 inaccessible); 92 candidate occurrences consolidated to 43 directions; 14 Wordstat seeds; 160 returned Wordstat rows.

## Direction decisions

| Priority | Direction | Exact query | Search state | Final route | Visible selected domains |
|---:|---|---|---|---|---:|
| 1 | `OPEN_BALCONY_WATERPROOFING` | гидроизоляция для открытого балкона | SUCCEEDED | ADD_TO_PIPELINE | 0 |
| 2 | `SUN_PROTECTION_GLASS_UNIT` | солнцезащитный стеклопакет | SUCCEEDED | ADD_TO_PIPELINE | 2 |
| 3 | `MULTIFUNCTIONAL_GLASS_UNIT` | многофункциональный стеклопакет что это | SUCCEEDED | ADD_TO_PIPELINE | 3 |
| 4 | `IMPACT_RESISTANT_GLASS_UNIT` | ударопрочный стеклопакет | SUCCEEDED | ADD_TO_PIPELINE | 1 |
| 5 | `OLD_HOUSING_WINDOWS` | окна для старого фонда | OUTCOME_UNKNOWN | HOLD_EVIDENCE | 0 |
| 6 | `BALCONY_AS_OFFICE` | балконы под офис | SUCCEEDED | ADD_TO_PIPELINE | 1 |
| 7 | `BALCONY_AS_STORAGE` | кладовая на балконе | OUTCOME_UNKNOWN | HOLD_EVIDENCE | 0 |
| 8 | `BALCONY_ROOF_SOUNDPROOFING` | шумоизоляция на крышу балкона | SUCCEEDED | ADD_TO_PIPELINE | 1 |
| 9 | `WINDOW_PROFILE_REINFORCEMENT` | армирование оконного профиля | SUCCEEDED | ADD_TO_PIPELINE | 3 |

The seven successful directions have real Wordstat occurrence evidence, sufficient exact-query Search evidence, a frozen in-scope parent business unit, and no exact/close active semantic direction. They therefore enter the union-compatible acquisition delta. The two unknown queries remain `HOLD_EVIDENCE`; neither is interpreted as an empty SERP or zero demand.

## Accepted phrase occurrences

- гидроизоляция для открытого балкона — 35
- гидроизоляция открытого балкона в частном доме — 12
- лучшая гидроизоляция для открытого балкона — 2
- как сделать гидроизоляцию на открытом балконе — 2
- гидроизоляция открытого деревянного балкона — 1
- гидроизоляция балконной плиты открытого балкона — 1
- солнцезащитный стеклопакет — 28
- солнцезащитное стекло в стеклопакете — 4
- солнцезащитный стеклопакет rehau — 1
- многофункциональный стеклопакет что это — 5
- ударопрочный стеклопакет — 8
- балконы под офис — 7
- шумоизоляция на крышу балкона — 9
- шумоизоляция крыши балкона от дождя — 6
- шумоизоляция крыши балкона изнутри от дождя — 1
- армирование оконного профиля — 5

Close variants `WSR004`, `WSR026`, and `WSR047` are explicitly suppressed to prevent delta inflation. `WSR100` remains on hold because its Search outcome is unknown. No frequency is invented for the totalCount-only old-housing seed.

## Evidence boundaries

- Earlier competitor-page inspection proves topic/seed lineage, not exact-query rank. Every ranking claim in this report traces to a successful raw Search row.
- Observed rank is not traffic, clicks, leads, conversions, or commercial success.
- Search and Wordstat do not assign page ownership or authorize a physical site change.
- The delta is a union-compatible pre-release acquisition package marked `PROPAGATION_REQUIRED_BEFORE_NEXT_REAL_RELEASE`; it does not rewrite frozen Stage-5 authority.
- New Yandex Search, Wordstat, Alice, GenSearch, Webmaster, Metrika, Direct, competitor-page or substitute web-search calls by Work: 0.

## Next action

`STEP_5A_8_MEASURE_INFORMATION_GAIN_AND_ASSESS_FIRST_EXECUTION_PROJECT_VALIDATION_WITHOUT_AUTOMATIC_LEVEL1_PROMOTION`

This report supplies factual inputs only. Method promotion and `PROJECT_TEST_VALIDATED=true` are explicitly outside this task.
