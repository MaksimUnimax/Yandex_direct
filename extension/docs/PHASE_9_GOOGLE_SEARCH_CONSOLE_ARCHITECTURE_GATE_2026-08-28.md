# PHASE 9 — Google Search Console architecture gate

Date: 2026-08-28

Status: **ARCHITECTURE DECISION PASS / TEST-FIRST IMPLEMENTATION AUTHORIZED WITHOUT LIVE GOOGLE TRAFFIC**

Authority research:

`extension/docs/PHASE_9_GOOGLE_ORGANIC_PROVIDER_RESEARCH_2026-08-28.md`

## 1. Decision

Phase 9 first production candidate will use the official Google Search Console API for first-party Google organic evidence.

The existing five Yandex service invariant is intentionally revised by this gate.

New service:

```text
google_search_console
```

New protocol:

```text
GOOGLE_SEARCH_CONSOLE_API_V1
```

First slice methods:

```text
listSites
searchAnalytics
```

All first-slice methods are read-only.

This is an explicit governed architecture decision, not a silent reuse of `search` or `webmaster`.

## 2. Why a sixth service is required

Existing registry:

```text
wordstat
search
webmaster
metrika
direct
```

Current code hard-codes those five services in:

- `extension/src/shared/service_registry.js`;
- `extension/src/shared/credential_store_model.js`;
- `extension/src/shared/policy_model.js`;
- `extension/src/webmaster_worker_runtime.js`;
- popup service selector/credential/policy UI;
- backup/settings serialization;
- browser/runtime regression assumptions.

Google Search Console cannot truthfully be represented as existing `webmaster` because:

```text
provider != Yandex Webmaster
base API != api.webmaster.yandex.net
OAuth ownership != Yandex OAuth
method semantics != Yandex Webmaster
site/property identity != Yandex host identity
```

It cannot truthfully be represented as `search` because Search Console is first-party site performance data, not an arbitrary SERP request.

Therefore:

```text
GOOGLE_SEARCH_CONSOLE_AS_YANDEX_WEBMASTER = REJECT
GOOGLE_SEARCH_CONSOLE_AS_SEARCH_METHOD = REJECT
SIXTH_EXPLICIT_SERVICE = ACCEPT
```

## 3. OAuth architecture

Official Chrome Identity API is the preferred credential mechanism.

Relevant official docs:

- https://developer.chrome.com/docs/extensions/reference/api/identity
- https://developer.chrome.com/docs/extensions/reference/manifest/oauth2
- https://developer.chrome.com/docs/extensions/mv3/tut_oauth

Required Google scope for first slice:

```text
https://www.googleapis.com/auth/webmasters.readonly
```

The Chrome extension runtime should obtain/cycle access tokens through:

```text
chrome.identity.getAuthToken(...)
```

Do not persist Google access tokens into `ymb_service_credentials`.

Credential truth for this service should be identity-managed state, for example:

```text
UNCONFIGURED
AUTH_REQUIRED
PRESENT
NO_ACCESS
INVALID_OR_EXPIRED
NETWORK_ERROR
QUOTA
```

`PRESENT` means a non-interactive token can be obtained and a bounded readonly API check succeeds; it does not mean a token string is persisted.

## 4. Stable extension ID / OAuth client gate

Chrome OAuth client registration is bound to an extension ID. Chrome recommends a stable extension ID and notes that an extension manifest `key` may be used to preserve it.

Current production manifest does not contain:

```text
identity permission
oauth2 block
key
```

Therefore no production OAuth wiring may be frozen until the release identity path is explicit.

Permanent safety rule:

> Do not invent a new manifest `key` for an already-used extension build. A changed extension ID could orphan existing local extension storage/bindings.

Implementation may proceed behind an injected/mock identity adapter, but live Chrome OAuth requires a later exact identity decision using the existing installed/release extension ID.

## 5. Official provider contract

Base APIs:

```text
GET  https://www.googleapis.com/webmasters/v3/sites
POST https://www.googleapis.com/webmasters/v3/sites/{siteUrl}/searchAnalytics/query
```

No sitemap mutation, site add/delete, indexing request or URL Inspection in first slice.

### `listSites`

Provider mapping:

```text
GET /webmasters/v3/sites
```

Normalized evidence:

```text
site_url
permission_level
```

### `searchAnalytics`

Provider mapping:

```text
POST /webmasters/v3/sites/{siteUrl}/searchAnalytics/query
```

Required command fields:

```text
method = searchAnalytics
siteUrl
startDate
endDate
```

First-slice optional fields:

```text
dimensions[] subset of query,page,country,device,date
rowLimit 1..25000
startRow >= 0
dataState = final|all
searchType/type = web only in first slice
filters[] bounded and normalized
```

Allowed filter dimensions:

```text
query
page
country
device
```

Allowed operators first slice:

```text
equals
contains
notEquals
notContains
```

Regex filters are deferred until there is a concrete product need.

## 6. Evidence semantics

Normalized row:

```text
keys[]
clicks
impressions
ctr
average_position
```

Permanent provenance labels:

```text
provider = google_search_console
source = Search Analytics
position_semantics = average_topmost_position_over_impressions
```

Forbidden relabeling:

```text
average_position -> live_rank          FORBIDDEN
average_position -> exact_serp_rank    FORBIDDEN
missing row -> rank_not_found          FORBIDDEN
```

Search Console may omit detailed rows and exposes top data under internal limits. Missing rows are therefore `NOT_OBSERVED_IN_RETURNED_GSC_DATA`, not proof of absence from Google Search.

## 7. Pagination and data bounds

Provider allows `rowLimit <= 25,000` with `startRow` pagination.

Project first slice must be stricter than provider maximum by default:

```text
default rowLimit = 1000
hard command rowLimit max = 25000
max pages per command = explicit bounded value
no hidden pagination loop in one Bridge command
```

Preferred first slice behavior:

```text
one Bridge command = one provider HTTP request
```

ChatGPT may request subsequent pages explicitly by increasing `startRow`.

This preserves the existing Bridge invariant that a command never silently expands into an unbounded provider loop.

## 8. Policy model

Google Search Console API is currently free of charge but quota/load bounded.

Policy should therefore use request ceilings, not fabricated monetary cost:

```text
method_cost = 0
max_requests_per_run = conservative bounded default
manual_enabled = true
autorun_enabled = false by default
```

First-slice policy methods:

```text
listSites
searchAnalytics
```

Quota/load errors must be surfaced as provider truth and never automatically retried after unknown execution outcome.

## 9. Provider execution truth

For `listSites` and `searchAnalytics`:

```text
request_executed = false before fetch initiation
request_executed = true once provider initiation definitely occurs
```

If initiation may have occurred and final outcome is not known:

```text
outcome = OUTCOME_UNKNOWN
automatic_retry = false
```

No automatic replay.

OAuth token acquisition itself is not counted as a Search Console business request, but identity-interactive prompts must only occur from explicit user UI actions.

## 10. Popup / UX boundary

New active-service option:

```text
Google Search Console
```

Credential card should not contain a password/token input.

Expected controls:

```text
Connect Google
Check access
Disconnect / clear cached auth
```

The popup must explain:

```text
read-only Search Console access
only properties granted to the signed-in Google account
tokens are managed by Chrome Identity, not displayed or stored in YMB credential backup
```

Autorun remains off by default.

## 11. Backup / migration boundary

Existing `YMB_SETTINGS_BACKUP_V3` contains persistent secrets for Yandex services.

Google identity tokens must not be added to backup payloads.

If a Google service policy is added, settings schema/backup schema may be revised for policy only, while identity authorization remains external to backup.

Backward compatibility requirement:

```text
old backups without google_search_console policy remain importable
existing five-service credentials remain byte/semantic equivalent after migration
```

## 12. Manifest boundary

Eventually required for live OAuth/runtime:

```text
permission: identity
host permission: https://www.googleapis.com/*
OAuth client registration bound to stable extension ID
readonly Search Console scope
```

Do not add those production manifest fields until the extension-ID/OAuth-client issue is resolved.

Unit/protocol/runtime development before that point must use injected provider/identity adapters and make zero Google requests.

## 13. Test-first gate

Before provider runtime implementation, add tests proving:

```text
GOOGLE_SEARCH_CONSOLE service/prefix is explicit and does not alias Yandex services
protocol rejects unknown/write methods
listSites normalizes only readonly GET
searchAnalytics normalizes exact readonly POST body
rowLimit <= 25000
startRow >= 0
first-slice type = web
unsupported dimensions/operators rejected
no raw authorization token accepted in command JSON
policy defaults autorun=false
one command <= one business provider request
OUTCOME_UNKNOWN => no automatic retry
GSC average position provenance preserved
existing 5 service definitions remain unchanged in meaning
```

No real provider call is required for these tests.

## 14. Implementation order

```text
P9-00 exact main baseline = b13886df49c4591320f780769e78016eff23301e
P9-01 provider/registry/credential/popup/backup audit = PASS
P9-02 sixth-service + Chrome Identity architecture decision = PASS
P9-03 protocol + policy + registry tests first
P9-04 pure Google Search Console protocol/runtime using injected adapters
P9-05 worker/content routing + controlled browser stub
P9-06 manifest/OAuth wiring only after stable extension ID/client is resolved
P9-07 complete regression, zero real Google/Yandex requests
P9-08 minimal owner OAuth/live acceptance only after frozen exact candidate
```

## 15. Verdict

```text
PHASE9_GSC_ARCHITECTURE_GATE_PASS
service = google_search_console
protocol = GOOGLE_SEARCH_CONSOLE_API_V1
provider = official Google Search Console API
credential_model = chrome.identity managed / non-persistent token
methods = listSites,searchAnalytics
writes = disabled
autorun_default = false
live_google_requests_authorized = 0
next = test-first protocol/policy/registry work
```
