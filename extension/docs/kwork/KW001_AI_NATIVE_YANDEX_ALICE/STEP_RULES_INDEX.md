# KW-001 — STEP RULES INDEX

Date: 2026-08-29  
Status: **ACTIVE / UNIVERSAL / OWNER-APPROVED / OWNER-LOCKED**

This file is the index of step-specific methodology coverage.

It does not replace detailed method files. It answers two questions before execution:

```text
1. Has this roadmap stage actually earned a validated permanent method?
2. Where is the canonical detailed method / lesson authority for it?
```

Canonical rules:

```text
ROADMAP_STAGE_EXISTS != METHODOLOGY_VALIDATED
RESEARCH_COLLECTED != METHOD_VALIDATED
```

Before executing a major step, ChatGPT must:

```text
read SOURCE_TO_METHOD_TRACEABILITY_GATE.md;
check this index;
read the listed canonical method/lesson authority;
then perform fresh current external research for the step.
```

If a material step is `UNVALIDATED` or has no sufficient detailed entry:

```text
CURRENT INTERNET METHOD RESEARCH = REQUIRED
SOURCE_TO_METHOD TRACE = REQUIRED
OWNER-FACING METHOD REVIEW = REQUIRED
EXECUTION = BLOCKED UNTIL THAT REVIEW IS COMPLETE
```

Permanent promotion requires explicit owner instruction.

---

# Current methodology coverage

| Stage | Purpose | Permanent methodology status | Canonical method / reusable lesson |
|---|---|---|---|
| Step 0 | Order / scope freeze | **APPROVED / ACTIVE** | `STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md` — freeze brief before evidence. |
| Step 1 | Existing-site discovery / business-page model | **APPROVED / ACTIVE** | `STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md` — one discovery pass is not automatically complete; cross-check channels and preserve evidence strength. |
| Step 2 | Seed / acquisition probe plan | **APPROVED / ACTIVE** | `STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md` — seed is an acquisition probe, not a final keyword/page target. |
| Step 3 | Wordstat/provider acquisition | **APPROVED / ACTIVE** | `STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md` — provider/API success is not collection completion; complete returned evidence must be preserved and verified before advancing. |
| Step 3R | Repair of incomplete Step-3 acquisition | **JOB-SPECIFIC RECOVERY PATTERN / GOVERNED BY STEP 3** | Step-3 permanent rules + current-job repair evidence. |
| Step 4 | First post-Wordstat triage / cleanup preparation | **APPROVED / ACTIVE** | `STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md` — family triage is not row-level cleanup; low frequency alone is not irrelevance; associations are not auto-accepted. |
| Step 5 | Targeted second acquisition / expansion | **PARTIALLY DEFINED / NOT YET UNIVERSALLY VALIDATED** | `STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md` — every probe needs information gain; fresh research required before material reuse. |
| Step 6 | Demand dynamics / seasonality evidence | **UNVALIDATED AS PERMANENT METHOD** | Research before future execution/reuse. |
| Step 6A | Acquisition coverage revalidation | **UNVALIDATED AS PERMANENT METHOD** | Research before future execution/reuse. |
| Step 7 | Row-level semantic cleanup | **APPROVED / ACTIVE AFTER CORRECTION** | `STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md` — no default KEEP; KEEP requires positive evidence; accounting QA != semantic QA; fix causes/classes; uncertainty -> REVIEW. |
| **Step 8** | **Freeze Search-stage semantic set** | **APPROVED / ACTIVE AFTER METHOD CORRECTION** | **`STEP_08_SEARCH_STAGE_FREEZE_METHOD.md`** — only executable routes; no `REVIEW_BUSINESS`/`REVIEW_SEARCH_AND_BUSINESS` without a real independent evidence source; internal priority is not a semantic route; source-to-method trace required. |
| Step 9 | Ordinary Yandex Search/SERP validation | **UNVALIDATED** | Must research current Yandex/Search evidence methodology, query sampling/full-scope rules, preservation and page-boundary interpretation before execution. |
| Step 10 | User-task / SERP clustering | **UNVALIDATED** | Must establish how meaning, SERP compatibility and business compatibility combine; no automatic one-keyword-one-page logic. |
| Step 11 | Page ownership mapping | **UNVALIDATED** | Must define evidence required to map a cluster/task to an existing URL and when no current page is suitable. |
| Step 12 | Structural actions (keep/expand/split/merge/create) | **UNVALIDATED** | Must separate evidence-backed structural action from analyst preference. |
| Step 13 | Cannibalization diagnosis | **UNVALIDATED** | Must distinguish real competing-page conflict from normal multi-URL visibility. |
| Step 14 | Search-only architecture freeze | **UNVALIDATED** | Must define what evidence is sufficient to freeze classic Search architecture before AI evidence. |
| Step 15 | AI-case selection | **UNVALIDATED** | Must select high-information uncertain cases rather than querying AI search indiscriminately. |
| Step 16 | AI-search evidence acquisition | **UNVALIDATED** | Must research current Alice/GenSearch/Webmaster capabilities, preserve complete evidence and separate model/search behaviour from classic SERP evidence. |
| Step 17 | Search-vs-AI comparison | **UNVALIDATED** | Must define comparable evidence units and avoid forcing agreement between different retrieval surfaces. |
| Step 18 | Prioritization | **UNVALIDATED** | Must research/define how impact, evidence strength, public business relevance, internal client constraints, effort and uncertainty affect priority. |
| Step 19 | Client deliverables | **UNVALIDATED** | Must map analysis outputs to the sold deliverable and make evidence/uncertainty understandable to the client. |
| Step 20 | Final QA | **UNVALIDATED** | Must reconcile claims, counts, evidence, URLs/actions and unresolved items against the promised Kwork output. |
| Step 21 | Handoff / revisions | **UNVALIDATED** | Must define revision scope, evidence updates, version truth and acceptance boundaries. |
| Step 22 | Job close | **PARTIALLY DEFINED BY JOB_WORKSPACE_LIFECYCLE** | Close only after work, handoff/revisions and pending provider/operator actions are finished; then mark workspace safe to delete. |

---

# Required per-step detail

For any step marked `APPROVED / ACTIVE`, its canonical method authority must preserve:

```text
STEP PURPOSE
APPROVED METHOD
WHY THIS METHOD
METHOD ORIGIN / DIRECT SOURCES
SOURCE-TO-METHOD TRACE
KNOWN ERROR(S)
ROOT CAUSE
CORRECTED METHOD
NON-REPEAT CONTROLS
PASS GATE
STATUS
```

For a step marked `UNVALIDATED`, absence of known errors means only:

```text
WE HAVE NOT YET EARNED A PERMANENT METHOD
```

The next use requires fresh current research first.

---

# How this index is used

Before every major step:

```text
1. read SOURCE_TO_METHOD_TRACEABILITY_GATE.md;
2. locate current stage in STEP_RULES_INDEX.md;
3. if APPROVED -> read the listed canonical method, understand causal lessons, then still perform fresh external research;
4. if PARTIAL / UNVALIDATED -> do not infer/replay a method; research the step from current sources;
5. build a source-to-method trace for every material state/rule/route/threshold;
6. remove any unsupported/non-executable method element;
7. read current-job evidence and scope;
8. explain old errors + root causes + non-repeat controls;
9. wait for owner authorization;
10. execute only after the full gate passes.
```

Fresh research remains mandatory even for approved steps because provider/search behaviour and industry understanding can change.

---

# Step-8 permanent lesson summary

The Step-8 correction established:

```text
business relevance/potential = evaluation dimension
internal business priority = client/internal constraint
Search/SERP = observable evidence source

therefore:
EVALUATION_DIMENSION != EVIDENCE_ROUTE
```

A prior method invented `REVIEW_BUSINESS` and `REVIEW_SEARCH_AND_BUSINESS` after collecting external sources that did not support those routes. The permanent non-repeat control is `SOURCE_TO_METHOD_TRACEABILITY_GATE.md`.

Direct sources used in that correction:

- https://yandex.ru/support/webmaster/ru/recommendations/targeting
- https://yandex.ru/support/webmaster/ru/service/queries-selection
- https://www.yandex.ru/support/webmaster/ru/service/search-queries
- https://ahrefs.com/blog/keyword-intent/
- https://ahrefs.com/blog/keyword-strategy/
- https://www.semrush.com/blog/keyword-clustering/
- https://www.semrush.com/blog/keyword-mapping/

---

Markers:

```text
KW001_STEP_RULES_INDEX_ACTIVE = true
KW001_ROADMAP_STAGE_NOT_EQUAL_VALIDATED_METHOD = true
KW001_RESEARCH_COLLECTED_NOT_EQUAL_METHOD_VALIDATED = true
KW001_SOURCE_TO_METHOD_TRACEABILITY_REQUIRED = true
KW001_APPROVED_STEP_STILL_REQUIRES_FRESH_RESEARCH = true
KW001_UNVALIDATED_STEP_REQUIRES_METHOD_RESEARCH = true
KW001_STEP8_METHOD_APPROVED_AFTER_CORRECTION = true
KW001_PERMANENT_PROMOTION_REQUIRES_OWNER_APPROVAL = true
```