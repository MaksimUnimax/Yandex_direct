# KW-001 — BRIDGE EVIDENCE PERSISTENCE GATE

Date: 2026-08-31  
Status: **ACTIVE / UNIVERSAL / OWNER-APPROVED / OWNER-LOCKED**

## Purpose

This rule exists to prevent a useful Yandex Marketing Bridge result from existing only in chat/runtime memory and then being lost before it is used in later analysis.

The objective is **not** to archive every Bridge message.

Canonical distinction:

```text
BRIDGE MESSAGE != PROJECT EVIDENCE
USEFUL SUCCESSFUL BRIDGE EVIDENCE -> DURABLE GITHUB STORAGE
ADMINISTRATIVE / ERROR / EMPTY ACK -> DO NOT ARCHIVE AS EVIDENCE
CHAT != DURABLE PROJECT STORAGE
```

## What MUST be persisted immediately

Persist a Bridge result before further analysis or another provider action when it is a **successful substantive result that will be used downstream**.

Typical required cases:

```text
1. successful provider_result with real Wordstat / Search / Webmaster / Metrika / Direct / GenSearch data;
2. successful batch/chunk containing one or more real provider results that matter to the job;
3. successful projection/recovery result containing substantive provider evidence that is needed for analysis or reconstruction;
4. any other successful Bridge output whose loss would remove evidence needed to reproduce, verify or continue the current analytical step.
```

For paid provider acquisition, the trigger is especially strict:

```text
SUCCESSFUL USEFUL PROVIDER EVIDENCE RECEIVED
-> IMMEDIATE GITHUB WRITE
-> GITHUB READBACK + ACCOUNTING QA
-> ONLY THEN ANALYZE / ISSUE NEXT PAID PROVIDER ACTION
```

The full useful evidence must be preserved with enough fidelity for downstream work. If normalization is used, do not discard unique source fields that are required later.

## What MUST NOT be archived as evidence merely because Bridge returned it

Do not create evidence files for routine control-plane noise that has no downstream analytical value, including:

```text
SERVICE_NOT_ACTIVE and other admission errors;
failed validation before provider execution;
empty start acknowledgements;
empty status acknowledgements;
pause/resume/cancel acknowledgements without substantive evidence;
service-switch acknowledgements;
other request_executed=false administrative responses with no useful provider data;
duplicate copies of evidence already durably stored.
```

If such a control response changes execution state, record only the **minimal current state needed to continue safely** in the job state/flow. Do not preserve the whole response as an evidence artifact unless the owner explicitly asks or the response itself becomes necessary to diagnose a material system defect.

## Operational-state exception

A successful control response may be represented minimally in current job state when needed for safe continuation, for example:

```text
job_id
job status
pending / succeeded / failed / unknown counts
current provider-call count / cost
next safe action
observed installed Bridge version or active service when operationally material
```

This is not an instruction to archive the entire control response.

## Analysis source rule

After useful Bridge evidence has been persisted:

```text
ANALYZE FROM GITHUB READBACK
NOT FROM THE CHAT PASTE AS THE ONLY SOURCE
```

The chat may deliver the result, but it is only a transport channel.

## Fail-closed rules

```text
USEFUL_SUCCESSFUL_PROVIDER_EVIDENCE_WITHOUT_GITHUB_WRITE = PROCESS_FAILURE
NEXT_PAID_PROVIDER_ACTION_BEFORE_REQUIRED_WRITE_READBACK = PROHIBITED
CHAT_AS_ONLY_COPY_OF_USEFUL_PROVIDER_EVIDENCE = PROHIBITED
RUNTIME_STORAGE_AS_ONLY_COPY_OF_USEFUL_PROVIDER_EVIDENCE = PROHIBITED
ADMINISTRATIVE_BRIDGE_MESSAGE_ARCHIVED_AS_EVIDENCE_WITHOUT_DOWNSTREAM_NEED = PROCESS_NOISE
```

If GitHub write or readback fails:

```text
NEXT_PROVIDER_ACTION_ALLOWED = false
```

until the evidence is safely persisted or the owner explicitly changes the rule.

## Why this rule exists

A prior provider workflow demonstrated that browser/runtime storage and chat delivery can disappear independently after provider work has already occurred. Delayed persistence can force reconstruction, lose raw fields, or require paid replay.

The corrected principle is therefore:

```text
PERSIST WHAT IS VALUABLE TO THE WORK, NOT EVERYTHING THE BRIDGE SAYS.
```

This gate applies to every KW-001 step using Yandex Marketing Bridge.
