# KW-001 — CLIENT PRIVATE YANDEX ACCESS POLICY / Bridge capability update

Date: 2026-09-01  
Status: **ACTIVE / UNIVERSAL CAPABILITY UPDATE / OWNER-REQUESTED**

This addendum updates only the Yandex Marketing Bridge capability snapshot referenced by `CLIENT_PRIVATE_YANDEX_ACCESS_POLICY.md` Section 5. All commercial/access rules in the parent policy remain unchanged.

## Superseded capability statement

The earlier policy snapshot said that Webmaster support was limited to:

```text
listHosts
getSummary
getDiagnostics
getPopularQueries
```

and that Enhanced query-by-URL export was not implemented.

That capability statement is now stale and is superseded by this file.

## Current canonical Bridge capability authority

```text
BRIDGE_PRODUCT_BRANCH = bridge/webmaster-readiness-gzip-v0.1.4
BRIDGE_PRODUCT_HEAD = 8bb1365a9905df8a6d7e09917e81444a9b7f1024
BRIDGE_PRODUCT_VERSION = 0.1.4
BRIDGE_FULL_GATE_RUN = 33491679086
BRIDGE_FULL_GATE_CONCLUSION = success
```

The dedicated Bridge product branch is the authority for current Bridge capability. The older `extension/src` snapshot embedded in the Kwork roadmap branch is not the capability authority and must not be used to downgrade the current Bridge product state.

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

The Enhanced Export lifecycle remains explicitly governed: quota-confirmed start, explicit status checks, allowlisted storage collection, durable persistence, local chunk reads, no hidden polling, and no automatic replay of unknown-outcome external requests.

v0.1.4 also fixes the live-discovered compressed-export handling by using bytes-first collection with gzip detection/decompression and separate transport-vs-CSV accounting.

## What this does NOT change

Current Bridge capability does not create client access that does not exist.

For the current `OKNO_MSK` job:

```text
YANDEX_WEBMASTER_ACCESS_STATE = UNAVAILABLE
OKNO_MSK_HOST_ID_RESOLVED = false
YANDEX_WEBMASTER_PRIVATE_EVIDENCE_USED = false
BASE_PUBLIC_EVIDENCE_MODE = true
```

So Enhanced Export is available as a product capability but cannot and need not be executed for this no-access base-mode test job.

The parent policy remains authoritative:

```text
YANDEX_WEBMASTER_ACCESS_REQUIRED_TO_BUY = false
YANDEX_WEBMASTER_ACCESS_REQUIRED_TO_EXECUTE_BASE_SCOPE = false
CLIENT_PRIVATE_DATA_UNAVAILABLE = NORMAL_BASE_MODE
```

The first future job with usable client Webmaster access still triggers the controlled WITHOUT_ACCESS vs WITH_ACCESS comparison. Before using Bridge on that future property, the installed runtime and delegated property must be validated against the then-current canonical Bridge build.
