# KW-002 / BLOOD & SAND — STEP07 FINAL MANUAL-WORK WRAPPER FULL-VOLUME CORRECTION WORK PROMPT R2

Status: **CURRENT / EXECUTION-ONLY / LARGE-DATA FULL-VOLUME CORRECTION**

CONTINUE THE EXISTING KW-002 BLOOD & SAND GREENFIELD SEMANTIC-CORE REHEARSAL.

THIS IS NOT STEP08.
THIS IS NOT NEW BROWSER RECOVERY.
THIS IS NOT NEW COMPETITOR ACQUISITION.
THIS IS A FINAL NARROW FULL-VOLUME CORRECTION AFTER MAIN CHAT REJECTED THE PREVIOUS RETURN QA FOR A SECOND FALSE-NEGATIVE WRAPPER HARD GATE.

Repository:
`MaksimUnimax/Yandex_direct`

Branch:
`roadmap/kwork-productization-2026-08-28`

Job root:
`extension/docs/kwork/KW002_SEMANTIC_CORE_FROM_SCRATCH/work/BLOOD_SAND_GREENFIELD_2026-09-08`

======================================================================
0. ROLE BOUNDARY
======================================================================

Main Chat already completed:
- external-method audit;
- business-scope method design;
- two full-volume wrapper/noise QA passes;
- remote byte readback;
- independent full-corpus semantic scan;
- current hard-gate rejection.

Do NOT redo Main Chat research/governance.

Work executes only the current full-volume correction.

======================================================================
1. NARROW STARTUP PREFLIGHT
======================================================================

Fetch CURRENT remote branch and record WORK_START_REMOTE_HEAD.

Verify current existence/identity of:

```text
STEP07_FINAL_WRAPPER_CORRECTION_MAIN_CHAT_RETURN_QA_2026-09-18.json
COMPETITOR_GAP_CANDIDATES.csv
STEP07_CANDIDATE_PROVENANCE_LEDGER.csv
STEP07_EXECUTION_QA.md
STEP07_EXECUTION_HANDOFF_MANIFEST.json
STEP_07_OUTPUT_SCHEMA_CONTRACT.json
CLIENT_SUPPLIED_BRIEF.md
CLIENT_SUPPLIED_PRODUCT_CATALOG_OZON_76.csv
```

Expected current material Git blobs:

```text
COMPETITOR_GAP_CANDIDATES.csv
= cef347ed1e6fd0904ca3b9360ed0681f6fd4e391

STEP07_CANDIDATE_PROVENANCE_LEDGER.csv
= 8a25e332411d1f6ef113aa48b23b4bea42644f0e

STEP07_EXECUTION_QA.md
= 8ea94e7bee3d6a608741192ccd673f457b05336b

STEP07_EXECUTION_HANDOFF_MANIFEST.json
= 94346e2edf213d83fb27c6bfea483d15306b2311

STEP07_SOURCE_URL_LEDGER.csv
= cb55916fa69b6a4f10fb71bd670bce32ad25b84e

STEP07_COMPETITOR_COVERAGE_LEDGER.csv
= 86c7f5dc8d6e7f8a9be2fe784f4bb17d2719e510

STEP_07_OUTPUT_SCHEMA_CONTRACT.json
= 2af36b99af129a7bf3e59ffea889306a4889c0d4
```

The current candidate/provenance baseline above is the owner-uploaded `c01f1ca92dc463a8838baea2aa133664898508df` result and is explicitly authorized by:

`STEP07_FINAL_MANUAL_WORK_BASELINE_DRIFT_RESOLUTION_2026-09-18.json`

Do NOT compare against the stale pre-upload blobs `baa93fab...` / `3e73a36f...`; those were superseded for this correction.

Control-only commits after `c01f1ca...` do not constitute material authority drift if the listed material blobs remain exact.

If material candidate/provenance/schema/business authority changed from the R2 values above:
```text
STEP07_FINAL_MANUAL_WORK_WRAPPER_CORRECTION = BLOCKED_AUTHORITY_DRIFT
STOP
REPORT EXACT CONFLICT
```

Otherwise EXECUTE IMMEDIATELY.

======================================================================
2. WHY THIS CORRECTION EXISTS
======================================================================

Previous Work correctly transformed:

```text
S07C000567
BEFORE = Кулон кованый "Молот Тора" ручной работы
AFTER  = Кулон кованый "Молот Тора"
```

but then reported:

```text
LISTING_MANUAL_WORK_WRAPPER_HITS_AFTER = 0
```

Main Chat independently scanned ALL 794 remaining Step08-eligible candidates and found four additional current eligible product-name rows still containing the same wrapper class:

```text
S07C001277 = Славянский оберег "Велес" ручная работа, бронза
S07C001280 = Славянский оберег "Звезда Инглии" ручная работа, бронза
S07C001282 = Славянский оберег "Звезда Лады" ручная работа, бронза
S07C001291 = Славянский оберег "Лунница" малая, ручная работа, бронза
```

All four are:
- PRODUCT_NAME;
- single-source Livemaster listing evidence;
- currently NEW_CANDIDATE;
- currently ELIGIBLE_NEW_CANDIDATE;
- transformation_rule = NONE_EXACT;
- justified only by a generic retained-as-is note.

These four rows are regression examples, NOT the execution universe.

======================================================================
3. FULL-VOLUME EXECUTION UNIVERSE
======================================================================

Process ALL current Step08-eligible candidates:

```text
TARGET_CANDIDATES = 794
TARGET_LINKED_PROVENANCE = 1060
```

For every one of the 794 candidates:
- inspect candidate wording;
- inspect ALL linked provenance;
- run the complete manual-work / listing-wrapper detection contract;
- confirm or correct final wording/status/route.

Do NOT process only the four known rows.
Do NOT process only strings containing "ручная работа".
Do NOT sample.

Required:

```text
TARGET_CANDIDATES_REVIEWED = 794/794
TARGET_PROVENANCE_REVIEWED = 1060/1060
TARGET_SILENT_SKIP = 0
```

======================================================================
4. EXHAUSTIVE MANUAL-WORK WRAPPER DETECTION
======================================================================

At minimum detect the full lexical family, case-insensitively and with normal morphology:

```text
ручная работа
ручной работы
ручное изготовление
ручного изготовления
ручной труд
сделано вручную
сделан вручную
сделана вручную
изготовлено вручную
изготовлен вручную
изготовлена вручную
авторская работа
авторской работы
handmade
hand-made
хендмейд
```

Also inspect semantically equivalent seller/listing embellishments found during the full pass.

This is a semantic wrapper test, not a blind regex deletion rule.

For each hit:

1. Determine whether the manual-work phrase is merely marketplace/listing embellishment.
2. If it is wrapper/noise and a smaller literal product concept is safely present:
   - remove only the wrapper/noise;
   - preserve material semantic attributes that remain meaningful (for example a material such as bronze only if it is genuinely part of the product concept);
   - preserve raw_wording/source_context unchanged in provenance;
   - record explicit transformation_rule and transformation_detail;
   - reconcile the derived phrase against the complete 2172-candidate universe.
3. If manual-work wording is genuinely the independent semantic direction rather than listing fluff:
   - it may remain ONLY with an explicit reproducible justification in candidate notes;
   - classify the semantic role clearly;
   - do not leave generic "independently meaningful" boilerplate as the only justification.
4. If no safe compact concept exists:
   - OUT_OF_SCOPE or AMBIGUOUS.

======================================================================
5. KNOWN FOUR REGRESSION EXAMPLES
======================================================================

The following must NOT remain unchanged:

```text
S07C001277
S07C001280
S07C001282
S07C001291
```

Expected semantic reductions should remove the manual-work wrapper while preserving only justified product/material wording.

Do NOT hard-code exact replacement strings without checking:
- source wording;
- collisions with existing candidates;
- current business scope;
- existing material/variant semantics.

======================================================================
6. OTHER WRAPPER GATES REMAIN ACTIVE
======================================================================

Re-run all wrapper/noise gates across all 794:

```text
LISTING_MANUAL_WORK_WRAPPER
LISTING_AVAILABILITY_WRAPPER
LISTING_PRICE_PHOTO_WRAPPER
LISTING_DIMENSION_NOISE
LISTING_CONDITION_NOISE
LISTING_SELLER_FLUFF
COMPETITOR_BRAND_WRAPPER
OVERSPECIFIED_MARKETPLACE_TITLE
UNSUPPORTED_COMPACT_DERIVATION
EXISTING_IDENTITY_DUPLICATION
BUSINESS_SCOPE_LEAKAGE
EFFICACY_CLAIM_COPY
```

Do not weaken previously accepted business-scope rules.

======================================================================
7. NO NEW ACQUISITION
======================================================================

Forbidden:

```text
NEW BROWSER NAVIGATION = 0
NEW CRAWL = 0
NEW WORDSTAT = 0
NEW YANDEX SEARCH = 0
NEW AI SEARCH = 0
NEW GENSEARCH = 0
NEW PROVIDER CALLS = 0
STEP08 = NOT STARTED
```

======================================================================
8. OUTPUTS
======================================================================

Return only changed canonical files:

```text
COMPETITOR_GAP_CANDIDATES.csv
STEP07_CANDIDATE_PROVENANCE_LEDGER.csv
STEP07_EXECUTION_QA.md
STEP07_EXECUTION_HANDOFF_MANIFEST.json
```

Do NOT replace:
- STEP07_SOURCE_URL_LEDGER.csv
- STEP07_COMPETITOR_COVERAGE_LEDGER.csv
- browser-recovery evidence files.

Do NOT mutate JOB_FLOW/cursor.

======================================================================
9. REQUIRED HARD QA
======================================================================

Required:

```text
TARGET_CANDIDATES_REVIEWED = 794/794
TARGET_PROVENANCE_REVIEWED = 1060/1060
TARGET_SILENT_SKIP = 0

KNOWN_MANUAL_WORK_REGRESSION_ROWS = 4/4 CORRECTED
GENERIC_MANUAL_WORK_WRAPPER_HITS_AFTER = 0
UNJUSTIFIED_MANUAL_WORK_RETAINED = 0

LISTING_AVAILABILITY_WRAPPER_HITS_AFTER = 0
LISTING_PRICE_PHOTO_WRAPPER_HITS_AFTER = 0
LISTING_DIMENSION_NOISE_HITS_AFTER = 0
LISTING_CONDITION_NOISE_HITS_AFTER = 0
COMPETITOR_BRAND_WRAPPER_HITS_AFTER = 0
BUSINESS_SCOPE_LEAKAGE = 0
UNSUPPORTED_DERIVATIONS = 0
EXISTING_IDENTITY_DUPLICATION = 0

RAW_WORDING_IMMUTABLE = true
SOURCE_CONTEXT_IMMUTABLE = true

SCHEMA_COMPLIANCE = PASS
PRIMARY_KEYS_UNIQUE = PASS
FOREIGN_KEYS_RESOLVE = PASS
CANDIDATE_SOURCE_COUNTS_RECONCILE = PASS
STEP08_ROUTE_CONSISTENCY = PASS
DEMAND_VALIDATION_STATE = NOT_VALIDATED_STEP07 FOR ALL

HARD_GATE_FAILURES = 0
OPEN_CRITICAL_DEFECTS = 0
```

If a manual-work phrase remains eligible by deliberate semantic decision, report it explicitly in a dedicated table:

```text
candidate_id
wording
why_manual_work_is_semantic_not_wrapper
source/provenance basis
business-scope basis
```

Then `GENERIC_MANUAL_WORK_WRAPPER_HITS_AFTER = 0` means zero unjustified hits, not zero literal token occurrences.

======================================================================
10. FINAL REPORT
======================================================================

Return:

```text
WORK_START_REMOTE_HEAD
WORK_PRE_PUBLICATION_REMOTE_HEAD
AUTHORITY_DRIFT_STATUS
STEP07_FINAL_MANUAL_WORK_WRAPPER_STATUS

TARGET_CANDIDATES_REVIEWED
TARGET_PROVENANCE_REVIEWED
OLD_STEP08_ELIGIBLE = 794
NEW_STEP08_ELIGIBLE = <exact>

OLD_TO_NEW_TRANSITION_MATRIX
TRANSFORMED_DERIVED_COUNT
OUT_OF_SCOPE_DELTA
AMBIGUOUS_DELTA
ALREADY_PRESENT_DELTA
NORMALIZED_DUPLICATE_DELTA

KNOWN_MANUAL_WORK_REGRESSION_ROWS_CORRECTED
GENERIC_MANUAL_WORK_WRAPPER_HITS_AFTER
DELIBERATELY_RETAINED_MANUAL_WORK_SEMANTIC_ROWS

HARD_GATE_FAILURES
OPEN_CRITICAL_DEFECTS
QUALITY_TOTAL
QUALITY_SCORE

NEW_BROWSER_CALLS = 0
NEW_PROVIDER_CALLS = 0
STEP08_STARTED = false
WORK_GITHUB_COMMIT_PUSH_PR = false
MAIN_CHAT_ACCEPTANCE = PENDING
```

======================================================================
11. HANDOFF
======================================================================

Work MUST NOT commit/push/PR.

Use one upload target:

```text
repository = MaksimUnimax/Yandex_direct
branch = roadmap/kwork-productization-2026-08-28
directory = extension/docs/kwork/KW002_SEMANTIC_CORE_FROM_SCRATCH/work/BLOOD_SAND_GREENFIELD_2026-09-08
```

Provide:
- direct links for changed files;
- one ZIP with exactly changed files;
- manifest/hashes;
- one upload link;
- owner instruction: upload all together, commit, reply "готово".

Do not stop at the four known rows.
Process all 794 candidates and all 1060 linked provenance rows.


======================================================================
12. R2 BASELINE AUTHORITY AMENDMENT — 2026-09-18
======================================================================

The prior Work attempt correctly stopped because the earlier prompt contained stale expected candidate/provenance blobs.

Main Chat has classified that event as:

```text
STALE_PROMPT_BASELINE_NOT_MATERIAL_DATA_DRIFT
ROLLBACK_REQUIRED = false
CURRENT_C01F_OWNER_UPLOAD_BYTES = AUTHORIZED_CORRECTION_BASELINE
```

Current authorized material baseline:

```text
COMPETITOR_GAP_CANDIDATES.csv
= cef347ed1e6fd0904ca3b9360ed0681f6fd4e391

STEP07_CANDIDATE_PROVENANCE_LEDGER.csv
= 8a25e332411d1f6ef113aa48b23b4bea42644f0e

STEP07_EXECUTION_QA.md
= 8ea94e7bee3d6a608741192ccd673f457b05336b

STEP07_EXECUTION_HANDOFF_MANIFEST.json
= 94346e2edf213d83fb27c6bfea483d15306b2311
```

Execute the same full 794-candidate / 1060-provenance correction against this baseline.

Do not restore older candidate/provenance files.
Do not treat control-record commits as material drift.
