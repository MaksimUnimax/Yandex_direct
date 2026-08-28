# KW-001 / OKNO-MSK — STEP 04 JOB-SPECIFIC REVIEW CORRECTION

Date: 2026-08-28  
Status: **JOB-SPECIFIC CORRECTION / DISPOSABLE WITH OKNO-MSK WORKSPACE**

This file records what was corrected in Step 04 of the current OKNO-MSK job after the owner-requested source-backed retrospective review.

It does **not** define universal KW-001 rules. Permanent owner-approved methodology lives in the parent universal KW-001 layer.

If this file conflicts with the original `STEP_04_PROGRESSIVE_CLEANUP_1.md` about what happened in this job, this correction controls.

---

## 1. What Step 04 actually accomplished in this job

Step 04 performed:

```text
18 seed-family review
recurring pattern triage
obvious-noise taxonomy
ambiguity/review queue
pass-2 probe candidate generation
```

It did **not** perform a complete row-by-row classification of every raw Wordstat result.

Correct OKNO-MSK Step-04 status:

```text
FAMILY-LEVEL TRIAGE COMPLETE
FULL ROW-LEVEL SEMANTIC CLEANUP = NOT COMPLETE
```

The earlier job wording `ANALYTICAL CLEANUP COMPLETE` was too strong.

---

## 2. Classification correction applied to this job

The original OKNO-MSK Step-04 triage used:

```text
KEEP
REJECT_OBVIOUS
REVIEW
```

During retrospective review, `REJECT_OBVIOUS` was found to mix different reasons.

For all subsequent OKNO-MSK job files, the current owner-approved universal classification is applied as:

```text
KEEP
REVIEW
EXCLUDE_IRRELEVANT
EXCLUDE_SCOPE
EXCLUDE_MECHANICAL
```

This file records the application of that rule to this job; it does not create the rule.

---

## 3. Frequency correction applied to this job

The old Step-04 wording implied that low frequency could never participate in a later rejection/priority decision.

For this job, that wording is superseded.

Current OKNO-MSK handling:

```text
low frequency alone does not prove irrelevance;
later priority/page decisions may still consider demand magnitude together with business and SERP evidence.
```

No previously measured low-volume family is automatically removed by this correction.

---

## 4. Associations handling applied to this job

Official Yandex Wordstat semantics checked during the review:
- https://aistudio.yandex.ru/docs/ru/search-api/api-ref/Wordstat/getTop
- https://aistudio.yandex.ru/docs/ru/search-api/operations/wordstat-gettop.html

For OKNO-MSK, associations remain acquisition/vocabulary evidence only. They are not automatically accepted as final semantic phrases or separate page targets.

---

## 5. OKNO-MSK expansion-probe reclassification

### Current READY candidates for Step-5 preflight review

```text
оконная фурнитура
панорамные окна
остекление террасы
балкон с выносом
панорамное остекление балкона
окна для частного дома
```

These are still only job-specific candidates. No provider command is authorized by this file.

### Current AMBIGUOUS candidate

```text
монтаж окон
```

Job-specific reason: broader than the already measured `установка пластиковых окон` family and may add mixed meanings.

### Current REVIEW candidates

```text
регулировка окон пвх
москитные сетки на пластиковые окна
окна пвх
стеклопакет
оконный завод
```

These remain unresolved inside the OKNO-MSK job.

---

## 6. External sources consulted in this job review

Official provider documentation:
- https://aistudio.yandex.ru/docs/ru/search-api/api-ref/Wordstat/getTop
- https://aistudio.yandex.ru/docs/ru/search-api/operations/wordstat-gettop.html

External methodology corroboration used during the owner-requested audit:
- https://www.semrush.com/blog/keyword-clustering/
- https://ahrefs.com/blog/keyword-mapping/
- https://ahrefs.com/blog/keyword-intent/

These sources were used to audit this job's Step 04; this temporary file does not convert them into new universal rules.

---

## 7. What remains valid in this job

```text
raw Wordstat is not the final client semantic core
all 18 pass-1 families were reviewed
business-unknown directions remain unresolved
no final page/cluster decision was made
no provider request occurred in Step 04
Step 5 has not started
```

---

## 8. Remaining OKNO-MSK work after Step 04

Still not complete:

```text
full row-level cleanup
final semantic-core freeze
clustering
ordinary Yandex SERP validation
page mapping
final priorities
```

---

## 9. Job-specific verdict

```text
OKNO_MSK_STEP04_FAMILY_LEVEL_TRIAGE = PASS
OKNO_MSK_STEP04_FULL_ROW_LEVEL_CLEANUP = NOT_COMPLETE
OKNO_MSK_STEP04_RETRO_REVIEW = COMPLETE
OKNO_MSK_STEP05_PROVIDER_EXECUTION = NOT_STARTED
```

This file will be deleted together with the entire OKNO-MSK workspace after the job is fully closed.
