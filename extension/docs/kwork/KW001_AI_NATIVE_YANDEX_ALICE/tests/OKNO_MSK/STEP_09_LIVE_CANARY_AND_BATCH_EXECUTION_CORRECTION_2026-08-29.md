# KW-001 / OKNO-MSK — Step 09 live canary and batch-execution correction

Date: 2026-08-29  
Status: **ACTIVE LIVE EXECUTION EVIDENCE / HISTORICAL CANARY + COMPLETED CORRECTION**

This document records the first real ordinary-Yandex-Search execution of Step 09, the live Manual-layer failure observed immediately before it, the resulting product correction, and the later completed `nextN` rollout.

For current state also read:

- `STEP_09_CURRENT_STATE_AND_EXECUTION_PROTOCOL_2026-08-29.md`
- `STEP_09_NEXTN_LIVE_CHUNK_VALIDATION_2026-08-29.md`
- `STEP_09_COLLECTION_METHOD_AND_IMMEDIATE_PERSISTENCE_POSTMORTEM_2026-08-29.md`
- `extension/docs/SEARCH_BATCH_NEXTN100_V0_1_2_CHANGELOG_AND_ACCEPTANCE_2026-08-29.md`

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

This satisfies the start gate: the bounded queue existed and creating it caused zero provider requests.

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

Therefore the Search transport/result path itself was live-validated for continuing Step 09.

## 7. Operational gap found at canary time

At the moment of the canary, the Search batch protocol exposed only:

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

and the installed Manual validator required exactly one `SEARCH_BATCH_API_V1` command per Manual block.

At that historical point:

```text
protocol had only next
+
Manual accepted one Search-batch command
=
one Manual click per paid item
```

For a 75-query tranche this was safe but operationally poor.

This section is a **historical pre-patch state**, not the current Bridge capability.

## 8. Product correction implemented

The correct fix was not to weaken `BATCH_SINGLE_COMMAND_REQUIRED` or place many `next` commands in one Manual block.

Instead Bridge `0.1.2` added an explicit bounded Manual-only action:

```text
SEARCH_BATCH_API_V1
{"action":"nextN","jobId":"...","count":N}
```

Current contract:

```text
1 <= count <= 100
Manual only
one Manual block = exactly one SEARCH_BATCH_API_V1 command
sequential execution
existing provider boundary reused
persist previous item before next provider boundary
UNKNOWN => stop immediately
terminal/non-OK => stop immediately
job maxRequests/maxCostRub remain authoritative
```

This implementation is current repository source, not a future proposal.

## 9. Actual live rollout after `nextN` support

The live rollout explicitly tested these requested `nextN.count` values:

```text
4
10
25
31
```

Therefore:

```text
LIVE_NEXT_N_REQUESTED_COUNTS_TESTED = [4, 10, 25, 31]
LIVE_NEXT_N_MAX_REQUESTED_COUNT_TESTED = 31
```

The earlier plan recorded before execution (`4 -> 10 -> approximately 15`) is superseded by the actual live sequence above.

Do not confuse requested count with confirmed provider executions for a given call:

```text
nextN.count = upper bound for that invocation
actual execution = confirmed_provider_executions + stopped_early/stop_reason truth
```

The distinct values `4,10,25,31` are known tested command sizes. They are not asserted here as the complete mathematical partition of the final R2 job.

## 10. Hard limit versus live-tested size

Protocol/runtime local testing validated:

```text
count = 100
```

with only three remaining synthetic items. Exactly three provider boundaries occurred and the runtime stopped at completion.

Therefore:

```text
HARD_PROTOCOL_CEILING = 100
COUNT_100_LOCAL_BOUNDED_TEST = PASS
COUNT_100_LOCAL_BOUNDED_TEST != 100 LIVE YANDEX REQUESTS IN ONE CHUNK
LARGEST_EXPLICIT_LIVE_REQUESTED_COUNT_TESTED = 31
```

The supported hard ceiling is 100; the largest explicitly live-tested requested size from this Step-09 rollout is 31.

## 11. Final live provider accounting

Because the original canary job later was not present in the current extension runtime, the remaining 74 frozen queries were run as a continuation job without replaying the paid first query:

```text
job_id = kw001-okno-msk-search-step09-20260829-r2
queries = 74
requests_started = 74
succeeded = 74
failed_terminal = 0
outcome_unknown = 0
estimated_cost_rub = 36.112
status = COMPLETED
```

Combined with the first canary:

```text
provider requests executed = 75
successful provider requests = 75
failed_terminal = 0
outcome_unknown = 0
estimated cumulative cost = 36.600 RUB
normalized TOP-10 rows recoverable/persisted = 750
```

Thus the old canary-time statement `initial 75-query tranche complete = false` is historical and superseded.

Current truth:

```text
PROVIDER_ACQUISITION_INITIAL_75 = COMPLETE
STEP09_COMPLETE = false
STEP10_ALLOWED = false
```

Provider acquisition completion does not equal analytical Step-09 acceptance.

## 12. Second process error discovered during the rollout: delayed project persistence

Although Bridge internally persisted each item before advancing, the workflow did **not** immediately write every returned live chunk/result to the project repository before allowing the next paid chunk.

That was a separate process error.

False assumption:

```text
BRIDGE_INTERNAL_DURABILITY == PROJECT_EVIDENCE_DURABILITY
```

Correct rule:

```text
BRIDGE_INTERNAL_DURABILITY != PROJECT_EVIDENCE_DURABILITY
CHAT_DELIVERY != PROJECT_EVIDENCE_DURABILITY
```

Required future gate:

```text
NEXT_N_RESULT_RECEIVED
-> PARSE_AND_VALIDATE
-> IMMEDIATE_REPOSITORY_WRITE_OF_COMMAND_AND_FULL_RESULT
-> GITHUB_READ_BACK_QA
-> COVERAGE/COST CHECKPOINT
-> ONLY THEN NEXT PAID CHUNK
```

If the write/read-back fails, another paid chunk is prohibited.

This error and its evidence-loss boundary are documented in detail in:

`STEP_09_COLLECTION_METHOD_AND_IMMEDIATE_PERSISTENCE_POSTMORTEM_2026-08-29.md`

## 13. Non-repeat controls from the complete live episode

```text
A. Do not infer service-specific Manual admission from the generic Manual contract.
B. Verify the exact installed validator behavior before designing a multi-command execution shape.
C. Distinguish transport/runtime capability from command-surface capability.
D. A successful canary validates the Search result path, not the full semantic tranche.
E. Prefer explicit bounded orchestration actions over repeated commands in source text.
F. Record actual live tested `nextN.count` values when executed.
G. Immediately persist every paid returned command/result receipt to project storage.
H. Read the persisted evidence back before issuing another paid chunk.
I. Never treat browser extension storage or chat delivery as the only durable project evidence copy.
J. Preserve historical pre-patch facts as historical; do not leave them phrased as current capability.
```

Canonical current operational lesson:

```text
ONE SEARCH-BATCH COMMAND PER MANUAL BLOCK
+
EXPLICIT MANUAL-ONLY nextN(count<=100)
+
SEQUENTIAL EXISTING PROVIDER BOUNDARY
+
STOP-ON-UNKNOWN / TERMINAL CONTROLS
+
IMMEDIATE PROJECT DURABLE WRITE AFTER EACH RETURNED CHUNK
=
CURRENT SAFE BOUNDED EXECUTION MODEL
```
