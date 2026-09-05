# KW-001 — Step 19 recipient-artifact completeness gate

Updated: 2026-09-05  
Status: **ACTIVE / UNIVERSAL / OWNER-DIRECTED PERMANENT NON-REPEAT CONTROL**  
Scope: **Step 19 companion gate / Level 1**

This gate supplements `STEP_19_CLIENT_DELIVERABLE_PACKAGING_METHOD.md`. Step 19 remains an owner-directed corrected method candidate; this file adds a narrow permanent control earned from post-release recipient review.

Concrete client domains, URLs, case counts, action IDs, file names and current-job findings are forbidden in this Level1 gate.

## 1. Failure class — package-wide completeness mistaken for recipient-artifact completeness

A package can contain deep research, canonical tables and full evidence while a promised recipient artifact is still too compressed or wrongly materialized for its intended use.

```text
PACKAGE-WIDE TRUTH EXISTS
!= EACH PROMISED RECIPIENT ARTIFACT IS COMPLETE FOR ITS OWN PURPOSE

MASTER RESEARCH COMPLETE
!= CLIENT RESEARCH REPORT COMPLETE

SELF-CONTAINED DATA
!= SELF-CONTAINED KNOWLEDGE
```

A required recipient must not be forced to reconstruct the promised research from internal master files, specialist guides, raw workbooks, serialization objects or repository history when their own artifact is declared self-contained.

## 2. Client research report anti-overcompression gate

A client-facing research report may include an executive summary, but it must not collapse the substantive research into only summary bullets and a short recommendation list when the sold/approved product promises a full research report.

For each material finding or declared group of equivalent findings, the report must expose enough of the following chain for the recipient to understand the conclusion without repository reconstruction:

```text
WHAT WAS CHECKED
CURRENT STATE
EVIDENCE / OBSERVATION
INTERPRETATION
WHAT IS CORRECT / WRONG / INSUFFICIENT
WHY IT MATTERS
TARGET STATE
EXACT CHANGE / LOCATION WHEN APPLICABLE
MATERIAL QUERIES / TOPICS / QUESTIONS WHEN APPLICABLE
EXAMPLE WHEN JUSTIFIED
WHAT SHOULD REMAIN UNCHANGED
LIMITATION / UNCERTAINTY
```

Grouping equivalent findings is allowed. Hiding all evidence behind internal codes is not.

## 3. Search evidence visibility

If ordinary Search materially governed semantics/page architecture, the recipient artifact must show what Search actually contributed.

Aggregate prose alone is insufficient when the product promise requires evidence-based research and material Search cases exist.

Use client-readable cases or another equivalent surface that preserves:

```text
QUERY / TASK OR DECLARED CASE SCOPE
OBSERVED SEARCH PATTERN
SUPPORTED PAGE/INTENT CONCLUSION
DOWNSTREAM DECISION
CLAIM BOUNDARY
```

```text
SEARCH LEDGER EXISTS INTERNALLY
!= SEARCH RESEARCH CLIENT-VISIBLE
```

## 4. AI causal visibility

If AI verification is a material product differentiator, aggregate verdict counts do not by themselves satisfy recipient visibility.

For each material AI case, or an explicitly justified equivalent grouping, preserve:

```text
WHY SELECTED
FROZEN PRE-AI DECISION
AI EVIDENCE / OBSERVATION
COMPARISON
CHANGE | DE_RISK | NO_CHANGE | INSUFFICIENT
DOWNSTREAM ACTION OR EXPLICIT NO-ACTION
LIMITATION
```

```text
AI CAUSAL LEDGER COMPLETE
!= AI VALUE RECIPIENT-VISIBLE
```

## 5. Full decision-map visibility

A report that highlights only top priorities can hide important positive retain/no-change decisions and unresolved states.

Where the job contains a finite material decision universe, provide a recipient-readable map or equivalent summary that distinguishes at least:

```text
CHANGE / IMPROVE
ROUTE / REASSIGN
RETAIN / KEEP
NO NEW PAGE / NO DESTRUCTIVE ACTION
RECHECK / PENDING DETAIL
HOLD / DEFERRED / UNRESOLVED
```

The map may point to a specialist guide for implementation detail, but the client must be able to see the complete material outcome set.

## 6. Uncertainty explanation

Counts alone are not an adequate explanation of a material unresolved universe.

Group uncertainty by material reason/class and explain:

```text
WHAT KIND OF QUESTION REMAINS OPEN
WHY IT IS OPEN
WHETHER IT BLOCKS CURRENT READY ACTIONS
WHAT EVIDENCE WOULD REOPEN/RESOLVE IT
```

## 7. Recipient-language compliance

Every recipient-facing artifact must comply with its declared language contract.

Internal source prose may be translated during materialization without changing analytical meaning. Immutable identifiers, URLs, filenames and standard technical tokens may remain unchanged.

```text
MIXED INTERNAL LANGUAGE ACCEPTABLE IN SOURCE
!= MIXED INTERNAL LANGUAGE ACCEPTABLE IN RECIPIENT ARTIFACT
```

## 8. AI research knowledge handoff completeness

When a deliverable is promised for another AI/LLM, first declare its actual recipient purpose. For a research-knowledge handoff, the purpose is to transfer the accepted results and meaning of the completed research so that a new AI can use those results in a later task explicitly supplied by the user.

It is not an execution-control artifact unless the contract separately and explicitly says so.

```text
AI RESEARCH KNOWLEDGE HANDOFF
!= INTERNAL EXECUTION HANDOFF

RESEARCH CONTEXT TRANSFER
!= CONTINUE ROADMAP FROM LAST CHECKPOINT

AI KNOWLEDGE DOCUMENT
!= EXECUTION CURSOR
```

A research knowledge handoff must make the following recoverable without repository reconstruction:

```text
WHAT WAS RESEARCHED
BUSINESS / SITE / SCOPE
RESEARCH PURPOSE
EVIDENCE CLASSES AND METHOD
CURRENT ACCEPTED MODEL / AUTHORITIES
MATERIAL FINDINGS
WHY MATERIAL DECISIONS WERE MADE
ORDINARY SEARCH CONTRIBUTION
AI CAUSAL CONTRIBUTION
KEEP / RETAIN / NO_CHANGE / DE_RISK RESULTS
SUPPORTED CHANGES
UNCERTAINTY / HOLD / RECHECK / SEARCH_REQUIRED
CLAIM BOUNDARIES / FORBIDDEN INFERENCES
```

The normal usage contract is:

```text
USER LOADS PRIMARY AI KNOWLEDGE DOCUMENT
-> AI TREATS IT AS SELF-CONTAINED RESEARCH CONTEXT
-> USER PROVIDES A NEW TASK
-> AI USES THE RESEARCH RESULTS / EVIDENCE / BOUNDARIES FOR THAT TASK
```

Loading the artifact alone must not imply permission or instruction to execute another internal roadmap stage.

### 8.1 Primary physical format

The primary physical format must be chosen for the recipient task, not for serialization convenience.

For an LLM-oriented research/context handoff, a self-contained narrative Markdown document is the default unless the job contract demonstrates that another physical format is equally or more usable for the target AI environment.

Structured `JSON/CSV/TSV` may be supplied as appendices or machine-readable companion layers when row-level completeness or deterministic processing requires them. They do not automatically replace the primary knowledge/context artifact.

```text
MACHINE-READABLE != LLM-USABLE
JSON_PARSE_PASS != AI_HANDOFF_PASS
ALL ROWS PRESENT != RESEARCH MEANING RECOVERABLE
```

If a non-Markdown format is chosen as the sole primary AI handoff, the deliverable contract must record why that format better satisfies the actual recipient task and how equivalent context comprehension will be tested.

## 9. Workbook front-door usability

A semantically correct workbook may retain detailed canonical/audit sheets, but client usability requires a front-door decision surface.

Unless the job contract explicitly defines an equivalent interface, provide clearly discoverable recipient-oriented surfaces for:

```text
HOW TO USE
KEY FINDINGS
PAGE / TASK / DECISION MAP
READY ACTIONS
NO-CHANGE / RETAIN
UNCERTAINTY / HOLD / RECHECK
SEARCH / AI EVIDENCE SUMMARY
```

Detailed `semantic master`, `units`, `evidence`, `manifest` or similar authority sheets may remain as appendices/detail views.

```text
CORRECT DATABASE
!= CLIENT-USABLE WORKBOOK
```

## 10. Recipient-task walkthrough

Before Step 19 PASS, define realistic recipient tasks rather than only file/render properties.

Equivalent walkthrough questions:

```text
CAN A CLIENT FIND THE DECISION FOR A MATERIAL PAGE/TOPIC WITHOUT REPOSITORY KNOWLEDGE?
CAN A SPECIALIST DISTINGUISH READY FROM ANALYTICAL-ONLY / HOLD / RECHECK?
CAN THE RECIPIENT UNDERSTAND WHY A MATERIAL DECISION WAS MADE?
CAN SEARCH AND AI CONTRIBUTIONS BE FOUND WITHOUT MANUAL JOINS?
CAN UNCERTAINTY BE DISTINGUISHED FROM NO-CHANGE?
CAN A NEW AI USE THE RESEARCH KNOWLEDGE ARTIFACT FOR A USER-SUPPLIED TASK WITHOUT EXECUTION-STATE RECONSTRUCTION?
```

## 11. PASS gate

A Step19 deliverable package cannot receive full recipient-usability PASS when any applicable condition is false:

```text
PROMISED_CLIENT_REPORT_SELF_CONTAINED_FOR_RESEARCH_PURPOSE = true
MATERIAL_FINDINGS_NOT_OVERCOMPRESSED = true
MATERIAL_SEARCH_CONTRIBUTION_VISIBLE = true when in scope
MATERIAL_AI_CAUSAL_RESULTS_VISIBLE = true when in scope
FULL_MATERIAL_DECISION_MAP_VISIBLE = true
MATERIAL_UNCERTAINTY_EXPLAINED = true
RECIPIENT_LANGUAGE_COMPLIANT = true
AI_HANDOFF_PURPOSE_EXPLICIT = true when AI handoff promised
AI_HANDOFF_NOT_CONFLATED_WITH_EXECUTION_CURSOR = true when research handoff promised
AI_HANDOFF_PRIMARY_FORMAT_RECIPIENT_JUSTIFIED = true when AI handoff promised
AI_HANDOFF_RESEARCH_MEANING_SELF_CONTAINED = true when AI handoff promised
WORKBOOK_FRONT_DOOR_USABLE = true when workbook promised
RECIPIENT_TASK_WALKTHROUGH = PASS
```

Hard non-equivalences:

```text
EXECUTIVE SUMMARY != FULL RESEARCH REPORT
INTERNAL EVIDENCE EXISTS != RECIPIENT CAN SEE RESEARCH
AGGREGATE AI COUNTS != AI CAUSAL RESULT
CORRECT DATABASE != CLIENT-USABLE WORKBOOK
PACKAGE-WIDE COMPLETENESS != RECIPIENT-ARTIFACT COMPLETENESS
MACHINE-READABLE != LLM-USABLE
SELF-CONTAINED DATA != SELF-CONTAINED KNOWLEDGE
AI RESEARCH HANDOFF != EXECUTION CHECKPOINT
```

This file follows `PERMANENT_STEP_RULE_UNIVERSALITY_AND_JOB_SEPARATION_GATE.md`.
