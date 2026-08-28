# CURRENT STATE — Yandex Marketing Bridge

Status: **PHASES 0–8 CLOSED — O-001 COMPARATIVE GATE PASS — GENSEARCH + BULK SERP/TOP/RANK HANDS ACCEPTED IN MAIN — PHASE 9 GOOGLE GAP = NEXT RESEARCH PHASE**  
Updated: 2026-08-28

Always fetch live `main` HEAD and exact file/tree identity before a workflow-stage transition or product write.

---

## 1. Permanent operating model

```text
ChatGPT Plus
= analyst / planner / semantic architect / QA / report author

Yandex Marketing Bridge
= authenticated, bounded, repeatable provider hands

Human owner/operator
= authorization/access boundary and irreducible local/live actions
```

The extension productizes acquisition, persistence, deterministic projections, policy, recovery and safe execution. It does not replace ChatGPT with hard-coded SEO judgment where model reasoning from evidence is the stronger worker.

Permanent credential rule:

```text
Wordstat/Search cloud credential = separate
Webmaster OAuth = separate
Metrika OAuth = separate
Direct OAuth = separate
no credential consolidation/reuse project is authorized
```

Service registry remains exactly:

```text
wordstat
search
webmaster
metrika
direct
```

---

## 2. Closed provider phases

### Phase 1 — Wordstat

```text
status = LIVE PASS / CLOSED
protocol = WORDSTAT_API_V1
methods = getTop,getDynamics,getRegionsDistribution,getRegionsTree
```

### Phase 2 — ordinary Yandex Search

```text
status = LIVE PASS / CLOSED
protocol = SEARCH_API_V1
ordinary endpoint = POST /v2/web/search
accepted original Search source = b7869180c229356a6b3d51ac980ec3da5df4c23c
```

Ordinary Search remains the regional SERP evidence hand. Its normalized result preserves ranked URL/domain/title/snippet evidence.

### Lifecycle button gating

```text
status = OWNER LIVE PASS / CLOSED
accepted source = 939e880f820e52beae9dcbcedc86d5cd9e13b075
```

### Phase 3 — Webmaster

```text
status = LIVE PASS / CLOSED
methods = listHosts,getSummary,getDiagnostics,getPopularQueries
writes = disabled
```

Authority:
`extension/tests/PHASE3_WEBMASTER_OWNER_LIVE_PASS_2026-08-26.md`

### Phase 4 — Metrika

```text
status = LIVE PASS / CLOSED
methods = listCounters,getCounter,getTrafficSummary,getTrafficByTime
writes = disabled
```

Authority:
`extension/tests/PHASE4_METRIKA_OWNER_LIVE_PASS_2026-08-26.md`

### Phase 5 — Yandex Direct

```text
status = PASS / CLOSED
methods = listCampaigns,listAdGroups,listAds,listKeywords,getCampaignPerformance
writes/bids/budgets/finance = disabled
```

Final closure authority:
`extension/tests/PHASE5_DIRECT_FINAL_CLOSURE_2026-08-27.md`

---

## 3. Phase 6 — Semantic Core / durable Wordstat batch CLOSED

Phase 6 is no longer a requirements-only phase. The first productionized batch hand is accepted and in `main`.

Protocol:

```text
WORDSTAT_BATCH_API_V1
WORDSTAT_BATCH_RESULT_V1
service = wordstat
```

Management/execution model:

```text
start / status / pause / resume / cancel = no provider request
one explicit next = at most one Wordstat provider request
```

The shared provider-batch lifecycle now provides durable per-item state, stable fingerprints, persisted request identity, request/cost bounds, pause/resume/cancel, worker recovery and fail-closed `OUTCOME_UNKNOWN` behavior.

Frozen Phase-6 product authority:

```text
source_commit = 34f50688268970f4863dddb2089a33d891b91372
extension/src_tree = adab628a8ec328fa5079ae35f45005a0ee7de2c1
artifact_id = 9649039904
inner_zip_sha256 = 05d587b02f5fc08c64ebbf1fbd5d14765491c7b9931195c23262e1f42d692c2f
```

Independent complete gate:

```text
workflow_run = 33079158530
source suite = 81/81
packaged suite = 81/81
real_yandex_requests = 0
product byte identity = PASS
```

Owner-live bounded acceptance:

```text
3 distinct Wordstat seeds
3 successful provider requests
3 distinct request ids
pause/resume = no replay
final status = COMPLETED
requests_started = 3
estimated_cost_rub = 0.06
automatic_retry = false
```

Authority:
`extension/tests/PHASE6_WORDSTAT_BATCH_FINAL_ACCEPTANCE_2026-08-27.md`

**PHASE6_WORDSTAT_BATCH_FINAL_ACCEPTANCE_PASS**

---

## 4. O-001 — AI-Native Semantic Rebuild: methodology gate PASS

The clean comparative methodology experiment is complete.

Valid clean Pass A was frozen before any Alice evidence was opened in that clean context. Pass B then added the frozen canonical consumer-Alice evidence and compared action-level semantic/page-job decisions.

Verdict:

```text
AI_NATIVE_COMPARATIVE_GATE_PASS
```

The controlled real-project comparison showed material decision-level uplift/de-risking in areas including page-job scope, hybrid content-commerce requirements, launch priority, source-worthiness and contamination control.

This proves methodology value on the controlled dataset. It does not prove revenue uplift and does not guarantee AI citation/ranking/traffic.

Canonical comparison:
`extension/tests/AI_NATIVE_BLOOD_SAND_COMPARISON_2026-08-27.md`

---

## 5. Official GenSearch hand: VALIDATED / IN PRODUCTION MAIN

Official Yandex GenSearch is implemented as a bounded method of the existing Search service:

```text
service = search
protocol = SEARCH_API_V1
method = genSearch
endpoint = POST /v2/gen/search
result mode = generative
```

It does not create a sixth service and does not reuse Webmaster/Metrika/Direct credentials.

Bounded proxy validation against the frozen consumer-Alice evidence completed with:

```text
representative_roots = 5
SAME_OR_STRONGLY_ALIGNED = 4
PARTIALLY_ALIGNED = 1
MATERIALLY_DIFFERENT = 0
NOT_COMPARABLE = 0
systematic_contradictions = 0
```

Verdict:

```text
AI_NATIVE_GENSEARCH_PROXY_VALIDATION_PASS
```

Important provenance boundary remains permanent:

```text
GEN_SEARCH_QUERY_OBSERVED != ALICE_FANOUT_OBSERVED
GEN_SEARCH_ANSWER != CONSUMER_ALICE_ANSWER
GEN_SEARCH_SOURCE != CONSUMER_ALICE_SOURCE
```

GenSearch is accepted as a distinct repeatable structured AI-search evidence hand, not as consumer-Alice equivalence.

Production contract:
`extension/docs/AI_NATIVE_GENSEARCH_PRODUCTION_CONTRACT_2026-08-28.md`

Proxy validation:
`extension/tests/AI_NATIVE_GENSEARCH_PROXY_VALIDATION_FINAL_2026-08-28.md`

Production integration:

```text
main_commit = 67aeee71a42bdc0edb516341297987c1d1d26972
extension/src_tree = 04dc6d015977270fb064b669ee03d04f6e130612
postmerge_gate_run = 33140809518
postmerge_gate = SUCCESS
node_tests = 99/99
controlled_browser_real_yandex_requests = 0
```

---

## 6. Current production capability boundary

Current `main` can provide ChatGPT with these controlled hands:

```text
Wordstat single requests
Wordstat durable batch orchestration
ordinary Yandex Search / ranked SERP evidence
bounded official GenSearch evidence
Webmaster read evidence
Metrika read evidence
Direct read evidence
```

ChatGPT remains responsible for:

```text
research plan
seed/query selection
semantic cleanup
intent interpretation
clustering by user job
page split/merge/reject decisions
keyword → target-page mapping
cannibalization decisions
source interpretation
recommendations
client workbooks/reports
```

---

## 7. Phase 8 — Bulk SERP / TOP-overlap / rank evidence CLOSED / IN MAIN

Phase 8 is accepted and no longer an active development phase.

Production protocol:

```text
SEARCH_BATCH_API_V1
SEARCH_BATCH_RESULT_V1
service = search
queries[] up to 500
start/status/pause/resume/cancel/projection/overlapPage = 0 provider requests
one explicit next = at most one ordinary Search provider request
```

Accepted product identity:

```text
source authority = 0377d6e1f176d4b7ddd8553c0099e02a4f1e8716
extension tree = 446fed6970c5fec627be34c3893800dc4511c6c9
extension/src tree = bdad1e87a2537d8646e480ca23f8068c3dced17e
freeze run = 33143237276 / SUCCESS
frozen ZIP sha256 = 8f6ba92dbe1f592a62c66cd250ed942e261f56deffbe87117371bd9c481e6332
```

Owner-live acceptance:

```text
job = p8-owner-live-2026-08-28
queries = 2
successful provider requests = 2
requests_started = 2
estimated_cost_rub = 0.976
automatic_retry = false
outcome_unknown = 0
status/projection/overlapPage provider requests = 0
```

Observed deterministic evidence included `market.yandex.ru` at best observed rank 3 for `печать велеса`, `ru.wikipedia.org` at rank 1 for `алатырь`, and pairwise TOP-10 domain overlap `shared_count=0`, `union_count=15`, `jaccard=0`.

Production integration:

```text
main integration commit = ebd697e5733a7d40d13401d4c02b82a75711231c
postmerge gate = 33144396638 / SUCCESS
Node regression = 118/118
controlled browser real Yandex requests = 0
product immutability = PASS
```

Final authority:
`extension/tests/PHASE8_SEARCH_BATCH_FINAL_ACCEPTANCE_2026-08-28.md`

**PHASE8_SEARCH_BATCH_FINAL_ACCEPTANCE_PASS**

---

## 8. Authorized autonomous next sequence

```text
Phase 8 = CLOSED / IN MAIN
→ Phase 9 research: official/stable/legal Google organic evidence options
→ evaluate source quality, cost, privacy and ToS before freezing any provider contract
→ do not implement a Google hand before provider research and a test-first contract
→ preserve the current five-service registry unless a governed architecture decision explicitly changes it
```

Phase 10 crawler/importer evidence work remains lower priority than Phase 9 provider research.

---

## 9. Open blockers

```text
Phase 6 = NONE / PASS
O-001 comparative methodology gate = NONE / PASS
GenSearch repeatable official hand = NONE / ACCEPTED
Phase 8 bulk SERP/TOP/rank = NONE / PASS / IN MAIN
owner action now = NONE
next engineering = Phase 9 Google organic provider research
```

No further Phase-8 owner ceremony is required.
