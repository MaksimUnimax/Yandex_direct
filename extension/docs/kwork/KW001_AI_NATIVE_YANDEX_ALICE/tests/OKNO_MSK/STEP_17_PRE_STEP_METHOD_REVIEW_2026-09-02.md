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

## 4. Remaining work after this pre-step

1. Execute Step 17 comparison for all 8 selected cases.
2. Materialize any justified AI-derived delta overlay against the Step-14 Search-only architecture.
3. Step 18 prioritization.
4. Step 19 client deliverables.
5. Step 20 final QA.
6. Step 21 handoff/revision flow.
7. Step 22 job close.

## 5. Step-17 goal

For all eight frozen AI-tested exact queries, compare the ordinary-Yandex Search evidence with corrected GenSearch evidence and current-page evidence, then decide the **material decision delta**:

```text
CHANGE
DE_RISK
NO_CHANGE
INSUFFICIENT
```

The comparison must identify what differs and whether the difference is strong enough to alter the already frozen Search-only page/content responsibility.

## 6. What Step 17 solves

Step 17 closes the question:

```text
DID THE GENSEARCH OBSERVATION MATERIALLY CHANGE OR DE-RISK
THE SEARCH-ONLY DECISION FOR THIS EXACT QUERY?
```

It must distinguish:

- difference in wording/presentation only;
- difference in user task;
- difference in commercial vs explanatory/procedural/comparison role;
- difference in specificity/taxonomy;
- different source-page role;
- a real architecture/content-role consequence;
- unresolved evidence where no decision is justified.

## 7. Required Step-17 output

For 8/8 cases preserve at minimum:

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

Step 17 must also produce one final comparison ledger, QA, current state, and a bounded delta overlay against Step 14 where justified.

---

# 8. Method authorities checked before execution

Research checked on 2026-09-02.

## OFFICIAL — Yandex Search quality / user-task principle

https://yandex.ru/support/webmaster/ru/search-quality

Supports:

- Yandex Search aims to provide full, useful and relevant information so the user can solve the task quickly.
- Search analyzes the query, page content and other signals.
- Page/search usefulness is tied to solving the user task.

Execution consequence:

`ordinary_search_task` must be inferred from actual saved Yandex Search evidence, not from keyword wording alone.

## OFFICIAL — Yandex GenSearch API response semantics

https://aistudio.yandex.ru/ru/docs/search-api/api-ref/GenSearch/search

Supports provider-native observables:

```text
message
sources[].url/title/used
searchQueries[].text/reqId
```

Execution consequence:

- `used=true` means the document was used in the answer.
- `searchQueries[]` are YandexGPT-refined queries used for the generative response.
- The API does not expose a source importance/ranking weight.

## OFFICIAL — how Alice AI forms answers / source semantics

https://yandex.ru/support/webmaster/ru/alice

Supports:

- generated answers are based on search-selected content;
- source links differ from classic Search in number/order;
- Alice does not rank source links by their displayed order;
- answer/source composition can vary over time;
- source pages should be expert, useful, original and substantive.

This is consumer-Alice context, not proof that GenSearch is identical. It is used only for claim/source-order boundaries and content-quality context.

## OFFICIAL — Webmaster Alice visibility

https://yandex.ru/support/webmaster/ru/service/alice-answers

Supports:

- real owned Alice visibility is a separate Webmaster surface;
- Yandex recommends comparing queries, competitor landing pages and content that solves user tasks;
- answers/source sets may vary over time.

Current-job consequence:

`WEBMASTER_ALICE_VISIBILITY = UNAVAILABLE_NOT_EXECUTED`; Step 17 cannot claim real owned Alice visibility.

## INDUSTRY PRACTICE — SERP intent analysis by page type/format/angle

https://ahrefs.com/blog/search-intent/

Supports a practitioner method of reading the dominant top-result:

```text
content type
content format
content angle
```

This is not a Yandex standard. It is a practical structure for describing what the already saved Yandex results are doing.

## INDUSTRY CONTEXT — AI platform results should not be silently aggregated

https://ai-visibility-index.semrush.com/methodology

Supports keeping AI-platform measurements separate where behavior differs rather than collapsing them into one generic AI score.

Current-job consequence:

GenSearch evidence remains GenSearch-specific; it is not merged with unobserved consumer Alice evidence.

## EXTERNAL EVAL PRACTICE — uncertainty and independent review

https://airc.nist.gov/airmf-resources/airmf/5-sec-core/

Supports documenting test conditions, uncertainty, benchmark/comparison conditions, reporting and independent review.

Current-job consequence:

A single stochastic observation cannot silently become a claim of stable behavior, and Step-17 QA must challenge its own conclusions.

---

# 9. Prior failures carried causally into Step 17

## S16-M01 — reproducibility under-specified

What failed: seven cases have one GenSearch run; C15-010 has two same-query observations in a short window.

Why: the earlier method did not pre-register claim strength vs repeat evidence.

Step-17 control:

```text
single GenSearch observation
!=
stable behavior
```

A **material AI-driven contradiction** to the frozen Search architecture cannot receive final `CHANGE` from one unreproduced GenSearch snapshot alone. It becomes `INSUFFICIENT` for an architecture-changing AI claim unless a qualifying independent evidence route already resolves the same issue. Any new paid repeat requires separate information-gain justification and owner authorization.

C15-010 may use only the bounded claim:

`installation/how-to direction reproduced in two same-query observations in a short window`.

## S16-M02 — exact-query evidence expanded into user-job-family claims

Step-17 control:

```text
TEST_SCOPE = EXACT_QUERY
```

All task descriptions are scoped to the exact tested wording/evidence. No statement may generalize to every natural formulation of the user job.

## S16-M03 — GenSearch proxy boundary was not fully enforced

Step-17 control:

```text
EVIDENCE_SURFACE = YANDEX_GENSEARCH_API_PROXY
GEN_SEARCH != CONSUMER_ALICE
GEN_SEARCH != WEBMASTER_ALICE_VISIBILITY
```

## S16-M04 — acquisition crossed into comparison

Step-17 control:

Old Step-16 `DE_RISK / NO_CHANGE / CHANGE_CONFIRMED` labels are historical only and must not be used as Step-17 input verdicts. Step 17 reassesses from Step-15 Search baseline + Step-16 corrected observations/raw.

---

# 10. Scope-boundary reconciliation before execution

A potential conflict was found during this pre-step review:

- the original commercial implementation plan separates `Search-vs-AI comparison` from `final semantic/page architecture`;
- the expanded OKNO_MSK job roadmap already froze a Search-only architecture in Step 14 and has no separate post-Step17 architecture stage before Step18 Prioritization.

Resolved job-specific boundary:

```text
STEP 14 = frozen Search-only architecture baseline
STEP 17 = compare Search vs GenSearch + create ONLY AI-DERIVED DELTA OVERLAY where justified
STEP 17 != rebuild the entire architecture
STEP 17 != prioritization
STEP 18 = prioritize the effective recommendations after the Step-17 overlay
```

Therefore Step 17 may modify the effective architecture **only through an explicit case-scoped delta overlay**. Every unchanged unit inherits Step 14 unchanged.

This mapping is `PROJECT_SPECIFIC_BUT_REASONED`, not an external industry standard.

---

# 11. Exact comparison method

For each of the eight cases:

## Phase A — freeze evidence inputs

Use only current authorities:

```text
STEP_15_SELECTED_CASES_V2.tsv
STEP_16_OBSERVATIONS_CORRECTED_V2_2026-09-02.json
authoritative Step-16 raw verbatim files
Step-14/14A current Search-only architecture/current-site authorities
persisted ordinary Search evidence referenced by Step 15
```

Old Step-16 final labels are forbidden input.

## Phase B — describe ordinary Search task

From persisted Yandex Search evidence identify:

```text
user task for this exact query
dominant content type
dominant format
dominant angle
commercial / transactional / informational / procedural / comparison orientation
specificity / taxonomy boundary
```

Do not infer from query wording alone when saved Search evidence exists.

## Phase C — describe GenSearch task

From corrected Step-16 raw/observation evidence identify:

```text
answer task/orientation
answer mode: explanatory / procedural / comparison / commercial-support / mixed
refined queries
used=true sources
source specificity
```

Never infer source rank from array order or used-source count.

## Phase D — directly validate page roles where material

If a verdict depends on a `used=true` source being DIY, service, product, category, comparison, specialist, broad, etc.:

```text
open/read current page
-> preserve direct page-role evidence
-> only then use that role decisively
```

URL/title alone remains weak descriptive evidence.

Likewise, if a proposed delta depends on what the current OKNO_MSK target page actually contains, directly read the current page or use a same-day authoritative current-page artifact sufficient to prove the point.

## Phase E — compare fixed axes

For every case compare:

```text
TASK: same / broader / narrower / different / mixed
COMMERCIALITY: more commercial / more explanatory / more procedural / more comparison-led / no material change
SPECIFICITY: same / broader / narrower / taxonomy shift / mixed
SOURCE ROLE: same role / complementary role / conflicting role / unresolved
TARGET-SITE FIT: current owner/content can satisfy both / needs bounded expansion / needs ownership/content-role reconsideration / unresolved
```

## Phase F — final Step-17 verdict

### CHANGE

Allowed only when the difference is material to the frozen page/content responsibility and the evidence chain is sufficient.

Required:

```text
material Search-vs-GenSearch difference
+ direct source/page validation where role matters
+ current target-page evidence
+ reproducibility sufficient for any material AI-driven contradiction
+ explicit Step-14 baseline -> proposed delta trace
```

### DE_RISK

GenSearch provides additional compatible evidence that reduces uncertainty around the frozen Search-only decision. It does not mean long-term AI stability.

### NO_CHANGE

The surfaces differ in wording, source mix or presentation but the frozen responsibility/action does not materially change.

### INSUFFICIENT

Use when the evidence cannot safely discriminate the decision, including an unreproduced material AI-only contradiction, unresolved source roles, or insufficient target-page evidence.

Do not force `CHANGE`.

## Phase G — bounded architecture delta overlay

For `CHANGE` only, preserve:

```text
affected_step14_unit_or_page
baseline_search_only_state
proposed_ai_derived_delta
delta_reason
evidence_refs
confidence / limitation
global_coherence_recheck_required
```

No whole-site re-architecture is performed in Step 17.

---

# 12. Fresh-request policy

Base plan:

```text
NEW PAID GENSEARCH CALLS = 0
NEW PAID ORDINARY SEARCH CALLS = 0
```

Existing same-day Step-15 Search and Step-16 GenSearch evidence is reused.

A fresh paid/search-provider request is allowed only if execution exposes a blocking evidence gap and the `RESEARCH_TO_EXECUTION_SCHEMA_GATE` is satisfied:

```text
exact unresolved question
why existing evidence is insufficient
exact operation/query
expected information gain
cost/quota
retry boundary
persistence destination
acceptance use
owner authorization
```

No request is launched merely for completeness or reassurance.

---

# 13. What Step 17 will NOT do yet

```text
no broad user-job prompt expansion
no site-wide Alice visibility measurement
no consumer-Alice claims
no silent new GenSearch sampling
no source ranking from source order/count
no full architecture rebuild
no Step-18 prioritization
no client deliverables
no final-project QA
```

---

# 14. Step-17 PASS condition

Step 17 may pass only if:

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
FINAL_VERDICT_PRESENT = 8/8
CHANGE_WITHOUT_EXPLICIT_DELTA_TRACE = 0
REVERSE_TRACE_MISSING = 0
UNAUTHORIZED_PROVIDER_CALLS = 0
INDEPENDENT_QA_BLOCKING_FINDINGS = 0
FINAL_GITHUB_READBACK = PASS
```

---

# 15. Ten-point pre-execution blocking check

Before Step-17 execution begins, all ten must be `YES`:

```text
1. Full roadmap/current-state truth loaded?
2. Step-15 V2 exact baseline loaded for all 8?
3. Step-16 corrected authority/raw lineage loaded for all 8?
4. Old Step-16 final labels excluded from decision input?
5. EXACT_QUERY claim boundary active?
6. GenSearch/consumer-Alice boundary active?
7. Source-role direct-inspection rule active?
8. Reproducibility rule active for material CHANGE?
9. Step17 delta-overlay / Step18 prioritization boundary active?
10. No unapproved paid/provider calls planned?
```

Any `NO`:

`STEP17_EXECUTION = BLOCKED`.

## Method verdict

```text
STEP17_METHOD_REVIEW = PROJECT_SPECIFIC_BUT_REASONED
STEP17_EXTERNAL_RESEARCH_COMPLETE = true
STEP17_RESEARCH_TO_EXECUTION_SCHEMA_REQUIRED = true
STEP17_EXECUTION_STARTED = false
OWNER_AUTHORIZATION_REQUIRED = true
```
