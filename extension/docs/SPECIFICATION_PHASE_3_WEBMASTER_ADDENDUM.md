# SPECIFICATION — Phase 3 Webmaster addendum

Status: **CURRENT PHASE-3 CONTRACT / FIRST SLICE DEFINED / PRODUCTION IMPLEMENTATION NOT YET AUTHORIZED UNTIL PLAN+GATE ARE COMMITTED**  
Adopted: 2026-08-26

This addendum extends `SPECIFICATION.md` for the first Yandex Webmaster API slice.

## 1. Official authority checked 2026-08-26

Current official Yandex Webmaster API authority:

```text
API version: 4.1
base: https://api.webmaster.yandex.net/
auth: OAuth 2.0
request header: Authorization: OAuth <token>
default response: JSON
user identity bootstrap: GET /v4/user
```

Official sources:

```text
https://yandex.ru/dev/webmaster/doc/ru/
https://yandex.com/dev/webmaster/doc/ru/tasks/how-to-get-oauth
https://yandex.ru/dev/webmaster/doc/ru/concepts/getting-started
https://yandex.ru/dev/webmaster/doc/ru/reference/user
https://yandex.ru/dev/webmaster/doc/ru/reference/hosts
https://yandex.ru/dev/webmaster/doc/ru/reference/host-id-summary
https://yandex.ru/dev/webmaster/doc/ru/reference/host-diagnostics-get
https://yandex.ru/dev/webmaster/doc/ru/reference/host-search-queries-popular
https://yandex.ru/dev/webmaster/doc/ru/reference/errors
```

The official authorization guide states that the OAuth token is obtained through Yandex OAuth and is valid for six months. It demonstrates Webmaster permissions `webmaster:hostinfo` and `webmaster:verify`. This first slice is read-only and does not invoke verification/write endpoints.

## 2. Service/protocol identity

```text
service = webmaster
command signature = WEBMASTER_API_V1
result signature = WEBMASTER_RESULT_V1
provider API = Yandex Webmaster API v4.1
provider base = https://api.webmaster.yandex.net/v4
```

`WEBMASTER_API_V1` becomes executable only after the Phase-3 production implementation and applicable gate are complete. Before that, the prefix remains future/disabled and must not cause provider traffic.

## 3. First slice — read-only only

Enabled first-slice methods:

```text
listHosts
getSummary
getDiagnostics
getPopularQueries
```

Provider mapping:

```text
listHosts
→ GET /v4/user/{user-id}/hosts

getSummary
→ GET /v4/user/{user-id}/hosts/{host-id}/summary

getDiagnostics
→ GET /v4/user/{user-id}/hosts/{host-id}/diagnostics

getPopularQueries
→ GET /v4/user/{user-id}/hosts/{host-id}/search-queries/popular
```

Explicitly deferred/locked from the first slice:

```text
add/delete host
verification writes/check requests
recrawl submission
Sitemap add/delete
important URL mutation
original text submission
PRO/extended SERP export tasks
query analytics POST endpoints
all other Webmaster POST/DELETE operations
```

No write-capable Webmaster operation may be exposed through `WEBMASTER_API_V1` in this slice.

## 4. Credential model

Webmaster MUST NOT reuse the current Yandex Cloud `Api-Key + folderId` credential used by Wordstat/Search.

Required Webmaster credential record:

```text
webmaster.oauth_token      secret string
webmaster.user_id          derived int64
webmaster.verified_at       local ISO timestamp or null
```

Rules:

- token is entered/saved only in trusted popup/settings UI or secret-bearing backup import;
- token never appears in executable ChatGPT commands, result envelopes, errors, debug logs or GitHub evidence;
- editing/replacing the OAuth token invalidates the stored derived `user_id` until the token is checked again;
- explicit **Check** performs exactly one read-only `GET https://api.webmaster.yandex.net/v4/user` using `Authorization: OAuth <token>`;
- successful Check stores returned `user_id` and `verified_at`;
- command execution requires both a non-empty token and a positive derived `user_id`;
- HTTP 401 marks the Webmaster credential `INVALID_OR_EXPIRED`;
- a generic authorization/scope denial may map to `NO_ACCESS` without exposing token data;
- no command may accept `oauth_token`, `Authorization` or raw credential fields from ChatGPT.

The existing capability vocabulary remains:

```text
PRESENT
MISSING
INVALID_OR_EXPIRED
NO_ACCESS
```

For this service, `PRESENT` means token + derived `user_id` are locally available. A token present without derived `user_id` is not executable and is treated as incomplete credentials until Check succeeds.

## 5. Credential UI restoration requirement

Phase 3 must not ship with a misleading single generic credential field pretending all services share one auth model.

Before Phase-3 owner handoff, popup credential management must expose dedicated service sections for every enabled service and restore the previously required operator workflow:

```text
service-specific credential inputs
→ Save
→ explicit Check / verification outcome
→ Export settings
→ Import settings restores each credential to the correct service
```

At minimum:

```text
Wordstat  → Api-Key + folderId
Search    → Api-Key + folderId
Webmaster → OAuth token + derived user_id status
```

Backward compatibility:

- legacy/current shared `apiKey + folderId` must migrate safely so existing Wordstat/Search installations do not lose credentials;
- migration may seed both Wordstat and Search credential slots from the existing shared values once;
- after migration, service records are distinct and may diverge;
- backup schema must be versioned and checksum-protected;
- import/export must preserve service mapping and must never log secrets.

Live credential checks must not silently create paid traffic. If a Search credential check requires a billable Search request, the UI must require explicit owner confirmation and show that the check is billable; controlled QA uses a stub instead.

## 6. Command contract

### 6.1 `listHosts`

```text
WEBMASTER_API_V1
{
  "method": "listHosts"
}
```

No `userId` is accepted in the command. The Bridge uses the derived credential `user_id`.

### 6.2 `getSummary`

```text
WEBMASTER_API_V1
{
  "method": "getSummary",
  "hostId": "https:example.com:443"
}
```

`hostId` is required and must be a non-empty string obtained from `listHosts` or another trusted operator source.

### 6.3 `getDiagnostics`

```text
WEBMASTER_API_V1
{
  "method": "getDiagnostics",
  "hostId": "https:example.com:443"
}
```

### 6.4 `getPopularQueries`

```text
WEBMASTER_API_V1
{
  "method": "getPopularQueries",
  "hostId": "https:example.com:443",
  "orderBy": "TOTAL_SHOWS",
  "queryIndicator": "TOTAL_CLICKS",
  "deviceTypeIndicator": "ALL",
  "dateFrom": "2026-08-01",
  "dateTo": "2026-08-07",
  "offset": 0,
  "limit": 100
}
```

Allowed `orderBy`:

```text
TOTAL_SHOWS
TOTAL_CLICKS
```

Allowed `queryIndicator` when supplied:

```text
TOTAL_SHOWS
TOTAL_CLICKS
AVG_SHOW_POSITION
AVG_CLICK_POSITION
```

Allowed `deviceTypeIndicator` when supplied:

```text
ALL
DESKTOP
MOBILE_AND_TABLET
MOBILE
TABLET
```

Validation:

```text
offset = integer >= 0
limit = integer 1..500
dateFrom/dateTo = valid date/datetime strings when supplied
hostId = non-empty bounded string
unknown fields = rejected
unknown enum = rejected
unsupported method = rejected
```

For `getPopularQueries`, provider defaults may be used when optional fields are omitted. Official documentation states the default window is the last week, default offset is 0, default limit is 500 and default device type is `ALL`.

## 7. Provider request rules

All first-slice requests are HTTPS GET and JSON-only from the Bridge.

Common request headers:

```text
Authorization: OAuth <secret token>
Accept: application/json
```

The Bridge must percent-encode path/query components correctly. `hostId` must never be concatenated unsafely.

One accepted executable command = one provider request. Runtime execution MUST NOT silently call `/v4/user` before every command. `user_id` is derived by the explicit credential Check workflow and stored locally.

## 8. Normalized results

All service results use:

```text
WEBMASTER_RESULT_V1
```

Common envelope follows the base specification:

```text
bridge
version
service = webmaster
operation
request_id
run_id
status
reason
policy
command
http_status
elapsed_ms
result
request_executed
automatic_retry
```

No OAuth token or Authorization header is permitted in the envelope.

### `listHosts` result

Normalize at minimum:

```text
hosts[]:
  host_id
  ascii_host_url
  unicode_host_url
  verified
  main_mirror? { host_id, ascii_host_url, unicode_host_url, verified }
```

### `getSummary` result

Normalize at minimum:

```text
sqi
excluded_pages_count
searchable_pages_count
site_problems
```

### `getDiagnostics` result

Normalize the provider problem map without losing provider problem keys:

```text
problems[problem_code]:
  severity
  state
  last_state_update
```

### `getPopularQueries` result

Normalize at minimum:

```text
queries[]:
  query_id
  query_text
  indicators

date_from
date_to
count
```

Provider indicator keys are retained only from the documented first-slice indicator set.

## 9. Policy/budget

Webmaster first-slice methods are modeled as quota-only/read-only operations, not RUB-priced Search requests.

Local policy defaults:

```text
manual_enabled = true
autorun_enabled = false
allowed_methods = [listHosts, getSummary, getDiagnostics, getPopularQueries]
max_requests_per_run = 50
method_cost_rub = 0 for all first-slice methods
max_cost_rub_per_run = 0
```

The local request ceiling is defense in depth; it is not a claim about Yandex's provider quota.

Official Webmaster errors include `429 QUOTA_EXCEEDED` and `429 TOO_MANY_REQUESTS_ERROR`; some resources have additional method/domain-specific limits. The Bridge must surface provider quota errors and MUST NOT automatically retry them.

## 10. Error/retry semantics

Base no-blind-retry rules remain mandatory.

```text
validation / missing credential / policy rejection before fetch
→ request_executed = false
→ automatic_retry = false

HTTP response received, including 4xx/5xx/429
→ request_executed = true
→ automatic_retry = false

network/timeout/session loss after initiation with unknown outcome
→ request_executed = "UNKNOWN"
→ automatic_retry = false
→ identical automatic replay forbidden
```

Important provider errors include at least:

```text
401 Unauthorized
403 INVALID_USER_ID
404 HOST_NOT_VERIFIED
404 HOST_NOT_INDEXED
404 HOST_NOT_LOADED
429 QUOTA_EXCEEDED
429 TOO_MANY_REQUESTS_ERROR
```

The exact provider error body should be normalized/redacted, not discarded.

## 11. Service isolation

When `active_service != webmaster`, a `WEBMASTER_API_V1` command must fail/skip locally with zero Webmaster provider request according to the existing service-isolation contract.

Likewise, when Webmaster is active, Wordstat/Search commands cannot execute through the Webmaster adapter.

## 12. Manual/Autorun

The common lifecycle/button/delivery contract is inherited unchanged.

For this first slice:

- Manual is enabled by default subject to operator policy;
- Autorun exists but is disabled by default;
- lifecycle-blocked Yandex action remains disabled/non-clickable according to the accepted inter-phase patch;
- RUN request accounting counts actual Webmaster provider requests;
- credential Check is a settings operation, not a RUN command.

## 13. Security/redaction

Never emit or persist outside secret storage/backup:

```text
OAuth token
Authorization header
full secret-bearing settings backup
```

Derived `user_id`, host IDs and public site URLs are not secrets, but ordinary diagnostics should still avoid unnecessary full payload dumps.

## 14. Acceptance boundary

Controlled QA must use fake credentials and a controlled Webmaster endpoint/stub with **zero real Yandex requests**.

Owner-live acceptance should be minimal:

1. explicitly save/check a real Webmaster OAuth token;
2. execute one useful read-only first-slice operation, preferably `listHosts` or `getSummary`;
3. confirm normalized non-empty/expected response;
4. no extra provider calls solely for repetitive testing.

Any write-capable Webmaster behavior remains out of scope and cannot be inferred from this first-slice PASS.
