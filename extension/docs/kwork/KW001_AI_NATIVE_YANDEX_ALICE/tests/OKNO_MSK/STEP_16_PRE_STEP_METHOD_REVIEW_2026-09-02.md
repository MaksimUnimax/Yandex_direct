# OKNO_MSK — STEP 16 PRE-STEP METHOD / EVIDENCE REVIEW

Date: 2026-09-02  
Status: **PRE-STEP RESEARCH COMPLETE / PROJECT-SPECIFIC METHOD READY FOR OWNER REVIEW / PROVIDER EXECUTION NOT AUTHORIZED**

## 1. Whole KW-001 goal

Deliver a complete evidence-backed semantic and page architecture for ordinary Yandex Search plus selective AI-search evidence, then produce prioritized client-ready deliverables without overstating what any provider surface proves.

## 2. Current roadmap state

```text
Steps 0–13 = COMPLETE
Step 14 / 14A = FINAL PASS
Step 15 V2 = FINAL PASS
Step 16 = PRE-STEP PREPARED / PROVIDER EXECUTION NOT STARTED
Steps 17–22 = NOT STARTED
```

Current Step-15 authority:

```text
STEP_15_SELECTED_CASES_V2.tsv
STEP_15_CURRENT_STATE.json
JOB_FLOW_STEP15_EXECUTION_SYNC_2026-09-02.md
../../STEP_15_AI_CASE_SELECTION_METHOD.md
```

Step 15 selected exactly eight Step-16 cases:

```text
C15-004  DIAGNOSTIC_PROBE    панорамные алюминиевые окна
C15-006  DIAGNOSTIC_PROBE    алюминиевые окна для веранды
C15-007  STABILITY_CONTROL   панорамное остекление балкона
C15-010  DIAGNOSTIC_PROBE    установка подоконника на пластиковые окна
C15-013  DIAGNOSTIC_PROBE    французские панорамные окна
C15-018  STABILITY_CONTROL   замена окна на пластиковое цена москва
C15-019  DIAGNOSTIC_PROBE    как открыть пластиковое окно
C15-020  DIAGNOSTIC_PROBE    лучшие пластиковые окна
```

The selected set remains:

```text
DECISION_DIAGNOSTIC_SET_WITH_STABILITY_CONTROLS
REPRESENTATIVE_SAMPLE = false
PREVALENCE_CLAIMS_AUTHORIZED = false
```

## 3. Current Step-16 goal

Acquire a complete, reproducible official Yandex GenSearch observation for every selected case and materialize it into evidence that Step 17 can compare against the already frozen ordinary-Search baseline.

Step 16 answers:

```text
WHAT DID THE CURRENT OFFICIAL GENSEARCH SURFACE OBSERVE / GENERATE FOR EACH FROZEN QUERY?
DOES THAT OBSERVATION SUPPORT NO_CHANGE / DE_RISK OR CREATE A MATERIAL CHANGE/control-break candidate?
IS A MATERIAL DELTA REPRODUCED BY A SEPARATE CONFIRMATION OBSERVATION?
```

Step 16 does **not** make final page-architecture changes.

## 4. Exact required output

At Step-16 completion the job must contain:

```text
1. complete raw Bridge/GenSearch result for every executed provider interaction;
2. one normalized observation record for every selected case;
3. all returned message/sources/searchQueries and transport metadata preserved;
4. exact provenance labels separating GenSearch from consumer Alice / Webmaster Alice visibility;
5. initial outcome for all 8 cases;
6. confirmation evidence for every material CHANGE_CANDIDATE / CONTROL_BREAK_CANDIDATE if the owner authorizes the conditional confirmation branch;
7. explicit INSUFFICIENT state for cases that do not produce discriminative usable evidence;
8. exact request/cost/retry accounting;
9. final 8-case observation ledger;
10. independent/reconciliation QA;
11. Step-16 final report and current-state record;
12. Step-17 handoff with no automatic architecture rewrite.
```

## 5. Relevant prior errors / corrections

### E16-01 — provider technical success was previously confused with project evidence completion

Relevant permanent lesson from the Wordstat/Search acquisition history:

```text
HTTP 200 / status OK / request_executed=true
!=
COMPLETE PROJECT EVIDENCE
```

**Non-repeat control:** after every useful GenSearch interaction, save the complete evidence to GitHub, read it back, reconcile required fields/counts, and only then analyze it or send the next paid provider command.

### E16-02 — research was previously collected without being operationalized

Step-13 exposed `RESEARCH_TO_EXECUTION_SCHEMA_GAP`.

**Non-repeat control:** every material Step-16 research finding receives a requirement ID, executable action/output, claim boundary, QA and acceptance check in `STEP_16_RESEARCH_TO_EXECUTION_SCHEMA_2026-09-02.json`.

### E16-03 — GenSearch must not be relabeled as consumer Alice

Project validation established:

```text
GEN_SEARCH_QUERY_OBSERVED != ALICE_FANOUT_OBSERVED
GEN_SEARCH_ANSWER != CONSUMER_ALICE_ANSWER
GEN_SEARCH_SOURCE != CONSUMER_ALICE_SOURCE
```

**Non-repeat control:** every saved observation uses GenSearch-specific provenance only.

### E16-04 — Step-15 V1 lineage drift

V1 manually reconstructed upstream metadata and was superseded.

**Non-repeat control:** Step 16 accepts only the exact eight V2 rows and exact `authoritative_query` strings from `STEP_15_SELECTED_CASES_V2.tsv`. No manual paraphrase is permitted.

### E16-05 — a single AI delta must not automatically rewrite architecture

Step-15 permanent correction pre-registered `confirmation_required_if_material_delta=true` for all eight cases.

**Non-repeat control:** initial material deltas are only `CHANGE_CANDIDATE` / `CONTROL_BREAK_CANDIDATE`; architecture-changing evidence is handed forward only after a separately persisted confirmation observation reproduces the same material direction. A non-reproduced delta becomes `MATERIAL_DELTA_NOT_REPRODUCED`, not a change instruction.

### E16-06 — unsupported source-order semantics

The current official GenSearch API schema exposes `sources[].url`, `sources[].title`, and `sources[].used`, but does not define the array position as a ranking signal.

**Non-repeat control:** Step 16 may classify source role/specificity and whether `used=true`, but must not interpret source list order as rank, importance score or consumer-visible citation order.

## 6. Current Bridge capability state

Current capability authority:

```text
BRIDGE_BRANCH = bridge/webmaster-readiness-gzip-v0.1.4
BRIDGE_HEAD = 8bb1365a9905df8a6d7e09917e81444a9b7f1024
BRIDGE_VERSION = 0.1.4
FULL_GATE_RUN = 33491679086
FULL_GATE_CONCLUSION = success
```

GenSearch contract in the current source:

```text
service = search
prefix = SEARCH_API_V1
method = genSearch
endpoint = POST /v2/gen/search
allowed command fields = method, queryText, confirmBillable
confirmBillable must equal true
Bridge queryText bound = <=400 Unicode characters / <=40 words
provider request uses getPartialResults=false
```

The current Bridge preserves:

```text
message.content
message.role
sources[].url
sources[].title
sources[].used
searchQueries[].text
searchQueries[].reqId
fixedMisspellQuery
isAnswerRejected
isBulletAnswer
hints[]
problematicAnswer
transport.wire_format
transport.frame_count
request_id
http_status
request_executed
automatic_retry
cost_estimate
```

There is no Step-16 need for new Bridge engineering.

The public provider API currently exposes additional scope/rich-answer options that the Bridge's bounded production command does not expose. Those options are not required by this job's Step-16 acceptance goal. The current selected questions intentionally test the open-web AI-search surface, so no capability-gap implementation is justified before execution.

## 7. Access state / evidence mode

Current job access state is already established:

```text
YANDEX_WEBMASTER_ACCESS_STATE = UNAVAILABLE
YANDEX_WEBMASTER_PRIVATE_EVIDENCE_USED = false
BASE_PUBLIC_EVIDENCE_MODE = true
```

Therefore:

```text
BASE_REQUIRED AI ROUTE = official GenSearch
OWNED_WEBMASTER_ALICE_VISIBILITY = OPTIONAL_ENHANCEMENT / UNAVAILABLE / NOT EXECUTED
```

No claim may imply that OKNO_MSK owned Alice visibility, Share of Voice, historical Alice source examples or private Webmaster AI evidence was observed.

## 8. Current external research — direct authorities

Research checked: 2026-09-02.

### Yandex AI Studio — generative response concept

https://aistudio.yandex.ru/en/docs/search-api/concepts/generative-response

Supports:

```text
GenSearch = official Yandex Search API generative response surface;
full response can be requested synchronously;
without site/host/url restriction, search runs across the Yandex search index;
response may legitimately omit fields when no relevant data exists;
no relevant documents / extraction uncertainty are valid special cases rather than automatic analytical evidence.
```

### Yandex AI Studio — GenSearch REST reference

https://aistudio.yandex.ru/ru/docs/search-api/api-ref/GenSearch/search

Supports exact response observables:

```text
message
sources[].url/title/used
searchQueries[].text/reqId
fixedMisspellQuery
isAnswerRejected
isBulletAnswer
hints[]
problematicAnswer
```

The API reference says `searchQueries[]` are queries refined by the YandexGPT model and used for the generative response. It does not define `sources[]` list order as ranking.

### Yandex AI Studio — quotas and limits

https://aistudio.yandex.ru/en/docs/search-api/concepts/limits

Current published limits include:

```text
generative response requests per second = 1
generative response requests per hour = 1000
maximum request length = 400 characters
maximum request words = 40
```

Step 16 will be sequential and therefore does not need concurrency.

### Yandex AI Studio — pricing

https://aistudio.yandex.ru/ru/docs/search-api/pricing

Current published RUB price:

```text
5080 RUB / 1000 synchronous generative-response requests
= 5.08 RUB / request
```

Base eight-request cost:

```text
8 * 5.08 = 40.64 RUB
```

### Yandex Webmaster — Search with Alice

https://yandex.ru/support/webmaster/en/alice

Supports only the consumer Search-with-Alice context: generated answers are assembled from content selected from Yandex Search and contain source links. It does **not** authorize equivalence to GenSearch.

### Yandex Webmaster — Site visibility in Alice AI

https://yandex.ru/support/webmaster/ru/service/alice-answers

Supports:

```text
owned Alice visibility requires a verified Webmaster site;
data covers the last 3 months and is updated weekly;
query/page examples are an owned/private analytical surface;
Alice AI builds a new answer from current search evidence and answer/source composition may differ over time.
```

For OKNO_MSK this source defines the unavailable optional enhancement and the claim boundary; it is not an executed evidence route.

### NIST AI RMF — Measure

https://airc.nist.gov/airmf-resources/airmf/5-sec-core/

Supports documenting test conditions, uncertainty, reliability, limitations and monitoring/measurement rather than treating one AI observation as universally stable truth.

NIST does not prescribe the exact KW-001 confirmation count. The one-confirmation rule below is explicitly project-specific.

## 9. Source-to-method trace

| Method element | Source / evidence | What it supports | Project-specific part | Executable action/output |
|---|---|---|---|---|
| Use official GenSearch for base Step 16 | Yandex GenSearch docs + current access policy | Official generative Search API exists; private access is unavailable but not base-required | Selected 8-case base mode | Send exact `SEARCH_API_V1 method=genSearch` command per selected query |
| Preserve full response observables | GenSearch API reference + Bridge source | Exact available response fields | Add case/provenance metadata | Raw JSON + normalized observation record |
| `INSUFFICIENT` is a valid outcome | GenSearch generative-response special cases | Response fields may be absent / no relevant information may be available | Map non-discriminative successful evidence to job state | `evidence_usability=INSUFFICIENT` |
| Do not infer source ranking from array order | Official API defines `used` but no rank semantics + source-to-method gate | Unsupported rank inference is not authorized | Evaluate roles/specificity only | Preserve source order as raw data but do not score by position |
| Search full index | GenSearch docs + current Bridge command contract | No scope fields means provider searches unrestricted index | Desired for competitor/source landscape | No site/host/url restriction added |
| Sequential execution | Yandex quota + persistence gate | <=1 GenSearch request/sec; durable write required between paid actions | Manual one-command execution simplifies gate | One provider interaction at a time |
| Base cost 5.08 RUB/request | Yandex current pricing | Current unit price | Eight frozen initial cases | Planned 8 / 40.64 RUB |
| Material delta requires confirmation | Step-15 V2 + NIST uncertainty/reliability context | Material AI evidence should not be overgeneralized from one observation | One same-query confirmation is a KW-001 risk-control heuristic, not Yandex standard | Initial delta -> confirmation gate |
| Do not confirm ordinary NO_CHANGE/DE_RISK | Step-15 change-risk boundary + provider information-gain policy | Confirmation is needed before architecture-changing interpretation, not to inflate sample count | Cost/time-efficient asymmetric risk control | Finalize non-material outcome after persisted initial observation |
| No-usable / OUTCOME_UNKNOWN retry | BRIDGE_EVIDENCE_PERSISTENCE_GATE.md owner rule | Up to 3 additional retries after original unusable/unknown result, with disclosure | Same exact question; retries are not semantic confirmation | Announce retry N/3, execute, persist if useful |
| Preserve GenSearch provenance | GenSearch proxy validation + production contract | GenSearch is useful but not consumer Alice equivalent | All observation fields use `GEN_SEARCH_*` labels | No consumer-Alice claims |
| Private Alice evidence unavailable | Client-private access policy + current job state + Webmaster docs | Owned surface requires access/verification | Base mode continues | Optional route explicitly SKIPPED/UNAVAILABLE |
| Step 16 does not change architecture | Step-15 V2 confirmation handoff + roadmap boundary | Acquisition precedes Search-vs-AI comparison | Step 17 owns comparison/decision | Step16 output is evidence + classified handoff only |

## 10. Practical execution method

### Phase A — freeze inputs

Use only `STEP_15_SELECTED_CASES_V2.tsv`.

For every case preserve without rewriting:

```text
case_id
case_role
query_family_id
authoritative_query
primary_owner
supporting_or_other_url
pre_ai_baseline
evaluation_purpose
change_or_control_break_condition
de_risk_condition
no_change_condition
insufficient_condition
confirmation_required_if_material_delta
```

### Phase B — initial observations

For each of the eight cases, one at a time:

```text
SEARCH_API_V1 {"method":"genSearch","queryText":"<EXACT authoritative_query>","confirmBillable":true}
```

No paraphrase, prompt expansion, site restriction, answer-leading instruction or Search-baseline hint is added to the provider query.

After delivery:

```text
1. determine request_executed / outcome truth;
2. preserve complete raw result in GitHub;
3. read back saved result;
4. verify full message/sources/searchQueries + transport metadata are preserved as returned;
5. create normalized case observation;
6. only then classify the current observation and consider another paid provider action.
```

### Phase C — observation interpretation

Initial Step-16 outcome taxonomy:

```text
CHANGE_CANDIDATE
CONTROL_BREAK_CANDIDATE
DE_RISK
NO_CHANGE
INSUFFICIENT
```

`CHANGE_CANDIDATE` is allowed only for `DIAGNOSTIC_PROBE` cases.

`CONTROL_BREAK_CANDIDATE` is allowed only for `STABILITY_CONTROL` cases.

Interpretation compares the persisted GenSearch evidence against the **pre-registered condition from Step 15**. It does not invent a new success criterion after seeing the result.

Source handling:

```text
used=true = provider says source was used in the answer
used=false = preserve, but do not treat as used evidence
source array order = no ranking inference
source role = classify only when supportable from URL/title/current known page role
unclear role = SOURCE_ROLE_UNRESOLVED
```

`searchQueries[]` handling:

```text
preserve exact text + reqId;
treat as GenSearch refined queries only;
do not relabel as consumer Alice fan-out;
do not infer that absence of expansion means absence of broader consumer intent.
```

### Phase D — no-usable-result / unknown handling

If the initial paid question returns no usable analytical result or OUTCOME_UNKNOWN:

```text
record minimal operational state
announce retry 1/3 with exact query + incremental cost
retry same exact question
if usable -> persist/readback and stop retrying
otherwise continue to retry 2/3 and 3/3 under the existing owner-approved retry rule
```

After retry 3/3 fails:

```text
FINAL CASE OUTCOME = INSUFFICIENT
NO FURTHER PAID RETRY WITHOUT NEW OWNER AUTHORIZATION
```

### Phase E — material-delta confirmation

If a usable initial observation is `CHANGE_CANDIDATE` or `CONTROL_BREAK_CANDIDATE`, do not hand it to Step 17 as confirmed architecture-changing evidence yet.

Proposed project-specific confirmation mechanic:

```text
1. persist/read back the initial candidate observation;
2. execute one additional independent same-query GenSearch observation only if the owner authorization includes the conditional confirmation branch;
3. persist/read back confirmation independently;
4. compare material direction, not text identity;
5. same material direction -> CHANGE_CONFIRMED or CONTROL_BREAK_CONFIRMED;
6. materially inconsistent / non-discriminative confirmation -> MATERIAL_DELTA_NOT_REPRODUCED / INSUFFICIENT_FOR_ARCHITECTURE_CHANGE.
```

This is a pragmatic confirmation gate, not a statistical estimate and not proof of long-term temporal stability.

### Phase F — final Step-16 ledger

One row per selected case with at least:

```text
case_id
case_role
authoritative_query
initial_observation_id
initial_request_id
initial_evidence_usability
initial_outcome
confirmation_required
confirmation_observation_id
confirmation_request_id
final_step16_outcome
message_orientation_summary
used_source_count
used_target_domain_urls
primary_owner_used
supporting_owner_used
refined_queries
fixed_misspell_query
answer_rejected
bullet_answer
problematic_answer
raw_evidence_refs
provider_calls
provider_cost_rub
claim_boundary
step17_handoff
```

Free-text orientation summaries must remain evidence-grounded. They are analyst interpretation, not provider-native fields.

## 11. Cost and request envelope

Base planned execution:

```text
INITIAL_PROVIDER_CALLS = 8
UNIT_COST_RUB = 5.08
BASE_COST_RUB = 40.64
```

Conditional semantic confirmations if all eight initial observations were material candidates:

```text
MAX_CONFIRMATION_CALLS = 8
MAX_CONFIRMATION_COST_RUB = 40.64
```

Existing owner-approved failure/unknown retry policy allows up to three additional retries after an unusable/unknown original attempt. If every one of the eight initial cases required all three retries, the theoretical incremental retry cost ceiling is:

```text
24 * 5.08 = 121.92 RUB
```

The pathological absolute envelope if all cases used three retries and then also required one semantic confirmation is:

```text
40 provider calls
203.20 RUB
```

This is **not planned spend**. Every retry must be announced before execution, and semantic confirmation is conditional on the owner-authorized Step-16 execution scope.

## 12. YMB interaction gate embedded for Step 16

```text
YMB STEP OBJECTIVE
= obtain complete usable official GenSearch evidence for each exact selected Step-15 query.

YMB REQUIRED MODE
= service=search; method=genSearch; sequential Manual one-command interactions; confirmBillable=true only after owner authorization.

YMB REQUIRED SAVED RESULT
= complete delivered Bridge result envelope plus complete normalized observation with all returned message/source/searchQuery/transport fields and exact case identity.

YMB COMPLETENESS CHECK
= exact case/query match; provider outcome known; complete raw envelope saved; response fields preserved without representative-only truncation; source/searchQuery counts reconcile; GitHub readback succeeds; normalized observation points to raw evidence.

YMB STOP CONDITION
= if a useful result is not durably saved/read back and verified, STOP; no next paid provider interaction.
```

Required markers:

```text
YMB_INTERACTION_GATE_EMBEDDED = true
YMB_PROJECT_RESULT_DEFINED = true
YMB_REQUIRED_STORAGE_DEFINED = true
YMB_COMPLETENESS_CHECK_DEFINED = true
YMB_STOP_ON_INCOMPLETE_RESULT = true
```

## 13. Adversarial self-audit findings

### Finding A — `used-source hierarchy` wording is too strong if interpreted positionally

Step-15 rows use phrases such as `used-source hierarchy`. Current official API documentation supports `used` status and source identity, but not a positional ranking claim.

Resolution for this job:

```text
NO SOURCE-ORDER RANKING
ROLE/SPECIFICITY COMPOSITION ONLY
```

No historical Step-15 artifact is rewritten.

### Finding B — official API has more options than the current Bridge command

Current official API documents site/host/url scope and rich-answer/search-filter options, while current Bridge GenSearch command remains intentionally bounded to `method/queryText/confirmBillable`.

This is **not a blocker** for the Step-16 goal because the selected cases need open-index generative search evidence, not a site-restricted retrieval test.

### Finding C — consumer Alice temporal variability cannot be silently generalized into exact GenSearch behavior

Yandex explicitly documents time-varying consumer Alice answers/sources in Webmaster. GenSearch is a separate surface.

Resolution:

```text
consumer-Alice variability evidence = METHOD CONTEXT ONLY
exact GenSearch confirmation rule = PROJECT-SPECIFIC RISK CONTROL
```

### Finding D — one same-session confirmation does not establish long-term stability

Resolution:

```text
CONFIRMED = reproduced material direction in the bounded Step-16 confirmation design
CONFIRMED != long-term stable consumer behavior
```

## 14. Risks / uncertainties

```text
1. A successful GenSearch response may be too sparse/non-discriminative for a case.
2. Refined queries may merely repeat the root query; this is valid evidence, not a failure.
3. Source usage may omit both frozen OKNO_MSK pages; this does not by itself prove either page should be removed.
4. The model may answer with a different framing while sources remain mixed; outcome may remain INSUFFICIENT.
5. Current installed Bridge runtime identity is observable only from actual delivered runtime evidence; if the first delivered result reports an unexpected material version/capability mismatch, stop before the next provider call and reassess.
6. Confirmation proves only bounded near-term reproduction, not future stability.
```

## 15. What Step 16 will NOT do

```text
no final Search-vs-AI architecture verdict;
no automatic page merge/split/create/delete;
no prevalence percentage for AI-vs-Search differences;
no GenSearch==Alice claim;
no source-order ranking inference;
no private Webmaster AI claims;
no new ordinary Search acquisition unless a separate later gate establishes a material need;
no Bridge engineering merely because the upstream API exposes optional parameters;
no provider call before explicit owner authorization.
```

## 16. Proposed Step-16 pass gate

```text
INPUT_SELECTED_CASES = 8/8 exact V2 rows
INITIAL_CASES_ACCOUNTED = 8/8
SILENT_CASE_DROPS = 0
RAW_USEFUL_PROVIDER_RESULTS_PERSISTED_AND_READ_BACK = 100%
NORMALIZED_OBSERVATION_RECORDS = 8/8
GEN_SEARCH_PROVENANCE_VIOLATIONS = 0
SOURCE_ORDER_RANKING_INFERENCES = 0
PRE_REGISTERED_CONDITION_USED = 8/8
MATERIAL_DELTA_WITHOUT_REQUIRED_CONFIRMATION = 0
UNRESOLVED_PROVIDER_OUTCOME_SILENTLY_TREATED_AS_EVIDENCE = 0
RETRY_ANNOUNCEMENT_VIOLATIONS = 0
PROVIDER_CALLS_RECONCILED = 100%
PROVIDER_COST_RECONCILED = 100%
CLAIMS_EXCEEDING_EVIDENCE_MODE = 0
STEP17_ARCHITECTURE_DECISIONS_EXECUTED_IN_STEP16 = 0
FINAL_GITHUB_READBACK = PASS
```

## 17. Pre-step verdict

```text
METHOD_VERDICT = PROJECT_SPECIFIC_BUT_REASONED
STEP16_PERMANENT_METHOD_STATUS = UNVALIDATED
CURRENT_JOB_EXECUTION_SCHEMA_READY = true
BRIDGE_CAPABILITY_SUFFICIENT = true
NEW_BRIDGE_ENGINEERING_REQUIRED = false
OWNER_METHOD_REVIEW_PRESENTED = true after chat presentation
STEP16_PROVIDER_CALL_AUTHORIZED = false
STEP16_EXECUTED = false
```

Next legal transition:

```text
OWNER REVIEWS METHOD + COST / CONFIRMATION BOUNDARY
-> EXPLICIT STEP16 PROVIDER AUTHORIZATION
-> EXECUTE EXACTLY THE FROZEN MANIFEST
```
