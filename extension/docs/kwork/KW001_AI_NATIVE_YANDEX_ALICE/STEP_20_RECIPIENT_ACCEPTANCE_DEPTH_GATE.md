# KW-001 — Step 20 recipient acceptance depth gate

Updated: 2026-09-05  
Status: **ACTIVE / UNIVERSAL / OWNER-DIRECTED PERMANENT NON-REPEAT CONTROL**  
Scope: **Step 20 companion gate / Level 1**

This gate supplements `STEP_20_FINAL_QA_AND_RELEASE_ASSURANCE_METHOD.md`. It addresses a post-release failure class where physical, canonical and package-wide QA could all pass while the owner later found material defects in recipient-facing completeness and implementability.

Concrete job/domain values belong only in Level2.

## 1. Failure class — package acceptance substituted for recipient-specific acceptance

```text
PACKAGE CONTAINS THE REQUIRED KNOWLEDGE
!= REQUIRED RECIPIENT ARTIFACT FULFILLS ITS OWN CONTRACT

INTERNAL PRODUCT QA PASS
!= OWNER / COMMISSIONER ACCEPTANCE
```

A result cannot be called fully client-accepted merely because the analyst can trace missing detail to another package artifact.

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

## 5. Workbook recipient-usability validation

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

## 6. Language/localization QA

Search recipient-facing text for unexplained internal-language leakage when a language contract exists.

Do not restrict language QA to headings. Check action explanations, reasons, target states, evidence descriptions, limitations, acceptance instructions, table labels and workbook front-door surfaces.

Technical identifiers may remain immutable; explanatory prose must obey the recipient contract.

## 7. Search and AI visibility QA

When Search or AI contribution is part of the product promise, verify the recipient artifact contains decision-useful evidence, not only aggregate counts or a statement that a ledger exists.

```text
SEARCH CASES INTERNAL ONLY => RECIPIENT-VISIBILITY FAIL when Search research is promised
AI VERDICT COUNTS ONLY => RECIPIENT-VISIBILITY FAIL when AI causal contribution is promised
```

## 8. Owner / commissioner acceptance boundary

For external/client-facing delivery, distinguish:

```text
ANALYST_ASSURANCE_PASS
OWNER_OR_COMMISSIONER_ACCEPTANCE
```

If owner/commissioner review is outside the currently authorized step, the release state must preserve that boundary. Do not use wording equivalent to `FINAL CLIENT ACCEPTANCE COMPLETE` unless the required recipient acceptance actually occurred or the contract explicitly makes analyst assurance sufficient.

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

## 9. Hard PASS gate

Applicable product/deliverable acceptance requires:

```text
EACH_PROMISED_RECIPIENT_ARTIFACT_CONTRACT = PASS
RECIPIENT_LANGUAGE_QA = PASS
RESEARCH_DEPTH_QA = PASS when full research promised
SPECIALIST_EXECUTABILITY_QA = PASS when implementation guide promised
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
ANALYST QA != OWNER ACCEPTANCE
```

## 10. Non-repeat purpose

The goal is to catch the defect **before release** that an owner would otherwise find only after opening and trying to use the actual deliverable.

Step20 must therefore perform the recipient task, not merely verify the artifact.

This file follows `PERMANENT_STEP_RULE_UNIVERSALITY_AND_JOB_SEPARATION_GATE.md`.
