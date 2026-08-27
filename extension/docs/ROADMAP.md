# ROADMAP v0.13 — Yandex Marketing Bridge

Status: active roadmap.  
Updated: 2026-08-27.

## Governing rule

**One implementation phase = one controlled development closure + one final live acceptance boundary.**

Testing cadence:

```text
during development/change
→ focused tests for changed code + affected dependencies

working candidate frozen for handoff
→ exact artifact preparation through mandatory QA transport runbook
→ one complete independent Codex pre-delivery regression campaign
→ exact package/identity verification
→ owner real-profile/live acceptance only for irreducible live behavior
→ integration into main
→ mandatory post-merge final gate
```

Research / evidence rule:

```text
DO NOT GUESS missing provider/API facts.

fact needed
→ check live project source of truth
→ check current official provider documentation/site directly
→ if incomplete/inaccessible/ambiguous, use Codex as a read-only research agent to browse official sites, inspect documentation, follow links, download available public reference/spec/artifact material, and return traceable evidence
→ if ChatGPT + Codex still cannot establish the fact, ask the project owner for one concrete action/material
→ until proven, record UNKNOWN / NOT VERIFIED / explicit conflict
```

Codex is not limited to QA. It is also an authorized information-gathering/research tool. Research authority does **not** imply permission to edit product/production, credentials, provider account settings or external resources; those require separate authorization.

Exact current identities, blockers and authorized next action are authoritative in the Phase-specific closure/checkpoint documents. `CURRENT_STATE.md` is not promoted to CLOSED for an active phase before owner-live + integration + post-merge PASS.

---

# PERMANENT OPERATING MODEL — CHATGPT IS THE WORKER, BRIDGE IS THE HANDS

Capability and freelance-service decisions use this boundary:

```text
CHATGPT PLUS
= analyst
= planner
= semantic architect
= data interpreter
= report/artifact author
= QA/recommendation layer

YANDEX MARKETING BRIDGE
= controlled provider/API acquisition and execution hands
= persistence/safety/repeatability boundary

HUMAN OPERATOR
= authorizes/runs the extension
= supplies required account access
= does not substitute for ChatGPT as the expert analytical worker
```

A service does not require every analytical step to be hard-coded into the extension. If ChatGPT can reliably perform the reasoning from evidence acquired by the Bridge and can produce the client deliverable, that capability counts toward end-to-end service coverage.

Productization priority is therefore given to **missing hands, repeated acquisition/orchestration burden, persistence, safe resume, evidence provenance and repeatability**, not to replacing ChatGPT reasoning with deterministic code for its own sake.

---

# PHASE 0 — REPOSITORY / REFERENCE / CORE DESIGN

**Status: PASS / CLOSED.**

---

# PHASE 1 — WORDSTAT + UNIFIED CORE

**Status: LIVE PASS / CLOSED.**

Accepted Phase-1 artifact:

```text
yandex-marketing-bridge-0.1.1-phase1-manual-enable-order-fix-candidate.zip
SHA-256: e13a26072039550792e740b8ed73e2bd56d48bdceb075a060406d2359e402a65
bytes: 209505
files: 45
ZIP entries: 48
```

---

# PHASE 2 — YANDEX SEARCH / SERP

**Status: LIVE PASS / CLOSED.**

Accepted first slice:

```text
protocol: SEARCH_API_V1
service: search
method: search
mode: synchronous text WebSearch only
provider endpoint: POST https://searchapi.api.cloud.yandex.net/v2/web/search
response format: FORMAT_XML
normalized result: SEARCH_RESULT_V1
```

Accepted product:

```text
source commit: b7869180c229356a6b3d51ac980ec3da5df4c23c
artifact SHA-256: ce824a9fff5ddee47bc0145f57db4da10c6352e782c859fa500e3a1fb98088aa
independent Codex complete gate: PASS
owner real-profile/live Search: PASS
```

Deferred Search async/image/generative surfaces remain locked unless a later demand-driven phase explicitly authorizes them.

---

# INTER-PHASE PATCH — LIFECYCLE GUARD BUTTON GATING

**Status: OWNER LIVE PASS / CLOSED.**

Accepted source:

```text
939e880f820e52beae9dcbcedc86d5cd9e13b075
```

Accepted behavior:

```text
MANUAL_OPERATION_ACTIVE → Yandex action button disabled / non-clickable
DELIVERY_IN_PROGRESS   → Yandex action button disabled / non-clickable
blocking state cleared → button becomes clickable again
```

---

# PHASE 3 — WEBMASTER

**Status: LIVE PASS / CLOSED.**

Accepted first slice:

```text
protocol: WEBMASTER_API_V1
result: WEBMASTER_RESULT_V1
provider base: https://api.webmaster.yandex.net/v4
auth: OAuth token + derived user_id
methods: listHosts,getSummary,getDiagnostics,getPopularQueries
writes: disabled
```

Accepted product identity:

```text
source: a7d9f947759f4f6a4fc20b39c7df3f25d81ce3e5
frozen ZIP SHA-256: 1c700640d5fa7b041468c1b987ce3793f4da7631b417e9fb5b0a59b54abd1fd8
accepted src tree: e5fa694f1354e1ee048a352481a416413e94a3c9
merged main: 6c95cf15462b5ad61a267bf1186bb75fa8dd4dff
owner-live acceptance: PASS
```

Durable closure evidence:

```text
extension/tests/PHASE3_WEBMASTER_OWNER_LIVE_PASS_2026-08-26.md
```

Webmaster writes and deferred advanced surfaces remain locked.

---

# PHASE 4 — METRIKA

**Status: LIVE PASS / CLOSED.**

Accepted first slice:

```text
service: metrika
protocol: METRIKA_API_V1
result: METRIKA_RESULT_V1
auth: dedicated OAuth token with metrika:read
Management API: https://api-metrika.yandex.net/management/v1
Reports API: https://api-metrika.yandex.net/stat/v1
methods: listCounters,getCounter,getTrafficSummary,getTrafficByTime
writes: disabled
```

Accepted product identity:

```text
source: 643445758e86d3b06ac42a6daea5c97b6e9223c7
frozen ZIP SHA-256: 99c3719b447185481125964f0ff543c4c706714f9fe23fe150b7a8fbc8700217
frozen ZIP bytes: 117375
accepted src tree: fbc52f9a84195278b7b5e942f2a84c7d69778b98
merged main: 52b0cbf92872f6e7cb9f4cb96d0877d55221ceb4
independent Codex final QA: run 32955512254 attempt 2 PASS
post-merge QA: run 32957778009 PASS
owner-live acceptance: PASS
```

Durable closure evidence:

```text
extension/tests/PHASE4_METRIKA_OWNER_LIVE_PASS_2026-08-26.md
```

All Metrika write/import/Logs/arbitrary-report surfaces remain locked.

---

# PHASE 5 — YANDEX DIRECT

**Status: IMPLEMENTATION COMPLETE / FROZEN / INDEPENDENT CODEX PASS / OWNER-LIVE READY / NOT CLOSED.**

The implementation and independent pre-delivery QA are complete. The remaining irreducible boundary is one minimal owner-live read-only acceptance against the owner's approved Direct account, followed by controlled integration and post-merge final QA.

## Accepted source identity

```text
accepted source commit:
841a1e2c1a503c4a05572a957ba97c55b9b60c52

accepted extension/src tree:
edf1c2d3494ebbc53ae778d23be1457eb885b605

corrected candidate branch:
candidate/phase5-direct-first-slice-r2-2026-08-27

freeze trigger commit:
389084290635fbf2ac305098adc3aae17f967c83
```

The previous candidate `candidate/phase5-direct-first-slice-2026-08-27` is superseded and must never be used because its credential runtime could lose/overwrite independent service records under stale migration/concurrent saves.

Corrected credential behavior:

```text
five separate credential records remain
module-level serialized mutation queue
load migration re-reads current store under mutation lock
service save is read-modify-write under the same lock
backup import uses the same exclusive mutation queue
NO token consolidation/reuse
```

## Frozen authoritative artifact

```text
freeze run: 33037955943
artifact name: phase5-direct-r2-frozen-candidate-841a1e2
artifact id: 9632728199

inner installable ZIP:
yandex-marketing-bridge-0.1.1-phase5-direct-first-slice-r2-candidate.zip

SHA-256:
ac8efc444578e9d3f31ac0325baca4b286fd608bc511850f480e0d397936620b

bytes: 406656
product files: 39
```

Freeze proves exact accepted source/tree, deterministic byte-identical rebuild, ZIP integrity, extraction/per-file identity, syntax validation and **zero real Yandex requests**.

## Independent Codex acceptance

**PASS.**

Permanent evidence:

```text
extension/tests/PHASE5_DIRECT_R2_CODEX_COMPLETE_PASS_2026-08-27.md
```

Genuine independent campaign proved:

```text
source suite: 34/34
packaged suite: 34/34
syntax: 33/33 both
JSON: 2/2 both
credential concurrency: PASS
Direct popup D18: PASS
Manual lifecycle: PASS
Direct addendum: PASS
prior-service compatibility: PASS
D00-D22: PASS
controlled provider Direct requests: 2
controlled Search stub: 1
real Direct requests: 0
all real Yandex requests: 0
real credentials: NO
product/test/harness mutation during run: NO
workspaces clean: PASS
product bytes post-test: IDENTICAL
enabled NOT_RUN: 0
marker: PHASE5_DIRECT_R2_INDEPENDENT_RUNNER_PASS
```

## Direct first-slice contract

```text
protocol: DIRECT_API_V1
result: DIRECT_RESULT_V1
methods:
  listCampaigns
  listAdGroups
  listAds
  listKeywords
  getCampaignPerformance
writes: disabled
```

Provider/access contract:

```text
OAuth source: direct:api
approved Direct API application request: required
production data: full access required
transport: HTTPS POST
JSON endpoint pattern: https://api.direct.yandex.com/json/v501/{service}
Reports endpoint: https://api.direct.yandex.com/json/v501/reports
Authorization: Bearer <dedicated Direct OAuth token>
Client-Login: optional; blank for ordinary advertiser, exact client login only for true agency-client context
Use-Operator-Units: locked
Payment-Token / finance: locked
```

Read routes:

```text
listCampaigns → Campaigns.get
listAdGroups   → AdGroups.get
listAds        → Ads.get
listKeywords   → Keywords.get
```

Reports first slice:

```text
ReportType: CAMPAIGN_PERFORMANCE_REPORT
DateRangeType: CUSTOM_DATE
Format: TSV
processingMode: online only
FieldNames: Date,CampaignId,CampaignName,Impressions,Clicks,Cost
IncludeVAT: YES
money: integer micros, normalized as cost_micros
max local period: 31 days
max local rows: 1000
```

Offline/auto report creation, HTTP 201/202 polling and arbitrary reports remain deferred.

## Permanent credential boundary

```text
Wordstat → own credential
Search → own credential/configuration
Webmaster → own OAuth
Metrika → own OAuth
Direct → own dedicated OAuth
```

Do **not** consolidate/reuse OAuth tokens. Credential consolidation may only be reconsidered as a separate architecture decision after the whole service foundation is complete.

## Owner-live status and exact next action

Owner reports that Direct access is now ready for testing. This authorizes the already-defined minimal live acceptance; it is **not itself live PASS evidence**.

Canonical checklist:

```text
extension/tests/PHASE5_DIRECT_OWNER_LIVE_CHECKLIST_2026-08-27.md
```

Exact safe live sequence:

```text
1. load exact frozen candidate
2. select Direct; Autorun OFF
3. save dedicated Direct OAuth token locally once; never paste/log it
4. Direct Check exactly once
   = Campaigns.get, FieldNames=[Id], Limit=1
5. if Check PASS, run exactly once:
   DIRECT_API_V1
   {"method":"listCampaigns","limit":10,"offset":0}
6. if campaign exists and a downstream read is useful, run ONE listAdGroups request
7. if campaign + real-date data make it useful, run ONE short online campaign-performance report, preferably one day
8. do NOT add listAds/listKeywords merely for coverage
9. stop immediately on unexpected error; do not blindly retry an initiated request
```

If the account has zero campaigns:

```text
listCampaigns empty
→ NOT_APPLICABLE_EMPTY_ACCOUNT
→ this is a legitimate owner-live result after successful authenticated capability proof
```

Owner-live must never perform writes, bids, budgets, finance/account changes, offline report polling, quota stress, concurrency testing or intentional error generation.

After real success, create:

```text
extension/tests/PHASE5_DIRECT_OWNER_LIVE_PASS_2026-08-27.md
```

## Final integration / closure after owner-live

Do **not** merge the entire historical independent-Codex QA branch into main.

Product authority remains accepted source `841a1e2...` and accepted `extension/src` tree `edf1c2d...`.

If live `main` remains the expected baseline and candidate lineage remains clean, integrate the accepted Phase-5 product lineage plus permanent QA/evidence only. If main has moved, create a fresh integration branch from the new main and apply the accepted Phase-5 delta while preserving exact `extension/src` product identity. Any unexpected product conflict/diff means STOP and requalify.

Permanent final post-merge workflow:

```text
.github/workflows/phase5-direct-postmerge-final.yml
```

Final marker required:

```text
PHASE5_DIRECT_POSTMERGE_FINAL_PASS
```

Closure order:

```text
owner-live PASS
→ durable owner-live evidence
→ controlled integration
→ main product identity verification
→ postmerge final workflow PASS
→ update CURRENT_STATE / final closure checkpoint
→ PHASE 5 CLOSED
```

All Direct writes, bids, finance/payment, arbitrary reports, offline report queues and automatic retries remain locked.

---

# POST-PHASE-5 PRODUCT ROADMAP — DEMAND-DRIVEN FREELANCE EXECUTION

The next roadmap is no longer “add providers endlessly.” The existing provider foundation is used to execute real freelance-marketplace jobs with ChatGPT Plus as the worker.

Source of truth for market demand:

```text
extension/docs/FREELANCE_ORDER_CAPABILITY_MATRIX.md
```

Permanent duplicate rule:

```text
same marketplace card / same underlying offer encountered again
→ mark as duplicate evidence
→ do not create fake new demand count
→ may strengthen recurrence/market-density signal
→ update reusable capability priority only when the repeated card adds genuinely new scope/constraints
```

## GATE A — BLOOD_SAND AI-NATIVE COMPARATIVE PROOF

**Status: REQUIRED AFTER PHASE 5 / NOT YET RUN.**

Canonical protocol:

```text
extension/docs/AI_NATIVE_BLOOD_SAND_REQUIRED_COMPARATIVE_GATE.md
```

Strategic offer specification:

```text
extension/docs/AI_NATIVE_SEMANTIC_SERVICE_OPPORTUNITY.md
```

Purpose:

> Prove or falsify, once on real `blood_sand` data, whether Alice evidence materially improves semantic/page decisions versus a strong ordinary SEO baseline.

Execution order:

```text
freeze ordinary SEO Pass A without Alice evidence
→ run AI-native Pass B on the same baseline + canonical Alice evidence
→ compute decision deltas
→ PASS only if at least one meaningful action-level decision changes or is materially de-risked with traceable evidence
```

Valid results:

```text
AI_NATIVE_COMPARATIVE_GATE_PASS
NO_PROVEN_UPLIFT
INVALID_BASELINE_LEAKAGE
INSUFFICIENT_CANONICAL_EVIDENCE
```

No fresh paid Yandex measurements are required by default: the current `blood_sand` canonical evidence already contains Wordstat, Search, Alice and a Query Evidence Ledger.

This gate is **not a Direct Phase-5 blocker**. It runs immediately after Phase 5 closes and **before Alice-specific implementation is promoted to an engineering phase**.

---

# PHASE 6 — SEMANTIC CORE / FREELANCE WORKFLOW PRODUCTIZATION

**Status: PLANNED / DEMAND-PROVEN.**

Market analysis already shows repeated demand for semantic-core collection, cleanup, grouping, Wordstat frequency, competitor/intent interpretation and client artifacts.

Current service ability is stronger than the current product automation because ChatGPT Plus can already perform the reasoning. Phase 6 therefore targets repeated operational burden, not replacement of ChatGPT.

Target reusable hand:

```text
SEMANTIC CORE JOB

client/site/topic/region intake
→ seed queue
→ bounded Wordstat collection
→ raw evidence checkpoint
→ unique phrase registry
→ expansion queue
→ dedup / normalization support
→ safe resume without paid-request repetition
→ progress / budget visibility
→ handoff to ChatGPT for cleaning, intent, grouping, page mapping
→ deterministic XLSX/CSV artifact assembly
→ QA manifest
```

Priority requirements:

- preserve exactly-once paid-request semantics;
- save evidence before issuing the next paid collection;
- explicit region/device provenance;
- no forced padding to requested keyword count when the real niche is exhausted;
- duplicates across seeds remain traceable before final dedup;
- ChatGPT remains responsible for semantic judgment, intent, grouping and client recommendations;
- support base semantic-core offers before premium AI-native additions.

This phase is market-proven independently of Alice and should remain useful even if Gate A returns `NO_PROVEN_UPLIFT`.

---

# CONDITIONAL PHASE 7 — ALICE OBSERVATION / AI VISIBILITY HAND

**Status: CONDITIONAL ON GATE A + PROVIDER PATH VALIDATION.**

Promote this into implementation only if the comparative gate demonstrates meaningful incremental decision value.

Primary target:

```text
AI SEARCH / ALICE OBSERVATION JOB

query registry
→ clean isolated Alice observation
→ answer snapshot
→ source URLs/domains/page types
→ observed fan-out
→ timestamp/context metadata
→ raw immutable evidence
→ normalized observation
→ safe resume/review
```

Hard evidence rules:

- observed fan-out and inferred fan-out are different fields;
- contaminated-context runs are invalid evidence, not weak evidence;
- source display order is not called ranking without provider proof;
- repeat observations append history rather than overwrite it;
- no deterministic source-presence guarantee;
- no guarantee of Alice indexing/ranking/SoV.

Secondary target:

```text
WEBMASTER ALICE VISIBILITY CAPTURE / IMPORT

Share of Voice
query examples
source/page presence
competitor/source environment
dynamics
```

Preferred provider order:

```text
stable official API if verified
→ official export/import if available
→ controlled browser-assisted capture
```

Do not implement unsupported private endpoints or brittle scraping merely to claim Alice coverage.

Ongoing official API/feature monitoring may continue while this phase is conditional.

---

# PHASE 8 — BULK SERP / RANK TRACKER + GOOGLE GAP

**Status: PLANNED / MARKET-DEMAND DRIVEN.**

Repeated marketplace demand shows a separate bulk rank-tracking family.

Yandex side target:

```text
domain normalization
→ keyword registry
→ bounded Yandex SERP collection
→ first matching rank/domain
→ per-key evidence checkpoint
→ safe resume
→ progress/budget
→ final XLSX position report
```

High-volume economics must re-evaluate deferred Yandex Search modes before implementation; do not assume synchronous Search is the optimal commercial acquisition path.

Google side remains a real provider gap:

```text
need a verified organic SERP source
with geography fidelity + depth suitable for rank tracking + viable quotas/pricing
```

Do not substitute a generic Google search API unless it is proven to represent the organic SERP needed by the service.

---

# PRIORITY DECISION RULE AFTER PHASE 5

Use evidence, not feature enthusiasm:

```text
1. close Direct safely
2. run blood_sand comparative AI-native gate once
3. continue market-card analysis / duplicate-aware demand counting
4. productize the highest repeated operational bottleneck
5. build Alice hand only if Gate A demonstrates incremental decision value
6. build other provider gaps only when repeated sellable work requires them
```

Commercial hierarchy:

```text
READY NOW services
→ sell with current Bridge + ChatGPT workflow

PARTIAL services
→ identify exact missing hand/provider
→ prioritize by repeated market demand and margin potential

OWN STRATEGIC OFFERS
→ keep separate from marketplace demand counts
→ require explicit proof gates before calling differentiation proven
```

---

# O-001 — AI-NATIVE SEMANTIC REBUILD

**Strategic hypothesis: YES.**  
**Market differentiation signal: STRONG.**  
**Commercial proof: EXPERIMENTAL until Gate A PASS.**  
**Strict repeatable toolchain: PARTIAL until Alice evidence acquisition is productized.**

Operating concept:

```text
BASE
Semantic Core Builder
= human search demand + cleaning + grouping + page mapping

PREMIUM CANDIDATE
AI-Native Semantic Rebuild
= BASE
+ direct Yandex SERP evidence
+ Alice evidence
+ Search-vs-AI intent gaps
+ source competition
+ H/A/C/O
+ AI-aware page jobs
+ post-launch AI visibility measurement
```

Never market this as guaranteed `ИИ-индексация`. The safe promise is a transparent evidence-driven semantic/page rebuild for ordinary and generative search, with measurable observations and explicit uncertainty.
