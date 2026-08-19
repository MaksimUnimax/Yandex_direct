# CURRENT STATE — Yandex Marketing Bridge

Status: **CURRENT CONTROL-PLANE AUTHORITY**  
Updated: 2026-08-19

This file applies immediately in the current conversation and every new/resumed conversation. Live GitHub remains authoritative; always fetch current `main` HEAD before action.

## Repository

```text
repo: MaksimUnimax/Yandex_direct
branch: main
```

## Mandatory QA transport runbook

Before preparing any future Codex pre-delivery prompt, ChatGPT must read and execute:

```text
extension/docs/CODEX_QA_ARTIFACT_TRANSPORT_AND_GATE_RUNBOOK.md
```

This runbook contains the concrete proven sequence that actually carried the repaired 0.1.1 candidate through exact artifact reconstruction and a complete Codex PASS. It is mandatory in addition to the abstract workflow/gate rules.

In particular, future QA preparation must not stop at “do not do X”. It must follow the positive preparation sequence recorded there:

```text
freeze exact target
→ reuse the proven transport pattern
→ verify exact preimage/input identity
→ publish byte-safe transport components
→ read those components back from the Codex-accessible GitHub path
→ verify component hashes
→ fresh reconstruct source
→ git apply --check PASS
→ verify complete postimage tree 45/45 (or the current candidate's full manifest)
→ read back and execute the published canonical byte-complete packer unchanged
→ require exact frozen artifact SHA + bytes + ZIP integrity + file/entry identity
→ complete fresh consumer-conformance PASS
→ only then authorize/give Codex prompt
→ Codex independently repeats artifact identity phase
→ only then PD-00..PD-17/product QA
```

A new or resumed conversation must not reconstruct this procedure from memory or invent a new transport while the proven runbook remains applicable.

## Previous owner-live product failure

The previous artifact:

```text
yandex-marketing-bridge-0.1.1-phase1-external-ui-manual-delivery-candidate.zip
SHA-256 31cc5f3f8a8fe0df9450bb9abd005996ddf7d842df0b18c7bafd0631ed6a4e14
bytes 209697
files 45
```

had a complete controlled Codex PASS but then failed owner real-profile acceptance because Manual ON could self-revert OFF and remove the external `Яндекс` action.

Classification:

```text
31cc5f... owner-live: FAIL_PRODUCT
that artifact is retired from owner handoff
```

## Current repaired exact candidate

```text
yandex-marketing-bridge-0.1.1-phase1-manual-enable-order-fix-candidate.zip
SHA-256 e13a26072039550792e740b8ed73e2bd56d48bdceb075a060406d2359e402a65
bytes 209505
files 45
ZIP entries including dirs 48
version 0.1.1
```

Production hashes:

```text
content_script.js
ddf9ed51c60ab90dcdeb1fcd5a1b955c3dd88dfc53a0ddfd5842d66ebe9a02cc

popup.js
ac87ad973e8b673bf0c235a43b3dc29dfb67865594ea62e085f943660f0a7ab2

service_worker.js
2ae878ed4a5f89e07056dd228344b3c3ab0086f5f8d6d1e026431a9e23bd3e3b
```

Repair invariant:

```text
popup Manual ON commits authoritative worker ON before applying content ON
content refuses successful ON when worker is not actually ON
failed content apply rolls worker back OFF
ordinary content resync cannot self-revert a successful Manual ON transaction
```

Mandatory regression supplement:

```text
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_MANUAL_ON_TRANSACTION_ADDENDUM_2026-08-19.md
```

## Artifact/transport failure history retained for governance

Two earlier `e13a…` QA attempts failed in the artifact/process layer before product QA:

1. invalid GitHub binary object: `37d896…`, 14999 bytes, not a ZIP;
2. underspecified prose packer: exact 45/45 source but reconstructed ZIP SHA `8359c6…` instead of `e13a…`.

Neither attempt changed production bytes or produced product-test evidence. Permanent prevention rules are recorded in `WORKFLOW_OPERATING_RULES.md`, the living full gate, and the mandatory QA transport runbook.

## Exact executable reconstruction authority used by the successful campaign

Codex used:

```text
qa transport branch: qa/e13a-exact-reconstruction-v3
exact preimage SHA-256: 31cc5f3f8a8fe0df9450bb9abd005996ddf7d842df0b18c7bafd0631ed6a4e14
raw patch SHA-256: 709234433bd446f52a18c95785675d0f5ca3450b82459ce2631d36bdb7269bc2
canonical executable packer: extension/tests/qa_transport/e13a/canonical_packer_exact.py
```

The executable packer fixes complete byte-affecting ZIP metadata, including UNIX file-type bits and `external_attr`, and reproduces exact artifact `e13a2607… / 209505`.

The positive step-by-step preparation and consumer-conformance sequence for this successful path is preserved in:

```text
extension/docs/CODEX_QA_ARTIFACT_TRANSPORT_AND_GATE_RUNBOOK.md
```

## Latest complete Codex pre-delivery full gate — PASS

Authority at gate start:

```text
live main HEAD: 7bab312c84877627c3f264ff99c3fe5b4546a5b2
qa transport branch: qa/e13a-exact-reconstruction-v3
```

Exact artifact independently reconstructed and tested by Codex:

```text
SHA-256 e13a26072039550792e740b8ed73e2bd56d48bdceb075a060406d2359e402a65
bytes 209505
files 45
ZIP entries 48
ZIP integrity PASS
target tree identity PASS
canonical packer modified NO
```

Complete result:

```text
PD-00..PD-17: ALL PASS
Manual-ON transaction regression: PASS
real installed extension popup used: PASS
worker ON committed before content apply: PASS
content final Manual ON: PASS
popup final Manual ON: PASS
Yandex action present/enabled after apply: PASS
Yandex action present after ordinary resync: PASS
popup reopen Manual ON: PASS
OFF transition: PASS
second ON transition: PASS
ON→OFF self-revert observed: NO
source suite: 361/361 PASS
packaged suite: 361/361 PASS
syntax: 40/40 PASS
JSON: 2/2 PASS
source/package identity: PASS
real Yandex requests: 0
production modified during gate: 0
tests modified during gate: 0
failures: NONE
verdict: PASS
```

Codex evidence paths:

```text
D:\codex\Yandex\qa-evidence-ymb-full-gate-20260819-06\CODEX_YANDEX_PRE_DELIVERY_FULL_REGRESSION_GATE_2026-08-19.md
D:\codex\Yandex\qa-evidence-ymb-full-gate-20260819-06\CODEX_YANDEX_PRE_DELIVERY_FULL_REGRESSION_GATE_2026-08-19.json
D:\codex\Yandex\qa-evidence-ymb-full-gate-20260819-06\yandex-marketing-bridge-0.1.1-phase1-manual-enable-order-fix-candidate.zip
```

This controlled PASS authorizes handoff of **this exact `e13a…` artifact only**. It does not fabricate owner real-profile/live PASS.

## Current control-plane reconstruction

```text
PRODUCT_SOURCE = repaired e13a target source; production hashes above
HANDOFF_ARTIFACT = e13a26072039550792e740b8ed73e2bd56d48bdceb075a060406d2359e402a65 / 209505 / 45 files / full Codex PASS
LATEST_FULL_GATE = PASS on exact e13a artifact; PD-00..PD-17 ALL PASS; Manual-ON addendum PASS
PRODUCTION_BYTES_CHANGED_SINCE_GATE = NO
OWNER_LIVE = PENDING on e13a
OPEN_BLOCKERS = owner real-profile Yandex functional acceptance; issues #1/#2 remain open until owner-live PASS
AUTHORIZED_NEXT_STAGE = OWNER_REAL_PROFILE_YANDEX_FUNCTIONAL_ACCEPTANCE
```

## Authorized next stage

```text
AUTHORIZED_NEXT_STAGE = OWNER_REAL_PROFILE_YANDEX_FUNCTIONAL_ACCEPTANCE
```

Owner-live policy for the current campaign:

- use only exact artifact SHA `e13a2607…`;
- only functional tests involving Yandex are required; standalone UI test cases are not required;
- give exactly one test at a time;
- UI behavior is observed naturally while functional tests execute;
- start with the free real `getRegionsTree` path, then advance through paid Wordstat operations one at a time;
- freshly verify official Yandex pricing immediately before every executable paid request;
- no blind retry;
- keep issues #1/#2 open and Search/Phase 2 blocked until owner-live functional acceptance passes.
