# Phase 2 Stage 4 — refrozen exact candidate checkpoint

Date: 2026-08-24

Status: **REFROZEN / COMPLETE SOURCE+PACKAGE PREFLIGHT PASS / FINAL CODEX TRANSPORT PASS / CODEX FULL GATE PENDING**

## Exact source authority

```text
repo: MaksimUnimax/Yandex_direct
product branch lineage: candidate/phase2-search-reconstruction-2026-08-23
Stage-3 production closure: 75d18291224069a6ae67c110498481ec7320d3c0
Stage-4 refrozen source: 0ee1d38f8d28cfccceb5a07f9606fa715261bc27
```

The earlier source `1869d17...` and ZIP `0f0b035c...` are superseded because two QA test files inside the package payload were corrected after the first packaged-suite preflight. Runtime production bytes did not change; package test bytes did, so a new exact freeze was mandatory.

## Exact artifact

```text
filename: yandex-marketing-bridge-0.1.1-phase2-search-reconstruction-candidate.zip
SHA-256: d58b5bd20921e9492a90b687ae3910c7049ddff17741da44ba832369eb1c0f16
bytes: 170734
files: 65
ZIP entries: 68
ZIP integrity: PASS
```

## Exact manifest

```text
EXACT_CANDIDATE_MANIFEST_2026-08-24.json
SHA-256: 0edfcecdfb1025e7292d2d81f36b8fb6e5edb6f3332ef884d7f31e604ebdf7de
bytes: 11421
source_commit: 0ee1d38f8d28cfccceb5a07f9606fa715261bc27
format: YMB_PHASE2_EXACT_CANDIDATE_V1
```

The manifest fixes all 65 package paths, byte counts and SHA-256 values.

## Complete refreeze preflight

```text
workflow: phase2-stage4-freeze
run: 32714268931
job: 97392079851
conclusion: SUCCESS
permissions: contents read
```

Results:

```text
complete source suite: 231/231 PASS
fail: 0
skipped: 0
cancelled: 0

deterministic build A/B: identical
EXACT_ARTIFACT_IDENTITY_PASS
SOURCE_PACKAGE_IDENTITY_PASS
ZIP integrity: PASS

complete packaged suite through governed adapter: 231/231 PASS
PACKAGED_SYNTAX_PASS count=59
PACKAGED_JSON_PASS count=2
PACKAGE_EXACT_IDENTITY_PASS
PACKAGED_SUITE_LAYOUT_IDENTITY_PASS
PACKAGED_SUITE_PASS files=38
PACKAGED_PREDELIVERY_PREFLIGHT_PASS

real Yandex requests: 0
```

Governed packaged-suite adapter:

```text
extension/tests/qa_transport/phase2-candidate/run_packaged_suite.py
extension/tests/PHASE_2_STAGE_4_PACKAGED_SUITE_ADAPTER_2026-08-24.md
```

## Actions transport round-trip

```text
artifact: phase2-stage4-frozen-candidate-0ee1d38
artifact ID: 9515289771
wrapper SHA-256: 9936e229e8f080d2a24a06892d4ca231a9f625e1ecc267fba57662b446c45e55
wrapper bytes: 182585
```

Fresh consumer independently verified:

```text
inner ZIP SHA-256 = d58b5bd20921e9492a90b687ae3910c7049ddff17741da44ba832369eb1c0f16
inner bytes = 170734
manifest SHA-256 = 0edfcecdfb1025e7292d2d81f36b8fb6e5edb6f3332ef884d7f31e604ebdf7de
manifest bytes = 11421
ZIP integrity = PASS
65/65 payload rows = PASS
```

## Final Codex-accessible transport

```text
branch: qa/phase2-stage4-final-b64-transport-0ee1d38-2026-08-24
commit: 9dedf7bf624174996fae7efa7a4bdbff6904d348
path: extension/tests/qa_transport/phase2-stage4-final-b64/
format: YMB_PHASE2_STAGE4_FINAL_EXACT_B64_TRANSPORT_V1
chunks: 16
chunk bytes: 14228 each
base64 length: 227648
```

Fresh-consumer proof:

```text
QA PR: #9 — closed without merge
run: 32715052351
job: 97394394286
permission: Contents read

B64_REASSEMBLY_PASS
EXACT_ZIP_IDENTITY_PASS
ROUNDTRIP_PAYLOAD_MANIFEST_PASS
ROUNDTRIP_ZIP_INTEGRITY_PASS
FROZEN_AUTHORITY_MATCH_PASS
FINAL_FROZEN_AUTHORITY_MATCH_PASS
REAL_YANDEX_REQUESTS=0
```

Temporary publisher/verifier workflows were removed after evidence was captured.

## Gate status

```text
EXACT_REFROZEN_CANDIDATE = PASS
COMPLETE_SOURCE_PREFLIGHT = PASS
DETERMINISTIC_REBUILD = PASS
SOURCE_PACKAGE_IDENTITY = PASS
COMPLETE_PACKAGED_PREFLIGHT = PASS
ACTIONS_ARTIFACT_ROUNDTRIP = PASS
CODEX_ACCESSIBLE_TRANSPORT_CONSUMER_PROOF = PASS
CODEX_EXECUTION_MAP = PASS
CODEX_COMPLETE_PD00_PD17_PLUS_ADDENDA = PENDING
OWNER_LIVE_SEARCH = BLOCKED
```

Current next authorized action is one complete Codex campaign against the exact artifact above. Any production or package-test byte change invalidates this checkpoint and requires a new freeze. QA/reporting/harness fixes must not mutate frozen payload bytes.
