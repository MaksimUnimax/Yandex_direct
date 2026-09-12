# YMB Deferred Search Patch B — Node scale block 2

Date: 2026-09-12
Candidate: Patch B candidate1, production bytes unchanged since Block 1.
Provider: synthetic only, real Yandex requests = 0.

Mandatory scale matrix completed:

| items | total ms | RSS delta after GC | max job JSON | max item JSON | submit calls | collect calls | result |
|---:|---:|---:|---:|---:|---:|---:|---|
| 10 | 24.4 | 2.5 MB | 525 B | 788 B | 10 | 10 | PASS |
| 100 | 80.0 | 7.8 MB | 534 B | 794 B | 100 | 100 | PASS |
| 500 | 316.2 | 5.9 MB | 536 B | 796 B | 500 | 500 | PASS |
| 1500 | 1032.9 | 29.3 MB | 543 B | 802 B | 1500 | 1500 | PASS |

Whole process maximum RSS from `/usr/bin/time -v`: `73352 KB`; swaps: `0`; exit status: `0`.

For 1500 items:

```text
status = COMPLETED
succeeded = 1500
job_has_items = false
job_writes = 6001
item_writes = 7500
result_writes = 1500
submit_calls = 1500
collect_calls = 1500
```

The job record remains bounded instead of embedding the 1500-item list. Per-item mutation does not clone/stringify one giant batch object.

Verdict:

```text
PATCH_B_NODE_SCALE_10_100_500_1500 = PASS
REAL_INDEXEDDB_BROWSER_SCALE = STILL_REQUIRED
RELEASE_ALLOWED = NO
```
