# KW-001 / OKNO-MSK — STEP 08 SEARCH-STAGE SEMANTIC FREEZE — CORRECTED METHOD REVIEW

Date: 2026-08-29
Status: **CORRECTED AFTER METHOD AUDIT / ORIGINAL BUSINESS-ROUTE MODEL SUPERSEDED**

## 1. Whole Kwork goal

Deliver a complete, evidence-backed semantic set and site/page structure recommendation for Yandex ordinary Search plus selective AI-search evidence, with client-ready artifacts and final QA.

## 2. Full roadmap at this correction

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
| **8. Freeze Search-stage semantic set** | **Freeze exact Search input and route unresolved evidence** | **🔁 CORRECTED / COMPLETE AFTER METHOD FIX** |
| 9. Ordinary Yandex Search validation | Resolve material intent/page-boundary uncertainty with real SERP evidence | ⬜ NOT STARTED |
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

## 3. Step-8 purpose

Create a stable, reproducible handoff between accepted Step-07C phrase decisions and ordinary Yandex Search validation.

The freeze is a **project-specific workflow control**, not an official Yandex SEO stage. Its job is to preserve the exact input and show which unresolved rows require a real next evidence action.

## 4. Source-to-method traceability

Every material methodological statement below is tied to a direct source. Project-specific mechanics are labelled separately.

### 4.1 Query relevance is about user need and whether the site can answer it

Official Yandex Webmaster:
https://yandex.ru/support/webmaster/ru/recommendations/targeting

Yandex states that Search answers users' questions, ranking depends on how well page content matches query wording, and suitable key phrases should describe the product/service and user need.

**Supported rule:** Search-stage semantic relevance must be judged against user need + known site/business offer. There is no separate external `business evidence route` implied by this guidance.

### 4.2 Query selection is about suitable/promising queries for the site

Official Yandex Webmaster query selection:
https://yandex.ru/support/webmaster/ru/service/queries-selection

Yandex describes selecting suitable target queries, analyzing their potential, and examining pages/market results.

**Supported rule:** demand discovery and query potential are evaluated for the site; an invented `REVIEW_BUSINESS` queue is not part of the source methodology.

### 4.3 Search intent and business potential are different attributes, not different evidence providers

Ahrefs Keyword Intent, updated 2026-03-13:
https://ahrefs.com/blog/keyword-intent/

Ahrefs describes keyword/search intent as the reason behind a query and uses it as an early filter for whether a keyword belongs in a strategy. It separately discusses Business Potential as how naturally the product can be presented as a solution.

Ahrefs Keyword Strategy, updated 2026-03-13:
https://ahrefs.com/blog/keyword-strategy/

The workflow separately scores business potential and maps keywords to search intent/content type.

**Supported rule:** `business fit/potential` is an evaluation dimension; `search intent` is another evaluation dimension. Neither source supports representing them as parallel downstream evidence channels called `SEARCH`, `BUSINESS`, and `SEARCH_AND_BUSINESS`.

### 4.4 Clustering/page decisions follow intent compatibility

Semrush Keyword Clustering, 2025-10-29:
https://www.semrush.com/blog/keyword-clustering/

Semrush defines keyword clustering around queries that share the same search intent and can be targeted on one page.

Semrush Keyword Mapping, updated 2026-07-27:
https://www.semrush.com/blog/keyword-mapping/

Mapping connects target keywords/topics with existing or planned pages and is affected by changes in search results.

**Supported rule:** final clustering and page mapping stay downstream of Search/intent evidence; Step 8 must not invent page ownership or merge decisions.

### 4.5 Existing query/page evidence is a Search layer

Official Yandex Webmaster query groups:
https://www.yandex.ru/support/webmaster/ru/service/search-queries

Yandex explicitly shows which pages appear for which queries.

**Supported rule:** query/page compatibility is Search evidence, not an internal-business-priority evidence channel.

## 5. What was wrong in the original Step-8 method

The original pre-step invented these routing states:

```text
REVIEW_BUSINESS
REVIEW_SEARCH_AND_BUSINESS
```

No cited source defined or required those states.

The specific logical error was:

```text
business fit / business priority
was converted from an evaluation dimension
into a supposed future evidence source / resolution route
```

That produced a route that this workflow could not actually execute.

The empty `REVIEW_BUSINESS = 0` was a symptom: instead of asking whether the category was necessary, the original analysis defended a schema that the data did not use and the sources did not support.

## 6. Root cause

```text
EXTERNAL_RESEARCH_WAS_COLLECTED
but
SOURCE_TO_METHOD_TRACEABILITY_WAS_NOT_ENFORCED
```

The research was treated as general background support. I did not require every material invented state/operation to answer:

```text
Which source supports this?
OR
What concrete project/data necessity requires this project-specific mechanic?
What real next action can execute it?
```

As a result, a convenient symmetric taxonomy was added after the research even though the research did not justify it.

## 7. Corrected Step-8 routing model

Only real next-action states remain:

```text
CORE_CANDIDATE
= accepted Step-07C KEEP; retained as an eligible working candidate.

REVIEW_SEARCH
= unresolved phrase requiring ordinary Search/SERP evidence to clarify intent, relevance, result type, boundary or compatibility.

REVIEW_DEFERRED
= retained unresolved evidence for which immediate Search acquisition is not justified in the bounded next stage; association-only evidence is the current class.

EXCLUDED_PRESERVED
= accepted Step-07C exclusion preserved for audit, with no active Search route.
```

These exact state names are **PROJECT-SPECIFIC**. Their justification is operational minimality: each state maps to a real workflow action and none pretends that an unavailable internal-business source will later resolve the row.

## 8. Business relevance vs internal business priority

Correct distinction:

```text
PUBLIC BUSINESS RELEVANCE / FIT
= can the known public offer/site reasonably satisfy the query once intent is understood?

INTERNAL BUSINESS PRIORITY
= margin, capacity, strategic growth priority, operational preference, etc.
```

Public business relevance is part of semantic/strategy evaluation together with intent. Internal business priority is not a Step-8 evidence route. If unavailable, it remains an explicit limitation and can constrain later prioritization; it must not create an unresolved semantic-routing class.

External support:
- Yandex user-need/site-fit guidance: https://yandex.ru/support/webmaster/ru/recommendations/targeting
- Ahrefs business-potential + intent separation: https://ahrefs.com/blog/keyword-strategy/
- Ahrefs intent guidance: https://ahrefs.com/blog/keyword-intent/

## 9. Corrected execution contract

Input remains the accepted Step-07C universe:

```text
exact phrase keys = 2840
KEEP = 1388
REVIEW = 1118
EXCLUDE_* = 334
```

Correct routing rules:

```text
KEEP -> CORE_CANDIDATE
REVIEW association-only -> REVIEW_DEFERRED
all other accepted REVIEW reasons -> REVIEW_SEARCH
EXCLUDE_* -> EXCLUDED_PRESERVED
```

No Step-07C semantic status may be rewritten by Step 8.

## 10. Corrected pass gate

```text
Step-08 rows = 2840/2840
CORE_CANDIDATE = 1388
all REVIEW routed = 1118/1118
REVIEW_SEARCH = 944
REVIEW_DEFERRED = 174
EXCLUDED_PRESERVED = 334
forbidden REVIEW_BUSINESS states = 0
forbidden REVIEW_SEARCH_AND_BUSINESS states = 0
silent drops = 0
Step-07C status rewrites = 0
non-exact duplicate groups preserved = 9/9
non-exact duplicate auto-merges = 0
Search/provider calls during Step 8 = 0
```

## 11. Non-repeat control added by this correction

Before any future step is authorized, every material state, decision rule, threshold, route or operation must have a **source-to-method trace**:

```text
METHOD_ELEMENT
→ SOURCE / PROJECT EVIDENCE
→ WHAT THE SOURCE ACTUALLY SUPPORTS
→ PROJECT-SPECIFIC PART, IF ANY
→ REAL EXECUTABLE NEXT ACTION
```

If an invented category has no supporting source, no proven project necessity, or no executable next action, it must be removed before execution.

Canonical correction:

```text
RESEARCH_COLLECTED != METHOD_VALIDATED
SOURCE_TO_METHOD_TRACEABILITY_REQUIRED = true
UNSUPPORTED_DECISION_STATE_FORBIDDEN = true
NON_EXECUTABLE_EVIDENCE_ROUTE_FORBIDDEN = true
```

## 12. What Step 8 still does NOT decide

```text
no new Wordstat
no ordinary Search requests
no final clustering
no page ownership
no structural actions
no cannibalization verdict
no AI evidence
no internal margin/capacity assumptions
no final prioritization
```

## 13. Corrected method verdict

```text
ORIGINAL_STEP08_METHOD = CORRECTION_REQUIRED
BUSINESS_ROUTE_TAXONOMY = REJECTED
CORRECTED_STEP08_METHOD = PROJECT_SPECIFIC_BUT_SOURCE_TRACED
STEP08_EXECUTION_RESULT = REBUILT_AND_RECONCILED
```

### Зачем нужен этот шаг

Чтобы перед Search зафиксировать точный набор запросов и не менять вход задним числом.

### Что он решает

Сохраняет все принятые, спорные и исключённые строки и показывает только реальные дальнейшие действия, не придумывая источники информации, которых у нас нет.

### Как мы это делаем

Сохраняем Step-07C без переписывания, отправляем действительно спорные intent/relevance случаи в Search, association-only оставляем отложенными и сохраняем исключения для аудита.