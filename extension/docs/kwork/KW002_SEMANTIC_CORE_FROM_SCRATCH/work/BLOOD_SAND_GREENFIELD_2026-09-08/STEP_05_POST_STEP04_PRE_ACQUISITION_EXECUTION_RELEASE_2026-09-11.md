# KW-002 Blood & Sand — Step05 post-Step04 pre-acquisition execution release

Date: 2026-09-11
Status: **RELEASED TO WORK / PROVIDER CALLS FORBIDDEN IN THIS PASS**

## Accepted upstream

```text
STEP03A = PASS
STEP03B_CORRECTED = ACCEPTED
STEP04_POST_SANITATION = ACCEPTED / PASS
STEP04_REMOTE_READBACK = PASS
CURRENT_STEP04_FAMILIES = 26 / 24 OBSERVED / 2 COVERAGE GAPS
CURRENT_STEP04_QUEUE_ROWS = 13
CURRENT_STEP04_FEEDBACK_ROWS = 10
```

Main ChatGPT acceptance authority:

`STEP_04_POST_SANITATION_MAIN_CHATGPT_RETURN_QA_2026-09-11.md`

## Current Step05 pre-step authorities

Read and execute exactly:

`STEP_05_POST_STEP04_PRE_ACQUISITION_WORK_PROMPT_2026-09-11.md`

Also read:

`STEP_05_POST_STEP04_PRE_STEP_EXTERNAL_RESEARCH_2026-09-11.md`

`STEP_05_POST_STEP04_QUEUE_GATE_2026-09-11.tsv`

`STEP_04_POST_SANITATION_EXECUTION_LESSON_2026-09-11.md`

`LEVEL1/EXECUTION_FAILURE_LEDGER_AND_ANTI_REGRESSION_RULE.md`

`KW002_EXECUTION_FAILURE_LEDGER_2026-09-11.md`

## Historical Step05 evidence boundary

The historical 17-row queue is superseded.

The durable E013 provider evidence is NOT superseded merely because queue IDs changed.

Mandatory reconciliation:

```text
HISTORICAL_E013 -> CURRENT_PSQ010
REPLAY_WITHOUT_GAP_PROOF = FORBIDDEN
```

Do not use the old 2026-09-10 `next_candidate_before_pause` as current authority. Upstream Step03B/Step04 rework materially changed the queue and family context.

## Work execution allowed now

Allowed:

- full current 13-row queue reconciliation;
- complete prior-acquisition overlap analysis;
- durable existing-evidence reuse analysis;
- exact candidate probe design;
- selection of exactly one first new probe if justified;
- pre-acquisition QA/materialization;
- GitHub publication/readback or owner relay.

Forbidden:

```text
WORDSTAT_PROVIDER_CALLS = 0
SEARCH_PROVIDER_CALLS = 0
GENSEARCH_PROVIDER_CALLS = 0
AI_SEARCH_PROVIDER_CALLS = 0
STEP06 = NOT STARTED
FINAL_ROW_CLEANUP = false
FINAL_CLUSTERING = false
PAGE_MAPPING = false
IA = false
```

## Stop

After the pre-acquisition Work return, STOP for Main ChatGPT QA.

A provider request may only be emitted after Main ChatGPT has verified the Work-selected first probe and frozen an exact single-request execution command.
