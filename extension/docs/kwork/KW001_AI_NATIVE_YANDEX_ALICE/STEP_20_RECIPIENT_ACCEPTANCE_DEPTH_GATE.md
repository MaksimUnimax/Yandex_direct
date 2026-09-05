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

A different artifact may supplement the recipient view only when the contract permits it; it may never silently satisfy information declared self-contained in the current artifact.

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

## 5. AI artifact — independence and self-containment validation

When an AI artifact is promised as a self-contained way to use the completed research, Step20 must test **independence first**.

The exact hard scenario is:

```text
SEPARATE / LOCAL LLM
NO PREVIOUS CHAT
NO GITHUB
NO INTERNAL PROJECT FILES
NO LIVE SITE
NO INTERNET
NO SEARCH ENGINE
NO EXTERNAL PROVIDER / API
ONLY THE PROMISED FINAL AI ARTIFACT
```

The AI artifact passes only if, in that environment, the model can explain the completed research and the confirmed implementation work at the promised depth without needing another source that the artifact should contain.

The model must be able to recover and explain:

```text
WHAT WAS RESEARCHED
WHAT WAS FOUND
WHAT IS ALREADY CORRECT
WHAT IS WRONG / INSUFFICIENT
WHY EACH MATERIAL FINDING EXISTS
WHAT EVIDENCE SUPPORTS IT
WHAT MUST REMAIN UNCHANGED
WHAT SHOULD BE CHANGED
WHERE THE CHANGE APPLIES
HOW THE CONFIRMED CHANGE SHOULD BE PERFORMED
HOW TO CHECK THE RESULT
WHAT REMAINS UNCERTAIN / UNRESOLVED
```

```text
SELF-CONTAINED = CAN ANSWER FROM THE ARTIFACT ITSELF
NOT = CAN FIND THE ANSWER SOMEWHERE ELSE IN THE PACKAGE
```

### 5.1 Practical plain-language walkthrough

Ask a fresh model practical client questions without specialist terminology. Verify that the AI can correctly:

```text
EXPLAIN THE RESEARCH SCOPE
EXPLAIN A MATERIAL FINDING ON A PAGE / TOPIC
EXPLAIN WHAT IS ALREADY CORRECT AND MUST NOT BE BROKEN
EXPLAIN WHY THE FINDING EXISTS
EXPLAIN THE SUPPORTING EVIDENCE AND ITS LIMITS
EXPLAIN WHAT SHOULD BE CHANGED
EXPLAIN WHERE THE CHANGE APPLIES
EXPLAIN HOW A HUMAN WITH SITE ACCESS SHOULD IMPLEMENT IT
IDENTIFY RELEVANT / EXCLUDED QUERIES OR TOPICS WHEN MATERIAL
EXPLAIN PAGE / BLOCK / LINK RELATIONSHIPS
CREATE A CLEAR TASK FOR A DEVELOPER OR WRITER WHEN SUPPORTED
EXPLAIN PRIORITY / DEPENDENCIES WHEN PROVEN
EXPLAIN THE ACCEPTANCE CHECK
DISTINGUISH READY / NO_CHANGE / HOLD / RECHECK / SEARCH_REQUIRED
EXPLAIN ORDINARY SEARCH AND AI-SEARCH CONTRIBUTION
REFUSE TO INVENT A MISSING FACT
```

If a material accepted finding exists elsewhere in the package but is not recoverable from the promised AI artifact itself, the AI artifact fails.

### 5.2 Reasoning-depth validation

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
-> WHERE IT APPLIES
-> DEPENDENCIES / DO-NOT-BREAK BOUNDARY
-> ACCEPTANCE CHECK
-> LIMITATION / REOPEN CONDITION
```

### 5.3 AI consultation is not direct site modification

The artifact equips the AI to explain `WHAT / WHY / WHERE / HOW`. It does not by itself grant CMS, code, server or account access.

```text
AI EXPLAINS IMPLEMENTATION
!= AI PHYSICALLY MODIFIES THE SITE
```

The physical change is performed by a human or separately authorized system with the required access.

### 5.4 Internal-execution boundary

The AI artifact must not be confused with the analyst's internal research roadmap.

```text
AI RESEARCH / IMPLEMENTATION CONSULTANT
!= INTERNAL RESEARCH EXECUTION HANDOFF

AI KNOWLEDGE DOCUMENT
!= EXECUTION_CURSOR
```

### 5.5 One-document contract validation

If the job promises **one final self-contained AI document**, QA must enforce that literally.

```text
ONLY ONE FINAL AI DOCUMENT PROVIDED
NO SECOND CONTEXT FILE
NO REQUIRED COMPANION JSON/CSV/TSV/XLSX/PDF
NO GITHUB / CHAT / INTERNAL FILE DEPENDENCY
```

A model that needs a second file to explain a material finding or confirmed change causes FAIL.

Where the contract specifically names Markdown as the corrected AI format, QA must test that one Markdown file as the entire recipient input.

```text
SECOND FILE REQUIRED != SELF-CONTAINED PASS
ALL DATA SOMEWHERE IN PACKAGE != ONE-DOCUMENT PASS
JSON_PARSE_PASS != AI KNOWLEDGE PASS
```

### 5.6 Workset reconciliation

If a human-specialist implementation guide exists in parallel, the confirmed analytical workset represented by the AI artifact must reconcile with it.

```text
HUMAN SPECIALIST CONFIRMED WORKSET
== AI ARTIFACT CONFIRMED WORKSET
```

This does not mean the AI artifact can rely on the specialist guide at runtime. Reconciliation is a QA operation performed before delivery; the final AI recipient still receives only the artifact promised by its own contract.

### 5.7 Fail conditions

The AI artifact fails if any applicable condition is true:

```text
CANNOT EXPLAIN A MATERIAL RESEARCH FINDING FROM THE ARTIFACT ALONE
CANNOT EXPLAIN A MATERIAL POSITIVE / KEEP RESULT
KNOWS WHAT BUT CANNOT EXPLAIN WHY
UNDERSTANDS THE PROBLEM BUT CANNOT EXPLAIN HOW AT THE PROVEN DETAIL LEVEL
CANNOT BIND GUIDANCE TO THE CONCRETE PAGE / QUERY / BLOCK / RELATIONSHIP WHEN THAT IS PROVEN
CANNOT EXPLAIN ACCEPTANCE CHECK
REQUIRES A SECOND FILE FOR KNOWLEDGE PROMISED AS SELF-CONTAINED
REQUIRES GITHUB / PREVIOUS CHAT / INTERNAL PROJECT FILES
REQUIRES EXTERNAL ACCESS FOR INFORMATION THAT SHOULD HAVE BEEN INCLUDED
INVENTS MISSING FACTS OR IMPLEMENTATION DETAIL
CONFUSES FACT / ANALYTICAL CONCLUSION / LIMITATION / UNCERTAINTY
AI WORKSET DIFFERS FROM CONFIRMED HUMAN-SPECIALIST WORKSET
CONFUSES AI CONSULTATION WITH DIRECT SITE MODIFICATION
CONFUSES CLIENT QUESTIONS WITH INTERNAL RESEARCH ROADMAP
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
AI_OFFLINE_SELF_CONTAINED = true when AI artifact promised
AI_CAN_EXPLAIN_FULL_MATERIAL_RESEARCH = true when promised
AI_CAN_EXPLAIN_FULL_CONFIRMED_CHANGE_SET = true when promised
AI_CAN_EXPLAIN_WHY_WHERE_AND_HOW = true when promised
AI_CAN_EXPLAIN_ACCEPTANCE_CHECK = true when promised
AI_REQUIRES_NO_UNDECLARED_SECOND_CONTEXT = true
ONE_DOCUMENT_PROMISE_SATISFIED_BY_ONE_FILE = true when promised
AI_WORKSET_EQUALS_CONFIRMED_SPECIALIST_WORKSET = true when parallel paths promised
AI_DOES_NOT_CLAIM_DIRECT_SITE_MODIFICATION = true
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
ALL DATA SOMEWHERE IN PACKAGE != SELF-CONTAINED AI ARTIFACT
SECOND FILE REQUIRED != ONE-DOCUMENT SELF-CONTAINMENT
JSON_PARSE_PASS != AI KNOWLEDGE PASS
AI CONSULTATION != DIRECT SITE MODIFICATION
AI CONSULTANT != INTERNAL RESEARCH EXECUTION CHECKPOINT
ANALYST QA != OWNER ACCEPTANCE
```

## 11. Non-repeat purpose

The goal is to catch the defect **before release** that an owner would otherwise find only after opening and trying to use the actual deliverable.

Step20 must therefore perform the recipient task, not merely verify the artifact.

This file follows `PERMANENT_STEP_RULE_UNIVERSALITY_AND_JOB_SEPARATION_GATE.md`.
