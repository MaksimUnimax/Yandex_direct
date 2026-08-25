# CURRENT STATE — Yandex Marketing Bridge

Status: **PHASE 2 SEARCH REPAIR FROZEN — CODEX CAMPAIGN #1 FAIL_HARNESS / STAGE-4 HARNESS RECONCILED / COMPLETE CODEX RERUN READY / OWNER LIVE BLOCKED**  
Updated: 2026-08-25

Always fetch live `main` HEAD and commit metadata before any workflow-stage transition or control-plane write.

## Mandatory reconstruction record

```text
LIVE_HEAD_BEFORE_THIS_STATE_WRITE = d9d3c51605120169e10c6d20e26da91dd2fbbd14
PRODUCT_SOURCE = b7869180c229356a6b3d51ac980ec3da5df4c23c
PRODUCT_PARENT = f4aee34c0a3455aa7199f6aa54bd581c71d97337
HANDOFF_ARTIFACT = ce824a9fff5ddee47bc0145f57db4da10c6352e782c859fa500e3a1fb98088aa / 179013 bytes / 69 files / 72 ZIP entries
PAYLOAD_MANIFEST = ee9d99733c99d2562cd7ebb8addca19fa6a34e1fb0bd8002bba44f6bb594acf1 / 12125 bytes
FREEZE_RUN = 32805530317 / job 97674800575 PASS
WINDOWS_SAFE_TRANSPORT = 9fb1fcf17766d8f88b733d8198d1c550e4b8fa77
WINDOWS_TRANSPORT_PROOF = run 32805811476 / job 97675604279 PASS
REPAIR_BROWSER_HARNESS = 81625e073d507d70451f1457185a3e906c640c66 / blob 790539464d7f72214a3126c6585aac74e1afec39
INDEPENDENT_CODEX_CAMPAIGN_1 = FAIL_HARNESS
CODEX_CAMPAIGN_1_PRODUCT_FAILURE = NO
CODEX_CAMPAIGN_1_REAL_YANDEX_REQUESTS = 0
CURRENT_STAGE4_WRAPPER = 1babfe66222251e2eb63e6e0d4e3eb726ed898e9 / blob e1763df3cec988c3bee93efcdd6369eb8c12d695
CURRENT_STAGE4_PREFLIGHT = run 32809552231 / job 97686152475 PASS
PRODUCTION_BYTES_CHANGED_SINCE_FREEZE = NO
PACKAGE_TEST_BYTES_CHANGED_SINCE_FREEZE = NO
OWNER_LIVE = BLOCKED / NOT AUTHORIZED
REAL_YANDEX_REQUESTS_SINCE_REOPEN = 0
OPEN_BLOCKERS = independent Codex complete rerun has not yet returned PASS on exact ce824a9f... artifact
AUTHORIZED_NEXT_STAGE = INDEPENDENT_CODEX_COMPLETE_RERUN_SAME_EXACT_CE824A9F
```

## Frozen repaired product

The owner-visible real-profile context failure was repaired before this freeze. Historical factual evidence used the real conversation id:

```text
6a82924e-5ed0-83eb-84a2-851ddad40c88
```

The repaired source restores:

```text
- factual ChatGPT conversation-id acceptance without the invalid UUID version 1-5 restriction;
- trusted location + canonical identity resolution with fail-closed conflict handling;
- delivered-but-invalid WS_GET_IDENTITY treated as failure/recovery, not success;
- supported ChatGPT page availability separated from confirmed conversation identity so Bind can recover;
- Manual ON transaction order: page/content acknowledgement before worker authorization;
- Manual OFF safety order: worker OFF before page cleanup.
```

Clean repair source `b786918...` is exactly one commit above `f4aee34...` and changes four production files plus two package-test files. Focused repair verification passed 37/37 and the complete source suite passed 244/244 with zero real Yandex requests.

Current exact artifact:

```text
yandex-marketing-bridge-0.1.1-phase2-real-profile-binding-repair-candidate.zip
SHA-256 = ce824a9fff5ddee47bc0145f57db4da10c6352e782c859fa500e3a1fb98088aa
bytes = 179013
files = 69
ZIP entries = 72
payload manifest SHA-256 = ee9d99733c99d2562cd7ebb8addca19fa6a34e1fb0bd8002bba44f6bb594acf1
payload manifest bytes = 12125
```

The older `739dd5d7...` artifact remains withdrawn and must not be used.

## Freeze and exact transport

ChatGPT-owned freeze/preflight established:

```text
source suite = 244/244 PASS
packaged suite = 244/244 PASS
deterministic byte-identical rebuild = PASS
source syntax = 22/22 PASS
packaged syntax = 63/63 PASS
source JSON = 2/2 PASS
packaged JSON = 2/2 PASS
real Yandex requests = 0
```

The exact Actions artifact was downloaded back and round-trip verified. The Windows-safe B64 transport at `9fb1fcf...` is one commit above exact product source and contains exactly five transport files. Windows Server 2025 / Git 2.55.0.windows.4 / `core.autocrlf=true` successfully reassembled the exact ZIP and full payload manifest with clean checkout.

These are ChatGPT-owned packaging/transport proofs, not Codex evidence.

## Independent Codex campaign #1 — FAIL_HARNESS

The owner supplied the complete independent Codex result. Exact identity, source/package suites, syntax/JSON and the two repair-specific real-profile browser scenarios all passed. No real credentials or Yandex requests were used and product/package-test/repair-harness bytes were not modified.

Blocking result:

```text
verdict = FAIL_HARNESS
gate = B-03 / PD-10 / S-11
error = TimeoutError: Waiting failed: 10000ms exceeded
evidence = browser_phase2_stage4_gate.mjs:109
frozen_product_bytes_involved = NO
enabled_not_run_sections = 0
```

The historical Stage-4 browser harness opened `popup.html` using an obsolete inactive-tab lifecycle and waited directly for `conversationMeta`. That venue predates the repaired `popup_context_bootstrap` initialization contract. The failure therefore does not authorize product mutation or refreeze.

Durable diagnosis/reconciliation:

```text
extension/tests/PHASE_2_REAL_PROFILE_BINDING_STAGE4_HARNESS_RECONCILIATION_2026-08-25.md
```

## Reconciled Stage-4 B-01/B-02/B-03 browser venue

Historical assertion authority remains unchanged:

```text
commit = 667fda2f9a0e4197c4873ea96f27862c8453f2f0
browser harness blob = 127e6042037ac0cbb044e81b2a9c554f24b5aa6b
```

Current external compatibility wrapper:

```text
branch = qa/phase2-current-stage4-browser-harness-b786918-2026-08-25
commit = 1babfe66222251e2eb63e6e0d4e3eb726ed898e9
path = extension/tests/qa_browser/phase2-stage4-current/run_current_stage4_gate.mjs
blob = e1763df3cec988c3bee93efcdd6369eb8c12d695
```

The wrapper changes only temporary QA popup open/close lifecycle. It preserves the historical B-01/B-02/B-03 body and assertions, binds popup bootstrap to the intended active ChatGPT tab, resolves popup by exact tab id, requires the current bootstrap outcome, and confirms tab destruction before reopen.

ChatGPT-owned Windows preflight against the exact transported `ce824a9f...` package:

```text
run = 32809552231
job = 97686152475
Chrome = 151.0.7922.47
puppeteer-core = 25.4.0
result = PASS
```

Observed required markers include:

```text
HISTORICAL_STAGE4_ASSERTIONS_PRESERVED
CURRENT_POPUP_BOOTSTRAP_VENUE_PASS
B01_PROJECT_WORK_PASS
B02_MANUAL_ON_TRANSACTION_PASS
B03_SEARCH_AUTORUN_PASS
BROWSER_CONTROLLED_SEARCH_STUB_REQUESTS=1
BROWSER_GATE_REAL_YANDEX_REQUESTS=0
PHASE2_STAGE4_BROWSER_GATE_PASS
CURRENT_STAGE4_BROWSER_PREFLIGHT_PASS
CURRENT_STAGE4_PREFLIGHT_CLEAN_PASS
```

This is harness preflight only and cannot substitute for independent Codex.

## Independent Codex complete rerun boundary

The first Codex campaign is complete `FAIL_HARNESS`; it must not be partially resumed. The next campaign starts again at Step 0 / PD-00 on the **same exact frozen artifact**.

Current rerun execution authority:

```text
extension/tests/CODEX_PHASE_2_REAL_PROFILE_BINDING_REPAIR_FULL_GATE_RERUN_HANDOFF_2026-08-25.md
```

Codex must execute all enabled PD-00..PD-17, mandatory Manual-ON, S-00..S-17, the reconciled Stage-4 B-01/B-02/B-03 venue, native popup geometry, and both repair-specific real-profile browser scenarios. No enabled `NOT_RUN` may appear in PASS. Zero real credentials and zero real Yandex requests remain mandatory. Codex must not edit product/tests/harness/wrapper.

Until a complete independent PASS returns:

```text
OWNER_LIVE_SEARCH = BLOCKED
PHASE_3_WEBMASTER = BLOCKED
```

## Current authorized next action

```text
AUTHORIZED_NEXT_ACTION = RUN_INDEPENDENT_CODEX_COMPLETE_RERUN_ON_SAME_EXACT_CE824A9F_USING_RECONCILED_STAGE4_WRAPPER
OWNER_LIVE_SEARCH = BLOCKED
PHASE_3_WEBMASTER = BLOCKED
```

Do not refreeze/rebuild/change product or package-test bytes unless separate evidence proves a product defect. A production or package-test byte change creates a new candidate and restarts the complete freeze/transport/Codex chain.