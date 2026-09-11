# KW-002 Blood & Sand — independent full-volume Step04 result audit Work prompt

Date: 2026-09-11
Status: CANONICAL ADVERSARIAL AUDIT PROMPT / NO CORRECTION IN THIS PASS

Continue the EXISTING KW-002 Blood & Sand greenfield semantic-core rehearsal.

THIS IS NOT A NEW PROJECT.
THIS IS NOT STEP05.
THIS IS NOT STEP06.
THIS IS NOT A PROVIDER-ACQUISITION TASK.
THIS IS NOT A CORRECTION PASS.

Your role is intentionally adversarial: independently evaluate the QUALITY OF THE ALREADY ACCEPTED STEP04 RESULT over the full data volume. Do not defend the previous Work output merely because its mechanical QA passed or because Work created it.

Repository:
`MaksimUnimax/Yandex_direct`

Branch:
`roadmap/kwork-productization-2026-08-28`

Job root:
`extension/docs/kwork/KW002_SEMANTIC_CORE_FROM_SCRATCH/work/BLOOD_SAND_GREENFIELD_2026-09-08`

## 0. Hard boundaries

Do NOT:
- call Wordstat;
- call ordinary Yandex Search;
- call GenSearch / AI-search / Alice;
- start or advance Step05;
- start Step06;
- modify Step03A or Step03B;
- rewrite Step04 families in this pass;
- perform final SERP clustering;
- perform final intent classification;
- map queries to pages;
- design IA/site structure;
- use sealed prior Blood & Sand analytical research.

This pass is AUDIT ONLY. Findings may recommend rework, but do not perform the rework.

## 1. Fetch current live branch first

Fetch CURRENT remote branch. Record LIVE_BASE_HEAD. Do not assume any SHA from this prompt is still current. Do not overwrite unrelated concurrent changes.

## 2. Read mandatory authorities in full

Read:

- `LEVEL1/EXECUTION_FAILURE_LEDGER_AND_ANTI_REGRESSION_RULE.md`
- `LEVEL1/DATA_VOLUME_SANITATION_AND_DELIVERY_SCOPE_RULE.md`
- `LEVEL1/PRE_STEP_EXTERNAL_RESEARCH_AND_SOURCE_DISCLOSURE_RULE.md`
- `LEVEL1/WORK_HANDOFF_RULE.md`
- `LEVEL2/STEP_RULES_INDEX.md`
- `KW002_EXECUTION_FAILURE_LEDGER_2026-09-11.md`
- `STEP_04_POST_SANITATION_MAIN_CHATGPT_RETURN_QA_2026-09-11.md`
- `STEP_04_EXTERNAL_METHODOLOGY_REVIEW_MAIN_CHATGPT_2026-09-11.md`
- `STEP_04_POST_SANITATION_QA_2026-09-11.md`
- `STEP_04_POST_SANITATION_WORK_RETURN_2026-09-11.md`
- `STEP_04_POST_SANITATION_ARTIFACT_MANIFEST_2026-09-11.json`
- `STEP_04_POST_SANITATION_MATERIALIZER_2026-09-11.py`
- `STEP_04_POST_SANITATION_FAMILY_TRIAGE_2026-09-11.tsv`
- `STEP_04_POST_SANITATION_TARGETED_EXPANSION_QUEUE_2026-09-11.tsv`
- `STEP_04_POST_SANITATION_SANITATION_FEEDBACK_REGISTER_2026-09-11.tsv`
- `STEP_04_POST_SANITATION_KNOWN_FAILURE_REGRESSION_MATRIX_2026-09-11.tsv`
- `STEP_04_POST_SANITATION_OCCURRENCE_FAMILY_LEDGER_2026-09-11.tsv`
- accepted corrected Step03B authorities used as Step04 input.

## 3. Fresh external methodology research is mandatory

Independently research current authoritative/practitioner guidance before auditing. At minimum verify principles against:

- Yandex Webmaster query selection / query clusters (meaning or user intent)
  https://yandex.ru/support/webmaster/ru/service/queries-selection
- Yandex Search quality / user objective
  https://yandex.com/support/webmaster/en/search-quality
- Topvisor SERP Top-10 clustering
  https://topvisor.com/ru/support/clustering/
- Ahrefs keyword clustering + term clustering
  https://ahrefs.com/blog/keyword-clustering/
- Ahrefs search intent
  https://ahrefs.com/blog/search-intent/
- Semrush keyword clustering
  https://www.semrush.com/blog/keyword-clustering/

You may add higher-quality current sources. Persist a source-to-method trace. Do not treat any external source as authority for Blood & Sand business facts.

## 4. Full-volume scope

Audit ALL:

```text
NORMALIZED_IDENTITIES = 24576
ACTIVE_PLUS_HOLD_IDENTITIES = 18135
EXCLUDED_IDENTITIES_HISTORY = 6441
RAW_OCCURRENCES = 25979
FAMILIES = 26
OBSERVED_FAMILIES = 24
COVERAGE_GAP_FAMILIES = 2
EXPANSION_QUEUE_ROWS = 13
SANITATION_FEEDBACK_ROWS = 10
```

No first-N, no sampling-only verdict, no representative-example-only verdict.

Sampling may be used only as an auxiliary explanation after exhaustive machine/analytical checks; it may not replace full-volume accounting and family-membership audit.

## 5. Core audit question

The Step04 method is accepted only as PRELIMINARY FAMILY TRIAGE, not final SEO clustering.

Audit whether the ACTUAL RESULT safely fulfills that limited role.

Do not judge it by whether it is a good final page cluster map. Judge whether it is a coherent, traceable, non-destructive intermediate topical/business family model that preserves ambiguity for later intent/SERP work.

## 6. Required independent audit dimensions

### A. Full accounting / lineage

Reconfirm independently:
- 25,979 unique RAW occurrence IDs;
- zero unassigned;
- zero unexpected duplicates;
- zero RAW lineage loss;
- every active/HOLD identity has exactly one preliminary primary family;
- every EXCLUDE remains excluded history;
- no Step03B state mutation occurred.

### B. Family coherence — FULL VOLUME

For every one of the 24 observed families, inspect ALL members algorithmically/semantically and determine whether the family has one defensible preliminary topical/business boundary.

Detect:
- multiple materially different user tasks hidden in one family;
- foreign-context leakage;
- catalog-name collisions hidden inside generic groups;
- product vs information mixtures that are too broad even for preliminary family triage;
- lexical rule artifacts;
- long-tail subthemes large enough to warrant a separate preliminary family or explicit subfamily marker;
- residual/noise buckets that conceal coherent business subfamilies.

Do NOT split/correct yet; report defects.

### C. Large-family heterogeneity audit

Mandatory adversarial attention to at least:
- PSF001 (~2,953 identities)
- PSF006 (~2,109)
- PSF014 (~6,540)
- PSF018 (~558)
- PSF024 (~708)

But do not limit the audit to them.

Use at least one independent diagnostic not equivalent to the existing ordered lexicon classifier, for example:
- token/phrase co-occurrence subtopic decomposition;
- term clustering;
- independent semantic grouping over all members;
- within-family lexical/topic entropy;
- rule-agnostic nearest-neighbor/topic partitioning available in the Work environment.

This diagnostic is NOT final SERP clustering and must not assign pages.

### D. Rule-order / lexicon bias audit

Read the materializer in full and test whether family outcome is unduly determined by rule ordering or hand-built dictionaries.

Find:
- overlapping rules where the first match hides a more informative family;
- substring/prefix collision risks not covered by current regressions;
- business-name dictionaries that over-pull unrelated phrases;
- generic product markers that overrule meaningful foreign context;
- ambiguity classes that are too generic to preserve downstream evidence needs.

Do not merely rerun the same existing regression matrix.

### E. User-task and intent safety

Check whether `primary_user_task_hypothesis` and `intent_hint_not_final` are supported by family members rather than by labels alone.

Flag any family where wording implies a final intent verdict that the phrase set cannot support without SERP.

### F. Business-lineage discipline

Check that catalog membership is used only as business support, not as proof that ambiguous searchers mean the product.

Audit especially:
- short catalog names;
- mythological/religious names;
- media/game/entity collisions;
- zodiac names;
- automobile-use/model collisions.

### G. Coverage-gap validity

Audit PSF025 and PSF026 and all 13 expansion queue rows.

For each queue row classify:
- VALID_GAP
- DUPLICATES_EXISTING_EVIDENCE
- OWNER_FACT_FIRST
- DEFER_TO_LATER_INTENT_OR_SERP
- NOT_MATERIAL
- DEFECTIVE_GAP_LOGIC

Do not make provider calls.

### H. Sanitation feedback validity

Audit all 10 feedback rows against their full underlying member sets. Determine whether each is:
- justified class-level feedback;
- too broad;
- too narrow;
- missing a material feedback class.

### I. Cross-family boundary audit

Detect whether materially equivalent preliminary topics/user tasks are split across multiple families solely due to classifier ordering.

Produce a symmetric family-boundary risk matrix or equivalent evidence.

### J. Frequency independence

Prove that frequency did not determine family assignment. Also check whether omission of frequency from assignment causes no semantic problem at this stage. Frequency may remain descriptive/prioritization evidence only.

## 7. Required row-level audit overlay

Materialize a full-volume overlay covering all 24,576 normalized identities with at least:

```text
normalized_phrase_id
canonical_phrase
current_step03b_state
current_step04_family_id
audit_family_coherence_status
audit_boundary_status
audit_user_task_status
audit_business_lineage_status
audit_ambiguity_preservation_status
audit_rule_bias_flag
audit_recommended_disposition
audit_reason
```

Allowed recommended dispositions:

```text
PASS_AS_PRELIMINARY_FAMILY
REVIEW_MEMBER_ASSIGNMENT
FAMILY_TOO_BROAD
FAMILY_TOO_NARROW
CROSS_FAMILY_BOUNDARY_DEFECT
AMBIGUITY_ROUTING_DEFECT
RULE_ORDER_DEFECT
COVERAGE_GAP_DEFECT
STEP03B_FEEDBACK_NEEDED
```

Do not correct rows in this pass.

## 8. Required family-level audit authority

For all 26 families materialize:

```text
family_id
member_count
coherence_score_10
boundary_precision_score_10
user_task_coherence_score_10
ambiguity_safety_score_10
rule_bias_risk_score_10
large_family_heterogeneity_findings
cross_family_overlap_findings
external_method_alignment
verdict
required_action
```

Verdict must be one of:
- PASS
- PASS_WITH_NONBLOCKING_FINDINGS
- REWORK_REQUIRED

## 9. Required outputs

Create at minimum:

1. `STEP_04_INDEPENDENT_FULL_VOLUME_RESULT_AUDIT_REPORT_2026-09-11.md`
2. `STEP_04_INDEPENDENT_FULL_VOLUME_RESULT_AUDIT_OVERLAY_2026-09-11.tsv`
3. `STEP_04_INDEPENDENT_FAMILY_COHERENCE_AUDIT_2026-09-11.tsv`
4. `STEP_04_INDEPENDENT_FAMILY_BOUNDARY_RISK_MATRIX_2026-09-11.tsv`
5. `STEP_04_INDEPENDENT_QUEUE_FEEDBACK_AUDIT_2026-09-11.tsv`
6. `STEP_04_INDEPENDENT_EXTERNAL_METHOD_SOURCE_TRACE_2026-09-11.md`
7. `STEP_04_INDEPENDENT_AUDIT_METRICS_2026-09-11.json`
8. artifact manifest with row counts / bytes / SHA-256.

If any output is very large, follow the owner-relay rule. ZIP is transport only, never sole authority.

## 10. Scoring

Do NOT inherit the previous 97.20/100 self-score.

Create a fresh audit score based on independent evidence. At minimum score:
- full-volume accounting
- family coherence
- boundary precision
- ambiguity preservation
- user-task coherence
- business-lineage discipline
- lexical/rule-order bias control
- cross-family overlap control
- coverage-gap quality
- sanitation-feedback quality
- traceability
- downstream safety
- external-method alignment

PASS requires:
- score >= 90/100;
- no critical family-boundary defect;
- no silent loss;
- no Step03B mutation;
- no evidence that preliminary families are being treated as final page clusters;
- all material hidden heterogeneity explicitly surfaced.

## 11. Final verdict

Use exactly one:

```text
STEP04_RESULT_AUDIT = PASS
STEP04_RESULT_AUDIT = PASS_WITH_NONBLOCKING_FINDINGS
STEP04_RESULT_AUDIT = REWORK_REQUIRED
```

If rework is required, specify exact family/rule classes and affected row counts, but DO NOT perform the correction.

## 12. Stop boundary

After artifacts + QA + publication/owner relay, STOP for Main ChatGPT review.

Provider calls = 0.
Step05 advancement = false.
Step06 advancement = false.
No correction in this pass.
