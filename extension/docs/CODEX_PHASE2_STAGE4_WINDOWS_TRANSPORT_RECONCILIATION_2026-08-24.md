# Phase 2 Stage 4 — Windows-safe transport reconciliation

Date: 2026-08-24
Status: **CURRENT / MANDATORY TRANSPORT OVERRIDE FOR THE COMPLETE CODEX GATE**

This document reconciles the only artifact-transport defect found by the second Codex attempt. It does **not** change product bytes, package-test bytes, frozen source, exact ZIP bytes, payload manifest bytes, or the governed PD/S acceptance semantics.

## Precedence and scope

For the next complete Codex campaign, this document supersedes **only** stale references to the previous transport commit `9dedf7bf624174996fae7efa7a4bdbff6904d348` in earlier Stage-4 handoff/current-state/execution-map/checkpoint text.

All other requirements in these documents remain in force:

- `extension/docs/CODEX_PHASE2_STAGE4_FINAL_HANDOFF_2026-08-24.md`
- `extension/docs/PHASE_2_STAGE_4_CODEX_EXECUTION_MAP_2026-08-24.md`
- `extension/docs/CURRENT_STATE.md`
- `extension/tests/PHASE_2_STAGE_4_REFROZEN_CANDIDATE_CHECKPOINT_2026-08-24.md`
- parent PD gate and both mandatory addenda.

The explicit current owner/Codex instruction plus this reconciliation are the authority for transport identity. The old `9ded...` transport commit remains historical Linux consumer evidence only and must not be used for a new Codex checkout.

## Frozen candidate remains unchanged

```text
source commit: 0ee1d38f8d28cfccceb5a07f9606fa715261bc27
artifact: yandex-marketing-bridge-0.1.1-phase2-search-reconstruction-candidate.zip
artifact SHA-256: d58b5bd20921e9492a90b687ae3910c7049ddff17741da44ba832369eb1c0f16
artifact bytes: 170734
files: 65
ZIP entries: 68
payload manifest bytes: 11421
payload manifest SHA-256: 0edfcecdfb1025e7292d2d81f36b8fb6e5edb6f3332ef884d7f31e604ebdf7de
```

No refreeze is required because frozen package/test bytes did not change.

## Root cause of second Codex failure

The previous transport commit stored the correct LF payload-manifest blob, and Linux fresh-consumer verification passed. On Windows, Git checkout with CRLF conversion changed the working-tree manifest bytes:

```text
canonical LF bytes: 11421
canonical SHA-256: 0edfcecdfb1025e7292d2d81f36b8fb6e5edb6f3332ef884d7f31e604ebdf7de
LF newline count: 338
Windows CRLF bytes observed by Codex: 11759
Windows CRLF SHA-256 observed by Codex: b9586d1ad36cba70ef87f99f6b5749052c9d227e00b641b48d053cf878f38f36
11759 - 11421 = 338
```

Classification: `FAIL_ARTIFACT` at the consumed transport working-tree layer, caused by QA transport EOL policy. Frozen product bytes were not involved.

## Current Windows-safe transport authority

```text
branch: qa/phase2-stage4-final-b64-transport-0ee1d38-2026-08-24
transport commit: bc7754cff6416ff59942ff6f1052d450792888d5
path: extension/tests/qa_transport/phase2-stage4-final-b64/
```

The only change after historical transport commit `9ded...` is:

```text
extension/tests/qa_transport/phase2-stage4-final-b64/.gitattributes
content: * -text
```

This disables Git text/EOL conversion for every exact transport file in that directory.

## Mandatory Windows consumer proof already completed

A fresh read-only GitHub Actions Windows consumer was executed with Git-for-Windows and explicit `core.autocrlf=true`.

```text
run: 32717179084
job: 97400791303
OS: Microsoft Windows Server 2025
Git: 2.55.0.windows.4
core.autocrlf: true
transport head: bc7754cff6416ff59942ff6f1052d450792888d5
GitHub token: contents read
```

Observed proof:

```text
git check-attr text .../EXACT_CANDIDATE_MANIFEST_2026-08-24.json
=> text: unset

WINDOWS_RAW_MANIFEST_IDENTITY_PASS
B64_REASSEMBLY_PASS
EXACT_ZIP_IDENTITY_PASS
ROUNDTRIP_PAYLOAD_MANIFEST_PASS
ROUNDTRIP_ZIP_INTEGRITY_PASS
FROZEN_AUTHORITY_MATCH_PASS
WINDOWS_FROZEN_AUTHORITY_MATCH_PASS
WINDOWS_TRANSPORT_CLEAN_PASS
REAL_YANDEX_REQUESTS=0
```

The raw manifest after Windows checkout remained exactly `11421` bytes with SHA-256 `0edfcecd...`.

## Required Codex transport procedure

Start a **new** complete campaign. Do not resume either stopped attempt.

1. Fetch live `origin/main` and read commit metadata.
2. Read all mandatory Step-0 authority files, including this reconciliation.
3. Fresh-checkout exact transport commit:

```text
git checkout bc7754cff6416ff59942ff6f1052d450792888d5
```

4. Before running the transport verifier, prove the working-tree raw manifest identity:

```text
bytes = 11421
SHA-256 = 0edfcecdfb1025e7292d2d81f36b8fb6e5edb6f3332ef884d7f31e604ebdf7de
```

5. Run:

```text
python extension/tests/qa_transport/phase2-stage4-final-b64/verify_exact_b64_transport.py
```

Require:

```text
B64_REASSEMBLY_PASS
EXACT_ZIP_IDENTITY_PASS
ROUNDTRIP_PAYLOAD_MANIFEST_PASS
ROUNDTRIP_ZIP_INTEGRITY_PASS
FROZEN_AUTHORITY_MATCH_PASS
REAL_YANDEX_REQUESTS=0
```

6. Materialize the ZIP from the 16 chunks exactly as described by the final handoff, then execute the full campaign.

## Complete campaign remains mandatory

```text
PD-00..PD-17
+ mandatory Manual-ON real-popup transaction
+ S-00..S-17 Search Phase-2 addendum
```

No enabled `NOT_RUN` may receive PASS credit. Browser-owned assertions must execute in the qualified browser. Real Yandex requests and credentials remain forbidden. Do not patch product/tests during the campaign.

## Historical failed attempts

Attempt 1:

```text
FAIL_HARNESS at PD-00
cause: packaged-suite adapter authority document missing from main
reconciled by main commit 5fe4201c8fa62331efb3dec30a08b99f0f2aaa13
product bytes involved: NO
real Yandex requests: 0
```

Attempt 2:

```text
FAIL_ARTIFACT at PD-00 consumed transport layer
cause: Windows CRLF checkout converted exact manifest working-tree bytes
reconciled by transport commit bc7754cff6416ff59942ff6f1052d450792888d5
Windows fresh-consumer PASS run 32717179084 / job 97400791303
product bytes involved: NO
real Yandex requests: 0
```

Neither attempt executed product/source/package/browser/provider sections beyond PD-00, so neither is product-failure evidence.

## Final rule

If exact checkout `bc7754...` on Codex Windows still does not yield raw manifest `11421 / 0edfcecd...`, return `FAIL_HARNESS` with Git config/attribute evidence and do not continue. If identity passes, execute the **entire** existing Stage-4 gate without stopping at the historical failures.
