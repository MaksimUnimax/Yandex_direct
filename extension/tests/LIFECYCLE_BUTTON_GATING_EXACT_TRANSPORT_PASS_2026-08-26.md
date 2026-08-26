# Lifecycle button gating — exact B64 transport PASS

Date: 2026-08-26  
Status: **PASS — exact artifact transport round-trip proven; independent Codex gate may start**

## Authority

```text
LIVE_MAIN_HEAD_BEFORE_WRITE = 5c7c4378c1bd44327093f80f3c517ad27eacaafa
CANDIDATE_SOURCE = 939e880f820e52beae9dcbcedc86d5cd9e13b075
FROZEN_ARTIFACT = yandex-marketing-bridge-0.1.1-lifecycle-button-gating-candidate.zip
FROZEN_SHA256 = 0430463ea979c31c5e74a48c899f2ce0fb141b62c4baf132df153380fbc0a262
FROZEN_BYTES = 179877
FROZEN_FILES = 69
FROZEN_ENTRIES = 72
```

Freeze authority:

```text
extension/tests/LIFECYCLE_BUTTON_GATING_FREEZE_2026-08-26.md
```

## Published transport

```text
branch = qa/lifecycle-button-gating-exact-transport-2026-08-26
transport commit = e11b4f9d5dfb9f5b1bd01bd885151aefdcddc797
transport directory = extension/tests/qa_transport/lifecycle-button-gating
```

Published authority files:

```text
canonical_packer_exact.py
SHA-256 = 09c927ee97eb89714c7e1f3d96f23141f67940dc74d9a8a601608e526f557345

target-tree-sha256.tsv
SHA-256 = 8c2bfc969888d63ba75c29990c8f99cb28da14b57b07bc9a58239e2ec2e67296
files described = 69

transport_manifest.json
artifact.zip.b64.part00 ... artifact.zip.b64.part68
```

The exact executable packer was locally consumer-tested before publication and reproduced the frozen artifact byte-for-byte.

## Text-safe artifact encoding

`transport_manifest.json` records:

```text
format = YMB_EXACT_ZIP_B64_TRANSPORT_V1
candidate_source = 939e880f820e52beae9dcbcedc86d5cd9e13b075
chunk_chars = 3500
chunk_count = 69
base64_chars = 239836
base64_sha256 = a226f87c626659ba16b9f992fc526019c3d3d98702d5655659846b5a8f74e359
artifact_sha256 = 0430463ea979c31c5e74a48c899f2ce0fb141b62c4baf132df153380fbc0a262
artifact_bytes = 179877
artifact_files = 69
artifact_entries = 72
```

Parts `00..67` contain exactly 3500 ASCII base64 characters each; `part68` contains 1836 characters. The manifest contains the per-part SHA-256 values and is the authoritative chunk list/order.

## ChatGPT transport builder / fresh-consumer proof

GitHub Actions transport run:

```text
run id = 32919877249
job id = 98031197439
result = SUCCESS
```

This run is a transport/preflight proof, **not independent Codex product QA evidence**.

The run performed:

```text
published packer + published 69-file target manifest
-> exact candidate source 939e880...
-> build ZIP
-> require 0430463e... / 179877 / 69 / 72 / ZIP PASS
-> base64 encode exact ZIP
-> split to 69 text chunks
-> publish chunks + transport manifest to GitHub QA branch
-> fresh clone the published QA branch from GitHub
-> verify every chunk chars + SHA against transport_manifest.json
-> concatenate in manifest order
-> verify base64 chars + SHA
-> strict base64 decode
-> verify ZIP SHA + bytes
-> verify ZIP opens / 69 files / 72 entries
-> byte-compare reassembled ZIP with exact built frozen target
```

Observed fresh-consumer result:

```text
FRESH_CONSUMER_EXACT_B64_ROUNDTRIP_PASS
chunk_count = 69
base64_chars = 239836
base64_sha256 = a226f87c626659ba16b9f992fc526019c3d3d98702d5655659846b5a8f74e359
artifact_sha256 = 0430463ea979c31c5e74a48c899f2ce0fb141b62c4baf132df153380fbc0a262
artifact_bytes = 179877
BYTE_IDENTICAL_TO_BUILT_FROZEN_TARGET_PASS
```

Therefore the mandatory pre-Codex round-trip requirement is satisfied.

## Authorization

```text
ARTIFACT_TRANSPORT = PASS
FAIL_ARTIFACT = NO
AUTHORIZED_NEXT_STAGE = INDEPENDENT_CODEX_COMPLETE_PRE_DELIVERY_FULL_GATE
OWNER_HANDOFF_AUTHORIZED = NO
OWNER_LIVE_AUTHORIZED = NO
```

Codex must independently fetch the exact transport commit, verify/reassemble the artifact again, and only after exact artifact identity PASS execute the complete living applicable product gate with zero real credentials and zero real Yandex requests.
