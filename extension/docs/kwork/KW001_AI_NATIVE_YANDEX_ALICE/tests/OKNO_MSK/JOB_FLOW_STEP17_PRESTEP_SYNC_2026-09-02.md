# OKNO_MSK — JOB FLOW SYNC / STEP 17 PRE-STEP

Date: 2026-09-02  
Status: **STEP 17 PREPARED / METHOD RESEARCH COMPLETE / PREEXECUTION SELF-AUDIT CORRECTED / EXECUTION NOT STARTED / OWNER AUTHORIZATION REQUIRED**

## Full roadmap

| Step | Meaning | Status |
|---|---|---|
| 0 | Scope freeze | ✅ COMPLETE |
| 1 | Existing-site/business discovery | ✅ COMPLETE |
| 2 | Wordstat acquisition plan | ✅ COMPLETE |
| 3 / 3R | Wordstat acquisition + durable repair | ✅ COMPLETE |
| 4 | Family triage | ✅ COMPLETE |
| 5 | Targeted expansion | ✅ COMPLETE |
| 6 / 6A | Demand dynamics + coverage revalidation | ✅ COMPLETE / PRESERVED |
| 7 | Row-level cleanup | ✅ COMPLETE AFTER CORRECTION |
| 8 | Search-stage semantic freeze | ✅ COMPLETE AFTER METHOD CORRECTION |
| 9 | Ordinary Yandex Search validation | ✅ COMPLETE AFTER CORRECTIONS |
| 10 | User-task/SERP clustering | ✅ COMPLETE / VERIFIED |
| 11 | Page ownership | ✅ COMPLETE AFTER AUDIT |
| 12 | Structural actions | ✅ COMPLETE AFTER CORRECTIONS |
| 13 | Cannibalization diagnosis | ✅ COMPLETE / BASE PUBLIC MODE |
| 14 / 14A | Search-only architecture freeze + current-site revalidation | ✅ FINAL PASS |
| 15 V2 | AI-case selection | ✅ FINAL PASS |
| 16 | GenSearch evidence acquisition | ✅ COMPLETE / POST-RUN CORRECTED / FINAL READBACK PASS |
| **17** | **Search-vs-GenSearch comparison + bounded AI-derived delta overlay** | **🟡 PREPARED / NOT STARTED** |
| 18 | Prioritization | ⬜ NOT STARTED |
| 19 | Client deliverables | ⬜ NOT STARTED |
| 20 | Final QA | ⬜ NOT STARTED |
| 21 | Handoff/revisions | ⬜ NOT STARTED |
| 22 | Job close | ⬜ NOT STARTED |

## Step-17 prepared authorities

```text
STEP_17_PRE_STEP_METHOD_REVIEW_2026-09-02.md
STEP_17_RESEARCH_TO_EXECUTION_SCHEMA_2026-09-02.json
STEP_17_EXECUTION_MANIFEST_2026-09-02.json
STEP_17_CASE_COMPARISON_PLAN_2026-09-02.tsv
STEP_17_CURRENT_STATE.json
```

## Step-17 input truth

```text
CASES = 8 exact queries
SEARCH BASELINE = STEP_15_SELECTED_CASES_V2.tsv
GENSEARCH AUTHORITY = STEP_16_OBSERVATIONS_CORRECTED_V2_2026-09-02.json + raw verbatim
SEARCH-ONLY ARCHITECTURE = Step14/14A accepted baseline
OLD STEP16 FINAL LABELS = HISTORICAL / FORBIDDEN AS VERDICT INPUT
```

## Method boundary

```text
STEP17 = compare all 8 exact-query cases
STEP17 VERDICTS = CHANGE / DE_RISK / NO_CHANGE / INSUFFICIENT
STEP17 MAY = create case-scoped AI-derived architecture delta overlay for qualified CHANGE
STEP17 MAY NOT = rebuild whole architecture
STEP17 MAY NOT = perform Step18 prioritization
```

## Evidence/claim boundaries

```text
GEN_SEARCH != CONSUMER_ALICE
GEN_SEARCH != WEBMASTER_ALICE_VISIBILITY
EXACT_QUERY != USER_JOB_FAMILY
SINGLE_RUN != LONG_TERM_STABILITY
SHORT_WINDOW_REPEAT != LONG_TERM_STABILITY
INDEPENDENT_NON_AI_EVIDENCE != AI_REPRODUCTION
UPSTREAM_BASELINE_CORRECTION != AI_DRIVEN_CHANGE
SOURCE_ORDER != RANK
USED_SOURCE_COUNT != RANK
URL_TITLE_ROLE_HINT != MATERIAL_ROLE_PROOF
```

## Preexecution self-audit correction

The first Step-17 draft allowed independent non-AI evidence to substitute for reproduction of a material single-run AI contradiction. This was rejected before execution.

Correct rule:

```text
AI-DRIVEN CHANGE
-> requires sufficient AI reproduction/evidence strength for the claim
-> independent non-AI evidence is not a substitute

IF direct non-AI evidence independently proves Step14 baseline wrong/stale
-> UPSTREAM_BASELINE_CORRECTION_REQUIRED
-> stop affected Step17 case verdict
-> correct/re-freeze affected upstream baseline
-> only then resume comparison
```

This prevents an upstream Search/current-page error from being mislabeled as "AI changed the architecture".

## Provider plan

```text
NEW ORDINARY SEARCH CALLS = 0
NEW GENSEARCH CALLS = 0
NEW WEBMASTER CALLS = 0
PLANNED PROVIDER COST = 0 RUB
```

Fresh provider work is permitted only after a blocking evidence gap is documented under the research-to-execution gate and the owner explicitly authorizes the exact request.

## Current Step-17 execution truth

```text
METHOD RESEARCH COMPLETE = true
RESEARCH_TO_EXECUTION SCHEMA = PRE-EXECUTION PASS AFTER SELF-AUDIT CORRECTION
EXECUTION MANIFEST = FROZEN FOR OWNER REVIEW
CASE PLAN = 8/8 PREPARED
TEN-POINT PRE-EXECUTION CHECK = PASS FOR OWNER REVIEW
STEP17 EXECUTION STARTED = false
CASES COMPARED = 0
FINAL VERDICTS = 0
ARCHITECTURE DELTA ROWS = 0
PROVIDER CALLS = 0
PROVIDER COST = 0 RUB
```

## Next legal action

```text
OWNER REVIEW / EXPLICIT STEP17 EXECUTION AUTHORIZATION
```

Until that authorization:

```text
STEP17_EXECUTION = BLOCKED
STEP18 = NOT STARTED
```
