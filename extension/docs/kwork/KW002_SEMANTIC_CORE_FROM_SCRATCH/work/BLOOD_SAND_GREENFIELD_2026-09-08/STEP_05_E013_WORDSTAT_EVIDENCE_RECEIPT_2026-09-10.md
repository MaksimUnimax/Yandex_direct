# STEP 05 — E013 WORDSTAT EVIDENCE RECEIPT

Date: 2026-09-10
Job: `BLOOD_SAND_GREENFIELD_2026-09-08`
Step: `05 — targeted expansion / coverage control`
Queue item: `E013`
Status: **PROVIDER EVIDENCE ACQUIRED / PERSISTED / REMOTE COUNT PASS / E013 COVERAGE QUESTION CLOSED FOR STEP05**

## Provider request

```text
SERVICE = wordstat
OPERATION = getTop
BRIDGE = yandex-marketing-bridge 0.1.4
REQUEST_ID = wordstat-132a43ff-7cf9-4544-a6e2-68da666c4813
PHRASE = !чётки
NUM_PHRASES = 2000
REGION = 225
DEVICE = DEVICE_ALL
HTTP_STATUS = 200
STATUS = OK
ELAPSED_MS = 24656
REQUEST_EXECUTED = true
AUTOMATIC_RETRY = false
ESTIMATED_COST_RUB = 0.02
```

## Why this probe existed

Step04 queue item `E013` preserved a material morphology boundary: provider observations for `чётки` were mixed with `чётко/чёткий`. The fresh Step05 source trace established that the Wordstat `!` operator fixes the word form. The purpose of this request was therefore not final cleanup or clustering, but a controlled test of whether the exact-token family exposes a stable physical-product vocabulary.

## Durable RAW

```text
RAW_PATH = STEP_05_WORDSTAT_RAW/STEP05__E013__wordstat-132a43ff-7cf9-4544-a6e2-68da666c4813.raw.txt
RAW_BLOB_SHA = 550add6010ddbd10e0d807fd1a11046d2b782a4a
RAW_COMMIT = 9161fe6f286d1e7bc02f9f46698c71df444792e4
NORMALIZATION = UTF-8 normalized equivalent; all provider fields, all results and all associations preserved; not claimed byte-identical transport
```

## Remote completeness QA

The normalized RAW uses one result object per line and one association object per line.

```text
FIRST_RESULT_LINE = 32
LAST_RESULT_LINE = 2031
RESULT_ROWS = 2031 - 32 + 1 = 2000 / DIRECT REMOTE LINE-POSITION COUNT / PASS
RESULTS_CLOSE_LINE = 2032
ASSOCIATIONS_MARKER_LINE = 2033
FIRST_ASSOCIATION_LINE = 2034
LAST_ASSOCIATION_LINE = 2052
ASSOCIATION_ROWS = 2052 - 2034 + 1 = 19 / DIRECT REMOTE LINE-POSITION COUNT / PASS
TOTALCOUNT_LINE = 2054
TOTALCOUNT = 119294 / PASS
REMOTE_FIRST_RESULT = четки / 503654
REMOTE_LAST_RESULT = четки барнаул / 55
REMOTE_READBACK = PASS
```

## Evidence interpretation

The operator result does **not** mean every returned row is the physical product. `!` fixes the target word form; it does not ban other words in the same query, so rows such as `четкие четки` can legitimately remain. There are also typo/semantic-noise rows, media/book/music contexts and unrelated uses. Those remain for later row-level cleanup.

However, the exact-token corpus independently exposes a large and diverse physical/commercial vocabulary. Representative observed rows include:

```text
четки = 503654
купить четки = 14171
четки православные = 12029
четки перекидные = 9342
мусульманские четки = 5715
четки в машину = 3736
нефритовые четки = 3407
четки сколько бусин = 3321
четки из камня = 2145
где купить четки = 1803
четки цена = 1641
деревянные четки = 1365
четки из дерева = 1322
четки из янтаря = 1004
четки из натуральных камней = 730
четки на авито = 708
четки в автомобиль = 463
четки в авто = 342
четки в машину на зеркало = 302
купить четки в машину = 290
четки автомобильные = 271
купить четки на озоне = 236
четки оберег = 156
```

This is enough for the Step05 coverage question: `чётки` is not merely a provider morphology artifact. Physical-product, commercial, religious-form, material and in-car formulations are directly observed.

The 19 associations are mostly generic (`очень`, `лучше всех`, `что это такое`, etc.) and have low information value for this queue item. They are preserved as provider evidence but are not used to invent new Blood & Sand families.

## Step05 decision for E013

```text
E013_PROVIDER_EVIDENCE = ACQUIRED
E013_MORPHOLOGY_BOUNDARY = CLARIFIED
E013_PHYSICAL_PRODUCT_VOCABULARY_OBSERVED = YES
E013_COMMERCIAL_VOCABULARY_OBSERVED = YES
E013_AUTOMOTIVE_VOCABULARY_OBSERVED = YES
E013_ADDITIONAL_WORDSTAT_PROBE_REQUIRED_NOW = NO
E013_FINAL_RELEVANCE_CLEANUP_PERFORMED = false
E013_FINAL_CLUSTERING_PERFORMED = false
E013_PAGE_DECISION_PERFORMED = false
```

E013 is therefore closed for **Step05 coverage acquisition**, not declared finally cleaned or clustered. Relevant rows remain input for later row-level cleanup / intent stages.

## Cost / sequencing

```text
STEP05_PROVIDER_CALLS_EXECUTED = 1
STEP05_ESTIMATED_PROVIDER_COST_RUB = 0.02
NEXT_PROVIDER_CALL_ALLOWED_ONLY_AFTER_THIS_RECEIPT_AND_CURSOR_ARE_DURABLY PERSISTED_AND_READ_BACK = true
```
