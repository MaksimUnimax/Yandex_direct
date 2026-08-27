# Phase 5 Direct R2 — independent Codex complete gate PASS

Date: 2026-08-27

Status: **INDEPENDENT PRE-DELIVERY PASS / OWNER-LIVE AUTHORIZED / PHASE 5 NOT CLOSED**

## Authority

```text
repository = MaksimUnimax/Yandex_direct
live main at campaign start = c2d5c59dc922ca82da55643cf94d7656339135b9
campaign = PHASE5_DIRECT_R2_COMPLETE_APPLICABLE_GATE_RERUN2
handoff branch = qa/phase5-direct-independent-codex-handoff-r2-2026-08-27
handoff commit = 1ebb8351bf896df1f7b7fd54001aefc048466f8f
step_0_authority = PASS
```

This was a new complete independent campaign. No PASS credit was transferred from earlier attempts.

Two earlier campaigns ended in `FAIL_HARNESS`. Those results are retained as historical harness-portability evidence only; neither was a product or artifact failure and neither changed/refroze the product.

## Immutable candidate identity

```text
candidate source = 841a1e2c1a503c4a05572a957ba97c55b9b60c52
extension/src tree = edf1c2d3494ebbc53ae778d23be1457eb885b605
candidate branch = candidate/phase5-direct-first-slice-r2-2026-08-27
freeze run = 33037955943
artifact id = 9632728199
artifact name = phase5-direct-r2-frozen-candidate-841a1e2
inner ZIP = yandex-marketing-bridge-0.1.1-phase5-direct-first-slice-r2-candidate.zip
ZIP SHA-256 = ac8efc444578e9d3f31ac0325baca4b286fd608bc511850f480e0d397936620b
ZIP bytes = 406656
ZIP files = 39
transport = PASS
```

## Source and packaged verification

```text
source_suite = 34/34
packaged_suite = 34/34
source_syntax = 33/33
packaged_syntax = 33/33
source_json = 2/2
packaged_json = 2/2
credential_concurrency_regression = PASS
```

## Installed-browser verification

```text
browser_direct_popup_d18 = PASS
browser_direct_manual_lifecycle = PASS
browser_direct_addendum = PASS
browser_prior_phase_compatibility = PASS
```

This covers the governed Direct popup geometry/save behavior, Manual lifecycle, controlled Direct addendum/Autorun coverage, and prior-phase browser compatibility.

## Governed Phase 5 gate

```text
D-00 = PASS
D-01 = PASS
D-02 = PASS
D-03 = PASS
D-04 = PASS
D-05 = PASS
D-06 = PASS
D-07 = PASS
D-08 = PASS
D-09 = PASS
D-10 = PASS
D-11 = PASS
D-12 = PASS
D-13 = PASS
D-14 = PASS
D-15 = PASS
D-16 = PASS
D-17 = PASS
D-18 = PASS
D-19 = PASS
D-20 = PASS
D-21 = PASS
D-22 = PASS
```

No required section remained unexecuted:

```text
enabled_not_run_sections = 0
NOT_RUN_COUNT = 0
```

## Controlled network / credential boundary

```text
direct_controlled_provider_requests = 2
controlled_search_stub_requests = 1
real_yandex_direct_requests = 0
real_yandex_requests = 0
real_credentials_used = NO
```

The campaign did not use owner credentials and did not contact the real Yandex provider.

## Immutability / cleanliness

```text
production_modified_during_gate = NO
package_tests_modified_during_gate = NO
direct_harness_modified_during_gate = NO
compatibility_harness_modified_during_gate = NO
source_workspace_clean = PASS
transport_workspace_clean = PASS
browser_harness_workspaces_clean = PASS
PRODUCT_BYTES_POST_TEST = IDENTICAL
runner_final_marker = PHASE5_DIRECT_R2_INDEPENDENT_RUNNER_PASS
```

## Independent verdict

```text
verdict = PASS
```

Interpretation:

```text
immutable candidate = PASS
exact artifact transport = PASS
source and packaged suites = PASS
installed-browser gates = PASS
D-00..D-22 = PASS
NOT_RUN_COUNT = 0
product bytes after gate = IDENTICAL
independent pre-delivery acceptance = PASS
```

Therefore the narrow Phase-5 owner-live boundary is now authorized.

This document does **not** close Phase 5 and does **not** authorize a product modification, refreeze, merge, Direct write operation, bid change, finance action, quota/error experiment, offline report queue, polling, or repeated exploratory live traffic.

Next required stage:

```text
AUTHORIZED_NEXT_STAGE = PHASE5_DIRECT_OWNER_LIVE
PHASE5_DIRECT_CLOSURE = BLOCKED_UNTIL_OWNER_LIVE_PASS
```
