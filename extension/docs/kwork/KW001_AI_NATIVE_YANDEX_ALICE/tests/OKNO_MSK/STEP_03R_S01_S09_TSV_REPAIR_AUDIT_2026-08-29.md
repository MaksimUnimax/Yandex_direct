# KW-001 / OKNO-MSK — STEP 03R S01-S09 TSV REPAIR AUDIT

Date: 2026-08-29
Job: `kw001-okno-msk-wordstat-pass1-repair-20260829`
Status: **REPAIR COMPLETE FOR S01-S09 / HISTORY-PRESERVING CORRECTION**

## Why this correction exists

The frozen Step-03R manifest required two reusable preservation layers after every provider item:

1. complete raw provider result;
2. normalized TSV containing every returned `results[] + associations[]` row.

S01-S09 raw JSON files were preserved and read back before later provider items, but their item checkpoints were marked `CURRENT_ITEM = COMPLETE` before the required Step-03R normalized TSV files existed.

Therefore those historical completion verdicts were premature under the frozen manifest. This audit does not rewrite that history. It records the defect and the completed local repair before S10 is allowed.

## Repair method

No provider request was executed during this repair.

For each S01-S09 item:

```text
open preserved raw provider JSON
→ preserve seed/request/region/device/numPhrases/totalCount metadata
→ convert every returned results[] row to TSV section=result
→ convert every returned associations[] row to TSV section=association
→ preserve sparse-field absence for S08
→ write TSV
→ reopen TSV beginning and verify request/seed metadata
→ reopen calculated final line and verify exact file boundary
→ reconcile normalized data-row count against raw provider row count
```

The raw JSON remains the authoritative provider-level evidence. The TSV is the complete normalized analysis copy required by the frozen manifest.

## Quantitative reconciliation

| Seed | Results rows | Association rows | Raw rows | TSV rows | Verified |
|---|---:|---:|---:|---:|---|
| S01 `пластиковые окна` | 200 | 18 | 218 | 218 | PASS |
| S02 `окна rehau` | 200 | 20 | 220 | 220 | PASS |
| S03 `французские окна` | 129 | 15 | 144 | 144 | PASS |
| S04 `окна п 44` | 12 | 17 | 29 | 29 | PASS |
| S05 `пластиковые двери` | 200 | 15 | 215 | 215 | PASS |
| S06 `остекление балконов` | 200 | 18 | 218 | 218 | PASS |
| S07 `остекление балкона с крышей` | 6 | 13 | 19 | 19 | PASS |
| S08 `остекление балкона п 46` | 0 | 0 | 0 | 0 | PASS — sparse response; fields absent, `totalCount=19` preserved |
| S09 `пластиковые окна митино` | 3 | 10 | 13 | 13 | PASS |
| **TOTAL** | **950** | **126** | **1076** | **1076** | **PASS** |

`totalCount` is frequency evidence and is not included in returned-row counts.

## Created normalized artifacts

```text
STEP_03R_S01_RAW_NORMALIZED.tsv
STEP_03R_S02_RAW_NORMALIZED.tsv
STEP_03R_S03_RAW_NORMALIZED.tsv
STEP_03R_S04_RAW_NORMALIZED.tsv
STEP_03R_S05_RAW_NORMALIZED.tsv
STEP_03R_S06_RAW_NORMALIZED.tsv
STEP_03R_S07_RAW_NORMALIZED.tsv
STEP_03R_S08_RAW_NORMALIZED.tsv
STEP_03R_S09_RAW_NORMALIZED.tsv
```

## Read-back verification

For every non-sparse TSV:

```text
metadata block readable = PASS
seed id = expected S01-S09 = PASS
request_id = matching raw provider result = PASS
region = 213 = PASS
device = DEVICE_ALL = PASS
numPhrases = 200 = PASS
totalCount = matching raw provider result = PASS
TSV header readable = PASS
last expected data line exists = PASS
no data line exists beyond expected row boundary = PASS
TSV data rows = raw results rows + raw association rows = PASS
```

For S08:

```text
results[] field absent in raw = preserved
associations[] field absent in raw = preserved
normalized rows expected = 0
normalized rows saved = 0
TSV readable = PASS
```

## Historical checkpoint correction

The `CURRENT_ITEM = COMPLETE` / `NEXT_PROVIDER_ITEM = ALLOWED` verdicts in the original S01-S09 checkpoints were temporally premature because the required normalized TSV layer did not yet exist.

Current authoritative interpretation:

```text
AT ORIGINAL CHECKPOINT TIME:
S01-S09 manifest completeness = INCOMPLETE because TSV requirement was unmet

AFTER THIS REPAIR AUDIT:
S01-S09 raw provider results preserved = 9/9
S01-S09 normalized TSV artifacts present = 9/9
S01-S09 normalized row counts reconciled = 1076/1076
S01-S09 readable/usable preservation = 9/9
S01-S09 current manifest completeness = COMPLETE
```

## YMB / cost accounting

```text
provider calls during repair = 0
additional provider cost during repair = 0 RUB
existing Step03R provider calls = 9
known provider outcomes = 9
outcome_unknown = 0
failed_terminal = 0
existing estimated provider cost = 0.18 RUB
```

## Non-repeat control

The prior Step-3 failure was accepting technical/provider success without complete reusable preservation. A second local process defect was discovered before S10: the frozen manifest also required normalized TSV, but S01-S09 had only raw JSON at checkpoint time.

The control now enforced for every remaining item S10-S18 is:

```text
ONE PROVIDER ITEM
→ SAVE COMPLETE RAW RESULT
→ COUNT results[] + associations[]
→ CREATE COMPLETE NORMALIZED TSV
→ REOPEN RAW + TSV
→ RECONCILE RETURNED = SAVED = VERIFIED
→ ONLY THEN MARK CURRENT ITEM COMPLETE
→ ONLY THEN ALLOW NEXT batch.next
```

```text
NON_REPEAT_CONTROLS = PASS
S01_S09_REPAIR = COMPLETE
STEP_03R_COMPLETED_ITEMS = 9/18
STEP_03R_REMAINING_ITEMS = 9/18
NEXT_PROVIDER_ITEM = ALLOWED
FORWARD_ANALYTICAL_STEP = BLOCKED UNTIL 18/18
```
