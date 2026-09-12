# YMB Deferred Search Patch B — durable checkpoint after Block 1

Date: 2026-09-12
Status: **WIP / BLOCK1 PASS / NOT RELEASED / DO NOT RESTART FROM SCRATCH**

## Exact baseline

Owner-provided archive: `yandex-marketing-bridge-0.1.4-webmaster-readiness-gzip(2).zip`

SHA-256: `b812c4c54d1054d63a24ea852e1721e813d133172487c9872bac347998e3e53f`

Patch B is built independently from the exact owner 0.1.4 baseline. Withdrawn 0.1.5 is not a baseline.

## Scope

Patch B candidate1 contains deferred ordinary Yandex Search core only. It deliberately does not include Patch A file delivery or export-to-file integration. That integration is deferred until Patch B is independently accepted.

Changed production paths: exactly 8:

1. `manifest.json`
2. `phase3_service_worker_bootstrap.js`
3. `search_async_worker_transport.js` — new
4. `shared/search_async_content_bridge.js` — new
5. `shared/search_async_protocol.js` — new
6. `shared/search_async_runtime.js` — new
7. `shared/search_async_store.js` — new
8. `shared/search_async_transport.js` — new

Core architecture:

- separate `SEARCH_ASYNC_BATCH_API_V1` orchestration protocol belonging to service `search`;
- submit endpoint `/v2/web/searchAsync`;
- operation collection endpoint fixed to `https://operation.api.cloud.yandex.net/operations/<operation_id>`;
- IndexedDB database `ymb_search_async_v2` with separate `jobs`, `items`, `results` stores;
- no giant mutable `items[]` inside the job record;
- operation IDs are durably persisted per item;
- stale `SUBMITTING` recovery becomes `OUTCOME_UNKNOWN` and cannot blind-resubmit;
- accepted operations remain collectable after local cancel;
- standalone Patch B is Manual-only; Autorun deferred provider execution is explicitly rejected locally;
- existing sync `SEARCH_API_V1` and `SEARCH_BATCH_API_V1` remain separate;
- standalone Patch B does not expose `export`; file export is an A+B integration concern.

## Block 1 executed evidence

All tests used synthetic provider adapters; real Yandex requests = 0.

```text
protocol_1500_limit = PASS
1501_rejected = PASS
dedup = PASS
result_envelope_does_not_echo_full_commands = PASS
operation_url_fixed_and_encoded = PASS
operation_parser_strict = PASS
bounded_job_record = PASS
operation_id_persistence = PASS
unknown_submit_outcome_blocks_replay = PASS
pre-provider_failure_rolls_back_reservation = PASS
stale_SUBMITTING_recovery_to_OUTCOME_UNKNOWN = PASS
collectN_one_GET_per_waiting_item_per_command = PASS
valid_XML_normalization = PASS
malformed_XML_fail_closed = PASS
pause_no_provider_submit = PASS
cancel_local_only_waiting_operation_still_collectable = PASS
expired_operation_terminal_no_resubmit = PASS
async_marker_coexists_with_ordinary_Search_and_Search Batch = PASS
standalone_export_not_exposed = PASS
```

Node test result: `14/14 PASS`.

Production syntax/JSON checks also passed before this block.

## Release state

```text
PATCH_B_BLOCK1 = PASS
PATCH_B_SCALE_10_100_500_1500 = NOT_RUN_ON_CANDIDATE1_YET
PATCH_B_REAL_INDEXEDDB_BROWSER_SCALE = NOT_RUN_ON_CANDIDATE1_YET
PATCH_B_BROWSER_DEPENDENCY_REGRESSION = NOT_RUN
PATCH_B_PROVIDER_AUTH_CANARY = NOT_RUN_LIVE
PATCH_B_ACCEPTED_FOR_INTEGRATION = NO
INTEGRATED_A_PLUS_B = NOT_RUN
RELEASE_ALLOWED = NO
OWNER_HANDOFF = FORBIDDEN
```

## Exact continuation point

Do not recreate Patch B candidate1. Reconstruct it from the exact 0.1.4 baseline plus the exact postimage/diff/hash evidence stored beside this checkpoint, verify hashes, then continue with the mandatory `10 / 100 / 500 / 1500` scale matrix and recovery/cost/provider-boundary blocks.
