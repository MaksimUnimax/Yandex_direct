# YMB Deferred Search Patch B — browser 1500 recovery session 3 checkpoint

Date: 2026-09-12
Branch: `wip/ymb-search-async-patch-b-2026-09-12`
Candidate: exact Patch B candidate1; full candidate SHA manifest rechecked after this run: `59/59 PASS`, no extra/missing files, production bytes unchanged.
Browser: Chrome/Chromium 144.0.7559.96 controlled QA profile.
Real Yandex traffic: 0.

## Proven prior state

Two prior browser lifecycles already persisted all 1500 synthetic async submit operations into the same IndexedDB profile:

- lifecycle 1: 750 submit -> `PENDING=750`, `WAITING_PROVIDER_RESULT=750`;
- browser restart;
- lifecycle 2: remaining 750 submit -> `PENDING=0`, `WAITING_PROVIDER_RESULT=1500`.

Those PASS results were preserved; the job was not recreated and no submit was replayed for this checkpoint.

## Resume-state reconciliation

At the start of this new standalone collect lifecycle, durable state was:

```text
PENDING = 0
WAITING_PROVIDER_RESULT = 1432
SUCCEEDED = 68
FAILED_TERMINAL = 0
OUTCOME_UNKNOWN = 0
CANCELLED = 0
job_json_bytes = 518
job_has_items = false
```

The `68 SUCCEEDED` records were already durable from the previously aborted/diagnostic browser collection attempt. They are recorded as pre-existing evidence and were not recomputed or resubmitted.

## Session 3 action

This session executed collection only:

```text
new_submit_calls = 0
new_operation_GET_calls = 750
unexpected_fetch_calls = 0
```

Progress completed through all 750 requested collects without worker/CDP loss.

Final durable state after session 3:

```text
PENDING = 0
WAITING_PROVIDER_RESULT = 682
SUCCEEDED = 818
FAILED_TERMINAL = 0
OUTCOME_UNKNOWN = 0
CANCELLED = 0
job_status = RUNNING
job_json_bytes = 519
job_has_items = false
```

Timing / resource observation:

```text
collect_750_seconds = 7.533
process_tree_rss_before = 592560128
process_tree_rss_after = 722694144
rss_delta_during_active_collection = 130134016
```

This RSS delta is an active-operation observation, not a leak verdict by itself; the browser process was terminated at the end of the bounded QA lifecycle. No unbounded monotonic multi-session claim is made from this single observation.

Chromium managed policy was restored by the outer cleanup trap. Restored SHA-256:

`3b740260e337305aaef268e6c63af8fa2796057ce46f43df5ae5a3949e085e86`

## Verdict / continuation

```text
BROWSER_1500_SUBMIT_PERSISTENCE_ACROSS_RESTART = PASS
SESSION3_COLLECT_750 = PASS
NO_SUBMIT_REPLAY_IN_SESSION3 = PASS
JOB_RECORD_REMAINS_BOUNDED = PASS
REMAINING_WAITING = 682
PATCH_B_BROWSER_1500_COMPLETE = NO
RELEASE_ALLOWED = NO
```

Next action is a new short browser lifecycle on the same preserved profile that collects exactly the remaining 682 operations, verifies `COMPLETED / SUCCEEDED=1500`, then checkpoints that final browser-scale result before any subsequent dependency block.
