# Patch B — B7: Manual deferred Search ingress and worker binding

Date: 2026-09-12.
Status: **CODE + TESTS + EVIDENCE PERSISTED / NOT BROWSER ACCEPTED / NOT RELEASED**.

## Continuity

B7 continues from the saved B6 trusted worker/owner binding and B5 shared admission. Patch A and A/B1-B6 snapshots were not rebuilt. The owner baseline remains `yandex-marketing-bridge-0.1.4-webmaster-readiness-gzip(2).zip`, SHA-256 `b812c4c54d1054d63a24ea852e1721e813d133172487c9872bac347998e3e53f`.

## Implemented B7 behavior

- Separate `SEARCH_ASYNC_BATCH_API_V1` ingress for Manual ChatGPT use.
- No deferred Autorun in this stage.
- No background timers, `chrome.alarms`, intervals or hidden polling scheduler.
- Deferred commands require the trusted B6 shared-admission binding.
- Manual preflight checks bound conversation/tab, Manual enabled, active Search service, paused-or-terminal Autorun state, no other active Manual operation and no pending outbox.
- `start`, `status`, `itemsPage`, `pause`, `resume`, `cancelPending` remain local and perform no provider request.
- `submitN` / `collectN` are bounded explicit actions only.
- Raw provider result arrays/query list are not returned in the compact command report.
- UNKNOWN network outcome stops the same command and does not replay another request.
- Local recovery is performed before an explicit provider step.
- Binding accepts the durable `search_async_requesting` Manual status rather than authority claimed in chat metadata.
- Bootstrap imports deferred modules only after shared Search admission is loaded.
- At this exact B7 checkpoint, `https://operation.api.cloud.yandex.net/*` host permission is deliberately still absent; therefore provider-enabled deferred transport is not accepted as an installable capability yet. Existing Search API host permission remains unchanged.

## Persisted exact code/evidence

Production-candidate WIP bytes and deltas:

- `candidate/b7/search_async_worker_transport.js` — SHA-256 `71a3e7e6d424f197cb3d3c39fff74df024e941858ea791e163245f1535e3080f`.
- `candidate/b7/search_admission_worker_binding.js` — `5f9468110c4ed7d51d3d8c1cd7c306549dd2428a49efc9892c9d4a7b70b49bba`.
- `candidate/b7/phase3_service_worker_bootstrap.js` — `40565b792b9210b5b97795bb7b9c71577a5008bb312077e06a4a54b349dd9c88`.
- `evidence/B7_BINDING_DELTA.diff` — `73659d4fffa407ec3deedde7c61179198ccbfbd416ab65203243616cfaf998ea`.
- `evidence/B7_BOOTSTRAP_DELTA.diff` — `3e2fb262843be9de218c05be3c02e4ed1611506f0d9a0665c5d9a37da0cc8618`.

Persisted executable QA:

- `qa/b7_worker.test.mjs` — `3d0249cd36b45e038c8127bab4e192aae227449d757e38416dbef3efa8430b3c`.
- `qa/b7_bootstrap.test.mjs` — `d9f7fb301d0fcbf29fedab1fca870844c2ccd4a2596352f5ed46c968d995c773`.
- `qa/b6_binding_regression.test.mjs` — `de7ddd10cf4420e2a5a7755803a5082fc46be3809d8c2a52476fa232254e9808`.
- `qa/block_command_discovery.js` — `179700660b5960adf5bdd352104673166ce7fdc2e0a11ecf78222495642a82d1`.
- Final TAP is persisted as `evidence/B7_ALL_GREEN.tap`.
- Structured evidence is persisted as `evidence/B7_TEST_RESULTS.json`.

## RED -> GREEN

Initial B7 run: 44 tests, 37 PASS / 7 FAIL.

Actual new product defect found before release: public `submitN` and `collectN` commands were rejected by the internal B7 action allowlist, so the explicit deferred provider path could not execute. Six downstream failing checks depended on this same blocked action path. One dependency-error assertion was also strengthened in the QA layer.

After correcting the product action handling, the same B7 set passed 44/44.

Then the B6 trusted-binding regression was added back to the combined campaign. Final result:

```text
B6_TRUSTED_BINDING_REGRESSION = 18 PASS
B7_BOOTSTRAP_PERMISSION = 4 PASS
B7_MANUAL_WORKER = 26 PASS
TOTAL = 48 PASS / 0 FAIL / 0 SKIPPED
```

Final TAP SHA-256: `0ece9b180ccd3e15cdb1df107a2ce7797c5f2a19291a4e59a6eb68428b912f46`.

## What this does NOT prove

This is Node/source-layer evidence. It does not establish:

- installed Chrome/MV3 behavior of the B7 bytes;
- actual IndexedDB durability/restart behavior;
- Chrome memory/resource safety of B7/B1-B7 combined;
- real provider authentication/Operation GET compatibility of the owner's key;
- actual operation-host permission path, because permission is intentionally not enabled in B7;
- final Patch A file export composition;
- full existing-extension regression after an installable A+B composition;
- final package identity.

No provider requests were made by this B7 validation.

## Release verdict

```text
B7_NODE_CONTRACTS = PASS_FOR_RECORDED_CASES
B7_BROWSER = NOT_RUN
B7_REAL_INDEXEDDB = NOT_RUN
B7_OPERATION_HOST_CAPABILITY = DISABLED_FAIL_CLOSED
COMBINED_A_PLUS_B_RESOURCE_GATE = NOT_RUN
FINAL_PRE_DELIVERY_GATE = NOT_RUN
RELEASE_ALLOWED = NO
OWNER_HANDOFF = FORBIDDEN
```

## Exact continuation point

Do not restart Patch A or B1-B7.

Next work is limited to what can be verified in the current environment:

1. compose bounded Search result export through the preserved Patch A artifact/file-delivery path without rebuilding that path;
2. preserve Manual ownership and compact-response boundaries;
3. build the exact A+B candidate tree only after all source dependencies are enumerated;
4. run all non-browser dependency regressions and package/static checks that are possible here;
5. leave real Chrome/IndexedDB/resource checks explicitly BLOCKED/NOT_RUN until a qualified environment is available;
6. do not add the operation host permission or claim provider capability as accepted merely to make a synthetic test pass.

RELEASE_ALLOWED remains NO until mandatory release-blocking evidence is complete.
