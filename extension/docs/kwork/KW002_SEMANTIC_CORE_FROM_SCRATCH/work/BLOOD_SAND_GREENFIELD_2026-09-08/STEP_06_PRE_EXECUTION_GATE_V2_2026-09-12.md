# KW-002 Blood & Sand — Step06 corrected pre-execution gate V2

Date: 2026-09-12
Status: **PRE-STEP PACKAGE PREPARED / OWNER-FACING DISCLOSURE REQUIRED IN CHAT / SEARCH EXECUTION NOT RELEASED**

## 1. Kwork goal

Build a from-scratch semantic core and planned site architecture for Yandex with clean business/source lineage, current demand evidence, current ordinary Search evidence for final decisions, later AI-search reconciliation, and client-ready deliverables.

## 2. Full roadmap / state entering Step06 preparation

| Step | Purpose | Current state |
|---|---|---|
| 00 | Scope/source freeze | COMPLETE / PASS |
| 01 | Business + assortment model | COMPLETE / PASS / 76 of 76 Ozon rows |
| 02 | Seed/acquisition map | COMPLETE / V2 PASS |
| 03 | Primary Wordstat + durable evidence | COMPLETE / 79 of 79 durable |
| 03A | Normalization / safe dedupe | COMPLETE / 24,576 identities / 25,979 RAW |
| 03B | Conservative sanitation | CORRECTED AUTHORITY ACCEPTED |
| 04 | Preliminary family/topic/task triage | W09 CURRENT AUTHORITY ACCEPTED |
| 05 | Targeted expansion / coverage control | COMPLETE / PASS CURRENT SNAPSHOT |
| 06 | Current Yandex organic competitor discovery | **NOT STARTED — CURRENT PRE-STEP UNIT** |
| 07 | Competitor semantic expansion | NOT STARTED |
| 08 | Competitor-derived Wordstat | NOT STARTED |
| 09 | Candidate semantic master + reserve freeze | NOT STARTED |
| 10 | Row-level relevance/task/intent/priority | NOT STARTED |
| 11 | Delivery-scope/Search-stage freeze | NOT STARTED |
| 12 | Current ordinary Yandex Search evidence for full frozen Search-stage set | NOT STARTED |
| 13 | SERP + task-first clustering | NOT STARTED |
| 14 | Query→page ownership + Search-only IA | NOT STARTED |
| 15 | AI diagnostic case selection | NOT STARTED |
| 16 | AI-search evidence | NOT STARTED |
| 17 | Search-vs-AI reconciliation | NOT STARTED |
| 18 | Final core + IA + Page Jobs + internal links | NOT STARTED |
| 19 | Client deliverables | NOT STARTED |
| 20 | Final QA / recipient acceptance | NOT STARTED |
| 21 | Revision/productization measurement | NOT STARTED |
| 22 | Final handoff / close | NOT STARTED |

## 3. Completed / remaining

Completed through Step05. Step06 actual Search collection has not begun. Steps07–22 have not begun.

Step05 current bounded conclusion includes W10C001 executed once with `SUCCESS_WITH_ZERO_ROWS` and no new semantic rows; Step05 queue is reconciled 13/13 for the current snapshot.

## 4. Step06 goal

Identify the domains and pages that **currently compete in ordinary Yandex organic results** across materially different retained demand directions.

```text
BUSINESS RIVAL != SEARCH COMPETITOR
```

A marketplace, publisher, directory or other indirect site may compete in Search without being a direct business rival.

## 5. Problem Step06 solves

The client supplied no SEO competitor list and the site is new, so there is no reliable existing-domain ranking overlap to start from. Competitors must be discovered from current Search evidence around retained demand directions rather than guessed from business similarity.

## 6. Required output

Step06 execution must eventually produce:

1. durable per-query Search result evidence;
2. request/provenance register;
3. normalized ranked result ledger;
4. domain recurrence matrix by query and coverage direction;
5. URL/page evidence register;
6. result-type classification;
7. current Search competitor registry with inclusion reasoning;
8. single-observation / recurring / selected distinctions;
9. quantitative QA/accounting;
10. remote readback and Step06 closure authority.

Step07 may use only the accepted Step06 competitor registry.

## 7. Relevant prior failures reread

### F03 — provider success mistaken for durable project completion

Observed earlier in this same job during Step03: provider outcomes existed but durable feed-forward was incomplete until recovery.

Non-repeat control for Step06:

```text
one Search provider result
→ receive complete normalized result envelope
→ persist every returned result row + required provenance
→ GitHub remote readback
→ row/field reconciliation
→ only then next provider request
```

### F06+ — preliminary family mistaken for final cluster/page

Step04 W09 families are discovery/triage authority only.

Non-repeat control:

```text
STEP04 FAMILY != FINAL INTENT
STEP04 FAMILY != FINAL SERP CLUSTER
STEP04 FAMILY != PAGE
```

Step06 uses families to choose competitor-discovery probes only.

### Current preparation incident

V1 Step06 preparation violated the required owner-facing pre-step protocol and also contained an accounting error and over-strict rawData claim. V1 is superseded for execution by the V2 correction package.

## 8. Fresh method/provider research

Authority: `STEP_06_PRE_STEP_EXTERNAL_RESEARCH_V2_2026-09-12.md`.

Freshly checked on 2026-09-12:

- official Yandex Web Search API request/response schema;
- current Search API text-search behavior and depth/defaults;
- current quotas/limits;
- current pricing;
- region 225 = Russia;
- current Yandex guidance showing search can mix result types/interpretations;
- Ahrefs arbitrary-keyword-list competitor discovery practice;
- Semrush organic competitor/shared-keyword practice;
- current repository Bridge Search implementation.

## 9. Representative query plan V2

Authority: `STEP_06_REPRESENTATIVE_QUERY_MANIFEST_V2_2026-09-12.tsv`.

Accounting:

```text
QUERY_ROWS = 22
UNIQUE_QUERY_IDS = 22
UNIQUE_QUERY_TEXTS = 22
COVERAGE_DIRECTIONS = 12
ANALYST_INVENTED_QUERY_TEXTS = 0
PROVIDER_CALL_STATUS_NOT_RELEASED = 22/22
```

Coverage directions:

```text
GENERIC_PRODUCT
COMMERCIAL_PRODUCT
AUTOMOBILE_USE
ROSARY_OBJECT
QUALIFIED_CATALOG_SYMBOL
ZODIAC_PRODUCT
EFFECT_AUDIENCE
SELECT_GIFT
USE_CARE
MEANING_HISTORY
DIY_CRAFT
ACQUIRE_ACCESS
```

These are representative Step06 discovery probes, not final keywords or page targets.

Excluded from direct Step06 probe authority are collision-only/foreign/noise families, zero-member gaps and owner-fact-dependent directions that do not currently justify competitor selection.

## 10. Planned ordinary Search contract

After a separate execution release:

```text
service = search
method = search
searchType = SEARCH_TYPE_RU
region = 225
page = 0
groupsOnPage = 20
groupMode = GROUP_MODE_FLAT
docsInGroup = 1
sortMode = SORT_MODE_BY_RELEVANCE
sortOrder = SORT_ORDER_DESC
familyMode = FAMILY_MODE_MODERATE
fixTypoMode = FIX_TYPO_MODE_OFF
responseFormat = FORMAT_XML
```

GenSearch/AI-search are outside Step06.

### Why `fixTypoMode=OFF`

The query set is already observed demand vocabulary. Disabling provider autocorrection keeps the probe identity explicit and avoids silently changing the exact query being used for competitor discovery. This is a project-specific control, not an external SEO standard.

### Why `groupsOnPage=20`

Current Yandex XML Search allows 1..100 groups and currently defaults to 20. Step06 uses top-20 as a bounded competitor-discovery heuristic.

```text
20 returned rows = TOP20_CUTOFF_BY_DESIGN
20 returned rows != COMPLETE SERP
provider max 250 != required Step06 depth
```

Step12 later has a separate owner-frozen `FULL_SERP_COVERAGE` requirement for the final Search-stage phrase set. Step06 does not satisfy or replace Step12.

## 11. Planned provider volume / cost

```text
PLANNED_SEARCH_REQUESTS = 22
MAX_RESULTS_PER_QUERY_BY_PLAN = 20
MAX_NORMALIZED_RESULT_ROWS = 440
DAY_SYNC_PRICE = 0.488 RUB/request
NIGHT_SYNC_PRICE = 0.366 RUB/request
DAY_MAX_ESTIMATED_COST = 10.736 RUB
NIGHT_MAX_ESTIMATED_COST = 8.052 RUB
```

Provider quota is much larger than this plan; quota capacity is not execution permission.

## 12. Execution sequencing

Do not use a multi-request burst before durability is proven.

```text
prepare bounded local job / command identity
→ execute ONE provider request
→ receive full normalized result envelope
→ persist evidence file + request provenance
→ remote GitHub readback
→ reconcile result_count / results[] / required fields
→ only then authorize next item
```

If current runtime later proves a batch `nextN` mode capable of preserving and remotely persisting each item before another request, that would require a separately proven execution path. It is not assumed here.

## 13. Required durable evidence per query

At minimum:

```text
query_id
query_text
request_id
received_at / observation snapshot
search_type
region
page
groups_requested
result_count
rank
url
domain
title
snippet where present
modtime where present
provider status
request_executed truth
automatic_retry truth
cost/provenance where supplied
```

All returned result rows must be retained. Null optional fields remain null; rows are not dropped because a title/snippet/modtime is absent.

A top-domain summary or representative sample is not sufficient evidence.

## 14. Outcome contract

```text
SUCCESS_WITH_RESULTS
  -> persist complete normalized result envelope;
  -> reconcile rows/fields/readback;
  -> then analyze domain recurrence.

SUCCESS_WITH_ZERO_RESULTS
  -> exact-query/current-region/current-settings snapshot zero only;
  -> no universal competitor/no-demand conclusion.

SUCCESS_BUT_EVIDENCE_INCOMPLETE
  -> unresolved;
  -> do not count domains;
  -> stop before next provider request.

VALIDATION_FAILURE
  -> no Search evidence;
  -> correct under separate release.

PROVIDER_FAILURE
  -> no semantic competitor conclusion;
  -> persist failure truth and stop.

OUTCOME_UNKNOWN
  -> no competitor conclusion;
  -> blind retry forbidden.

NORMALIZATION_FAILURE_AFTER_REQUEST
  -> provider request may have executed but usable Step06 evidence is unresolved;
  -> stop; do not infer from partial/chat fragments.
```

## 15. Domain recurrence / selection contract

No universal threshold is claimed.

Analytical evidence tiers:

```text
SINGLE_OBSERVATION
= domain observed once in the selected query set.

RECURRING_WITHIN_DIRECTION
= domain observed across 2+ selected queries in one coverage direction.

CROSS_DIRECTION_RECURRING
= domain observed in 2+ different coverage directions.
```

These are candidate-evidence tiers only. Selection into the competitor registry additionally requires relevance/result-type review. Numeric recurrence alone does not force competitor inclusion.

## 16. Result-type classification

Project-specific analytical labels:

```text
SPECIALTY_SELLER_OR_BRAND
MARKETPLACE
INFORMATIONAL_PUBLISHER
DIRECTORY_OR_AGGREGATOR
UGC_OR_SOCIAL_OR_MEDIA
OTHER
UNKNOWN
```

A type is assigned only when the visible domain/page evidence supports it; otherwise `UNKNOWN`.

## 17. Claim boundaries

- ranking for `амулет защиты` or `талисман удачи` does not prove the claimed effect;
- zodiac queries retain the product-vs-astrology ambiguity boundary;
- informational/DIY rankings do not prove the future site needs those pages;
- catalog-name queries do not prove separate page need;
- current rank/competitor status is a snapshot, not permanent truth;
- Step06 competitor discovery does not perform Step07 competitor-topic extraction;
- Step06 does not perform Step12 full final Search coverage or Step13 clustering.

## 18. Bridge gate

### Repository implementation verified

Current branch source supports ordinary synchronous `/v2/web/search`, Search result normalization and complete JSON formatting of the normalized result envelope.

Current repository normalization preserves every XML `<doc>` into `results[]` with:

```text
rank
url
domain
title
snippet
modtime
```

This is compatible with the existing Level1 allowance for a durable normalized Search result reference, provided every returned row is persisted/read back.

### Remaining blocker: installed runtime/source mismatch

```text
OWNER_OBSERVED_INSTALLED_RUNTIME = 0.1.4
CURRENT_BRANCH_PRODUCT_VERSION = 0.1.2
```

No `0.1.4` source/commit was found in the current repository during corrected preparation.

Before a paid Search request:

```text
RECONCILE INSTALLED SEARCH RUNTIME SCHEMA/SOURCE
OR
PERFORM A NON-PROVIDER RUNTIME/SCHEMA HANDSHAKE THAT PROVES THE ACCEPTED COMMAND PATH
→ THEN ISSUE SEPARATE STEP06 SEARCH EXECUTION RELEASE
```

No paid Search call is authorized by this V2 gate.

## 19. Work gate

Current Step06 acquisition/analysis plan is bounded to at most 440 normalized result rows plus simple deterministic recurrence tables. Ordinary chat does not require sampling or row dropping for this unit.

```text
WORK_TRIGGER = NOT_MET_FOR_STEP06_PREPARED_UNIT
WORK_HANDOFF = NOT_REQUIRED
```

If actual data shape later exceeds reliable ordinary-context processing, the existing Work rule must be re-evaluated rather than sampling.

## 20. PASS conditions for eventual Step06 execution

Step06 may close only if all applicable conditions pass:

```text
OWNER_FACING_PRE_STEP_DISCLOSURE = PASS before execution
INSTALLED_RUNTIME_SEARCH_CONTRACT = RECONCILED
SEPARATE_SEARCH_EXECUTION_RELEASE = PRESENT
AUTHORIZED_QUERY_ITEMS = EXECUTED_OR_EXPLICITLY_RESOLVED
ALL_PROVIDER_OUTCOMES_KNOWN_OR_GOVERNED
ALL_SUCCESSFUL_RESULTS_DURABLY_PERSISTED
RETURNED_RESULT_ROWS = DURABLE_RESULT_ROWS
REMOTE_READBACK = PASS
QUERY/REGION/SETTINGS_PROVENANCE_COMPLETE = true
NO_CLIENT_NAMED_COMPETITOR_ONLY_INCLUSION = true
SELECTED_COMPETITORS_HAVE_CURRENT_SERP_LINEAGE = true
BUSINESS_RIVAL_NOT_CONFLATED_WITH_SEARCH_COMPETITOR = true
STEP07_NOT_EXECUTED_DURING_STEP06 = true
STEP12_FULL_COVERAGE_NOT_FALSLY_CLAIMED = true
END_OF_STEP_ACCOUNTING = PASS
QUALITY_SCORE >= 9/10
NO_OPEN_CRITICAL_DEFECT = true
```

## 21. Current decision

```text
STEP06_PRE_STEP_V1 = SUPERSEDED_FOR_EXECUTION
STEP06_PRE_STEP_V2 = PREPARED
OWNER_FACING_DISCLOSURE = REQUIRED_IN_CURRENT_CHAT_BEFORE_ANY_EXECUTION
SEARCH_EXECUTION_RELEASED = false
SEARCH_CALLS_ALLOWED_NOW = 0
GENSEARCH_CALLS_ALLOWED_NOW = 0
WORDSTAT_CALLS_ALLOWED_NOW = 0
AI_SEARCH_CALLS_ALLOWED_NOW = 0
STEP06_ACTUAL_EXECUTION = NOT_STARTED
STEP07 = NOT_STARTED
STEP08 = NOT_STARTED
```

## 22. Next physical action after owner-facing disclosure

Perform the non-provider installed-runtime/Search-schema reconciliation. If it passes, recheck live HEAD/current provider docs and materialize a separate first Search execution release. Only that later release may authorize the first ordinary Search request.
