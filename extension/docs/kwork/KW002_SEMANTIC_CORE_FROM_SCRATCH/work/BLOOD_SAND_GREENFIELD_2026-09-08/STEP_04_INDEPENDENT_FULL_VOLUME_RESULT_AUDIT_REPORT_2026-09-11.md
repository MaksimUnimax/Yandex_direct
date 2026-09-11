# KW-002 Blood & Sand — independent full-volume Step04 result audit

Date: 2026-09-11

Live base fetched before execution: `8a09e1610d68f61769b6a4d44d1382cab4dd37b7`

Role: adversarial result audit only; no correction and no Step05/06 advancement.

## Verdict

```text
STEP04_RESULT_AUDIT = REWORK_REQUIRED
FRESH_AUDIT_SCORE = 67.69/100
PROVIDER_CALLS = 0
STEP04_CORRECTIONS = 0
STEP05_ADVANCEMENT = false
STEP06_ADVANCEMENT = false
```

The accepted Step04 result is mechanically complete and traceable, but it is not safe to pass unchanged as preliminary family authority. Three material, reproducible family/rule classes affect **255 unique normalized identities**. PASS is impossible because critical family-boundary and rule-bias defects exist even though RAW lineage is intact.

## Full-volume accounting

| Control | Result |
|---|---:|
| Normalized identities | 24,576 / unique 24,576 |
| Active + HOLD identities | 18,135 / exactly one observed family |
| EXCLUDE history | 6,441 / no Step04 family / unchanged |
| RAW occurrences | 25,979 / unique occurrence IDs 25,979 |
| RAW lineage loss | 0 |
| Step03B state/reason mismatches | 0 |
| Families | 26 = 24 observed + 2 zero-member gaps |
| Queue / feedback | 13 / 10, all audited |

The audit overlay contains all 24,576 identities. Excluded identities are present for accounting with `NOT_APPLICABLE_EXCLUDED_HISTORY`; they were not re-triaged.

## Material defects — no correction performed

| Family / rule class | Affected identities | Exhaustive evidence | Required later action |
|---|---:|---|---|
| PSF019 broad `игр*` prefix | 8 | Every row has independent `TOY`; none has an exact GAME signal. Examples include `игрушка оберег`, `игрушка талисман`, `алатырь игрушки`. | Separate game morphology from `игруш*`; audit blast radius, then reroute only in an approved correction pass. |
| PSF014 early zodiac route | 199 unique | 156 MEANING + 38 MEDIA + 5 TOY. PSF014 says the task is insufficiently specified, but these rows state a task. | Rework precedence/coverage across PSF014↔PSF015/018/012 after Main ChatGPT approval. |
| PSF001 generic fall-through | 48 | Explicit `сделать/создать/изготовить/связать/сшить/сплести/своими руками` task survives inside a family labelled unqualified. | Define a DIY preliminary task boundary or marker; do not infer a final page. |

These counts are mutually disjoint by current family, so total material affected identities = 8 + 199 + 48 = **255**. The overlay recommends `RULE_ORDER_DEFECT` for 207 and `FAMILY_TOO_BROAD` for 48; all other 24,321 identities receive no material row-level defect in this pass.

## Independent full-volume diagnostic

The diagnostic did not reuse the ordered classifier as its semantic judge. It fitted TF-IDF word/co-occurrence features and a deterministic 32-topic MiniBatchKMeans model over all 18,135 active/HOLD phrases, computed family centroids and symmetric cross-family similarities, and evaluated simultaneous signals rather than first-match routing. Generic product/zodiac words were removed from the diagnostic feature space to reduce label echo. Short-text/topic metrics remain warnings, not truth and not final SERP clustering.

| Family | Members | Topic entropy | Dominant-topic share | Mean own-centroid cosine | Alternate-centroid override rate | Verdict |
|---|---:|---:|---:|---:|---:|---|
| PSF001 | 2953 | 0.678 | 0.328 | 0.044 | 0.006 | REWORK_REQUIRED |
| PSF006 | 2109 | 0.727 | 0.231 | 0.259 | 0.009 | PASS_WITH_NONBLOCKING_FINDINGS |
| PSF014 | 6540 | 0.669 | 0.445 | 0.107 | 0.004 | REWORK_REQUIRED |
| PSF018 | 558 | 0.700 | 0.400 | 0.206 | 0.050 | PASS_WITH_NONBLOCKING_FINDINGS |
| PSF024 | 708 | 0.663 | 0.380 | 0.118 | 0.031 | PASS_WITH_NONBLOCKING_FINDINGS |

- PSF006 is lexically heterogeneous but deliberately preserves short catalog-name ambiguity; this is nonblocking only while catalog membership is not treated as product intent.
- PSF018 is heterogeneous by design as an explicit media/title collision family; its feedback must remain active.
- PSF024 is not a semantic page cluster. It is safe only as a quarantined residual/feedback bucket.
- Topic entropy and nearest-centroid results for all 26 families are in the family authority and metrics JSON; all 676 directed cells of the symmetric 26×26 boundary matrix are materialized.

## Queue and coverage gaps

All 13 rows were classified without a provider call:

| Classification | Count |
|---|---:|
| VALID_GAP | 2 |
| OWNER_FACT_FIRST | 5 |
| DUPLICATES_EXISTING_EVIDENCE | 5 |
| DEFER_TO_LATER_INTENT_OR_SERP | 1 |

PSF025 and PSF026 are valid zero-member coverage hypotheses, not observed demand. PSQ005-PSQ008 duplicate current qualified evidence in whole or material part; PSQ010 also duplicates preserved historical E013 evidence. PSQ011 explicitly belongs after a concrete later collision. Exact row decisions are in the combined queue/feedback audit.

## Sanitation feedback

Nine of ten feedback rows are justified class-level controls. PSFB003 is `TOO_BROAD`: legitimate game ambiguity is mixed with eight non-game toy rows produced by the Step04 prefix defect. Three missing material audit classes are appended for PSF001 DIY, PSF014 task leakage and PSF019 toy/game collision. They are findings only and make zero Step03B changes.

## Frequency and lineage discipline

No frequency field enters the independent signals, TF-IDF topic membership defect rules, family verdicts or queue classifications. Frequency remains descriptive only. Omitting frequency is semantically safe at preliminary triage because relevance, referent and user task are not frequency functions; later prioritization may use frequency without changing these boundaries.

Catalog/brief membership is treated only as business support. It is not evidence that a short mythological, religious, zodiac, media, game, entity or vehicle-collision phrase means the client's product.

## Fresh score

The previous 97.20/100 self-score was not inherited.

| Dimension | Score / 10 |
|---|---:|
| full_volume_accounting | 10.0 |
| family_coherence | 5.5 |
| boundary_precision | 5.0 |
| ambiguity_preservation | 8.0 |
| user_task_coherence | 5.0 |
| business_lineage_discipline | 8.5 |
| lexical_rule_order_bias_control | 3.0 |
| cross_family_overlap_control | 4.5 |
| coverage_gap_quality | 7.0 |
| sanitation_feedback_quality | 7.0 |
| traceability | 9.5 |
| downstream_safety | 8.0 |
| external_method_alignment | 7.0 |

Equal-weight total: **67.69/100**. The score is below 90 and critical boundary defects exist; either condition blocks PASS.

## External-method alignment and limits

The fresh method trace is in `STEP_04_INDEPENDENT_EXTERNAL_METHOD_SOURCE_TRACE_2026-09-11.md`. It separates preliminary term diagnostics from final SERP clustering and keeps user objective, ambiguity and business facts distinct. No ordinary search, Wordstat, GenSearch, AI-search or sealed prior Blood & Sand analysis was used.

## Stop state

This pass materialized audit evidence only. The accepted Step04 source artifacts retain their verified SHA-256 hashes and were not rewritten. Work stops here for Main ChatGPT review. Any correction, queue revision or Step05 resumption requires a new explicit release.
