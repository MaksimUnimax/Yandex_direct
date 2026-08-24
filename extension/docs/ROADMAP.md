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

For exact current identities, blockers and the authorized next action, `CURRENT_STATE.md` is authoritative over this roadmap.

---

# PHASE 0 — REPOSITORY / REFERENCE / CORE DESIGN

**Status: PASS.**

Reference authority remains the owner-supplied audited Wordstat material and current canonical documentation.

Historical early Job/GitHub runtime coupling is superseded: GitHub/job concepts are external workflow concerns, not mandatory Bridge runtime dependencies.

---

# PHASE 1 — WORDSTAT + UNIFIED CORE

**Status: LIVE PASS / CLOSED.**

Accepted exact artifact:

```text
yandex-marketing-bridge-0.1.1-phase1-manual-enable-order-fix-candidate.zip
SHA-256: e13a26072039550792e740b8ed73e2bd56d48bdceb075a060406d2359e402a65
bytes: 209505
files: 45
ZIP entries: 48
```

Final controlled gate:

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

Final owner real-profile functional acceptance:

```text
getRegionsTree            PASS
getTop                    PASS
getDynamics               PASS after correction of invalid test date instruction
getRegionsDistribution    PASS
```

Phase-1 authority remains historical accepted baseline only; it does not replace the combined Wordstat+Search Phase-2 gate.

---

# PHASE 2 — YANDEX SEARCH / SERP

**Status: STAGE 4 ACTIVE — EXACT REFROZEN CANDIDATE READY FOR A NEW COMPLETE CODEX GATE.**

The older roadmap wording that Phase-2 implementation had not started is superseded by the completed Phase-2 development history and current `CURRENT_STATE.md`.

## Enabled first Search slice

```text
protocol: SEARCH_API_V1
service: search
method: search
mode: synchronous text WebSearch only
provider endpoint: POST https://searchapi.api.cloud.yandex.net/v2/web/search
response format: FORMAT_XML
normalized result: SEARCH_RESULT_V1
```

Current companion authority:

```text
extension/docs/PHASE_2_SEARCH_REQUIREMENTS_AND_IMPLEMENTATION_PLAN.md
extension/docs/SPECIFICATION_PHASE_2_SEARCH_ADDENDUM.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_SEARCH_PHASE2_ADDENDUM.md
```

Still locked in Phase 2:

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

**Status: PASS / COMPLETED.**

Search protocol registration, strict validation/request building, Base64 XML decode and `SEARCH_RESULT_V1` normalization are implemented and covered by the frozen source suite.

## Stage 2 — provider / credentials / policy

**Status: PASS / COMPLETED.**

Current Search provider path, local credential capability, policy/cost guards, request accounting and no-blind-retry semantics are implemented and covered by the frozen source suite.

## Stage 3 — Manual / Autorun / owner / delivery integration

**Status: PASS / COMPLETED.**

Search is integrated through the common Bridge Manual/Autorun lifecycle, owner/conversation fences and durable delivery path; Stage 3 production closure is recorded in current authority.

## Stage 4 — exact pre-delivery candidate

**Status: ACTIVE / PREPARED FOR COMPLETE CODEX RERUN.**

Current exact candidate:

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

Current preflight state:

```text
source suite: 231/231 PASS
packaged suite: 231/231 PASS
packaged syntax: 59/59 PASS
packaged JSON: 2/2 PASS
exact artifact identity: PASS
Windows-safe exact transport consumer proof: PASS
installed-extension browser B-01: PASS
mandatory real-popup Manual-ON B-02: PASS
Search Autorun/operator B-03: PASS
controlled browser Search stub requests: 1
real Yandex requests: 0
```

Current transport authority:

```text
branch: qa/phase2-stage4-final-b64-transport-0ee1d38-2026-08-24
commit: bc7754cff6416ff59942ff6f1052d450792888d5
```

Current browser-harness authority:

```text
commit: 667fda2f9a0e4197c4873ea96f27862c8453f2f0
path: extension/tests/qa_browser/phase2-stage4/browser_phase2_stage4_gate.mjs
Windows PASS run: 32720334374
job: 97410193364
```

Mandatory candidate-specific reconciliations:

```text
extension/docs/CODEX_PHASE2_STAGE4_WINDOWS_TRANSPORT_RECONCILIATION_2026-08-24.md
extension/docs/CODEX_PHASE2_STAGE4_BROWSER_HARNESS_RECONCILIATION_2026-08-24.md
```

The latest complete Codex attempt returned `FAIL_HARNESS` only because current browser venues had not yet been published. That blocker is now reconciled by the exact browser harness and independent Windows PASS above. Product bytes did not change.

### Authorized next Phase-2 action

```text
NEW COMPLETE CODEX CAMPAIGN FROM THE BEGINNING
PD-00..PD-17
+ mandatory Manual-ON transaction
+ S-00..S-17 Search Phase-2 addendum
+ complete source/package suites
+ exact B-01/B-02/B-03 browser harness
+ final artifact/cleanliness proof
```

Owner-live paid Search remains blocked until that complete campaign returns PASS and ChatGPT performs a fresh official pricing check.

---

# PHASE 3 — WEBMASTER

**Status: BLOCKED.**

Do not start until Phase 2 closes its governed owner-live boundary.

---

# PHASE 4 — METRIKA

**Status: BLOCKED.**

Do not start until prior phases close.

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
PHASE 2  SEARCH STAGE 4 — COMPLETE CODEX RERUN AUTHORIZED
PHASE 3  BLOCKED
PHASE 4  BLOCKED
PHASE 5  BLOCKED
PHASE 6  BLOCKED
PHASE 7  BLOCKED
PHASE 8  BLOCKED
```
