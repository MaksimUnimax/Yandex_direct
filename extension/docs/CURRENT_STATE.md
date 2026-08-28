# CURRENT STATE — Yandex Marketing Bridge

Status: **PHASES 0–6 CLOSED — O-001 COMPARATIVE GATE PASS — GENSEARCH PRODUCTION HAND ACCEPTED — PHASE 8 BULK SERP/TOP/RANK = ACTIVE NEXT ENGINEERING PHASE**  
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

## 7. Phase 8 — Bulk SERP / TOP-overlap / rank evidence ACTIVE NEXT

Market authority identifies durable bulk ordinary-Search orchestration as the next high-leverage gap for F-013/F-014/F-015-style TOP clustering and rank evidence.

Canonical requirements:

`extension/docs/PHASE_8_BULK_SERP_TOP_RANK_REQUIREMENTS_AND_PLAN.md`

Target first slice:

```text
SEARCH_BATCH_API_V1
service = search
queries[] up to 500
one explicit next <= one ordinary Search provider request
durable checkpoint/resume
no replay of completed/unknown items
persisted ranked URL/domain results
local paged projections
local paged TOP/domain-overlap evidence
bounded sampled target-domain rank evidence
explicit request/cost ceilings
```

Final semantic clustering thresholds/labels remain ChatGPT work rather than hidden hard-coded SEO logic.

Phase-8 dev branch:

```text
phase8/bulk-serp-top-rank-2026-08-28
base main = 67aeee71a42bdc0edb516341297987c1d1d26972
```

At the time of this state update, Phase-8 work has changed documentation only; no Phase-8 `extension/src` product byte has been modified yet.

---

## 8. Authorized autonomous next sequence

```text
P8-00 freeze exact live-main baseline identity
P8-01 audit SearchProtocol/Search XML/provider-batch reuse points
P8-02 define SEARCH_BATCH_API_V1 + storage/projection contracts in tests first
P8-03 focused model/runtime tests
P8-04 minimal Search batch runtime over ordinary search only
P8-05 durable per-item SERP persistence
P8-06 deterministic projection/rank evidence
P8-07 bounded paged overlap projection
P8-08 restart/tab-close/pause/resume/double-submit/stale-event/no-replay tests
P8-09 request/cost bounds including 500-key economics without real provider traffic
P8-10 all prior-service regression including GenSearch and Wordstat batch
P8-11 controlled browser gate with local provider stub
P8-12 freeze exact candidate + complete applicable pre-delivery gate
P8-13 minimal owner-live Search batch acceptance
P8-14 integrate accepted bytes to main and close Phase 8
```

During active development, use focused tests plus impacted regressions. Full pre-delivery is run only after an exact candidate is frozen.

---

## 9. Open blockers

```text
Phase 6 = NONE
O-001 comparative methodology gate = NONE / PASS
GenSearch repeatable official hand = NONE / ACCEPTED
Phase 8 requirements = NONE
Phase 8 engineering preparation = autonomous
owner action now = NONE
```

The next expected owner-only action is the eventual minimal real Search-batch acceptance after the exact Phase-8 candidate has passed its independent complete gate. Do not invent earlier owner ceremonies.
