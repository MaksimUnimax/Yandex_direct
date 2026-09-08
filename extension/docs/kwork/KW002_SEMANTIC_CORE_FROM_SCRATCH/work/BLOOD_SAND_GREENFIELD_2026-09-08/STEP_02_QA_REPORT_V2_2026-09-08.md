# KW-002 «Кровь и Песок» — STEP 02 V2 QA

Дата: 2026-09-08

Статус: **PASS / REMOTE READBACK PASS**

## 1. Проверяемые V2 артефакты

```text
STEP_02_V2_DECISION_OVERLAY.csv
STEP_02_V2_ADDITIONAL_PROBES.csv
STEP_02_PRIMARY_ACQUISITION_MANIFEST_V2.csv
STEP_02_DEFERRED_CONTROL_MANIFEST_V2.csv
STEP_02_SEARCH_PROBE_QUALITY_COVERAGE_V2.csv
STEP_02_V2_INFORMATION_GAIN_POLICY.csv
STEP_02_REWORK_REPORT_V2_2026-09-08.md
```

V1 артефакты сохранены как история и не являются текущим Step-03 execution authority.

## 2. Количественный QA

```text
V1_RETAINED_PRIMARY = 48
V1_BARE_PROBES_DEMOTED = 19
V2_QUALIFIED_REFINEMENT_PROBES = 19
V2_USE_SYNONYM_PROBES = 12
V2_NEW_PROBES_TOTAL = 31
V2_PRIMARY_MANIFEST_ROWS = 79
V2_DEFERRED_CONTROL_ROWS = 49
V2_DECISION_OVERLAY_ROWS = 24
V2_SEARCH_QUALITY_COVERAGE_ROWS = 26
```

Remote terminal-row checks:

```text
PRIMARY_MANIFEST_LAST_RUN_ORDER = 79
PRIMARY_MANIFEST_LAST_SEED = U012
DEFERRED_MANIFEST_LAST_ROW = S097
ADDITIONAL_PROBES_LAST_ROW = U012
DECISION_OVERLAY_LAST_ROW = S096
SEARCH_QUALITY_COVERAGE_LAST_ROW = QC026
```

Remote blob SHA:

```text
PRIMARY_MANIFEST_SHA = 9087d272444727bd03f342b4fae1c989ba55a307
DEFERRED_MANIFEST_SHA = 9e9b4d38dcf98bc233f26d651645d7721bfcf66e
ADDITIONAL_PROBES_SHA = ab14a5be575cea598cd3c3701c4ed6b2769a6bdc
DECISION_OVERLAY_SHA = 4688f393d8fb97dae9167c88f49f9882289d2124
SEARCH_QUALITY_COVERAGE_SHA = 4353d0e23f2b944bcf1427e59883654e31fe8716
INFORMATION_GAIN_POLICY_SHA = 4f090df99b93d4df61e9281c2541c0a7b67cb1c0
```

## 3. External-audit defect closure

### Defect 1 — catalog coverage was mistaken for search-quality coverage

```text
CLOSED = true
```

Now preserved separately:

```text
CATALOG_LINEAGE_COVERAGE = inherited 76/76
SEARCH_PROBE_QUALITY_COVERAGE = 26/26 material quality groups PASS
```

### Defect 2 — high-noise bare primary without refinement

```text
CLOSED = true
```

19 ambiguous/high-noise bare probes were demoted to control/deferred and replaced by 19 qualified primary routes.

Broad roots (`амулет`, `оберег`, `талисман`, `чётки`, `знак зодиака`) remain deliberate broad controls but have explicit scoped/qualified companion routes.

```text
HIGH_NOISE_PRIMARY_WITHOUT_REFINEMENT_OR_CONTROL_JUSTIFICATION = 0
```

### Defect 3 — unsystematic vehicle wording coverage

```text
CLOSED = true
```

Bounded synonym axis added:

```text
для машины
для автомобиля
для авто
```

across four frozen roots:

```text
талисман
амулет
оберег
чётки
```

Existing `в машину` routes are preserved.

```text
MATERIAL_USE_CONTEXT_WITHOUT_BOUNDED_SYNONYM_PLAN = 0
```

### Defect 4 — exact seller names were over-promoted by default

```text
CLOSED = true
```

19 ambiguous bare names were demoted. Distinct low-noise names remain primary only after explicit ambiguity/noise screening.

```text
SELLER_NAMES_PROMOTED_TO_PRIMARY_BY_DEFAULT = 0
```

### Defect 5 — boilerplate information-gain rationale

```text
CLOSED = true
```

Current priority is governed by explicit discriminating classes in `STEP_02_V2_INFORMATION_GAIN_POLICY.csv`:

```text
BROAD_VOCABULARY_DISCOVERY
CONFIRMED_USE_CONTEXT
USE_CONTEXT_COMBINATION
UNIQUE_DISCOVERY_BRANCH
ALTERNATE_WORDING_BRANCH
SCOPED_FAMILY_COVERAGE
NOISE_REFINEMENT
SYNONYM_USE_CONTEXT_COVERAGE
```

### Defect 6 — provider cost could over-influence deferral

```text
CLOSED = true
```

V2 primary/deferred decisions are based on information gain/noise/redundancy. Request cost is secondary and is not used as a standalone deferral reason.

## 4. Claim-boundary QA

```text
SEED_AS_FINAL_KEYWORD_CLAIMS = 0
SEO_CLUSTER_DECISIONS = 0
PAGE_OWNERSHIP_DECISIONS = 0
SITE_IA_DECISIONS = 0
SEARCH_DEMAND_CLAIMS = 0
FINAL_INTENT_DECISIONS = 0
ANALYST_COMPOSED_PROBES_UNLABELLED = 0
OLD_RESEARCH_CONTAMINATION = 0
WB_ROWS_USED = 0
WORDSTAT_CALLS_DURING_REWORK = 0
SEARCH_CALLS_DURING_REWORK = 0
AI_SEARCH_CALLS_DURING_REWORK = 0
```

Qualified OR probes are diagnostic only and do not prove the named product belongs to any one of the business classes.

## 5. Step-03 operator handoff boundary

19 qualified probes use Wordstat OR syntax around client business classes.

```text
OR_OPERATOR_DOCUMENTED_BY_YANDEX = true
BRIDGE_OR_OPERATOR_EXECUTION_VERIFIED = false
```

This is not a Step-02 blocker because the semantic acquisition intent is deterministic.

Step 03 must perform a capability/behavior check before mass execution.

Fallback if the Bridge/provider route does not accept the grouped OR probe:

```text
ONE Q-PROBE
→ split deterministically into 3 class-qualified probes:
   амулет + name
   оберег + name
   талисман + name
→ preserve parent Q seed lineage
→ do not silently drop the branch
```

## 6. QUALITY SCORE — EACH CRITERION IS SCORED 0–10

Governed by `LEVEL1/RESULT_QUALITY_SCORING_RULE.md`.

**This table uses the owner-corrected rule: every criterion has its own 0–10 scale. It is forbidden to treat ten criteria as ten 0–1 components.**

| Критерий | Балл из 10 | Основание |
|---|---:|---|
| Цель и полнота результата | **10/10** | Исправленные primary/deferred manifests и отдельное quality coverage материализованы полностью. |
| Методика и источники | **10/10** | V2 напрямую operationalizes выводы официального Яндекса и отраслевого внешнего аудита. |
| Входные данные и provenance | **10/10** | V1 lineage сохранена; каждый новый probe связан с клиентским фактом/V1 source. |
| Coverage / полнота покрытия | **10/10** | Catalog lineage сохранён, отдельная search-quality matrix проходит 26/26 material groups. |
| Аналитическая корректность и границы утверждений | **9/10** | Qualified diagnostics размечены корректно; остаётся небольшая эвристичность в low-vs-ambiguous screening до реального Wordstat. |
| Качество adversarial QA | **9/10** | Все шесть дефектов внешнего аудита ретестированы; фактическое provider-поведение относится уже к Step 03. |
| Persistence / readback / воспроизводимость | **10/10** | Все V2 manifests прочитаны обратно с remote, terminal rows и SHA проверены. |
| Понятность владельцу/клиенту | **9/10** | Rework-report объясняет исправления простым языком; внутренние manifests остаются техническими по необходимости. |
| Information gain / стоимость / эффективность | **9/10** | Priority теперь определяется классами информационного выигрыша, cost-only deferrals отсутствуют. |
| Готовность следующего шага | **7/10** | Primary manifest детерминирован, но реальное поведение grouped OR через Bridge ещё нужно проверить на Step 03. |
| **СУММА** | **93/100** | 10 критериев × максимум 10 баллов. |
| **ИТОГОВАЯ ОЦЕНКА** | **9.3/10** | `93 / 10 = 9.3`. PASS candidate. |

### За что сняты баллы

```text
Аналитическая корректность: -1
Причина: часть ambiguity/noise screening остаётся аналитической эвристикой до реального Wordstat evidence.
Блокирует PASS: нет.
Что даст 10/10: подтверждение/коррекция screening на реальном Step-03/04 evidence.

Adversarial QA: -1
Причина: actual provider execution ещё не происходил; QA пока проверяет подготовленный acquisition design.
Блокирует PASS: нет, потому что provider execution принадлежит следующему шагу.
Что даст 10/10: успешный Step-03 capability/provider check без обнаружения новой методической дыры.

Понятность: -1
Причина: часть внутренних manifests неизбежно техническая.
Блокирует PASS: нет.
Что даст 10/10: дополнительная recipient-friendly визуализация/выжимка, если она окажется реально нужна владельцу/клиенту.

Information gain / эффективность: -1
Причина: полезность отдельных probes до реального Wordstat всё ещё прогнозная.
Блокирует PASS: нет.
Что даст 10/10: подтверждение, что primary routes дают различимый полезный вклад без лишней дубликации.

Готовность следующего шага: -3
Причина: grouped OR syntax документирован Яндексом, но ещё не проверен через фактический Yandex Marketing Bridge route.
Блокирует PASS Step 02: нет, поскольку определён deterministic fallback.
Что даст 10/10: успешный capability check OR-route или подтверждённый deterministic split без потери lineage.
```

## 7. Final PASS gate

```text
CATALOG_LINEAGE_COVERAGE = PASS
SEARCH_PROBE_QUALITY_COVERAGE = PASS
HIGH_NOISE_PRIMARY_WITHOUT_GOVERNED_ROUTE = 0
USE_CONTEXT_SYNONYM_PLAN = PASS
INFO_GAIN_RATIONALE = PASS
PRIMARY_ACQUISITION_MANIFEST = MATERIALIZED / 79 ROWS
DEFERRED_CONTROL_MANIFEST = MATERIALIZED / 49 ROWS
STEP02_QUALITY_TOTAL = 93 / 100
STEP02_QUALITY_SCORE = 9.3 / 10
ALL_HARD_GATES = PASS
REMOTE_READBACK = PASS
```

Final verdict:

```text
STEP_02 = COMPLETE / PASS AFTER V2 REWORK
NEXT_STEP_ALLOWED = true
NEXT_STEP = STEP_03_PRIMARY_WORDSTAT_ACQUISITION
```

## ПРОСТЫМИ СЛОВАМИ — ОЦЕНКА

**Оценка результата:** 93/100, то есть **9.3/10**.

**Что сделано хорошо:** исправлены все шесть дефектов первой версии, новый Wordstat manifest детерминирован и проверен, шумные запросы управляются отдельно.

**За что сняты баллы:** мы ещё не видели реальные ответы Wordstat по этим probes и не проверили grouped OR через сам Bridge.

**Можно ли идти дальше:** да, Step 02 проходит PASS. На Step 03 сначала обязателен capability/provider check, а не массовый запуск вслепую.
