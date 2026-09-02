# OKNO_MSK — STEP 16 OWNER-FACING PRE-STEP GATE REISSUED

Date: 2026-09-02  
Status: **COMPLETE / OWNER-FACING GATE REISSUED / PROVIDER EXECUTION NOT AUTHORIZED**

## A. Whole Kwork goal — plain language

Deliver an evidence-backed site/page structure for ordinary Yandex Search plus selective AI-search evidence, then produce understandable client-ready recommendations, final QA, handoff/revision and job close without claiming more than the evidence proves.

## B. Full Kwork roadmap with current progress

| Step | Plain-language purpose | Status |
|---|---|---|
| 0 | Freeze order, region, business and scope | ✅ COMPLETE |
| 1 | Understand the current site and real public pages | ✅ COMPLETE |
| 2 | Prepare the initial demand-acquisition plan | ✅ COMPLETE |
| 3 / 3R | Acquire Wordstat and repair incomplete persistence | ✅ COMPLETE |
| 4 | Separate obvious noise and unresolved demand families | ✅ COMPLETE |
| 5 | Acquire missing targeted demand directions | ✅ COMPLETE |
| 6 / 6A | Preserve seasonality context and revalidate acquisition coverage | ✅ COMPLETE |
| 7 | Perform row-level semantic cleanup | ✅ COMPLETE |
| 8 | Freeze the Search-stage phrase universe | ✅ COMPLETE |
| 9 | Observe ordinary Yandex Search results | ✅ COMPLETE |
| 10 | Group queries by real user task | ✅ COMPLETE |
| 11 | Decide which existing page should answer each task and materialize phrase→page mapping | ✅ COMPLETE |
| 12 | Decide structural actions and routing/content changes | ✅ COMPLETE |
| 13 | Diagnose related/competing pages without inventing historical harm | ✅ COMPLETE |
| 14 / 14A | Freeze Search-only architecture and reconcile it against the current site/topology | ✅ COMPLETE |
| 15 | Select only useful AI-test cases plus stability controls | ✅ COMPLETE |
| 16 | Acquire and preserve AI-search evidence for the 8 frozen cases | 🟡 CURRENT |
| 17 | Compare ordinary Search and AI evidence and decide material implications | ⬜ NOT STARTED |
| 18 | Prioritize actions | ⬜ NOT STARTED |
| 19 | Produce client deliverables | ⬜ NOT STARTED |
| 20 | Final QA of claims, URLs, counts and limitations | ⬜ NOT STARTED |
| 21 | Handoff and revisions | ⬜ NOT STARTED |
| 22 | Close job and workspace | ⬜ NOT STARTED |

## C. Completed work

Verified complete:

```text
Steps 0–13
Step 14 / 14A FINAL PASS
Step 15 V2 FINAL PASS
25 Step-15 candidates reviewed
8 selected = 6 DIAGNOSTIC_PROBE + 2 STABILITY_CONTROL
Step16 provider calls executed = 0
Step16 provider cost incurred = 0.0 RUB
```

## D. Remaining work

```text
Step 16 provider acquisition + persistence + QA
Step 17 Search-vs-AI comparison
Step 18 prioritization
Step 19 client deliverables
Step 20 final QA
Step 21 handoff/revisions
Step 22 close
```

## E. Current Step-16 goal

Obtain one complete reproducible official Yandex GenSearch observation for each of the eight frozen Step-15 V2 cases, preserve it durably, and classify whether the observation supports the current Search-only decision, de-risks it, creates a material change/control-break candidate, or is insufficient.

Step 16 does not perform the final architecture comparison/change; Step 17 owns that decision.

## F. What Step 16 solves

The current architecture is evidence-backed for ordinary Yandex Search. The remaining uncertainty is whether a selected set of difficult and stable user tasks is materially interpreted differently by the official generative Search surface.

Step 16 closes the evidence-acquisition uncertainty without hindsight rewriting of the Search baseline.

## G. Required Step-16 output

At completion the job must contain:

```text
8/8 initial cases accounted;
complete raw GenSearch result for every useful executed interaction;
GitHub write + readback + completeness QA after every useful interaction;
normalized observation per case;
full message/sources/searchQueries and relevant response/transport fields;
exact GenSearch provenance;
initial outcome per case;
required confirmation observation for every material CHANGE_CANDIDATE / CONTROL_BREAK_CANDIDATE;
explicit INSUFFICIENT where evidence cannot discriminate the preregistered boundary;
provider-call/cost/retry accounting;
final observation ledger;
independent QA;
Step16 report/current-state;
Step17 handoff with no Step17 architecture action executed inside Step16.
```

## Relevant prior errors / corrections

### P16-01 — technical provider success was treated as project completion in earlier provider work

Root cause: API/workflow status was allowed to substitute for complete durable evidence.

Non-repeat control:

```text
USEFUL PROVIDER RESULT
-> COMPLETE GITHUB RAW WRITE
-> READBACK + COMPLETENESS/ACCOUNTING QA
-> NORMALIZED OBSERVATION WRITE + READBACK
-> ONLY THEN ANALYSIS OR NEXT PAID ACTION
```

### P16-02 — Step15 V1 candidate-lineage drift

Root cause: manual reconstruction of QF metadata instead of exact authoritative joins.

Non-repeat control: Step16 accepts only the exact V2 case IDs and exact `authoritative_query` strings from `STEP_15_SELECTED_CASES_V2.tsv`. V1 is forbidden as execution input.

### P16-03 — GenSearch provenance can be overclaimed as consumer Alice

Non-repeat control:

```text
GEN_SEARCH_* != CONSUMER_ALICE_*
GEN_SEARCH_QUERY_OBSERVED != ALICE_FANOUT_OBSERVED
```

### P16-04 — one material generative observation can be overgeneralized

Non-repeat control: initial material result is only `CHANGE_CANDIDATE` / `CONTROL_BREAK_CANDIDATE`; one additional same-exact-query observation is required before Step17 may receive it as a confirmed material direction. This is a bounded project-specific risk control, not a statistical or Yandex standard.

### P16-05 — unsupported source-order semantics

Official GenSearch exposes `sources[].url/title/used` but does not define array order as ranking/importance. Step16 preserves source order raw but never interprets position as source rank. Step15 wording such as `used-source hierarchy` is operationalized in Step16 as source role/specificity + `used=true/false`, not array-order ranking.

### P16-06 — owner-facing goal/roadmap/plain-language gate was originally executed in the wrong order

Root cause: technical/research gates were treated as sufficient and method research began before the full owner-facing goal/roadmap/status block.

Non-repeat control: this document and the live chat reissue restore the required order before any provider authorization or execution.

## Input evidence

Canonical input: `STEP_15_SELECTED_CASES_V2.tsv` only.

Exact selected cases:

```text
C15-004  DIAGNOSTIC_PROBE   панорамные алюминиевые окна
C15-006  DIAGNOSTIC_PROBE   алюминиевые окна для веранды
C15-007  STABILITY_CONTROL  панорамное остекление балкона
C15-010  DIAGNOSTIC_PROBE   установка подоконника на пластиковые окна
C15-013  DIAGNOSTIC_PROBE   французские панорамные окна
C15-018  STABILITY_CONTROL  замена окна на пластиковое цена москва
C15-019  DIAGNOSTIC_PROBE   как открыть пластиковое окно
C15-020  DIAGNOSTIC_PROBE   лучшие пластиковые окна
```

Claim boundary: `DECISION_DIAGNOSTIC_SET_WITH_STABILITY_CONTROLS`, not a representative sample of site demand.

## Yandex Webmaster access check

```text
CURRENT ACCESS STATE = UNAVAILABLE
WHY IT CAN HELP = owned Webmaster Alice-AI visibility/examples/SoV could provide separate first-party owned evidence
BASE PATH WITHOUT ACCESS = official GenSearch
ENHANCED PATH WITH ACCESS = preserve owned Webmaster Alice evidence separately and compare without relabeling it as GenSearch
FIRST-ACCESS COMPARISON STATE = NOT_YET_RUN / NOT_THIS_JOB
```

Absence of Webmaster access does not block the base job.

## Method origin and current direct sources

Freshness checked: 2026-09-02.

OFFICIAL / PRIMARY:

- Yandex AI Studio — GenSearch/generative response concept: `https://aistudio.yandex.ru/en/docs/search-api/concepts/generative-response`
- Yandex AI Studio — GenSearch REST response fields: `https://aistudio.yandex.ru/ru/docs/search-api/api-ref/GenSearch/search`
- Yandex AI Studio — Search API quotas/limits: `https://aistudio.yandex.ru/en/docs/search-api/concepts/limits`
- Yandex AI Studio — pricing: `https://aistudio.yandex.ru/ru/docs/search-api/pricing`
- Yandex Webmaster — Alice AI visibility: `https://yandex.ru/support/webmaster/ru/service/alice-answers`
- Yandex Webmaster — how Alice AI responses are formed: `https://www.yandex.ru/support/webmaster/ru/alice`

EXTERNAL RISK/EVALUATION CONTEXT:

- NIST AI RMF Measure: `https://airc.nist.gov/airmf-resources/airmf/5-sec-core/`

PROJECT TEST / OWNER RULES:

- `BRIDGE_EVIDENCE_PERSISTENCE_GATE.md`
- `CLIENT_PRIVATE_YANDEX_ACCESS_POLICY.md`
- `RESEARCH_TO_EXECUTION_SCHEMA_GATE.md`
- `SOURCE_TO_METHOD_TRACEABILITY_GATE.md`
- `STEP_15_AI_CASE_SELECTION_METHOD.md`

Current review verdict: `PROJECT_SPECIFIC_BUT_REASONED`.

## What the current sources support

```text
GenSearch is an official synchronous Yandex Search API generative surface.
Without site/host/url restriction it can search the whole Yandex search index.
The response exposes message, sources with used flag, refined searchQueries and answer-status fields.
Source-array position is not documented as a ranking signal.
Current published GenSearch quota = 1 request/sec and 1000/hour.
Current RUB price = 5080 RUB / 1000 synchronous generative requests = 5.08 RUB/request.
Owned Webmaster Alice visibility is a distinct optional first-party surface requiring verified site access.
Yandex documents that consumer Alice-AI answer/source composition can vary over time; this supports caution but is not direct proof of identical GenSearch variability.
NIST supports documenting test conditions, uncertainty and reliability; it does not prescribe the exact KW001 confirmation count.
```

## What is project-specific

```text
8-case selected diagnostic/control set;
initial outcome taxonomy;
one additional same-query observation for a material candidate;
not confirming ordinary NO_CHANGE/DE_RISK cases;
Step16/17 split of acquisition vs architecture decision;
normalized observation schema;
GitHub file naming and QA mechanics.
```

These are bounded job/project controls, not Yandex or industry standards.

## Practical Step-16 procedure

1. Execute cases sequentially in frozen order, beginning C15-004.
2. Use exact `authoritative_query` only; no paraphrase, prompt expansion or baseline hint.
3. Command surface: `SEARCH_API_V1 method=genSearch confirmBillable=true`.
4. After delivery determine provider-execution truth and usable-evidence state.
5. Persist complete useful raw result to GitHub immediately.
6. Read it back and reconcile case/query/message/sources/searchQueries/transport/accounting fields.
7. Write and read back normalized observation.
8. Compare persisted evidence only against the preregistered Step15 condition.
9. Initial allowed outcomes: `CHANGE_CANDIDATE`, `CONTROL_BREAK_CANDIDATE`, `DE_RISK`, `NO_CHANGE`, `INSUFFICIENT`.
10. Material candidate -> one separately authorized/covered same-query confirmation observation after initial evidence is durably persisted/read back.
11. Confirmation compares material direction, not text identity.
12. No usable result / OUTCOME_UNKNOWN -> governed retry rule, up to 3 additional retries after original, mandatory pre-retry chat disclosure and separate cost accounting.
13. No Step17 architecture change is executed in Step16.

## Provider plan / cost boundary

```text
initial calls = 8
unit cost = 5.08 RUB
base planned cost = 40.64 RUB

conditional semantic confirmations:
max count = 8
max incremental cost = 40.64 RUB
status = NOT AUTHORIZED

no-usable/OUTCOME_UNKNOWN retries:
max additional retries after each original = 3
announce exact query + retry ordinal + reason + incremental cost before each retry
```

The pathological theoretical envelope is not the planned spend.

## Adversarial self-audit findings

1. The selected set is intentionally diagnostic + controls and cannot support prevalence claims.
2. GenSearch is not consumer Alice; provenance separation is mandatory.
3. Consumer-Alice temporal variability cannot be silently generalized as an exact GenSearch native property.
4. `sources[].used` is provider evidence; `sources[]` order is not documented ranking.
5. A successful sparse response may be analytically insufficient.
6. One confirmation is only a bounded reproduction check, not long-term stability proof.
7. Confirmation is asymmetric: material architecture-changing candidates are rechecked; ordinary NO_CHANGE/DE_RISK is not repeated merely to increase sample count.
8. Step16 cannot change architecture; Step17 owns comparison/decision.
9. Existing Bridge v0.1.4 capability is sufficient; no new engineering is justified for the current acceptance goal.
10. The original owner-communication ordering defect has been explicitly corrected before provider authorization/execution.

## Risks / uncertainties

```text
generative observations are dated snapshots;
provider response may be sparse/non-discriminative;
consumer Alice and GenSearch are distinct surfaces;
current job lacks owned Webmaster Alice visibility;
selected cases do not estimate site-wide prevalence;
one confirmation cannot establish statistical or long-term stability;
future Yandex model/search changes can alter observations.
```

## What Step16 will not do

```text
no page ownership rewrite;
no merge/split/create/delete decision;
no prioritization;
no client-final recommendation;
no consumer-Alice equivalence claim;
no source-array ranking claim;
no site-wide prevalence claim;
no new Webmaster access requirement;
no new Bridge engineering without a newly proven capability gap.
```

## Proposed pass gate

```text
INPUT_SELECTED_CASES = 8/8
INITIAL_CASES_ACCOUNTED = 8/8
SILENT_CASE_DROPS = 0
USEFUL_RAW_RESULTS_PERSISTED_READBACK = 100%
NORMALIZED_OBSERVATIONS = 8/8
GENSEARCH_PROVENANCE_VIOLATIONS = 0
SOURCE_ORDER_RANKING_INFERENCES = 0
PREREGISTERED_CONDITION_USED = 8/8
MATERIAL_DELTA_WITHOUT_REQUIRED_CONFIRMATION = 0
SILENT_UNKNOWN_AS_EVIDENCE = 0
RETRY_ANNOUNCEMENT_VIOLATIONS = 0
PROVIDER_CALLS_RECONCILED = 100%
PROVIDER_COST_RECONCILED = 100%
CLAIMS_EXCEEDING_EVIDENCE_MODE = 0
STEP17_ARCHITECTURE_DECISIONS_EXECUTED_IN_STEP16 = 0
FINAL_GITHUB_READBACK = PASS
```

## Plain-language pre-step summary

### Зачем нужен этот шаг?

Мы уже решили, какие страницы должны отвечать на запросы в обычном Яндексе. Теперь проверяем восемь специально выбранных ситуаций, чтобы увидеть, не понимает ли AI эти вопросы заметно иначе.

### Что конкретно будем делать?

Зададим Яндексу ровно восемь заранее выбранных запросов. После каждого ответа полностью сохраним ответ, использованные источники и дополнительные поисковые формулировки. Сравнивать будем с заранее записанными условиями, а не придумывать критерии после ответа. Необычный материальный результат перепроверим тем же запросом до передачи в следующий шаг.

### Что получим в конце?

Получим восемь проверенных AI-наблюдений: где AI подтверждает нашу текущую структуру, где делает её надёжнее, где действительно появляется повод пересмотреть решение и где данных недостаточно. Только после этого Step17 будет решать, требуется ли изменение архитектуры.

## Authorization boundary

```text
OWNER_FACING_GATE_REISSUED = true
OWNER_PROVIDER_AUTHORIZATION_READY = true
STEP16_INITIAL_PROVIDER_CALLS_AUTHORIZED = false
STEP16_CONFIRMATION_PROVIDER_CALLS_AUTHORIZED = false
STEP16_PROVIDER_CALLS_EXECUTED = 0
STEP16_PROVIDER_COST_INCURRED_RUB = 0.0
```

Next legal action after GitHub readback: explicit owner provider authorization. No GenSearch command before that authorization.