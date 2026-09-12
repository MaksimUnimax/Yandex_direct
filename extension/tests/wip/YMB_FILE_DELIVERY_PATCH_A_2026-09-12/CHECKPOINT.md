# YMB file-delivery Patch A — durable WIP checkpoint

Date: 2026-09-12
Status: **WIP SNAPSHOT / NOT RELEASED / DO NOT RESTART FROM SCRATCH**

## Exact baseline

Owner-provided baseline archive:

`yandex-marketing-bridge-0.1.4-webmaster-readiness-gzip(2).zip`

Exact baseline ZIP SHA-256 is stored in `BASELINE_ZIP_SHA256.txt` and the full extracted-tree SHA manifest is stored in `BASELINE_TREE_SHA256.txt`.

The withdrawn 0.1.5 build is only a permanent RED/negative regression example and is not an accepted baseline.

## Exact current candidate snapshot

The current local candidate at this checkpoint is `ymb_patch_candidate2`.

The complete candidate tree SHA manifest is stored in `CANDIDATE2_TREE_SHA256.txt`.

Only seven production paths differ from the exact 0.1.4 baseline. Their exact postimage bytes are represented by `PATCH_A_CANDIDATE2.diff`, and `CHANGED_FILES.md` records baseline/postimage hashes.

Changed production paths:

1. `content_script.js`
2. `manifest.json`
3. `phase3_service_worker_bootstrap.js`
4. `file_delivery_content.js` — new
5. `file_delivery_worker_transport.js` — new
6. `shared/chatgpt_file_attachment.js` — new
7. `shared/file_artifact_store.js` — new

Notably, candidate2 keeps the large-file transport out of the monolithic `service_worker.js`; the baseline `service_worker.js` bytes are unchanged.

## Architecture currently implemented

Patch A is intentionally limited to ChatGPT large-text/file delivery. Deferred Search is not included in this candidate.

The corrected path is:

`large result -> chunked binary IndexedDB artifact -> bounded per-chunk worker transfer -> one destination buffer in content -> File/DataTransfer -> ChatGPT attachment -> confirmation -> cleanup`.

The withdrawn 0.1.5 anti-pattern is explicitly not used:

- no all-chunks-in-one `chrome.storage.local` Base64 object;
- no full-store read/deserialization for every 256-KB chunk;
- no retained decoded `chunks[]` plus an additional full destination buffer;
- no deferred-Search monolithic batch state in this Patch A candidate.

## Resource evidence already completed on candidate2

### Node/store stress

`STORE_STRESS_CANDIDATE2.log` + `.time` cover:

`1 MB -> 10 MB -> 32 MB -> 64 MB -> 64 MB -> 64 MB`

Observed candidate2 final repeated 64-MB runs:

- run 4: after cleanup ~133.1 MB RSS;
- run 5: after cleanup ~136.3 MB RSS;
- run 6: after cleanup ~137.7 MB RSS;
- process max RSS: 272040 KB;
- exit status: 0;
- swaps: 0.

This demonstrates the earlier repeated-64-MB timeout was not the final state of candidate2. Candidate2 later completed the repeated store-stress sequence successfully.

### Browser File/DataTransfer memory matrix

`BROWSER_FILE_MEMORY_MATRIX_CANDIDATE2.log` records Chrome 144.0.7559.96 and:

- baseline ~399.6 MB;
- 1 MB: before 399.7 / attached 401.7 / cleanup 402.0 MB;
- 10 MB: before 402.0 / attached 413.0 / cleanup 402.2 MB;
- 32 MB: before 402.2 / attached 435.2 / cleanup 402.3 MB;
- 64 MB run 1: before 402.3 / attached 468.2 / cleanup 402.7 MB;
- 64 MB run 2: before 402.8 / attached 467.4 / cleanup 402.4 MB;
- 64 MB run 3: before 402.1 / attached 468.3 / cleanup 402.2 MB.

All six cases completed; the three repeated 64-MB browser cycles returned close to the pre-case memory level rather than showing monotonic growth.

## Important supersession of the 2026-09-11 checkpoint

The older checkpoint said a repeated 64-MB cycle had timed out and remained unresolved. Work continued after that checkpoint and before the later ChatGPT message-delivery timeout. The local evidence now preserved here shows that the rebuilt `candidate2` completed three 64-MB browser cycles and three 64-MB store cycles.

This WIP checkpoint therefore supersedes the older resource-progress statement, but **does not authorize release**.

## Tests/evidence still not complete

The following remain release-blocking / not yet established for the full final product:

- complete affected-dependency regression on candidate2;
- full worker/state/recovery/owner-isolation matrix for the modularized file-delivery path;
- full `CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md` campaign on an exact frozen installable artifact;
- fresh-package extraction and byte-identity proof;
- Deferred Search Patch B (`10/100/500/1500`, persistence/recovery/cost/provider-boundary) has not been integrated into this Patch A candidate;
- integrated A+B cross-layer regression has not been performed.

## Release verdict

```text
PATCH_A_RESOURCE_MATRIX = PASS_FOR_RECORDED_CASES
PATCH_A_REPEATED_64MB_BROWSER = PASS_FOR_RECORDED_CASES
PATCH_A_REPEATED_64MB_STORE = PASS_FOR_RECORDED_CASES
ALL_IMPACTED_DEPENDENCIES = INCOMPLETE
FULL_PRE_DELIVERY_GATE = NOT_RUN
DEFERRED_SEARCH_PATCH_B = NOT_IN_THIS_CANDIDATE
INTEGRATED_A_PLUS_B = NOT_RUN
FRESH_PACKAGE_IDENTITY = NOT_RUN
RELEASE_ALLOWED = NO
OWNER_HANDOFF = FORBIDDEN
```

## Exact continuation point

Do not rebuild Patch A from scratch.

Resume from the exact owner 0.1.4 baseline plus `PATCH_A_CANDIDATE2.diff`, then verify every target hash against `CANDIDATE2_TREE_SHA256.txt`.

Next work should be:

1. complete all affected-dependency regressions for Patch A candidate2;
2. if any production byte changes, rerun affected tests and the resource matrix as required;
3. only after Patch A is accepted, implement Deferred Search Patch B separately;
4. run Patch B scale/recovery matrix `10 / 100 / 500 / 1500`;
5. integrate accepted A+B and run cross-layer/full pre-delivery/fresh-package gates;
6. only then may `RELEASE_ALLOWED` become YES.
