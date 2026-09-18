# KW-002 / BLOOD & SAND — STEP08 PRE-STEP EXTERNAL RESEARCH AND SOURCE TRACE

Date: 2026-09-18
Status: **PASS / MAIN CHAT PRE-STEP RESEARCH COMPLETE**
Step: `STEP08 — COMPETITOR-DERIVED WORDSTAT EXPANSION`
Prepared against live branch HEAD: `9933b714e09ecf22b5ff5891add036ea980c142d`

## 1. Exact Step08 question

Step08 does not ask whether competitor wording should become a production keyword.

It asks:

> Which genuinely new Step07 competitor-derived directions are already answered by durable KW-002 Yandex demand evidence, and which still require a new bounded Wordstat GetTop acquisition to test/expand current Yandex demand?

The current bounded Step07 handoff contains:

```text
STEP08_ELIGIBLE = 794
NEW_CANDIDATE = 787
POSSIBLE_VARIANT = 7
REGION = RUSSIA
LANGUAGE = RUSSIAN
SEARCH_ENGINE = YANDEX
RANKING_QUERY_SOURCE_LIMITATION = ACTIVE
```

`794` is an analysis universe, not a provider-call authorization count.

## 2. Fresh official Yandex research

### S08-S01 — Wordstat GetTop API reference

Source class: `OFFICIAL_PROVIDER`

URL:
https://aistudio.yandex.ru/ru/docs/search-api/api-ref/Wordstat/getTop

Checked: 2026-09-18.

Supports:

- GetTop returns last-30-day popular queries containing the supplied keyword plus similar queries;
- `phrase` max length = 400;
- `numPhrases` accepts 1..2000;
- up to 100 regions;
- up to 3 device types;
- response contains `totalCount`, `results[]`, `associations[]`;
- `DEVICE_ALL` is supported.

Project application:

- Step08 uses `getTop` for demand discovery/validation of justified competitor-derived seeds;
- the complete returned `results[]` and `associations[]` are RAW evidence and must be retained;
- a response at the 2000-result boundary is a provider-depth limitation, not semantic completeness.

Claim boundary:

Wordstat demand evidence does not prove client relevance, final intent, final cluster, page need or ranking.

### S08-S02 — Wordstat GetTop operation guide

Source class: `OFFICIAL_PROVIDER`

URL:
https://aistudio.yandex.ru/ru/docs/search-api/operations/wordstat-gettop

Checked: 2026-09-18.

Supports:

- request fields `phrase`, `numPhrases`, `regions`, `devices`, `folderId`;
- operators are supported in `phrase`;
- default response depth is 50, maximum is 2000;
- API-key/IAM authentication and folder identity are required.

Project application:

- current YMB schema must remain aligned to the provider fields before release;
- no provider call is valid merely because a command string was printed.

### S08-S03 — Wordstat operators

Source class: `OFFICIAL_YANDEX`

URL:
https://yandex.ru/support2/wordstat/ru/content/operators

Checked: 2026-09-18.

Supports current operators including:

```text
-
!
+
""
[]
()
|
```

Project application:

- Step08 must choose operator shape according to the information question;
- recall-first discovery must not automatically be converted into morphology-fixed precision testing;
- exact-form/order/word-count tests require explicit justification;
- no universal `always use !` or `never use !` rule is allowed.

### S08-S04 — Search API Wordstat quotas and limits

Source class: `OFFICIAL_PROVIDER`

URL:
https://aistudio.yandex.ru/ru/docs/search-api/concepts/limits

Checked: 2026-09-18.

Supports:

```text
WORDSTAT_REQUESTS_PER_SECOND = 10
WORDSTAT_REQUESTS_PER_HOUR = 100
MAX_ASSOCIATIONS = 20
```

Project application:

- provider execution must respect the current hourly/statistics quota;
- provider-ready seeds may require deterministic execution tranches;
- quota is an execution constraint, not a relevance or seed-selection rule.

The generic Search API result-limit row is not used to override the method-specific GetTop API reference, which explicitly allows `numPhrases` up to 2000.

### S08-S05 — Search API pricing

Source class: `OFFICIAL_PROVIDER`

URL:
https://aistudio.yandex.ru/ru/docs/search-api/pricing

Checked: 2026-09-18.

Current Russian-price table states:

```text
Wordstat GetTop = 20 RUB / 1000 requests, VAT included
```

Thus the direct provider estimate per successful GetTop request is approximately:

```text
0.02 RUB / request
```

Project application:

- cost is tracked;
- cost does not justify duplicate calls;
- within one justified GetTop request, using a deeper response limit does not increase the request count;
- final depth remains information-question dependent and is frozen only after candidate reconciliation.

### S08-S06 — Wordstat concept

Source class: `OFFICIAL_PROVIDER`

URL:
https://aistudio.yandex.ru/ru/docs/search-api/concepts/wordstat

Checked: 2026-09-18.

Supports:

- Wordstat provides Yandex query statistics;
- GetTop is the method for current popular queries around supplied words/phrases;
- Wordstat API operates synchronously;
- the current API methods are GetTop, GetDynamics, GetRegionsDistribution and GetRegionsTree.

Project application:

Step08 uses GetTop. Dynamics/RegionsDistribution are not added without a separate information-gain question.

## 3. Current Bridge capability recheck

Source class: `PROJECT_TEST_VALIDATED / CURRENT_REPOSITORY_CODE`

Current accepted production branch:

`hotfix/ymb-file-delivery-p0-2026-09-14`

Current pinned commit:

`b218afb0187bd26af1d7ada3590b02edc2d4a2de`

Fresh comparison on 2026-09-18:

```text
b218afb... vs hotfix/ymb-file-delivery-p0-2026-09-14 = IDENTICAL
```

Relevant current source identities:

```text
extension/src/shared/wordstat_protocol.js
git_blob = 07765acbca6bbb0d3535e170d0198ce8cfa7f2ae

extension/src/shared/wordstat_batch_protocol.js
git_blob = 2846a0bdfeba6a9241b5aced255ed44b06cffcad
```

Verified local contract:

```text
WORDSTAT_API_V1 -> WORDSTAT_RESULT_V1
WORDSTAT_BATCH_API_V1 -> WORDSTAT_BATCH_RESULT_V1

batch actions:
start | next | status | pause | resume | cancel

batch.start:
provider request = false
phrases max = 500
numPhrases = 1..2000
maxRequests = 1..500

batch.next:
at most one claimed provider GetTop item
automatic_retry = false
OUTCOME_UNKNOWN must not be blindly replayed
```

Step08 execution is NOT released by this research artifact.

## 4. KW-001 project-tested competitor-gap precedent

Source class: `PROJECT_TEST_VALIDATED`

Relevant KW-001 authorities:

- `KW001.../MK03_COMPETITOR_SEMANTIC_GAP/steps/STEP_04_COMPETITOR_DERIVED_SEEDS.md`
- `KW001.../MK03_COMPETITOR_SEMANTIC_GAP/steps/STEP_05_WORDSTAT_NORMALIZATION_SANITATION.md`
- `KW001.../MK03_COMPETITOR_SEMANTIC_GAP/tests/OKNO_MSK/MK03_PROVIDER_REUSE_RECEIPT_2026-09-11.json`
- `KW001.../MK03_COMPETITOR_SEMANTIC_GAP/tests/OKNO_MSK/MK03_ACQUISITION_FINAL_ACCOUNTING_2026-09-11.json`

The tested method states:

```text
COMPETITOR PAGE TOPIC
-> BOUNDED MISSED-DEMAND HYPOTHESIS
-> RECONCILE AGAINST EXISTING EVIDENCE
-> WORDSTAT ONLY FOR JUSTIFIED UNANSWERED SEEDS
-> RAW
-> NORMALIZE
-> SANITIZE
-> NEW | ALREADY_COVERED | REJECT | HOLD
```

KW-001 explicitly rejected:

- one provider seed per heading/SKU/lexical variant;
- competitor wording as accepted keyword;
- provider acquisition without novelty/information gain.

Observed KW-001 Phase-5 execution:

```text
COMPETITOR_DERIVED_OCCURRENCES = 92
DEDUPLICATED_DIRECTIONS = 43
WORDSTAT_SEED_ACQUISITIONS_REUSED = 14
WORDSTAT_ROWS_RECONCILED = 160
NEW_PROVIDER_CALLS = 0
SILENT_DROPS = 0
```

This is project evidence that competitor-gap validation can be reuse-first rather than call-per-candidate.

## 5. Source-to-method decisions for Step08

| Method element | Source basis | Step08 decision | Claim boundary |
|---|---|---|---|
| Use Yandex demand evidence | Official Wordstat docs | GetTop is the demand acquisition method for unanswered seeds | demand != final SEO decision |
| 794 eligible candidates | current Step07 authority | process 794/794 in preparation | 794 != 794 provider calls |
| Reuse first | inherited KW-001 + KW002 Level1 + KW001 MK03 tested execution | reconcile every candidate against durable existing evidence before provider release | broad evidence cannot close narrower qualified question |
| Seed design | KW001 MK03 + info-gain rule | create bounded acquisition seeds, not one request per page phrase/SKU | seed != keyword |
| Operator shape | official operators + project gate | classify recall-first vs precision/exact before operator choice | no universal operator shortcut |
| Depth | official GetTop + depth gate | candidate/group-specific depth decision after reconciliation; 2000 may be selected where recall-first coverage justifies it | maximum depth != semantic completeness |
| Region | frozen Step00 | Russia / region 225 | not a global-demand claim |
| Device | current job/provider convention | DEVICE_ALL unless a later evidence question needs a device split | device split not inferred |
| Provider cost | official pricing | approx. 0.02 RUB per GetTop request at current tariff | price does not define relevance |
| Quota | official limits | max 100 Wordstat statistics requests/hour under current quota | quota does not justify dropping valid seeds |
| RAW persistence | KW002 persistence gate | complete envelope/results/associations/errors before next provider call | chat is not evidence storage |
| New provider rows | KW002 sanitation rules | 03A-compatible normalization + 03B-compatible sanitation before union | RAW != accepted semantic row |
| Large-data preparation | Work rule | 794-row plus large prior-evidence reconciliation goes to Work full-volume | no sampling/truncation |

## 6. Research verdict

```text
PRE_STEP_EXTERNAL_RESEARCH = PASS
CURRENT_PROVIDER_METHOD_RECHECK = PASS
CURRENT_LIMITS_RECHECK = PASS
CURRENT_PRICE_RECHECK = PASS
CURRENT_BRIDGE_PROTOCOL_RECHECK = PASS
KW001_PROJECT_PRECEDENT_RECHECK = PASS
SOURCE_TO_METHOD_TRACE = PASS
WORDSTAT_PROVIDER_EXECUTION_RELEASED = false
```

Next allowed action:

`STEP08_FULL_VOLUME_PRE_ACQUISITION_RECONCILIATION_IN_WORK`
