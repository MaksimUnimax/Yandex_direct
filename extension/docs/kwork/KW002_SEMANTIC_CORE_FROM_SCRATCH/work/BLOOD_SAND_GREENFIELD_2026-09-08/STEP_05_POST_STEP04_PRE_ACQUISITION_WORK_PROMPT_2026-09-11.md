# KW-002 Blood & Sand — Step05 post-Step04 pre-acquisition Work prompt

Date: 2026-09-11
Status: **CANONICAL WORK PROMPT / NO PROVIDER CALLS IN THIS PASS**

Continue the EXISTING KW-002 Blood & Sand greenfield semantic-core rehearsal.

THIS IS NOT A NEW PROJECT.
THIS IS NOT STEP04.
THIS IS NOT STEP06.
THIS IS NOT FINAL CLEANUP.
THIS IS A STEP05 PRE-ACQUISITION RECONCILIATION AND EXECUTION-MANIFEST TASK.

Repository:
`MaksimUnimax/Yandex_direct`

Branch:
`roadmap/kwork-productization-2026-08-28`

Job root:
`extension/docs/kwork/KW002_SEMANTIC_CORE_FROM_SCRATCH/work/BLOOD_SAND_GREENFIELD_2026-09-08`

## 0. Hard execution boundary

Do NOT make any provider request in this Work pass.

Specifically do NOT call:

- Wordstat;
- ordinary Search;
- GenSearch;
- AI-search/Alice;
- any external keyword database as project evidence.

Do NOT start Step06.
Do NOT perform final intent, final row cleanup, SERP clustering, query→page mapping, IA or Page Jobs.

The only purpose of this pass is to decide exactly what Step05 should acquire next, if anything, without duplicating already durable evidence.

## 1. Fetch live branch first

Fetch the CURRENT live branch before reading or writing.

Do not assume the branch is still at any SHA named in this prompt.

Shared branch may contain concurrent unrelated Kwork commits. Never reset, force-push or overwrite unrelated work.

## 2. Mandatory methodology/error authorities — read in full

Read in full before analysis:

`LEVEL1/EXECUTION_FAILURE_LEDGER_AND_ANTI_REGRESSION_RULE.md`

`LEVEL1/DATA_VOLUME_SANITATION_AND_DELIVERY_SCOPE_RULE.md`

`LEVEL1/PRE_STEP_EXTERNAL_RESEARCH_AND_SOURCE_DISCLOSURE_RULE.md`

`LEVEL1/WORK_HANDOFF_RULE.md`

`LEVEL2/STEP_RULES_INDEX.md`

Job-specific:

`KW002_EXECUTION_FAILURE_LEDGER_2026-09-11.md`

`STEP_04_POST_SANITATION_EXECUTION_LESSON_2026-09-11.md`

Current Step04 acceptance:

`STEP_04_POST_SANITATION_MAIN_CHATGPT_RETURN_QA_2026-09-11.md`

## 3. Current Step05 authorities — read in full

Read:

`STEP_04_POST_SANITATION_TARGETED_EXPANSION_QUEUE_2026-09-11.tsv`

Expected current queue rows = 13.

Read:

`STEP_05_POST_STEP04_PRE_STEP_EXTERNAL_RESEARCH_2026-09-11.md`

`STEP_05_POST_STEP04_QUEUE_GATE_2026-09-11.tsv`

These are current Step05 pre-step authorities.

The historical 17-row Step05 queue is superseded as a queue, but preserved evidence from it may still be valid.

## 4. Existing provider evidence that MUST be reconciled before any new probe

Read in full:

`STEP_05_E013_WORDSTAT_EVIDENCE_RECEIPT_2026-09-10.md`

`STEP_05_EXECUTION_CURSOR_2026-09-10.json`

And the durable RAW carrier referenced by that receipt:

`STEP_05_WORDSTAT_RAW/STEP05__E013__wordstat-132a43ff-7cf9-4544-a6e2-68da666c4813.raw.txt`

Known preserved facts:

```text
historical queue item = E013
phrase = !чётки
results = 2000
associations = 19
remote readback = PASS
raw blob = 550add6010ddbd10e0d807fd1a11046d2b782a4a
```

Current queue item `PSQ010` preserves historical `E013` lineage.

Do NOT replay `!чётки` merely because the queue was rebuilt.

You must determine whether:

```text
A. E013 fully answers current PSQ010 acquisition need;
B. E013 partially answers it but a genuinely different singular-form/product-form gap remains;
C. current PSQ010 should be deferred without new acquisition.
```

If B, propose the exact NEW probe, but do not execute it.

## 5. Primary-acquisition deduplication authority

Before proposing any NEW Step05 probe, reconcile it against what has already been asked/acquired.

Read at minimum:

`STEP_02_PRIMARY_ACQUISITION_MANIFEST_V2.csv`

`STEP_03_WORDSTAT_EXECUTION_MANIFEST_V1.csv`

`STEP_03_COLLECTION_CLOSURE_2026-09-09.md`

`STEP_03_RAW_RECOVERY_FINAL_RECEIPT_2026-09-10.md`

`STEP_03_RAW_RECOVERY_COMPLETION_STATE_2026-09-10.json`

Complete relevant `STEP_03_WORDSTAT_RAW` evidence as needed.

Do not decide uniqueness by comparing only literal seed strings.

For every proposed probe ask:

```text
Is this literally already acquired?
Is it semantically equivalent to an already acquired broad probe?
Would operators actually isolate a previously unresolved referent?
Does it target a current Step04 coverage gap/collision?
What information could change after this probe?
What is the stop condition?
Would no new evidence be a useful answer?
```

If the proposed query is merely a reordered or cosmetically altered version of prior acquisition, reject it as `DUPLICATE_LOW_INFORMATION_GAIN`.

## 6. Frozen client/business authorities

Use only allowed current job authorities.

Read:

`CLIENT_SUPPLIED_BRIEF.md`

`CLIENT_SUPPLIED_ASSORTMENT_MANIFEST.md`

`CLIENT_SUPPLIED_PRODUCT_CATALOG_OZON_76.csv`

`ALLOWED_INPUTS_AND_SEALED_SOURCES.md`

Do not use sealed prior Blood & Sand SEO/research.

Do not infer physical form/material/effect/audience from search queries when the client catalog does not state it.

## 7. Current queue gate to challenge, not blindly copy

Main ChatGPT's current provisional split is:

```text
NEW_PROVIDER_CANDIDATE_NEEDS_DEDUPED_PROBE_DESIGN:
PSQ001, PSQ004, PSQ005, PSQ006, PSQ007, PSQ008

OWNER_FACT_FIRST / OWNER_FACT_ONLY:
PSQ002, PSQ003, PSQ009, PSQ012, PSQ013

REUSE_EXISTING_PROVIDER_EVIDENCE_FIRST:
PSQ010

DEFER_TO_STEP10_UNLESS_CONCRETE_BOUNDARY_SURVIVES:
PSQ011
```

This split is an audit hypothesis.

You MUST independently verify it against the actual current data and prior acquisition history.

You may move a queue row to another gate if evidence proves the provisional classification wrong.

Do not optimize for preserving Main ChatGPT's split.

## 8. Required row-level queue output

Create:

`STEP_05_POST_STEP04_QUEUE_RECONCILIATION_WORK_2026-09-11.tsv`

Exactly one row per current PSQ001..PSQ013.

Minimum columns:

```text
queue_id
family_id
historical_relation
current_problem
current_evidence_summary
prior_acquisition_overlap
existing_provider_evidence_locator
owner_fact_dependency
provider_evidence_usefulness
recommended_gate
recommended_probe_id
recommended_probe_phrase
operator_rationale
region
device
num_phrases
expected_information_gain
what_result_would_change_decision
stop_condition
duplicate_probe_risk
collision_risk
later_route
confidence
```

Allowed `recommended_gate` values:

```text
OWNER_FACT_FIRST
OWNER_FACT_ONLY_NO_PROVIDER
REUSE_EXISTING_EVIDENCE_CLOSE
REUSE_EXISTING_EVIDENCE_PARTIAL
NEW_PROVIDER_PROBE_CANDIDATE
DEFER_STEP10
DEFER_SERP
NO_FURTHER_ACTION
```

## 9. Existing-evidence reuse register

Create:

`STEP_05_POST_STEP04_EXISTING_EVIDENCE_REUSE_REGISTER_2026-09-11.tsv`

At minimum audit historical E013 → current PSQ010.

Columns:

```text
current_queue_id
historical_queue_id
provider_request_id
raw_path
raw_blob_sha
results_rows
associations_rows
remote_readback
what_current_question_it_answers
what_it_does_not_answer
replay_required
replay_reason
```

Any durable evidence with `replay_required=YES` must explain why its preserved payload is insufficient.

## 10. Build the minimal NEW provider candidate manifest

Create:

`STEP_05_POST_STEP04_PROVIDER_CANDIDATE_MANIFEST_V1_2026-09-11.tsv`

This is NOT an execution result.

Include only genuinely non-duplicate candidate probes.

Minimum columns:

```text
probe_id
queue_id
priority_order
phrase
numPhrases
regions
devices
operator_usage
prior_probe_difference
expected_information_gain
collision_guard
stop_condition
max_requests_for_this_probe
estimated_cost_rub
execution_status
```

Required:

```text
execution_status = NOT_EXECUTED
```

Current externally verified provider defaults, only if current Bridge evidence remains compatible:

```text
numPhrases <= 2000
region = 225
device = DEVICE_ALL
Wordstat GetTop current rate = 0.02 RUB/request
project execution = sequential one-result persist/readback before next
```

Do not inflate the manifest just because six queue rows are provisional provider candidates.

It is valid for some rows to have **no new probe** after acquisition-history reconciliation.

## 11. Select exactly ONE first new provider candidate

If at least one new provider probe survives deduplication, select exactly ONE as the next executable probe.

Selection priority:

```text
1. material current coverage gap or collision;
2. no required unresolved client fact;
3. clearly non-duplicate of Step03 and preserved Step05 evidence;
4. high expected boundary/coverage information gain;
5. bounded operator expression with low foreign-context spill;
6. useful negative result / clear stop condition;
7. smallest safe request footprint.
```

Do not select by raw frequency.

Do not select because the old 2026-09-10 cursor had a next candidate.

The old next candidate is not current authority after upstream rework.

## 12. Mandatory anti-regression checks

At minimum:

```text
CURRENT_QUEUE_ROWS = 13
CURRENT_QUEUE_ROWS_RECONCILED = 13
UNKNOWN_QUEUE_ROWS = 0
DUPLICATE_QUEUE_ROWS = 0

HISTORICAL_E013_FOUND = true
HISTORICAL_E013_REMOTE_EVIDENCE_VALID = true|false with evidence
BLIND_E013_REPLAY = false

PROPOSED_NEW_PROBES_ALREADY_LITERAL_IN_STEP03 = 0
PROPOSED_NEW_PROBES_SEMANTICALLY_REDUNDANT_WITHOUT_OPERATOR_GAIN = 0
OWNER_FACT_GATED_ROWS_SENT_TO_PROVIDER = 0
STEP10_DEFERRED_ROWS_SENT_TO_PROVIDER = 0

PROVIDER_CALLS_EXECUTED_IN_WORK = 0
WORDSTAT_CALLS_EXECUTED_IN_WORK = 0
SEARCH_CALLS_EXECUTED_IN_WORK = 0
GENSEARCH_CALLS_EXECUTED_IN_WORK = 0
AI_SEARCH_CALLS_EXECUTED_IN_WORK = 0

SEALED_SOURCE_VIOLATIONS = 0
DELIVERY_CAP_USED_AS_RELEVANCE_RULE = 0
FINAL_CLEANUP_PERFORMED = false
FINAL_CLUSTERING_PERFORMED = false
PAGE_OR_IA_DECISIONS = 0
```

Schema anti-regression from the accepted Step04 execution lesson:

```text
OUTPUT_SCHEMA_FROZEN = PASS
QA_SCHEMA_COMPATIBILITY = PASS
```

Validate schemas before full output materialization.

## 13. Pre-acquisition QA report

Create:

`STEP_05_POST_STEP04_PRE_ACQUISITION_QA_2026-09-11.md`

It must include:

- all counts;
- queue gate breakdown;
- historical E013 disposition;
- deduplication results against Step02/03;
- all candidate probes with reasons accepted/rejected;
- exact selected first probe if any;
- exact bridge-envelope parameters for that first probe;
- expected cost;
- persistence/readback plan;
- immediate Step03A/03B feed-forward plan for new rows;
- known failure regression matrix;
- hard stop after the first provider result;
- quality score;
- plain-Russian explanation.

## 14. Quality gate

Fresh score; do not reuse Step04 score.

Minimum dimensions:

```text
CURRENT_QUEUE_RECONCILIATION
EXISTING_EVIDENCE_REUSE
PROBE_DEDUPLICATION
INFORMATION_GAIN_QUALITY
OWNER_FACT_BOUNDARY
PROVIDER_METHOD_ACCURACY
PERSISTENCE_PLAN
STEP03A_03B_FEED_FORWARD_SAFETY
KNOWN_FAILURE_REGRESSION
SCOPE_CONTROL
REPRODUCIBILITY
```

PASS candidate requires:

```text
overall >= 90/100
critical dimensions >= 9/10
zero duplicate/replay defects
zero owner-fact bypass
zero provider calls in this Work pass
```

## 15. Work return

Create:

`STEP_05_POST_STEP04_PRE_ACQUISITION_WORK_RETURN_2026-09-11.md`

Return exactly:

```text
LIVE_BASE_HEAD = <sha>
CURRENT_QUEUE_ROWS = 13
QUEUE_RECONCILED = 13/13

NEW_PROVIDER_PROBE_CANDIDATES = <integer>
OWNER_FACT_FIRST_OR_ONLY = <integer>
EXISTING_EVIDENCE_REUSE = <integer>
DEFERRED = <integer>
NO_FURTHER_ACTION = <integer>

HISTORICAL_E013_DISPOSITION = <state>
HISTORICAL_E013_REPLAY_REQUIRED = true|false

FIRST_NEW_PROBE_SELECTED = true|false
FIRST_NEW_PROBE_ID = <id or NONE>
FIRST_NEW_PROBE_QUEUE_ID = <queue id or NONE>
FIRST_NEW_PROBE_PHRASE = <exact phrase or NONE>
FIRST_NEW_PROBE_MAX_REQUESTS = <integer>
FIRST_NEW_PROBE_MAX_COST_RUB = <number>

DUPLICATE_PROBES_REJECTED = <integer>
OWNER_FACT_BYPASSES = 0
PROVIDER_CALLS_EXECUTED = 0
SEALED_SOURCE_VIOLATIONS = 0

QUALITY_SCORE_100 = <number>
FINAL_WORK_VERDICT = PASS_CANDIDATE|REWORK_REQUIRED

STEP05_PROVIDER_EXECUTION_ALLOWED = false
STEP06_STARTED = false
```

Then add `ПРОСТЫМИ СЛОВАМИ` explaining which current gaps remain, what old evidence was reused, why the selected first probe is genuinely new, and why no provider call was made yet.

## 16. Publication

Persist the Work outputs to GitHub if transport is reliable and perform remote readback.

If transport is not reliable, prepare owner-relay individual files + ZIP exactly as in the accepted prior workflow.

Do not spend time debugging transport.

## 17. Stop condition

STOP after materializing and publishing/relay-preparing the pre-acquisition authorities.

Do not execute the selected provider probe.
Do not start Step06.
Return control to Main ChatGPT for the first-provider-command gate.
