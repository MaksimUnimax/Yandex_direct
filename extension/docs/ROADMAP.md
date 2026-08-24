# ROADMAP v0.6 — Yandex Marketing Bridge

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

## Final controlled and owner-live acceptance

```text
PD-00..PD-17: ALL PASS
source suite: 361/361 PASS
packaged suite: 361/361 PASS
source/package identity: PASS
owner-live getRegionsTree: PASS
owner-live getTop: PASS
owner-live getDynamics: PASS
owner-live getRegionsDistribution: PASS
PHASE 1 LIVE PASS = TRUE
```

Historical withdrawn/failed artifacts remain historical evidence only and must not be used for current acceptance.

---

# PHASE 2 — YANDEX SEARCH / SERP

**Status: STAGE 4 ACTIVE — FROZEN-CANDIDATE / PRE-DELIVERY PREPARATION.**

Current Search slice:

```text
SEARCH_API_V1
method = search
POST https://searchapi.api.cloud.yandex.net/v2/web/search
synchronous text web search
responseFormat = FORMAT_XML
SEARCH_RESULT_V1
```

Explicitly outside the current slice:

```text
searchAsync / polling
image Search
generative Search
HTML SERP normalization
yandex.ru scraping
```

Phase-2 requirement reconstruction is complete. The current functional reconstruction exists on:

```text
candidate/phase2-search-reconstruction-2026-08-23
PR #5
```

Four-stage execution status:

```text
STAGE 1 — exact base + Search foundation                 PASS / COMPLETED
STAGE 2 — worker/provider/credential/policy execution    PASS / COMPLETED
STAGE 3 — Manual/Autorun/operator/delivery integration   PASS / COMPLETED
STAGE 4 — frozen candidate/full gate/owner-live          ACTIVE
```

Final Stage-3 production authority:

```text
75d18291224069a6ae67c110498481ec7320d3c0
fix: recover missing Autorun start delivery
service_worker.js blob 87b90dcb0a1ecca8afc5587d8ab7f6ddfd2c241a
```

Final Stage-3 focused development verification:

```text
workflow: phase2-focused-development
run: 32703002791
job: 97358197549
focused Stage-3 tests: 77/77 PASS
service_worker.js syntax: PASS
popup.js syntax: PASS
real owner-live Search requests: 0
```

Durable Stage-3 checkpoint:

```text
extension/tests/PHASE_2_STAGE_3_FOCUSED_CHECKPOINT_2026-08-24.md
```

Stage 4 now owns the remaining Phase-2 work:

```text
freeze one exact combined Wordstat+Search candidate
production/test hashes + complete target manifest
deterministic package + source/package identity
mandatory QA transport round-trip / consumer-conformance
one complete combined pre-delivery regression gate
zero real Yandex traffic during controlled gate
then minimal owner-live real Search acceptance
```

A Stage-4 gate failure may reopen only the proven failing layer; Stage 3 is not reopened for speculative adjacent edge-case searching.

---

# PHASE 3 — WEBMASTER

**Status: BLOCKED PENDING PHASE 2 LIVE PASS.**

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
PHASE 2  YANDEX SEARCH — STAGE 4 ACTIVE
PHASE 3  BLOCKED PENDING PHASE 2 LIVE PASS
PHASE 4  BLOCKED
PHASE 5  BLOCKED
PHASE 6  BLOCKED
PHASE 7  BLOCKED
PHASE 8  BLOCKED
```
