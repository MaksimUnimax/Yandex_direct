# YMB Deferred Search Patch B — exact identity / WIP transport block 7

Date: 2026-09-12
Branch: `wip/ymb-search-async-patch-b-2026-09-12`
Candidate: Patch B candidate1.

## Exact production identity

The full saved candidate manifest was rechecked after all Patch-B Blocks 1–6 and browser-scale/provider-boundary work.

```text
EXPECTED_FILES = 59
ACTUAL_FILES = 59
SHA256_MISMATCHES = 0
JS_FILES_CHECKED = 53
JS_SYNTAX_FAIL = 0
MANIFEST_JSON_PARSE = PASS
PACKAGE_JSON_PARSE = PASS
PRODUCTION_BYTE_DRIFT = 0
```

The candidate remains exactly the same production bytes exercised by the recorded Node/browser evidence.

## Durable WIP postimage transport

The invalid/truncated earlier one-file Base64 evidence object was removed from the WIP branch. It is not authority.

The exact changed-postimage tar is now represented by six small independently persisted files under `postimage_parts/` plus `POSTIMAGE_PARTS_MANIFEST.md`.

Remote GitHub readback matched local Git blob SHA and byte count for all six parts:

```text
part-01: 4000 bytes / 38d5b38155abde72f938e7716abba7993acb6e5c
part-02: 4000 bytes / 94c8f1426bb6688d37b22b54e85893495e4a3e40
part-03: 4000 bytes / 4cf71a87a065517f8722795e334808938f1e9aca
part-04: 4000 bytes / 0902004fc3d199beac46d4c8ca665d2b7dfefbc8
part-05: 4000 bytes / e56b65ad591959d9496bbb18f75d0300fe913d28
part-06: 2856 bytes / 87ff5cd14c2a1253b8a6b9d08bf480506258cd6d
REMOTE_PART_READBACK = 6/6 PASS
```

Expected reconstruction identities:

```text
combined_base64_bytes = 22856
combined_base64_sha256 = 04c6b247460e1de6c625cdd5adc0a985f096200c286956deaf1fed8f378491dc
decoded_tar_gz_bytes = 17141
decoded_tar_gz_sha256 = 4c2fc2c4d97149b73d27b6b329749ce16b6b2f01fe838d2516dd536d677a62ef
changed_postimages_in_tar = 8
```

This evidence transport changes no production bytes.

## Verdict

```text
PATCH_B_EXACT_CANDIDATE_IDENTITY = PASS
PATCH_B_WIP_POSTIMAGE_TRANSPORT = PASS
PRODUCTION_BYTES_CHANGED_IN_BLOCK = NO
PATCH_B_ACCEPTED_FOR_INTEGRATION = READY_FOR_DECISION
RELEASE_ALLOWED = NO
OWNER_HANDOFF = FORBIDDEN
```

Patch B may now receive an acceptance-for-integration checkpoint, but it is not an installable release and must still pass A+B integration, final cross-layer resource/dependency regression, full pre-delivery gate and fresh-package identity before any owner ZIP.
