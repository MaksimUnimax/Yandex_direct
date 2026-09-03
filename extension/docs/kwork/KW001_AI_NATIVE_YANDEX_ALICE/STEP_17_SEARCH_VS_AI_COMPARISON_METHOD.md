# KW-001 — STEP 17 SEARCH-vs-AI COMPARISON METHOD

Date: 2026-09-03  
Status: **ACTIVE / OWNER-APPROVED / PERMANENT STEP-SPECIFIC METHOD / POST-RUN CORRECTED**

## 0. Purpose

Step 17 determines whether selective AI-search evidence materially changes, de-risks, leaves unchanged, or is insufficient to judge the Search-only page/architecture decisions frozen upstream. Separately, it evaluates whether AI-used source content exposes a bounded improvement opportunity inside the already accepted page owner.

Step 17 is not a sitewide AI-visibility measurement and is not a consumer-Alice ranking test.

Canonical split:

```text
STEP17_ARCHITECTURE_QUESTION
= does AI evidence materially change/de-risk/not change/fail to resolve the frozen Search decision?

STEP17_CONTENT_QUESTION
= do directly validated AI-used sources expose a material content-fit gap/opportunity inside the accepted owner?

NO_ARCHITECTURE_CHANGE != NO_CONTENT_CHANGE
```

## 1. Why this permanent method exists

The first concrete Step-17 execution produced a useful case matrix but did not earn a permanent method. A V2 correction fixed several job-level outputs, yet the external method audit found that the process still treated some important limitations as disclosures instead of executable gates.

### Failure class S17-P01 — contract completion substituted for method validation

The job could show 8/8 case rows, 100% output-field coverage and a passing QA while `STEP_RULES_INDEX.md` still correctly marked Step 17 `UNVALIDATED`.

Root cause:

```text
JOB OUTPUT COMPLETENESS
WAS ALLOWED TO LOOK LIKE
PERMANENT METHOD VALIDATION
```

Permanent rule:

```text
CASE_MATRIX_COMPLETE != METHOD_VALIDATED
JOB_PASS != PERMANENT_STEP_METHOD_EARNED
```

A Step17 PASS now requires both a job-level evidence verdict and the currently applicable approved Step17 method/claim gates.

### Failure class S17-P02 — limitation disclosed but not governed

The corrected job report correctly stated:

```text
EXACT_QUERY != USER_JOB_FAMILY
SINGLE_RUN != LONG_TERM_STABILITY
SHORT_WINDOW_REPETITION != LONG_TERM_STABILITY
```

but those statements did not yet automatically change claim eligibility, confidence state or confirmation requirements.

Root cause:

```text
LIMITATION DISCLOSURE
WAS NOT ALWAYS CONVERTED INTO
A CLAIM / CONFIDENCE / PASS CONTROL
```

Permanent rule:

```text
LIMITATION_DISCLOSED != LIMITATION_GOVERNED

EVERY MATERIAL LIMITATION
-> ALLOWED CLAIM SCOPE
-> CONFIDENCE STATE
-> CONFIRMATION / RECHECK TRIGGER
-> PASS CONSEQUENCE
```

### Failure class S17-P03 — exact-query diagnostic evidence overextended toward user-job inference

AI systems can reformulate or fan out a user request, and the same underlying need may be expressed through materially different prompt wording. A single exact query is therefore a diagnostic observation, not evidence for an entire user-job family.

Permanent rule:

```text
ONE EXACT QUERY
= EXACT_QUERY_DIAGNOSTIC
!= USER_JOB_FAMILY_COVERAGE
```

When a material architecture/content conclusion depends on wording-sensitive AI behavior, Step17 must either include at least one representative reformulation from the same user job or keep the result explicitly bounded to the exact query and prevent family-level claims. A universal fixed number of variants is forbidden. Additional variants require information gain, not mechanical expansion.

### Failure class S17-P04 — one observation overextended toward stability

Generative answers and source sets can change across runs/time. A single observation can be useful for diagnosis, but cannot establish stable AI behavior.

Permanent rule:

```text
SINGLE_OBSERVATION = SNAPSHOT_ONLY
TWO_SHORT_WINDOW_RUNS = SHORT_WINDOW_REPRODUCTION_ONLY
LONGITUDINAL_STABILITY = REQUIRES TIME-SEPARATED EVIDENCE
```

If a material AI delta would change architecture, one observation is never sufficient by itself. Confirmation is mandatory before `CHANGE` can be accepted on AI evidence alone.

### Failure class S17-P05 — decisive direct-read provenance was not forced to 1:1 completeness

A job-level case ledger could contain a valid direct public-page read used in reasoning while the dedicated direct-read provenance ledger omitted that source row.

Permanent rule:

```text
EVERY DECISIVE DIRECT EXTERNAL PAGE READ
-> DEDICATED PROVENANCE ROW
-> URL
-> RETRIEVAL DATE/STATE
-> OBSERVED FACTS
-> DECISIVE USE
-> LIMITATION
-> CASE REFERENCE

MISSING DECISIVE PROVENANCE ROW > 0
=> STEP17 FINAL PASS BLOCKED
```

### Failure class S17-P06 — architecture and content effects were initially conflated

```text
ARCHITECTURE VERDICT AND CONTENT VERDICT ARE SEPARATE REQUIRED OUTPUTS
```

### Failure class S17-P07 — source-worthiness terminology could imply citation probability

Permanent terminology:

```text
AI_SOURCE_CONTENT_FIT
= observed fit between source content and the user task / generated answer

AI_SOURCE_CONTENT_FIT
!= PROBABILITY_OF_AI_CITATION
!= GUARANTEE_OF_AI_VISIBILITY
```

Legacy `source-worthiness` fields may be retained for backward compatibility, but future analytical claims must use or explicitly define the narrower content-fit meaning.

## 2. Method origin / direct external support

### Official Yandex — how Alice AI builds answers

Authority: https://www.yandex.ru/support/webmaster/ru/alice

Supports: query analysis/refinement, Search-related source selection, source-link order not being ranking, and task/quality-oriented source evaluation.

### Official Yandex — site visibility in Alice AI

Authority: https://yandex.ru/support/webmaster/ru/service/alice-answers

Supports: reviewing example queries and competitor/source pages, comparing them with own content, measuring visibility over time, and expecting same-query answer/source changes over time.

### Official Yandex — EPOS / user-task quality

Authority: https://yandex.ru/support/webmaster/ru/epos

Supports evaluating content around the real user task, expertise, usefulness, originality and meaningful completeness rather than keyword imitation.

### Industry practice — representative prompt sets / query fan-out

Authorities:
- https://www.semrush.com/blog/which-ai-search-prompts-to-track/
- https://www.semrush.com/blog/query-fan-out/

Classification: `INDUSTRY_PRACTICE`, not Yandex policy. Supports representative same-job prompt variants, no mechanical prompt explosion, and no family-level claim from one exact wording.

### Independent volatility evidence

Authority: https://ahrefs.com/blog/ai-overview-change/

Classification: `INDUSTRY_PRACTICE / CROSS-SYSTEM SUPPORT`, not Yandex-specific proof. Supports only the general discipline that generative answer/citation sets should not be treated as a static SERP position.

## 3. Required upstream authorities

```text
1. current universal rules and STEP_RULES_INDEX
2. this STEP_17_SEARCH_VS_AI_COMPARISON_METHOD.md
3. current job manifest / job flow / sold deliverable
4. accepted Step14/14A Search architecture freeze
5. accepted Step15 selected-case ledger + roles + preregistration
6. direct persisted Step13 ordinary-Search evidence for every selected case
7. Step16 raw AI evidence + corrected observation authority
8. current target-page evidence
9. direct external AI-used source content where a content-fit claim is intended
10. CLIENT_PRIVATE_YANDEX_ACCESS_POLICY.md for optional Webmaster Alice visibility
11. provider/cost state only if a fresh acquisition need is proven
```

Historical summaries may help navigation but cannot substitute for direct evidence authorities.

## 4. Required Step17 execution schema

Every case must materialize at least these fields or exact equivalents.

### A. Identity / upstream lineage

```text
case_id
case_role = DIAGNOSTIC_PROBE | STABILITY_CONTROL
query_family_id / upstream IDs
frozen_search_owner
frozen_search_decision
exact_authoritative_query
```

### B. Ordinary Search evidence unit

```text
ordinary_search_direct_evidence_refs
observed_result_count
ordinary_search_decisive_rows
ordinary_search_user_task
ordinary_search_content_type
ordinary_search_format
ordinary_search_angle
ordinary_search_specificity
ordinary_search_trace_state
```

Descriptions must be derived from persisted result rows, not only upstream prose summaries.

### C. AI evidence unit

```text
ai_raw_refs
ai_observation_count
ai_answer_mode
ai_refined_queries
ai_used_source_urls
ai_surface
ai_scope_class
ai_temporal_state
```

Allowed scope states:

```text
EXACT_QUERY_DIAGNOSTIC
REPRESENTATIVE_JOB_VARIANT_CHECKED
USER_JOB_FAMILY_SUPPORTED
```

`USER_JOB_FAMILY_SUPPORTED` is forbidden unless representative evidence sufficient for that scope was actually collected.

Allowed temporal states:

```text
SINGLE_SNAPSHOT
SHORT_WINDOW_REPRODUCED
TIME_SEPARATED_REPRODUCED
LONGITUDINAL_FIRST_PARTY_SIGNAL
```

### D. Direct source-content validation

For every external AI-used source decisive to a content-fit conclusion preserve exact URL, provider used-state, retrieval date/state, observed role, material facts, decisive use, limitations and provenance row ID.

```text
URL/TITLE MAY PROVE IDENTITY
URL/TITLE MUST NOT PROVE MATERIAL CONTENT DEPTH
```

### E. Current target-page validation

Preserve target URL, current retrieval state, current role, material task coverage and limitations. Old page descriptions do not substitute for a current read when a material content claim is made.

### F. Search-vs-AI delta matrix

Compare at minimum:

```text
user_task_delta
commerciality_delta
specificity_delta
content_type_or_format_delta
source_role_delta
refined_query_delta
target_site_fit
```

Do not force Search and AI to agree.

## 5. Prompt-family coverage gate

```text
EXACT_QUERY_ONLY
-> ai_scope_class = EXACT_QUERY_DIAGNOSTIC
-> family-level claim = FORBIDDEN
```

A representative same-job reformulation becomes mandatory before a stronger claim when wording ambiguity can change the task, AI refined queries materially reframe it, proposed architecture CHANGE depends on AI, a material content action appears wording-specific, or Step15 preregistered a confirmation need that a same-job variant can test.

The reformulation must preserve the same real user job. No universal fixed variant count exists; each extra provider request requires information gain.

## 6. Repetition / stability gate

### Single snapshot

May support a bounded diagnostic DE_RISK / NO_CHANGE / INSUFFICIENT and a bounded content candidate with direct source comparison. It may not establish longitudinal stability, sitewide AI visibility, consumer-Alice behavior from GenSearch, or an architecture CHANGE on AI evidence alone.

### Short-window repeat

Two close-time runs establish only `SHORT_WINDOW_REPRODUCTION`, not longitudinal stability.

### Time-separated repeat

When a material AI delta would rewrite architecture, obtain time-separated confirmation if the approved evidence route and authorization permit it. No arbitrary universal hour/day threshold is imposed.

### Private first-party signal

If Webmaster Alice visibility is available in scope, it may strengthen longitudinal/owned-site evidence. Missing private access does not block the base diagnostic method.

## 7. Architecture verdicts

Exactly one:

```text
CHANGE
DE_RISK
NO_CHANGE
INSUFFICIENT
```

`CHANGE` requires a material boundary difference and the required confirmation/coverage gates. A single AI snapshot alone cannot qualify `CHANGE`.

`DE_RISK` means AI evidence independently supports/resolves uncertainty around the frozen Search decision.

`NO_CHANGE` means AI adds no material architecture information beyond the Search decision at the validated scope.

`INSUFFICIENT` means evidence is too weak, ambiguous, incomplete or non-comparable.

## 8. Content-fit verdicts

Exactly one:

```text
CONTENT_EXPANSION_CANDIDATE
NO_MATERIAL_CONTENT_GAP_OBSERVED
INSUFFICIENT
NOT_APPLICABLE
```

`CONTENT_EXPANSION_CANDIDATE` requires direct evidence of useful decision-relevant source depth and means a bounded within-owner improvement hypothesis, not proof of absence, new-page need or future AI citation.

`NO_MATERIAL_CONTENT_GAP_OBSERVED` requires direct target/source comparison at the claimed decision dimensions and is not exhaustive parity.

`INSUFFICIENT` is required when decisive source/target content is not directly validated deeply enough.

`NOT_APPLICABLE` is used when the probe itself is too ambiguous/mismatched to produce a safe content brief for the frozen owner.

## 9. Confidence and claim governance

Confidence is categorical and evidence-derived; no magic numerical score.

### HIGH

Requires direct Search trace + current target read + decisive source reads where content is claimed + required prompt-family coverage + required repetition/longitudinal evidence + complete provenance.

### MODERATE

Typical for a bounded exact-query diagnostic with direct Search/target/source support but without family-wide or longitudinal evidence.

### LOW

Use when source content is incomplete, query intent materially ambiguous, target-role evidence weak, or another required route unavailable.

Hard rule:

```text
CONFIDENCE LABEL MUST CHANGE WHAT MAY BE CLAIMED
```

## 10. Provider-call / information-gain gate

Step17 normally analyzes persisted Step13 + Step16 evidence. Fresh paid/quota-bearing acquisition is allowed only when a named missing evidence requirement exists, persisted evidence cannot answer it, the result could materially alter verdict/confidence/claim eligibility, the exact provider surface is declared, authorization/cost gates pass, and `BRIDGE_EVIDENCE_PERSISTENCE_GATE` is applied.

No blind replay for “more confidence”.

## 11. Required durable artifacts

```text
STEP17_METHOD / PRE-STEP REVIEW
STEP17_RESEARCH_TO_EXECUTION_SCHEMA
STEP17_EXECUTION_MANIFEST
STEP17_CASE_COMPARISON_LEDGER
STEP17_DIRECT_SOURCE_PROVENANCE_LEDGER
STEP17_CLAIM_SCOPE_CONFIDENCE_LEDGER
STEP17_CONTRACT / REQUIREMENT COVERAGE AUDIT
STEP17_QA
STEP17_REPORT
STEP17_CURRENT_STATE / JOB FLOW SYNC
```

Historical accepted states are not silently overwritten; corrections create clearly superseding artifacts.

## 12. Mandatory QA

```text
selected_cases_accounted = 100%
ordinary_search_direct_trace = 100%
ai_raw_trace = 100%
architecture_verdict_present = 100%
content_verdict_present = 100%
ai_scope_class_present = 100%
ai_temporal_state_present = 100%
confidence_state_present = 100%
claim_boundary_present = 100%
decisive_direct_source_provenance_missing = 0
unsupported_family_level_claims = 0
unsupported_stability_claims = 0
source_order_as_rank_claims = 0
url_title_as_material_content_claims = 0
gensearch_as_consumer_alice_claims = 0
architecture_content_conflations = 0
reverse_trace_missing = 0
blocking_adversarial_findings = 0
final_github_readback = PASS
```

`ADVERSARIAL_SELF_REVIEW != INDEPENDENT_REVIEW`.

## 13. Acceptance gate

`STEP17_FINAL_ACCEPTANCE = PASS` only if every selected case has direct Search/raw AI trace; architecture and content states are separate; every material limitation governs claim/confidence/PASS; every decisive external direct read has a dedicated provenance row; prompt-family and temporal scope are explicit; any architecture CHANGE has passed confirmation; AI source content fit is not presented as citation probability; provider evidence is durably preserved when used; reverse trace/QA pass; and final GitHub readback confirms the accepted set.

A job with only exact-query/single-snapshot evidence may still PASS as a **BOUNDED DIAGNOSTIC STEP**, but must say so explicitly.

## 14. Handoff to Step18

Step18 must receive per case/action:

```text
architecture_verdict
content_verdict
ai_scope_class
ai_temporal_state
confidence_state
evidence_limitations
recheck_trigger
```

```text
EXACT_QUERY_DIAGNOSTIC + SINGLE_SNAPSHOT + MODERATE
= DIAGNOSTIC SUPPORTING EVIDENCE
!= STABLE FIRST-PARTY AI VISIBILITY MEASUREMENT
```

## 15. Permanent non-repeat markers

```text
KW001_STEP17_METHOD_ACTIVE = true
KW001_STEP17_JOB_PASS_NOT_EQUAL_METHOD_VALIDATED = true
KW001_STEP17_LIMITATION_MUST_GOVERN_CLAIM = true
KW001_STEP17_EXACT_QUERY_NOT_EQUAL_USER_JOB_FAMILY = true
KW001_STEP17_SINGLE_RUN_NOT_EQUAL_STABILITY = true
KW001_STEP17_SHORT_WINDOW_REPEAT_NOT_EQUAL_LONGITUDINAL = true
KW001_STEP17_MATERIAL_AI_ARCHITECTURE_CHANGE_REQUIRES_CONFIRMATION = true
KW001_STEP17_SEARCH_AND_AI_SURFACES_MUST_NOT_BE_FORCED_TO_AGREE = true
KW001_STEP17_ARCHITECTURE_AND_CONTENT_VERDICTS_SEPARATE = true
KW001_STEP17_AI_SOURCE_CONTENT_FIT_NOT_EQUAL_CITATION_PROBABILITY = true
KW001_STEP17_SOURCE_ORDER_NOT_EQUAL_RANK = true
KW001_STEP17_URL_TITLE_NOT_EQUAL_MATERIAL_CONTENT_PROOF = true
KW001_STEP17_DECISIVE_DIRECT_READ_PROVENANCE_1_TO_1_REQUIRED = true
KW001_STEP17_CONFIDENCE_MUST_CHANGE_ALLOWED_CLAIM = true
KW001_STEP17_NO_MAGIC_NUMERICAL_CONFIDENCE_SCORE = true
KW001_STEP17_BASE_DIAGNOSTIC_PASS_WITHOUT_PRIVATE_WEBMASTER_ALLOWED = true
KW001_STEP17_PROVIDER_REPLAY_REQUIRES_INFORMATION_GAIN = true
KW001_STEP17_FINAL_GITHUB_READBACK_REQUIRED = true
```
