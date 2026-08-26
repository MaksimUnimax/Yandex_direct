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
artifact: yandex-marketing-bridge-0.1.1-phase2-real-profile-binding-repair-candidate.zip
SHA-256: ce824a9fff5ddee47bc0145f57db4da10c6352e782c859fa500e3a1fb98088aa
bytes: 179013
files: 69
ZIP entries: 72
independent Codex complete gate: PASS
owner real-profile/live Search: PASS
```

Still deferred/locked beyond the accepted first slice:

```text
Search async/deferred polling
Search image
Search generative
HTML SERP normalization
yandex.ru scraping
```

---

# INTER-PHASE PATCH — LIFECYCLE GUARD BUTTON GATING

**Status: OWNER LIVE PASS / CLOSED.**

Accepted behavior:

```text
MANUAL_OPERATION_ACTIVE → Yandex action button disabled / non-clickable
DELIVERY_IN_PROGRESS   → Yandex action button disabled / non-clickable
blocking state cleared → button becomes clickable again
```

Exact accepted candidate:

```text
source: 939e880f820e52beae9dcbcedc86d5cd9e13b075
parent: b7869180c229356a6b3d51ac980ec3da5df4c23c
artifact: yandex-marketing-bridge-0.1.1-lifecycle-button-gating-candidate.zip
SHA-256: 0430463ea979c31c5e74a48c899f2ce0fb141b62c4baf132df153380fbc0a262
bytes: 179877
files: 69
ZIP entries: 72
independent Codex complete applicable gate: PASS
owner real-profile acceptance: PASS
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

Owner-live read-only result:

```text
operation: listHosts
request_id: webmaster-d73003d9-74ae-4428-8bc7-eac57be193ea
http_status: 200
status: OK
result.hosts: []
request_executed: true
automatic_retry: false
channel: manual
```

An empty host collection is accepted as a successful real-provider response. No `getSummary` was executed because no real `hostId` was available, preserving the narrow owner-live boundary.

Phase-3 credential architecture now established for the unified core:

```text
Wordstat  → dedicated Api-Key + folderId → Save → Check
Search    → dedicated Api-Key + folderId → Save → Check
Webmaster → dedicated OAuth token + derived user_id → Save → Check
Export/Import preserves service mapping
```

Durable closure evidence:

```text
extension/tests/PHASE3_WEBMASTER_OWNER_LIVE_PASS_2026-08-26.md
```

Still deferred/locked beyond the first slice:

```text
host add/delete
verification mutations
recrawl submission
Sitemap mutation
important URL mutation
original text submission
PRO export tasks
query analytics POST
all other Webmaster POST/DELETE surfaces
```

---

# PHASE 4 — METRIKA

**Status: RECONSTRUCTION AUTHORIZED.**

Phase 3 is closed, so Phase 4 is no longer blocked.

No Metrika production implementation is authorized yet. The next governed stage is official API reconstruction and first-slice definition.

Required reconstruction sequence:

```text
1. identify current official Yandex Metrika API version/base endpoints
2. establish OAuth/scopes and whether existing Webmaster OAuth storage may or may not be reused
3. inventory read-only reporting/management surfaces
4. choose a minimal useful first slice
5. define METRIKA_API_V1 and normalized result envelope
6. define request/pagination/quota/cost/error truthfulness and no-retry behavior
7. lock all write/mutation surfaces by default
8. define service-specific credential/UI changes if needed
9. write Phase-4 specification + requirements/implementation plan + Codex gate addendum
10. authorize implementation only after the contract is complete
```
