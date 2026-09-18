# KW-002 / BLOOD & SAND — STEP07 POST-EXTERNAL-AUDIT FULL-VOLUME BUSINESS-SCOPE REWORK QA

Date: 2026-09-18
Action: `STEP07_POST_EXTERNAL_AUDIT_FULL_VOLUME_BUSINESS_SCOPE_REWORK`
Work start remote HEAD: `7dd56fd6930b7140d0f3c905dcc1fc8094495fdf`
Pre-publication remote HEAD: `7dd56fd6930b7140d0f3c905dcc1fc8094495fdf`
Authority drift: **NONE**
Overall hard QA: **PASS**
Step result: **PASS_FULL_VOLUME_BUSINESS_SCOPE_REWORK**

## 1. Exact final report

```text
WORK_START_REMOTE_HEAD = 7dd56fd6930b7140d0f3c905dcc1fc8094495fdf
WORK_PRE_PUBLICATION_REMOTE_HEAD = 7dd56fd6930b7140d0f3c905dcc1fc8094495fdf
AUTHORITY_DRIFT_STATUS = NONE
STEP07_POST_AUDIT_REWORK_STATUS = PASS_FULL_VOLUME_BUSINESS_SCOPE_REWORK

TARGET_CANDIDATES_REVIEWED = 1548/1548
LINKED_PROVENANCE_REVIEWED = 2633/2633
OLD_STEP08_ELIGIBLE = 1548
NEW_STEP08_ELIGIBLE = 794
BUSINESS_SCOPE_REJECTIONS = 452
WRAPPER_NOISE_REJECTIONS_OR_DERIVATIONS = 329
AMBIGUOUS_HOLD = 16
ALREADY_PRESENT_AFTER_RECONCILIATION = 0
SINGLE_VS_MULTI_SOURCE_FINAL_COUNTS = 756 / 38

HARD_GATE_FAILURES = 0
QUALITY_TOTAL = 98/100
QUALITY_SCORE = 9.8/10

NEW_BROWSER_CALLS = 0
NEW_WORDSTAT_CALLS = 0
NEW_YANDEX_SEARCH_CALLS = 0
NEW_AI_SEARCH_OR_GENSEARCH_CALLS = 0
NEW_PROVIDER_CALLS = 0
STEP08_STARTED = false
WORK_GITHUB_COMMIT_PUSH_PR = false
MAIN_CHAT_ACCEPTANCE = PENDING
```

## 2. Full-volume decision accounting

```text
CURRENT_CANDIDATE_UNIVERSE_LOADED = 2172/2172
CURRENT_PROVENANCE_UNIVERSE_LOADED = 3948/3948
TARGET_CANDIDATES_SILENTLY_SKIPPED = 0
ALL_LINKED_PROVENANCE_FOR_TARGETS_REVIEWED = true

RETAINED_AS_IS = 751
RECLASSIFIED_OUT_OF_SCOPE = 738
RECLASSIFIED_AMBIGUOUS = 16
TRANSFORMED_DERIVED = 43
ALREADY_PRESENT_AFTER_RECONCILIATION = 0
REMAINING_STEP08_ELIGIBLE = 794
```

The business-scope gate was applied before symbol/topic overlap. Competitor page,
title, product, and claim text was treated as seed evidence only. Single-source
and multi-source counts were used as confidence signals, never as sole decision
rules.

### Old 1548 → new status transition matrix

| FROM_STATUS | TO_STATUS | ROW_COUNT |
|---|---|---|
| `NEW_CANDIDATE` | `AMBIGUOUS` | 16 |
| `NEW_CANDIDATE` | `NEW_CANDIDATE` | 787 |
| `NEW_CANDIDATE` | `OUT_OF_SCOPE` | 737 |
| `POSSIBLE_VARIANT` | `OUT_OF_SCOPE` | 1 |
| `POSSIBLE_VARIANT` | `POSSIBLE_VARIANT` | 7 |

### Final complete candidate status counts

| STATUS | IDENTITIES |
|---|---|
| `ALREADY_PRESENT` | 52 |
| `AMBIGUOUS` | 114 |
| `NEW_CANDIDATE` | 787 |
| `OUT_OF_SCOPE` | 1212 |
| `POSSIBLE_VARIANT` | 7 |

### OUT_OF_SCOPE accounting for the 1548 targets

| OUT_OF_SCOPE_REASON | IDENTITIES |
|---|---|
| `FOREIGN_PRODUCT_OR_SERVICE` | 232 |
| `MEDICAL_OR_BIOLOGICAL` | 8 |
| `UI_OR_FORMATTING_NOISE` | 286 |
| `UNRELATED_SITE_BRANCH` | 206 |
| `UNSUPPORTED_BUSINESS_CLAIM` | 6 |

```text
BUSINESS_SCOPE_REJECTIONS = 452
WRAPPER_NOISE_REJECTIONS = 286
TRANSFORMED_DERIVED = 43
```

## 3. Corrected Step08 queue

### Eligible by candidate type

| CANDIDATE_TYPE | ELIGIBLE_IDENTITIES |
|---|---|
| `ATTRIBUTE` | 8 |
| `INFORMATIONAL_FORMULATION` | 55 |
| `PRODUCT_NAME` | 411 |
| `SUBCATEGORY` | 74 |
| `TERMINOLOGY` | 236 |
| `USE_CASE` | 10 |

### Eligible by competitor-source-count band

| COMPETITOR_SOURCE_COUNT | ELIGIBLE_IDENTITIES |
|---|---|
| `1` | 756 |
| `2` | 22 |
| `3` | 14 |
| `4+` | 2 |

```text
SINGLE_SOURCE_FINAL = 756
MULTI_SOURCE_FINAL = 38
MULTI_SOURCE_REJECTED_OR_HELD = 8
```

### Top competitor sources after correction

Counts are distinct final Step08-eligible candidate identities linked to the source;
one candidate may occur at more than one source.

| COMPETITOR_DOMAIN | ELIGIBLE_CANDIDATES |
|---|---|
| livemaster.ru | 307 |
| slavyanskieoberegi.ru | 90 |
| avito.ru | 84 |
| xn--80aejvmu5h.xn--80aswg | 65 |
| kartaslov.ru | 39 |
| ru.wikipedia.org | 34 |
| wildberries.ru | 34 |
| happywitch.ru | 33 |
| simvolroda.ru | 27 |
| actro.online | 26 |
| lunaro.ru | 16 |
| blog.beregy.ru | 15 |

## 4. Compact transformations

Every transformation preserves immutable `raw_wording` and `source_context` in
the provenance ledger. Derived text is an explicit literal span/format cleanup,
is checked against all 2,172 current identities and the accepted Step03B
semantic universe, and creates no comparison-key collision.

| CANDIDATE_ID | OLD_WORDING | NEW_WORDING | RULE |
|---|---|---|---|
| `S07C000156` | 1. Скандинавская руна Феу | Скандинавская руна Феу | `UI_NOISE_REMOVAL` |
| `S07C000157` | 10. Скандинавская руна Наутиз | Скандинавская руна Наутиз | `UI_NOISE_REMOVAL` |
| `S07C000158` | 11. Скандинавская руна Иса | Скандинавская руна Иса | `UI_NOISE_REMOVAL` |
| `S07C000159` | 12. Скандинавская руна Йера | Скандинавская руна Йера | `UI_NOISE_REMOVAL` |
| `S07C000160` | 13. Скандинавская руна Эйваз | Скандинавская руна Эйваз | `UI_NOISE_REMOVAL` |
| `S07C000161` | 14. Скандинавская руна Перта | Скандинавская руна Перта | `UI_NOISE_REMOVAL` |
| `S07C000162` | 15. Скандинавская руна Альгиз | Скандинавская руна Альгиз | `UI_NOISE_REMOVAL` |
| `S07C000163` | 16. Скандинавская руна Соуло | Скандинавская руна Соуло | `UI_NOISE_REMOVAL` |
| `S07C000164` | 17. Скандинавская руна Тейваз | Скандинавская руна Тейваз | `UI_NOISE_REMOVAL` |
| `S07C000165` | 18. Скандинавская руна Беркана | Скандинавская руна Беркана | `UI_NOISE_REMOVAL` |
| `S07C000166` | 19. Скандинавская руна Эваз | Скандинавская руна Эваз | `UI_NOISE_REMOVAL` |
| `S07C000167` | 2. Скандинавская руна Уруз | Скандинавская руна Уруз | `UI_NOISE_REMOVAL` |
| `S07C000168` | 20. Скандинавская руна Манназ | Скандинавская руна Манназ | `UI_NOISE_REMOVAL` |
| `S07C000169` | 21. Скандинавская руна Лагуз | Скандинавская руна Лагуз | `UI_NOISE_REMOVAL` |
| `S07C000170` | 22. Скандинавская руна Ингуз | Скандинавская руна Ингуз | `UI_NOISE_REMOVAL` |
| `S07C000171` | 23. Скандинавская руна Отал | Скандинавская руна Отал | `UI_NOISE_REMOVAL` |
| `S07C000172` | 24. Скандинавская руна Дагаз | Скандинавская руна Дагаз | `UI_NOISE_REMOVAL` |
| `S07C000173` | 25. Скандинавская руна Один | Скандинавская руна Один | `UI_NOISE_REMOVAL` |
| `S07C000174` | 3. Скандинавская руна Турисаз | Скандинавская руна Турисаз | `UI_NOISE_REMOVAL` |
| `S07C000175` | 4. Скандинавская руна Ансуз | Скандинавская руна Ансуз | `UI_NOISE_REMOVAL` |
| `S07C000176` | 5. Скандинавская руна Райдо | Скандинавская руна Райдо | `UI_NOISE_REMOVAL` |
| `S07C000177` | 6. Скандинавская руна Кеназ | Скандинавская руна Кеназ | `UI_NOISE_REMOVAL` |
| `S07C000178` | 7. Скандинавская руна Гебо | Скандинавская руна Гебо | `UI_NOISE_REMOVAL` |
| `S07C000180` | 8. Скандинавская руна Вуньо | Скандинавская руна Вуньо | `UI_NOISE_REMOVAL` |
| `S07C000181` | 9. Скандинавская руна Хагалаз | Скандинавская руна Хагалаз | `UI_NOISE_REMOVAL` |
| `S07C000219` | Амулет с руной Одал — привлекает связь с предками и наследием | Амулет с руной Одал | `LONG_FORM_SPAN_DERIVATION` |
| `S07C000394` | Значение Руны Альгиз — защита и оберег | Значение руны Альгиз | `LONG_FORM_SPAN_DERIVATION` |
| `S07C000395` | Значение Руны Одал — наследство и родовая связь | Значение руны Одал | `LONG_FORM_SPAN_DERIVATION` |
| `S07C000396` | Значение Руны Феху — богатство и благополучие | Значение руны Феху | `LONG_FORM_SPAN_DERIVATION` |
| `S07C000441` | Значение слова АМУЛЕТ. Что такое АМУЛЕТ? | Что такое амулет | `LONG_FORM_SPAN_DERIVATION` |
| `S07C000442` | Значение слова КУЛОН. Что такое КУЛОН? | Что такое кулон | `LONG_FORM_SPAN_DERIVATION` |
| `S07C000443` | Значение слова ЛАДАНКА. Что такое ЛАДАНКА? | Что такое ладанка | `LONG_FORM_SPAN_DERIVATION` |
| `S07C000444` | Значение слова МЕДАЛЬОН. Что такое МЕДАЛЬОН? | Что такое медальон | `LONG_FORM_SPAN_DERIVATION` |
| `S07C000445` | Значение слова ОБЕРЕГ. Что такое ОБЕРЕГ? | Что такое оберег | `LONG_FORM_SPAN_DERIVATION` |
| `S07C000446` | Значение слова РУНА. Что такое РУНА? | Что такое руна | `LONG_FORM_SPAN_DERIVATION` |
| `S07C000448` | Значение слова РУНЫ. Что такое РУНЫ? | Что такое руны | `LONG_FORM_SPAN_DERIVATION` |
| `S07C000449` | Значение слова ТАЛИСМАН. Что такое ТАЛИСМАН? | Что такое талисман | `LONG_FORM_SPAN_DERIVATION` |
| `S07C001099` | Руна Альгиз: значение, описание и толкование перевернутой с фото | Руна Альгиз: значение, описание и толкование перевернутой | `UI_NOISE_REMOVAL` |
| `S07C001117` | Руна Одал: значение, описание и толкование перевернутой с фото | Руна Одал: значение, описание и толкование перевернутой | `UI_NOISE_REMOVAL` |
| `S07C001132` | Руна Феху: значение богатства и изобилия \| Лунаро | Руна Феху: значение богатства и изобилия | `BRAND_WRAPPER_REMOVAL_DERIVED` |
| `S07C001134` | Руна Феху: значение, описание и толкование перевернутой с фото | Руна Феху: значение, описание и толкование перевернутой | `UI_NOISE_REMOVAL` |
| `S07C001161` | Самый мощный амулет на удачу и богатство в мире цена и фото | Амулет на удачу и богатство | `LONG_FORM_SPAN_DERIVATION` |
| `S07C001201` | Символ ОМ (АУМ) - значение и происхождение🕉️ | Символ ОМ (АУМ) — значение и происхождение | `PUNCTUATION_FORMATTING_CLEANUP` |

```text
TRANSFORMED_DERIVED = 43
UNSUPPORTED_DERIVATIONS = 0
EXISTING_IDENTITY_DUPLICATION = 0
```

## 5. Full-volume regression matrix

| REGRESSION_CLASS | EVIDENCE | RESULT |
|---|---|---|
| `ADJACENT_PRODUCT_CLASS_LEAKAGE` | eligible_hits=0 | PASS |
| `BROAD_MARKETPLACE_PRODUCT_LEAKAGE` | eligible_hits=0 | PASS |
| `SYMBOL_MATCH_WITH_WRONG_PRODUCT_CLASS` | eligible_hits=0 | PASS |
| `PAGE_TITLE_WRAPPER_AS_CANDIDATE` | eligible_hits=0 | PASS |
| `DICTIONARY_ASSOCIATION_WRAPPER` | eligible_hits=0 | PASS |
| `DEFINITIONAL_SENTENCE_AS_CANDIDATE` | eligible_hits=0 | PASS |
| `EFFICACY_CLAIM_COPY_AS_CANDIDATE` | eligible_hits=0 | PASS |
| `LISTING_DIMENSION_CONDITION_NOISE` | eligible_hits=0 | PASS |
| `COMPETITOR_BRAND_WRAPPER` | eligible_hits=0 | PASS |
| `SINGLE_SOURCE_AUTO_REJECTION` | eligible_single_source=756 | PASS |
| `MULTI_SOURCE_AUTO_ACCEPTANCE` | rejected_or_held_multi_source=8 | PASS |
| `UNSUPPORTED_DERIVED_QUERY` | explicit_rule_derived=43, unsupported=0 | PASS |
| `EXISTING_IDENTITY_DUPLICATION` | duplicate_normalized_comparison_keys=0 | PASS |

### Named regression assertions

| CANDIDATE_ID | ORIGINAL | FINAL_STATUS | FINAL_ROUTE | RESULT |
|---|---|---|---|---|
| `S07C000316` | Винтажная настольная лампа в форме Будды на одну светоточку | `OUT_OF_SCOPE` | `EXCLUDED_OUT_OF_SCOPE` | PASS |
| `S07C000761` | Настольная лампа с фигурой Будды | `OUT_OF_SCOPE` | `EXCLUDED_OUT_OF_SCOPE` | PASS |
| `S07C000533` | Картхолдер Молот Тора Руна Одал ручной работы из кожи | `OUT_OF_SCOPE` | `EXCLUDED_OUT_OF_SCOPE` | PASS |
| `S07C000579` | Латунный состаренный ваджрный пестик и ступка латунный брелок золотой кулон | `OUT_OF_SCOPE` | `EXCLUDED_OUT_OF_SCOPE` | PASS |
| `S07C000531` | Картина Подкова | `OUT_OF_SCOPE` | `EXCLUDED_OUT_OF_SCOPE` | PASS |
| `S07C001039` | Подсвечник Молот Тора | `OUT_OF_SCOPE` | `EXCLUDED_OUT_OF_SCOPE` | PASS |
| `S07C000241` | Ассоциации к слову «амулет» | `OUT_OF_SCOPE` | `EXCLUDED_OUT_OF_SCOPE` | PASS |
| `S07C000247` | Ассоциации к слову «оберег» | `OUT_OF_SCOPE` | `EXCLUDED_OUT_OF_SCOPE` | PASS |
| `S07C000239` | Ассоциации к словосочетанию «рунические знаки» | `OUT_OF_SCOPE` | `EXCLUDED_OUT_OF_SCOPE` | PASS |
| `S07C000358` | Джапа — это повторение любой мантры или имени Бога | `OUT_OF_SCOPE` | `EXCLUDED_OUT_OF_SCOPE` | PASS |
| `S07C000221` | Амулет с руной Феху — привлекает богатство и благополучие | `OUT_OF_SCOPE` | `EXCLUDED_OUT_OF_SCOPE` | PASS |

Named examples are assertions over the general rules, not the processed
universe. The actual universe remained all 1,548 targets.

## 6. Decision-rule accounting

| DECISION_RULE | TARGET_IDENTITIES |
|---|---|
| `ADJACENT_PRACTICE_OR_SERVICE_CONTENT` | 108 |
| `ADJACENT_PRODUCT_CLASS_OR_WRONG_REFERENT` | 197 |
| `ADJACENT_SOUVENIR_OR_DECOR_CLASS` | 7 |
| `BRAND_WRAPPER_REMOVAL_DERIVED` | 1 |
| `BROAD_MANTRA_PRACTICE_NOT_ASSORTMENT_SUPPORT` | 59 |
| `BROAD_RELIGION_TOPIC_NOT_PRODUCT_SUPPORT` | 11 |
| `CITATION_SECTION_WRAPPER` | 3 |
| `DEFINITIONAL_SENTENCE_NOT_CANDIDATE` | 1 |
| `DICTIONARY_OR_ASSOCIATION_PAGE_WRAPPER` | 207 |
| `DICTIONARY_SENSE_LABEL_WRAPPER` | 4 |
| `EFFICACY_CLAIM_COPY_COMPACT_ALREADY_REPRESENTED` | 2 |
| `EFFICACY_CLAIM_COPY_NOT_CLIENT_FACT` | 4 |
| `EQUESTRIAN_HORSESHOE_INVENTORY_NOT_TALISMAN` | 1 |
| `INDEPENDENT_IN_SCOPE_SEMANTIC_DIRECTION` | 751 |
| `LISTING_DIMENSION_CONDITION_OR_SELLER_NOISE` | 31 |
| `LITERAL_HORSESHOE_OR_DECOR_NOT_TALISMAN` | 11 |
| `LONG_FORM_SPAN_DERIVATION` | 13 |
| `MANUAL_CLASS_INSTANCE_OF_GENERAL_SCOPE_RULE` | 44 |
| `MEDICAL_OR_HEALING_CLAIM_BRANCH` | 8 |
| `OVERSPECIFIED_MARKETPLACE_LISTING_TITLE` | 21 |
| `PAGE_OR_COMPETITOR_BRAND_WRAPPER` | 19 |
| `PUNCTUATION_FORMATTING_CLEANUP` | 1 |
| `REFERENT_REQUIRES_LATER_DEMAND_CONTEXT` | 16 |
| `UI_NOISE_REMOVAL` | 28 |

## 7. Independent hard QA

| INVARIANT | EVIDENCE | RESULT |
|---|---|---|
| `FULL_TARGET_1548_REVIEWED` | 1548/1548 | PASS |
| `TARGET_SILENT_SKIP` | 0 | PASS |
| `ALL_TARGET_PROVENANCE_REVIEWED` | 2633/2633 | PASS |
| `FROZEN_BUSINESS_SCOPE_USED` | 76 Ozon rows + frozen generic category | PASS |
| `UNRELATED_PRODUCT_CLASS_ROUTED_STEP08` | 0 | PASS |
| `PAGE_WRAPPER_ROUTED_STEP08_WHEN_COMPACT_CONCEPT_SHOULD_REPLACE_IT` | 0 | PASS |
| `UNSUPPORTED_DERIVATIONS` | 0 | PASS |
| `CLAIM_LANGUAGE_TREATED_AS_CLIENT_FACT` | 0 | PASS |
| `SINGLE_SOURCE_ONLY_USED_AS_REJECTION_RULE` | false; 756 eligible single-source | PASS |
| `MULTI_SOURCE_ONLY_USED_AS_ACCEPTANCE_RULE` | false; 8 multi-source rejected/held | PASS |
| `KNOWN_REGRESSION_EXAMPLES` | 11/11 | PASS |
| `FULL_VOLUME_REGRESSION_MATRIX` | 13/13 | PASS |
| `SCHEMA_COMPLIANCE` | exact 4/4 headers; required/enums/types valid | PASS |
| `PRIMARY_KEYS_UNIQUE` | 2172 candidates; 1976 URLs; 3948 provenance | PASS |
| `FOREIGN_KEYS_RESOLVE` | all candidate/URL/authority references | PASS |
| `CANDIDATE_SOURCE_COUNTS_RECONCILE` | 2172/2172 | PASS |
| `STEP08_ROUTE_CONSISTENCY` | 2172/2172 | PASS |
| `DEMAND_VALIDATION_STATE` | NOT_VALIDATED_STEP07 for all | PASS |
| `RAW_WORDING_AND_CONTEXT_IMMUTABLE` | 3948/3948 | PASS |
| `NON_TARGET_CANDIDATES_UNCHANGED` | 624/624 | PASS |
| `NON_TARGET_PROVENANCE_UNCHANGED` | 1315/1315 | PASS |
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

## 8. Immutable artifacts

`STEP07_SOURCE_URL_LEDGER.csv`, `STEP07_COMPETITOR_COVERAGE_LEDGER.csv`, and all
seven accepted browser-recovery evidence files are byte-unchanged. Provenance
replacement is required because target statuses, explicit derived normalization,
and review receipts changed; raw evidence fields did not.

```text
STEP07_SOURCE_URL_LEDGER_SHA256 = f923c412f00fdb318bd57c0610ca404d8093a3a7cad4d7c71e2c31e86de568f7
STEP07_COMPETITOR_COVERAGE_LEDGER_SHA256 = 0ee233a792d9e97b1b3d45fe051ce2068f261fd0b53dc1408b6cd7345483c898
SOURCE_URL_REPLACEMENT_REQUIRED = false
COMPETITOR_COVERAGE_REPLACEMENT_REQUIRED = false
PROVENANCE_REPLACEMENT_REQUIRED = true
```

## 9. Universal quality score

| DIMENSION | SCORE / 10 | BASIS |
|---|---|---|
| Goal and output completeness | 10 | All 1548 targets and 2633 linked evidence rows reviewed. |
| Method and source support | 10 | Frozen business/assortment and accepted Step07 corpus only. |
| Input evidence and provenance integrity | 10 | Raw wording/context immutable; source counts recomputed. |
| Coverage and completeness | 10 | Zero silent skips; full candidate/provenance universe reconciled. |
| Analytical correctness and claim boundaries | 9 | Business referent precedes token overlap; claims remain competitor evidence. |
| Adversarial QA quality | 10 | 13/13 full-volume regression classes pass. |
| Persistence/readback/reproducibility | 10 | Explicit rules, decision notes, review hashes, stable IDs. |
| Owner/client usability/plain language | 9 | Four-file atomic replacement package and one transport ZIP. |
| Information gain/cost/execution efficiency | 10 | No acquisition/provider calls; accepted corpus reused. |
| Downstream readiness | 10 | 794-candidate Step08 queue; Step08 not started. |

```text
QUALITY_TOTAL = 98 / 100
QUALITY_SCORE = 9.8 / 10
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
