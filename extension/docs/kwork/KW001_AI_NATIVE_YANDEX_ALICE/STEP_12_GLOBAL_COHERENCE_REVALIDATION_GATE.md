# Step 12 — Global coherence revalidation gate after later evidence

Date: 2026-08-31  
Status: **APPROVED / ACTIVE / PERMANENT NON-REPEAT CONTROL**

## Why this rule exists

The D12-27 correction correctly re-opened two known mixed structural units and explicitly reviewed 65 phrases. The independent verifier then proved that those 65 exact resolutions were applied and that the two known units no longer contained the known wrong members.

That was still not enough.

During the later D12-28 current-content audit, other accepted units were found to contain incompatible terminal tasks, for example:

```text
BALCONY_RENOVATION_WITH_GLAZING
  contains "ремонт балкона без остекления"

PVC_DOOR_INFO
  combines product/dimension/color questions with DIY adjustment/repair questions

WINDOW_COMPONENT_SELECTION_INFO
  combines handle selection with seal/gasket selection

WINDOW_FINISHING_DIY_INFO
  combines slopes, windowsill repair/installation and drip-cap installation

WINDOW_HARDWARE_SELECTION_GUIDE
  includes a seal-selection phrase inside a hardware-guide unit
```

Therefore the prior D12-27 PASS validated the **known regression set**, not global semantic coherence of every unit that could be affected by later evidence.

## Exact failure

The failed assumption was:

```text
KNOWN BAD EXAMPLES FIXED
+ KNOWN REGRESSION SET = 0
→ GLOBAL CLASS IS CLEAN
```

That implication is invalid.

Permanent distinction:

```text
KNOWN_REGRESSION_ZERO
!= GLOBAL_SEMANTIC_COHERENCE_PASS
```

A regression list is a minimum non-repeat check. It is never proof that no other member of the affected analytical class violates the same rule.

## Root cause

```text
D12_27_REVIEW_SCOPE_WAS_LIMITED_TO_ALREADY_DISCOVERED_UNITS
EXACT_PHRASE_REGRESSION_WAS_MISTAKEN_FOR_FULL_CLASS_REVALIDATION
THE VERIFIER PROVED APPLICATION OF KNOWN RESOLUTIONS BUT DID NOT ADVERSARIALLY RECHALLENGE EVERY AFFECTED UNIT
LATER CONTENT EVIDENCE WAS ALLOWED TO CHANGE ACTION/GAP STATE WITHOUT FORCING A NEW COHERENCE PASS ACROSS THE WHOLE AFFECTED CLASS
```

This is another instance of the same higher-level failure: the verifier checked the expected artifact mechanics but did not sufficiently try to falsify the remaining analytical boundaries.

## Permanent rule

Whenever later material evidence changes, narrows, or challenges a decision class, every affected structural unit must be re-audited for member coherence before the class can receive a new PASS.

```text
LATER EVIDENCE CHANGES / CHALLENGES UNIT INTERPRETATION
→ IDENTIFY COMPLETE AFFECTED UNIT CLASS
→ MATERIALIZE ALL MEMBER PHRASES FOR EVERY UNIT IN THAT CLASS
→ RECHECK EACH MEMBER AGAINST TERMINAL USER TASK / OBJECT / FORMAT / EXPECTED OWNER
→ SPLIT / REASSIGN / DEFER WRONG MEMBERS
→ REBUILD UNIT COUNTS + ACTIONS + PHRASE MAP + LINKS + PAIR GRAPH
→ INDEPENDENT VERIFIER RECOMPUTES COHERENCE FROM MEMBER PHRASES
```

The complete affected class may be narrower than all 160 units, but it must be defined by a causal criterion, not by a manually selected list of already-known mistakes.

For example, D12-28 affects all units whose final action/content-gap diagnosis depends on a fresh current-content read. Therefore all 20 historical `QUALITY_GAP` units and all of their 322 member phrases must be challenged, not only the first unit that disproved its old action.

## Required semantic fields for revalidation

For every affected unit preserve:

```text
STRUCTURAL_UNIT_ID
MEMBER_PHRASE_COUNT
TERMINAL_USER_TASK
PRIMARY_OBJECT
EXPECTED_RESULT_OR_PAGE_ROLE
ALL_MEMBER_PHRASES_REVIEWED = true
MISFIT_MEMBER_COUNT
MISFIT_PHRASES
MISFIT_RESOLUTION
COHERENCE_VERDICT = STRONG / PARTIAL / FAIL / EVIDENCE_INSUFFICIENT
```

A `STRONG` verdict cannot be obtained only because the unit survived a previous pass.

## Fail-closed checks

```text
AFFECTED_UNITS_WITHOUT_FULL_MEMBER_REVIEW = 0
KNOWN_MISFIT_PHRASES_LEFT_IN_ORIGINAL_UNIT = 0
COHERENCE_PASS_DERIVED_ONLY_FROM_PRIOR_UNIT_ID = 0
ACTION_OR_GAP_REBUILT_BEFORE_MEMBER_COHERENCE = 0
AFFECTED_PHRASE_ACCOUNTING_MISMATCH = 0
GLOBAL_ACCOUNTING_AFTER_REASSIGNMENT = 2332/2332 for current OKNO-MSK job
```

Independent QA must include both:

```text
KNOWN REGRESSION ASSERTIONS
AND
AN ADVERSARIAL FULL-MEMBER REVIEW / RECOMPUTATION FOR THE COMPLETE AFFECTED CLASS
```

## Current OKNO-MSK implication

The post-PASS audit adds a third open defect:

```text
D12-30 = D12-27 correction proved the known 65-phrase regression set but did not establish global coherence for all units later affected by content-evidence revalidation.
```

The 20 D12-28 units contain 322 member phrases and form the mandatory current affected class. Any additional units reached by phrase reassignment must also enter the revalidation graph before acceptance.

Until this passes:

```text
STEP12_COMPLETE = false
STEP13_BLOCKED = true
```

## Markers

```text
KW001_STEP12_KNOWN_REGRESSION_ZERO_NOT_EQUAL_GLOBAL_COHERENCE = true
KW001_STEP12_LATER_EVIDENCE_REQUIRES_COMPLETE_AFFECTED_CLASS_REVIEW = true
KW001_STEP12_FULL_MEMBER_REVIEW_REQUIRED_FOR_AFFECTED_UNITS = true
KW001_STEP12_PRIOR_UNIT_ID_CANNOT_PROVE_COHERENCE = true
KW001_STEP12_D12_27_LOCAL_REGRESSION_SCOPE_FAILURE_DOCUMENTED = true
```
