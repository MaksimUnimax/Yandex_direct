# OKNO_MSK — STEP 13 FIRST-PARTY QUERY×URL HISTORY RECOVERY PLAN

Date: 2026-09-01  
Status: **OPTIONAL ENHANCED / WITH-ACCESS PATH / NOT REQUIRED FOR BASE STEP-13 CLOSURE**

## Objective

If a future job has usable client Yandex Webmaster access and an enhanced/research-grade historical diagnosis is authorized, add a first-party evidence layer:

```text
QUERY FAMILY × TARGET-SITE URL × TIME
```

This plan is not part of the current no-access OKNO-MSK base closure.

No additional paid ordinary Search request is part of this plan.

## Current OKNO-MSK access boundary

Historical durable probe:

```text
WEBMASTER_API_V1
method = listHosts
HTTP 200
hosts = []
request_executed = true
```

Current job state:

```text
WEBMASTER_API_REACHABLE = true
YANDEX_WEBMASTER_ACCESS_STATE = UNAVAILABLE
OKNO_MSK_HOST_ID_RESOLVED = false
YANDEX_WEBMASTER_PRIVATE_EVIDENCE_USED = false
HOST_SCOPED_QUERY_HISTORY_ALLOWED = false
```

Do not guess hostId and do not repeat provider calls for this test job merely to satisfy an optional enhanced path.

## Bridge capability status — actualized

The old version of this recovery plan treated Bridge capability as a blocker because the Kwork branch contained an older four-method Webmaster snapshot.

That statement is superseded.

Current canonical Bridge product authority:

```text
BRIDGE_PRODUCT_BRANCH = bridge/webmaster-readiness-gzip-v0.1.4
BRIDGE_PRODUCT_HEAD = 8bb1365a9905df8a6d7e09917e81444a9b7f1024
BRIDGE_PRODUCT_VERSION = 0.1.4
BRIDGE_FULL_GATE_RUN = 33491679086
BRIDGE_FULL_GATE_CONCLUSION = success
WEBMASTER_METHOD_COUNT = 16
ENHANCED_QUERY_URL_EXPORT_SUPPORTED = true
GET_HOST_INFO_SUPPORTED = true
```

The v0.1.4 protocol includes:

```text
getExportRegions
getExportLimits
getExportDates
startQueryUrlExport
getQueryUrlExportStatus
collectQueryUrlExport
readQueryUrlExportChunk
```

It also includes `getAllQueryHistory` / `getQueryHistory` and `getHostInfo`.

The Enhanced Export collection path is bytes-first and supports gzip detection/decompression with separate downloaded-vs-CSV accounting.

Therefore:

```text
BRIDGE_CAPABILITY_BLOCKER = false
CURRENT_OKNO_MSK_ACCESS_BLOCKER_FOR_ENHANCED_MODE = true
CURRENT_OKNO_MSK_ACCESS_BLOCKER_FOR_BASE_MODE = false
```

## Kwork-branch version note

The Kwork roadmap branch may still contain an older embedded `extension/src` snapshot (`0.1.2`). That snapshot is not the authority for current Bridge product capability.

For any future real with-access execution, use and validate the then-current canonical Bridge product build rather than the embedded Kwork snapshot.

## Future enhanced recovery sequence

### R13-H1 — delegated access readiness

On a future job where access is actually provided:

```text
1. Confirm delegated Yandex Webmaster access under the working Yandex ID.
2. Confirm the exact property variant.
3. Validate the installed current Bridge build.
4. Run one bounded listHosts check.
5. Persist/read back the useful result before host-scoped work.
```

### R13-H2 — host discovery and readiness

Resolve the exact provider `host_id`; never guess it.

Then, where useful, run explicit `getHostInfo` to preserve `host_data_status` / `webmaster_data_ready` evidence. A non-ready host state must not be reinterpreted as an OAuth/access failure without evidence.

### R13-H3 — choose first-party route

Available governed routes may include:

```text
ROUTE A = authorized Webmaster UI/query monitoring/export
ROUTE B = current Bridge Enhanced Export
ROUTE C = explicitly justified comparable first-party query×URL history source
```

For Route B, validate the installed runtime before the real property run even though the current product capability exists.

### R13-H4 — freeze historical manifest

Create:

`STEP_13_FIRST_PARTY_HISTORY_MANIFEST.tsv`

Required columns:

```text
case_id
query_family
probe_query_or_query_filter
candidate_urls
region
date_from
date_to
time_granularity
source_route
expected_fields
quota_units_estimate
why_window_is_sufficient_or_partial
storage_artifact
```

The window must be justified using actual date availability, seasonality, query volume, candidate count, provider quota and decision value.

### R13-H5 — acquisition and preservation

For each provider/export unit:

```text
DEFINE REQUIRED OUTPUT
→ EXECUTE ONE UNIT
→ RECEIVE RESULT / TASK STATUS
→ IF ASYNC EXPORT: USE EXPLICIT STATUS COMMANDS ONLY
→ COLLECT ONLY AFTER SUCCESS
→ SAVE COMPLETE REQUIRED RESULT
→ GITHUB READBACK
→ COMPLETENESS QA
→ ONLY THEN NEXT UNIT
```

A successful export initialization is not the dataset:

```text
EXPORT_TASK_CREATED != EXPORT_DATA_ACQUIRED
```

### R13-H6 — normalized history evidence

Create:

`STEP_13_FIRST_PARTY_QUERY_URL_HISTORY.tsv`

At minimum preserve when supplied:

```text
date
host
url
query
region
clicks
impressions
position
case_id
source_route
source_artifact
```

### R13-H7 — historical case analysis

Create:

`STEP_13_HISTORICAL_COMPETITION_DIAGNOSIS.tsv`

For each material case record:

```text
candidate_urls
same_query_multi_url_observed
stable_primary_url
owner_switching_observed
switching_periods
impression_fragmentation_signal
click_fragmentation_signal
position_instability_signal
benign_explanation_present
historical_competition_verdict
harm_evidence_state
evidence_limitations
```

No fixed numerical harm threshold is invented by this plan.

### R13-H8 — compare against the frozen no-access baseline

The active Layer-A policy requires the first real with-access job to compare WITH_ACCESS against the already frozen WITHOUT_ACCESS outputs.

Required comparison labels:

```text
CHANGE
DE_RISK
NEW_FINDING
NO_CHANGE
INSUFFICIENT_TO_COMPARE
```

### R13-H9 — remediation delta

Recompute only cases affected by first-party history. Preserve non-destructive posture unless new evidence qualifies a stronger action.

### R13-H10 — enhanced QA

QA must verify:

```text
history manifest rows accounted
provider/export units accounted
history rows saved/readable
material cases mapped to history evidence or explicit evidence limitation
historical verdict from one public SERP = 0
harm claim without harm evidence = 0
WITH_ACCESS vs WITHOUT_ACCESS comparison complete
```

## Current stop condition

For OKNO-MSK now:

```text
STEP13_BASE_MODE_COMPLETE = true
OKNO_MSK_HOST_ID_RESOLVED = false
ENHANCED_EXPORT_BRIDGE_OPERATION_AVAILABLE = true
HISTORICAL_PROVIDER_EXECUTION_ALLOWED_NOW = false
HISTORICAL_PROVIDER_EXECUTION_REQUIRED_NOW = false
```

Therefore the correct current action is to leave this optional enhanced plan dormant and proceed to Step 14.
