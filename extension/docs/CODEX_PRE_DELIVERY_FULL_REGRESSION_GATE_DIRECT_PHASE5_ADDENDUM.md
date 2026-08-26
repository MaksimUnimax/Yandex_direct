# Codex pre-delivery full regression gate — Phase 5 Yandex Direct addendum

Status: **MANDATORY WHEN DIRECT PRODUCT BYTES ARE PRESENT**  
Adopted: 2026-08-26

This addendum extends `CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md` for the Phase-5 Direct first slice. It does not replace any existing core/Phase-1/2/3/4 gate section.

Codex remains an independent QA executor during this gate. Its additional project role as a read-only research agent does not permit changing candidate/product/test/harness bytes during final QA.

## D-00 — authority / exact candidate

Require:

```text
live main reconstructed
Phase-4 closure present
Phase-5 spec/plan/gate read
exact candidate source established
exact handoff ZIP SHA/bytes/files/entries established
exact GitHub artifact transported and round-tripped
zero candidate substitution
zero product/test/harness mutation during final gate
```

Before development starts, accepted Phase-4 `extension/src` tree must be:

```text
fbc52f9a84195278b7b5e942f2a84c7d69778b98
```

## D-01 — registry / prefix / future lock

Before Direct implementation, `DIRECT_API_V1` must remain non-executable. After implementation require exactly one service registration:

```text
service = direct
prefix = DIRECT_API_V1
result = DIRECT_RESULT_V1
```

Unknown service/prefix remains local/no-provider.

## D-02 — protocol strictness

Source and packaged tests must cover:

```text
listCampaigns
listAdGroups
listAds
listKeywords
getCampaignPerformance
missing method
unsupported method
unknown field
credential/header/raw URL injection
Client-Login injection
provider method/service injection
ID validation and cardinality
limit/offset validation
report dates and 31-day local bound
campaignIds report filter bound
```

Arbitrary Direct JSON, provider fields, report fields/filters/headers must reject before provider initiation.

## D-03 — credential isolation

Require five independently addressable service credential records:

```text
Wordstat != Search != Webmaster != Metrika != Direct
```

Direct uses only its dedicated OAuth token and optional saved client_login.

No Direct token/Authorization may appear in commands, public state, result envelopes, errors, diagnostics, DOM text, logs or final evidence.

`client_login` must not leak to normal result/debug evidence.

## D-04 — credential migration / backup

Controlled tests prove:

```text
legacy/current backup without Direct imports safely
new backup carries five service credential records
export/import preserves exact five-way mapping
Direct token/client_login never copied to another service
other OAuth tokens never copied to Direct
blank Direct OAuth Save preserves existing token
common settings Save does not clear Direct token
checksum tamper rejects before mutation
active Manual/Autorun state remains authoritative
runtime transactions never restored
```

## D-05 — Direct Check exactly one request

Controlled stub only. Require exactly one:

```text
POST /json/v501/campaigns
method = get
SelectionCriteria = {}
FieldNames = [Id]
Page = {Limit:1,Offset:0}
```

Headers must be trusted-worker generated:

```text
Authorization: Bearer <fake-token>
Accept-Language: ru
Content-Type: application/json; charset=utf-8
Client-Login only from saved controlled credential when explicitly testing agency context
```

Require:

```text
zero campaigns success → PRESENT
one campaign success → PRESENT
53 invalid token → INVALID_OR_EXPIRED
1002 only with invalid-token context → INVALID_OR_EXPIRED compatibility
54 → NO_ACCESS
58 → APP_ACCESS_NOT_APPROVED
513 → DIRECT_ACCOUNT_MISSING
3000 → NO_API_ACCESS
152 → UNITS_EXHAUSTED
506 → CONCURRENCY_LIMIT
network unknown → UNKNOWN / no retry
```

`automatic_retry=false` always. Real Direct credentials/traffic forbidden.

## D-06 — policy defaults

Require:

```text
manual_enabled = true
autorun_enabled = false
allowed_methods = listCampaigns,listAdGroups,listAds,listKeywords,getCampaignPerformance
max_requests_per_run = 20
max_page_size = 1000
max_report_days = 31
max_report_rows = 1000
method_cost_rub = 0
max_cost_rub_per_run = 0
```

Local limits must not be described as provider quotas.

## D-07 — listCampaigns provider path

Controlled request must use:

```text
POST /json/v501/campaigns
provider method get
fixed FieldNames = Id,Name,StartDate,EndDate,Type,Status,State,Currency
Page Limit/Offset bounded locally
SelectionCriteria.Ids only when campaignIds supplied
```

Require exactly one provider request and allowlisted normalization.

Forbidden provider fields must not leak, including funds, notification email, manager/agency and type-specific campaign structures.

## D-08 — listAdGroups provider path

Require local selector:

```text
campaignIds OR adGroupIds
```

Provider fixed common fields only:

```text
Id,Name,CampaignId,Status,ServingStatus,Type
```

Exactly one provider request. No type-specific group structures.

## D-09 — listAds provider path

Require at least one:

```text
campaignIds OR adGroupIds OR adIds
```

Fixed fields:

```text
Id,CampaignId,AdGroupId,Status,State,Type,Subtype
```

Exactly one request. No creative text/URL/tracking/ERIR/type-specific payload requested or returned.

## D-10 — listKeywords provider path / Units restraint

Require one selector set and fixed fields only:

```text
Id,Keyword,State,Status,ServingStatus,AdGroupId,CampaignId,Bid,ContextBid,StrategyPriority
```

Must prove provider request does NOT contain:

```text
Productivity
StatisticsSearch
StatisticsNetwork
```

`Bid` and `ContextBid` normalized as exact integer micros.

Exactly one provider request.

## D-11 — campaign Reports online-only path

Controlled request:

```text
POST /json/v501/reports
processingMode: online
skipReportHeader: true
skipReportSummary: true
returnMoneyInMicros:false ABSENT
skipColumnHeader ABSENT
ReportType = CAMPAIGN_PERFORMANCE_REPORT
DateRangeType = CUSTOM_DATE
Format = TSV
IncludeVAT = YES
FieldNames = Date,CampaignId,CampaignName,Impressions,Clicks,Cost
Page.Limit <= 1000
```

If campaign IDs supplied, only trusted `CampaignId IN [...]` filter may be constructed.

Require:

```text
one command = one report request
valid TSV exact expected columns
cost parsed as integer cost_micros
no offline queue
no polling
no repeat request
```

## D-12 — Reports async/offline future lock

Controlled fixtures for HTTP 201 and 202 must be terminal first-slice outcomes:

```text
no retryIn scheduling
no queue polling
no repeated same report request
automatic_retry=false
```

`processingMode=offline` and `auto` must be impossible from assistant payload and normal first-slice runtime.

`SEARCH_QUERY_PERFORMANCE_REPORT` must be unavailable.

## D-13 — Direct provider semantic errors

Controlled fixtures cover at least:

```text
53
54
55
58
152
506
513
1002 generic/non-token context
1002 verified invalid-token context
3000
4000
4001
4002
8000
500/server failure
malformed JSON
```

Semantic JSON error must never normalize as `DIRECT_RESULT_V1 status=OK` merely because HTTP is 200.

Any received HTTP response means `request_executed=true`.

## D-14 — unknown outcome / no blind retry

Controlled network interruption after initiation:

```text
request_executed = UNKNOWN
automatic_retry = false
no replay of provider POST
```

This applies to both JSON object services and Reports.

## D-15 — RequestId / Units truth

Fixtures must prove:

```text
RequestId preserved when present
Units x/y/z parsed as integer spent/remaining/daily_limit
missing Units → no fabricated values
malformed Units → no fabricated values
Units-Used-Login not emitted to ordinary results/logs
Direct Units never represented as RUB
```

At minimum include a low-remaining-Units response and prove it is reported truthfully without hidden retry.

## D-16 — service isolation

Require all directions:

```text
active non-Direct + DIRECT_API_V1 → SERVICE_NOT_ACTIVE / zero Direct traffic
active Direct + WORDSTAT_API_V1 → zero Direct traffic
active Direct + SEARCH_API_V1 → zero Direct traffic
active Direct + WEBMASTER_API_V1 → zero Direct traffic
active Direct + METRIKA_API_V1 → zero Direct traffic
```

Credential isolation proven independently of routing.

## D-17 — Manual lifecycle

Installed-extension qualified browser/runtime coverage against controlled Direct provider must prove:

```text
one eligible DIRECT_API_V1 block → exactly one Yandex action
click → one Manual admission
operation active → action disabled/non-clickable
delivery active → action disabled/non-clickable
blocked click → no second execution
completion → action re-enabled
one admitted command → at most one provider request
```

At minimum exercise `listCampaigns` and `getCampaignPerformance` through the real installed-extension lifecycle.

Existing lifecycle regressions remain mandatory.

## D-18 — popup / credentials / convenience save / geometry

Qualified Chrome/Puppeteer must prove:

```text
popup remains 430×560
Direct exists in active-service selector
OAuth input masked
Client login optional field present with agency-only explanation
Save and Check distinct
saved OAuth absent from visible DOM after rerender
Check warning mentions one Campaigns.get and Direct Units
service switching preserves all credentials
Direct policy remains within internal scroll
top common-settings Save control exists near service selector
bottom common-settings Save still exists
both invoke the same handler/state path and produce equivalent saved state
```

The convenience top button must not introduce a second worker/state lifecycle.

## D-19 — Export/Import UI

Browser test must export/import controlled secret-bearing backup and prove:

```text
Wordstat restored to Wordstat
Search restored to Search
Webmaster restored to Webmaster
Metrika restored to Metrika
Direct token/client_login restored to Direct
no cross-service overwrite
checksum enforced
```

Never print secret values in final evidence.

## D-20 — Autorun default lock / controlled enablement

Require:

```text
Direct Autorun default OFF
start while disabled → local AUTORUN_DISABLED / zero provider
controlled explicit enable → one safe first-slice read may run
active service immutable
one fingerprint admission
one provider request
one delivery
no duplicate execution
pause/resume/finish unchanged
```

No Direct mutation method can be registered or policy-enabled.

## D-21 — write/future surface lock

Source and packaged negative tests prove local zero-provider rejection for attempts to invoke:

```text
add/update/delete
campaign suspend/resume/archive/unarchive
ad moderate/suspend/resume/archive/unarchive
keyword add/update/delete/suspend/resume
bid set/setAuto/setBids
finance/payment operations
Payment-Token
Use-Operator-Units
AgencyClients mutations
Feeds mutations
Strategies mutations
offline/auto Reports
SEARCH_QUERY_PERFORMANCE_REPORT
arbitrary/custom report constructor
arbitrary FieldNames/SelectionCriteria/report filters/headers/raw provider URL
```

## D-22 — cleanliness / final acceptance

Final campaign requires:

```text
real_credentials_used = NO
real_yandex_direct_requests = 0
production_modified_during_gate = NO
package_tests_modified_during_gate = NO
direct_harness_modified_during_gate = NO
source_workspace_clean = PASS
transport_workspace_clean = PASS
enabled_not_run_sections = 0
PRODUCT_BYTES_POST_TEST = IDENTICAL
```

All still-applicable permanent/core/Phase-1/2/3/4 gates remain mandatory.

## Final report extension

A PASS campaign containing Direct must report:

```text
D-00: PASS
D-01: PASS
...
D-22: PASS
direct_controlled_provider_requests: <actual integer>
direct_real_yandex_requests: 0
direct_real_credentials_used: NO
NOT_RUN_COUNT=0
PRODUCT_BYTES_POST_TEST=IDENTICAL
```

No enabled Direct section may be `NOT_RUN` in PASS.

## Owner-live boundary after exact Codex PASS

Owner-live remains outside controlled pre-delivery QA and is intentionally narrow:

```text
1. verify OAuth application includes direct:api
2. verify approved full Direct API access for production testing
3. save one dedicated real Direct OAuth token
4. save Client-Login only if owner is using an agency-client account context
5. Check exactly once
6. listCampaigns exactly once
7. if real campaign exists, at most one bounded downstream object read if needed
8. getCampaignPerformance exactly once for a short period if real report data exists and online generation succeeds
```

No mutation, bidding, finance, quota/concurrency/error testing, offline queue or report polling against real Direct.
