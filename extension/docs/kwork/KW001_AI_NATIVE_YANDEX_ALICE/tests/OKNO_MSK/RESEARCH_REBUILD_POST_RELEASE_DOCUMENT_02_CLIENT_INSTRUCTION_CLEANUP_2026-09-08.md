# Report №02 — client instruction cleanup after owner review

Status: **ANALYST RECHECK PASS / OWNER REVIEW PENDING**

## Owner-identified failure classes corrected

The owner rejected remaining client-facing text that described internal process, things the specialist should not do, or obvious browser/editor mechanics instead of the actual specialist work.

Permanent gate now records these additional failures:

- client process-history narration;
- negative pseudo-actions instead of required work;
- obvious `open/find/navigate/check` filler in specialist steps;
- repeated instructions across fields and rows.

The report-specific gate was rewritten so a specialist brief contains required work, concrete clarification tasks and observable acceptance results only.

## Client report cleanup

Removed from Report №02:

- report-stage process narration;
- `не делать` / `не внедрять` / `не размещать` style pseudo-actions;
- readiness meta-language such as `не выдавать за готовую задачу`;
- abstract `получить доказательство` language;
- obvious `откройте / найдите / перейдите / проверьте` mechanics;
- repeated `физически страницу не менять` text across 46 semantic rows;
- repeated identical missing-context text across 14 internal-link rows;
- client-facing prohibition blocks.

Replaced with:

- positive action language;
- action-specific professional operations;
- exact `Что уточнить` tasks for the five non-ready items;
- compact semantic mapping table;
- compact internal-link pair table;
- positive preservation requirements;
- one common acceptance section.

## Scope boundary

No new project-specific site, Search, Wordstat, Alice/AI or business-fact acquisition was performed. Quarantined post-hoc evidence was not used.

## Final structure

- ready actions: 3;
- clarification items: 5;
- semantic assignments: 46;
- additional checks: 4;
- unique internal-link pairs: 14;
- bibliography: 10;
- final PDF: 8 pages.

## QA

`RESEARCH_REBUILD_POST_RELEASE_DOCUMENT_02_CLIENT_INSTRUCTION_CLEANUP_QA_2026-09-08.json`

Results:

- banned client pseudo-action phrases: 0;
- obvious open/find/navigate mechanics: 0;
- project-internal traceability leaks: 0;
- literal `не` hits in the current client Markdown: 0;
- client process-meta hits: 0;
- semantic rows: 46;
- internal-link rows: 14;
- MD/DOCX/PDF banned-language hits: 0 / 0 / 0;
- DOCX visual QA: PASS, 8/8 pages;
- PDF visual QA: PASS, 8/8 pages.

NEXT_ACTION = OWNER_REVIEW_CLIENT_CLEANED_DOCUMENT_02__DO_NOT_START_DOCUMENT_03
