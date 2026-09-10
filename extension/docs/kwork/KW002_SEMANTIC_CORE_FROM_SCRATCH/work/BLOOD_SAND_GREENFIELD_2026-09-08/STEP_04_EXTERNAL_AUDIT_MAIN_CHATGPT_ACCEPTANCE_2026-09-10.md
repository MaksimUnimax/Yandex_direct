# STEP 04 — EXTERNAL AUDIT MAIN CHATGPT ACCEPTANCE

Date: 2026-09-10
Job: `BLOOD_SAND_GREENFIELD_2026-09-08`
Status: **AUDIT ACCEPTED / LIMITED STEP04 REWORK REQUIRED / STEP05 REMAINS PAUSED**

## Accepted audit authorities

Original Step04 frozen execution commit:
`91fc6e1ce155c0f854c9d3c7ebf5a7b5dea40d70`

External audit content commit:
`cf5fe62fa7e8260b2c6d08caec74070fb065596d`

External audit final readback commit:
`54dffce61ee1473791dd4efcf7329698b1f98a45`

Accepted audit result:

```text
AUDIT_VERDICT = REWORK_REQUIRED
QUALITY_SCORE_100 = 87/100
QUALITY_SCORE_10 = 8.7/10
HARD_FAILS = NONE
STEP04_CONCLUSION_MATERIALLY_CHANGES = NO
STEP05_RESUME_RECOMMENDATION = KEEP_PAUSED_PENDING_STEP04_REWORK
```

Main ChatGPT independently read the audit return, affected family rows, affected expansion rows and defect register from the live branch. The audit is accepted as the corrective authority for Step04.

## Git reconciliation

`cf5fe62...` is the content commit that materialized the five audit outputs.
`54dffce...` is the following finalization commit that changed only the Work-return receipt from readback-pending to `REMOTE_GITHUB_READBACK = PASS / 5/5`.

Later live-branch commits after `54dffce...` affect unrelated MK02 productization files, not this KW-002 Step04 audit authority. No force update is authorized.

## Accepted defect set

### Global material defect

`D14 QA_OR_REPRODUCIBILITY_DEFECT`

The aggregate family counts reconcile to 25,979 occurrences, but there is no durable deterministic occurrence-level ledger showing exactly which current occurrence was assigned to which family. A corrected Step04 must publish a complete occurrence identity → family mapping and prove zero unassigned / zero duplicated occurrence identities.

### Family rows requiring correction

```text
F010 = wording-only clarification; keep mixed umbrella but expose sub-boundaries
F011 = correct assignment logic; explicit media member(s) must leave effects/audience
F015 = wording/subtype cleanup for automotive non-client products such as paint/color
F017 = explicit media remains out-of-scope; unqualified `счастливый амулет` must not be forced out-of-scope
F022 = explicit unrelated products remain out-of-scope; unqualified `талисман кота` must not be forced out-of-scope
F025 = explicit `оберег для водителя и автомобиля` belongs to supported car-use family F003
F032 = remove as standalone material coverage gap; merge run-70 exact-form zero provenance into F003
```

The known examples are minimum demonstrated defects. The rework must fix the underlying deterministic rule and rerun assignment over the complete frozen end-of-Step04 corpus so sibling occurrences affected by the same defective rule are corrected too. Do not manually patch only the representative examples.

### Expansion queue corrections

```text
E004 + E017 -> one client-fact-gated prayer/product boundary item
E007 + E014 -> one consolidated car-use / vehicle-collision item
```

Expected corrected queue accounting:

```text
QUEUE_ROWS = 15
OWNER_OR_CLIENT_FACT_ROWS = 5
PROVIDER_RELEVANT_QUEUE_ROWS = 13
```

No Step05 provider work is authorized by this acceptance.

## Rework scope

This is a **limited corrective pass**, not a new Step04 research run.

Use only evidence available at end of Step04:
- frozen client/business/assortment authorities;
- complete current Step03 79/79 feed-forward corpus;
- original Step04 artifacts;
- accepted external audit artifacts and methodology source pack.

Do not use later Step05 `!чётки` evidence to change the corrected Step04 semantic decisions. It may be mentioned only as post-hoc evidence outside the rework decision logic.

Do not use sealed prior Blood & Sand research.
Do not call Wordstat, ordinary Search, GenSearch, Alice or any other provider.
Do not perform final row cleanup, SERP clustering, query-to-page ownership, IA or Page Jobs.

## Required corrected outputs

The corrective Work pass must create new versioned authorities and preserve the historical original Step04 files:

1. `STEP_04_OCCURRENCE_FAMILY_LEDGER_CORRECTED_2026-09-10.tsv`
2. `STEP_04_FAMILY_TRIAGE_CORRECTED_2026-09-10.tsv`
3. `STEP_04_TARGETED_EXPANSION_QUEUE_CORRECTED_2026-09-10.tsv`
4. `STEP_04_LIMITED_REWORK_QA_2026-09-10.md`
5. `STEP_04_LIMITED_REWORK_WORK_RETURN_2026-09-10.md`

Do not overwrite the original 2026-09-10 Step04 family/queue/QA/return artifacts audited at `91fc6e1...`.

## Acceptance conditions before Step05 may resume

```text
CURRENT_SOURCE_RESOLUTION = 79/79
RESULT_OCCURRENCES = 24722
ASSOCIATION_OCCURRENCES = 1257
TOTAL_OCCURRENCES = 25979
OCCURRENCE_LEDGER_ROWS = 25979
UNIQUE_OCCURRENCE_IDS = 25979
UNASSIGNED_OCCURRENCE_IDS = 0
DUPLICATE_OCCURRENCE_IDS = 0
FAMILY_LEDGER_COUNT_RECONCILIATION = PASS
KNOWN_FAMILY_DEFECTS_REMAINING = 0
CORRECTED_QUEUE_ROWS = 15
OWNER_OR_CLIENT_FACT_ROWS = 5
PROVIDER_RELEVANT_QUEUE_ROWS = 13
NEW_PROVIDER_CALLS = 0
POST_STEP04_PROVIDER_EVIDENCE_USED_IN_REWORK = 0
SEALED_SOURCE_VIOLATIONS = 0
FINAL_ROW_CLEANUP_PERFORMED = false
FINAL_SERP_CLUSTERING_PERFORMED = false
PAGE_OR_IA_DESIGN_PERFORMED = false
STEP05_ADVANCED = false
```

After Work returns, Main ChatGPT must independently remote-read the corrected outputs and accept or reject the rework. Step05 remains paused until that acceptance.