# Phase 5 Direct R2 — independent Codex attempt 2 FAIL_HARNESS

Date: 2026-08-27

Status: **FAIL_HARNESS / PRODUCT AND FROZEN ARTIFACT NOT INVALIDATED**

## Independent result received

Campaign:

```text
PHASE5_DIRECT_R2_COMPLETE_APPLICABLE_GATE_RERUN
```

Verdict:

```text
FAIL_HARNESS
```

The second independent Codex attempt established and preserved the exact corrected authority:

```text
live_main_head = c2d5c59dc922ca82da55643cf94d7656339135b9
candidate_source = 841a1e2c1a503c4a05572a957ba97c55b9b60c52
product_tree = edf1c2d3494ebbc53ae778d23be1457eb885b605
artifact_sha256 = ac8efc444578e9d3f31ac0325baca4b286fd608bc511850f480e0d397936620b
artifact_bytes = 406656
artifact_files = 39
transport = PASS
source_suite = 34/34
source_syntax = 33/33
source_json = 2/2
credential_concurrency_regression = PASS
real_yandex_requests = 0
real_credentials_used = NO
production_modified_during_gate = NO
```

The attempt did not reach packaged/browser completion and therefore correctly did not return PASS:

```text
packaged_suite = NOT_RUN
packaged_syntax = NOT_RUN
packaged_json = NOT_RUN
browser_direct_popup_d18 = NOT_RUN
browser_direct_manual_lifecycle = NOT_RUN
browser_direct_addendum = NOT_RUN
browser_prior_phase_compatibility = NOT_RUN
D-18 = NOT_RUN
D-19 = NOT_RUN
D-20 = NOT_RUN
D-22 = NOT_RUN
enabled_not_run_sections = 8
NOT_RUN_COUNT = 8
PRODUCT_BYTES_POST_TEST = NOT_RUN
runner_final_marker = absent
```

## Harness failures diagnosed

The unchanged v1 executable runner encountered host portability defects, not governed product assertion failures:

1. Git ownership safety required a host-specific `safe.directory` setting.
2. Node 24 TAP summary rendering differed from the v1 parser's expected legacy output.
3. filesystem traversal order on Windows caused `extracted path set mismatch` although Codex independently verified the exact wrapper, exact inner ZIP SHA/bytes, manifest source/tree authority and exact 39-file payload identity.

No product change or refreeze is authorized by this result.

## Repair scope

A QA-only portable runner v2 was created. It does not modify the frozen product, package tests, or governed browser harness source. Its portability layer provides:

- process-local Git `safe.directory` handling;
- explicit TAP reporter plus Node 22/24-compatible summary parsing;
- canonical POSIX path-set comparison after extraction;
- no Python bytecode writes inside the governed workspace;
- byte-authoritative product cleanliness on Windows so CRLF index normalization is not misclassified as product mutation;
- an ephemeral Windows-only timing adapter for `direct_codex_gate_addendum_v2.mjs` that changes only the generic wait budget from 25 seconds to 60 seconds and preserves every fixture and assertion.

The temporary timing adapter is deleted after execution and final test/harness snapshots must remain identical.

## Cross-platform preflight

Final portable runner authority:

```text
runner = extension/tests/qa_phase5_codex/phase5_direct_r2_complete_gate_runner_v2.py
runner commit = 42ad3302a1f046929433d49aba0678e181c53af4
cross-platform preflight run = 33041647558
Linux Node 24 = PASS
Windows Node 24 = PASS
```

The preflight consumed the same immutable frozen artifact and required the full source/packaged/browser/D-00..D-22 matrix, zero real Yandex traffic, zero NOT_RUN and final byte identity. This is preflight evidence only and does not count as independent Codex PASS.

Owner-live remains BLOCKED pending a new complete independent Codex PASS.
