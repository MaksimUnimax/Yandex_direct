# KW-002 «Кровь и Песок» — STEP 02 QA

Дата: 2026-09-08

Статус до remote readback: **LOCAL QA PASS / REMOTE READBACK PENDING**

## 1. Проверяемый результат

- `STEP_02_SEED_MAP.csv`
- `STEP_02_COVERAGE_MATRIX.csv`
- `STEP_02_DEFERRED_OR_TARGETED_PROBES.csv`
- `STEP_02_REPORT.md`

## 2. Количественный QA

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
```

## 3. Seed-class accounting

```text
CLIENT_HEAD_CLASS = 3
EXPLICIT_USE_OR_FORM = 2
ANALYST_COMPOSED_USE_DIAGNOSTIC = 3
EXACT_NAMED_PRODUCT_OR_SYMBOL = 38
ZODIAC_FAMILY = 1
ZODIAC_SIGN_SCOPED = 12
EXPLICIT_ALIAS_OR_ALTERNATE_WRITING = 10
VARIANT_MARKER_DIAGNOSTIC = 26
BRAND = 2
TOTAL = 97
```

Priority reconciliation:

```text
PRIMARY = 67
DEFERRED_TARGETED = 30
TOTAL = 97
```

## 4. Adversarial method checks

```text
ALL_SEEDS_HAVE_SOURCE_LINEAGE = true
ALL_SEEDS_HAVE_EXPLICIT_PURPOSE = true
ALL_SEEDS_STATUS_DISCOVERY_PROBE = true
CLIENT_TERMS_RELABELLED_AS_PROVEN_DEMAND = 0
ANALYST_COMPOSED_SEEDS_UNLABELLED = 0
STEP01_NAC_BUCKETS_USED_AS_SEO_TAXONOMY = 0
UNSUPPORTED_PRODUCT_FACTS_USED = 0
MATERIAL_CLIENT_CARDS_WITHOUT_PRIMARY_PROBE_ROUTE = 0
REDUNDANT_NORMALIZED_SEEDS = 0
STANDALONE_INTERNAL_VARIANT_MARKER_PRIMARY_SEEDS = 0
```

## 5. Provider / contamination checks

```text
WORDSTAT_CALLS = 0
SEARCH_CALLS = 0
AI_SEARCH_CALLS = 0
WB_ROWS_USED = 0
OLD_RESEARCH_CONTAMINATION = 0
```

## 6. Coverage checks

`STEP_02_COVERAGE_MATRIX.csv` содержит 76 строк.

```text
EXPECTED_OZON_CARDS = 76
COVERAGE_ROWS = 76
CARDS_WITH_PRIMARY_PROBE_ROUTE = 76
CARDS_WITHOUT_PRIMARY_PROBE_ROUTE = 0
```

Variant-marker probes не заменяют basic routes: variant-карточки уже имеют основной route через конкретное название/знак, а variant probe записан как deferred.

## 7. Claim-boundary checks

В Step 02 не создано:

```text
KEEP/REJECT keyword verdicts
final frequency values
search intent
SEO clusters
query→page ownership
site IA
SEO priority
competitor conclusions
AI-search conclusions
```

Наличие probe означает только, что эту формулировку целесообразно использовать как измерительный вход или сохранить как отложенный diagnostic.

## 8. PASS gate

До удалённого readback:

```text
LOCAL_QA = PASS
REMOTE_GITHUB_READBACK = PENDING
STEP_02_COMPLETE = PENDING_REMOTE_READBACK
NEXT_STEP_ALLOWED = false
```

После записи всех пяти файлов и remote readback должны быть подтверждены:

```text
REMOTE_SEED_ROWS = 97
REMOTE_COVERAGE_ROWS = 76
REMOTE_DEFERRED_ROWS = 30
REMOTE_GITHUB_READBACK = PASS
```

Только тогда:

```text
STEP_02 = COMPLETE / PASS
NEXT_STEP_ALLOWED = true
NEXT_STEP = STEP_03_PRIMARY_WORDSTAT_ACQUISITION
```
