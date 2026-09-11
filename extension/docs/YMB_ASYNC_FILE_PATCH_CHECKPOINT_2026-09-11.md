# Yandex Marketing Bridge — async Search + ChatGPT file-delivery patch checkpoint

Date: 2026-09-11  
Status: **STOPPED BY OWNER / PATCH NOT RELEASED / RESOURCE GATE NOT PASSED**

## 1. Exact working boundary

The patch work is based on the owner-provided installable archive:

`yandex-marketing-bridge-0.1.4-webmaster-readiness-gzip(2).zip`

The withdrawn `0.1.5` candidate is **not** an accepted baseline and must not be reused as a release candidate.

Permanent patch/release authority already adopted for this work:

`extension/docs/YMB_PATCH_DEPENDENCY_AND_RESOURCE_SAFETY_RULE.md`

The rule is also linked from:

`extension/README.md`

## 2. Withdrawn 0.1.5 defect already established

The previous 0.1.5 file-delivery implementation was rejected because it could amplify memory usage through a combination of:

- full-payload Base64 materialization;
- storing all Base64 chunks in one large `chrome.storage.local` object;
- repeatedly reading/deserializing the whole artifact store for individual chunk requests;
- retaining decoded chunk arrays and allocating another full destination buffer;
- creating an additional File/Blob representation;
- similar large-object cloning/amplification risks in the deferred Search batch path.

This failure pattern is now a permanent negative regression case in `YMB_PATCH_DEPENDENCY_AND_RESOURCE_SAFETY_RULE.md`.

## 3. Intended corrected architecture

### File delivery

The corrected direction is to adapt the proven Ozon Bridge ChatGPT file-delivery architecture rather than invent another simplified transport:

- binary artifact persistence via IndexedDB;
- bounded chunk transfer;
- checksum/integrity verification;
- ChatGPT File/DataTransfer attachment path;
- confirmation/recovery without provider replay;
- cleanup of delivered artifacts;
- ChatGPT-specific text/file threshold only (do not inherit Alice limits).

### Deferred Search

Deferred Search must not use one giant mutable JSON job that is cloned/serialized for every item transition.

Required direction:

- per-job/per-item durable state;
- persisted provider operation IDs;
- no blind re-submit after unknown submit outcome;
- bounded collection/polling;
- no monolithic full-batch rewrite on each item;
- no hidden provider replay from recovery;
- resource/scale evidence at realistic batch sizes.

## 4. Dependency rule for this patch

After every material production edit, all affected dependencies must be retested. Applicable paths include:

- JS/MJS syntax;
- protocol/command contracts;
- worker/state machine;
- storage/persistence/recovery;
- quota/cost accounting;
- ownership/tab/conversation isolation;
- Manual/Autorun compatibility where affected;
- composer/attachment/delivery/confirmation;
- browser/Puppeteer runtime;
- provider boundary/network failures;
- credential isolation;
- backup/import compatibility;
- manifest/permissions/load order;
- adjacent Wordstat/Search/GenSearch/Webmaster/Metrika/Direct regressions when shared code is touched;
- fresh-package extraction and exact candidate identity.

If an affected dependency is untested, release remains forbidden.

## 5. Resource-gate progress at stop point

Current working-session notes reached the following point:

- browser-owned file-delivery path was being tested on the exact production candidate rather than only in a Node/VM mock;
- an initial large-file matrix covering `1 MB / 10 MB / 32 MB / 64 MB` was exercised and showed bounded/linear behavior in the first cycle;
- the mandatory repeated-run test then encountered a **timeout on a repeated 64 MB cycle**;
- the exact stage of that repeated-cycle timeout (staging / IndexedDB / chunk transfer / DOM attachment / confirmation / cleanup) has **not yet been root-caused and closed**.

Therefore the only valid current verdict is:

```text
MEMORY_STRESS = NOT_ACCEPTED
REPEATED_RUN_LEAK_TEST = NOT_PASSED
BROWSER_REQUIRED_TESTS = INCOMPLETE
ALL_IMPACTED_DEPENDENCIES = INCOMPLETE
FRESH_PACKAGE_EXTRACTION = NOT_RUN_FOR_FINAL_CANDIDATE
PACKAGE_BYTES_MATCH_TESTED_CANDIDATE = NOT_ESTABLISHED
RELEASE_ALLOWED = NO
OWNER_HANDOFF = FORBIDDEN
```

No installable ZIP from the current patch work is approved for owner use.

## 6. Exact stop point / next required action

Work is intentionally stopped here by owner request.

When work resumes, do **not** restart from scratch and do **not** hand off a ZIP.

Resume at:

1. reproduce the repeated 64 MB timeout on the same exact candidate;
2. identify the exact phase where it stalls;
3. classify the cause as product / harness / environment;
4. if product: make the smallest bounded correction;
5. rerun all dependencies affected by that correction;
6. rerun the complete resource matrix from the start, including repeated 64 MB cycles, cleanup and recovery;
7. continue deferred Search scale/recovery testing (`10 / 100 / 500 / 1500`) only after the file-delivery resource gate is clean;
8. freeze exact final candidate;
9. run the mandatory full pre-delivery gate;
10. fresh-extract the final ZIP and prove byte identity before any owner handoff.

## 7. Owner stop instruction

```text
OWNER_REQUEST = FIX_PROGRESS_AND_STOP
PATCH_EXECUTION = STOPPED
NO_FURTHER_CODE_EDIT = YES
NO_FURTHER_TEST_EXECUTION = YES
NO_PACKAGE_HANDOFF = YES
```
