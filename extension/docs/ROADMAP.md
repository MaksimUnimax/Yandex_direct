# ROADMAP v0.9 — Yandex Marketing Bridge

Status: active roadmap.  
Updated: 2026-08-25.

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

Controlled gate and owner real-profile functional Wordstat acceptance passed. Phase 1 remains the accepted baseline carried into later combined builds.

---

# PHASE 2 — YANDEX SEARCH / SERP

**Status: LIVE PASS / CLOSED.**

## Enabled first slice

```text
protocol: SEARCH_API_V1
service: search
method: search
mode: synchronous text WebSearch only
provider endpoint: POST https://searchapi.api.cloud.yandex.net/v2/web/search
response format: FORMAT_XML
normalized result: SEARCH_RESULT_V1
```

Still deferred/locked beyond the accepted first slice:

```text
Search async/deferred polling
Search image
Search generative
HTML SERP normalization
yandex.ru scraping
```

## Accepted product / controlled gate

```text
source commit: b7869180c229356a6b3d51ac980ec3da5df4c23c
artifact: yandex-marketing-bridge-0.1.1-phase2-real-profile-binding-repair-candidate.zip
SHA-256: ce824a9fff5ddee47bc0145f57db4da10c6352e782c859fa500e3a1fb98088aa
bytes: 179013
files: 69
ZIP entries: 72
independent Codex complete rerun: PASS
source suite: 244/244 PASS
packaged suite: 244/244 PASS
PD-00..PD-17: ALL PASS
manual_on_transaction: PASS
S-00..S-17: ALL PASS
controlled Search stub requests: 1
real Yandex requests during controlled QA: 0
```

## Owner real-profile/live acceptance

**PASS / COMPLETED.**

The owner executed one real synchronous `SEARCH_API_V1` request through the exact accepted artifact.

```text
request_id: search-392c90df-7440-451b-8b09-d71cdce46720
status: OK
http_status: 200
request_executed: true
automatic_retry: false
response_format: FORMAT_XML
result_count: 5
elapsed_ms: 1347
```

The normalized result list was non-empty and usable. Fresh official tariff verification matched the Bridge estimate of 0.488 RUB for the daytime synchronous request.

Durable evidence:

```text
../tests/PHASE_2_REAL_PROFILE_BINDING_CODEX_COMPLETE_PASS_2026-08-25.md
../tests/PHASE_2_REAL_PROFILE_OWNER_LIVE_SEARCH_PASS_2026-08-25.md
../tests/PHASE_2_OWNER_FUNCTIONAL_LATEST_CHECKPOINT.md
```

Closure:

```text
PHASE 2 SEARCH FIRST SLICE = LIVE PASS / CLOSED
OWNER MANUAL SEARCH FUNCTIONAL RUN = COMPLETE
```

---

# NEXT GOVERNED PATCH — LIFECYCLE GUARD BUTTON GATING

**Status: READY / NEXT BEFORE PHASE 3 IMPLEMENTATION.**

This is an inter-phase unified-core UI/safety patch discovered during owner functional Search testing. It does not invalidate the accepted Phase-2 artifact; it must be delivered as a new governed candidate.

Required behavior:

```text
MANUAL_OPERATION_ACTIVE → Yandex action button disabled / non-clickable
DELIVERY_IN_PROGRESS   → Yandex action button disabled / non-clickable
blocking state cleared → button becomes clickable again
```

Requirements:

- prevent the invalid click in the UI instead of accepting it and only then returning the lifecycle guard error;
- retain existing backend/manual-admission guards as fail-closed defense in depth;
- re-enable only after positive observation that the blocking lifecycle state is cleared;
- do not reset worker timers, delivery timers, service state, or unrelated runtime state merely to refresh button availability;
- preserve current popup geometry;
- add regression coverage for `blocked → click impossible → lifecycle completes → clickable again`;
- any product/package-test byte change creates a new exact candidate and requires the applicable governed gate before owner handoff.

Patch source note:

```text
../tests/PHASE_2_OWNER_FUNCTIONAL_RUN_CHECKLIST_2026-08-25.md
```

After this patch closes, continue directly to Phase 3.

---

# PHASE 3 — WEBMASTER

**Status: UNBLOCKED / QUEUED AFTER LIFECYCLE BUTTON PATCH.**

First Phase-3 action is **governed requirement reconstruction**, not implementation from memory.

Required start sequence:

```text
1. Reconstruct the current Webmaster contract from live canonical docs and historical repo evidence.
2. Define the first Webmaster API slice: protocol, allowed methods, credentials/capability, policy/budget, response normalization and failure semantics.
3. Write/update specification + implementation plan + acceptance/gate requirements before production code.
4. Implement only the approved first slice.
5. Run focused tests, freeze exact candidate, independent Codex full applicable gate, then owner-live acceptance only where irreducible.
```

---

# PHASE 4 — METRIKA

**Status: BLOCKED UNTIL PHASE 3 CLOSES.**
