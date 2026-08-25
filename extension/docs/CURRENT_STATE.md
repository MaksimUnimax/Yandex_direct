# CURRENT STATE — Yandex Marketing Bridge

Status: **PHASE 2 SEARCH REPAIR FROZEN — WINDOWS TRANSPORT PASS / INDEPENDENT CODEX FULL GATE PENDING / OWNER LIVE BLOCKED**  
Updated: 2026-08-25

Always fetch live `main` HEAD and commit metadata before any workflow-stage transition or control-plane write.

## Mandatory reconstruction record

```text
LIVE_HEAD_BEFORE_THIS_STATE_WRITE = ed8f867ebfcdbd96162773e75744dba5b5472dad
PRODUCT_SOURCE = b7869180c229356a6b3d51ac980ec3da5df4c23c
PRODUCT_PARENT = f4aee34c0a3455aa7199f6aa54bd581c71d97337
HANDOFF_ARTIFACT = ce824a9fff5ddee47bc0145f57db4da10c6352e782c859fa500e3a1fb98088aa / 179013 bytes / 69 files / 72 ZIP entries
PAYLOAD_MANIFEST = ee9d99733c99d2562cd7ebb8addca19fa6a34e1fb0bd8002bba44f6bb594acf1 / 12125 bytes
FREEZE_RUN = 32805530317 / 97674800575 PASS
CHATGPT_INTERNAL_FREEZE_GATE = PASS: source 244/244, packaged 244/244, deterministic rebuild PASS, real Yandex requests 0; this is NOT Codex
WINDOWS_SAFE_TRANSPORT = 9fb1fcf17766d8f88b733d8198d1c550e4b8fa77
WINDOWS_TRANSPORT_PROOF = run 32805811476 / job 97675604279 PASS on Windows Server 2025, Git 2.55.0.windows.4, core.autocrlf=true
REPAIR_BROWSER_HARNESS = 81625e073d507d70451f1457185a3e906c640c66 / blob 790539464d7f72214a3126c6585aac74e1afec39
INDEPENDENT_CODEX_FULL_GATE = NOT RUN
PRODUCTION_BYTES_CHANGED_SINCE_FREEZE = NO
PACKAGE_TEST_BYTES_CHANGED_SINCE_FREEZE = NO
OWNER_LIVE = BLOCKED / NOT AUTHORIZED
REAL_YANDEX_REQUESTS_SINCE_REOPEN = 0
OPEN_BLOCKERS = mandatory independent Codex full regression gate has not yet returned PASS on exact ce824a9f... artifact
AUTHORIZED_NEXT_STAGE = INDEPENDENT_CODEX_FULL_GATE_EXACT_CE824A9F
```

## Repaired defect

The real-profile failure occurred before the Yandex provider boundary. Historical evidence proved a working ChatGPT conversation id `6a82924e-5ed0-83eb-84a2-851ddad40c88`, while the reconstructed identity parser incorrectly required RFC UUID version nibbles 1-5. The reconstruction had also lost trusted canonical `/c/<id>` fallback, accepted delivered-but-invalid identity bootstrap as success, circularly disabled Bind when identity was not already confirmed, and reversed the proven Manual-ON transaction order.

The repaired source restores the proven semantics without weakening trusted-origin fences:

```text
- factual ChatGPT conversation ids are accepted without the invalid UUID-version filter;
- location + trusted canonical identity candidates are resolved fail-closed on conflict;
- delivered-but-invalid WS_GET_IDENTITY is not bootstrap success;
- supported ChatGPT page availability is distinct from confirmed conversation identity, so Bind can recover context;
- Manual ON requires content/page acknowledgement before worker authorization;
- Manual OFF safety order remains worker OFF first, then page cleanup.
```

Clean repair source `b786918...` is exactly one commit above `f4aee34...` and changes exactly four production files plus two package-test files. Focused repair verification reached 37/37 PASS and the complete source suite reached 244/244 PASS with zero real Yandex requests.

## New exact frozen candidate

The old `739dd5d7cbefa98568bf51ae0ecab556360db534954fa0e27878ca5a77e7ae46` artifact remains withdrawn/historical and must not be used.

Current exact candidate:

```text
yandex-marketing-bridge-0.1.1-phase2-real-profile-binding-repair-candidate.zip
SHA-256 = ce824a9fff5ddee47bc0145f57db4da10c6352e782c859fa500e3a1fb98088aa
bytes = 179013
files = 69
ZIP entries = 72
payload manifest SHA-256 = ee9d99733c99d2562cd7ebb8addca19fa6a34e1fb0bd8002bba44f6bb594acf1
payload manifest bytes = 12125
```

ChatGPT's exact freeze run passed source 244/244, packaged 244/244, deterministic byte-identical rebuild, syntax/JSON checks and archive integrity. The Actions artifact was downloaded back and round-trip verified before transport work.

## Windows-safe transport

The published transport is one commit above the exact source and contains exactly five QA transport files. Windows Server 2025 with Git `2.55.0.windows.4` and `core.autocrlf=true` successfully reassembled the exact `ce824a9f...` ZIP and matched the full payload manifest.

This proves artifact transport only. It is not a substitute for the independent Codex pre-delivery gate.

## Independent Codex boundary

The exact execution handoff is:

```text
extension/tests/CODEX_PHASE_2_REAL_PROFILE_BINDING_REPAIR_FULL_GATE_HANDOFF_2026-08-25.md
```

Codex must execute the complete permanent gate, Manual-ON addendum, Search Phase-2 addendum and the additional pinned real-profile browser regression. Codex must use zero real credentials and zero real Yandex requests and must not edit product/tests/harness.

Until that independent campaign returns complete PASS:

```text
OWNER_LIVE_SEARCH = BLOCKED
PHASE_3_WEBMASTER = BLOCKED
```

ChatGPT's own Actions/browser evidence may be used as preflight/transport evidence only and must never be relabeled as Codex evidence.

## Current authorized next action

```text
AUTHORIZED_NEXT_ACTION = RUN_INDEPENDENT_CODEX_FULL_GATE_ON_EXACT_CE824A9F
OWNER_LIVE_SEARCH = BLOCKED
PHASE_3_WEBMASTER = BLOCKED
```

Do not refreeze/rebuild/change product bytes unless new evidence proves a defect. Any production or package-test byte change creates a new candidate and restarts the complete controlled gate chain.
