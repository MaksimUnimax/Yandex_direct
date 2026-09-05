# KW-001 — Step 20 recipient acceptance depth gate

Updated: 2026-09-05  
Status: **ACTIVE / UNIVERSAL / OWNER-DIRECTED PERMANENT NON-REPEAT CONTROL**  
Scope: **Step 20 companion gate / Level 1**

This gate supplements `STEP_20_FINAL_QA_AND_RELEASE_ASSURANCE_METHOD.md`. It addresses a post-release failure class where physical, canonical and package-wide QA could all pass while the owner later found material defects in recipient-facing completeness, implementability or AI-recipient usability.

Concrete job/domain values belong only in Level2.

## 1. Failure class — package acceptance substituted for recipient-specific acceptance

```text
PACKAGE CONTAINS THE REQUIRED KNOWLEDGE
!= REQUIRED RECIPIENT ARTIFACT FULFILLS ITS OWN CONTRACT

INTERNAL PRODUCT QA PASS
!= OWNER / COMMISSIONER ACCEPTANCE
```

A result cannot be called fully accepted merely because the analyst can trace missing detail to another package artifact.

## 2. Recipient-specific QA universes

Before product/deliverable QA, derive a separate acceptance universe for every promised recipient artifact, for example:

```text
CLIENT RESEARCH REPORT
SPECIALIST IMPLEMENTATION GUIDE
AI / MACHINE KNOWLEDGE ARTIFACT
WORKBOOK / DATA INTERFACE
DELIVERY / README SURFACE
```

For each artifact declare:

```text
INTENDED RECIPIENT
INTENDED DECISIONS / TASKS
PROMISED DEPTH
LANGUAGE CONTRACT
MANDATORY EVIDENCE VISIBILITY
MANDATORY IMPLEMENTATION DETAIL
ALLOWED CROSS-REFERENCES
WHAT MUST BE SELF-CONTAINED
PRIMARY PHYSICAL FORMAT AND WHY IT FITS THE RECIPIENT
WHAT THE ARTIFACT IS EXPLICITLY NOT FOR
```

A different artifact may supplement the recipient view, but may not silently satisfy a requirement declared self-contained in the current artifact.

## 3. Depth validation for research reports

QA must test material findings, not only section existence.

For a full research report, choose the complete material finding universe when bounded, or a declared risk-based set plus all high-risk findings when not practical. Verify that the recipient can recover an equivalent chain:

```text
QUESTION
-> CURRENT STATE
-> EVIDENCE
-> INTERPRETATION
-> DECISION
-> TARGET STATE / ACTION OR NO-ACTION
-> LIMITATION
```

A report consisting primarily of an executive summary plus top recommendations cannot pass a `FULL RESEARCH REPORT` contract solely because the complete chain exists in an internal master report.

## 4. Specialist executability validation

For every work item claimed READY, Step20 must test the applicable execution mode rather than merely check that a standard set of fields is non-empty.

Verify:

```text
IMPLEMENTATION_MODE IS EXPLICIT
REAL-SITE CHANGE YES/NO IS RESOLVED
LOCATION / PLACEMENT IS SUFFICIENT FOR THE MODE
EVIDENCE MEANING IS HUMAN-READABLE
ACCEPTANCE TEST MATCHES THE ACTUAL CHANGE
RECIPIENT LANGUAGE IS COMPLIANT
```

Routing/link/ownership rows require their own mode-specific tests.

## 5. AI site-specific SEO consultant validation

When an AI artifact is intended to let a non-specialist client implement confirmed recommendations through an AI assistant, Step20 must test that exact client scenario.

The intended function is:

```text
CLIENT LOADS ONE SELF-CONTAINED AI ARTIFACT
-> AI BECOMES A SITE-SPECIFIC SEO IMPLEMENTATION CONSULTANT
-> CLIENT ASKS QUESTIONS IN ORDINARY LANGUAGE
-> AI EXPLAINS WHAT / WHY / HOW / WHAT NOT TO BREAK / HOW TO CHECK
-> CLIENT IMPLEMENTS THE CONFIRMED SITE CHANGES
```

If a human-specialist implementation guide exists in parallel, both recipient paths must represent the same confirmed workset.

```text
HUMAN SPECIALIST PATH WORKSET
== AI CONSULTANT PATH CONFIRMED WORKSET
```

The AI artifact is not accepted if it merely acts as an archive/reference and cannot support practical implementation.

### 5.1 Internal-execution boundary

The AI may guide the client's **site implementation progress**. That must not be confused with the analyst's internal research roadmap.

```text
AI CLIENT IMPLEMENTATION CONSULTANT
!= INTERNAL RESEARCH EXECUTION HANDOFF

CLIENT SITE IMPLEMENTATION PROGRESS
!= INTERNAL ROADMAP CHECKPOINT

AI KNOWLEDGE DOCUMENT
!= EXECUTION_CURSOR
```

A client question such as “I completed part of the work; what should I do next?” must be interpreted against the confirmed implementation workset, dependencies and priorities—not against internal Stage/Step state.

### 5.2 Primary-format validation

Do not accept a primary physical format merely because it is easy to serialize or count.

For an LLM-oriented consultant/context artifact, Markdown is the default primary format unless the deliverable contract demonstrates that another physical format is equally or more usable for the target AI environment.

Structured JSON/CSV/TSV may be companion data layers. If a non-Markdown format is the sole primary artifact, QA must validate why it better serves the client-consultation task and prove equivalent practical consultation quality.

```text
MACHINE-READABLE != AI-CONSULTANT-USABLE
JSON_PARSE_PASS != AI-CONSULTANT PASS
ALL DATA PRESENT != PRACTICAL IMPLEMENTATION GUIDANCE RECOVERABLE
```

### 5.3 Strict offline / clean-context walkthrough

Use a fresh/local AI context with:

```text
NO PREVIOUS CHAT
NO GITHUB
NO INTERNAL PROJECT FILES
NO LIVE SITE
NO INTERNET
NO SEARCH ENGINE
NO PROVIDER / API
ONLY THE PROMISED FINAL AI ARTIFACT
```

Ask practical plain-language client questions. Verify that the AI can correctly:

```text
EXPLAIN WHAT IS WRONG ON A MATERIAL PAGE
EXPLAIN WHAT IS ALREADY CORRECT AND MUST NOT BE BROKEN
EXPLAIN WHY THE FINDING EXISTS
EXPLAIN THE SUPPORTING EVIDENCE AND ITS LIMITS
GIVE A STEP-BY-STEP IMPLEMENTATION PATH
IDENTIFY RELEVANT / EXCLUDED QUERIES OR TOPICS WHEN MATERIAL
EXPLAIN PAGE / BLOCK / LINK RELATIONSHIPS
CREATE A CLEAR TASK FOR A DEVELOPER OR WRITER WHEN SUPPORTED
EXPLAIN PRIORITY / DEPENDENCIES
EXPLAIN THE ACCEPTANCE CHECK
HANDLE “I COMPLETED PART OF THE WORK; WHAT CONFIRMED STEP IS NEXT?”
DISTINGUISH READY / NO_CHANGE / HOLD / RECHECK / SEARCH_REQUIRED
EXPLAIN ORDINARY SEARCH AND AI-SEARCH CONTRIBUTION
REFUSE TO INVENT A MISSING FACT
```

The AI must not require the client to understand specialist terminology or the internal research repository to follow the instructions.

### 5.4 Reasoning-depth validation

The AI artifact cannot be only an instruction list. Test that the model can explain the reasoning behind a recommendation and adapt that explanation to a client question while remaining inside the accepted evidence boundary.

For material decisions, the artifact should support an equivalent chain:

```text
CURRENT FACT / STATE
-> USER TASK / QUERY CONTEXT
-> EVIDENCE
-> INTERPRETATION
-> CONFIRMED DECISION
-> WHY
-> TARGET STATE
-> IMPLEMENTATION ACTION
-> DEPENDENCIES / DO-NOT-BREAK BOUNDARY
-> ACCEPTANCE CHECK
-> LIMITATION / REOPEN CONDITION
```

### 5.5 Fail conditions

The AI consultant artifact fails if any applicable condition is true:

```text
ARCHIVE_ONLY_NOT_PRACTICAL_CONSULTANT
KNOWS_WHAT_BUT_CANNOT_EXPLAIN_WHY
UNDERSTANDS_PROBLEM_BUT_CANNOT_EXPLAIN_HOW_STEP_BY_STEP
CANNOT_BIND_GUIDANCE_TO_CONCRETE_PAGE_QUERY_BLOCK_OR_RELATIONSHIP
CANNOT_EXPLAIN_POSITIVE_KEEP_NO_CHANGE
CANNOT_CREATE_CLEAR_IMPLEMENTER_TASK_WHEN SUPPORTED
CANNOT_EXPLAIN_PRIORITY_OR_DEPENDENCIES
CANNOT_EXPLAIN_ACCEPTANCE_CHECK
REQUIRES_EXTERNAL_ACCESS_FOR_INFORMATION_THAT_SHOULD_BE_SELF_CONTAINED
INVENTS_MISSING_FACTS
CONFUSES_FACT / ANALYTICAL_CONCLUSION / LIMITATION / UNCERTAINTY
AI_WORKSET_DIFFERS_FROM_CONFIRMED_HUMAN_SPECIALIST_WORKSET
CLIENT_MUST_ALREADY_KNOW_SEO_TO_USE_THE_GUIDANCE
CONFUSES_CLIENT_IMPLEMENTATION_PROGRESS_WITH_INTERNAL_RESEARCH_ROADMAP
```

## 6. Workbook recipient-usability validation

Workbook QA has two separate verdicts:

```text
DATA / AUTHORITY QA
RECIPIENT-USABILITY QA
```

Recipient-usability must test actual tasks, such as finding a decision, understanding why it exists, distinguishing ready/no-change/hold, locating evidence and determining the next action without repository joins.

```text
RENDER PASS + FORMULA PASS + COUNT PASS
!= WORKBOOK RECIPIENT-USABILITY PASS
```

## 7. Language/localization QA

Search recipient-facing text for unexplained internal-language leakage when a language contract exists.

Do not restrict language QA to headings. Check action explanations, reasons, target states, evidence descriptions, limitations, acceptance instructions, table labels and workbook front-door surfaces.

Technical identifiers may remain immutable; explanatory prose must obey the recipient contract.

## 8. Search and AI visibility QA

When Search or AI contribution is part of the product promise, verify the recipient artifact contains decision-useful evidence, not only aggregate counts or a statement that a ledger exists.

```text
SEARCH CASES INTERNAL ONLY => RECIPIENT-VISIBILITY FAIL when Search research is promised
AI VERDICT COUNTS ONLY => RECIPIENT-VISIBILITY FAIL when AI causal contribution is promised
```

## 9. Owner / commissioner acceptance boundary

For external/client-facing delivery, distinguish:

```text
ANALYST_ASSURANCE_PASS
OWNER_OR_COMMISSIONER_ACCEPTANCE
```

If owner/commissioner review is outside the currently authorized step, the release state must preserve that boundary. Do not use wording equivalent to `FINAL RECIPIENT ACCEPTANCE COMPLETE` unless the required recipient acceptance actually occurred or the contract explicitly makes analyst assurance sufficient.

If a later owner review finds material recipient defects:

```text
OWNER_REVIEW_FINDING
-> OPEN REWORK OVERLAY
-> INVALIDATE FINAL RECIPIENT-ACCEPTANCE CLAIM
-> PRESERVE HISTORICAL TECHNICAL RELEASE PROVENANCE
-> CORRECT AFFECTED RECIPIENT ARTIFACTS
-> RERUN RECIPIENT-SPECIFIC QA
-> OWNER/COMMISSIONER RECHECK WHEN REQUIRED
```

## 10. Hard PASS gate

Applicable product/deliverable acceptance requires:

```text
EACH_PROMISED_RECIPIENT_ARTIFACT_CONTRACT = PASS
RECIPIENT_LANGUAGE_QA = PASS
RESEARCH_DEPTH_QA = PASS when full research promised
SPECIALIST_EXECUTABILITY_QA = PASS when implementation guide promised
AI_SITE_SPECIFIC_SEO_CONSULTANT_QA = PASS when AI consultant artifact promised
AI_CLIENT_CAN_IMPLEMENT_WITHOUT_SPECIALIST_KNOWLEDGE = true when promised
AI_WORKSET_EQUALS_CONFIRMED_SPECIALIST_WORKSET = true when parallel paths promised
AI_OFFLINE_SELF_CONTAINED = true when promised
AI_CAN_EXPLAIN_WHY_AND_HOW = true
AI_CAN_EXPLAIN_ACCEPTANCE_CHECK = true
AI_PRIMARY_FORMAT_JUSTIFIED = true
AI_INTERNAL_ROADMAP_CONFLATION = 0
WORKBOOK_RECIPIENT_USABILITY_QA = PASS when workbook promised
SEARCH_AI_VISIBILITY_QA = PASS when in scope
OWNER_ACCEPTANCE_STATE = TRUTHFULLY_DECLARED
```

Hard non-equivalences:

```text
PACKAGE-WIDE PASS != RECIPIENT-SPECIFIC PASS
SECTION EXISTS != REQUIRED DEPTH EXISTS
FIELDS NONEMPTY != TASK EXECUTABLE
VISUAL PASS != WORKBOOK USABILITY PASS
MACHINE-READABLE != AI-CONSULTANT-USABLE
JSON_PARSE_PASS != AI-CONSULTANT PASS
AI CLIENT IMPLEMENTATION CONSULTANT != INTERNAL RESEARCH EXECUTION CHECKPOINT
ANALYST QA != OWNER ACCEPTANCE
```

## 11. Non-repeat purpose

The goal is to catch the defect **before release** that an owner would otherwise find only after opening and trying to use the actual deliverable.

Step20 must therefore perform the recipient task, not merely verify the artifact.

This file follows `PERMANENT_STEP_RULE_UNIVERSALITY_AND_JOB_SEPARATION_GATE.md`.
