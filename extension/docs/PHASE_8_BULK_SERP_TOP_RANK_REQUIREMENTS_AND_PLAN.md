# PHASE 8 — Bulk SERP / TOP-overlap / rank evidence

Date: 2026-08-28

Status: **PASS / CLOSED / IN MAIN**

## 1. Product objective

Phase 8 productizes the already accepted ordinary Yandex Search hand into a durable high-volume evidence job for:

```text
keyword list + region
→ one bounded ordinary Yandex Search request per keyword
→ durable per-key checkpoint
→ ranked URL/domain evidence
→ deterministic TOP/domain projections
→ paged TOP-overlap evidence
→ bounded target-domain rank evidence
→ ChatGPT clustering / interpretation / client artifact
```

This phase is not an autonomous SEO clustering engine. The Bridge owns deterministic acquisition, persistence, projection, safety and recovery; ChatGPT remains the semantic analyst.

Permanent worker boundary:

```text
ChatGPT Plus
= keyword-set strategy / clustering judgment / page-job decisions / competitor interpretation / QA / client artifact

Yandex Marketing Bridge
= paid Search queue / exactly-once-safe execution / persisted SERPs / deterministic domain+rank projections / progress+budget truth

Human owner/operator
= authorization / credential / irreducible owner-live boundary
```

## 2. Market authority

Canonical market evidence:

`extension/docs/FREELANCE_ORDER_CAPABILITY_MATRIX.md`

Phase 8 directly addresses the documented P1 gap:

```text
F-013 semantic core + TOP/SERP clustering
F-014 Wordstat core + TOP grouping
F-015 standalone TOP/SERP clustering, supplied base = 500 keys
```

The exact blocker already identified by the market matrix is:

```text
durable bulk SERP queue/checkpoint/resume + cost/progress controls
```

The current bounded service can handle roughly ~100 keys manually/operationally. Phase 8 targets repeatable handling up to the documented 500-key class without asking ChatGPT to remember which paid requests already ran.

## 3. Accepted production baseline

Phase 8 starts only from accepted `main` after:

```text
Phase 6 Wordstat batch = CLOSED / ACCEPTED
Gate A O-001 comparative methodology = PASS
GenSearch proxy validation = PASS
GenSearch production hand = integrated into main
```

Exact main at Phase-8 requirements start:

```text
67aeee71a42bdc0edb516341297987c1d1d26972
```

No Phase-8 production byte is authorized to modify accepted ordinary Search or GenSearch semantics merely to create this requirements document.

## 4. Existing primitives to reuse

### 4.1 Ordinary Search provider contract

Existing `SEARCH_API_V1` ordinary `search` already supports:

```text
POST /v2/web/search
queryText
searchType
region
page
groupsOnPage
familyMode
fixTypoMode
sortMode
sortOrder
groupMode
docsInGroup
maxPassages
l10n
```

The accepted XML normalizer already returns ranked records:

```text
rank
url
domain
title
snippet
modtime
```

Phase 8 must reuse this exact ordinary Search provider path rather than invent a new SERP provider.

### 4.2 Batch lifecycle model

Phase 6 already introduced a provider-generic durable batch model with states equivalent to:

```text
PENDING
CLAIMED
REQUEST_STARTED
SUCCEEDED
FAILED_TERMINAL
OUTCOME_UNKNOWN
SKIPPED
CANCELLED
```

It already carries:

```text
stable command fingerprint
request id
worker-session identity
request_executed truth
automatic_retry=false
request/cost totals
pause/resume/cancel
recovery after worker restart
OUTCOME_UNKNOWN => no automatic replay
```

Phase 8 should reuse this model. Do not build a second lifecycle/state machine for Search.

### 4.3 Existing Search economics

Current bridge estimate:

```text
ordinary synchronous Search = 0.488 RUB/request
GenSearch = 5.08 RUB/request
```

Phase 8 first slice uses ordinary `search` only. It must never silently switch a bulk TOP job to `genSearch`.

## 5. First-slice protocol boundary

Candidate production protocol:

```text
SEARCH_BATCH_API_V1
SEARCH_BATCH_RESULT_V1
service = search
```

This is orchestration inside the existing Search service. It must not create a sixth registry service.

Required management/execution actions:

```text
start
next
status
pause
resume
cancel
projection
overlapPage
```

Provider boundary rule:

```text
start/status/pause/resume/cancel/projection/overlapPage = 0 provider requests
one explicit next = at most 1 ordinary Search provider request
```

No hidden loop and no automatic provider retry.

## 6. `start` contract

`start` defines a frozen job manifest before any paid request occurs.

Required/allowed semantic fields for the first slice:

```text
action = start
jobId = optional explicit stable id
queries[] = 1..500
searchType = existing Search enum, default SEARCH_TYPE_RU
region = existing Search region semantics, default 225 for RU
groupsOnPage = 1..100, default 10
maxRequests = explicit positive integer <= deduplicated query count
maxCostRub = explicit non-negative job ceiling
confirmBillable = literal true
```

First slice intentionally fixes provider-detail fields not needed for TOP evidence to existing safe ordinary-Search defaults:

```text
page = 0
docsInGroup = 1
groupMode = GROUP_MODE_FLAT
sortMode = SORT_MODE_BY_RELEVANCE
sortOrder = SORT_ORDER_DESC
familyMode = FAMILY_MODE_MODERATE
fixTypoMode = FIX_TYPO_MODE_ON
```

Do not expose arbitrary raw Search request bodies through the batch protocol.

Exact duplicate queries may be mechanically deduplicated after normalized command construction, with input count and duplicate count preserved.

`start` itself must return:

```text
request_executed = false
automatic_retry = false
requests_started = 0
```

## 7. Paid execution contract

Each safe pending query becomes one normalized ordinary `SEARCH_API_V1` command owned by the durable job.

Before provider initiation, `next` must:

1. load authoritative persisted job state;
2. recover/fail closed if an earlier `REQUEST_STARTED` outcome is unknown;
3. check job request/cost limits;
4. check normal Search policy/credential admission;
5. claim exactly one safe pending item;
6. persist the claim;
7. persist `REQUEST_STARTED` + request id before the provider boundary;
8. execute exactly one ordinary Search request;
9. persist terminal payload/state before caller delivery.

If provider initiation may have happened and outcome is unknown:

```text
item = OUTCOME_UNKNOWN
job progression = blocked
same item = never automatically replayed
```

## 8. Persistence contract

Persist at minimum:

```text
job id / schema / revision
frozen start manifest
normalized per-query Search command
command fingerprint
item lifecycle state
request id / worker session id
request_started_at / completed_at
request_executed
automatic_retry
estimated cost
provider/result error truth
normalized ordinary Search result payload
ranked result rows
job progress totals
stop/pause/cancel reason
```

Credential secrets must never be stored in the job evidence.

Successful provider evidence must survive service-worker suspension/restart and tab close.

## 9. Deterministic SERP projection

For every successful item, Phase 8 may derive a pure deterministic projection from the already normalized Search result.

Required projection semantics:

```text
query_text
region
search_type
requested_groups
observed_result_count
ranked_results[] = {rank,url,domain,title}
top_domains[] = unique domains in first-observed rank order
```

For duplicate domains in the same SERP, `top_domains` keeps the domain once at its best/first rank.

Projection must never rewrite provider rank truth or infer semantic similarity.

## 10. `projection` management action

`projection` is local-only and must not contact Yandex.

Purpose:

- page through completed query evidence;
- optionally calculate rank evidence for a small explicit target-domain set;
- let ChatGPT consume a large batch without dumping an unbounded payload into one message.

Candidate bounded fields:

```text
jobId
offset >= 0
limit = 1..100
topN = 1..100
targetDomains[] = optional, max 20
```

For each returned query, target-domain evidence is mechanical:

```text
domain
best_rank_within_observed_topN | null
matching_urls[]
```

Important boundary:

> `rank` means rank inside the sampled ordinary Yandex Search result for this exact job/region/time. It is not Google rank, not longitudinal rank tracking, and not a promise of universal/consumer-personalized position.

## 11. `overlapPage` management action

TOP overlap is deterministic repetitive computation and belongs in the Bridge as evidence, but final clustering judgment remains ChatGPT work.

`overlapPage` must use only persisted successful SERPs and must make **zero** provider requests.

For a selected `topN`, each query is represented by its unique top-domain set. Pairwise evidence may include:

```text
left_item_id / left_query
right_item_id / right_query
left_domain_count
right_domain_count
shared_domains[]
shared_count
union_count
jaccard = shared_count / union_count
left_containment = shared_count / left_domain_count
right_containment = shared_count / right_domain_count
```

Because 500 keys produce 124,750 pairs, overlap output must be paged/bounded rather than emitted as one giant chat payload.

Candidate fields:

```text
jobId
topN = 1..100
offset >= 0
limit = 1..1000
```

The Bridge must not turn these overlap numbers into an unexplained final semantic cluster label.

## 12. Cost and budget safety

The job manifest must carry explicit economics before execution.

At current bridge estimate:

```text
100 ordinary Search requests ≈ 48.8 RUB
500 ordinary Search requests ≈ 244 RUB
```

Therefore Phase 8 must require explicit bounded job authorization and preserve both:

```text
maxRequests
maxCostRub
```

The job ceiling may be stricter than global Search policy but must never bypass a stricter global policy.

Every result/progress surface must preserve:

```text
requests_started
estimated_cost_rub
max_requests
max_cost_rub
next_safe_action / stop_reason
```

No automatic retry after provider initiation.

## 13. What remains ChatGPT work

Do not hard-code these decisions into Phase 8:

- keyword selection strategy;
- whether 10, 20, 50 or 100 SERP results are decision-relevant;
- semantic cluster labels;
- threshold that automatically means `same page` or `different page`;
- page split/merge decisions;
- intent interpretation;
- competitor importance;
- new-page/cannibalization decisions;
- final workbook/report structure and prose.

ChatGPT may use overlap evidence plus business context, Wordstat, ordinary Search snippets, GenSearch where selectively justified, Webmaster/Metrika/Direct evidence and site structure to make those judgments.

## 14. Explicit non-goals

Phase 8 first slice does not include:

- Google Search;
- exact consumer-personalized Yandex ranking;
- browser scraping of Yandex consumer SERPs;
- GenSearch batching;
- bulk image search;
- autonomous final semantic clustering;
- automatic SEO changes/publication;
- Webmaster/Metrika/Direct writes;
- external Ahrefs/Keys.so metrics;
- historical rank tracking scheduler.

Longitudinal measurement can be a later job revision/scheduled product after this one-shot evidence hand is stable.

## 15. Compatibility invariants

Phase 8 must preserve:

- exactly five service registry entries;
- existing `SEARCH_API_V1` ordinary search behavior;
- existing `genSearch` behavior and provenance separation;
- existing Search credential ownership;
- Wordstat batch behavior and storage;
- shared provider batch lifecycle semantics;
- Manual/Autorun owner/conversation fences;
- no blind replay after unknown outcome;
- prior Wordstat/Webmaster/Metrika/Direct behavior;
- no provider writes.

Search batch storage must use its own versioned key and may reuse the generic model but must not mix Search jobs into the Wordstat storage map.

## 16. Test-first implementation sequence

```text
P8-00 fetch exact live main; freeze commit/tree/baseline identities
P8-01 audit SearchProtocol + Search XML normalizer + provider-batch model + Wordstat batch adapter/runtime reuse points
P8-02 freeze SEARCH_BATCH_API_V1 protocol and storage contract in tests
P8-03 model/runtime tests: start has zero provider calls; one next <= one provider call
P8-04 implement Search batch protocol/runtime with ordinary search only
P8-05 persist per-item SERP payload before delivery
P8-06 implement pure projection + target-domain sampled-rank evidence
P8-07 implement bounded paged overlap projection
P8-08 recovery tests: worker restart/tab close/pause-resume/double-submit/stale event/no replay
P8-09 request/cost ceiling tests including 500-key economics without real provider calls
P8-10 regression: ordinary Search + GenSearch + Wordstat batch + Webmaster + Metrika + Direct
P8-11 controlled browser gate with local provider stub; real_yandex_requests = 0
P8-12 freeze exact candidate + deterministic packaging + complete applicable pre-delivery gate
P8-13 minimal owner-live acceptance on a small real ordinary-Search batch
P8-14 integrate exact accepted bytes to main; post-merge identity proof; close Phase 8
```

No runtime implementation should precede the P8-00/P8-02 test/model contract.

## 17. Acceptance target

A minimal real owner-live acceptance should prove a small set of distinct ordinary Search queries with one explicit region:

```text
start = 0 provider requests
N safe next actions = exactly N provider requests
all successful item payloads durable
status/pause/resume = 0 provider requests
resume does not replay completed queries
worker recovery does not replay completed queries
request_executed / request ids / cost totals truthful
projection returns ranked domains/URLs from persisted payloads
overlapPage returns mathematically correct pair evidence with 0 provider requests
target-domain sampled rank matches persisted SERP rows
OUTCOME_UNKNOWN contract blocks automatic replay
ordinary Search and GenSearch regressions remain PASS
five-service registry remains unchanged
```

The gate validates the reliability of the evidence hand, not the quality of ChatGPT's final semantic clusters.

## 18. Authorized next action

```text
fetch exact current main
→ create governed Phase-8 dev branch
→ P8-00 exact baseline evidence
→ P8-01 architecture audit
→ P8-02 protocol/model tests before product runtime changes
```

No project-owner action is required during this engineering preparation.

## 19. Final closure

```text
PHASE8_SEARCH_BATCH_FINAL_ACCEPTANCE_PASS
source authority = 0377d6e1f176d4b7ddd8553c0099e02a4f1e8716
extension tree = 446fed6970c5fec627be34c3893800dc4511c6c9
extension/src tree = bdad1e87a2537d8646e480ca23f8068c3dced17e
freeze run = 33143237276 / SUCCESS
frozen ZIP sha256 = 8f6ba92dbe1f592a62c66cd250ed942e261f56deffbe87117371bd9c481e6332
owner-live job = p8-owner-live-2026-08-28
owner-live real provider requests = 2
owner-live automatic retries = 0
owner-live estimated cost = 0.976 RUB
main integration = ebd697e5733a7d40d13401d4c02b82a75711231c
postmerge gate = 33144396638 / SUCCESS
postmerge Node regression = 118/118
postmerge controlled browser real Yandex requests = 0
```

Phase 8 is closed. No further owner-live ceremony is required.
