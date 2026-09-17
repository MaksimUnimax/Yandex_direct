# KW-002 — LEVEL 1 PRE-STEP EXTERNAL RESEARCH AND SOURCE DISCLOSURE RULE

Status: **ACTIVE / OWNER-LOCKED / REQUIRED / MAIN-CHAT-GOVERNANCE**  
Owner instruction: 2026-09-09  
Owner clarification: 2026-09-11 — plain-language summary must be real plain Russian.  
Role-boundary clarification: 2026-09-17 — **MAIN CHAT PERFORMS THIS RESEARCH/DISCLOSURE BEFORE WORK RELEASE; CHATGPT WORK DOES NOT REPEAT IT DURING ORDINARY EXECUTION.**

## 1. Purpose

Before every major KW-002 roadmap step, Main Chat must check the proposed method against fresh external internet sources relevant to that exact step.

```text
INTERNAL RUNBOOK = PROCESS AUTHORITY
INTERNAL RUNBOOK != INDEPENDENT METHOD PROOF
PAST WEB RESEARCH != AUTOMATICALLY FRESH ENOUGH
```

The owner must be able to inspect the cited basis directly from chat before execution is released.

## 2. Exact role boundary

```text
MAIN CHAT
= FRESH EXTERNAL RESEARCH
+ SOURCE→METHOD TRACE
+ OWNER-FACING CLICKABLE DISCLOSURE
+ PLAIN-LANGUAGE PRE-STEP REPORT
+ RELEASE DECISION

CHATGPT WORK
= EXECUTE THE ALREADY-RELEASED CONTRACT
```

The gate condition is:

```text
MAIN CHAT COMPLETES RESEARCH/DISCLOSURE
→ ONLY THEN MAY WORK EXECUTION BEGIN
```

This does **not** mean Work itself must redo the research/disclosure.

By default, ordinary Work execution MUST NOT be instructed to:

- search the web again for methodology;
- re-evaluate the method against external sources;
- show the owner clickable source disclosure;
- produce the owner-facing pre-step report;
- decide whether Main Chat's release was valid.

Exception: a Work task whose explicit purpose is methodology/research/audit may of course perform research because that is the task itself.

## 3. Mandatory Main Chat pre-step research

Before release of every major step, Main Chat must:

1. define the exact methodological/provider questions;
2. search the current internet for sources answering them;
3. read relevant source material, not just snippets;
4. prefer current official/primary documentation;
5. add strong industry corroboration where official guidance does not define the analytical method;
6. compare sources with the project method;
7. correct/rework the method if evidence exposes a defect;
8. persist source→method trace in the step preparation/release artifact;
9. show clickable source list + supported claim directly in owner-facing chat;
10. only then release execution.

## 4. Source priority

Use the strongest source available:

```text
1. OFFICIAL PROVIDER / SEARCH ENGINE DOCUMENTATION
2. OFFICIAL PRODUCT / API / POLICY / PRICING DOCUMENTATION
3. PRIMARY TECHNICAL / STANDARDS SOURCES
4. HIGH-QUALITY INDUSTRY PRACTICE / SPECIALIST METHODOLOGY
5. PROJECT_TEST_VALIDATED EVIDENCE
6. ANALYST HEURISTIC — clearly labelled
```

No arbitrary source-count target exists. Enough sources means every material method question has adequate support or an explicit evidence gap.

## 5. Mandatory owner-facing disclosure by Main Chat

The pre-step chat must contain a visible section equivalent to:

`ИСТОЧНИКИ / МАТЕРИАЛЫ, КОТОРЫЕ Я ИЗУЧИЛ ПЕРЕД ШАГОМ`

For every material source show:

```text
SOURCE TITLE
PUBLISHER / SOURCE CLASS
CLICKABLE URL
DATE/FRESHNESS when material
WHAT EXACTLY IT SUPPORTS
HOW IT CONFIRMS / CHANGES THE STEP METHOD
LIMITATION / WHAT IT DOES NOT PROVE
```

A source name without a clickable link is insufficient.
A raw URL without supported-claim explanation is insufficient.

## 6. Durable research trace

Every major job-level pre-step/release artifact must preserve at least:

```text
source_id
source_title
publisher
source_class
url
checked_at
method_element_supported
exact_claim_supported
project_specific_application
claim_boundary
```

If one source supports several method elements, retain that mapping.

## 7. Freshness

Refresh research for materially changing topics such as:

- provider/API capabilities;
- pricing/quotas/limits;
- search-engine features;
- AI-search behavior;
- laws/policies;
- product functionality;
- current SEO/search guidance.

Do not reuse an earlier chat's web check automatically.

## 8. If no adequate external source exists

Still perform the search.

Record explicitly:

```text
NO ADEQUATE EXTERNAL SOURCE FOUND
SOURCE_CLASS = PROJECT_TEST_VALIDATED | ANALYST_HEURISTIC | OWNER_SCOPE_RULE
```

Then state whether the gap requires HOLD, controlled experiment, provider check, owner decision or bounded project heuristic.

Never fabricate a source.

## 9. Provider-step special requirement

When a future step uses Yandex Marketing Bridge or another provider, Main Chat's pre-release research must verify material current items such as:

- operation/method semantics;
- request/response fields;
- region/device/operators;
- limits/depth/pagination;
- pricing/quota/cost;
- current provider capability boundaries.

Separately verify the Bridge's current repository capability.

```text
PROVIDER DOCS != BRIDGE CAPABILITY PROOF
BRIDGE TESTS != CURRENT PROVIDER DOCS
```

Again, Work does not redo this check unless its task explicitly is provider/method auditing.

## 10. Analytical SEO-step requirement

For steps such as seed design, cleanup, intent, clustering, page ownership, competitor expansion or AI-search reconciliation, Main Chat distinguishes:

```text
OFFICIAL SEARCH-ENGINE GUIDANCE where relevant
+
HIGH-QUALITY INDUSTRY PRACTICE where official material is incomplete
+
CURRENT PROJECT EVIDENCE
```

Third-party industry practice must not be presented as an official Yandex rule.

## 11. Required Main Chat pre-step report structure

Before release, the owner-facing chat must show an equivalently complete structure:

```text
WHOLE KWORK GOAL
FULL ROADMAP
COMPLETED
REMAINING
CURRENT STEP GOAL
WHAT PROBLEM THE STEP SOLVES
REQUIRED OUTPUT
RELEVANT PRIOR ERRORS
NON-REPEAT CONTROLS
FRESH INTERNET RESEARCH
CLICKABLE SOURCE LIST + WHAT EACH SUPPORTS
SOURCE→METHOD TRACE
METHOD / EXECUTION PLAN
BRIDGE/WORK GATE if applicable
PASS CONDITIONS
ПРОСТЫМИ СЛОВАМИ: WHY / WHAT / RESULT / BLOCKER / NEXT ACTION
```

The plain-language block must be normal conversational Russian and must explain:

1. why the step is needed;
2. what will/was done;
3. what result will be obtained and why it matters;
4. whether execution may continue;
5. blocker if not;
6. next physical action.

Technical hashes/IDs/status dumps do not satisfy this requirement.

## 12. PASS / FAIL

Main Chat may release execution only when:

```text
PRE_STEP_EXTERNAL_RESEARCH = PASS
SOURCE_DISCLOSURE_IN_CHAT = PASS
SOURCE_TO_METHOD_TRACE = PASS
PLAIN_LANGUAGE_SUMMARY = PASS
MAIN_CHAT_EXECUTION_RELEASE_ALLOWED = true
```

Fail if any material method claim lacks adequate support without an explicit evidence gap, sources lack clickable links/explanation, or the owner-facing/plain-language sections are missing.

## 13. Work runtime statement

Once Main Chat release is PASS:

```text
DO NOT SEND THIS WHOLE GATE TO WORK AS RUNTIME WORK
```

Work receives the canonical task prompt containing the resulting execution method and claim boundaries.

Work may perform only the narrow release/input freshness check required by its prompt.

## 14. Markers

```text
KW002_PRE_STEP_INTERNET_RESEARCH_REQUIRED_FOR_MAIN_CHAT = true
KW002_PRE_STEP_CLICKABLE_SOURCE_DISCLOSURE_REQUIRED_IN_MAIN_CHAT = true
KW002_SOURCE_TO_METHOD_EXPLANATION_REQUIRED = true
KW002_STALE_WEB_RESEARCH_NOT_AUTOMATICALLY_REUSABLE = true
KW002_OWNER_FACING_PLAIN_LANGUAGE_SUMMARY_REQUIRED = true
KW002_EXECUTION_BLOCKED_UNTIL_MAIN_CHAT_SOURCE_DISCLOSURE = true
KW002_WORK_MUST_NOT_REPEAT_PRE_STEP_RESEARCH_BY_DEFAULT = true
KW002_WORK_MUST_NOT_REPEAT_OWNER_SOURCE_DISCLOSURE = true
KW002_WORK_MUST_NOT_REPEAT_MAIN_CHAT_RELEASE_REPORT = true
```
