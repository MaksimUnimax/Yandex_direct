# KW-001 — STEP 15 AI-CASE SELECTION METHOD

Date: 2026-09-02  
Updated: 2026-09-03  
Status: **APPROVED / ACTIVE / UNIVERSAL / OWNER-AUTHORIZED AFTER POST-RUN CORRECTION**

## 0. Purpose

Step 15 selects the smallest useful set of cases to send into the separately gated Step 16 AI-evidence acquisition stage.

Step 15 does **not** itself call GenSearch, consumer AI surfaces, private first-party analytics, Wordstat, ordinary Search or another provider. It works from already accepted upstream Search/architecture evidence.

```text
STEP15 = CASE DESIGN / SELECTION / PREREGISTRATION
STEP16 = AI EVIDENCE ACQUISITION
STEP15 PASS != STEP16 PROVIDER AUTHORIZATION
```

Concrete job case IDs, queries, owners, URLs, counts and selected-set results belong in the current Level-2 workspace.

---

## 1. Permanent failure lessons

### S15-D01 — manual candidate lineage drift

**What failed**

A prior case ledger was manually reconstructed from remembered/inferred upstream relationships. This produced mismatches such as a candidate joined to the wrong authoritative upstream ID, incorrect pair IDs, an owner copied from another case, or a representative query shortened/rewritten enough to change the boundary being tested.

**Root cause**

```text
MANUAL RECONSTRUCTION / MEMORY
WAS ALLOWED TO SUBSTITUTE FOR
EXACT AUTHORITATIVE-ID JOIN
```

**Corrected method**

```text
STEP15_CANDIDATE_LINEAGE
= EXACT JOIN OF AUTHORITATIVE UPSTREAM IDS
!= MANUAL REMAPPING
```

If a current upstream artifact exposes stable IDs, Step15 must join on them mechanically. Pair IDs or related references must come from the authoritative upstream definition first and only then resolve to their referenced evidence.

### S15-D02 — diagnostic-only selection

**What failed**

An information-gain gate was applied as if every selected case had to be a high-uncertainty diagnostic probe. Stable cases were then rejected as “decorative,” leaving no controls to show how the AI surface behaves when ordinary Search already resolves the boundary clearly.

**Root cause**

```text
ACTIVE-LEARNING / INFORMATION-GAIN PRINCIPLE
WAS APPLIED AS THE ONLY SELECTION TRACK
```

**Corrected method**

```text
STEP15_SELECTED_SET
= DIAGNOSTIC_PROBES
+ STABILITY_CONTROLS WHEN REQUIRED BY EVALUATION VALIDITY
```

The exact number of controls is job-scoped. No universal quota is allowed.

### S15-D03 — generalization risk

A decision-focused selection is intentionally enriched for hard/uncertain cases.

```text
SELECTED STEP15 SET
!= REPRESENTATIVE QUERY DISTRIBUTION
!= ESTIMATE OF HOW OFTEN AI DIFFERS FROM SEARCH
```

Controls improve interpretability; they do not automatically make a small diagnostic set statistically representative.

### S15-D04 — no confirmation handoff for material AI deltas

A single later AI observation may vary by time/model/surface. Step15 must pre-register whether a later architecture-material delta requires confirmation before Step17 may accept a change.

Default:

```text
ARCHITECTURE_MATERIAL_CHANGE_FROM_AI
-> CONFIRMATION_REQUIRED_IN_STEP16/17 METHOD
```

Step15 records the requirement; the exact confirmation mechanism belongs to Step16/17.

---

## 2. Method sources and what they support

### Official Yandex — GenSearch observables

- https://aistudio.yandex.ru/en/docs/search-api/concepts/generative-response
- https://aistudio.yandex.ru/en/docs/search-api/api-ref/grpc/GenSearch/search

Supports selecting cases whose uncertainty can be informed by actual GenSearch observables such as generated answer orientation, sources, used-state and refined queries; also supports preserving missing/weak results as insufficient evidence.

### Expected information gain / experimental-design analogy

- https://www.nature.com/articles/s41598-024-65196-w

Supports using value of information to choose which costly observations are worth acquiring. This is a transferred experimental-design principle, not an SEO ranking standard.

### Active learning — informativeness and diversity

- https://aclanthology.org/2022.emnlp-main.414/
- https://arxiv.org/abs/2107.14263

Supports avoiding redundant batches and combining informativeness with diversity. These sources do not prescribe a fixed query count for this project.

### Evaluation validity / representative conditions

- https://airc.nist.gov/airmf-resources/airmf/5-sec-core/
- https://airc.nist.gov/airmf-resources/airmf/3-sec-characteristics/

Supports documenting test sets/methods and evaluating under conditions relevant to expected use. For this workflow it motivates separating diagnostic edge cases from stable controls.

### Practical eval design

- https://openai.com/index/evals-drive-next-chapter-of-ai/

General evaluation-design support for using real-world cases, edge cases and explicit error analysis. Not Yandex ranking authority.

---

## 3. Required upstream authorities

Before execution read, in order:

```text
1. current universal rules and STEP_RULES_INDEX
2. this Step15 method
3. current accepted upstream Search/architecture state
4. authoritative upstream case/family definitions with stable IDs
5. authoritative competing-page/boundary diagnosis where applicable
6. latest current-site architecture deltas/overlays where applicable
7. pair/unit evidence only by exact upstream IDs
8. ordinary Search baseline artifacts referenced by the upstream diagnosis
9. current provider count/cost constraints
10. client-private access policy only for downstream evidence-route boundaries
```

Historical prose summaries may help navigation but must not substitute for direct authoritative IDs/evidence.

---

## 4. Phase A — construct the closed candidate universe by exact join

Do not begin from all phrases and do not manually invent candidate identities.

For each upstream-derived candidate preserve equivalent fields:

```text
CANDIDATE_ID
UPSTREAM_FAMILY_OR_CASE_ID
PAIR_OR_RELATED_IDS from upstream authority
REPRESENTATIVE_QUERY exact from upstream authority
EVIDENCE_MODE
PRIMARY_OWNER / RESPONSIBILITY exact from accepted authority
SUPPORTING_URL_OR_SCOPE when applicable
UPSTREAM_VERDICT
LATEST_ARCHITECTURE_DELTAS by exact join
```

For a material current-site topic not represented by an upstream family/case ID, create a delta-derived candidate with the exact delta ID and without inventing an upstream identity.

### Mandatory lineage QA

```text
upstream_id_mismatch = 0
pair_or_related_id_mismatch = 0
representative_query_mismatch = 0
primary_owner_mismatch = 0
supporting_scope_mismatch = 0
upstream_verdict_mismatch = 0
unexplained_latest_delta_join = 0
```

Any unexplained non-zero mismatch = Step15 FAIL / repair before selection.

---

## 5. Phase B — classify candidate track

Every reviewed candidate gets exactly one final role:

```text
DIAGNOSTIC_PROBE
STABILITY_CONTROL
REJECT
HOLD
```

### Track 1 — DIAGNOSTIC_PROBE

A diagnostic probe must satisfy:

`D1 FROZEN_DECISION_LINK` — exact link to an accepted Search-only responsibility/boundary decision.  
`D2 SPECIFIC_DECISION_AT_STAKE` — a concrete owner/page-role/taxonomy/source-fit/intent/boundary decision can change or become materially safer.  
`D3 PRE_AI_BASELINE_EXISTS` — exact Search-only baseline is persisted before AI evidence.  
`D4 COUNTERFACTUAL_INFORMATION_GAIN` — at least one plausible AI observation would mean `CHANGE` or `DE_RISK`.  
`D5 OBSERVABLE_MATCH` — the uncertainty can be informed by fields/behavior the Step16 method can actually observe.  
`D6 WRONG_SOURCE_REJECT` — if the missing truth is client business truth/private analytics/another non-AI source, reject AI acquisition for that uncertainty.

### Track 2 — STABILITY_CONTROL

A stability control is intentionally low-uncertainty and does not need D4 in the same form.

It must satisfy:

`C1 STABLE_SEARCH_BASELINE` — accepted Search evidence strongly resolves responsibility.  
`C2 DISTINCT_STABLE_ARCHETYPE` — represents a useful stable pattern not duplicated by another control.  
`C3 AI_OBSERVABLE` — later AI surface can express a comparable user job/source role.  
`C4 FALSIFICATION_ROLE` — pre-register what would constitute a control break.  
`C5 NO_ARCHITECTURE_AUTOCHANGE` — one control break triggers confirmation/validity review, not automatic architecture mutation.

---

## 6. Phase C — pre-register interpretation

Every selected case must record before Step16:

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

Expected outcomes must not be used to coerce the observation.

---

## 7. Phase D — diagnostic diversity and control coverage

For diagnostic probes:

1. choose distinct high-leverage uncertainty families first;
2. then medium-leverage distinct families;
3. duplicate a diagnostic archetype only with explicit reason.

For controls:

1. choose stable cases after the diagnostic set is known;
2. prefer materially different stable archetypes;
3. prefer a fresh accepted baseline when available;
4. do not choose controls merely to satisfy a numeric quota.

---

## 8. Count and budget handling

No universal magic query count exists.

A current product/job may define a bounded local target. Apply it only as a scoped constraint.

```text
LOCAL_COUNT_TARGET != SCIENTIFIC_STANDARD
COUNT_LIMIT != QUALITY_QUOTA
```

If controls would exceed a local target, replace redundant diagnostics or obtain a documented owner-reviewed exception; never silently violate the constraint.

---

## 9. Selected-set claim boundary

Every report must state one of:

```text
DECISION_DIAGNOSTIC_SET
DECISION_DIAGNOSTIC_SET_WITH_STABILITY_CONTROLS
REPRESENTATIVE_SAMPLE  # only with a separate valid sampling method
```

Default diagnostic sets are not representative samples.

Forbidden unless separately supported:

```text
"AI differs from Search in X% of site demand"
"these cases represent the whole semantic core"
"the AI surface usually behaves this way"
```

---

## 10. Mandatory QA

```text
candidate_universe_closed = true
reviewed = selected + rejected + hold
silent_drops = 0
lineage_mismatches_unresolved = 0
all selected have exact baseline refs
all diagnostic probes pass D1-D6
all controls pass C1-C5
all selected have preregistered outcomes
controls have explicit stable archetype + falsification role
selected-set claim boundary explicit
provider_calls = 0
generative_search_calls = 0
consumer_ai_calls = 0
step16_executed = false
step16_provider_call_authorized = false
```

---

## 11. Current access-policy interaction

Do not rewrite access policy inside Step15.

The current client-private access policy remains authoritative for downstream with-access vs without-access handling.

Step15 only records which later evidence could answer a case. It must never claim private evidence was observed when it was not.

---

## 12. Non-repeat markers

```text
KW001_STEP15_METHOD_ACTIVE = true
KW001_STEP15_EXACT_UPSTREAM_ID_JOIN_REQUIRED = true
KW001_STEP15_MANUAL_LINEAGE_RECONSTRUCTION_FORBIDDEN = true
KW001_STEP15_REPRESENTATIVE_QUERY_MUST_EQUAL_AUTHORITY = true
KW001_STEP15_PRIMARY_OWNER_MUST_EQUAL_AUTHORITY_OR_EXPLICIT_LATER_DELTA = true
KW001_STEP15_DIAGNOSTIC_AND_CONTROL_TRACKS_SEPARATE = true
KW001_STEP15_DIAGNOSTIC_SET_NOT_REPRESENTATIVE_BY_DEFAULT = true
KW001_STEP15_STABLE_CONTROLS_REQUIRE_ACCEPTED_BASELINE = true
KW001_STEP15_SINGLE_AI_CHANGE_DOES_NOT_AUTOCHANGE_ARCHITECTURE = true
KW001_STEP15_PROVIDER_CALLS_FORBIDDEN = true
KW001_STEP15_STEP16_AUTHORIZATION_SEPARATE = true
KW001_STEP15_JOB_SPECIFIC_RESULTS_FORBIDDEN_IN_PERMANENT_METHOD = true
```

This file follows `PERMANENT_STEP_RULE_UNIVERSALITY_AND_JOB_SEPARATION_GATE.md`.
