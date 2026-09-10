# MK01 / OKNO_MSK — analytical client report rebuild remote readback

Status: **TEXT/METHOD/SOURCE READBACK PASS / OWNER DOCUMENT REVIEW NEXT**

Date: **2026-09-10**

## Current client-report identity

```text
CLIENT REPORT = MK01_OKNO_MSK_CLIENT_REPORT_2026-09-10.pdf
LOCAL REVIEWED PDF SHA-256 = 9faae858b40a5e6617019f0688759d11034f27d4d800b3b46dc180461788764b
LOCAL REVIEWED PDF BYTES = 281897
LOCAL REVIEWED PDF PAGES = 8 (descriptive only, not a PASS target)
LOCAL REVIEWED DOCX SHA-256 = bcc83a4c350a0144333635d1b2fe989d70907490070ec41fcb2af32a07263057
```

New provider calls during rebuild: **0**. Semantic data changes: **0**.

## Remote authorities read back

The following current branch files were read back after correction:

- `CLIENT_REPORT_SPEC.md` — analytical-report contract; no fixed page-count gate;
- `steps/STEP_10_CLIENT_MATERIALIZATION_QA.md` — mandatory `CLIENT REPORT != EXECUTION PROTOCOL` gate + E38/E39;
- `ERRORS_AND_LESSONS.md` — E38/E39 permanent failure classes;
- `QA_AND_RELEASE.md` — executive-summary/demand-structure/major-groups/review-exclusion recipient gate;
- `PRODUCT_SCOPE.md` — commercial result = XLSX + analytical PDF + handoff; no 4–8 page rule;
- `PRODUCT_PACKAGING.md` — analytical PDF role and no page-count proxy;
- `PRODUCT_ROADMAP.md` — current analytical rebuild dated 2026-09-10; visuals remain deferred;
- `CLIENT_HANDOFF_TEMPLATE.md` — client wording describes analytical findings, not only process;
- `tests/OKNO_MSK/CLIENT_HANDOFF_PACKAGE.md` — current report points to 2026-09-10 revision;
- `tests/OKNO_MSK/CLIENT_REPORT_SOURCE_2026-09-10.md` — current recipient content source;
- `tests/OKNO_MSK/CLIENT_REPORT_ARTIFACT_MANIFEST_2026-09-10.json` — counts/shares/hashes;
- `tests/OKNO_MSK/PHASE_6_CLIENT_REPORT_REBUILD_QA_2026-09-10.md` — 25 PASS / 0 FAIL;
- `tests/OKNO_MSK/RECIPIENT_REVIEW.md` — XLSX + analytical PDF recipient review;
- `tests/OKNO_MSK/build_mk01_client_report_v2.py` — generator-side analytical preflight;
- `tests/OKNO_MSK/build_mk01_client_report.py` — legacy entrypoint redirected to v2;
- historical `CLIENT_REPORT_SOURCE_2026-09-09.md` and `PHASE_6_CLIENT_REPORT_CORRECTION_QA.md` — explicitly superseded.

## Reconciled analytical facts

```text
WORKING CORE = 2185
INTENT PHRASES = 1112 + 687 + 299 + 74 + 13 = 2185
WORKING GROUPS = 15 + 20 + 14 + 4 + 1 = 54
COMMERCIAL + SERVICE = 1799 / 82.3%
INFORMATIONAL + SELF-SERVICE = 373 / 17.1%
TOP-10 GROUPS = 1455 / 66.6% of working corpus by phrase count
REVIEW = 13 + 174 = 187
EXCLUDED = 180 + 120 + 34 + 134 = 468
OUTSIDE-TASK GROUPS = 59 + 42 + 22 + 9 + 2 = 134
```

These shares describe the governed semantic corpus, not market share, traffic or commercial priority.

## Permanent non-repeat rule

```text
E38: CLIENT PDF BECAME EXECUTION PROTOCOL INSTEAD OF ANALYTICAL REPORT
E39: PAGE COUNT WAS USED AS A PROXY FOR REPORT QUALITY

CLIENT REPORT != EXECUTION PROTOCOL
CORRECT COUNTS + CLEAN LAYOUT != ANALYTICAL REPORT PASS
```

Future Step-10 PASS requires evidence-backed executive findings, working-core structure, material semantic groups, uncertainty/exclusion analysis and practical interpretation.

## Binary persistence boundary

The active GitHub connector in this session does not accept the local PDF/DOCX as a binary file parameter. Therefore this receipt does **not** claim remote binary PDF readback. The exact reviewed binary identities are recorded by SHA-256; source, generator, manifest, method rules and QA are persisted/read back in Git. The owner receives the reviewed PDF/DOCX artifact directly.

This limitation is recorded explicitly rather than converted into a false `REMOTE_PDF_BINARY_PASS`.

## Next action

```text
OWNER REVIEW:
1. MK01_OKNO_MSK_SEMANTIC_CORE_2026-09-09.xlsx
2. MK01_OKNO_MSK_CLIENT_REPORT_2026-09-10.pdf

VISUAL/KWORK COVER WORK REMAINS DEFERRED UNTIL OWNER DOCUMENT PASS.
```
