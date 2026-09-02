# OKNO_MSK — Step 15 pre-step methodology research and owner review

Date: 2026-09-02  
Job: `OKNO_MSK`  
Step: `15 — AI-case selection`  
Status: `PRE-STEP RESEARCH COMPLETE / METHOD PROPOSED / EXECUTION NOT AUTHORIZED`  
Bridge/provider mode: `NO_BRIDGE / ZERO_PROVIDER_CALLS`

## 1. Step purpose

Select a small, decision-relevant set of Search-vs-generative-search cases **before** any GenSearch acquisition.

Step 15 does not collect AI evidence. It decides which cases are worth spending Step-16 provider requests on.

The current job enters Step 15 only after accepted Search-only Step 14 closure at commit:

`16d7f38b7b48369d3d2687553f7a865b86bf133e`

Step-14 state used as the frozen baseline:

- active phrases: 2332
- assigned phrases: 2313
- preserved unresolved: 19
- structural units: 168
- Step-13 effective pairs: 199
- Step-13 query-family cases: 21
- Step-14A newly discovered URLs classified: 2624/2624
- architecture-material Step-14A URLs: 21
- material crawl errors unresolved: 0
- new-page actions: 0
- destructive actions: 0
- internal-link topology: 15/15 classified

## 2. Why a fresh method review was required

`STEP_RULES_INDEX.md` still classifies Step 15 as `UNVALIDATED`.

Therefore the universal gates require current external research, source-to-method traceability, research-to-execution operationalization, an owner-facing method review, and no execution until that review is accepted.

This file is the owner-facing review. It does **not** approve Step 15 as a permanent universal method.

## 3. Current external research

### S15-01 — Yandex official generative-search semantics

Source: Yandex AI Studio, “Search with a generative response”  
URL: https://aistudio.yandex.ru/en/docs/search-api/concepts/generative-response  
Accessed: 2026-09-02

Current Yandex documentation says generative search analyzes relevant Yandex Search API text-search results and produces one coherent response. Search scope can be constrained by `site`, `host`, or `url`, or left across the full Yandex index. The service can return full or partial responses.

Method consequence: Step 15 must select cases where a generative answer/search-source view is capable of answering a **specific decision uncertainty**; it must not query the semantic core indiscriminately.

### S15-02 — Yandex official observable GenSearch fields

Source: Yandex AI Studio, `GenSearchService.Search` API reference  
URL: https://aistudio.yandex.ru/en/docs/search-api/api-ref/grpc/GenSearch/search  
Accessed: 2026-09-02

The response schema exposes:
- generated `message`;
- `sources[]` documents used to form the response;
- source URL/title and `used` flag;
- `search_queries[]` refined by the Yandex model;
- fixed-misspelling query and other metadata.

Method consequence: a selected Step-15 case must say **which observable field can de-risk or change the frozen Search decision**. “AI seems interesting” is not a valid selection reason.

### S15-03 — Yandex official failure/insufficient-evidence behavior

Source: same Yandex generative-response documentation as S15-01.

Yandex documents legitimate cases where no relevant documents are found, extraction fails, or the system is doubtful about answer quality. Response fields are not all mandatory.

Method consequence: `INSUFFICIENT` is a first-class future Step-16 outcome. A failed/weak generative answer must never be coerced into `CHANGE` or `DE_RISK`.

### S15-04 — expected information gain / value-of-information principle

Source: Scientific Reports (2024), “Identifying Bayesian optimal experiments for uncertain biochemical pathway models”  
URL: https://www.nature.com/articles/s41598-024-65196-w  
Accessed: 2026-09-02

Bayesian optimal experimental design selects experiments expected to provide the most useful information, commonly by maximizing expected information gain under uncertainty and resource constraints.

Method consequence: Step 15 uses **decision value of information**, not raw query volume, as the primary selection principle. This is a transfer of the experimental-design principle, not a claim that SEO case selection is Bayesian parameter estimation.

### S15-05 — informativeness + representativeness/diversity

Source: Zhang, Strubell, Hovy (EMNLP 2022), “A Survey of Active Learning for Natural Language Processing”  
URL: https://aclanthology.org/2022.emnlp-main.414/  
Accessed: 2026-09-02

The survey separates query informativeness from representativeness and discusses query strategies, cost, and stopping.

Method consequence: after decision-value gating, the batch must cover distinct uncertainty families instead of selecting many near-duplicate variants of the same question.

### S15-06 — batch redundancy risk

Source: Citovsky et al. (2021), “Batch Active Learning at Scale”  
URL: https://arxiv.org/abs/2107.14263  
Accessed: 2026-09-02

Batch selection can lose adaptivity and sample redundant examples; combining uncertainty and diversity is used to reduce this risk.

Method consequence: one representative per uncertainty family is preferred before adding a second case from the same family. A duplicate requires an explicit control/repeat rationale.

### S15-07 — current practical caution

Source: Romberg et al. (EACL 2026), “Reassessing Active Learning Adoption in Contemporary NLP: A Community Survey”  
URL: https://aclanthology.org/2026.eacl-long.120/  
Accessed: 2026-09-02

The 2026 survey reports that active-learning-style selection remains relevant but practical constraints and uncertain cost reduction remain important.

Method consequence: do not turn a sophisticated acquisition heuristic into a mandatory large experiment. Keep the selection operational, bounded, and auditable.

### S15-08 — model-discrimination principle

Source: Nature Reviews Neuroscience (2026), “Making models disagree to learn how brains compute”  
URL: https://www.nature.com/articles/s41583-026-01070-0  
Accessed: 2026-09-02

The review describes optimizing stimuli to distinguish competing model predictions and maximizing model-comparison power.

Method consequence: prefer cases where ordinary Search and the generative surface have a plausible opportunity to expose **different user-job/source/content responsibilities**. This is a cross-domain experimental-design analogy, not evidence about Yandex ranking.

## 4. Current-job product constraint

Current job/product authority:

`extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/IMPLEMENTATION_PLAN.md`

The rehearsal plan says Step 6 should select only queries where AI evidence could change or materially de-risk a decision and gives a **normally about 3–10 query** default for the base rehearsal.

This is a scoped commercial/product constraint, not a universal scientific threshold.

Configured rule for `OKNO_MSK`:

```text
TARGET RANGE = normally 3–10 selected cases
FEWER THAN 3 = allowed if fewer cases pass the materiality/information-gain gates
MORE THAN 10 = requires an explicit owner-reviewed reason before Step16
COUNT DOES NOT OVERRIDE QUALITY
```

## 5. Proposed executable Step-15 method

### Phase A — build the candidate universe

Do not start from all 2332 phrases.

Start from decision-bearing frozen evidence:

1. Step-14 final architecture and current-site delta.
2. Step-13 query-family/cannibalization boundaries.
3. Step-12 units with real ownership/content-role ambiguity still relevant after Step 14.
4. Ordinary Search baseline evidence from Step 9/13 where it materially supports the case.
5. No candidate may be created merely because a phrase is high-frequency.

### Phase B — hard eligibility gates

A candidate is eligible only if all are true:

`E1 FROZEN_DECISION_LINK`  
It reverse-traces to an exact Step-14 structural unit, query family, page boundary, or current-page competition decision.

`E2 SPECIFIC_DECISION_AT_STAKE`  
There is a concrete decision that could change or become materially safer: owner choice, specialist-vs-hub boundary, commercial-vs-explanatory page job, cannibalization/differentiation, source-worthiness, or similar architecture/content responsibility.

`E3 PRE_AI_BASELINE_EXISTS`  
The ordinary-Search/Search-only baseline is written before looking at new AI evidence.

`E4 COUNTERFACTUAL_INFORMATION_GAIN`  
Before acquisition, at least one plausible future GenSearch observation would cause `CHANGE` or `DE_RISK`; otherwise the case is decorative and is rejected.

`E5 OBSERVABLE_MATCH`  
The uncertainty can be informed by GenSearch observables such as answer orientation, cited/used sources, and model-refined search queries.

`E6 WRONG_EVIDENCE_SOURCE_REJECT`  
If the real missing evidence is client business truth, private analytics, historical first-party query×URL data, or another non-AI source, the case is rejected from Step 15 rather than misusing GenSearch.

### Phase C — pre-register future interpretation

For each eligible case, before Step 16, record:

- exact Search-only baseline;
- uncertainty;
- decision at stake;
- expected information gain;
- future evidence question;
- what observation would mean `CHANGE`;
- what observation would mean `DE_RISK`;
- what observation would mean `NO_CHANGE`;
- what conditions mean `INSUFFICIENT`.

This blocks post-hoc storytelling after seeing AI output.

### Phase D — deduplicate and diversify

Group eligible candidates by `uncertainty_family`.

Selection order:

1. first representative from each high-leverage distinct family;
2. then medium-leverage distinct families;
3. only then a second case from an already represented family, and only with an explicit control/repeat reason.

No unexplained duplicate family is allowed.

### Phase E — ordinal prioritization, no magic score

Do not collapse the decision into an unexplained numeric score.

Record separate dimensions:

- `decision_leverage = HIGH | MEDIUM | LOW`
- `baseline_uncertainty = HIGH | MEDIUM | LOW`
- `ai_observability_fit = HIGH | MEDIUM | LOW`
- `diversity_contribution = NEW_FAMILY | CONTROL_REPEAT | REDUNDANT`
- `wrong_source_risk = NONE | MATERIAL`
- `selection_verdict = SELECT | REJECT | HOLD`

Priority is lexicographic after hard gates: material decision leverage and uncertainty first, then AI-observability fit and diversity.

### Phase F — bounded final set

For the current `OKNO_MSK` rehearsal, target approximately 3–10 cases after deduplication.

The selected set is not allowed to exceed the local product constraint merely to “cover everything”. Step 16 is evidence acquisition, not a second full crawl of the semantic core.

## 6. Mandatory output ledger for actual Step-15 execution

Actual case selection must produce a row for every reviewed candidate, selected or rejected, with at least:

```text
case_id
candidate_origin
structural_unit_ids
query_family_ids
representative_query
frozen_search_owner_or_action
ordinary_search_baseline_ref
uncertainty_family
specific_decision_at_stake
decision_leverage
baseline_uncertainty
ai_observability_fit
expected_information_gain
future_evidence_question
change_condition
de_risk_condition
no_change_condition
insufficient_condition
diversity_contribution
wrong_source_risk
selection_verdict
selection_reason
step16_provider_call_authorized
```

`step16_provider_call_authorized` must remain `false` in Step 15.

## 7. Non-repeat / claim boundaries

```text
GEN_SEARCH_QUERY_OBSERVED != ALICE_FANOUT_OBSERVED
GEN_SEARCH_ANSWER != CONSUMER_ALICE_ANSWER
GEN_SEARCH_SOURCE != CONSUMER_ALICE_SOURCE

HIGH_FREQUENCY != HIGH_INFORMATION_GAIN
UNCERTAIN != AUTOMATICALLY_AI_RELEVANT
AI_INTERESTING != DECISION_RELEVANT
SELECTED_QUERY != PAGE_RECOMMENDATION
GEN_SEARCH_NO_RESULT != NEGATIVE_SEO_FACT
BATCH_SIZE_TARGET != QUALITY_QUOTA
```

GenSearch evidence in Step 16 will be treated as an official Yandex generative-search evidence surface, not as a literal replay of consumer Alice.

## 8. Step-15 execution acceptance gates

Actual selection may pass only when:

1. Every selected case reverse-traces to a frozen Search-only decision.
2. Every selected case has a pre-AI baseline.
3. Every selected case has explicit `CHANGE / DE_RISK / NO_CHANGE / INSUFFICIENT` interpretation rules.
4. Every selected case names the GenSearch observable it expects to learn from.
5. No case uses GenSearch as a substitute for missing business truth/private analytics/history.
6. Duplicate uncertainty-family selections have explicit control reasons.
7. Selected-set size is reconciled to the local 3–10 target or an explicit owner-reviewed exception.
8. All reviewed candidates are accounted for; no silent drops.
9. Provider requests during Step 15 = 0.
10. GenSearch/Alice calls during Step 15 = 0.
11. Step 16 remains not started.
12. Owner-facing method review is accepted before case-selection execution begins.

## 9. Current decision

```text
STEP15_PRESTEP_RESEARCH_COMPLETE = true
STEP15_SOURCE_TO_METHOD_TRACE_COMPLETE = true
STEP15_RESEARCH_TO_EXECUTION_SCHEMA_COMPLETE = true
STEP15_OWNER_FACING_METHOD_REVIEW_PRESENTED = true
STEP15_EXECUTION_AUTHORIZED = false
STEP15_CASE_SELECTION_EXECUTED = false
STEP15_PROVIDER_CALLS = 0
STEP16_EXECUTED = false
```

Next legal action after owner acceptance: execute the deterministic candidate review/selection against the frozen Step-14 state, persist the complete selected/rejected ledger, QA it, and stop again before any Step-16 provider acquisition gate.
