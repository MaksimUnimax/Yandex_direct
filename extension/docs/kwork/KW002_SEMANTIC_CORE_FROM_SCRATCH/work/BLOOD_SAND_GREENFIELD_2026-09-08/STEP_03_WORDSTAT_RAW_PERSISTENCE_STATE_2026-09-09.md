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

They remain:

```text
LEGACY_PRE_GATE_BACKFILL = PENDING
DO_NOT_REISSUE_PROVIDER_REQUESTS_FOR_STORAGE_RECOVERY = true
```

Existing historical batch raw files are not to be falsely relabelled as these later manual request IDs.

The pre-gate storage debt must be recovered from an exact preserved transcript/provider artifact if one is available. It must not be reconstructed from summaries and must not cause duplicate Wordstat requests.

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
