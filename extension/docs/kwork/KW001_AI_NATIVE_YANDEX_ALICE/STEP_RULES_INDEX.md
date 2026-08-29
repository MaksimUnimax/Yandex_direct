# KW-001 — STEP RULES INDEX

Date: 2026-08-29  
Status: **ACTIVE / UNIVERSAL / OWNER-APPROVED / OWNER-LOCKED**

This file is the index of step-specific methodology coverage.

It does not replace `STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md`. The ledger contains the actual rules, causes, errors and controls. This index prevents a future ChatGPT from assuming that a step has a validated method merely because it appears in the job roadmap.

Canonical rule:

```text
ROADMAP_STAGE_EXISTS != METHODOLOGY_VALIDATED
```

Before executing a major step, ChatGPT must check this index and then read the detailed step entry in the permanent lessons ledger.

If a material step is `UNVALIDATED` or has no sufficient detailed entry:

```text
CURRENT INTERNET METHOD RESEARCH = REQUIRED
OWNER-FACING METHOD REVIEW = REQUIRED
EXECUTION = BLOCKED UNTIL THAT REVIEW IS COMPLETE
```

A current job may execute a newly researched method after the full pre-step gate and owner authorization, but the method does not become a permanent universal lesson automatically. Permanent promotion still requires explicit owner instruction.

---

# Current methodology coverage

| Stage | Purpose | Permanent methodology status | Known reusable lesson/error state |
|---|---|---|---|
| Step 0 | Order / scope freeze | **APPROVED / ACTIVE** | Prevent later evidence from silently rewriting the original brief. |
| Step 1 | Existing-site discovery / business-page model | **APPROVED / ACTIVE** | One discovery pass is not automatically complete; preserve evidence strength and cross-check channels. |
| Step 2 | Seed / acquisition probe plan | **APPROVED / ACTIVE** | Seed is an acquisition probe, not a final keyword/page target. |
| Step 3 | Wordstat/provider acquisition | **APPROVED / ACTIVE** | Provider/API success is not collection completion; complete returned evidence must be preserved and verified before advancing. |
| Step 3R | Repair of incomplete Step-3 acquisition | **JOB-SPECIFIC RECOVERY PATTERN / GOVERNED BY STEP 3** | Repair should recover missing reusable evidence without pretending the defective historical pass was valid. Exact repair mechanics remain job-specific. |
| Step 4 | First post-Wordstat triage / cleanup preparation | **APPROVED / ACTIVE** | Family triage is not row-level cleanup; low frequency alone is not irrelevance; associations are not auto-accepted keywords. |
| Step 5 | Targeted second acquisition / expansion | **PARTIALLY DEFINED / NOT YET UNIVERSALLY VALIDATED** | Every probe needs information gain; avoid recursive acquisition and association/volume over-promotion. Fresh research required before material reuse. |
| Step 6 | Demand dynamics / seasonality evidence | **UNVALIDATED AS PERMANENT METHOD** | Current job has preserved evidence, but no owner-approved reusable method entry yet. Research before future execution/reuse. |
| Step 6A | Acquisition coverage revalidation | **UNVALIDATED AS PERMANENT METHOD** | Current job performed a coverage decision, but the reusable cross-job method has not yet been promoted. Research before future execution/reuse. |
| Step 7 | Row-level semantic cleanup | **APPROVED / ACTIVE AFTER CORRECTION** | No default KEEP; KEEP requires positive evidence; accounting QA != semantic QA; fix causes/classes, not only examples; uncertainty -> REVIEW. |
| Step 8 | Freeze Search-stage semantic set | **UNVALIDATED** | Must define what can enter Search and what unresolved rows remain blocked/deferred. Research before execution. |
| Step 9 | Ordinary Yandex Search/SERP validation | **UNVALIDATED** | Must research current Yandex/Search evidence methodology, query sampling/full-scope rules, preservation and page-boundary interpretation before execution. |
| Step 10 | User-task / SERP clustering | **UNVALIDATED** | Must establish how meaning, SERP compatibility and business compatibility combine; no automatic one-keyword-one-page logic. Research before execution. |
| Step 11 | Page ownership mapping | **UNVALIDATED** | Must define evidence required to map a cluster/task to an existing URL and when no current page is suitable. Research before execution. |
| Step 12 | Structural actions (keep/expand/split/merge/create) | **UNVALIDATED** | Must separate evidence-backed structural action from analyst preference. Research before execution. |
| Step 13 | Cannibalization diagnosis | **UNVALIDATED** | Must distinguish real competing-page conflict from normal multi-URL visibility. Research before execution. |
| Step 14 | Search-only architecture freeze | **UNVALIDATED** | Must define what evidence is sufficient to freeze the classic Search architecture before AI evidence. Research before execution. |
| Step 15 | AI-case selection | **UNVALIDATED** | Must select high-information uncertain cases rather than querying AI search indiscriminately. Research before execution. |
| Step 16 | AI-search evidence acquisition | **UNVALIDATED** | Must research current Alice/GenSearch/Webmaster capabilities, preserve complete evidence and separate model/search behaviour from classic SERP evidence. |
| Step 17 | Search-vs-AI comparison | **UNVALIDATED** | Must define comparable evidence units and avoid forcing agreement between two different retrieval surfaces. Research before execution. |
| Step 18 | Prioritization | **UNVALIDATED** | Must research/define how impact, evidence strength, business relevance, effort and uncertainty affect priority. |
| Step 19 | Client deliverables | **UNVALIDATED** | Must map analysis outputs to the sold deliverable and make evidence/uncertainty understandable to the client. |
| Step 20 | Final QA | **UNVALIDATED** | Must reconcile claims, counts, evidence, URLs/actions and unresolved items against the promised Kwork output. |
| Step 21 | Handoff / revisions | **UNVALIDATED** | Must define revision scope, evidence updates, version truth and acceptance boundaries. |
| Step 22 | Job close | **PARTIALLY DEFINED BY JOB_WORKSPACE_LIFECYCLE** | Close only after work, handoff/revisions and pending provider/operator actions are finished; then mark workspace safe to delete. |

---

# Required per-step detail

For any step marked `APPROVED / ACTIVE`, the permanent ledger entry must preserve:

```text
STEP PURPOSE
APPROVED METHOD
WHY THIS METHOD
METHOD ORIGIN / CURRENT EXTERNAL SUPPORT
KNOWN ERROR(S)
ROOT CAUSE
CORRECTED METHOD
NON-REPEAT CONTROLS
PASS GATE
STATUS
```

For a step marked `UNVALIDATED`, the absence of known errors does not mean the step is safe. It means:

```text
WE HAVE NOT YET EARNED A PERMANENT METHOD
```

The next use of that step requires current research first.

---

# How this index is used

Before every major step:

```text
1. locate current stage in STEP_RULES_INDEX.md;
2. if APPROVED -> read the detailed ledger entry, understand its causal lessons, then still perform fresh external step research;
3. if PARTIAL / UNVALIDATED -> do not invent/reuse a method mechanically; research the step from current sources and present the method to the owner;
4. read current-job evidence and scope;
5. explain relevant old errors + root causes + non-repeat controls;
6. wait for owner authorization;
7. execute only after the full gate passes.
```

Fresh research remains mandatory even for approved steps because provider/search behaviour and industry understanding can change.

---

Markers:

```text
KW001_STEP_RULES_INDEX_ACTIVE = true
KW001_ROADMAP_STAGE_NOT_EQUAL_VALIDATED_METHOD = true
KW001_APPROVED_STEP_STILL_REQUIRES_FRESH_RESEARCH = true
KW001_UNVALIDATED_STEP_REQUIRES_METHOD_RESEARCH = true
KW001_PERMANENT_PROMOTION_REQUIRES_OWNER_APPROVAL = true
```
