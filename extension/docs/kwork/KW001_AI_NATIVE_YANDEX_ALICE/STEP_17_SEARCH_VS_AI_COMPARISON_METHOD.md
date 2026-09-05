# KW-001 — STEP 17 SEARCH-vs-AI COMPARISON METHOD

Updated: 2026-09-05  
Status: **APPROVED / ACTIVE / UNIVERSAL / POST-RUN CORRECTED**

Concrete case IDs, queries, URLs, row counts, provider results and current job verdicts belong only in the current Level-2 workspace.

Companion authorities:

- `STEP_RULES_INDEX.md`
- `SOURCE_TO_METHOD_TRACEABILITY_GATE.md`
- `RESEARCH_TO_EXECUTION_SCHEMA_GATE.md`
- `BRIDGE_EVIDENCE_PERSISTENCE_GATE.md`
- `CLIENT_PRIVATE_YANDEX_ACCESS_POLICY.md`
- `PERMANENT_STEP_RULE_UNIVERSALITY_AND_JOB_SEPARATION_GATE.md`

## 0. Purpose

Step17 determines whether selective AI-search evidence materially changes, de-risks, leaves unchanged, or is insufficient to judge the Search-only page/architecture decisions frozen upstream. Separately, it evaluates whether directly validated AI-used source content exposes a bounded content-fit opportunity inside the already accepted owner.

```text
STEP17_ARCHITECTURE_QUESTION
= does AI evidence change/de-risk/not change/fail to resolve the frozen Search decision?

STEP17_CONTENT_QUESTION
= does direct source/target comparison expose a material within-owner content opportunity?

NO_ARCHITECTURE_CHANGE != NO_CONTENT_CHANGE
```

Step17 is not a sitewide AI-visibility measurement and is not a consumer-surface ranking test unless a separately validated method/evidence route actually establishes that scope.

---

## 1. Permanent failure lessons

### S17-P01 — job output completeness substituted for method validation

**Failure:** a concrete execution could have all expected case rows/fields and a clean job QA while the reusable Step17 method itself had not yet been validated.

**Root cause:**

```text
JOB OUTPUT COMPLETENESS
WAS ALLOWED TO LOOK LIKE
PERMANENT METHOD VALIDATION
```

**Control:**

```text
CASE MATRIX COMPLETE != METHOD VALIDATED
JOB PASS != PERMANENT STEP METHOD EARNED
```

A job PASS requires the currently approved method/claim gates; permanent promotion is a separate owner-authorized process.

### S17-P02 — limitation disclosed but not governed

**Failure:** reports could state that evidence was exact-query or snapshot-only without making that limitation change claim eligibility, confidence or confirmation requirements.

**Root cause:**

```text
LIMITATION DISCLOSURE
WAS NOT ALWAYS CONVERTED INTO
CLAIM / CONFIDENCE / PASS CONTROL
```

**Control:**

```text
EVERY MATERIAL LIMITATION
-> ALLOWED CLAIM SCOPE
-> CONFIDENCE STATE
-> CONFIRMATION / RECHECK TRIGGER
-> PASS CONSEQUENCE
```

### S17-P03 — exact-query diagnostic evidence overextended to a user-job family

```text
ONE EXACT QUERY
= EXACT_QUERY_DIAGNOSTIC
!= USER_JOB_FAMILY_COVERAGE
```

When a material conclusion is wording-sensitive, either obtain an information-gain-justified representative same-job reformulation or keep the conclusion exact-query bounded.

### S17-P04 — one observation overextended toward stability

```text
SINGLE_OBSERVATION = SNAPSHOT_ONLY
SHORT_WINDOW_REPETITION = SHORT_WINDOW_REPRODUCTION_ONLY
LONGITUDINAL_STABILITY = REQUIRES TIME-SEPARATED / FIRST-PARTY LONGITUDINAL EVIDENCE
```

A single AI observation cannot alone authorize an architecture-material CHANGE.

### S17-P05 — decisive direct-read provenance not forced to one-to-one completeness

Every decisive external page read used for a material content-fit conclusion requires its own provenance row containing equivalent fields:

```text
URL
RETRIEVAL DATE/STATE
OBSERVED FACTS
DECISIVE USE
LIMITATION
CASE REFERENCE
```

Missing decisive provenance blocks final PASS.

### S17-P06 — architecture and content effects were conflated

Architecture verdict and content-fit verdict are separate required outputs.

### S17-P07 — source-fit terminology could imply citation probability

```text
AI_SOURCE_CONTENT_FIT
= observed fit between source content and the user task / generated answer

AI_SOURCE_CONTENT_FIT
!= PROBABILITY_OF_AI_CITATION
!= GUARANTEE_OF_AI_VISIBILITY
```

---

## 2. Method origin / external support

### Official Yandex

- Alice/search behavior: https://www.yandex.ru/support/webmaster/ru/alice
- owned site visibility in Alice AI when available: https://yandex.ru/support/webmaster/ru/service/alice-answers
- EPOS/user-task quality: https://yandex.ru/support/webmaster/ru/epos

These support query refinement/search-source behavior, task/quality-oriented content analysis and the fact that AI-source/answer behavior may change over time.

### Industry practice

- Semrush representative AI prompts: https://www.semrush.com/blog/which-ai-search-prompts-to-track/
- Semrush query fan-out: https://www.semrush.com/blog/query-fan-out/
- Ahrefs AI-answer/citation volatility: https://ahrefs.com/blog/ai-overview-change/

These are supporting industry/cross-system practices, not Yandex-specific ranking rules. They support bounded prompt-family design and caution against treating generative source sets as static ranking positions.

---

## 3. Required upstream authorities

Before execution read/reconcile:

```text
current universal rules + Step17 method
current job manifest/flow/sold deliverable
accepted Search-only architecture freeze
accepted AI-case selection + preregistration
persisted direct ordinary-Search evidence
persisted raw AI evidence
current target-page evidence
direct AI-used source content when a content-fit claim is intended
client-private access policy for optional owned evidence
provider/cost state only if a fresh information-gain need is proven
```

Historical prose summaries may aid navigation but cannot substitute for direct evidence authorities.

---

## 4. Required execution schema

### A. Identity / lineage

```text
case_id
case_role = DIAGNOSTIC_PROBE | STABILITY_CONTROL
upstream ids
frozen_search_owner
frozen_search_decision
exact_authoritative_query
```

### B. Ordinary Search evidence

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

### C. AI evidence

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

Allowed scope states include:

```text
EXACT_QUERY_DIAGNOSTIC
REPRESENTATIVE_JOB_VARIANT_CHECKED
USER_JOB_FAMILY_SUPPORTED
```

`USER_JOB_FAMILY_SUPPORTED` is forbidden unless evidence sufficient for that scope was actually collected.

Allowed temporal states include:

```text
SINGLE_SNAPSHOT
SHORT_WINDOW_REPRODUCED
TIME_SEPARATED_REPRODUCED
LONGITUDINAL_FIRST_PARTY_SIGNAL
```

### D. Direct source-content validation

For every decisive external AI-used source preserve URL, provider used-state, retrieval state/date, observed role/material facts, decisive use, limitation and provenance ID.

```text
URL/TITLE MAY PROVE IDENTITY
URL/TITLE MUST NOT PROVE MATERIAL CONTENT DEPTH
```

### E. Current target validation

A material current content claim requires a current target read; old page descriptions cannot substitute when current content depth matters.

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

---

## 5. Prompt-family coverage gate

```text
EXACT_QUERY_ONLY
-> ai_scope_class = EXACT_QUERY_DIAGNOSTIC
-> family-level claim = FORBIDDEN
```

A representative same-job reformulation is required before a stronger family-level/material CHANGE claim when wording ambiguity/refinement can change the task or the upstream preregistration requires confirmation.

No universal fixed variant count exists; every extra provider request requires information gain.

---

## 6. Temporal / stability gate

A single snapshot may support bounded diagnostic `DE_RISK / NO_CHANGE / INSUFFICIENT` and a bounded content candidate when direct comparison supports it. It may not establish longitudinal stability, sitewide AI visibility, consumer-surface behavior from a proxy, or architecture CHANGE on AI evidence alone.

A short-window repeat establishes only short-window reproduction.

A material AI architecture delta requires the confirmation/time-scope route required by the current approved evidence plan.

Optional owned first-party AI evidence may strengthen longitudinal scope when available; missing private access does not automatically block the base bounded diagnostic mode.

---

## 7. Architecture verdicts

Exactly one equivalent state:

```text
CHANGE
DE_RISK
NO_CHANGE
INSUFFICIENT
```

`CHANGE` requires a material boundary difference plus required scope/confirmation gates.

---

## 8. Content-fit verdicts

Exactly one equivalent state:

```text
CONTENT_EXPANSION_CANDIDATE
NO_MATERIAL_CONTENT_GAP_OBSERVED
INSUFFICIENT
NOT_APPLICABLE
```

A content candidate is a bounded within-owner hypothesis. It is not proof of new-page need or future AI citation.

---

## 8A. Complete AI causal-result object

Every material selected case must preserve one causal object that survives into prioritization and client delivery:

```text
WHY SELECTED BEFORE AI
-> FROZEN SEARCH-ONLY DECISION
-> PRESERVED AI EVIDENCE
-> SEARCH-vs-AI COMPARISON
-> CHANGE | DE_RISK | NO_CHANGE | INSUFFICIENT
-> ARCHITECTURE EFFECT
-> CONTENT EFFECT
-> EXACT DOWNSTREAM ACTION OR EXPLICIT NO-ACTION
-> CLIENT-VISIBLE IMPLICATION
-> LIMITATION / RECHECK
```

```text
AI_NATIVE_VALUE != FACT_OF_AI_REQUESTS
SUPPORTED NO_CHANGE / DE_RISK != NO ANALYTICAL RESULT
```

A case may produce no new page or action and still be a material result when it confirms a frozen decision, reduces change risk or preserves uncertainty. Such a result must not disappear from downstream client views.
## 9. Confidence and claim governance

Confidence is categorical/evidence-derived; no magic numeric score is required.

A stronger confidence state requires direct evidence appropriate to the claimed scope. Missing family/temporal/source/target provenance mechanically narrows the allowed claim.

```text
CONFIDENCE LABEL MUST CHANGE WHAT MAY BE CLAIMED
```

---

## 10. Provider information-gain gate

Step17 normally reuses persisted Search + AI evidence. Fresh paid/quota-bearing acquisition is allowed only when:

```text
named missing evidence requirement exists
persisted evidence cannot answer it
new result could materially alter verdict/confidence/claim eligibility
exact provider surface is declared
cost/authorization gates pass
Bridge evidence is persisted/read back before another acquisition
```

No replay merely for “more confidence.”

---

## 11. Required durable outputs

Equivalent artifacts should preserve:

```text
pre-step/method review
research-to-execution schema / manifest
case comparison ledger
complete per-case causal-result ledger
direct source provenance ledger
claim-scope/confidence ledger
contract/requirement coverage audit
QA
report
current state / job-flow sync
```

Corrections must not silently overwrite historical accepted evidence.

---

## 12. Mandatory QA

```text
ALL SELECTED CASES ACCOUNTED = true
ALL CASES HAVE PRE_AI_SELECTION_RATIONALE = true
ALL CASES HAVE FROZEN_SEARCH_BASELINE = true
ALL CASES HAVE EXACT_ACTION_OR_EXPLICIT_NO_ACTION = true
ALL CASES HAVE_CLIENT_VISIBLE_IMPLICATION = true
SUPPORTED_NO_CHANGE_OR_DE_RISK_RESULTS_DROPPED = 0
ORDINARY SEARCH DIRECT TRACE COMPLETE = true
RAW AI TRACE COMPLETE = true
ARCHITECTURE VERDICT PRESENT = true
CONTENT VERDICT PRESENT = true
AI SCOPE CLASS PRESENT = true
AI TEMPORAL STATE PRESENT = true
CONFIDENCE / CLAIM BOUNDARY PRESENT = true
DECISIVE DIRECT SOURCE PROVENANCE MISSING = 0
UNSUPPORTED FAMILY-LEVEL CLAIMS = 0
UNSUPPORTED STABILITY CLAIMS = 0
SOURCE ORDER AS RANK CLAIMS = 0
URL/TITLE AS MATERIAL CONTENT PROOF = 0
PROXY SURFACE RELABELLED AS CONSUMER SURFACE = 0
ARCHITECTURE/CONTENT CONFLATIONS = 0
REVERSE TRACE MISSING = 0
BLOCKING ADVERSARIAL FINDINGS = 0
FINAL GITHUB READBACK = PASS
```

`ADVERSARIAL_SELF_REVIEW != INDEPENDENT_REVIEW`.

---

## 13. Acceptance meaning

A job may PASS as a **bounded diagnostic** with exact-query/snapshot evidence when every claim is bounded accordingly. A stronger user-job-family/longitudinal/architecture-CHANGE claim requires its stronger evidence gate.

---

## 14. Handoff to Step18

Pass the complete per-case causal object, not only terminal verdict fields:

```text
selection_rationale_before_ai
frozen_search_only_decision_ref
preserved_ai_evidence_ref
search_vs_ai_comparison
architecture_verdict
content_verdict
architecture_effect
content_effect
exact_downstream_action_or_explicit_no_action
client_visible_implication
ai_scope_class
ai_temporal_state
confidence_state
evidence_limitations
recheck_trigger
```

```text
EXACT_QUERY_DIAGNOSTIC + SINGLE_SNAPSHOT
= DIAGNOSTIC SUPPORTING EVIDENCE
!= STABLE FIRST-PARTY AI VISIBILITY MEASUREMENT
```

---

## 15. Permanent markers

```text
KW001_STEP17_METHOD_ACTIVE = true
KW001_STEP17_JOB_SPECIFIC_RESULTS_FORBIDDEN_IN_PERMANENT_METHOD = true
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
KW001_STEP17_DECISIVE_DIRECT_READ_PROVENANCE_REQUIRED = true
KW001_STEP17_CONFIDENCE_MUST_CHANGE_ALLOWED_CLAIM = true
KW001_STEP17_NO_MAGIC_NUMERICAL_CONFIDENCE_SCORE = true
KW001_STEP17_BASE_DIAGNOSTIC_PASS_WITHOUT_PRIVATE_ACCESS_ALLOWED = true
KW001_STEP17_PROVIDER_REPLAY_REQUIRES_INFORMATION_GAIN = true
KW001_STEP17_COMPLETE_AI_CAUSAL_RESULT_OBJECT_REQUIRED = true
KW001_STEP17_AI_NATIVE_VALUE_NOT_EQUAL_REQUEST_FACT = true
KW001_STEP17_SUPPORTED_NO_CHANGE_AND_DE_RISK_MUST_REACH_CLIENT = true
KW001_STEP17_EXACT_ACTION_OR_EXPLICIT_NO_ACTION_REQUIRED = true
```

This file follows `PERMANENT_STEP_RULE_UNIVERSALITY_AND_JOB_SEPARATION_GATE.md`.

## ПРОСТЫМИ СЛОВАМИ

Step17 сравнивает уже проверенную картину обычного поиска с ограниченной AI-проверкой. Один AI-ответ показывает только то, что случилось для конкретного запроса в конкретный момент; он не доказывает поведение всей темы и не даёт права автоматически перестраивать сайт. Поэтому отдельно проверяются изменения структуры и идеи по улучшению содержания, а сила вывода всегда ограничивается реальной шириной и повторяемостью доказательств.
