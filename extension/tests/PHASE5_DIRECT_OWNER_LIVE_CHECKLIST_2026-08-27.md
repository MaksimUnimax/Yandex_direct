# Phase 5 Direct — owner-live acceptance checklist

Date: 2026-08-27

Status: **AUTHORIZED AFTER INDEPENDENT PASS / OWNER ACTION REQUIRED / PHASE 5 NOT CLOSED**

## 0. Exact product under test

Use the exact frozen candidate only. Do not rebuild, edit, repack, or substitute another extension package.

```text
candidate source = 841a1e2c1a503c4a05572a957ba97c55b9b60c52
extension/src tree = edf1c2d3494ebbc53ae778d23be1457eb885b605
freeze run = 33037955943
artifact id = 9632728199
artifact name = phase5-direct-r2-frozen-candidate-841a1e2
inner ZIP = yandex-marketing-bridge-0.1.1-phase5-direct-first-slice-r2-candidate.zip
SHA-256 = ac8efc444578e9d3f31ac0325baca4b286fd608bc511850f480e0d397936620b
bytes = 406656
files = 39
```

Independent pre-delivery acceptance is recorded in:

```text
extension/tests/PHASE5_DIRECT_R2_CODEX_COMPLETE_PASS_2026-08-27.md
```

## 1. Hard live-safety rules

Owner-live is intentionally narrow.

Do not:

- paste the Direct OAuth token into chat, screenshots, logs, evidence, or issue text;
- reuse the Webmaster or Metrika OAuth token;
- replace the dedicated Direct credential with a shared credential;
- perform any Direct write/mutation operation;
- change bids, budgets, campaigns, ads, keywords, finance/payment state, or account settings;
- intentionally provoke provider errors, quota exhaustion, Units exhaustion, or concurrency errors;
- use offline Reports mode or polling;
- retry an initiated request just because the result is unknown or slow;
- repeat successful requests merely for exploration.

Stop the live sequence immediately on an unexpected provider/product error and record the non-secret result before doing anything else.

## 2. Provider/account prerequisites

Before sending any real API request, confirm outside this repository:

```text
[ ] the OAuth application has Direct scope: direct:api
[ ] the Direct API access request for the application/account is approved for production use
[ ] the token to be saved is the dedicated Direct OAuth token
```

If production Direct API access is not approved, stop. Do not treat Sandbox/trial access as owner-live production acceptance.

## 3. Install / select service

```text
[ ] install/load the exact frozen candidate identified in section 0
[ ] open the extension popup
[ ] select Yandex Direct as the active service
[ ] confirm Direct Autorun remains disabled in the production popup
```

Do not modify product files after loading the candidate.

## 4. Dedicated Direct credential

In the Direct credential card:

```text
OAuth token = enter the dedicated Direct token locally in the popup
Client-Login = leave blank for an ordinary advertiser account
```

Use `Client-Login` only if this is an agency/operator account acting for a specific client and the exact client login is required for that account relationship.

Then:

```text
[ ] click Direct Save once
[ ] confirm the saved OAuth token is not rendered back into the password field
```

Do not change/re-save the Webmaster or Metrika OAuth credentials during this test.

## 5. Direct Check — exactly once

The Check action is a real read-only provider request and spends Direct Units.

```text
[ ] click Direct Check exactly once
```

Expected product behavior:

```text
one POST only
Campaigns.get
FieldNames = ["Id"]
Limit = 1
no automatic retry
```

Record only non-secret evidence:

```text
check_status = <visible normalized status>
provider_request_id = <value if shown, otherwise null>
provider_units = <spent/remaining/daily_limit if shown, otherwise null>
```

PASS condition: the credential/capability check returns a governed successful state. Zero campaigns is valid.

If Check returns an error or unknown outcome, STOP. Do not click Check again.

## 6. Manual listCampaigns — exactly once

With Direct active and Manual mode enabled, submit exactly one bounded command:

```text
DIRECT_API_V1
{"method":"listCampaigns","limit":10,"offset":0}
```

Then use the normal Manual action button exactly once for that command.

Record the resulting `DIRECT_RESULT_V1` without secrets. At minimum record:

```text
operation = listCampaigns
status = <...>
request_id = <bridge request id if present>
http_status = <...>
request_executed = <true/false>
automatic_retry = <true/false>
provider_request_id = <... or null>
provider_units = <... or null>
result_count = <number of normalized campaigns>
first_campaign_id = <id or null>
first_campaign_name = <name or null>
```

PASS condition:

```text
status = OK
request_executed = true
automatic_retry = false
```

An empty campaign array is a valid live PASS for this step.

If this request returns an error or unknown provider outcome, STOP. Do not repeat it.

## 7. Optional one bounded downstream read

Run this section only if `listCampaigns` returned at least one real campaign and a downstream-object proof is useful.

Choose one returned campaign ID and execute **one** bounded `listAdGroups` read:

```text
DIRECT_API_V1
{"method":"listAdGroups","campaignIds":[<CAMPAIGN_ID>],"limit":10,"offset":0}
```

Use the Manual action once.

Record:

```text
operation = listAdGroups
status = <...>
request_executed = <true/false>
automatic_retry = <true/false>
provider_request_id = <... or null>
provider_units = <... or null>
result_count = <number of normalized ad groups>
```

Do not add `listAds`/`listKeywords` merely to increase coverage. Controlled QA already covers those routes.

If there is no campaign, mark this section `NOT_APPLICABLE_EMPTY_ACCOUNT`.

## 8. One short online performance report

Run this section only if a real campaign exists and the account has a date range where campaign data can reasonably exist.

Prefer a **single calendar day** known to contain or plausibly contain activity. Use one returned campaign ID when possible.

Example shape:

```text
DIRECT_API_V1
{"method":"getCampaignPerformance","dateFrom":"YYYY-MM-DD","dateTo":"YYYY-MM-DD","campaignIds":[<CAMPAIGN_ID>],"limit":100,"offset":0}
```

Use the normal Manual action exactly once.

Expected product behavior:

```text
online Reports request only
no polling
no automatic retry
fixed governed fields only
```

Record:

```text
operation = getCampaignPerformance
status = <...>
request_executed = <true/false>
automatic_retry = <true/false>
provider_request_id = <... or null>
provider_units = <... or null>
report_rows = <number>
first_row_date = <date or null>
first_row_campaign_id = <id or null>
```

Zero rows is acceptable if the provider returns a successful valid online report for the selected real campaign/date.

If there is no real campaign or no reasonable real-data date, mark this section `NOT_APPLICABLE_NO_REAL_DATA` rather than generating artificial traffic or repeating queries.

If the report returns 201/202, an online-generation error, provider error, or unknown transport outcome, STOP. Do not poll or replay.

## 9. Owner-live PASS criteria

Minimum required PASS chain:

```text
exact frozen candidate identity = CONFIRMED
direct:api scope = CONFIRMED
production Direct API access = APPROVED
dedicated Direct credential save = PASS
Direct Check exactly once = PASS
listCampaigns exactly once = PASS
no automatic retry = PASS
no write/mutation endpoint = PASS
no secret exposure = PASS
```

Conditional live evidence:

```text
listAdGroups = PASS or NOT_APPLICABLE_EMPTY_ACCOUNT
getCampaignPerformance = PASS or NOT_APPLICABLE_NO_REAL_DATA
```

A provider/product error is not converted into PASS by retrying.

Phase 5 may be closed only after the owner returns sufficient non-secret evidence for the applicable steps and that evidence is recorded in a permanent `PHASE5_DIRECT_OWNER_LIVE_PASS_2026-08-27.md` acceptance record.

## 10. Return template

Return this template to the project chat. Never include the OAuth token or Authorization header.

```text
PHASE5_DIRECT_OWNER_LIVE_RESULT

exact_candidate_loaded: YES/NO
direct_api_scope_confirmed: YES/NO
production_direct_access_approved: YES/NO
client_login_mode: BLANK_ORDINARY_ACCOUNT / AGENCY_CLIENT_LOGIN

check:
  attempted: YES
  status: <...>
  provider_request_id: <... or null>
  provider_units: <... or null>
  automatic_retry: NO

listCampaigns:
  attempted: YES
  status: <...>
  http_status: <...>
  request_executed: <true/false>
  automatic_retry: <true/false>
  provider_request_id: <... or null>
  provider_units: <... or null>
  result_count: <...>
  first_campaign_id: <... or null>
  first_campaign_name: <... or null>

listAdGroups:
  attempted: YES/NO
  status: <PASS / NOT_APPLICABLE_EMPTY_ACCOUNT / error code>
  request_executed: <true/false/not_applicable>
  automatic_retry: <true/false/not_applicable>
  provider_request_id: <... or null>
  provider_units: <... or null>
  result_count: <... or null>

getCampaignPerformance:
  attempted: YES/NO
  status: <PASS / NOT_APPLICABLE_NO_REAL_DATA / error code>
  date_from: <YYYY-MM-DD or null>
  date_to: <YYYY-MM-DD or null>
  campaign_id: <id or null>
  request_executed: <true/false/not_applicable>
  automatic_retry: <true/false/not_applicable>
  provider_request_id: <... or null>
  provider_units: <... or null>
  report_rows: <... or null>

writes_or_mutations_executed: NO
retries_after_provider_initiation: NO
secret_in_evidence: NO

owner_live_verdict: PASS / FAIL / STOPPED_ON_ERROR
```
