# KW-001 / OKNO-MSK — Step 09 collection method and immediate-persistence postmortem

Date: 2026-08-29  
Status: **ACTIVE STEP-09 PROCESS AUTHORITY / NON-REPEAT CONTROL**

## What Step 09 collected

Step 09 uses **ordinary Yandex Search**, not GenSearch, to obtain bounded real SERP evidence for intent/result-type/page-boundary questions before clustering and page ownership.

Frozen Search request profile:

```text
service = search
protocol = SEARCH_BATCH_API_V1
provider operation = ordinary Search
searchType = SEARCH_TYPE_RU
region = 213 / Moscow
page = 0
groupsOnPage = 10
docsInGroup = 1
groupMode = GROUP_MODE_FLAT
sortMode = SORT_MODE_BY_RELEVANCE
sortOrder = SORT_ORDER_DESC
familyMode = FAMILY_MODE_MODERATE
fixTypoMode = FIX_TYPO_MODE_ON
response format = FORMAT_XML at provider boundary
normalized evidence used by projection = TOP-10 rank/url/domain/title
```

The 75 frozen probes are a bounded diagnostic tranche. They are not permission to transfer one probe's result to unprobed rows merely because wording, cleanup reason, acquisition source or lexical shape is similar.

## How the acquisition was executed

### Initial canary

The original job executed one real paid Search request through the legacy one-item action:

```text
query #1 = аксессуары для пластиковых окон
provider requests = 1
succeeded = 1
estimated cost = 0.488 RUB
```

The canary result was persisted in `STEP_09_SERP_RESULTS.tsv` with its full available normalized/provider fields.

### Bridge patch introduced during Step 09

The one-item Manual round-trip was operationally inefficient, so Yandex Marketing Bridge received a bounded Manual-only action:

```text
SEARCH_BATCH_API_V1
{"action":"nextN","jobId":"...","count":N}
```

Protocol ceiling:

```text
1 <= N <= 100
```

`nextN` does not create a new provider path. It repeatedly invokes the existing safe `next()` path sequentially; each previous item is persisted before the next provider boundary.

The Bridge change is documented in:

```text
extension/docs/SEARCH_BATCH_NEXTN100_V0_1_2_CHANGELOG_AND_ACCEPTANCE_2026-08-29.md
```

### What quantity was actually tested

Two different facts must not be conflated.

#### Local bounded-command test

```text
count = 100
```

was tested at protocol/runtime level. The test intentionally supplied only three remaining items and proved that `nextN count=100` executes exactly three provider boundaries and then stops at completion. This validates the hard ceiling and bounded behavior.

It does **not** mean that 100 real Yandex requests were sent in one live chunk.

#### Live provider test / Step-09 R2

The patched Bridge was used for the real R2 acquisition:

```text
job_id = kw001-okno-msk-search-step09-20260829-r2
total real provider requests = 74
requests_started = 74
succeeded = 74
failed_terminal = 0
outcome_unknown = 0
estimated cost = 36.112 RUB
job status = COMPLETED
```

Combined with the one-request canary:

```text
real Search probes = 75
successful = 75
terminal failures = 0
unknown outcomes = 0
estimated cumulative cost = 36.600 RUB
```

The final `projection(offset=0,limit=74,topN=10)` proved the complete R2 job and returned 740 normalized ranked results.

Important limitation:

```text
R2 74/74 SUCCESS != EVIDENCE OF THE EXACT SIZE OF EACH INDIVIDUAL nextN COMMAND
```

The final projection does not contain the command-history of chunk sizes. Exact live per-command `count` values must not be reconstructed from memory or invented.

## Critical process error: provider results were not durably written immediately

### What I did wrong

During the live R2 acquisition I allowed successful provider work to continue while relying on:

1. Search Batch's internal `chrome.storage.local` job state; and
2. returned chat/Bridge result delivery;

instead of immediately copying every completed result/chunk into the project's durable repository evidence ledger before permitting the next paid chunk.

That was a workflow error.

Canonical statement:

```text
BRIDGE_INTERNAL_DURABILITY != PROJECT_EVIDENCE_DURABILITY
CHAT_DELIVERY != PROJECT_EVIDENCE_DURABILITY
JOB_COMPLETION != REPOSITORY_EVIDENCE_PERSISTENCE
```

### Why the error was plausible

The Bridge itself correctly persisted each Search item and its `result_payload` before moving to the next item. Because the job could later be queried with `status` / `projection`, I treated that runtime persistence as if it were sufficient evidence persistence for the Kwork.

That assumption was false because browser-extension storage and project evidence have different failure domains.

The missing process gate was:

```text
SUCCESSFUL_PROVIDER_RESULT
must block further paid work
until project-level durable write is confirmed.
```

### Why this was dangerous

Any of the following can invalidate runtime-only evidence independently of the provider execution:

- extension identity/path change;
- extension uninstall/reload/storage reset;
- browser/profile loss;
- job lifecycle cleanup;
- runtime replacement;
- tab/conversation delivery failure;
- connection/session interruption before evidence is copied out;
- accidental cleanup of local state.

The original canary job later became `SEARCH_BATCH_JOB_NOT_FOUND` in the current runtime. The R2 job remained available long enough to recover normalized data through a final projection, but that was recovery luck plus Bridge durability, not a sound project workflow.

If the R2 runtime state had also disappeared before projection, the already-paid evidence might have required reacquisition.

That is unacceptable.

### Actual evidence loss boundary in this incident

Recovery through `projection` allowed us to persist:

```text
74 R2 queries
740 normalized TOP-10 rows
query_text
item_id
region
rank
url
domain
title
```

Together with the canary:

```text
75 queries
750 normalized ranked rows
```

However the projection did not expose all original raw per-item fields, including complete per-item provider request IDs/raw XML and fields such as snippet/modtime for the R2 set.

Therefore the delayed persistence did not force paid replay this time, but it reduced the recoverable evidence fidelity.

## Mandatory corrected workflow

From this point forward, every paid or otherwise non-trivial provider acquisition in this Kwork follows this gate:

```text
1. EXECUTE bounded provider command/chunk.
2. RECEIVE complete Bridge result.
3. PARSE and validate result/accounting.
4. IMMEDIATELY WRITE the result to the project repository evidence ledger.
5. READ BACK the written file/rows from GitHub.
6. VERIFY:
   - expected query/item count;
   - expected ranks/result count;
   - request_executed / provider execution accounting;
   - failed_terminal / outcome_unknown;
   - cost/progress;
   - no missing or duplicated item identities.
7. UPDATE the persistent coverage/accounting checkpoint.
8. ONLY AFTER PASS may another paid chunk be issued.
```

For `nextN`, the atomic project workflow unit is the **returned chunk**:

```text
NEXT_N_RESULT_RECEIVED
-> DURABLE_WRITE_ALL_CHUNK_ITEMS
-> READ_BACK_QA
-> COVERAGE_CHECKPOINT
-> NEXT_PAID_CHUNK_ALLOWED
```

If durable write or read-back QA fails:

```text
NEXT_PAID_CHUNK_ALLOWED = false
```

No throughput or convenience exception is allowed.

## Additional recovery checkpoint

At bounded milestones and at job completion, execute non-provider controls as appropriate:

```text
status
projection
```

and persist their accounting/projection receipts as secondary recovery evidence.

These controls do not replace immediate per-result/chunk persistence; they are an additional reconciliation layer.

## Non-repeat controls

```text
PROVIDER_SUCCESS_WITHOUT_PROJECT_WRITE = PROCESS_FAILURE
NEXT_PAID_CHUNK_BEFORE_READBACK_QA = PROHIBITED
RUNTIME_STORAGE_AS_ONLY_EVIDENCE_COPY = PROHIBITED
CHAT_AS_ONLY_EVIDENCE_COPY = PROHIBITED
JOB_COMPLETED_WITHOUT_REPOSITORY_LEDGER = NOT_ACCEPTED
```

The purpose is simple: once money/time has been spent obtaining evidence, an unrelated connection, browser, extension or chat failure must not force the project to pay for the same evidence again.

## Current incident outcome

After the recovery projection, normalized persistence is now complete:

```text
canary = 10 ranked rows
R2 = 740 ranked rows
combined = 750 ranked rows
normalized query coverage = 1..75
```

Authority:

- `STEP_09_SERP_RESULTS.tsv`
- `STEP_09_SERP_R2_PROJECTION_RAW_PART_01.tsv`
- `STEP_09_SERP_R2_PROJECTION_RAW_PART_02.tsv`
- `STEP_09_SERP_R2_PROJECTION_RAW_PART_03.tsv`
- `STEP_09_SERP_R2_PROJECTION_RAW_PART_04.tsv`
- `STEP_09_SERP_R2_PROJECTION_INDEX.md`

Step 09 remains analytically incomplete until its remaining evidence decisions, duplicate overlap analysis, coverage accounting and acceptance QA are finished. This postmortem does not authorize Step 10.
