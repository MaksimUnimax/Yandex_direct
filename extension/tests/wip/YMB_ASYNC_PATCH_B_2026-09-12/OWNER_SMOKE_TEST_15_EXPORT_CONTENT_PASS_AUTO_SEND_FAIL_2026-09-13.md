# OWNER SMOKE TEST-15 — EXPORT CONTENT PASS / AUTO-SEND DEFECT

Date: 2026-09-13
Product under test: Yandex Marketing Bridge 0.1.6 final owner candidate
Branch: `wip/ymb-file-delivery-patch-a-2026-09-12`
Job: `owner-smoke-016-01`

## Command

`SEARCH_ASYNC_BATCH_API_V1 {"action":"exportPage","jobId":"owner-smoke-016-01","after":-1,"limit":25}`

## Bridge response

- action: `exportPage`
- ok: `true`
- request_executed: `false`
- provider_calls: `0`
- schema: `YMB_SEARCH_ASYNC_EXPORT_PAGE_V1`
- filename: `search-owner-smoke-016-01-r7-0-0.json`
- declared bytes: `38964`
- revision: `7`
- item_count: `1`
- result_row_count: `10`
- items_with_raw: `1`
- items_with_normalized: `1`
- states: `SUCCEEDED=1`
- next_after: `0`
- has_more: `false`
- all_job_items_in_this_file: `true`

## Owner-delivered artifact verification

The actual JSON artifact was delivered back by the owner and independently parsed.

- observed byte length: `38964` — matches bridge descriptor
- whole-file SHA-256: `d4aca77bab50a269f3e977fe72d03a48164b0dc02baa124923718f57903add9f`
- JSON parses successfully
- schema/job/revision match the bridge response
- job summary: `SUCCEEDED=1`, `FAILED=0`, `UNKNOWN=0`, `unresolved=0`, `all_successful=true`
- durable operation id: `sprnnhjulgb8ofo593bc`
- raw provider response is present
- raw `response.rawData` base64 decodes as UTF-8 XML
- decoded request query is `тестовый запрос bridge 0.1.6`
- decoded XML contains 10 result documents
- normalized payload contains 10 result rows
- normalized validation reports `document_count=10`, `usable_for_url_comparison=true`, no missing/unsafe URL ranks

## Delivery observation

The file was attached into the ChatGPT composer, but this TEST-15 delivery did not press Send automatically. The owner had to press Send manually. Earlier owner-smoke responses in the same installed 0.1.6 session were sent automatically.

Therefore this is not classified as an export-data failure. It is a file-delivery auto-send failure at the post-attachment send boundary.

## Verdict

- export generation: PASS
- staged artifact content: PASS
- artifact byte count: PASS
- raw preservation: PASS
- normalization preservation: PASS
- zero provider-call export: PASS
- attachment creation: PASS
- automatic Send: FAIL_PRODUCT
- overall TEST-15: FAIL_PRODUCT

Release qualification remains blocked on the file-delivery auto-send defect until patched/requalified. No production source was changed by this evidence commit.
