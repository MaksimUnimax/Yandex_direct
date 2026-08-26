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

Owner acceptance confirmed the Bridge-owned action is non-clickable while the lifecycle is blocked and returns to normal availability after completion. Validation remained local (`request_executed=false`), so no Yandex provider request was made.

Durable closure evidence:

```text
../tests/LIFECYCLE_BUTTON_GATING_CODEX_COMPLETE_PASS_2026-08-26.md
../tests/LIFECYCLE_BUTTON_GATING_OWNER_LIVE_PASS_2026-08-26.md
```

---

# PHASE 3 — WEBMASTER

**Status: ACTIVE — GOVERNED REQUIREMENT RECONSTRUCTION.**

Production implementation is not yet authorized. First Phase-3 action is reconstruction from current official Yandex Webmaster API documentation plus historical repo evidence.

Required sequence:

```text
1. Reconstruct current Webmaster API capabilities, auth model, quotas/limits and endpoint semantics.
2. Define the first Webmaster API slice: protocol, allowed methods, credentials/capability, policy/budget, response normalization and failure/retry semantics.
3. Write/update Phase-3 specification + implementation plan + acceptance/gate requirements before production code.
4. Implement only the approved first slice.
5. Run focused tests, freeze exact candidate, independent Codex full applicable gate, then owner-live acceptance only where irreducible.
```

---

# PHASE 4 — METRIKA

**Status: BLOCKED UNTIL PHASE 3 CLOSES.**
