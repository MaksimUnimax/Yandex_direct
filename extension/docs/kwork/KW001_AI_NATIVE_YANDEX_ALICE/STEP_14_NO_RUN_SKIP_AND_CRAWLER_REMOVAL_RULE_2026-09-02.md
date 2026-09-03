# KW-001 — Step 14 no-run-skip and obsolete-runner removal rule

Date: 2026-09-02  
Updated: 2026-09-03  
Status: **ACTIVE / STEP-14-SPECIFIC / UNIVERSAL / OWNER-REQUIRED**

## Purpose

Preserve the complete history of deterministic evidence attempts while allowing a superseded or unsafe implementation to be removed from the active working tree.

## Mandatory distinction

```text
DELETE_BAD_OR_OBSOLETE_CODE != DELETE_RUN_RECORD
SUPERSEDED_IMPLEMENTATION != SUPERSEDED_EVIDENCE_HISTORY
```

If a custom runner/crawler implementation has been superseded by a safer current collection method, remove or disable the obsolete active implementation as required by the current method. Do not delete historical evidence of its attempts.

Job-specific implementation paths and run-ledger filenames belong in the current Level-2 workspace/configuration, not in this permanent rule.

## Why this rule exists

A prior execution needed to abandon an unreliable custom collection implementation after several blocked attempts. The methodological risk was that deleting the obsolete implementation could be confused with permission to delete or omit the failed-run evidence.

### Root cause

```text
ACTIVE CODE LIFECYCLE
AND
EVIDENCE HISTORY LIFECYCLE
WERE NOT EXPLICITLY SEPARATED
```

The correction is to allow implementation replacement while making run history append-only/auditable.

## No-run-skip rule

```text
EVERY DETERMINISTIC RUN ATTEMPT -> CURRENT JOB RUN LEDGER / EQUIVALENT DURABLE RECORD
FAILED_RUN != DISPOSABLE_HISTORY
NO RUN MAY BE SILENTLY SKIPPED
NO LATER SUCCESS MAY ERASE AN EARLIER FAILURE
```

If a known attempt is missing from the current job run ledger, add the exact available state/result before final acceptance.

Every later attempt must append or otherwise preserve its own identity and outcome.

## Active execution mode

The active collector is whatever the current approved Step14 method declares after tool-selection review.

```text
CURRENT_APPROVED_COLLECTION_TOOL = JOB/METHOD CONFIGURATION
OBSOLETE_COLLECTION_IMPLEMENTATION = FORBIDDEN FOR NEW ACCEPTANCE EVIDENCE
```

Code may still be used as a narrow helper for normalization, deduplication, reconciliation, counting or artifact formatting where the current method permits it.

## Pass gate

```text
ALL_KNOWN_RUN_ATTEMPTS_ACCOUNTED = true
FAILED_RUN_HISTORY_PRESERVED = true
OBSOLETE_ACTIVE_IMPLEMENTATION_REMOVED_OR_DISABLED = true when required
CURRENT_ACCEPTANCE_OUTPUTS_TRACE_TO_CURRENT_APPROVED_RUN = true
NO_STALE_FAILED_OUTPUT_PROMOTED_TO_FINAL = true
```

This file follows `PERMANENT_STEP_RULE_UNIVERSALITY_AND_JOB_SEPARATION_GATE.md`.

## Markers

```text
KW001_STEP14_NO_RUN_SKIP = true
KW001_STEP14_FAILED_RUN_HISTORY_PRESERVATION_REQUIRED = true
KW001_STEP14_OBSOLETE_RUNNER_CODE_REMOVAL_REQUIRED = true
KW001_STEP14_CURRENT_APPROVED_COLLECTION_MODE_REQUIRED = true
```
