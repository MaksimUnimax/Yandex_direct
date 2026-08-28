# ROADMAP v0.14 — Yandex Marketing Bridge

Status: **ACTIVE**  
Updated: 2026-08-28

## Governing product model

```text
ChatGPT Plus = brain / analyst / planner / semantic architect / QA
Yandex Marketing Bridge = controlled provider hands
Human owner/operator = authorization and irreducible execution boundary
```

The extension automates repetitive deterministic acquisition, persistence, policy, recovery and safe execution. It does **not** replace ChatGPT with hard-coded SEO judgment where model reasoning from evidence is the stronger worker.

Permanent credential rule:

```text
Wordstat/Search cloud credential = separate
Webmaster OAuth = separate
Metrika OAuth = separate
Direct OAuth = separate
no credential unification project is authorized
```

Permanent service registry:

```text
wordstat
search
webmaster
metrika
direct
```

Development rule:

```text
research / contract
→ exact live-main baseline
→ governed dev branch
→ tests/model contract before risky runtime behavior
→ implementation
→ focused verification
→ freeze exact candidate
→ independent complete applicable gate
→ minimal irreducible owner-live
→ integrate accepted bytes
→ post-merge identity proof
→ close phase
```

Do not invent additional owner ceremonies after the accepted evidence chain is complete.

---

# PHASE 0 — Repository / reference / core design

**Status: PASS / CLOSED.**

---

# PHASE 1 — Wordstat + unified core

**Status: LIVE PASS / CLOSED.**

Accepted provider methods:

```text
WORDSTAT_API_V1
getTop
getDynamics
getRegionsDistribution
getRegionsTree
```

---

# PHASE 2 — Yandex Search / SERP

**Status: LIVE PASS / CLOSED.**

Accepted ordinary Search slice:

```text
SEARCH_API_V1
method = search
POST /v2/web/search
synchronous text WebSearch
regional bounded Yandex SERP evidence
```

Original accepted Search source:

`b7869180c229356a6b3d51ac980ec3da5df4c23c`

Generative Search was deliberately handled later as AI-native work rather than retroactively redefining Phase 2.

---

# INTER-PHASE — Lifecycle button gating

**Status: OWNER LIVE PASS / CLOSED.**

Accepted source:

`939e880f820e52beae9dcbcedc86d5cd9e13b075`

---

# PHASE 3 — Webmaster

**Status: LIVE PASS / CLOSED.**

Accepted first slice:

```text
WEBMASTER_API_V1
listHosts
getSummary
getDiagnostics
getPopularQueries
writes = disabled
```

---

# PHASE 4 — Metrika

**Status: LIVE PASS / CLOSED.**

Accepted first slice:

```text
METRIKA_API_V1
listCounters
getCounter
getTrafficSummary
getTrafficByTime
writes = disabled
```

---

# PHASE 5 — Yandex Direct

**Status: PASS / CLOSED.**

Accepted first slice:

```text
DIRECT_API_V1
listCampaigns
listAdGroups
listAds
listKeywords
getCampaignPerformance
writes = disabled
```

Final closure authority:

`extension/tests/PHASE5_DIRECT_FINAL_CLOSURE_2026-08-27.md`

---

# GATE A — O-001 AI-Native Semantic Rebuild comparative validation

**Status: PASS / CLOSED.**

Question tested:

> Does adding direct AI/Alice evidence materially improve semantic/page-job decisions compared with a strong ordinary SEO baseline using the same business, Wordstat and ordinary Search evidence?

The valid clean baseline was generated in an isolated context from a sealed Alice-free packet and frozen before Pass B.

Final verdict:

```text
AI_NATIVE_COMPARATIVE_GATE_PASS
```

Canonical evidence:

```text
extension/docs/AI_NATIVE_BLOOD_SAND_REQUIRED_COMPARATIVE_GATE.md
extension/tests/AI_NATIVE_BLOOD_SAND_BASELINE_PASS_A_2026-08-27.md
extension/tests/AI_NATIVE_BLOOD_SAND_AI_NATIVE_PASS_B_2026-08-27.md
extension/tests/AI_NATIVE_BLOOD_SAND_COMPARISON_2026-08-27.md
```

The result proves material methodology uplift/de-risking on a controlled real project dataset. It does not prove guaranteed revenue, ranking, citation or AI visibility.

---

# PHASE 6 — Semantic Core Builder / Wordstat batch evidence orchestration

**Status: PASS / CLOSED / IN MAIN.**

Productionized first slice:

```text
WORDSTAT_BATCH_API_V1
service = wordstat
start / next / status / pause / resume / cancel
```

Core lifecycle:

```text
seed list
→ deterministic item queue
→ one trusted Wordstat command per safe next
→ durable per-item state
→ persisted provider evidence
→ checkpoint/resume
→ no replay of completed work
→ OUTCOME_UNKNOWN => no automatic retry
→ request/cost bound
```

Frozen authority:

```text
source = 34f50688268970f4863dddb2089a33d891b91372
src tree = adab628a8ec328fa5079ae35f45005a0ee7de2c1
artifact = 9649039904
```

Independent gate + owner-live acceptance are PASS. Owner-live executed three distinct real Wordstat items exactly once each and completed 3/3 with no replay.

Authority:

`extension/tests/PHASE6_WORDSTAT_BATCH_FINAL_ACCEPTANCE_2026-08-27.md`

---

# PHASE 7 — AI Search / official GenSearch evidence hand

**Status: PASS / CLOSED / IN MAIN.**

Gate A authorized the AI-specific work. Official GenSearch was then validated against the frozen canonical consumer-Alice evidence before production promotion.

Production boundary:

```text
service = search
protocol = SEARCH_API_V1
method = genSearch
POST /v2/gen/search
```

It remains inside the existing Search service and does not create a sixth service.

Proxy validation:

```text
representative roots = 5
SAME_OR_STRONGLY_ALIGNED = 4
PARTIALLY_ALIGNED = 1
MATERIALLY_DIFFERENT = 0
systematic contradictions = 0
verdict = AI_NATIVE_GENSEARCH_PROXY_VALIDATION_PASS
```

Permanent provenance distinction:

```text
GEN_SEARCH_QUERY_OBSERVED != ALICE_FANOUT_OBSERVED
GEN_SEARCH_ANSWER != CONSUMER_ALICE_ANSWER
GEN_SEARCH_SOURCE != CONSUMER_ALICE_SOURCE
```

Production integration:

```text
main = 67aeee71a42bdc0edb516341297987c1d1d26972
extension/src tree = 04dc6d015977270fb064b669ee03d04f6e130612
postmerge run = 33140809518 / SUCCESS
Node regression = 99/99
controlled browser real Yandex requests = 0
```

Canonical production contract:

`extension/docs/AI_NATIVE_GENSEARCH_PRODUCTION_CONTRACT_2026-08-28.md`

Validation authority:

`extension/tests/AI_NATIVE_GENSEARCH_PROXY_VALIDATION_FINAL_2026-08-28.md`

---

# PHASE 8 — Bulk SERP / TOP-overlap / rank evidence

**Status: ACTIVE NEXT ENGINEERING PHASE / REQUIREMENTS READY.**

Canonical requirements:

`extension/docs/PHASE_8_BULK_SERP_TOP_RANK_REQUIREMENTS_AND_PLAN.md`

## Market reason

Demand is established by the consolidated freelance matrix, especially:

```text
F-013 semantic core + TOP/SERP clustering
F-014 Wordstat core + TOP grouping
F-015 standalone TOP/SERP clustering, supplied base = 500 keys
```

Current blocker is operational rather than analytical:

```text
durable bulk ordinary-Search queue
+ per-key checkpoint/resume
+ cost/progress controls
+ persisted domain/rank projections
```

## First slice

Candidate orchestration hand:

```text
SEARCH_BATCH_API_V1
service = search
queries[] = up to 500
```

Target behavior:

```text
keyword list + region
→ deterministic ordinary-Search queue
→ one paid provider boundary per explicit safe next
→ durable SERP payload per key
→ checkpoint/resume/no replay
→ ranked URL/domain projections
→ paged deterministic TOP-overlap evidence
→ bounded sampled target-domain rank evidence
→ ChatGPT cluster/page-job reasoning
```

Pure local management/projection actions must not contact the provider. Final cluster labels and page split/merge decisions remain ChatGPT work.

## Phase-8 execution order

```text
P8-00 exact live-main baseline freeze
P8-01 SearchProtocol/Search XML/provider-batch architecture reuse audit
P8-02 protocol/storage/projection tests first
P8-03 focused model/runtime tests
P8-04 minimal ordinary-Search batch runtime
P8-05 durable per-item SERP persistence
P8-06 local projection + target-domain sampled-rank evidence
P8-07 bounded paged overlap projection
P8-08 restart/tab-close/pause/resume/double-submit/stale-event/no-replay tests
P8-09 request/cost bound tests
P8-10 prior-service regression including GenSearch + Wordstat batch
P8-11 controlled browser gate with local provider stub
P8-12 freeze candidate + independent complete gate
P8-13 minimal owner-live real Search-batch acceptance
P8-14 integrate exact accepted bytes / postmerge identity / close
```

Phase 8 does not authorize Google, consumer-SERP scraping, GenSearch batching, autonomous semantic clustering or provider writes.

---

# PHASE 9 — Google organic gap

**Status: PLANNED / EXTERNAL PROVIDER RESEARCH REQUIRED.**

Potential unlocks:

- Yandex + Google rank tracking;
- cross-engine competition validation;
- seller-equivalent deliverables that explicitly require Google metrics.

Do not invent a Google provider. Research official/stable/legal acquisition options before contract freeze.

---

# PHASE 10 — Crawler / technical SEO evidence hand

**Status: PLANNED / LOWER PRIORITY THAN PHASE 8.**

If implemented, it should be a crawler/evidence hand for ChatGPT rather than an attempt to autonomously repair arbitrary CMS/code.

A crawl-export importer may be a cheaper intermediate product slice before a native crawler.

---

# MARKET-DISCOVERY AUTHORITY

Canonical matrix:

`extension/docs/FREELANCE_ORDER_CAPABILITY_MATRIX.md`

Current product conclusion:

```text
mass-market base = Semantic Core Builder
premium differentiated method = AI-Native Semantic Rebuild with selective GenSearch evidence
next highest-leverage engineering = durable bulk ordinary-Search / TOP evidence hand
```

---

# CURRENT ACTIVE ORDER

```text
DONE: Phases 0–6 closed
DONE: Gate A O-001 comparative methodology PASS
DONE: Phase 7 GenSearch validated, frozen, integrated and postmerge verified

NOW:
Phase 8 P8-00 → P8-02 baseline / architecture / test-first contract

THEN:
Phase 8 runtime → focused regression → freeze → independent gate → minimal owner-live → main integration

LATER:
Phase 9 Google organic provider research
Phase 10 crawler/importer evidence hand
```

No project-owner action is currently required.
