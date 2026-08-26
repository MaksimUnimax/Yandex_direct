# CURRENT STATE — Yandex Marketing Bridge

Status: **PHASE 1 WORDSTAT = LIVE PASS / CLOSED — PHASE 2 SEARCH = LIVE PASS / CLOSED — LIFECYCLE BUTTON PATCH = OWNER LIVE PASS / CLOSED — PHASE 3 WEBMASTER = LIVE PASS / CLOSED — PHASE 4 METRIKA = CONTRACT READY / IMPLEMENTATION AUTHORIZED**  
Updated: 2026-08-26

Always fetch live `main` HEAD and commit metadata before any workflow-stage transition or control-plane write.

## Mandatory current record

```text
LIVE_MAIN_BEFORE_PHASE3_OWNER_LIVE_CLOSURE = 6c95cf15462b5ad61a267bf1186bb75fa8dd4dff

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

PHASE3_PROTOCOL = WEBMASTER_API_V1
PHASE3_RESULT = WEBMASTER_RESULT_V1
PHASE3_FIRST_SLICE = listHosts,getSummary,getDiagnostics,getPopularQueries
PHASE3_WRITES_ENABLED = NO
PHASE3_STATUS = LIVE PASS / CLOSED

PHASE4_PROTOCOL = METRIKA_API_V1
PHASE4_RESULT = METRIKA_RESULT_V1
PHASE4_FIRST_SLICE = listCounters,getCounter,getTrafficSummary,getTrafficByTime
PHASE4_AUTH = dedicated OAuth token with metrika:read
PHASE4_PROVIDER_MANAGEMENT = https://api-metrika.yandex.net/management/v1
PHASE4_PROVIDER_REPORTS = https://api-metrika.yandex.net/stat/v1
PHASE4_WRITES_ENABLED = NO
PHASE4_CONTRACT = READY

PRODUCTION_BYTES_CHANGED_BY_PHASE3_CLOSURE_OR_PHASE4_CONTRACT_DOCS = NO
OPEN_BLOCKERS = NONE
AUTHORIZED_NEXT_STAGE = PHASE_4_METRIKA_IMPLEMENTATION_FROM_EXACT_LIVE_MAIN
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

Acceptance chain is complete:

```text
focused/unit/integration coverage = PASS
controlled browser runtime = PASS
Webmaster lifecycle browser = PASS
W-00..W-19 = PASS
independent Codex final campaign attempt 2 = PASS
NOT_RUN_COUNT = 0
exact frozen candidate merged to main = PASS
post-merge source identity = PASS
post-merge source suite = 313 / 313 PASS
owner-live OAuth Save/Check = PASS
owner-live real listHosts = PASS
```

Owner-live result:

```text
operation = listHosts
request_id = webmaster-d73003d9-74ae-4428-8bc7-eac57be193ea
status = OK
http_status = 200
elapsed_ms = 784
result.hosts = []
request_executed = true
automatic_retry = false
policy.channel = manual
policy.active_service = webmaster
estimated_rub = 0
```

`hosts: []` is an accepted successful real-provider response. No host-specific live request was made because no real `hostId` was returned.

Durable closure evidence:

```text
extension/tests/PHASE3_WEBMASTER_OWNER_LIVE_PASS_2026-08-26.md
```

Canonical closed Phase-3 authority:

```text
extension/docs/SPECIFICATION_PHASE_3_WEBMASTER_ADDENDUM.md
extension/docs/PHASE_3_WEBMASTER_REQUIREMENTS_AND_IMPLEMENTATION_PLAN.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_WEBMASTER_PHASE3_ADDENDUM.md
```

Deferred Webmaster writes/mutations remain locked.

## Phase 4 — Metrika contract

Current official reconstruction establishes:

```text
service = metrika
protocol = METRIKA_API_V1
result = METRIKA_RESULT_V1
auth = OAuth token with metrika:read
Management API = https://api-metrika.yandex.net/management/v1
Reports API = https://api-metrika.yandex.net/stat/v1
```

Dedicated credential model:

```text
credentials.metrika = {
  oauth_token,
  checked_at,
  check_state
}
```

Metrika never implicitly reuses the Webmaster OAuth credential.

Explicit Metrika Check is exactly one read-only request:

```text
GET /management/v1/counters?per_page=1
Authorization: OAuth <token>
```

200 with either non-empty or empty `counters` is a successful credential check. No automatic retry is permitted.

First-slice methods:

```text
listCounters
getCounter
getTrafficSummary
getTrafficByTime
```

Provider mappings:

```text
listCounters      → GET /management/v1/counters
getCounter        → GET /management/v1/counter/{counterId}
getTrafficSummary → GET /stat/v1/data
getTrafficByTime  → GET /stat/v1/data/bytime
```

Reports use a fixed first-slice metric set only:

```text
ym:s:visits
ym:s:users
ym:s:pageviews
```

No arbitrary provider URL, Authorization header, metrics, dimensions, filters or preset may come from assistant command text.

Default Phase-4 policy:

```text
manual_enabled = true
autorun_enabled = false
allowed_methods = [listCounters,getCounter,getTrafficSummary,getTrafficByTime]
max_requests_per_run = 50
max_report_days = 366
method_cost_rub = 0
max_cost_rub_per_run = 0
```

Truth contract:

```text
pre-fetch rejection → request_executed=false
HTTP response received → request_executed=true
unknown post-initiation network outcome → request_executed=UNKNOWN
automatic_retry=false
```

Quota compatibility handling includes provider HTTP 420 and 429 as terminal quota outcomes with no automatic retry.

All write/import/Logs surfaces are locked in Phase 4 first slice.

## Canonical Phase-4 authority

```text
extension/docs/SPECIFICATION_PHASE_4_METRIKA_ADDENDUM.md
extension/docs/PHASE_4_METRIKA_REQUIREMENTS_AND_IMPLEMENTATION_PLAN.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_METRIKA_PHASE4_ADDENDUM.md
```

Final Metrika acceptance must execute `M-00..M-19` plus every still-applicable permanent/core/Phase-1/2/3 gate. PASS forbids enabled `NOT_RUN`.

## Current authorized next action

Phase-4 implementation is authorized only after these control-plane documents land on live `main` and the accepted Phase-3 product source tree is reverified unchanged.

Implementation sequence:

```text
1. land Phase-3 closure + Phase-4 contract docs on main
2. fetch new live main HEAD
3. verify extension/src tree remains e5fa694f1354e1ee048a352481a416413e94a3c9
4. create Phase-4 dev branch from that exact main
5. implement dedicated Metrika credential + backup migration
6. implement METRIKA_API_V1 protocol + registry + policy
7. implement trusted Metrika provider executor
8. implement bounded popup Metrika credential/policy UI
9. add focused/unit/integration/browser tests
10. run development verification
11. freeze exact candidate
12. exact artifact transport round-trip
13. independent Codex full applicable campaign including M-00..M-19
14. narrow owner-live Metrika acceptance
15. close Phase 4 only after live PASS
```
