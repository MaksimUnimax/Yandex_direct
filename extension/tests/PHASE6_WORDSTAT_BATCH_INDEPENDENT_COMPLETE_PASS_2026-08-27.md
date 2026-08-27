# Phase 6 Wordstat batch — independent complete gate PASS

Date: 2026-08-27

Status: **INDEPENDENT PRE-DELIVERY PASS / P6-11 OWNER-LIVE AUTHORIZED / PHASE 6 NOT CLOSED**

## Immutable candidate authority

```text
source_commit = 34f50688268970f4863dddb2089a33d891b91372
extension/src_tree = adab628a8ec328fa5079ae35f45005a0ee7de2c1
candidate_branch = candidate/phase6-wordstat-batch-first-slice-2026-08-27
freeze_trigger_commit = a837baac899d0e945a015f7a1980c6a13d874f88
freeze_run = 33078753960
artifact_id = 9649039904
artifact_name = phase6-wordstat-batch-frozen-candidate-34f5068
artifact_wrapper_sha256 = bcc33634c1673170c71e979f9e1412c944d372ebd7e351b5a3b31c973762f478
inner_zip = yandex-marketing-bridge-0.1.1-phase6-wordstat-batch-first-slice-candidate.zip
inner_zip_sha256 = 05d587b02f5fc08c64ebbf1fbd5d14765491c7b9931195c23262e1f42d692c2f
inner_zip_bytes = 133127
product_files = 47
```

## Independent campaign

```text
qa_branch = qa/phase6-wordstat-batch-independent-gate-2026-08-27
runner_commit = 0809e2ddef4b8ebe4a6a310d292a0ae330f045e2
workflow_commit = 597f0504ae6b324ffbf5ae264aa67fd330ce5bb4
workflow_run = 33079158530
job = independent-complete-gate
verdict = PASS
```

The campaign independently downloaded the exact GitHub artifact wrapper, verified its wrapper digest, verified the inner ZIP identity and manifest, proved exact source/artifact byte identity, executed the source and packaged suites, and re-ran permanent browser regressions against the frozen product bytes.

## Source / package verification

```text
SOURCE_SUITE = 81/81
PACKAGED_SUITE = 81/81
SOURCE_PHASE6_FOCUSED = 47/47
PACKAGED_PHASE6_FOCUSED = 47/47
SOURCE_SYNTAX = 41/41
PACKAGED_SYNTAX = 41/41
SOURCE_JSON = 2/2
PACKAGED_JSON = 2/2
PHASE6_ARTIFACT_TRANSPORT_ROUNDTRIP_PASS
PHASE6_SOURCE_ARTIFACT_BYTE_IDENTITY_PASS
```

Focused Phase 6 execution covers durable item identity/state, exact duplicate discipline, persistence, successful-payload durability before delivery, authoritative request metadata, policy admission, Manual/Autorun routing, owner/conversation fencing, double-submit, stale event suppression, worker restart/tab-close recovery, unknown-outcome reconciliation/no replay, request limit and cost limit.

## Permanent compatibility browser verification

```text
BROWSER_DIRECT_POPUP_D18 = PASS
BROWSER_DIRECT_MANUAL_LIFECYCLE = PASS
BROWSER_DIRECT_ADDENDUM = PASS
BROWSER_PRIOR_PHASE_COMPATIBILITY = PASS
DIRECT_REAL_YANDEX_REQUESTS = 0
BROWSER_GATE_REAL_YANDEX_REQUESTS = 0
```

## Final cleanliness and safety

```text
real_credentials_used = NO
real_yandex_requests = 0
enabled_not_run_sections = 0
NOT_RUN_COUNT = 0
PRODUCT_BYTES_POST_TEST = IDENTICAL
PHASE6_WORDSTAT_BATCH_INDEPENDENT_RUNNER_PASS
```

No production product byte was modified by the independent campaign.

## Authorized next stage — P6-11 narrow owner-live

Owner-live is now authorized only against the exact frozen candidate above.

The minimum acceptance should use a deliberately small real Wordstat batch and prove:

1. one `start` creates a durable job without provider traffic;
2. three distinct seeds are used so several items can be observed;
3. `next` is invoked explicitly once per intended paid item; no hidden advance loop;
4. each successful seed executes exactly once and returns provider evidence;
5. `status` does not contact the provider;
6. after at least one successful item, `pause` then `resume` does not replay it;
7. the remaining item(s) continue from pending state rather than restarting the job;
8. final progress totals match the actual item outcomes and request count;
9. no unrelated Yandex service is contacted;
10. no automatic retry is attempted if any real provider call has an unknown outcome — stop immediately and reconcile instead.

Recommended first live manifest:

```text
WORDSTAT_BATCH_API_V1 {"action":"start","jobId":"p6-owner-live-20260827-01","phrases":["купить кондиционер","установка кондиционера","обслуживание кондиционера"],"numPhrases":20,"regions":["225"],"devices":["DEVICE_ALL"],"maxRequests":3}
```

Then use only explicit commands, one at a time, reading the returned `job_id` and progress after every result:

```text
WORDSTAT_BATCH_API_V1 {"action":"next","jobId":"p6-owner-live-20260827-01"}
WORDSTAT_BATCH_API_V1 {"action":"status","jobId":"p6-owner-live-20260827-01"}
WORDSTAT_BATCH_API_V1 {"action":"pause","jobId":"p6-owner-live-20260827-01"}
WORDSTAT_BATCH_API_V1 {"action":"resume","jobId":"p6-owner-live-20260827-01"}
WORDSTAT_BATCH_API_V1 {"action":"next","jobId":"p6-owner-live-20260827-01"}
WORDSTAT_BATCH_API_V1 {"action":"next","jobId":"p6-owner-live-20260827-01"}
WORDSTAT_BATCH_API_V1 {"action":"status","jobId":"p6-owner-live-20260827-01"}
```

Do not issue another `next` after `OUTCOME_UNKNOWN`; reconciliation is mandatory. Do not test artificial quota failures, credential failures, concurrency failures, or repeated unknown-result traffic in owner-live.

## Closure boundary

P6-12 merge/close remains blocked until the narrow owner-live result is recorded. Any product-byte change invalidates this candidate and requires a new freeze and independent complete gate.