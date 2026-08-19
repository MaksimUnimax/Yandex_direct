# CURRENT STATE — Yandex Marketing Bridge

Status: **CURRENT CONTROL-PLANE AUTHORITY**  
Updated: 2026-08-19

This file applies immediately in the current conversation and every new/resumed conversation. Live GitHub remains authoritative; always fetch current `main` HEAD before action.

## Repository

```text
repo: MaksimUnimax/Yandex_direct
branch: main
```

## Previous owner-live product failure

The previously full-gate-passed artifact:

```text
yandex-marketing-bridge-0.1.1-phase1-external-ui-manual-delivery-candidate.zip
SHA-256 31cc5f3f8a8fe0df9450bb9abd005996ddf7d842df0b18c7bafd0631ed6a4e14
bytes 209697
files 45
```

failed owner real-profile acceptance before Yandex functional testing could start.

Observed failure: Manual ON briefly decorated an eligible block, then content self-reverted to Manual OFF and removed the external `Яндекс` action. Owner diagnostics showed repeated `manual_on → MANUAL_MODE_APPLIED true → manual_off → MANUAL_MODE_APPLIED false` on the same confirmed tab/conversation.

Classification:

```text
31cc5f... owner-live result: FAIL_PRODUCT
previous full Codex PASS: does not authorize handoff after this uncovered defect
Phase 1 LIVE PASS: FALSE
Search / Phase 2: BLOCKED
```

## Product repair and frozen target candidate

The product/test-design root cause was the incompatible Manual-ON transaction ordering:

- popup committed content ON first, worker ON second;
- content `WS_APPLY_MANUAL_MODE(true)` re-read authoritative worker state;
- worker was still OFF during that re-read;
- content therefore turned itself OFF and removed the Yandex action;
- the old tests did not assert the final cross-layer transaction state.

Permanent mandatory gate supplement:

```text
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_MANUAL_ON_TRANSACTION_ADDENDUM_2026-08-19.md
```

Current frozen repaired target identity:

```text
yandex-marketing-bridge-0.1.1-phase1-manual-enable-order-fix-candidate.zip
SHA-256 e13a26072039550792e740b8ed73e2bd56d48bdceb075a060406d2359e402a65
bytes 209505
files 45
```

Production bytes changed from `31cc5f…` only in:

```text
content_script.js
  old 6358418ff04de37a21368a28046c1109280a7a6b8d942972a319d4dc09dabd9e
  new ddf9ed51c60ab90dcdeb1fcd5a1b955c3dd88dfc53a0ddfd5842d66ebe9a02cc

popup.js
  old 7286ea024033293110ad10ebc16856de0beacf512f6f86a229ac0271ac20c28c
  new ac87ad973e8b673bf0c235a43b3dc29dfb67865594ea62e085f943660f0a7ab2
```

`service_worker.js` remains byte-identical:

```text
2ae878ed4a5f89e07056dd228344b3c3ab0086f5f8d6d1e026431a9e23bd3e3b
```

Development evidence before Codex remains:

```text
focused old-product regression with repaired tests: 42/44 PASS, 2/44 intended FAIL
focused repaired popup+content: 44/44 PASS
source suite: 361/361 PASS
packaged suite: 361/361 PASS
syntax: 40/40 PASS
JSON: 2/2 PASS
source↔package: 45/45 byte-identical
deterministic local ZIP A/B: byte-identical
real Yandex requests: 0
```

These are development checks only, not a pre-delivery PASS.

## QA transport attempts — both artifact attempts failed before product QA

### Attempt 1 — invalid direct-binary GitHub object

The first direct-binary GitHub transport was invalid and removed from `main`.

Expected frozen target:

```text
SHA-256 e13a26072039550792e740b8ed73e2bd56d48bdceb075a060406d2359e402a65
bytes 209505
```

Codex obtained instead:

```text
SHA-256 37d896fb8c1542509abfb33780fee6ca802b0d76238b39d76ec78c309b22cf6d
bytes 14999
not a ZIP
```

Classification:

```text
FAIL_ARTIFACT
product tests: NOT RUN
production modified during gate: NO
```

Permanent lesson: a successful blob/upload/commit call is not transport proof; exact artifact round-trip must be established before a Codex prompt.

### Attempt 2 — reconstruction transport contract insufficient for independent exact package reproduction

Historical reconstruction transport branch/checkpoint:

```text
qa/e13a-reconstruction-transport
3920b8c992a8f9393afddb6a0b36505162848ed1
```

Codex independently verified:

```text
exact 31cc preimage: PASS
transport chunks: PASS
concatenated base64 SHA: PASS
gzip SHA: PASS
raw patch SHA: PASS
git apply check: PASS
target source tree identity: PASS
ZIP A/B byte-identical: PASS
ZIP integrity: PASS
actual reconstructed ZIP bytes: 209505
actual reconstructed ZIP SHA-256: 8359c6cf46ed9ca107675d56aec0d37b9615a009fa007b7f68abcddba3a96400
required frozen ZIP SHA-256: e13a26072039550792e740b8ed73e2bd56d48bdceb075a060406d2359e402a65
```

Therefore the previous label `validated reconstruction transport` is **REVOKED**. The published reconstruction/packaging contract was not sufficient for an independent consumer to reproduce the exact frozen ZIP bytes even though the source tree matched.

Classification:

```text
FAIL_ARTIFACT
PD-00..PD-17 product campaign: NOT RUN
Manual-ON browser transaction regression: NOT RUN
source suite: NOT RUN by Codex in this attempt
packaged suite: NOT RUN by Codex in this attempt
production modified during gate: NO
tests modified during gate: NO
```

The frozen product target `e13a2607…` remains unchanged. These artifact/process failures do not authorize product mutation.

## Permanent governance corrections now active

`WORKFLOW_OPERATING_RULES.md` and `CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md` now permanently require:

- reuse of a demonstrated successful Codex transport route before inventing a new one;
- no Codex prompt before exact transport round-trip proof;
- mandatory transport precedence: proven exact ZIP route → verified exact ZIP route → byte-safe encoding of the exact ZIP bytes → reconstruction only as a genuine last resort;
- successful API/blob/commit response is not byte-identity evidence;
- reconstruction requires a byte-complete executable packaging contract, including all ZIP metadata capable of affecting bytes;
- reconstruction/encoded transport requires fresh independent consumer-conformance to the exact expected SHA/bytes before Codex receives a prompt;
- `FAIL_ARTIFACT` fixes stay in artifact/transport/packaging/prompt layers and do not mutate product bytes.

## Current control-plane reconstruction

```text
PRODUCT_SOURCE = repaired e13a target source; production hashes above
HANDOFF_ARTIFACT = frozen target e13a26072039550792e740b8ed73e2bd56d48bdceb075a060406d2359e402a65 / 209505 / 45 files; NOT YET CODEX-ACCEPTED
LATEST_FULL_GATE = no valid full PASS for e13a; latest attempts FAIL_ARTIFACT before product campaign
PRODUCTION_BYTES_CHANGED_SINCE_LAST_ATTEMPT = NO
OWNER_LIVE = previous 31cc FAIL; e13a owner-live NOT AUTHORIZED before Codex PASS
OPEN_BLOCKERS = exact e13a QA transport not yet proven through current retry path; full Codex gate pending; issues #1/#2 open
AUTHORIZED_NEXT_STAGE = QA_TRANSPORT_REPAIR_AND_PRE_PROMPT_ROUNDTRIP_PROOF
```

## Authorized next stage

```text
AUTHORIZED_NEXT_STAGE = QA_TRANSPORT_REPAIR_AND_PRE_PROMPT_ROUNDTRIP_PROOF
```

ChatGPT must now first identify and reuse the demonstrated successful route that previously carried the exact `31cc5f…` artifact into Codex and reached real gate execution, if that route remains applicable. A new route may be used only after evidence proves the demonstrated route cannot carry the current exact artifact.

Before another Codex prompt is allowed, ChatGPT itself must prove the selected Codex-accessible input path by round-tripping/reassembling the exact frozen `e13a…` ZIP and requiring:

```text
SHA-256 e13a26072039550792e740b8ed73e2bd56d48bdceb075a060406d2359e402a65
bytes 209505
ZIP integrity/open PASS
fresh extracted identity PASS
Codex accessibility of that verified input PASS
owner file handling NO
```

If exact ZIP bytes are encoded for transport, a fresh consumer using only published transport inputs must reassemble the exact `e13a…` ZIP before prompt authorization.

If reconstruction is considered, it is forbidden until evidence establishes that no exact-byte artifact transport is possible; it must then pass the independent consumer-conformance requirements in the living gate before prompt authorization.

No owner real-profile retest is allowed before a complete Codex PASS. The owner remains prompt-only for Codex QA. Issues #1/#2 remain open. Do not start Search.
