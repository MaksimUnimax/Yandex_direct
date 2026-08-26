# Codex pre-delivery full regression gate — Phase 3 Webmaster addendum

Status: **MANDATORY WHEN WEBMASTER PRODUCT BYTES ARE PRESENT**  
Adopted: 2026-08-26

This addendum extends `CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md` for the first Phase-3 Webmaster slice. It does not replace any existing Phase-1/2/core gate section.

## W-00 — authority / exact candidate

Require:

```text
live main reconstructed
current Phase-3 spec/plan read
exact candidate source established
exact handoff ZIP SHA/bytes/files/entries established
exact artifact transported and round-tripped
zero product/test/harness mutation during gate
```

## W-01 — registry and future-prefix lock

Before Webmaster implementation, `WEBMASTER_API_V1` must remain non-executable. After implementation, require exactly one `webmaster` service registration and one `WEBMASTER_API_V1` prefix.

Unknown service/prefix remains local/no-provider.

## W-02 — protocol strictness

Execute source and packaged protocol tests covering:

```text
listHosts
getSummary
getDiagnostics
getPopularQueries
missing method
unsupported method
unknown field
credential/Authorization fields rejected from command
hostId validation
popular-query enum/range/date validation
```

## W-03 — credential isolation

Require distinct credential records:

```text
Wordstat != Search != Webmaster
```

Webmaster uses OAuth token + derived user_id and never reads Api-Key/folderId as its credential.

No token/Authorization leakage in commands, results, errors, diagnostics or tracked QA evidence.

## W-04 — credential migration / backup

Controlled tests must prove:

```text
current shared apiKey/folderId migrates safely to dedicated Wordstat and Search records
migration is idempotent
records can diverge after migration
V2 backup import remains compatible
new backup export/import preserves service mapping
checksum tamper rejects before mutation
active execution safety state is not restored from backup
```

## W-05 — Webmaster Check

Against controlled stub only:

```text
explicit Check sends exactly one GET /v4/user
Authorization: OAuth <fake-token>
200 {user_id} stores derived user_id
401 → invalid/expired state
permission denial → no-access state
network error → no automatic retry
```

Real credentials/real Yandex requests = 0.

## W-06 — policy

Require default policy:

```text
manual_enabled = true
autorun_enabled = false
allowed methods = first-slice methods only
max_requests_per_run = 50
method cost = 0
max cost RUB = 0
```

Policy rejects pre-network with `request_executed=false`.

## W-07 — listHosts provider path

Controlled provider fixture:

```text
GET /v4/user/{user-id}/hosts
exactly one provider request
JSON normalized to WEBMASTER_RESULT_V1
request_executed=true
automatic_retry=false
```

## W-08 — getSummary provider path

Controlled fixture:

```text
GET /v4/user/{user-id}/hosts/{host-id}/summary
sqi/excluded/searchable/site_problems preserved
one provider request
```

## W-09 — getDiagnostics provider path

Controlled fixture:

```text
GET /v4/user/{user-id}/hosts/{host-id}/diagnostics
problem keys + severity/state/last_state_update preserved
one provider request
```

## W-10 — getPopularQueries provider path

Controlled fixture verifies exact query mapping and safe encoding for:

```text
order_by
query_indicator
device_type_indicator
date_from
date_to
offset
limit
```

Normalize `queries`, `date_from`, `date_to`, `count` without secret leakage.

## W-11 — provider errors

Controlled fixtures must cover at minimum:

```text
401 Unauthorized
403 INVALID_USER_ID
404 HOST_NOT_VERIFIED
404 HOST_NOT_INDEXED
404 HOST_NOT_LOADED
429 QUOTA_EXCEEDED
429 TOO_MANY_REQUESTS_ERROR
500 provider error
malformed provider JSON
```

HTTP response received means `request_executed=true`; no automatic retry.

## W-12 — unknown outcome / no blind retry

Controlled network fault after initiation:

```text
request_executed = UNKNOWN
automatic_retry = false
no replay of identical provider initiation
```

## W-13 — service isolation

Require both directions:

```text
active non-Webmaster + WEBMASTER_API_V1 → local SERVICE_NOT_ACTIVE/no Webmaster provider request
active Webmaster + WORDSTAT_API_V1/SEARCH_API_V1 → no cross-adapter execution
```

## W-14 — Manual lifecycle

Installed-extension browser/runtime coverage against controlled Webmaster stub:

```text
one eligible assistant block → exactly one Yandex action
click → one Manual admission
while manual operation/delivery active → action disabled/non-clickable
blocked click → no second execution
completion → action re-enabled
one provider request at most
```

Existing lifecycle gating regression remains mandatory.

## W-15 — popup credentials / geometry

Chrome/Puppeteer must prove:

```text
popup native geometry remains 430×560
Webmaster service is selectable
Webmaster OAuth input masked
Save and Check distinct
Check status visible without token leak
switching services preserves distinct credentials
```

## W-16 — Export/Import UI

Browser/runtime test must export and re-import a controlled secret-bearing backup and prove:

```text
Wordstat credential restored to Wordstat
Search credential restored to Search
Webmaster credential restored to Webmaster
no cross-service overwrite
checksum enforced
```

Never print secret values in final evidence.

## W-17 — Autorun default lock / controlled enablement

Require:

```text
Webmaster Autorun default OFF
start while disabled → local AUTORUN_DISABLED/no provider
controlled explicit enable → existing common Autorun lifecycle may execute first-slice read-only commands under request limit
```

No write-capable method is present.

## W-18 — first-slice future locks

All deferred Webmaster surfaces must remain unavailable, including writes, recrawl submission, Sitemap mutation, verification mutation and PRO export tasks.

Attempted unsupported method → local rejection, `request_executed=false`, no provider.

## W-19 — cleanliness / safety

Final campaign requires:

```text
real_credentials_used = NO
real_yandex_requests = 0
production_modified_during_gate = NO
package_tests_modified_during_gate = NO
webmaster_harness_modified_during_gate = NO
source_workspace_clean = PASS
transport_workspace_clean = PASS
enabled_not_run_sections = 0
```

## Final report extension

A PASS campaign containing Webmaster must report at minimum:

```text
W-00: PASS
W-01: PASS
...
W-19: PASS
webmaster_controlled_provider_requests: <actual integer>
webmaster_real_yandex_requests: 0
webmaster_real_credentials_used: NO
```

No enabled Webmaster section may be `NOT_RUN` in a PASS verdict.
