# KW-001 / OKNO-MSK — STEP 04 METHOD REVIEW CORRECTION

Date: 2026-08-28  
Status: **AUTHORITATIVE CORRECTION / SUPERSEDES CONFLICTING STEP-04 WORDING**

This document records the source-backed retrospective audit of Step 04 and corrects claims that were too broad or insufficiently precise.

If this file conflicts with `STEP_04_PROGRESSIVE_CLEANUP_1.md`, this correction controls.

---

## 1. What Step 04 actually accomplished

Step 04 performed:

```text
18 seed-family review
+ recurring pattern triage
+ obvious-noise taxonomy
+ ambiguity/review queue
+ pass-2 probe candidate generation
```

It did **not** perform a complete row-by-row classification of every raw Wordstat result.

Therefore the correct description is:

```text
FAMILY-LEVEL TRIAGE COMPLETE
CLEANUP RULES FROZEN
FULL ROW-LEVEL SEMANTIC CLEANUP = NOT COMPLETE
```

The previous phrase `ANALYTICAL CLEANUP COMPLETE` was too strong and must not be reused as authority.

---

## 2. Corrected triage states

The original three-state model:

```text
KEEP
REJECT_OBVIOUS
REVIEW
```

was a useful analyst heuristic but merged materially different exclusion reasons.

Going forward use at least:

```text
KEEP
= relevant and retained for later semantic stages

REVIEW
= potentially relevant but business/intent/page ownership remains unresolved

EXCLUDE_IRRELEVANT
= wrong semantic meaning, unrelated product/task, employment intent where not target, marketplace/used intent incompatible with scope, or other true relevance failure

EXCLUDE_SCOPE
= semantically valid demand excluded only because it is outside the frozen region/product/audience/client scope

EXCLUDE_MECHANICAL
= exact/mechanical duplicate or equivalent processing-only exclusion
```

`EXCLUDE_SCOPE` must remain recoverable if the client later revises scope.

---

## 3. Corrected frequency rule

Previous wording was too absolute:

```text
low frequency is never a rejection reason
```

Correct rule:

```text
LOW_FREQUENCY_ALONE != PROOF_OF_IRRELEVANCE
```

Meaning:

- At early cleanup, a low count alone does not prove a phrase is irrelevant.
- A low-volume phrase may still be a useful supporting long-tail, diagnostic probe or member of a larger cluster.
- Later prioritization/page-target decisions may legitimately consider frequency/traffic potential together with relevance, business value, cluster size and regional SERP evidence.

Frequency is therefore a signal, not a universal binary keep/delete rule.

---

## 4. Corrected handling of Wordstat associations

Official Yandex Wordstat GetTop semantics state that the method returns popular queries containing the specified keyword and queries similar to the specified one; `associations` are similar queries.

Official sources:
- https://aistudio.yandex.ru/docs/ru/search-api/api-ref/Wordstat/getTop
- https://aistudio.yandex.ru/docs/ru/search-api/operations/wordstat-gettop.html

Therefore:

```text
ASSOCIATION = vocabulary / expansion evidence
ASSOCIATION != automatically accepted keyword
ASSOCIATION COUNT != business relevance proof
ASSOCIATION COUNT != separate-page proof
```

A broad association may be valuable specifically because it tests an acquisition gap. That makes it a **probe**, not automatically a final semantic target.

---

## 5. Corrected expansion-candidate confidence

Replace vague `strong candidate` language with probe statuses:

```text
EXPANSION_PROBE_READY
= materially new vocabulary/job/subfamily; clear information gain; in-scope enough to justify provider measurement

EXPANSION_PROBE_AMBIGUOUS
= may add information but is broader/mixed and must be interpreted as a probe rather than a semantic target

EXPANSION_PROBE_REVIEW
= plausible but business scope, redundancy or evidence source is unresolved; do not execute automatically
```

Current Step-04 reclassification:

### EXPANSION_PROBE_READY candidates for Step-5 preflight review

```text
оконная фурнитура
панорамные окна
остекление террасы
балкон с выносом
панорамное остекление балкона
окна для частного дома
```

These are still **not authorized provider commands**. Step 5 must independently review redundancy, business scope and expected information gain before freezing its manifest.

### EXPANSION_PROBE_AMBIGUOUS

```text
монтаж окон
```

Reason: materially broader than `установка пластиковых окон`; can include other materials, service meanings and employment-adjacent vocabulary. High association count is not enough for `READY` status.

### EXPANSION_PROBE_REVIEW

```text
регулировка окон пвх
москитные сетки на пластиковые окна
окна пвх
стеклопакет
оконный завод
```

Reasons include unresolved business priority, synonym redundancy, standalone-product boundary or trust-modifier ambiguity.

---

## 6. Why `REVIEW` remains valid

The exact label is project-specific, not an official Yandex standard.

However the underlying logic is supported by external practice: search intent and business value should be considered before mapping keywords/topics to pages, and similar-intent queries may belong to one page rather than becoming separate targets.

Corroborating methodology:
- https://www.semrush.com/blog/keyword-clustering/
- https://ahrefs.com/blog/keyword-mapping/
- https://ahrefs.com/blog/keyword-intent/

Thus the valid conclusion is:

```text
ambiguous demand should survive long enough for business/SERP resolution
```

not:

```text
our exact KEEP/REVIEW labels are an industry standard
```

The labels are `ANALYST_HEURISTIC`; the evidence-preservation principle is externally supported.

---

## 7. Geography correction

Official Wordstat documentation describes `regions` as regions where the query was made.

Therefore an out-of-scope city name appearing inside a query returned for Moscow-region origin is not a provider error and should not be called semantic garbage automatically.

Correct handling:

```text
relevant phrase + wrong frozen client GEO -> EXCLUDE_SCOPE
unrelated place/name coincidence -> EXCLUDE_IRRELEVANT
```

This preserves semantic truth separately from current commercial scope.

---

## 8. What remains valid from original Step 04

The following original decisions survive the audit:

```text
RAW WORDSTAT != CLIENT SEMANTIC CORE
seed-family triage before clustering = valid
obvious unrelated noise can be excluded early
business-priority unknowns remain REVIEW
associations are vocabulary evidence, not accepted final keywords
no final page/cluster decision in Step 04
no new provider acquisition in Step 04
review queue survives into later stages
```

The Step-04 analysis is therefore **not discarded**. Its scope and labels are corrected.

---

## 9. Row-level provenance requirement added

Before final semantic-core freeze, every retained/excluded raw phrase used in the deliverable workflow must be traceable with at least:

```text
phrase
source seed/request or result provenance
count / provider observation
scope region/device where relevant
decision state
reason code
family/cluster candidate
review note when unresolved
```

Step 04 did not yet satisfy this final row-level requirement and must not claim to have done so.

---

## 10. Step-04 corrected verdict

```text
FAMILY_LEVEL_TRIAGE = PASS
CLEANUP_RULE_FREEZE = PASS AFTER CORRECTION
FULL_ROW_LEVEL_CLEANUP = NOT YET COMPLETE
FINAL_SEMANTIC_CORE = NOT FROZEN
CLUSTERING = NOT PERFORMED
PAGE_MAPPING = NOT PERFORMED
SERP_VALIDATION = NOT PERFORMED
PROVIDER_REQUESTS_IN_STEP_04 = 0
STEP_05_PROVIDER_EXECUTION = NOT STARTED
```

Method-review verdict after correction:

```text
STEP_04_RETRO_VERDICT = CORRECTED_AND_REFREEZABLE
```

The next Step-5 pre-step review may proceed only after `STEP_04_ACCEPTANCE.md` is updated to reference this correction.

Markers:

```text
KW001_OKNO_MSK_STEP04_FAMILY_TRIAGE_NOT_FULL_CLEANUP = true
KW001_OKNO_MSK_STEP04_EXCLUDE_SCOPE_SEPARATED = true
KW001_OKNO_MSK_STEP04_LOW_FREQ_RULE_CORRECTED = true
KW001_OKNO_MSK_STEP04_ASSOCIATION_PROBE_RULE_CORRECTED = true
KW001_OKNO_MSK_STEP04_METHOD_CORRECTION_ACTIVE = true
```
