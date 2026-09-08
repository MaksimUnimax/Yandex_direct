# KW-002 Blood & Sand — STEP 02 V1 QUALITY SCORE

Date: 2026-09-08

Evaluated version: original 97-probe Step-02 result before external-method rework.

Owner scoring clarification applied retroactively:

```text
EACH CRITERION = 0–10
NOT 0–1
```

Verdict:

```text
QUALITY_TOTAL = 65 / 100
QUALITY_SCORE = 6.5 / 10
STATUS = REWORK_REQUIRED
STEP_03_ALLOWED = false
```

## Dimension score

| Критерий | Балл из 10 | Причина |
|---|---:|---|
| Цель и полнота результата | **10/10** | Seed map, coverage, deferred list, report and QA existed. |
| Методика и источники | **7/10** | Core `seed = discovery probe` был поддержан, но quality-specific refinement rules отсутствовали. |
| Evidence / provenance integrity | **10/10** | Client/Ozon lineage и analyst-composed labels были сохранены. |
| Coverage / полнота | **6/10** | 76/76 catalog rows имели routes, но quality coverage была смешана с catalog accounting coverage. |
| Аналитическая корректность / claim boundaries | **8/10** | Не было преждевременных SEO-решений, но noisy bare names были слишком легко продвинуты в PRIMARY. |
| Качество adversarial QA | **4/10** | QA хорошо проверял counts/lineage, но недостаточно атаковал search usefulness/noise. |
| Persistence / readback / reproducibility | **10/10** | Remote GitHub readback прошёл. |
| Понятность владельцу/клиенту | **7/10** | Отчёт был понятен, но ошибочно создавал впечатление готовности через PASS. |
| Information gain / cost / efficiency | **2/10** | Многие exact-name rationales были шаблонными; экономия provider calls могла слишком сильно влиять на deferral. |
| Готовность следующего шага | **1/10** | Step 03 был открыт до появления search-probe-quality QA и refinement/synonym controls. |
| **СУММА** | **65/100** | 10 критериев × максимум 10 баллов. |
| **ИТОГОВАЯ ОЦЕНКА** | **6.5/10** | `65 / 10 = 6.5`. Material defects / rework required. |

## Что сняло баллы

```text
- bare ambiguous names считались достаточными quality routes;
- HIGH-noise names не имели обязательной refinement strategy;
- automobile synonym/use-context coverage не была системной;
- exact seller names слишком автоматически становились PRIMARY;
- expected information gain был повторяющимся и слабо различал now/later/control;
- Step 03 был открыт до отдельного search-probe-quality QA.
```

## Что подняло бы оценку

```text
- separate catalog-lineage coverage from search-quality coverage;
- add refinement/qualification routes for ambiguous names;
- add bounded machine/automobile/auto wording coverage;
- rebalance exact names versus qualified/broad probes;
- rewrite information-gain rationale;
- materialize a deterministic corrected primary acquisition manifest;
- rerun adversarial QA and remote readback.
```

## ПРОСТЫМИ СЛОВАМИ

**Оценка V1:** 65/100, то есть **6.5/10**.

Файлы и учёт были сделаны хорошо, но сам список запросов был недостаточно качественно подготовлен к Wordstat: слишком много неоднозначных названий считались хорошими основными входами. Поэтому V1 правильно остаётся `REWORK_REQUIRED / SUPERSEDED`.
