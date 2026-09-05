# KW-001 — Step 18 execution-ticket completeness gate

Updated: 2026-09-05  
Status: **ACTIVE / UNIVERSAL / OWNER-DIRECTED PERMANENT NON-REPEAT CONTROL**  
Scope: **Step 18 companion gate / Level 1**

This gate supplements `STEP_18_PRIORITIZATION_AND_IMPLEMENTATION_READINESS_METHOD.md`. It does not change the validated status of the parent method. It prevents an analytically correct routing/link/ownership row from being mislabeled as an executable implementation ticket.

Concrete domains, URLs, action IDs, row counts, client-specific priorities and current-job evidence belong only in Level2.

## 1. Failure class — analytical routing map mistaken for executable website task

A row can correctly answer:

```text
WHICH PAGE OWNS THE TASK?
WHICH PAGE SUPPORTS IT?
```

while still failing to answer:

```text
WHAT MUST THE IMPLEMENTER ACTUALLY CHANGE ON THE WEBSITE?
```

Therefore:

```text
CORRECT OWNER / ROUTE
!= READY WEBSITE IMPLEMENTATION TICKET

FIELDS PRESENT
!= EXECUTION DECISION RESOLVED
```

## 2. Required implementation mode

Every material work package that may be shown as `READY` must declare one explicit implementation mode or a job-specific equivalent with the same semantics.

Recommended universal classes:

```text
SEMANTIC_MAPPING_ONLY
CONTEXTUAL_LINK
NAVIGATION_CHANGE
CONTENT_BLOCK
METADATA_OR_LABEL_CHANGE
NO_SITE_CHANGE
RECHECK_ONLY
HOLD
```

Multiple modes may be combined only when every required change is separately specified.

`SEMANTIC_MAPPING_ONLY` means the analytical/customer working map changes but the current public page does not automatically require a content/navigation edit.

`NO_SITE_CHANGE` is a positive implementation result and must not be silently converted into a website task.

## 3. Link-task completeness

A link recommendation may be analytically valid before exact placement is known. It becomes implementation-ready only when applicable fields are materialized:

```text
SOURCE_PAGE_OR_OBJECT
SOURCE_BLOCK_OR_LOCATION
TARGET_PAGE_OR_OBJECT
ANCHOR_OR_ANCHOR_INTENT
SURROUNDING_CONTEXT_OR_SENTENCE_INTENT
WHY_THIS_PLACEMENT
DEPENDENCIES
ACCEPTANCE_CHECK
```

If placement/context is material and not established:

```text
IMPLEMENTATION_SPEC_STATE = PENDING_DETAIL
```

not `READY_LINK`.

## 4. Routing/ownership completeness

A routing work package must distinguish:

```text
ANALYTICAL OWNER CHANGE
REAL-SITE CHANGE REQUIRED = YES | NO | UNRESOLVED
```

When `YES`, specify the mechanism and location: contextual link, navigation, content block, metadata/label or another declared website change.

When `NO`, do not invent breadcrumbs, copy changes, links or navigation changes merely because ownership changed in the semantic model.

When `UNRESOLVED`, the task cannot be implementation-ready.

## 5. Evidence meaning versus evidence locator

A technical filename, row ID, query ID or ledger reference is provenance, not a recipient-facing explanation of evidence.

Required pair for implementation-ready recipient artifacts:

```text
EVIDENCE_MEANING
= short human-readable statement of the observed fact supporting the action

EVIDENCE_LOCATOR
= exact technical source for audit/reverse trace
```

```text
EVIDENCE_LOCATOR ONLY
!= IMPLEMENTATION EVIDENCE EXPLAINED
```

## 6. Recipient-language gate

The source authority may contain internal English or technical prose. A recipient-facing implementation guide must obey the job's language contract.

```text
SOURCE LANGUAGE
!= RECIPIENT INSTRUCTION LANGUAGE
```

URLs, stable IDs, immutable filenames, API names and genuinely standard technical tokens may remain unchanged. Explanatory `AS-IS`, reason, `TO-BE`, instructions, acceptance and do-not-do text must be in the required recipient language unless the job contract explicitly says otherwise.

## 7. QA / PASS gate

For every action claimed implementation-ready:

```text
IMPLEMENTATION_MODE_DECLARED = true
REAL_SITE_CHANGE_STATE_RESOLVED = true
EXACT_LOCATION_PRESENT_WHEN_MODE_REQUIRES_IT = true
LINK_PLACEMENT_AND_CONTEXT_PRESENT_WHEN_MODE_IS_LINK = true
EVIDENCE_MEANING_PRESENT = true
EVIDENCE_LOCATOR_PRESENT = true
RECIPIENT_LANGUAGE_COMPLIANT = true
ACCEPTANCE_TEST_MATCHES_IMPLEMENTATION_MODE = true
```

Hard failures:

```text
ANALYTICAL_ROUTE_LABELLED_READY_WITHOUT_EXECUTION_MODE > 0 => FAIL
LINK_LABELLED_READY_WITHOUT_MATERIAL_PLACEMENT_CONTEXT > 0 => FAIL
RECIPIENT_INSTRUCTIONS_REQUIRING_TRANSLATION_BY_IMPLEMENTER > 0 => FAIL
FILENAME_ONLY_EVIDENCE_FOR_READY_MATERIAL_ACTION > 0 => FAIL
```

## 8. Non-repeat summary

```text
ACCOUNTING BATCH != WORK PACKAGE
ANALYTICAL ACTION != IMPLEMENTATION SPECIFICATION
CORRECT ROUTE != WEBSITE CHANGE
FIELDS PRESENT != EXECUTION DECISION RESOLVED
EVIDENCE LOCATOR != EVIDENCE EXPLANATION
SOURCE LANGUAGE != RECIPIENT INSTRUCTION LANGUAGE
```

This file follows `PERMANENT_STEP_RULE_UNIVERSALITY_AND_JOB_SEPARATION_GATE.md`.
