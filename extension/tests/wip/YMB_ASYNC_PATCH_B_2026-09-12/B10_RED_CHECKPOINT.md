# B10 first full-path RED checkpoint

Date: 2026-09-12. Exact input B9 tree SHA-256: `d1fc4f49718f023f1bc1a6a3ec921fa7253d63b805cedadff6fbcf2e70180612`.
The saved B9 materializer completed and all 108 source-snapshot Git blobs matched the archive manifest. Source retrieval reused the existing read-only workflow, artifact 10295161425. Owner014 ZIP hash verified. No earlier blocks were reimplemented.

## Executed before any production correction

11 full-worker deferred invocation/recovery assertions were run in Node v22.16.0 using the preserved B9 complete-worker harness with two explicit QA additions: a simulated operation-host getManifest value, and a controllable clock. Production manifest remains unchanged. Actual store/runtime/policy/normalizer/transport are loaded; Chrome and IndexedDB are fixtures, fetch is controlled. Real provider calls: 0.

Result: 0 PASS / 11 FAIL. This is NOT eleven independent bugs. Most downstream tests are blocked by a common first failure:

- B6 policy uses worker ID `${sessionId}:search-admission`.
- B8 Manual runtime uses `${sessionId}-search-async`.
- The actual policy.recover rejects the mismatch before the first submit: ASYNC_POLICY_WORKER_MISMATCH.
- Earlier disabled-provider full-worker cases and factory seams did not reach this mismatch.

An independent explicit restart scenario also remains stuck in `search_async_requesting`: the async worker's recovery method is a no-op and normal Manual preflight blocks before recovery.

## Bounded correction plan / affected dependencies

1. Use the same trusted session identity in the shared policy and async runtime; retest trusted binding, policy and old Search guard.
2. Full Manual deferred execution must retain confirmed/unknown execution provenance across later exceptions, stop on normalization/provider failure, bound the slice by elapsed time, and locally normalize immediate submit responses.
3. Explicit later Manual invocation may reconcile a previous worker's interrupted async operation locally, preserve an already-written outbox, and never perform provider replay. Current-worker active operations remain fenced.
4. Retest complete-worker B9, new B10, B6/B7/B8 dependencies and affected module regression on exact postimages.

No release, no browser PASS, no change to operation-host permissions. Next: corrections and same RED assertions, then persist exact code/tests/logs before further integration.
