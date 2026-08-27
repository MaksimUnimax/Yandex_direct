# ROADMAP v0.13 — Yandex Marketing Bridge

Status: **ACTIVE**  
Updated: 2026-08-27

## Governing product model

```text
ChatGPT Plus = brain / analyst / planner / semantic architect / QA
Yandex Marketing Bridge = controlled provider hands
Human owner/operator = authorization and execution boundary
```

The extension should automate repetitive deterministic acquisition, persistence, policy, recovery and safe execution. It should **not** attempt to replace ChatGPT with hard-coded SEO judgment where model reasoning from evidence is the stronger worker.

Permanent credential rule:

```text
Wordstat/Search credential = separate
Webmaster OAuth = separate
Metrika OAuth = separate
Direct OAuth = separate
no credential unification project is authorized
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
→ close phase
```

Do not invent additional owner ceremonies after the accepted evidence chain is complete. GitHub/QA/documentation work is the assistant's responsibility unless a real owner-only external action is irreducible.

---

# PHASE 0 — Repository / reference / core design

**Status: PASS / CLOSED.**

---

# PHASE 1 — Wordstat + unified core

**Status: LIVE PASS / CLOSED.**

Accepted core provider methods:

```text
WORDSTAT_API_V1
getTop
getDynamics
getRegionsDistribution
getRegionsTree
```

The service remains the primary human-demand hand for semantic workflows.

---

# PHASE 2 — Yandex Search / SERP

**Status: LIVE PASS / CLOSED.**

Accepted first slice:

```text
SEARCH_API_V1
POST /v2/web/search
synchronous text WebSearch
regional bounded Yandex SERP evidence
```

Accepted source:

`b7869180c229356a6b3d51ac980ec3da5df4c23c`

Deferred async/image/generative surfaces are not retroactively part of Phase 2.

Official GenSearch provider research is now tracked separately for future AI-native work:

`extension/docs/AI_NATIVE_YANDEX_GENSEARCH_PROVIDER_RESEARCH_2026-08-27.md`

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

Accepted source/tree:

```text
source = a7d9f947759f4f6a4fc20b39c7df3f25d81ce3e5
src tree = e5fa694f1354e1ee048a352481a416413e94a3c9
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

Accepted source/tree:

```text
source = 643445758e86d3b06ac42a6daea5c97b6e9223c7
src tree = fbc52f9a84195278b7b5e942f2a84c7d69778b98
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

Accepted product:

```text
source = 841a1e2c1a503c4a05572a957ba97c55b9b60c52
src tree = edf1c2d3494ebbc53ae778d23be1457eb885b605
frozen ZIP SHA-256 = ac8efc444578e9d3f31ac0325baca4b286fd608bc511850f480e0d397936620b
```

Independent exact-candidate acceptance:

```text
source/packaged suites = PASS
browser gates = PASS
D-00..D-22 = PASS
NOT_RUN = 0
product immutability = PASS
```

Owner-live acceptance:

```text
Direct Check = PASS
real listCampaigns = HTTP 200 / OK
request_executed = true
automatic_retry = false
campaigns = []
listAdGroups = NOT_APPLICABLE_EMPTY_ACCOUNT
getCampaignPerformance = NOT_APPLICABLE_NO_REAL_DATA
writes/mutations = 0
```

Final integration:

```text
PR #25
integration main = 20f0605f8b0cdafc009c6719529859d63e8c0eba
main src tree after merge = edf1c2d3494ebbc53ae778d23be1457eb885b605
exact identity = PASS
```

Closure evidence:

`extension/tests/PHASE5_DIRECT_FINAL_CLOSURE_2026-08-27.md`

### Post-merge workflow clarification

The manually dispatched `.github/workflows/phase5-direct-postmerge-final.yml` is **not** a mandatory project-owner action and is not required to validate or close Phase 5. It is optional QA infrastructure only.

Phase 5 is closed on the completed accepted-candidate + independent-gate + owner-live + exact-main-integration evidence chain.

---

# GATE A — O-001 AI-Native Semantic Rebuild comparative validation

**Status: MANDATORY ONE-TIME METHODOLOGY VALIDATION / PREPARED / CLEAN PASS A PENDING.**

This is not a numbered provider phase and does not block market-proven Phase 6 engineering.

Question:

> Does adding direct AI/Alice evidence materially improve semantic/page-job decisions compared with a strong ordinary SEO baseline using the same business, Wordstat and ordinary Search evidence?

Canonical gate:

`extension/docs/AI_NATIVE_BLOOD_SAND_REQUIRED_COMPARATIVE_GATE.md`

Frozen clean baseline manifest:

`extension/tests/AI_NATIVE_BLOOD_SAND_BASELINE_SOURCE_MANIFEST_2026-08-27.md`

Pass design:

```text
Pass A
= business/product + Wordstat + ordinary Search
= no Alice evidence / no Alice-derived conclusions

freeze Pass A

Pass B
= exact same baseline
+ canonical Alice evidence

compare action-level decision deltas
```

Valid outcomes:

```text
AI_NATIVE_COMPARATIVE_GATE_PASS
NO_PROVEN_UPLIFT
INVALID_BASELINE_LEAKAGE
INSUFFICIENT_CANONICAL_EVIDENCE
```

Current conversation has already consumed Alice-derived `blood_sand` conclusions, therefore it must **not** fabricate a clean Pass A. A clean independent analysis context is required for that one baseline pass.

Gate A controls whether Alice/GenSearch-specific engineering becomes a high-priority implementation phase. It does not stop Phase 6.

---

# PHASE 6 — Semantic Core Builder / batch evidence orchestration

**Status: ACTIVE NEXT ENGINEERING PHASE — REQUIREMENTS READY / IMPLEMENTATION AUTHORIZED.**

Canonical requirements:

`extension/docs/PHASE_6_SEMANTIC_CORE_BUILDER_REQUIREMENTS_AND_PLAN.md`

## Why Phase 6 is next

The freelance-market study repeatedly shows demand for:

- Wordstat semantic collection;
- cleanup/dedup;
- grouping;
- page mapping;
- advertising semantics;
- competitor-derived semantics;
- exact-frequency enrichment;
- TOP clustering.

The largest current gap is not ChatGPT's analysis capability. It is reliable large-batch provider acquisition and checkpointing.

## Phase 6 first slice

Primary hand:

```text
WORDSTAT_BATCH_JOB_V1 concept
```

Required behavior:

```text
seed-list input
→ deterministic item queue
→ one trusted Wordstat command per item
→ durable per-item state
→ result persistence
→ checkpoint/resume
→ no replay of completed items
→ OUTCOME_UNKNOWN => no automatic retry
→ progress truth
→ request/cost bound
→ raw + normalized evidence for ChatGPT
```

Reuse existing run/autorun recovery and cost-policy invariants instead of creating a second lifecycle system.

## What ChatGPT continues to do

Not hard-coded:

```text
seed strategy
semantic cleanup
intent classification
frequency-band interpretation
clustering by user job
page boundaries
keyword → target page
cannibalization decisions
competitor interpretation
recommendations
client workbook/report
```

Phase 6 validates the **hands**, not an autonomous SEO algorithm.

## Phase 6 execution order

```text
P6-00 exact live-main baseline / branch freeze
P6-01 architecture audit of existing autorun/run-context/cost/storage
P6-02 batch job state/fingerprint/storage contract
P6-03 model + recovery tests first
P6-04 minimal Wordstat batch runtime
P6-05 bounded UI/control/status surface
P6-06 restart/tab-close/pause/resume/double-submit/stale-event tests
P6-07 unknown outcome no-replay test
P6-08 request/cost bound test
P6-09 all prior-service regression including Direct
P6-10 freeze + independent gate
P6-11 minimal owner-live batch acceptance
P6-12 integrate/close
```

---

# CONDITIONAL PHASE 7 — AI Search / GenSearch evidence hand

**Status: RESEARCHED / IMPLEMENTATION GATED ON GATE A.**

Official provider path found:

```text
POST https://searchapi.api.cloud.yandex.net/v2/gen/search
```

Useful structured response evidence includes:

```text
answer
sources[].url/title/used
searchQueries[].text/reqId
hints / answer flags
```

Provider research:

`extension/docs/AI_NATIVE_YANDEX_GENSEARCH_PROVIDER_RESEARCH_2026-08-27.md`

Do not equate GenSearch with exact consumer Alice UI behavior without bounded validation.

If Gate A is PASS, the next AI-specific work is:

```text
1. bounded GenSearch vs canonical blood_sand Alice comparison
2. freeze provenance/protocol contract
3. extend Search hand to GenSearch
4. preserve GEN_SEARCH_* provenance separately from consumer ALICE_* evidence
5. add safe request/cost policy
6. later add/import post-launch Alice visibility evidence if a stable official path exists
```

If Gate A returns `NO_PROVEN_UPLIFT`, keep GenSearch as research/monitoring and prioritize market-proven workflow gaps first.

---

# PHASE 8 — Bulk SERP / TOP clustering / rank evidence

**Status: PLANNED / HIGH MARKET SIGNAL.**

Target hands:

```text
Search batch orchestration
per-key SERP checkpoint/resume
domain-set extraction
TOP-overlap evidence
rank measurement
safe cost budgeting
```

This phase moves F-015-style 500-key TOP clustering from PARTIAL to repeatable YES and improves niche/competitive analysis.

Do not hard-code final semantic clusters if ChatGPT can make the business/user-job judgment from the overlap evidence.

---

# PHASE 9 — Google organic gap

**Status: PLANNED / EXTERNAL PROVIDER REQUIRED.**

Unlocks or improves:

- Yandex+Google rank tracking;
- seller-equivalent semantic reports requiring Google metrics;
- cross-engine competition validation.

Do not invent a Google provider. Research official/stable/legal acquisition options before contract freeze.

---

# PHASE 10 — Crawler / technical SEO evidence hand

**Status: PLANNED / LOWER FIT THAN SEMANTIC CORE FOR CURRENT PRODUCT DIRECTION.**

The user explicitly excluded programmer-style technical audit work from the immediate freelance scope during market review. Therefore this is not ahead of the semantic-core, AI-native or bulk-SERP work.

If revisited, it should be a crawler/evidence hand for ChatGPT rather than an attempt to autonomously repair arbitrary CMS/code.

---

# MARKET-DISCOVERY AUTHORITY

Canonical matrix:

`extension/docs/FREELANCE_ORDER_CAPABILITY_MATRIX.md`

Current product conclusion:

```text
mass-market base = Semantic Core Builder
premium differentiated hypothesis = AI-Native Semantic Rebuild
highest leverage engineering = reliable batch/checkpoint provider hands
```

Duplicate freelance listings must not create fake unique-demand counts, but independent seller/listing observations may strengthen confidence in the same workflow family.

---

# CURRENT ACTIVE ORDER

```text
DONE: Phase 5 Direct closed

NOW:
A. Phase 6 P6-00/P6-03 engineering preparation and implementation
B. prepare valid clean independent blood_sand Pass A when isolated context is available

THEN:
- continue Phase 6 through freeze/acceptance
- run Pass B + comparison after Pass A is frozen
- promote/defer GenSearch phase based on comparative result
- continue Bulk SERP/TOP/rank work from market priority
```

No project-owner GitHub action is currently required.