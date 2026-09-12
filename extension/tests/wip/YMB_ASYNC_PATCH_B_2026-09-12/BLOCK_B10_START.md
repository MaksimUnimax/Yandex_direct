# B10 — remaining full invocation and failure-stop contracts

Date: 2026-09-12. Frozen live input: `aae11100d0ac53b79302e77b50851f1517ad9bba`.
Continue from the exact combined B9 candidate (`d1fc4f49718f023f1bc1a6a3ec921fa7253d63b805cedadff6fbcf2e70180612`, 67 files). Do not rewrite A/B1-B9.

Owner baseline ZIP is present locally and its SHA-256 was rechecked: `b812c4c54d1054d63a24ea852e1721e813d133172487c9872bac347998e3e53f`.
The cursor, mandatory dependency/resource rule and pre-delivery gate were read. Final gate and installable ZIP are not authorized by intermediate Node results.

## Planned bounded unit

Use the preserved complete-worker harness to exercise deferred submit/collect on controlled responses, real command-to-worker paths, existing Check/Autorun/batch invocation, truthful outcome propagation, stop-on-error, and local recovery/delivery. Permission fixture may simulate operation-host access only inside QA; the actual manifest stays unchanged. No real provider requests. If a production assertion fails, preserve exact RED evidence, make the smallest dependency-bounded correction, and rerun affected regressions.

## Dependency impact to record

Manual worker -> B3 runtime -> B5 policy/legacy guard -> B6 owner binding -> shared state/outbox -> existing batch/Autorun -> content discovery contracts. Enumerate exact changed modules and their callers before a production correction. Source-only tests cannot establish live DOM behavior.

## Evidence boundary

Only execute checks available in this environment. Do not repeat the known administratively blocked browser launch or bypass policies. Node/fixtures are not Chromium memory, actual IndexedDB durability or installed-extension proof.

## Recovery transport

Existing local source snapshot predates B9. Reuse the existing read-only source-snapshot Actions workflow pinned to the frozen B9 ref, download its internal QA artifact, and verify Git blobs before reconstruction. Do not pass source payloads through chat or ask the owner to move QA files. No new product build is created by that transport.

CURRENT_UNIT = B10_IN_PROGRESS
RELEASE_ALLOWED = NO
PROVIDER_CALLS = 0
NEXT = restore exact B9 source snapshot, then execute full-path tests and persist the first material result.
