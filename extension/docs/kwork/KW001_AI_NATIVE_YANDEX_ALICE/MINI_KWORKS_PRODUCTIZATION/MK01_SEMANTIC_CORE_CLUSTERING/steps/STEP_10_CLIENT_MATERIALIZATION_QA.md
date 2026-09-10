# MK01 STEP 10 — CLIENT MATERIALIZATION / QA

## PURPOSE
Turn current MK01 semantic authority into a complete recipient-ready client package and prove that both the working data and the explanatory report are useful to the client.

## WHY THIS STEP EXISTS
KW-001 and the MK01 rehearsals exposed several distinct recipient failures. Canonical data/counts can be correct while the workbook is not recipient-ready. A usable workbook can still be insufficient as a compact explanation for an owner/non-analyst. And a numerically correct, visually clean PDF can still fail if it behaves like an execution protocol — describing what the analyst did without explaining what the research actually showed about demand.

Therefore completion requires both a working XLSX and an evidence-backed analytical client report.

## INPUTS
Accepted current semantic universe, cluster authority, demand/provenance data, unresolved states, current-job business/scope record and delivery contract.

## REQUIRED EVIDENCE
Current-authority manifest; source dataset identities/counts; client language/region; Wordstat metric semantics; final cluster summary/taxonomy; review/exclusion breakdowns; generated XLSX and PDF outputs; client-report specification.

## METHOD
Freeze the physical delivery contract before generation. Generate from current authority; never patch a stale workbook or stale report as truth. Reconcile technical assignment with cluster business fit before building the active-core view: confirmed outside-task clusters remain in full/audit views, not the working core. Reconcile all saved Search decisions as exact-universe joins versus control/anchor queries outside the universe.

Generate the seven-sheet XLSX required by `DELIVERABLE_SPEC.md`.

Then generate the client PDF governed by `CLIENT_REPORT_SPEC.md` from the same accepted authority.

### Mandatory anti-repeat rule: CLIENT REPORT != EXECUTION PROTOCOL

The report must answer **«Что исследование показало?» before «Что мы сделали?»**.

A chronology of collection/cleaning/clustering, correct row counts, a valid PDF and clean visual layout are necessary but **not sufficient** for report PASS.

Before release, the report must derive and explain, when supported by the current evidence:

1. an executive summary with material findings, not only process statistics;
2. the structure of the working core by user task / intent or another evidence-backed segmentation defined by the current clustering authority;
3. the largest or otherwise material semantic groups, with the selection rule stated and real current-job examples;
4. what remains uncertain/reviewed and why, including useful breakdowns when available;
5. what was excluded and why, including coherent outside-task groups when they materially explain the cleanup;
6. how the client should interpret these findings without converting phrase counts into market share, traffic or commercial priority;
7. how to use the XLSX and where to find the underlying working data;
8. the Yandex/Wordstat evidence boundary and important snapshot/mode limitations;
9. what logically comes next, without silently performing or claiming downstream products.

Do not include internal pilot history merely because it exists in the repository. Internal controls such as later competitor additions, exact set-difference checks or QA-only row-history belong in internal QA unless the client needs them to understand the purchased result.

### No page-count proxy

There is **no fixed page-count PASS criterion**. The report should be concise enough for a client/owner but long enough to explain the material current-job evidence. Page count is descriptive only. Empty filler, repetition or artificial compression to meet a page target is a failure.

Translate internal technical vocabulary into normal Russian client language. Use visualizations only when they encode real current-job data and materially improve comprehension; never create decorative or invented analytical charts. Set workbook geometry against the whole sheet; render/inspect every workbook sheet and every PDF page. The short marketplace/chat handoff attaches both files and is not a separate TXT report.

## OUTPUTS
1. Standalone seven-sheet MK01 XLSX.
2. Concise evidence-backed analytical client PDF report; length determined by current evidence and recipient task, not a fixed page target.
3. Short handoff message attaching both.
4. QA/readback record.

## SOURCE KW-001 AUTHORITY
`STEP_19_CLIENT_DELIVERABLE_PACKAGING_METHOD.md`; `STEP_20_STANDALONE_SEMANTIC_CORE_GATE.md`; post-release recipient-acceptance lessons; MK01 `CLIENT_REPORT_SPEC.md`; OKNO_MSK analytical-report rebuild dated 2026-09-10.

## KNOWN FAILURE CLASSES
E22 no standalone workbook; E23 stale workbook reused; E24 unnecessary recollection; E25 broad count mislabeled exact; E26 overlapping sums called market volume; E27 English/API leakage; E28 sheet names missed by language QA; E29 automated QA treated as acceptance; E30 bad representative phrase; E31 outside-task assignment leaked into active core; E32 Search-control decision misreported as an exact-universe join; E33 later block overwrote worksheet column width; E36 usable XLSX mistaken for complete client communication; E37 internal QA jargon leaked into client PDF; **E38 client PDF became an execution protocol instead of an analytical report; E39 page count was used as a proxy for report quality.**

## ROOT CAUSES
Repository completeness was confused with client completeness; a working data artifact was confused with complete recipient communication; technical correctness/layout correctness were confused with analytical usefulness; internal traceability/presentation convenience replaced recipient meaning; a formatting target was treated as a quality metric.

## NON-REPEAT CONTROLS
Current authority manifest; audit preserved evidence before new provider calls; active-core business-fit projection; separate Search totals for all decisions / exact-universe joins / outside-universe controls; deterministic Russian display mapping; working-first group ordering; one geometry definition per worksheet column; workbook-wide language scan including sheet titles; PDF internal-jargon/placeholder scan; evidence-backed executive-summary gate; intent/task-structure reconciliation; material-group selection rule; review/exclusion breakdown reconciliation; explicit `CLIENT REPORT != EXECUTION PROTOCOL` review; no fixed page-count acceptance; render every XLSX sheet and every PDF page; reconcile PDF counts/examples/findings with current authority; data/semantic/workbook/PDF/visual/recipient QA separated; final remote readback.

## CLAIM BOUNDARIES
The client package reports Yandex semantic demand/clustering only. Phrase/group shares describe the composition of the governed semantic corpus and do not automatically mean market share, traffic, revenue or business priority. The report does not imply Google support, page architecture, implementation TZ, ranking guarantees or exhaustive competitor/AI research.

## UNKNOWN / BLOCKER BEHAVIOR
Unresolved semantic rows remain visible in an appropriate review view. Missing metric metadata blocks stronger frequency labels. Missing evidence for an analytical finding means the finding is omitted or stated as unknown — never invented. Stale authority or mismatch between XLSX/PDF counts, examples or derived findings blocks release.

## PASS GATE
Source counts/joins reconcile; active core contains no confirmed outside-task members; Search decisions reconcile to exact-universe joins plus controls; semantic QA PASS; XLSX opens and is usable; PDF counts/examples/derived findings match current authority; PDF has an evidence-backed executive summary; the report explains material demand/task structure and major groups; review/exclusion logic is understandable; report answers «what did we learn?» rather than only listing work performed; page count is not used as a quality proxy; Russian display layer PASS in both files; metric labels accurate; uncertainty visible; no stale authority; every final PDF page is visually inspected; recipient task walkthrough PASS; final package persistence/readback is recorded honestly.

## CLIENT-FACING MEANING
«Вы получаете рабочий Excel с ядром и группами и отдельный аналитический PDF-отчёт. В отчёте не просто перечислены этапы работы: простым языком показано, что удалось узнать о структуре спроса, какие группы наиболее крупные, что осталось спорным, что исключено и как использовать результат дальше.»
