# OKNO_MSK — аудит данных для отдельного семантического ядра

**Статус:** `COMPLETE__PERSISTED_IN_GITHUB__STANDALONE_XLSX_NOT_MATERIALIZED`  
**Проверенный branch HEAD:** `d4e88e1f406c91b544a40c7ed10287f41da26f7f`  
**Граница:** документы №01–№03 не изменялись; новое ядро не создавалось; provider-вызовы не выполнялись.

## 1. Итог

Подозрение об отсутствии частотности подтверждено только частично. Числовой Wordstat count сохранён для каждой из 2 840 уникальных фраз, однако это broad `getTop` snapshot по Москве без операторов, а не exact/phrase-match частотность.

Для базового отдельного semantic core новых provider-вызовов не требуется. Нужна новая локальная материализация из текущих canonical authorities. Старый `step19_correction_materialized/STEP_19_03_SEMANTIC_CORE_MATERIALIZED.csv` содержит корректный demand/provenance слой, но его cluster/page/intent-поля предшествуют Stage-5 rebuild и не могут использоваться как финальная authority.

## 2. Reconciliation

```text
Wordstat pass 1                         2 415
Targeted Wordstat expansion               550
Raw rows before deduplication            2 965
Unique phrases after deduplication       2 840
Active phrases                           2 332
Assigned phrases                         2 313
SEARCH_REQUIRED                             19
Canonical structural units                 168
```

Stage-5 states:

| State | Rows |
|---|---:|
| ASSIGNED | 2 271 |
| ASSIGNED_HOLD | 42 |
| SEARCH_REQUIRED | 19 |
| REVIEW_DEFERRED | 174 |
| EXCLUDED_PRESERVED | 334 |
| **Total** | **2 840** |

Raw phrase set and Stage-5 phrase set are identical: missing on either side = `0`. Stage-8 frequency/provenance values reconcile to raw normalized Wordstat rows with `0` mismatches.

## 3. What we already have

| Field | Present | Coverage | Source | Notes |
|---|---|---:|---|---|
| Search phrase | YES | 2 840/2 840 | Stage-5 final semantic master | Unique phrase key; duplicates in master = 0 |
| Region | YES, not surfaced row-by-row in Stage-5 | 22/22 collection packets | Step-03R/Step-05 raw normalized files | Moscow, region `213` |
| Devices | YES | 22/22 packets | Step-03R/Step-05 | `DEVICE_ALL` |
| Observed Wordstat count | YES | 2 840/2 840 | Step-08 + raw normalized files | Every value is positive |
| Frequency semantics | YES | all packets | Step-02/Step-05 manifests | `getTop`, operators `NONE`, broad snapshot |
| Phrase-level measurement | YES | 2 840/2 840 | raw normalized files | Not inherited from a cluster or seed |
| Result/association role | YES | 2 840/2 840 | Step-08 | Every active phrase has a result count |
| Demand source/provenance | YES | 2 840/2 840 | Step-08 | `source_ids` and row-level provenance |
| Final semantic status | YES | 2 840/2 840 | Stage-5 master | Includes active, hold, unresolved, deferred and excluded |
| Final structural unit | YES where assigned | 2 313/2 332 active | Stage-5 master | The 19 SEARCH_REQUIRED rows intentionally have no unit |
| Canonical unit task | YES | 168/168 units | Stage-5 unit authority | Readable but currently English |
| Russian final cluster label | NOT MATERIALIZED | 0/168 | local derivation required | Can be produced from canonical unit task |
| Canonical representative phrase | NOT MATERIALIZED | 0/168 | local derivation required | Can be calculated for 168/168 units |
| Intent | YES where assigned | 2 313/2 313 | Stage-5 master | Not invented for unresolved rows |
| Business boundary | YES where assigned | 2 313/2 313 | Stage-5 master | IN_SCOPE/OUTSIDE/NO_STANDALONE/DEFERRED variants |
| Previous Step-11 target URL | PARTIAL | 1 647/2 313 | Stage-11 embedded in Stage-5 | Historical/pre-final mapping only |
| Final primary page | YES where permitted | 1 920/2 313 | Stage-5 master | 60 unique final URLs |
| Final supporting pages | PARTIAL | 1 051/2 313 | Stage-5 master | Blank is allowed when no support page is canonical |
| Structural action | YES | 2 313/2 313 | Stage-5 master/unit authority | KEEP/ROUTE/NO_STANDALONE/DEFER/etc. |
| Confidence/maturity | YES | 2 313/2 313 | Stage-5 master | Not a traffic or revenue forecast |
| Uncertainty/claim boundary | YES | 2 840/2 840 | Stage-5 master | Uncertainty is preserved |
| Phrase-level priority | NO | 0/2 332 | local derivation required | Step-18 priority is action-level, not phrase-level |

## 4. Frequency — exact answer

The 22 acquisition packets contain 2 965 raw rows: 2 636 `result` rows and 329 `association` rows. All 2 965 rows contain a positive numerical count.

After deduplication:

```text
unique phrases with a positive observed count = 2 840/2 840
result-only phrases                         = 2 572
association-only phrases                    =   259
result + association phrases                =     9
```

For the active set:

```text
active phrases                              = 2 332
active with own result count                = 2 332/2 332
result-only active phrases                  = 2 323
result + association active phrases         =     9
association-only active phrases             =     0
```

All 22 collections used:

```text
method = getTop
region = 213
devices = DEVICE_ALL
operators = NONE
```

The count is attached to the exact text returned in the provider row; it is not inherited from a seed or cluster. It is nevertheless a broad Wordstat query count and is not exact-match frequency. The project correctly records this boundary as `OBSERVED_PROVIDER_COUNT_NOT_GUARANTEED_EXACT_QUERY_FREQUENCY`.

There were 125 duplicate occurrences across 101 repeated phrases. Six repeated phrases had differing counts; the accepted demand layer preserves the maximum observed result and association count separately.

Existing broad counts are sufficient for filtering, rough sorting, representative selection and bounded demand comparison. They are not sufficient for a precise traffic forecast or an unqualified exact-demand ranking.

## 5. Cluster and page audit

- Assigned phrases: `2 313`; every assigned phrase has one final structural unit.
- Final units: `168`; missing unit-authority rows = `0`.
- Unit contract conflicts = `0`.
- Units containing multiple final primary-page decisions = `0`.
- Duplicate phrase keys across final units = `0`.
- SEARCH_REQUIRED: `19`; their unit/page remains intentionally unresolved.
- Every unit has a canonical user task, but no standalone Russian display label or canonical representative field is persisted.
- A representative can be derived locally for all 168 units from the highest observed active result count, with deterministic tie-breaking.

Final page coverage among assigned phrases:

```text
final page present                          1 920
final page intentionally absent               393
  NO_STANDALONE_PAGE                           246
  OUTSIDE_SCOPE_NO_ACTION                      115
  DEFER_PENDING_EVIDENCE                        32
```

The 393 blank URLs are governed outcomes, not missing joins. The standalone core must expose the reason rather than silently filling a URL.

Cluster-level demand can be calculated locally. Because broad query counts overlap, `SUM` must be labelled as a non-additive indicator rather than unique market volume. Cluster summaries should expose member count, maximum, median and explicitly labelled broad-count sum.

## 6. Existing materializations

### Old Step-19 semantic core

`step19_correction_materialized/STEP_19_03_SEMANTIC_CORE_MATERIALIZED.csv` contains all 2 332 active phrases and its Wordstat counts match Step-08 with zero frequency mismatches. It must not be reused as current semantic/page authority because it was built from Step-08/10/11 before the Stage-5 rebuild.

Compared with current Stage-5:

```text
cluster/unit mismatches                      803
user-task mismatches                         851
intent mismatches                            185
target URL mismatches                        518
```

### Rebuilt research workbook

`OKNO_MSK_REBUILT_RESEARCH_WORKBOOK_2026-09-05.xlsx` contains the current 2 840-row Stage-5 semantic master and 168 units, but its Semantic Master sheet does not expose Wordstat counts, region, demand source IDs, final Russian cluster labels, representatives or phrase-level priority. It is a broader research workbook, not the required separate semantic-core deliverable.

## 7. Gaps before delivery

### A. Derivable locally

- Join Step-08 observed result/association counts and provenance to Stage-5 by normalized phrase.
- Add Moscow/213, DEVICE_ALL and explicit metric type.
- Create Russian labels for 168 final units.
- Derive representative phrase for every final unit.
- Calculate within-cluster and within-page demand ranks.
- Calculate cluster/page summaries with non-additive broad-count labels.
- Expose active/excluded/deferred/unresolved flags.

### B. Formatting/joining/normalization only

- Build a new standalone semantic-core XLSX rather than extracting the old Step-19 view.
- Expose previous mapping separately from final Stage-5 target.
- Normalize URL display without changing canonical page decisions.
- Preserve blank target pages together with the canonical no-page/deferred/outside reason.

### C. External collection genuinely required

`NONE_FOR_BASE_STANDALONE_CORE`.

### D. Optional, not required for delivery

- phrase-match/operator-based Wordstat frequency;
- additional historical dynamics beyond the four preserved diagnostic roots;
- Webmaster/Metrika metrics;
- conversion, revenue or traffic forecasting.

If precise phrase-level demand ranking is commissioned later, the justified optional collection subset is all 2 332 active phrases, not the 508 excluded/deferred phrases and not only 168 representatives. Controls: Moscow region `213`, `DEVICE_ALL`, one consistent snapshot, operator-based phrase-match metric, join by normalized exact phrase.

## 8. Recommended standalone schema

Ordered phrase-level columns:

1. `ID фразы`
2. `Поисковая фраза`
3. `Статус фразы`
4. `В рабочем ядре`
5. `Регион`
6. `Код региона`
7. `Устройства`
8. `Wordstat result count`
9. `Wordstat association count`
10. `Тип частотности`
11. `Правило агрегации`
12. `Источники Wordstat`
13. `Количество source occurrences`
14. `Дата снимка`
15. `ID структурной единицы`
16. `Кластер`
17. `Основной запрос кластера`
18. `Пользовательская задача`
19. `Интент`
20. `Граница бизнеса`
21. `Уверенность назначения`
22. `URL до финальной сверки`
23. `Финальная целевая страница`
24. `Поддерживающие страницы`
25. `Роль страницы`
26. `Рекомендация`
27. `Готовность решения`
28. `Неопределённость`
29. `Что нужно для пересмотра`
30. `Ранг внутри кластера`
31. `Ранг внутри страницы`
32. `Операционный приоритет`
33. `Основание приоритета`
34. `Комментарий / граница вывода`
35. `Provenance`

## 9. Recommended file structure

One standalone XLSX with sheets:

1. `01_Все_фразы` — all 2 840 unique rows, including deferred and excluded.
2. `02_Активное_ядро` — 2 332 active rows.
3. `03_Кластеры` — 168 final units with representatives, demand indicators, page and action.
4. `04_Страницы` — 60 final URLs plus governed no-page/outside/deferred groups.
5. `05_SEARCH_REQUIRED` — the 19-row resolution queue.
6. `06_Справочник` — metric, status, priority and reopen definitions.

An optional CSV export of `02_Активное_ядро` may accompany the XLSX, but it must be generated from the same joined truth.

## 10. Final verdict

For a complete standalone semantic core, the project already has the full 2 840-phrase universe, Moscow broad Wordstat counts for every phrase, 2 332 active states, 2 313 final assignments, 168 final structural units and the current Stage-5 page/action authority.

What is missing is not provider data but current standalone materialization: Stage-5 must be joined with Step-08 frequency/provenance and Stage-5 unit authority, then exposed through Russian cluster labels, representatives, ranks and operational summaries.

```text
BASE_PROVIDER_COLLECTION_REQUIRED = false
OLD_STEP19_SEMANTIC_CORE_FINAL_AUTHORITY = false
STANDALONE_SEMANTIC_CORE_XLSX_MATERIALIZED = false
NEXT_ACTION = MATERIALIZE_NEW_STANDALONE_SEMANTIC_CORE_XLSX_FROM_STAGE5_FINAL_SEMANTIC_TRUTH__STEP08_FREQUENCY_PROVENANCE__STAGE5_UNIT_AUTHORITY
```
