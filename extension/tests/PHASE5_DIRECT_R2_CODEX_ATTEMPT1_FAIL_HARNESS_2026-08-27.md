# Phase 5 Direct R2 — independent Codex attempt 1

Date: 2026-08-27  
Verdict: **FAIL_HARNESS**

The first independent Codex campaign established the exact corrected frozen candidate and completed the source/Direct Node portion, but did not execute mandatory packaged static/test staging or installed-extension browser gates.

Reported evidence:

```text
campaign: PHASE5_DIRECT_R2_COMPLETE_APPLICABLE_GATE
live_main_head: c2d5c59dc922ca82da55643cf94d7656339135b9
candidate_source: 841a1e2c1a503c4a05572a957ba97c55b9b60c52
product_tree: edf1c2d3494ebbc53ae778d23be1457eb885b605
artifact_sha256: ac8efc444578e9d3f31ac0325baca4b286fd608bc511850f480e0d397936620b
artifact_bytes: 406656
artifact_files: 39
transport: PASS
source_suite: 34/34
credential_concurrency_regression: PASS
D-00..D-17: PASS
D-21: PASS
D-18: NOT_RUN
D-19: NOT_RUN
D-20: NOT_RUN
D-22: NOT_RUN
enabled_not_run_sections: 10
NOT_RUN_COUNT: 10
PRODUCT_BYTES_POST_TEST: IDENTICAL
real_yandex_requests: 0
real_credentials_used: NO
verdict: FAIL_HARNESS
```

Classification:

- no product failure was established;
- no product/test/harness mutation occurred;
- no real Yandex credential/request was used;
- no refreeze is authorized or required;
- owner-live remains blocked;
- a new complete campaign must start from the beginning using the executable rerun handoff/runner.
