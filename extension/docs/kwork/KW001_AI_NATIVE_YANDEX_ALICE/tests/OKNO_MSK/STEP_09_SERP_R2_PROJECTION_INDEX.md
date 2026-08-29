# KW-001 / OKNO-MSK — Step 09 R2 projection persistence index

Date: 2026-08-29  
Status: **PASS — NORMALIZED R2 SERP PROJECTION PERSISTED**

## Source event

```text
job_id = kw001-okno-msk-search-step09-20260829-r2
projection.offset = 0
projection.limit = 74
projection.topN = 10
projection.total_successful = 74
projection.next_offset = null
projection.request_executed = false
```

The recovery projection was non-provider / non-billable. No additional Search request was executed to persist this evidence.

## Repository persistence

R2 normalized projection rows are split only to keep the evidence files reviewable and write-safe.

| File | Frozen query indexes | Queries | Ranked rows | Git blob SHA |
|---|---:|---:|---:|---|
| `STEP_09_SERP_R2_PROJECTION_RAW_PART_01.tsv` | 2–20 | 19 | 190 | `9d65c493ce56e70fd023bd12abba51dbe0964d04` |
| `STEP_09_SERP_R2_PROJECTION_RAW_PART_02.tsv` | 21–39 | 19 | 190 | `4fae969c23d8742168647d840c2466e26ea29627` |
| `STEP_09_SERP_R2_PROJECTION_RAW_PART_03.tsv` | 40–58 | 19 | 190 | `c290e399d9e5367ff90c9d915cad9ffd111c173d` |
| `STEP_09_SERP_R2_PROJECTION_RAW_PART_04.tsv` | 59–75 | 17 | 170 | `0fe83859497efc7752151639332f35d3687dcd33` |

R2 total:

```text
queries = 74
ranked rows = 740
query index coverage = 2..75 contiguous
ranks per query = 1..10
```

The previously persisted canary remains in:

```text
STEP_09_SERP_RESULTS.tsv
query index = 1
query = аксессуары для пластиковых окон
ranked rows = 10
blob SHA = ca877bcba86a02134568faade98a4d108abb4537
```

Combined initial-tranche persistence:

```text
queries = 75
normalized ranked rows = 750
query index coverage = 1..75
R2 normalized projection ledger complete = true
canary ledger intact = true
repository normalized SERP ledger complete = true
```

## Re-read QA

The files were read back from GitHub after writing.

Observed boundaries:

```text
part 01 starts: query 2 / rank 1
part 01 ends:   query 20 / rank 10

part 02 starts: query 21 / rank 1
part 02 ends:   query 39 / rank 10

part 03 starts: query 40 / rank 1
part 03 ends:   query 58 / rank 10

part 04 starts: query 59 / rank 1
part 04 ends:   query 75 / rank 10
```

EOF range reads confirm the expected file lengths:

```text
part 01 = header + 190 data rows
part 02 = header + 190 data rows
part 03 = header + 190 data rows
part 04 = header + 170 data rows
R2 total = 740 data rows
```

The canary file was also re-read and still contains ranks 1–10 for query 1.

Persistence QA result:

```text
NORMALIZED_R2_SERP_PERSISTENCE = PASS
COMBINED_75_QUERY_NORMALIZED_SERP_PERSISTENCE = PASS
```

## Evidence boundary

The four R2 TSV files preserve only fields directly supported by the projection used for recovery:

```text
query_index          # frozen-manifest position added for reconciliation
query_text
item_id
region
rank
url
domain
title
```

The projection did not expose the following per R2 item/result fields:

```text
snippet
modtime
provider request_id
http_status
response_format
raw provider XML
```

Therefore those fields were **not invented** and are not claimed as recovered.

Canonical distinction:

```text
REPOSITORY_NORMALIZED_SERP_LEDGER_COMPLETE = true
R2_NORMALIZED_PROJECTION_ROWS_PERSISTED = 740
CANARY_FULL_ROWS_PERSISTED = 10
COMBINED_NORMALIZED_RANKED_ROWS_PERSISTED = 750
R2_RAW_PER_ITEM_PROVIDER_XML_LEDGER_COMPLETE = false
R2_PER_ITEM_PROVIDER_REQUEST_ID_LEDGER_COMPLETE = false
```

This is enough to preserve the normalized TOP-10 evidence returned by the live projection. It is not evidence that unavailable raw provider payload fields were recovered.

## Workflow status

This recovery fixes evidence persistence only.

```text
PROVIDER_ACQUISITION_INITIAL_75 = COMPLETE
REPOSITORY_NORMALIZED_SERP_LEDGER_COMPLETE = true
STEP09_ANALYTICALLY_ACCEPTED = false
STEP10_ALLOWED = false
```

No Step-10 clustering or Step-11 page ownership is authorized by this persistence recovery.
