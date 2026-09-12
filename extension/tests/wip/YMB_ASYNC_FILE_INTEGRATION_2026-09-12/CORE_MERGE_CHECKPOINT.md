# YMB accepted Patch A + Patch B — core merge checkpoint

Date: 2026-09-12
Branch: `wip/ymb-async-file-integration-2026-09-12`
Status: **WIP CORE MERGE / NOT RELEASED / CONTINUE FROM THIS MERGE**

## Accepted component authorities

Patch A file delivery acceptance-for-integration:

- branch: `wip/ymb-file-delivery-patch-a-2026-09-12`
- acceptance commit: `af421242389206acc4ffa64a37d17577070efbf9`

Patch B deferred Search acceptance-for-integration:

- branch: `wip/ymb-search-async-patch-b-2026-09-12`
- acceptance commit: `fa82e693d3f7bc2c94fb1bdc6539781f592b0ae7`

Exact owner baseline remains:

`yandex-marketing-bridge-0.1.4-webmaster-readiness-gzip(2).zip`

SHA-256:

`b812c4c54d1054d63a24ea852e1721e813d133172487c9872bac347998e3e53f`

## Local integrated candidate

`/mnt/data/ymb_integrated_candidate1`

The candidate was rebuilt from the exact 0.1.4 baseline, then accepted A/B non-conflicting postimages were overlaid. The two shared integration files were merged explicitly rather than taking one side wholesale:

- `manifest.json`
- `phase3_service_worker_bootstrap.js`

Core-merge identities:

```text
production_files = 63
javascript_files = 57
manifest_sha256 = 98af922638d59479b5bacf738f41905ba4656cd88d6520a3ab3ad4b1891c3d8a
phase3_bootstrap_sha256 = 10086f8512845bdf49d7e13d76a84451d5b990177f80a95220cc38298d228db4
JS_SYNTAX = PASS
MANIFEST_JSON_PARSE = PASS
PACKAGE_JSON_PARSE = PASS
```

## Merge rules

`manifest.json` contains the union of accepted A+B requirements while preserving baseline order/semantics:

- baseline host permissions retained;
- Patch-B operation host added: `https://operation.api.cloud.yandex.net/*`;
- Search Batch content bridge remains in place;
- Patch-B async protocol/transport/content bridge load after Search Batch bridge;
- Patch-A ChatGPT file-attachment helper loads after composer helper;
- baseline `content_script.js` replacement from accepted Patch A is used;
- Patch-A `file_delivery_content.js` loads after `content_script.js`.

`phase3_service_worker_bootstrap.js` keeps the accepted baseline/Wordstat/Search-Batch/phase-runtime chain and appends both bounded module groups:

1. Patch-B Search Async protocol/store/runtime/transport/worker transport;
2. Patch-A file artifact store/file-delivery worker transport.

No service provider implementation from the baseline was replaced.

## Current boundary

This checkpoint is **only the accepted A+B core merge**. Large async-result export has not yet been integrated.

Next material block must reuse Patch A's accepted binary artifact pipeline for async-result export. It must not create a second Base64/chrome.storage file transport.

After export integration, every dependency affected by the integration must be retested, including both accepted A/B matrices and the final browser/resource gates.

```text
A_ACCEPTED_FOR_INTEGRATION = YES
B_ACCEPTED_FOR_INTEGRATION = YES
A_PLUS_B_CORE_MERGE_SYNTAX = PASS
ASYNC_EXPORT_INTEGRATION = NOT_STARTED
FINAL_CROSS_LAYER_REGRESSION = NOT_RUN
FINAL_PRE_DELIVERY_GATE = NOT_RUN
FRESH_FINAL_PACKAGE = NOT_BUILT
RELEASE_ALLOWED = NO
OWNER_HANDOFF = FORBIDDEN
```
