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

**Status: PASS / CLOSED / IN MAIN.**

Accepted production hand:

```text
SEARCH_BATCH_API_V1
service = search
queries[] up to 500
one explicit next <= one ordinary Search provider request
durable per-query checkpoint/result evidence
local projection + sampled target-domain rank
local paged TOP/domain overlap
OUTCOME_UNKNOWN => no automatic replay
```

Accepted identity and gates:

```text
source authority = 0377d6e1f176d4b7ddd8553c0099e02a4f1e8716
extension tree = 446fed6970c5fec627be34c3893800dc4511c6c9
extension/src tree = bdad1e87a2537d8646e480ca23f8068c3dced17e
freeze run = 33143237276 / SUCCESS
candidate ZIP sha256 = 8f6ba92dbe1f592a62c66cd250ed942e261f56deffbe87117371bd9c481e6332
owner-live = PHASE8_SEARCH_BATCH_OWNER_LIVE_PASS
main integration = ebd697e5733a7d40d13401d4c02b82a75711231c
postmerge run = 33144396638 / SUCCESS
Node regression = 118/118
controlled browser real Yandex requests = 0
```

Owner-live used two real ordinary Search queries. `start` made zero provider requests; two explicit `next` calls produced exactly two successful provider requests; `status`, `projection` and `overlapPage` remained local-only with `requests_started=2` and total estimated cost `0.976 RUB`.

Final semantic clustering/page split decisions remain ChatGPT work rather than hidden threshold logic.

Final authority:
`extension/tests/PHASE8_SEARCH_BATCH_FINAL_ACCEPTANCE_2026-08-28.md`

---

# PHASE 9 — Google organic gap

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
bulk ordinary-Search/TOP evidence hand = ACCEPTED / IN MAIN
next highest-leverage engineering = Phase 9 Google organic provider research
```

---

# CURRENT ACTIVE ORDER

```text
DONE: Phases 0–8 closed
DONE: Gate A O-001 comparative methodology PASS
DONE: Phase 7 GenSearch validated, frozen, integrated and postmerge verified
DONE: Phase 8 Search batch/TOP/rank frozen, owner-live accepted, integrated and postmerge verified

NOW:
Phase 9 Google organic provider research — official/stable/legal acquisition options first

THEN:
Provider/contract decision only after research; Phase 10 crawler/importer remains lower priority
```

No project-owner action is currently required.
