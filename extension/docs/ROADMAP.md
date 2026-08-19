# ROADMAP v0.5 — Yandex Marketing Bridge

Status: active roadmap.  
Updated: 2026-08-19.

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

Permanent authorities:

```text
extension/docs/WORKFLOW_OPERATING_RULES.md
extension/docs/CURRENT_STATE.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md
extension/docs/CODEX_QA_ARTIFACT_TRANSPORT_AND_GATE_RUNBOOK.md
```

No new service implementation starts until the current service closes its governed live boundary.

---

# PHASE 0 — REPOSITORY / REFERENCE / CORE DESIGN

**Status: PASS.**

Reference authority remains the owner-supplied audited Wordstat material and current canonical documentation.

Historical early Job/GitHub runtime coupling is superseded: GitHub/job concepts are external workflow concerns, not mandatory Bridge runtime dependencies.

---

# PHASE 1 — WORDSTAT + UNIFIED CORE

**Status: LIVE PASS / CLOSED.**

Service:

```text
active_service = wordstat
```

Supported methods:

```text
getTop
getDynamics
getRegionsDistribution
getRegionsTree
```

## Final exact accepted 0.1.1 artifact

```text
yandex-marketing-bridge-0.1.1-phase1-manual-enable-order-fix-candidate.zip
SHA-256 e13a26072039550792e740b8ed73e2bd56d48bdceb075a060406d2359e402a65
size 209505 bytes
files 45
ZIP entries 48
```

Production hashes:

```text
content_script.js ddf9ed51c60ab90dcdeb1fcd5a1b955c3dd88dfc53a0ddfd5842d66ebe9a02cc
popup.js ac87ad973e8b673bf0c235a43b3dc29dfb67865594ea62e085f943660f0a7ab2
service_worker.js 2ae878ed4a5f89e07056dd228344b3c3ab0086f5f8d6d1e026431a9e23bd3e3b
```

## Final controlled gate

```text
PD-00..PD-17: ALL PASS
Manual-ON transaction regression: PASS
source suite: 361/361 PASS
packaged suite: 361/361 PASS
syntax: 40/40 PASS
JSON: 2/2 PASS
source/package identity: PASS
real Yandex requests during controlled gate: 0
production modified during gate: NO
tests modified during gate: NO
verdict: PASS
```

The exact `e13a…` package was independently reconstructed by Codex through the published byte-complete transport/packer contract before product testing.

## Final owner real-profile functional acceptance

The owner explicitly narrowed final live acceptance to functional Yandex tests only, one at a time, with UI observed naturally during execution.

Exact live results on `e13a…`:

```text
getRegionsTree            PASS
getTop                    PASS
getDynamics               PASS
getRegionsDistribution    PASS
```

The first `getDynamics` test command produced HTTP 400 because its ending date was the first rather than last day of the month. The bridge reported `request_executed:true` and `automatic_retry:false`. After the test-instruction cause was established, a corrected command was issued and returned HTTP 200. Classification: prompt/execution-instruction error, not product failure; no blind retry.

Sequential Manual execution across all results, including the error-delivery contour, proved that the stale Manual-operation lock blocker is resolved in the owner real profile. Repeated new command blocks exposed a usable external `Яндекс` action without requiring native Copy as the execution trigger.

Final Phase-1 authority:

```text
CONTROLLED PRE-DELIVERY GATE = PASS
OWNER REAL-PROFILE YANDEX FUNCTIONAL ACCEPTANCE = PASS
PHASE 1 LIVE PASS = TRUE
Issue #1 = CLOSED / COMPLETED
Issue #2 = CLOSED / COMPLETED
```

Detailed live evidence:

```text
extension/docs/PHASE_1_0.1.1_LIVE_ACCEPTANCE.md
```

Historical withdrawn/failed artifacts remain historical evidence only and must not be used for current acceptance.

---

# PHASE 2 — YANDEX SEARCH / SERP

**Status: UNLOCKED FOR REQUIREMENT RECONSTRUCTION. IMPLEMENTATION NOT STARTED.**

Before any product changes:

1. reconstruct current live project authority;
2. inspect current official Yandex Search API documentation, pricing, auth, quota and operation surface;
3. define the Phase-2 service contract and safety/paid-operation policy;
4. update specification/gate coverage before implementation;
5. preserve the unified Bridge runtime and exactly-once/no-blind-retry invariants.

Do not implement Search from stale memory or historical assumptions.

---

# PHASE 3 — WEBMASTER

**Status: BLOCKED.**

Read-first. Missing OAuth/access returns controlled unavailable/error evidence without breaking unrelated services.

---

# PHASE 4 — METRIKA

**Status: BLOCKED.**

Read-first; large/async and write operations remain separate later permission classes.

---

# PHASE 5 — DIRECT READ

**Status: BLOCKED.**

Prove zero mutation and quota guard before write work.

---

# PHASE 6 — DIRECT DRAFT / PRE-LIVE WRITE

**Status: BLOCKED.**

Every write requires expected-change validation and read-back verification.

---

# PHASE 7 — DIRECT LIVE WRITE

**Status: BLOCKED.**

No unrestricted live-write Autorun. Explicit changeset/transaction approval plus verification required.

---

# PHASE 8 — FULL ORDER E2E

**Status: BLOCKED.**

Order workspaces in GitHub remain an external ChatGPT workflow and are not a Bridge runtime dependency.

---

# Current status summary

```text
PHASE 0  PASS
PHASE 1  WORDSTAT LIVE PASS / CLOSED on exact e13a…
PHASE 2  YANDEX SEARCH UNLOCKED FOR REQUIREMENT RECONSTRUCTION
PHASE 3  BLOCKED
PHASE 4  BLOCKED
PHASE 5  BLOCKED
PHASE 6  BLOCKED
PHASE 7  BLOCKED
PHASE 8  BLOCKED
```
