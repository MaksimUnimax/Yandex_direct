# Specification addendum — Phase 4 Yandex Metrika

Status: **RECONSTRUCTION COMPLETE / FIRST SLICE DEFINED**  
Date: 2026-08-26

This addendum extends the unified Yandex Marketing Bridge specification after Phase 3 Webmaster closure. It defines the contract boundary for the first Phase-4 Metrika slice. No implementation may exceed this slice without a governed contract update.

## 1. Official provider authority

Current official Yandex Metrika API authority checked 2026-08-26:

```text
API host = https://api-metrika.yandex.net
Management API base = https://api-metrika.yandex.net/management/v1
Reports API base = https://api-metrika.yandex.net/stat/v1
Authorization = OAuth token in Authorization: OAuth <token>
required read scope = metrika:read
```

Official references:

```text
https://yandex.ru/dev/metrika/ru/
https://yandex.ru/dev/metrika/ru/intro/authorization
https://yandex.ru/dev/metrika/ru/intro/quotas
https://yandex.ru/dev/metrika/ru/management/openapi/counter/counters
https://yandex.ru/dev/metrika/ru/management/openapi/counter/counter
https://yandex.ru/dev/metrika/ru/stat/openapi/data
https://yandex.ru/dev/metrika/ru/stat/openapi/bytime
https://yandex.ru/dev/metrika/ru/stat/metrics/visits/basic
```

Phase 4 first slice is read-only. Import API, Logs API and every management mutation are locked.

## 2. Service identity

```text
service = metrika
protocol prefix = METRIKA_API_V1
result prefix = METRIKA_RESULT_V1
```

No `METRIKA_API_V1` command may be executed by Wordstat, Search or Webmaster adapters.

## 3. Credential model

Metrika gets its own dedicated credential record:

```text
credentials.metrika = {
  oauth_token,
  checked_at,
  check_state
}
```

The Metrika token MUST NOT be implicitly copied from or read from `credentials.webmaster`, even though both services use OAuth. OAuth grants are scope-specific and Metrika requires `metrika:read`.

A user may manually paste the same physical token into both service records only if that token was explicitly issued with both required scope sets. The Bridge never assumes this and never performs cross-service fallback.

Public state may expose only non-secret metadata such as:

```text
has_oauth_token
checked_at
check_state
```

The raw token and Authorization header are secret.

## 4. Credential Check

Explicit Metrika Check performs exactly one read-only request:

```text
GET https://api-metrika.yandex.net/management/v1/counters?per_page=1
Authorization: OAuth <token>
Accept: application/json
```

Interpretation:

```text
200 with counters or empty counters → PRESENT / valid read capability
401 → INVALID_OR_EXPIRED
403 → NO_ACCESS / scope or account access failure
quota response → QUOTA / check failed, no retry
network unknown → NETWORK_ERROR / no automatic retry
```

Check does not persist any counter ID. It validates the saved Metrika read capability only.

The runtime MUST NOT perform a hidden credential Check before every Metrika command.

## 5. First-slice methods

Exactly four first-slice methods are enabled:

```text
listCounters
getCounter
getTrafficSummary
getTrafficByTime
```

All are one-request GET operations.

### 5.1 listCounters

Provider mapping:

```text
GET /management/v1/counters
```

Allowed command fields:

```text
method
page
perPage
permission
```

Local defaults/limits:

```text
page = 1
perPage = 100
1 <= perPage <= 1000
permission optional enum: own | view | edit
```

The provider currently allows a larger page size; the lower 1000-row limit is a Bridge safety/bounded-result limit, not a claim about provider maximum.

Normalized result preserves only useful non-secret counter discovery fields:

```text
rows
counters[] = {
  id,
  name,
  site,
  status,
  permission,
  owner_login,
  favorite,
  type,
  code_status,
  activity_status
}
```

### 5.2 getCounter

Provider mapping:

```text
GET /management/v1/counter/{counterId}
```

Allowed fields:

```text
method
counterId
```

`counterId` must be a positive safe integer.

Normalized result is an allowlisted metadata subset and must not expose measurement tokens, grants, filters, operations or other optional secret/sensitive configuration fields unless a later contract explicitly adds them.

### 5.3 getTrafficSummary

Provider mapping:

```text
GET /stat/v1/data
```

The Bridge constructs the report itself. Assistant commands do not supply arbitrary metrics, dimensions, filters, presets or Direct client logins in the first slice.

Fixed metrics:

```text
ym:s:visits
ym:s:users
ym:s:pageviews
```

Allowed command fields:

```text
method
counterId
dateFrom
dateTo
```

Dates use `YYYY-MM-DD`. Default report period follows Bridge policy:

```text
dateTo = today
dateFrom = 6daysAgo equivalent resolved locally
```

For explicit dates:

```text
dateFrom <= dateTo
maximum local span = 366 days
```

The 366-day bound is a local first-slice safety rule, not a provider quota statement.

Normalized result:

```text
counter_id
date_from
date_to
metrics = {
  visits,
  users,
  pageviews
}
sampled
sample_share
sample_size
sample_space
contains_sensitive_data
data_lag
total_rows
total_rows_rounded
```

### 5.4 getTrafficByTime

Provider mapping:

```text
GET /stat/v1/data/bytime
```

Fixed metrics:

```text
ym:s:visits
ym:s:users
ym:s:pageviews
```

Allowed command fields:

```text
method
counterId
dateFrom
dateTo
group
```

First-slice time grouping enum:

```text
day
week
month
```

Default:

```text
group = day
```

Same 366-day local date-span bound applies.

Normalized result preserves chart-useful provider truth:

```text
counter_id
date_from
date_to
group
series / provider time buckets and metric arrays
totals
sampled
sample_share
sample_size
sample_space
contains_sensitive_data
data_lag
total_rows
total_rows_rounded
```

The implementation must preserve time-bucket ordering from the provider and map each metric array unambiguously to `visits`, `users`, and `pageviews`.

## 6. Command safety

Assistant payloads MUST NOT contain:

```text
oauth_token
token
Authorization
headers
raw provider URL
metrics
dimensions
filters
preset
direct_client_logins
callback
pretty
measurement token
write body
```

Unknown fields reject locally before provider initiation.

No raw URL/proxy method exists.

## 7. Write lock

Locked in Phase 4 first slice:

```text
create/update/delete counter
create/update/delete goals
filters and operations mutation
access/grant mutation
representatives mutation
labels mutation
measurement-token management
offline conversions
user parameters
expenses import
CRM/client/order import
Logs API prepare/status/download/clean
any POST, PUT, PATCH or DELETE Metrika request
any report endpoint other than /stat/v1/data and /stat/v1/data/bytime
arbitrary metrics/dimensions/filter/preset execution
```

Any attempted unsupported method fails locally with `request_executed=false` and zero provider traffic.

## 8. Policy defaults

```text
manual_enabled = true
autorun_enabled = false
allowed_methods = [listCounters, getCounter, getTrafficSummary, getTrafficByTime]
max_requests_per_run = 50
max_report_days = 366
method_cost_rub = 0
max_cost_rub_per_run = 0
```

Yandex Metrika's standard API is quota-limited; this contract does not model a per-request RUB tariff.

The local request ceiling is independent from provider quota.

## 9. Current provider quotas / safety model

Official Russian quota documentation checked 2026-08-26 states, among other limits:

```text
30 API requests / second per IP
3 concurrent API requests per user_login
5000 API requests / day per user_login
200 Reports API /stat/v1/data requests per 5 minutes per user_login
```

Current Russian documentation states quota overflow returns HTTP 429. The English page currently shows a conflicting 420 value. Implementation and controlled tests must therefore fail closed and normalize both 429 and legacy/alternate 420 as quota responses, with no automatic retry.

The Bridge does not attempt to consume quotas aggressively and does not automatically retry quota failures.

## 10. Exactly-once / truthful outcome

```text
validation/credential/policy rejection before fetch → request_executed=false
HTTP response received, including HTTP error → request_executed=true
unknown network outcome after initiation → request_executed=UNKNOWN
automatic_retry=false in every Metrika first-slice result/error
```

One admitted command = exactly one provider fetch.

## 11. Report truth / privacy

Metrika Reports API may sample data and may limit disclosure for privacy. The Bridge must preserve provider truth fields rather than presenting sampled or restricted data as exact/unrestricted:

```text
sampled
sample_share
sample_size
sample_space
contains_sensitive_data
data_lag
```

No attempt may be made to bypass provider privacy thresholds.

## 12. Backup/import

Bump the versioned settings backup schema only if required by the existing backup implementation to add:

```text
settings.credentials.metrika
```

Requirements:

```text
Metrika token remains in the Metrika record only
Webmaster token remains in the Webmaster record only
old backups without Metrika import safely with Metrika unchanged/default
new backup round-trip preserves all four service mappings
checksum remains mandatory
contains_secrets remains explicit
active runtime transactions are never restored
```

## 13. UI

Popup remains bounded at governed `430×560`.

Add:

```text
Metrika in active-service selector
Metrika credential card
masked OAuth field
Save
Check
read-only check status
Metrika policy section
```

No saved OAuth token is rendered back into visible text/DOM after save.

## 14. Autorun

Metrika Autorun is **OFF by default** in Phase 4. The common Autorun engine may only be enabled in controlled testing after explicit policy enablement and must retain immutable active-service ownership, request budget, exactly-once and delivery lifecycle semantics.

## 15. Owner-live boundary

After exact candidate freeze + complete independent Codex PASS:

```text
1. save a real Metrika OAuth token carrying metrika:read
2. Check exactly once
3. execute listCounters exactly once
4. if a real counter is returned, execute one getTrafficSummary for a short period
5. optionally execute one getTrafficByTime only if needed to prove chart-route normalization
```

No write calls. No quota/error testing against real Yandex. No repeated exploratory calls.
