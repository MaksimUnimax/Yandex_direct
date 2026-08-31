# Step 13 — pre-step methodology research and review

Date: 2026-08-31  
Status: **PRE-STEP METHOD RESEARCH COMPLETE / OWNER-FACING REVIEW REQUIRED BEFORE EXECUTION**

Job: `OKNO_MSK`  
Step: 13 — cannibalization / competing-page diagnosis

## WHOLE KWORK GOAL

Produce an evidence-based semantic/page architecture for `okno-msk.ru` for ordinary Yandex Search, then selectively compare materially uncertain cases with AI-search evidence and deliver prioritized client-facing recommendations. The frozen base rehearsal excludes Webmaster, Metrika and Direct account access.

## COMPLETED WORK

Steps 0–12 are complete under current accepted job evidence. Step 12 ended with:

```text
SOURCE_ACTIVE_PHRASES = 2332
FINAL_PHRASE_ACTION_ROWS = 2332
FINAL_STRUCTURAL_UNITS = 168
STEP13_CANDIDATE_PAIRS = 195
PAIRS_MARKED_FOR_STEP13 = 186
STEP13_DEPENDENCY_UNITS = 98
NEW_PAGE_ACTIONS = 0
STEP13_EXECUTED = false
```

Step-12 D12-28..D12-30 corrections are durably closed and the final Step-12 execution protocol is registered in `STEP_RULES_INDEX.md`.

## REMAINING WORK

```text
13. Cannibalization / competing-page diagnosis
14. Search-only architecture freeze
15. AI-case selection
16. Selected AI-search evidence
17. Search-vs-AI comparison
18. Prioritization
19. Client deliverables
20. Final QA
21. Handoff/revisions
22. Job close
```

## CURRENT STEP GOAL

Determine which Step-12 candidate URL relationships are:

```text
NORMAL / INTENDED MULTI-PAGE STRUCTURE
vs
SEARCH-OWNERSHIP CONFLICT SIGNAL
vs
PROBABLE CANNIBALIZATION / DUPLICATE CONFLICT
vs
EVIDENCE INSUFFICIENT
```

without treating two related URLs or one target/relevant mismatch as proof of harmful cannibalization.

## WHAT THIS STEP SOLVES

Step 12 deliberately produced a broad candidate-pair handoff. It did not prove that those URLs compete. Step 13 must determine whether the same query family / user intent is being served by multiple pages in a way that causes unstable or conflicting Search ownership and whether any structural remediation is justified.

## REQUIRED OUTPUT

At the end of Step 13, the job must contain at minimum:

```text
STEP_13_PAIR_ELIGIBILITY.tsv
STEP_13_QUERY_FAMILY_CASES.tsv
STEP_13_CURRENT_PAGE_EVIDENCE.tsv
STEP_13_EXISTING_SEARCH_EVIDENCE.tsv
STEP_13_SEARCH_MANIFEST.tsv              # only if fresh Search is actually required
STEP_13_SEARCH_RESULTS.tsv               # only if provider executed
STEP_13_CONFLICT_DIAGNOSIS.tsv
STEP_13_REMEDIATION_RECOMMENDATIONS.tsv
STEP_13_QA.json
STEP_13_QA_FINDINGS.tsv
STEP_13_REPORT.md
STEP_13_ACCEPTANCE_2026-08-31.md
```

All 195 input pair IDs must be accounted for, either directly or through an explicitly materialized query-family / URL-set case that references them.

## RELEVANT PRIOR ERRORS / CORRECTIONS

Freshly re-read `STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md` and Step-12 permanent controls.

Relevant failures:

1. **Candidate relationship was previously at risk of being read as a verdict.** Step 12 must hand off pair candidates; Step 13 makes the diagnosis.
2. **Historical source-cluster / graph adjacency is not evidence of same Search responsibility.** A broad upstream cluster can legitimately split into different user tasks.
3. **Action/verdict cannot prove itself.** The same logic that proposes a conflict may not generate the only evidence accepted by the verifier.
4. **Known-regression zero is not global QA.** Every pair/case in the declared Step-13 universe must be accounted for.
5. **Target URL != relevant URL is a signal, not automatic cannibalization.** Search engines can legitimately select a different page; diagnosis needs query intent, current page roles and, for strong claims, repeated/historical or performance evidence.
6. **One Search snapshot cannot prove historical rank swapping or performance harm.**

## WHAT FAILED BEFORE

The recurring cross-step failure pattern was promoting an internally derived relationship/state into evidence:

```text
GRAPH / CLUSTER / TARGET ASSIGNMENT
→ SUSPECTED CONFLICT
→ VERIFIER CHECKS THE SAME DERIVED STATE
→ FALSE CERTAINTY
```

Step 13 must instead use current pages + exact query responsibility + observed Search evidence as causally upstream evidence.

## NON-REPEAT CONTROL FOR THIS STEP

```text
PAIR CANDIDATE
→ CURRENT TASK / PAGE EVIDENCE
→ QUERY-FAMILY ELIGIBILITY
→ REUSE EXISTING SEARCH EVIDENCE
→ FRESH SEARCH ONLY IF MATERIAL GAP SURVIVES
→ EVIDENCE-STRENGTH VERDICT
→ REMEDIATION ONLY AFTER VERDICT
→ INDEPENDENT RECOMPUTATION
→ DURABLE READBACK
```

The final verifier must be able to close cases as normal and reject proposed conflict/remediation.

## INPUT EVIDENCE

Primary current-job inputs:

- `STEP_12_STEP13_CANDIDATE_PAIRS_V6.tsv` — 195 broad pair candidates;
- `STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V6.tsv` — final structural unit/page roles;
- `STEP_12_PHRASE_ACTION_MAP_FINAL_V6.tsv` — 2332 phrase-level current assignments;
- `STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V7.tsv` — current structural membership;
- persisted Step-9/Step-11 ordinary Search results and decisions;
- current public first-party pages;
- current frozen job scope.

## METHOD ORIGIN

### Official Yandex evidence

1. Yandex Webmaster duplicate-page documentation states that duplicates may be grouped, the wrong page can remain in Search, and in some cases similar documents can participate separately and compete.
   - https://yandex.ru/support/webmaster/ru/robot-workings/double
   - https://yandex.ru/support/webmaster/ru/yandex-indexing/about-doubles

2. Yandex extended query analytics by URL exposes the ideal historical evidence unit:

```text
DATE
HOST
URL
QUERY
REGION
CLICKS
IMPRESSIONS
POSITION
```

   - https://yandex.ru/support/webmaster/ru/service/queries-export
   - https://yandex.ru/dev/webmaster/doc/ru/reference/enhanced-export

3. Yandex query monitoring groups statistics by query and URL and exposes impressions/clicks/position/CTR.
   - https://yandex.ru/support/webmaster/ru/service/popular-queries
   - https://yandex.ru/support/webmaster/ru/service/queries-analytic

4. Yandex explains that when a different site page appears for a query, the algorithm chooses based on relevance; another page appearing is not by itself proof of a defect.
   - https://yandex.ru/support/webmaster/ru/yandex-indexing/site-indexing

### Current industry methodology

Semrush, 2026-07-14:
- cannibalization means multiple pages target the same keyword(s) and **harm** each other's search visibility;
- multiple pages ranking for one keyword does not always mean cannibalization;
- multiple URLs earning impressions/clicks is a potential signal; pages must then be manually checked for overlapping search intent;
- remediation depends on circumstances: redirect true redundant pages, canonicalize duplicate variants, differentiate useful pages, use noindex only selectively/last-resort.
- https://www.semrush.com/blog/keyword-cannibalization-guide/

Ahrefs, 2026-08:
- strong cannibalization scenario = pages target the same keyword **and same intent** and either ranking swaps repeatedly or multiple similar pages rank simultaneously and are similar enough to consolidate;
- mixed-intent pages can legitimately coexist;
- history matters.
- https://ahrefs.com/blog/how-to-increase-organic-traffic/
- https://ahrefs.com/blog/keyword-intent/

Ahrefs cannibalization methodology also emphasizes that a real issue ultimately means the multiple pages hurt overall organic performance; same-keyword overlap alone is not sufficient.
- https://ahrefs.com/blog/keyword-cannibalization/

Topvisor, updated 2026:
- `target URL` is the intended page;
- `relevant URL` is the page actually ranking / considered relevant by the search engine;
- target/relevant mismatch and **history of relevant URL changes** are useful diagnostics.
- https://topvisor.com/ru/support/rankings/target-url/

## SOURCE-TO-METHOD CONCLUSION

The correct primary analysis object is not merely `PAGE_A × PAGE_B`.

Use:

```text
QUERY FAMILY
×
CANDIDATE URL SET
```

The Step-12 pair ledger remains a discovery graph and accounting universe.

## HOW WE WILL DO IT

### Stage 1 — freeze the 195-pair universe

No pair disappears. Every pair receives a Step-13 eligibility disposition or maps to a query-family case that preserves the originating pair IDs.

### Stage 2 — deduplicate current-page reads by URL

Build the unique URL set from all pairs. Re-read each material current URL once under `CURRENT_SITE_FRESHNESS_AND_EXISTENCE_GATE.md`; reuse that page evidence across all pairs that contain the URL.

Do not perform 195×2 duplicate page reads.

### Stage 3 — pair eligibility before paid Search

For each pair compare:

```text
PAGE A PRIMARY TASK / OBJECT / INTENT
PAGE B PRIMARY TASK / OBJECT / INTENT
EXACT MEMBER PHRASES / QUERY RESPONSIBILITY
PARENT-CHILD OR PRIMARY-SUPPORTING RELATION
CURRENT CONTENT DIFFERENTIATION
```

Ask:

```text
COULD THE SAME REAL QUERY FAMILY REASONABLY EXPECT BOTH URLS
AS ALTERNATIVE PRIMARY ANSWERS TO THE SAME / VERY SIMILAR INTENT?
```

If NO, close without provider Search as one of:

```text
NORMAL_DISTINCT_INTENT
NORMAL_DISTINCT_OBJECT
NORMAL_PARENT_CHILD
NORMAL_PRIMARY_SUPPORTING
NORMAL_MIXED_INTENT_DIVERSIFICATION
```

### Stage 4 — materialize query-family cases for surviving pairs

Pairs that survive eligibility are grouped into query-family × URL-set cases so the same underlying conflict is not investigated repeatedly through many pair combinations.

Each case preserves all source pair IDs and representative/member queries.

### Stage 5 — reuse existing Search evidence first

Join persisted Step-9/Step-11 ordinary Yandex Search evidence before any new provider call.

Materialize:

```text
INTENDED_URL
OBSERVED_YANDEX_URLS
TARGET_RELEVANT_MATCH_STATE
OBSERVED_RANKS
OBSERVED_QUERY
EVIDENCE_DATE
```

A mismatch is a signal, not a verdict.

### Stage 6 — decide whether fresh Search is necessary

Fresh ordinary Yandex Search is allowed only for a named surviving material case where current/persisted evidence cannot resolve Search ownership.

No Search request is issued merely because `later_direct_search_check_needed=true` in Step 12.

### Stage 7 — fresh ordinary Search, if authorized and required

Use Yandex Marketing Bridge ordinary `search` / `search_batch`; **do not use GenSearch** in Step 13.

The bounded objective is the same accepted ordinary-Search result contract used in Step 9: preserve the complete returned ranked result page for every selected query, not representative examples.

For each query preserve target-domain hits, ranks, URLs, titles/snippets where returned, request identity and cost.

### Stage 8 — evidence-strength verdict

Allowed verdict classes for this base rehearsal:

```text
NORMAL_DISTINCT_INTENT
NORMAL_DISTINCT_OBJECT
NORMAL_HIERARCHICAL_OR_SUPPORTING
NORMAL_MIXED_INTENT
NO_CURRENT_MULTI_URL_CONFLICT_OBSERVED
TARGET_RELEVANT_URL_MISMATCH_SIGNAL
MULTI_URL_VISIBILITY_SIGNAL
PROBABLE_SEARCH_OWNERSHIP_CONFLICT
TRUE_DUPLICATE_OR_NEAR_DUPLICATE_CONFLICT
EVIDENCE_INSUFFICIENT_FOR_CANNIBALIZATION
```

`CONFIRMED_HARMFUL_CANNIBALIZATION` is **not available in this base rehearsal from one public SERP snapshot alone**.

It requires adequate historical/performance evidence such as Yandex Webmaster query×URL data, ranking history or equivalent evidence capable of demonstrating repeated conflict/harm.

### Stage 9 — remediation only after verdict

Possible recommendations:

```text
KEEP_BOTH_NO_ACTION
KEEP_BOTH_DIFFERENTIATE_RESPONSIBILITY
CLARIFY_INTERNAL_LINK_SIGNALING
REASSIGN_QUERY_OWNER / ON-PAGE FOCUS
CONSOLIDATION_CANDIDATE
REDIRECT_DUPLICATE_CANDIDATE
CANONICAL_DUPLICATE_CANDIDATE
DEFER_FOR_WEBMASTER_OR_HISTORY
```

Rules:

- no automatic MERGE from keyword overlap;
- no automatic redirect/noindex from one public Search snapshot;
- canonical/redirect is reserved for true duplicate/near-duplicate situations with appropriate evidence;
- useful pages with distinct intent remain separate;
- destructive actions remain recommendations pending sufficient current value/performance evidence.

### Stage 10 — independent QA and durable readback

Independent QA must recompute:

```text
195/195 input pair accounting
pair→case mapping
normal-relationship closures
surviving case eligibility
provider manifest/result accounting if Search executed
verdict evidence-strength consistency
no strong verdict from one snapshot
no destructive remediation without qualifying evidence
no Step-14 execution
```

Persist diagnostics before final gate, read back from GitHub, then close Step 13.

## SELF-AUDIT FINDINGS

1. The 195-pair Step-12 universe is intentionally overinclusive. Rows such as homepage vs specific family or aluminium general vs distinct accessory/door tasks demonstrate why shared upstream cluster provenance cannot be used as conflict proof.
2. Step 13 must reduce repeated pair combinations into query-family cases before Search acquisition, or provider work will be wasteful and methodologically biased toward finding conflicts.
3. The base rehearsal has no Webmaster/Metrika account access. Therefore public Search can prove current selection/multi-URL signals but cannot prove performance harm over time.
4. The strongest Yandex-native historical method would use Webmaster extended URL-query analytics, but that capability is not available in the current job scope.
5. Step 13 must preserve uncertainty rather than relabel a weak signal as confirmed cannibalization.

## RISKS / UNCERTAINTIES

- current public Search is a snapshot and rankings are not constant;
- personalized/region/device differences can alter observed ranking;
- a page can rank for many long-tail queries, so same-head-query overlap can coexist with distinct value;
- current Step-12 pair derivation includes historical/shared-cluster routes that are discovery aids, not conflict evidence;
- some relevant current page content may have changed since earlier reads, requiring freshness checks;
- no private performance data means some cases will necessarily end as `EVIDENCE_INSUFFICIENT_FOR_CANNIBALIZATION` or `PROBABLE_SEARCH_OWNERSHIP_CONFLICT`, not confirmed harm.

## WHAT WE WILL NOT DO YET

```text
NO GenSearch / Alice calls
NO Step 14 architecture freeze
NO automatic MERGE/REDIRECT/NOINDEX from keyword overlap
NO confirmed harmful-cannibalization claim from one SERP snapshot
NO fresh Search for all 186 flagged pairs by default
NO Webmaster/Metrika claims without account access
```

## YMB BLOCK — REQUIRED BEFORE ANY STEP-13 PROVIDER CALL

```text
YMB STEP OBJECTIVE
= collect complete ordinary Yandex Search evidence only for surviving material query-family cases whose ownership remains unresolved after current-page and persisted-evidence review.

YMB REQUIRED MODE
= service SEARCH; ordinary search/search_batch only; no GenSearch; Moscow region/job configuration consistent with accepted Step-9 Search evidence.

YMB REQUIRED SAVED RESULT
= for every selected query, the complete bounded ordinary-Search result page returned by the accepted Step-9 contract, plus request ID/outcome/cost and normalized target-domain hit URL/rank evidence.

YMB COMPLETENESS CHECK
= planned queries == provider outcomes accounted; every executed successful query has the complete returned ranked rows saved; returned/saved normalized counts reconcile; request IDs/outcome/cost are preserved; result is readable from GitHub before the next provider batch/action.

YMB STOP CONDITION
= if any current provider result is incomplete, unsaved, unreadable, OUTCOME_UNKNOWN without accepted recovery truth, or row counts do not reconcile, STOP; do not issue the next YMB action.

YMB_INTERACTION_GATE_EMBEDDED = true
YMB_PROJECT_RESULT_DEFINED = true
YMB_REQUIRED_STORAGE_DEFINED = true
YMB_COMPLETENESS_CHECK_DEFINED = true
YMB_STOP_ON_INCOMPLETE_RESULT = true
```

## PROPOSED PASS GATE

Step 13 may pass only when:

```text
INPUT_PAIR_ROWS = 195/195 ACCOUNTED
SILENT_PAIR_DROPS = 0
ALL MATERIAL PAIRS HAVE CURRENT PAGE/TASK EVIDENCE
ALL SURVIVING PAIRS MAP TO EXPLICIT QUERY-FAMILY CASES
NORMAL_RELATIONSHIPS ARE CLOSED WITHOUT UNNECESSARY SEARCH
EXISTING SEARCH EVIDENCE IS REUSED BEFORE FRESH SEARCH
IF SEARCH EXECUTED: PLANNED/EXECUTED/RETURNED/SAVED/VERIFIED COUNTS RECONCILE
STRONG_VERDICT_FROM_ONE_SNAPSHOT = 0
DESTRUCTIVE_REMEDIATION_WITHOUT_QUALIFYING_EVIDENCE = 0
EVERY VERDICT HAS CAUSALLY UPSTREAM EVIDENCE
INDEPENDENT_QA_FINDINGS = 0
FINAL_GITHUB_READBACK = PASS
STEP14_EXECUTED = false
```

## REVIEW VERDICT

```text
HIGH-LEVEL METHOD = SUPPORTED
EVIDENCE-STRENGTH / VERDICT TAXONOMY = PROJECT_SPECIFIC_BUT_REASONED
CURRENT STEP-13 PERMANENT UNIVERSAL METHOD = UNVALIDATED / NOT PROMOTED
PROVIDER EXECUTION = BLOCKED UNTIL EXPLICIT OWNER AUTHORIZATION AFTER THIS REVIEW
```
