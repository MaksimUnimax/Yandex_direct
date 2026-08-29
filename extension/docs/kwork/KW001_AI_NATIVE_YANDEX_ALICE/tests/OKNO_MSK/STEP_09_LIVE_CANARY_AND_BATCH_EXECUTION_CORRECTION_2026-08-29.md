# KW-001 / OKNO-MSK — Step 09 live canary and batch-execution correction

Date: 2026-08-29  
Status: **ACTIVE LIVE EXECUTION EVIDENCE / OPERATIONAL CORRECTION**

This document records the first real ordinary-Yandex-Search execution of Step 09, the live Manual-layer failure observed immediately before it, and the resulting correction to the operational execution model.

## 1. Why this document exists

The corrected Step-09 method intentionally separated semantic evidence quality from transport/accounting QA. The first live execution then exposed a different class of error: the project documentation reasoned from the generic Manual multi-command contract and the Search batch runtime, but did not verify the stricter Search-batch Manual admission rule actually enforced by the installed extension.

That mistake matters because an operational plan can be logically safe at the runtime level yet still be impossible at the actual Manual command boundary.

Canonical lesson:

```text
GENERIC MULTI-COMMAND SUPPORT
!=
SEARCH_BATCH MANUAL ADMISSION SUPPORT
```

The real installed validator is the authority for what one Manual block can admit.

## 2. Failed live attempt before provider execution

The first attempted Manual block contained two `SEARCH_BATCH_API_V1` commands:

```text
start
next
```

The installed bridge rejected the block before any provider request:

```text
status = ERROR
stage = COMMAND_VALIDATION
code = BATCH_SINGLE_COMMAND_REQUIRED
message = Один Manual block должен содержать ровно одну SEARCH_BATCH_API_V1 команду.
request_executed = false
automatic_retry = false
```

Therefore:

```text
provider requests caused by failed block = 0
provider cost caused by failed block = 0 RUB
```

### False assumption

The mistaken reasoning was:

> The generic Manual contract supports multiple registered commands in one block, therefore multiple Search-batch commands can be placed in one Manual block.

This was wrong because Search batch has an additional service-specific admission constraint. The generic contract describes worker multi-command behavior in general, but does not override a stricter validator for a registered protocol.

### Correct consequence

Before designing any batch interaction shape, inspect all three layers:

```text
1. generic Manual block contract;
2. service protocol actions;
3. service-specific Manual admission/validation behavior.
```

A plan is executable only if all three permit it.

## 3. Successful bounded job start

A second Manual action contained exactly one `SEARCH_BATCH_API_V1 start` command for:

```text
job_id = kw001-okno-msk-search-step09-20260829
queries = 75
searchType = SEARCH_TYPE_RU
region = 213
groupsOnPage = 10
maxRequests = 75
maxCostRub = 39.04
confirmBillable = true
```

Observed result:

```text
operation = batch.start
status = OK
job status = RUNNING
total = 75
pending = 75
succeeded = 0
requests_started = 0
estimated_cost_rub = 0
request_executed = false
automatic_retry = false
next_safe_action = CLAIM_NEXT
```

This satisfies the start gate: the bounded queue exists and creating it caused zero provider requests.

## 4. First paid canary

The next Manual action contained exactly one command:

```text
SEARCH_BATCH_API_V1
{"action":"next","jobId":"kw001-okno-msk-search-step09-20260829"}
```

It executed the first frozen query:

```text
аксессуары для пластиковых окон
```

Observed provider/result truth:

```text
operation = batch.next
status = OK
item status = SUCCEEDED
request_executed = true
automatic_retry = false
http_status = 200
region = 213
response_format = FORMAT_XML
result_count = 10
requests_started = 1
succeeded = 1
pending = 74
outcome_unknown = 0
estimated_cost_rub = 0.488
next_safe_action = CLAIM_NEXT
```

Identifiers preserved:

```text
request_id = search-batch-06923ff5-1455-4ca9-99f3-d8778976c96a
item_id = kw001-okno-msk-search-step09-20260829:ca2ccadf3fb1cddc
fingerprint = ca2ccadf3fb1cddc
```

The complete observed TOP-10 was persisted to:

`STEP_09_SERP_RESULTS.tsv`

## 5. First observed SERP interpretation

Query:

```text
аксессуары для пластиковых окон
```

Observed TOP-10 composition:

```text
rank 1 = OZON category for window fittings/accessories
ranks 2-6 = individual REHAU window-handle products
rank 7 = REHAU window-handle catalog
ranks 8-10 = specific REHAU accessory/component products
```

The SERP therefore shows a strong product/category transactional-shopping pattern around window fittings/accessories/components.

This is direct evidence for this exact query only. It does **not** automatically transfer to the other non-probed accessory/fittings phrases.

Current exact-query evidence statement:

```text
query = аксессуары для пластиковых окон
observed dominant result pattern = product/category commerce for accessories/fittings
ordinary general window-installation service intent = not dominant in observed TOP-10
transfer to other phrases = not yet authorized
```

No Step-10 cluster or Step-11 page-ownership decision is made here.

## 6. Completeness-gate result for canary #1

The first paid canary passes the Step-09 project completeness gate because:

```text
1. governed item outcome is known = yes;
2. request_executed truth is known = true;
3. request_id/item_id/job_id preserved = yes;
4. complete provider result payload present = yes;
5. normalized ranked rows readable = yes, 10;
6. observed_result_count reconciles = 10 / 10;
7. query/region/request parameters preserved = yes;
8. accounting updated = 1 request / 0.488 RUB;
9. OUTCOME_UNKNOWN absent = yes;
10. reusable evidence persisted in STEP_09_SERP_RESULTS.tsv = yes.
```

Therefore the Search transport/result path itself is live-validated for continuing Step 09.

## 7. New operational gap: no bounded chunk action

The current Search batch protocol supports:

```text
start
next
status
pause
resume
cancel
projection
overlapPage
```

It does not expose a bounded action such as:

```text
nextN
runChunk
advance(count=N)
```

At the same time, the installed Manual validator requires exactly one `SEARCH_BATCH_API_V1` command per Manual block.

Together these facts imply:

```text
current protocol + current Manual admission
=> one Manual click per paid `next`
```

For a 75-query tranche this would require up to 75 paid Manual interactions. That is safe but operationally poor and creates unnecessary human repetition.

## 8. Why simply restoring multi-command blocks is not the right correction

The defect should not be fixed by merely weakening `BATCH_SINGLE_COMMAND_REQUIRED` and stuffing many `next` commands into one block.

Reason:

- the service-specific one-command boundary is explicit and may protect command/job ownership semantics;
- a real chunk operation can carry an explicit bounded count;
- the runtime can stop on terminal/error/OUTCOME_UNKNOWN conditions;
- one result envelope can report exactly how many items were attempted/completed;
- request and cost ceilings remain enforceable at the job model;
- chunk size becomes an auditable service parameter rather than accidental source-text repetition.

Therefore the preferred product correction is an explicit bounded Search-batch chunk action, not a parser workaround.

## 9. Required semantics for a future bounded chunk action

A correct chunk action should minimally provide:

```text
action = nextN / runChunk
jobId = existing bounded job
count = explicit positive integer with a conservative max
```

Execution semantics:

```text
for at most count pending items:
  claim exactly one next item;
  perform at most one provider request;
  persist provider result before advancing;
  stop immediately on OUTCOME_UNKNOWN;
  stop on local/provider terminal error unless an explicitly validated policy says otherwise;
  never exceed job maxRequests;
  never exceed job maxCostRub;
return one combined chunk result with per-item outcomes and updated job progress.
```

No parallel provider fan-out is needed or desired.

## 10. Optimal Step-09 live rollout after chunk support exists

The operational rollout should remain canary-based rather than immediately running all 75:

```text
canary #1 = already complete
next bounded chunk = 4
if complete and clean:
  next chunk = 10
then controlled chunks of approximately 15 until the initial tranche is exhausted
```

The exact later chunk sizes are an operational safety choice, not an SEO/Search methodology claim.

## 11. Current live truth

```text
bounded job created = true
initial queue = 75
provider requests executed = 1
successful provider requests = 1
pending = 74
failed_terminal = 0
outcome_unknown = 0
estimated incurred cost = 0.488 RUB
complete saved SERPs = 1
initial 75-query tranche complete = false
Step 09 complete = false
Step 10 allowed = false
```

## 12. Non-repeat controls added by this live test

```text
A. Do not infer service-specific Manual admission from the generic Manual contract.
B. Verify the exact installed validator behavior before designing a multi-command execution shape.
C. Distinguish transport/runtime capability from command-surface capability.
D. A successful canary validates the Search result path, not the entire 75-query semantic tranche.
E. Preserve each live SERP before additional paid acquisition.
F. Prefer explicit bounded orchestration actions over repeating service commands in source text.
```

Canonical operational lesson:

```text
RUNTIME CAN ADVANCE ONE ITEM SAFELY
+
MANUAL ACCEPTS ONE SEARCH-BATCH COMMAND
+
PROTOCOL HAS ONLY NEXT
=
SAFE BUT UNACCEPTABLY REPETITIVE OPERATOR LOOP.

THE CORRECT PRODUCT FIX IS EXPLICIT BOUNDED CHUNK ORCHESTRATION.
```
