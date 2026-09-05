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

## 5. AI research knowledge handoff validation

When an artifact is intended to transfer completed research knowledge to another AI/LLM, Step20 must test that actual recipient task in a clean context.

The intended purpose must be explicit:

```text
TRANSFER COMPLETED RESEARCH KNOWLEDGE
-> USER SUPPLIES A NEW TASK
-> NEW AI USES THE RESEARCH RESULTS FOR THAT TASK
```

For this artifact class, the following are not equivalent:

```text
AI RESEARCH KNOWLEDGE HANDOFF
!= INTERNAL EXECUTION HANDOFF

AI KNOWLEDGE DOCUMENT
!= EXECUTION CURSOR

MACHINE-READABLE
!= LLM-USABLE

JSON_PARSE_PASS
!= AI_HANDOFF_PASS

ALL DATA PRESENT
!= RESEARCH MEANING RECOVERABLE
```

### 5.1 Primary-format validation

Do not accept a primary physical format merely because it is easy to serialize or count.

For an LLM-oriented research/context handoff, Markdown is the default primary format unless the deliverable contract demonstrates that another physical format is equally or more usable for the target AI environment.

Structured JSON/CSV/TSV may be companion data layers. If a non-Markdown format is the sole primary artifact, QA must validate the reason for that choice and prove equivalent context comprehension.

### 5.2 Clean-context walkthrough

Use a fresh AI context that has no repository history, prior chat context, execution cursor or hidden project state. Supply only the promised primary AI knowledge artifact plus the explicit recipient task.

The walkthrough must verify that the AI can correctly recover, where applicable:

```text
WHAT WAS RESEARCHED
BUSINESS / SITE / SCOPE
RESEARCH PURPOSE
EVIDENCE CLASSES AND METHOD
CURRENT ACCEPTED MODEL / AUTHORITIES
MATERIAL FINDINGS
WHY MATERIAL DECISIONS WERE MADE
ORDINARY SEARCH CONTRIBUTION AND BOUNDARIES
AI CAUSAL CONTRIBUTION AND DECISION DELTA
KEEP / RETAIN / NO_CHANGE / DE_RISK RESULTS
SUPPORTED CHANGES
UNCERTAINTY / HOLD / RECHECK / SEARCH_REQUIRED
FORBIDDEN OR UNSUPPORTED CLAIMS
```

Then test realistic user-directed tasks such as:

```text
EXPLAIN WHY A MATERIAL DECISION EXISTS
DISTINGUISH NO_CHANGE FROM HOLD / RECHECK
IDENTIFY WHAT SEARCH EVIDENCE SUPPORTS AND WHERE ITS BOUNDARY ENDS
EXPLAIN AN AI CASE AND ITS DECISION DELTA
USE THE RESEARCH CONTEXT IN A NEW DERIVED USER TASK
REFUSE TO INVENT A MISSING FACT
```

The AI must not require internal Stage/Step reconstruction to perform these tasks.

### 5.3 Non-purpose boundary

For a research handoff, loading the artifact alone must not cause or imply automatic continuation of an internal roadmap, next-stage execution or checkpoint recovery.

```text
USER-SUPPLIED NEW TASK REQUIRED
```

If an execution handoff is separately promised, it must be a separately declared artifact/contract with its own acceptance universe.

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
AI_HANDOFF_CLEAN_CONTEXT_QA = PASS when AI research handoff promised
AI_HANDOFF_PRIMARY_FORMAT_JUSTIFIED = true when AI research handoff promised
AI_HANDOFF_NOT_CONFLATED_WITH_EXECUTION_STATE = true when AI research handoff promised
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
MACHINE-READABLE != LLM-USABLE
JSON_PARSE_PASS != AI_HANDOFF PASS
AI RESEARCH HANDOFF != EXECUTION CHECKPOINT
ANALYST QA != OWNER ACCEPTANCE
```

## 11. Non-repeat purpose

The goal is to catch the defect **before release** that an owner would otherwise find only after opening and trying to use the actual deliverable.

Step20 must therefore perform the recipient task, not merely verify the artifact.

This file follows `PERMANENT_STEP_RULE_UNIVERSALITY_AND_JOB_SEPARATION_GATE.md`.
