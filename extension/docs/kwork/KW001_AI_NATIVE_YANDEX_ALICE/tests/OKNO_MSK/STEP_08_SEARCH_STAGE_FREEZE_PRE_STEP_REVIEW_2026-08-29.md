# KW-001 / OKNO-MSK — STEP 08 SEARCH-STAGE SEMANTIC FREEZE — PRE-STEP REVIEW

Date: 2026-08-29
Status: **PRE-STEP REVIEW COMPLETE / WAITING OWNER AUTHORIZATION / EXECUTION NOT STARTED**

## 1. Whole Kwork goal

Deliver a complete, evidence-backed semantic set and site/page structure recommendation for Yandex ordinary Search plus selective AI-search evidence, with client-ready artifacts and final QA.

## 2. Full roadmap

| Major step | Meaning | Status |
|---|---|---|
| 0. Scope freeze | Freeze business/region/order boundaries | ✅ COMPLETE |
| 1. Existing-site discovery | Build cross-checked site/business/page model | ✅ COMPLETE |
| 2. Wordstat acquisition plan | Freeze first-pass demand probes | ✅ COMPLETE |
| 3. Historical first pass | Original provider-success-only acceptance | 🔁 SUPERSEDED |
| 3R. Repaired first pass | Preserve complete reusable Wordstat data | ✅ COMPLETE |
| 4. Family-level triage | Identify families/noise/ambiguity/probe candidates | ✅ COMPLETE AS TRIAGE |
| 5. Targeted Wordstat expansion | Fill/confirm material acquisition directions | ✅ COMPLETE |
| 6. Demand dynamics | Preserve seasonality context | ✅ PRESERVED |
| 6A. Acquisition coverage revalidation | Decide whether more Wordstat is needed | ✅ COMPLETE |
| 7. Row-level semantic cleanup | Produce trustworthy phrase-level decisions | ✅ COMPLETE AFTER CORRECTION |
| **8. Freeze Search-stage semantic set** | **Create an immutable handoff from cleanup into Search without prematurely deciding clusters/pages** | **🟡 CURRENT — PRE-STEP REVIEW COMPLETE** |
| 9. Ordinary Yandex Search validation | Resolve intent/page boundaries with real SERP | ⬜ NOT STARTED |
| 10. User-task / SERP clustering | Group compatible search jobs | ⬜ NOT STARTED |
| 11. Page ownership | Map clusters to best existing URLs | ⬜ NOT STARTED |
| 12. Structural actions | Keep/expand/split/merge/create decisions | ⬜ NOT STARTED |
| 13. Cannibalization diagnosis | Confirm real competing-page conflicts | ⬜ NOT STARTED |
| 14. Search-only architecture freeze | Freeze architecture before AI | ⬜ NOT STARTED |
| 15. AI-case selection | Select high-information uncertain cases | ⬜ NOT STARTED |
| 16. AI-search evidence | Gather selected Alice/GenSearch evidence | ⬜ NOT STARTED |
| 17. Search-vs-AI comparison | Compare classic Search and AI evidence | ⬜ NOT STARTED |
| 18. Prioritization | Rank recommended actions | ⬜ NOT STARTED |
| 19. Client deliverables | Produce client-ready workbooks/maps/matrices | ⬜ NOT STARTED |
| 20. Final QA | Reconcile evidence, numbers and recommendations | ⬜ NOT STARTED |
| 21. Handoff/revisions | Deliver and process allowed revisions | ⬜ NOT STARTED |
| 22. Job close | Mark safe-to-delete and remove disposable workspace | ⬜ NOT STARTED |

## 3. Completed work relevant to this step

- Step 07C semantic correction is owner-accepted for workflow progression.
- Complete source provenance remains preserved: 2965 source occurrences -> 2840 exact phrase keys.
- Accepted corrected Step-07C decisions:

```text
KEEP = 1388
REVIEW = 1118
EXCLUDE_SCOPE = 180
EXCLUDE_IRRELEVANT = 120
EXCLUDE_MECHANICAL = 34
TOTAL = 2840
```

- No default KEEP fallthrough remains.
- Non-exact duplicate candidate groups remain unresolved rather than silently merged.

## 4. Remaining work after this step

After Step 8, the job still must perform ordinary Yandex Search validation, user-task/SERP clustering, page ownership, structural actions, cannibalization diagnosis, Search-only architecture freeze, selective AI evidence, Search-vs-AI comparison, prioritization, client deliverables, final QA, handoff/revisions and job close.

## 5. Step 8 purpose

Create a frozen, reproducible semantic handoff between accepted phrase-level cleanup and ordinary Yandex Search validation.

This step must answer:

```text
What exact phrase universe is allowed to enter the Search stage?
Which phrases are accepted working candidates versus unresolved candidates?
What evidence route is required for each unresolved candidate?
Which rows remain excluded but preserved for audit?
Which non-exact duplicate candidates must remain visible for later Search/intent resolution?
What exact immutable snapshot/hashes define the Search-stage input?
```

## 6. What Step 8 solves

Step 07C produced reliable phrase-level KEEP / REVIEW / EXCLUDE decisions, but Search cannot safely start from an implicit interpretation of those states.

Without a freeze/handoff step, several process errors are possible:

```text
REVIEW could be silently discarded;
KEEP could be treated as a final keyword/page target;
excluded phrases could disappear from audit history;
Search could be run on an arbitrary subset chosen ad hoc;
non-exact duplicate candidates could be silently collapsed;
later Search results could be compared against a moving input list;
page/clustering decisions could leak into the workflow before SERP evidence exists.
```

Step 8 therefore freezes the evidence boundary. It does not try to finish the SEO architecture.

## 7. Required output

Planned artifacts:

```text
STEP_08_SEARCH_STAGE_SEMANTIC_SET.tsv
STEP_08_REVIEW_RESOLUTION_ROUTES.tsv
STEP_08_NONEXACT_DUPLICATE_HANDOFF.tsv
STEP_08_SEARCH_STAGE_FREEZE_RECONCILIATION.md
```

### 7.1 Search-stage semantic set

One row per accepted Step-07C exact phrase key, preserving Step-07C status/reason and adding only handoff metadata.

Proposed fields:

```text
phrase
step07c_status
step07c_reason
semantic_confidence
source_occurrences
result_occurrences
association_occurrences
max_result_count
max_association_count
source_ids
provenance
search_stage_disposition
next_resolution_route
route_reason
```

Step 8 must not rewrite the accepted Step-07C semantic status without new evidence.

### 7.2 Search-stage disposition

The Step-07C statuses remain the semantic truth. Step-8 disposition is a routing layer, not a replacement classification.

Proposed routing semantics:

```text
CORE_CANDIDATE
= accepted Step-07C KEEP; remains eligible working semantic evidence.

REVIEW_SEARCH
= uncertainty is materially about search intent, result type, semantic/page boundary or whether similar phrases can be targeted together; ordinary Search is the proper next evidence.

REVIEW_BUSINESS
= uncertainty primarily depends on frozen/unknown business priority or service/assortment scope and cannot be solved by SERP alone.

REVIEW_SEARCH_AND_BUSINESS
= both market/Search evidence and business-scope truth matter.

REVIEW_DEFERRED
= plausible evidence retained, but it does not justify Search acquisition in the immediate bounded Search stage unless later grouping exposes material value.

EXCLUDED_PRESERVED
= Step-07C EXCLUDE_*; remains in the audit snapshot but is not an active Search semantic candidate.
```

These route names are project-specific mechanics, not claimed industry standards.

### 7.3 Review routing

Every one of the 1118 Step-07C REVIEW rows must receive exactly one next-resolution route.

The route must be derived from the Step-07C reason and known scope, not from frequency alone.

Examples of likely Search-resolvable classes:

```text
mixed/comparison intent
technical/informational intent when content fit is uncertain
navigation/entity ambiguity
architecture/inspiration vs product intent
panoramic real-estate vs glazing intent
non-exact duplicate/variant intent boundary
page-boundary uncertainty
```

Examples requiring business truth or combined evidence:

```text
standalone installation priority
repair/service acquisition priority
accessories/fittings as standalone acquisition
finance/instalment acquisition priority
unproven service boundaries such as demolition
```

The frozen mock-order answers explicitly leave several of those business priorities UNKNOWN, so Search evidence must not be allowed to silently invent the commercial decision.

### 7.4 Non-exact duplicates

Carry all Step-07C non-exact candidate groups forward unchanged as unresolved evidence.

No automatic merge in Step 8.

### 7.5 Reconciliation

The freeze must prove:

```text
Step-07C phrase keys expected = 2840
Step-08 phrase keys written = 2840
CORE_CANDIDATE expected from Step-07C KEEP = 1388
all Step-07C REVIEW rows routed exactly once = 1118
all Step-07C EXCLUDE rows preserved = 334
1388 + 1118 + 334 = 2840
unclassified/unrouted REVIEW = 0
silent drops = 0
Step-07C status rewrites = 0
non-exact duplicate candidate groups preserved = 9
provider/Search requests executed = 0
provider cost = 0 RUB
```

The actual route subtotals inside the 1118 REVIEW rows are execution outputs and must be reported after the step.

## 8. Relevant previous errors / root causes / non-repeat controls

### Error: technical completeness mistaken for project completeness

Earlier provider acquisition passed on request success before complete reusable data had been preserved.

Root cause:

```text
activity/status success was confused with the actual step objective
```

Step-8 control:

```text
file creation alone cannot pass;
all 2840 rows and all 1118 REVIEW routes must reconcile;
freeze hashes and audit tables must exist.
```

### Error: family-level triage mistaken for row-level cleanup

Root cause:

```text
high-level coverage was confused with exhaustive row-level decision accounting
```

Step-8 control:

```text
every Step-07C phrase key must receive a Search-stage disposition;
no implicit omissions.
```

### Error: default KEEP fallthrough in Step 07B

Root cause:

```text
absence of a known negative rule was treated as positive relevance evidence
```

Step-8 control:

```text
Step 8 does not reclassify REVIEW to CORE merely because no blocking route is known;
CORE_CANDIDATE comes only from accepted Step-07C KEEP.
```

### Error risk: REVIEW treated as reject

Root cause:

```text
uncertainty can be mistaken for irrelevance when trying to simplify a large list
```

Step-8 control:

```text
all 1118 REVIEW rows must be preserved and routed;
none may disappear merely to reduce Search volume.
```

### Error risk: Search/page/clustering conclusions made before Search

Root cause:

```text
semantic similarity or analyst intuition can be mistaken for evidence that queries share one page job
```

Step-8 control:

```text
no final clustering;
no page ownership;
no structural action;
no automatic non-exact merge;
those decisions remain downstream.
```

## 9. Fresh external methodology research

Step 8 is marked `UNVALIDATED` in the permanent `STEP_RULES_INDEX.md`; therefore fresh research was required instead of mechanically inferring the method from Step 7 or Step 9.

### Official Yandex

Yandex Webmaster — user-needs / targeting guidance:
https://yandex.ru/support/webmaster/ru/recommendations/targeting

Support relevant to Step 8:
- search exists to answer user needs expressed through queries;
- suitable key phrases must be selected for what the site can actually answer;
- Wordstat/related-query vocabulary is discovery evidence, not automatic proof that every phrase belongs in the final target strategy.

Yandex Wordstat:
https://yandex.ru/support2/wordstat/ru/interface/new

Support relevant to Step 8:
- Wordstat returns popular queries containing the phrase and similar queries;
- those data remain demand/vocabulary evidence rather than a final page map.

Yandex Webmaster — query groups:
https://yandex.ru/support/webmaster/ru/service/search-queries

Support relevant downstream:
- Yandex explicitly supports working with query groups and seeing which pages appear for queries;
- this reinforces keeping query/page evidence distinct from raw keyword acquisition.

Yandex Webmaster — query selection beta:
https://yandex.ru/support/webmaster/en/service/queries-selection

Support relevant to Step 8:
- query selection is about choosing suitable/promising queries, not treating the entire discovered vocabulary as equally actionable.

### Current industry methodology

Ahrefs — Keyword Intent, updated 2026-03-13:
https://ahrefs.com/blog/keyword-intent/

Relevant principle:
- keyword intent acts as an early filter for deciding whether a keyword belongs in the strategy;
- mixed/uncertain intent requires stronger evidence rather than forced classification.

Ahrefs — Keyword Strategy, updated 2026-03-13:
https://ahrefs.com/blog/keyword-strategy/

Relevant principle:
- actual ranking results are the most reliable practical evidence for what searchers expect when intent is not clear.

Semrush — Keyword Clustering, 2025-10-29:
https://www.semrush.com/blog/keyword-clustering/

Relevant principle:
- clustering groups terms that share search intent and may target one page;
- subtle intent differences matter and should not be flattened before evidence.

Semrush — Keyword Mapping, 2026-07-27:
https://www.semrush.com/blog/keyword-mapping/

Relevant principle:
- keyword mapping follows from relevant topics/clusters and assigns them to the page that best satisfies the intent;
- mapping is therefore downstream of the current freeze stage.

Topvisor — semantic-core cleanup, 2025-04-04:
https://journal.topvisor.com/ru/seo-kitchen/how-to-understand-from-which-requests-clean-the-core/

Relevant principles:
- cleanup is gradual;
- non-obvious duplicates and unsuitable intent require care;
- SERP can be used to check commercial/informational intent;
- low-frequency phrases are not universally disposable.

Rush Analytics — clustering / intent, updated 2025-08-28:
https://www.rush-analytics.ru/blog/chto-takoe-klasterizacziya-zaprosov

Relevant principles:
- determine intent before clustering;
- current search results/types of ranking sites are useful evidence;
- automated processing still requires expert correction.

## 10. Method origin classification

```text
OFFICIAL:
- Yandex user-needs/query-selection/query-group guidance
- Wordstat semantics

INDUSTRY_PRACTICE:
- intent-based keyword selection
- SERP evidence for ambiguous intent
- clustering/mapping only after intent/relevance preparation
- non-obvious duplicates require caution

PROJECT_TEST_VALIDATED:
- exact provenance/accounting controls
- no-default-KEEP correction
- REVIEW as explicit uncertainty preservation

ANALYST_HEURISTIC / PROJECT-SPECIFIC:
- the exact Step-8 routing-state names
- using a distinct immutable Search-stage freeze artifact
- exact logic for REVIEW_SEARCH / REVIEW_BUSINESS / combined/deferred routing
```

There is no official Yandex standard called `Step 8 Search-stage semantic freeze`. The freeze is a project workflow control designed to keep the input stable and auditable before Search evidence changes later decisions.

## 11. Adversarial self-audit

### Could Step 8 simply take all KEEP rows and discard REVIEW?

No. That would repeat the mistake of treating uncertainty as irrelevance and would remove precisely the cases ordinary Search is meant to resolve.

### Could Step 8 send all 2506 non-excluded phrases directly to Search?

Not automatically. Search validation is a decision-evidence stage, not a requirement to issue one Search request per phrase. The next stage should target material intent/page-boundary evidence and use representative/group-aware logic where justified.

### Could Step 8 cluster the 2506 phrases now to reduce requests?

Not finally. Semantic/topic pre-grouping may later help operational batching, but final user-task/SERP clustering belongs after ordinary Search evidence. Performing final clusters now would use the answer before collecting the evidence.

### Could volume determine which REVIEW rows survive?

No. The accepted methodology already records that low frequency alone is not irrelevance. Volume may later help prioritize evidence or actions, but it cannot erase a potentially relevant phrase by itself.

### Could Search decide business priorities such as whether repair/accessories/finance should be actively sold?

No. Search can show demand and result intent, but it cannot determine the client's margin, capacity or strategic priority. Those unresolved business assumptions must stay explicit.

## 12. Proposed method verdict

```text
METHOD_VERDICT = PROJECT_SPECIFIC_BUT_REASONED
STEP_08_PERMANENT_METHODOLOGY_STATUS = UNVALIDATED
EXECUTION_READY_AFTER_OWNER_AUTHORIZATION = true
```

The external sources support the separation of relevance/intent preparation, SERP evidence, clustering and mapping. The exact freeze/routing mechanics are project-specific controls for auditability and workflow discipline.

## 13. What Step 8 will NOT do

```text
no new Wordstat acquisition
no Yandex Search/provider requests
no final cluster creation
no final page ownership
no keep/merge/split/create page decisions
no cannibalization verdicts
no AI-search evidence
no frequency-only deletion
no automatic non-exact duplicate merge
no silent resolution of client-unknown business priorities
```

## 14. Pass gate

Step 8 may pass only if:

```text
accepted Step-07C exact phrase keys read = 2840
Step-08 frozen rows = 2840
accepted KEEP carried as CORE_CANDIDATE = 1388
accepted REVIEW routed exactly once = 1118
accepted EXCLUDE_* preserved = 334
status rewrites without new evidence = 0
unrouted REVIEW = 0
silent drops = 0
non-exact duplicate candidate groups carried = 9
all output hashes recorded
Search/provider calls = 0
provider cost = 0 RUB
final clustering/page ownership decisions = 0
```

If any count fails, Step 8 is incomplete and Step 9 remains blocked.

## 15. Plain-language owner summary

### Зачем нужен этот шаг

Чтобы перед проверкой в реальной выдаче Яндекса зафиксировать один точный список, от которого мы дальше работаем, и больше не менять вход задним числом.

### Что он решает

Он не даёт потерять спорные запросы, принять их за мусор или наоборот незаметно считать готовыми. Для каждого спорного запроса будет указано, какое доказательство нужно дальше: выдача Яндекса, бизнес-решение или оба источника.

### Как мы это делаем

Берём принятый результат очистки как есть, ничего заново не придумываем, добавляем к каждой фразе только маршрут следующей проверки, сохраняем исключённые и спорные варианты для аудита и фиксируем неизменяемый снимок перед Search.

---

```text
PRE_STEP_REVIEW_COMPLETE = true
OWNER_AUTHORIZATION_REQUIRED_FOR_EXECUTION = true
STEP_08_EXECUTION_STARTED = false
NEXT_STEP_09_BLOCKED = true
```
