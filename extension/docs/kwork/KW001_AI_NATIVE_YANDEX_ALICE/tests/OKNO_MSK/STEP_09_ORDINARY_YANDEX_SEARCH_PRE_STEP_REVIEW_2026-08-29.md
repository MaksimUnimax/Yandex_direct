# KW-001 / OKNO-MSK — STEP 09 ORDINARY YANDEX SEARCH VALIDATION — PRE-STEP REVIEW

Date: 2026-08-29
Status: **PRE-STEP METHOD REVIEW COMPLETE / OWNER AUTHORIZATION REQUIRED / PROVIDER EXECUTION NOT STARTED**

## 1. Whole Kwork goal

Deliver a complete, evidence-backed semantic set and site/page structure recommendation for Yandex ordinary Search plus selective Yandex AI-search evidence, with client-ready artifacts and final QA.

## 2. Full roadmap

| Stage | What this stage does | Status |
|---|---|---|
| 0. Scope freeze | Freeze business/region/order boundaries | ✅ COMPLETE |
| 1. Existing-site discovery | Build cross-checked site/business/page model | ✅ COMPLETE |
| 2. Wordstat acquisition plan | Freeze first-pass demand probes | ✅ COMPLETE |
| 3. Historical first pass | Original defective provider-success-only acceptance | 🔁 SUPERSEDED |
| 3R. Repaired first pass | Preserve complete reusable Wordstat data | ✅ COMPLETE |
| 4. Family-level triage | Identify families/noise/ambiguity/probe candidates | ✅ COMPLETE AS TRIAGE |
| 5. Targeted Wordstat expansion | Fill/confirm material acquisition directions | ✅ COMPLETE |
| 6. Demand dynamics | Preserve seasonality context | ✅ PRESERVED |
| 6A. Acquisition coverage revalidation | Decide whether more Wordstat is needed | ✅ COMPLETE |
| 7. Row-level semantic cleanup | Produce trustworthy phrase-level decisions | ✅ COMPLETE AFTER CORRECTION |
| 8. Freeze Search-stage semantic set | Freeze exact Search input and executable unresolved routes | ✅ COMPLETE AFTER METHOD CORRECTION |
| **9. Ordinary Yandex Search validation** | **Collect bounded real Yandex SERP evidence for material intent/page-boundary questions** | **🟡 CURRENT — PRE-STEP COMPLETE / AUTHORIZATION PENDING** |
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

## 3. Accepted input truth

Corrected Step 08 is the only Search-stage input authority.

```text
CORE_CANDIDATE = 1388
REVIEW_SEARCH = 944
REVIEW_DEFERRED = 174
EXCLUDED_PRESERVED = 334
TOTAL = 2840
```

Step 09 acts on material Search questions arising from `CORE_CANDIDATE` anchors and the `944 REVIEW_SEARCH` rows. It does not promote `REVIEW_DEFERRED` merely because Search is now available.

All 944 `REVIEW_SEARCH` rows must remain traceable to an evidence question or remain explicitly unresolved after this step. No row may disappear because it was not selected as a provider probe.

## 4. Current step goal

Collect reproducible ordinary Yandex Search evidence sufficient to resolve the **material** intent/result-type/page-boundary questions that block later clustering and page ownership.

Step 09 is an evidence-acquisition and interpretation stage. It is not a command to issue one paid Search request for every non-excluded phrase.

## 5. What this step solves

It must establish, for selected material query relationships:

```text
what kind of pages Yandex currently ranks;
whether the dominant intent is commercial / informational / navigational / mixed;
which exact URLs recur across compared queries;
whether compared queries show materially similar or divergent result sets;
whether a phrase that looked ambiguous in cleanup belongs to the same observable search job as a core anchor;
which questions remain mixed or insufficient after real SERP evidence.
```

It must NOT yet decide final clusters, final page ownership, structural actions or cannibalization.

## 6. Fresh external methodology research

### 6.1 Official Yandex — user need and relevance

https://yandex.ru/support/webmaster/en/recommendations/targeting

Supports:
- Search is intended to answer user needs expressed in queries;
- page relevance depends on how content matches the wording/need of the query.

### 6.2 Official Yandex — query/page evidence

https://yandex.ru/support/webmaster/ru/service/search-queries

Supports:
- Yandex exposes which pages appear for which queries;
- query↔page relationships are a real Search evidence layer;
- query groups are an analysis convenience, not proof that every member is one page job.

### 6.3 Official Yandex — query selection / popular pages

https://yandex.ru/support/webmaster/ru/service/queries-selection

Supports:
- suitable queries can be selected and their potential analyzed;
- popular pages/sites for selected queries are useful market evidence;
- Yandex itself describes clustering as grouping queries close by meaning or user intent.

### 6.4 Official Yandex Search API — ordinary text Search

https://aistudio.yandex.ru/docs/ru/search-api/concepts/web-search.html
https://aistudio.yandex.ru/docs/ru/search-api/api-ref/WebSearch/search.html

Supports:
- ordinary Yandex Search can be queried programmatically;
- XML contains the search results proper;
- `region` affects ranking rules;
- `page`, `groupsOnPage`, grouping, typo mode, relevance sorting and other parameters are explicit and reproducible;
- `GROUP_MODE_FLAT` keeps one document per group rather than grouping a domain into one container.

### 6.5 Official Yandex region authority

https://aistudio.yandex.ru/ru/docs/search-api/reference/regions

Supports:
- region affects generated results;
- `213` = Moscow;
- `1` = Moscow and Moscow Region.

### 6.6 Official Yandex pricing

https://aistudio.yandex.ru/ru/docs/search-api/pricing

Current public price used for the safety calculation:

```text
daytime synchronous ordinary Search = 488 RUB / 1000 requests
= 0.488 RUB / request
```

The bridge's accepted production contract currently uses ordinary synchronous Search for the bulk SERP hand.

### 6.7 Industry practice — compare actual result sets

Rush Analytics:
https://www.rush-analytics.ru/faq/klasterizaciya-zaprosov-semanticheskogo-yadra-rukovodstvo

Supports:
- gather TOP-10 URLs for queries and compare the result sets;
- shared URLs are evidence used to group queries;
- marker-query logic is used operationally.

Topvisor:
https://journal.topvisor.com/ru/seo-kitchen/how-to-make-clusterization/
https://journal.topvisor.com/ru/dictionary/what-is-clustering/

Supports:
- TOP-10 overlap is an established Yandex/SEO clustering input;
- soft/middle/hard methods differ, proving there is no single universally mandated overlap rule.

Ahrefs:
https://ahrefs.com/blog/keyword-clustering/
https://help.ahrefs.com/en/articles/9063645-what-are-all-the-things-i-can-do-in-serp-overview

Supports:
- keywords with similar search results are candidates for the same cluster/page;
- pairwise SERP comparison is useful when deciding whether two queries belong together;
- similarity can account for common results and positions.

Ahrefs intent / strategy:
https://ahrefs.com/blog/keyword-intent/
https://ahrefs.com/blog/keyword-strategy/

Supports:
- search intent is the reason behind a query;
- actual ranking results are practical evidence of the content type/format users expect;
- business potential is separate from intent and does not replace SERP evidence.

Semrush:
https://www.semrush.com/blog/keyword-manager-clustering-tool/
https://www.semrush.com/blog/what-are-methods-for-keyword-clustering-and-topic-modeling/

Supports:
- SERP overlap is used because shared ranked URLs indicate that one content asset may serve multiple queries;
- clustering can combine intent, SERP overlap and semantic review.

## 7. Source-to-method trace

| Method element | Source / evidence | What it supports | Project-specific part | Executable action/output |
|---|---|---|---|---|
| Use ordinary Yandex Search, not GenSearch | Yandex Search API docs + project Phase-8 Search contract | ordinary Search returns ranked search results | Step 09 is intentionally classic Search-only | `service=search`, ordinary Search only |
| Moscow baseline | Yandex regions docs | region affects ranking; 213=Moscow | Moscow is frozen primary region | `region=213` for baseline queries |
| TOP-10 observation | Rush + Topvisor + bridge Phase 8 | TOP-10 overlap is established SERP evidence | no claim that 10 is an official Yandex SEO threshold | `groupsOnPage=10`, `page=0` |
| Flat ranked documents | Yandex Search API + bridge contract | flat grouping returns individual documents | required for page-level evidence | `GROUP_MODE_FLAT`, `docsInGroup=1` |
| XML organic-result payload | Yandex Search API | XML contains search results proper; HTML may include ads/extra SERP elements | Step 09 needs normalized organic evidence | preserve raw XML + normalized ranked rows |
| Relevance sorting | Yandex API | relevance is default sorting | keep provider default consistent | `SORT_MODE_BY_RELEVANCE` |
| Exact URL overlap as primary page-boundary evidence | Rush/Topvisor/Ahrefs | shared ranked URLs are evidence of same/similar search job | no automatic same-page threshold | compute exact URL intersections for declared comparisons |
| Domain overlap as secondary evidence | bridge `overlapPage` | deterministic competitive-composition projection | cannot replace exact URL overlap | preserve domain overlap/Jaccard as secondary evidence |
| No universal overlap cutoff | Rush soft/hard + Topvisor soft/middle/hard + Ahrefs graded similarity | methods use different overlap/similarity rules | analyst must interpret evidence instead of hard-coding one threshold | no `3 URLs => same page` automatic verdict |
| Representative probe selection | Rush marker-query practice + project bounded-service need | marker queries are operationally useful | coverage algorithm is KW-001-specific | build frozen evidence-question manifest before paid calls |
| Preserve all 944 REVIEW_SEARCH rows | accepted Step 08 | uncertainty cannot silently disappear | non-probed rows link to evidence questions, not discarded | row→evidence-question map |
| Provider cap | Yandex pricing + project Phase-8 budget model | cost is per request; bridge supports explicit maxRequests/maxCostRub | **80 is a safety ceiling, not SEO methodology** | `maxRequests <= 80`, `maxCostRub <= 39.04` |
| One provider request per explicit `next` | project `PHASE_8_BULK_SERP_TOP_RANK_REQUIREMENTS_AND_PLAN.md` | exactly-once-safe Search batch lifecycle | required by project YMB safety | sequential `next`; verify saved result before another |
| No final clustering/page ownership | current roadmap + industry stage separation | SERP evidence informs clustering/mapping | Step 10/11 own those decisions | Step 09 outputs evidence/verdicts only |

Trace verdict:

```text
DIRECT_SOURCE_LINKS_PRESENT = true
MATERIAL_METHOD_ELEMENTS_TRACED = true
UNSUPPORTED_METHOD_ELEMENTS = 0
NON_EXECUTABLE_EVIDENCE_ROUTES = 0
PROJECT_SPECIFIC_ELEMENTS_LABELLED = true
SOURCE_CLAIMS_NOT_OVEREXTENDED = true
```

## 8. Query-selection method — bounded evidence questions, not one call per keyword

### 8.1 Mandatory coverage obligations

Before any paid Search call, create a frozen local manifest that covers at minimum:

```text
A. all material Step-01 page-boundary questions;
B. all 8 active non-exact duplicate groups that Step 08 routed to ordinary Search;
C. every distinct corrected_reason represented inside REVIEW_SEARCH;
D. all base commercial/page directions needed as core comparison anchors;
E. any material geo question selected for this base-package architecture test.
```

A single query may satisfy several obligations. Exact duplicate planned queries are deduplicated before provider execution.

### 8.2 Marker and contrast selection

For each evidence question:

```text
1. choose a marker query that represents the question;
2. where the question is a boundary/comparison, choose the minimum contrast query/query set needed to observe that boundary;
3. prefer queries with stronger demand evidence when several phrases are otherwise equally representative;
4. frequency is used only to choose an efficient marker, never as proof of relevance or exclusion;
5. attach every selected query to the exact evidence question(s) it is meant to test.
```

### 8.3 Coverage of non-probed rows

Every `REVIEW_SEARCH` row must receive:

```text
evidence_question_id
coverage_state = DIRECT_PROBE | REPRESENTED_BY_QUESTION | UNRESOLVED
```

`REPRESENTED_BY_QUESTION` does not mean automatically resolved. After SERP evidence is collected, ChatGPT must decide whether the row is genuinely compatible with that evidence question. If not, it remains `UNRESOLVED`.

### 8.4 Safety ceiling

First authorized tranche proposal:

```text
MAX_PROVIDER_REQUESTS = 80
MAX_PROVIDER_COST_RUB = 39.04
```

This is a **project-specific cost/scope ceiling**, not an SEO quality threshold.

If the frozen manifest requires more than 80 direct Search probes to meet the declared coverage obligations:

```text
PROVIDER_EXECUTION = BLOCKED
STEP_09 = NOT_COMPLETE
REPORT MANIFEST SIZE + REASON
REQUEST NEW OWNER AUTHORIZATION BEFORE ADDITIONAL COST
```

## 9. Search request baseline

For ordinary baseline Search evidence:

```text
service = search
protocol = SEARCH_BATCH_API_V1
searchType = SEARCH_TYPE_RU
region = 213
page = 0
groupsOnPage = 10
docsInGroup = 1
groupMode = GROUP_MODE_FLAT
sortMode = SORT_MODE_BY_RELEVANCE
sortOrder = existing safe bridge default
familyMode = FAMILY_MODE_MODERATE
fixTypoMode = FIX_TYPO_MODE_ON
responseFormat = FORMAT_XML
```

Why:
- official API docs define these controls;
- TOP-10 is the industry evidence unit chosen here;
- flat XML results preserve individual ranked organic documents;
- Moscow is the frozen primary region.

For a deliberately selected geo-boundary question, a separate manifest row may use another **officially verified** region ID. Results from different regions must not be silently mixed into one overlap comparison.

If typo correction materially changes a suspicious malformed query, a separate exact-typo diagnostic may be proposed; it is not part of the default batch.

## 10. Required saved result per provider query

For every executed Search item preserve before the next provider interaction:

```text
job_id
item_id
query_text
all normalized request parameters
region
request_id
request_executed truth
provider outcome state
observation timestamp
estimated cost
complete raw ordinary-Search payload
observed_result_count
ranked_results[] with at least:
  rank
  url
  domain
  title
  snippet
```

Sparse successful result sets remain successful evidence and must preserve the actual observed count; do not fabricate 10 rows.

## 11. Comparison/interpretation output

For every declared query comparison preserve:

```text
left_query
right_query
left_top10_urls
right_top10_urls
shared_exact_urls
shared_exact_url_count
shared_domains
shared_domain_count
domain_jaccard
observed dominant page types
observed intent pattern
analyst_evidence_verdict
supporting notes
```

Allowed analyst evidence verdicts are project-specific labels:

```text
SERP_COMPATIBLE
SERP_DIVERGENT
MIXED_OR_INSUFFICIENT
```

Meanings:

```text
SERP_COMPATIBLE
= evidence is consistent with one search job / potentially one page target, but final clustering remains Step 10.

SERP_DIVERGENT
= evidence shows materially different intent/result/page patterns; final structural action remains downstream.

MIXED_OR_INSUFFICIENT
= current SERP does not justify a confident compatibility conclusion.
```

No fixed URL-overlap count automatically assigns these verdicts.

## 12. YMB interaction gate for this exact step

Before first YMB command, state actual active service/mode/manual state.

Required mode:

```text
YMB STEP OBJECTIVE
= collect complete reusable ordinary Yandex TOP-10 evidence for the frozen Step-09 manifest.

YMB REQUIRED MODE
= service=search; SEARCH_BATCH_API_V1; ordinary Search only; no GenSearch; explicit sequential paid `next` actions.

YMB REQUIRED SAVED RESULT
= complete provider result + normalized ranked rows + request/cost/outcome truth for the current item.

YMB COMPLETENESS CHECK
= current item has a known outcome and the complete required payload/rows are durably preserved and readable.

YMB STOP CONDITION
= if complete current-item evidence is not saved/verified, STOP; no next paid Search action.
```

Required markers:

```text
YMB_INTERACTION_GATE_EMBEDDED = true
YMB_PROJECT_RESULT_DEFINED = true
YMB_REQUIRED_STORAGE_DEFINED = true
YMB_COMPLETENESS_CHECK_DEFINED = true
YMB_STOP_ON_INCOMPLETE_RESULT = true
```

`OUTCOME_UNKNOWN` blocks automatic replay and further progression until governed recovery.

## 13. Relevant prior errors and non-repeat controls

### Step 03 error — request success mistaken for data completion

Control:

```text
HTTP 200 / request_executed / SUCCEEDED != PROJECT_RESULT_COMPLETE
```

Every Search response must be fully preserved and verified before the next paid request.

### Step 07 error — structural/accounting QA mistaken for semantic QA

Control:

Search batch success does not prove the intent/page-boundary interpretation. Provider QA and analytical QA are separate gates.

### Step 08 error — external research collected but unsupported method states invented

Control:

Every Step-09 state, selection rule, threshold, route and PASS condition is included in the source-to-method trace above. No unsupported automatic overlap threshold is allowed.

### Non-exact duplicate risk

Control:

All 8 active duplicate groups receive direct comparison evidence before any later merge. Lexical similarity alone does not merge them.

### Region-mixing risk

Control:

Baseline comparisons use Moscow `213`. Any geo-specific alternate region is explicit and cannot be mixed silently with baseline evidence.

## 14. Required artifacts after execution

```text
STEP_09_SEARCH_PROBE_MANIFEST.tsv
STEP_09_REVIEW_SEARCH_COVERAGE.tsv
STEP_09_SERP_RESULTS.tsv
STEP_09_SERP_COMPARISONS.tsv
STEP_09_EVIDENCE_QUESTION_DECISIONS.tsv
STEP_09_SEARCH_RECONCILIATION.md
STEP_09_SEARCH_ACCEPTANCE_2026-08-29.md
```

Bridge-native durable job/checkpoint evidence remains authoritative provider provenance and is referenced from the job artifacts rather than replaced by a summary.

## 15. Step 09 PASS gate

Step 09 may pass only if:

```text
1. paid manifest frozen before first provider request;
2. manifest provider queries <= authorized maxRequests;
3. actual provider cost <= authorized maxCostRub;
4. all mandatory coverage obligations represented in the manifest;
5. all 944 REVIEW_SEARCH rows remain mapped to evidence questions or explicitly UNRESOLVED;
6. all 8 active non-exact duplicate groups receive direct comparison evidence;
7. every attempted provider item has known governed outcome;
8. every successful item has complete raw + normalized result preserved;
9. observed result counts reconcile with saved ranked rows;
10. no automatic replay after OUTCOME_UNKNOWN;
11. comparison evidence is produced without a universal hard overlap threshold;
12. provider/data QA = PASS;
13. analytical interpretation QA = PASS;
14. material evidence questions are either resolved or explicitly MIXED_OR_INSUFFICIENT;
15. no final cluster/page ownership/structural action is silently performed;
16. provider requests/cost/results/errors reconcile quantitatively.
```

If the first <=80 request tranche cannot satisfy material evidence coverage, Step 09 remains open. Additional Search requires a new explicit owner authorization and cost ceiling.

## 16. Method verdict

```text
METHOD_VERDICT = PROJECT_SPECIFIC_BUT_REASONED
STEP_09_PERMANENT_METHOD = UNVALIDATED
STEP_09_JOB_SPECIFIC_PRE_STEP_REVIEW_COMPLETE = true
STEP_09_EXECUTION_ALLOWED = false
OWNER_AUTHORIZATION_REQUIRED = true
```

This job-specific method is externally grounded, but it must not be promoted into permanent universal Step-09 methodology automatically.

## 17. Plain-language summary

### Зачем нужен этот шаг

Чтобы посмотреть, что Яндекс реально показывает людям по спорным запросам, и перестать решать границы страниц только по словам и нашей интуиции.

### Что он решает

Он показывает, какие запросы ведут к похожим поисковым результатам и пользовательским задачам, а какие на самом деле требуют другого типа ответа. Это даёт доказательства для следующей кластеризации и выбора страниц.

### Как мы это делаем

Не отправляем в Яндекс все тысячи фраз подряд. Сначала фиксируем ограниченный набор запросов, который покрывает реальные спорные вопросы, затем по каждому сохраняем полный ТОП‑10 Москвы и сравниваем реальные URL, типы страниц и интент. Если данных не хватает, оставляем вопрос нерешённым, а не придумываем ответ.
