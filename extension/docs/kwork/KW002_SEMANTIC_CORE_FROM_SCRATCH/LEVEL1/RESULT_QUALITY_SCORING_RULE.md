# KW-002 — LEVEL 1 RESULT QUALITY SCORING RULE

Status: **ACTIVE / OWNER-LOCKED / REQUIRED**  
Owner instruction: 2026-09-08  
Owner clarification: 2026-09-08 — **EACH QUALITY CRITERION IS SCORED ON ITS OWN 0–10 SCALE. DO NOT SCORE TEN CRITERIA AS 0–1 EACH.**

## 1. Purpose

Every major KW-002 result must be evaluated explicitly after execution and QA.

The score exists to prevent a technically complete artifact from being called high-quality merely because files, rows, commits or provider responses exist.

```text
FILE EXISTS != HIGH-QUALITY RESULT
ROW ACCOUNTING PASS != ANALYTICAL QUALITY PASS
PROVIDER SUCCESS != RESULT QUALITY
REMOTE READBACK != METHOD CORRECTNESS
```

## 2. Mandatory use

A quality score is required after:

```text
- every major roadmap step;
- every material rework/correction of a major step;
- every major client-facing deliverable;
- every late external-method audit that materially changes confidence in a previous PASS;
- final package QA.
```

The score must appear:

1. in the durable step/QA artifact;
2. in the owner-facing chat summary;
3. in current job state when it changes PASS/REWORK status.

## 3. Ten scoring dimensions — EACH DIMENSION IS 0–10

The default score uses ten dimensions.

**Each criterion is independently scored from 0 to 10.**

```text
1. GOAL_AND_OUTPUT_COMPLETENESS                  = 0.0–10.0
2. METHOD_AND_SOURCE_SUPPORT                    = 0.0–10.0
3. INPUT_EVIDENCE_AND_PROVENANCE_INTEGRITY      = 0.0–10.0
4. COVERAGE_AND_COMPLETENESS                     = 0.0–10.0
5. ANALYTICAL_CORRECTNESS_AND_CLAIM_BOUNDARIES  = 0.0–10.0
6. ADVERSARIAL_QA_QUALITY                        = 0.0–10.0
7. PERSISTENCE_READBACK_AND_REPRODUCIBILITY      = 0.0–10.0
8. OWNER_CLIENT_USABILITY_AND_PLAIN_LANGUAGE     = 0.0–10.0
9. INFORMATION_GAIN_COST_AND_EXECUTION_EFFICIENCY = 0.0–10.0
10. DOWNSTREAM_READINESS                         = 0.0–10.0
```

Forbidden interpretation:

```text
10 criteria × max 1 point each
1.0/1.0 per criterion
0.9/1.0 per criterion
```

Required interpretation:

```text
EVERY CRITERION = SCORE OUT OF 10
```

Example:

```text
Goal/output completeness = 10/10
Method/source support = 10/10
Analytical correctness = 9/10
Downstream readiness = 7/10
```

Each dimension must include a short evidence-based explanation. Do not award points merely because the field exists.

Decimal scores are allowed where justified, e.g. `8.5/10`.

## 4. Calculation formula

For the default ten dimensions:

```text
QUALITY_TOTAL_100
= sum of the ten individual 0–10 criterion scores
= 0–100

QUALITY_SCORE_10
= QUALITY_TOTAL_100 / 10
= 0–10
```

Both must be shown.

Example:

```text
10 + 10 + 10 + 10 + 9 + 9 + 10 + 9 + 9 + 7
= 93 / 100

QUALITY_SCORE = 9.3 / 10
```

Do not hide the individual criterion scores behind only one final average.

## 5. Score bands

The pass bands use the **final average on the 0–10 scale**:

```text
9.0–10.0 = PASS CANDIDATE
8.0–8.9  = REWORK_REQUIRED
6.0–7.9  = MATERIAL DEFECTS / INCOMPLETE
0.0–5.9  = FAIL
```

Equivalent totals for the default ten dimensions:

```text
90–100 / 100 = PASS CANDIDATE
80–89.9 / 100 = REWORK_REQUIRED
60–79.9 / 100 = MATERIAL DEFECTS / INCOMPLETE
0–59.9 / 100 = FAIL
```

A major step may be marked `PASS` only when:

```text
QUALITY_SCORE >= 9.0 / 10
AND
QUALITY_TOTAL_100 >= 90 / 100
AND
ALL HARD PASS GATES = PASS
AND
NO CRITICAL DEFECT = OPEN
```

The score never overrides a hard failure.

Example:

```text
QUALITY_SCORE = 9.4 / 10
QUALITY_TOTAL_100 = 94 / 100
REMOTE_READBACK = PASS
BUT OLD_RESEARCH_CONTAMINATION = true

=> STEP = FAIL / REWORK_REQUIRED
```

## 6. Critical-gate override

Any critical defect blocks PASS regardless of average score, including applicable cases such as:

```text
silent row loss
prohibited-source contamination
unsupported material conclusion
provider result not durably preserved when required
incorrect current owner/job scope
missing required output
unresolved contradiction in canonical state
client-facing artifact materially unusable
critical search/provider evidence gap
```

## 7. Late review can invalidate an old score/PASS

If a later external-method review, owner review, recipient review or evidence correction discovers a material defect:

```text
OLD PASS != IMMUTABLE
```

Required action:

```text
record defect
→ rescore previous result criterion-by-criterion on 0–10 scales
→ recalculate total /100 and average /10
→ invalidate PASS if score/hard gates no longer qualify
→ mark REWORK_REQUIRED
→ block dependent downstream steps where material
→ preserve old artifacts as history
→ correct
→ rerun QA
→ assign new score
```

Do not rewrite history as if the first version never existed.

## 8. Scoring must be discriminating

Forbidden:

```text
10/10 because all files exist
10/10 because row counts match
10/10 because provider returned 200
10/10 because remote readback passed
```

The score must expose weaknesses.

For every criterion below 10/10 state:

```text
WHAT LOST POINTS
WHY
WHETHER IT BLOCKS PASS
WHAT WOULD RAISE THE SCORE
```

## 9. Plain-language owner summary

After the technical score, always explain in ordinary Russian:

```text
Оценка результата: X/100, то есть Y/10.
Что сделано хорошо.
За что сняты баллы по конкретным критериям.
Можно ли идти дальше.
Что нужно исправить, если нельзя.
```

This does not replace the existing mandatory plain-language `why / what / result` summary; both are required.

## 10. Relation to Level 2

Every Level-2 step must define step-specific quality checks that feed the universal ten dimensions.

A generic score without step-specific criteria is insufficient.

Each Level-2 implementation/QA table must preserve the universal scale:

```text
CRITERION SCORE = 0–10
NOT 0–1
```

## 11. Marker

```text
KW002_RESULT_QUALITY_SCORE_REQUIRED = true
KW002_EACH_CRITERION_SCALE_MIN = 0.0
KW002_EACH_CRITERION_SCALE_MAX = 10.0
KW002_DEFAULT_CRITERION_COUNT = 10
KW002_QUALITY_TOTAL_MAX = 100.0
KW002_FINAL_AVERAGE_SCALE_MAX = 10.0
KW002_PASS_SCORE_MIN = 9.0
KW002_PASS_TOTAL_MIN = 90.0
KW002_ONE_POINT_PER_CRITERION_SCORING_FORBIDDEN = true
KW002_HARD_GATE_OVERRIDES_SCORE = true
KW002_LATE_REVIEW_CAN_INVALIDATE_PASS = true
KW002_SCORE_REQUIRED_IN_CHAT_AND_ARTIFACT = true
```