# KW-001 — CLIENT PRIVATE YANDEX ACCESS POLICY / Bridge capability update

Date: 2026-09-01  
Updated: 2026-09-03  
Status: **ACTIVE / UNIVERSAL CAPABILITY UPDATE / OWNER-REQUESTED**

This addendum updates only the Yandex Marketing Bridge capability snapshot referenced by `CLIENT_PRIVATE_YANDEX_ACCESS_POLICY.md`. All commercial/access rules in the parent policy remain unchanged.

This file is Level-1 product/method capability authority. Concrete client/test access state, host IDs, property URLs and whether private evidence was used belong only in the current Level-2 job workspace.

## Superseded capability statement

The earlier policy snapshot said that Webmaster support was limited to:

```text
listHosts
getSummary
getDiagnostics
getPopularQueries
```

and that Enhanced query-by-URL export was not implemented.

That capability statement is stale and is superseded by this file.

## Current canonical Bridge capability authority

```text
BRIDGE_PRODUCT_BRANCH = bridge/webmaster-readiness-gzip-v0.1.4
BRIDGE_PRODUCT_HEAD = 8bb1365a9905df8a6d7e09917e81444a9b7f1024
BRIDGE_PRODUCT_VERSION = 0.1.4
BRIDGE_FULL_GATE_RUN = 33491679086
BRIDGE_FULL_GATE_CONCLUSION = success
```

These values describe the reusable Bridge product capability itself, not a client job. The dedicated Bridge product branch is the authority for current Bridge capability. An older extension snapshot embedded in another working branch must not be used to downgrade the current product capability.

## Current Webmaster surface

The v0.1.4 Webmaster protocol exposes 16 governed methods:

```text
listHosts
getHostInfo
getSummary
getDiagnostics
getPopularQueries
getAllQueryHistory
getQueryHistory
getIndexingSamples
getInSearchSamples
getExportRegions
getExportLimits
getExportDates
startQueryUrlExport
getQueryUrlExportStatus
collectQueryUrlExport
readQueryUrlExportChunk
```

Therefore:

```text
CURRENT_WEBMASTER_BRIDGE_ENHANCED_QUERY_URL_EXPORT_SUPPORTED = true
CURRENT_WEBMASTER_BRIDGE_HOST_READINESS_SUPPORTED = true
CURRENT_WEBMASTER_BRIDGE_QUERY_HISTORY_READ_SURFACE_SUPPORTED = true
```

The Enhanced Export lifecycle remains explicitly governed: quota-confirmed start, explicit status checks, allowlisted storage collection, durable persistence, local chunk reads, no hidden polling and no automatic replay of unknown-outcome external requests.

v0.1.4 also fixes compressed-export handling by using bytes-first collection with gzip detection/decompression and separate transport-vs-CSV accounting.

## Capability != access

Current Bridge capability does not create client access that does not exist.

For every current job, Level-2 state must separately record equivalent fields:

```text
YANDEX_WEBMASTER_ACCESS_STATE
HOST_OR_PROPERTY_RESOLUTION_STATE
YANDEX_WEBMASTER_PRIVATE_EVIDENCE_USED
CURRENT_ACCESS_MODE
INSTALLED_RUNTIME / BRIDGE VERSION WHEN MATERIAL
```

Canonical boundary:

```text
BRIDGE CAPABILITY AVAILABLE
!= CLIENT ACCESS AVAILABLE
!= PROPERTY RESOLVED
!= PRIVATE EVIDENCE USED
```

A no-access base job does not need to execute Enhanced Export merely because the Bridge can do it.

The parent policy remains authoritative:

```text
YANDEX_WEBMASTER_ACCESS_REQUIRED_TO_BUY = false
YANDEX_WEBMASTER_ACCESS_REQUIRED_TO_EXECUTE_BASE_SCOPE = false
CLIENT_PRIVATE_DATA_UNAVAILABLE = NORMAL_BASE_MODE
```

The first future job with usable client Webmaster access still triggers the controlled WITHOUT_ACCESS vs WITH_ACCESS comparison defined by the parent policy. Before using Bridge on a future delegated property, the installed runtime and delegated property must be validated against the then-current canonical Bridge build.

This file follows `PERMANENT_STEP_RULE_UNIVERSALITY_AND_JOB_SEPARATION_GATE.md`.
