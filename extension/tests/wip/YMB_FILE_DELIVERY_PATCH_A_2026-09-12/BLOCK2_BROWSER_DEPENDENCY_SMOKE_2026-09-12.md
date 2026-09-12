# YMB Patch A — browser dependency smoke block 2

Date: 2026-09-12
Branch: `wip/ymb-file-delivery-patch-a-2026-09-12`
Candidate: exact candidate2; production bytes unchanged in this block.
Browser: Chromium/Chrome 144 controlled QA profile.
Real provider traffic: 0.

## Harness correction before rerun

The first browser-smoke attempt referenced the file-delivery global used by an older integrated candidate (`YMBFileDeliveryWorker`) instead of Patch A candidate2 (`YMBFileDeliveryWorkerTransport` + `YMBFileArtifactStore`). The product loaded; the assertion expression itself threw before evaluating the product.

Classification:

```text
FAIL_HARNESS = YES
FAIL_PRODUCT = NO
PRODUCTION_MODIFICATIONS = 0
```

Only the temporary QA script was corrected and the browser smoke was rerun from the beginning.

## Final rerun

```text
worker_globals_and_load_order = PASS
ordinary_protocol_contracts = PASS
search_batch_local_no_provider = PASS
wordstat_batch_local_no_provider = PASS
popup_load = PASS
content_runtime_load = PASS
BLOCK2_BROWSER_DEPENDENCY_SMOKE = PASS
```

Verified worker/runtime surfaces:

- product version remained 0.1.4;
- Wordstat/Search/Webmaster/Metrika/Direct protocols all loaded;
- Wordstat batch runtime loaded;
- Search batch runtime loaded;
- Phase-5 provider runtime loaded;
- Patch-A file-delivery runtime loaded;
- original Manual and Autorun handlers remained functions;
- file DB is `ymb_delivery_artifacts_v2`;
- ordinary Search request builder still points to `/v2/web/search`;
- Search Batch local start/status/cancel stayed provider-free;
- Wordstat Batch local start/status/cancel stayed provider-free;
- popup loaded and completed;
- ChatGPT content runtime loaded its extension surface and composer binding;
- managed Chromium policy bytes were restored exactly after the test.

## Release status

```text
BLOCK2 = PASS
PRODUCTION_BYTES_CHANGED_IN_BLOCK = NO
RELEASE_ALLOWED = NO
```

Recovery, owner-isolation and remaining dependency regressions are still required.
