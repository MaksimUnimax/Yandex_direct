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

Root cause:

- popup committed content ON first, worker ON second;
- content `WS_APPLY_MANUAL_MODE(true)` re-read authoritative worker state;
- worker was still OFF during that re-read;
- content therefore turned itself OFF and removed the Yandex action;
- previous tests did not assert final cross-layer transaction state.

Mandatory regression supplement:

```text
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_MANUAL_ON_TRANSACTION_ADDENDUM_2026-08-19.md
```

Current frozen repaired target:

```text
yandex-marketing-bridge-0.1.1-phase1-manual-enable-order-fix-candidate.zip
SHA-256 e13a26072039550792e740b8ed73e2bd56d48bdceb075a060406d2359e402a65
bytes 209505
files 45
ZIP entries including dirs 48
```

Production bytes changed from `31cc5f…` only in:

```text
content_script.js
  old 6358418ff04de37a21368a28046c1109280a7a6b8d942972a319d4dc09dabd9e
  new ddf9ed51c60ab90dcdeb1fcd5a1b955c3dd88dfc53a0ddfd5842d66ebe9a02cc

popup.js
  old 7286ea024033293110ad10ebc16856de0beacf512f6f86a229ac0271ac20c28c
  new ac87ad973e8b673bf0c235a43b3dc29dfb67865594ea62e085f943660f0a7ab2

service_worker.js
  unchanged 2ae878ed4a5f89e07056dd228344b3c3ab0086f5f8d6d1e026431a9e23bd3e3b
```

Development evidence only:

```text
old 31cc product + repaired tests: 42/44 PASS, 2/44 intended FAIL
repaired focused popup+content: 44/44 PASS
source suite: 361/361 PASS
packaged suite: 361/361 PASS
syntax: 40/40 PASS
JSON: 2/2 PASS
source↔package: 45/45 byte-identical
local deterministic ZIP A/B: byte-identical
real Yandex requests: 0
```

## Artifact transport failure history

### FAIL_ARTIFACT #1 — invalid direct binary object

Expected `e13a… / 209505`; Codex received:

```text
SHA-256 37d896fb8c1542509abfb33780fee6ca802b0d76238b39d76ec78c309b22cf6d
bytes 14999
not a ZIP
```

Product campaign was NOT RUN. Production bytes were not changed.

### FAIL_ARTIFACT #2 — underspecified packer prose

Codex independently obtained exact 31cc preimage, exact patch inputs and exact 45/45 target tree, but the old prose packaging contract omitted UNIX file-type metadata in ZIP `external_attr`.

Codex therefore produced:

```text
SHA-256 8359c6cf46ed9ca107675d56aec0d37b9615a009fa007b7f68abcddba3a96400
bytes 209505
```

instead of required `e13a…`.

The former label `validated reconstruction transport` is revoked. Product campaign was NOT RUN. Production bytes were not changed.

## Current QA transport — byte-complete executable reconstruction fallback

Direct binary GitHub transport through the available connector was empirically invalid. The connector exposes text/blob APIs but no machine-safe local-file/raw-binary upload path. A manual giant-base64 copy through model/tool arguments is not an acceptable machine-driven transport and was rejected before Codex execution.

Therefore the governed reconstruction fallback is used. It mirrors the class of deterministic exact-package reproduction that reached execution in the successful 31cc campaign, but removes the prior underspecified prose packer.

Exact old accepted preimage already proven available in Codex:

```text
D:\codex\Yandex\qa-evidence-ymb-full-gate-20260819-04\yandex-marketing-bridge-0.1.1-phase1-external-ui-manual-delivery-candidate.zip
SHA-256 31cc5f3f8a8fe0df9450bb9abd005996ddf7d842df0b18c7bafd0631ed6a4e14
bytes 209697
files 45
```

Exact patch transport remains on:

```text
branch: qa/e13a-reconstruction-transport
checkpoint: 3920b8c992a8f9393afddb6a0b36505162848ed1
extension/tests/qa_transport/e13a/transport-manifest.json
extension/tests/qa_transport/e13a/patch.gz.b64.part00
extension/tests/qa_transport/e13a/patch.gz.b64.part01
extension/tests/qa_transport/e13a/target-tree-sha256.tsv
```

Those patch inputs already independently produced the exact 45/45 target source tree in Codex. The only second-attempt failure was package metadata.

The byte-complete executable packer authority is now published separately on a clean QA branch:

```text
branch: qa/e13a-exact-packer-transport
checkpoint: 466aaa16cef9e491cd6ece1cdc18a3be4f65e121
packer: extension/tests/qa_transport/e13a-exact/e13a_exact_packer.py
packer Git blob SHA-1: af5a6b1ad6f0621951d53867094ba0b53b2135c4
packer SHA-256: 3507522d03735c446411fb6b83db767dd1c83188315e8f576e03e7763c976cb7
manifest: extension/tests/qa_transport/e13a-exact/target-tree-sha256.tsv
manifest Git blob SHA-1: 16c626dae276def8870c0a40c0f64a276cd3df1a
manifest SHA-256: 7c7234e184403de6a02e843b92bfd5f2fa12ed2391c054f4fa221d690f5b44b7
manifest files: 45
```

The executable packer fixes the actual byte-affecting ZIP metadata, including:

```text
create_system = 3
create_version = 20
extract_version = 20
flag_bits = 0
internal_attr = 0
extra = empty
comments = empty
directory external_attr = ((S_IFDIR | 0755) << 16) | 0x10
regular-file external_attr = ((S_IFREG | 0644) << 16)
directories = root/shared/tests, ZIP_STORED
files = lexicographic, ZIP_DEFLATED level 9
fixed timestamp = 2025-12-31 19:00:00
forward-slash paths
```

### Pre-prompt independent consumer-conformance proof

Before authorizing Codex, ChatGPT performed a fresh consumer proof using the published byte-identical packer/manifest inputs and the governed frozen source identity. Result:

```text
published packer Git blob identity: PASS
published manifest Git blob identity: PASS
source identity against manifest: 45/45 PASS
output SHA-256: e13a26072039550792e740b8ed73e2bd56d48bdceb075a060406d2359e402a65
output bytes: 209505
files: 45
ZIP entries: 48
ZIP test/integrity: PASS
output byte-identical to locally frozen e13a target: YES
consumer process exit: 0
```

The failed GitHub Actions experiment is not an authorized transport: live `main` contains scaffold under `extension/src`, not the frozen candidate source tree that lives in the governed Codex workspace. The workflow failed closed before artifact publication and is not used for the gate.

## Current control-plane reconstruction

```text
PRODUCT_SOURCE = repaired e13a target source; production hashes above
HANDOFF_ARTIFACT = target e13a26072039550792e740b8ed73e2bd56d48bdceb075a060406d2359e402a65 / 209505 / 45 files
LATEST_FULL_GATE = no valid full PASS for e13a; two historical FAIL_ARTIFACT attempts before product QA
PRODUCTION_BYTES_CHANGED_SINCE_LATEST_ATTEMPT = NO
OWNER_LIVE = previous 31cc FAIL; e13a owner-live PENDING and blocked until Codex PASS
OPEN_BLOCKERS = full Codex PD-00..PD-17 + Manual-ON addendum pending; issues #1/#2 open
AUTHORIZED_NEXT_STAGE = CODEX_COMPLETE_PRE_DELIVERY_FULL_GATE
```

## Authorized next stage

```text
AUTHORIZED_NEXT_STAGE = CODEX_COMPLETE_PRE_DELIVERY_FULL_GATE
```

Codex must:

1. independently verify the exact 31cc preimage;
2. independently verify/read the exact patch transport inputs at checkpoint `3920b8c…`;
3. reconstruct the exact 45/45 target source in a fresh directory with no EOL rewriting;
4. independently verify the executable packer and manifest at checkpoint `466aaa16…`;
5. execute that packer, not a prose reimplementation;
6. require exact `e13a2607… / 209505 / 45 files / 48 entries / ZIP integrity PASS` before any product PASS credit;
7. use that exact output ZIP as primary package under test;
8. run the complete living `PD-00…PD-17` campaign from the beginning plus the mandatory Manual-ON transaction addendum and real installed-extension popup browser scenario;
9. make zero real Yandex requests and use no real credentials;
10. never modify product or tests during QA.

If the exact package identity is not produced, verdict remains `FAIL_ARTIFACT`; no logically equivalent substitute is allowed.

No owner real-profile retest is allowed before a complete Codex PASS. The owner remains prompt-only for Codex QA. Issues #1/#2 remain open. Search remains blocked.
