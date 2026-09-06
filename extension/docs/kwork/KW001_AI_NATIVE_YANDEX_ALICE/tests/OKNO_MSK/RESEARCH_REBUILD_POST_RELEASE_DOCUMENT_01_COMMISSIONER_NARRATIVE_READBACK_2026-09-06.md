# OKNO-MSK — Document 01 semantic-core client-report remote readback

Date: 2026-09-06  
Status: **ANALYST_RECHECK_PASS / OWNER_REVIEW_PENDING**

Material commit: `7ad4fd1d6a6cb716cb737aa2689c7a1cd30aead2`

## Artifact identity

```text
source bytes = 51321
source sha256 = 232030778a3c7378d35dc10397f48f0262d4facd043ecc111c51d711ac49caff
docx bytes = 52500
docx sha256 = 1ea24043099ec8c4955baf88d35942d379c355c01d728cf2a5a87357bb67c57c
pdf bytes = 200538
pdf sha256 = 4591598241e6528b542c3e274862f3c64f90a1becac151d592923df080130045
pdf pages = 10
```

## Corrected research framing

```text
primary object = semantic/search core + search demand + query-to-page distribution
user intent = grouping criterion only, not the research object
Wordstat first pass = 2415 rows
targeted expansion = 550 rows
source rows before cleanup = 2965
unique formulations after deduplication = 2840
2840 != 2840 exact-frequency measurements
active formulations = 2332
assigned = 2313
unresolved = 19
demand groups = 168
ordinary Yandex targeted observations = 75
Alice candidate themes = 25
Alice complete checks = 8 = 6 decision-sensitive + 2 controls
repeated candidate types not selected = 16
held candidate theme = 1
material results = 34
ready recommendations with explicit why = 7
company fact requests = 2
```

## Recipient-language / value gate

All nine owner-review defect classes are hard-failed by the current Report-01 QA: no uncertainty-selling, no internal family/status jargon, every ready recommendation includes why it matters, no client-facing partially-ready pseudo-result, no “changes forbidden” output, no “disputed families”, no internal GenSearch/proxy jargon, no invented opposite goal, and no negative pseudo-actions in the priority plan. Native brand/query spellings are preserved.

Document 02 and Document 03 were not advanced. No new provider calls were made.

```text
CURRENT_DOCUMENT = 01
DOCUMENT_01_ANALYST_RECHECK = PASS
DOCUMENT_01_OWNER_REVIEW = PENDING__AWAITING_OWNER_RECHECK
DOCUMENT_02_OWNER_REVIEW = PENDING
DOCUMENT_03_OWNER_REVIEW = PENDING
FINAL_OWNER_RECIPIENT_ACCEPTANCE = OPEN
NEXT_ACTION = OWNER_REVIEW_CORRECTED_DOCUMENT_01
```
