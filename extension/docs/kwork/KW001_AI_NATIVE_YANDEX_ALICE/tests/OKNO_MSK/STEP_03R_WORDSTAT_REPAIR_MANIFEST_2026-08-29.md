# KW-001 / OKNO-MSK — STEP 03R WORDSTAT REPAIR MANIFEST

Date: 2026-08-29
Status: **FROZEN / OWNER AUTHORIZED / READY FOR MANUAL YMB EXECUTION**

## Whole Kwork goal

Deliver a complete, evidence-backed semantic set and site/page structure recommendation for Yandex human search plus selective Yandex AI-search evidence, with client-ready artifacts and final QA.

## Already genuinely completed

- Step 0 scope freeze.
- Step 1 site/business discovery.
- Step 2 frozen 18-seed acquisition plan.
- Step-05 four provider observations preserved completely, with sufficiency to be rechecked after Step 03R.
- Step-06 four dynamics observations preserved completely.
- Historical Step-03 acceptance has been superseded because complete phrase rows were not preserved.

## Remaining work across the Kwork

1. Complete Step 03R: reacquire and preserve all 18 first-pass Wordstat responses.
2. Recheck whether the complete first-pass set reveals additional important acquisition directions.
3. Clean the complete phrase set.
4. Freeze the working semantic set.
5. Check important query/page boundaries in ordinary Yandex Search.
6. Group queries by user task and determine page actions.
7. Select material uncertain cases for Yandex AI-search evidence.
8. Compare ordinary Search and AI evidence.
9. Prioritize actions.
10. Produce client deliverables.
11. Run final QA and revision gate.

## Current step goal

Collect the exact original 18 Wordstat `getTop` observations again and preserve every returned `results[]` and `associations[]` row before any next provider request is allowed.

## What this step solves

The historical first acquisition pass technically executed 18 successful provider calls but failed the project goal because complete returned phrase rows were not preserved. Downstream semantic work is blocked until a complete reusable first-pass dataset exists.

## Required output

For all 18 frozen seeds, the current job workspace must contain and verify:

```text
seed_id
seed_phrase
normalized command
region = 213
device = DEVICE_ALL
numPhrases = 200
request_id
provider outcome truth
exact complete delivered result envelope
root totalCount
all results[] rows
all associations[] rows
results_count_returned
associations_count_returned
rows_saved = results_count_returned + associations_count_returned
rows_verified = rows_saved
readable/usable saved artifact
```

`totalCount` is frequency evidence and is NOT the returned-row count.

## Past errors reread before this step

Authority: `../../STEP_METHOD_REVIEW_AND_LESSONS_LEDGER.md`, Step 3.

Relevant prior error:

```text
technical API success was treated as collection completion;
representative examples were saved instead of complete returned rows;
the batch was accepted as complete and downstream work continued.
```

Non-repeat control for this step:

```text
ONE PROVIDER ITEM
→ RECEIVE FULL RESULT
→ SAVE FULL RESULT
→ COUNT RESULTS[]
→ COUNT ASSOCIATIONS[]
→ VERIFY SAVED COUNTS
→ VERIFY READABLE/USABLE
→ ONLY THEN NEXT PROVIDER ITEM
```

If any preservation/completeness check fails:

```text
CURRENT_ITEM = INCOMPLETE
NEXT_PROVIDER_ITEM = BLOCKED
STEP_03R = NOT_COMPLETE
FORWARD_ANALYSIS = BLOCKED
```

## External method support checked before execution

Official Yandex Wordstat GetTop:
- https://aistudio.yandex.ru/en/docs/search-api/api-ref/Wordstat/getTop
- https://aistudio.yandex.ru/ru/docs/search-api/operations/wordstat-gettop

Official pricing:
- https://aistudio.yandex.ru/docs/ru/search-api/pricing.html

Confirmed current official semantics:
- GetTop is the Wordstat method for top queries containing the specified phrase plus similar queries.
- numPhrases supports 1..2000.
- region/device are request controls.
- official example uses region 213 and DEVICE_ALL.
- GetTop costs 20 RUB per 1000 requests in the current RUB tariff.

Method classification:

```text
GetTop semantics = OFFICIAL
region/device/numPhrases request controls = OFFICIAL
same 18 frozen seeds = PROJECT-SPECIFIC / previously frozen Step-02 input
200-row bound = PROJECT-SPECIFIC productization control
per-item save-before-next gate = OWNER-APPROVED PROCESS CORRECTION + PROJECT_TEST_VALIDATED
```

## Frozen provider controls

```text
service = wordstat
method = getTop
execution_mode = Manual
manual = ON
autorun = OFF
job_id = kw001-okno-msk-wordstat-pass1-repair-20260829
region = 213
devices = ["DEVICE_ALL"]
numPhrases = 200
seed_count = 18
maxRequests = 18
estimated_provider_cost = 0.36 RUB
```

## Exact frozen seed order

```text
S01 пластиковые окна
S02 окна rehau
S03 французские окна
S04 окна п 44
S05 пластиковые двери
S06 остекление балконов
S07 остекление балкона с крышей
S08 остекление балкона п 46
S09 пластиковые окна митино
S10 остекление веранды
S11 алюминиевые окна
S12 аксессуары для пластиковых окон
S13 установка пластиковых окон
S14 ремонт пластиковых окон
S15 цены на пластиковые окна
S16 окна в рассрочку
S17 как выбрать пластиковые окна
S18 пластиковые окна от производителя
```

No seed substitution or new expansion phrase is allowed inside Step 03R.

## YMB step objective

Obtain the complete current GetTop result for each of the 18 frozen seeds and preserve it as reusable project evidence.

## YMB required mode

```text
ACTIVE SERVICE = Wordstat
EXECUTION MODE = Manual
MANUAL = ON
AUTORUN = OFF
```

## YMB required saved result after every provider interaction

For the current item, save:

1. the exact complete `WORDSTAT_BATCH_RESULT_V1` envelope;
2. every `provider_result.result.results[]` row;
3. every `provider_result.result.associations[]` row;
4. metadata identifying seed, request, region, device and requested count;
5. a normalized TSV copy for later analysis.

## YMB completeness check after every provider interaction

```text
provider outcome known
request_executed truth known
results_count = results.length
associations_count = associations.length
normalized_rows_saved = results_count + associations_count
normalized_rows_verified = normalized_rows_saved
raw envelope saved = true
normalized TSV readable = true
```

Only after all applicable checks pass may the next `batch.next` be issued.

## YMB stop conditions

Stop immediately and do not issue another provider request when:

- provider outcome is `OUTCOME_UNKNOWN`;
- complete provider payload is missing;
- returned arrays cannot be counted;
- raw envelope cannot be saved;
- saved row counts do not reconcile;
- saved artifact is unreadable/unusable.

A pre-provider failure with `request_executed=false` may be repaired/replayed only after the cause is understood and the unchanged item remains safe to execute.

## Required markers

```text
KWORK_GOAL_RESTATED = true
COMPLETED_WORK_REVIEWED = true
REMAINING_WORK_REVIEWED = true
STEP_GOAL_DEFINED = true
STEP_REQUIRED_OUTPUT_DEFINED = true
PAST_STEP_ERRORS_REREAD = true
PAST_ERRORS_REPORTED_TO_OWNER = true
NON_REPEAT_CONTROLS_DEFINED = true
YMB_INTERACTION_GATE_EMBEDDED = true
YMB_PROJECT_RESULT_DEFINED = true
YMB_REQUIRED_STORAGE_DEFINED = true
YMB_COMPLETENESS_CHECK_DEFINED = true
YMB_STOP_ON_INCOMPLETE_RESULT = true
OWNER_AUTHORIZED = true
```

## Step pass condition

Step 03R can pass only when:

```text
provider items planned = 18
all 18 required items have known outcomes
all successful required provider results are fully preserved
sum(results rows returned) = sum(results rows saved) = sum(results rows verified)
sum(association rows returned) = sum(association rows saved) = sum(association rows verified)
incomplete items = 0
outcome_unknown = 0
all required artifacts readable/usable = true
NON_REPEAT_CONTROLS = PASS
```

Technical success alone cannot satisfy this gate.
