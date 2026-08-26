# ROADMAP v0.12 — Yandex Marketing Bridge

Status: active roadmap.  
Updated: 2026-08-26.

## Governing rule

**One phase = one service = one controlled development closure + one final live acceptance boundary.**

Testing cadence:

```text
during development/change
→ focused tests for changed code + affected dependencies

working candidate frozen for handoff
→ exact artifact preparation through mandatory QA transport runbook
→ one complete independent Codex pre-delivery regression campaign
→ exact package/identity verification
→ owner real-profile/live acceptance only for irreducible live behavior
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

Exact current identities, blockers and authorized next action are authoritative in `CURRENT_STATE.md`.

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

Deferred Search async/image/generative/HTML scraping surfaces remain locked.

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

Owner-live used real counter `111970611` on `openscript.ru` and proved real Management and Reports API reads.

Durable closure evidence:

```text
extension/tests/PHASE4_METRIKA_OWNER_LIVE_PASS_2026-08-26.md
```

All Metrika write/import/Logs/arbitrary-report surfaces remain locked.

---

# PHASE 5 — YANDEX DIRECT

**Status: CONTRACT READY / IMPLEMENTATION AUTHORIZED.**

Official Direct API reconstruction is complete for the first slice.

Provider/access contract:

```text
OAuth source: direct:api
approved Direct API application request: required
production data: full access required
transport: HTTPS POST
JSON endpoint pattern: https://api.direct.yandex.com/json/v501/{service}
Reports endpoint: https://api.direct.yandex.com/json/v501/reports
Authorization: Bearer <dedicated Direct OAuth token>
Client-Login: optional saved credential field, used only for agency-client context
Use-Operator-Units: locked in first slice
Payment-Token / finance: locked
```

First slice:

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

Read routes:

```text
listCampaigns → Campaigns.get
listAdGroups   → AdGroups.get
listAds        → Ads.get
listKeywords   → Keywords.get
```

All object reads use fixed safe FieldNames constructed by trusted code. Assistant commands cannot supply provider JSON, service/method names, headers, raw URL, FieldNames or arbitrary SelectionCriteria.

Reports first slice:

```text
ReportType: CAMPAIGN_PERFORMANCE_REPORT
DateRangeType: CUSTOM_DATE
Format: TSV
processingMode: online only
FieldNames: Date,CampaignId,CampaignName,Impressions,Clicks,Cost
IncludeVAT: YES (Bridge decision)
money: integer micros, normalized as cost_micros
max local period: 31 days
max local rows: 1000
```

Offline/auto report creation, HTTP 201/202 polling and `SEARCH_QUERY_PERFORMANCE_REPORT` are explicitly deferred.

Direct provider capacity is measured in Units. Current official constraints/evidence include:

```text
max 5 simultaneous API requests per advertiser
Units response = spent / remaining / daily_limit
Campaigns.get = 10/call + 1/object
AdGroups.get = 15/call + 1/object
Ads.get = 15/call + 1/object
Keywords.get = 15/call plus per-2000 component
Reports = max 20 requests per 10 seconds per user
```

Bridge first-slice local policy is deliberately lower/bounded:

```text
manual_enabled = true
autorun_enabled = false
max_requests_per_run = 20
max_page_size = 1000
max_report_days = 31
max_report_rows = 1000
method_cost_rub = 0
```

Direct Units are not converted to RUB. `RequestId` and sanitized `Units` truth are preserved when present; `Units-Used-Login` is not exposed in ordinary results.

Current official invalid-token documentation conflict is retained explicitly:

```text
errors table → code 53 invalid OAuth token
auth-token page → invalid token references code 1002
```

Implementation must not blindly map all `1002` responses to invalid token; compatibility mapping requires provider context identifying token invalidity.

Dedicated credential model:

```text
credentials.direct = {
  oauth_token,
  client_login,
  checked_at,
  check_state
}
```

No automatic token reuse from Webmaster or Metrika.

Direct Check is exactly one `Campaigns.get` with `FieldNames=[Id]`, `Limit=1`. Empty campaign list is a successful capability result. Check consumes provider Units and must be labeled accordingly in UI.

During the governed Phase-5 popup implementation, also implement the already requested convenience duplicate of the common settings Save button near the active service selector, but it MUST call the exact same existing save handler/state path as the bottom common Save button. It is a UI duplication only, not a second storage/lifecycle implementation.

Canonical Phase-5 documents:

```text
extension/docs/SPECIFICATION_PHASE_5_DIRECT_ADDENDUM.md
extension/docs/PHASE_5_DIRECT_REQUIREMENTS_AND_IMPLEMENTATION_PLAN.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_DIRECT_PHASE5_ADDENDUM.md
```

Mandatory final gate:

```text
all applicable permanent/core/Phase-1/2/3/4 regressions
+
D-00..D-22
+
zero enabled NOT_RUN
+
zero real Yandex Direct traffic during controlled QA
+
exact product immutability
```

Implementation sequence:

```text
1. merge Phase-5 contract docs only
2. fetch exact new live main
3. prove extension/src remains fbc52f9a84195278b7b5e942f2a84c7d69778b98
4. create Phase-5 dev branch from that main
5. dedicated Direct credential + safe backup migration
6. DIRECT_API_V1 protocol + registry + policy
7. trusted Direct provider runtime + semantic error/Units handling
8. four object get routes
9. one online-only Campaign Performance Reports route
10. bounded popup Direct credential/policy UI
11. duplicate top common Save control using same existing save handler
12. focused/unit/integration/browser/lifecycle coverage
13. development verification
14. freeze exact candidate
15. exact artifact transport round-trip
16. independent Codex full applicable gate including D-00..D-22
17. owner-live: approved full API access + Direct token → Check once → listCampaigns once → minimal bounded reads/report only if real data exists
18. close Phase 5 only after live PASS
```

All Direct writes, bids, finance/payment, arbitrary reports, offline report queues and automatic retries remain locked.
