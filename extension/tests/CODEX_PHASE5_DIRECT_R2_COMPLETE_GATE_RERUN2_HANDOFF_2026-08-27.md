# Codex Phase 5 Direct R2 — complete gate rerun 2 handoff

Date: 2026-08-27

Status: **READY FOR ONE NEW COMPLETE INDEPENDENT CODEX CAMPAIGN / EXACT FROZEN ARTIFACT / OWNER-LIVE BLOCKED**

## 0. Campaign reset and role

This is a new independent campaign from the beginning.

Two earlier independent attempts returned `FAIL_HARNESS`. Neither was `FAIL_PRODUCT` or `FAIL_ARTIFACT`, and neither authorizes a product change or refreeze. Do not transfer PASS credit from those attempts.

Codex is the independent QA executor only. Do not:

- edit product bytes;
- edit the frozen ZIP;
- edit package tests;
- edit governed browser harnesses;
- edit either complete-gate runner;
- weaken, skip, reinterpret or replace assertions;
- use real Yandex credentials;
- make real Yandex requests;
- substitute a rebuilt/logically equivalent ZIP for the exact frozen artifact.

Allowed final verdicts only:

```text
PASS
FAIL_PRODUCT
FAIL_ARTIFACT
FAIL_HARNESS
```

A PASS requires the complete campaign to finish with all required sections executed and the final runner marker present.

## 1. Repository and live authority

Repository:

```text
MaksimUnimax/Yandex_direct
```

Fetch live `origin/main` at campaign start and record its SHA.

Read the living Phase 5 authority from main, including at minimum:

```text
extension/docs/WORKFLOW_OPERATING_RULES.md
extension/docs/CURRENT_STATE.md
extension/docs/SPECIFICATION_PHASE_5_DIRECT_ADDENDUM.md
extension/docs/PHASE_5_DIRECT_REQUIREMENTS_AND_IMPLEMENTATION_PLAN.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_DIRECT_PHASE5_ADDENDUM.md
extension/docs/CODEX_PRE_DELIVERY_NATIVE_ACTION_POPUP_GEOMETRY_ADDENDUM_2026-08-24.md
extension/docs/CODEX_QA_ARTIFACT_TRANSPORT_AND_GATE_RUNBOOK.md
```

Also read the prior attempt records on this handoff branch:

```text
extension/tests/PHASE5_DIRECT_R2_CODEX_ATTEMPT1_FAIL_HARNESS_2026-08-27.md
extension/tests/PHASE5_DIRECT_R2_CODEX_ATTEMPT2_FAIL_HARNESS_2026-08-27.md
```

They are failure-history evidence only.

## 2. Immutable corrected product authority

Use only:

```text
source commit = 841a1e2c1a503c4a05572a957ba97c55b9b60c52
extension/src tree = edf1c2d3494ebbc53ae778d23be1457eb885b605
candidate branch = candidate/phase5-direct-first-slice-r2-2026-08-27
candidate freeze trigger = 389084290635fbf2ac305098adc3aae17f967c83
freeze run = 33037955943
artifact id = 9632728199
artifact name = phase5-direct-r2-frozen-candidate-841a1e2
inner ZIP = yandex-marketing-bridge-0.1.1-phase5-direct-first-slice-r2-candidate.zip
inner ZIP SHA-256 = ac8efc444578e9d3f31ac0325baca4b286fd608bc511850f480e0d397936620b
inner ZIP bytes = 406656
product files = 39
```

The old `fcfb19c7...` candidate is superseded and forbidden.

Credential architecture must remain:

```text
Wordstat != Search != Webmaster != Metrika != Direct
```

No credential consolidation is allowed.

## 3. Exact runner authority for this campaign

Do **not** execute the v1 runner as the campaign entrypoint.

Execute exactly:

```text
extension/tests/qa_phase5_codex/phase5_direct_r2_complete_gate_runner_v2.py
```

The portable v2 runner is a QA-only execution layer over the unchanged v1 campaign logic. Its exact tested runner commit is:

```text
42ad3302a1f046929433d49aba0678e181c53af4
```

The final v2 runner was independently preflighted on the exact same frozen product bytes in both:

```text
GitHub Actions run = 33041647558
Linux Node 24 = PASS
Windows Node 24 = PASS
```

This is venue/preflight evidence only; do not transfer PASS credit.

The v2 portability layer changes no product assertion. It only handles host differences:

- process-local Git safe-directory;
- Node 22/24 TAP output;
- Windows filesystem path ordering;
- Python `__pycache__` avoidance;
- CRLF Git-index noise after byte-authoritative product identity;
- a Windows-only ephemeral copy of the Direct addendum where the generic wait timeout is changed from 25s to 60s. Every fixture and assertion is otherwise identical, the governed source harness remains unchanged, and the temporary adapter is deleted before final cleanliness.

Do not modify this portability behavior during the campaign.

## 4. Artifact acquisition

Use authenticated GitHub transport and retrieve artifact ID `9632728199` from freeze run `33037955943`.

Preferred GitHub CLI retrieval into a fresh temporary directory:

```text
gh run download 33037955943 --repo MaksimUnimax/Yandex_direct --name phase5-direct-r2-frozen-candidate-841a1e2 --dir <FRESH_TEMP_TRANSPORT>
```

Then run v2 with the explicit transport directory:

```text
python extension/tests/qa_phase5_codex/phase5_direct_r2_complete_gate_runner_v2.py --transport-dir <FRESH_TEMP_TRANSPORT>
```

If the host has an authenticated `gh` and the runner's automatic artifact acquisition is available, running without `--transport-dir` is acceptable:

```text
python extension/tests/qa_phase5_codex/phase5_direct_r2_complete_gate_runner_v2.py
```

Do not ask the owner to download/re-upload the artifact.

Do not manually unpack and substitute another product tree. The runner must establish exact transport identity itself.

## 5. Runtime dependencies

Node 24 is explicitly supported by v2 and was preflighted on Windows and Linux. Node 22 is also acceptable, but switching versions is not required.

The runner is allowed to provision external QA dependencies such as:

```text
puppeteer@24
Chrome for Testing
xvfb on headless Linux when already available/required
```

External QA dependencies are not product mutations.

On Windows, run the Python runner directly. No `xvfb` is required.

Do not stop merely because Git reports LF/CRLF index noise for `extension/src`; v2 independently hashes the exact product bytes and treats that byte identity as authoritative while still requiring the rest of the governed workspace to remain clean.

## 6. Mandatory complete result

The v2 runner must independently execute all of the following in this one campaign:

```text
source suite
source JS syntax
source JSON
credential concurrency regression
exact artifact SHA/bytes/manifest/path/hash verification
packaged suite against exact frozen bytes
packaged JS syntax
packaged JSON
Direct addendum coverage
Direct popup D18 installed-extension browser gate
Direct Manual lifecycle installed-extension browser gate
Direct D16/D17/D19/D20 installed-extension browser addendum
prior Phase2/Stage4 browser compatibility gate
final product/test/harness/artifact byte identity and cleanliness
D-00 through D-22 final matrix
```

A PASS requires at minimum these final values/markers:

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
enabled_not_run_sections=0
NOT_RUN_COUNT=0
PRODUCT_BYTES_POST_TEST=IDENTICAL
D-00: PASS
D-01: PASS
D-02: PASS
D-03: PASS
D-04: PASS
D-05: PASS
D-06: PASS
D-07: PASS
D-08: PASS
D-09: PASS
D-10: PASS
D-11: PASS
D-12: PASS
D-13: PASS
D-14: PASS
D-15: PASS
D-16: PASS
D-17: PASS
D-18: PASS
D-19: PASS
D-20: PASS
D-21: PASS
D-22: PASS
PHASE5_DIRECT_R2_INDEPENDENT_RUNNER_PASS
```

If the final runner marker is absent, PASS is forbidden.

If any enabled section is NOT_RUN, PASS is forbidden.

If a governed product assertion fails after the exact artifact is established, classify it `FAIL_PRODUCT` rather than repairing it.

If artifact identity fails, classify it `FAIL_ARTIFACT`.

If only the execution environment/runner cannot execute a required section, classify it `FAIL_HARNESS` and return the exact command/error without modifying the runner or governed harnesses.

## 7. Required final report

Return one report headed exactly:

```text
CODEX_YANDEX_PRE_DELIVERY_FULL_REGRESSION_GATE_RESULT
```

Include at minimum:

```text
campaign: PHASE5_DIRECT_R2_COMPLETE_APPLICABLE_GATE_RERUN2
live_main_head: <actual>
step_0_authority: PASS|FAIL
candidate_source: 841a1e2c1a503c4a05572a957ba97c55b9b60c52
product_tree: edf1c2d3494ebbc53ae778d23be1457eb885b605
artifact_sha256: ac8efc444578e9d3f31ac0325baca4b286fd608bc511850f480e0d397936620b
artifact_bytes: 406656
artifact_files: 39
transport: PASS|FAIL
source_suite: <pass>/<total>|NOT_RUN
packaged_suite: <pass>/<total>|NOT_RUN
source_syntax: <pass>/<total>|NOT_RUN
packaged_syntax: <pass>/<total>|NOT_RUN
source_json: <pass>/<total>|NOT_RUN
packaged_json: <pass>/<total>|NOT_RUN
credential_concurrency_regression: PASS|FAIL|NOT_RUN
browser_direct_popup_d18: PASS|FAIL|NOT_RUN
browser_direct_manual_lifecycle: PASS|FAIL|NOT_RUN
browser_direct_addendum: PASS|FAIL|NOT_RUN
browser_prior_phase_compatibility: PASS|FAIL|NOT_RUN
D-00: PASS|FAIL|NOT_RUN
...
D-22: PASS|FAIL|NOT_RUN
direct_controlled_provider_requests: <integer>|NOT_RUN
controlled_search_stub_requests: <integer>|NOT_RUN
direct_real_yandex_requests: 0|<actual>
real_yandex_requests: 0|<actual>
direct_real_credentials_used: NO|YES
real_credentials_used: NO|YES
production_modified_during_gate: NO|YES
package_tests_modified_during_gate: NO|YES
direct_harness_modified_during_gate: NO|YES
compatibility_harness_modified_during_gate: NO|YES
source_workspace_clean: PASS|FAIL|NOT_RUN
transport_workspace_clean: PASS|FAIL|NOT_RUN
browser_harness_workspaces_clean: PASS|FAIL|NOT_RUN
enabled_not_run_sections: <integer>
NOT_RUN_COUNT: <integer>
PRODUCT_BYTES_POST_TEST: IDENTICAL|CHANGED|NOT_RUN
runner_final_marker: present|absent
verdict: PASS|FAIL_PRODUCT|FAIL_ARTIFACT|FAIL_HARNESS
```

## 8. Owner-live boundary

Owner-live remains BLOCKED during this campaign.

Only after a real independent Codex report returns:

```text
verdict: PASS
enabled_not_run_sections: 0
NOT_RUN_COUNT: 0
PRODUCT_BYTES_POST_TEST: IDENTICAL
runner_final_marker: present
```

may the project record independent Codex PASS and move to the narrow owner-live Direct acceptance.
