# KW-002 — LEVEL 1 RESULT QUALITY SCORING RULE

Status: **ACTIVE / OWNER-LOCKED / REQUIRED**  
Owner instruction: 2026-09-08

## 1. Purpose

Every major KW-002 result must be evaluated explicitly on a **10-point quality scale** after execution and QA.

The score exists to prevent a technically complete artifact from being called high-quality merely because files, rows, commits or provider responses exist.

```text
FILE EXISTS != HIGH-QUALITY RESULT
ROW ACCOUNTING PASS != ANALYTICAL QUALITY PASS
PROVIDER SUCCESS != RESULT QUALITY
REMOTE READBACK != METHOD CORRECTNESS
```

## 2. Mandatory use

A 10-point quality score is required after:

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

## 3. Ten scoring dimensions

Default score is the sum of ten dimensions, each worth up to 1.0 point:

```text
1. GOAL_AND_OUTPUT_COMPLETENESS
2. METHOD_AND_SOURCE_SUPPORT
3. INPUT_EVIDENCE_AND_PROVENANCE_INTEGRITY
4. COVERAGE_AND_COMPLETENESS
5. ANALYTICAL_CORRECTNESS_AND_CLAIM_BOUNDARIES
6. ADVERSARIAL_QA_QUALITY
7. PERSISTENCE_READBACK_AND_REPRODUCIBILITY
8. OWNER_CLIENT_USABILITY_AND_PLAIN_LANGUAGE
9. INFORMATION_GAIN_COST_AND_EXECUTION_EFFICIENCY
10. DOWNSTREAM_READINESS
```

Each dimension must include a short evidence-based explanation. Do not award points merely because the field exists.

Half/decimal points are allowed where justified.

## 4. Score bands

```text
9.0–10.0 = PASS CANDIDATE
8.0–8.9  = REWORK_REQUIRED
6.0–7.9  = MATERIAL DEFECTS / INCOMPLETE
0.0–5.9  = FAIL
```

A major step may be marked `PASS` only when:

```text
QUALITY_SCORE >= 9.0 / 10
AND
ALL HARD PASS GATES = PASS
AND
NO CRITICAL DEFECT = OPEN
```

The score never overrides a hard failure.

Example:

```text
QUALITY_SCORE = 9.4
REMOTE_READBACK = PASS
BUT OLD_RESEARCH_CONTAMINATION = true

=> STEP = FAIL / REWORK_REQUIRED
```

## 5. Critical-gate override

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

## 6. Late review can invalidate an old score/PASS

If a later external-method review, owner review, recipient review or evidence correction discovers a material defect:

```text
OLD PASS != IMMUTABLE
```

Required action:

```text
record defect
→ rescore previous result
→ invalidate PASS if score/hard gates no longer qualify
→ mark REWORK_REQUIRED
→ block dependent downstream steps where material
→ preserve old artifacts as history
→ correct
→ rerun QA
→ assign new score
```

Do not rewrite history as if the first version never existed.

## 7. Scoring must be discriminating

Forbidden:

```text
10/10 because all files exist
10/10 because row counts match
10/10 because provider returned 200
10/10 because remote readback passed
```

The score must expose weaknesses.

For every score below 10/10 state:

```text
WHAT LOST POINTS
WHY
WHETHER IT BLOCKS PASS
WHAT WOULD RAISE THE SCORE
```

## 8. Plain-language owner summary

After the technical score, always explain in ordinary Russian:

```text
Оценка результата: X/10.
Что сделано хорошо.
За что сняты баллы.
Можно ли идти дальше.
Что нужно исправить, если нельзя.
```

This does not replace the existing mandatory plain-language `why / what / result` summary; both are required.

## 9. Relation to Level 2

Every Level-2 step must define step-specific quality checks that feed the universal 10-point score.

A generic 10-point score without step-specific criteria is insufficient.

## 10. Marker

```text
KW002_RESULT_QUALITY_SCORE_REQUIRED = true
KW002_SCORE_SCALE_MAX = 10.0
KW002_PASS_SCORE_MIN = 9.0
KW002_HARD_GATE_OVERRIDES_SCORE = true
KW002_LATE_REVIEW_CAN_INVALIDATE_PASS = true
KW002_SCORE_REQUIRED_IN_CHAT_AND_ARTIFACT = true
```
