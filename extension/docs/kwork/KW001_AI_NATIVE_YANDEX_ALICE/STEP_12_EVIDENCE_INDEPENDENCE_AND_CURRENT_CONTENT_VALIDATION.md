# Step 12 — Evidence independence and current-content validation

Date: 2026-08-31  
Status: **APPROVED / ACTIVE / PERMANENT NON-REPEAT CONTROL**

This rule exists because Step 12 was incorrectly declared complete more than once even after external methodology research had identified the right principles. The recurring failure was not lack of research. The recurring failure was that the implementation and verifier accepted **fields that restated the selected action** instead of independently proving the evidence that should cause the action.

## 1. Exact failure that caused the repeated false PASS

The failed pattern was:

```text
EXTERNAL PRINCIPLE
→ ADD FIELD / STATE / QA CHECK
→ GENERATOR POPULATES THE FIELD USING ITS OWN ACTION LOGIC
→ VERIFIER CHECKS THAT THE FIELD EXISTS / IS CONSISTENT WITH THE ACTION
→ PASS
```

Examples:

```text
EXPAND_EXISTING_PAGE
→ write GAP_TYPE = QUALITY_GAP
→ write GAP_EVIDENCE = "the page requires fuller coverage"
→ verifier sees a non-empty gap_type/gap_evidence consistent with EXPAND
→ PASS
```

and:

```text
ROUTING GRAPH CONNECTS PAGE A TO PAGE B
→ create IMPLEMENT internal-link row
→ verifier sees source_url + target_url + relation fields
→ PASS
```

Both are circular. In the first case the action proves the gap that is then used to justify the action. In the second case the graph relation proves a link without proving that the current source context and target content actually make that link useful.

### Root cause

```text
SCHEMA COMPLETENESS WAS TREATED AS EVIDENCE COMPLETENESS
ACTION CONSISTENCY WAS TREATED AS CAUSAL VALIDATION
THE SAME MODEL/LOGIC THAT GENERATED A DECISION ALSO GENERATED ITS EXPLANATION
THE VERIFIER CHECKED REPRESENTATION INVARIANTS, NOT THE UNDERLYING REAL-WORLD CLAIM
```

This is the reason Step 12 could receive a technically clean PASS while still containing unsupported `QUALITY_GAP`, `EXPAND`, `SECTION`, or `IMPLEMENT` conclusions.

## 2. Permanent causal rule

The following rule is absolute:

```text
ACTION MUST NEVER BE AN EVIDENCE SOURCE FOR ITSELF
```

Therefore:

```text
STRUCTURAL ACTION
!= GAP EVIDENCE

STRUCTURAL UNIT ID
!= PROOF OF UNIT COHERENCE

NON-EMPTY FIELD
!= PROOF THE FIELD IS TRUE

KNOWN URL
!= PAGE FIT

ROUTING GRAPH EDGE
!= IMPLEMENTABLE INTERNAL LINK

GENERATOR CONSISTENCY CHECK
!= INDEPENDENT VERIFICATION
```

The causal order is:

```text
CURRENT EXTERNAL / FIRST-PARTY EVIDENCE
→ EXPLICIT OBSERVATION
→ DIAGNOSIS
→ ALTERNATIVE COMPARISON
→ ACTION
→ INDEPENDENT VERIFICATION THAT RECOMPUTES THE DIAGNOSIS WITHOUT USING ACTION AS INPUT
```

If the diagnosis cannot be recomputed without looking at the action, the action is not independently proven.

## 3. Source grounding

Current external sources that constrain this rule:

- Semrush, *Keyword Mapping*, 2026-07-27: keyword maps must stay current; existing/planned URL assignments should be checked against actual current pages before optimizing or creating content.  
  https://www.semrush.com/blog/keyword-mapping/
- Semrush, *Content Gap Analysis*, 2026-06-23: a quality gap means current content is thin, outdated, unclear or otherwise low quality; gap analysis compares what users want with what the content actually answers.  
  https://www.semrush.com/blog/content-gap-analysis/
- Semrush, *Content Audit*: Keep / Update / Consolidate / Delete decisions depend on content quality, gaps, performance and business outcomes, not merely semantic ownership.  
  https://www.semrush.com/blog/content-audit/
- Ahrefs, *Internal Links for SEO*, updated 2026-03-10: internal links should point to contextually relevant content that genuinely helps the reader; link context and destination relevance matter, not only site-graph adjacency.  
  https://ahrefs.com/blog/internal-links-for-seo/
- Ahrefs, *Keyword Strategy*, updated 2026-03-13: page/content decisions should use current ranking evidence to infer content type, format and angle when material.  
  https://ahrefs.com/blog/keyword-strategy/
- Yandex Webmaster, *Site structure*: pages should be connected by clear links that help users find relevant documents; links are part of the actual site structure.  
  https://yandex.ru/support/webmaster/ru/recommendations/site-structure
- Yandex Webmaster, *Low-value or low-demand pages*: pages may be excluded when duplicate, empty, or not sufficiently aligned with user queries; there is no quota requiring extra pages.  
  https://yandex.ru/support/webmaster/ru/site-indexing/low-demand

## 4. Structural gap and content-enhancement gap must be separated

The previous single `GAP_TYPE` field mixed architectural and content-quality diagnoses.

Permanent model:

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

Source-derived categories are:

```text
TOPIC_GAP
INTENT_GAP
QUALITY_GAP
ORIGINALITY_GAP
```

Operational project states such as `MIXED_*` and `*_EVIDENCE_INSUFFICIENT` are our fail-closed controls and must not be attributed to Semrush as source categories.

### Consequences

```text
TOPIC_GAP / INTENT_GAP
may change URL structure / owner / split / create decision.

QUALITY_GAP / ORIGINALITY_GAP
may require content enhancement while the structural owner remains unchanged.
```

A content-quality verdict must not be used to imply a new structural boundary without separate structural evidence.

## 5. Mandatory current-page validation for content-changing actions

Fresh current-page validation is required not only before CREATE.

It is mandatory before accepting any action that asserts a change to current page content or structure:

```text
EXPAND_EXISTING_PAGE
ADD_SECTION_OR_FAQ_TO_EXISTING
SPLIT_EXISTING_PAGE
MERGE_STRUCTURALLY_REDUNDANT_PAGES
NEW_* PAGE
```

For `KEEP_*` with `STRUCTURAL_GAP_STATE=NONE`, current evidence must at least prove the present structural role; this still does not certify performance optimization when analytics are unavailable.

### Required evidence for QUALITY_GAP

Every `QUALITY_GAP` must preserve independently observed current-page deficits:

```text
CURRENT_URL
CURRENT_PAGE_READ_DATE
MEMBER_USER_NEEDS
NEEDS_ALREADY_COVERED
EXPLICIT_MISSING_NEEDS
CURRENT_PAGE_EVIDENCE
WHY_MISSING_NEEDS_ARE_MATERIAL
```

Prohibited evidence:

```text
"the action requires more coverage"
"EXPAND was selected"
"SECTION was selected"
"current_page_fit = PARTIAL"
```

unless those statements are accompanied by the independent current-content observations that caused them.

Fail-closed rules:

```text
QUALITY_GAP_WITHOUT_EXPLICIT_MISSING_NEED = 0
QUALITY_GAP_WITHOUT_CURRENT_PAGE_READ = 0
QUALITY_GAP_EVIDENCE_DERIVED_ONLY_FROM_ACTION = 0
EXPAND_OR_SECTION_WITHOUT_INDEPENDENT_CONTENT_DEFICIT = 0
```

If current content already covers the accepted user need sufficiently for structural purposes:

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

Required evidence:

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

Otherwise:

```text
NO SOURCE CONTEXT → DEFER_SOURCE_CONTEXT_NOT_MATERIALIZED
TARGET DOES NOT SERVE TASK → DEFER_TARGET_CONTENT_GAP
RELATION NOT USEFUL TO USER → NOT_APPLICABLE
```

Prohibited shortcut:

```text
ROUTING GRAPH EDGE
→ IMPLEMENT
```

without current source/target content validation.

Fail-closed rules:

```text
IMPLEMENT_WITHOUT_CURRENT_SOURCE_CONTEXT = 0
IMPLEMENT_WITHOUT_CURRENT_TARGET_FIT = 0
IMPLEMENT_WITHOUT_USER_HELPFULNESS_JUSTIFICATION = 0
```

## 7. KEEP naming and performance boundary

The permanent semantic meaning is:

```text
KEEP_STRUCTURAL_OWNER
```

Historical artifacts may retain `KEEP_EXISTING_STRUCTURE` for traceability, but new reporting/method language must explain it as `KEEP_STRUCTURAL_OWNER` / `KEEP_URL_ROLE`.

It never means:

```text
KEEP_AS_IS
NO_CONTENT_CHANGE_NEEDED
SEO_OPTIMIZED
PERFORMANCE_GOOD
```

unless separate performance/content evidence explicitly proves those claims.

## 8. Zero CREATE semantics

`CREATE = 0` means only:

```text
NO NEW URL IS JUSTIFIED BY THE CURRENT JOB'S AVAILABLE PUBLIC-SITE + WORDSTAT + SEARCH + OWNER-EVIDENCE SCOPE
```

It must never be reported as:

```text
THE SITE HAS NO TOPIC GAPS
THE AUDIENCE HAS NO OTHER NEEDS
```

because base scope may not include CRM, sales calls, support tickets, interviews, private analytics or other audience evidence.

## 9. DELETE / NOINDEX / RETIRE boundary

Step-12 semantic/structural evidence alone cannot authorize destructive actions such as:

```text
DELETE
NOINDEX
RETIRE
301 REDIRECT AS REMOVAL
```

unless a dedicated evidence route has established the required current performance/value/duplicate/business state.

Default outcome when removal looks plausible but is not proven:

```text
RETIREMENT_REVIEW_REQUIRED
```

## 10. Verifier independence requirements

The independent verifier must recompute evidence claims from raw/current evidence and must not use the final action as a causal input.

For quality/content checks:

```text
CURRENT PAGE CONTENT + MEMBER NEEDS
→ EXPECTED CONTENT ENHANCEMENT STATE
→ compare with generated state/action
```

For internal links:

```text
CURRENT SOURCE PAGE + CURRENT TARGET PAGE + USER JOURNEY
→ EXPECTED LINK ACTION STATE
→ compare with generated link row
```

The verifier must be capable of producing both positive and negative outcomes.

A validator that cannot reject an `EXPAND`, `SECTION`, `QUALITY_GAP` or `IMPLEMENT` row is not a valid independent verifier.

## 11. Mandatory reopen rule after a post-PASS methodological contradiction

If a post-PASS audit proves that an accepted verifier did not independently validate a material claim class:

```text
DO NOT PATCH THE REPORT AND LEAVE STEP COMPLETE
```

Instead:

```text
REGISTER NEW DEFECT CLASS
→ REOPEN STEP
→ MARK NEXT STEP BLOCKED
→ REVALIDATE EVERY ROW IN THE AFFECTED CLASS
→ REBUILD ALL DOWNSTREAM OUTPUTS AFFECTED BY CHANGED ACTIONS/ROUTES
→ RUN A NEW INDEPENDENT VERIFIER
→ PERSIST DIAGNOSTICS
→ GITHUB READBACK
→ ONLY THEN RESTORE PASS
```

This rule exists specifically to prevent the repeated failure where a new field was added, schema QA passed, and Step 12 was prematurely declared complete again.

## 12. Current OKNO-MSK correction triggered by this rule

Current post-PASS defects:

```text
D12-28 = QUALITY_GAP / EXPAND / SECTION can be circular because current-content deficit was not independently materialized for every accepted QUALITY_GAP unit.
D12-29 = some IMPLEMENT internal-link rows were derived from routing relations without independently proving current source context + current target-task fit.
```

Until all affected rows are revalidated:

```text
STEP12_COMPLETE = false
STEP13_BLOCKED = true
STEP13_EXECUTED = false
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
```
