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

has now **FAILED owner real-profile acceptance** before Yandex functional testing could start.

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
- latest content `WS_APPLY_MANUAL_MODE(true)` now immediately re-reads authoritative worker state;
- worker was still OFF during that re-read;
- content therefore turned itself OFF and removed the Yandex action;
- the handler still returned an acknowledgement that the old tests treated as success.

This was a ChatGPT product/test-design regression. Codex executed the supplied tests; the missing cross-layer assertion was not Codex's responsibility to invent.

Permanent mandatory gate supplement:

```text
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_MANUAL_ON_TRANSACTION_ADDENDUM_2026-08-19.md
```

It is mandatory together with `CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md` until merged into that living gate.

## Current repaired candidate — pending Codex full gate

New exact frozen candidate:

```text
yandex-marketing-bridge-0.1.1-phase1-manual-enable-order-fix-candidate.zip
SHA-256 e13a26072039550792e740b8ed73e2bd56d48bdceb075a060406d2359e402a65
bytes 209505
files 45
```

QA transport path in this repository:

```text
extension/tests/qa_artifacts/yandex-marketing-bridge-0.1.1-phase1-manual-enable-order-fix-candidate.zip
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

`service_worker.js` remains byte-identical to the previous candidate:

```text
2ae878ed4a5f89e07056dd228344b3c3ab0086f5f8d6d1e026431a9e23bd3e3b
```

## Development evidence before Codex

The corrected regression was first run against the old `31cc5f…` production bytes with only the repaired tests substituted. Result:

```text
focused old-product regression: 42/44 PASS, 2/44 FAIL
```

The two failures are the intended proof that the new tests catch the old defect:

1. content must not report successful Manual ON while worker gate is still OFF;
2. popup Manual ON must preserve final worker/content ON rather than use the obsolete content-first ordering.

Repaired candidate local evidence:

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

Codex must test the exact `e13a2607…` ZIP from repository QA transport, verify SHA/size before extraction, then execute the entire living `PD-00…PD-17` campaign from the beginning plus the mandatory Manual-ON transaction addendum.

The new mandatory browser scenario must start from worker OFF + content OFF and turn Manual ON through the **real extension popup**, using actual popup→worker→content messaging. Independent popup mocks, direct `applyManualMode(true)`, pre-seeding Manual ON, or merely proving the external button after it is already armed are not substitutes.

No owner real-profile retest is allowed before a new complete Codex PASS. The owner remains prompt-only for Codex QA; no QA file transport or environment setup may be delegated to the owner.

Issues #1/#2 remain open. Do not start Search.
