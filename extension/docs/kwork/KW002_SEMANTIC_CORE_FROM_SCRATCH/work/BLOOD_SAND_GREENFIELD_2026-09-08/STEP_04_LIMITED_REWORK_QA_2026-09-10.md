# STEP 04 — LIMITED CORRECTIVE REWORK QA

Дата: 2026-09-10  
Статус: **PASS**  
Объект проверки: ограниченная коррекция первого Step04 после принятого внешнего аудита. Это не Step05.

## 1. Источник и воспроизводимость

- Замороженный оригинал Step04: `91fc6e1ce155c0f854c9d3c7ebf5a7b5dea40d70`.
- Принятый внешний аудит: content commit `cf5fe62`, final-readback commit `54dffce`.
- Исходный классификатор повторно запущен на полном реконструированном корпусе. До коррекции он в точности воспроизвёл 25 непустых original-family counts и 25,979 occurrences замороженного результата.
- Использованы только разрешённые end-of-Step04 источники и клиентские ассортиментные authorities. Post-Step04/Step05 evidence в правила не включалось.
- Исторические исходные Step04-файлы не изменены: family blob `e3922acb63ada6705a5d98b453e37705a455afb8`, queue blob `77f48776bdae85fa93983fcf24cda2bba84f10da`.

## 2. Обязательное полное accounting

| Проверка | Результат |
|---|---:|
| INPUT_PRIMARY_PROBES_ACCOUNTED | **79/79 PASS** |
| SOURCE_CARRIERS_READ_OR_RECONSTRUCTED | **79/79 PASS** |
| RESULT_OCCURRENCES | **24,722** |
| ASSOCIATION_OCCURRENCES | **1,257** |
| TOTAL_OCCURRENCES | **25,979** |
| OCCURRENCE_LEDGER_ROWS | **25,979** |
| UNIQUE_OCCURRENCE_IDS | **25,979** |
| UNASSIGNED_OCCURRENCES | **0** |
| DUPLICATE_OCCURRENCE_IDS | **0** |
| FAMILY_OCCURRENCE_SUM | **25,979** |
| SILENT_SOURCE_DROPS | **0** |
| EMPTY_SOURCE_RUNS | **7: 49, 50, 51, 57, 66, 67, 70** |
| RUNS_REPRESENTED_IN_FAMILY_PROVENANCE | **79/79** |
| FAMILY_ROWS_CORRECTED | **31** |

Повторяющаяся фраза в разных run/channel сохранена как отдельная occurrence identity. Дедупликации на входе или в canonical ledger нет.

Канонический accounting gate:

```text
CANONICAL_PRIMARY_PROBES = 79
CURRENT_SOURCE_RESOLUTION = 79/79
RESULT_OCCURRENCES = 24722
ASSOCIATION_OCCURRENCES = 1257
TOTAL_OCCURRENCES = 25979
OCCURRENCE_LEDGER_ROWS = 25979
UNIQUE_OCCURRENCE_IDS = 25979
UNASSIGNED_OCCURRENCE_IDS = 0
DUPLICATE_OCCURRENCE_IDS = 0
LEDGER_RESULTS_ROWS = 24722
LEDGER_ASSOCIATION_ROWS = 1257
FAMILY_OCCURRENCE_SUM = 25979
FAMILY_LEDGER_COUNT_RECONCILIATION = PASS
EMPTY_CURRENT_RUNS = 49,50,51,57,66,67,70
EMPTY_CURRENT_RUN_COUNT = 7
```

## 3. Регрессии принятых исправлений

| Дефект/требование | Проверка | Результат |
|---|---|---:|
| F010 | umbrella явно разбит в reason text на meaning/history/mythology, image/photo, runes, tattoo/body-art; кластер/page не заявлены | **PASS** |
| F011 | occurrences с `детектив*` или `детектор*` в F011 | **0 PASS** |
| F015 | label/reason охватывают модели, детали, краску/цвет и vehicle-fit; явный fit-context перенесён | **PASS** |
| F017 | недостаточно квалифицированные `счастлив* амулет` не форсируются в media | **0 remaining PASS** |
| F022 | голый/неразрешённый `талисман кота` не объявляется явно чужим; Cat Noir — explicit media | **0 remaining PASS** |
| F025 | explicit `для водителя` после коррекции | **0 PASS** |
| F025 | explicit vehicle-fit `подходят на амулет` после коррекции | **0 PASS** |
| F032 | standalone gap row | **0; REMOVED PASS** |
| run70 | provenance включён в F003 с zero-outcome и без вывода о спросе exact-form | **PASS** |
| E004+E017 | объединены в E004, owner fact first | **PASS** |
| E007+E014 | объединены в E014, run70 не создаёт отдельного expansion item | **PASS** |

KNOWN_AUDITED_DEFECTS_REMAINING = **0**.

Канонический regression gate:

```text
F010_BOUNDARY_WORDING_FIXED = PASS
F011_MEDIA_LEAK_FIXED = PASS
F015_AUTOMOTIVE_LABEL_OR_ROUTING_FIXED = PASS
F017_BARE_HAPPY_AMULET_NOT_FORCED_MEDIA = PASS
F022_BARE_CAT_TALISMAN_NOT_FORCED_OUT = PASS
F025_SUPPORTED_CAR_USE_MOVED_TO_F003 = PASS
F032_STANDALONE_GAP_REMOVED = PASS
E004_E017_CONSOLIDATED = PASS
E007_E014_CONSOLIDATED = PASS
CORRECTED_QUEUE_ROWS = 15
OWNER_OR_CLIENT_FACT_ROWS = 5
PROVIDER_RELEVANT_QUEUE_ROWS = 13
KNOWN_AUDIT_DEFECTS_REMAINING = 0
```

## 4. Изменения occurrence→family

- Всего изменено назначений: **68**.
- Прямо названные audit examples (с учётом двух независимых occurrence identity bare `счастливый амулет`): **5**.
- Дополнительные sibling occurrences, изменённые теми же исправленными правилами: **63**.

| corrected rule | changed occurrences |
|---|---:|
| C01_FALSE_AUDIENCE_PREFIX_DETECTOR | 1 |
| C01_MEDIA_TOKEN_BOUNDARY_DETECTIVE | 10 |
| C02_BARE_HAPPY_AMULET_ASSOCIATION_HOLD | 1 |
| C02_HAPPY_AMULET_EFFECT_HOLD | 1 |
| C02_HAPPY_AMULET_INFORMATION_HOLD | 1 |
| C02_HAPPY_AMULET_UNQUALIFIED_HOLD | 46 |
| C03_EXPLICIT_CAT_NOIR_MEDIA | 1 |
| C03_UNQUALIFIED_CAT_TALISMAN_HOLD | 4 |
| C04_EXPLICIT_DRIVER_CAR_USE | 2 |
| C05_EXPLICIT_VEHICLE_FIT_CONTEXT | 1 |

| family | old count | corrected count | delta |
|---|---:|---:|---:|
| F003 | 144 | 146 | +2 |
| F010 | 1262 | 1263 | +1 |
| F011 | 254 | 244 | -10 |
| F013 | 1093 | 1094 | +1 |
| F015 | 488 | 489 | +1 |
| F017 | 1718 | 1680 | -38 |
| F022 | 109 | 104 | -5 |
| F025 | 3312 | 3360 | +48 |

Полный перечень всех изменённых назначений:

| occurrence_id | phrase | old | new | rule | scope |
|---|---|---:|---:|---|---|
| R001\|results\|0002 | счастливый амулет | F017 | F025 | C02_HAPPY_AMULET_UNQUALIFIED_HOLD | KNOWN_AUDIT_EXAMPLE |
| R001\|results\|0009 | счастливый амулет и город | F017 | F025 | C02_HAPPY_AMULET_UNQUALIFIED_HOLD | ADDITIONAL_SIBLING |
| R001\|results\|0010 | счастливый амулет и город перестал | F017 | F025 | C02_HAPPY_AMULET_UNQUALIFIED_HOLD | ADDITIONAL_SIBLING |
| R001\|results\|0099 | счастливый амулет новое | F017 | F025 | C02_HAPPY_AMULET_UNQUALIFIED_HOLD | ADDITIONAL_SIBLING |
| R001\|results\|0130 | счастливый амулет последнее | F017 | F025 | C02_HAPPY_AMULET_UNQUALIFIED_HOLD | ADDITIONAL_SIBLING |
| R001\|results\|0249 | счастливый амулет маковые | F017 | F025 | C02_HAPPY_AMULET_UNQUALIFIED_HOLD | ADDITIONAL_SIBLING |
| R001\|results\|0317 | счастливый амулет история | F017 | F010 | C02_HAPPY_AMULET_INFORMATION_HOLD | ADDITIONAL_SIBLING |
| R001\|results\|0358 | счастливый амулет путь | F017 | F025 | C02_HAPPY_AMULET_UNQUALIFIED_HOLD | ADDITIONAL_SIBLING |
| R001\|results\|0359 | счастливый амулет калинов | F017 | F025 | C02_HAPPY_AMULET_UNQUALIFIED_HOLD | ADDITIONAL_SIBLING |
| R001\|results\|0383 | счастливый амулет хутор | F017 | F025 | C02_HAPPY_AMULET_UNQUALIFIED_HOLD | ADDITIONAL_SIBLING |
| R001\|results\|0398 | счастливый амулет калина хутор | F017 | F025 | C02_HAPPY_AMULET_UNQUALIFIED_HOLD | ADDITIONAL_SIBLING |
| R001\|results\|0425 | счастливый амулет ч | F017 | F025 | C02_HAPPY_AMULET_UNQUALIFIED_HOLD | ADDITIONAL_SIBLING |
| R001\|results\|0435 | счастливый амулет стеклянная | F017 | F025 | C02_HAPPY_AMULET_UNQUALIFIED_HOLD | ADDITIONAL_SIBLING |
| R001\|results\|0509 | счастливый амулет ушла | F017 | F025 | C02_HAPPY_AMULET_UNQUALIFIED_HOLD | ADDITIONAL_SIBLING |
| R001\|results\|0544 | счастливый амулет когда уже не ждешь | F017 | F025 | C02_HAPPY_AMULET_UNQUALIFIED_HOLD | ADDITIONAL_SIBLING |
| R001\|results\|0551 | счастливый амулет когда уже ничего не ждешь | F017 | F025 | C02_HAPPY_AMULET_UNQUALIFIED_HOLD | ADDITIONAL_SIBLING |
| R001\|results\|0579 | счастливый амулет от судьбы | F017 | F025 | C02_HAPPY_AMULET_UNQUALIFIED_HOLD | ADDITIONAL_SIBLING |
| R001\|results\|0583 | от судьбы не уйти счастливый амулет | F017 | F025 | C02_HAPPY_AMULET_UNQUALIFIED_HOLD | ADDITIONAL_SIBLING |
| R001\|results\|0607 | счастливый амулет новый город перестал дышать | F017 | F025 | C02_HAPPY_AMULET_UNQUALIFIED_HOLD | ADDITIONAL_SIBLING |
| R001\|results\|0616 | счастливый амулет чужие | F017 | F025 | C02_HAPPY_AMULET_UNQUALIFIED_HOLD | ADDITIONAL_SIBLING |
| R001\|results\|0663 | счастливый амулет муж | F017 | F025 | C02_HAPPY_AMULET_UNQUALIFIED_HOLD | ADDITIONAL_SIBLING |
| R001\|results\|0692 | счастливый амулет алена | F017 | F025 | C02_HAPPY_AMULET_UNQUALIFIED_HOLD | ADDITIONAL_SIBLING |
| R001\|results\|0929 | счастливый амулет измена | F017 | F025 | C02_HAPPY_AMULET_UNQUALIFIED_HOLD | ADDITIONAL_SIBLING |
| R001\|results\|1078 | счастливый амулет чашка | F017 | F025 | C02_HAPPY_AMULET_UNQUALIFIED_HOLD | ADDITIONAL_SIBLING |
| R001\|results\|1126 | счастливый амулет клюквино | F017 | F025 | C02_HAPPY_AMULET_UNQUALIFIED_HOLD | ADDITIONAL_SIBLING |
| R001\|results\|1141 | счастливый амулет счастливый билет | F017 | F025 | C02_HAPPY_AMULET_UNQUALIFIED_HOLD | ADDITIONAL_SIBLING |
| R001\|results\|1247 | счастливый амулет в новую жизнь | F017 | F025 | C02_HAPPY_AMULET_UNQUALIFIED_HOLD | ADDITIONAL_SIBLING |
| R001\|results\|1260 | счастливый амулет билет в новую | F017 | F025 | C02_HAPPY_AMULET_UNQUALIFIED_HOLD | ADDITIONAL_SIBLING |
| R001\|results\|1265 | счастливый амулет когда поют | F017 | F025 | C02_HAPPY_AMULET_UNQUALIFIED_HOLD | ADDITIONAL_SIBLING |
| R001\|results\|1290 | счастливый амулет любить | F017 | F025 | C02_HAPPY_AMULET_UNQUALIFIED_HOLD | ADDITIONAL_SIBLING |
| R001\|results\|1331 | счастливый амулет странная женщина | F017 | F011 | C02_HAPPY_AMULET_EFFECT_HOLD | ADDITIONAL_SIBLING |
| R001\|results\|1353 | алена берндт счастливый амулет | F017 | F025 | C02_HAPPY_AMULET_UNQUALIFIED_HOLD | ADDITIONAL_SIBLING |
| R001\|results\|1396 | счастливый амулет эта странная | F017 | F025 | C02_HAPPY_AMULET_UNQUALIFIED_HOLD | ADDITIONAL_SIBLING |
| R001\|results\|1412 | счастливый амулет седьмая | F017 | F025 | C02_HAPPY_AMULET_UNQUALIFIED_HOLD | ADDITIONAL_SIBLING |
| R001\|results\|1422 | счастливый амулет старая старая жена | F017 | F025 | C02_HAPPY_AMULET_UNQUALIFIED_HOLD | ADDITIONAL_SIBLING |
| R001\|results\|1485 | от каких машин подходят на амулет | F025 | F015 | C05_EXPLICIT_VEHICLE_FIT_CONTEXT | ADDITIONAL_SIBLING |
| R001\|results\|1536 | счастливый амулет новая старая | F017 | F025 | C02_HAPPY_AMULET_UNQUALIFIED_HOLD | ADDITIONAL_SIBLING |
| R001\|results\|1537 | счастливый амулет новая старая жена | F017 | F025 | C02_HAPPY_AMULET_UNQUALIFIED_HOLD | ADDITIONAL_SIBLING |
| R001\|results\|1538 | счастливый амулет дорога домой | F017 | F025 | C02_HAPPY_AMULET_UNQUALIFIED_HOLD | ADDITIONAL_SIBLING |
| R001\|results\|1556 | счастливый амулет любить запрещается | F017 | F025 | C02_HAPPY_AMULET_UNQUALIFIED_HOLD | ADDITIONAL_SIBLING |
| R001\|results\|1564 | на выход счастливый амулет | F017 | F025 | C02_HAPPY_AMULET_UNQUALIFIED_HOLD | ADDITIONAL_SIBLING |
| R001\|results\|1565 | счастливый амулет прошу | F017 | F025 | C02_HAPPY_AMULET_UNQUALIFIED_HOLD | ADDITIONAL_SIBLING |
| R001\|results\|1566 | счастливый амулет прошу на выход | F017 | F025 | C02_HAPPY_AMULET_UNQUALIFIED_HOLD | ADDITIONAL_SIBLING |
| R001\|results\|1615 | счастливый амулет кукуево | F017 | F025 | C02_HAPPY_AMULET_UNQUALIFIED_HOLD | ADDITIONAL_SIBLING |
| R001\|results\|1654 | счастливый амулет г | F017 | F025 | C02_HAPPY_AMULET_UNQUALIFIED_HOLD | ADDITIONAL_SIBLING |
| R001\|results\|1681 | счастливый амулет за озером | F017 | F025 | C02_HAPPY_AMULET_UNQUALIFIED_HOLD | ADDITIONAL_SIBLING |
| R001\|results\|1691 | детектор амулет | F011 | F025 | C01_FALSE_AUDIENCE_PREFIX_DETECTOR | ADDITIONAL_SIBLING |
| R001\|results\|1710 | счастливый амулет сегодня | F017 | F025 | C02_HAPPY_AMULET_UNQUALIFIED_HOLD | ADDITIONAL_SIBLING |
| R001\|results\|1795 | счастливый амулет коробка | F017 | F025 | C02_HAPPY_AMULET_UNQUALIFIED_HOLD | ADDITIONAL_SIBLING |
| R001\|results\|1931 | та что тебя хранит счастливый амулет | F017 | F025 | C02_HAPPY_AMULET_UNQUALIFIED_HOLD | ADDITIONAL_SIBLING |
| R002\|results\|1182 | оберег для водителя | F025 | F003 | C04_EXPLICIT_DRIVER_CAR_USE | ADDITIONAL_SIBLING |
| R003\|results\|0006 | талисман кота | F022 | F025 | C03_UNQUALIFIED_CAT_TALISMAN_HOLD | KNOWN_AUDIT_EXAMPLE |
| R003\|results\|0420 | как сделать талисман кота | F022 | F025 | C03_UNQUALIFIED_CAT_TALISMAN_HOLD | ADDITIONAL_SIBLING |
| R003\|results\|1048 | как выглядит талисман кота | F022 | F025 | C03_UNQUALIFIED_CAT_TALISMAN_HOLD | ADDITIONAL_SIBLING |
| R003\|results\|1354 | владелец талисмана кота | F022 | F025 | C03_UNQUALIFIED_CAT_TALISMAN_HOLD | ADDITIONAL_SIBLING |
| R003\|results\|1907 | талисман кота нуара | F022 | F017 | C03_EXPLICIT_CAT_NOIR_MEDIA | ADDITIONAL_SIBLING |
| R014\|results\|0013 | сельский детектив чернобог | F011 | F017 | C01_MEDIA_TOKEN_BOUNDARY_DETECTIVE | KNOWN_AUDIT_EXAMPLE |
| R014\|results\|0016 | детектив месть чернобога | F011 | F017 | C01_MEDIA_TOKEN_BOUNDARY_DETECTIVE | ADDITIONAL_SIBLING |
| R014\|results\|0018 | сельский детектив месть чернобога | F011 | F017 | C01_MEDIA_TOKEN_BOUNDARY_DETECTIVE | ADDITIONAL_SIBLING |
| R014\|results\|0038 | сельский детектив 2 месть чернобога | F011 | F017 | C01_MEDIA_TOKEN_BOUNDARY_DETECTIVE | ADDITIONAL_SIBLING |
| R014\|results\|0067 | сельский детектив месть чернобога 2019 | F011 | F017 | C01_MEDIA_TOKEN_BOUNDARY_DETECTIVE | ADDITIONAL_SIBLING |
| R014\|results\|0074 | сельский детектив серии месть чернобога | F011 | F017 | C01_MEDIA_TOKEN_BOUNDARY_DETECTIVE | ADDITIONAL_SIBLING |
| R014\|results\|0119 | сельский детектив месть чернобога онлайн | F011 | F017 | C01_MEDIA_TOKEN_BOUNDARY_DETECTIVE | ADDITIONAL_SIBLING |
| R014\|results\|0168 | сельский детектив месть чернобога 1 | F011 | F017 | C01_MEDIA_TOKEN_BOUNDARY_DETECTIVE | ADDITIONAL_SIBLING |
| R014\|results\|0377 | сельский детектив месть чернобога содержание | F011 | F017 | C01_MEDIA_TOKEN_BOUNDARY_DETECTIVE | ADDITIONAL_SIBLING |
| R014\|results\|0446 | х ф сельский детектив месть чернобога | F011 | F017 | C01_MEDIA_TOKEN_BOUNDARY_DETECTIVE | ADDITIONAL_SIBLING |
| R061\|associations\|0001 | счастливый амулет | F017 | F013 | C02_BARE_HAPPY_AMULET_ASSOCIATION_HOLD | KNOWN_AUDIT_EXAMPLE |
| R075\|results\|0002 | оберег для водителя и автомобиля | F025 | F003 | C04_EXPLICIT_DRIVER_CAR_USE | KNOWN_AUDIT_EXAMPLE |

## 5. Исправленная expansion queue

| Проверка | Значение |
|---|---:|
| CORRECTED_QUEUE_ROWS | **15 PASS** |
| OWNER_OR_CLIENT_FACT_ROWS | **5 PASS** |
| PROVIDER_RELEVANT_ROWS (`provider_call_required != NO`) | **13 PASS** |
| QUEUE_ROWS_WITH_SUPERSESSION | **15/15 PASS** |
| QUEUE_ROWS_WITH_INFORMATION_GAIN_STOPPING_RULE | **15/15 PASS** |

## 6. Запрещённые действия и границы

| Проверка | Результат |
|---|---:|
| NEW_PROVIDER_CALLS | **0** |
| WORDSTAT / SEARCH / GENSEARCH / ALICE / AI-SEARCH CALLS | **0** |
| SEALED_SOURCE_VIOLATIONS | **0** |
| POST_STEP04_EVIDENCE_USED_IN_CORRECTION_LOGIC | **0** |
| LOW_FREQUENCY_ONLY_REJECTIONS | **0** |
| FORCED_AMBIGUITY_DECISIONS | **0** |
| FINAL_ROW_CLEANUP_PERFORMED | **false** |
| FINAL_CLUSTERING_PERFORMED | **false** |
| QUERY_TO_PAGE_OWNERSHIP_PERFORMED | **false** |
| IA_OR_PAGE_JOBS_PERFORMED | **false** |
| STEP05_ADVANCED | **false** |
| STEP06_STARTED | **false** |

```text
NEW_PROVIDER_CALLS = 0
POST_STEP04_PROVIDER_EVIDENCE_USED_IN_REWORK = 0
SEALED_SOURCE_VIOLATIONS = 0
FINAL_ROW_CLEANUP_PERFORMED = false
FINAL_SERP_CLUSTERING_PERFORMED = false
QUERY_PAGE_OWNERSHIP_PERFORMED = false
PAGE_OR_IA_DESIGN_PERFORMED = false
STEP05_ADVANCED = false
STEP06_PLUS_STARTED = false
```

## 7. Итог QA

`STEP_04_LIMITED_REWORK_QA = PASS`  
`CORPUS_ACCOUNTING = 25,979 / 25,979`  
`CORRECTED_FAMILY_ROWS = 31`  
`CORRECTED_QUEUE_ROWS = 15`  
`NEXT_STEP_EXECUTED = false`
