# KW-002 — universal method-layer audit and refactor

Date: 2026-09-11
Status: **COMPLETE / EARLY STEPS + STEP04 UNIVERSALIZATION PASS**

## Purpose

Verify that permanent KW-002 methodology is reusable for any eligible site/business and does not encode one job's client vocabulary, family IDs, counts, owner approvals or observed defect examples as the rule itself.

Canonical separation:

```text
LEVEL1 = universal root causes + cross-step rules
LEVEL2 = universal Step00–22 roadmap/methods
work/<JOB_ID>/ = concrete job facts/evidence/examples/counts/status
```

## Files reviewed

### Level1

- `CLIENT_INTAKE_AND_SCOPE_RULE.md`
- `COMMON_RULES.md`
- `DATA_VOLUME_SANITATION_AND_DELIVERY_SCOPE_RULE.md`
- `EXECUTION_FAILURE_LEDGER_AND_ANTI_REGRESSION_RULE.md`
- `INHERITED_KW001_UNIVERSAL_RULES.md`
- `JOB_DATA_SEPARATION_AND_LIFECYCLE.md`
- `METHOD_SOURCE_AND_EVIDENCE_RULES.md`
- `PRE_STEP_EXTERNAL_RESEARCH_AND_SOURCE_DISCLOSURE_RULE.md`
- `RESULT_QUALITY_SCORING_RULE.md`
- `SERP_COVERAGE_MODE_DECISION_2026-09-10.md`
- `WORK_HANDOFF_RULE.md`

### Level2

- `README.md`
- `STEP_RULES_INDEX.md`
- `INHERITED_KW001_RULES_MAP.md`
- `INHERITED_KW001_STEP_RULES.md`
- `STEP_02_SEED_ACQUISITION_QUALITY_GATE.md`
- `STEP_03_WORDSTAT_DEPTH_JUSTIFICATION_GATE.md`
- `STEP_03_WORDSTAT_RAW_PERSISTENCE_GATE.md`
- former `STEP04_OWNER_EXECUTION_GATE_2026-09-10.md`

## Material violations found and corrected

### 1. Universal failure ledger described concrete job incidents instead of only the mechanism

Problem:

The permanent Level1 failure authority mixed universal rules with current-job examples/counts.

Why structurally wrong:

A future site should not need knowledge of the job that discovered the error in order to understand or execute the prevention rule.

Correction:

`LEVEL1/EXECUTION_FAILURE_LEDGER_AND_ANTI_REGRESSION_RULE.md` was rewritten around reusable root causes such as:

- source/scope authority drift;
- business completeness vs search completeness;
- provider success vs durable evidence;
- destructive normalization;
- unsafe prefix/stem shortcuts;
- business-token vs foreign-context collisions;
- mechanical QA vs semantic QA;
- premature ambiguity destruction;
- missing occurrence-level reproducibility;
- example-only patching;
- upstream invalidation;
- first-match precedence bias;
- generic fallback/closed-taxonomy bias;
- missing independent taxonomy challenge;
- duplicate evidence acquisition;
- owner-fact gaps sent to provider;
- preliminary family mistaken for final SEO cluster.

Concrete counts/examples remain job evidence only.

### 2. Data-volume/sanitation Level1 rule contained job-specific defect history

Problem:

Permanent sanitation guidance named one rehearsal's concrete defect history.

Correction:

`LEVEL1/DATA_VOLUME_SANITATION_AND_DELIVERY_SCOPE_RULE.md` now states only generic mechanisms and gates: lexical collision risk, referent/intent separation, ambiguity preservation, independent semantic QA and full lineage.

### 3. Step02 universal gate contained concrete rehearsal counts and niche examples

Problem:

The Step02 gate included one job's probe count/catalog coverage and niche-specific examples as part of the permanent lesson.

Root cause:

Historical evidence was stored in the method layer instead of being abstracted into the information-acquisition failure mechanism.

Correction:

`LEVEL2/STEP_02_SEED_ACQUISITION_QUALITY_GATE.md` now explains generically:

```text
business-lineage coverage != search-probe quality
ambiguous bare name needs refinement/control
client taxonomy != acquisition taxonomy
information gain > trivial call-count economy
```

No client/product-specific vocabulary is required to execute the gate.

### 4. Step03 depth gate contained a current-job application section

Problem:

A universal Level2 gate included a section for the active rehearsal and historical blocker.

Root cause:

Job execution state was mixed with provider-depth methodology.

Correction:

`LEVEL2/STEP_03_WORDSTAT_DEPTH_JUSTIFICATION_GATE.md` now contains only the general failure mechanism:

```text
provider/technical parameter != semantic coverage decision
```

and a reusable evidence-depth justification process.

### 5. Job-specific Step04 owner approval lived inside Level2

Problem:

`LEVEL2/STEP04_OWNER_EXECUTION_GATE_2026-09-10.md` contained current owner approval, current counts, current job paths and current execution status.

Correction:

The file was moved to the concrete job root as historical evidence:

`work/BLOOD_SAND_GREENFIELD_2026-09-08/STEP04_OWNER_EXECUTION_GATE_2026-09-10.md`

and removed from Level2.

### 6. Step04 lacked a dedicated universal quality gate for the newly discovered rule-system failure classes

Correction:

Created:

`LEVEL2/STEP_04_PRELIMINARY_FAMILY_TRIAGE_QUALITY_GATE.md`

It defines universal controls for:

- first-match precedence bias;
- generic fallback / missing task discovery;
- lexical overreach;
- independent taxonomy challenge;
- preliminary-vs-final cluster boundary;
- occurrence-level reproducibility;
- coverage-gap and owner-fact separation.

### 7. Roadmap index carried job-history provenance and was not explicit enough about root causes

Correction:

`LEVEL2/STEP_RULES_INDEX.md` was rebuilt as a universal Step00–22 roadmap.

Every step now states, as applicable:

```text
WHY
INPUT
METHOD
UNIVERSAL ROOT CAUSES PREVENTED
OUTPUT
PASS
```

The roadmap contains no current job family IDs, row counts, client/site names or owner execution status.

### 8. Inherited Step rules mentioned the current rehearsal in the universal layer

Correction:

`LEVEL2/INHERITED_KW001_STEP_RULES.md` was rewritten as generic reusable rules only, including reasons/failure mechanisms and references to the stricter current dedicated gates.

## Files reviewed and already suitable as universal authorities

No material current-site contamination requiring rewrite was found in:

- `LEVEL1/CLIENT_INTAKE_AND_SCOPE_RULE.md`
- `LEVEL1/METHOD_SOURCE_AND_EVIDENCE_RULES.md`
- `LEVEL1/PRE_STEP_EXTERNAL_RESEARCH_AND_SOURCE_DISCLOSURE_RULE.md`
- `LEVEL1/RESULT_QUALITY_SCORING_RULE.md`
- `LEVEL1/SERP_COVERAGE_MODE_DECISION_2026-09-10.md` — product-level policy, not client-specific
- `LEVEL1/WORK_HANDOFF_RULE.md`
- `LEVEL2/STEP_03_WORDSTAT_RAW_PERSISTENCE_GATE.md`
- `LEVEL2/INHERITED_KW001_RULES_MAP.md`

`LEVEL1/INHERITED_KW001_UNIVERSAL_RULES.md` was checked for current job/site references; no current-job site values were found. Its KW-001 provenance is method-history, while executable current KW-002 behavior is controlled by the current universal Level1/Level2 authorities.

## New hard architecture authority

Created:

`LEVEL1/ROADMAP_AND_METHOD_GENERALIZATION_RULE.md`

Universal promotion sequence:

```text
CONCRETE JOB DEFECT
→ ROOT CAUSE / MECHANISM
→ PROVE CLASS-GENERAL RELEVANCE
→ UNIVERSAL LEVEL1 CONTROL
→ APPLICABLE LEVEL2 GATES
→ CONCRETE EXAMPLES REMAIN IN work/<JOB_ID>/
```

Forbidden:

```text
one bad phrase -> global special case
one family ID -> permanent taxonomy
one client's vocabulary -> universal lexical rule
current owner approval -> Level2 method
```

## Current W08 synchronization

The current Step04 corrective Work pass was revised so it does not patch the current site's observed 255 rows as special cases.

Canonical V2 prompt:

`work/BLOOD_SAND_GREENFIELD_2026-09-08/STEP_04_POST_AUDIT_CORRECTIVE_REWORK_WORK_PROMPT_V2_UNIVERSAL_CAUSE_2026-09-11.md`

V2 release:

`work/BLOOD_SAND_GREENFIELD_2026-09-08/STEP_04_POST_AUDIT_CORRECTIVE_REWORK_EXECUTION_RELEASE_V2_UNIVERSAL_CAUSE_2026-09-11.md`

The concrete audit rows are regression fixtures. W08 must correct the general producer mechanisms and rerun the complete current job universe.

## Universal QA result

```text
LEVEL1_JOB_SPECIFIC_RULE_DEFINITION_FOUND_AND_LEFT_UNCORRECTED = 0
LEVEL2_CURRENT_JOB_OWNER_GATE_REMAINING = 0
LEVEL2_CURRENT_JOB_COUNTS_AS_METHOD_THRESHOLDS = 0
LEVEL2_CURRENT_JOB_FAMILY_IDS_AS_UNIVERSAL_TAXONOMY = 0
EARLY_STEP_FAILURES_WITHOUT_ROOT_CAUSE_IN_CURRENT_DEDICATED_GATES = 0
UNIVERSAL_STEP00_22_ROADMAP_PRESENT = true
ANY_SITE_EXECUTABILITY_TEST = PASS
W08_BOUND_TO_UNIVERSAL_ROOT_CAUSES = true
```

## Boundary

This methodology refactor does not change the already collected current-job evidence or accepted Step03A/Step03B states. It changes how future/current corrections are governed and how permanent methodology is stored.
