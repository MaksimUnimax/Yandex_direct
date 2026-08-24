# Phase 2 Stage 4 — exact frozen candidate checkpoint

Date: 2026-08-24

Status: **FROZEN / CONSUMER-CONFORMANCE PASS / CODEX FULL GATE PENDING**

## Frozen source authority

```text
repo: MaksimUnimax/Yandex_direct
branch lineage: candidate/phase2-search-reconstruction-2026-08-23
Stage-3 production closure: 75d18291224069a6ae67c110498481ec7320d3c0
Stage-4 frozen source commit: 1869d17f3cb64417a07088de18dafa5687c83840
Stage-4 packer blob at frozen source: 5de1631d45f3cc1fd76d59e4af05c43a25e37129
```

The later commit `328c823ff4376502035c0e1679dc8c3c7ad7b293` synchronizes only `.github/workflows/phase2-candidate-gate.yml` with `main`; it is not part of the frozen package source. The package builder is pinned to `1869d17...`.

## Exact handoff artifact

```text
filename: yandex-marketing-bridge-0.1.1-phase2-search-reconstruction-candidate.zip
root: yandex-marketing-bridge-0.1.1-phase2-search-reconstruction-candidate/
SHA-256: 0f0b035c6bc04da841d549182c3dcea6e7cf10074eddebafdf1c3a4c21c98411
bytes: 170726
files: 65
ZIP entries: 68
ZIP integrity: PASS
```

The package contains the established Phase-2 payload layout: every file under `extension/src/**` plus root-level `extension/tests/*.test.mjs`. Repository docs, evidence directories and `.github/**` are not package payload.

## Generated manifest authority

The freeze job generated `EXACT_CANDIDATE_MANIFEST_2026-08-24.json` containing the full 65-file path/byte/SHA-256 payload manifest.

```text
manifest bytes: 11421
manifest SHA-256: 1acda380ef8fee4aca255014cdacf48a50059037113ff121bd86c738e4fceea9
format: YMB_PHASE2_EXACT_CANDIDATE_V1
source_commit: 1869d17f3cb64417a07088de18dafa5687c83840
```

## Deterministic freeze evidence

Dedicated Stage-4 workflow:

```text
workflow: phase2-stage4-freeze
run: 32705402373
job: 97365293002
conclusion: SUCCESS
GITHUB_TOKEN: contents: read
```

The job:

1. checked out exact commit `1869d17...`;
2. asserted clean source identity;
3. built the candidate and verified fresh extraction identity;
4. rebuilt independently from the same frozen source;
5. verified the generated manifest;
6. verified the second extraction identity;
7. required byte-for-byte `cmp` between both ZIPs;
8. uploaded the exact candidate + manifest.

Both builds returned:

```text
SHA-256: 0f0b035c6bc04da841d549182c3dcea6e7cf10074eddebafdf1c3a4c21c98411
bytes: 170726
files: 65
entries: 68
zip_test: PASS
SOURCE_PACKAGE_IDENTITY_PASS
STAGE4_FREEZE_CONSUMER_CONFORMANCE_PASS
```

## Actions transport evidence

```text
artifact name: phase2-stage4-frozen-candidate-1869d17
artifact ID: 9512033721
wrapper bytes: 182577
wrapper SHA-256/digest: b5ba907514c2a417c537fcce82ddfe5ca6605df6fb71ea309942700605fb4e33
retention: 30 days from 2026-08-24
```

A fresh consumer downloaded artifact ID `9512033721` through the GitHub connector. The downloaded wrapper SHA-256 was independently recalculated as exactly `b5ba9075...`.

The wrapper contained exactly:

```text
yandex-marketing-bridge-0.1.1-phase2-search-reconstruction-candidate.zip  170726 bytes
EXACT_CANDIDATE_MANIFEST_2026-08-24.json                                  11421 bytes
```

Fresh consumer verification of the downloaded inner ZIP:

```text
inner SHA-256 = 0f0b035c6bc04da841d549182c3dcea6e7cf10074eddebafdf1c3a4c21c98411
inner bytes = 170726
files = 65
entries = 68
ZIP integrity = PASS
all 65 file paths/bytes/SHA-256 match the downloaded full manifest = PASS
ROUNDTRIP_PAYLOAD_MANIFEST_PASS
ROUNDTRIP_ZIP_INTEGRITY_PASS
```

Therefore transport upload success is not being used as proof by itself; the published artifact was actually consumed back and verified independently.

## Current focused regression sanity check

Combined read-only PR workflow after CI-only synchronization:

```text
workflow: phase2-focused-development
run: 32705402326
focused job: 97365292925
freeze job: 97365292591
focused tests: 77/77 PASS
fail: 0
service_worker.js syntax: PASS
popup.js syntax: PASS
freeze job: SUCCESS
```

This is not the Stage-4 complete Codex full gate. It is only a sanity check that the frozen-stage CI work did not regress the already closed Stage-3 focused set.

## Safety / paid-provider status

```text
real Yandex requests during freeze: 0
owner-live Search: NOT STARTED
blind retry: NOT PERMITTED
```

## Stage-4 execution pointer

```text
EXACT_FROZEN_CANDIDATE = PASS
DETERMINISTIC_REBUILD = PASS
SOURCE_PACKAGE_IDENTITY = PASS
ACTIONS_TRANSPORT_ROUNDTRIP = PASS
CODEX_COMPLETE_PRE_DELIVERY_FULL_GATE = PENDING
OWNER_LIVE_SEARCH = BLOCKED UNTIL CODEX PASS
```

The next authorized action is one complete Codex pre-delivery campaign against the exact frozen artifact above. A product-byte change invalidates this frozen identity and requires a new freeze. QA/transport/documentation fixes must not mutate the frozen production payload.
