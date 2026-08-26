# ROADMAP v0.9 — Yandex Marketing Bridge

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
methods:
  listHosts
  getSummary
  getDiagnostics
  getPopularQueries
writes: disabled
```

Accepted product identity:

```text
source: a7d9f947759f4f6a4fc20b39c7df3f25d81ce3e5
frozen ZIP SHA-256: 1c700640d5fa7b041468c1b987ce3793f4da7631b417e9fb5b0a59b54abd1fd8
frozen ZIP bytes: 222592
accepted src tree: e5fa694f1354e1ee048a352481a416413e94a3c9
merged main: 6c95cf15462b5ad61a267bf1186bb75fa8dd4dff
independent Codex final gate: PASS
post-merge source suite: 313 / 313 PASS
owner-live acceptance: PASS
```

Owner-live:

```text
listHosts → HTTP 200 / OK
request_executed = true
automatic_retry = false
result.hosts = []
```

No host-specific live call was made because no real `hostId` was returned.

Durable closure evidence:

```text
extension/tests/PHASE3_WEBMASTER_OWNER_LIVE_PASS_2026-08-26.md
```

Webmaster writes and deferred advanced surfaces remain locked.

---

# PHASE 4 — METRIKA

**Status: CONTRACT READY / IMPLEMENTATION AUTHORIZED.**

Official reconstruction and the first-slice contract are complete.

Service contract:

```text
service: metrika
protocol: METRIKA_API_V1
result: METRIKA_RESULT_V1
auth: dedicated OAuth token with metrika:read
Management API: https://api-metrika.yandex.net/management/v1
Reports API: https://api-metrika.yandex.net/stat/v1
```

First slice:

```text
listCounters
getCounter
getTrafficSummary
getTrafficByTime
```

Provider mapping:

```text
listCounters      → GET /management/v1/counters
getCounter        → GET /management/v1/counter/{counterId}
getTrafficSummary → GET /stat/v1/data
getTrafficByTime  → GET /stat/v1/data/bytime
```

Report metrics are fixed in the first slice:

```text
ym:s:visits
ym:s:users
ym:s:pageviews
```

Metrika gets a dedicated OAuth credential record. It must not automatically reuse the Webmaster OAuth token.

Explicit Check:

```text
GET /management/v1/counters?per_page=1
```

A 200 response with either an empty or non-empty counter list is a successful capability check.

Default local policy:

```text
manual_enabled = true
autorun_enabled = false
allowed_methods = listCounters,getCounter,getTrafficSummary,getTrafficByTime
max_requests_per_run = 50
max_report_days = 366
cost = 0
```

First-slice write lock:

```text
all Management API mutations = disabled
Import API = disabled
Logs API = disabled
arbitrary raw report constructor = disabled
arbitrary metrics/dimensions/filters/preset = disabled
POST/PUT/PATCH/DELETE provider operations = disabled
```

Canonical Phase-4 documents:

```text
extension/docs/SPECIFICATION_PHASE_4_METRIKA_ADDENDUM.md
extension/docs/PHASE_4_METRIKA_REQUIREMENTS_AND_IMPLEMENTATION_PLAN.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_METRIKA_PHASE4_ADDENDUM.md
```

Mandatory final gate:

```text
permanent/core/Phase-1/2/3 applicable regressions
+
M-00..M-19
+
zero enabled NOT_RUN
+
zero real Yandex traffic during controlled QA
```

Implementation sequence:

```text
1. land Phase-3 closure + Phase-4 contract docs on live main
2. verify accepted Phase-3 src tree unchanged
3. create Phase-4 dev branch from exact live main
4. dedicated Metrika credential + backup migration
5. METRIKA_API_V1 protocol + registry + policy
6. trusted Metrika provider executor
7. bounded popup credential/policy UI
8. focused/unit/integration/browser coverage
9. development verification
10. exact candidate freeze
11. exact transport round-trip
12. independent Codex full applicable gate including M-00..M-19
13. owner-live: Check once → listCounters once → bounded traffic read only if real counter exists
14. close Phase 4 only after live PASS
```
