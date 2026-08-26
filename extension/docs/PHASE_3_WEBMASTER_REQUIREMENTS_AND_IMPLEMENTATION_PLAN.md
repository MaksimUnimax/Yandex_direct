# Phase 3 — Yandex Webmaster requirements and implementation plan

Status: **RECONSTRUCTION COMPLETE / IMPLEMENTATION PLAN READY**  
Date: 2026-08-26

Authority:

```text
CURRENT_STATE.md
SPECIFICATION.md
SPECIFICATION_PHASE_3_WEBMASTER_ADDENDUM.md
WORKFLOW_OPERATING_RULES.md
CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md
```

No production implementation may exceed the first slice defined here without a governed contract update first.

## 1. Reconstruction result

Current official Yandex Webmaster API is v4.1 and uses OAuth 2.0, not the Yandex Cloud `Api-Key + folderId` auth used by existing Wordstat/Search adapters.

First-slice provider base:

```text
https://api.webmaster.yandex.net/v4
```

Credential bootstrap/check:

```text
GET /v4/user
Authorization: OAuth <token>
→ { user_id }
```

First slice is read-only:

```text
listHosts
getSummary
getDiagnostics
getPopularQueries
```

No Webmaster write endpoint is enabled.

## 2. Why credential work is part of Phase 3

The current production source has only a shared `apiKey + folderId` capability for Wordstat/Search. Webmaster cannot safely be added by overloading those fields.

Therefore Phase 3 includes a governed unified-core credential migration before Webmaster owner handoff.

Required end-state UI:

```text
Wordstat credentials
Search credentials
Webmaster credentials
```

Each section has:

```text
service-specific fields
Save
Check
clear success/failure reason
Export/Import preservation
```

This restores the previously required multi-service credential workflow and prevents future services from sharing incompatible auth fields.

## 3. Storage and backup migration

### 3.1 New service credential records

Target local storage model:

```text
credentials.wordstat = {
  api_key,
  folder_id,
  checked_at,
  check_state
}

credentials.search = {
  api_key,
  folder_id,
  checked_at,
  check_state
}

credentials.webmaster = {
  oauth_token,
  user_id,
  verified_at,
  check_state
}
```

Exact storage key names may be chosen during implementation but must be explicit constants, independently addressable per service and migration-tested.

### 3.2 Existing installation migration

Current shared storage:

```text
wsmb_api_key
wsmb_folder_id
```

Migration rule:

```text
if dedicated Wordstat/Search records do not yet exist
→ copy current shared apiKey/folderId into both Wordstat and Search records
→ preserve current runtime behavior
→ never delete the old keys until a governed later cleanup proves no rollback/compatibility need
```

Dedicated records take precedence after migration.

### 3.3 Backup schema

Create a new versioned backup schema for service credentials.

Target payload shape:

```text
settings.credentials.wordstat
settings.credentials.search
settings.credentials.webmaster
```

Requirements:

- checksum remains canonical SHA-256 over settings payload;
- `contains_secrets=true` remains mandatory;
- export includes each enabled service credential in its own record;
- import restores credentials to the matching service only;
- current V2 backup remains import-compatible and migrates its shared Wordstat/Search credential to both dedicated records;
- do not guess unsupported historical schemas; add older-schema migration only from exact recovered evidence;
- active RUN/manual transaction safety rules remain unchanged;
- import never restores active execution transactions.

## 4. Credential Check semantics

### Webmaster

Explicit Check:

```text
GET https://api.webmaster.yandex.net/v4/user
Authorization: OAuth <token>
Accept: application/json
```

Success stores `user_id` and `verified_at`.

Failures:

```text
401 → INVALID_OR_EXPIRED
403/general permission denial → NO_ACCESS
network unknown → check failed; no automatic retry
```

### Wordstat

Use a governed read-only/non-billable credential probe only if the current official provider contract still proves it safe at implementation/live-check time. The existing `getRegionsTree` path is the preferred candidate because current policy models it at zero RUB. Verify current provider authority before shipping the live Check.

### Search

There is no assumed free credential-probe endpoint. Do not silently spend money to test Search credentials.

If live verification requires one real Search request:

```text
UI explicitly says the check is billable
→ operator explicitly confirms
→ exactly one request
→ no automatic retry
```

Controlled tests use a stub and never real credentials/provider traffic.

## 5. Webmaster protocol implementation

Add new shared protocol module, expected path:

```text
extension/src/shared/webmaster_protocol.js
```

Responsibilities:

- parse `WEBMASTER_API_V1`;
- strict allowed-field validation;
- method-specific normalization;
- enums/ranges/date validation;
- safe path/query construction;
- provider error normalization;
- `WEBMASTER_RESULT_V1` construction/formatting;
- zero credential knowledge inside command payload.

First-slice methods:

```text
listHosts
getSummary
getDiagnostics
getPopularQueries
```

## 6. Service registry/core integration

Update the service registry to add:

```text
WEBMASTER: webmaster
prefix: WEBMASTER_API_V1
```

Update all service-dispatch surfaces that currently enumerate only Wordstat/Search:

```text
service registry
credential registry
policy model
service worker executor/router
popup active-service selector
settings public state
backup import/export
command discovery tests
service-isolation tests
```

No fallback from Webmaster to another adapter.

## 7. Policy model

Add Webmaster policy:

```text
manual_enabled = true
autorun_enabled = false
allowed_methods = [listHosts, getSummary, getDiagnostics, getPopularQueries]
max_requests_per_run = 50
method_cost_rub = 0
max_cost_rub_per_run = 0
```

Do not claim this local limit equals provider quota.

Provider 429 errors are terminal for the individual request and are never automatically retried.

## 8. Service worker/provider implementation

Add `executeWebmasterCommand` / equivalent service adapter path.

Rules:

```text
credentials/policy/validation complete before fetch
one admitted command = exactly one provider fetch
Authorization header built only inside trusted worker/provider layer
GET only for first slice
Accept: application/json
no token in logs/errors/result
```

The runtime MUST NOT call `/v4/user` implicitly for every API command. `user_id` must come from the saved verified Webmaster credential metadata.

Request truthfulness:

```text
pre-fetch reject → false
HTTP response received → true
unknown post-initiation outcome → UNKNOWN
never blind retry
```

## 9. Popup/UI implementation

Popup must remain within governed **430×560** geometry.

Requirements:

- active service selector includes Webmaster;
- service-specific credential section switches with/alongside selected service;
- OAuth token input is password/masked by default;
- derived Webmaster user ID is displayed as non-secret status metadata, not editable command data;
- Save and Check are distinct actions;
- Check status states are explicit (`not checked`, `checking`, `valid`, `invalid/expired`, `no access`, `network error`);
- no secret values are placed in DOM text/log plaques beyond the masked input value;
- Export/Import controls remain available;
- UI must not expand native popup beyond 430×560; use bounded scroll/collapsible service credential sections if necessary.

## 10. Protocol validation matrix

Development tests must cover at minimum:

### Common

```text
missing method
unsupported method
unknown field
credential fields supplied in command → reject
wrong active service → zero provider
missing Webmaster credential → zero provider
missing derived user_id → zero provider
manual disabled → zero provider
autorun disabled → zero provider
request limit → zero provider
```

### Host methods

```text
missing hostId
empty hostId
oversized hostId
safe percent-encoding
```

### Popular queries

```text
invalid orderBy
invalid queryIndicator
invalid deviceTypeIndicator
invalid offset
limit 0
limit 501
invalid dateFrom/dateTo
unknown field
```

## 11. Provider normalization tests

Controlled provider fixtures must cover:

```text
listHosts 200
getSummary 200
getDiagnostics 200
getPopularQueries 200
401 Unauthorized
403 INVALID_USER_ID
404 HOST_NOT_VERIFIED
404 HOST_NOT_INDEXED
404 HOST_NOT_LOADED
429 QUOTA_EXCEEDED
429 TOO_MANY_REQUESTS_ERROR
500 provider error
network/timeout unknown outcome
malformed JSON response
```

Assertions include `request_executed` and `automatic_retry=false` for every path.

## 12. Credential migration/export/import tests

Mandatory tests:

```text
existing shared apiKey/folderId → Wordstat dedicated record
existing shared apiKey/folderId → Search dedicated record
migration idempotent
service records may diverge after migration
Webmaster token never copied into other services
V2 backup import → dedicated Wordstat/Search records
new backup export → three service credential records
new backup re-import → exact service mapping preserved
checksum tamper → reject before mutation
active RUN/manual safety preserved
secrets absent from logs/result/error
```

## 13. Browser/runtime tests

Qualified Chrome/Puppeteer coverage must prove:

```text
popup remains 430×560
Webmaster appears as service
Webmaster OAuth save/check against controlled endpoint
Check stores derived user_id
wrong/expired token status shown without secret leak
service switching does not overwrite credentials
Export/Import retains service mapping
Manual Webmaster block gets one Yandex action
lifecycle button gating still works during Webmaster Manual lifecycle
controlled Webmaster request reaches only Webmaster stub
zero real Yandex requests
```

## 14. Gate update

Before freeze, add a Phase-3 Webmaster addendum to the permanent Codex gate mapping every new assertion to executable Node/browser/stub coverage.

Complete pre-delivery campaign must include all existing Phase-1/2/core regressions plus all enabled Webmaster sections. No `NOT_RUN` in PASS.

## 15. Owner-live boundary

After exact Codex PASS, owner-live is intentionally narrow:

```text
1. enter/save real Webmaster OAuth token
2. Check token once → user_id confirmed
3. execute one read-only command (`listHosts` preferred)
4. optionally one host `getSummary` only if needed to confirm host-specific route
```

No repetitive calls. No write endpoints. No synthetic quota/error testing against real Yandex.

## 16. Implementation order

```text
A. commit Phase-3 contract/plan/gate addendum
B. create dev branch from exact accepted lifecycle source 939e880f...
C. implement dedicated credential storage + migration + backup schema
D. implement Webmaster protocol + registry + policy
E. implement worker executor/provider normalization
F. implement popup service credential UI within 430×560
G. add focused/unit/integration/browser tests
H. run focused development verification
I. freeze exact candidate
J. exact artifact transport round-trip
K. independent Codex complete applicable gate
L. narrow owner-live acceptance
M. close Phase 3 and unblock Phase 4 Metrika
```
