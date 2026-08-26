# Phase 4 — Yandex Metrika requirements and implementation plan

Status: **RECONSTRUCTION COMPLETE / IMPLEMENTATION PLAN READY**  
Date: 2026-08-26

Authority:

```text
CURRENT_STATE.md
ROADMAP.md
SPECIFICATION.md
SPECIFICATION_PHASE_4_METRIKA_ADDENDUM.md
WORKFLOW_OPERATING_RULES.md
CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md
```

No production implementation may exceed the Phase-4 first slice defined here without a governed contract update first.

## 1. Reconstruction result

Current official Metrika API uses OAuth and exposes multiple API families on `api-metrika.yandex.net`.

Phase 4 enables only two read-only families:

```text
Management API:
  https://api-metrika.yandex.net/management/v1

Reports API:
  https://api-metrika.yandex.net/stat/v1
```

Required scope:

```text
metrika:read
```

First slice:

```text
listCounters
getCounter
getTrafficSummary
getTrafficByTime
```

All write/import/Logs surfaces remain disabled.

## 2. Product baseline rule

Phase-4 implementation begins only after the Phase-3 closure + Phase-4 contract documentation is on live `main`.

Before creating the dev branch:

```text
fetch live main HEAD
verify extension/src tree = e5fa694f1354e1ee048a352481a416413e94a3c9
verify no uncontrolled product changes since Phase-3 acceptance
```

The implementation branch must be created from that exact live main state. Do not develop Phase 4 from historical Phase-3 QA branches.

## 3. Service-specific credential foundation

Add a dedicated Metrika OAuth record to the existing service credential registry.

Target conceptual model:

```text
credentials.wordstat
credentials.search
credentials.webmaster
credentials.metrika
```

Requirements:

```text
Metrika reads only credentials.metrika
Webmaster reads only credentials.webmaster
no automatic OAuth token sharing
no secret in public state/diagnostics/results
blank masked Save preserves existing Metrika token
partial common settings Save never overwrites Metrika token
```

## 4. Backup/import migration

Extend the current versioned backup format to carry Metrika credential mapping safely.

Required compatibility:

```text
existing backup without Metrika → imports without erasing current/default Metrika state
new backup → contains four service credential records
new export/import → exact four-way service mapping preserved
checksum tamper → reject before any mutation
active Autorun/Manual safety locks remain authoritative
runtime transaction state never restored from backup
```

If a backup schema version bump is needed, write explicit migration tests before changing the version.

## 5. Metrika protocol module

Add expected module:

```text
extension/src/shared/metrika_protocol.js
```

Responsibilities:

```text
parse METRIKA_API_V1
strict method/field validation
positive integer counterId validation
page/perPage/permission normalization
date range validation
local 366-day report span guard
group enum day|week|month
safe query/path encoding
provider error normalization
METRIKA_RESULT_V1 envelope construction
zero credential knowledge in command payload
```

No arbitrary raw URL, metrics, dimensions, filters or headers are accepted from assistant text.

## 6. Registry/core integration

Add exactly one service registration:

```text
METRIKA: metrika
prefix: METRIKA_API_V1
```

Update all unified-core service enumerations:

```text
service registry
credential registry
policy registry
service worker router/executor
public state
popup active-service selector
Manual command discovery
Autorun service ownership
backup/export/import
service-isolation tests
```

Unknown service remains fail-closed.

## 7. Provider executor

Add `executeMetrikaCommand` or equivalent trusted worker/provider path.

Common rules:

```text
credential/policy/validation before fetch
Authorization built only in trusted worker layer
GET only
Accept: application/json
one admitted command = one fetch
no hidden Check before runtime command
no automatic retry
no token in logs/errors/results
```

### listCounters

```text
GET /management/v1/counters
```

Map local `page/perPage/permission` to provider query parameters and normalize only allowlisted counter discovery metadata.

### getCounter

```text
GET /management/v1/counter/{counterId}
```

Do not request optional `field` expansions in the first slice. Normalize only a safe metadata subset.

### getTrafficSummary

```text
GET /stat/v1/data
ids={counterId}
metrics=ym:s:visits,ym:s:users,ym:s:pageviews
date1={resolved dateFrom}
date2={resolved dateTo}
```

Do not send dimensions, filters, preset or Direct client logins.

Map provider `totals` by fixed metric order and preserve sampling/privacy truth fields.

### getTrafficByTime

```text
GET /stat/v1/data/bytime
ids={counterId}
metrics=ym:s:visits,ym:s:users,ym:s:pageviews
date1={resolved dateFrom}
date2={resolved dateTo}
group={day|week|month}
```

Preserve provider row/time ordering. Map metric arrays deterministically to visits/users/pageviews.

## 8. Credential Check implementation

Metrika Check is distinct from Save and uses exactly one controlled/read-only provider call:

```text
GET /management/v1/counters?per_page=1
```

Status mapping:

```text
200 → PRESENT
401 → INVALID_OR_EXPIRED
403 → NO_ACCESS
420 or 429 quota response → QUOTA
network fault → NETWORK_ERROR
```

`automatic_retry=false` for every Check outcome.

Controlled tests use fake token + stub. Real credentials are forbidden before final owner-live acceptance.

## 9. Policy

Default:

```text
manual_enabled = true
autorun_enabled = false
allowed_methods = listCounters,getCounter,getTrafficSummary,getTrafficByTime
max_requests_per_run = 50
max_report_days = 366
method_cost_rub = 0
max_cost_rub_per_run = 0
```

Do not claim the 50-request local ceiling is a Yandex provider quota.

Official current quota facts must be documented in UI/help only as provider context, not as internal budgets:

```text
30 requests/sec per IP
3 concurrent requests per user_login
5000 requests/day per user_login
200 /stat/v1/data requests per 5 minutes per user_login
```

No automatic retry on quota failures.

## 10. Error truthfulness

Provider fixtures must cover at minimum:

```text
200 valid management response
200 empty counter list
200 report exact/no sampling
200 report sampled=true
200 report contains_sensitive_data=true
400 invalid provider-side request
401 Unauthorized
403 access denied
404 counter not found or unavailable
420 quota compatibility response
429 current quota response
500 provider failure
malformed JSON
network unknown outcome
```

Truth contract:

```text
pre-fetch local reject → request_executed=false
HTTP response received → request_executed=true
unknown post-initiation network outcome → request_executed=UNKNOWN
automatic_retry=false
```

## 11. Protocol validation matrix

### Common

```text
missing method
unsupported method
unknown field
credential/token/header supplied in command
raw URL supplied
wrong active service
missing Metrika credential
Manual disabled
Autorun disabled
request budget exhausted
```

All reject before provider fetch.

### listCounters

```text
page < 1
perPage < 1
perPage > 1000
invalid permission
unknown field
```

### getCounter / reports

```text
missing counterId
counterId 0
counterId negative
counterId float
counterId unsafe integer
```

### report dates

```text
invalid date format
dateFrom > dateTo
explicit span > 366 days
```

### getTrafficByTime

```text
invalid group
allowed day
allowed week
allowed month
```

## 12. Response normalization tests

Mandatory assertions:

```text
listCounters allowlists fields and ignores unrequested provider extras
getCounter does not leak measurement tokens or expanded grants/config
traffic summary maps totals to visits/users/pageviews in fixed order
bytime preserves temporal order and fixed metric association
sampled/sample_share/sample_size/sample_space preserved
contains_sensitive_data preserved
data_lag preserved
provider query echoed only in sanitized/normalized form if exposed at all
```

## 13. Service isolation

Mandatory both directions:

```text
active Metrika + WORDSTAT_API_V1 → zero Metrika fetch
active Metrika + SEARCH_API_V1 → zero Metrika fetch
active Metrika + WEBMASTER_API_V1 → zero Metrika fetch
active non-Metrika + METRIKA_API_V1 → local SERVICE_NOT_ACTIVE / zero Metrika fetch
```

Credential isolation must be proven independently of service routing.

## 14. Popup/UI

Popup stays within `430×560` governed geometry.

Add Metrika credential card:

```text
OAuth token input masked
Save
Check
status: not checked/checking/valid/invalid/no access/quota/network error
```

Add Metrika policy panel without expanding native popup geometry; use existing internal scroll model.

Service switching must preserve all service credentials independently.

## 15. Browser/runtime coverage

Qualified installed-extension Chrome/Puppeteer coverage against a controlled Metrika provider route must prove:

```text
Metrika appears in active service selector
Metrika OAuth Save keeps secret out of visible DOM after rerender
Metrika Check executes exactly one management request
empty counters 200 is accepted
one Manual listCounters command = one provider request
one Manual getTrafficSummary command = one provider request
lifecycle button blocks duplicate admission during operation/delivery
result delivery re-enables action
service switching does not overwrite Webmaster token
backup export/import preserves four-service mapping
popup geometry remains 430×560
real Yandex requests = 0
```

Browser network routing must fail closed to local controlled endpoints only.

## 16. Autorun

Default Metrika Autorun OFF must be tested.

Controlled explicit enablement may exercise one first-slice command through the common Autorun lifecycle, proving:

```text
immutable active service
one command fingerprint admission
one provider request
one delivery
no duplicate execution
pause/resume/finish semantics unchanged
```

## 17. Gate / freeze

Before freeze:

```text
all focused source tests PASS
qualified browser coverage PASS
existing Wordstat/Search/Webmaster/core regressions PASS
no real credentials/provider traffic
Phase-4 Metrika gate addendum fully executable
```

Freeze exact candidate only after implementation is working.

Then:

```text
exact deterministic candidate package
manifest/hash/bytes/files/entries identity
transport round-trip
independent Codex complete applicable gate
no enabled NOT_RUN in PASS
```

## 18. Owner-live boundary

Only after complete exact-candidate Codex PASS:

```text
A. save real metrika:read OAuth token
B. Check once
C. listCounters once
D. if a real counter exists, getTrafficSummary once for a short bounded period
E. optionally getTrafficByTime once if chart-route proof is still irreducible
```

No write/import/Logs operations. No quota/error experiments against real provider.

## 19. Implementation order

```text
A. land Phase-3 closure + Phase-4 contract docs
B. fetch live main and verify accepted Phase-3 product src tree identity
C. create Phase-4 dev branch from exact live main
D. add dedicated Metrika credential + backup migration
E. add METRIKA_API_V1 protocol and service registry/policy
F. add trusted Metrika worker/provider executor
G. add bounded popup credential/policy UI
H. add focused/unit/integration tests
I. add controlled installed-browser tests
J. run development verification
K. freeze exact candidate
L. transport round-trip
M. independent Codex complete applicable campaign
N. narrow owner-live acceptance
O. close Phase 4 only after live PASS
```
