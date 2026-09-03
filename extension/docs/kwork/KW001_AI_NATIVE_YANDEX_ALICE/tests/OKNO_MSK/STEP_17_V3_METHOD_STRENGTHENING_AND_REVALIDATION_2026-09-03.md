# OKNO_MSK — STEP 17 V3 METHOD STRENGTHENING / REVALIDATION

Date: 2026-09-03  
Step: 17 — Search-vs-GenSearch comparison  
Status: **V3 METHOD/GOVERNANCE STRENGTHENED / BOUNDED DIAGNOSTIC PASS / V2 VERDICTS PRESERVED / STEP 18 NOT STARTED**

## 1. Why V3 exists

Step17 V2 repaired three concrete defects and produced a defensible bounded case analysis, but an external method audit against current Yandex guidance and current AI-search evaluation practice found that the process was still stronger at *disclosing* limitations than at *governing* what those limitations allow us to claim.

The most important process failure was visible in permanent methodology:

```text
JOB-LEVEL STEP17 V2 = PASS
PERMANENT STEP17 METHOD IN STEP_RULES_INDEX = UNVALIDATED
```

That state should not have been allowed to look final. V2 completed the concrete job output but did not yet convert the learned corrections into a permanent reusable Step17 method.

V3 closes that method/governance gap without inventing new provider observations.

## 2. What failed before and why

### S17-P01 — job output completion was allowed to substitute for method validation

V2 had 8/8 cases, 100% contract output coverage, direct Search trace and final readback, yet Step17 remained permanently `UNVALIDATED`.

Root cause: `OUTPUT COMPLETENESS != METHOD VALIDATION`.

Non-repeat control: owner-approved `STEP_17_SEARCH_VS_AI_COMPARISON_METHOD.md` now defines evidence units, prompt-family scope, temporal scope, provenance, confidence, claims and PASS.

### S17-P02 — limitations were written but not always operationalized

V2 correctly wrote `EXACT_QUERY != USER_JOB_FAMILY` and `SINGLE_RUN != LONG_TERM_STABILITY`, but these were still mostly claim-boundary prose.

Non-repeat control: every case now has required `ai_scope_class`, `prompt_family_coverage`, `ai_temporal_state`, categorical confidence, allowed claim and recheck trigger. A limitation that does not change allowed claims/confidence/PASS state is not considered governed.

### S17-P03 — exact-query diagnostic set was too easy to overread

Seven of eight cases have one GenSearch observation; C15-010 has two same-query observations in a short window. No selected case has representative same-job prompt-variant coverage or longitudinal first-party visibility evidence.

Current governed truth:

```text
8/8 current cases = EXACT_QUERY_DIAGNOSTIC
0/8 = USER_JOB_FAMILY_SUPPORTED
7/8 = SINGLE_SNAPSHOT
1/8 = SHORT_WINDOW_REPRODUCED
0/8 = TIME_SEPARATED_REPRODUCED
0/8 = LONGITUDINAL_FIRST_PARTY_SIGNAL
```

Therefore no family-wide or long-term stability claim is eligible in the current job.

### S17-P04 — decisive direct-read provenance was not forced to 1:1 completeness

V2 case reasoning referenced direct public reads for C15-007, C15-013 and C15-020 that were not all represented as dedicated rows in the original direct-page validation ledger.

Non-repeat control: `STEP_17_DIRECT_SOURCE_PROVENANCE_V3_SUPPLEMENT.tsv` materializes the missing decisive source records and the permanent method now blocks final PASS when `decisive_direct_source_provenance_missing > 0`.

### S17-P05 — source-worthiness terminology was too broad

The useful analytical object is the content fit of a source to the observed user task/answer, not an implied probability that the target will later be cited.

Permanent correction:

```text
AI_SOURCE_CONTENT_FIT != PROBABILITY_OF_AI_CITATION
```

## 3. External method audit

### Official Yandex — how Alice AI forms answers
Source: https://www.yandex.ru/support/webmaster/ru/alice

Supports: AI request analysis/refinement, Search-related source selection, source-order not being ranking, and task/quality-oriented source evaluation.

### Official Yandex — site visibility in Alice AI
Source: https://yandex.ru/support/webmaster/ru/service/alice-answers

Supports: examining example queries and other sites/pages in Alice AI answers; comparing them with own content; analyzing visibility over time; and expecting answer/source composition for the same query to change over time.

### Official Yandex — EPOS / user-task quality
Source: https://yandex.ru/support/webmaster/ru/epos

Supports comparing pages by how well they solve the real user task and by expertise, usefulness, originality and meaningful completeness rather than keyword imitation.

### Industry practice — prompt coverage / query fan-out
Sources:
- https://www.semrush.com/blog/which-ai-search-prompts-to-track/
- https://www.semrush.com/blog/query-fan-out/

Classification: industry practice, not Yandex authority. Supports representative-prompt evaluation, no one-exact-query family claim, and no mechanical prompt explosion.

### Independent cross-system volatility support
Source: https://ahrefs.com/blog/ai-overview-change/

Classification: cross-system evaluation support only. It reinforces the generic need for repeated/temporal observations; its numerical findings are not transferred to Yandex.

## 4. Current OKNO_MSK evidence truth after V3

No new Yandex provider calls were fabricated or executed during V3.

```text
NEW ORDINARY SEARCH CALLS = 0
NEW GENSEARCH CALLS = 0
NEW WEBMASTER CALLS = 0
NEW PAID PROVIDER COST = 0 RUB
```

Underlying V2 architecture verdicts remain unchanged because the audit found no evidence that reverses them:

```text
C15-004 = DE_RISK
C15-006 = DE_RISK
C15-007 = DE_RISK
C15-010 = NO_CHANGE
C15-013 = DE_RISK
C15-018 = NO_CHANGE
C15-019 = NO_CHANGE
C15-020 = INSUFFICIENT

CHANGE = 0
DE_RISK = 4
NO_CHANGE = 3
INSUFFICIENT = 1
ARCHITECTURE DELTA ROWS = 0
```

Content states remain:

```text
C15-004 = CONTENT_EXPANSION_CANDIDATE
C15-006 = INSUFFICIENT
C15-007 = NO_MATERIAL_CONTENT_GAP_OBSERVED
C15-010 = NO_MATERIAL_CONTENT_GAP_OBSERVED
C15-013 = CONTENT_EXPANSION_CANDIDATE
C15-018 = INSUFFICIENT
C15-019 = NOT_APPLICABLE
C15-020 = CONTENT_EXPANSION_CANDIDATE
```

The improvement is not a fake verdict change. The improvement is that verdicts are now paired with explicit claim eligibility and evidence scope.

## 5. V3 scope/confidence result

Authority: `STEP_17_V3_SCOPE_CONFIDENCE_LEDGER.tsv`

```text
CASES = 8/8
EXACT_QUERY_DIAGNOSTIC = 8/8
USER_JOB_FAMILY_SUPPORTED = 0/8
SINGLE_SNAPSHOT = 7/8
SHORT_WINDOW_REPRODUCED = 1/8 (C15-010)
TIME_SEPARATED_REPRODUCED = 0/8
LONGITUDINAL_FIRST_PARTY_SIGNAL = 0/8
ARCHITECTURE HIGH CONFIDENCE FROM AI = 0/8
ARCHITECTURE MODERATE = 7/8
ARCHITECTURE LOW = 1/8 (C15-020)
CONTENT MODERATE = 5/8
CONTENT LOW = 3/8
```

Interpretation:

```text
STEP17 CURRENT JOB RESULT
= BOUNDED DIAGNOSTIC SUPPORTING EVIDENCE
!= SITEWIDE AI VISIBILITY STUDY
!= USER-JOB-FAMILY PREVALENCE ESTIMATE
!= LONGITUDINAL ALICE VISIBILITY MEASUREMENT
```

## 6. Provenance repair

`STEP_17_DIRECT_SOURCE_PROVENANCE_V3_SUPPLEMENT.tsv` repairs dedicated-record gaps for decisive direct reads used in accepted V2 reasoning:

- C15-007 — exact used=true Svetokna panoramic-balcony URL recovered from raw Step16; accepted V2 material direct-read facts are materialized in a dedicated row.
- C15-013 — exact used=true Oknarosta French-window explanatory URL recovered from raw Step16 and publicly revalidated; definition, use-case, material, glazing and hardware guidance recorded.
- C15-020 — exact used=true Okna2.0 and Mosokna ranking/profile URLs recovered from raw Step16 and publicly revalidated; comparison criteria/current-year/profile-selection depth recorded.

This does not make source order or source count a ranking signal. It only closes 1:1 provenance for sources actually used decisively in content reasoning.

## 7. Canonical Step17 execution order from now on

```text
1. READ RULES / STEP17 METHOD / JOB FLOW / UPSTREAM AUTHORITIES
2. FREEZE STEP17 INPUT CASES FROM STEP15 BY EXACT ID
3. DIRECT-TRACE ORDINARY SEARCH FOR EACH CASE TO PERSISTED STEP13 RESULTS
4. TRACE RAW STEP16 AI OBSERVATIONS / USED SOURCES / REFINED QUERIES
5. ASSIGN AI SCOPE CLASS (EXACT / REPRESENTATIVE VARIANT / FAMILY)
6. ASSIGN TEMPORAL STATE (SINGLE / SHORT-WINDOW / TIME-SEPARATED / LONGITUDINAL)
7. APPLY PROMPT-FAMILY CONFIRMATION GATE WHEN A MATERIAL CLAIM DEPENDS ON WORDING ROBUSTNESS
8. APPLY TEMPORAL CONFIRMATION GATE WHEN A MATERIAL ARCHITECTURE CHANGE DEPENDS ON AI
9. DIRECT-READ EVERY DECISIVE AI-USED EXTERNAL SOURCE NEEDED FOR CONTENT-FIT CLAIMS
10. DIRECT-READ CURRENT TARGET PAGE AT REQUIRED MATERIAL DEPTH
11. COMPARE SEARCH-vs-AI: TASK / COMMERCIALITY / SPECIFICITY / FORMAT / SOURCE ROLE / REFINED QUERY / TARGET FIT
12. ISSUE ARCHITECTURE VERDICT: CHANGE / DE_RISK / NO_CHANGE / INSUFFICIENT
13. ISSUE SEPARATE CONTENT VERDICT: EXPANSION / NO MATERIAL GAP / INSUFFICIENT / N/A
14. ASSIGN CATEGORICAL CONFIDENCE THAT CHANGES ALLOWED CLAIMS
15. RECORD CLAIM BOUNDARY + RECHECK TRIGGER
16. VERIFY 1:1 DECISIVE SOURCE PROVENANCE
17. RUN REVERSE TRACE + CONTRACT/REQUIREMENT COVERAGE AUDIT
18. RUN ADVERSARIAL QA; LABEL INDEPENDENCE TRUTHFULLY
19. WRITE/READ BACK FINAL GITHUB ARTIFACT SET
20. HAND OFF TO STEP18 WITH EVIDENCE STRENGTH, NOT A FLATTENED AI SIGNAL
```

## 8. What Step17 must never do again

```text
JOB PASS != PERMANENT METHOD VALIDATION
LIMITATION DISCLOSED != LIMITATION GOVERNED
EXACT QUERY != USER JOB FAMILY
SINGLE SNAPSHOT != STABILITY
SHORT-WINDOW REPEAT != LONGITUDINAL STABILITY
SOURCE ORDER != RANK
USED SOURCE COUNT != RANK
URL/TITLE != MATERIAL CONTENT PROOF
AI SOURCE CONTENT FIT != CITATION PROBABILITY
GEN_SEARCH != CONSUMER ALICE
GEN_SEARCH != WEBMASTER ALICE VISIBILITY
NO ARCHITECTURE CHANGE != NO CONTENT CHANGE
ADVERSARIAL SELF REVIEW != INDEPENDENT REVIEW
```

## 9. V3 quality assessment

The external audit rated V2 approximately **8/10 for its bounded diagnostic purpose**, mainly penalizing prompt-family coverage, temporal reproducibility and provenance governance.

V3 does not pretend missing observations were collected. Instead it prevents them from being overclaimed, creates mandatory acquisition/recheck gates for any stronger conclusion, closes dedicated provenance gaps, and promotes a full permanent Step17 method.

```text
STEP17 METHOD / GOVERNANCE QUALITY = approximately 9/10
CURRENT OKNO_MSK AI DATA COVERAGE = BOUNDED / MODERATE, not 9/10 longitudinal coverage
```

A stronger 9.5–10/10 evidence study would require actual representative same-job variants and/or time-separated/first-party longitudinal Alice visibility where materially justified and available. That is deliberately not fabricated here.

## 10. Transition

```text
STEP17_V2_CASE_VERDICTS = PRESERVED
STEP17_V3_METHOD_GOVERNANCE = PASS
STEP17_V3_PROVENANCE_REPAIR = PASS
STEP17_CURRENT_SCOPE = BOUNDED_DIAGNOSTIC
STEP17_SITEWIDE_AI_VISIBILITY_CLAIM = FORBIDDEN
STEP17_LONGITUDINAL_AI_STABILITY_CLAIM = FORBIDDEN
STEP18_EXECUTION_STARTED = false
STEP18_PRESTEP_ALLOWED = true
NEXT_LEGAL_ACTION = STEP18_PRE_STEP_GATE_ONLY
```
