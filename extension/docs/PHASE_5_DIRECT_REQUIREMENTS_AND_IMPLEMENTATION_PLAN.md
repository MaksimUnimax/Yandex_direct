# Phase 5 — Yandex Direct requirements and implementation plan

Status: **RECONSTRUCTION COMPLETE / IMPLEMENTATION PLAN READY**  
Date: 2026-08-26

Authority:

```text
CURRENT_STATE.md
ROADMAP.md
PROJECT_PURPOSE.md
SPECIFICATION.md
SPECIFICATION_PHASE_5_DIRECT_ADDENDUM.md
WORKFLOW_OPERATING_RULES.md
CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md
```

No production implementation may exceed the Phase-5 first slice defined here without a governed contract update first.

## 1. Reconstruction result

Current official Direct API uses OAuth 2.0 and HTTPS POST requests to per-service JSON endpoints.

Production service base pattern:

```text
https://api.direct.yandex.com/json/v501/{service}
```

Required OAuth data source:

```text
direct:api
```

Real production requests additionally require an approved Direct API access request for the OAuth application. Trial access is Sandbox-only.

Phase-5 first slice:

```text
listCampaigns
listAdGroups
listAds
listKeywords
getCampaignPerformance
```

Every first-slice operation is read-only. Provider write/mutation methods remain unavailable even though the Direct OAuth scope itself can authorize broader account actions.

## 2. Product baseline rule

Implementation starts only after this Phase-5 contract package lands on live `main`.

Before creating the dev branch:

```text
fetch exact live main HEAD
verify extension/src tree = fbc52f9a84195278b7b5e942f2a84c7d69778b98
verify no uncontrolled product change since accepted Phase-4 source
```

Do not develop from historical Phase-4 candidate or QA branches.

## 3. Dedicated Direct credential

Extend the service credential foundation with:

```text
credentials.direct = {
  oauth_token,
  client_login,
  checked_at,
  check_state
}
```

Requirements:

```text
Direct runtime reads only Direct credential
no implicit Metrika/Webmaster token reuse
blank masked OAuth Save preserves current Direct token
partial common-settings Save never clears Direct token
client_login blank is valid for ordinary advertiser accounts
client_login is used only as trusted Client-Login header when nonblank
Direct OAuth token/Authorization never appears in public state/DOM/logs/evidence
```

Credential status needs explicit Direct-specific outcomes at minimum:

```text
PRESENT
MISSING
INVALID_OR_EXPIRED
NO_ACCESS
APP_ACCESS_NOT_APPROVED
DIRECT_ACCOUNT_MISSING
NO_API_ACCESS
UNITS_EXHAUSTED
CONCURRENCY_LIMIT
NETWORK_ERROR
```

Do not broaden global credential semantics in a way that regresses existing services; adapter-specific mapping is acceptable.

## 4. Backup/import migration

Extend the accepted Backup V3 or current governed version only as required for the fifth service.

Mandatory compatibility:

```text
old backup without Direct → imports without erasing current/default Direct record
new backup → carries five service mappings
Direct token/client_login remain in Direct only
no service credential overwrites another
checksum tamper rejects before mutation
active conversation/Manual/Autorun safety state remains authoritative
runtime transactions are never restored
```

If a version bump is required, add migration tests before the bump.

## 5. Direct protocol module

Add expected module:

```text
extension/src/shared/direct_protocol.js
```

Responsibilities:

```text
parse DIRECT_API_V1
strict method/field allowlists
safe positive integer ID arrays
bounded array cardinality
limit/offset validation
YYYY-MM-DD report date validation
31-day local report span guard
safe normalized result/error envelopes
provider semantic error normalization
Units header normalization helper if appropriate
zero credential/header/provider-URL knowledge in assistant payload
```

No assistant-provided raw Direct JSON request body is accepted.

## 6. Registry/core integration

Add exactly one service registration:

```text
DIRECT: direct
prefix: DIRECT_API_V1
result: DIRECT_RESULT_V1
```

Update unified service enumerations and routing where required:

```text
service registry
block command discovery
credential registry/store/runtime
policy registry
worker router/provider runtime
public state
popup selector
Manual service admission
Autorun service ownership
backup/export/import
service isolation tests
```

Unknown services/prefixes remain fail-closed.

## 7. Trusted Direct provider runtime

Add a dedicated trusted provider module, conceptually:

```text
extension/src/shared/phase5_provider_runtime.js
```

and worker integration equivalent to the proven Phase-3/4 provider-runtime pattern.

Common request rules:

```text
validation + credential + policy before fetch
HTTPS production host constructed only by trusted code
Authorization: Bearer built only in trusted worker
Accept-Language: ru fixed by trusted code
Content-Type JSON fixed by trusted code
Client-Login derived only from saved Direct credential
Use-Operator-Units absent
Payment-Token absent
one admitted command = one provider request
no hidden credential Check
no automatic retry
```

Controlled tests must redirect/replace the provider boundary to a local fixture and prove zero real Yandex traffic.

## 8. listCampaigns implementation

Build:

```text
POST https://api.direct.yandex.com/json/v501/campaigns
{
  "method":"get",
  "params":{
    "SelectionCriteria": {"Ids": [...]}, // omitted/empty if no IDs
    "FieldNames":["Id","Name","StartDate","EndDate","Type","Status","State","Currency"],
    "Page":{"Limit":...,"Offset":...}
  }
}
```

Normalize only:

```text
id,name,start_date,end_date,type,status,state,currency
limited_by
provider_request_id
provider_units
```

Do not normalize/provider-leak Funds, notifications, manager/agency, negative keywords or type-specific campaign data.

## 9. listAdGroups implementation

Require at least one local selector:

```text
campaignIds OR adGroupIds
```

Build trusted fixed FieldNames:

```text
Id,Name,CampaignId,Status,ServingStatus,Type
```

No type-specific group fields.

## 10. listAds implementation

Require at least one:

```text
campaignIds OR adGroupIds OR adIds
```

Fixed common FieldNames only:

```text
Id,CampaignId,AdGroupId,Status,State,Type,Subtype
```

Do not request creative bodies, href/tracking fields, type-specific substructures or current combinatorial/responsive creative payloads.

## 11. listKeywords implementation

Require one selector set:

```text
campaignIds OR adGroupIds OR keywordIds
```

Fixed FieldNames:

```text
Id,Keyword,State,Status,ServingStatus,AdGroupId,CampaignId,Bid,ContextBid,StrategyPriority
```

Do not request:

```text
Productivity
StatisticsSearch
StatisticsNetwork
AutotargetingSettings categories/brands
```

Normalize bid values as exact integer micros.

## 12. getCampaignPerformance implementation

Trusted Reports request:

```text
POST https://api.direct.yandex.com/json/v501/reports
processingMode: online
skipReportHeader: true
skipReportSummary: true

params.ReportType = CAMPAIGN_PERFORMANCE_REPORT
params.DateRangeType = CUSTOM_DATE
params.Format = TSV
params.IncludeVAT = YES
params.FieldNames = [Date,CampaignId,CampaignName,Impressions,Clicks,Cost]
params.Page.Limit <= 1000
```

If `campaignIds` are supplied, trusted code constructs exactly one `CampaignId IN [...]` filter.

ReportName is generated internally and must not include credentials/account login. Example safe form:

```text
YMB-P5-<operation-id>
```

Keep column header; parse TSV by strict expected-column match. Reject malformed/mismatched report before presenting it as valid data.

Because `returnMoneyInMicros:false` is intentionally omitted, parse `Cost` as integer micros and expose `cost_micros`.

Online-only behavior:

```text
200 + valid TSV → success
provider online-generation error → terminal provider error, no retry
201/202 → unexpected/non-first-slice async outcome, terminal, no polling
network unknown → UNKNOWN, no replay
```

## 13. Direct Check

Against controlled stub during development/final QA, Direct Check must create exactly one `Campaigns.get` request with `Limit=1` and `FieldNames=[Id]`.

No campaign returned is still a valid capability proof.

Provider semantic mapping must include:

```text
53 invalid token → INVALID_OR_EXPIRED
1002 + verified invalid-token context/message → INVALID_OR_EXPIRED compatibility
54 → NO_ACCESS
58 → APP_ACCESS_NOT_APPROVED
513 → DIRECT_ACCOUNT_MISSING
3000 → NO_API_ACCESS
152 → UNITS_EXHAUSTED
506 → CONCURRENCY_LIMIT
8000 → PROVIDER_INVALID_REQUEST
```

Never retry Check automatically. UI must state that a real owner-live Check spends Units.

## 14. Direct Units accounting

Parse `Units` response header format:

```text
spent/remaining/daily_limit
```

Strictly numeric nonnegative integer components only. If absent/malformed, do not fabricate values; expose null/unknown metadata.

Normal result metadata may include:

```text
provider_request_id
provider_units.spent
provider_units.remaining
provider_units.daily_limit
```

Do not expose `Units-Used-Login` in normal result or logs.

Do not represent provider Units as RUB. Existing cost ledger remains RUB=0 for Direct first slice; Direct points are a separate provider-capacity truth.

## 15. Policy

Default Direct policy:

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

Local request limit `20` is intentionally conservative and is not documented as a provider quota.

No automatic retry for Units exhaustion, concurrency or provider/server errors.

## 16. Provider/error fixture matrix

Controlled fixtures must cover at minimum:

```text
200 successful Campaigns.get empty
200 successful Campaigns.get populated + LimitedBy
200 successful AdGroups.get
200 successful Ads.get with current ad Type/Subtype values
200 successful Keywords.get
200 valid Reports TSV
200 malformed Direct JSON
200 JSON semantic error 53
200/4xx semantic error 58
semantic 54 / 513 / 3000 / 152 / 506 / 8000 / 4001 / 4002
500 provider/server response
network unknown after initiation
Reports 201 and 202 terminal/no-poll handling
Reports invalid TSV/header mismatch
Reports online-mode cannot-generate error
```

Do not assume provider semantic errors always correspond to a specific HTTP status; parse body truth when available.

## 17. Protocol validation matrix

Common pre-fetch rejection:

```text
missing method
unsupported method
unknown field
token/Authorization/header supplied in command
raw URL supplied
provider method/service supplied
Client-Login supplied in command
wrong active service
Direct credential missing
Manual disabled
Autorun disabled
request budget exhausted
```

ID arrays:

```text
empty array where selector required
0 / negative / float / unsafe integer
string IDs if protocol requires integer
array over local bound
duplicate handling deterministic
```

Page:

```text
limit <1
limit >1000
offset <0
non-integer values
```

Reports:

```text
invalid date format
dateFrom > dateTo
span >31 days
campaignIds >10
limit >1000
arbitrary report field/filter/header injection
```

Every local validation failure must prove zero provider traffic.

## 18. Response normalization

Mandatory assertions:

```text
Campaigns allowlist only governed fields
AdGroups allowlist only governed common fields
Ads omit creative/type-specific payloads
Keywords omit productivity/statistics fields
bid/context bid remain exact micros
LimitedBy preserved as pagination truth
RequestId preserved when present
Units parsed without Units-Used-Login leakage
semantic error body never normalized as success
TSV exact columns required
TSV rows preserve Date/Campaign mapping
Cost parsed as integer micros
```

## 19. Service/credential isolation

Routing isolation all directions:

```text
active non-Direct + DIRECT_API_V1 → local SERVICE_NOT_ACTIVE / zero Direct fetch
active Direct + WORDSTAT_API_V1 → zero Direct fetch
active Direct + SEARCH_API_V1 → zero Direct fetch
active Direct + WEBMASTER_API_V1 → zero Direct fetch
active Direct + METRIKA_API_V1 → zero Direct fetch
```

Credential isolation must independently prove five service records remain stable across save/check/switch/export/import.

## 20. Popup/UI

Preserve `430×560` native popup geometry.

Direct credential card:

```text
OAuth token masked
Client login optional text input
Save
Check
status
warning: Check performs exactly one read-only Campaigns.get and spends Direct Units
```

Direct policy panel uses existing internal scroll model.

Implement the owner-requested top convenience save button during Phase-5 UI change:

```text
place a duplicate UI control near active-service selection/binding controls
label = same/common-save meaning
invoke the SAME existing common-settings save handler/state path
no duplicated save logic
no separate storage transaction model
both top and bottom save buttons remain behaviorally equivalent
```

This UI convenience is not an authorization to alter Manual worker lifecycle or service-switch semantics.

## 21. Browser/runtime coverage

Installed-extension qualified browser coverage against controlled Direct fixture must prove:

```text
Direct appears in service selector
Direct OAuth Save hides secret after rerender
Client login persists independently
Direct Check exactly one Campaigns.get
empty Campaigns success accepted
Manual listCampaigns exactly one provider request
Manual getCampaignPerformance exactly one provider request
operation/delivery button gating blocks duplicate execution
top and bottom common-save controls use same state path
service switching preserves all five credential records
Backup export/import preserves Direct mapping
popup remains 430×560
real Yandex requests = 0
```

Network boundary must fail closed to controlled endpoints only.

## 22. Autorun

Default Direct Autorun OFF.

Controlled explicit enablement may exercise one safe first-slice read and must prove:

```text
immutable active service
single fingerprint admission
one provider request
one delivery
no duplicate execution
pause/resume/finish semantics preserved
```

No Direct mutation can ever be selected by the registry/policy.

## 23. Gate / freeze / transport

Before freeze:

```text
focused tests PASS
complete applicable Wordstat/Search/Webmaster/Metrika/core regressions PASS
qualified popup/browser Direct route PASS
Direct lifecycle browser proof PASS
no real credentials
no real Yandex traffic
```

Then:

```text
freeze exact candidate
deterministic package identity
manifest/SHA/bytes/files/entries recorded
GitHub artifact transport round-trip
independent Codex full applicable campaign
no product/test/harness mutation during final gate
NOT_RUN_COUNT=0 for PASS
```

## 24. Owner-live boundary

Only after immutable candidate + independent full PASS:

```text
A. confirm direct:api on the OAuth app
B. confirm Direct access request status; production test requires approved full access
C. save dedicated Direct token
D. leave client_login blank unless this account is an agency acting for a client
E. Check once
F. listCampaigns once
G. if campaign exists, one bounded downstream list read if needed
H. one short getCampaignPerformance online report if real data exists
```

No writes, bidding changes, financing, error/quota tests, offline queue, polling or repeated exploratory requests.

## 25. Implementation order

```text
A. land Phase-5 contract docs on main
B. fetch new live main and verify Phase-4 accepted src tree unchanged
C. create Phase-5 dev branch from exact main
D. add Direct credential + backup migration
E. add DIRECT_API_V1 protocol + registry/policy
F. add trusted Direct provider runtime and semantic error/Units handling
G. add four object reads + one online Reports route
H. add bounded Direct popup UI + duplicated common-save convenience button using same handler
I. add focused/unit/integration tests
J. add controlled installed-browser/lifecycle tests
K. run development verification
L. freeze exact candidate
M. exact artifact transport round-trip
N. independent Codex full applicable campaign
O. narrow owner-live acceptance
P. close Phase 5 only after live PASS
```
