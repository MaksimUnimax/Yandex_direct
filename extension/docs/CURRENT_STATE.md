# CURRENT STATE — Yandex Marketing Bridge

Status: **PHASE 1 WORDSTAT = LIVE PASS / CLOSED — PHASE 2 SEARCH = LIVE PASS / CLOSED — LIFECYCLE BUTTON PATCH = OWNER LIVE PASS / CLOSED — PHASE 3 WEBMASTER = LIVE PASS / CLOSED — PHASE 4 METRIKA = LIVE PASS / CLOSED — PHASE 5 DIRECT = CONTRACT READY / IMPLEMENTATION AUTHORIZED**  
Updated: 2026-08-26

Always fetch live `main` HEAD and commit metadata before any workflow-stage transition or control-plane write.

## Mandatory current record

```text
LIVE_MAIN_BEFORE_PHASE4_OWNER_LIVE_CLOSURE_DOCS = 52b0cbf92872f6e7cb9f4cb96d0877d55221ceb4
LIVE_MAIN_BEFORE_PHASE5_RECONSTRUCTION = 14ae900516479ee5a7a3a61be34b832341c9df4b

ACCEPTED_PHASE2_SOURCE = b7869180c229356a6b3d51ac980ec3da5df4c23c
ACCEPTED_PHASE2_ARTIFACT_SHA256 = ce824a9fff5ddee47bc0145f57db4da10c6352e782c859fa500e3a1fb98088aa
ACCEPTED_PHASE2_FULL_GATE = PASS
ACCEPTED_PHASE2_OWNER_LIVE = PASS

ACCEPTED_LIFECYCLE_PATCH_SOURCE = 939e880f820e52beae9dcbcedc86d5cd9e13b075
ACCEPTED_LIFECYCLE_PATCH_SHA256 = 0430463ea979c31c5e74a48c899f2ce0fb141b62c4baf132df153380fbc0a262
ACCEPTED_LIFECYCLE_PATCH_FULL_CODEX_GATE = PASS
ACCEPTED_LIFECYCLE_PATCH_OWNER_LIVE = PASS

ACCEPTED_PHASE3_SOURCE = a7d9f947759f4f6a4fc20b39c7df3f25d81ce3e5
ACCEPTED_PHASE3_ZIP_SHA256 = 1c700640d5fa7b041468c1b987ce3793f4da7631b417e9fb5b0a59b54abd1fd8
ACCEPTED_PHASE3_ZIP_BYTES = 222592
ACCEPTED_PHASE3_SRC_TREE = e5fa694f1354e1ee048a352481a416413e94a3c9
ACCEPTED_PHASE3_MAIN_MERGE = 6c95cf15462b5ad61a267bf1186bb75fa8dd4dff
ACCEPTED_PHASE3_CODEX_FINAL = PASS
ACCEPTED_PHASE3_POSTMERGE_SUITE = 313/313 PASS
ACCEPTED_PHASE3_OWNER_LIVE = PASS

ACCEPTED_PHASE4_SOURCE = 643445758e86d3b06ac42a6daea5c97b6e9223c7
ACCEPTED_PHASE4_ZIP_SHA256 = 99c3719b447185481125964f0ff543c4c706714f9fe23fe150b7a8fbc8700217
ACCEPTED_PHASE4_ZIP_BYTES = 117375
ACCEPTED_PHASE4_SRC_TREE = fbc52f9a84195278b7b5e942f2a84c7d69778b98
ACCEPTED_PHASE4_MAIN_MERGE = 52b0cbf92872f6e7cb9f4cb96d0877d55221ceb4
ACCEPTED_PHASE4_FREEZE_RUN = 32953269753
ACCEPTED_PHASE4_FREEZE_ARTIFACT_ID = 9600980289
ACCEPTED_PHASE4_CODEX_FINAL_RUN = 32955512254
ACCEPTED_PHASE4_CODEX_FINAL_ATTEMPT = 2
ACCEPTED_PHASE4_CODEX_FINAL = PASS
ACCEPTED_PHASE4_POSTMERGE_RUN = 32957778009
ACCEPTED_PHASE4_POSTMERGE = PASS
ACCEPTED_PHASE4_OWNER_LIVE = PASS

PHASE4_PROTOCOL = METRIKA_API_V1
PHASE4_RESULT = METRIKA_RESULT_V1
PHASE4_FIRST_SLICE = listCounters,getCounter,getTrafficSummary,getTrafficByTime
PHASE4_AUTH = dedicated OAuth token with metrika:read
PHASE4_WRITES_ENABLED = NO
PHASE4_STATUS = LIVE PASS / CLOSED

PHASE5_BASELINE_SRC_TREE = fbc52f9a84195278b7b5e942f2a84c7d69778b98
PHASE5_PROTOCOL = DIRECT_API_V1
PHASE5_RESULT = DIRECT_RESULT_V1
PHASE5_FIRST_SLICE = listCampaigns,listAdGroups,listAds,listKeywords,getCampaignPerformance
PHASE5_AUTH = dedicated Direct OAuth token; direct:api; optional trusted client_login for agency-client context
PHASE5_PROVIDER_JSON = https://api.direct.yandex.com/json/v501/{service}
PHASE5_PROVIDER_REPORTS = https://api.direct.yandex.com/json/v501/reports
PHASE5_REPORT_MODE = online only
PHASE5_WRITES_ENABLED = NO
PHASE5_CONTRACT = READY

PRODUCTION_BYTES_CHANGED_BY_PHASE5_CONTRACT_DOCS = NO
OPEN_BLOCKERS = NONE
AUTHORIZED_NEXT_STAGE = PHASE_5_DIRECT_IMPLEMENTATION_FROM_EXACT_POST_CONTRACT_MAIN
```

## Phase 3 — Webmaster closure

Accepted first slice remains read-only:

```text
protocol = WEBMASTER_API_V1
result = WEBMASTER_RESULT_V1
base = https://api.webmaster.yandex.net/v4
auth = OAuth token + derived user_id
methods = listHosts,getSummary,getDiagnostics,getPopularQueries
writes = disabled
```

Phase 3 remains closed. Durable evidence:

```text
extension/tests/PHASE3_WEBMASTER_OWNER_LIVE_PASS_2026-08-26.md
```

A post-Metrika owner-live recheck also proved the existing dedicated Webmaster credential was not broken or overwritten:

```text
operation = listHosts
request_id = webmaster-99e68d1f-3fd5-4d0f-9851-b1d50a620572
status = OK
http_status = 200
result.hosts = []
request_executed = true
automatic_retry = false
```

Deferred Webmaster writes/mutations remain locked.

## Phase 4 — Metrika closure

Accepted service contract:

```text
service = metrika
protocol = METRIKA_API_V1
result = METRIKA_RESULT_V1
auth = dedicated OAuth token with metrika:read
Management API = https://api-metrika.yandex.net/management/v1
Reports API = https://api-metrika.yandex.net/stat/v1
methods = listCounters,getCounter,getTrafficSummary,getTrafficByTime
writes = disabled
```

Final accepted product identity:

```text
source = 643445758e86d3b06ac42a6daea5c97b6e9223c7
frozen ZIP SHA-256 = 99c3719b447185481125964f0ff543c4c706714f9fe23fe150b7a8fbc8700217
frozen ZIP bytes = 117375
accepted extension/src tree = fbc52f9a84195278b7b5e942f2a84c7d69778b98
main merge = 52b0cbf92872f6e7cb9f4cb96d0877d55221ceb4
independent final QA = run 32955512254 attempt 2 PASS
post-merge QA = run 32957778009 PASS
```

Controlled acceptance chain:

```text
focused/unit/integration coverage = PASS
qualified controlled popup/browser coverage = PASS
Metrika lifecycle browser coverage = PASS
M-00..M-19 = PASS
NOT_RUN_COUNT = 0
real Yandex traffic during controlled gate = 0
exact frozen product immutability = PASS
post-merge source identity = PASS
post-merge QA = PASS
```

Owner-live acceptance used a real owner-created counter:

```text
counter_id = 111970611
name = openscript
site = openscript.ru
permission = own
status = Active
```

Owner-live proved real Management + Reports routes with `HTTP 200`, `request_executed=true`, `automatic_retry=false`. Durable evidence:

```text
extension/tests/PHASE4_METRIKA_OWNER_LIVE_PASS_2026-08-26.md
```

Canonical closed Phase-4 authority:

```text
extension/docs/SPECIFICATION_PHASE_4_METRIKA_ADDENDUM.md
extension/docs/PHASE_4_METRIKA_REQUIREMENTS_AND_IMPLEMENTATION_PLAN.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_METRIKA_PHASE4_ADDENDUM.md
```

All Metrika write/import/Logs/arbitrary-report surfaces remain locked.

## Phase 5 — Yandex Direct contract

Official reconstruction establishes the provider transport/access boundary:

```text
API version family = Direct API v5
production JSON pattern = https://api.direct.yandex.com/json/v501/{service}
transport = HTTPS POST
OAuth header = Authorization: Bearer <token>
OAuth data source = direct:api
approved Direct API application access request = required
trial access = Sandbox only
full access = real production data + Sandbox
Client-Login = only for agency requests on behalf of an advertiser client
Use-Operator-Units = locked out in first slice
Payment-Token / finance = locked
```

Direct has dynamic provider Units rather than a fixed per-call RUB tariff. The Bridge will preserve sanitized `Units` response truth separately from its existing RUB cost ledger.

First-slice contract:

```text
service = direct
protocol = DIRECT_API_V1
result = DIRECT_RESULT_V1
methods = listCampaigns,listAdGroups,listAds,listKeywords,getCampaignPerformance
writes = disabled
```

Object reads use provider `get` methods with strict Bridge field allowlists and local pagination bounds. Direct provider pages can return up to 10,000 objects, but Phase 5 intentionally limits ordinary pages to at most 1000.

Reports first slice is deliberately synchronous/online only:

```text
endpoint = https://api.direct.yandex.com/json/v501/reports
ReportType = CAMPAIGN_PERFORMANCE_REPORT
DateRangeType = CUSTOM_DATE
Format = TSV
processingMode = online
fixed fields = Date,CampaignId,CampaignName,Impressions,Clicks,Cost
IncludeVAT = YES (explicit Bridge decision)
returnMoneyInMicros:false = absent
money normalization = integer cost_micros
max local report span = 31 days
max local rows = 1000
```

Offline/auto Reports, HTTP 201/202 polling, and `SEARCH_QUERY_PERFORMANCE_REPORT` are outside the first slice. If an online report cannot be generated, it is surfaced as a terminal provider outcome with no automatic replay.

Current official error documentation has a conflict that is preserved rather than hidden:

```text
errors table: code 53 = invalid OAuth token
authorization-token page: invalid token links to code 1002
```

Implementation must treat `53` as canonical invalid-token evidence and may map `1002` to invalid only when provider context/message explicitly identifies token invalidity. Generic `1002` remains generic operation error.

Default Direct policy:

```text
manual_enabled = true
autorun_enabled = false
max_requests_per_run = 20
max_page_size = 1000
max_report_days = 31
max_report_rows = 1000
method_cost_rub = 0
```

Owner-live will be postponed until after exact freeze and complete independent Codex PASS. It will not be used to explore provider errors or consume Units repeatedly.

Canonical Phase-5 authority:

```text
extension/docs/SPECIFICATION_PHASE_5_DIRECT_ADDENDUM.md
extension/docs/PHASE_5_DIRECT_REQUIREMENTS_AND_IMPLEMENTATION_PLAN.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_DIRECT_PHASE5_ADDENDUM.md
```

## Current authorized next action

Once the Phase-5 control-plane documents are merged to live `main`:

```text
1. fetch the new exact main HEAD
2. reverify extension/src = fbc52f9a84195278b7b5e942f2a84c7d69778b98
3. create Phase-5 Direct dev branch from that exact main
4. implement dedicated Direct credential + backup migration
5. implement DIRECT_API_V1 protocol + policy/registry
6. implement trusted Direct JSON provider and online Reports executor
7. implement bounded Direct popup UI
8. during the same governed popup change, add the owner-requested top duplicate common-settings Save control by reusing exactly the existing common save handler
9. add focused/unit/integration/browser/lifecycle coverage
10. run development verification
11. freeze exact candidate
12. perform exact artifact transport round-trip
13. run independent Codex complete applicable campaign including D-00..D-22
14. only then perform narrow owner-live Direct acceptance
15. close Phase 5 only after live PASS
```

No Direct write method, bid mutation, finance surface, arbitrary provider request/report constructor, offline report queue or automatic retry is authorized.
