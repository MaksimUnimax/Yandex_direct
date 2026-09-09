# MK01 STEP 10 — CLIENT MATERIALIZATION / QA

## PURPOSE
Turn current MK01 semantic authority into a complete recipient-ready client package and prove that both working data and explanatory report are usable.

## WHY THIS STEP EXISTS
KW-001 and the MK01 rehearsal showed two distinct failure modes: canonical data/counts can be correct while the workbook is not recipient-ready, and a usable workbook can still be insufficient as a compact explanation for an owner/non-analyst client. Therefore completion requires both a working XLSX and a concise PDF report.

## INPUTS
Accepted current semantic universe, cluster authority, demand/provenance data, unresolved states and delivery contract.

## REQUIRED EVIDENCE
Current-authority manifest; source dataset identities/counts; client language/region; Wordstat metric semantics; generated XLSX and PDF outputs; client-report specification.

## METHOD
Freeze the physical delivery contract before generation. Generate from current authority, never patch a stale workbook or report as truth. Reconcile technical assignment with cluster business fit before building the active-core view: confirmed outside-task clusters remain in the full/audit views, not the working core. Reconcile all saved Search decisions as exact-universe joins vs control/anchor queries outside the universe.

Generate the seven-sheet XLSX required by `DELIVERABLE_SPEC.md`. Then generate a 4–8 page client PDF governed by `CLIENT_REPORT_SPEC.md` using the same accepted counts and only real current-job group examples. The PDF must explain scope, work performed, headline results, examples of groups, uncertainty/exclusions, how to use the XLSX, Wordstat limitations, Yandex-only boundary and next-step options without inventing downstream decisions.

Translate internal technical vocabulary into normal Russian client language. Set workbook geometry against the whole sheet; render/inspect every workbook sheet and every PDF page. The short marketplace/chat handoff attaches both files and is not a separate TXT report.

## OUTPUTS
1. Standalone seven-sheet MK01 XLSX.
2. Concise 4–8 page client PDF report.
3. Short handoff message attaching both.
4. QA/readback record.

## SOURCE KW-001 AUTHORITY
`STEP_19_CLIENT_DELIVERABLE_PACKAGING_METHOD.md`; `STEP_20_STANDALONE_SEMANTIC_CORE_GATE.md`; post-release recipient-acceptance lessons; MK01 `CLIENT_REPORT_SPEC.md` validated on OKNO_MSK.

## KNOWN FAILURE CLASSES
E22 no standalone workbook; E23 stale workbook reused; E24 unnecessary recollection; E25 broad count mislabeled exact; E26 overlapping sums called market volume; E27 English/API leakage; E28 sheet names missed by language QA; E29 automated QA treated as acceptance; E30 bad representative phrase; E31 outside-task assignment leaked into active core; E32 Search-control decision misreported as an exact-universe join; E33 later block overwrote worksheet column width; E36 usable XLSX mistaken for complete client communication; E37 internal QA jargon leaked into client PDF.

## ROOT CAUSES
Repository completeness was confused with client completeness; a working data artifact was confused with a complete recipient explanation; internal traceability/presentation convenience replaced recipient semantics.

## NON-REPEAT CONTROLS
Current authority manifest; audit preserved evidence before new provider calls; active-core business-fit projection; separate Search totals for all decisions / exact-universe joins / outside-universe controls; deterministic Russian display mapping; working-first group ordering; one geometry definition per worksheet column; workbook-wide language scan including sheet titles; PDF internal-jargon/placeholder scan; render every XLSX sheet and every PDF page; reconcile PDF counts/examples with current authority; data/semantic/workbook/PDF/visual/recipient QA separated; final remote readback.

## CLAIM BOUNDARIES
The client package reports Yandex semantic demand/clustering only. It does not imply Google support, page architecture, implementation TZ, ranking guarantees or exhaustive competitor/AI research.

## UNKNOWN / BLOCKER BEHAVIOR
Unresolved semantic rows remain visible in an appropriate review view. Missing metric metadata blocks stronger frequency labels; stale authority or mismatch between XLSX/PDF counts blocks release.

## PASS GATE
Source counts/joins reconcile; active core contains no confirmed outside-task members; Search decisions reconcile to exact-universe joins plus controls; semantic QA PASS; XLSX opens and is usable; PDF is 4–8 pages and every page is visually inspected; PDF counts/examples match current authority; Russian display layer PASS in both files; metric labels accurate; uncertainty visible; no stale authority; recipient task walkthrough PASS; both client files are persisted/read back remotely.

## CLIENT-FACING MEANING
«Вы получаете два нормальных итоговых документа: рабочий Excel с ядром и группами и короткий PDF-отчёт, где простым языком объяснено, что исследовано, что получилось, как читать файл и какие ограничения есть у результата.»
