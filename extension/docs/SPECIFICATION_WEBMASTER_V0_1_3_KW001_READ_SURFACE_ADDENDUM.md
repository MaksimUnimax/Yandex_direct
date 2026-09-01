# SPECIFICATION — Webmaster v0.1.3 KW-001 full read/export surface

Status: **CURRENT VERSION-SPECIFIC CONTRACT / OWNER AUTHORIZED / SUPERSEDES PHASE-3 FIRST-SLICE LIMITS FOR v0.1.3**  
Adopted: 2026-09-01  
Product: Yandex Marketing Bridge 0.1.3

## 0. Authority and supersession

This addendum extends the accepted Phase-3 Webmaster implementation without changing the service identity, OAuth credential model, five-service registry, Manual/delivery lifecycle, or no-blind-retry contract.

For Yandex Marketing Bridge `0.1.3+`, this file supersedes only the first-slice method/deferred-surface restrictions in:

`SPECIFICATION_PHASE_3_WEBMASTER_ADDENDUM.md`

The original Phase-3 document remains historical authority for the accepted first slice and remains authoritative for credential isolation, read-only site mutation boundary, result/error semantics, service isolation and security where not superseded here.

Explicit current owner requirement:

```text
KW-001 roadmap needs optional first-party Webmaster evidence when a client grants access.
Implement the complete official Webmaster evidence surface needed by the roadmap now,
test every affected dependency, and do not require another product retrofit later.
```

## 1. Permanent mutation boundary

`WEBMASTER_API_V1` remains non-destructive with respect to the client site/property.

Still forbidden:

```text
add/delete host
verification mutation
recrawl submission
Sitemap mutation
important-URL mutation
original-text submission
rights/owner mutation
any other site/property write endpoint
```

The one new provider `POST` is **not a site mutation**. It creates an asynchronous analytics export task only:

```text
POST .../pro/serp/queries/download/
```

It is quota-bearing and therefore receives stricter confirmation/recovery rules than ordinary read GETs.

## 2. Enabled Webmaster methods in v0.1.3

```text
listHosts
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

No undocumented/internal Webmaster endpoint is allowed.

## 3. KW-001 roadmap coverage

```text
Step 1 existing-site discovery
→ getIndexingSamples / getInSearchSamples when client access exists

Step 11 page ownership
→ getPopularQueries / getAllQueryHistory / getQueryHistory
→ enhanced query×URL export where needed

Step 12 structural actions
→ query history + query×URL evidence as first-party performance/routing context

Step 13 cannibalization
→ enhanced query×URL×date×region export is the principal historical owned-evidence surface

Step 16 AI evidence
→ no undocumented Alice API is invented;
→ official Webmaster Alice UI evidence remains operator/UI evidence when available;
→ GenSearch remains the repeatable Bridge API path

Step 18 prioritization
→ stored first-party query/history evidence may be reused

Step 20 QA / Step 22 close
→ reconcile any durable export task/result that the job actually used
```

Capability availability is not execution authorization for a concrete provider call.

## 4. Provider mappings

Existing Phase-3 mappings remain unchanged.

Additional ordinary GET resources:

```text
getAllQueryHistory
→ GET /v4/user/{user-id}/hosts/{host-id}/search-queries/all/history

getQueryHistory
→ GET /v4/user/{user-id}/hosts/{host-id}/search-queries/{query-id}/history

getIndexingSamples
→ GET /v4/user/{user-id}/hosts/{host-id}/indexing/samples

getInSearchSamples
→ GET /v4/user/{user-id}/hosts/{host-id}/search-urls/in-search/samples
```

Enhanced export resources:

```text
getExportRegions
→ GET /v4/user/{user-id}/hosts/{host-id}/pro/regions

getExportLimits
→ GET /v4/user/{user-id}/hosts/{host-id}/pro/limits

getExportDates
→ GET /v4/user/{user-id}/hosts/{host-id}/pro/serp/dates

startQueryUrlExport
→ POST /v4/user/{user-id}/hosts/{host-id}/pro/serp/queries/download/

getQueryUrlExportStatus
→ GET /v4/user/{user-id}/hosts/{host-id}/pro/serp/queries/download/{task-id}
```

The provider status can return a temporary download URL on `storage.mds.yandex.net`. The Bridge may fetch that URL only through `collectQueryUrlExport` after strict allowlist validation.

`readQueryUrlExportChunk` is local-only and creates zero network requests.

## 5. History query contract

Allowed history indicators:

```text
TOTAL_SHOWS
TOTAL_CLICKS
AVG_SHOW_POSITION
AVG_CLICK_POSITION
```

Multiple indicators are emitted as repeated `query_indicator=` parameters.

Optional:

```text
deviceTypeIndicator = ALL|DESKTOP|MOBILE_AND_TABLET|MOBILE|TABLET
dateFrom
dateTo
```

`getQueryHistory` additionally requires a non-empty `queryId` and percent-encodes it in the provider path.

## 6. URL sample contract

For `getIndexingSamples` and `getInSearchSamples`:

```text
offset >= 0
limit = 1..100
```

One command performs exactly one provider GET. Pagination is explicit; no hidden auto-pagination.

## 7. Enhanced export start / quota guard

Required start fields:

```text
hostId
1..100 dates[]        # YYYY-MM-DD
1..100 paths[]        # site-relative paths beginning with /
regionIds[] optional
useProTariff boolean; default false
confirmQuota = true
expectedQuotaUnits = paths.length × dates.length
```

Provider payload cardinality guard:

```text
paths.length + dates.length <= 100
```

Local projection:

```text
quota_units = paths.length × dates.length
```

Start is rejected pre-network if `expectedQuotaUnits` does not equal the deterministic projection.

Base mode:

```text
useProTariff = false
quota_units <= 100 per one accepted command
```

PRO mode:

```text
useProTariff = true
AND confirmProTariff = true
```

The Bridge must never silently switch to PRO or infer commercial authorization from ordinary Manual/Autorun enablement.

## 8. Async export lifecycle

The lifecycle is deliberately split into explicit operations:

```text
startQueryUrlExport
→ exactly one POST
→ durable task_id + manifest + quota accounting

getQueryUrlExportStatus
→ exactly one status GET
→ persist IN_PROGRESS | SUCCESS | FAILED

collectQueryUrlExport
→ only after durable SUCCESS + allowlisted download URL
→ exactly one report download GET
→ no OAuth Authorization header sent to storage host

readQueryUrlExportChunk
→ local chrome.storage read only
→ zero network
```

No command hides `status + download` or any other multiple provider initiations behind one command.

## 9. Unknown outcome / replay boundary

For `startQueryUrlExport`:

```text
network/session failure after POST initiation
→ request_executed = UNKNOWN
→ automatic_retry = false
→ no phantom task_id is created locally
→ identical automatic replay forbidden
```

A later operator/ChatGPT reconciliation decision is required before another start.

Status/download network uncertainty is also reported truthfully and never blindly retried by the Bridge.

## 10. Durable export record

Local storage key:

```text
ymb_webmaster_query_url_exports_v1
```

Per task preserve at minimum:

```text
task_id
host_id
start manifest
projection
quota accounting
download_status
safe temporary download URL internally only
created_at / updated_at / collected_at
raw CSV
raw SHA-256
raw byte count
columns
normalized rows
row_count
parse warning if any
```

Never store in that record:

```text
OAuth token
Authorization header
client password/cookie/session secret
```

The temporary storage URL is implementation state and is not echoed into ordinary ChatGPT result text.

## 11. Download allowlist

A report URL is accepted only when all are true:

```text
scheme = https
hostname = storage.mds.yandex.net
pathname starts /get-webmaster-download/
username/password absent
```

Redirect/final response URL must satisfy the same rule.

Manifest permission must be narrow:

```text
https://storage.mds.yandex.net/*
```

Do not use wildcard `*.yandex.net` for this feature.

## 12. CSV preservation / normalization

The full raw report is preserved before analytical chunk delivery.

Recognized semantic fields:

```text
date
host
URL
query
region
clicks
impressions
position
```

Parser requirements:

```text
UTF-8/BOM tolerant
quoted field support
escaped quote support
CRLF/LF support
comma / semicolon / TAB delimiter detection
English/Russian stable header aliases
numeric nullability preserved
```

If the report downloads successfully but required headers cannot be recognized:

```text
raw report + hash + bytes remain preserved
parse_warning is explicit
normalized rows are not fabricated
```

## 13. Large result delivery

The full CSV/row universe must not be forced into one ChatGPT delivery.

`collectQueryUrlExport` returns:

```text
manifest
bounded preview
```

`readQueryUrlExportChunk` returns:

```text
offset
limit <= 500
returned
total
has_more
rows[]
```

Full durable evidence preservation and bounded chat delivery are separate responsibilities.

## 14. Policy compatibility

Webmaster methods remain zero-RUB in Bridge local policy; this does not imply unlimited provider quota.

Default:

```text
manual_enabled = true
autorun_enabled = false
max_requests_per_run = 50
max_cost_rub_per_run = 0
all v0.1.3 methods allowed by default
```

An exact legacy four-method Phase-3 default policy is migrated to the full v0.1.3 default allowlist. A deliberately non-default/custom allowlist remains restrictive.

Webmaster production Autorun remains UI-locked unless separately governed in a future product change. v0.1.3 acceptance does not require enabling Webmaster Autorun.

## 15. AI/Alice boundary

No undocumented Alice-visibility API is added.

```text
Webmaster Alice UI evidence != WEBMASTER_API_V1 provider evidence
GenSearch != consumer Alice
```

This release closes official API gaps needed for owned Yandex Search evidence, not undocumented UI scraping.

## 16. Official authority checked 2026-09-01

```text
https://yandex.ru/dev/webmaster/doc/ru/reference/host-search-queries-history-all
https://yandex.ru/dev/webmaster/doc/ru/reference/host-search-queries-history
https://yandex.ru/dev/webmaster/doc/ru/reference/hosts-indexing-samples
https://yandex.ru/dev/webmaster/doc/ru/reference/hosts-indexing-insearch-samples
https://yandex.ru/dev/webmaster/doc/ru/reference/enhanced-export
https://yandex.ru/dev/webmaster/doc/ru/reference/regions
https://yandex.ru/dev/webmaster/doc/ru/reference/limits
https://yandex.ru/dev/webmaster/doc/ru/reference/dates
https://yandex.ru/dev/webmaster/doc/ru/reference/initialization-export
https://yandex.ru/dev/webmaster/doc/ru/reference/status-retrieval
```

## 17. Acceptance invariant

```text
NEW WEBMASTER CAPABILITY
+ every touched dependency regression
+ exact deterministic package identity
+ source and packaged complete suites
+ installed-extension controlled browser regression
+ zero real Yandex requests during controlled QA
+ no Kwork/job files in Bridge product delta
= candidate eligible for owner live acceptance
```
