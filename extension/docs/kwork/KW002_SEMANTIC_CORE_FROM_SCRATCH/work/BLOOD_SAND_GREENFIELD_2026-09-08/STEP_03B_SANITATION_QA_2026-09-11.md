# KW-002 Blood & Sand — Step03B sanitation QA

Date: 2026-09-11  
Status: **COMPLETE / PASS CANDIDATE / MAIN CHATGPT RETURN QA REQUIRED**

## Method and claim boundary

- Every one of the `24576` normalized identities is evaluated; sampling, truncation and first-N fallback are absent.
- State is derived from the normalized phrase text, frozen client business wording, frozen Ozon-only catalog names and explicit high-confidence context rules.
- Corrected Step04 family assignments are not sanitation inputs. They are joined only after sanitation for the separate reconciliation summary.
- Counts/frequency are not inputs to any sanitation decision.
- Bare catalog names or product terms with unresolved foreign/entity/information context go to `HOLD_AMBIGUOUS`; they do not inherit exclusion from longer phrases.
- This step makes no final intent, cluster, page, IA or delivery-selection decision.

## Mechanical accounting

```text
NORMALIZED_UNIQUE_ROWS = 24576
KEEP_CANDIDATE_ROWS = 5074
AUTO_EXCLUDED_ROWS = 6752
HOLD_AMBIGUOUS_ROWS = 12750
COLLAPSED_ROWS = 0
NORMALIZED_ACCOUNTING_RECONCILIATION = PASS
AUTO_EXCLUDED_WITHOUT_REASON = 0
HOLD_WITHOUT_REASON = 0
LOW_FREQUENCY_ONLY_EXCLUSIONS = 0
HIGH_FREQUENCY_ONLY_KEEPS = 0
AMBIGUOUS_SILENT_EXCLUSIONS = 0
RAW_LINEAGE_LOSS = 0
SEALED_SOURCE_VIOLATIONS = 0
```

## AUTO_EXCLUDED rows by reason code

```text
EXCLUDE_EXPLICIT_ASTROLOGY_INFORMATION = 2219
EXCLUDE_EXPLICIT_FOREIGN_ENTITY = 74
EXCLUDE_EXPLICIT_GAME = 242
EXCLUDE_EXPLICIT_MEDIA = 1667
EXCLUDE_EXPLICIT_ORGANIZATION = 9
EXCLUDE_EXPLICIT_PERSON = 23
EXCLUDE_EXPLICIT_PLACE = 340
EXCLUDE_EXPLICIT_RELIGIOUS_PRACTICE = 120
EXCLUDE_EXPLICIT_VEHICLE_OR_MODEL = 554
EXCLUDE_LEXICAL_GARBAGE = 1225
EXCLUDE_TECHNICAL_NOISE = 65
EXCLUDE_UNRELATED_PRODUCT = 214
```

## Occurrence-level reconciliation through normalized identities

```text
KEEP_CANDIDATE_OCCURRENCES = 5236
AUTO_EXCLUDED_OCCURRENCES = 7243
HOLD_AMBIGUOUS_OCCURRENCES = 13500
TOTAL_RECONCILED_RAW_OCCURRENCES = 25979
```

## Universal quality score

| Dimension | Score | Evidence |
|---|---:|---|
| GOAL_AND_OUTPUT_COMPLETENESS | 10.0/10 | All required Step03A/03B, funnel and reconciliation-ready outputs are present. |
| METHOD_AND_SOURCE_SUPPORT | 10.0/10 | Frozen Level-1/Level-2, job inputs and current RAW evidence govern every rule. |
| INPUT_EVIDENCE_AND_PROVENANCE_INTEGRITY | 10.0/10 | 79/79 outcomes and 25,979 occurrence identities reconcile exactly. |
| COVERAGE_AND_COMPLETENESS | 10.0/10 | Full universe processed with no sampling or truncation. |
| ANALYTICAL_CORRECTNESS_AND_CLAIM_BOUNDARIES | 9.5/10 | Conservative HOLD policy avoids unsupported rejection; Main ChatGPT semantic return QA remains required. |
| ADVERSARIAL_QA_QUALITY | 10.0/10 | Loss, double mapping, missing reasons, count-based decisions and source contamination were tested. |
| PERSISTENCE_READBACK_AND_REPRODUCIBILITY | 8.0/10 | Deterministic local artifacts are frozen; remote publication/readback is a separate handoff gate at generation time. |
| OWNER_CLIENT_USABILITY_AND_PLAIN_LANGUAGE | 9.5/10 | Governed states, reasons and lineage are explicit; large TSVs still require machine use. |
| INFORMATION_GAIN_COST_AND_EXECUTION_EFFICIENCY | 10.0/10 | Zero new paid/provider/search calls; existing evidence only. |
| DOWNSTREAM_READINESS | 9.0/10 | Reconciliation summary exists; owner delivery cap and Main ChatGPT acceptance intentionally remain open. |

```text
QUALITY_TOTAL_100 = 96.0
QUALITY_SCORE_10 = 9.6
ALL_HARD_GATES = PASS
OPEN_CRITICAL_DEFECTS = 0
```

No provider, Search, GenSearch or AI-search call was executed. Step05 was not started.
