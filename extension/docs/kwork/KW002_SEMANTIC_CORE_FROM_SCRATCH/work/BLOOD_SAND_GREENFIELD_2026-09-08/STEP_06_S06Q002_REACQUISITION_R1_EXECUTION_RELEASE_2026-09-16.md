# KW-002 Step06 — S06Q002 CONTROLLED REACQUISITION R1 EXECUTION RELEASE

Date: 2026-09-16
Status: **PUBLISHED FOR ONE BOUNDED REACQUISITION / ACTIVATION REQUIRES REMOTE READBACK / NO NEXT QUERY RELEASED**

## 1. Scope

This authority covers only a fresh controlled reacquisition of the second current V2 representative-query row for Step06 competitor discovery.

```text
QUERY_ID = S06Q002
COVERAGE_DIRECTION = GENERIC_PRODUCT
SOURCE_FAMILY_ID = PSF001
QUERY_TEXT = оберег
SOURCE_STATUS = OBSERVED_REPRESENTATIVE_PHRASE
QUERY_ROLE = HEAD_TERM_DISCOVERY
BUSINESS_ALIGNMENT = CLIENT_PRODUCT_CLASS
COUNTING_ROLE = COUNT_SERP_DOMAIN_EVIDENCE
ATTEMPT = CONTROLLED_REACQUISITION_R1
```

Source row remains `STEP_06_REPRESENTATIVE_QUERY_MANIFEST_V2_2026-09-12.tsv`.

No other Step06 query is released by this file.

## 2. Why reacquisition is required

The historical S06Q002 provider operation `sprridu5n6oqitgg774b` completed successfully under job `kw002-s06q002-20260915`, and its collect evidence was persisted and remote-read back. However, the old YMB 0.1.6 durable-job ownership model bound the job to a single ChatGPT `conversation_key`. That design prevented reliable continuation/export after project handoff and therefore prevented exact exported evidence closure.

The owner explicitly chose not to preserve or migrate that old job. Historical evidence remains in the repository and MUST NOT be rewritten or deleted, but it is superseded as the current evidence candidate by this fresh acquisition.

The infrastructure defect was corrected in Yandex Marketing Bridge 0.1.8: durable deferred Search ownership is now credential-scoped (`search-folder:<folder_id>`) rather than conversation-scoped, while live conversation authority remains required for execution.

```text
YMB_VERSION = 0.1.8
YMB_PRODUCTION_HOTFIX_COMMIT = 1af6d07828b352ac7a520896d8cc41e9f24a17b0
DURABLE_JOB_OWNER_MODEL = SEARCH_FOLDER_SCOPE
OLD_CONVERSATION_OWNED_JOB_MIGRATION = NOT_REQUIRED
```

## 3. Exact Search method contract

The Search settings are unchanged from the original S06Q002 release:

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

The accepted `SearchProtocol` supplies `LOCALIZATION_RU` and `maxPassages=4` as normal defaults when omitted. No analytical search-setting change is introduced by the reacquisition.

## 4. Exact Bridge command contract

Fresh job identity:

```text
JOB_ID = kw002-s06q002-r1-20260916
```

After this release and its canonical cursor have been remote-read back and activation has been recorded, exactly one local start may be executed:

```text
SEARCH_ASYNC_BATCH_API_V1 {"action":"start","jobId":"kw002-s06q002-r1-20260916","queries":["оберег"],"confirmBillable":true,"maxRequests":1,"maxCostRub":0.0305,"searchType":"SEARCH_TYPE_RU","region":"225","page":0,"groupsOnPage":20,"docsInGroup":1,"groupMode":"GROUP_MODE_FLAT","familyMode":"FAMILY_MODE_MODERATE","fixTypoMode":"FIX_TYPO_MODE_OFF","sortMode":"SORT_MODE_BY_RELEVANCE","sortOrder":"SORT_ORDER_DESC"}
```

`start` is local-only and must execute zero provider calls.

Only after a successful local start is persisted and remote-read back may exactly one deferred provider submission be separately released:

```text
SEARCH_ASYNC_BATCH_API_V1 {"action":"submitN","jobId":"kw002-s06q002-r1-20260916","count":1}
```

`maxRequests=1` and `maxCostRub=0.0305` cap this reacquisition to a single provider Search request.

## 5. Publication-time provider boundary

At publication time this file does not itself activate execution.

```text
LOCAL_START_CALLS_ALLOWED_BEFORE_RELEASE_READBACK = 0
DEFERRED_SEARCH_SUBMISSIONS_ALLOWED_BEFORE_RELEASE_READBACK = 0
DEFERRED_SEARCH_COLLECTION_CALLS_ALLOWED = 0
SYNCHRONOUS_SEARCH_CALLS_ALLOWED = 0
WORDSTAT_CALLS_ALLOWED = 0
GENSEARCH_CALLS_ALLOWED = 0
AI_SEARCH_CALLS_ALLOWED = 0
S06Q003_RELEASED = false
STEP07_STARTED = false
STEP08_STARTED = false
PROVIDER_CALLS_ALREADY_EXECUTED_BY_THIS_RELEASE = 0
```

## 6. Evidence and durability gate

For this new job:

1. preserve exact local-start result before any provider release;
2. remote-readback the persisted local-start evidence;
3. release at most one `submitN count=1`;
4. preserve exact returned provider operation identity before any collect;
5. if submit returns `WAITING`, do not resubmit;
6. collect only when due and only from the persisted pending operation;
7. preserve complete raw provider result and complete normalized result;
8. export the exact complete evidence through the 0.1.8 credential-scoped job model;
9. persist exact export and closure to GitHub;
10. remote-readback persisted evidence before any S06Q003 release.

No summary-only evidence, sampling, silent truncation, automatic retry, synchronous fallback, GenSearch fallback, or replacement resubmit is allowed.

## 7. Outcome contract

- `SUCCESS_WITH_RESULTS` → persist full evidence, close, remote-readback, then separately decide S06Q003.
- `SUCCESS_WITH_ZERO_RESULTS` → bounded zero for this exact query/settings/snapshot only; persist and remote-readback.
- `WAITING` → persist exact pending operation; no additional submission.
- `SUCCESS_BUT_EVIDENCE_INCOMPLETE` → unresolved; stop.
- validation/provider/unknown/normalization failure → preserve failure truth; no competitor inference; no blind retry.

## 8. Interpretation boundary

This is one bounded current-Yandex competitor-discovery probe. It is not a final keyword, final intent, final SERP cluster, final page target, final competitor registry, site architecture, or Step12 full-SERP claim.

## 9. Publication verdict

```text
S06Q002_R1_RELEASE_PUBLICATION = PASS
S06Q002_R1_RELEASE_REMOTE_READBACK_REQUIRED = true
S06Q002_R1_LOCAL_START_ALLOWED_BEFORE_READBACK = false
S06Q002_R1_PROVIDER_SUBMISSION_ALLOWED_BEFORE_READBACK = false
S06Q003_RELEASED = false
PROVIDER_CALLS_ALREADY_EXECUTED_BY_THIS_RELEASE = 0
```
