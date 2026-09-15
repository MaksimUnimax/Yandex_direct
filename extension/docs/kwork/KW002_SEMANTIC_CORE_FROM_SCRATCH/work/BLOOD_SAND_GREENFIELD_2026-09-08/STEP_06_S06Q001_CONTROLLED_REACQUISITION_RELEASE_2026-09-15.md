# KW-002 Step06 — S06Q001 CONTROLLED REACQUISITION RELEASE

Date: 2026-09-15
Status: **ONE CONTROLLED REACQUISITION RELEASED / OLD OPERATION FROZEN / NO S06Q002**

## Why reacquisition is required

The first S06Q001 deferred Search lifecycle did not produce durable Search result evidence:

1. the original submit was accepted and produced operation `spr2q2fbfldmt6poichd`;
2. first collect settled as `ASYNC_NETWORK_OUTCOME_UNKNOWN`;
3. second collect definitely reached Operation.Get and returned HTTP 404;
4. no raw Search result was received;
5. normalized Search rows remain 0;
6. the old operation is frozen from further blind GET attempts.

The query `S06Q001 / амулет` is the first mandatory representative Step06 discovery probe. Step06 cannot honestly treat the missing result as zero-result evidence and cannot advance to S06Q002 while this first released probe has no usable Search evidence.

Therefore one reacquisition is authorized as an explicit recovery action. It is not an automatic retry and it does not overwrite or erase the failed original lifecycle.

## Rule basis

Current KW-002 Level1 requires:
- no blind/automatic retry;
- explicit incremental information gain for new provider calls;
- technical failure must not become negative semantic evidence;
- complete durable persistence/readback before the next provider action;
- truthful uncertainty when evidence is missing.

Incremental information gain of this reacquisition:

```text
MISSING REQUIRED S06Q001 SERP EVIDENCE
-> reacquire exactly the same bounded query once
-> either obtain the missing current Search evidence
   OR produce a second, freshly controlled provider lifecycle showing a current reproducible blocker
```

Either outcome is informative. Repeating the old Operation.Get is not.

## Current provider/method recheck

Official Yandex sources rechecked 2026-09-15:
- Operation.Get endpoint: https://aistudio.yandex.ru/ru/docs/search-api/api-ref/Operation/get
- deferred mode: https://aistudio.yandex.ru/ru/docs/search-api/operations/web-search
- limits: https://aistudio.yandex.ru/en/docs/search-api/concepts/limits
- pricing: https://aistudio.yandex.ru/ru/docs/search-api/pricing

Current facts used:
- deferred minimum processing time: 5 minutes;
- deferred result maximum retention: 12 hours;
- daytime deferred price: 30.5 RUB / 1000 requests;
- nighttime deferred price: 25.41 RUB / 1000 requests.

Accepted Bridge v0.1.6 live smoke evidence also proves that the installed deferred Operation.Get path has previously completed successfully (`B19_OWNER_SMOKE_TEST_12_REAL_COLLECT_PASS_2026-09-13.md`).

## Reacquisition identity

```text
QUERY_ID = S06Q001
ACQUISITION_ATTEMPT = CONTROLLED_REACQUISITION_R1
QUERY_TEXT = амулет
COVERAGE_DIRECTION = GENERIC_PRODUCT
SOURCE_FAMILY_ID = PSF001
OLD_JOB_ID = kw002-s06q001-20260914
OLD_OPERATION_ID = spr2q2fbfldmt6poichd
NEW_JOB_ID = kw002-s06q001-r1-20260915
```

The query text and Search parameters MUST remain identical to the original released probe so the recovery changes only provider lifecycle identity, not analytical scope.

## Exact Search contract

```text
SEARCH_TYPE = SEARCH_TYPE_RU
REGION = 225
PAGE = 0
GROUPS_ON_PAGE = 20
DOCS_IN_GROUP = 1
GROUP_MODE = GROUP_MODE_FLAT
FAMILY_MODE = FAMILY_MODE_MODERATE
FIX_TYPO_MODE = FIX_TYPO_MODE_OFF
SORT_MODE = SORT_MODE_BY_RELEVANCE
SORT_ORDER = SORT_ORDER_DESC
RESPONSE_FORMAT = FORMAT_XML (internal request construction)
MAX_REQUESTS = 1
MAX_COST_RUB = 0.0305
```

## Exact local start released now

```text
SEARCH_ASYNC_BATCH_API_V1 {"action":"start","jobId":"kw002-s06q001-r1-20260915","queries":["амулет"],"confirmBillable":true,"maxRequests":1,"maxCostRub":0.0305,"searchType":"SEARCH_TYPE_RU","region":"225","page":0,"groupsOnPage":20,"docsInGroup":1,"groupMode":"GROUP_MODE_FLAT","familyMode":"FAMILY_MODE_MODERATE","fixTypoMode":"FIX_TYPO_MODE_OFF","sortMode":"SORT_MODE_BY_RELEVANCE","sortOrder":"SORT_ORDER_DESC"}
```

`start` is local only. Expected safe outcome has `request_executed=false` and `provider_calls=0`.

## Provider-call gate after start

If and only if the exact new-job start returns PASS with no provider request, one later `submitN count=1` may be released for `kw002-s06q001-r1-20260915` after start truth is reconciled.

No provider submission is authorized by this file before the local start result is observed.

## Hard boundaries

```text
OLD_JOB_START_OR_SUBMIT = FORBIDDEN
OLD_OPERATION_FURTHER_COLLECT = FORBIDDEN
NEW_JOB_LOCAL_STARTS_RELEASED_NOW = 1
NEW_JOB_PROVIDER_SUBMISSIONS_RELEASED_NOW = 0
NEW_JOB_COLLECTIONS_RELEASED_NOW = 0
S06Q002_RELEASED = false
STEP07_STARTED = false
AUTOMATIC_RETRY = false
SECOND_REACQUISITION = NOT_AUTHORIZED
```

If the controlled replacement itself encounters a material provider/transport failure, stop and persist that truth before deciding anything else. Do not silently create another job.
