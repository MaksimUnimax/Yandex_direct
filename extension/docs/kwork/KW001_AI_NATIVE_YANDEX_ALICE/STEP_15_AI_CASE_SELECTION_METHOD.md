# KW-001 — STEP 15 AI-CASE SELECTION METHOD

Date: 2026-09-02  
Status: **ACTIVE / OWNER-REQUESTED PERMANENT STEP-15 METHOD AFTER POST-RUN CORRECTION**

## 0. Purpose

Step 15 selects the smallest useful set of cases to send into the separately gated Step 16 AI-evidence acquisition stage.

Step 15 does **not** call GenSearch, consumer Alice, Webmaster-private Alice visibility, Wordstat, Search, or any other provider. It works only from already frozen Search-stage evidence and current accepted architecture evidence.

Canonical boundary:

```text
STEP15 = CASE DESIGN / SELECTION / PREREGISTRATION
STEP16 = AI EVIDENCE ACQUISITION
STEP15 PASS != STEP16 PROVIDER AUTHORIZATION
```

## 1. Why this permanent method exists

The first OKNO_MSK Step-15 execution correctly introduced information-gain selection, diversity and pre-registration, but the post-run audit found two material method defects.

### Defect S15-D01 — manual candidate lineage drift

The V1 ledger was manually reconstructed from remembered/inferred Step-13/14 relationships instead of being built as an exact join on the authoritative Step-13 IDs.

Observed examples included:

- a V1 `C15-008` labelled as aluminium-glazing replacement even though authoritative `QF008` is `PVC_DOOR_INSTALLATION`;
- wrong `pair_ids` on multiple QF rows;
- a wrong primary-owner description on QF010;
- shortening the QF013 representative query from `французские панорамные окна` to `французские окна`, changing the tested boundary;
- wrong frozen-owner URLs in QF019/QF020 descriptions.

Root cause:

```text
MANUAL RECONSTRUCTION / MEMORY
WAS ALLOWED TO SUBSTITUTE FOR
EXACT AUTHORITATIVE-ID JOIN
```

Permanent correction:

```text
STEP15_CANDIDATE_LINEAGE
= EXACT JOIN OF AUTHORITATIVE UPSTREAM IDS
!= MANUAL REMAPPING
```

For Step13-derived candidates the minimum authority chain is:

```text
STEP_13_QUERY_FAMILY_DEFINITIONS.tsv
JOIN case_id/QF_ID
STEP_13_CONFLICT_DIAGNOSIS.tsv
JOIN exact QF_ID
STEP_14A_ARCHITECTURE_DELTA.tsv where affected_query_families contains that exact QF_ID
```

If Step12 pair metadata is required, pair IDs must come from the Step13 definition row first and only then be resolved against the accepted Step12 pair table. Never invent or substitute pair IDs.

### Defect S15-D02 — diagnostic-only selection

The first method made `COUNTERFACTUAL_INFORMATION_GAIN` a hard gate for every selected case. That is correct for diagnostic probes, but it automatically rejected stable cases as "decorative". The resulting set was strong for finding possible Search-vs-AI differences but had no stability controls showing how the AI surface behaves on boundaries that ordinary Search already resolves clearly.

Root cause:

```text
ACTIVE-LEARNING / INFORMATION-GAIN PRINCIPLE
WAS APPLIED AS THE ONLY SELECTION TRACK
```

Permanent correction:

```text
STEP15_SELECTED_SET
= DIAGNOSTIC_PROBES
+ STABILITY_CONTROLS WHEN REQUIRED BY EVALUATION VALIDITY
```

The exact number of controls is job-scoped; a universal fixed count is forbidden. If all selected diagnostic probes are high-uncertainty / edge-boundary cases, at least one materially different stable control archetype must be considered, and normally more than one should be used when the local provider budget/count allows. An explicit documented exception is required to use no controls in such a set.

### Defect S15-D03 — generalization risk

A decision-focused Step15 set is intentionally enriched for difficult/uncertain cases. It is not a representative sample of the whole semantic core.

Permanent claim boundary:

```text
SELECTED STEP15 SET
!= REPRESENTATIVE QUERY DISTRIBUTION
!= ESTIMATE OF HOW OFTEN AI DIFFERS FROM SEARCH
```

Controls improve interpretability; they do not make a small diagnostic set statistically representative.

### Defect S15-D04 — no confirmation handoff for material AI deltas

A single later AI observation may vary by time/model/surface. Step15 must therefore pre-register whether a later `CHANGE` or control break requires confirmation before Step17 can alter architecture.

Default:

```text
ARCHITECTURE_MATERIAL_CHANGE_FROM_AI
-> CONFIRMATION_REQUIRED_IN_STEP16/17 METHOD
```

The exact confirmation mechanism belongs to Step16/17 and must be researched there; Step15 only hands off the requirement.

## 2. Method sources and what they support

### Official Yandex — GenSearch observables

- https://aistudio.yandex.ru/en/docs/search-api/concepts/generative-response
- https://aistudio.yandex.ru/en/docs/search-api/api-ref/grpc/GenSearch/search

Supports selecting cases whose uncertainty can be informed by actual GenSearch observables such as generated message orientation, `sources[]`, source `used`, and refined `search_queries[]`; also supports treating missing/weak results as legitimate insufficient evidence.

### Expected information gain / experimental design analogy

- https://www.nature.com/articles/s41598-024-65196-w

Supports using value of information to choose which expensive observations are worth acquiring. This is a transferred experimental-design principle, not an SEO ranking standard.

### Active learning — informativeness and diversity

- https://aclanthology.org/2022.emnlp-main.414/
- https://arxiv.org/abs/2107.14263

Supports avoiding redundant batches and combining informativeness with diversity/representativeness considerations. These sources do not prescribe a fixed KW-001 query count.

### Evaluation validity / representative conditions

- https://airc.nist.gov/airmf-resources/airmf/5-sec-core/
- https://airc.nist.gov/airmf-resources/airmf/3-sec-characteristics/

NIST AI RMF guidance supports documenting test sets/methods and evaluating under conditions relevant to expected use. For KW-001 this motivates explicitly separating diagnostic edge cases from stable controls and forbids presenting the diagnostic set as a prevalence estimate.

### Practical eval design / real-world + edge cases

- https://openai.com/index/evals-drive-next-chapter-of-ai/

Supports using real-world cases together with edge cases and explicit error analysis. For KW-001 this is used as general evaluation-design guidance, not as a Yandex-specific ranking authority.

## 3. Required upstream authorities

Before Step15 execution read, in order:

```text
1. current STEP_RULES_INDEX / applicable Step15 registration
2. this STEP_15_AI_CASE_SELECTION_METHOD.md
3. current job STEP14 final state/freeze
4. STEP_13_QUERY_FAMILY_DEFINITIONS.tsv
5. STEP_13_CONFLICT_DIAGNOSIS.tsv
6. STEP_14A_ARCHITECTURE_DELTA.tsv or later equivalent current-site delta
7. relevant Step12 pair/unit authority only by exact IDs from Step13
8. ordinary Search baseline artifacts referenced by Step13
9. current product/provider count and cost constraints
10. CLIENT_PRIVATE_YANDEX_ACCESS_POLICY.md only for downstream evidence-route boundaries; Step15 itself performs no private/provider acquisition
```

## 4. Phase A — construct the closed candidate universe by exact ID join

Do not begin from all phrases and do not manually invent candidate identities.

For Step13-derived rows:

```text
CANDIDATE_ID = stable Step15 case ID
QUERY_FAMILY_ID = exact Step13 QF ID
PAIR_IDS = exact Step13 definition pair_ids
REPRESENTATIVE_QUERY = exact Step13 conflict-diagnosis representative_query
EVIDENCE_MODE = exact Step13 evidence_mode
PRIMARY_OWNER = exact Step13 primary_owner
SUPPORTING_URL = exact Step13 supporting_or_other_url
STEP13_VERDICT = exact Step13 final_verdict
STEP14A_DELTAS = exact affected_query_families join + separately declared structural-only overlays
```

For Step14-only material topics not represented by a Step13 QF, create a delta-derived candidate with exact delta IDs and no invented QF.

### Mandatory lineage QA

Before selection, compare every candidate against upstream authority:

```text
qf_id_mismatch = 0
pair_id_mismatch = 0
representative_query_mismatch = 0
primary_owner_mismatch = 0
supporting_url_mismatch = 0
step13_verdict_mismatch = 0
unexplained_step14_delta_join = 0
```

Any non-zero unexplained mismatch = Step15 FAIL / repair before selection.

## 5. Phase B — classify candidate track

Every reviewed candidate gets exactly one final role:

```text
DIAGNOSTIC_PROBE
STABILITY_CONTROL
REJECT
HOLD
```

`SELECT` is a verdict, while `case_role` explains why the selected case exists.

### Track 1 — DIAGNOSTIC_PROBE

A diagnostic probe must satisfy:

`D1 FROZEN_DECISION_LINK`  
Exact link to a frozen Search-only architecture/page-role/boundary decision.

`D2 SPECIFIC_DECISION_AT_STAKE`  
A concrete owner, page-role, taxonomy, source-worthiness, intent or cannibalization/differentiation decision can change or become materially safer.

`D3 PRE_AI_BASELINE_EXISTS`  
Exact ordinary-Search/Search-only baseline is persisted before AI evidence.

`D4 COUNTERFACTUAL_INFORMATION_GAIN`  
At least one plausible AI observation would mean `CHANGE` or `DE_RISK`.

`D5 OBSERVABLE_MATCH`  
The uncertainty can be informed by fields/surface behavior the later Step16 method can actually observe.

`D6 WRONG_SOURCE_REJECT`  
If the missing truth is client business truth, private analytics/history or another non-AI source, reject AI acquisition for that uncertainty.

### Track 2 — STABILITY_CONTROL

A stability control is intentionally low-uncertainty and does **not** need D4 in the same sense.

It must satisfy:

`C1 STABLE_SEARCH_BASELINE`  
A fresh/direct or otherwise explicitly accepted Search baseline strongly resolves the page responsibility.

`C2 DISTINCT_STABLE_ARCHETYPE`  
The control represents a useful stable pattern not already duplicated by another control, e.g. exact specialist owner, clear transactional service owner, clean parent/child routing.

`C3 AI_OBSERVABLE`  
The later AI surface can still express a comparable user job/source role.

`C4 FALSIFICATION_ROLE`  
Before Step16, record what outcome would constitute a control break or warn that AI evidence is systematically over-generalizing/reinterpreting stable Search boundaries.

`C5 NO_ARCHITECTURE_AUTOCHANGE`  
A single control break never directly changes architecture. It triggers confirmation/validity review in Step16/17.

Controls exist to interpret the diagnostic batch, not to manufacture extra AI deltas.

## 6. Phase C — pre-register selected-case interpretation

Every selected diagnostic or control must record before Step16:

```text
case_id
case_role
exact representative_query
exact Search-only baseline ref
frozen primary/supporting responsibility
specific decision/evaluation purpose
expected AI observables
CHANGE / CONTROL_BREAK condition
DE_RISK condition
NO_CHANGE condition
INSUFFICIENT condition
confirmation_required_if_material_delta
step16_provider_call_authorized=false
```

For controls, expected normal outcome is usually `NO_CHANGE` or `DE_RISK`, but this expectation must not be used to coerce the observed result.

## 7. Phase D — diagnostic diversity + control coverage

For diagnostic probes:

1. choose distinct high-leverage uncertainty families first;
2. then medium-leverage distinct families;
3. duplicate diagnostic families only with explicit reason.

For controls:

1. choose stable cases only after the diagnostic set is known;
2. prefer distinct stable archetypes;
3. do not use a presearch/no-fresh-query case as a control when a fresh stable case is available;
4. do not choose a control solely to reach a numeric quota.

## 8. Count and budget handling

No universal magic query count exists.

The current job/product may define a local bounded target such as 3–10 total selected cases. Apply that only as a scoped constraint.

```text
LOCAL_COUNT_TARGET != SCIENTIFIC_STANDARD
COUNT_LIMIT != QUALITY_QUOTA
```

If adding controls exceeds a local target, either replace redundant diagnostics or obtain an explicit owner-reviewed exception; never silently violate the product constraint.

## 9. Mandatory selected-set claim boundary

Every Step15 report must state one of:

```text
DECISION_DIAGNOSTIC_SET
DECISION_DIAGNOSTIC_SET_WITH_STABILITY_CONTROLS
REPRESENTATIVE_SAMPLE  # only if a separate representative-sampling method actually supports it
```

Default KW-001 Step15 sets are **not** representative samples.

Forbidden downstream statements unless separately supported:

```text
"AI differs from Search in X% of site demand"
"these cases represent the whole semantic core"
"Alice usually behaves this way"
```

## 10. Mandatory QA

Step15 may PASS only if:

```text
candidate_universe_closed = true
reviewed = selected + rejected + hold
silent_drops = 0
lineage_mismatches_unresolved = 0
all selected have exact baseline refs
all diagnostic probes pass D1-D6
all controls pass C1-C5
all selected have preregistered outcomes
selected controls have explicit stable archetype + falsification role
selected set claim boundary is explicit
provider_calls = 0
gensearch_calls = 0
consumer_alice_calls = 0
step16_executed = false
step16_provider_call_authorized = false
```

## 11. Error-prevention controls

```text
KW001_STEP15_EXACT_QF_JOIN_REQUIRED = true
KW001_STEP15_MANUAL_PAIR_ID_RECONSTRUCTION_FORBIDDEN = true
KW001_STEP15_REPRESENTATIVE_QUERY_MUST_EQUAL_AUTHORITY = true
KW001_STEP15_PRIMARY_OWNER_MUST_EQUAL_AUTHORITY_OR_EXPLICIT_LATER_DELTA = true
KW001_STEP15_DIAGNOSTIC_AND_CONTROL_TRACKS_SEPARATE = true
KW001_STEP15_DIAGNOSTIC_SET_NOT_REPRESENTATIVE_BY_DEFAULT = true
KW001_STEP15_STABLE_CONTROLS_REQUIRE_FRESH_ACCEPTED_BASELINE = true
KW001_STEP15_SINGLE_AI_CHANGE_DOES_NOT_AUTOCHANGE_ARCHITECTURE = true
KW001_STEP15_PROVIDER_CALLS_FORBIDDEN = true
KW001_STEP15_STEP16_AUTHORIZATION_SEPARATE = true
```

## 12. Current access-policy interaction

Do not rewrite access policy inside Step15.

The existing `CLIENT_PRIVATE_YANDEX_ACCESS_POLICY.md` remains authoritative for downstream Step16 with-access vs without-access handling.

Step15 only records which later evidence could answer the case. It must never claim that client-private evidence was observed when it was not.
