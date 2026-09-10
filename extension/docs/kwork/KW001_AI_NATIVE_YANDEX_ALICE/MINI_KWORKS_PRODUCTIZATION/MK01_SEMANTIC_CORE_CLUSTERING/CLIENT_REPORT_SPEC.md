# MK01 — CLIENT REPORT SPEC

Status: **MANDATORY ANALYTICAL CLIENT PDF / CORRECTED AND REVALIDATED ON OKNO_MSK**

## 1. Purpose

MK01 client delivery includes a concise analytical PDF in addition to the working XLSX. The PDF is a product standard of MK01, not a universal industry rule. Its purpose is to let a client/owner understand **what the semantic research showed**, without reading thousands of spreadsheet rows.

The PDF is not:

- a duplicate dump of the spreadsheet;
- an internal QA document;
- a chronological execution protocol;
- a decorative brochure with invented charts;
- a substitute for the working XLSX.

Canonical rule:

```text
CLIENT REPORT != EXECUTION PROTOCOL
CORRECT COUNTS + CLEAN LAYOUT != ANALYTICAL REPORT PASS
```

## 2. Client delivery set

Every completed MK01 order delivers:

1. standalone seven-sheet XLSX semantic core;
2. client analytical PDF report;
3. short handoff message in the marketplace/chat attaching both files.

A separate TXT file is not a client deliverable.

## 3. Required analytical contents

The report must be organized around recipient questions rather than internal processing chronology.

### A. Executive summary — what did we learn?

Start with evidence-backed findings that materially describe the current semantic corpus. Examples of valid finding classes when current evidence supports them:

- balance of commercial, service, informational and other user tasks;
- concentration of the working core in major semantic groups;
- meaningful informational layer;
- amount and type of unresolved demand;
- material exclusion/outside-task patterns.

Do not write generic SEO advice as a “finding”.

### B. Scope and data passport

State in plain language:

- site;
- region;
- relevant data/snapshot dates;
- Yandex Wordstat mode and device/operator context when material;
- volume of collected observations and governed unique phrases;
- use/status of targeted ordinary Yandex Search where applicable.

### C. Working-core structure

Show the semantic structure that actually follows from current accepted clustering authority. Where intent/task labels exist, provide counts and useful shares by phrase count and/or group count.

Important:

```text
CORPUS SHARE != MARKET SHARE
PHRASE COUNT != TRAFFIC FORECAST
GROUP SIZE != COMMERCIAL PRIORITY
```

### D. Material semantic groups

Show major/material groups using a declared selection rule such as phrase count, rather than choosing arbitrary examples. Include real current-job examples and explain what task each group represents.

### E. Uncertainty and exclusions

Explain:

- what remains on review/deferred and why;
- useful breakdown of review routes if present;
- what was excluded and for what reasons;
- coherent outside-task groups when these materially explain cleaning.

Uncertainty is a result, not an embarrassment to hide.

### F. How to use the XLSX

Explain which sheet to open first, what each key sheet is for and which data are working versus audit/review material.

### G. Evidence and interpretation limits

Explain Wordstat metric meaning and the Yandex-only boundary. Do not present broad/no-operator Wordstat counts as exact phrase frequency, unique users, market volume or traffic forecast.

### H. Next-step boundary

May explain what the client can logically do next, but must not silently claim that page ownership, architecture, competitor gap work, implementation TZ, Alice/Neuro analysis or Google research has already been performed.

## 4. Data truth

Every number, share, chart and example in the PDF must derive from accepted current-job authority after QA.

The report must not invent:

- example phrases;
- cluster counts;
- frequency values;
- percentages;
- traffic/ranking forecasts;
- commercial priorities;
- market-share claims;
- downstream recommendations unsupported by MK01 evidence.

All derived totals/shares used as findings must be reconciled machine-checkably where practical.

The PDF is a generated view, not a competing analytical source of truth.

## 5. Visual analytics

Charts are optional, not decorative requirements. If used, every chart must encode real accepted current-job data and answer a recipient question.

Useful examples include:

- structure of working core by intent/task;
- largest semantic groups by phrase count;
- exclusion/review breakdown.

A chart whose values cannot be reconciled to current authority = FAIL.

## 6. Language boundary

The ordinary display layer must not expose unexplained internal repository jargon such as Stage, Step IDs, authority, provenance, route state, failure class, exact-universe join, phrase key or provider request IDs.

Internal pilot history is not client content merely because it exists in the repository. For example, downstream experimental additions or internal set-difference controls stay in QA unless required to explain the purchased result.

Technical detail is translated into ordinary client language.

## 7. Wordstat boundary

When visible metrics come from broad/no-operator collection, the PDF explicitly states that they are not exact phrase frequency, unique users or a traffic forecast. Overlapping query counts are not summed and called market volume.

## 8. Length / page count

There is **no fixed page-count acceptance target**.

The report should be concise for a client/owner while fully explaining material current-job evidence. Page count is descriptive only.

Fail examples:

- padding with empty space or repeated text to reach a target length;
- compressing necessary analytical findings merely to stay under a page target;
- calling a report complete because it contains N pages.

## 9. Physical and analytical QA

Before delivery:

- render the final PDF to images;
- inspect every page;
- verify no clipping, overlap, broken glyphs, unreadable tables or blank filler pages;
- scan for internal jargon/placeholders;
- reconcile all PDF counts, shares, charts and examples with current authority;
- verify an evidence-backed executive summary exists;
- verify the report explains the working-core structure and material groups;
- verify uncertainty/exclusions are explained;
- verify the report answers “what did we learn?” and is not only a chronology of work;
- verify the PDF opens normally and is not encrypted;
- record save/commit/readback state honestly.

## 10. OKNO_MSK correction history

The first client PDF dated 2026-09-09 was physically readable and numerically correct but was rejected as analytically weak because it behaved too much like an execution protocol.

Permanent failure classes:

- **E38 — client PDF became an execution protocol instead of an analytical report.**
- **E39 — page count was used as a proxy for report quality.**

Corrected analytical report:

`tests/OKNO_MSK/MK01_OKNO_MSK_CLIENT_REPORT_2026-09-10.pdf`

Its current accepted content includes an executive summary, intent/task structure, top semantic groups, review/exclusion breakdown, Excel usage, interpretation boundaries and official Yandex methodology sources. Its exact page count is metadata, not a PASS condition.
