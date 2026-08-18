# ROADMAP v0.4 — Yandex Marketing Bridge

Status: active roadmap.  
Updated: 2026-08-18.

## Governing rule

**One phase = one service = one controlled development closure + one final live acceptance boundary.**

Testing cadence is explicitly split:

```text
during development/change
→ focused tests for changed code + affected dependencies only

when a working candidate is frozen and is about to be handed to the owner
→ ONE complete Codex pre-delivery regression campaign
→ exact package/identity verification
→ only then owner/live acceptance where required
```

Permanent pre-delivery gate authority:

```text
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md
```

The full gate is **not** run after every edit. It is mandatory immediately before handing the owner a working build/candidate. Any mandatory FAIL blocks handoff; after a production fix the whole pre-delivery gate is rerun from the beginning on the new exact candidate.

No new service starts until the current service passes its governed live acceptance. Controlled Codex/Puppeteer evidence must never be relabeled as real-profile/live evidence.

## Current authority — 2026-08-18

Older 0.1.1 candidate/hash blocks are retained only as development history where referenced by old evidence. They are **not current distribution authority**.

Current Phase-1 production authority is the exact reconstructed **45-file Manual Surface v2 source tree** governed by the Manual-v2 contract/evidence and patch-part reconstruction records.

Current controlled product state:

```text
exact source identity:                    45/45 PASS
source suite:                             358/358 PASS
actual CfT extension installation:        PASS
MV3 worker/content/popup:                  PASS
Manual OFF/ON convergence:                 PASS
Manual Surface v2 eligible/decorated:      7/7 PASS
content-independent yellow + Яндекс:       PASS
generic response Copy excluded:            PASS
ambiguous locality fail-closed:             PASS
mutation/rescan/idempotence/restore:        PASS
representative click/core controlled QA:   PASS
real Yandex requests in controlled run:     0
production changes needed for QA fixes:     0
```

Controlled Manual-v2 PASS evidence is recorded at commit:

```text
505c73e01f862c38285291e69fc615c86c2f3c37
```

A later attempt to drive the owner's normal Chrome from Codex established only an external capability blocker; it did **not** establish a product FAIL. That history remains in the live ledger.

### Frozen pre-delivery artifact

The mandatory living pre-delivery regression gate was executed against the exact 45-file candidate at authority main SHA:

```text
653adb63a68f98f03f21534658f3397fd389e0c6
```

Validation evidence commit:

```text
c71e1e69aa70babd31c30b4f461323299562ae2b
branch: validation/yandex-pre-delivery-full-regression-2026-08-18
```

Result:

```text
PD-00…PD-17:                            ALL PASS
coverage registry:                       PASS
source suite:                            358/358 PASS
fresh packaged suite:                    358/358 PASS
JS/MJS syntax:                           40/40 PASS
JSON:                                     2/2 PASS
manifest entrypoints:                    11/11 PASS
Chrome for Testing / Puppeteer runtime:  PASS
production modified during gate:          0
harness modified during gate:             0
real Yandex requests:                     0
secrets in report:                        0
```

Exact owner-handoff / final-live-acceptance artifact:

```text
yandex-marketing-bridge-0.1.1-phase1-final-live-acceptance-candidate.zip
SHA-256 4973c5f87c3ad7d4c052e66c449c2afef412d20a6e4d767bbe761d62abf7cb84
size 199530 bytes
files 45
deterministic Build A/B: PASS
source ↔ fresh extraction: 45/45 byte-identical
```

**Pre-delivery regression gate: PASS. Owner handoff is allowed for this exact artifact only.**

Any production-byte change after this checkpoint invalidates this handoff PASS and requires the entire pre-delivery gate to be rerun on the new frozen candidate. Documentation/evidence-only commits do not alter the tested artifact identity.

## PHASE 0 — REPOSITORY / REFERENCE / CORE DESIGN

**Status: PASS.**

Reference authority remains the owner-supplied audited Wordstat artifact and its canonical documentation.

The Phase 0 architectural decision that placed Job/GitHub concepts inside extension runtime was later proven incorrect by live testing and is superseded by the Phase 1 repair documented below. Historical evidence remains preserved.

## PHASE 1 — WORDSTAT + UNIFIED CORE

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

### Withdrawn 0.1.0 candidate

The earlier candidate:

```text
yandex-marketing-bridge-0.1.0-phase1-wordstat-candidate.zip
SHA-256 79c2bca5e2e65aaa1cb7cc38754589a0bf3b0b436c82f36416934cd175cafa2a
```

is **WITHDRAWN / LIVE FAIL** and must not be installed for current acceptance.

### Historical 0.1.1 repair/pre-live candidates

Multiple 0.1.1 development candidates and package checkpoints were produced while repairing Phase 1. Their hashes remain valid historical evidence but do not override the current 45-file Manual Surface v2 authority and frozen pre-delivery artifact described above.

### Current 0.1.1 contract

The current Phase-1 implementation enforces:

- no mandatory `job_id` in extension runtime;
- no GitHub/workspace dependency in extension runtime;
- one RUN = one immutable active service;
- legacy `wsmb_*` storage continuity;
- Export/Import settings backup with SHA-256 validation and active-state safety;
- all bound-conversation errors automatically delivered regardless of Debug Mode;
- Debug Mode adds only redacted diagnostics;
- durable result/error claim/commit/reconciliation and no duplicate Send;
- recoverable Autorun continuation when safe;
- unknown external request outcome is never blindly retried;
- Manual on a PAUSED RUN shares the same RUN request/cost budget;
- owner-tab/conversation/native-Copy/single-flight fences remain fail-closed;
- **Manual Surface v2:** with Manual ON, every uniquely resolved supported assistant code/writing block local Copy is visibly armed yellow + `Яндекс` independent of block contents; generic whole-response Copy is excluded; ambiguous locality fails closed; native Copy remains intact; complete clicked block is sent to worker/core, which owns command discovery/validation/errors.

### PHASE 1 CURRENT GATE

**Status: PRE-DELIVERY FULL REGRESSION PASS / REAL-PROFILE LIVE ACCEPTANCE PENDING.**

The exact frozen artifact above is permitted to enter final owner real-profile/live acceptance. Controlled PASS is not itself Phase 1 LIVE PASS.

The owner's final live acceptance must use this exact artifact identity. If production bytes change, this pre-delivery PASS is invalid and the full Gate must be rerun.

No Search implementation is authorized until Phase 1 live acceptance passes.

### 2026-08-18 live-fix supersession state

The historical artifact `yandex-marketing-bridge-0.1.1-phase1-final-live-acceptance-candidate.zip` (SHA-256 `4973c5f87c3ad7d4c052e66c449c2afef412d20a6e4d767bbe761d62abf7cb84`) passed the controlled pre-delivery Gate historically. Owner real-profile acceptance subsequently found live defects #1 (native Copy/Yandex action not independently surfaced) and #2 (a subsequent Manual action remained `MANUAL_OPERATION_ACTIVE` after committed delivery confirmation was missed). Therefore the old artifact is not the current handoff candidate.

The exact live patch source-focused QA is `183/183 PASS`. Controlled-browser focused validation is pending at document-edit time. A new full pre-delivery Gate must run after focused controlled-browser PASS. Phase 1 LIVE PASS remains **FALSE** and Search remains **BLOCKED**.

Task-015 controlled-browser status: **HARNESS_FAIL / bounded harness correction required**. Independent sibling-control assertions passed, but the harness did not validly establish the positive late-confirmation or negative unresolved-fence scenarios. This is not a product failure classification. Phase 1 LIVE PASS remains **FALSE** and Search remains **BLOCKED**.

## PHASE 2 — YANDEX SEARCH / SERP

**Status: BLOCKED BY PHASE 1 LIVE GATE.**

After unlock, add Search read collection incrementally. Paid operation classes must have separate operator-controlled limits and exactly-once initiation semantics.

## PHASE 3 — WEBMASTER

**Status: BLOCKED.**

Read-first. Missing OAuth/access returns controlled unavailable/error evidence without breaking unrelated services.

## PHASE 4 — METRIKA

**Status: BLOCKED.**

Read-first; large/async and write operations separated into later permission classes.

## PHASE 5 — DIRECT READ

**Status: BLOCKED.**

Prove zero mutation and quota guard before any write work.

## PHASE 6 — DIRECT DRAFT / PRE-LIVE WRITE

**Status: BLOCKED.**

Every write requires expected-change validation and read-back verification.

## PHASE 7 — DIRECT LIVE WRITE

**Status: BLOCKED.**

No unrestricted live-write Autorun. Explicit changeset/transaction approval + verification required.

## PHASE 8 — FULL ORDER E2E

**Status: BLOCKED.**

Order workspaces in GitHub remain an external ChatGPT workflow and are not a Bridge runtime dependency.

## Current status summary

```text
PHASE 0  PASS
PHASE 1  0.1.0 WITHDRAWN
PHASE 1  0.1.1 PRE-DELIVERY FULL REGRESSION PASS / REAL-PROFILE LIVE PENDING
PHASE 2  BLOCKED
PHASE 3  BLOCKED
PHASE 4  BLOCKED
PHASE 5  BLOCKED
PHASE 6  BLOCKED
PHASE 7  BLOCKED
PHASE 8  BLOCKED
```
