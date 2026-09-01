# OKNO_MSK — STEP 13 FIRST-PARTY QUERY×URL HISTORY RECOVERY PLAN

Date: 2026-09-01
Status: **REQUIRED / BLOCKED BEFORE PROVIDER EXECUTION**

## Objective

Complete the evidence layer missing from the first Step-13 execution:

```text
QUERY FAMILY × TARGET-SITE URL × TIME
```

using first-party Yandex Webmaster evidence where possible.

No additional paid ordinary Search request is part of this recovery plan.

## Current durable blockers

### A. Webmaster property/account blocker

Existing durable probe:

```text
WEBMASTER_API_V1
method = listHosts
HTTP 200
hosts = []
request_executed = true
```

Therefore:

```text
WEBMASTER_API_REACHABLE = true
OKNO_MSK_HOST_ID_RESOLVED = false
HOST_SCOPED_QUERY_HISTORY_ALLOWED = false
```

Do not guess hostId. Do not blind-repeat `listHosts` until account/version correction has actually occurred.

### B. Bridge capability blocker

Current repository `extension/src/shared/webmaster_protocol.js` allows only:

```text
listHosts
getSummary
getDiagnostics
getPopularQueries
```

The official enhanced query-by-URL export workflow is not implemented in the current first slice.

Official Yandex API currently exposes enhanced-export resources including:

```text
/v4/user/{user-id}/hosts/{host-id}/pro/regions
/v4/user/{user-id}/hosts/{host-id}/pro/limits
/v4/user/{user-id}/hosts/{host-id}/pro/serp/dates
/v4/user/{user-id}/hosts/{host-id}/pro/serp/queries/download/
/v4/user/{user-id}/hosts/{host-id}/pro/serp/queries/download/{task-id}
```

### C. Runtime/version boundary

```text
repository extension version = 0.1.2
last durable live Webmaster probe runtime = 0.1.1
```

Resolve or explicitly accept this boundary before treating a new live result as current production evidence.

## Required recovery sequence

### R13-H1 — account/property correction

Operator-side prerequisites:

```text
1. Confirm the Yandex account used by the Bridge has access to okno-msk.ru in Webmaster.
2. Confirm the saved Webmaster OAuth token belongs to that account.
3. Update/reload the installed Bridge to the intended current build or explicitly record the accepted runtime version.
```

Only after one of those facts materially changes may `listHosts` be executed again.

### R13-H2 — single host discovery recheck

When prerequisites are corrected, execute exactly once:

```text
WEBMASTER_API_V1
{"method":"listHosts"}
```

Required result persistence:

```text
request_id
runtime version
http status
request_executed
hosts[] complete
exact host_id for okno-msk.ru if returned
```

Then persist to GitHub and read back before any host-scoped action.

If `hosts=[]` again:

```text
STOP
ACCOUNT_PROPERTY_BLOCKER_REMAINS = true
NO HOST-SCOPED REQUEST
```

### R13-H3 — choose executable historical route

After hostId resolution, choose one real route:

```text
ROUTE A = authorized Webmaster UI/query monitoring/export
ROUTE B = governed Bridge enhancement for official enhanced export
ROUTE C = explicitly justified comparable first-party query×URL history source
```

Do not declare ROUTE B available merely because Yandex API documentation exists. The operation must be implemented, tested and available in the installed runtime.

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

The window is not a universal fixed number. It must be justified using actual date availability, seasonality, query volume, candidate count, provider quota and decision value.

### R13-H5 — acquisition and preservation

For each provider/export unit:

```text
DEFINE REQUIRED OUTPUT
→ EXECUTE ONE UNIT
→ RECEIVE RESULT / TASK STATUS
→ IF ASYNC EXPORT: POLL ONLY ACCORDING TO THE GOVERNED ROUTE, WITHOUT BLIND RECREATION
→ SAVE COMPLETE REQUIRED RESULT
→ GITHUB READBACK
→ COMPLETENESS QA
→ ONLY THEN NEXT UNIT
```

A successful export initialization is not the dataset.

```text
EXPORT_TASK_CREATED != EXPORT_DATA_ACQUIRED
```

### R13-H6 — normalized history evidence

Create:

`STEP_13_FIRST_PARTY_QUERY_URL_HISTORY.tsv`

At minimum preserve when provider supplies them:

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

For every material case record:

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

### R13-H8 — merge with preserved public/current layer

Rebuild final `STEP_13_CONFLICT_DIAGNOSIS.tsv` using:

```text
current page/task evidence
+ current public Search evidence
+ historical first-party query×URL evidence
```

Keep the layers distinguishable in the final explanation.

### R13-H9 — remediation rebuild

Recompute only cases affected by history. Preserve non-destructive posture unless new evidence qualifies a stronger action.

### R13-H10 — QA and acceptance

QA must explicitly verify:

```text
history manifest rows accounted
provider/export units accounted
history rows saved/readable
material cases mapped to history evidence or explicit evidence limitation
known required source silently skipped = 0
historical verdict from one public SERP = 0
harm claim without harm evidence = 0
blocking findings = 0
```

Only after this may `STEP_13_ACCEPTANCE_2026-09-01.md` return to full PASS.

## Current stop condition

At the time this plan is written:

```text
OKNO_MSK_HOST_ID_RESOLVED = false
ENHANCED_EXPORT_BRIDGE_OPERATION_AVAILABLE = false
HISTORICAL_PROVIDER_EXECUTION_ALLOWED_NOW = false
```

Therefore the correct action is to preserve the blocker and stop provider execution, not to spend another Search request or guess credentials/host identifiers.
