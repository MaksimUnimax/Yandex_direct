# KW-001 / OKNO-MSK — STEP 03 WORDSTAT PASS #1 PREFLIGHT

Date: 2026-08-28  
Status: **READY FOR PROVIDER EXECUTION / RESULTS NOT YET ACQUIRED**

Depends on:

```text
STEP_01_ACCEPTANCE.md
STEP_02_SEED_QUERY_PLAN.md
STEP_02_ACCEPTANCE.md
../../DIALOGUE_AND_ANALYTICAL_DISCIPLINE.md
```

## 1. Step purpose

Execute the frozen first Wordstat discovery pass over the 18 Step-02 seeds using the accepted durable batch hand.

This step is not complete until all safely executable batch items reach terminal evidence states and the results are preserved for the next cleanup step.

---

## 2. Critical interpretation rule — SEED IS NOT FINAL KEYWORD

**RULE**  
A Wordstat seed is an acquisition probe used to open a demand/vocabulary family. It is not automatically a keyword that will be retained in the client's final semantic core.

**PURPOSE**  
Allow uncertain, narrow or diagnostic formulations to be measured without prematurely declaring them valuable search targets.

**EVIDENCE**  
The accepted Wordstat workflow uses broad seeds to discover provider-returned query vocabulary. Final relevance, intent, frequency role, clustering and page mapping happen after acquisition.

**FAILURE IF IGNORED**  
If seed and final keyword are conflated, the analyst may either:

```text
keep a useless phrase merely because it was used as a seed
OR
remove a useful diagnostic seed merely because it sounds uncommon before measurement
```

**REVIEW TRIGGER**  
None. Seed provenance and final semantic status are different fields by design.

Later semantic states must be decided from returned evidence, not seed membership. A phrase may ultimately become:

```text
PRIMARY
SUPPORTING_LONGTAIL
REVIEW
EXCLUDED
```

and a seed phrase itself may be excluded while the vocabulary it discovers remains useful.

---

## 3. Region preflight

Frozen mock order:

```text
primary_region = Moscow
```

Verified provider region:

```text
Moscow = 213
Russia = 225
Moscow + Moscow Region = 1
```

The accepted batch protocol defaults missing `regions` to `["225"]`, which would incorrectly broaden this order to all Russia.

Therefore every pass-1 command must explicitly use:

```text
regions = ["213"]
```

**PURPOSE**  
Prevent a silent default from changing the geographic meaning of the demand evidence.

Official verification basis: current Yandex Wordstat/Search API documentation states that region `213` is Moscow and that allowable Wordstat regions can be obtained from `getRegionsTree`.

---

## 4. Accepted batch protocol verified

Current accepted source:

```text
extension/src/shared/wordstat_batch_protocol.js
```

Protocol facts verified before execution:

```text
prefix = WORDSTAT_BATCH_API_V1
actions = start / next / status / pause / resume / cancel
phrases maximum per job = 500
numPhrases = 1..2000
regions = explicit array
devices = DEVICE_ALL / DEVICE_DESKTOP / DEVICE_PHONE / DEVICE_TABLET
maxRequests = bounded integer
```

The batch runtime verifies:

```text
start = creates durable job, no provider request
next = claims exactly one safe pending item and can initiate at most one provider request
successful items are persisted
OUTCOME_UNKNOWN is persisted and is not automatically replayed
resume continues from safe pending items rather than restarting the list
```

---

## 5. Frozen pass-1 job manifest

```text
job_id = kw001-okno-msk-wordstat-pass1-20260828
method = getTop
region = 213 (Moscow)
devices = DEVICE_ALL
numPhrases = 200
maxRequests = 18
seed_count = 18
```

Seeds, unchanged from frozen Step 02:

```text
01 пластиковые окна
02 окна rehau
03 французские окна
04 окна п 44
05 пластиковые двери
06 остекление балконов
07 остекление балкона с крышей
08 остекление балкона п 46
09 пластиковые окна митино
10 остекление веранды
11 алюминиевые окна
12 аксессуары для пластиковых окон
13 установка пластиковых окон
14 ремонт пластиковых окон
15 цены на пластиковые окна
16 окна в рассрочку
17 как выбрать пластиковые окна
18 пластиковые окна от производителя
```

No seed is treated as client-approved final semantics merely because it is present in this list.

---

## 6. Exact start command

```text
WORDSTAT_BATCH_API_V1
{"action":"start","jobId":"kw001-okno-msk-wordstat-pass1-20260828","phrases":["пластиковые окна","окна rehau","французские окна","окна п 44","пластиковые двери","остекление балконов","остекление балкона с крышей","остекление балкона п 46","пластиковые окна митино","остекление веранды","алюминиевые окна","аксессуары для пластиковых окон","установка пластиковых окон","ремонт пластиковых окон","цены на пластиковые окна","окна в рассрочку","как выбрать пластиковые окна","пластиковые окна от производителя"],"numPhrases":200,"regions":["213"],"devices":["DEVICE_ALL"],"maxRequests":18}
```

Expected start truth:

```text
request_executed = false
progress.total = 18
progress.pending = 18
```

---

## 7. Execution procedure after start

For each safe next item use:

```text
WORDSTAT_BATCH_API_V1
{"action":"next","jobId":"kw001-okno-msk-wordstat-pass1-20260828"}
```

One `next` claims one pending item and attempts at most one Wordstat request.

Execution may be sent in small controlled groups at the chat transport layer, but every `next` remains an independent accepted batch command and the runtime persists each item before proceeding.

If any item reports:

```text
request_executed = UNKNOWN
```

stop issuing further `next` commands until the unknown outcome is reconciled. Do not replay that item automatically.

After the final item, obtain:

```text
WORDSTAT_BATCH_API_V1
{"action":"status","jobId":"kw001-okno-msk-wordstat-pass1-20260828"}
```

---

## 8. Step-03 completion gate

Step 03 can PASS only when:

```text
region 213 explicitly used = true
job created = true
18 frozen seeds unchanged = true
all safely executable items terminal = true
no automatic replay of OUTCOME_UNKNOWN = true
provider request count recorded = true
estimated/provider cost truth recorded = true
raw provider results preserved = true
item-level failures/unknowns preserved = true
final job status captured = true
```

No semantic cleaning is performed inside Step 03 except mechanical preservation. Relevance decisions belong to the next step.

Current marker:

```text
KW001_OKNO_MSK_STEP_03_WORDSTAT_PASS1_PREFLIGHT_READY = true
KW001_OKNO_MSK_STEP_03_WORDSTAT_PASS1_COMPLETE = false
```
