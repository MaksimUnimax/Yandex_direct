# KW-001 — STEP METHOD REVIEW AND LESSONS LEDGER

Date created: 2026-08-28  
Status: **ACTIVE / UNIVERSAL / MUST BE READ BEFORE EVERY MAJOR STEP**

This file is the permanent cross-case memory for methodology mistakes, validated corrections and reusable lessons discovered during KW-001 execution.

It is deliberately separate from case-specific evidence. Do not copy concrete domains, URLs, counts or client-specific conclusions here. Concrete incidents belong under `tests/<CASE_ID>/`.

## Mandatory use

Before every major step ChatGPT must read:

```text
PRE_STEP_EVIDENCE_AND_METHOD_REVIEW_GATE.md
STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md
current case STEP_REVIEW_AND_ERRORS_LEDGER.md if one exists
previous step acceptance/evidence
```

After every major step, before declaring the step fully closed, ChatGPT must append/update the relevant lesson record with:

```text
STEP / STAGE
WHAT WAS DONE
WHAT WAS CORRECT
WHAT WAS WRONG / TOO STRONG / UNDER-SPECIFIED
METHOD ORIGIN
EVIDENCE USED
CORRECTION
PREVENT-REPEAT RULE
STATUS
```

A PASS gate does not mean the methodology can never be corrected later. If a later review finds a defect, preserve the original historical artifact and create/update an explicit correction that supersedes the defective claim.

---

# STEP-BY-STEP LESSONS

## Step 0 — order / scope freeze

### What is correct

- Freeze business, region, goal, scope, known exclusions and requested outputs before provider evidence.
- Later findings may change recommendations but must not silently rewrite the original brief.

### Known failure to prevent

Do not let later evidence retroactively redefine the order so the analysis appears cleaner than it really was.

### Method origin

`PROJECT_TEST_VALIDATED + ANALYST_DISCIPLINE`.

### Prevent-repeat rule

Every scope change after freeze must be logged as a client/owner revision, not silently substituted.

Status: **SUPPORTED / ACTIVE**.

---

## Step 1 — existing-site discovery and business/page model

### What is correct

- For a non-trivial existing site, combine deep internal architecture discovery with an independent public/search-visible discovery channel.
- Preserve evidence states: opened/read is stronger than discovered-link or inferred-template evidence.
- Merge complementary passes rather than selecting one agent/report and discarding the other.
- Site architecture is factual/business discovery input; it does not prove that every current page deserves its own SEO target.

### Error already caught

A single discovery pass was initially treated as sufficient. A later independent pass exposed complementary blind spots.

### Correction

Use cross-channel saturation and provenance-preserving merge before freezing the business/page model.

### Prevent-repeat rule

Never freeze a non-trivial existing-site inventory from one discovery channel unless completeness is demonstrated and recorded.

Method origin: `PROJECT_TEST_VALIDATED + INDUSTRY_REASONING`.

Status: **CORRECTED / ACTIVE**.

---

## Step 2 — seed/query plan

### What is correct

- A seed is an acquisition probe, not a final semantic-core keyword.
- Do not mirror every existing URL into one seed; use bounded representative roots so provider evidence can challenge current site taxonomy.
- Every second-pass expansion must have an explicit reason code and information purpose.
- Numerical request/row caps used for rehearsal economics are project controls, not industry standards.

### Error already caught

The distinction `SEED != FINAL KEYWORD` was not explained clearly enough in live dialogue. A diagnostic low-volume-looking seed was challenged and ChatGPT initially leaned toward agreement before provider measurement.

### Correction

Always explain what uncertainty each seed is probing and never defend/reject it based on intuition alone when measurement is the purpose of the probe.

### Prevent-repeat rule

Before freezing a seed manifest, record `seed -> business/search-job family -> uncertainty tested -> reason for inclusion`.

Method origin: `PROJECT_TEST_VALIDATED + ANALYST_HEURISTIC`.

Status: **CORRECTED / ACTIVE**.

---

## Step 3 — Wordstat pass #1 provider acquisition

### What is correct

- Freeze the manifest before provider execution.
- Preserve exact phrase, region, device, provider request identity, cost and outcome state.
- `SEED != FINAL KEYWORD` and `RAW WORDSTAT != CLIENT SEMANTIC CORE`.
- Wordstat `associations` are similar-query vocabulary evidence, not automatically accepted semantic-core phrases.
- A successful sparse response is not a provider failure and not proof of zero demand.
- `OUTCOME_UNKNOWN` must never be blindly replayed.

### Errors/incidents already caught

1. Operator instruction once omitted the required active YMB service, causing a recoverable `SERVICE_NOT_ACTIVE` admission failure with no provider request.
2. A separate delivery/send-button failure occurred before provider execution; replay was safe only because `request_executed=false`.

### Correction

Always state active service + execution mode before every YMB command. Use provider-execution truth, not UI intuition, to decide whether replay is safe.

### Prevent-repeat rule

Never issue an operator command without explicit YMB mode. Never replay a failed/uncertain provider action unless execution truth proves the original attempt did not execute or the accepted recovery contract explicitly permits it.

Method origin: `OFFICIAL provider semantics + PROJECT_TEST_VALIDATED`.

Status: **SUPPORTED WITH OPERATOR-DISCIPLINE CORRECTION / ACTIVE**.

---

## Step 4 — first post-Wordstat triage / cleanup preparation

### What was correct

- Do not treat raw Wordstat output as a ready semantic core.
- Remove clearly irrelevant semantic noise while preserving ambiguous potentially valuable demand for later business/SERP resolution.
- Do not use Wordstat associations as automatically accepted keywords; use them as possible vocabulary/expansion probes.
- Do not make final cluster/page decisions before ordinary SERP evidence where page-boundary uncertainty remains.
- Business-priority unknowns such as standalone services/accessories/finance must remain unresolved rather than being silently promoted or deleted.

### Defects found in retrospective audit

#### Defect A — scope of work was overstated

The artifact said `ANALYTICAL CLEANUP COMPLETE`, but the actual work was family-level/pattern-level triage across seed results, not a complete row-by-row classification of every raw Wordstat phrase.

**Correction:** call this stage `FAMILY-LEVEL TRIAGE / CLEANUP RULE FREEZE`. Full row-level retained/excluded provenance must exist before the final semantic-core freeze.

#### Defect B — one rejection bucket mixed different reasons

`REJECT_OBVIOUS` mixed true irrelevance with valid-but-out-of-scope geography.

**Correction:** separate at least:

```text
KEEP
REVIEW
EXCLUDE_IRRELEVANT
EXCLUDE_SCOPE
EXCLUDE_MECHANICAL
```

A relevant phrase outside the frozen region/business scope is not semantically bad; it is excluded by scope and must remain recoverable if scope changes.

#### Defect C — low-frequency rule was too absolute

`low frequency is never a rejection reason` was directionally useful but over-broad.

**Correction:**

```text
LOW_FREQUENCY_ALONE != PROOF_OF_IRRELEVANCE
```

Frequency may still contribute later to prioritization/page-target decisions together with relevance, business value, cluster size/traffic potential and SERP evidence.

#### Defect D — expansion confidence was too strong for some broad associations

A broad association can be useful as an acquisition probe without being a strong semantic candidate.

**Correction:** expansion handoff must classify candidates as probes by expected information gain and ambiguity, e.g.:

```text
EXPANSION_PROBE_READY
EXPANSION_PROBE_AMBIGUOUS
EXPANSION_PROBE_REVIEW
```

Do not label a broad related phrase `strong` merely because its association count is high.

### External methodology support checked

Official Yandex Wordstat GetTop documentation:
- https://aistudio.yandex.ru/docs/ru/search-api/api-ref/Wordstat/getTop
- `results` are returned query results; `associations` are queries similar to the requested phrase; `regions` are regions where the query was made.

External clustering/intent methodology used as corroboration, not as Yandex policy:
- https://www.semrush.com/blog/keyword-clustering/
- https://ahrefs.com/blog/keyword-mapping/
- https://ahrefs.com/blog/keyword-intent/

These sources support separating keyword collection from later intent/topic/page grouping and checking user intent/business value instead of treating raw volume as a page decision.

### Prevent-repeat rule

Never call a family-level review `complete semantic cleanup`. Preserve row-level provenance for final cleanup. Separate irrelevance from scope exclusion. Treat frequency as one signal, not a universal delete/keep rule. Treat associations as probe evidence, not accepted keywords.

Method origin: `OFFICIAL + INDUSTRY_PRACTICE + ANALYST_HEURISTIC (corrected)`.

Status: **CORRECTED / ACTIVE**.

---

## Step 5 — targeted Wordstat expansion pass #2

Status: **NOT EXECUTED YET**.

Before execution, the pre-step gate must specifically test:

```text
Does each proposed probe add information rather than duplicate pass #1?
Is the phrase a semantic target or only an acquisition probe?
What exact uncertainty will its provider result resolve?
Is the business family actually in scope or still client-unknown?
Is a broad association being over-promoted merely because of count?
Can the same uncertainty be resolved later by SERP instead of another Wordstat request?
```

No Step-5 provider batch may be created until the owner sees the source-backed pre-step review and explicitly authorizes it.

---

# FUTURE STEP TEMPLATE

For each later step append a section before/after execution:

```text
## Step N — <name>

PRE-STEP METHOD REVIEW
- intended operation:
- external/official sources checked:
- method-origin labels:
- prior-step defects checked:
- pre-step verdict:

POST-STEP LESSONS
- what was done correctly:
- what failed / was ambiguous:
- what was learned:
- correction made:
- prevent-repeat rule:
- artifacts/acceptance affected:
- status:
```

A future clean-context ChatGPT must not proceed merely because a step appears in the runbook. It must read the accumulated lessons and the latest correction authority first.

Markers:

```text
KW001_PER_STEP_LESSONS_LEDGER_ACTIVE = true
KW001_PREVENT_REPEAT_ERROR_MEMORY_ACTIVE = true
KW001_FAMILY_TRIAGE_NOT_EQUAL_FULL_CLEANUP = true
KW001_SCOPE_EXCLUSION_SEPARATE_FROM_IRRELEVANCE = true
KW001_LOW_FREQUENCY_ALONE_NOT_IRRELEVANCE_PROOF = true
KW001_ASSOCIATION_IS_PROBE_NOT_ACCEPTED_KEYWORD = true
```
