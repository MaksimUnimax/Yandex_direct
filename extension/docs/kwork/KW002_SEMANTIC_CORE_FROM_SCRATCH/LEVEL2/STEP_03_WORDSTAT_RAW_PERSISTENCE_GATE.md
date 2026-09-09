# KW-002 — LEVEL 2 / STEP 03 WORDSTAT FULL RAW PERSISTENCE GATE

Updated: 2026-09-09  
Status: **ACTIVE / UNIVERSAL / OWNER-LOCKED / MANDATORY AFTER EVERY WORDSTAT PROVIDER RESPONSE**

## 0. Purpose

This gate exists to prevent a repeated project failure: treating a provider response as usable merely because it appeared in ChatGPT, returned HTTP 200, returned `status=OK`, or was visually inspected.

The authoritative rule is stricter:

> **Every factual Wordstat provider response must be durably recorded in full before another provider request is allowed.**

This applies to KW-002 Step 03 and to later Wordstat acquisition stages inheriting Step-03 semantics:

```text
STEP 03 = primary Wordstat acquisition
STEP 05 = targeted Wordstat expansion / coverage
STEP 08 = competitor-derived Wordstat expansion
```

It applies to successful responses, provider errors, empty payloads, skipped results, and outcome-unknown receipts.

---

# 1. OWNER-LOCKED ORDER AFTER EVERY PROVIDER RESPONSE

```text
PROVIDER REQUEST EXECUTED
→ RECEIVE COMPLETE BRIDGE RESULT ENVELOPE
→ INSPECT THAT THE ACTUAL FACTUAL BODY IS PRESENT
→ WRITE THE COMPLETE RAW RESULT TO work/<JOB_ID>/ RAW EVIDENCE
→ WRITE/UPDATE RECEIPT + REQUEST/SEED/REGION/DEVICE/COST PROVENANCE
→ REMOTE GITHUB READBACK OF THE SAVED RAW ARTIFACT
→ RECONCILE BODY FIELDS / ROW COUNTS / REQUEST ID
→ ONLY THEN MAY ANOTHER PROVIDER REQUEST BE ISSUED
```

Before remote readback passes:

```text
NEXT_WORDSTAT_PROVIDER_REQUEST_ALLOWED = false
```

---

# 2. WHAT “FULL RAW RESULT” MEANS

Do **not** save only a summary, status, count, examples, or analyst interpretation.

For `WORDSTAT_RESULT_V1`, preserve the complete returned envelope, including every field actually returned by the Bridge, at minimum where present:

```text
bridge
version
service
operation
request_id
run_id
job_id
status
reason
cost_estimate
policy
command
http_status
elapsed_ms
result
request_executed
automatic_retry
```

Inside `result`, preserve the complete factual provider body exactly as returned, including all rows:

```text
results[]        = EVERY returned phrase + count
associations[]   = EVERY returned association phrase + count
totalCount
```

For an error, preserve the complete error body instead of converting it to a note:

```text
result.error.http_status
result.error.code
result.error.message
```

For `{}` or another unusual payload, preserve the literal returned payload. Do not synthesize missing fields into raw evidence.

---

# 3. HARD FAILURE CLASSES

The following are all FAIL:

```text
HTTP 200 = SAVED EVIDENCE
STATUS OK = SAVED EVIDENCE
RESPONSE VISIBLE IN CHAT = SAVED EVIDENCE
ANALYST READ THE RESPONSE = SAVED EVIDENCE
TOTALCOUNT SAVED WITHOUT RESULTS[] = FAIL
ROW COUNT SAVED WITHOUT ROWS = FAIL
FIRST / LAST / SAMPLE PHRASES ONLY = FAIL
ASSOCIATIONS DROPPED = FAIL
DUPLICATE OCCURRENCES DROPPED = FAIL
ERROR BODY REPLACED BY SUMMARY = FAIL
CHAT USED AS THE ONLY RAW STORAGE = FAIL
NEXT PROVIDER REQUEST BEFORE RAW REMOTE READBACK = FAIL
```

---

# 4. RAW OCCURRENCE AUTHORITY

Every returned occurrence remains tied to the request that produced it.

Do not deduplicate or clean the raw provider evidence while saving it.

```text
SEED A → phrase X
SEED B → phrase X
```

are two preserved raw occurrences even if the phrase text is identical.

Noise, ambiguity, morphology collisions, irrelevant rows, low-frequency rows and duplicate text are analytical matters for later steps. They are **not** reasons to drop raw acquisition evidence.

---

# 5. REQUIRED JOB STORAGE

Job-specific raw provider evidence belongs under the active job, for example:

```text
work/<JOB_ID>/STEP_03_WORDSTAT_RAW/
```

Each provider response must have a unique durable artifact keyed by stable request provenance. Preferred filename shape:

```text
<sequence>__<seed_id>__<request_id>.txt
```

or, for a controlled diagnostic/manual request outside a production batch lineage:

```text
MANUAL__<sequence>__<sanitized_phrase>__<request_id>.txt
```

The raw file must contain the complete `WORDSTAT_RESULT_V1` / `WORDSTAT_BATCH_RESULT_V1` material received for that provider action.

Maintain a receipt register containing at least:

```text
sequence
seed_id / diagnostic_id
seed_phrase
request_id
http_status
status
request_executed
results_rows
association_rows
total_count
raw_file
raw_blob_sha / readback locator
cost_estimate
remote_readback
notes
```

A receipt register is **not** a replacement for raw files.

---

# 6. MULTI-COMMAND / LARGE-RESPONSE RULE

A Manual multi-command block may prove Bridge sequencing/transport, but it does not weaken persistence requirements.

If one user delivery contains multiple provider result envelopes:

```text
RESULT 1
RESULT 2
...
RESULT N
```

then **all N complete factual envelopes must be persisted** before another provider command is emitted.

```text
MULTI-COMMAND DELIVERY
!= permission to save only one aggregate summary
```

An aggregate transcript may additionally be saved, but per-request provenance must remain recoverable.

Large response volume is not a reason to truncate evidence:

```text
LARGE BODY
→ SAVE FULL BODY
→ USE DURABLE STORAGE / WORK FOR LATER LARGE-SCALE TRANSFORMATION

LARGE BODY
!= SAMPLE IT
!= SUMMARIZE IT IN PLACE OF RAW
!= KEEP IT ONLY IN CHAT
```

---

# 7. READBACK CHECK

Before allowing another provider request, verify from GitHub that the raw artifact contains the factual body, not just an envelope shell.

For a successful GetTop response where fields are present, verify:

```text
REQUEST_ID_MATCH = true
COMMAND_PHRASE_MATCH = true
NUM_PHRASES_MATCH = true
REGION_MATCH = true
DEVICE_MATCH = true
RESULTS_ARRAY_PRESENT = true
RESULT_ROWS_PRESERVED = true
ASSOCIATIONS_ARRAY_PRESENT = true
ASSOCIATION_ROWS_PRESERVED = true
TOTAL_COUNT_PRESERVED = true
RAW_TRUNCATION_DETECTED = false
REMOTE_GITHUB_READBACK = PASS
```

For an error response:

```text
REQUEST_ID_MATCH = true
HTTP_STATUS_PRESERVED = true
ERROR_CODE_PRESERVED = true
ERROR_MESSAGE_PRESERVED = true
REMOTE_GITHUB_READBACK = PASS
```

---

# 8. PASS / FAIL

A single provider result reaches persistence PASS only when:

```text
COMPLETE_BRIDGE_ENVELOPE_SAVED = true
COMPLETE_PROVIDER_BODY_SAVED = true
ALL_RETURNED_RESULTS_ROWS_SAVED = true
ALL_RETURNED_ASSOCIATION_ROWS_SAVED = true
TOTAL_COUNT_SAVED_WHEN_RETURNED = true
REQUEST_PROVENANCE_SAVED = true
ERROR_BODY_SAVED_WHEN_ERROR = true
RAW_FILE_REMOTE_READBACK = PASS
NO_CHAT_ONLY_RAW_EVIDENCE = true
```

Only then:

```text
CURRENT_RESULT_PERSISTENCE_GATE = PASS
NEXT_WORDSTAT_PROVIDER_REQUEST_ALLOWED = true
```

Any missing condition:

```text
CURRENT_RESULT_PERSISTENCE_GATE = FAIL / HOLD
NEXT_WORDSTAT_PROVIDER_REQUEST_ALLOWED = false
```

---

# 9. NON-REPEAT LESSON

### What failed before

The assistant sometimes inspected provider output, confirmed that phrases were visible, and proceeded to the next request without first materializing the full factual return in durable project storage.

### Why this is wrong

The chat window is not the acquisition authority. A future context can lose or truncate the body, and a status/count does not reproduce the returned semantic evidence.

### Permanent control

```text
NO NEXT PROVIDER REQUEST
UNTIL
FULL CURRENT RAW RESULT IS IN GITHUB AND READ BACK
```

---

# 10. PLAIN-LANGUAGE OWNER RULE

> **Не “пришло и всё ОК”, а сначала записать полностью всё, что реально пришло: каждую фразу, каждую частотность, associations, totalCount, request/envelope и ошибки. Только после проверки сохранённого raw разрешён следующий запрос. Чат не считается хранилищем результата.**
