# CURRENT STATE — Yandex Marketing Bridge

Status: **PHASE 2 SEARCH = LIVE PASS / CLOSED — LIFECYCLE BUTTON PATCH = OWNER LIVE PASS / CLOSED — PHASE 3 WEBMASTER = CONTRACT READY / IMPLEMENTATION AUTHORIZED**  
Updated: 2026-08-26

Always fetch live `main` HEAD and commit metadata before any workflow-stage transition or control-plane write.

## Mandatory reconstruction record

```text
LIVE_HEAD_BEFORE_PHASE3_CONTRACT = 24d2994f420e748358f497ca246834e9880ec7fe

ACCEPTED_PHASE2_SOURCE = b7869180c229356a6b3d51ac980ec3da5df4c23c
ACCEPTED_PHASE2_ARTIFACT = ce824a9fff5ddee47bc0145f57db4da10c6352e782c859fa500e3a1fb98088aa / 179013 bytes / 69 files / 72 ZIP entries
ACCEPTED_PHASE2_FULL_GATE = PASS
ACCEPTED_PHASE2_OWNER_LIVE = PASS

ACCEPTED_LIFECYCLE_PATCH_SOURCE = 939e880f820e52beae9dcbcedc86d5cd9e13b075
ACCEPTED_LIFECYCLE_PATCH_PARENT = b7869180c229356a6b3d51ac980ec3da5df4c23c
ACCEPTED_LIFECYCLE_PATCH_ARTIFACT = yandex-marketing-bridge-0.1.1-lifecycle-button-gating-candidate.zip
ACCEPTED_LIFECYCLE_PATCH_SHA256 = 0430463ea979c31c5e74a48c899f2ce0fb141b62c4baf132df153380fbc0a262
ACCEPTED_LIFECYCLE_PATCH_BYTES = 179877
ACCEPTED_LIFECYCLE_PATCH_FILES = 69
ACCEPTED_LIFECYCLE_PATCH_ZIP_ENTRIES = 72
ACCEPTED_LIFECYCLE_PATCH_FULL_CODEX_GATE = PASS
ACCEPTED_LIFECYCLE_PATCH_OWNER_LIVE = PASS

PHASE3_IMPLEMENTATION_BASE = 939e880f820e52beae9dcbcedc86d5cd9e13b075
PHASE3_PROTOCOL = WEBMASTER_API_V1
PHASE3_RESULT = WEBMASTER_RESULT_V1
PHASE3_FIRST_SLICE = listHosts,getSummary,getDiagnostics,getPopularQueries
PHASE3_PROVIDER = Yandex Webmaster API v4.1
PHASE3_AUTH = OAuth token + derived user_id
PHASE3_WRITES_ENABLED = NO
PHASE3_CONTRACT = READY

PRODUCTION_BYTES_CHANGED_SINCE_LATEST_GATE = NO
PACKAGE_TEST_BYTES_CHANGED_SINCE_LATEST_GATE = NO
OPEN_BLOCKERS = NONE
AUTHORIZED_NEXT_STAGE = PHASE_3_WEBMASTER_IMPLEMENTATION_FROM_ACCEPTED_LIFECYCLE_SOURCE
```

## Accepted baseline

The accepted product baseline for Phase-3 development is the lifecycle-button artifact/source, not the older Phase-2 source:

```text
source = 939e880f820e52beae9dcbcedc86d5cd9e13b075
artifact = yandex-marketing-bridge-0.1.1-lifecycle-button-gating-candidate.zip
SHA-256 = 0430463ea979c31c5e74a48c899f2ce0fb141b62c4baf132df153380fbc0a262
bytes = 179877
files = 69
ZIP entries = 72
Codex complete applicable gate = PASS
owner real-profile acceptance = PASS
```

Durable lifecycle closure evidence:

```text
extension/tests/LIFECYCLE_BUTTON_GATING_CODEX_COMPLETE_PASS_2026-08-26.md
extension/tests/LIFECYCLE_BUTTON_GATING_OWNER_LIVE_PASS_2026-08-26.md
```

## Phase 3 — Webmaster reconstruction result

Current official authority checked 2026-08-26 establishes:

```text
API version = 4.1
base = https://api.webmaster.yandex.net/v4
auth = OAuth 2.0
header = Authorization: OAuth <token>
user identity = GET /v4/user → user_id
```

First slice is read-only only:

```text
listHosts
getSummary
getDiagnostics
getPopularQueries
```

Deferred/locked:

```text
host add/delete
verification mutations
recrawl submission
Sitemap mutation
important URL mutation
original text submission
PRO export tasks
query analytics POST
all other Webmaster POST/DELETE surfaces
```

Canonical Phase-3 documents:

```text
extension/docs/SPECIFICATION_PHASE_3_WEBMASTER_ADDENDUM.md
extension/docs/PHASE_3_WEBMASTER_REQUIREMENTS_AND_IMPLEMENTATION_PLAN.md
extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE_WEBMASTER_PHASE3_ADDENDUM.md
```

The base `SPECIFICATION.md` has been reconciled to Phase 3 and now treats Wordstat/Search/lifecycle as closed and Webmaster as active.

## Credential architecture requirement

Webmaster cannot reuse the existing Yandex Cloud `Api-Key + folderId`. Phase 3 therefore includes service-specific credential restoration/migration.

Required operator model before Phase-3 handoff:

```text
Wordstat  → dedicated Api-Key + folderId → Save → Check
Search    → dedicated Api-Key + folderId → Save → Check
Webmaster → dedicated OAuth token + derived user_id → Save → Check
Export/Import preserves exact service mapping
```

Migration must preserve current shared Wordstat/Search values and seed dedicated records without deleting old compatibility keys.

Webmaster Check is exactly one read-only `GET /v4/user`; successful Check stores derived `user_id`. Search Check must never silently create a billable request — explicit confirmation is required if no free credential probe exists.

## Phase-3 policy

Default Webmaster policy:

```text
manual_enabled = true
autorun_enabled = false
allowed_methods = [listHosts, getSummary, getDiagnostics, getPopularQueries]
max_requests_per_run = 50
method_cost_rub = 0
max_cost_rub_per_run = 0
```

This local request ceiling is not a claim about provider quota. Provider 429 responses are surfaced and never automatically retried.

## Error/exactly-once contract

```text
pre-fetch validation/credential/policy rejection → request_executed=false
HTTP response received → request_executed=true
unknown post-initiation network outcome → request_executed=UNKNOWN
automatic_retry=false in all cases
```

Runtime command execution must not silently call `/v4/user` before every command. The explicit credential Check workflow derives/stores `user_id`, preserving one accepted command = one provider request.

## Testing/gate requirement

Webmaster product bytes require the existing permanent full gate plus the new `W-00..W-19` Webmaster addendum.

Controlled QA:

```text
fake credentials only
controlled Webmaster provider/stub
zero real Yandex requests
no secret leakage
popup geometry remains 430×560
all enabled existing Phase-1/2/core regressions still run
all W-00..W-19 execute
PASS forbids enabled NOT_RUN
```

## Current authorized next action

```text
1. create Phase-3 dev branch from exact accepted source 939e880f...
2. implement credential storage/migration/backup foundation
3. implement Webmaster protocol/registry/policy/worker
4. implement bounded popup credential/service UI
5. add focused/unit/integration/browser tests
6. development verification only
7. freeze exact candidate only when implementation is working
```
