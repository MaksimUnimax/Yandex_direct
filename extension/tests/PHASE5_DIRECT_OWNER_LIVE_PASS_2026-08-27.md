# Phase 5 Direct — owner-live PASS

Date: 2026-08-27

Status: **OWNER-LIVE PASS / FINAL INTEGRATION AUTHORIZED / PHASE 5 NOT CLOSED UNTIL POST-MERGE GATE**

## Scope

Owner-live validation was performed against the exact frozen Phase 5 Direct R2 candidate and the dedicated local Direct credential. No OAuth token, authorization header, or other secret is recorded in this evidence.

Accepted authority:

```text
accepted source = 841a1e2c1a503c4a05572a957ba97c55b9b60c52
accepted extension/src tree = edf1c2d3494ebbc53ae778d23be1457eb885b605
frozen candidate run = 33037955943
frozen artifact id = 9632728199
frozen artifact name = phase5-direct-r2-frozen-candidate-841a1e2
inner ZIP SHA-256 = ac8efc444578e9d3f31ac0325baca4b286fd608bc511850f480e0d397936620b
```

Owner confirmed:

```text
exact frozen candidate loaded = YES
Direct Check = PASS
```

## Live read-only request

Exactly one governed `listCampaigns` request was executed after Direct Check:

```text
protocol = DIRECT_API_V1
method = listCampaigns
limit = 10
offset = 0
channel = manual
```

Observed result:

```text
result protocol = DIRECT_RESULT_V1
bridge = yandex-marketing-bridge
version = 0.1.1
service = direct
operation = listCampaigns
status = OK
http_status = 200
request_executed = true
automatic_retry = false
campaigns = []
provider_request_id = 8933639207276598861
provider_units_spent = 10
provider_units_remaining = 159980
provider_units_daily_limit = 160000
```

The returned account had no campaigns.

Therefore the downstream live checks are not applicable and were intentionally not executed:

```text
listAdGroups = NOT_APPLICABLE_EMPTY_ACCOUNT
getCampaignPerformance = NOT_APPLICABLE_NO_REAL_DATA
```

No campaign was created merely to manufacture test data.

## Safety boundary

Confirmed for this owner-live run:

```text
Direct OAuth credential = dedicated and local
credential secret recorded in evidence = NO
write/mutation request executed = NO
bids/budgets/finance mutation = NO
offline Reports flow = NO
intentional provider error/quota test = NO
blind retry after provider initiation = NO
repeated successful request for exploration = NO
```

The observed successful request is sufficient to prove the production Direct API path, credential separation, provider request execution, response normalization, `RequestId`, and `Units` preservation for the governed read-only first slice.

## Verdict

```text
PHASE5_DIRECT_OWNER_LIVE = PASS
DIRECT_CHECK = PASS
LIST_CAMPAIGNS = PASS
LIST_ADGROUPS = NOT_APPLICABLE_EMPTY_ACCOUNT
GET_CAMPAIGN_PERFORMANCE = NOT_APPLICABLE_NO_REAL_DATA
OWNER_LIVE_PRODUCT_DEFECT = NO
FINAL_INTEGRATION = AUTHORIZED
PHASE5_STATUS = OWNER-LIVE PASS / POST-MERGE GATE PENDING
```

Phase 5 must not be marked closed until the accepted product/evidence is integrated to `main` and `.github/workflows/phase5-direct-postmerge-final.yml` passes on `main` with `PHASE5_DIRECT_POSTMERGE_FINAL_PASS`.
