# MK02 STEP 12 — COMPETING-PAGE SAFETY DIAGNOSIS

## PURPOSE
Check related/current candidate pages deeply enough to prevent false cannibalization claims and unsafe architecture actions before the target architecture is frozen.

## WHY THIS STEP EXISTS
Multiple related pages, one Search snapshot or shared vocabulary can look like cannibalization while actually representing normal distinct tasks, parent/child roles or supporting content. MK02 needs a safety layer, but it does not sell a full standalone historical cannibalization audit.

## INPUTS
Step10 ownership map; Step11 structural actions; current related-page universe; current page evidence; saved ordinary Search evidence; optional first-party Yandex query×URL history when declared/available.

## REQUIRED EVIDENCE
Current page purpose for material URLs; current Search evidence where used; explicit execution mode/access state for first-party history; relationship/accounting universe; qualifying historical/harm evidence only when stronger claims are made.

## METHOD
Declare one mode before diagnosis:

```text
BASE_PUBLIC_EVIDENCE_MODE
ENHANCED_WITH_ACCESS_MODE
RESEARCH_GRADE_HISTORY_REQUIRED_MODE
```

In base MK02, default to `BASE_PUBLIC_EVIDENCE_MODE` unless separately expanded. Classify material URL/query-family cases as normal distinct tasks, parent/child, primary/supporting, current mismatch/multi-URL signals, duplicate/near-duplicate candidates, or evidence-insufficient. Keep current Search signal, historical competition and harmful impact as separate claim levels.

When first-party history is optional but unavailable, record that state explicitly; do not call the base product failed. When stronger historical/harm proof is required by a proposed destructive action, unavailable required history blocks/degrades that action.

## OUTPUTS
Competing-page case ledger; declared evidence mode; relationship/conflict verdicts; bounded remediation implications; unresolved/history-required handoff; QA.

## SOURCE KW-001 AUTHORITY
`STEP_13_COMPETING_PAGE_DIAGNOSIS_METHOD.md`; private-Yandex-access policy; research-to-execution schema gate.

## KNOWN FAILURE CLASSES
C13-01 through C13-08 in `ERRORS_AND_LESSONS.md`.

## ROOT CAUSES
Source discovery, current overlap and historical behavior were repeatedly compressed into stronger conclusions than the evidence supported.

## NON-REPEAT CONTROLS
Mode declaration; explicit source/access/capability/collection states; related-page relationship classification before conflict; historical claims require history; harm claims require qualifying harm evidence; QA tests missing required evidence; destructive remediation bounded by evidence.

## CLAIM BOUNDARIES
```text
RELATED PAGES != CANNIBALIZATION
CURRENT SERP OVERLAP != HISTORICAL COMPETITION
HISTORICAL COMPETITION != PROVEN HARM
BASE PUBLIC MODE != FULL HISTORY AUDIT
```

## UNKNOWN / BLOCKER BEHAVIOR
If public evidence cannot resolve the relationship, use `EVIDENCE_INSUFFICIENT` or equivalent. If a destructive action depends on unavailable history, defer that action rather than upgrade the claim.

## PASS GATE
All material cases accounted; current pages re-read where needed; mode/access state explicit; no public-only historical/harm overclaim; destructive recommendations do not exceed evidence; missing required evidence checked; affected Step11 actions updated/bounded when necessary.

## CLIENT-FACING MEANING
«Похожие страницы не называем каннибализацией автоматически. Сначала проверяем, отвечают ли они на разные задачи и действительно ли есть конфликт. Если для сильного вывода не хватает истории Яндекса, так и фиксируем и не предлагаем опасное объединение или удаление без основания.»
