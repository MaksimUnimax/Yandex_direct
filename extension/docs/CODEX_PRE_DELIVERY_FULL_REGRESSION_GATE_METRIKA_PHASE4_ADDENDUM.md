# Codex pre-delivery full regression gate — Phase 4 Metrika addendum

Status: **MANDATORY WHEN METRIKA PRODUCT BYTES ARE PRESENT**  
Adopted: 2026-08-26

This addendum extends `CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md` for the first Phase-4 Metrika slice. It does not replace any existing Phase-1/2/3/core gate section.

## M-00 — authority / exact candidate

Require:

```text
live main reconstructed
Phase-3 owner-live closure present
current Phase-4 spec/plan read
exact Phase-4 candidate source established
exact handoff ZIP SHA/bytes/files/entries established
exact artifact transported and round-tripped
zero product/test/harness mutation during final gate
```

Before Phase-4 development starts, accepted Phase-3 `extension/src` tree identity must be proven as:

```text
e5fa694f1354e1ee048a352481a416413e94a3c9
```

## M-01 — registry and future-prefix lock

Before Metrika implementation, `METRIKA_API_V1` must remain non-executable. After implementation require exactly one service registration:

```text
service = metrika
prefix = METRIKA_API_V1
result = METRIKA_RESULT_V1
```

Unknown service/prefix remains local/no-provider.

## M-02 — protocol strictness

Execute source and packaged protocol tests covering:

```text
listCounters
getCounter
getTrafficSummary
getTrafficByTime
missing method
unsupported method
unknown field
credential/token/header supplied in command
raw URL supplied in command
counterId validation
page/perPage/permission validation
date range validation
366-day local report span guard
group enum day|week|month
```

Arbitrary metrics, dimensions, filters, preset, headers or provider URL injection must be rejected before provider initiation.

## M-03 — credential isolation

Require four independently addressable service credential records:

```text
Wordstat != Search != Webmaster != Metrika
```

Metrika uses only its dedicated OAuth token and must never implicitly reuse the Webmaster OAuth token.

No OAuth token or Authorization header may appear in commands, public state, result envelopes, errors, diagnostics, DOM text, logs or final QA evidence.

## M-04 — credential migration / backup

Controlled tests must prove:

```text
existing backup without Metrika imports without corrupting existing services
new backup carries four service credential records
new export/import preserves exact four-way service mapping
Metrika token never copied into Webmaster or other services
Webmaster token never copied into Metrika
blank masked Save preserves existing Metrika token
partial common-settings Save does not overwrite Metrika token
checksum tamper rejects before mutation
active Manual/Autorun safety state is not restored from backup
runtime transaction state is never restored from backup
```

Any backup schema version bump must have explicit migration tests.

## M-05 — Metrika Check

Against controlled stub only:

```text
GET /management/v1/counters?per_page=1
Authorization: OAuth <fake-token>
Accept: application/json
```

Require exactly one provider request and status normalization:

```text
200 with counters → PRESENT
200 with empty counters → PRESENT
401 → INVALID_OR_EXPIRED
403 → NO_ACCESS
420 → QUOTA
429 → QUOTA
network fault → NETWORK_ERROR
```

`automatic_retry=false` in every Check outcome. Real credentials and real Yandex requests are forbidden in the controlled gate.

## M-06 — policy

Require default policy:

```text
manual_enabled = true
autorun_enabled = false
allowed_methods = listCounters,getCounter,getTrafficSummary,getTrafficByTime
max_requests_per_run = 50
max_report_days = 366
method_cost_rub = 0
max_cost_rub_per_run = 0
```

Policy rejects before network with `request_executed=false`.

The local 50-request ceiling must not be represented as a provider quota.

## M-07 — listCounters provider path

Controlled provider fixture:

```text
GET /management/v1/counters
```

Verify safe mapping of only governed optional fields:

```text
page
per_page
permission
```

Require exactly one provider request and allowlisted normalization of counter discovery metadata. Provider extras and secret-like fields must not leak into `METRIKA_RESULT_V1`.

## M-08 — getCounter provider path

Controlled fixture:

```text
GET /management/v1/counter/{counterId}
```

Require safe positive-integer path construction, no optional field expansions in the first slice, exactly one provider request, and normalization to an allowlisted safe counter metadata subset.

## M-09 — getTrafficSummary provider path

Controlled fixture:

```text
GET /stat/v1/data
ids={counterId}
metrics=ym:s:visits,ym:s:users,ym:s:pageviews
date1={resolved dateFrom}
date2={resolved dateTo}
```

Require exactly one request. No dimensions, filters, preset, Direct client logins or arbitrary metrics may be sent.

Map provider `totals` in fixed order to:

```text
visits
users
pageviews
```

and preserve governed truth metadata including sampling/privacy/data-lag fields when present.

## M-10 — getTrafficByTime provider path

Controlled fixture:

```text
GET /stat/v1/data/bytime
ids={counterId}
metrics=ym:s:visits,ym:s:users,ym:s:pageviews
date1={resolved dateFrom}
date2={resolved dateTo}
group={day|week|month}
```

Require exactly one request. Preserve provider temporal ordering and deterministic metric association to visits/users/pageviews.

## M-11 — provider errors / quota compatibility

Controlled fixtures must cover at minimum:

```text
400 provider-side invalid request
401 Unauthorized
403 access denied
404 counter not found/unavailable
420 quota compatibility response
429 quota response
500 provider error
malformed provider JSON
```

Any HTTP response received means `request_executed=true`; no automatic retry.

## M-12 — unknown outcome / no blind retry

Controlled network fault after provider initiation:

```text
request_executed = UNKNOWN
automatic_retry = false
no replay of identical provider initiation
```

A network unknown must never be silently converted to a safe-to-retry pre-fetch failure.

## M-13 — service isolation

Require all directions:

```text
active non-Metrika + METRIKA_API_V1 → local SERVICE_NOT_ACTIVE / zero Metrika provider request
active Metrika + WORDSTAT_API_V1 → zero Metrika provider request
active Metrika + SEARCH_API_V1 → zero Metrika provider request
active Metrika + WEBMASTER_API_V1 → zero Metrika provider request
```

Credential isolation must be proven independently of routing isolation.

## M-14 — Manual lifecycle

Installed-extension browser/runtime coverage against controlled Metrika provider route must prove:

```text
one eligible METRIKA_API_V1 assistant block → exactly one Yandex action
click → one Manual admission
while manual operation/delivery active → action disabled/non-clickable
blocked click → no second execution
completion → action re-enabled
one admitted command → at most one provider request
```

At minimum exercise `listCounters` and `getTrafficSummary` through the real installed-extension lifecycle.

Existing lifecycle-button regressions remain mandatory.

## M-15 — popup credentials / geometry

Qualified Chrome/Puppeteer must prove:

```text
popup native geometry remains 430×560
Metrika appears in active-service selector
Metrika OAuth input is masked
Save and Check are distinct
saved secret is absent from visible DOM after rerender
Check status is visible without secret leakage
service switching preserves all credentials independently
Metrika policy controls stay inside bounded internal scroll
```

## M-16 — Export/Import UI

Browser/runtime test must export and re-import a controlled secret-bearing backup and prove:

```text
Wordstat credential restored to Wordstat
Search credential restored to Search
Webmaster credential restored to Webmaster
Metrika credential restored to Metrika
no cross-service overwrite
checksum enforced
```

Never print any secret value in final evidence.

## M-17 — Autorun default lock / controlled enablement

Require:

```text
Metrika Autorun default OFF
start while disabled → local AUTORUN_DISABLED / zero provider
controlled explicit enable → common Autorun lifecycle may execute one first-slice command
active service remains immutable for admitted run
one command fingerprint admission
one provider request
one delivery
no duplicate execution
pause/resume/finish semantics unchanged
```

No write-capable Metrika method may be registered.

## M-18 — response truth / first-slice future locks

Controlled response tests must prove:

```text
listCounters allowlists fields
getCounter omits unrequested expansions/secrets
traffic summary fixed visits/users/pageviews mapping
bytime fixed metric mapping and temporal order
sampled preserved
sample_share preserved
sample_size preserved
sample_space preserved
contains_sensitive_data preserved
data_lag preserved
```

All deferred Metrika surfaces remain unavailable, including:

```text
management mutations
counter create/update/delete
goal mutations
filters/operations mutations
Import API
Logs API
arbitrary raw Reports API constructor
arbitrary metrics/dimensions/filters/preset
POST/PUT/PATCH/DELETE provider operations
```

Unsupported method/field must reject locally with `request_executed=false` and zero provider request.

## M-19 — cleanliness / safety / final acceptance

Final campaign requires:

```text
real_credentials_used = NO
real_yandex_requests = 0
production_modified_during_gate = NO
package_tests_modified_during_gate = NO
metrika_harness_modified_during_gate = NO
source_workspace_clean = PASS
transport_workspace_clean = PASS
enabled_not_run_sections = 0
```

Final evidence must also prove exact candidate/product immutability after all source/browser tests.

## Final report extension

A PASS campaign containing Metrika must report at minimum:

```text
M-00: PASS
M-01: PASS
...
M-19: PASS
metrika_controlled_provider_requests: <actual integer>
metrika_real_yandex_requests: 0
metrika_real_credentials_used: NO
NOT_RUN_COUNT=0
PRODUCT_BYTES_POST_TEST=IDENTICAL
```

No enabled Metrika section may be `NOT_RUN` in a PASS verdict.

## Owner-live boundary after exact Codex PASS

Owner-live remains outside the controlled pre-delivery gate and is intentionally narrow:

```text
1. save one real OAuth token carrying metrika:read
2. Check exactly once
3. listCounters exactly once
4. if a real counter exists, getTrafficSummary exactly once for a short bounded period
5. getTrafficByTime at most once only if still needed to prove the chart/time route
```

No write/import/Logs operations and no quota/error experiments against the real provider.
