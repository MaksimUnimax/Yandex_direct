# OKNO_MSK — STEP 17 PRE-STEP METHOD / EVIDENCE REVIEW

Date: 2026-09-02  
Status: **METHOD RESEARCH COMPLETE / EXECUTION NOT STARTED / AWAITING OWNER AUTHORIZATION**

## 1. Whole KW-001 goal

Deliver an evidence-backed semantic/page architecture for ordinary Yandex Search plus selective generative-search evidence, then produce prioritized client-ready outputs without claiming GenSearch is consumer Alice and without making unsupported page decisions.

## 2. Full current roadmap

| Step | Meaning | Status |
|---|---|---|
| 0 | Scope/order freeze | ✅ COMPLETE |
| 1 | Existing-site/business discovery | ✅ COMPLETE |
| 2 | Wordstat acquisition plan | ✅ COMPLETE |
| 3 / 3R | Wordstat acquisition + durable repair | ✅ COMPLETE |
| 4 | Family triage | ✅ COMPLETE |
| 5 | Targeted Wordstat expansion | ✅ COMPLETE |
| 6 / 6A | Demand dynamics + coverage revalidation | ✅ COMPLETE / PRESERVED |
| 7 | Row-level semantic cleanup | ✅ COMPLETE AFTER CORRECTION |
| 8 | Search-stage semantic freeze | ✅ COMPLETE AFTER METHOD CORRECTION |
| 9 | Ordinary Yandex Search validation | ✅ COMPLETE AFTER CORRECTIONS |
| 10 | User-task / SERP clustering | ✅ COMPLETE / VERIFIED |
| 11 | Page ownership | ✅ COMPLETE AFTER AUDIT |
| 12 | Structural actions | ✅ COMPLETE AFTER CORRECTIONS |
| 13 | Cannibalization diagnosis | ✅ COMPLETE / BASE PUBLIC MODE |
| 14 / 14A | Search-only architecture freeze + current-site/topology revalidation | ✅ FINAL PASS |
| 15 V2 | AI-case selection / preregistration | ✅ FINAL PASS |
| 16 | Yandex GenSearch evidence acquisition | ✅ COMPLETE / POST-RUN CORRECTED / FINAL READBACK PASS |
| 17 | Search-vs-GenSearch comparison + bounded AI-derived architecture delta overlay | 🟡 PREPARED / EXECUTION NOT STARTED |
| 18 | Prioritization | ⬜ NOT STARTED |
| 19 | Client deliverables | ⬜ NOT STARTED |
| 20 | Final QA | ⬜ NOT STARTED |
| 21 | Handoff/revisions | ⬜ NOT STARTED |
| 22 | Job close | ⬜ NOT STARTED |

## 3. Completed work relevant to Step 17

- Step 14/14A froze the Search-only architecture after current-site discovery/topology correction.
- Step 15 V2 selected exactly eight diagnostic/control exact-query cases and froze ordinary-Search baselines and decision questions.
- Step 16 acquired 8 initial GenSearch observations plus one additional same-query short-window observation for C15-010: 9 provider calls, 45.72 RUB, 9 authoritative verbatim raw files, 100% raw readback.
- Post-run Step-16 correction superseded old final `DE_RISK / NO_CHANGE / CHANGE_CONFIRMED` semantics. Current Step-16 authority contains observations only.
- Evidence mode is `YANDEX_GENSEARCH_API_PROXY`; direct consumer Alice and Webmaster Alice visibility were not observed.
- Test scope is `EXACT_QUERY`, not user-job-family coverage.

## 4. Remaining work

1. Execute Step 17 comparison for all 8 selected cases.
2. Materialize any justified AI-derived delta overlay against the Step-14 Search-only architecture.
3. Step 18 prioritization.
4. Step 19 client deliverables.
5. Step 20 final QA.
6. Step 21 handoff/revision flow.
7. Step 22 job close.

## 5. Step-17 goal

For all eight frozen AI-tested exact queries, compare ordinary-Yandex Search evidence with corrected GenSearch evidence and current-page evidence, then decide the material decision delta:

```text
CHANGE
DE_RISK
NO_CHANGE
INSUFFICIENT
```

The comparison must identify what differs and whether the difference is strong enough to alter the frozen Search-only page/content responsibility.

## 6. Required output

For 8/8 cases preserve:

```text
case_id
authoritative_query
ordinary_search_baseline
ordinary_search_task
ordinary_search_content_type
ordinary_search_format
ordinary_search_angle
ordinary_search_specificity
gensearch_observation
gensearch_answer_mode
gensearch_refined_queries
used_source_pages
used_source_roles_validated
current_target_page_evidence
task_delta
commerciality_delta
specificity_delta
source_role_delta
materiality_reason
reproducibility_state
final_step17_verdict = CHANGE | DE_RISK | NO_CHANGE | INSUFFICIENT
architecture_delta_required
architecture_delta_overlay
claim_boundary
evidence_refs
qa_state
```

Also required: final comparison ledger, bounded Step-14 delta overlay, QA, report/current state and GitHub readback.

---

# 7. External method authorities checked before execution

Research checked: 2026-09-02.

### OFFICIAL — Yandex Search quality / user-task principle
https://yandex.ru/support/webmaster/ru/search-quality

Supports: Search is designed to give useful/relevant information so the user can solve a task; query/page evidence matters. Therefore `ordinary_search_task` must be described from actual saved Yandex results, not query wording alone.

### OFFICIAL — Yandex GenSearch API
https://aistudio.yandex.ru/ru/docs/search-api/api-ref/GenSearch/search

Supports provider observables `message`, `sources[].url/title/used`, `searchQueries[].text/reqId`. `used=true` means the document was used in the answer. No source importance/rank weight is exposed.

### OFFICIAL — how Alice AI forms answers
https://yandex.ru/support/webmaster/ru/alice

Supports source-order and variability boundaries: consumer-Alice source links are not ranked by displayed order; answer/source composition can vary; source pages should be expert/useful/original/substantive. This is consumer-Alice context only and is not evidence of GenSearch equivalence.

### OFFICIAL — Webmaster Alice visibility
https://yandex.ru/support/webmaster/ru/service/alice-answers

Supports that owned Alice visibility is a separate surface; Yandex recommends examining user questions, competitor landing pages and content solving the user task; answers/source sets can vary over time. In this job this evidence route is unavailable/not executed.

### INDUSTRY PRACTICE — SERP intent description
https://ahrefs.com/blog/search-intent/

Supports using dominant content type, format and angle as a practical description of observed SERP intent. This is not a Yandex standard.

### INDUSTRY CONTEXT — keep AI surfaces separate
https://ai-visibility-index.semrush.com/methodology

Supports keeping measurements for different AI platforms/surfaces separate rather than silently combining them.

### EXTERNAL EVAL PRACTICE — uncertainty / independent review
https://airc.nist.gov/airmf-resources/airmf/5-sec-core/

Supports documented test conditions, uncertainty, benchmarks/comparisons and independent review. NIST does not prescribe a specific SEO verdict taxonomy or repeat count.

---

# 8. Prior Step-16 failures carried causally into Step 17

## S16-M01 — reproducibility under-specified

Seven cases have one GenSearch run; C15-010 has two same-query observations in a short window.

Mandatory Step-17 rule:

```text
SINGLE_GENSEARCH_OBSERVATION != STABLE_BEHAVIOR
```

A **material AI-driven contradiction** to the frozen Search-only decision cannot receive `CHANGE` from one unreproduced GenSearch snapshot.

For this job:

```text
AI_DRIVEN_CHANGE
-> requires a materially relevant AI direction with sufficient reproduction for the claim being made
-> C15-010 has only bounded short-window reproduction
-> long-term stability is never claimed
```

If a single-run case produces a material AI-vs-Search contradiction, Step 17 returns `INSUFFICIENT` for an AI-driven architecture change unless the owner separately authorizes the evidence needed to test reproduction.

**Important upstream distinction:** independent non-AI evidence cannot be used as a substitute for reproducing an AI-driven contradiction. If direct current-page/Search evidence instead proves that the frozen Step-14 baseline itself is factually wrong/stale independent of GenSearch, that is not a Step-17 AI `CHANGE`. It is:

```text
UPSTREAM_BASELINE_CORRECTION_REQUIRED
-> STOP current case verdict
-> correct/re-freeze the affected upstream baseline
-> only then resume Search-vs-GenSearch comparison
```

This prevents Step 17 from hiding an upstream error inside an “AI changed the decision” label.

C15-010 allowed claim remains only:

`installation/how-to direction reproduced in two same-query observations in a short bounded window`.

## S16-M02 — exact-query evidence expanded into user-job-family claims

```text
TEST_SCOPE = EXACT_QUERY
```

No result may be generalized to every natural formulation of the broader user job.

## S16-M03 — GenSearch proxy boundary

```text
EVIDENCE_SURFACE = YANDEX_GENSEARCH_API_PROXY
GEN_SEARCH != CONSUMER_ALICE
GEN_SEARCH != WEBMASTER_ALICE_VISIBILITY
```

## S16-M04 — acquisition crossed into comparison

Old Step-16 `DE_RISK / NO_CHANGE / CHANGE_CONFIRMED` labels are historical only and forbidden as Step-17 verdict input.

---

# 9. Scope-boundary reconciliation

The original implementation plan separates Search-vs-AI comparison from final architecture, while the expanded OKNO_MSK roadmap already froze Search-only architecture at Step 14 and moves from Step 17 directly to Step 18 Prioritization.

Current job-specific boundary:

```text
STEP 14 = frozen Search-only architecture baseline
STEP 17 = compare Search vs GenSearch + create ONLY case-scoped AI-derived delta overlay where justified
STEP 17 != rebuild whole architecture
STEP 17 != prioritization
STEP 18 = prioritize the effective recommendations after Step-17 overlay
```

All non-CHANGE units inherit Step 14 unchanged. This mapping is `PROJECT_SPECIFIC_BUT_REASONED`.

---

# 10. Exact execution method

For each of the 8 cases:

### A — freeze inputs
Use only:

```text
STEP_15_SELECTED_CASES_V2.tsv
STEP_16_OBSERVATIONS_CORRECTED_V2_2026-09-02.json
Step-16 authoritative verbatim raw files
Step-14/14A accepted Search-only/current-site authorities
persisted ordinary Search evidence referenced by Step 15
```

### B — ordinary Search side
Describe exact-query task using saved Yandex results:

```text
task
content type
content format
content angle
commercial / transactional / informational / procedural / comparison orientation
specificity / taxonomy boundary
```

### C — GenSearch side
Describe from corrected/raw evidence:

```text
answer task/orientation
answer mode
refined queries
used=true sources
source specificity
```

Never infer source rank from order or source count.

### D — direct page-role validation when material

If a verdict depends on a used source being service/product/DIY/comparison/specialist/broad/etc., open/read the current page before using that role decisively. URL/title alone is a weak hint.

If a proposed delta depends on what the current OKNO_MSK target page actually contains, directly read the current page or use same-day authoritative evidence sufficient to prove the point.

If this direct check independently invalidates the Step-14 baseline, trigger `UPSTREAM_BASELINE_CORRECTION_REQUIRED`; do not disguise it as an AI-driven Step-17 change.

### E — compare fixed axes

```text
TASK: same / broader / narrower / different / mixed
COMMERCIALITY: more commercial / more explanatory / more procedural / more comparison-led / no material change
SPECIFICITY: same / broader / narrower / taxonomy shift / mixed
SOURCE ROLE: same / complementary / conflicting / unresolved
TARGET-SITE FIT: satisfies both / bounded expansion needed / role reconsideration needed / unresolved
```

### F — verdict

**CHANGE** — only when a material Search-vs-GenSearch difference changes frozen responsibility and all required evidence gates pass, including AI reproducibility when the change is AI-driven.

**DE_RISK** — compatible GenSearch evidence reduces uncertainty around the Search-only decision; does not prove long-term AI stability.

**NO_CHANGE** — wording/source/presentation differs but frozen responsibility/action does not materially change.

**INSUFFICIENT** — evidence cannot safely discriminate, including an unreproduced material AI-only contradiction.

### G — bounded architecture overlay

For `CHANGE` only:

```text
affected_step14_unit_or_page
baseline_search_only_state
proposed_ai_derived_delta
delta_reason
evidence_refs
confidence / limitation
global_coherence_recheck_required
```

No whole-site re-architecture in Step 17.

---

# 11. Fresh-request policy

Base plan:

```text
NEW PAID GENSEARCH CALLS = 0
NEW PAID ORDINARY SEARCH CALLS = 0
```

A fresh request is allowed only if a blocking evidence gap appears and the permanent research-to-execution gate is satisfied with exact question, insufficiency reason, operation/query, information gain, cost/retry/persistence, acceptance use and explicit owner authorization.

---

# 12. What Step 17 will NOT do

```text
no broad user-job prompt expansion
no site-wide Alice visibility measurement
no consumer-Alice claims
no silent new GenSearch sampling
no source ranking from source order/count
no full architecture rebuild
no hiding an upstream Step14 error as an AI change
no Step18 prioritization
no client deliverables
no final-project QA
```

---

# 13. PASS condition

```text
CASES_ACCOUNTED = 8/8
ORDINARY_SEARCH_BASELINE_ACCOUNTED = 8/8
CORRECTED_GENSEARCH_OBSERVATION_ACCOUNTED = 8/8
OLD_STEP16_FINAL_LABELS_USED_AS_VERDICT_INPUT = 0
MATERIAL_USED_SOURCE_ROLES_WITHOUT_DIRECT_VALIDATION = 0
MATERIAL_TARGET_PAGE_CLAIMS_WITHOUT_CURRENT_EVIDENCE = 0
SOURCE_ORDER_RANK_INFERENCES = 0
USED_SOURCE_COUNT_AS_RANK_INFERENCES = 0
CONSUMER_ALICE_EQUIVALENCE_CLAIMS = 0
USER_JOB_FAMILY_GENERALIZATIONS_FROM_EXACT_QUERY = 0
UNREPRODUCED_AI_ONLY_MATERIAL_CHANGE_VERDICTS = 0
UPSTREAM_BASELINE_DEFECTS_HIDDEN_AS_STEP17_CHANGE = 0
FINAL_VERDICT_PRESENT = 8/8
CHANGE_WITHOUT_EXPLICIT_DELTA_TRACE = 0
REVERSE_TRACE_MISSING = 0
UNAUTHORIZED_PROVIDER_CALLS = 0
INDEPENDENT_QA_BLOCKING_FINDINGS = 0
FINAL_GITHUB_READBACK = PASS
```

# 14. Ten-point pre-execution blocking check

All ten must be YES:

```text
1. Full roadmap/current-state truth loaded?
2. Step-15 V2 exact baseline loaded for all 8?
3. Step-16 corrected authority/raw lineage loaded for all 8?
4. Old Step-16 final labels excluded?
5. EXACT_QUERY boundary active?
6. GenSearch/consumer-Alice boundary active?
7. Direct source/target-page validation rule active?
8. Reproducibility gate active and upstream-baseline correction kept separate?
9. Step17 delta-overlay / Step18 prioritization boundary active?
10. No unapproved paid/provider calls planned?
```

Any `NO` -> `STEP17_EXECUTION = BLOCKED`.

## Method verdict

```text
STEP17_METHOD_REVIEW = PROJECT_SPECIFIC_BUT_REASONED
STEP17_EXTERNAL_RESEARCH_COMPLETE = true
STEP17_RESEARCH_TO_EXECUTION_SCHEMA_REQUIRED = true
STEP17_EXECUTION_STARTED = false
OWNER_AUTHORIZATION_REQUIRED = true
```
