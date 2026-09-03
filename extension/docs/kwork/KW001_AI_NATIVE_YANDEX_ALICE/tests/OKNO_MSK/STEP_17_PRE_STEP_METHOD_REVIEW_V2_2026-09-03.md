# OKNO_MSK — STEP 17 PRE-STEP METHOD / EVIDENCE REVIEW V2

Date: 2026-09-03
Status: **CORRECTED METHOD AUTHORITY / STEP17 CORRECTION REQUIRED / STEP18 BLOCKED**
Supersedes for future Step-17 execution:
- `STEP_17_PRE_STEP_METHOD_REVIEW_2026-09-02.md`

Mandatory correction authority:
- `STEP_17_METHOD_FAILURES_AND_CORRECT_EXECUTION_ADDENDUM_2026-09-03.md`

## Why V2 exists

The first Step-17 method was researched before execution, but post-run audit found three omissions:

```text
S17-M01 — required source-worthiness implication was not materialized
S17-M02 — Search-side final claims were not directly reverse-traced to concrete persisted SERP evidence
S17-M03 — adversarial self-review was partially labelled as independent QA
```

The failure was not absence of research. It was incomplete conversion of the original Step-17 contract into final fields and QA.

Canonical V2 rule:

```text
ORIGINAL CONTRACT + EXTERNAL RESEARCH + PRIOR LESSONS
-> MASTER REQUIREMENT REGISTER
-> EXECUTION FIELD FOR EVERY REQUIREMENT
-> FINAL ARTIFACT FIELD FOR EVERY EXECUTION FIELD
-> QA / ACCEPTANCE CHECK FOR EVERY FINAL FIELD
```

If any arrow is missing, Step 17 is not ready.

## Whole KW-001 goal

Deliver an evidence-backed semantic/page architecture for ordinary Yandex Search plus selective Yandex generative-search evidence, then prioritize and package recommendations without equating GenSearch with consumer Alice and without hiding content/source-worthiness gaps behind an unchanged architecture verdict.

## Current roadmap truth

```text
Steps 0–16 = COMPLETE under their current accepted/corrected authorities
Step 17 = CORRECTION REQUIRED after external post-run audit
Step 18 = BLOCKED
Steps 19–22 = NOT STARTED
```

## Correct Step-17 goal

For every frozen AI-tested exact query, compare ordinary Yandex Search evidence with corrected GenSearch evidence and current-page evidence, then produce **two separate result layers**:

```text
A. MATERIAL / ARCHITECTURE DELTA
   CHANGE | DE_RISK | NO_CHANGE | INSUFFICIENT

B. SOURCE-WORTHINESS / CONTENT-IMPROVEMENT STATE
   NO_MATERIAL_CONTENT_GAP_OBSERVED
   CONTENT_EXPANSION_CANDIDATE
   SOURCE_WORTHINESS_GAP
   INSUFFICIENT
   NOT_APPLICABLE
```

Step 17 must not treat layer A as a substitute for layer B.

Canonical prohibition:

```text
NO_ARCHITECTURE_CHANGE
!=
NO_CONTENT_CHANGE
```

## Required outputs for every case

### Search-side direct evidence

```text
ordinary_search_direct_evidence_refs
ordinary_search_observed_result_count
ordinary_search_decisive_result_refs
ordinary_search_task
ordinary_search_content_type
ordinary_search_format
ordinary_search_angle
ordinary_search_specificity
ordinary_search_task_derivation_note
ordinary_search_trace_state
```

### GenSearch-side evidence

```text
gensearch_raw_refs
gensearch_observation
gensearch_answer_mode
gensearch_refined_queries
used_source_pages
used_source_roles_validated
reproducibility_state
```

### Current target/source-worthiness evidence

```text
current_target_page_evidence
source_worthiness_evidence
source_worthiness_implication
content_gap_vs_used_sources
content_improvement_state
content_improvement_action_if_any
content_claim_boundary
```

### Comparison / decision

```text
task_delta
commerciality_delta
specificity_delta
source_role_delta
target_site_fit
materiality_reason
final_step17_verdict
architecture_delta_required
architecture_delta_overlay
claim_boundary
evidence_refs
qa_state
```

## Correct execution sequence

The detailed mandatory procedure is defined in:

`STEP_17_METHOD_FAILURES_AND_CORRECT_EXECUTION_ADDENDUM_2026-09-03.md`

Execution order:

```text
0. Freeze original Step17 contract and master requirement register.
1. Build case evidence map with direct Search and GenSearch refs.
2. Derive ordinary-Search task directly from persisted SERP evidence.
3. Derive GenSearch side from corrected raw evidence, excluding old Step16 verdicts.
4. Direct-read material used sources and current target pages.
5. Compare fixed Search-vs-GenSearch axes.
6. Separately analyze source-worthiness/content gap.
7. Assign architecture/material verdict and content-improvement state separately.
8. Apply reproducibility and upstream-baseline gates.
9. Run adversarial self-review; independent QA only if actually independent.
10. Run final original-contract coverage + reverse-trace audit.
11. Only after all gates pass, accept Step17 and allow Step18 pre-step.
```

## Why each phase exists

```text
Phase 0 prevents missing required fields from the original implementation plan.
Phase 1 prevents a comparison with one side represented only by analyst prose.
Phase 2 makes Search conclusions auditable against concrete SERP evidence.
Phase 3 prevents old Step16 labels from contaminating Step17.
Phase 4 prevents URL/title guesses from becoming material content claims.
Phase 5 keeps all cases on the same comparison axes.
Phase 6 captures AI/content implications even when architecture remains unchanged.
Phase 7 prevents NO_CHANGE from being misread as NO_SITE_IMPROVEMENT.
Phase 8 prevents stochastic AI snapshots from overdriving architecture decisions.
Phase 9 keeps QA terminology truthful and separates self-review from independence.
Phase 10 catches the exact failure that escaped V1: a sensible method with incomplete required outputs.
Phase 11 blocks downstream prioritization until the comparison artifact is actually complete.
```

## Evidence/claim boundaries retained from V1

```text
GEN_SEARCH != CONSUMER_ALICE
GEN_SEARCH != WEBMASTER_ALICE_VISIBILITY
EXACT_QUERY != USER_JOB_FAMILY
SINGLE_RUN != LONG_TERM_STABILITY
SHORT_WINDOW_REPEAT != LONG_TERM_STABILITY
SOURCE_ORDER != RANK
USED_SOURCE_COUNT != RANK
URL_TITLE_ROLE_HINT != MATERIAL_ROLE_PROOF
OLD_STEP16_FINAL_LABELS != STEP17 VERDICT INPUT
```

## Provider policy

```text
NEW PAID ORDINARY SEARCH CALLS = 0 BY DEFAULT
NEW PAID GENSEARCH CALLS = 0 BY DEFAULT
```

Correction must first reuse already persisted evidence.

A new request is allowed only if a specific blocking evidence gap remains after attempting to recover/use existing artifacts and the existing information-gain/owner-authorization gate passes.

## V2 PASS condition

Step 17 cannot pass until:

```text
CASES_ACCOUNTED = 8/8
SEARCH_DIRECT_TRACE = 8/8
GENSEARCH_DIRECT_TRACE = 8/8
SOURCE_WORTHINESS_IMPLICATION = 8/8
CONTENT_IMPROVEMENT_STATE = 8/8
MATERIAL_SOURCE_ROLE_WITHOUT_DIRECT_VALIDATION = 0
MATERIAL_SOURCE_WORTHINESS_WITHOUT_DIRECT_VALIDATION = 0
MATERIAL_TARGET_CONTENT_WITHOUT_CURRENT_EVIDENCE = 0
OLD_STEP16_FINAL_LABEL_CONTAMINATION = 0
SOURCE_ORDER_RANK_INFERENCE = 0
CONSUMER_ALICE_EQUIVALENCE = 0
UNREPRODUCED_AI_ONLY_CHANGE = 0
QA_MODE_LABEL_MATCHES_ACTUAL_PROCESS = true
ORIGINAL_CONTRACT_FINAL_OUTPUT_COVERAGE = 100%
REVERSE_TRACE_MISSING = 0
FINAL_GITHUB_READBACK = PASS
```

Until then:

```text
STEP17 = CORRECTION_REQUIRED
STEP18 = BLOCKED
```
