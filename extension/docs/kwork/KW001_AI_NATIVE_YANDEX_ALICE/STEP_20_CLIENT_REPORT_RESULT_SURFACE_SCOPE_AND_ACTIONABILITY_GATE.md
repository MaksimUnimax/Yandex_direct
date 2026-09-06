# KW-001 — Step 20 client-report result-surface, scope and actionability gate

Updated: 2026-09-06  
Status: **ACTIVE / UNIVERSAL / PERMANENT NON-REPEAT CONTROL**  
Scope: **Step 19 materialization + Step 20 recipient acceptance / Level 1**

This companion gate extends `STEP_20_CLIENT_REPORT_OWNER_VALUE_AND_PLAIN_LANGUAGE_GATE.md`.

Concrete client domains, URLs, query counts, brands, case IDs and current-job values are forbidden here. Job-specific values belong only in Level 2.

## 1. Failure class — client terminology describes the research process instead of the observed result

When the report is talking about the actual results shown to a user, the wording must name the result surface precisely in ordinary client language.

For example, if the material conclusion comes from what was displayed in Yandex results, client prose should describe the **выдача / results shown**, not loosely substitute a word equivalent to "search" when that changes the meaning from output to process.

```text
SEARCH PROCESS
!= SEARCH RESULTS / OUTPUT SURFACE
```

The title and section headings must use the same distinction. A sold comparison of two result surfaces must be visible as a comparison of two result surfaces.

## 2. One client-facing name for one product surface

A client report must not rotate between multiple labels for the same surface merely because the internal method uses several technical names.

If the job contract or owner-approved vocabulary specifies one familiar client label, that label is the canonical client-facing name throughout:

```text
TITLE
FIRST SCREEN
METHOD EXPLANATION
DETAILED FINDINGS
CONCLUSIONS
```

Alternative internal labels may remain in Level-2 evidence and methodology but must not create the impression that several different systems were tested when only one client-facing surface is being reported.

```text
ONE TESTED CLIENT SURFACE
+ MULTIPLE CLIENT LABELS
= AMBIGUITY / FAIL
```

## 3. A complete selected verification set must not be described as a partial research volume

A deliberately selected verification set can be the **complete and sufficient scope of that verification stage** even when it is smaller than the demand universe examined earlier.

Never write language equivalent to:

```text
THIS IS NOT THE WHOLE RESEARCH
ONLY A SMALL PART WAS STUDIED
```

when the selected set actually is the full approved set for that stage.

The client explanation must instead state:

```text
HOW MANY CANDIDATE DECISION AREAS WERE REVIEWED BEFORE SELECTION, WHEN MATERIAL
HOW MANY CASES WERE SELECTED
WHY THOSE CASES WERE SELECTED
WHICH DISTINCT DECISION TYPES THEY COVERED
WHY ADDITIONAL NEAR-DUPLICATE CHECKS WOULD NOT ADD A NEW DECISION QUESTION
WHY THE SELECTED SET WAS SUFFICIENT FOR THE DECLARED PURPOSE
```

Sufficiency must be justified by decision coverage, diversity and control coverage — never by an arbitrary universal quota.

A valid design may combine:

```text
DIAGNOSTIC CASES
= cases where the additional surface could change, refine or materially de-risk a decision

STABILITY CONTROLS
= already-clear cases used to check that the additional surface does not spuriously overturn a stable conclusion
```

The report must translate these ideas into ordinary client language.

## 4. Exact numbers replace vague scope words when canonical totals exist

When an exact accepted job count exists, client prose must use that number rather than vague phrases equivalent to:

```text
THE WHOLE ARRAY
A LARGE SET
ALL THE DATA
A LOT OF PHRASES
```

The report must make the numerical relationship explicit when different stages have different counts:

```text
FULL ACCEPTED DEMAND TOTAL
→ ASSIGNED / CLASSIFIED TOTAL
→ USER-TASK OR GROUP TOTAL WHEN MATERIAL
→ EXACT ORDINARY-RESULT VALIDATION TOTAL
→ SELECTED ADDITIONAL-SURFACE VERIFICATION TOTAL
→ FINAL MATERIAL ACTION / DECISION TOTAL WHEN MATERIAL
```

Counts must be explained, not merely listed. The reader must know whether a smaller number is a filter, a targeted validation set, a selected verification set, an implementation set or another derived subset.

## 5. Main report is not an exhaustive dump of already-correct routing

A full client research report must explain the work, but its main body must remain decision-oriented.

An exhaustive page-role or demand-routing catalogue must not dominate the report when most entries require no change and add no practical decision for the owner.

The main report should prioritize:

```text
WHAT NEEDS TO CHANGE
WHY IT NEEDS TO CHANGE
WHERE TO CHANGE IT
WHAT SHOULD BE PRESERVED
WHAT THE RESULT SHOULD LOOK LIKE
HOW TO CHECK IT
WHAT SPECIFIC BUSINESS FACT IS STILL NEEDED, IF ANY
```

Correct/no-change findings remain part of the research and may be summarized as positive validation. Detailed exhaustive mappings may live in a workbook, appendix or specialist/reference layer when that is useful and promised.

```text
FULL RESEARCH COMPLETENESS
!= REPEAT EVERY NO-CHANGE MAPPING IN MAIN CLIENT NARRATIVE
```

Do not rewrite the entire site into the report merely to demonstrate that every page was reviewed.

## 6. Main-report inclusion test

Before keeping any detailed item in the main client report, ask:

```text
DOES THIS ITEM REQUIRE A CHANGE?
DOES IT EXPLAIN WHY A MATERIAL CHANGE IS NEEDED?
DOES IT PROVE THAT AN APPARENT CHANGE WOULD BE WASTEFUL OR HARMFUL?
DOES IT EXPLAIN A MATERIAL PART OF THE SOLD METHOD / RESULT?
DOES THE OWNER NEED THIS DETAIL TO MAKE A DECISION?
```

If all are false, move the detail out of the main narrative or compress it into an appropriate positive summary.

## 7. Hard FAIL conditions

Any applicable condition below causes recipient FAIL:

```text
RESULT_SURFACE_DESCRIBED_AS_SEARCH_PROCESS_WHEN_OUTPUT_IS_MEANT
TITLE_DOES_NOT_NAME_THE_TWO_COMPARED_RESULT_SURFACES_ACCURATELY
MULTIPLE_CLIENT_LABELS_FOR_ONE_TESTED_SURFACE_CREATE_AMBIGUITY
COMPLETE_SELECTED_VERIFICATION_SCOPE_DESCRIBED_AS PARTIAL OR NOT-THE-WHOLE RESEARCH
SELECTED_CASE_COUNT_WITHOUT SUFFICIENCY AND SELECTION EXPLANATION
ARBITRARY_CASE_QUOTA_PRESENTED_AS METHODOLOGICAL SUFFICIENCY
VAGUE_SCOPE_WORDING_WHEN_EXACT_CANONICAL_TOTAL_EXISTS
COUNTS_LISTED_WITHOUT THEIR RELATION TO EACH OTHER
NON_ACTIONABLE_MAPPING_DUMP_DOMINATES_MAIN_REPORT
MAIN_REPORT_REPEATS_ALREADY_CORRECT_SITE MAPPING WITHOUT CLIENT DECISION VALUE
```

## 8. PASS gate

```text
RESULT_SURFACE_VOCABULARY_PRECISE = true
ONE_CLIENT_LABEL_PER_TESTED_SURFACE = true
SELECTED_VERIFICATION_SET_DESCRIBED_AS COMPLETE_FOR ITS DECLARED PURPOSE WHEN TRUE = true
SELECTION_AND_SUFFICIENCY_RATIONALE_VISIBLE = true
NO_ARBITRARY_UNIVERSAL_CASE_QUOTA = true
EXACT_CANONICAL_COUNTS_USED_WHEN_AVAILABLE = true
COUNT_RELATIONSHIPS_EXPLAINED = true
MAIN_REPORT_ACTION_DENSITY = PASS
NO_CHANGE_FINDINGS_SUMMARIZED_WITHOUT EXHAUSTIVE NON-ACTION DUMP = true
OWNER_CAN_DISTINGUISH RESEARCH DEPTH FROM MAIN-NARRATIVE PRIORITY = true
```

## 9. Non-repeat purpose

This gate prevents a client report from becoming misleading in three ways at once:

1. naming the wrong thing (`process` instead of `result surface`);
2. understating a complete selected verification stage as though it were incomplete research;
3. proving completeness by flooding the main report with no-action mappings rather than explaining the changes that matter.

This file follows `PERMANENT_STEP_RULE_UNIVERSALITY_AND_JOB_SEPARATION_GATE.md`.