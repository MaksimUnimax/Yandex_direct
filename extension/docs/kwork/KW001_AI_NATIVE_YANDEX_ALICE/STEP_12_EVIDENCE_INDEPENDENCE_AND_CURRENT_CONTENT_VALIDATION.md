# Step 12 — Evidence independence and current-content validation

Date: 2026-08-31  
Updated: 2026-09-03  
Status: **APPROVED / ACTIVE / UNIVERSAL / PERMANENT NON-REPEAT CONTROL**

This rule exists because Step 12 was incorrectly declared complete more than once even after external methodology research had identified the right principles. The recurring failure was not lack of research. The recurring failure was that implementation and verification accepted **fields that restated the selected action** instead of independently proving the evidence that should cause the action.

## 1. Failure that caused the repeated false PASS

Failed pattern:

```text
EXTERNAL PRINCIPLE
→ ADD FIELD / STATE / QA CHECK
→ GENERATOR POPULATES FIELD USING ITS OWN ACTION LOGIC
→ VERIFIER CHECKS FIELD EXISTS / IS CONSISTENT WITH ACTION
→ PASS
```

Generic examples:

```text
EXPAND EXISTING PAGE
→ write QUALITY_GAP
→ write gap evidence that merely paraphrases the expansion decision
→ verifier sees a non-empty field consistent with EXPAND
→ false PASS
```

and:

```text
ROUTING GRAPH CONNECTS PAGE A TO PAGE B
→ create IMPLEMENT internal-link row
→ verifier sees source_url + target_url + relation fields
→ false PASS without current source-context/target-fit proof
```

### Root cause

```text
SCHEMA COMPLETENESS WAS TREATED AS EVIDENCE COMPLETENESS
ACTION CONSISTENCY WAS TREATED AS CAUSAL VALIDATION
THE SAME LOGIC GENERATED BOTH DECISION AND ITS “PROOF”
THE VERIFIER CHECKED REPRESENTATION INVARIANTS, NOT THE REAL-WORLD CLAIM
```

This can produce a technically clean PASS while material content-gap or link recommendations remain unsupported.

## 2. Permanent causal rule

```text
ACTION MUST NEVER BE AN EVIDENCE SOURCE FOR ITSELF
```

Therefore:

```text
STRUCTURAL ACTION != GAP EVIDENCE
STRUCTURAL UNIT ID != PROOF OF UNIT COHERENCE
NON-EMPTY FIELD != PROOF THE FIELD IS TRUE
KNOWN URL != PAGE FIT
ROUTING GRAPH EDGE != IMPLEMENTABLE INTERNAL LINK
GENERATOR CONSISTENCY CHECK != INDEPENDENT VERIFICATION
```

Correct causal order:

```text
CURRENT EXTERNAL / FIRST-PARTY EVIDENCE
→ EXPLICIT OBSERVATION
→ DIAGNOSIS
→ ALTERNATIVE COMPARISON
→ ACTION
→ INDEPENDENT VERIFICATION THAT RECOMPUTES DIAGNOSIS WITHOUT USING ACTION AS INPUT
```

If the diagnosis cannot be recomputed without looking at the action, the action is not independently proven.

## 3. Source grounding

- Semrush, Keyword Mapping: https://www.semrush.com/blog/keyword-mapping/
- Semrush, Content Gap Analysis: https://www.semrush.com/blog/content-gap-analysis/
- Semrush, Content Audit: https://www.semrush.com/blog/content-audit/
- Ahrefs, Internal Links for SEO: https://ahrefs.com/blog/internal-links-for-seo/
- Ahrefs, Keyword Strategy: https://ahrefs.com/blog/keyword-strategy/
- Yandex Webmaster, Site structure: https://yandex.ru/support/webmaster/ru/recommendations/site-structure
- Yandex Webmaster, Low-value or low-demand pages: https://yandex.ru/support/webmaster/ru/site-indexing/low-demand

These sources constrain the evidence principles; exact KW-001 states are project controls.

## 4. Structural gap and content-enhancement gap must be separated

```text
STRUCTURAL_GAP_STATE =
  NONE
  TOPIC_GAP
  INTENT_GAP
  MIXED_STRUCTURAL_GAP
  STRUCTURAL_EVIDENCE_INSUFFICIENT

CONTENT_ENHANCEMENT_STATE =
  NONE
  QUALITY_GAP
  ORIGINALITY_GAP
  CONTENT_EVIDENCE_INSUFFICIENT
  NOT_ASSESSED
```

Source-derived concepts include topic/intent/content-quality/originality gaps. Operational `*_EVIDENCE_INSUFFICIENT` states are fail-closed project controls and must not be attributed to external sources as their taxonomy.

```text
TOPIC_GAP / INTENT_GAP
may change URL structure / owner / split / create decision.

QUALITY_GAP / ORIGINALITY_GAP
may require content enhancement while structural owner remains unchanged.
```

A content-quality verdict must not imply a new structural boundary without separate structural evidence.

## 5. Mandatory current-page validation for content-changing actions

Fresh current-page validation is required before accepting an action that asserts a material current page content/structure change, for example:

```text
EXPAND_EXISTING_PAGE
ADD_SECTION_OR_FAQ_TO_EXISTING
SPLIT_EXISTING_PAGE
MERGE_STRUCTURALLY_REDUNDANT_PAGES
NEW_* PAGE
```

For structural KEEP, current evidence must prove the present structural role; this does not certify performance optimization when analytics are unavailable.

### Required evidence for QUALITY_GAP

Every `QUALITY_GAP` must preserve equivalent independently observed fields:

```text
CURRENT_URL
CURRENT_PAGE_READ_DATE
MEMBER_USER_NEEDS
NEEDS_ALREADY_COVERED
EXPLICIT_MISSING_NEEDS
CURRENT_PAGE_EVIDENCE
WHY_MISSING_NEEDS_ARE_MATERIAL
```

Prohibited as sole proof:

```text
“the action requires more coverage”
“EXPAND was selected”
“SECTION was selected”
“current_page_fit = PARTIAL”
```

Fail-closed rules:

```text
QUALITY_GAP_WITHOUT_EXPLICIT_MISSING_NEED = 0
QUALITY_GAP_WITHOUT_CURRENT_PAGE_READ = 0
QUALITY_GAP_EVIDENCE_DERIVED_ONLY_FROM_ACTION = 0
EXPAND_OR_SECTION_WITHOUT_INDEPENDENT_CONTENT_DEFICIT = 0
```

If current content already covers the accepted need sufficiently for structural purposes:

```text
CONTENT_ENHANCEMENT_STATE = NONE
STRUCTURAL OWNER MAY REMAIN KEEP
```

If evidence is incomplete:

```text
CONTENT_ENHANCEMENT_STATE = CONTENT_EVIDENCE_INSUFFICIENT
ACTION MUST REMAIN PROVISIONAL / DEFERRED
```

## 6. Mandatory source-context and target-fit validation for internal-link IMPLEMENT

An internal-link row is `IMPLEMENT` only when both sides are independently validated from current content.

Required equivalent evidence:

```text
SOURCE_URL
SOURCE_PAGE_READ_DATE
SOURCE_CONTEXT_EXCERPT_OR_SECTION_DESCRIPTION
TARGET_URL
TARGET_PAGE_READ_DATE
TARGET_TASK_FIT_EVIDENCE
USER_NEXT_STEP_HELPFUL = true
RELATION_TYPE
ANCHOR_CONCEPT
PLACEMENT_CONTEXT
```

Causal gate:

```text
CURRENT SOURCE CONTEXT EXISTS
+ CURRENT TARGET ACTUALLY SERVES THE NEXT USER TASK
+ LINK HELPS USER NAVIGATE / UNDERSTAND / CONVERT
→ IMPLEMENT
```

Otherwise use an explicit defer/not-applicable state.

Forbidden shortcut:

```text
ROUTING GRAPH EDGE -> IMPLEMENT
```

without current source/target validation.

## 7. KEEP naming and performance boundary

Permanent semantic meaning:

```text
KEEP_STRUCTURAL_OWNER
```

Historical artifacts may use another accepted label for traceability, but new reporting must explain the meaning.

It never means, without separate evidence:

```text
KEEP_AS_IS
NO_CONTENT_CHANGE_NEEDED
SEO_OPTIMIZED
PERFORMANCE_GOOD
```

## 8. Zero CREATE semantics

`CREATE = 0` means only that no new URL is justified by the current job's available evidence and scope.

It does not prove the audience has no other needs or the business has no unobserved content opportunities.

## 9. DELETE / NOINDEX / RETIRE boundary

Step12 semantic/structural evidence alone cannot authorize destructive actions such as delete/noindex/retire/redirect-as-removal unless a dedicated evidence route proves the necessary performance/value/duplicate/business state.

Default when removal is plausible but unproven:

```text
RETIREMENT_REVIEW_REQUIRED
```

## 10. Verifier independence requirements

For content:

```text
CURRENT PAGE CONTENT + MEMBER NEEDS
→ EXPECTED CONTENT ENHANCEMENT STATE
→ compare with generated state/action
```

For links:

```text
CURRENT SOURCE PAGE + CURRENT TARGET PAGE + USER JOURNEY
→ EXPECTED LINK ACTION STATE
→ compare with generated link row
```

A validator that cannot produce a negative verdict against an unsupported proposed action is not an independent verifier.

## 11. Mandatory reopen rule after a post-PASS methodological contradiction

If a later audit proves that an accepted verifier did not independently validate a material claim class:

```text
DO NOT PATCH THE REPORT AND LEAVE STEP COMPLETE
```

Instead:

```text
REGISTER NEW DEFECT CLASS
→ REOPEN STEP
→ MARK DOWNSTREAM STEP BLOCKED AS REQUIRED
→ REVALIDATE EVERY ROW IN THE AFFECTED CLASS
→ REBUILD AFFECTED DOWNSTREAM OUTPUTS
→ RUN NEW INDEPENDENT VERIFICATION
→ PERSIST DIAGNOSTICS
→ GITHUB READBACK
→ ONLY THEN RESTORE PASS
```

### Root cause this control prevents

A new schema field or QA assertion can create the appearance of stronger validation without changing the causal evidence path. The reopen rule forces the actual affected claim class to be recomputed.

## 12. Job-specific correction boundary

Concrete defect IDs, affected row counts, phrases, URLs, job state and downstream block status belong only in the current Level-2 workspace.

```text
PERMANENT FAILURE CLASS + ROOT CAUSE + CONTROL
= LEVEL 1

CURRENT AFFECTED ROWS / IDS / COUNTS / STATUS
= LEVEL 2
```

## Markers

```text
KW001_STEP12_ACTION_CANNOT_PROVE_ITSELF = true
KW001_STEP12_SCHEMA_COMPLETENESS_NOT_EQUAL_EVIDENCE_COMPLETENESS = true
KW001_STEP12_STRUCTURAL_AND_CONTENT_GAPS_SEPARATED = true
KW001_STEP12_QUALITY_GAP_REQUIRES_CURRENT_CONTENT_DEFICIT = true
KW001_STEP12_CONTENT_CHANGING_ACTION_REQUIRES_FRESH_PAGE_READ = true
KW001_STEP12_INTERNAL_LINK_IMPLEMENT_REQUIRES_CURRENT_SOURCE_AND_TARGET_VALIDATION = true
KW001_STEP12_KEEP_MEANS_STRUCTURAL_OWNER_NOT_KEEP_AS_IS = true
KW001_STEP12_ZERO_CREATE_DOES_NOT_MEAN_ZERO_AUDIENCE_GAPS = true
KW001_STEP12_DESTRUCTIVE_ACTIONS_REQUIRE_SEPARATE_EVIDENCE = true
KW001_STEP12_POST_PASS_METHOD_CONTRADICTION_REOPENS_STEP = true
KW001_STEP12_JOB_SPECIFIC_CORRECTION_STATE_FORBIDDEN_IN_PERMANENT_METHOD = true
```
