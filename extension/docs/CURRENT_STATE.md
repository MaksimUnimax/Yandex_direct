# CURRENT STATE — Yandex Marketing Bridge

Status: **CURRENT CONTROL-PLANE AUTHORITY**  
Updated: 2026-08-19

This file applies immediately in the current conversation and every new/resumed conversation. Live GitHub remains authoritative; always fetch current `main` HEAD before action.

## Repository

```text
repo: MaksimUnimax/Yandex_direct
branch: main
```

## Owner-live result on previous candidate

The previously full-gate-passed artifact:

```text
yandex-marketing-bridge-0.1.1-phase1-external-ui-manual-delivery-candidate.zip
SHA-256 31cc5f3f8a8fe0df9450bb9abd005996ddf7d842df0b18c7bafd0631ed6a4e14
bytes 209697
files 45
```

has **FAILED owner real-profile acceptance** before Yandex functional testing could start.

Observed failure: Manual ON briefly decorated an eligible block, then content self-reverted to Manual OFF and removed the external `Яндекс` action. Owner diagnostics show repeated `manual_on → MANUAL_MODE_APPLIED true → manual_off → MANUAL_MODE_APPLIED false` on the same confirmed tab/conversation.

Classification:

```text
31cc5f... owner-live result: FAIL_PRODUCT
previous full Codex PASS: does not authorize handoff after this newly proven uncovered defect
Phase 1 LIVE PASS: FALSE
Search / Phase 2: BLOCKED
```

## Root cause

The previous popup Manual-ON transaction and the latest content-state synchronization patch became incompatible:

- popup committed content ON first, worker ON second;
- latest content `WS_APPLY_MANUAL_MODE(true)` immediately re-read authoritative worker state;
- worker was still OFF during that re-read;
- content therefore turned itself OFF and removed the Yandex action;
- the old tests did not assert the final cross-layer state.

This was a ChatGPT product/test-design regression. Codex executed the supplied tests; the missing cross-layer assertion was not Codex's responsibility to invent.

Permanent mandatory gate supplement:

```text
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_MANUAL_ON_TRANSACTION_ADDENDUM_2026-08-19.md
```

It is mandatory together with `CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md`.

## Current repaired candidate — pending Codex full gate

Frozen target identity:

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

## QA transport status — direct binary route rejected, byte-safe fallback validated

The first direct-binary GitHub transport attempt is **INVALID and removed from `main`**. It produced a 14999-byte non-ZIP instead of the frozen 209505-byte target and caused Codex `FAIL_ARTIFACT`. It must never be used again.

Because the available GitHub connector path in this session was empirically unable to preserve the exact binary ZIP, living-gate section 3A.C fallback is now used: exact old accepted ZIP preimage + byte-verified text transport of the complete patch + full target-tree manifest + deterministic packer.

Validated QA transport branch:

```text
qa/e13a-reconstruction-transport
transport branch checkpoint: 3920b8c992a8f9393afddb6a0b36505162848ed1
```

Authority files on that branch:

```text
extension/tests/qa_transport/e13a/transport-manifest.json
extension/tests/qa_transport/e13a/patch.gz.b64.part00
extension/tests/qa_transport/e13a/patch.gz.b64.part01
extension/tests/qa_transport/e13a/target-tree-sha256.tsv
```

Round-trip verification already performed by ChatGPT before authorizing Codex:

```text
patch chunk 00 Git blob SHA-1: eecddec70dd896a324fb7fc2db64810cf404c66f
patch chunk 01 Git blob SHA-1: 8584db901f65be77cc3cd520692e4d222d049cd6
target tree manifest Git blob SHA-1: 16c626dae276def8870c0a40c0f64a276cd3df1a
transport manifest Git blob SHA-1: 2c9b7fdb20201447a8469e1363d2b08270f506ac
```

The downloaded/read-back text objects match the locally generated transport objects exactly. Locally, a **fresh reconstruction proof using those exact transported chunk bytes** was executed:

```text
concatenate chunks → base64 decode → gzip decompress
raw patch SHA-256: 709234433bd446f52a18c95785675d0f5ca3450b82459ce2631d36bdb7269bc2
fresh exact 31cc preimage extraction
`git apply --check`: PASS
patch apply: PASS
target source tree: 45/45 exact against target-tree-sha256.tsv
canonical deterministic rebuild: PASS
rebuilt ZIP bytes: 209505
rebuilt ZIP SHA-256: e13a26072039550792e740b8ed73e2bd56d48bdceb075a060406d2359e402a65
rebuilt ZIP byte-identical to locally frozen target: YES
ZIP integrity/open: PASS
```

Canonical packer is recorded in `transport-manifest.json`: Python stdlib `zipfile`; root directory then all directories lexicographically as ZIP_STORED entries; files lexicographically with ZIP_DEFLATED level 9; fixed timestamp `2025-12-31 19:00:00`; dirs 0755; files 0644; forward slashes; no EOL rewriting.

Codex must independently repeat every identity check. If the exact old preimage cannot be found by SHA, any transport object differs, target tree differs, or deterministic ZIP does not become exact `e13a2607… / 209505`, result is `FAIL_ARTIFACT`; Codex must not substitute a logically equivalent candidate.

## Development evidence before Codex

Corrected regression against old `31cc5f…` production bytes with repaired tests:

```text
focused old-product regression: 42/44 PASS, 2/44 FAIL
```

The two intended failures prove the corrected tests catch the old defect.

Repaired candidate development evidence:

```text
focused popup+content: 44/44 PASS
source suite: 361/361 PASS
packaged suite: 361/361 PASS
syntax: 40/40 PASS
JSON: 2/2 PASS
source↔package: 45/45 byte-identical
deterministic ZIP A/B: byte-identical
real Yandex requests: 0
```

These are development checks only, not a pre-delivery PASS.

## Authorized next stage

```text
AUTHORIZED_NEXT_STAGE = CODEX_COMPLETE_PRE_DELIVERY_FULL_GATE
```

Codex must first reconstruct and prove the **exact target bytes** through the validated fallback transport above. Only after exact `e13a2607… / 209505 / 45 files` identity is established may Codex execute the complete living `PD-00…PD-17` campaign from the beginning plus the mandatory Manual-ON transaction addendum.

The mandatory browser scenario starts from worker OFF + content OFF and turns Manual ON through the **real installed extension popup**, using actual popup→worker→content messaging. Independent popup mocks, direct `applyManualMode(true)`, pre-seeding Manual ON, or merely proving an already-armed external button are not substitutes.

No owner real-profile retest is allowed before a new complete Codex PASS. The owner remains prompt-only for Codex QA; no QA file transport or environment setup may be delegated to the owner.

Issues #1/#2 remain open. Do not start Search.
