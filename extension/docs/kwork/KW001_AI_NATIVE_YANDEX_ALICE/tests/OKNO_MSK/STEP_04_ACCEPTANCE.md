# KW-001 / OKNO-MSK — STEP 04 ACCEPTANCE

Date: 2026-08-28  
Status: **PASS AFTER RETROSPECTIVE CORRECTION / FAMILY-LEVEL TRIAGE FROZEN**

## 1. Authority and supersession

This acceptance was re-opened after a source-backed methodology audit.

Authoritative Step-04 documents are now:

```text
STEP_04_PROGRESSIVE_CLEANUP_1.md          # historical/original analysis
STEP_04_METHOD_REVIEW_CORRECTION.md       # authoritative correction where wording conflicts
STEP_REVIEW_AND_ERRORS_LEDGER.md           # case-specific error memory
STEP_04_ACCEPTANCE.md                      # current re-frozen gate
```

The original phrase `ANALYTICAL CLEANUP COMPLETE` is superseded. Step 04 was a **family-level triage and cleanup-rule freeze**, not a complete row-by-row semantic cleanup.

---

## 2. Correct Step-04 scope

Step 04 closed:

```text
18 pass-1 seed families reviewed
recurring relevant/noise patterns identified
ambiguous business/intents preserved for review
exclusion taxonomy corrected
second-pass expansion probe pool prepared
```

Step 04 did **not** close:

```text
full row-level classification of every raw Wordstat phrase
final semantic-core cleanup
clustering
SERP validation
page mapping
cannibalization decisions
final priority decisions
```

Therefore:

```text
FAMILY_LEVEL_TRIAGE = COMPLETE
FULL_ROW_LEVEL_CLEANUP = NOT YET COMPLETE
```

---

## 3. Corrected triage contract

The original `KEEP / REJECT_OBVIOUS / REVIEW` heuristic is no longer sufficient as the canonical classification because it mixed true irrelevance with valid demand excluded only by scope.

Canonical states going forward:

```text
KEEP
REVIEW
EXCLUDE_IRRELEVANT
EXCLUDE_SCOPE
EXCLUDE_MECHANICAL
```

Meaning:

- `KEEP` — relevant and retained for later stages; no separate page is implied.
- `REVIEW` — potentially relevant but business/intent/page ownership remains unresolved.
- `EXCLUDE_IRRELEVANT` — wrong semantic meaning/task/product or otherwise genuinely unsuitable for the order.
- `EXCLUDE_SCOPE` — valid demand excluded only by frozen geography/product/audience/client scope; recoverable after scope revision.
- `EXCLUDE_MECHANICAL` — exact/mechanical duplicate or processing-only exclusion.

Business-priority unknowns such as standalone installation, repair, accessories and finance remain `REVIEW` until client/business or later evidence resolves them.

---

## 4. Corrected frequency discipline

Old wording `low frequency is never a rejection reason` was too absolute.

Canonical rule:

```text
LOW_FREQUENCY_ALONE != PROOF_OF_IRRELEVANCE
```

A low count alone cannot prove that a query is semantically irrelevant. However frequency/traffic potential may later contribute to prioritization or page-target decisions together with:

```text
relevance
business value
cluster/topic size
regional SERP intent/page overlap
commercial capacity/priority
```

Low-volume measured families remain available for later SERP/page-boundary judgment without implying that every low-volume phrase must survive to the final client core.

---

## 5. Wordstat association discipline

Official Yandex GetTop semantics distinguish returned query results from `associations`, which are queries similar to the requested phrase.

Official sources:
- https://aistudio.yandex.ru/docs/ru/search-api/api-ref/Wordstat/getTop
- https://aistudio.yandex.ru/docs/ru/search-api/operations/wordstat-gettop.html

Therefore the accepted rule is:

```text
ASSOCIATION = vocabulary / expansion evidence
ASSOCIATION != automatically accepted keyword
ASSOCIATION COUNT != business relevance proof
ASSOCIATION COUNT != separate-page proof
```

This preserves useful new wording without letting provider similarity suggestions silently become client semantics.

---

## 6. Corrected expansion handoff

Replace the earlier `strong candidate` wording with information-gain probe states.

### EXPANSION_PROBE_READY — subject to Step-5 preflight

```text
оконная фурнитура
панорамные окна
остекление террасы
балкон с выносом
панорамное остекление балкона
окна для частного дома
```

### EXPANSION_PROBE_AMBIGUOUS

```text
монтаж окон
```

Reason: broader than `установка пластиковых окон`; high association count alone does not establish a clean target family.

### EXPANSION_PROBE_REVIEW

```text
регулировка окон пвх
москитные сетки на пластиковые окна
окна пвх
стеклопакет
оконный завод
```

These remain candidates/probes only. **No Step-5 manifest is frozen by this Step-04 acceptance.**

---

## 7. External method review incorporated

The retrospective review checked current sources rather than relying on the project runbook as self-proof.

Official provider semantics:
- Yandex Wordstat GetTop API documentation above.

External methodology corroboration:
- https://www.semrush.com/blog/keyword-clustering/
- https://ahrefs.com/blog/keyword-mapping/
- https://ahrefs.com/blog/keyword-intent/

These support separating collection from later intent/topic/page grouping and considering business/search intent rather than treating raw volume as a page decision. They do **not** make our exact internal status names an industry standard; the labels remain project-specific analyst mechanics.

---

## 8. Row-level provenance requirement added

Before final semantic-core freeze, retained/excluded raw phrases used in the workflow must be traceable with at least:

```text
phrase
source seed/request provenance
provider count/observation
scope region/device where relevant
decision state
reason code
family/cluster candidate
review note when unresolved
```

Step 04 has **not** yet satisfied this final row-level cleanup requirement.

---

## 9. Step-04 request truth

```text
WORDSTAT provider requests = 0
SEARCH provider requests = 0
GENSEARCH provider requests = 0
new paid provider cost = 0 RUB
```

No Step-5 provider batch was created during the retrospective correction.

---

## 10. Corrected gate

```text
all 18 pass-1 seed families reviewed = PASS
family-level triage = PASS
full row-level cleanup = NOT COMPLETE
scope exclusion separated from irrelevance = PASS
ambiguous/business-unknown demand preserved = PASS
low-frequency-alone treated as irrelevance proof = FALSE
association automatically treated as accepted keyword = FALSE
review queue preserved = PASS
pass-2 probe pool reclassified by information-gain confidence = PASS
new provider acquisition = NONE
final semantic core frozen = FALSE
clustering performed = FALSE
page mapping performed = FALSE
SERP validation performed = FALSE
```

## 11. Acceptance verdict

```text
STEP_04_RESULT = PASS_AFTER_CORRECTION
STEP_04_FAMILY_LEVEL_TRIAGE_COMPLETE = true
STEP_04_FULL_ROW_LEVEL_CLEANUP_COMPLETE = false
STEP_04_METHOD_CORRECTION_APPLIED = true
STEP_04_PASS2_PROBE_POOL_READY_FOR_PREFLIGHT = true
STEP_04_PASS2_MANIFEST_FROZEN = false
STEP_04_FINAL_SEMANTIC_CORE = false
STEP_04_NEXT_STEP_AUTHORIZED_AUTOMATICALLY = false
```

Final markers:

```text
KW001_OKNO_MSK_STEP_04_PASS_AFTER_CORRECTION = true
KW001_OKNO_MSK_STEP_04_FAMILY_TRIAGE_COMPLETE = true
KW001_OKNO_MSK_STEP_04_FULL_ROW_CLEANUP_COMPLETE = false
KW001_OKNO_MSK_STEP_04_METHOD_REVIEW_CORRECTION_APPLIED = true
```

Owner stop gate still applies. Step 5 requires a fresh source-backed pre-step review and explicit owner authorization before any Wordstat batch is created.
