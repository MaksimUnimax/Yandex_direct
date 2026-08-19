# ROADMAP v0.4 — Yandex Marketing Bridge

Status: active roadmap.  
Updated: 2026-08-19.

## Governing rule

**One phase = one service = one controlled development closure + one final live acceptance boundary.**

Testing cadence:

```text
during development/change
→ focused tests for changed code + affected dependencies only

working candidate frozen and intended for owner handoff
→ ONE complete Codex pre-delivery regression campaign
→ exact package/identity verification
→ only then owner/live acceptance where required
```

Permanent operating/process authority:

```text
extension/docs/WORKFLOW_OPERATING_RULES.md
```

Compact current-state authority:

```text
extension/docs/CURRENT_STATE.md
```

Permanent pre-delivery gate authority:

```text
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md
```

No new service starts until the current service passes governed owner real-profile/live acceptance. Controlled Codex/Puppeteer evidence must never be relabeled as owner real-profile/live evidence.

---

# CURRENT PHASE-1 AUTHORITY — 2026-08-19

Older candidate/hash blocks are historical evidence only and are **not current distribution authority**.

## Current exact frozen product

Version:

```text
0.1.1
```

Exact frozen production hashes:

```text
content_script.js 6358418ff04de37a21368a28046c1109280a7a6b8d942972a319d4dc09dabd9e
service_worker.js 2ae878ed4a5f89e07056dd228344b3c3ab0086f5f8d6d1e026431a9e23bd3e3b
```

Exact handoff/tested artifact:

```text
yandex-marketing-bridge-0.1.1-phase1-external-ui-manual-delivery-candidate.zip
SHA-256 31cc5f3f8a8fe0df9450bb9abd005996ddf7d842df0b18c7bafd0631ed6a4e14
size 209697 bytes
files 45
```

Deterministic package evidence:

```text
Build A SHA-256 31cc5f3f8a8fe0df9450bb9abd005996ddf7d842df0b18c7bafd0631ed6a4e14
Build B SHA-256 31cc5f3f8a8fe0df9450bb9abd005996ddf7d842df0b18c7bafd0631ed6a4e14
A/B byte-identical: YES
source ↔ fresh extraction: 45/45 byte-identical
```

## Latest complete pre-delivery gate

The exact candidate above received one complete Codex gate PASS against product/governance authority:

```text
07e0140d0a01a327d639e23bea8446a79818ceac
```

Result:

```text
PD-00..PD-17:                            ALL PASS
source suite:                            361/361 PASS
fresh packaged suite:                    361/361 PASS
JS/MJS syntax:                            40/40 PASS
JSON:                                      2/2 PASS
source/package identity:                  45/45 PASS
Chrome for Testing / Puppeteer runtime:   PASS
real Yandex requests:                         0
production modified during gate:             NO
failures:                                  NONE
verdict:                                   PASS
```

Exact Codex report paths recorded by the completed campaign:

```text
D:\codex\Yandex\qa-evidence-ymb-full-gate-20260819-04\CODEX_YANDEX_PRE_DELIVERY_FULL_REGRESSION_GATE_2026-08-19.md
D:\codex\Yandex\qa-evidence-ymb-full-gate-20260819-04\CODEX_YANDEX_PRE_DELIVERY_FULL_REGRESSION_GATE_2026-08-19.json
```

## Post-gate documentation reconciliation

After this product PASS, documentation/process governance was corrected to prevent repeated QA/workflow mistakes and to remove stale current-contract wording.

The reconciliation is documentation/process-only with respect to production bytes. `SPECIFICATION.md` was corrected to match the already-tested product/gate behavior:

- Bridge-owned external Yandex action independent of native Copy lifecycle;
- Yandex action available before native Copy exists when structural binding is valid;
- current Manual completion is Send→ready/Microphone;
- obsolete matching-sent-user-turn `manual_reconcile`, 12-attempt retry budget and reconciliation exhaustion are not current acceptance behavior.

The gate's product assertions already tested these current behaviors before the documentation reconciliation. Therefore this reconciliation does **not** create a new product candidate by itself.

Whether any later documentation change requires refreshed gate evidence is governed by `WORKFLOW_OPERATING_RULES.md`; do not assume either that every docs change invalidates PASS or that docs can never invalidate PASS.

## Current Phase-1 gate state

```text
PRE-DELIVERY FULL REGRESSION: PASS
EXACT ARTIFACT: 31cc5f3f8a8fe0df9450bb9abd005996ddf7d842df0b18c7bafd0631ed6a4e14
OWNER REAL-PROFILE ACCEPTANCE: PENDING
PHASE 1 LIVE PASS: FALSE until owner acceptance
PHASE 2 SEARCH: BLOCKED
```

Issues #1 and #2 remain open until owner real-profile acceptance confirms the repaired behavior.

---

# PHASE 0 — REPOSITORY / REFERENCE / CORE DESIGN

**Status: PASS.**

Reference authority remains the owner-supplied audited Wordstat artifact and its canonical documentation.

The early Phase-0/Phase-1 decision that placed Job/GitHub concepts inside extension runtime was later proven wrong by live testing and is superseded by the current contracts. Historical evidence remains preserved in the append-only development context.

---

# PHASE 1 — WORDSTAT + UNIFIED CORE

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

## Current 0.1.1 contract

The current Phase-1 implementation enforces:

- no mandatory `job_id` in extension runtime;
- no GitHub/workspace dependency in extension runtime;
- one RUN = one immutable active service;
- legacy `wsmb_*` storage continuity;
- Export/Import settings backup with SHA-256 validation and active-state safety;
- all bound-conversation errors automatically delivered regardless of Debug Mode;
- Debug Mode adds only redacted diagnostics;
- durable worker-owned result/error delivery and no duplicate Send;
- recoverable Autorun continuation when safe;
- unknown external request outcome is never blindly retried;
- Manual on a PAUSED RUN shares the same RUN request/cost budget;
- owner-tab/conversation/single-flight fences remain fail-closed;
- native Copy remains native and never dispatches Bridge Manual;
- Manual ON uses one Bridge-owned **external** Yandex action per structurally/uniquely bound eligible block, independent of native Copy lifecycle;
- current Manual committed-delivery recovery is watch-only; ready/Microphone confirmation releases the lock; occupied composer text is preserved and resumed exactly once when safe.

## Historical withdrawn/superseded artifacts

### 0.1.0 — withdrawn

```text
yandex-marketing-bridge-0.1.0-phase1-wordstat-candidate.zip
SHA-256 79c2bca5e2e65aaa1cb7cc38754589a0bf3b0b436c82f36416934cd175cafa2a
```

Status: **WITHDRAWN / LIVE FAIL**.

### Historical 0.1.1 artifact `4973…`

```text
yandex-marketing-bridge-0.1.1-phase1-final-live-acceptance-candidate.zip
SHA-256 4973c5f87c3ad7d4c052e66c449c2afef412d20a6e4d767bbe761d62abf7cb84
```

This artifact historically passed an earlier controlled gate, but owner real-profile acceptance found:

1. Yandex action was not independent enough from native Copy lifecycle;
2. a later Manual action could remain blocked by stale `MANUAL_OPERATION_ACTIVE` after committed delivery completion was not reconciled correctly.

Therefore `4973…` is **historical and must not be used for current acceptance**.

## Historical live-fix / harness investigation

The 2026-08-18/19 repair campaign included focused source tests, controlled browser checks, harness failures and later architecture corrections. Those intermediate `HARNESS_FAIL`, `FAIL_ARTIFACT` and partial results remain historical evidence only.

They do not override the latest complete PASS on artifact `31cc5f…`.

The permanent QA/workflow lessons from that campaign are now captured in:

```text
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md
extension/docs/WORKFLOW_OPERATING_RULES.md
```

---

# PHASE 1 CURRENT GATE

**Status: PRE-DELIVERY FULL REGRESSION PASS / OWNER REAL-PROFILE LIVE ACCEPTANCE PENDING.**

The exact artifact allowed to enter owner real-profile acceptance is only:

```text
yandex-marketing-bridge-0.1.1-phase1-external-ui-manual-delivery-candidate.zip
SHA-256 31cc5f3f8a8fe0df9450bb9abd005996ddf7d842df0b18c7bafd0631ed6a4e14
```

Controlled PASS is not itself Phase 1 LIVE PASS.

No Search implementation is authorized until Phase 1 owner live acceptance passes.

---

# PHASE 2 — YANDEX SEARCH / SERP

**Status: BLOCKED BY PHASE 1 LIVE GATE.**

After unlock, add Search read collection incrementally. Paid operation classes must have separate operator-controlled limits and exactly-once initiation semantics.

# PHASE 3 — WEBMASTER

**Status: BLOCKED.**

Read-first. Missing OAuth/access returns controlled unavailable/error evidence without breaking unrelated services.

# PHASE 4 — METRIKA

**Status: BLOCKED.**

Read-first; large/async and write operations separated into later permission classes.

# PHASE 5 — DIRECT READ

**Status: BLOCKED.**

Prove zero mutation and quota guard before any write work.

# PHASE 6 — DIRECT DRAFT / PRE-LIVE WRITE

**Status: BLOCKED.**

Every write requires expected-change validation and read-back verification.

# PHASE 7 — DIRECT LIVE WRITE

**Status: BLOCKED.**

No unrestricted live-write Autorun. Explicit changeset/transaction approval + verification required.

# PHASE 8 — FULL ORDER E2E

**Status: BLOCKED.**

Order workspaces in GitHub remain an external ChatGPT workflow and are not a Bridge runtime dependency.

---

# Current status summary

```text
PHASE 0  PASS
PHASE 1  0.1.0 WITHDRAWN
PHASE 1  historical 0.1.1 artifact 4973… WITHDRAWN AFTER OWNER LIVE FAIL
PHASE 1  current 0.1.1 artifact 31cc… PRE-DELIVERY FULL REGRESSION PASS
PHASE 1  OWNER REAL-PROFILE LIVE ACCEPTANCE PENDING
PHASE 2  BLOCKED
PHASE 3  BLOCKED
PHASE 4  BLOCKED
PHASE 5  BLOCKED
PHASE 6  BLOCKED
PHASE 7  BLOCKED
PHASE 8  BLOCKED
```
