# Codex pre-delivery full regression gate — Webmaster v0.1.3 addendum

Status: **MANDATORY FOR v0.1.3 WEBMASTER FULL READ/EXPORT CANDIDATE**  
Adopted: 2026-09-01

This file extends `CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md` and supersedes the **first-slice-only** assertions of `CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_WEBMASTER_PHASE3_ADDENDUM.md` for product version 0.1.3.

The old Phase-3 gate remains applicable to all unchanged credential, original-method, service-isolation, Manual/core, popup, backup and security invariants. Specifically, old W-18 must no longer reject official enhanced analytics export; it continues to reject all client-site/property mutation endpoints.

## WM13-00 — authority / separation / exact identity

Require:

```text
source branch derives from live main product authority
Bridge/Kwork separation = PASS
changed product/test docs limited to extension/**
Kwork job/methodology product leakage = 0
manifest/product/package version = 0.1.3
exact handoff ZIP SHA/bytes/files/entries established
source↔package identity = PASS
```

## WM13-01 — original Phase-3 compatibility

Source and packaged tests must prove unchanged semantics for:

```text
listHosts
getSummary
getDiagnostics
getPopularQueries
OAuth + derived user_id
WEBMASTER_RESULT_V1
no credential leakage
one command = one external provider initiation
no blind retry
```

## WM13-02 — new protocol strictness

Cover every v0.1.3 method:

```text
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

Require unknown fields/methods/enums/ranges/dates/task IDs rejected pre-network.

## WM13-03 — query-history routes and normalization

Controlled fixtures prove:

```text
all/history exact GET route
{query-id}/history exact GET route
repeated query_indicator encoding
query-id percent encoding
date/device filters
stable indicator normalization
one command = one GET
```

## WM13-04 — URL sample routes

Controlled fixtures prove:

```text
indexing/samples
search-urls/in-search/samples
offset >= 0
limit 1..100
one command = one GET
only stable analysis fields retained
```

## WM13-05 — export discovery

Controlled fixtures prove exact single-GET resources:

```text
/pro/regions
/pro/limits
/pro/serp/dates
```

No hidden start/status/download occurs during discovery.

## WM13-06 — deterministic quota projection / confirmation

Require:

```text
quota_units = paths × dates
confirmQuota=true mandatory
expectedQuotaUnits exact match mandatory
paths + dates <= 100
BASE start >100 projected units rejected
useProTariff defaults false
useProTariff=true requires confirmProTariff=true
PRO never inferred from generic Manual/Autorun permission
```

All rejection paths = zero provider requests.

## WM13-07 — export start boundary

Controlled fixture:

```text
exactly one POST
exact official initialization route
OAuth only to api.webmaster.yandex.net
body dates/paths/region_ids/use_pro_tariff exact
task_id + quota accounting persisted durably
OAuth never persisted in job
request_executed=true on received response
automatic_retry=false
```

Network fault after initiation:

```text
request_executed=UNKNOWN
automatic_retry=false
no automatic second POST
no fabricated local task_id
```

## WM13-08 — durable status

Controlled fixture:

```text
one explicit status GET per command
IN_PROGRESS persisted
SUCCESS persisted
FAILED persisted and delivered as failure evidence
host/task mismatch rejected
```

Temporary URL must not be echoed to ordinary ChatGPT result text.

## WM13-09 — storage download security

Require URL allowlist:

```text
https only
host exactly storage.mds.yandex.net
path starts /get-webmaster-download/
no credentials in URL
redirect/final URL revalidated
manifest permission narrow
```

Non-Yandex/unsafe URL is rejected without fetching it.

`collectQueryUrlExport` sends no Webmaster OAuth token/Authorization header to storage host.

## WM13-10 — CSV/raw preservation

Controlled report must prove:

```text
quoted CSV fields
escaped quotes
LF/CRLF
comma/semicolon/TAB detection
required field mapping
raw CSV retained
raw SHA-256 retained
raw byte count retained
row_count exact
parse warning explicit instead of invented rows
```

## WM13-11 — bounded delivery / local chunks

Require:

```text
collect returns manifest + bounded preview
readQueryUrlExportChunk limit <= 500
chunk is deterministic by offset/limit
local chunk request_executed=false
local chunk creates zero network requests
full raw/result remains durable across multiple reads
```

## WM13-12 — dependency regression

Must execute all currently applicable tests for code paths v0.1.3 touches transitively:

```text
Phase-3 Webmaster compatibility
Phase-4 Metrika delegation
Phase-5 Direct delegation
credential concurrency/isolation
policy normalization/migration
settings backup/import
service registry/routing
Manual/common delivery lifecycle
Search Batch accepted v0.1.2 nextN behavior
Wordstat/Search existing protocols
```

The complete top-level Node suite must pass in source and again after extraction from exact candidate ZIP.

## WM13-13 — popup/browser

Qualified Chrome for Testing + Puppeteer on installed extension must prove at minimum:

```text
extension loads as MV3
popup = 430×560
five service selector preserved
Webmaster OAuth input masked
Save and Check distinct
Webmaster Check = exactly one controlled GET /v4/user
fake token not rendered/logged
v0.1.3 Webmaster policy survives common Save without shrinking to legacy four methods
Metrika/Direct/Wordstat/Search UI unaffected
```

## WM13-14 — controlled provider browser runtime

With service-worker fetch replaced by a controlled stub and **zero real Yandex traffic**, prove representative new Webmaster calls through the actually installed extension:

```text
query history
export limits/dates/regions
one BASE start POST
durable task state
one status GET
one allowlisted storage download GET
local chunk with zero fetch
```

Browser fixture must count provider boundaries exactly and assert OAuth is used only on Webmaster API host.

## WM13-15 — common Manual lifecycle regression

Because v0.1.3 changes service protocol/provider bytes but not common action/composer code, require:

```text
existing installed-extension Manual lifecycle harness PASS
one action/admission
busy disable/no second dispatch
completion re-enable
no duplicate provider initiation
no delivery replay
```

A representative Webmaster Manual command must additionally pass deterministic worker/provider integration. Existing Direct/common lifecycle evidence alone cannot replace all Webmaster provider assertions, but it can prove unchanged common lifecycle code.

## WM13-16 — package determinism / immutability

Require:

```text
canonical packer executable
build A == build B byte-for-byte
ZIP integrity PASS
full file SHA manifest
fresh extraction matches every source file hash/byte count
source full suite PASS
packaged full suite PASS
product bytes unchanged during browser/final QA
```

## WM13-17 — real-request boundary

Controlled development/pre-delivery QA:

```text
real_credentials_used = NO
real_yandex_requests = 0
PRO_tariff_used = NO
owner_site_modified = NO
```

Owner live acceptance is separate and minimal. Any actual BASE export start must be explicitly authorized with its exact projected quota units before the command is issued.

## WM13-18 — final result requirements

Final candidate is not handoff-ready unless:

```text
all enabled parent PD sections = PASS
all applicable old Webmaster sections = PASS under v0.1.3 supersession
WM13-00..WM13-17 = PASS
enabled_not_run_sections = 0
exact artifact identity remains unchanged
```

Final report must list each touched production file and, for each, the affected dependency surfaces and concrete tests proving no regression.
