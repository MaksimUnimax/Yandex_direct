# YMB Deferred Search Patch B — browser 1500 scale/restart completion

Date: 2026-09-12
Branch: `wip/ymb-search-async-patch-b-2026-09-12`
Candidate: exact Patch B candidate1; no production edits during the browser 1500 recovery campaign.
Browser: Chrome/Chromium 144.0.7559.96 controlled QA profile.
Real Yandex requests: 0.

## Durable campaign result

One 1500-item async job survived multiple fresh browser/MV3 worker lifecycles on the same profile/IndexedDB.

Submit evidence:

- lifecycle 1: 750 submits persisted;
- restart;
- lifecycle 2: remaining 750 submits persisted;
- total submit operations persisted = 1500;
- `PENDING=0`, `WAITING_PROVIDER_RESULT=1500` before collection campaign;
- no item list embedded in job record.

Collection evidence:

- an earlier aborted diagnostic had durably completed 68 items before its harness timeout;
- standalone lifecycle/session 3 then executed exactly 750 new Operation GETs, zero submits;
- standalone lifecycle/session 4 executed exactly the remaining 682 Operation GETs, zero submits;
- final durable job state:

```text
status = COMPLETED
PENDING = 0
SUBMITTING = 0
WAITING_PROVIDER_RESULT = 0
SUCCEEDED = 1500
FAILED_TERMINAL = 0
OUTCOME_UNKNOWN = 0
CANCELLED = 0
job_json_bytes = 543
job_has_items = false
```

Session 3:

```text
new_GET = 750
new_submit = 0
unexpected_fetch = 0
seconds = 7.533
pre = WAITING 1432 / SUCCEEDED 68
post = WAITING 682 / SUCCEEDED 818
```

Session 4:

```text
new_GET = 682
new_submit = 0
unexpected_fetch = 0
seconds = 9.531
pre = WAITING 682 / SUCCEEDED 818
post = WAITING 0 / SUCCEEDED 1500 / COMPLETED
```

The previous long single-CDP harness timeout is classified as a QA lifecycle problem: a long-lived direct CDP attachment to one MV3 service worker crossed the service-worker lifecycle boundary. The same persisted product state completed when tested through bounded fresh browser/worker lifecycles. Production was not modified to accommodate the harness.

## Resource observation

The active process-tree RSS increased while 750/682 results were being parsed and persisted, but every browser lifecycle was deliberately bounded and terminated after its checkpoint. These observations do not by themselves claim post-GC in-process reclamation; the relevant product-scale acceptance here is bounded per-session lifecycle, successful durable completion, no giant job object and no replay. Cross-layer final resource evidence remains required after A+B integration.

## Policy cleanup

The external cleanup trap restored the exact managed Chromium policy after each lifecycle.

Restored policy SHA-256:

`3b740260e337305aaef268e6c63af8fa2796057ce46f43df5ae5a3949e085e86`

## Verdict

```text
PATCH_B_BROWSER_IDB_SCALE_1500 = PASS
PATCH_B_BROWSER_RESTART_PERSISTENCE = PASS
NO_SUBMIT_REPLAY_ACROSS_RESTART = PASS
FINAL_SUCCEEDED = 1500
FINAL_JOB_RECORD_BOUNDED = PASS
PRODUCTION_BYTES_CHANGED = NO
PATCH_B_ACCEPTED_FOR_INTEGRATION = NOT_YET
RELEASE_ALLOWED = NO
```

Next mandatory blocks: rate-limit/cost/provider-boundary, shared sync-service dependency regression, exact-candidate identity, then Patch-B acceptance-for-integration decision.
