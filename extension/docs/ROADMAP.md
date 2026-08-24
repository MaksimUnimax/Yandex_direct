# ROADMAP v0.7 — Yandex Marketing Bridge

Status: active roadmap.  
Updated: 2026-08-24.

## Governing rule

**One phase = one service = one controlled development closure + one final live acceptance boundary.**

Testing cadence:

```text
during development/change
→ focused tests for changed code + affected dependencies

working candidate frozen for handoff
→ exact artifact preparation through mandatory QA transport runbook
→ one complete Codex pre-delivery regression campaign
→ exact package/identity verification
→ owner real-profile/live acceptance only for irreducible live behavior
```

Current exact identities, blockers and next action are authoritative in:

```text
extension/docs/CURRENT_STATE.md
```

---

# PHASE 0 — REPOSITORY / REFERENCE / CORE DESIGN

**Status: PASS / CLOSED.**

---

# PHASE 1 — WORDSTAT + UNIFIED CORE

**Status: LIVE PASS / CLOSED.**

Accepted artifact:

```text
yandex-marketing-bridge-0.1.1-phase1-manual-enable-order-fix-candidate.zip
SHA-256: e13a26072039550792e740b8ed73e2bd56d48bdceb075a060406d2359e402a65
bytes: 209505
files: 45
ZIP entries: 48
```

Controlled gate and owner real-profile functional Wordstat acceptance both passed. Phase-1 remains the accepted baseline carried into later combined builds.

---

# PHASE 2 — YANDEX SEARCH / SERP

**Status: CONTROLLED PRE-DELIVERY PASS — OWNER LIVE SEARCH AUTHORIZED.**

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

## Stage 1 — Search foundation

**PASS / COMPLETED.**

Protocol registration, strict validation/request building, Base64 XML decode and `SEARCH_RESULT_V1` normalization are implemented.

## Stage 2 — provider / credentials / policy

**PASS / COMPLETED.**

Search provider path, credential capability, cost/policy guard, exactly-once initiation accounting and no-blind-retry semantics are implemented.

## Stage 3 — Manual / Autorun / owner / delivery integration

**PASS / COMPLETED.**

Search uses the common Bridge lifecycle, owner/conversation fences and durable result/error delivery path.

## Stage 4 — exact pre-delivery candidate

**CONTROLLED PASS / COMPLETED.**

Exact candidate:

```text
source commit: 0ee1d38f8d28cfccceb5a07f9606fa715261bc27
artifact: yandex-marketing-bridge-0.1.1-phase2-search-reconstruction-candidate.zip
SHA-256: d58b5bd20921e9492a90b687ae3910c7049ddff17741da44ba832369eb1c0f16
bytes: 170734
files: 65
ZIP entries: 68
payload manifest SHA-256: 0edfcecdfb1025e7292d2d81f36b8fb6e5edb6f3332ef884d7f31e604ebdf7de
payload manifest bytes: 11421
```

Final complete Codex campaign:

```text
PD-00..PD-17: ALL PASS
mandatory Manual-ON transaction: PASS
S-00..S-17: ALL PASS
source suite: 231/231 PASS
packaged suite: 231/231 PASS
packaged syntax: 59/59 PASS
packaged JSON: 2/2 PASS
browser B-01: PASS
browser B-02: PASS
browser B-03: PASS
controlled Search stub requests: 1
real Yandex requests: 0
real credentials: NO
production modified during gate: NO
tests modified during gate: NO
not_run_enabled_sections: 0
failures: []
verdict: PASS
```

Durable evidence:

```text
extension/tests/PHASE_2_STAGE_4_CODEX_FULL_GATE_PASS_2026-08-24.md
```

## Final Phase-2 live boundary

Fresh official Search pricing was checked after the complete gate PASS:

```text
daytime synchronous: 488 RUB / 1000 = 0.488 RUB/request
night synchronous:   366 RUB / 1000 = 0.366 RUB/request
night window:         00:00:00–07:59:59 UTC+3
```

Canonical owner-live procedure:

```text
extension/docs/PHASE_2_0.1.1_LIVE_ACCEPTANCE.md
```

Only one minimal real synchronous Search request is required. Controlled browser/UI checks are not manually repeated.

Expected current live request reservation:

```text
0.488 RUB
```

On a truthful usable `SEARCH_RESULT_V1` PASS:

```text
PHASE 2 SEARCH FIRST SLICE = LIVE PASS / CLOSED
→ PHASE 3 WEBMASTER may unlock
```

On ambiguous provider outcome, no blind retry is allowed.

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
PHASE 2  SEARCH CONTROLLED PASS / OWNER LIVE AUTHORIZED
PHASE 3  BLOCKED UNTIL PHASE 2 LIVE PASS
PHASE 4  BLOCKED
PHASE 5  BLOCKED
PHASE 6  BLOCKED
PHASE 7  BLOCKED
PHASE 8  BLOCKED
```
