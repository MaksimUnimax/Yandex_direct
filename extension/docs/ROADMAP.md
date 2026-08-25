# ROADMAP v0.8 — Yandex Marketing Bridge

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
→ one complete governed pre-delivery regression campaign
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

**Status: CONTROLLED PRE-DELIVERY PASS — OWNER LIVE SEARCH AUTHORIZED / PENDING.**

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

Still locked:

```text
Search async/deferred polling
Search image
Search generative
HTML SERP normalization
yandex.ru scraping
Webmaster
Metrika
Direct
```

## Stages 1–3 — implementation

**PASS / COMPLETED.**

Search protocol/validation, provider/credential/policy guard, exactly-once initiation/no-blind-retry behavior, XML normalization, Manual/Autorun integration, conversation ownership and durable delivery are implemented and covered by the controlled regression suite.

## Stage 4 — current exact pre-delivery candidate

**CONTROLLED PASS / COMPLETED.**

Current exact candidate after Chrome-151 popup geometry repair and already-open-ChatGPT context-recovery repair:

```text
source commit: f4aee34c0a3455aa7199f6aa54bd581c71d97337
artifact: yandex-marketing-bridge-0.1.1-phase2-search-context-recovery-candidate.zip
SHA-256: 739dd5d7cbefa98568bf51ae0ecab556360db534954fa0e27878ca5a77e7ae46
bytes: 175971
files: 68
ZIP entries: 71
payload manifest SHA-256: bbe8b2665c3339f9ac4bc2243b88a4076680a585220d38b224d10ae02cd91478
payload manifest bytes: 11933
Windows-safe transport commit: 7c787eedd9856c3f91fbed85aeaea7f3405ad473
```

Complete governed campaign:

```text
run: 32801788251
job: 97663951211
Windows Server 2025
Chrome for Testing: 151.0.7922.47
source suite: 239/239 PASS
packaged suite: 239/239 PASS
packaged syntax: 62/62 PASS
packaged JSON: 2/2 PASS
B-01 Project/Work: PASS
B-02 mandatory Manual-ON transaction: PASS
B-03 Search Autorun: PASS
B-04 native Chrome-151 action popup geometry: PASS
B-05 already-open-ChatGPT context recovery: PASS
PD-00..PD-17: ALL PASS
mandatory Manual-ON transaction: PASS
S-00..S-17: ALL PASS
controlled Search stub requests: 1
real Yandex requests: 0
real credentials used: NO
production modified during gate: NO
tests modified during gate: NO
not_run_enabled_sections: 0
final exactness: PASS
final cleanliness: PASS
verdict: PASS
```

Durable current evidence:

```text
../tests/PHASE_2_CONTEXT_RECOVERY_FREEZE_PASS_2026-08-25.md
../tests/PHASE_2_CONTEXT_RECOVERY_WINDOWS_TRANSPORT_PASS_2026-08-25.md
../tests/PHASE_2_CONTEXT_RECOVERY_COMPLETE_GATE_PASS_2026-08-25.md
```

Older `0ee1d38... / d58b5bd...` and `10bb3aca... / 0186b35d...` candidates are historical evidence only and are not eligible for the current owner-live handoff.

## Final Phase-2 live boundary

Canonical procedure:

```text
PHASE_2_0.1.1_LIVE_ACCEPTANCE.md
```

Exactly one minimal real synchronous Search request is required. Controlled browser/UI checks are not manually repeated.

Before that paid request, re-check the current official Yandex Search synchronous price and tariff window; do not rely on a historical price snapshot as current billing authority.

On a truthful usable `SEARCH_RESULT_V1` PASS:

```text
PHASE 2 SEARCH FIRST SLICE = LIVE PASS / CLOSED
→ PHASE 3 WEBMASTER may unlock
```

If provider initiation may have happened but the outcome is ambiguous, no blind retry is allowed.

No refreeze, rebuild or another controlled complete gate is authorized unless new evidence invalidates the current PASS.

---

# PHASE 3 — WEBMASTER

**Status: BLOCKED UNTIL PHASE 2 OWNER-LIVE PASS.**

---

# PHASE 4 — METRIKA

**Status: BLOCKED.**

---

# PHASE 5 — DIRECT READ

**Status: BLOCKED.**

---

# PHASE 6 — DIRECT DRAFT / PRE-LIVE WRITE

**Status: BLOCKED.**

---

# PHASE 7 — DIRECT LIVE WRITE

**Status: BLOCKED.**

---

# PHASE 8 — FULL ORDER E2E

**Status: BLOCKED.**

---

# Current status summary

```text
PHASE 0  PASS / CLOSED
PHASE 1  WORDSTAT LIVE PASS / CLOSED
PHASE 2  SEARCH CONTROLLED PASS / OWNER LIVE AUTHORIZED / PENDING
PHASE 3  BLOCKED UNTIL PHASE 2 LIVE PASS
PHASE 4  BLOCKED
PHASE 5  BLOCKED
PHASE 6  BLOCKED
PHASE 7  BLOCKED
PHASE 8  BLOCKED
```
