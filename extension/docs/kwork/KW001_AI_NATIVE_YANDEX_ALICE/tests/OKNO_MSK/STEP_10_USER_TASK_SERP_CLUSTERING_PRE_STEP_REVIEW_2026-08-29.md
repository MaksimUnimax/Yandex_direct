# KW-001 / OKNO-MSK — STEP 10 USER-TASK / SERP CLUSTERING — PRE-STEP METHOD REVIEW

Date: 2026-08-29
Status: **PRE-STEP METHOD REVIEW COMPLETE / OWNER EXECUTION AUTHORIZATION REQUIRED**

## 1. Whole Kwork goal

Deliver a complete, evidence-backed semantic set and site/page structure recommendation for Yandex ordinary Search plus selective Yandex AI-search evidence, with client-ready artifacts and final QA.

## 2. Step status from the universal rules index

`STEP_RULES_INDEX.md` marks Step 10 as:

```text
Step 10 | User-task / SERP clustering | UNVALIDATED
Must establish how meaning, SERP compatibility and business compatibility combine;
no automatic one-keyword-one-page logic.
```

Therefore this job cannot infer or replay a clustering method from memory. Current external research, source-to-method traceability, owner-facing method review and explicit execution authorization are required before clustering begins.

Permanent promotion remains separate:

```text
STEP_10_PERMANENT_METHOD = UNVALIDATED
THIS_DOCUMENT = JOB_SPECIFIC_PRE_STEP_METHOD
```

## 3. Accepted input truth

Step 08 Search-stage input:

```text
CORE_CANDIDATE = 1388
REVIEW_SEARCH = 944
REVIEW_DEFERRED = 174
EXCLUDED_PRESERVED = 334
TOTAL = 2840
```

Step 09 accepted Search evidence:

```text
ordinary Yandex Search probes = 75
normalized TOP-10 rows = 750
direct probe decisions = 75/75
active non-exact duplicate comparisons = 8/8
DIRECT_REVIEW_SEARCH rows = 45
UNRESOLVED_UNPROBED REVIEW_SEARCH rows = 899
automatic evidence-transfer rows = 0
```

The Step-09 evidence scope remains binding:

```text
DIRECT_QUERY_ONLY__NO_UNPROBED_TRANSFER
```

No Step-10 method may silently convert the 899 unprobed REVIEW_SEARCH rows into SERP-validated rows.

## 4. Current Step-10 goal

Build an auditable user-task clustering layer that answers:

```text
which phrases express the same or materially compatible user task;
which phrases can reasonably live in one query cluster;
which phrases must stay separate because intent/result type/task differs;
which rows are only semantically compatible but lack direct SERP support;
which material boundaries still require additional ordinary Search evidence;
which rows are outside the active business/search clustering scope.
```

Step 10 does **not** yet decide:

```text
final ownership by a specific existing URL;
keep/expand/split/merge/create structural action;
cannibalization;
Search-only architecture freeze;
AI-search cases or AI evidence.
```

Those belong to later roadmap stages.

## 5. Fresh external methodology research

### 5.1 Official Yandex — clustering is based on meaning / user intent

https://yandex.ru/support/webmaster/ru/service/queries-selection

Current Yandex Webmaster guidance states that query clustering is automatic grouping of queries that are close by meaning or by user intent. It also exposes popular pages/sites for selected queries as market evidence.

Supported consequence:

```text
cluster identity must be user-task / intent based;
word overlap or acquisition provenance is not enough.
```

### 5.2 Official Yandex — the site must answer the user's need

https://yandex.ru/support/webmaster/en/recommendations/targeting

Yandex says Search exists to answer user questions/needs and relevance depends on how page content matches the wording/need of the query.

Supported consequence:

```text
one cluster must describe one coherent answer/job that a page could realistically satisfy;
business/site fit must be checked separately from lexical similarity.
```

### 5.3 Official Yandex — query ↔ displayed-page evidence is observable

https://www.yandex.ru/support/webmaster/ru/service/search-queries

Yandex Webmaster exposes which site pages appear for which queries.

Supported consequence:

```text
query/page behaviour is an evidence layer;
SERP/page compatibility may strengthen or contradict a semantic grouping hypothesis.
```

### 5.4 Rush Analytics — TOP-10 comparison is a page-level clustering input

https://www.rush-analytics.ru/faq/klasterizaciya-zaprosov-semanticheskogo-yadra-rukovodstvo

Current revision: 2025-12-04.

Rush describes clustering by collecting TOP-10 URLs per query and comparing result sets. It supports Soft and Hard approaches and explicitly states that the appropriate overlap/accuracy setting differs by site/task; commercial and informational groups should not be blindly merged.

Supported consequence:

```text
real SERP overlap is strong page-boundary evidence;
there is no project-independent numeric cutoff that can self-decide every cluster;
manual intent review remains required.
```

### 5.5 Topvisor — intent, semantic similarity and TOP-10 are distinct inputs

https://journal.topvisor.com/ru/seo-kitchen/how-to-make-clusterization/

Topvisor describes three clustering inputs: intent, semantic similarity and TOP-10 evidence; it also distinguishes soft/middle/hard approaches and states that automatic clustering requires manual correction.

Supported consequence:

```text
semantic similarity can propose candidate groups;
SERP evidence can validate/refute page compatibility;
automatic output cannot self-accept the final clustering.
```

### 5.6 Ahrefs — same/similar intent + similar SERPs can share a page

https://ahrefs.com/blog/keyword-clustering/
https://ahrefs.com/blog/secondary-keywords/
https://ahrefs.com/blog/keyword-intent/
https://ahrefs.com/blog/keyword-strategy/

Current Ahrefs material distinguishes intent clustering from term clustering, recommends looking at actual ranking results to understand intent, and treats business potential as a separate strategic dimension.

Supported consequence:

```text
term/token similarity != intent compatibility;
actual result types/pages inform intent;
business value/fit does not replace search-intent evidence.
```

### 5.7 Semrush — SERP overlap is page-level evidence, not word similarity

https://www.semrush.com/blog/keyword-clustering/
https://www.semrush.com/blog/keyword-manager-clustering-tool/
https://www.semrush.com/blog/what-are-methods-for-keyword-clustering-and-topic-modeling/
https://www.semrush.com/blog/keyword-mapping/

Current Semrush material describes clustering by shared search intent, SERP overlap and semantic similarity. Its 2026 keyword-mapping guidance says an existing or planned page should satisfy the topic's search intent and that unmatched ideas should remain unmatched rather than being forced to a URL.

Supported consequence:

```text
page-level cluster logic should combine intent + SERP evidence + semantic review;
absence of a suitable match is a valid state;
forced assignment is prohibited.
```

## 6. Source-to-method trace

| Method element | Source/evidence | What it supports | Project-specific part | Executable Step-10 action |
|---|---|---|---|---|
| Cluster by user task / intent | Yandex query selection + targeting | meaning/intent and user need are primary | user-task labels are KW-001-specific | derive explicit `user_task` per active phrase/group |
| Use semantic similarity only to generate candidates | Topvisor + Ahrefs term-vs-intent distinction | similar words/topics can aid grouping but do not prove same intent | candidate-generation rules are project-specific | propose candidate groups, then validate boundaries |
| Use actual SERP compatibility as stronger page-boundary evidence | Rush + Ahrefs + Semrush + Step-09 evidence | shared result pages indicate one page may serve multiple queries | exact URL overlap is already persisted for declared Step-09 comparisons | attach available Step-09 SERP evidence to candidate clusters |
| Do not use a universal overlap threshold | Rush varied accuracy + Topvisor soft/middle/hard + Ahrefs interpretation caveat | different tasks/niches require different strictness | no `N common URLs => final cluster` rule | store overlap as evidence, not self-executing verdict |
| Separate materially different intents/result types | Yandex need/relevance + Rush + Topvisor + Ahrefs | commercial/informational/navigation/etc may require different answers/pages | exact task labels are project-specific | split or flag boundary review where task/result type differs |
| Public business compatibility is a filter, not an evidence route | Yandex targeting + Ahrefs business potential/strategy | relevance to what site can serve matters; business value is separate from intent | known public okno-msk offer/scope is accepted upstream truth | label `PUBLIC_BUSINESS_FIT`; do not invent internal priority |
| Keep unsupported rows unresolved | Semrush mapping + Step-09 no-transfer correction | unmatched/uncertain cases need not be forced | `UNRESOLVED_SEARCH_REQUIRED` is KW-001 state | preserve uncertain material boundaries instead of forcing a cluster |
| Frequency helps choose anchors, not prove grouping | Rush marker/frequency workflows + project Step-09 correction | frequency can order/select markers | Wordstat counts already exist | use frequency only for primary/anchor selection inside an already supported cluster |
| No page ownership yet | roadmap stage separation | clustering precedes URL mapping | Step 11 owns existing URL assignment | Step-10 output contains no final target URL decision |

Trace verdict:

```text
DIRECT_SOURCE_LINKS_PRESENT = true
MATERIAL_METHOD_ELEMENTS_TRACED = true
UNSUPPORTED_SELF_EXECUTING_THRESHOLD = 0
NON_EXECUTABLE_ROUTE = 0
PROJECT_SPECIFIC_STATES_LABELLED = true
```

## 7. Causal lessons carried into Step 10

### Known failure class A — process metadata was mistaken for intent structure

Step 09 already established:

```text
CLEANUP_REASON != SEARCH_INTENT_CLUSTER
ACQUISITION_SOURCE != SEARCH_INTENT_CLUSTER
LEXICAL_SIMILARITY != SERP_COMPATIBILITY
TRACEABILITY_COMPLETE != FULL_SERP_EVIDENCE_COVERAGE
```

Root cause:

```text
accounting compression was treated as semantic representativeness.
```

Non-repeat control:

```text
no Step-10 cluster may exist only because rows share corrected_reason,
source_id, Wordstat provenance, token overlap or acquisition family.
```

### Known failure class B — accounting QA can look perfect while semantic QA is wrong

Prior project lesson:

```text
ACCOUNTING_QA != SEMANTIC_QA
```

Non-repeat control:

```text
row counts and zero silent drops are necessary but cannot self-accept cluster meaning.
Every cluster receives a human-readable user task and evidence explanation.
```

### Risk C — one keyword = one page

`STEP_RULES_INDEX.md` explicitly forbids automatic one-keyword-one-page logic.

Non-repeat control:

```text
phrases with compatible user task may belong together;
phrases with materially different task/result type remain separate even when wording is close.
```

## 8. Step-10 executable clustering model

### 8.1 Accounting scope

All 2840 Step-08 phrase keys remain accounted.

Active clustering analysis scope:

```text
CORE_CANDIDATE 1388
+ REVIEW_SEARCH 944
= 2332 active Search-stage rows
```

Non-active states remain visible but are not force-clustered:

```text
REVIEW_DEFERRED = 174
EXCLUDED_PRESERVED = 334
```

Arithmetic gate:

```text
2332 + 174 + 334 = 2840
```

### 8.2 User-task decomposition

For each active phrase derive, as supported by wording/upstream evidence:

```text
object_or_service
user_action_or_goal
intent_orientation
material_modifier(s)
brand_or_entity_modifier
geo_modifier
result/content type expectation when known
public_business_fit
```

Examples of material modifiers include distinctions such as:

```text
new purchase vs used marketplace
purchase vs repair
commercial service vs DIY instruction
product vs accessory/component
brand/entity navigation vs generic product
commercial vs informational comparison
specific glazing object/use case
material/product subtype
material geo boundary when it changes the task
```

This decomposition is used to reason about the task; it is not a universal taxonomy promoted beyond this job.

### 8.3 Candidate grouping

Candidate groups are generated from **compatible user task**, not from matching words alone.

Allowed candidate evidence:

```text
shared user goal/action
same product/service object
compatible material modifiers
compatible intent orientation
compatible dominant result/content type when directly observed
public business fit compatible with the same offered answer/service
```

Forbidden standalone cluster authority:

```text
same corrected_reason
same source_id
same Wordstat seed/provenance
same lexical root/token set
similar frequency
absence of contradiction
```

### 8.4 Step-09 SERP integration

For the 75 directly observed queries attach:

```text
probe_id
observed_serp_job
dominant_result_type
step10_handoff
confidence
```

For the eight direct duplicate comparisons attach:

```text
exact_url_overlap
pairwise Step-09 conclusion
```

Direct contradictions override a purely lexical grouping hypothesis.

Known mandatory example:

```text
DUP-0004
`пластиковые окна от производителя rehau`
vs
`пластиковые окна рехау от производителя`
exact URL overlap = 1/10
=> must NOT be auto-merged in Step 10.
```

The seven other duplicate pairs are `CLUSTER_TOGETHER_CANDIDATE`, not automatic final merges; intent/task consistency must still be checked.

### 8.5 Treatment of the 899 unprobed REVIEW_SEARCH rows

The 899 rows do **not** inherit Step-09 SERP evidence from a sampled query.

Each row is reviewed on its own semantics and material modifiers.

Allowed states:

```text
SEMANTIC_CLUSTER_CANDIDATE_NO_DIRECT_SERP
= wording/task evidence supports compatibility with a cluster,
  but this row has no direct Step-09 SERP proof.

UNRESOLVED_SEARCH_REQUIRED
= a material intent/page-boundary question remains that semantics alone cannot safely resolve.
```

Assigning `SEMANTIC_CLUSTER_CANDIDATE_NO_DIRECT_SERP` is **not** evidence transfer. The row's evidence scope remains explicit and reversible.

No rule may bulk-transfer one direct probe to every phrase with the same cleanup reason/source/wording family.

### 8.6 Cluster evidence states

Each cluster receives one of these job-specific evidence states:

```text
SERP_SUPPORTED
= at least one material boundary/anchor is directly supported by Step-09 SERP evidence and no direct evidence contradicts the cluster task.

SEMANTIC_SUPPORTED_NO_DIRECT_SERP
= coherent user task and public business fit, but no direct Step-09 SERP evidence for the material boundary.

MIXED_OR_BOUNDARY_REVIEW
= direct or semantic evidence is mixed; cluster cannot be treated as stable.

SEARCH_REQUIRED
= additional ordinary Search evidence is needed before the material boundary can be accepted.
```

These are evidence-confidence states, not page-action states.

### 8.7 Mixed intent rule

Do not force informational and commercial tasks into one cluster merely because the subject is the same.

Where Search itself is genuinely mixed:

```text
preserve MIXED_OR_BOUNDARY_REVIEW;
document the dominant observed result types;
do not pre-decide a hybrid page in Step 10.
```

A later structural stage may decide whether one hybrid asset can serve the mixed task.

### 8.8 Public business fit rule

Use only accepted public/business-scope truth from upstream site discovery.

```text
PUBLIC_BUSINESS_FIT = FIT | ADJACENT | OUTSIDE | UNKNOWN_PUBLIC_FIT
```

Do not use unavailable internal information such as margin, capacity, growth priority or operational preference to create/split clusters.

Canonical distinction:

```text
PUBLIC BUSINESS FIT = Step-10 evaluation dimension
INTERNAL BUSINESS PRIORITY = later client/prioritization constraint
```

### 8.9 Frequency rule

Wordstat frequency may choose:

```text
primary/anchor query inside an already supported cluster
review ordering
priority for later analysis
```

It may not prove:

```text
same intent
same cluster
same page
relevance
business fit
```

## 9. Required Step-10 outputs

Execution will produce at minimum:

### `STEP_10_CLUSTER_ASSIGNMENTS.tsv`

One row per Step-08 phrase key with fields equivalent to:

```text
phrase
input_disposition
user_task
intent_orientation
material_modifiers
public_business_fit
step09_probe_id
step09_evidence_scope
observed_serp_job
dominant_result_type
cluster_id
cluster_role
cluster_evidence_state
assignment_reason
confidence
additional_search_required
```

### `STEP_10_CLUSTER_SUMMARY.tsv`

One row per produced candidate/stable cluster:

```text
cluster_id
cluster_label
user_task
intent_orientation
public_business_fit
primary_query
member_count
direct_serp_member_count
semantic_only_member_count
cluster_evidence_state
boundary_notes
```

### `STEP_10_BOUNDARY_REVIEW.tsv`

Explicit list of:

```text
mixed-intent cases
SERP contradictions
material unprobed boundaries
SEARCH_REQUIRED rows/groups
DUP-0004 handling
other cases blocked from stable clustering
```

### `STEP_10_RECONCILIATION.md`

Quantitative and semantic QA.

### `STEP_10_ACCEPTANCE_2026-08-29.md`

Final Step-10 verdict after execution and QA.

## 10. Step-10 PASS gate

Step 10 may pass only if all of the following are true:

```text
1. all 2840 Step-08 phrase keys are accounted exactly once;
2. all 2332 active Search-stage rows receive an explicit cluster/unresolved state;
3. REVIEW_DEFERRED 174 remain preserved unless separately re-authorized;
4. EXCLUDED_PRESERVED 334 remain preserved and are not silently reintroduced;
5. every cluster has a human-readable user task, intent orientation and public business-fit state;
6. no cluster exists solely from corrected_reason, source_id, Wordstat provenance, lexical similarity or frequency;
7. all 75 Step-09 direct probe decisions are consumed as evidence/handoff inputs;
8. all 8 active Step-09 duplicate comparisons are consumed;
9. DUP-0004 is not auto-merged;
10. the 899 unprobed REVIEW_SEARCH rows do not inherit direct SERP evidence without individual justification;
11. every material uncertain boundary is explicitly MIXED_OR_BOUNDARY_REVIEW or SEARCH_REQUIRED;
12. no universal numeric SERP-overlap cutoff is used as an automatic final verdict;
13. accounting QA passes;
14. semantic/manual QA passes independently;
15. no final existing-URL ownership is assigned;
16. no keep/expand/split/merge/create structural action is decided;
17. no cannibalization conclusion is made;
18. zero silent drops;
19. source-to-method trace remains satisfied after execution.
```

If material `SEARCH_REQUIRED` boundaries remain after clustering:

```text
STEP_10 may report the clustering work as incomplete or partially accepted;
STEP_11 must not silently treat unresolved boundaries as final clusters.
```

Any additional paid Search tranche requires a separate bounded provider plan/cost gate and explicit owner authorization before provider execution.

## 11. What this method deliberately does not claim

```text
SERP overlap is not a universal deterministic SEO law;
semantic similarity alone is not same-page proof;
all 899 unprobed rows are not suddenly SERP-validated;
one keyword does not imply one page;
one cluster does not yet imply one existing URL;
public business fit does not reveal internal business priority;
Step 10 does not decide architecture actions.
```

## 12. Pre-step verdict

```text
STEP10_PERMANENT_METHOD = UNVALIDATED
STEP10_CURRENT_EXTERNAL_RESEARCH = COMPLETE
STEP10_SOURCE_TO_METHOD_TRACE = PASS
STEP10_CURRENT_JOB_INPUTS_READ = true
STEP10_KNOWN_FAILURE_CLASSES_INTEGRATED = true
STEP10_EXECUTABLE_METHOD_DEFINED = true
STEP10_PASS_GATE_DEFINED = true
STEP10_OWNER_FACING_METHOD_REVIEW = READY
STEP10_EXECUTION_AUTHORIZATION = PENDING
STEP10_CLUSTERING_EXECUTION_STARTED = false
```

Execution remains blocked until owner review/authorization of this Step-10 method.