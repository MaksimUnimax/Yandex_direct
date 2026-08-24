# Phase 2 Stage 4 — browser-harness reconciliation

Date: 2026-08-24  
Status: **CURRENT / MANDATORY BROWSER-VENUE OVERRIDE FOR THE COMPLETE CODEX GATE**

This document reconciles the browser-harness defects exposed by the third complete Codex attempt and by the subsequent owner-authored Windows preflights. It is QA authority only. It does **not** change production bytes, package-test bytes, frozen source, exact ZIP bytes, payload-manifest bytes, or the governed PD/S acceptance semantics.

## Precedence and scope

For the next complete Codex campaign, this document supersedes stale browser-venue instructions in:

- `extension/docs/CODEX_PHASE2_STAGE4_FINAL_HANDOFF_2026-08-24.md`
- `extension/docs/PHASE_2_STAGE_4_CODEX_EXECUTION_MAP_2026-08-24.md`
- `extension/docs/CURRENT_STATE.md`

Specifically, do **not** use the old standalone `browser_project_route_smoke.mjs` venue as the complete B-01/B-02/B-03 authority and do not treat the previously missing B-02/B-03 fixtures as unresolved.

The Windows transport reconciliation remains mandatory and independently supersedes stale references to transport commit `9dedf7bf624174996fae7efa7a4bdbff6904d348`:

`extension/docs/CODEX_PHASE2_STAGE4_WINDOWS_TRANSPORT_RECONCILIATION_2026-08-24.md`

All parent PD/S gate requirements, the Manual-ON addendum, Search Phase-2 addendum, exact frozen candidate identity and acceptance semantics remain in force.

## Frozen candidate remains unchanged

```text
source commit: 0ee1d38f8d28cfccceb5a07f9606fa715261bc27
artifact: yandex-marketing-bridge-0.1.1-phase2-search-reconstruction-candidate.zip
artifact SHA-256: d58b5bd20921e9492a90b687ae3910c7049ddff17741da44ba832369eb1c0f16
artifact bytes: 170734
files: 65
ZIP entries: 68
payload manifest bytes: 11421
payload manifest SHA-256: 0edfcecdfb1025e7292d2d81f36b8fb6e5edb6f3332ef884d7f31e604ebdf7de
```

No refreeze is required.

## Current exact browser-harness authority

```text
harness commit: 667fda2f9a0e4197c4873ea96f27862c8453f2f0
harness file: extension/tests/qa_browser/phase2-stage4/browser_phase2_stage4_gate.mjs
harness blob: 127e6042037ac0cbb044e81b2a9c554f24b5aa6b
TLS cert: extension/tests/qa_browser/phase2-stage4/qa-chatgpt-local.cert.pem
TLS cert blob: d91cb127e8d8f6cfa5a95723a15612fd03478af6
TLS key: extension/tests/qa_browser/phase2-stage4/qa-chatgpt-local.key.pem
TLS key blob: 2d0ab1f091b119d964a7ebdcd15720f6cd9728ad
```

The TLS key is a local-only self-signed QA fixture key for the controlled loopback fixture. It is not a provider credential and is not part of the frozen installable artifact.

The harness drives the **real installed extension** and the **real extension popup**. Popup actions are executed by native DOM events inside the actual popup page so production listeners and worker/content transactions execute normally. The harness does not call internal product shortcuts to fake Manual ON or Autorun state.

The current revision also waits for real popup completion statuses before starting the next action:

```text
Диалог привязан.
Настройки сохранены.
Ручной режим включён.
Ручной режим выключен.
Автоматический режим search запущен.
Пауза включена.
Работа продолжена.
Автоматический режим завершён.
```

This closes the real race discovered when the Bind handler was still executing `refresh()` after worker binding state had already changed.

## Product-byte containment proof

The browser QA infrastructure was added on `main` after transport reconciliation commit `8fe5a751abb9e16225118b8b9bd8c982e6f5e30e`.

Comparison:

```text
base: 8fe5a751abb9e16225118b8b9bd8c982e6f5e30e
head: 667fda2f9a0e4197c4873ea96f27862c8453f2f0
commits: 9
changed paths only:
  .github/workflows/phase2-stage4-browser-harness-verify.yml
  extension/tests/qa_browser/phase2-stage4/browser_phase2_stage4_gate.mjs
  extension/tests/qa_browser/phase2-stage4/qa-chatgpt-local.cert.pem
  extension/tests/qa_browser/phase2-stage4/qa-chatgpt-local.key.pem
```

No frozen production file and no package-test byte changed.

## Independent Windows browser proof — PASS

The synchronized harness was fresh-checked out and executed on Windows against the exact artifact reconstructed from the Windows-safe transport.

```text
QA PR: #10
workflow: phase2-stage4-browser-harness-verify
run: 32720334374
job: 97410193364
conclusion: SUCCESS
OS: Microsoft Windows Server 2025
Git: 2.55.0.windows.4
core.autocrlf: true
harness commit: 667fda2f9a0e4197c4873ea96f27862c8453f2f0
transport commit: bc7754cff6416ff59942ff6f1052d450792888d5
Chrome for Testing: 151.0.7922.47
Puppeteer: 25.4.0
```

Transport/artifact precheck markers:

```text
B64_REASSEMBLY_PASS
EXACT_ZIP_IDENTITY_PASS
ROUNDTRIP_PAYLOAD_MANIFEST_PASS
ROUNDTRIP_ZIP_INTEGRITY_PASS
FROZEN_AUTHORITY_MATCH_PASS
REAL_YANDEX_REQUESTS=0
BROWSER_EXACT_ARTIFACT_MATERIALIZED_PASS
```

Browser markers:

```text
B01_PROJECT_WORK_PASS
BROWSER_STEP_BIND_PASS
BROWSER_STEP_SEARCH_SETTINGS_PASS
BROWSER_STEP_MANUAL_FIRST_ON_PASS
BROWSER_STEP_NATIVE_COPY_PASS
B02_MANUAL_ON_TRANSACTION_PASS
BROWSER_STEP_AUTORUN_START_PASS
BROWSER_STEP_SEARCH_DELIVERY_PASS
B03_SEARCH_AUTORUN_PASS
BROWSER_CONTROLLED_SEARCH_STUB_REQUESTS=1
BROWSER_GATE_REAL_YANDEX_REQUESTS=0
PHASE2_STAGE4_BROWSER_GATE_PASS
BROWSER_HARNESS_CLEAN_PASS
```

This proves that B-01, B-02 and B-03 now have a current executable installed-extension browser venue for the exact frozen candidate.

## What the browser gate proves

### B-01 — Project/Work installed-extension baseline

Require at minimum:

- exact extracted `d58b5bd...` extension installed;
- MV3 worker available;
- Project/Work conversation route recognized;
- real popup initialization complete;
- controlled local HTTPS fixture only;
- no real Yandex traffic.

### B-02 — mandatory real-popup Manual-ON transaction

The harness executes the governed Manual-ON transaction through the real popup and checks the required worker/content/action behavior, including:

- initial Manual OFF truth;
- first real popup Manual ON;
- authoritative worker state;
- exactly one external `Яндекс` action;
- ordinary DOM mutation/resync stability;
- popup reopen truth;
- real popup OFF removal;
- second real popup ON re-arm;
- native Copy independence;
- zero real Yandex requests.

This is the current executable venue for the mandatory Manual-ON addendum.

### B-03 — Search Autorun/operator lifecycle

The harness uses the real popup plus controlled local Search stub and checks:

- governed Search settings save;
- Start;
- WAITING_COMMAND;
- controlled Search command pickup;
- exactly one controlled Search provider-stub initiation;
- result delivery through the real extension path;
- popup reopen truth;
- Pause;
- owner/non-owner isolation;
- Resume;
- Finish;
- zero real Yandex requests.

Deterministic source/integration tests remain mandatory for crash/recovery states that the execution map assigns outside the browser venue.

## Required Codex browser procedure

Start a **new complete campaign from the beginning**. Do not resume a previous stopped Codex workspace state.

After Step-0 authority and exact transport/artifact verification, create a clean detached harness worktree at:

```text
667fda2f9a0e4197c4873ea96f27862c8453f2f0
```

Use the exact extracted frozen extension root and the harness fixtures from that worktree.

Install only the external driver dependency into the QA harness directory without changing tracked bytes:

```text
npm install --prefix extension/tests/qa_browser/phase2-stage4 --no-save --package-lock=false puppeteer-core@25.4.0
```

Use Chrome for Testing `151.0.7922.47` (or the exact same qualified build already available in the Codex environment) and execute:

```text
node extension/tests/qa_browser/phase2-stage4/browser_phase2_stage4_gate.mjs \
  <CHROME_PATH> \
  <EXACT_EXTRACTED_D58B5BD_EXTENSION_ROOT> \
  extension/tests/qa_browser/phase2-stage4/qa-chatgpt-local.key.pem \
  extension/tests/qa_browser/phase2-stage4/qa-chatgpt-local.cert.pem
```

Require all browser markers listed in the Windows PASS evidence above. `BROWSER_CONTROLLED_SEARCH_STUB_REQUESTS` must equal `1`. `BROWSER_GATE_REAL_YANDEX_REQUESTS` must equal `0`.

After browser execution, remove temporary `node_modules`/browser profile/materialized QA files and prove the harness/source checkout is clean.

## Historical browser-harness failures — reconciled

Third Codex attempt reached exact artifact/source/package PASS but returned `FAIL_HARNESS` because the browser venues were not yet published:

```text
B-01 / PD-04: local TLS key/certificate fixture not published
B-02 / Manual-ON: only historical Phase-1 browser fixture available
B-03 / Search Autorun: no current installed-extension browser harness published
```

These were QA-authoring omissions, not product failures.

Subsequent owner preflights exposed and reconciled harness-only defects:

```text
1. Puppeteer ElementHandle/input timeout on background popup
   -> replaced driver-only input with native DOM events inside real popup page

2. DataCloneError from cloning fixture helper function
   -> fixture snapshots made explicitly serializable

3. popup target reuse race
   -> openPopup waits for a newly-created popup target

4. Search settings race after Bind
   -> harness waits for real popup action completion statuses before proceeding
```

No product/runtime/package-test bytes were modified by these fixes.

## Complete campaign remains mandatory

A browser preflight PASS does not itself grant the final Stage-4 PASS. Codex must still execute the entire governed campaign against the same exact candidate:

```text
PD-00..PD-17
+ mandatory Manual-ON real-popup transaction
+ S-00..S-17 Search Phase-2 addendum
+ complete source suite
+ complete packaged suite
+ final artifact/cleanliness proof
```

No enabled mandatory section may remain `NOT_RUN` in a PASS verdict. Browser-owned assertions must use this qualified installed-extension venue. Real Yandex requests and real Yandex credentials remain forbidden.

## Final rule

If the exact harness commit/fixture cannot be consumed or the controlled browser venue itself fails before a product assertion, return `FAIL_HARNESS` with evidence and do not weaken the assertion. If the harness executes and a production assertion fails, classify the actual failing layer. Do not patch product or package tests during the campaign.
