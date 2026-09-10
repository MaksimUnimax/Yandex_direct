# MK01 / OKNO_MSK — client report analytical rebuild QA

Status: **PASS AFTER ANALYTICAL REPORT REBUILD / OWNER REVIEW NEXT**

Date: **2026-09-10**

## Why the previous PDF was rejected

The previous PDF was numerically correct and physically readable, but it was too close to an execution protocol: it emphasized what was done and how many rows existed, while under-explaining what the semantic research actually showed about demand structure. That is not sufficient recipient value for a client/owner report.

This rebuild closes that failure class at the report-method level rather than only rewriting one document.

## Rebuilt artifact

`MK01_OKNO_MSK_CLIENT_REPORT_2026-09-10.pdf`

- pages: **8** — descriptive metadata, not a PASS target;
- A4: PASS;
- encrypted: NO;
- PDF SHA-256: `9faae858b40a5e6617019f0688759d11034f27d4d800b3b46dc180461788764b`;
- DOCX SHA-256: `bcc83a4c350a0144333635d1b2fe989d70907490070ec41fcb2af32a07263057`;
- new provider calls: **0**;
- semantic dataset changes: **0**.

## Analytical additions

The rebuilt report now contains:

1. executive summary with evidence-backed findings;
2. data/snapshot passport;
3. working-core intent structure by both phrase count and group count;
4. top-10 semantic groups and their contribution to the working corpus;
5. explicit review breakdown: `13 + 174 = 187`;
6. explicit exclusion breakdown: `180 + 120 + 34 + 134 = 468`;
7. all five outside-task groups and their counts;
8. practical Excel-reading workflow;
9. conclusions for further work without silently performing downstream products;
10. official Yandex methodology sources.

## Reconciliation

```text
INTENT PHRASES
1112 + 687 + 299 + 74 + 13 = 2185 PASS

INTENT GROUPS
15 + 20 + 14 + 4 + 1 = 54 PASS

TOP-10 GROUPS
282 + 239 + 179 + 128 + 128 + 114 + 107 + 106 + 100 + 72 = 1455
1455 / 2185 = 66.6% PASS

REVIEW
13 + 174 = 187 PASS

EXCLUDED
180 + 120 + 34 + 134 = 468 PASS

OUTSIDE-TASK GROUPS
59 + 42 + 22 + 9 + 2 = 134 PASS
```

## QA ledger

| ID | Check | Result |
|---|---|---|
| A01 | Executive summary answers “what did we learn?” | PASS |
| A02 | Findings are evidence-backed rather than generic SEO advice | PASS |
| A03 | Intent phrase counts reconcile to working core | PASS |
| A04 | Intent group counts reconcile to 54 working groups | PASS |
| A05 | Commercial + service = 1799 / 82.3% | PASS |
| A06 | Informational + self-service = 373 / 17.1% | PASS |
| A07 | Top-10 group sum = 1455 / 66.6% | PASS |
| A08 | Top groups use current cluster authority | PASS |
| A09 | Review split 13/174 reconciles to 187 | PASS |
| A10 | Exclusion split reconciles to 468 | PASS |
| A11 | Five outside-task groups reconcile to 134 | PASS |
| A12 | Broad Wordstat values are not called exact phrase frequency | PASS |
| A13 | Group/intent shares are not called market share or traffic | PASS |
| A14 | No client-visible Step5A/16-phrase internal history | PASS |
| A15 | No internal Stage/Step/authority/provenance jargon | PASS |
| A16 | No `scope`, `DIY`, `provider`, `gap`, `phrase key` leakage | PASS |
| A17 | No query→URL / architecture / implementation claim leakage | PASS |
| A18 | Google explicitly outside scope | PASS |
| A19 | All 8 pages rendered and visually inspected | PASS |
| A20 | No blank pages / clipping / overlap / broken glyphs | PASS |
| A21 | Page count is descriptive, not an acceptance proxy | PASS |
| A22 | XLSX remains the primary working artifact | PASS |
| A23 | PDF is an analytical summary, not a duplicate row dump | PASS |
| A24 | Official Yandex sources are named and linked | PASS |
| A25 | Owner review is still required after technical QA | PASS |

Final: **25 PASS / 0 FAIL**.

## Failure classes added

### E38 — client PDF became an execution protocol instead of an analytical report

**Root cause:** correctness/layout QA was treated as sufficient recipient value. The report answered “what was done?” but not adequately “what did the research show?”.

**Permanent control:** every MK01 client report must contain an evidence-backed executive summary, structure of the working core, material semantic groups, uncertainty/exclusion analysis, practical interpretation and next-step boundaries. A numerically correct chronology is not enough.

### E39 — page count was used as a proxy for report quality

**Root cause:** the previous report specification used a fixed page-range target as though page count could prove report completeness.

**Permanent control:** no fixed page count is a PASS gate. Length is determined by the current evidence and recipient task. QA checks information value, reconciliation, readability and absence of repetition/empty filler.

## Persistence boundary

Text source, report specification, Step-10 rules, error ledger, QA and artifact manifest are persisted in Git. PDF/DOCX SHA-256 values identify the reviewed binary artifacts exactly. Do not claim remote binary readback unless the active Git persistence channel actually verifies those binaries.
