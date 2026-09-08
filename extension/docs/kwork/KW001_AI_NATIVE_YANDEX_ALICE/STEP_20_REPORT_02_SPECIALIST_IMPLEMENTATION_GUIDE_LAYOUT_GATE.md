# KW-001 — Step 20 Report №02 physical-layout gate

Updated: 2026-09-08  
Status: **ACTIVE / REPORT №02 / PERMANENT**

This gate supplements `STEP_20_REPORT_02_SPECIALIST_IMPLEMENTATION_GUIDE_GATE.md` for DOCX/PDF materialization.

## Failure O — empty navigation furniture in the recipient document

**What failed:** the generated DOCX/PDF displayed the heading `Содержание` but the table of contents itself was empty.

**Root cause:** a generic DOCX export preset inserted a TOC field that the export/render path did not populate.

**Correct control:** a compact specialist guide gets a contents block only when it contains useful visible entries. An empty TOC heading is removed rather than shipped as decorative furniture.

```text
EMPTY TOC / EMPTY CONTENTS HEADING = FAIL
```

## Failure P — field label orphaned from its content

**What failed:** short field labels such as `Пример смысловой реализации`, `Что уточнить` or `Результат уточнения` remained at the bottom of one page while the actual content started on the next page.

**Root cause:** the renderer kept formal headings with the following paragraph but did not keep semantic field-label paragraphs with their body.

**Correct control:** field labels used as mini-headings are formatted with `keep with next` or an equivalent layout control.

```text
FIELD LABEL ALONE AT PAGE BOTTOM = FAIL
FIELD LABEL + FIRST CONTENT LINE TOGETHER = REQUIRED
```

## Physical PASS gate

Report №02 physical materialization may pass only when:

```text
EMPTY TOC HEADING = 0
ORPHAN FIELD LABELS = 0
CLIPPED TEXT = 0
OVERLAPPED TEXT = 0
BROKEN GLYPHS = 0
BROKEN TABLES = 0
TABLE HEADERS REPEAT WHEN TABLE CONTINUES = true where applicable
DIRECT URLS ARE LEGIBLE = true
BOLD IMPLEMENTATION EXAMPLES ARE LEGIBLE = true
ALL FINAL PDF PAGES VISUALLY INSPECTED = true
FINAL PDF RENDER MATCHES THE COMMITTED BINARY = true
```

The physical QA must inspect the final committed PDF render, not a local predecessor or a different office/rendering environment.
