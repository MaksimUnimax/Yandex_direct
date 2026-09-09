# MK01 — CLIENT REPORT SPEC

Status: **MANDATORY CLIENT PDF REPORT / VALIDATED ON OKNO_MSK**

## 1. Purpose

MK01 client delivery includes a concise PDF report in addition to the working XLSX. The PDF is not a duplicate dump of the spreadsheet and not an internal QA document. Its purpose is to let a client/owner understand the result without reading thousands of rows.

## 2. Client delivery set

Every completed MK01 order delivers:

1. standalone seven-sheet XLSX semantic core;
2. client PDF report;
3. short handoff message in the marketplace/chat attaching both files.

A separate TXT file is not a client deliverable.

## 3. Required PDF contents

The PDF must normally be 4–8 pages and explain in plain Russian:

- site, region and research scope;
- what was done and why;
- headline counts: collected/preserved, working core, review, excluded, groups;
- selected real examples of semantic groups from the current order;
- what remains uncertain or excluded and why;
- how to use the XLSX and which sheet to open first;
- how to interpret visible Wordstat metrics;
- explicit Yandex-only boundary;
- what is outside MK01;
- practical next-step options without silently performing/selling them as already completed;
- methodology sources where useful.

## 4. Data truth

Every number and example in the PDF must come from the accepted current-job authority after QA. The report must not invent example phrases, cluster counts, frequency values, result percentages, traffic forecasts or ranking claims.

The PDF is a generated view, not a competing analytical source of truth.

## 5. Language boundary

The ordinary display layer must not expose internal repository jargon such as Stage, Step IDs, authority, provenance, route state, failure class, exact-universe join, phrase key or provider request IDs.

Technical detail is translated into ordinary client language.

## 6. Wordstat boundary

If the visible metric comes from broad/no-operator collection, the PDF must explicitly say that it is not exact phrase frequency, unique users or a traffic forecast.

## 7. Physical QA

Before delivery:

- render the final PDF to images;
- inspect every page;
- verify no clipping, overlap, broken glyphs or unreadable tables;
- scan for internal jargon/placeholders;
- reconcile all PDF counts with the final manifest/XLSX authority;
- verify the PDF opens normally and is not encrypted;
- save -> commit -> remote readback.

## 8. OKNO_MSK validation

Validated report:

`tests/OKNO_MSK/MK01_OKNO_MSK_CLIENT_REPORT_2026-09-09.pdf`

Validated length: 6 pages.

The report uses the accepted partition `2840 / 2185 / 187 / 468`, 59 groups, and only real group examples from the current cluster authority.
