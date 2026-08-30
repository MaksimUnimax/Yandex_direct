# KW-001 / OKNO-MSK — STEP 11 WEBMASTER BRIDGE PROBE

Date: 2026-08-30
Status: **EXECUTED / API REACHABLE / ZERO HOSTS RETURNED / HOST-SCOPED METHODS BLOCKED**

## Manual probe

```text
service = webmaster
method = listHosts
channel = manual
request_id = webmaster-dfb58cef-de8a-49d0-baa1-2e48b4bc9f1f
http_status = 200
request_executed = true
automatic_retry = false
estimated_cost_rub = 0
bridge_reported_version = 0.1.1
result.hosts = []
```

## Interpretation

The Yandex Webmaster API request itself succeeded. The active OAuth/user context visible to the Bridge returned zero Webmaster hosts.

Therefore the current execution has no evidence-backed `hostId` and must not guess one.

```text
LIST_HOSTS_API_REACHABLE = true
WEBMASTER_HOSTS_RETURNED = 0
OKNO_MSK_HOST_ID_RESOLVED = false
GET_SUMMARY_ALLOWED = false until hostId resolved
GET_DIAGNOSTICS_ALLOWED = false until hostId resolved
GET_POPULAR_QUERIES_ALLOWED = false until hostId resolved
```

## Important version observation

The running Bridge result reports version `0.1.1`, while the current repository product/manifest authority is `0.1.2`.

This mismatch must be corrected or explicitly accepted before relying on the local extension as current production evidence.

## Next diagnostic actions

1. Verify in the Yandex Webmaster browser UI whether `okno-msk.ru` is visible under the currently logged-in Yandex account.
2. Verify that the OAuth token stored in the Bridge belongs to the Yandex account that has access to that property.
3. Update/reload the local extension to the current repository build `0.1.2` and preserve/recheck credentials.
4. Re-run `WEBMASTER_API_V1 {"method":"listHosts"}` only after account/version correction; do not blind-repeat the current zero-host call.
5. In parallel, use authorized Work/Cloud Browser access to collect the query↔URL Webmaster evidence so Step 11 does not stop on the Bridge account mismatch.

## Evidence discipline

```text
HTTP_200 != TARGET_SITE_ACCESS_CONFIRMED
EMPTY_HOST_LIST != HOST_NOT_EXISTING
EMPTY_HOST_LIST = CURRENT_API_ACCOUNT_CONTEXT_SEES_ZERO_HOSTS
HOST_ID_MUST_NOT_BE_GUESSED
```
