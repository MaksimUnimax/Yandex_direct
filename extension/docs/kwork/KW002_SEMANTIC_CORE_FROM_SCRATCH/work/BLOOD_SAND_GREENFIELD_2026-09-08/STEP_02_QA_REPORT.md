# KW-002 «Кровь и Песок» — STEP 02 QA

Дата: 2026-09-08

Статус: **SUPERSEDED BY EXTERNAL METHOD AUDIT / REWORK_REQUIRED**

## 1. Исторический локальный/структурный QA

Первоначальный QA подтвердил корректность materialization и accounting:

```text
SEED_ROWS_TOTAL = 97
PRIMARY_SEEDS = 67
DEFERRED_TARGETED_SEEDS = 30
DUPLICATE_NORMALIZED_SEED_PHRASES = 0
SEEDS_WITHOUT_PURPOSE = 0
SEEDS_WITHOUT_SOURCE_LINEAGE = 0
SEEDS_NOT_DISCOVERY_PROBE = 0
COVERAGE_ROWS = 76
COVERAGE_ROWS_WITHOUT_PRIMARY_ROUTE = 0
WORDSTAT_CALLS = 0
SEARCH_CALLS = 0
AI_SEARCH_CALLS = 0
WB_ROWS_USED = 0
OLD_RESEARCH_CONTAMINATION = 0
REMOTE_GITHUB_READBACK = PASS
```

Этот QA остаётся исторически верным в части файлов, количества строк, lineage и запретов.

## 2. Почему прежний PASS больше не действует

После требования владельца выполнен отдельный внешний методический аудит по официальным материалам Яндекса и отраслевым статьям:

```text
STEP_02_EXTERNAL_METHOD_AUDIT_2026-09-08.md
```

Аудит установил, что первоначальный QA проверял:

```text
card has a primary route
```

но не проверял достаточно строго:

```text
primary route is search-discovery-quality
ambiguous bare seed has a qualified/refinement route
synonym/use-context coverage is sufficient
PRIMARY vs DEFERRED rationale is discriminating rather than boilerplate
```

Поэтому старое утверждение:

```text
STEP_02 = COMPLETE / PASS
```

отменено поздней проверкой.

## 3. Текущий финальный verdict

```text
STEP_02_STRUCTURAL_ACCOUNTING_QA = PASS
STEP_02_EXTERNAL_METHOD_QA = FAIL
STEP_02 = REWORK_REQUIRED
NEXT_STEP_ALLOWED = false
STEP_03 = BLOCKED
```

## 4. Обязательные исправления перед новым PASS

```text
SEARCH_PROBE_QUALITY_COVERAGE_REQUIRED = true
HIGH_NOISE_BARE_SEEDS_REQUIRE_REFINEMENT_ROUTE = true
SYSTEMATIC_BOUNDED_USE_SYNONYM_COVERAGE_REQUIRED = true
EXACT_NAME_PRIMARY_BIAS_MUST_BE_REVIEWED = true
INFORMATION_GAIN_RATIONALE_MUST_BE_DISCRIMINATING = true
PRIMARY_DEFERRED_REVIEW_MUST_IGNORE_TRIVIAL_DIRECT_API_COST = true
NEW_REMOTE_READBACK_REQUIRED = true
```

Новый Step-02 PASS может быть выставлен только после пересборки seed map/coverage/QA и удалённого readback.