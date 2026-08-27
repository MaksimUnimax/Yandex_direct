# Codex Phase 5 Direct R2 — complete gate rerun handoff after FAIL_HARNESS

Date: 2026-08-27  
Status: **READY FOR ONE NEW COMPLETE INDEPENDENT CODEX CAMPAIGN / EXACT FROZEN ARTIFACT / OWNER-LIVE BLOCKED**

## 0. Why this rerun exists

The first independent Codex attempt correctly returned:

```text
verdict: FAIL_HARNESS
enabled_not_run_sections: 10
NOT_RUN_COUNT: 10
```

It independently established the exact artifact and passed source/Direct Node evidence, but did not execute packaged static/test staging or the required installed-extension browser gates. Therefore that attempt is not a product failure and does not authorize a product change or refreeze.

This rerun starts a **new complete campaign from the beginning**. Do not transfer PASS credit from the failed campaign. The exact product candidate remains unchanged.

## 1. Immutable candidate authority

Repository:

```text
MaksimUnimax/Yandex_direct
```

Exact product authority:

```text
source commit = 841a1e2c1a503c4a05572a957ba97c55b9b60c52
extension/src tree = edf1c2d3494ebbc53ae778d23be1457eb885b605
candidate branch = candidate/phase5-direct-first-slice-r2-2026-08-27
freeze trigger = 389084290635fbf2ac305098adc3aae17f967c83
freeze run = 33037955943
artifact id = 9632728199
artifact name = phase5-direct-r2-frozen-candidate-841a1e2
inner ZIP = yandex-marketing-bridge-0.1.1-phase5-direct-first-slice-r2-candidate.zip
inner ZIP SHA-256 = ac8efc444578e9d3f31ac0325baca4b286fd608bc511850f480e0d397936620b
inner ZIP bytes = 406656
product files = 39
```

The old `fcfb19c7...` candidate remains superseded and forbidden.

Credential architecture remains intentionally separate:

```text
Wordstat != Search != Webmaster != Metrika != Direct
```

No token/credential consolidation is authorized.

## 2. Rerun QA authority

Use this exact rerun handoff branch/commit supplied by ChatGPT. Before execution verify that, relative to the corrected frozen QA authority, the rerun delta contains QA-only runner/workflow/handoff files and **zero product bytes**.

The executable authority for this rerun is:

```text
extension/tests/qa_phase5_codex/phase5_direct_r2_complete_gate_runner.py
```

Do not edit this runner.

The runner is intentionally cross-platform:

- Windows: launches the Puppeteer installed-extension gates directly in a real headful Chrome process.
- Linux with DISPLAY: launches directly.
- Linux without DISPLAY: requires and uses `xvfb-run`.

It uses Node 22-compatible tests and installs only the external QA driver dependency `puppeteer@24` with `--no-save --package-lock=false`; it removes the temporary `node_modules` before final cleanliness validation.

## 3. Mandatory authority read

Before running the executable gate, fetch current `origin/main`, record its actual HEAD and read at minimum:

```text
extension/docs/WORKFLOW_OPERATING_RULES.md
extension/docs/CURRENT_STATE.md
extension/docs/PROJECT_PURPOSE.md
extension/docs/SPECIFICATION.md
extension/docs/SPECIFICATION_PHASE_2_SEARCH_ADDENDUM.md
extension/docs/SPECIFICATION_PHASE_3_WEBMASTER_ADDENDUM.md
extension/docs/SPECIFICATION_PHASE_4_METRIKA_ADDENDUM.md
extension/docs/SPECIFICATION_PHASE_5_DIRECT_ADDENDUM.md
extension/docs/PHASE_5_DIRECT_REQUIREMENTS_AND_IMPLEMENTATION_PLAN.md
extension/docs/ROADMAP.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_MANUAL_ON_TRANSACTION_ADDENDUM_2026-08-19.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_SEARCH_PHASE2_ADDENDUM.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_WEBMASTER_PHASE3_ADDENDUM.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_METRIKA_PHASE4_ADDENDUM.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_DIRECT_PHASE5_ADDENDUM.md
extension/docs/CODEX_PRE_DELIVERY_NATIVE_ACTION_POPUP_GEOMETRY_ADDENDUM_2026-08-24.md
extension/docs/CODEX_QA_ARTIFACT_TRANSPORT_AND_GATE_RUNBOOK.md
this rerun handoff
```

Do not substitute current `main` product bytes for the exact frozen candidate.

## 4. Exact execution procedure — do not leave mandatory sections NOT_RUN

Start from a fresh clean checkout of the exact rerun handoff commit.

Required tools:

```text
git
Python 3
Node.js 22 (or a compatible newer Node if 22 is unavailable; report actual version)
npm/npx
authenticated gh CLI only if the exact artifact files are not already materialized
Chrome installed/downloadable through Puppeteer
```

### Preferred execution

Run exactly:

```text
python extension/tests/qa_phase5_codex/phase5_direct_r2_complete_gate_runner.py
```

The runner will use authenticated `gh run download` to acquire the exact frozen artifact itself.

### If the exact Actions artifact was already independently materialized

You may instead pass the directory containing exactly these two files:

```text
yandex-marketing-bridge-0.1.1-phase5-direct-first-slice-r2-candidate.zip
PHASE5_DIRECT_R2_EXACT_CANDIDATE_MANIFEST_2026-08-27.json
```

Run:

```text
python extension/tests/qa_phase5_codex/phase5_direct_r2_complete_gate_runner.py --transport-dir <EXACT_ARTIFACT_DIRECTORY>
```

Do not rebuild or substitute another ZIP.

### Environment-specific browser rule

On Windows, do **not** search for `xvfb-run`; the runner launches the headful browser directly.

On Linux without DISPLAY, `xvfb-run` is required. If absent, installing/provisioning `xvfb` is a QA-environment action and is allowed because it does not mutate product/test/harness bytes. After provisioning, rerun the unchanged runner from a fresh clean campaign workspace.

Likewise, installing the runner-declared Puppeteer driver/browser is a QA-environment action, not a product mutation.

Do not classify a merely missing external dependency as justification to skip browser sections and continue to a PASS-shaped report. Either provision the dependency and execute the sections, or return `FAIL_HARNESS` with the exact failed command/error.

## 5. What the runner independently executes

The unchanged runner performs all of the following in one campaign:

1. verifies exact source `extension/src` tree;
2. creates a detached clean source worktree at `841a1e2...`;
3. runs the complete source Node suite;
4. runs source JS/MJS syntax checks and parses all product JSON;
5. runs the three credential-concurrency regression assertions;
6. downloads or consumes the exact frozen Actions artifact;
7. verifies ZIP SHA/bytes, manifest authority, ZIP integrity, exact 39-path set and every per-file SHA/byte count;
8. stages the **transported exact ZIP contents** as `extension/src` in the immutable QA harness workspace;
9. requires staged package bytes to equal the manifest and tracked frozen product;
10. runs the complete packaged Node suite;
11. runs packaged JS/MJS syntax checks and parses all packaged product JSON;
12. runs the Phase 5 Direct addendum Node gate and credential concurrency test against packaged bytes;
13. installs only temporary Puppeteer QA dependencies;
14. runs `direct_popup_d18.mjs`;
15. runs `direct_manual_worker_lifecycle.mjs`;
16. runs `direct_codex_gate_addendum_v2.mjs`;
17. runs `phase2-stage4/browser_phase2_stage4_compat_gate.mjs`;
18. requires exactly `DIRECT_CONTROLLED_PROVIDER_REQUESTS=2`;
19. requires exactly `BROWSER_CONTROLLED_SEARCH_STUB_REQUESTS=1`;
20. requires zero real Yandex traffic markers;
21. removes temporary npm runtime dependencies;
22. verifies product/test/browser-harness/transport hashes unchanged;
23. requires clean source and QA workspaces;
24. re-hashes the frozen ZIP;
25. emits `D-00..D-22 PASS`, `NOT_RUN_COUNT=0`, and `PRODUCT_BYTES_POST_TEST=IDENTICAL` only after every assertion above succeeds.

The runner itself does not make real Yandex requests and browser provider traffic is controlled/stubbed only.

## 6. Required success markers

A complete successful execution must contain at minimum:

```text
STEP0_AUTHORITY_PASS
TRANSPORT=PASS
CREDENTIAL_CONCURRENCY_REGRESSION=PASS
FROZEN_PRODUCT_INSTALLED_EXACTLY_PASS
FROZEN_NODE_D01_D17_D21_PASS
BROWSER_DIRECT_POPUP_D18=PASS
BROWSER_DIRECT_MANUAL_LIFECYCLE=PASS
BROWSER_DIRECT_ADDENDUM=PASS
BROWSER_PRIOR_PHASE_COMPATIBILITY=PASS
D-22: PASS
PRODUCT_BYTES_POST_TEST=IDENTICAL
enabled_not_run_sections=0
NOT_RUN_COUNT=0
direct_controlled_provider_requests=2
controlled_search_stub_requests=1
real_yandex_direct_requests=0
real_yandex_requests=0
D-00: PASS
...
D-22: PASS
PHASE5_DIRECT_R2_INDEPENDENT_RUNNER_PASS
```

If the final runner marker is absent, do not return PASS.

## 7. Mandatory role / mutation rules

Codex is independent QA executor only. During this campaign it MUST NOT:

- edit production code;
- edit package tests;
- edit the runner;
- edit browser/compatibility harnesses;
- edit or replace the exact artifact;
- weaken or skip assertions;
- refreeze;
- use real credentials;
- make real Yandex requests;
- patch a failing product/test/harness to manufacture PASS.

Allowed external environment provisioning is limited to runtime QA tooling such as Node/Python/Puppeteer/Chrome/xvfb. Product/repository authority must remain unchanged.

Allowed final verdicts only:

```text
PASS
FAIL_PRODUCT
FAIL_ARTIFACT
FAIL_HARNESS
```

A PASS requires:

```text
enabled_not_run_sections = 0
NOT_RUN_COUNT = 0
PHASE5_DIRECT_R2_INDEPENDENT_RUNNER_PASS present
```

## 8. Required final report

Return one report headed exactly:

```text
CODEX_YANDEX_PRE_DELIVERY_FULL_REGRESSION_GATE_RESULT
```

Include:

```text
campaign: PHASE5_DIRECT_R2_COMPLETE_APPLICABLE_GATE_RERUN
live_main_head: <actual>
step_0_authority: PASS|FAIL
candidate_source: 841a1e2c1a503c4a05572a957ba97c55b9b60c52
product_tree: edf1c2d3494ebbc53ae778d23be1457eb885b605
artifact_sha256: ac8efc444578e9d3f31ac0325baca4b286fd608bc511850f480e0d397936620b
artifact_bytes: 406656
artifact_files: 39
transport: PASS|FAIL
source_suite: <pass>/<total>
packaged_suite: <pass>/<total>
source_syntax: <pass>/<total>
packaged_syntax: <pass>/<total>
source_json: <pass>/<total>
packaged_json: <pass>/<total>
credential_concurrency_regression: PASS|FAIL
browser_direct_popup_d18: PASS|FAIL
browser_direct_manual_lifecycle: PASS|FAIL
browser_direct_addendum: PASS|FAIL
browser_prior_phase_compatibility: PASS|FAIL
D-00: PASS|FAIL
...
D-22: PASS|FAIL
direct_controlled_provider_requests: <integer>
controlled_search_stub_requests: <integer>
direct_real_yandex_requests: 0
real_yandex_requests: 0
direct_real_credentials_used: NO
real_credentials_used: NO
production_modified_during_gate: NO
package_tests_modified_during_gate: NO
direct_harness_modified_during_gate: NO
compatibility_harness_modified_during_gate: NO
source_workspace_clean: PASS|FAIL
transport_workspace_clean: PASS|FAIL
browser_harness_workspaces_clean: PASS|FAIL
enabled_not_run_sections: 0
NOT_RUN_COUNT: 0
PRODUCT_BYTES_POST_TEST: IDENTICAL
runner_final_marker: PHASE5_DIRECT_R2_INDEPENDENT_RUNNER_PASS
failures: [] | <complete failure list>
verdict: PASS|FAIL_PRODUCT|FAIL_ARTIFACT|FAIL_HARNESS
```

Owner-live remains blocked until this rerun returns a genuine independent `PASS`.
