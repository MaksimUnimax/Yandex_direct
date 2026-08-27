# Phase 5 Direct R2 — executable independent Codex runner preflight

Date: 2026-08-27  
Status: **PASS / QA-ONLY PREFLIGHT / NOT INDEPENDENT CODEX CREDIT**

Workflow run:

```text
33040808089
```

Job:

```text
98413735110
```

Exact preflight commit:

```text
8d0de953fa7b6357aac258e3ef96b0c1981599b4
```

The unchanged executable runner successfully consumed the exact frozen artifact and completed the full controlled matrix:

```text
source_suite=34/34
packaged_suite=34/34
source_syntax=33/33
packaged_syntax=33/33
source_json=2/2
packaged_json=2/2
CREDENTIAL_CONCURRENCY_REGRESSION=PASS
BROWSER_DIRECT_POPUP_D18=PASS
BROWSER_DIRECT_MANUAL_LIFECYCLE=PASS
BROWSER_DIRECT_ADDENDUM=PASS
BROWSER_PRIOR_PHASE_COMPATIBILITY=PASS
direct_controlled_provider_requests=2
controlled_search_stub_requests=1
real_yandex_direct_requests=0
real_yandex_requests=0
D-00..D-22=PASS
enabled_not_run_sections=0
NOT_RUN_COUNT=0
PRODUCT_BYTES_POST_TEST=IDENTICAL
PHASE5_DIRECT_R2_INDEPENDENT_RUNNER_PASS
INDEPENDENT_CODEX_RUNNER_PREFLIGHT_PASS
```

Final repository cleanliness also passed.

This proves the runner/venue is executable and complete. It does **not** replace the required independent Codex rerun. Owner-live remains blocked until Codex independently executes the rerun and returns PASS.
