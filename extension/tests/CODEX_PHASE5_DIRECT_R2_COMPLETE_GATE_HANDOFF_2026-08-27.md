# Codex Phase 5 Direct R2 — independent complete pre-delivery gate handoff

Date: 2026-08-27  
Status: **READY FOR ONE NEW INDEPENDENT CODEX COMPLETE CAMPAIGN / EXACT FROZEN ARTIFACT / OWNER-LIVE BLOCKED**

Codex is the independent QA executor for this campaign. ChatGPT owns development, repair, packaging, transport preparation and preflight. This campaign must independently consume and test the exact already-frozen candidate. It must not convert the existing GitHub Actions preflight into Codex PASS credit.

## 0. Mandatory role and verdict rules

Codex MUST NOT:

- edit production code;
- edit package tests;
- edit governed QA/browser harnesses;
- edit or replace the frozen candidate ZIP;
- weaken, skip, reinterpret or replace assertions;
- refreeze or substitute a logically equivalent package;
- use real Yandex credentials;
- make real Yandex requests;
- patch a failure and continue as though the original candidate passed.

Allowed final verdicts only:

```text
PASS
FAIL_PRODUCT
FAIL_ARTIFACT
FAIL_HARNESS
```

A PASS requires every enabled applicable section to execute. `enabled_not_run_sections` and `NOT_RUN_COUNT` must both be `0`.

If a mandatory assertion fails, preserve evidence and classify the failing layer. Continue unrelated safe sections when possible so the final report contains the complete failure set.

## 1. Reconstruct live project authority first

Repository:

```text
MaksimUnimax/Yandex_direct
```

Fetch current `origin/main` at campaign start. Record the actual live main SHA. Do not assume a historical SHA is still current.

At handoff preparation time main was:

```text
c2d5c59dc922ca82da55643cf94d7656339135b9
```

If main legitimately advanced, inspect the new commits and continue only when the Phase 5 authority below remains in force. Do not silently substitute newer production bytes for the frozen candidate.

Read from live `main` before product testing:

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
```

Also read this exact candidate checkpoint from the QA authority used for this handoff:

```text
branch: qa/phase5-direct-frozen-r2-gate-2026-08-27
path: extension/tests/PHASE5_DIRECT_R2_FROZEN_CANDIDATE_CHECKPOINT_2026-08-27.md
```

The GitHub Actions frozen-artifact gate recorded there is **pre-Codex evidence only**. It is not an independent Codex result.

## 2. Exact corrected candidate authority

The previous Phase 5 candidate containing the credential-store concurrency defect is superseded and forbidden for this campaign.

Do NOT use:

```text
candidate/phase5-direct-first-slice-2026-08-27
old ZIP SHA prefix: fcfb19c7
```

Use only the corrected authority:

```text
corrected source branch:
fix/phase5-credential-runtime-concurrency-2026-08-27

exact source commit:
841a1e2c1a503c4a05572a957ba97c55b9b60c52

exact extension/src tree:
edf1c2d3494ebbc53ae778d23be1457eb885b605

candidate branch:
candidate/phase5-direct-first-slice-r2-2026-08-27

candidate freeze-trigger commit:
389084290635fbf2ac305098adc3aae17f967c83
```

The corrected defect was a real credential-store concurrency race. The fix serializes credential-store mutations and re-reads current state under the same mutation lock; Backup credential import participates in that lock.

The credential architecture remains separate and must remain so:

```text
Wordstat != Search != Webmaster != Metrika != Direct
```

Any evidence of credential/token consolidation is `FAIL_PRODUCT`.

## 3. Acquire the exact frozen artifact from the proven GitHub Actions transport

Freeze run:

```text
33037955943
```

Published GitHub Actions artifact:

```text
name:
phase5-direct-r2-frozen-candidate-841a1e2

artifact id:
9632728199

GitHub artifact wrapper digest recorded by Actions:
sha256:ef8c7acd127d3f37820843e6a4f27379d7c8668d812022949739b7a0d598887c

GitHub artifact wrapper size recorded by Actions:
414023 bytes
```

The artifact contains:

```text
yandex-marketing-bridge-0.1.1-phase5-direct-first-slice-r2-candidate.zip
PHASE5_DIRECT_R2_EXACT_CANDIDATE_MANIFEST_2026-08-27.json
```

Authoritative inner installable ZIP identity:

```text
SHA-256:
ac8efc444578e9d3f31ac0325baca4b286fd608bc511850f480e0d397936620b

bytes:
406656

product files:
39
```

Use authenticated GitHub transport directly. A suitable route is the GitHub CLI / Actions API, for example:

```text
gh run download 33037955943 \
  --repo MaksimUnimax/Yandex_direct \
  --name phase5-direct-r2-frozen-candidate-841a1e2 \
  --dir <FRESH_QA_TEMP>/transport
```

Equivalent authenticated GitHub API retrieval is acceptable. Do not ask the owner to download/re-upload the artifact.

Immediately after acquisition:

1. require both published files above;
2. compute the inner ZIP SHA-256 and require exactly `ac8efc444578e9d3f31ac0325baca4b286fd608bc511850f480e0d397936620b`;
3. require exactly `406656` bytes;
4. parse the manifest;
5. require manifest `source_commit = 841a1e2c1a503c4a05572a957ba97c55b9b60c52`;
6. require manifest `product_tree = edf1c2d3494ebbc53ae778d23be1457eb885b605`;
7. require manifest `preflight_run_id = 33037727189`;
8. require manifest artifact SHA/bytes/files to match the values above;
9. require ZIP integrity PASS;
10. fresh-extract and verify exact 39-path set and every per-file SHA/byte count against the manifest.

Do not rebuild a substitute ZIP. A deterministic rebuild may be used as additional evidence only; the transported `ac8efc44...` ZIP is the package under test.

Any mismatch is `FAIL_ARTIFACT`. Do not start product PASS credit on mismatched bytes.

Known ChatGPT/GitHub pre-consumer proof exists:

```text
pre-freeze complete QA run: 33037727189 — PASS
freeze run: 33037955943 — PASS
frozen-artifact pre-Codex run: 33038048376 — PASS
```

Codex must still independently consume and verify the artifact itself.

## 4. Immutable QA harness authority

Use a clean QA workspace containing the current Phase 5 harnesses from:

```text
qa branch:
qa/phase5-direct-frozen-r2-gate-2026-08-27

pre-Codex frozen-gate execution base commit:
10036f4b8de99b03ea7719ffe0ef10673e79631d
```

The later checkpoint documentation commit is not a product or harness mutation.

Required QA files include:

```text
extension/tests/credential_runtime_concurrency.test.mjs
extension/tests/qa_phase5_codex/direct_addendum_coverage.test.mjs
extension/tests/qa_browser/direct_popup_d18.mjs
extension/tests/qa_browser/direct_manual_worker_lifecycle.mjs
extension/tests/qa_browser/direct_codex_gate_addendum_v2.mjs
extension/tests/qa_browser/phase2-stage4/browser_phase2_stage4_compat_gate.mjs
```

Do not edit them during the campaign.

The pre-Codex frozen gate used these harnesses against the exact extracted frozen bytes and finished with `PRODUCT_BYTES_POST_TEST=IDENTICAL`; this is venue proof, not transferable PASS credit.

## 5. Source and packaged Node/static coverage

Use one clean source workspace at exact source commit:

```text
841a1e2c1a503c4a05572a957ba97c55b9b60c52
```

Run the complete normal Node regression suite and the permanent credential-concurrency regression. Run the Phase 5 Direct addendum coverage unchanged.

At minimum independently prove the three concurrency assertions:

```text
stale migration cannot erase a concurrent Direct credential save
concurrent Direct and Metrika saves preserve both independent records
backup runtime participates in the same credential mutation lock
```

Then execute the same applicable Node/static tests against a fresh extraction of the exact transported ZIP. Use only a temporary QA execution layout when repository-relative test imports require it. Do not mutate the package or source authority.

Verify source/package syntax, JSON and manifest/entrypoint integrity. Report actual test/syntax/JSON counts rather than inventing historical denominators.

## 6. Execute the complete Direct D-00..D-22 matrix

Execute every section from:

```text
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_DIRECT_PHASE5_ADDENDUM.md
```

Required result in a PASS campaign:

```text
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
```

No enabled Direct section may be `NOT_RUN` in PASS.

## 7. Installed-extension Direct browser gates

Use a qualified isolated headful Chrome/Puppeteer environment and the exact extracted `ac8efc44...` product as the installed extension.

Run unchanged:

```text
extension/tests/qa_browser/direct_popup_d18.mjs
extension/tests/qa_browser/direct_manual_worker_lifecycle.mjs
extension/tests/qa_browser/direct_codex_gate_addendum_v2.mjs
```

Required Direct markers include:

```text
D18_POPUP_430X560_PASS
D18_TOP_BOTTOM_COMMON_SAVE_EQUIVALENT_PASS
PHASE5_DIRECT_POPUP_D18_PASS

D17_DIRECT_MANUAL_LIST_AUTOSEND_FALSE_PASS
D17_DIRECT_MANUAL_REPORT_AUTOSEND_TRUE_PASS
D17_DIRECT_REMOUNT_NO_REPLAY_PASS
D17_DIRECT_NO_DUPLICATE_PROVIDER_PASS
PHASE5_DIRECT_MANUAL_LIFECYCLE_PASS

D19_FIVE_SERVICE_BACKUP_UI_MAPPING_PASS
D17_MANUAL_BUSY_FENCE_SINGLE_PROVIDER_PASS
D16_NON_DIRECT_ACTIVE_DIRECT_PREFIX_ZERO_TRAFFIC_PASS
D20_DIRECT_AUTORUN_DEFAULT_DISABLED_LOCAL_PASS
D16_DIRECT_ACTIVE_OTHER_PREFIXES_ZERO_TRAFFIC_PASS
D20_DIRECT_AUTORUN_ONE_FINGERPRINT_ONE_PROVIDER_ONE_DELIVERY_PASS
D20_DIRECT_AUTORUN_PAUSE_RESUME_FINISH_PASS
DIRECT_REAL_YANDEX_REQUESTS=0
PHASE5_DIRECT_CODEX_BROWSER_ADDENDUM_PASS
```

Controlled Direct provider requests are local stub requests only. No real Direct endpoint traffic is allowed.

## 8. Prior-phase compatibility remains mandatory

Phase 5 must not silently regress accepted Wordstat/Search/Webmaster/Metrika behavior.

Run the current popup-independent compatibility venue unchanged:

```text
extension/tests/qa_browser/phase2-stage4/browser_phase2_stage4_compat_gate.mjs
```

Required markers:

```text
B01_PROJECT_WORK_IDENTITY_PASS
B01_BINDING_PASS
B02_MANUAL_RESYNC_SINGLE_ACTION_PASS
B02_MANUAL_REMOUNT_NO_REPLAY_PASS
B02_MANUAL_ON_OFF_TRANSACTION_PASS
B03_NON_OWNER_CONTROL_FENCE_PASS
B03_SEARCH_AUTORUN_PASS
BROWSER_CONTROLLED_SEARCH_STUB_REQUESTS=1
BROWSER_GATE_REAL_YANDEX_REQUESTS=0
PHASE2_STAGE4_COMPAT_BROWSER_GATE_PASS
```

Also retain every still-applicable permanent/core/Phase-1/2/3/4 Node/integration requirement from the living main gate and addenda. A current compatibility venue may replace stale UI mechanics, but it may not weaken the governed behavioral assertions.

## 9. Direct safety boundaries that must remain explicit

Require independently:

```text
Direct credential = dedicated Direct record only
optional Client-Login = Direct record only
Direct Check = exactly one controlled Campaigns.get request
Direct JSON reads = exactly one provider request per admitted command
Reports = online only
HTTP 201/202 report outcomes = terminal first-slice result, no polling
unknown POST outcome = UNKNOWN / automatic_retry=false / no replay
Units and RequestId = truthful provider metadata only
Direct Units != RUB
write/bid/finance/offline/future surfaces = local zero-provider rejection
production Direct Autorun default = OFF
controlled QA enablement = one fingerprint / one provider request / one delivery
```

No mutation, bidding, payment, finance, offline-report or arbitrary provider request surface is permitted.

## 10. Immutability and cleanliness audit

Before final verdict, prove:

```text
exact_artifact_modified = NO
production_modified_during_gate = NO
package_tests_modified_during_gate = NO
direct_harness_modified_during_gate = NO
compatibility_harness_modified_during_gate = NO
real_credentials_used = NO
real_yandex_direct_requests = 0
real_yandex_requests = 0
source_workspace_clean = PASS
transport_workspace_clean = PASS
browser_harness_workspaces_clean = PASS
enabled_not_run_sections = 0
NOT_RUN_COUNT = 0
PRODUCT_BYTES_POST_TEST = IDENTICAL
```

Re-hash the authoritative inner ZIP at the end and require the same `ac8efc444578e9d3f31ac0325baca4b286fd608bc511850f480e0d397936620b / 406656` identity.

## 11. Required final response

Return one complete report headed exactly:

```text
CODEX_YANDEX_PRE_DELIVERY_FULL_REGRESSION_GATE_RESULT
```

At minimum include:

```text
campaign: PHASE5_DIRECT_R2_COMPLETE_APPLICABLE_GATE
live_main_head: <actual SHA observed at campaign start>
step_0_authority: PASS|FAIL

candidate_source: 841a1e2c1a503c4a05572a957ba97c55b9b60c52
candidate_branch: candidate/phase5-direct-first-slice-r2-2026-08-27
candidate_freeze_trigger: 389084290635fbf2ac305098adc3aae17f967c83
product_tree: edf1c2d3494ebbc53ae778d23be1457eb885b605

freeze_run: 33037955943
artifact_id: 9632728199
artifact_name: phase5-direct-r2-frozen-candidate-841a1e2
artifact: yandex-marketing-bridge-0.1.1-phase5-direct-first-slice-r2-candidate.zip
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

browser_direct_popup_d18: PASS|FAIL|NOT_RUN
browser_direct_manual_lifecycle: PASS|FAIL|NOT_RUN
browser_direct_addendum: PASS|FAIL|NOT_RUN
browser_prior_phase_compatibility: PASS|FAIL|NOT_RUN

D-00: PASS|FAIL|NOT_RUN
D-01: PASS|FAIL|NOT_RUN
D-02: PASS|FAIL|NOT_RUN
D-03: PASS|FAIL|NOT_RUN
D-04: PASS|FAIL|NOT_RUN
D-05: PASS|FAIL|NOT_RUN
D-06: PASS|FAIL|NOT_RUN
D-07: PASS|FAIL|NOT_RUN
D-08: PASS|FAIL|NOT_RUN
D-09: PASS|FAIL|NOT_RUN
D-10: PASS|FAIL|NOT_RUN
D-11: PASS|FAIL|NOT_RUN
D-12: PASS|FAIL|NOT_RUN
D-13: PASS|FAIL|NOT_RUN
D-14: PASS|FAIL|NOT_RUN
D-15: PASS|FAIL|NOT_RUN
D-16: PASS|FAIL|NOT_RUN
D-17: PASS|FAIL|NOT_RUN
D-18: PASS|FAIL|NOT_RUN
D-19: PASS|FAIL|NOT_RUN
D-20: PASS|FAIL|NOT_RUN
D-21: PASS|FAIL|NOT_RUN
D-22: PASS|FAIL|NOT_RUN

direct_controlled_provider_requests: <actual integer>
controlled_search_stub_requests: <actual integer>
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
PRODUCT_BYTES_POST_TEST: IDENTICAL|CHANGED
failures: [] | <complete classified list>
verdict: PASS|FAIL_PRODUCT|FAIL_ARTIFACT|FAIL_HARNESS
```

A final `PASS` is valid only if all enabled sections passed, the exact artifact remained immutable, no real credentials or real Yandex traffic were used, and all governed workspaces are clean.

## 12. Owner-live remains blocked

Do not authorize owner-live from this handoff alone.

Only after ChatGPT receives and records a genuine independent Codex `PASS` for this exact campaign may owner-live begin.

The later owner-live is intentionally narrow and uses the exact same frozen `ac8efc44...` package. It may perform one real Direct Check, one `listCampaigns` and at most the bounded reads explicitly allowed by the Phase 5 Direct addendum. It must not exercise mutations, bidding, finance, quota/error experiments, offline reports or automatic replay.
