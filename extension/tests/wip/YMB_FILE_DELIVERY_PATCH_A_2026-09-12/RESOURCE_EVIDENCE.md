# Patch A candidate2 resource evidence

## Browser File/DataTransfer matrix

Chrome: `Chrome/144.0.7559.96`  
Baseline RSS: `399.0 MB`

| Run | Size MB | Before MB | Attached MB | After cleanup MB | Elapsed ms |
|---:|---:|---:|---:|---:|---:|
| 1 | 1 | 399.1 | 401.9 | 400.1 | 508 |
| 2 | 10 | 400.1 | 410.9 | 400.3 | 570 |
| 3 | 32 | 400.3 | 434.3 | 401.6 | 756 |
| 4 | 64 | 401.7 | 467.0 | 402.1 | 994 |
| 5 | 64 | 402.2 | 467.3 | 402.0 | 994 |
| 6 | 64 | 402.0 | 466.6 | 401.9 | 1044 |

Three consecutive 64-MB cases completed. Cleanup returned RSS to ~402 MB after each case; no monotonic 64-MB-cycle growth is visible in this recorded matrix.

## Node/store stress raw log

```text
[
  {"size_mb":1,"chunk_count":4,"before_mb":27,"after_text_mb":27,"after_stage_mb":31.6,"after_read_mb":33.6,"after_cleanup_mb":31.7,"stage_ms":40,"read_ms":11},
  {"size_mb":10,"chunk_count":40,"before_mb":27.6,"after_text_mb":27.6,"after_stage_mb":68.1,"after_read_mb":78.3,"after_cleanup_mb":55.7,"stage_ms":249,"read_ms":56},
  {"size_mb":32,"chunk_count":128,"before_mb":55.7,"after_text_mb":55.7,"after_stage_mb":125.6,"after_read_mb":161.3,"after_cleanup_mb":97.8,"stage_ms":526,"read_ms":186},
  {"size_mb":64,"chunk_count":256,"before_mb":77.2,"after_text_mb":77.2,"after_stage_mb":194.8,"after_read_mb":260.3,"after_cleanup_mb":133.1,"stage_ms":906,"read_ms":321},
  {"size_mb":64,"chunk_count":256,"before_mb":133.3,"after_text_mb":133.3,"after_stage_mb":199.4,"after_read_mb":264.3,"after_cleanup_mb":136.3,"stage_ms":680,"read_ms":343},
  {"size_mb":64,"chunk_count":256,"before_mb":136.3,"after_text_mb":136.3,"after_stage_mb":200.4,"after_read_mb":265.7,"after_cleanup_mb":137.7,"stage_ms":649,"read_ms":304}
]
```

## Process timing / max RSS

```text
Command: node --expose-gc file_artifact_store_stress.mjs
Elapsed wall clock: 0:05.07
Maximum resident set size: 272040 KB
Swaps: 0
Exit status: 0
```
