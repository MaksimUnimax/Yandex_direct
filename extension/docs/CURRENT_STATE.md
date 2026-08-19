# CURRENT STATE — Yandex Marketing Bridge

Status: **CURRENT CONTROL-PLANE AUTHORITY**
Updated: 2026-08-19

This file is intentionally compact. It exists so the current conversation and every new/resumed conversation can reconstruct the exact workflow state without relying on chat memory or stale historical sections in other documents.

## Live repository state

Repository: `MaksimUnimax/Yandex_direct`
Branch: `main`

The live HEAD must always be fetched before action. Do not trust a copied SHA in this file if live GitHub differs.

## Current product candidate

Version: `0.1.1`
Exact frozen source used by the latest complete Codex gate:

```text
D:\codex\Yandex\work\ymb-full-gate-20260819-02\source
```

Critical frozen production hashes:

```text
content_script.js 6358418ff04de37a21368a28046c1109280a7a6b8d942972a319d4dc09dabd9e
service_worker.js 2ae878ed4a5f89e07056dd228344b3c3ab0086f5f8d6d1e026431a9e23bd3e3b
```

Exact handoff/tested artifact:

```text
yandex-marketing-bridge-0.1.1-phase1-external-ui-manual-delivery-candidate.zip
SHA-256 31cc5f3f8a8fe0df9450bb9abd005996ddf7d842df0b18c7bafd0631ed6a4e14
bytes 209697
files 45
```

## Latest complete full regression gate

Codex result date: 2026-08-19
Candidate authority used by that gate:

```text
07e0140d0a01a327d639e23bea8446a79818ceac
```

Result:

```text
PD-00..PD-17: ALL PASS
source suite: 361/361 PASS
packaged suite: 361/361 PASS
syntax: 40/40 PASS
JSON: 2/2 PASS
source/package identity: 45/45 PASS
real Yandex requests: 0
production modified during gate: NO
verdict: PASS
```

## Post-gate documentation changes

After the full product gate PASS, documentation/governance was changed to record permanent QA/process lessons and workflow operating rules.

These changes are **documentation/process changes only** unless a changed document also changes a product contract or acceptance assertion. The current conversation must classify each such change before handoff rather than assuming automatically that the product PASS is either valid or invalid.

The current documentation cleanup includes:

- hardening `CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md` with QA transport/harness failure-prevention rules;
- adding `WORKFLOW_OPERATING_RULES.md`;
- strengthening `README.md` authority/workflow reconstruction rules;
- reconciling stale Manual lifecycle wording in `SPECIFICATION.md`;
- updating this `CURRENT_STATE.md`.

After this cleanup is complete, reconstruct live HEAD and classify whether any acceptance assertion changed relative to the passed gate. If only process/governance wording changed and product/gate assertions for the exact candidate remain unchanged, the exact product PASS can remain applicable. If acceptance assertions changed, rerun the required gate evidence before handoff.

## Owner live status

```text
Owner real-profile acceptance: PENDING
Issue #1: OPEN pending owner live acceptance
Issue #2: OPEN pending owner live acceptance
Phase 1 LIVE PASS: FALSE until owner acceptance
Search/Phase 2: BLOCKED until Phase 1 live PASS
```

## Authorized next stage

Current authorized work is **documentation/governance reconciliation only** until all current canonical documents agree.

After reconciliation:

1. fetch live HEAD;
2. verify no production bytes changed;
3. classify documentation changes under `WORKFLOW_OPERATING_RULES.md`;
4. if no acceptance assertion changed, preserve the exact full-gate PASS for artifact `31cc5f...` and proceed to owner real-profile acceptance;
5. if an acceptance assertion changed, run the required refreshed Codex gate before owner handoff.

Do not start Search. Do not close issues #1/#2 before owner real-profile PASS.
