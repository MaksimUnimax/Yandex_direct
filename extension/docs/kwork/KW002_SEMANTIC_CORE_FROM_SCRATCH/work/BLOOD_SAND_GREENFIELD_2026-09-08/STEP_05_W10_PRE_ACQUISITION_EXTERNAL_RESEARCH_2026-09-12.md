# KW-002 Blood & Sand — Step05 W10 pre-acquisition external research

Date: 2026-09-12  
Status: **CURRENT PRE-STEP RESEARCH / NO PROVIDER CALLS / W09 STEP04 AUTHORITY ONLY**

Repository: `MaksimUnimax/Yandex_direct`  
Branch: `roadmap/kwork-productization-2026-08-28`  
Job: `BLOOD_SAND_GREENFIELD_2026-09-08`  
Handoff: `KW002-BS-W10`  
Preparation base HEAD checked before materialization: `ea2707f757475f24550f5b89b1e453e44631abe3`

## 1. Current upstream authority

Current Step04 authority is the accepted W09 result, not the older post-sanitation queue/gate.

Current accepted Step04 queue contains 13 rows:

```text
SEARCH-GAP CANDIDATES REQUIRING STEP05 RECONCILIATION: PSQ001, PSQ004, PSQ005
OWNER FACT FIRST/ONLY: PSQ002, PSQ003, PSQ009, PSQ012, PSQ013
EXISTING EVIDENCE REUSE / NO BLIND REPLAY: PSQ006, PSQ007, PSQ008, PSQ010
DEFER TO LATER INTENT/SERP: PSQ011
PROVIDER_READY_NOW = 0
```

The historical Step05 E013 request for `!чётки` is durable evidence and is closed for Step05 acquisition. It must not be replayed merely because the queue was rebuilt.

## 2. Exact questions researched before Step05

The research checked:

1. what current Wordstat top-query evidence means and its time window;
2. whether region/device filtering is current provider functionality;
3. which query operators are supported and what `!` actually proves;
4. current provider quotas and relevant limits;
5. current provider pricing for GetTop;
6. the current repository-side Bridge command contract;
7. whether current public provider documentation and the Bridge command schema are identical;
8. what may and may not be inferred from search-demand evidence.

## 3. External sources and source-to-method trace

| source_id | source | publisher / class | checked | supports | Step05 application | claim boundary |
|---|---|---|---|---|---|---|
| S05-EXT-01 | https://yandex.ru/support2/wordstat/en/content/api-structure | Yandex Wordstat / official provider docs | 2026-09-12 | `/v1/topRequests` returns last-30-days popular queries containing the phrase and similar queries; supports optional regions/devices; POST JSON | Step05 probes are current-demand diagnostics, may use geographic/device controls where useful | This public Wordstat API page does **not** document the Bridge-specific `numPhrases` field |
| S05-EXT-02 | https://yandex.ru/support2/wordstat/ru/content/operators | Yandex Wordstat / official provider docs | 2026-09-12 | operators including `!`, quotes, `[]`, grouping; operators work in Top queries and Regions | use bounded operators only when they isolate the unresolved question; `!` may fix word form | operator match does not prove business relevance, inventory, intent or page ownership |
| S05-EXT-03 | https://yandex.cloud/en/docs/overview/concepts/quotas-limits | Yandex Cloud / official service limits | 2026-09-12 | Wordstat statistics: 10 requests/sec, 100 requests/hour; max associations 20 | W10 must remain far below quota and sequential; quota is not a reason to batch needless probes | general Search API result-count limits must not be silently treated as a Wordstat GetTop row-depth contract |
| S05-EXT-04 | https://yandex.cloud/en/blog/digest-april-2026 | Yandex Cloud / official product/pricing publication | 2026-09-12 | Wordstat GA pricing from 2026-05-18: GetTop 20 RUB/1000 calls; GetDynamics 20/1000; RegionsDistribution 50/1000; RegionsTree free | one GetTop diagnostic call has estimated provider price `0.02 RUB`; cost must still be checked again immediately before execution | price source establishes tariff, not semantic value of any proposed probe |
| S05-EXT-05 | https://yandex.cloud/en/docs/search-api/api-ref/grpc/Wordstat/ | Yandex Cloud / official API reference | 2026-09-12 | Search API Wordstat methods include GetTop/GetDynamics/GetRegionsDistribution/GetRegionsTree; GetTop covers last 30 days | confirms current method semantics used for provider planning | does not by itself prove the local Bridge command envelope or its accepted fields |
| S05-EXT-06 | https://yandex.cloud/ru/blog/digest-july-2026 | Yandex Cloud / official current product material | 2026-09-12 | Wordstat API is used for demand, regional differences, top queries, related queries and SEO work | corroborates Step05 use as targeted demand/coverage evidence | does not authorize using demand to infer client inventory/business facts |

## 4. Current Bridge implementation authority

Repository evidence checked on the live branch:

- `extension/src/shared/wordstat_protocol.js`
- `extension/src/service_worker.js`
- `extension/src/shared/product.js`
- `extension/docs/PHASE_1_WORDSTAT_IMPLEMENTATION_PLAN.md`
- historical accepted `STEP_05_E013_WORDSTAT_EVIDENCE_RECEIPT_2026-09-10.md`

Current local protocol accepts `WORDSTAT_API_V1` and methods:

```text
getTop
getDynamics
getRegionsDistribution
getRegionsTree
```

For current Bridge `getTop`, repository code validates:

```text
phrase: required
numPhrases: integer 1..2000, default 100
regions: string array, default ["225"]
devices: DEVICE_ALL | DEVICE_DESKTOP | DEVICE_PHONE | DEVICE_TABLET
```

The current Bridge adapter targets Yandex Search API Wordstat `/v2/wordstat/...` endpoints. The current public Wordstat documentation also exposes a public `/v1/...` API form with a different request surface.

Therefore the governing distinction for Step05 is:

```text
CURRENT OFFICIAL PROVIDER DOCS = method meaning / operators / pricing / quotas
CURRENT REPOSITORY BRIDGE CODE = executable command schema actually available to this project
HISTORICAL E013 = proven durable execution evidence
```

Do not rewrite one layer into another. In particular, do not claim `numPhrases=2000` is a current public Wordstat `/v1` documented field merely because the Bridge supports it and E013 successfully returned 2000 rows.

Current repository product identity is `Yandex Marketing Bridge 0.1.2`; the historical E013 receipt records execution under bridge `0.1.4`. W10 must use the current live Bridge contract at execution time rather than assuming the historical bridge version remains current.

## 5. Method implications for Step05

### 5.1 Targeted expansion is not a second primary acquisition

Step05 may only query a question that remains unresolved after reconciliation against all durable Step02/03/05 evidence.

```text
OLD EVIDENCE EXISTS -> REUSE FIRST
SEMANTICALLY EQUIVALENT PROBE -> REJECT
OWNER BUSINESS FACT -> OWNER, NOT WORDSTAT
LATER INTENT/SERP QUESTION -> DEFER
GENUINELY NEW SEARCH-VOCABULARY GAP -> MAY BECOME CANDIDATE
```

### 5.2 One new probe at a time

If a candidate survives W10 reconciliation, select exactly one first executable GetTop probe. Persist and remotely read back its complete result before considering another paid call.

### 5.3 Operators are isolation tools, not semantic truth

`!`, quotes, word-order and grouping operators may reduce ambiguity. They never prove:

- that the client sells a form/material/product;
- that an effect/claim is true;
- final user intent;
- final SEO cluster;
- query-to-page ownership.

### 5.4 Negative evidence has value

Every candidate must state in advance what a weak/empty/non-distinguishing result would close or defer. A probe with no useful negative outcome is low-information-gain and should not execute.

### 5.5 Current W09 queue supersedes the old Step05 provisional split

The old 2026-09-11 Step05 gate treated PSQ006/007/008 as possible provider candidates. W09 later reconciled them to durable existing evidence. They are no longer provider candidates.

Only `PSQ001`, `PSQ004`, `PSQ005` enter W10 as **candidate questions to challenge**, and none is provider-ready until the Work pass proves non-duplication and incremental information gain.

## 6. Required anti-regression controls

```text
CURRENT_STEP04_AUTHORITY = W09_ACCEPTED
CURRENT_QUEUE_ROWS = 13
PROVIDER_READY_NOW_AT_START = 0
BLIND_E013_REPLAY = false
OWNER_FACT_GATED_ROWS_SENT_TO_PROVIDER = 0
EXISTING_EVIDENCE_REUSE_ROWS_REPROBED = 0
DEFERRED_SERP_INTENT_ROW_SENT_TO_PROVIDER = 0
PROBE_LITERAL_DUPLICATES = 0
PROBE_SEMANTIC_DUPLICATES_WITHOUT_OPERATOR_OR_SCOPE_GAIN = 0
INCREMENTAL_INFORMATION_GAIN_EXPLICIT = true
NEGATIVE_RESULT_VALUE_EXPLICIT = true
STOP_CONDITION_EXPLICIT = true
PROVIDER_CALLS_IN_W10_PRE_ACQUISITION_WORK = 0
STEP06_STARTED = false
```

Before publication, re-fetch remote HEAD and reconcile any governing-authority changes. Mutable current-state files from a stale base must never overwrite newer authority.

## 7. Pre-step conclusion

The current method remains consistent with fresh official Yandex documentation and current repository Bridge evidence, with one correction to the old Step05 draft: **the current W09 queue has only three search-gap candidates to investigate, not six, and none is authorized for provider execution yet.**

Preparation may proceed to a no-provider Work reconciliation pass. Provider execution requires a separate Main ChatGPT release after that pass is read back and accepted.
