# KW-002 Blood & Sand — Step06 current Yandex organic competitor discovery preparation gate

Date: 2026-09-12
Status: **PREPARATION PASS / EXECUTION RELEASE HOLD / STEP06 NOT STARTED**

## 1. Purpose

Step06 will identify current Yandex organic SERP competitors from current Search API evidence across representative retained demand directions.

Hard boundary:

```text
BUSINESS RIVAL != SEARCH COMPETITOR
STEP06 != COMPETITOR SEMANTIC EXPANSION
STEP06 != COMPETITOR WORDSTAT
STEP06 != FINAL INTENT/SERP CLUSTERING/PAGE OWNERSHIP
STEP06 != GENSEARCH/AI SEARCH
```

Step07 may later inspect accepted current search competitors for missed vocabulary/topics. Step08 may later test genuinely new competitor-derived topics in Wordstat. Neither is started here.

## 2. Authority inputs

Accepted inputs:

- `CLIENT_SUPPLIED_BRIEF.md`
- `STEP_04_CURRENT_AUTHORITY_FAMILY_TRIAGE_2026-09-11.tsv`
- `STEP_04_W09_MAIN_CHATGPT_REMOTE_READBACK_ACCEPTANCE_2026-09-12.md`
- `STEP_05_W10_V3_FINAL_CLOSURE_2026-09-12.md`
- `STEP_06_PRE_STEP_EXTERNAL_RESEARCH_AND_SOURCE_TRACE_2026-09-12.md`
- `STEP_06_REPRESENTATIVE_QUERY_MANIFEST_V1_2026-09-12.tsv`
- Level1/Level2 current method authorities.

Step04 W09 remains preliminary-family authority only. Nothing in Step06 may retroactively promote a Step04 family into a final cluster/page.

## 3. Representative-query coverage design

Prepared manifest contains:

```text
QUERY_COUNT = 20
COVERAGE_DIRECTIONS = 10
QUERIES_PER_DIRECTION = 2 except ROSARY_OBJECT = 1 and DIY_CRAFT = 1, balanced by other directions
ALL_QUERY_TEXTS = OBSERVED STEP04 REPRESENTATIVE PHRASES
ANALYST_INVENTED_QUERY_TEXTS = 0
PROVIDER_CALLS = 0
```

Directions:

1. generic product;
2. commercial product;
3. automobile use;
4. rosary object;
5. qualified catalog symbol;
6. zodiac product;
7. effect/audience with strict claim boundary;
8. selection/gift;
9. use/care;
10. meaning/history + DIY informational edge.

The purpose is controlled current-competitor discovery across materially different retained directions. This is not a sample used to decide final semantic relevance, intent, cluster boundaries or page ownership. Those remain later full-method stages.

## 4. Intended provider contract after release blockers are cleared

Planned ordinary Search request template:

```text
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
fixTypoMode = FIX_TYPO_MODE_ON
responseFormat = FORMAT_XML
GenSearch = forbidden in Step06
```

Why top 20:

- Step06 needs recurring current competitors, not the provider's maximum-depth universe;
- top 20 gives two ordinary result pages' worth of ranked organic evidence under one bounded Search API request while keeping tail noise controlled;
- provider maximum `250` and XML maximum `groupsOnPage=100` are technical ceilings, not methodological targets;
- returning exactly 20 results means `TOP20_CUTOFF_BY_DESIGN`, never `SERP_COMPLETE`.

This depth choice is a KW002 project heuristic, not a Yandex provider claim.

## 5. Planned request accounting and current cost

```text
PLANNED_SEARCH_QUERIES = 20
PLANNED_PROVIDER_REQUESTS = 20
MAX_RESULTS_PER_QUERY_BY_PLAN = 20
MAX_NORMALIZED_SERP_ROWS_BY_PLAN = 400
DAY_PRICE_PER_SYNC_REQUEST = 0.488 RUB
DAY_MAX_ESTIMATED_COST = 9.76 RUB
NIGHT_PRICE_PER_SYNC_REQUEST = 0.366 RUB
NIGHT_MAX_ESTIMATED_COST = 7.32 RUB
GENSEARCH_REQUESTS = 0
WORDSTAT_REQUESTS = 0
```

Price authority: fresh official Yandex Search API pricing checked 2026-09-12 and recorded in the Step06 source trace.

## 6. Execution sequencing — no multi-call leapfrogging

Even though repository Search batch supports `nextN`, Step06 must obey Level1 F03.

Therefore intended execution sequence is:

```text
1. create/start bounded Search batch job locally (no provider request)
2. execute exactly ONE batch `next` / one Search provider request
3. obtain complete lossless provider RAW + request provenance
4. persist RAW to canonical job evidence path
5. remote GitHub readback
6. reconcile query/result counts and fields
7. only then execute the next provider request
8. repeat until manifest exhausted or a stop condition fires
```

Hard rule for Step06:

```text
SEARCH_BATCH_NEXTN_PROVIDER_BURST = FORBIDDEN
until lossless raw persistence/readback semantics are changed by an explicit method authority.
```

This prevents 20 successful provider calls from becoming chat/local-only evidence before durable feed-forward.

## 7. Per-query outcome contract

```text
SUCCESS_WITH_RESULTS
  -> evidence only after complete RAW persistence + remote readback;
  -> normalize rank/url/domain/title/snippet for analysis;
  -> mark TOP20_CUTOFF_BY_DESIGN if 20 rows returned.

SUCCESS_WITH_ZERO_RESULTS
  -> bounded zero result for exact query/region/settings/current snapshot;
  -> not proof that no competitor exists generally.

SUCCESS_BUT_RAW_INCOMPLETE
  -> query unresolved; do not count domains; do not issue next provider request.

VALIDATION_FAILURE
  -> no SERP evidence; preserve failure; stop until corrected/released.

PROVIDER_FAILURE
  -> no SERP evidence; preserve failure; stop until corrected/released.

OUTCOME_UNKNOWN
  -> no semantic/competitor answer; blind retry forbidden; stop and recover separately.
```

`NO_RETRY != NEGATIVE_EVIDENCE` remains active.

## 8. Domain/URL evidence model

For every successful query preserve at minimum:

```text
query_id
query_text
request_id
timestamp/snapshot identity
search_type
region
page
groups_requested
rank
provider domain
URL
title
snippet where present
raw evidence file/ref
```

Domain normalization for counting is conservative:

- lowercase;
- remove trailing dot;
- do not silently merge distinct subdomains/hosts into one business entity;
- any registrable-domain consolidation requires explicit review and retained raw host lineage.

## 9. Competitor-registry classification

Every observed domain remains evidence even if it is not a direct seller.

Result-type labels to be assigned from evidence, with `UNKNOWN` where unsupported:

```text
SPECIALTY_SELLER_OR_BRAND
MARKETPLACE
INFORMATIONAL_PUBLISHER
DIRECTORY_OR_AGGREGATOR
UGC_OR_SOCIAL_OR_MEDIA
OTHER
UNKNOWN
```

These are SERP-role types, not client business-competitor claims.

### Accepted competitor evidence tiers

`CROSS_FAMILY_SERP_COMPETITOR`
- domain observed in at least 2 materially different `coverage_direction` values.

`FAMILY_SPECIFIC_SERP_COMPETITOR`
- domain recurs across at least 2 queries inside one direction but not across directions; retain as direction-specific competitor.

`SINGLE_OBSERVATION_ONLY`
- one occurrence only; record it but do not promote it to selected semantic competitor without later independent evidence.

No domain may be accepted because the client named it: client supplied no competitor list anyway.

For Step07 candidate selection, preserve type diversity and prioritize current recurrence/relevance rather than third-party traffic estimates.

## 10. Query-family claim boundaries

- PSF011 effect/audience queries are used to observe SERP competition only; ranking pages do not prove mystical/physical effects.
- informational/DIY queries can surface informational SERP competitors; they do not prove that Blood & Sand should create corresponding pages.
- zodiac queries retain the product-vs-astrology collision boundary.
- qualified catalog-symbol queries do not prove that every catalog title deserves a page.
- current ranking is snapshot evidence, not permanent competitor status.

## 11. Prepared recipient outputs after execution

If execution later completes successfully, Step06 must materialize:

1. complete per-request RAW Search evidence files;
2. request/provenance register;
3. normalized SERP row ledger;
4. domain recurrence matrix by query and coverage direction;
5. URL/page evidence register;
6. typed Search competitor registry;
7. included/excluded/single-observation reasoning;
8. Step06 QA and accounting report;
9. current Step06 closure/readback authority.

## 12. Current blocking release gates

### HOLD A — installed runtime/source drift

Owner's immediately preceding Bridge output says runtime `0.1.4`; current GitHub source says product `0.1.2`.

Required before release:

```text
prove current installed Search runtime schema/source,
or sync the authoritative 0.1.4 runtime source into a reviewable authority;
then re-run Search contract QA.
```

### HOLD B — lossless Search RAW persistence not proven

Current repository Search path normalizes Base64/XML provider body and stores normalized rows, not the original provider body.

Required before release:

```text
lossless original provider result must remain recoverable,
with request identity/provenance,
and must be exportable/persistable to GitHub for remote readback before the next provider call.
```

A compact normalized projection is useful for analysis but is not a substitute for required durable provider evidence.

## 13. Gate verdict

```text
REMOTE_BASE_HEAD = 89ba3907196ea4f4f5b19388c0146f0b06d7db48
BASE_DRIFT = NONE
FRESH_EXTERNAL_RESEARCH = PASS
OWNER_SOURCE_DISCLOSURE = PASS_IN_CURRENT_DIALOG_AND_DURABLE_TRACE
STEP06_LEVEL2_BOUNDARY = PASS
REPRESENTATIVE_QUERY_MANIFEST = PREPARED_20_QUERIES
QUERY_LINEAGE_TO_STEP04 = PASS
CURRENT_PRICE_LIMITS = PASS
SEARCH_EXECUTION_CONTRACT = PREPARED
COMPETITOR_CLASSIFICATION_CONTRACT = PREPARED
LOSSLESS_RAW_GATE = HOLD
INSTALLED_RUNTIME_AUTHORITY_GATE = HOLD
PROVIDER_EXECUTION_RELEASE = false
SEARCH_CALLS_ALLOWED_NOW = 0
GENSEARCH_CALLS_ALLOWED_NOW = 0
WORDSTAT_CALLS_ALLOWED_NOW = 0
STEP06_STARTED = false
```

## 14. Next allowed unit

Resolve the two Bridge execution blockers without making a Search provider request:

1. reconcile installed runtime 0.1.4 against reviewable source/schema;
2. prove or patch lossless Search RAW preservation/export;
3. test that persistence path without paid provider execution where possible;
4. re-read current remote HEAD and current official pricing/schema;
5. then issue a separate Step06 provider execution release for the prepared 20-query manifest.

Do not start Step07 or Step08.
