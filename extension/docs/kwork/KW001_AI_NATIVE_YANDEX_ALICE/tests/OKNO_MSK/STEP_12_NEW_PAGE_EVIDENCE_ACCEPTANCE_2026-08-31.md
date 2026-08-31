# Step 12 — new-page evidence acceptance after V5

Date: 2026-08-31  
Scope: re-accept D12-02 after the residual direct-Search correction and accept D12-03 + D12-10.  
This document does **not** yet decide final confidence, hierarchy, Step-13 pairs or final Step-12 PASS.

## Why this correction exists

The first Step-12 run treated phrase count plus a plausible page gap as strong evidence for new pages. The external audit showed that vocabulary size is not demand and that a standalone page boundary may require direct Search evidence. A later evidence matrix then exposed one residual mixed phrase (`оконная фурнитура отзывы`) still contaminating the hardware-guide core, so D12-02 was reopened rather than hidden.

The accepted correction now uses:

```text
V5 explicit structural units
+ direct persisted Wordstat result counts only
+ exact Step-9 direct Search probes only
+ business truth/current-page alternatives
+ explicit evidence gaps
```

It does **not** sum overlapping Wordstat phrase counts as total unique demand and does not transfer one probed query's Search result type to unprobed neighbours.

## Accepted evidence artifacts

```text
STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V5.tsv
STEP_12_STRUCTURAL_UNITS_V5.tsv
STEP_12_STRUCTURAL_UNIT_CORRECTIONS_V5.tsv
STEP_12_STRUCTURAL_UNIT_CORRECTION_QA_V5.json
STEP_12_NEW_PAGE_EVIDENCE_V2.tsv
STEP_12_NEW_PAGE_DEMAND_PHRASE_EVIDENCE_V2.tsv
STEP_12_NEW_PAGE_EVIDENCE_QA_V2.json
STEP_12_EXISTING_DEMAND_SEARCH_EVIDENCE_INVENTORY.md
STEP_12_EXISTING_EVIDENCE_SCHEMA_PROFILE.md
```

## Evidence semantics

### Wordstat

Persisted normalized acquisition rows expose `section`, `phrase`, `count` and provenance. Only `section=result` / Step-08 `result_occurrences` are used as direct demand evidence. `association` rows remain related-query vocabulary evidence and are not counted as direct demand for a page.

Phrase counts are **not summed** into a claimed total market demand because the queries overlap. The matrix reports coverage, direct-result phrase counts, maximum/median observed direct counts and top direct phrases instead.

### Ordinary Search

Step 9 contains 75 directly probed queries. Evidence is used only when an exact corrected candidate-core phrase was actually probed. If no corrected core phrase was probed, the matrix says `NO_DIRECT_STEP09_CORE_QUERY`; it does not infer a page type from nearby queries.

## D12-02 reopened residual — hardware reviews

The first V4 evidence matrix showed:

```text
оконная фурнитура отзывы
-> Step09 observed job = WINDOW_HARDWARE_REVIEWS
-> dominant result type = REVIEWS_FORUM_INFORMATION
-> handoff = INFORMATIONAL_NON_LANDING
```

This contradicted V4, where that phrase still sat inside `WINDOW_HARDWARE_SELECTION_GUIDE`.

V5 correction:

```text
оконная фурнитура отзывы
-> WINDOW_HARDWARE_GENERIC_REVIEWS_INFO
-> NO_STANDALONE_FIRST_PARTY / UNSERVABLE_NEUTRAL_REVIEW
```

The general hardware-guide core falls from 31 to 30 phrases. Its only directly probed Step-9 phrase disappears from the core, so the corrected guide now honestly has **0 direct Step-9 core probes**.

Verdict: **D12-02 VERIFIED_FIXED AGAIN after evidence-triggered reopen + V5 readback.**

## Candidate-by-candidate evidence review

### 1. Panoramic windows commercial page

Corrected core:
`PANORAMIC_WINDOWS_COMMERCIAL_CORE = 45 phrases`

Direct Wordstat evidence:

```text
45/45 core phrases have direct result counts
панорамные окна = 9273
панорамные окна москва = 510
панорамные окна купить = 498
панорамные окна цена = 479
median observed direct count = 73
```

Supporting informational/outdoor units are recorded separately and do not inflate the 45-phrase commercial core.

Direct Step-9 core Search probes:
`0`

Verdict:

```text
DEMAND = STRONG_DIRECT_WORDSTAT_SUPPORT
STANDALONE_COMMERCIAL_SEARCH_BOUNDARY = NOT DIRECTLY PROBED
MATURITY = PROVISIONAL_PENDING_SEARCH_BOUNDARY
```

The page remains a strong candidate, not a final/high-confidence instruction.

### 2. Window hardware guide

Corrected core:
`WINDOW_HARDWARE_SELECTION_GUIDE = 30 phrases`

Direct Wordstat evidence:

```text
30/30 core phrases have direct result counts
largest corrected core counts:
- лучшая оконная фурнитура = 52
- рейтинг оконной фурнитуры = 34
- производители оконной фурнитуры = 32
- какая оконная фурнитура лучше = 19
- типы оконной фурнитуры = 17
median observed direct count = 5
```

Important: the broad acquisition seed `оконная фурнитура = 1459` is **not** treated as the guide's direct standalone demand because that broad root includes shopping/aftermarket tasks that V5 separated from the guide.

Direct Step-9 core Search probes after V5:
`0`

Verdict:

```text
DEMAND = PARTIAL_DIRECT_WORDSTAT_SUPPORT
SEARCH PAGE BOUNDARY = NOT DIRECTLY PROBED
MATURITY = PROVISIONAL_PENDING_SEARCH_BOUNDARY
```

This is the weakest of the five historical new-page candidates. It remains a candidate for later action/confidence review, not an accepted high-confidence page.

### 3. PVC-window DIY installation guide

Corrected core:
`PVC_WINDOW_INSTALLATION_DIY = 26 phrases`

Direct Wordstat evidence:

```text
26/26 direct-result evidence
как установить пластиковое окно = 1868
как снять пластиковое окно = 1677
установка пластиковых окон своими руками = 681
пошаговая установка пластиковых окон = 132
median observed direct count = 117
```

Direct Step-9 core probes:

```text
пошаговая установка пластиковых окон
-> DIY_WINDOW_INSTALLATION / INFORMATION_GUIDE / PROCEDURAL_INFORMATION_JOB

установка пластиковых окон пошагово
-> DIY_WINDOW_INSTALLATION / INFORMATION_GUIDE / PROCEDURAL_INFORMATION_JOB
```

Verdict:

```text
DEMAND = STRONG_DIRECT_WORDSTAT_SUPPORT
DIRECT SEARCH PAGE TYPE = INFORMATION_GUIDE
MATURITY = EVIDENCE_SUPPORTED_PENDING_ACTION_REEVALUATION
```

This is the strongest informational new-page candidate from existing evidence.

### 4. PVC-window DIY repair/adjustment guide

Corrected core:
`PVC_WINDOW_REPAIR_DIY_GENERAL + PVC_WINDOW_ADJUSTMENT_DIY = 17 phrases`

Direct Wordstat evidence:

```text
17/17 direct-result evidence
как отрегулировать пластиковое окно = 1211
ремонт пластиковых окон своими руками = 99
ремонт пластиковых окон видео = 29
median observed direct count = 7
```

Direct Step-9 core Search probes:
`0`

Verdict:

```text
DEMAND = STRONG_DIRECT_WORDSTAT_SUPPORT
SEARCH BOUNDARY / ONE GUIDE VS MORE THAN ONE = NOT DIRECTLY PROBED
MATURITY = PROVISIONAL_PENDING_SEARCH_BOUNDARY
```

The demand is real; whether repair + adjustment should remain one guide is not yet final.

### 5. Window replacement service

Corrected core:
`WINDOW_REPLACEMENT_SERVICE = 13 phrases`

Direct Wordstat evidence:

```text
13/13 direct-result evidence
замена пластиковых окон = 2664
замена окна на пластиковые цена = 205
замена алюминиевых окон = 154
поменять окна на пластиковые цена = 128
median observed direct count = 36
```

Direct Step-9 core Search probes:
`0`

Business truth:
- replacement workflow is present inside current installation work;
- a standalone replacement-service role is not yet directly proven.

Verdict:

```text
DEMAND = STRONG_DIRECT_WORDSTAT_SUPPORT
STANDALONE SERVICE PAGE BOUNDARY = NOT DIRECTLY PROBED
MATURITY = PROVISIONAL_PENDING_SEARCH_BOUNDARY
```

The page remains a strong commercial candidate, but not a final high-confidence instruction.

## What this fixes — and what it does not

### D12-03 — NEW_PAGE_EVIDENCE_NOT_MATERIALIZED

**VERIFIED_FIXED.**

Why:
- every surviving historical new-page candidate now has an explicit evidence row;
- evidence separates core vs supporting units;
- direct Wordstat demand, direct Search coverage/gap, business truth and current-page alternative are materialized;
- missing Search evidence is preserved as a named gap rather than invented away;
- no new provider requests were made merely to complete bookkeeping.

This defect is about **evidence materialization**, not automatically approving every candidate.

### D12-10 — PHRASE_COUNT_USED_AS_DEMAND_PROXY

**VERIFIED_FIXED.**

Why:
- candidate phrase count is retained only as coverage;
- demand claims use direct persisted Wordstat result counts;
- association-only evidence is excluded from direct-demand verdicts;
- overlapping phrase counts are not summed as total unique demand;
- the broad hardware seed 1459 is deliberately not misrepresented as guide demand after semantic separation.

### D12-02 — MIXED_UNITS_SURVIVED_FULL_AUDIT

**VERIFIED_FIXED AGAIN after reopen.**

Why:
- direct Search evidence exposed the residual reviews phrase;
- it was removed from the guide core in V5;
- V5 has 2332 rows, 19 upstream unresolved, 160 explicit units and zero metadata inconsistency;
- the V2 evidence matrix now shows zero direct Search core queries for the corrected guide rather than hiding the contradictory reviews result.

## What remains open

```text
D12-04 DEFAULT_HIGH_CONFIDENCE
D12-05 QA_SELF_CERTIFICATION_AND_SPLIT_MERGE_BUG
D12-06 STEP13_HANDOFF_MANUAL_NOT_DERIVED
D12-07 NEW_PAGE_HIERARCHY_INCOMPLETE
D12-11 PROVISIONAL_DEPENDENCIES_HIDDEN_BY_FINAL_ACTION
```

## Next correction

Next: D12-04. Confidence will be derived from explicit evidence dimensions rather than a default. The new-page evidence above will feed that derivation; candidates with missing material Search boundaries cannot become final HIGH.

## Plain-language summary

**Why we did this:** to stop treating “many different phrases” as proof that a new page deserves to exist.

**What we actually did:** for each of the five page ideas we attached real saved Wordstat demand, separated the phrases that truly belong to that page from supporting topics, and checked whether that exact topic had already been tested in ordinary Yandex Search.

**What we got:** one very strong informational candidate (DIY installation), several strong-demand but still provisional candidates, and one much weaker hardware-guide candidate. Missing evidence is now visible instead of being hidden behind `HIGH` confidence.
