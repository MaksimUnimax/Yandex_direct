# KW-002 Step06 — S06Q001 DEFERRED SEARCH EXECUTION RELEASE

Date: 2026-09-14
Status: **RELEASED FOR EXACTLY ONE PROVIDER SUBMISSION / NO NEXT QUERY RELEASED**

## 1. Scope

This authority releases only the first current V2 representative-query row for Step06 competitor discovery.

```text
QUERY_ID = S06Q001
COVERAGE_DIRECTION = GENERIC_PRODUCT
SOURCE_FAMILY_ID = PSF001
QUERY_TEXT = амулет
SOURCE_STATUS = OBSERVED_REPRESENTATIVE_PHRASE
QUERY_ROLE = HEAD_TERM_DISCOVERY
BUSINESS_ALIGNMENT = CLIENT_PRODUCT_CLASS
COUNTING_ROLE = COUNT_SERP_DOMAIN_EVIDENCE
```

Source row: `STEP_06_REPRESENTATIVE_QUERY_MANIFEST_V2_2026-09-12.tsv`.

No other Step06 query is released by this file.

## 2. Release basis

Current KW-002 base before this release:

`2b9b157f55745302d1fb8676a967d3af885a2def`

Runtime/method reconciliation authority:

`STEP_06_RUNTIME_RECONCILIATION_AND_METHOD_REFRESH_2026-09-14.md`

Accepted Search runtime capability:

```text
YMB_VERSION = 0.1.6 live-accepted Search path
YMB_RELEVANT_COMMIT = 6fe2d2f992b4c35fbbc37783182e9236e9f5b1a1
RUNTIME_SEARCH_CONTRACT_RECONCILED = true
TRANSPORT = DEFERRED_ASYNC
```

The current owner-facing Step06 disclosure is already complete. Current official Yandex provider documentation/pricing was refreshed before this release.

## 3. Exact Search method contract

The accepted query semantics are unchanged:

```text
searchType = SEARCH_TYPE_RU
region = 225
page = 0
groupsOnPage = 20
docsInGroup = 1
groupMode = GROUP_MODE_FLAT
familyMode = FAMILY_MODE_MODERATE
fixTypoMode = FIX_TYPO_MODE_OFF
sortMode = SORT_MODE_BY_RELEVANCE
sortOrder = SORT_ORDER_DESC
responseFormat = FORMAT_XML (set by Search protocol, not a deferred-command field)
```

The accepted `SearchProtocol` supplies `LOCALIZATION_RU` and `maxPassages=4` as normal defaults when omitted. They are not new analytical decisions.

## 4. Exact Bridge command contract

The accepted v0.1.6 `SearchAsyncProtocol` requires a local `start` before provider transport. `start` creates the job and executes zero provider calls.

Exact released local start command:

```text
SEARCH_ASYNC_BATCH_API_V1 {"action":"start","jobId":"kw002-s06q001-20260914","queries":["амулет"],"confirmBillable":true,"maxRequests":1,"maxCostRub":0.0305,"searchType":"SEARCH_TYPE_RU","region":"225","page":0,"groupsOnPage":20,"docsInGroup":1,"groupMode":"GROUP_MODE_FLAT","familyMode":"FAMILY_MODE_MODERATE","fixTypoMode":"FIX_TYPO_MODE_OFF","sortMode":"SORT_MODE_BY_RELEVANCE","sortOrder":"SORT_ORDER_DESC"}
```

After successful local start and only under the same bound conversation/service context, exactly one provider submission is released:

```text
SEARCH_ASYNC_BATCH_API_V1 {"action":"submitN","jobId":"kw002-s06q001-20260914","count":1}
```

The protocol normalizes `submitN` to exactly one deferred Search submission here. `maxRequests=1` and `maxCostRub=0.0305` prevent this job from authorizing a second provider request or exceeding the conservative current daytime single-request cap.

## 5. Provider-call boundary

```text
LOCAL_START_CALLS_ALLOWED = 1
DEFERRED_SEARCH_SUBMISSIONS_ALLOWED = 1
DEFERRED_SEARCH_COLLECTION_CALLS_RELEASED_NOW = 0
SYNCHRONOUS_SEARCH_CALLS_ALLOWED = 0
WORDSTAT_CALLS_ALLOWED = 0
GENSEARCH_CALLS_ALLOWED = 0
AI_SEARCH_CALLS_ALLOWED = 0
NEXT_STEP06_QUERY_RELEASED = false
STEP07_STARTED = false
STEP08_STARTED = false
```

A provider submission is counted only from actual Bridge/provider execution truth. The release itself is not a provider call.

## 6. Evidence and durability gate

After the one submission:

1. preserve the returned job/request/operation identity and Bridge execution accounting;
2. if the provider returns the result immediately, preserve the complete normalized result envelope and every returned result row;
3. if the provider returns `WAITING`, persist the exact pending operation identity/state; do not submit another query;
4. do not make a collect provider call until it is due and separately consistent with the current pending state;
5. after result receipt, preserve query ID/text, request/operation ID, snapshot/received time, Search parameters, provider status, result count, and every rank/url/domain/title/snippet/modtime field that is present;
6. publish the evidence and remote-read it before any next query can be released.

No summary-only, top-domain-only, representative sampling or silent truncation is allowed.

## 7. Outcome contract

- `SUCCESS_WITH_RESULTS` → persist complete evidence, remote readback, reconcile, then separately decide whether S06Q002 can be released.
- `SUCCESS_WITH_ZERO_RESULTS` → bounded zero for this exact query/settings/snapshot only; persist and remote-readback before any next action.
- `WAITING` → persist pending operation identity and stop provider progression until due collection is safely authorized.
- `SUCCESS_BUT_EVIDENCE_INCOMPLETE` → unresolved; stop before any next provider action.
- validation/provider/unknown/normalization failure → preserve the failure truth; no competitor inference; no blind retry.

Automatic retry is forbidden.

## 8. Interpretation boundary

This is one bounded competitor-discovery probe, not a final keyword, final cluster, final intent, final page target, or full-SERP claim. Top-20 is a Step06 discovery cutoff only. Step12 FULL_SERP_COVERAGE remains separate.

## 9. Release verdict

```text
S06Q001_EXECUTION_RELEASE = PASS
S06Q001_LOCAL_START_ALLOWED = true
S06Q001_PROVIDER_SUBMISSION_ALLOWED = exactly 1
S06Q002_RELEASED = false
PROVIDER_CALLS_ALREADY_EXECUTED_BY_THIS_RELEASE = 0
```
