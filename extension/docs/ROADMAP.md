# ROADMAP v0.3 — Yandex Marketing Bridge

Status: active roadmap.
Updated: 2026-08-12.

## Governing rule

**One phase = one service = one controlled live acceptance.**

No new service starts until the current service passes:

```text
official API check
→ implementation
→ source tests
→ exact packaged-extension tests
→ source/package identity
→ syntax/static checks
→ Chromium load smoke
→ controlled real Chrome + production ChatGPT acceptance
→ regression PASS
→ gate PASS
```

## PHASE 0 — REPOSITORY / REFERENCE / CORE DESIGN

**Status: PASS.**

Reference authority remains the owner-supplied audited Wordstat artifact and its canonical documentation.

The Phase 0 architectural decision that placed Job/GitHub concepts inside extension runtime was later proven incorrect by live testing and is superseded by the Phase 1 repair documented below. Historical evidence remains preserved; current living specification is v0.2.

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

is **WITHDRAWN / LIVE FAIL**.

Live failure exposed an incorrect mandatory `job_id` gate (`JOB_ID_MISSING`) and additional missing migration/error-reporting behavior. It must not be installed for further acceptance.

### Current repaired candidate — 0.1.1

Exact artifact:

```text
yandex-marketing-bridge-0.1.1-phase1-repair-candidate.zip
SHA-256 311353e2671052b7170e12db3e1318dfed4f59ccf945c7eda6ec59152ee3abfb
size 172705 bytes
files 41
```

Automated/pre-live evidence:

```text
source full suite:          311/311 PASS
fresh ZIP full suite:       311/311 PASS
source ↔ fresh ZIP:          41/41 byte-identical
fresh ZIP JS/MJS syntax:     36/36 PASS
manifest/package JSON:        2/2 PASS
manifest/package version:   0.1.1 / 0.1.1
Chromium 144 load smoke:     PASS
```

Machine-readable evidence:

```text
extension/tests/PHASE_1_0.1.1_PRELIVE_TEST_EVIDENCE.json
```

### 0.1.1 repair contract

The repaired candidate now enforces:

- no mandatory `job_id` in extension runtime;
- no GitHub/workspace dependency in extension runtime;
- GitHub persistence belongs to ChatGPT/development workflow outside the Bridge;
- one RUN = one immutable active service;
- proven legacy `wsmb_*` storage continuity, including `wsmb_api_key`;
- Export settings / Import settings with intentional secret backup + canonical SHA-256 validation;
- active RUN/manual-operation safety state preserved across import;
- all errors automatically delivered to the bound ChatGPT conversation regardless of Debug Mode;
- Debug Mode only adds additional redacted diagnostics;
- durable error claim/commit/reconciliation fencing;
- recoverable Autorun errors continue toward command waiting when safe;
- unknown external request outcome is never automatically retried;
- Manual invalid command errors also reach ChatGPT;
- error queue state and response contract are consistent;
- Manual on a PAUSED RUN shares the same RUN request/cost budget and cannot bypass it;
- reference conversation binding, owner-tab, native Copy, single-flight and no-blind-retry protections remain regression-covered.

### PHASE 1 CURRENT GATE

**Status: PRE-LIVE PASS / PRODUCTION CHATGPT LIVE ACCEPTANCE PENDING.**

Still required in owner's real Chrome/current production ChatGPT:

1. install exact 0.1.1 candidate;
2. verify popup version and in-place legacy key continuity or Export/Import migration;
3. verify reference-compatible local Copy/toasts;
4. verify one free `getRegionsTree` request after fresh official pricing check;
5. verify `WORDSTAT_RESULT_V1` returns to this conversation;
6. verify deliberately triggered errors return automatically as `YMB_ERROR_V1` with Debug OFF;
7. enable Debug Mode and verify the same error includes additional redacted logs;
8. verify Autorun continues after a recoverable error;
9. verify unknown-request recovery never duplicates the Yandex initiation;
10. verify Pause/Resume/Finish, duplicate-tab and conversation isolation;
11. verify Manual on PAUSED RUN cannot bypass configured RUN cost/request ceilings;
12. perform one minimal paid request only after fresh official tariff verification and only if all earlier gates pass.

No Search implementation is authorized until this acceptance passes.

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
PHASE 1  0.1.0 WITHDRAWN; 0.1.1 PRE-LIVE PASS / PRODUCTION LIVE PENDING
PHASE 2  BLOCKED
PHASE 3  BLOCKED
PHASE 4  BLOCKED
PHASE 5  BLOCKED
PHASE 6  BLOCKED
PHASE 7  BLOCKED
PHASE 8  BLOCKED
```
