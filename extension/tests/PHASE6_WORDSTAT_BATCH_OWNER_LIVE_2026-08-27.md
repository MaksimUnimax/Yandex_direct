# Phase 6 Wordstat batch — owner-live evidence

Date: 2026-08-27

Status: **P6-11 OWNER-LIVE IN PROGRESS / PHASE 6 NOT CLOSED**

## Immutable candidate authority

```text
source_commit = 34f50688268970f4863dddb2089a33d891b91372
extension/src_tree = adab628a8ec328fa5079ae35f45005a0ee7de2c1
artifact_id = 9649039904
inner_zip_sha256 = 05d587b02f5fc08c64ebbf1fbd5d14765491c7b9931195c23262e1f42d692c2f
```

## OL-01 — batch.start

Observed owner-live result:

```text
bridge = yandex-marketing-bridge
version = 0.1.1
service = wordstat
operation = batch.start
job_id = p6-owner-live-20260827-01
status = OK
phrases = 3
input_count = 3
duplicate_count = 0
pending = 3
claimed = 0
requesting = 0
succeeded = 0
failed_terminal = 0
outcome_unknown = 0
requests_started = 0
active_item_id = null
next_safe_action = CLAIM_NEXT
max_requests = 3
request_executed = false
automatic_retry = false
```

Verdict: **OL-01 PASS**. `start` created the durable three-item job without crossing the paid Wordstat provider boundary. No automatic retry occurred.

Next authorized owner-live action: exactly one `batch.next` for this job. If the result reports `OUTCOME_UNKNOWN`, stop immediately and reconcile; do not issue another `next`.
