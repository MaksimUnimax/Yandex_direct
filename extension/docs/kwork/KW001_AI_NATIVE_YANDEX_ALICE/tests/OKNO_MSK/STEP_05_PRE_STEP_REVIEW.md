# KW-001 / OKNO-MSK — STEP 05 PRE-STEP REVIEW

Date: 2026-08-28  
Status: **PRE-STEP REVIEW COMPLETE / WAITING OWNER AUTHORIZATION / NO PROVIDER EXECUTION**

This file is job-specific and disposable with the OKNO-MSK workspace.

## 1. Proposed Step 05

Targeted Yandex Wordstat expansion pass #2.

Purpose:

```text
use a small number of new acquisition probes
only where pass #1 exposed materially new vocabulary or an under-sampled user-job family
and where another Wordstat getTop call is expected to add information rather than repeat pass #1
```

This step is not clustering, page mapping, final cleanup or SERP validation.

## 2. Input authority

Job-specific inputs:

```text
STEP_03_ACCEPTANCE.md
STEP_03 raw/checkpoint Wordstat evidence
STEP_04_METHOD_REVIEW_CORRECTION.md
STEP_04_ACCEPTANCE.md
JOB_FLOW.md
```

Universal owner-locked rules were read but not modified.

## 3. External method check

### OFFICIAL

Yandex Wordstat / AI Studio:

- https://aistudio.yandex.ru/ru/docs/search-api/api-ref/Wordstat/getTop
- https://yandex.ru/support2/wordstat/ru/interface/new
- https://yandex.ru/support2/wordstat/ru/content/operators

Relevant official semantics:

```text
GetTop returns last-30-day popular queries containing the specified keyword
and queries similar to the specified one.
results = returned query results
associations = similar queries
regions = regions a query was made from
```

This supports using a materially new seed to expose additional query vocabulary. It does not say that every association should become a new seed.

### INDUSTRY_PRACTICE corroboration

- https://ahrefs.com/blog/seed-keywords/
- https://www.semrush.com/blog/seed-keywords/

Both describe seed keywords as inputs used to unlock additional keyword ideas and subtopics. Additional seeds can improve coverage when they represent vocabulary the original seed did not expose well.

No external source was found that prescribes a universal numeric rule for how many second-pass seeds to run. The bounded manifest below is therefore project-specific.

## 4. Method-origin labels

```text
Use additional seeds to discover additional vocabulary = INDUSTRY_PRACTICE
GetTop result/association semantics = OFFICIAL
Do not automatically promote associations to accepted keywords = OFFICIAL + ANALYST_REASONING
Run a second pass only for expected information gain = ANALYST_HEURISTIC, source-corroborated
Exact count of second-pass probes = ANALYST_HEURISTIC / project cost control
Region 213 + DEVICE_ALL = frozen job scope / PROJECT_SPECIFIC
numPhrases=200 = existing rehearsal acquisition control, not industry standard
```

## 5. Adversarial self-audit of Step-04 candidate pool

Question used for every candidate:

```text
Does this new getTop call have a credible chance to reveal useful vocabulary not already adequately exposed by pass #1?
Or is the unresolved question actually a SERP/business-boundary question that Wordstat cannot settle?
```

### A. `оконная фурнитура` — PROPOSED READY

Evidence:

```text
pass-1 seed `аксессуары для пластиковых окон` root totalCount = 29
association `оконная фурнитура` = 1458
```

Reason:

- material vocabulary shift;
- original literal wording clearly under-sampled the family;
- new seed is likely to expose handles, mechanisms, fittings, brands and service/product terms under the vocabulary users actually use.

Uncertainty:

Business priority for accessories remains unresolved, so result remains acquisition evidence only.

Verdict: `EXPANSION_PROBE_READY / NEW_VOCABULARY`.

### B. `панорамные окна` — PROPOSED READY

Evidence:

Pass #1 used `французские окна`, which exposed panoramic/floor-to-ceiling vocabulary but the broad panoramic wording itself was not independently probed.

Reason:

- plausible synonym/family vocabulary that may be materially broader than the French-window wording;
- can reveal house/apartment/balcony/use-case language missed by the original phrase.

Verdict: `EXPANSION_PROBE_READY / NEW_VOCABULARY + DISTINCT_USER_JOB`.

### C. `остекление балкона с выносом` — PROPOSED READY

Evidence:

Broad balcony pass exposed the `с выносом` engineering branch but did not deeply sample it as its own root.

Reason:

- distinct physical/engineering balcony job already present in the site's business model;
- a targeted seed can expose wording/types/price/house-series modifiers that broad balcony seed may truncate below top-200.

Verdict: `EXPANSION_PROBE_READY / KNOWN_SUBFAMILY_GAP`.

### D. `окна для частного дома` — PROPOSED READY

Evidence:

Private-house wording appeared incidentally in pass #1, but no broad house-use-case seed represented it directly.

Reason:

- distinct application/user-job family;
- likely to expose material/profile/energy-efficiency/design/price vocabulary not reachable from Moscow apartment-centric roots.

Verdict: `EXPANSION_PROBE_READY / DISTINCT_USER_JOB`.

## 6. Candidates NOT proposed for provider execution

### `остекление террасы` — DO NOT RUN IN PASS #2

Reason:

The `остекление веранды` pass already returned substantial terrace vocabulary, including combined veranda/terrace, price, aluminium, sliding and terrace-specific variants. Another Wordstat call is likely to be high-overlap. Whether veranda and terrace deserve separate page jobs is a later SERP/page-boundary question.

Status: `DEFER_TO_SERP / REDUNDANT_WORDSTAT_RISK`.

### `панорамное остекление балкона` — DO NOT RUN IN PASS #2

Reason:

The broad `остекление балконов` pass already returned direct panoramic-balcony demand and the proposed `панорамные окна` probe provides additional broader vocabulary coverage. Running both panoramic roots now risks duplicate acquisition.

Status: `DEFER / REDUNDANT_WITH_PASS1_AND_PROPOSED_PROBE`.

### `монтаж окон` — DO NOT RUN IN PASS #2

Reason:

High association count does not solve its ambiguity. It is broader than PVC installation and can mix materials and adjacent meanings. Pass #1 already sampled `установка пластиковых окон` deeply. The unresolved issue is more about search intent/page boundary than raw vocabulary.

Status: `DEFER_TO_SERP / AMBIGUOUS`.

### `регулировка окон пвх` — DO NOT RUN NOW

Reason:

Repair pass already sampled regulation vocabulary; standalone repair acquisition priority is still client-unknown. More Wordstat depth before resolving business scope is weak information gain.

Status: `REVIEW / BUSINESS_SCOPE_UNKNOWN`.

### `москитные сетки на пластиковые окна` — DO NOT RUN NOW

Reason:

Accessories business priority remains unknown and pass #1 already surfaced substantial mosquito-screen vocabulary across installation/price/accessory families.

Status: `REVIEW / BUSINESS_SCOPE_UNKNOWN + REDUNDANCY`.

### `окна пвх` — DO NOT RUN NOW

Reason:

Near-synonym of the already very broad `пластиковые окна` seed. Expected incremental vocabulary is low relative to overlap.

Status: `REDUNDANT`.

### `стеклопакет` — DO NOT RUN NOW

Reason:

Broad adjacent product family; current client scope does not establish standalone glass-unit sales as a business priority. Could dramatically widen semantics beyond the current order.

Status: `REVIEW / BUSINESS_BOUNDARY_UNKNOWN`.

### `оконный завод` — DO NOT RUN NOW

Reason:

Manufacturer/trust intent was already sampled by `пластиковые окна от производителя`; whether `завод` creates a distinct search job is better tested later through SERP if material.

Status: `DEFER / LIKELY MODIFIER_OVERLAP`.

## 7. Proposed frozen manifest after owner approval

```text
P2-01  оконная фурнитура
       reason = NEW_VOCABULARY

P2-02  панорамные окна
       reason = NEW_VOCABULARY + DISTINCT_USER_JOB

P2-03  остекление балкона с выносом
       reason = KNOWN_SUBFAMILY_GAP

P2-04  окна для частного дома
       reason = DISTINCT_USER_JOB
```

Proposed provider controls:

```text
method = getTop
regions = ["213"]
devices = ["DEVICE_ALL"]
numPhrases = 200
seed_count = 4
maxRequests = 4
estimated provider cost = 0.08 RUB
operators = NONE
```

Proposed job id:

```text
kw001-okno-msk-wordstat-pass2-20260828
```

No batch has been created yet.

## 8. What Step 05 will NOT decide

```text
no final keyword KEEP/EXCLUDE decision
no page creation decision
no cluster split/merge decision
no repair/accessories commercial-scope decision
no veranda-vs-terrace page split
no panoramic general-vs-balcony page split
no SERP intent decision
```

## 9. Proposed execution gate

After owner authorization Step 05 passes only if:

```text
exact 4-probe manifest frozen before batch start
region 213 explicitly used
DEVICE_ALL explicitly used
no silent seed substitution
one batch.next <= one provider request
all 4 items terminal
OUTCOME_UNKNOWN never blindly replayed
request count and cost recorded
raw result provenance preserved
final batch.status captured
no semantic/page decisions made inside acquisition
```

## 10. Pre-step verdict

```text
STEP_05_METHOD_VERDICT = SUPPORTED_WITH_PROJECT_SPECIFIC_MANIFEST
STEP_04_CORRECTION_BLOCK = CLEARED
STEP_05_PROVIDER_EXECUTION = NOT STARTED
STEP_05_OWNER_AUTHORIZATION_REQUIRED = true
```

No universal KW-001 rule was changed during this review.
