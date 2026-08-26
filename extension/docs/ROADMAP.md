# ROADMAP v0.11 — Yandex Marketing Bridge

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

Codex is therefore not limited to QA. It is also an authorized information-gathering/research tool. Research authority does **not** imply permission to edit product/production, credentials, provider account settings or external resources; those require separate authorization.

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
methods:
  listCounters
  getCounter
  getTrafficSummary
  getTrafficByTime
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

Owner-live used real counter `111970611` on `openscript.ru` and proved:

```text
listCounters → HTTP 200 / real counter discovered
getTrafficSummary → HTTP 200 / visits=2 users=2 pageviews=12
getTrafficByTime(group=day) → HTTP 200 / totals=2,2,12
request_executed = true on successful provider calls
automatic_retry = false
```

One preceding by-time attempt was locally blocked with `SEND_BUTTON_NOT_READY` and `request_executed=false`; it did not initiate a Yandex request.

`getCounter` was not required for owner-live and remains controlled-QA covered.

Durable closure evidence:

```text
extension/tests/PHASE4_METRIKA_OWNER_LIVE_PASS_2026-08-26.md
```

Canonical Phase-4 documents remain:

```text
extension/docs/SPECIFICATION_PHASE_4_METRIKA_ADDENDUM.md
extension/docs/PHASE_4_METRIKA_REQUIREMENTS_AND_IMPLEMENTATION_PLAN.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_METRIKA_PHASE4_ADDENDUM.md
```

All Management mutations, Import API, Logs API, arbitrary raw Reports constructor and arbitrary metrics/dimensions/filters/preset remain locked.

---

# PHASE 5 — YANDEX DIRECT

**Status: RECONSTRUCTION AUTHORIZED / IMPLEMENTATION NOT YET AUTHORIZED.**

`PROJECT_PURPOSE.md` identifies Yandex Direct as the remaining planned marketing service after Metrika.

No Direct runtime contract is defined by this roadmap entry. Before any production implementation, the project must reconstruct the current official Yandex Direct API surface and explicitly decide the narrow first slice.

Required control-plane sequence:

```text
1. fetch exact live main after Phase-4 closure docs merge
2. prove accepted Phase-4 extension/src tree remains unchanged
3. research current official Yandex Direct API/auth/quota/read-write behavior; do not infer missing values
4. where direct ChatGPT research is incomplete, assign Codex a read-only evidence task against official Yandex sources, including browser-only documentation and downloadable public reference/spec material when available
5. if a required fact is still unavailable, request one concrete retrieval/action from the project owner and keep the fact UNKNOWN / NOT VERIFIED until evidence exists
6. identify safe read-only first-slice candidates and explicitly defer mutation surfaces unless separately authorized
7. define credential isolation/migration requirements
8. define DIRECT protocol/result contracts and trusted provider mapping only after the research is complete
9. create Phase-5 specification addendum
10. create Phase-5 requirements/implementation plan
11. create mandatory Phase-5 Codex pre-delivery gate addendum
12. land those control-plane docs without modifying product bytes
13. only then authorize implementation from exact live main
```

Until that reconstruction is complete:

```text
Direct protocol prefix = NOT AUTHORIZED
Direct credential model = NOT AUTHORIZED
Direct provider endpoints = NOT AUTHORIZED
Direct methods = NOT AUTHORIZED
Direct writes = NOT AUTHORIZED
```
