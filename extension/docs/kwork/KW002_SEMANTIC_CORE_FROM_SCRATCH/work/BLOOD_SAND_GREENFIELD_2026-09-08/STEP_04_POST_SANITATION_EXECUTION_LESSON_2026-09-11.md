# KW-002 Blood & Sand — Step04 post-sanitation execution lesson

Date: 2026-09-11
Status: **RECORDED / ANTI-REGRESSION INPUT FOR LATER MATERIALIZERS**

## Confirmed execution issue

During the post-sanitation Step04 local QA, one intermediate mismatch was detected between the QA expectation and the produced field format/schema. The issue was localized and corrected before the final full-volume rerun and before the accepted owner-relay commit.

The surviving final artifacts do not preserve enough detail to name the exact intermediate field safely. Therefore this document records only what is supported and does not invent a field name or failure mechanism.

## Anti-regression rule

For every later full-volume materializer:

```text
1. freeze output schema before the expensive full-volume run;
2. validate field names, types, enum/value format and null/empty representation on a small deterministic fixture;
3. validate the QA parser against that same schema;
4. only then run full-volume materialization;
5. if a schema/QA mismatch appears, fix the underlying producer-or-contract mismatch;
6. rerun the complete dataset;
7. never patch only the failing QA sample;
8. record any confirmed schema defect in the execution failure ledger.
```

Required gate:

```text
OUTPUT_SCHEMA_FROZEN = PASS
QA_SCHEMA_COMPATIBILITY = PASS
FULL_VOLUME_RERUN_AFTER_SCHEMA_FIX = PASS if a fix was required
SAMPLE_ONLY_PATCHING = 0
```

## Scope

This is an execution-process lesson, not a semantic correction to Step04. The accepted Step04 authority and its counts remain unchanged.
