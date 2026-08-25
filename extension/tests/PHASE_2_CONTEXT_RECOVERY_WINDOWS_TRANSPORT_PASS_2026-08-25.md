# Phase 2 Context-Recovery Windows-Safe Exact Transport — PASS

Date: 2026-08-25

This checkpoint records Windows-safe byte transport of the exact frozen Phase-2 context-recovery candidate. It is QA/control-plane evidence only and does not change candidate product/package-test bytes.

## Frozen authority

```text
product source: f4aee34c0a3455aa7199f6aa54bd581c71d97337
candidate ZIP SHA-256: 739dd5d7cbefa98568bf51ae0ecab556360db534954fa0e27878ca5a77e7ae46
candidate bytes: 175971
files: 68
ZIP entries: 71
payload manifest SHA-256: bbe8b2665c3339f9ac4bc2243b88a4076680a585220d38b224d10ae02cd91478
payload manifest bytes: 11933
freeze run: 32799665340
freeze job: 97657914686
freeze Actions artifact ID: 9546054918
```

## Transport publication

Publisher PR: #15 (QA-only; closed without merge after PASS).

```text
publisher branch: qa/phase2-context-recovery-transport-publisher-2026-08-25
publisher head: a1c911493d2f5cec0dd0a169d1b95675f73abc51
workflow: phase2-context-recovery-transport
run: 32800990879
Ubuntu producer job: 97661608465
Windows consumer job: 97661642103
verdict: PASS
```

Published exact transport:

```text
branch: qa/phase2-context-recovery-final-b64-transport-f4aee34-2026-08-25
commit: 7c787eedd9856c3f91fbed85aeaea7f3405ad473
parent: f4aee34c0a3455aa7199f6aa54bd581c71d97337
path: extension/tests/qa_transport/phase2-context-recovery-final-b64/
format: YMB_PHASE2_CONTEXT_RECOVERY_EXACT_B64_TRANSPORT_V1
.gitattributes: * -text
```

Transport manifest:

```text
base64 length: 234628 bytes
chunk count: 1
chunk path: artifact.b64
chunk SHA-256: d72bce6d500582310bd1bda894ac5c57e023f03aa80f9b1ebd79427db4172398
```

## Producer proof

The producer did not trust or transform a prior text copy. It deterministically rebuilt the pinned product source with the governed candidate packer and stopped on any mismatch from frozen authority before encoding.

Observed producer gates:

```text
exact source = f4aee34c0a3455aa7199f6aa54bd581c71d97337
candidate SHA-256 = 739dd5d7cbefa98568bf51ae0ecab556360db534954fa0e27878ca5a77e7ae46
candidate bytes = 175971
payload manifest SHA-256 = bbe8b2665c3339f9ac4bc2243b88a4076680a585220d38b224d10ae02cd91478
files = 68
ZIP entries = 71
TRANSPORT_PRODUCER_FROZEN_AUTHORITY_PASS
TRANSPORT_PRODUCER_ZIP_INTEGRITY_PASS
TRANSPORT_B64_BUILD_PASS
B64_REASSEMBLY_PASS
EXACT_ZIP_IDENTITY_PASS
ROUNDTRIP_PAYLOAD_MANIFEST_PASS
ROUNDTRIP_ZIP_INTEGRITY_PASS
FROZEN_AUTHORITY_MATCH_PASS
REAL_YANDEX_REQUESTS=0
TRANSPORT_PUBLISH_PASS
```

## Windows consumer proof

The dependent consumer ran on `windows-latest` after forcing `core.autocrlf=true` before checkout of the exact published transport commit. The transport directory owns `.gitattributes` with `* -text`, so transport bytes must survive Windows checkout without newline conversion.

Observed Windows gates:

```text
WINDOWS_CORE_AUTOCRLF=true
WINDOWS_TRANSPORT_PARENT_PASS
WINDOWS_RAW_TEXT_POLICY_PASS
B64_REASSEMBLY_PASS
EXACT_ZIP_IDENTITY_PASS
ROUNDTRIP_PAYLOAD_MANIFEST_PASS
ROUNDTRIP_ZIP_INTEGRITY_PASS
FROZEN_AUTHORITY_MATCH_PASS
WINDOWS_SAFE_EXACT_TRANSPORT_PASS
REAL_YANDEX_REQUESTS=0
WINDOWS_TRANSPORT_CLEAN_PASS
```

The exact reconstructed ZIP on Windows therefore equals the frozen candidate `739dd5d7...`; its payload equals the exact payload manifest `bbe8b266...`; ZIP integrity and file/entry counts pass.

## Governance consequence

```text
PRODUCT_SOURCE = f4aee34c0a3455aa7199f6aa54bd581c71d97337
HANDOFF_ARTIFACT = 739dd5d7cbefa98568bf51ae0ecab556360db534954fa0e27878ca5a77e7ae46 / 175971 bytes / 68 files / 71 ZIP entries
PAYLOAD_MANIFEST = bbe8b2665c3339f9ac4bc2243b88a4076680a585220d38b224d10ae02cd91478 / 11933 bytes
WINDOWS_SAFE_TRANSPORT = PASS at 7c787eedd9856c3f91fbed85aeaea7f3405ad473
PRODUCTION_BYTES_CHANGED_SINCE_FREEZE = NO
PACKAGE_TEST_BYTES_CHANGED_SINCE_FREEZE = NO
OWNER_LIVE = BLOCKED
AUTHORIZED_NEXT_STAGE = COMPLETE_GOVERNED_GATE
```

The next gate must consume the exact Windows-safe transport and run the complete controlled campaign, including B-01/B-02/B-03, B-04 native popup geometry, B-05 already-open-ChatGPT context recovery, PD-00..PD-17, mandatory Manual-ON, S-00..S-17, final exactness and cleanliness, with zero real Yandex requests.
