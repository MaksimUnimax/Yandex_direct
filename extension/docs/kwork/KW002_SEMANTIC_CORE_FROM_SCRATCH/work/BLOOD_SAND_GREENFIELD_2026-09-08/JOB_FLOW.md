# KW-002 Blood & Sand — JOB FLOW

Status: **STEP 03 BLOCKED / BRIDGE MV3 >30S WORDSTAT FETCH DEFECT / REPAIR REQUIRED**

## Whole-job goal

```text
semantic core
→ user tasks / intent
→ Yandex-SERP-backed clusters
→ query→page ownership
→ Search-only site architecture
→ AI-search reconciliation
→ final IA / Page Jobs / internal-link model
→ client-ready deliverables
```

No prior Blood & Sand analytical research is an execution input before final freeze.

## Full roadmap / current status

| Step | Purpose | Status |
|---|---|---|
| 00 | Freeze order/scope/source boundary | ✅ COMPLETE / Ozon-only |
| 01 | Build factual business + complete assortment model | ✅ COMPLETE / PASS |
| 02 | Build seed/acquisition map | ✅ COMPLETE / V2 PASS / **93/100 = 9.3/10** |
| 03 | Primary Wordstat acquisition | 🔴 **BLOCKED — Bridge long-fetch transport defect** |
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
| 18 | Final semantic core + IA + Page Jobs | ⬜ NOT STARTED |
| 19 | Client deliverables | ⬜ NOT STARTED |
| 20 | Final QA / recipient acceptance | ⬜ NOT STARTED |
| 21 | Revision rehearsal + Kwork measurement | ⬜ NOT STARTED |
| 22 | Job close | ⬜ NOT STARTED |

## Completed work

```text
Step 00 scope/source freeze = PASS after Ozon-only correction
Step 01 Ozon 76-row factual assortment model = PASS
Step 01 main ChatGPT return QA = PASS
Step 02 V1 = 97 probes / 65/100 = 6.5/10 / SUPERSEDED
Step 02 external method audit = COMPLETE
Step 02 V2 primary manifest = 79
Step 02 V2 deferred/control = 49
Step 02 V2 QA = PASS / 93/100 = 9.3/10
Level-1 per-criterion 0–10 scoring rule = ACTIVE
Level-1 fresh internet research + clickable source disclosure = ACTIVE
Step 03 external-source disclosure = PASS
Step 03 pre-step/provider gate = COMPLETE
Step 03 execution manifest = 79 rows
Step 03 batch.start = PASS / 79 pending / 0 provider requests
Step 03 Q001 raw result = persisted + remote readback PASS
Step 03 S001 outcome-unknown raw result = persisted + remote readback PASS
Step 03 blocker investigation = COMPLETE / HIGH-CONFIDENCE ROOT CAUSE
Bridge repair handoff = MATERIALIZED
```

## Step-03 executed evidence

### Item 1 — Q001

```text
seed_id = Q001
phrase = (амулет|оберег|талисман) RSOTM
request_id = wordstat-batch-9292c032-e48e-443e-8576-a51ad4b2c8cc
HTTP = 200
item status = SUCCEEDED
request executed = true
elapsed = 1884 ms
provider result JSON = {}
cost = 0.02 RUB
```

Raw authority:

`STEP_03_WORDSTAT_RAW/001__Q001__wordstat-batch-9292c032-e48e-443e-8576-a51ad4b2c8cc.txt`

Interpretation boundary:

- grouped OR was accepted end-to-end (no syntax/provider error);
- `{}` is compatible with a zero-valued/empty ProtoJSON response because default-valued proto fields can be omitted;
- Yandex documentation reviewed does not explicitly state zero-result GetTop serializes as `{}`;
- raw evidence is not rewritten with synthetic fields.

### Item 2 — S001

```text
seed_id = S001
phrase = амулет
request_id = wordstat-batch-93be1f25-c5ff-4b43-a992-b286101d5c2a
item status = OUTCOME_UNKNOWN
reason = REQUEST_OUTCOME_UNKNOWN_NO_RETRY
result_ref = null
request_started_at = 2026-09-09T02:02:05.072Z
completed_at = 2026-09-09T02:02:35.728Z
observed duration = 30.656 s
cost ledger = 0.02 RUB
```

Raw authority:

`STEP_03_WORDSTAT_RAW/002__S001__OUTCOME_UNKNOWN__wordstat-batch-93be1f25-c5ff-4b43-a992-b286101d5c2a.txt`

## Blocking root cause

Official Chrome extension service-worker lifecycle states that Chrome terminates an extension service worker if a `fetch()` response takes more than 30 seconds to arrive:

https://developer.chrome.com/docs/extensions/develop/concepts/service-workers/lifecycle

Observed S001 duration was 30.656 seconds.

Observed runtime identifies Bridge `0.1.4`. A repository v0.1.4 authority exists at:

```text
branch = bridge/webmaster-readiness-gzip-v0.1.4
commit = 8bb1365a9905df8a6d7e09917e81444a9b7f1024
```

The inspected v0.1.4 source performs Wordstat via direct `await fetch(...)` in the MV3 service worker, and a thrown fetch is mapped to `REQUEST_OUTCOME_UNKNOWN_NO_RETRY`.

Current root-cause verdict:

```text
ROOT_CAUSE_CONFIDENCE = HIGH
SLOW WORDSTAT GETTOP (>30s)
+
DIRECT MV3 SERVICE-WORKER FETCH
→ CHROME FETCH-RESPONSE LIFETIME BOUNDARY
→ FETCH EXCEPTION / WORKER LOSS
→ OUTCOME_UNKNOWN
```

Current Yandex GetTop documentation reviewed contains no matching documented 30-second provider timeout.

Detailed authority:

`STEP_03_BRIDGE_MV3_30S_FETCH_BLOCKER_2026-09-09.md`

Bridge engineering handoff:

`extension/docs/WORDSTAT_MV3_LONG_FETCH_REPAIR_HANDOFF_2026-09-09.md`

## Provider/accounting truth

```text
WORDSTAT_BATCH_JOB = BLOOD_SAND_GREENFIELD_2026-09-08__STEP03_PRIMARY_V1
BRIDGE_RUNTIME_VERSION_OBSERVED = 0.1.4
BATCH_TOTAL = 79
PENDING = 77
SUCCEEDED = 1
OUTCOME_UNKNOWN = 1
TERMINAL = 2
REQUESTS_STARTED = 2
ESTIMATED_COST_RUB = 0.04
STOP_REASON = OUTCOME_UNKNOWN_REQUIRES_RECONCILIATION
NEXT_SAFE_ACTION = RECONCILE_UNKNOWN
THIRD_PROVIDER_REQUEST_ALLOWED = false
AUTO_RETRY_S001_ALLOWED = false
SEARCH_REQUESTS_STARTED = 0
AI_SEARCH_REQUESTS_STARTED = 0
```

## Why we do not reduce evidence depth as the default workaround

```text
lower numPhrases
!=
fix long-request transport
```

Reducing `numPhrases=2000` merely to fit a Bridge implementation limitation would reduce evidence coverage and leave the same architectural failure mode. It is not accepted as the default repair.

## Current authorities

```text
STEP_03_PRE_STEP_EXTERNAL_RESEARCH_AND_SOURCE_DISCLOSURE_2026-09-09.md
STEP_03_PRE_STEP_PROVIDER_GATE_2026-09-09.md
STEP_03_WORDSTAT_EXECUTION_MANIFEST_V1.csv
STEP_03_WORDSTAT_ACQUISITION_RECEIPTS.csv
STEP_03_Q001_EMPTY_PAYLOAD_INVESTIGATION_2026-09-09.md
STEP_03_BRIDGE_MV3_30S_FETCH_BLOCKER_2026-09-09.md
STEP_03_WORDSTAT_RAW/001__Q001__wordstat-batch-9292c032-e48e-443e-8576-a51ad4b2c8cc.txt
STEP_03_WORDSTAT_RAW/002__S001__OUTCOME_UNKNOWN__wordstat-batch-93be1f25-c5ff-4b43-a992-b286101d5c2a.txt
```

Upstream seed authority remains:

`STEP_02_PRIMARY_ACQUISITION_MANIFEST_V2.csv`

## Current exact action

```text
STEP_03_STARTED = true
STEP_03_COMPLETE = false
STEP_03_PROVIDER_PROGRESSION = BLOCKED
STEP_03_BLOCKER = BRIDGE_MV3_WORDSTAT_FETCH_GT_30S
STEP_03_THIRD_NEXT_ALLOWED = false
NEXT_STEP_ALLOWED = false
NEXT_ACTION = REPAIR_AND_ACCEPT_LONG_WORDSTAT_TRANSPORT_BEFORE_NEW_ACQUISITION_REVISION
```

After Bridge repair/acceptance, do not mutate this historical batch into success. Preserve it as the incident authority, reconcile/cancel it without replay, and start a new Step-03 acquisition revision with deliberate new request lineage.
