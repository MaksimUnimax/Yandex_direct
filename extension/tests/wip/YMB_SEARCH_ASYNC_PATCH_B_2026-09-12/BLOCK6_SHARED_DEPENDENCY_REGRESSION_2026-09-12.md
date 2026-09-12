# YMB Deferred Search Patch B — shared dependency regression block 6

Date: 2026-09-12
Branch: `wip/ymb-search-async-patch-b-2026-09-12`
Candidate: exact Patch B candidate1; production bytes unchanged.
Browser: Chrome/Chromium 144.0.7559.96 controlled QA profile.
Real provider traffic: 0 (all provider boundaries in this block were controlled/stubbed).

## Harness incident

The first attempt tried to read extension content-script globals from the page main world. Chrome content scripts run in the extension isolated world, so the harness hit `ReferenceError: SearchProtocol is not defined` before the content product assertion.

Classification:

```text
FAIL_HARNESS = YES
FAIL_PRODUCT = NO
PRODUCTION_MODIFICATIONS = 0
```

Only QA was corrected: the content assertion now executes through `chrome.scripting.executeScript(..., world: "ISOLATED")`. The full block was rerun from the beginning.

## Final rerun

All required assertions passed:

```text
worker_load = PASS
content_recognition = PASS
ordinary_search_manual_delegation = PASS
search_batch_manual_delegation = PASS
wordstat_batch_manual_delegation = PASS
async_wrong_service_local_block = PASS
async_manual_disabled_local_block = PASS
backup_import_async_db_isolation = PASS
non_async_autorun_delegation = PASS
popup_load = PASS
BLOCK6 = PASS
```

### Worker/load-order

Loaded successfully on the same MV3 worker:

- Wordstat protocol/batch;
- ordinary Search;
- Search Batch;
- Deferred Search Patch B;
- Webmaster;
- Metrika;
- Direct;
- Phase-5 runtime;
- existing Manual and Autorun handler chain.

### Content routing

The ChatGPT isolated content world recognized all of:

- `SEARCH_API_V1`;
- `SEARCH_BATCH_API_V1`;
- `SEARCH_ASYNC_BATCH_API_V1`;
- `WORDSTAT_API_V1`.

The existing composer and extension surface loaded normally.

### Manual wrapper-chain regression

A real synthetic bound ChatGPT tab was used.

Ordinary Search passed through the new outer async wrapper to the existing ordinary manual handler and executed exactly one stubbed sync Search call:

`https://searchapi.api.cloud.yandex.net/v2/web/search`

Search Batch `start` passed through the async wrapper to the existing Search-Batch handler and remained provider-free.

Wordstat Batch `start` passed through the async wrapper and Search-Batch wrapper to the existing Wordstat-Batch handler and remained provider-free.

### Async local fences

- active service != Search -> `SERVICE_NOT_ACTIVE`, zero fetch;
- Manual disabled -> `MANUAL_MODE_DISABLED`, zero fetch;
- non-async Autorun command delegated to the pre-existing Autorun handler (`AUTO_RUN_NOT_FOUND` in the controlled fixture), not to the async Manual-only rejection path.

### Backup/import isolation

A real pending async job was created in `ymb_search_async_v2`, then the existing settings backup/export+import path ran.

- settings backup did not include async job data/DB marker;
- settings import completed;
- pending async job remained durably present after import.

### Browser cleanup

Managed Chromium policy was restored exactly after the rerun:

`3b740260e337305aaef268e6c63af8fa2796057ce46f43df5ae5a3949e085e86`

## Verdict

```text
PATCH_B_SHARED_DEPENDENCIES = PASS
WRAPPER_CHAIN_REGRESSION = PASS
BACKUP_IMPORT_ISOLATION = PASS
PRODUCTION_BYTES_CHANGED = NO
PATCH_B_ACCEPTED_FOR_INTEGRATION = NOT_YET
RELEASE_ALLOWED = NO
```

Exact-candidate identity/static gate and durable WIP postimage repair remain before Patch-B acceptance-for-integration.
