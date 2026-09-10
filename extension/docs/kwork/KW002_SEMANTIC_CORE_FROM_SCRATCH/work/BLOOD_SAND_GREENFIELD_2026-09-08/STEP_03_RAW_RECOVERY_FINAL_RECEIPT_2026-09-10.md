# STEP 03 — RAW RECOVERY FINAL RECEIPT

Date: 2026-09-10
Job: `BLOOD_SAND_GREENFIELD_2026-09-08`
Status: **RECOVERY COMPLETE / DURABLE FEED-FORWARD 79/79 / STEP 04 NOT AUTHORIZED**

## What was repaired

Step03 provider acquisition itself had completed all 79 canonical primary probes. A later independent readback found that the GitHub feed-forward layer was not lossless for two large RAW carrier bundles.

Initial durable state discovered by late QA:

```text
CANONICAL_PRIMARY_PROBES = 79
PROVIDER_ACQUISITION_OUTCOMES = 79/79
LOSSLESS_GITHUB_FEED_FORWARD_RAW = 60/79
AFFECTED_RUN_ORDERS = 32-48,50,51
```

Run 49 was independently readable and never required recovery.

## Recovery method

The original complete delivery text for the affected blocks was located in preserved prior-dialogue File Library material. Runs 50 and 51 were small complete empty provider outcomes and were rehydrated without provider replay.

For large runs 32-48, the available file-search interface could not provide a lossless full rehydration stream, so the owner-authorized fallback was used: one fresh Wordstat recovery observation at a time, with complete persistence and GitHub readback before moving to the next probe.

Historical request IDs remained separate provenance and were never rewritten as fresh request IDs.

## Completed recovery inventory

```text
RUN_50 = RECOVERED WITHOUT PROVIDER REPLAY / PASS
RUN_51 = RECOVERED WITHOUT PROVIDER REPLAY / PASS
RUN_32 = FRESH CURRENT WORDSTAT RECOVERY OBSERVATION / PASS
RUN_33 = FRESH CURRENT WORDSTAT RECOVERY OBSERVATION / PASS
RUN_34 = FRESH CURRENT WORDSTAT RECOVERY OBSERVATION / PASS
RUN_35 = FRESH CURRENT WORDSTAT RECOVERY OBSERVATION / PASS
RUN_36 = FRESH CURRENT WORDSTAT RECOVERY OBSERVATION / PASS / 2000 RESULTS RECONCILED
RUN_37 = FRESH CURRENT WORDSTAT RECOVERY OBSERVATION / PASS / 595 RESULTS RECONCILED
RUN_38 = FRESH CURRENT WORDSTAT RECOVERY OBSERVATION / PASS / 783 RESULTS DIRECT REMOTE LINE COUNT
RUN_39 = FRESH CURRENT WORDSTAT RECOVERY OBSERVATION / PASS / 818 RESULTS DIRECT REMOTE LINE COUNT
RUN_40 = FRESH CURRENT WORDSTAT RECOVERY OBSERVATION / PASS / 569 RESULTS DIRECT REMOTE LINE COUNT
RUN_41 = FRESH CURRENT WORDSTAT RECOVERY OBSERVATION / PASS / 952 RESULTS DIRECT REMOTE LINE COUNT
RUN_42 = FRESH CURRENT WORDSTAT RECOVERY OBSERVATION / PASS / 548 RESULTS DIRECT REMOTE LINE COUNT
RUN_43 = FRESH CURRENT WORDSTAT RECOVERY OBSERVATION / PASS / 593 RESULTS DIRECT REMOTE LINE COUNT
RUN_44 = FRESH CURRENT WORDSTAT RECOVERY OBSERVATION / PASS / 1074 RESULTS DIRECT REMOTE LINE COUNT
RUN_45 = FRESH CURRENT WORDSTAT RECOVERY OBSERVATION / PASS / 987 RESULTS DIRECT REMOTE LINE COUNT
RUN_46 = FRESH CURRENT WORDSTAT RECOVERY OBSERVATION / PASS / 915 RESULTS DIRECT REMOTE LINE COUNT
RUN_47 = FRESH CURRENT WORDSTAT RECOVERY OBSERVATION / PASS / 809 RESULTS DIRECT REMOTE LINE COUNT
RUN_48 = FRESH CURRENT WORDSTAT RECOVERY OBSERVATION / PASS / 594 RESULTS DIRECT REMOTE LINE COUNT
```

Final run 48 authority:

```text
fresh_request_id = wordstat-9d96a936-b280-4cfb-abb0-5f4a280acd13
historical_request_id = wordstat-24ddaafc-4e79-4bec-9130-f97e7c0e1175
results_rows = 594 / lines 22..615
associations_rows = 15 / lines 618..632
totalCount = 37962
raw_blob_sha = e7e9e63d666ab5af0603ed582a3720abfcda33c0
remote_readback = PASS
```

## Provider accounting for recovery only

```text
FRESH_RECOVERY_PROVIDER_REQUESTS = 17
ESTIMATED_RECOVERY_PROVIDER_COST_RUB = 0.34
NEW_PROVIDER_REQUESTS_AFTER_RUN_48 = 0 REQUIRED
```

Historical provider economics remain separate and are not overwritten by recovery accounting.

## Final Step03 gate

```text
STEP03_PROVIDER_ACQUISITION_COMPLETE = true
STEP03_PROVIDER_ACQUISITION = 79/79
STEP03_DURABLE_RAW_COMPLETE = true
STEP03_DURABLE_FEED_FORWARD = 79/79
STEP03_REMAINING_RECOVERY = 0
STEP03_RAW_RECOVERY = COMPLETE / PASS
SILENT_ROW_LOSS_ACCEPTED = false
SEARCH_OR_GENSEARCH_USED_DURING_RECOVERY = false
```

## Independent Step04 boundary

Completing Step03 does **not** authorize Step04. Current Level2 authority remains:

`LEVEL2/STEP_RULES_INDEX.md` = `DRAFT FOR OWNER REVIEW / DO NOT EXECUTE YET`

Therefore:

```text
GATE_A_STEP03_DURABLE_79_OF_79 = PASS
GATE_B_LEVEL2_STEP04_OWNER_AUTHORITY = NOT YET ACCEPTED
STEP04_EXECUTION_ALLOWED = false
NEXT_ACTION = AWAIT / RECONCILE EXPLICIT OWNER DECISION FOR LEVEL2 STEP04 METHOD GATE
```

No Search, GenSearch, AI-search, semantic triage, clustering, ownership mapping, or sealed prior Blood & Sand analytical research was used to close this recovery task.
