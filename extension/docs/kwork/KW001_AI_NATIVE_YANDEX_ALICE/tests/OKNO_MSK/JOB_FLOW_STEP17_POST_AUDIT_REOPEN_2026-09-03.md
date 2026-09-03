# OKNO_MSK — JOB FLOW SYNC / STEP 17 POST-AUDIT REOPEN

Date: 2026-09-03
Authority type: **latest Step-17 roadmap/status overlay**
Status: **STEP 17 CORRECTION REQUIRED / STEP 18 BLOCKED**

This overlay supersedes the Step-17 completion status in `JOB_FLOW_STEP17_EXECUTION_SYNC_2026-09-02.md` where the two conflict.

## Full roadmap

| Step | Meaning | Status |
|---|---|---|
| 0 | Scope/order freeze | ✅ COMPLETE |
| 1 | Existing-site/business discovery | ✅ COMPLETE |
| 2 | Wordstat acquisition plan | ✅ COMPLETE |
| 3 / 3R | Wordstat acquisition + durable repair | ✅ COMPLETE |
| 4 | Family triage | ✅ COMPLETE |
| 5 | Targeted expansion | ✅ COMPLETE |
| 6 / 6A | Demand dynamics + coverage revalidation | ✅ COMPLETE / PRESERVED |
| 7 | Row-level cleanup | ✅ COMPLETE AFTER CORRECTION |
| 8 | Search-stage semantic freeze | ✅ COMPLETE AFTER METHOD CORRECTION |
| 9 | Ordinary Yandex Search validation | ✅ COMPLETE AFTER CORRECTIONS |
| 10 | User-task / SERP clustering | ✅ COMPLETE / VERIFIED |
| 11 | Page ownership | ✅ COMPLETE AFTER AUDIT |
| 12 | Structural actions | ✅ COMPLETE AFTER CORRECTIONS |
| 13 | Cannibalization diagnosis | ✅ COMPLETE / BASE PUBLIC MODE |
| 14 / 14A | Search-only architecture freeze + current-site/topology revalidation | ✅ FINAL PASS |
| 15 V2 | AI-case selection / preregistration | ✅ FINAL PASS |
| 16 | GenSearch evidence acquisition | ✅ COMPLETE / POST-RUN CORRECTED |
| **17 first pass** | Search-vs-GenSearch comparison | 🔁 HISTORICAL FIRST PASS / POST-RUN AUDIT FOUND 3 DEFECTS |
| **17 V2 correction** | Direct Search trace + source-worthiness/content-gap + truthful QA mode + contract coverage audit | **🟡 CORRECTION REQUIRED / NEXT LEGAL WORK** |
| 18 | Prioritization | ⛔ BLOCKED BY STEP17 V2 |
| 19 | Client deliverables | ⬜ NOT STARTED |
| 20 | Final QA | ⬜ NOT STARTED |
| 21 | Handoff/revisions | ⬜ NOT STARTED |
| 22 | Job close | ⬜ NOT STARTED |

## What the first Step-17 pass still established

Historical first-pass result remains preserved:

```text
CASES COMPARED = 8/8
CHANGE = 0
DE_RISK = 4
NO_CHANGE = 3
INSUFFICIENT = 1
ARCHITECTURE DELTA ROWS = 0
NEW PROVIDER CALLS = 0
STEP17 FIRST-PASS PROVIDER COST = 0 RUB
```

The audit did not automatically prove these architecture verdicts wrong.

What the audit proved is that Step 17 was **incomplete as the full original Search-vs-AI deliverable**.

## Three post-run defects

```text
S17-M01 — `source-worthiness implication` required by IMPLEMENTATION_PLAN was omitted from final case output.
S17-M02 — Search-side final task/type/format/angle claims were weakly reverse-traced to Step15 summaries instead of concrete persisted SERP evidence rows/results.
S17-M03 — adversarial self-review was partially represented with independent-QA acceptance terminology without demonstrated independence.
```

## Why this happened although research was done before Step 17

```text
EXTERNAL RESEARCH WAS DONE
PRIOR STEP16 LESSONS WERE READ
METHOD RULES WERE WRITTEN
BUT
NO FINAL ORIGINAL-CONTRACT COVERAGE AUDIT WAS RUN
```

The preparation validated whether the rules we had written were reasonable, but did not verify that **every required output in the original implementation plan** had become:

```text
required schema field
-> execution action
-> final ledger column
-> evidence reference
-> QA check
```

That is the process failure now recorded in:

`STEP_17_METHOD_FAILURES_AND_CORRECT_EXECUTION_ADDENDUM_2026-09-03.md`

## Correct Step-17 V2 result model

Every case must now produce two independent layers:

```text
1. ARCHITECTURE / MATERIAL DELTA
   CHANGE | DE_RISK | NO_CHANGE | INSUFFICIENT

2. CONTENT / SOURCE-WORTHINESS STATE
   NO_MATERIAL_CONTENT_GAP_OBSERVED
   CONTENT_EXPANSION_CANDIDATE
   SOURCE_WORTHINESS_GAP
   INSUFFICIENT
   NOT_APPLICABLE
```

Hard rule:

```text
NO_ARCHITECTURE_CHANGE != NO_CONTENT_CHANGE
```

## Correct V2 execution sequence

```text
0. Freeze original Step17 contract and master requirement register.
1. Build evidence map for all 8 cases.
2. Directly trace Search-side conclusions to persisted SERP evidence.
3. Read corrected GenSearch/raw evidence; old Step16 verdicts forbidden.
4. Direct-read material used sources and current target pages.
5. Compare fixed Search-vs-GenSearch axes.
6. Separately compare source-worthiness/content gaps.
7. Assign architecture verdict and content-improvement state separately.
8. Apply reproducibility/upstream-baseline gates.
9. Run adversarial self-review; independent QA only if truly independent.
10. Run original-contract final-output coverage and reverse-trace audit.
11. Final readback; only then Step17 PASS and Step18 pre-step allowed.
```

Detailed reasoning for every phase is authoritative in:

`STEP_17_METHOD_FAILURES_AND_CORRECT_EXECUTION_ADDENDUM_2026-09-03.md`

## Current V2 authorities

```text
STEP_17_METHOD_FAILURES_AND_CORRECT_EXECUTION_ADDENDUM_2026-09-03.md
STEP_17_PRE_STEP_METHOD_REVIEW_V2_2026-09-03.md
STEP_17_RESEARCH_TO_EXECUTION_SCHEMA_V2_2026-09-03.json
STEP_17_EXECUTION_MANIFEST_V2_2026-09-03.json
STEP_17_CURRENT_STATE.json
```

## Provider/cost truth

The correction itself does **not** require new paid calls by default.

```text
PLANNED NEW ORDINARY SEARCH CALLS = 0
PLANNED NEW GENSEARCH CALLS = 0
PLANNED NEW WEBMASTER CALLS = 0
PLANNED PROVIDER COST = 0 RUB
```

Existing persisted evidence must be reused first.

## Transition

```text
STEP17 = CORRECTION_REQUIRED
STEP18_PRESTEP_ALLOWED = false
STEP18_EXECUTION = BLOCKED
NEXT LEGAL ACTION = STEP17 V2 CORRECTION ONLY
```
