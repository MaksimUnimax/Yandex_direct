# B21 — Stage B automated qualification checkpoint — 2026-09-13

## Scope

This checkpoint records the completed automated qualification for the async deferred-Search popup Stage B candidate. It does **not** declare owner live acceptance.

Repository: `MaksimUnimax/Yandex_direct`

Product branch: `wip/ymb-async-popup-stage-b-2026-09-13`

Product commit: `404dd03874e5df80a95bc6cec1e6967bb71de405`

Accepted Stage-A baseline: `341c847089e1207dd23bf876f5ba3ac537b65a10`

Git tree at the product commit: `b48506becafa40bbad40605072ec9e640610edd2`

Canonical `extension/src` content-tree SHA-256 used by qualification: `bec51a30456cce132d2bc028b42b495097989fb6eecd8cd3d1ea6003b3d2b5ed`

Extension files: `68`

Qualified deterministic install ZIP:

- filename: `Yandex-Marketing-Bridge-0.1.6-stage-b.zip`
- SHA-256: `51491db92e1ea7c8e3c9555e95ba236cada5a4890b66e6c6134779550856c036`
- bytes: `232591`

## Production allowlist

Final production diff from accepted Stage A is exactly:

1. `extension/src/content_script.js`
2. `extension/src/popup_search_async_monitor.js`

No Stage-B production changes were made to manifest, async runtime, async provider transport, Search admission, file delivery, composer Send, attachment machinery, or credential handling.

## Stage-B-specific contract gate

Workflow: `YMB async popup Stage B contract`

Run: `34760385051`

Result: `SUCCESS`

Artifact: `ymb-stage-b-contract-package` / artifact id `10318533386`

Artifact digest: `sha256:dba7e537f082493daf143030f393f9a89c40f22f241998751166812786cd67bd`

Independent artifact readback confirmed the digest and the inner install ZIP identity.

Contract cases passed:

- popup metrics: 0/100, 37/100, 35+2, SUCCEEDED with zero SERP rows, 100%, UNKNOWN non-terminal;
- future due disabled/countdown, due-now enabled, complete export enabled, no-job state;
- structured popup messages only;
- wrong ChatGPT conversation => zero Manual execute;
- Manual OFF => zero Manual execute;
- Search not active => zero Manual execute;
- Autorun not paused => zero Manual execute;
- collect => exactly one existing `WS_EXECUTE_MANUAL_BLOCK` carrying `collectN` with `count:1`;
- export => existing `exportPage` Manual block;
- unsupported action => zero Manual execute;
- concurrent double-click => at most one Manual execute;
- malformed job id rejected;
- no direct provider primitive in the Stage-B content ingress.

## Exact-package real-Chrome gate

Workflow: `YMB async popup Stage B final qualification v2`

Run: `34760748405`

Exact-package browser job result: `SUCCESS`

Artifact: `ymb-stage-b-final-qualified-v2` / artifact id `10319150938`

Artifact digest: `sha256:88f147cbef3a211c1012ba527f9701e66a2b46a9695d913bcc3c90ae79a3ffbb`

Independent downloaded-artifact readback confirmed:

- product commit `404dd03874e5df80a95bc6cec1e6967bb71de405`;
- content tree `bec51a30456cce132d2bc028b42b495097989fb6eecd8cd3d1ea6003b3d2b5ed`;
- 68 files;
- install ZIP SHA-256 `51491db92e1ea7c8e3c9555e95ba236cada5a4890b66e6c6134779550856c036`;
- deterministic dual-build identity = PASS;
- fresh-extraction identity = PASS;
- targeted TEST-15 = PASS;
- real-Chrome popup qualification = PASS;
- B19 resource matrix = **16/16 PASS**;
- B19 deferred-network matrix = **9/9 PASS**;
- browser failures = `[]`;
- owned-browser remaining processes = `[]`;
- real provider calls during qualification = `0`;
- aggregate `FINAL_GATE.json` = `pass:true`.

### Resource matrix readback

All 16 rows are PASS, including exact candidate identity, real content/clipboard path, large file-delivery cases, occupied composer preservation, worker termination/recovery, real-IDB lifecycle cases and owned-browser cleanup.

### Deferred-network matrix readback

All 9 rows are PASS, including:

- exact 0.1.6 install identity;
- Manual start with zero network;
- one controlled Search Async POST;
- one controlled Operation GET + normalization;
- command injection cannot override provider origin/credential;
- Manual disabled blocks before network;
- UNKNOWN submit never automatically retries;
- campaign identity;
- owned-browser cleanup.

### Targeted TEST-15 readback

`provider_calls=0`, `failures=0`, all required scenarios PASS:

- `test15_blank_composer_auto_send_exactly_once`;
- `occupied_user_draft_is_preserved`;
- `same_delivery_inline_report_auto_sends_exactly_once`;
- `different_bridge_inline_text_is_preserved`.

## Node regression / baseline differential

Workflow: `YMB async popup Stage B Node differential v3`

Run: `34760926507`

Result: `SUCCESS`

Artifact: `ymb-stage-b-node-differential-v3` / artifact id `10318703602`

Artifact digest: `sha256:227d46587251af9aa5c74f938b524efc4a859196c7d67c51f0f037eeaf59ad91`

Independent artifact readback confirmed:

- accepted Stage A and Stage B were run through the same frozen B19 campaign with exact product overrides;
- `suite_delta = {}`;
- `static_equal_and_pass = true`;
- Stage-B-specific contract = PASS;
- real provider calls = `0`;
- aggregate differential result = `pass:true`.

Four legacy suites are fully green on both Stage A and Stage B:

- ORIGINAL: 132/132;
- MISSING: 78/78;
- MODULE: 254/254;
- EXPORT: 84/84.

The frozen pre-file-delivery harness retains the same already-known stale failures on both accepted Stage A and Stage B:

- FULL: 98/99 on both;
- DELIVERY: 56/69 on both.

These are not new Stage-B regressions: the failed test names and counts are byte-for-byte equivalent in the baseline differential, while the currently governing patched file-delivery behavior is separately qualified by the exact-package TEST-15/resource/network gates above.

## Preserved RED history

No RED was overwritten or re-labelled as product failure/pass.

- Initial Stage-B qualification run `34759745606`: QA-harness adaptation errors before product assertions (`$GITHUB_ENV` same-step use and wrong downloaded artifact path).
- Final qualification v1 run `34760601373`: TEST-15 and popup already PASS; B19 resource stopped on the frozen 67-file identity guard; Node exposed stale pre-file-delivery expectations.
- Final qualification v2 Node job: QA differential incorrectly pointed the canonical runner at current `repo/extension/src` for the Stage-A side and therefore did not create Stage-A `RESULT.json`. Corrected in Node differential v3 with an explicit product override.

These REDs are retained as audit evidence and do not alter the accepted product bytes.

## Current gate state

```text
STAGE_A = PASS
STAGE_B_IMPLEMENTATION = COMPLETE
STAGE_B_ARCHITECTURE_ALLOWLIST = PASS
STAGE_B_CONTRACT = PASS
STAGE_B_NODE_DIFFERENTIAL = PASS
STAGE_B_DETERMINISTIC_PACKAGE = PASS
STAGE_B_FRESH_EXTRACTION = PASS
STAGE_B_REAL_CHROME_POPUP = PASS
STAGE_B_RESOURCE_MATRIX = 16/16 PASS
STAGE_B_NETWORK_MATRIX = 9/9 PASS
STAGE_B_TARGETED_TEST15 = PASS
STAGE_B_ARTIFACT_READBACK = PASS
REAL_PROVIDER_CALLS_DURING_AUTOMATED_QUALIFICATION = 0
UNAUTHORIZED_PRODUCTION_CHANGES = 0
OWNER_LIVE_SMOKE = PENDING
STAGE_B_FINAL_OWNER_ACCEPTANCE = PENDING
```

Do **not** label Stage B fully accepted until the exact qualified ZIP above is installed in the owner's real Chrome profile and the owner live smoke passes.
