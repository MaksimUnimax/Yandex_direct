# OKNO_MSK — JOB FLOW SYNC / STEP 16 POST-RUN CORRECTED

Date: 2026-09-02  
Authority type: **latest job-specific Step-16 corrected completion overlay**  
Status: **STEP 16 CORRECTED EVIDENCE ACQUISITION COMPLETE / STEP 17 NOT STARTED**

## Current roadmap truth

| Step | Status |
|---|---|
| 0–13 | ✅ COMPLETE |
| 14 / 14A | ✅ FINAL PASS |
| 15 V2 | ✅ FINAL PASS |
| 16 original method validation | 🔁 FAILED POST-RUN AUDIT / CORRECTED |
| 16 provider evidence acquisition | ✅ COMPLETE |
| 16 corrected artifacts / claim boundaries | ✅ COMPLETE PENDING FINAL READBACK |
| 17 | ⬜ NOT STARTED |
| 18–22 | ⬜ NOT STARTED |

## What was corrected

Post-run external audit found four method-validation defects that should have been caught before paid execution:

```text
S16-M01 — reproducibility/repeat policy under-specified
S16-M02 — exact-query observations expanded into user-job claims
S16-M03 — GenSearch proxy boundary not fully enforced in result wording
S16-M04 — Step16 crossed into Step17 comparison/decision work
```

Authority:

`STEP_16_METHOD_VALIDATION_AND_CORRECT_EXECUTION_ADDENDUM_2026-09-02.md`

The paid raw provider evidence remains valid. The old Step-16 final-decision semantics are superseded.

## Corrected Step-16 meaning

```text
STEP16 = collect/persist official Yandex GenSearch observations
STEP17 = compare ordinary Search vs corrected GenSearch evidence and make final material/page decisions
```

Evidence surface actually executed:

```text
YANDEX_GENSEARCH_API_PROXY
```

Not executed:

```text
DIRECT CONSUMER ALICE
WEBMASTER ALICE VISIBILITY FOR OKNO_MSK
```

Test scope actually executed:

```text
EXACT_QUERY
```

Therefore one tested wording must not be generalized into the entire user-job family without more evidence.

## Provider execution truth

```text
SELECTED EXACT QUERIES = 8
INITIAL CALLS = 8
ADDITIONAL SAME-QUERY SHORT-WINDOW CALLS = 1 (C15-010)
RETRIES = 0
TOTAL PROVIDER CALLS = 9
TOTAL PROVIDER COST = 45.72 RUB
AUTHORITATIVE VERBATIM RAW FILES = 9
RAW READBACK = 100%
```

## Corrected observation states

```text
C15-004 = OBSERVED_DIRECTION
C15-006 = OBSERVED_DIRECTION
C15-007 = OBSERVED_DIRECTION / NO_CONTROL_ANOMALY_OBSERVED_IN_THIS_RUN
C15-010 = MATERIAL_OBSERVATION_REPRODUCED_SHORT_WINDOW
C15-013 = OBSERVED_DIRECTION
C15-018 = OBSERVATION_MIXED / NO_CONTROL_ANOMALY_CONFIRMED_IN_THIS_SINGLE_RUN
C15-019 = OBSERVATION_MIXED
C15-020 = OBSERVATION_INSUFFICIENT_FOR_TARGET_SITE_PAGE_ROLE_DECISION
```

Corrected observation authority:

`STEP_16_OBSERVATIONS_CORRECTED_V2_2026-09-02.json`

Corrected ledger:

`STEP_16_OBSERVATION_LEDGER_FINAL.tsv`

## Old labels

Historical Step-16 labels such as:

```text
DE_RISK
NO_CHANGE
CHANGE_CANDIDATE
CHANGE_CONFIRMED
```

remain visible only as historical artifacts. They are **not current final Search-vs-AI decision authority**.

Especially C15-010:

```text
SUPPORTED:
installation/how-to direction reproduced in two same-query observations in a short bounded window

NOT SUPPORTED:
long-term AI stability
consumer Alice behavior
architecture change confirmed
new page required
```

## Source-role boundary

If Step 17 materially depends on a used source being commercial/informational/DIY/service/specialist/broad, the current page must be opened/read and page-role evidence preserved before that role is used decisively.

```text
sources[] order != rank
used-source count != rank
URL/title alone = weak descriptive role evidence
```

## Corrected final artifacts

```text
STEP_16_PRE_STEP_METHOD_REVIEW_2026-09-02.md
STEP_16_RESEARCH_TO_EXECUTION_SCHEMA_2026-09-02.json
STEP_16_EXECUTION_MANIFEST_2026-09-02.json
STEP_16_CASE_EXECUTION_PLAN_2026-09-02.tsv
STEP_16_METHOD_VALIDATION_AND_CORRECT_EXECUTION_ADDENDUM_2026-09-02.md
STEP_16_OBSERVATIONS_CORRECTED_V2_2026-09-02.json
STEP_16_OBSERVATION_LEDGER_FINAL.tsv
STEP_16_QA_FINAL_2026-09-02.json
STEP_16_REPORT_2026-09-02.md
STEP_16_CURRENT_STATE.json
```

## Method status

```text
ORIGINAL PRE-STEP METHOD VALIDATION = FAILED POST-RUN AUDIT
CURRENT JOB RAW/PROVIDER EVIDENCE = VALID AND PRESERVED
CURRENT JOB STEP16 CORRECTED EVIDENCE ACQUISITION = PASS
PERMANENT STEP16 METHOD = UNVALIDATED
```

## Next legal transition

```text
STEP16 = CORRECTED EVIDENCE ACQUISITION COMPLETE
STEP17 = NOT STARTED
```

Before Step 17:

```text
-> issue a new whole-Kwork goal/full-roadmap block
-> read Step17 method/rules and Step16 correction authority
-> research/validate Step17 comparison method
-> use ordinary Search + corrected Step16 observations + current-site evidence
-> directly inspect material used sources when their page role matters
-> only then issue final Search-vs-GenSearch deltas and architecture/content-role decisions
```

No new paid GenSearch call is automatically required by this correction.