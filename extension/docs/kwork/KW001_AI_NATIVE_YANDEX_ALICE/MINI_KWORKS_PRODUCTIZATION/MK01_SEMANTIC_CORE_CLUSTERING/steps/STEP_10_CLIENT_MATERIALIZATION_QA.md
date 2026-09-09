# MK01 STEP 10 — CLIENT MATERIALIZATION / QA

## PURPOSE
Turn current MK01 semantic authority into a standalone recipient-ready result and prove that the client can actually use it.

## WHY THIS STEP EXISTS
KW-001 had cases where canonical data/counts were correct but the promised standalone workbook, language, metric explanation or recipient usability was still wrong.

## INPUTS
Accepted current semantic universe, cluster authority, demand/provenance data, unresolved states and delivery contract.

## REQUIRED EVIDENCE
Current-authority manifest; source dataset identities/counts; client language/region; Wordstat metric semantics; generated workbook/report outputs.

## METHOD
Freeze physical deliverable contract before generation. Generate from current authority, never patch a stale workbook as truth. Provide separate recipient views for scope/how-to-use, full preserved phrase universe, active core, cluster summary, unresolved/Search-required, dictionary/method/metric/provenance and short delivery summary. Translate technical enums into Russian display values while retaining secondary traceability. Explain Wordstat count semantics, region/mode/snapshot and non-additivity. Inspect workbook physically/visually and by recipient task.

## OUTPUTS
Standalone MK01 workbook/equivalent + short delivery summary + QA/readback record.

## SOURCE KW-001 AUTHORITY
`STEP_19_CLIENT_DELIVERABLE_PACKAGING_METHOD.md`; `STEP_20_STANDALONE_SEMANTIC_CORE_GATE.md`; post-release recipient-acceptance lessons.

## KNOWN FAILURE CLASSES
E22 no standalone workbook; E23 stale workbook reused; E24 unnecessary recollection; E25 broad count mislabeled exact; E26 overlapping sums called market volume; E27 English/API leakage; E28 sheet names missed by language QA; E29 automated QA treated as acceptance; E30 bad representative phrase.

## ROOT CAUSES
Repository completeness was confused with client completeness; generated views became stale parallel truth; internal traceability/presentation convenience replaced recipient semantics.

## NON-REPEAT CONTROLS
Current authority manifest; audit preserved evidence before new provider calls; deterministic Russian display mapping; workbook-wide language scan including sheet titles; data/semantic/workbook/visual/recipient QA separated; final remote readback.

## CLAIM BOUNDARIES
The artifact reports Yandex semantic demand/clustering only. It does not imply Google support, page architecture, implementation TZ, ranking guarantees or exhaustive competitor/AI research.

## UNKNOWN / BLOCKER BEHAVIOR
Unresolved semantic rows remain visible in an appropriate review view. Missing metric metadata blocks stronger frequency labels; stale authority blocks release.

## PASS GATE
Source counts/joins reconcile; semantic QA PASS; workbook opens and is usable; Russian display layer PASS; metric labels accurate; uncertainty visible; no stale authority; recipient task walkthrough PASS; persisted/remote identity PASS.

## CLIENT-FACING MEANING
«Вы получаете не техническую выгрузку, а рабочий файл: итоговое ядро, группы, спорные запросы, понятные частотности и объяснение, как читать результат.»
