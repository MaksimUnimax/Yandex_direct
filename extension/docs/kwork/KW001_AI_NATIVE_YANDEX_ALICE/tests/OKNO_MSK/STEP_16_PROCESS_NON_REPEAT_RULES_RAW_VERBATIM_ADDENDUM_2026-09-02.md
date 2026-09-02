# OKNO_MSK — Step 16 process non-repeat rules / verbatim raw-evidence addendum

Date: 2026-09-02
Authority type: **job-specific Step-16 execution rule / owner-requested non-repeat addendum**
Status: **ACTIVE FOR THE REMAINDER OF STEP 16**
Parent authority: `STEP_16_PROCESS_NON_REPEAT_RULES_2026-09-02.md`

## Failure S16-P09 — reconstructed provider JSON was initially treated as raw evidence

### What ChatGPT did wrong

After receiving the first live `SEARCH_RESULT_V1` for C15-004, ChatGPT created `STEP_16_C15-004_INITIAL_GENSEARCH_RAW.json` by reconstructing the returned fields into normalized JSON. That file preserved substantive provider fields but normalized presentation details and therefore was not a verbatim copy of the Bridge result supplied in dialogue.

The owner required the **complete response with all contents** to be preserved, not only parsed/reconstructed data.

### Why it happened

ChatGPT conflated two different evidence layers:

```text
COMPLETE SEMANTIC DATA CAPTURE
WAS INCORRECTLY TREATED AS
COMPLETE VERBATIM RAW CAPTURE
```

The persistence rule was applied at field-content level but not at original-response-text level.

### Correct authority for C15-004

```text
AUTHORITATIVE RAW:
STEP_16_C15-004_INITIAL_GENSEARCH_RAW_VERBATIM.txt

NON-AUTHORITATIVE RECONSTRUCTION:
STEP_16_C15-004_INITIAL_GENSEARCH_RAW.json

NORMALIZED ANALYTICAL RECORD:
STEP_16_C15-004_INITIAL_OBSERVATION.json
```

### Mandatory non-repeat control

For every subsequent Step-16 Bridge result, preserve evidence in this exact order:

```text
1. RECEIVE COMPLETE BRIDGE RESULT IN LIVE DIALOGUE
2. SAVE COMPLETE RESULT VERBATIM, INCLUDING RESULT PREFIX AND ALL CONTENT
3. READ BACK VERBATIM FILE
4. VERIFY THAT VERBATIM FILE CONTAINS:
   - full envelope
   - full message.content
   - every source object
   - every searchQueries object
   - every hint / optional semantic field present
   - transport fields
   - request_executed / automatic_retry
5. ONLY THEN CREATE NORMALIZED/PARSED OBSERVATION
6. READ BACK NORMALIZED OBSERVATION
7. ONLY THEN ANALYZE / CLASSIFY / PROCEED
```

A reconstructed JSON representation is allowed only as a derivative artifact and can never be named or treated as the authoritative raw response.

If verbatim persistence/readback fails:

```text
RAW_EVIDENCE_GATE = FAILED
ANALYSIS = BLOCKED
NEXT_PAID_ACTION = BLOCKED
```

## Markers

```text
STEP16_S16_P09_RAW_RECONSTRUCTION_FAILURE_RECORDED = true
STEP16_VERBATIM_RESULT_PREFIX_AND_FULL_CONTENT_REQUIRED = true
STEP16_NORMALIZED_DATA_NOT_EQUAL_RAW_EVIDENCE = true
STEP16_VERBATIM_READBACK_REQUIRED_BEFORE_ANALYSIS = true
```
