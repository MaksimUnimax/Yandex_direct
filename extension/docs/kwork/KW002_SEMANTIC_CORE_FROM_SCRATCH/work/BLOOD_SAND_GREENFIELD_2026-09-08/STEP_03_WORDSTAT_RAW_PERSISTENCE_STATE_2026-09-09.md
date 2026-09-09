# STEP 03 — WORDSTAT RAW PERSISTENCE STATE

Date: 2026-09-09
Job: `BLOOD_SAND_GREENFIELD_2026-09-08`

## Owner rule activation

The owner explicitly required that Wordstat factual results no longer be kept only in chat. From the activation point onward every provider result must be persisted in full factual form before the next provider block is issued.

```text
PERSISTENCE_ENFORCEMENT_START = M012
CURRENT_POLICY = FULL_RAW_BEFORE_NEXT_BLOCK
```

## Current post-gate state

M012–M021 have separate request-specific raw files under `STEP_03_WORDSTAT_RAW/`.

For each of M012–M021:

```text
COMMAND / REQUEST_ID PRESERVED = true
HTTP / STATUS PRESERVED = true
RESULTS[] PRESERVED = true
ASSOCIATIONS[] PRESERVED = true
TOTALCOUNT PRESERVED = true
REQUEST_EXECUTED PRESERVED = true
AUTOMATIC_RETRY PRESERVED = true
REMOTE_GITHUB_READBACK = PASS
```

The register authority is:

`STEP_03_MANUAL_LIVE_PROVIDER_RESULT_REGISTER_2026-09-09.csv`

## Pre-gate manual results M001–M011

M001–M011 were received before the owner introduced the full-raw-immediate-persistence rule. Their full manual envelopes were visible in chat, but separate durable manual raw files were not created at receipt time.

On 2026-09-09 an explicit repository-wide search was performed for every manual request id M001–M011:

```text
M001 wordstat-f3a8dbb5-fe66-42cd-b390-e0fa7224ebfa = NOT_FOUND
M002 wordstat-4e09043d-8d78-4f31-9052-c6dabf03b8b8 = NOT_FOUND
M003 wordstat-e1516768-06d8-4c2c-b98d-0f8e33ac06a1 = NOT_FOUND
M004 wordstat-acb25ed1-af95-4b4d-a3b9-6f0457f039e3 = NOT_FOUND
M005 wordstat-c5cd06dc-80f1-4c75-bcf1-38c5f80f394f = NOT_FOUND
M006 wordstat-c43215e7-c98c-4dd9-9c53-1d7567bc439b = NOT_FOUND
M007 wordstat-79853139-3b9c-41b2-81f1-93451f46f4fa = NOT_FOUND
M008 wordstat-da37bf5f-90fe-484c-9420-4f92f4428446 = NOT_FOUND
M009 wordstat-a80febbd-5fab-4af0-8206-c7ffb205ef2d = NOT_FOUND
M010 wordstat-01dc88a5-3877-4cf4-8312-1e2559016641 = NOT_FOUND
M011 wordstat-ae1bba7f-fb4e-473b-a57a-7e7087ce7794 = NOT_FOUND
```

Therefore the durable-storage truth is:

```text
MANUAL_RESULTS_RECEIVED_TOTAL = 21
FULL_RAW_DURABLY_SAVED_AND_READ_BACK = 10
FULL_RAW_NOT_DURABLY_SAVED = 11
M001_M011_DURABLE_STATUS = MISSING_EXACT_RAW / PRE_GATE_BACKFILL_REQUIRED
LEGACY_PRE_GATE_BACKFILL = PENDING
DO_NOT_REISSUE_PROVIDER_REQUESTS_FOR_STORAGE_RECOVERY = true
```

Existing historical batch raw files are not to be falsely relabelled as these later manual request IDs.

The pre-gate storage debt may only be recovered from an exact preserved transcript/provider artifact. It must not be reconstructed from summaries and must not cause duplicate Wordstat requests.

No report, QA output, cursor, or owner update may state that all 21 manual provider responses are durably saved until M001–M011 exact raw bodies have been recovered and independently read back.

## Progression rule from M012 onward

The historical pre-gate storage debt does not weaken the new prospective rule and does not authorize replay.

For every new provider delivery after M012:

```text
RECEIVE RESULT BLOCK
→ SAVE EACH COMPLETE FACTUAL RESULT SEPARATELY
→ REMOTE READBACK
→ UPDATE REGISTER
→ ONLY THEN ISSUE NEXT PROVIDER BLOCK
```

If any newly received post-gate result is not persisted/read back:

```text
NEXT_WORDSTAT_PROVIDER_BLOCK_ALLOWED = false
```

Current post-gate block M012–M021 has passed persistence/readback, therefore:

```text
CURRENT_POST_GATE_PERSISTENCE = PASS
NEXT_WORDSTAT_PROVIDER_BLOCK_ALLOWED = true
```
