# KW-001 — Step 14 no-run-skip and obsolete crawler removal rule

Date: 2026-09-02
Status: ACTIVE / STEP-14-SPECIFIC / OWNER-REQUIRED

## Mandatory distinction

```text
DELETE_BAD_CODE != DELETE_RUN_RECORD
SUPERSEDED_IMPLEMENTATION != SUPERSEDED_EVIDENCE_HISTORY
```

The obsolete Step-14A custom crawler implementation must be removed from the active working tree, but every Step-14A Codex attempt must remain durably accounted.

Known obsolete implementation path:

`tests/OKNO_MSK/step14a_codex_site_discovery.py`

Any helper CODE created solely for that crawler must also be removed from active Step-14A implementation.

Do NOT delete historical evidence of the crawler attempts, including blocked-run reports, merge reconciliation, factual failure notes, Git history, or the canonical run ledger.

Canonical run ledger:

`tests/OKNO_MSK/STEP_14A_CODEX_RUN_LEDGER_2026-09-02.md`

## No-run-skip rule

```text
EVERY_CODEX_RUN_ATTEMPT -> RUN_LEDGER
FAILED_RUN != DISPOSABLE_HISTORY
NO_RUN_MAY_BE SILENTLY SKIPPED
NO LATER SUCCESS MAY ERASE AN EARLIER FAILURE
```

If a known local Step-14A attempt is missing from the ledger, add it with the exact available state/result before final Step-14 acceptance.

Every new browser-first Codex attempt must append itself to the ledger.

## Active execution mode

```text
PRIMARY_COLLECTION_TOOL = CODEX_BROWSER
CUSTOM_CRAWLER_ACTIVE_IMPLEMENTATION = FORBIDDEN
```

Code may be used only as a narrow post-collection helper for normalization, deduplication, reconciliation, counting, or artifact formatting. Do not build or run another site crawler.

Markers:

```text
KW001_STEP14_NO_RUN_SKIP = true
KW001_STEP14_FAILED_RUN_HISTORY_PRESERVATION_REQUIRED = true
KW001_STEP14_OBSOLETE_CRAWLER_CODE_REMOVAL_REQUIRED = true
KW001_STEP14_BROWSER_FIRST_ACTIVE = true
```
