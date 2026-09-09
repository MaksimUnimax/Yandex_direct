# STEP 03 — WORDSTAT RAW PERSISTENCE STATE

Date: 2026-09-09
Job: `BLOOD_SAND_GREENFIELD_2026-09-08`

## Owner rule activation

The owner explicitly required that Wordstat factual results no longer be kept only in chat. From the activation point onward every provider result must be persisted in full factual form before the next provider block is issued.

```text
PERSISTENCE_ENFORCEMENT_START = M012
CURRENT_POLICY = FULL_RAW_BEFORE_NEXT_BLOCK
```

## M012–M021 current post-gate data

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

## Historical pre-gate M001–M011 vs current-provider re-query R001–R011

The original M001–M011 manual envelopes were received before full-raw immediate persistence was introduced. Their exact original request-specific bodies are still not present in the repository under their historical request IDs.

Historical original-ID durable truth remains:

```text
M001 wordstat-f3a8dbb5-fe66-42cd-b390-e0fa7224ebfa = ORIGINAL EXACT RAW NOT FOUND
M002 wordstat-4e09043d-8d78-4f31-9052-c6dabf03b8b8 = ORIGINAL EXACT RAW NOT FOUND
M003 wordstat-e1516768-06d8-4c2c-b98d-0f8e33ac06a1 = ORIGINAL EXACT RAW NOT FOUND
M004 wordstat-acb25ed1-af95-4b4d-a3b9-6f0457f039e3 = ORIGINAL EXACT RAW NOT FOUND
M005 wordstat-c5cd06dc-80f1-4c75-bcf1-38c5f80f394f = ORIGINAL EXACT RAW NOT FOUND
M006 wordstat-c43215e7-c98c-4dd9-9c53-1d7567bc439b = ORIGINAL EXACT RAW NOT FOUND
M007 wordstat-79853139-3b9c-41b2-81f1-93451f46f4fa = ORIGINAL EXACT RAW NOT FOUND
M008 wordstat-da37bf5f-90fe-484c-9420-4f92f4428446 = ORIGINAL EXACT RAW NOT FOUND
M009 wordstat-a80febbd-5fab-4af0-8206-c7ffb205ef2d = ORIGINAL EXACT RAW NOT FOUND
M010 wordstat-01dc88a5-3877-4cf4-8312-1e2559016641 = ORIGINAL EXACT RAW NOT FOUND
M011 wordstat-ae1bba7f-fb4e-473b-a57a-7e7087ce7794 = ORIGINAL EXACT RAW NOT FOUND
```

The owner subsequently explicitly allowed provider re-query when needed to recover the factual data. Eleven new Wordstat requests were therefore executed and returned as **new current-provider results with new request IDs**. They are recorded as `M001R`–`M011R` in the register and as `R001`–`R011` in the reconstruction package.

Their complete canonical response data is now durably persisted under:

`STEP_03_WORDSTAT_RAW/REQUERY_COMPRESSED/README_RECONSTRUCTION_2026-09-09.md`

Re-query package factual totals:

```text
REQUERY_CURRENT_PROVIDER_ENVELOPES = 11
REQUERY_PROVIDER_OK = 10
REQUERY_PROVIDER_ERROR_PRESERVED = 1
REQUERY_RESULTS_ROWS = 6599
REQUERY_ASSOCIATION_ROWS = 187
REQUERY_CANONICAL_RESPONSE_TEXT_BYTES = 691717
REQUERY_FULL_DATA_DURABLY_PERSISTED = 11/11
REQUERY_REMOTE_STORAGE_IDENTITY = PASS
REQUERY_LOCAL_RECONSTRUCTION_QA = PASS
```

Provenance boundary:

```text
R001..R011 != ORIGINAL M001..M011 BYTES
R001..R011 != ORIGINAL M001..M011 REQUEST IDS
ORIGINAL M001..M011 ROWS OVERWRITTEN = 0
```

The new data closes the **current factual data availability** problem for those eleven semantic probes while preserving the fact that the exact historical M001–M011 request bodies themselves were not recovered.

There is no repository-level rule forbidding a new Wordstat request merely because a prior request exists. Re-query/replay decisions must follow the owner instruction and the applicable execution/methodology gates for the specific task; this persistence file does not invent an independent provider-call prohibition.

## Durable counts after re-query persistence

```text
HISTORICAL_MANUAL_ROWS_M001_M021 = 21
HISTORICAL_ORIGINAL_RAW_DURABLY_SAVED = 10   # M012–M021
HISTORICAL_ORIGINAL_PRE_GATE_RAW_MISSING = 11 # M001–M011 originals
CURRENT_REQUERY_ROWS_M001R_M011R = 11
CURRENT_REQUERY_FULL_DATA_DURABLY_SAVED = 11
REGISTER_ROWS_TOTAL = 32
```

These categories must not be collapsed into a false statement such as “all original M001–M021 raw bodies were recovered.”

## Progression rule from M012 onward

For every newly received provider delivery under the owner persistence rule:

```text
RECEIVE RESULT BLOCK
→ SAVE THE COMPLETE FACTUAL RESULT
→ REMOTE READBACK / IDENTITY CHECK
→ UPDATE REGISTER
→ ONLY THEN TREAT THE PERSISTENCE CONDITION AS PASSED
```

If a newly received post-gate result is not persisted/read back:

```text
PERSISTENCE_GATE_NEXT_PROVIDER_BLOCK_ALLOWED = false
```

M012–M021 pass this prospective persistence condition. The later M001R–M011R data-persistence recovery also passes storage/readback and does not alter the M021 acquisition-cursor flag.

```text
CURRENT_POST_GATE_PERSISTENCE = PASS
REQUERY_DATA_PERSISTENCE = PASS
PERSISTENCE_GATE_NEXT_PROVIDER_BLOCK_ALLOWED = true
```

This last field is only the persistence gate. Any separate Wordstat depth/methodology, transport, owner, cost, or execution gate remains independently authoritative.
