# Specification addendum — Phase 5 Yandex Direct

Status: **RECONSTRUCTION COMPLETE / FIRST SLICE DEFINED**  
Date: 2026-08-26

This addendum extends the unified Yandex Marketing Bridge specification after Phase 4 Metrika closure. It defines the contract boundary for the first Phase-5 Yandex Direct slice. No implementation may exceed this slice without a governed contract update.

## 1. Authority and no-guess rule

Reconstruction was performed from current official Yandex Direct API documentation. Missing or contradictory provider facts must follow the project research escalation rule in `PROJECT_PURPOSE.md` and `ROADMAP.md`; they must never be silently guessed.

Official references checked 2026-08-26:

```text
https://yandex.ru/dev/direct/doc/ru/concepts/overview
https://yandex.ru/dev/direct/doc/ru/concepts/format
https://yandex.ru/dev/direct/doc/ru/concepts/headers
https://yandex.ru/dev/direct/doc/ru/concepts/access
https://yandex.ru/dev/direct/doc/ru/concepts/register
https://yandex.ru/dev/direct/doc/ru/concepts/auth-token
https://yandex.ru/dev/direct/doc/ru/register
https://yandex.ru/dev/direct/doc/ru/access-request
https://yandex.ru/dev/direct/doc/ru/concepts/units
https://yandex.ru/dev/direct/doc/ru/concepts/errors-list
https://yandex.ru/dev/direct/doc/ru/campaigns/get
https://yandex.ru/dev/direct/doc/ru/adgroups/get
https://yandex.ru/dev/direct/doc/ru/ads/get
https://yandex.ru/dev/direct/doc/ru/keywords/get
https://yandex.ru/dev/direct/doc/ru/reports
https://yandex.ru/dev/direct/doc/ru/headers
https://yandex.ru/dev/direct/doc/ru/mode
https://yandex.ru/dev/direct/doc/ru/spec
https://yandex.ru/dev/direct/doc/ru/type
https://yandex.ru/dev/direct/doc/ru/fields-list
https://yandex.ru/dev/direct/doc/ru/restrictions
```

Current production JSON service pattern:

```text
https://api.direct.yandex.com/json/v501/{service}
```

Reports JSON endpoint:

```text
https://api.direct.yandex.com/json/v501/reports
```

All Direct API requests in this slice use HTTPS POST. `get` is read-only at the provider semantic level even though the transport method is POST.

## 2. Access prerequisite and authorization

Real Direct API requests require both:

```text
OAuth application scope = direct:api
approved Yandex Direct API access request for the OAuth application
```

Trial access is Sandbox-only. Real production data requires full access.

The OAuth token is sent only by the trusted worker:

```text
Authorization: Bearer <token>
```

Optional/common trusted headers:

```text
Accept-Language: ru
Content-Type: application/json; charset=utf-8
```

`Client-Login` is required only when an agency makes a request for an advertiser client. It is never supplied by assistant command text.

`Use-Operator-Units: true` is locked out of the Phase-5 first slice. `Payment-Token` and all finance-token surfaces are locked.

`passport:business` is not a universal Direct requirement. It is relevant when authorization on behalf of a Yandex ID organization is required and therefore remains an account-specific setup concern, not an unconditional Bridge prerequisite.

## 3. Service identity

```text
service = direct
protocol prefix = DIRECT_API_V1
result prefix = DIRECT_RESULT_V1
```

No `DIRECT_API_V1` command may be executed by Wordstat, Search, Webmaster or Metrika adapters.

## 4. Credential model

Direct gets a dedicated service credential record:

```text
credentials.direct = {
  oauth_token,
  client_login,
  checked_at,
  check_state
}
```

Rules:

```text
Direct reads only credentials.direct
no implicit reuse of Webmaster OAuth
no implicit reuse of Metrika OAuth
no cross-service token fallback
client_login is optional and blank for a normal non-agency advertiser
raw OAuth token is secret
Authorization header is secret
client_login must not be echoed in normal results/diagnostics by default
```

A user may manually paste the same physical OAuth token into multiple service records only if they deliberately obtained a token carrying the necessary grants. The Bridge never assumes or performs that sharing.

Public state may expose only non-secret capability metadata such as:

```text
has_oauth_token
has_client_login
checked_at
check_state
```

## 5. Direct credential Check

Explicit Direct Check performs exactly one read-only Direct API call and consumes provider Units:

```text
POST https://api.direct.yandex.com/json/v501/campaigns
Authorization: Bearer <token>
Accept-Language: ru
Content-Type: application/json; charset=utf-8
[Client-Login only when a saved agency client_login exists]

{
  "method": "get",
  "params": {
    "SelectionCriteria": {},
    "FieldNames": ["Id"],
    "Page": {"Limit": 1, "Offset": 0}
  }
}
```

Interpretation:

```text
provider success with one or zero Campaigns → PRESENT / valid Direct read capability
provider error code 53 or provider error code 1002 when used for invalid-token semantics → INVALID_OR_EXPIRED
provider error 54 → NO_ACCESS
provider error 58 → APP_ACCESS_NOT_APPROVED
provider error 513 → DIRECT_ACCOUNT_MISSING
provider error 3000 → NO_API_ACCESS
provider error 152 → UNITS_EXHAUSTED
provider error 506 → CONCURRENCY_LIMIT
network unknown after initiation → NETWORK_ERROR_UNKNOWN / no automatic retry
```

Official Yandex pages currently conflict on invalid-token error code: the error table identifies code `53`, while the authorization-token page links invalid token to `1002`. The Bridge therefore treats `53` as the canonical explicit invalid-token code and also accepts `1002` as compatibility-invalid only when provider context/message identifies token invalidity. Generic code `1002` must not be blindly remapped without context.

No hidden Direct Check runs before ordinary Direct commands.

## 6. Phase-5 first-slice methods

Exactly five methods are enabled:

```text
listCampaigns
listAdGroups
listAds
listKeywords
getCampaignPerformance
```

All are read-only. All Direct mutations remain locked.

### 6.1 listCampaigns

Provider mapping:

```text
POST /json/v501/campaigns
provider method = get
```

Allowed assistant fields:

```text
method
campaignIds
limit
offset
```

Local rules:

```text
campaignIds optional, positive safe integers, max 10 in first slice
limit default 100, 1..1000
later page offset default 0, integer >= 0
```

Trusted provider request uses only:

```text
SelectionCriteria.Ids when campaignIds supplied
FieldNames = [Id,Name,StartDate,EndDate,Type,Status,State,Currency]
Page = {Limit,Offset}
```

Provider supports up to 10,000 returned objects and up to 1000 campaign IDs in SelectionCriteria; the lower Bridge limits are deliberate local safety bounds.

Normalized result:

```text
campaigns[] = {
  id,
  name,
  start_date,
  end_date,
  type,
  status,
  state,
  currency
}
limited_by
```

No funds, notification email, manager/agency identity, negative-keyword arrays or type-specific strategy structures are returned in the first slice.

### 6.2 listAdGroups

Provider mapping:

```text
POST /json/v501/adgroups
provider method = get
```

Allowed fields:

```text
method
campaignIds
adGroupIds
limit
offset
```

At least one of `campaignIds` or `adGroupIds` is required.

Local bounds:

```text
campaignIds: 1..10 items
adGroupIds: 1..1000 items
limit: 1..1000, default 100
offset: integer >= 0, default 0
```

Trusted fixed `FieldNames`:

```text
Id,Name,CampaignId,Status,ServingStatus,Type
```

No type-specific group structures are requested.

### 6.3 listAds

Provider mapping:

```text
POST /json/v501/ads
provider method = get
```

Allowed fields:

```text
method
campaignIds
adGroupIds
adIds
limit
offset
```

At least one identifier set is required.

Local bounds follow a bounded subset of official provider limits:

```text
campaignIds: 1..10
adGroupIds: 1..1000
adIds: 1..1000 in Bridge first slice
limit: 1..1000, default 100
offset: integer >= 0, default 0
```

Trusted fixed `FieldNames`:

```text
Id,CampaignId,AdGroupId,Status,State,Type,Subtype
```

No `TextAdFieldNames`, `ResponsiveAdFieldNames`, creative text, URLs, tracking fields, ERIR fields or other type-specific payloads are requested in Phase 5. This deliberately avoids coupling the first slice to the current ad-format migration surface.

### 6.4 listKeywords

Provider mapping:

```text
POST /json/v501/keywords
provider method = get
```

Allowed fields:

```text
method
campaignIds
adGroupIds
keywordIds
limit
offset
```

At least one identifier set is required.

Local bounds:

```text
campaignIds: 1..10
adGroupIds: 1..1000
keywordIds: 1..1000 in Bridge first slice
limit: 1..1000, default 100
offset: integer >= 0, default 0
```

Trusted fixed `FieldNames`:

```text
Id
Keyword
State
Status
ServingStatus
AdGroupId
CampaignId
Bid
ContextBid
StrategyPriority
```

The first slice intentionally does not request `Productivity`, `StatisticsSearch`, or `StatisticsNetwork`, because official Direct Units accounting charges a higher per-2000-keyword component when those fields are requested and the provider itself warns that bulk keyword statistics may be slower.

Bid-like monetary values are normalized as integer micros:

```text
bid_micros
context_bid_micros
```

No currency conversion is inferred.

### 6.5 getCampaignPerformance

Provider mapping:

```text
POST https://api.direct.yandex.com/json/v501/reports
```

The Bridge constructs the report definition. The assistant cannot provide raw report fields, filters, report name, processing mode or headers.

Allowed assistant fields:

```text
method
dateFrom
dateTo
campaignIds
limit
offset
```

Local limits:

```text
dates = YYYY-MM-DD
dateFrom <= dateTo
maximum inclusive span = 31 days
campaignIds optional, max 10
limit default 1000, 1..1000
offset default 0, integer >= 0
```

Trusted fixed report contract:

```text
ReportType = CAMPAIGN_PERFORMANCE_REPORT
DateRangeType = CUSTOM_DATE
Format = TSV
IncludeVAT = YES
FieldNames = [Date,CampaignId,CampaignName,Impressions,Clicks,Cost]
Page = {Limit,Offset}
processingMode: online
skipReportHeader: true
skipReportSummary: true
skipColumnHeader is NOT set, so the returned column header remains available for strict parser verification
returnMoneyInMicros: false is NOT set
```

`IncludeVAT=YES` is an explicit Bridge product decision for this first slice so spend is user-facing including VAT. It is not represented as a provider default.

By intentionally omitting `returnMoneyInMicros: false`, Direct returns money as integer micros. Normalize:

```text
rows[] = {
  date,
  campaign_id,
  campaign_name,
  impressions,
  clicks,
  cost_micros
}
```

`processingMode=online` is mandatory. If Yandex cannot generate the report online, the Bridge surfaces the provider error and does not enqueue or poll an offline report. HTTP 201/202 are therefore not successful first-slice outcomes and must never trigger automatic repeat requests.

`SEARCH_QUERY_PERFORMANCE_REPORT` is explicitly excluded because current official docs require it to be generated offline.

## 7. Provider Units / limits

Direct API uses provider points (`Units`), not a per-call RUB tariff.

Current official facts include:

```text
max simultaneous API requests per advertiser = 5
response Units header = spent / remaining / daily_limit
erroring method call generally costs 20 points, except server availability errors
Campaigns.get = 10 per call + 1 per returned object
AdGroups.get = 15 per call + 1 per returned object
Ads.get = 15 per call + 1 per returned object
Keywords.get = 15 per call + normal 1 point per 2000 returned keywords; 3 per 2000 when specified statistics/productivity fields are requested
if fewer than 2000 keywords are returned, only the method-call points are deducted
Reports = max 20 requests per 10 seconds per user
```

The Bridge must parse and preserve the sanitized `Units` response header when present:

```text
provider_units = {
  spent,
  remaining,
  daily_limit
}
```

`Units-Used-Login` is not exposed in ordinary results because it contains account identity. It may be used internally for debugging only in redacted form if later governed.

No automatic retry occurs on insufficient Units or concurrency errors.

## 8. Error truthfulness

Direct often returns semantic provider errors in JSON. HTTP transport status alone is not sufficient for success.

Relevant provider codes include:

```text
53 invalid OAuth token
58 application registration/access request incomplete
54 permission denied
513 Direct account missing
3000 no API access / IP restriction / other API access denial
152 insufficient Units
506 too many simultaneous connections
55 operation not found
8000 malformed/invalid request, missing token/header/required field/unknown field
4000 invalid request parameters
4001 invalid SelectionCriteria
4002 invalid Page
```

Truth contract:

```text
local validation/credential/policy rejection before fetch → request_executed=false
provider HTTP response received, including semantic JSON error → request_executed=true
unknown network outcome after initiation → request_executed=UNKNOWN
automatic_retry=false
```

One admitted first-slice command = exactly one provider HTTP request.

## 9. Assistant command safety

Assistant payloads MUST NOT contain:

```text
oauth_token
token
Authorization
headers
Client-Login
clientLogin
Use-Operator-Units
Payment-Token
raw provider URL
provider service name
provider method name
FieldNames
SelectionCriteria
ReportName
ReportType
Format
IncludeVAT
IncludeDiscount
processingMode
returnMoneyInMicros
skipReportHeader
skipColumnHeader
skipReportSummary
arbitrary filters
arbitrary report fields
```

Unknown fields reject locally before provider initiation.

No raw URL/proxy method exists.

## 10. Write lock

Locked in Phase 5 first slice:

```text
all add/update/delete methods
campaign suspend/resume/archive/unarchive
ad moderate/suspend/resume/archive/unarchive
keyword add/update/delete/suspend/resume
all bid mutation/set/setAuto/setBids methods
agency-client mutations
financial/payment methods and Payment-Token
feed mutations
strategy mutations
budget changes
campaign/ad/keyword edits
offline Reports queue creation/polling
processingMode offline/auto
SEARCH_QUERY_PERFORMANCE_REPORT
arbitrary/custom report constructor
arbitrary report fields/filters/order/header control
raw provider proxy
```

Unsupported methods/fields fail locally with `request_executed=false` and zero Direct traffic.

## 11. Default local policy

```text
manual_enabled = true
autorun_enabled = false
allowed_methods = [listCampaigns,listAdGroups,listAds,listKeywords,getCampaignPerformance]
max_requests_per_run = 20
max_page_size = 1000
max_report_days = 31
max_report_rows = 1000
method_cost_rub = 0
max_cost_rub_per_run = 0
```

These are Bridge safety limits, not provider quotas. Direct Units are dynamic provider-side capacity and are reported separately.

## 12. Backup/import

Extend the current versioned settings backup only as needed to carry:

```text
settings.credentials.direct
```

Requirements:

```text
Direct token remains only in Direct record
Direct client_login remains only in Direct record
existing Wordstat/Search/Webmaster/Metrika mappings remain untouched
old backups without Direct import safely without erasing current/default Direct state
new backup round-trip preserves all five service mappings
checksum remains mandatory
contains_secrets remains explicit
active Manual/Autorun runtime state is never restored from backup
```

## 13. Popup UI

Popup remains within governed `430×560` geometry using internal scrolling.

Add:

```text
Direct in active-service selector
Direct credential card
masked OAuth token input
optional Client login field with agency-only explanation
Save
Check
read-only Check status
Direct policy section
```

Direct Check UI must explicitly warn that it performs one real `Campaigns.get` request and consumes Yandex Direct Units.

No saved OAuth token is rendered back into visible text/DOM after save.

The previously requested convenience duplication of `Сохранить общие настройки` near the active-service selector is deferred to Phase-5 implementation UI work and may be implemented only by reusing the exact existing common-settings save handler; it must not create a second state path.

## 14. Autorun

Direct Autorun is OFF by default. It may be exercised only in controlled tests after explicit policy enablement and must retain common immutable active-service ownership, request budget, exactly-once and delivery semantics.

## 15. Owner-live boundary

Only after exact candidate freeze and complete independent Codex PASS:

```text
1. ensure the OAuth app has direct:api
2. ensure the Direct API access request is approved for the application; full access is required for production data
3. obtain/save a dedicated real Direct OAuth token
4. if agency-client context is used, save the exact Client-Login; otherwise leave blank
5. Direct Check exactly once
6. listCampaigns exactly once
7. if a real campaign exists, perform at most one bounded downstream object read needed for proof
8. perform getCampaignPerformance exactly once for a short bounded range only when a real campaign/account is available and online generation succeeds
```

No writes. No bid changes. No quota/concurrency/error experiments against real Yandex. No offline report queue or polling. No repeated exploratory calls.
