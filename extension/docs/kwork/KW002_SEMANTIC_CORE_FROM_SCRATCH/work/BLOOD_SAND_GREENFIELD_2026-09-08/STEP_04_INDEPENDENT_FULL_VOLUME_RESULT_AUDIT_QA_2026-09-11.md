# KW-002 Step04 independent full-volume result audit — local QA

Date: 2026-09-11

```text
LIVE_BASE_HEAD = 8a09e1610d68f61769b6a4d44d1382cab4dd37b7
LOCAL_ARTIFACT_COMPLETE = true
LOCAL_QA_PASS = true
PUBLICATION_HANDOFF_READY = true
PUBLICATION_ROUTE = OWNER_RELAY_REQUIRED
AUDIT_RESULT_UNDER_REVIEW = REWORK_REQUIRED
NORMALIZED_IDENTITIES = 24576
ACTIVE_PLUS_HOLD_IDENTITIES = 18135
EXCLUDED_IDENTITIES_HISTORY = 6441
RAW_OCCURRENCES = 25979
UNIQUE_RAW_OCCURRENCE_IDS = 25979
RAW_LINEAGE_LOSS = 0
STEP03B_STATE_OR_REASON_MISMATCHES = 0
FAMILIES = 26 / 24 OBSERVED / 2 GAPS
BOUNDARY_MATRIX_ROWS = 676 / SYMMETRIC
QUEUE_ROWS_AUDITED = 13
FEEDBACK_ROWS_AUDITED = 10
MATERIAL_DEFECT_IDENTITIES = 255
PROVIDER_CALLS = 0
STEP04_CORRECTIONS = 0
STEP05_ADVANCEMENT = false
STEP06_ADVANCEMENT = false
```

All accepted Step03B and Step04 input hashes match their frozen authorities. Every active/HOLD identity has exactly one observed family; every excluded identity remains history. Overlay dispositions total 24,576: 24,321 pass-as-preliminary, 207 rule-order defects and 48 family-too-broad findings.

The independent diagnostic processed all 18,135 active/HOLD texts with TF-IDF term/co-occurrence features, 32 deterministic topics and family-centroid comparisons. It is auxiliary evidence, not a final SERP or page-cluster model.

All 20 anti-regression controls pass as audit controls. This means the audit execution is complete and reproducible; it does not mean the audited Step04 result passes. The audited result verdict remains exactly:

```text
STEP04_RESULT_AUDIT = REWORK_REQUIRED
```
