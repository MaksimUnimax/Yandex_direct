# OKNO_MSK — фактические метрики MK02-only rehearsal

Дата: **2026-09-10**  
Назначение: вход для будущего Phase 8. **Цена и коммерческие лимиты здесь не назначаются.**

## Объём данных и решений

| Метрика | Факт |
|---|---:|
| Native semantic source rows / unique phrases | 2 840 / 2 840 |
| Working / review-uncertain / excluded | 2 185 / 187 / 468 |
| Total / working / outside groups | 59 / 54 / 5 |
| Active phrase→page mapping rows | 2 185 |
| Exact existing owner / no suitable exact page / outside / unresolved | 1 647 / 518 / 14 / 6 |
| Preserved unit ledger / active ownership units | 168 / 160 |
| Candidate ledgers / candidate comparisons | 59 / 105 |
| Current public topology nodes processed | 2 683 |
| Current relevant pages exposed to client | 80 |
| Known critical rechecks / independently discovered material pages | 59 / 21 |
| Successfully read/opened page states | 1 700 |
| Fetch error / non-HTML states preserved | 676 / 307 |
| Current internal edges raw / unique | 15 / 14 |
| Unique literal present / absent-planned relations | 8 / 6 |
| Preserved Search evidence reused | 85 observations |
| Competing-page cases / effective pair evidence | 21 / 199 |
| Private-history evidence reused | 0 — unavailable/not required for bounded claim |
| Target active units / unique existing family-owner pages | 160 / 59 |
| Unit→support relations | 103 |
| Current→target page deltas / relation deltas / total | 21 / 14 / 35 |

## Structural action volume

| Класс | Количество |
|---|---:|
| KEEP_EXISTING_STRUCTURE | 70 |
| SEMANTIC_MAPPING_ONLY | 45 |
| DEFER | 19 |
| NO_CHANGE class | 18 |
| CONTENT_CHANGE | 8 |
| CREATE | 0 |
| SPLIT | 0 |
| MERGE | 0 |
| Redirect/delete | 0 |

По disposition: **NO_CHANGE 133 / DEFER 19 / ACTION 8**. Эти числа не следует смешивать с пятью более узкими action classes выше.

## Implementation work packages

| Состояние | Количество |
|---|---:|
| READY_IMPLEMENTATION_SPEC | 3 |
| PENDING_BUSINESS_DETAIL | 1 |
| PENDING_TECHNICAL_DETAIL | 0 |
| PENDING_PLACEMENT_OR_CONTEXT | 10 |
| RECHECK_ONLY | 4 |
| SEMANTIC_MAPPING_ONLY | 19 |
| NO_SITE_CHANGE | 9 |
| HOLD | 1 |
| **Всего** | **47** |

Action-specific workload: 3 READY проверены по 12 обязательным полям и получили 3 acceptance rows; 1 пакет требует бизнес-факта; 4 контентных и 6 link packages требуют ровно одного места/контекста; 4 требуют page-pair recheck; 19 — аналитическая карта без физического изменения; 9 — доказанный no-change; 1 остаётся HOLD. Measurement interface содержит 6 Yandex-only/physical classes без обещания uplift.

## Materialization volume

- XLSX: 13 листов, 565 964 bytes, SHA-256 `acfa7f8337de43fe1499dc002aa2b1c42aee1057e1c2399b609faaf6844a6b69`.
- Основные XLSX row views: 2 840 universe; 2 185 core; 54 groups; 2 185 mapping; 80 relevant current pages; 160 target units; 35 deltas; 47 packages; 44 clarification/no-change/HOLD; 14 relations; 3 READY acceptance; 6 measurement classes.
- 13/13 sheets rendered and visually inspected; formula errors before/after re-import = 0.
- Narrative candidate views: README + analytical findings + action-first implementation plan.

## Реально выполненные операции

1. Доказательство native 2 840-source и exact-set join с MK01 product state.
2. Step5A semantic и downstream causal contamination audit.
3. Статусная reconciliation 2 840 строк и кластерный join.
4. Полная active-key projection в phrase→page map.
5. Пересборка 160 units и 105 owner-candidate comparisons.
6. Structural action evidence normalization.
7. Competing-page claims downgrade до public-evidence boundary.
8. Current topology reconciliation 2 683 nodes.
9. Target/current page and relation delta construction.
10. Work-package materialization и state classification.
11. READY completeness/placement/duplication review.
12. Client narrative materialization.
13. 13-sheet XLSX generation/recalculation/import/render QA.
14. Independent 21-check validator.
15. Owner failure classes A–U regression.
16. Recipient review и remote persistence/readback.

## Automation и ручной review

Можно автоматизировать exact-key joins, hashes/counts, set reconciliation, blank-state invariants, Step5A denylist, duplicate pairs, enum/state counts, READY field presence, placeholder/internal-token scans, XLSX cross-view counts и formula/readability smoke tests.

Аналитического review требуют task/intent boundaries, 160 unit roles, 105 owner comparisons, 21 competing-page cases, 21 newly material current pages, distinction structural-vs-content gap, 3 READY exact specifications, 10 placement/business boundaries и визуальная проверка 13 листов. Главные bottlenecks: доказательство current page meaning; точное место изменения; отделение normal parent/support relations от harmful competition; honest downgrade вместо угадывания.

## Provider profile

Фактические provider calls в rehearsal: **0**.

В реальном новом заказе обычно нужны bounded Wordstat collection, ordinary Yandex Search только для named ambiguity, независимый public-site discovery/current reads; Webmaster/Metrika/Direct — опционально при наличии доступа и необходимости усилить исторический/impact claim. Google и AI/Neuro/Alice не входят в MK02 base.

## Параметры будущего коммерческого лимита

Phase 8 должен учитывать: число source phrases/occurrences, ambiguous-review share, число task units/clusters, число текущих URL и current-minus discoveries, owner-candidate comparisons, Search ambiguity cases, competing-page cases, internal relations, число READY/pending work packages, требуемую глубину page reads, наличие/отсутствие private history и число форматов клиентской упаковки. Финальную цену по одной репетиции назначать нельзя.
