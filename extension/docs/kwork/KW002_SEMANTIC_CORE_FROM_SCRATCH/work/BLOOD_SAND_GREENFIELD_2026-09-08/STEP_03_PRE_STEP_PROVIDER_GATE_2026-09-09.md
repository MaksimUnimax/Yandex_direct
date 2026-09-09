# KW-002 Blood & Sand — STEP 03 PRE-STEP / PROVIDER GATE

Date: 2026-09-09  
Status: **PRE-STEP REVIEW COMPLETE / BATCH START ALLOWED / FIRST PROVIDER ITEM MUST BE OR-CAPABILITY CHECK**  
Job: `BLOOD_SAND_GREENFIELD_2026-09-08`

## 1. Whole Kwork goal

Build from scratch, from frozen client facts plus fresh Yandex evidence:

```text
business + actual assortment
→ acquisition probes
→ current Wordstat demand
→ coverage control
→ current Yandex competitors
→ competitor semantic expansion
→ candidate semantic master
→ row-level cleanup / user task / intent
→ ordinary Yandex Search evidence
→ task/SERP clustering
→ query→page ownership + Search-only IA
→ bounded generative Yandex/Alice evidence
→ Search-vs-AI reconciliation
→ final semantic core + IA + Page Jobs + internal links
→ client deliverables + QA
```

## 2. Full roadmap / current progress

| Step | Purpose | Status |
|---|---|---|
| 00 | Freeze order/scope/source boundary | ✅ COMPLETE / Ozon-only correction applied |
| 01 | Build factual business + complete Ozon assortment model | ✅ COMPLETE / PASS |
| 02 | Build seed/acquisition probe map | ✅ COMPLETE / V2 PASS / `93/100 = 9.3/10` |
| 03 | Primary Wordstat acquisition | 🟡 CURRENT / PRE-STEP PROVIDER GATE COMPLETE |
| 04 | First family triage | ⬜ NOT STARTED |
| 05 | Targeted expansion / coverage | ⬜ NOT STARTED |
| 06 | Current Yandex competitor discovery | ⬜ NOT STARTED |
| 07 | Competitor semantic expansion | ⬜ NOT STARTED |
| 08 | Competitor-derived Wordstat expansion | ⬜ NOT STARTED |
| 09 | Candidate semantic master freeze | ⬜ NOT STARTED |
| 10 | Row-level cleanup / intent / user job | ⬜ NOT STARTED |
| 11 | Search-stage semantic freeze | ⬜ NOT STARTED |
| 12 | Ordinary Yandex Search batch | ⬜ NOT STARTED |
| 13 | SERP + task-first clustering | ⬜ NOT STARTED |
| 14 | Query→page ownership + Search-only IA | ⬜ NOT STARTED |
| 15 | AI-search diagnostic selection | ⬜ NOT STARTED |
| 16 | AI-search evidence acquisition | ⬜ NOT STARTED |
| 17 | Search-vs-AI reconciliation | ⬜ NOT STARTED |
| 18 | Final core + IA + Page Jobs + internal links | ⬜ NOT STARTED |
| 19 | Client deliverables | ⬜ NOT STARTED |
| 20 | Final QA / recipient acceptance | ⬜ NOT STARTED |
| 21 | Revision rehearsal + Kwork measurement | ⬜ NOT STARTED |
| 22 | Final handoff / close | ⬜ NOT STARTED |

## 3. Live state read before Step 03

Live branch HEAD checked before this gate:

`7d06a732063dc3422cf56c72cd98733231fc0383`

The HEAD moved after the Step-02 work because of an unrelated KW-001 evidence commit. Current KW-002 `JOB_FLOW.md` and the V2 79-row primary manifest were re-read at the live HEAD and remain intact.

## 4. Current Step-03 exact goal

Acquire current Yandex human-demand evidence for every authorised Step-02 V2 primary probe while preserving the complete provider payload, request provenance and acquisition status.

```text
STEP03 = ACQUISITION / PERSISTENCE
STEP03 != CLEANUP
STEP03 != KEEP/REJECT
STEP03 != CLUSTERING
STEP03 != PAGE DESIGN
```

## 5. Permanent Step-03 rules applied

From KW002 Level 2 / inherited KW001 Step 3:

```text
DEFINE REQUIRED RESULT
→ EXECUTE
→ RECEIVE COMPLETE RESULT
→ DURABLY SAVE COMPLETE RETURNED ROWS
→ READBACK
→ COUNT/FIELD/PROVENANCE RECONCILIATION
→ ONLY THEN NEXT ITEM
```

Preserve all returned occurrences, including duplicates, low-frequency rows and association/similar rows.

```text
HTTP 200 != ACQUISITION COMPLETE
SUCCEEDED != EVIDENCE PERSISTED
RAW OCCURRENCE != DEDUPED SEMANTIC ROW
```

## 6. Relevant prior errors / non-repeat controls

### Error A — provider success was previously treated too close to evidence completion

Control: no next provider item before the current provider payload is durably persisted and read back.

### Error B — only summaries/examples could survive instead of the complete provider return

Control: preserve the complete `provider_result`, including `results`, `associations`, `totalCount`, command, request ID and batch/item metadata.

### Error C — duplicate phrase observations could be collapsed too early

Control: raw occurrence layer preserves every seed→phrase occurrence. Any exact-text deduplication is a separate derived view later.

### Error D — Step 02 V1 over-trusted noisy bare seeds

Control: current authority is only `STEP_02_PRIMARY_ACQUISITION_MANIFEST_V2.csv`; old V1 priorities are forbidden as the current execution list.

### Error E — grouped OR behavior through the actual Bridge path is not live-verified yet

Control: first provider item is Q001. Do not execute the second provider item until Q001 is persisted, inspected and the grouped-OR behavior is accepted.

## 7. External provider/method truth checked on 2026-09-09

Official Yandex Search API / Wordstat:

- GetTop returns last-30-day popular queries containing the supplied phrase and similar queries;
- response exposes `totalCount`, `results[]` and `associations[]`;
- `numPhrases` accepts 1..2000;
- region `225` = Russia;
- `DEVICE_ALL` = all devices;
- phrase supports search operators;
- current GetTop price = 20 RUB / 1000 requests including VAT.

Sources:

```text
https://aistudio.yandex.ru/en/docs/search-api/api-ref/Wordstat/getTop
https://aistudio.yandex.ru/en/docs/search-api/operations/wordstat-gettop
https://aistudio.yandex.ru/ru/docs/search-api/pricing
https://aistudio.yandex.ru/en/docs/search-api/reference/regions
```

## 8. Bridge capability / current production contract

Current Yandex Marketing Bridge version in this branch is `0.1.2`.

Accepted Wordstat batch protocol:

```text
WORDSTAT_BATCH_API_V1
WORDSTAT_BATCH_RESULT_V1
service = wordstat
actions = start | next | status | pause | resume | cancel
```

Important execution semantics:

```text
batch.start = 0 provider requests
batch.status/pause/resume/cancel = 0 provider requests
one explicit batch.next = at most 1 provider GetTop request
max phrases in one batch job = 500
numPhrases per item = 1..2000
regions = 1..100 values
maxRequests = 1..500
```

Current production acceptance proved durable per-item state, no replay on pause/resume, request/cost accounting and fail-closed `OUTCOME_UNKNOWN`.

## 9. Provider gate — exact execution parameters

```text
ACTIVE_SERVICE = wordstat
PROTOCOL = WORDSTAT_BATCH_API_V1
EXECUTION_MODE = durable batch / one explicit next per provider request
OPERATOR_MODE = AUTORUN recommended; Manual is also valid
PROJECT_JOB = BLOOD_SAND_GREENFIELD_2026-09-08
BATCH_JOB_ID = BLOOD_SAND_GREENFIELD_2026-09-08__STEP03_PRIMARY_V1
METHOD = getTop
REGION = ["225"]  # Russia
DEVICES = ["DEVICE_ALL"]
NUM_PHRASES = 2000
CURRENT_PRIMARY_SEEDS = 79
MAX_REQUESTS = 79
EXPECTED_DIRECT_YANDEX_COST = 1.58 RUB
BATCH_MAX_COST_RUB = 2.00
WORDSTAT_CALLS_BEFORE_STEP03 = 0
```

Why `numPhrases=2000`:

```text
- it is the provider maximum;
- billing is per GetTop request, not per returned phrase;
- reducing result depth would lower evidence coverage without reducing request count;
- if provider result still reaches its maximum/truncation boundary, preserve that limitation explicitly.
```

## 10. OR capability check before mass acquisition

The current V2 primary set contains 19 qualified probes with Wordstat OR syntax.

The source protocol accepts arbitrary phrase strings up to 400 characters, and official Yandex GetTop documentation states that `phrase` supports search operators. However the actual end-to-end Bridge/provider behavior for this exact grouped form has not been observed in this job.

Therefore the Step-03 execution order is deliberately changed without changing the 79-seed set:

```text
BATCH ITEM 1 = Q001 = (амулет|оберег|талисман) RSOTM
```

Only after Q001:

```text
provider result received
→ raw saved
→ readback
→ OR behavior accepted
```

may item 2 execute.

If Q001 is rejected because grouped OR is unsupported/invalid:

```text
STOP current batch
→ cancel without more provider traffic
→ replace every grouped Q probe deterministically with three child probes:
   амулет + name
   оберег + name
   талисман + name
→ preserve parent Q lineage
→ create revised Step-03 execution manifest
→ recompute request count/cost
```

No branch may be silently dropped.

## 11. Durable acquisition outputs

Per provider item, persist before the next provider call:

```text
STEP_03_WORDSTAT_RAW/<batch_order>__<seed_id>.json or .md
```

Each raw artifact must preserve the complete Bridge result envelope/provider payload.

Maintain:

`STEP_03_WORDSTAT_ACQUISITION_RECEIPTS.csv`

with at least:

```text
batch_order
seed_id
seed_phrase
batch_job_id
item_state
request_id
http_status
request_executed
results_rows
association_rows
total_count
raw_file
cost_estimate
remote_readback
notes
```

After all items are terminal, materialize complete occurrence tables with seed/request/region/device/role provenance. If the returned universe is large, this union/transformation is a ChatGPT Work task under `LEVEL1/WORK_HANDOFF_RULE.md`; do not sample or truncate it in ordinary chat.

## 12. Complete-payload / truncation boundary

For every GetTop response record:

```text
requested_numPhrases = 2000
results_rows
association_rows
totalCount
```

The Yandex API exposes no pagination parameter for GetTop beyond `numPhrases` up to 2000. Therefore Step 03 can promise complete preservation of the provider-returned payload, not an unlimited hidden universe beyond the provider maximum.

If a response reaches the provider depth boundary, mark that limitation rather than pretending exhaustive enumeration.

## 13. Stop conditions

Stop provider progression immediately on any of:

```text
OUTCOME_UNKNOWN
raw payload cannot be durably saved/read back
request/result provenance cannot be reconciled
OR capability failure on first item
provider quota/policy/cost stop
unexpected source/job mismatch
prohibited old Blood & Sand research contamination
```

No blind retry after uncertain provider outcome.

## 14. Step-03 PASS requirements

```text
ALL_AUTHORISED_EXECUTION_ITEMS_HAVE_TERMINAL_STATE = true
ALL_EXECUTED_PROVIDER_PAYLOADS_DURABLY_PRESERVED = true
RAW_RESULTS_SILENTLY_DROPPED = 0
ASSOCIATION_ROWS_SILENTLY_DROPPED = 0
REQUEST_ID_PROVENANCE_MISSING = 0
REGION_DEVICE_SEED_LINEAGE_MISSING = 0
OUTCOME_UNKNOWN_UNRESOLVED = 0
COMPLETE_OCCURRENCE_AUTHORITY_MATERIALIZED = true
REMOTE_GITHUB_READBACK = PASS
QUALITY_SCORING = performed under Level1 per-criterion 0–10 rule
```

Only then:

```text
STEP_03 = COMPLETE / PASS
NEXT_STEP_ALLOWED = true
NEXT_STEP = STEP_04_FIRST_FAMILY_TRIAGE
```

## ПРОСТЫМИ СЛОВАМИ

### Зачем нужен этот шаг

Чтобы перестать гадать, как люди ищут товары, и получить реальные формулировки и частотности из Яндекса.

### Что конкретно будем делать

Запускаем 79 проверенных стартовых запросов через Wordstat. Bridge выполняет их по одному. После каждого ответа сначала сохраняем всё, что вернул Яндекс, проверяем сохранение и только потом разрешаем следующий запрос.

Первым специально проверяем сложный OR-запрос. Если он работает — продолжаем. Если нет — не теряем эти темы, а раскладываем каждую на три обычных запроса.

### Что получим в конце

Полный сохранённый массив того, что реально вернул Wordstat по всем разрешённым направлениям, с частотностями и точной связью `какой seed → какой результат`. Только после этого можно переходить к первичному разбору спроса.
