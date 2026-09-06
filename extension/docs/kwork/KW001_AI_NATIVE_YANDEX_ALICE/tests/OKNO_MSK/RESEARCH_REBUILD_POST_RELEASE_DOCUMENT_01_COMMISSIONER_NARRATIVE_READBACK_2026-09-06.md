# OKNO-MSK — Document 01 semantic-core client-report remote readback

Date: 2026-09-06  
Status: **ANALYST_RECHECK_PASS / OWNER_REVIEW_PENDING**

Material commit: `251751852f67a3ea0ec60a03e9e8ed4ec7ddd97a`

## Artifact identity

```text
source bytes = 51252
source sha256 = 991a192928cc6cdd9f465f7033e0bc95c3f609d1bc72fa841852ea260c6a1faf
docx bytes = 52495
docx sha256 = c1372de99d517a6ac397555cfde2ed22066fdcc68c9594257a71b93c9280c3f3
pdf bytes = 200614
pdf sha256 = 78753698d7ac2284641902d1bcff9b6828f74035aaafceb372f07dfe79548dd2
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
