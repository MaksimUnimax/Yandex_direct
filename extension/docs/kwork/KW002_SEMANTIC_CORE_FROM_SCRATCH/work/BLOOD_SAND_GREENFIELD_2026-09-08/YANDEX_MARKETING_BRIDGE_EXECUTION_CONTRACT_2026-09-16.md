# KW-002 Blood & Sand — Yandex Marketing Bridge execution contract

Date: 2026-09-16
Status: **ACTIVE / CURRENT JOB EXECUTION CONTRACT**

Universal authority:

`../../../LEVEL1/YANDEX_MARKETING_BRIDGE_EXECUTION_RULE.md`

This job-specific contract pins the currently accepted Yandex Marketing Bridge production build and the command/result forms used by the active KW-002 rehearsal. It supplements but does not weaken the Level-1 rule.

## 1. Accepted current YMB production authority

```text
repository = MaksimUnimax/Yandex_direct
production_branch = hotfix/ymb-file-delivery-p0-2026-09-14
production_commit = b218afb0187bd26af1d7ada3590b02edc2d4a2de
product_version = 0.1.9
```

Relevant verified production identities:

```text
proven_writing_block_capture.js = 87782b405013f93eaa069a4ae4a5deb383e75f81
search_protocol.js = 49ca9a6f3a2786a3107f03d0724dfca7578cd096
search_async_protocol.js = 91df9051f4cf52d51ee73af9c66a196411a966d7
search_async_store.js = 1de12e529141649eb4a0f94cac155ab32f38b0dd
search_async_runtime.js = 571debe536e634aad1ed280f215c4e35b19925ae
search_async_policy.js = e18de13b36a617fc8fa78203459d8947869687f9
search_async_worker_transport.js = 75c5349531d7fb77641991d648cfb8b40a490bdc
manifest.json = dd89fb6ab3577f53b35b40f9723741e0f32e0a24
```

## 2. Real ChatGPT command surface

The installed 0.1.9 content layer discovers assistant code blocks through the accepted proven-writing capture path. Therefore executable Manual commands for this job must be emitted as a standalone fenced Markdown code block.

Required form:

```text
<PROTOCOL_PREFIX>
<JSON OBJECT>
```

The block must contain exactly one Bridge command and no explanation.

The assistant may write explanation before/after the block, but that text is not part of the command.

The Bridge then renders its `Яндекс` button/action for an eligible assistant code block. Only the owner/user clicking that action sends the block to the worker via `WS_EXECUTE_MANUAL_BLOCK`.

Therefore:

```text
assistant emitted command = NOT EXECUTED
code block visible = NOT EXECUTED
Яндекс button visible = NOT EXECUTED
Яндекс button clicked = execution attempt only
actual Bridge result delivered = observed execution outcome
```

## 3. Current protocol/result map

Verified against YMB 0.1.9 production source:

| Use | Command prefix | Actual result prefix | Notes |
|---|---|---|---|
| Wordstat single | `WORDSTAT_API_V1` | `WORDSTAT_RESULT_V1` | ordinary Manual Wordstat command |
| Wordstat batch | `WORDSTAT_BATCH_API_V1` | `WORDSTAT_BATCH_RESULT_V1` | batch orchestration; each provider request still accounted by runtime |
| ordinary Search | `SEARCH_API_V1` | `SEARCH_RESULT_V1` | `method:"search"` |
| GenSearch / AI-search | `SEARCH_API_V1` | `SEARCH_RESULT_V1` | `method:"genSearch"`; explicit billable confirmation required by protocol |
| deferred Search | `SEARCH_ASYNC_BATCH_API_V1` | `SEARCH_ASYNC_BATCH_RESULT_V1` | Manual-only durable async lifecycle |

If the installed/accepted YMB version changes, this table must be re-verified before the next provider command.

## 4. Manual preflight for this job

For the current deferred Search path, execution authority requires the live ChatGPT dialogue/tab and YMB state to satisfy the production preflight, including:

```text
dialogue is bound
Manual mode enabled
active service = Search
current Search credential exists
current Search folder matches durable job owner scope
no conflicting non-terminal Manual operation
no blocking delivery/outbox state
Autorun constraints respected
```

Do not bypass these controls through DevTools/console/IndexedDB/service-worker editing.

## 5. Deferred Search lifecycle/accounting

Current protocol actions are distinct:

```text
start
submit / submitN
collect / collectN / collectReady
status
itemsPage
pause / resume / cancelPending
normalizeSaved
exportPage
```

For accepted 0.1.9:

```text
start = durable local job creation, request_executed=false, provider_calls=0
submit/submitN = provider submit path when permitted
collect/collectN = explicit provider Operation GET path
status/itemsPage/local controls = local state operations
exportPage = local staged export/file-delivery path
```

The production manifest includes provider host permission for both deferred submit and deferred operation collection.

There is no deferred Autorun, no hidden `chrome.alarms` polling, no hidden retry and no automatic replay after an uncertain paid submit.

Interrupted ambiguous submit recovery is conservative and must not be blindly repeated.

## 6. Exact command-block rule for Step06 remaining queue

Current released preparation target:

```text
job_id = kw002-s06q003-q022-20260916
query_ids = S06Q003..S06Q022
query_count = 20
```

When the local `start` is actually presented for execution, it must be one standalone fenced code block with exactly one `SEARCH_ASYNC_BATCH_API_V1` command.

The command being printed in chat does not prove the local job exists.

Required proof of successful local creation:

```text
actual prefix = SEARCH_ASYNC_BATCH_RESULT_V1
action = start
job_id = kw002-s06q003-q022-20260916
request_executed = false
provider_calls = 0
progress.total = 20
progress.counts.PENDING = 20
```

Only the actual returned result controls the observed values. Do not invent missing fields or expected state.

## 7. Current correction to execution history

During the 2026-09-16 Step06 continuation, the assistant rendered the local-start command in ordinary response text/code but incorrectly stated that it had been "started" / "released" / "executed" without receiving an actual `SEARCH_ASYNC_BATCH_RESULT_V1`.

Correct state:

```text
V55_LOCAL_START_AUTHORIZED = true
LOCAL_START_COMMAND_PREPARED = true
ACTUAL_LOCAL_START_RESULT_OBSERVED = false
DURABLE_20_ITEM_JOB_CREATION_VERIFIED = false
PROVIDER_CALLS_AFTER_V55 = 0 proven increase
SUBMITN_RELEASED = false
COLLECTN_RELEASED = false
STEP07_STARTED = false
```

The false execution claim is superseded by this durable correction. No provider request is inferred from the rendered command.

## 8. Mandatory next-action discipline

For every future Bridge action in this job:

```text
prepare exact command
→ emit ONE standalone fenced code block
→ do not claim it ran
→ owner/user clicks `Яндекс`
→ wait for actual *_RESULT_V1
→ reconcile exact result fields
→ persist/update cursor as required
→ only then release next action
```

If the actual result does not arrive, execution remains unverified and the cursor does not advance.

## Marker

```text
KW002_JOB_YMB_VERSION = 0.1.9
KW002_JOB_YMB_PRODUCTION_COMMIT = b218afb0187bd26af1d7ada3590b02edc2d4a2de
KW002_JOB_YMB_COMMAND_SURFACE = STANDALONE_MARKDOWN_FENCED_CODE_BLOCK
KW002_JOB_YMB_ONE_COMMAND_PER_BLOCK = true
KW002_JOB_YMB_EXECUTION_TRIGGER = USER_CLICKS_YANDEX_ACTION
KW002_JOB_YMB_RESULT_REQUIRED = true
KW002_JOB_S06_REMAINING_START_OBSERVED = false
KW002_JOB_PROVIDER_CALLS_DURING_THIS_DOCUMENTATION_PATCH = 0
```
