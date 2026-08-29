# KW-001 / OKNO-MSK — STEP 03R S16 CHECKPOINT

Date: 2026-08-29
Seed: **S16 `окна в рассрочку`**
Job: `kw001-okno-msk-wordstat-pass1-repair-20260829`

## Provider truth

```text
request_id = wordstat-batch-a8acc98b-a792-4d16-aead-b066ffd96337
operation = getTop
region = 213
device = DEVICE_ALL
numPhrases = 200
status = OK / SUCCEEDED
http_status = 200
request_executed = true
automatic_retry = false
outcome_unknown = 0
item estimated cost = 0.02 RUB
totalCount = 507
```

`totalCount` is demand/frequency for the seed, not the number of returned rows.

## Preservation accounting

```text
results returned = 68
results raw saved = 68
results TSV saved = 68
results verified = 68

associations returned = 13
associations raw saved = 13
associations TSV saved = 13
associations verified = 13

total provider rows returned = 81
total provider rows raw saved = 81
total provider rows TSV saved = 81
total provider rows verified = 81
```

Artifacts:

```text
STEP_03R_S16_RAW_PROVIDER_RESULT_2026-08-29.json
STEP_03R_S16_RAW_NORMALIZED.tsv
```

Read-back boundary verified:

```text
last results[] phrase = пластиковые окна в рассрочку подольск
first association = оконные откосы
last association = пленка для бронирования оконных стекол
totalCount = 507
```

No phrase cleaning, deduplication, relevance filtering, clustering or semantic acceptance was performed in this acquisition checkpoint.

## Historical non-repeat control

Historical Step 3 failed project purpose because provider calls were treated as completion while complete reusable rows were not preserved. S16 does not repeat that error:

```text
provider execution alone accepted as completion = false
complete raw result preserved = true
complete TSV preserved = true
raw/TSV counts reconciled = true
saved result read back = true
next provider item blocked until verification = true
```

## Gate

```text
S16_COMPLETE = true
NON_REPEAT_CONTROLS = PASS
S17_ALLOWED = true
STEP_03R_COMPLETE = false
```

Cumulative after S16:

```text
complete items = 16/18
remaining = 2/18
results preserved/verified = 1998
associations preserved/verified = 228
total provider rows preserved/verified = 2226
provider requests executed = 16
known provider outcomes = 16
failed_terminal = 0
outcome_unknown = 0
estimated provider cost = 0.32 RUB
```
