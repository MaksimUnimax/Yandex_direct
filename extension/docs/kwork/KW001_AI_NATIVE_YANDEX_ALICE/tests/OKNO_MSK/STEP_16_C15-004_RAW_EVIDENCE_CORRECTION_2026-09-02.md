# OKNO_MSK — Step 16 / C15-004 raw-evidence authority correction

Date: 2026-09-02
Case: `C15-004`
Attempt: `INITIAL`
Status: **ACTIVE CORRECTION**

## Defect

`STEP_16_C15-004_INITIAL_GENSEARCH_RAW.json` was created by reconstructing/parsing the live Bridge result into normalized JSON. Although it preserved the substantive fields, it normalized presentation details such as Markdown-wrapped URLs and escaped text. Therefore it is **not authoritative verbatim raw evidence**.

Root cause:

```text
COMPLETE SEMANTIC FIELD PRESERVATION
WAS INCORRECTLY TREATED AS
VERBATIM RAW RESULT PRESERVATION
```

## Correct authority

The authoritative raw evidence for this interaction is:

`STEP_16_C15-004_INITIAL_GENSEARCH_RAW_VERBATIM.txt`

It preserves the complete Bridge result as supplied in live dialogue, including:

```text
SEARCH_RESULT_V1 envelope
bridge/version/service/operation
request_id/run_id/status/reason
cost_estimate and policy
complete command
http_status / elapsed_ms
complete result.message.content
complete result.message.role
all sources with URL/title/used
all searchQueries with text/reqId
fixedMisspellQuery
isAnswerRejected
isBulletAnswer
all hints
problematicAnswer
transport wire_format/frame_count
request_executed
automatic_retry
```

## Authority boundary

```text
STEP_16_C15-004_INITIAL_GENSEARCH_RAW_VERBATIM.txt = AUTHORITATIVE_RAW
STEP_16_C15-004_INITIAL_GENSEARCH_RAW.json = NON_AUTHORITATIVE_RECONSTRUCTION / MAY SUPPORT NORMALIZATION ONLY
```

The reconstructed file must never be cited as proof of verbatim provider payload text.

## Non-repeat control

For every subsequent Step-16 Bridge result:

```text
LIVE BRIDGE RESULT RECEIVED
-> SAVE COMPLETE RESULT VERBATIM FIRST
-> READ BACK VERBATIM FILE
-> VERIFY FULL ENVELOPE + FULL MESSAGE CONTENT + ALL ARRAYS/FIELDS
-> ONLY THEN CREATE NORMALIZED/PARSED ARTIFACT
```

No normalized or reconstructed artifact may substitute for the verbatim raw capture.

Markers:

```text
STEP16_VERBATIM_RAW_REQUIRED = true
STEP16_RECONSTRUCTED_JSON_NOT_RAW_AUTHORITY = true
STEP16_C15_004_RAW_AUTHORITY_CORRECTED = true
```
