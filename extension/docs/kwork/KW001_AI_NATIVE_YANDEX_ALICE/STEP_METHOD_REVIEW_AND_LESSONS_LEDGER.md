# KW-001 — STEP METHOD REVIEW AND LESSONS LEDGER

Date updated: 2026-08-29  
Status: **ACTIVE / UNIVERSAL / OWNER-LOCKED**

This file contains permanent, owner-approved KW-001 methodology lessons and corrections accumulated so far.

It is part of Layer A (permanent universal Kwork rules) and is **not** a per-job execution log.

## Owner-lock rule

This file does **not** update automatically after each job step.

During a concrete job ChatGPT may discover a possible reusable lesson, but without explicit owner instruction it may only:

```text
report the finding;
show evidence/sources;
propose a permanent change;
wait for owner instruction.
```

Only explicit owner authorization allows adding/removing/changing a permanent lesson here.

Concrete client/job words, URLs, provider results, matrices, page decisions and job histories must not be copied into this file.

## Mandatory read

Before every major step ChatGPT must read this file as part of the stable universal method, but must not mutate it unless explicitly authorized by the owner.

---

# OWNER-APPROVED STEP METHODOLOGY LESSONS

## Step 0 — order / scope freeze

### Approved rule

- Freeze business, region, goal, scope, known exclusions and requested outputs before provider evidence.
- Later findings may change recommendations but must not silently rewrite the original brief.

### Failure prevented

Do not let later evidence retroactively redefine the order so the analysis appears cleaner than it really was.

### Method origin

`PROJECT_TEST_VALIDATED + ANALYST_DISCIPLINE`.

Status: **APPROVED / ACTIVE**.

---

## Step 1 — existing-site discovery and business/page model

### Approved rule

- For a non-trivial existing site, combine deep internal architecture discovery with an independent public/search-visible discovery channel.
- Preserve evidence states: opened/read is stronger than discovered-link or inferred-template evidence.
- Merge complementary passes rather than selecting one report and discarding the other.
- Site architecture is factual/business discovery input; it does not prove that every current page deserves its own SEO target.

### Approved correction

A single discovery pass must not be treated as complete for a non-trivial site unless completeness is demonstrated and recorded.

### Method origin

`PROJECT_TEST_VALIDATED + INDUSTRY_REASONING`.

Status: **APPROVED / ACTIVE**.

---

## Step 2 — seed/query plan

### Approved rule

- A seed is an acquisition probe, not a final semantic-core keyword.
- Do not mirror every existing URL into one seed; use bounded representative roots so provider evidence can challenge current site taxonomy.
- Every second-pass expansion must have an explicit reason/information purpose.
- Numerical request/row caps used for rehearsal economics are project controls, not industry standards.

### Approved correction

Always explain what uncertainty each seed is probing and never defend/reject it based on intuition alone when measurement is the purpose of the probe.

### Method origin

`PROJECT_TEST_VALIDATED + ANALYST_HEURISTIC`.

Status: **APPROVED / ACTIVE**.

---

## Step 3 — Wordstat provider acquisition

### Approved rule

- Freeze the manifest before provider execution.
- Preserve exact phrase, region, device, provider request identity, cost and outcome state.
- `SEED != FINAL KEYWORD`.
- `RAW WORDSTAT != CLIENT SEMANTIC CORE`.
- Wordstat associations are similar-query vocabulary evidence, not automatically accepted semantic-core phrases.
- A successful sparse response is not a provider failure and not proof of zero demand.
- `OUTCOME_UNKNOWN` must never be blindly replayed.
- Before every YMB command explicitly state active service and execution mode.
- Replay safety is determined by provider-execution truth and accepted recovery policy, not UI appearance.

### Owner-approved correction — provider execution is not collection completion

The goal of Step 3 is to **collect a complete reusable dataset**, not to execute a target number of API requests.

A Step-3 provider item is complete only when the complete result required by the step has been preserved and verified before the next provider item is allowed.

Mandatory per-item sequence:

```text
DEFINE WHAT MUST BE COLLECTED
→ EXECUTE ONE PROVIDER ITEM
→ RECEIVE PROVIDER RESULT
→ PRESERVE THE COMPLETE REQUIRED RESULT
→ VERIFY PRESERVED COUNTS/FIELDS AGAINST PROVIDER TRUTH
→ CONFIRM THE SAVED RESULT IS READABLE/USABLE
→ ONLY THEN ALLOW THE NEXT PROVIDER ITEM
```

The following do **not** prove Step-3 completion by themselves:

```text
HTTP 200
status = OK
request_executed = true
item_status = SUCCEEDED
batch succeeded count
provider request count
cost recorded
representative examples
summary/checkpoint without complete returned rows
```

If the provider returns a result set and only representative examples are preserved, that item is **INCOMPLETE FOR THE PROJECT** even though the API request succeeded.

If the current item is incomplete:

```text
CURRENT_ITEM = INCOMPLETE
NEXT_PROVIDER_ITEM = BLOCKED
STEP_3 = NOT_COMPLETE
NEXT_ANALYTICAL_STEP = BLOCKED
```

For Wordstat `getTop`, preservation must explicitly account for the complete returned arrays required by the concrete step, including `results[]` and `associations[]` when those arrays are part of the acquisition objective. `totalCount` is demand/frequency evidence and must not be confused with the number of returned rows saved.

### Error that caused this correction

A controlled KW-001 rehearsal executed a multi-item Wordstat pass and recorded successful provider outcomes, but many item checkpoints preserved only counts and representative examples rather than the complete returned phrase rows. The batch was then incorrectly accepted as complete and downstream analysis proceeded without a complete reusable acquisition dataset.

The root process error was:

```text
technical success was treated as the goal
instead of verifying whether the actual data-collection goal had been achieved
```

### Failure prevented

Without this correction:

```text
a provider batch can look complete while the dataset needed by the client task is missing;
subsequent cleanup can operate on examples instead of all collected phrases;
expansion choices can be made from incomplete evidence;
several later steps can become invalid and require rework;
operator time and provider cost can be wasted;
request-count progress can replace actual project progress.
```

### Required Step-3 completion report

At the end of a Step-3 collection pass, the report must reconcile at minimum:

```text
provider items planned
provider items attempted
provider items actually executed
provider items with known outcomes
results rows returned
association rows returned where applicable
rows saved
rows verified
items incomplete
outcome_unknown
provider cost
```

If the relevant counts do not reconcile, Step 3 cannot pass.

### Method origin

`OFFICIAL provider semantics + PROJECT_TEST_VALIDATED + OWNER-APPROVED PROCESS CORRECTION`.

Status: **APPROVED / ACTIVE**.

---

## Step 4 — first post-Wordstat triage / cleanup preparation

### Approved rules

- Do not treat raw Wordstat output as a ready semantic core.
- Preserve ambiguous potentially valuable demand for later business/SERP resolution rather than deleting it prematurely.
- Wordstat associations are vocabulary/expansion evidence, not automatically accepted keywords.
- Do not make final cluster/page decisions before ordinary SERP evidence when page-boundary uncertainty remains.
- Business-priority unknowns must remain unresolved rather than being silently promoted or deleted.

### Approved correction A — family-level triage is not full cleanup

Do not call a family/pattern review `complete semantic cleanup`.

Before final semantic-core freeze, row-level retained/excluded provenance must exist for the phrases used in the workflow.

### Approved correction B — separate exclusion reasons

Use distinct states/reasons such as:

```text
KEEP
REVIEW
EXCLUDE_IRRELEVANT
EXCLUDE_SCOPE
EXCLUDE_MECHANICAL
```

A semantically valid phrase outside the frozen client scope is not the same thing as irrelevant demand.

### Approved correction C — frequency rule

Canonical rule:

```text
LOW_FREQUENCY_ALONE != PROOF_OF_IRRELEVANCE
```

Frequency may still contribute later to prioritization/page decisions together with relevance, business value, cluster/topic size and SERP evidence.

### Approved correction D — association confidence

A high-count broad association may justify an acquisition probe without becoming a strong semantic candidate.

Use probe confidence/status concepts such as:

```text
EXPANSION_PROBE_READY
EXPANSION_PROBE_AMBIGUOUS
EXPANSION_PROBE_REVIEW
```

### External support already checked when owner approved this correction

Official Yandex Wordstat GetTop:
- https://aistudio.yandex.ru/docs/ru/search-api/api-ref/Wordstat/getTop

External corroboration:
- https://www.semrush.com/blog/keyword-clustering/
- https://ahrefs.com/blog/keyword-mapping/
- https://ahrefs.com/blog/keyword-intent/

Exact internal status names remain project-specific mechanics, not claimed industry standards.

### Method origin

`OFFICIAL + INDUSTRY_PRACTICE + ANALYST_HEURISTIC (owner-approved correction)`.

Status: **APPROVED / ACTIVE**.

---

## Step 5 — targeted Wordstat expansion pass #2

Status: **NOT YET UNIVERSALLY VALIDATED BY EXECUTION**.

Current stable pre-step questions:

```text
Does each proposed probe add information rather than duplicate pass #1?
Is the phrase a semantic target or only an acquisition probe?
What exact uncertainty will its provider result resolve?
Is the business family actually in scope or still client-unknown?
Is a broad association being over-promoted merely because of count?
Can the uncertainty be resolved more appropriately by later SERP evidence instead?
```

A concrete job's exact Step-5 probe manifest belongs in that job workspace and does not belong here.

---

# Permanent-update policy

If a future job reveals a potential universal lesson:

```text
1. report it to the owner in the step report;
2. provide evidence and source support;
3. do not edit this file;
4. wait for explicit owner instruction;
5. only then update the permanent universal method if instructed.
```

Markers:

```text
KW001_PERMANENT_LESSONS_LEDGER_ACTIVE = true
KW001_PERMANENT_LESSONS_OWNER_LOCKED = true
KW001_NO_AUTOMATIC_LESSON_PROMOTION = true
KW001_STEP3_PROVIDER_EXECUTION_NOT_COLLECTION_COMPLETION = true
KW001_STEP3_NEXT_ITEM_BLOCKED_UNTIL_COMPLETE_RESULT_VERIFIED = true
KW001_STEP3_COMPLETION_COUNTS_MUST_RECONCILE = true
KW001_FAMILY_TRIAGE_NOT_EQUAL_FULL_CLEANUP = true
KW001_SCOPE_EXCLUSION_SEPARATE_FROM_IRRELEVANCE = true
KW001_LOW_FREQUENCY_ALONE_NOT_IRRELEVANCE_PROOF = true
KW001_ASSOCIATION_IS_PROBE_NOT_ACCEPTED_KEYWORD = true
```
