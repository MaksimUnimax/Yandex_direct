# KW-002 Step06 — S06Q002 CONTROLLED REACQUISITION R1 LOCAL START PASS EVIDENCE

Date: 2026-09-16
Status: **PASS / LOCAL-ONLY START / ZERO PROVIDER CALLS / PROVIDER SUBMIT NOT YET RELEASED**

## 1. Scope

```text
QUERY_ID = S06Q002
QUERY_TEXT = оберег
ATTEMPT = CONTROLLED_REACQUISITION_R1
JOB_ID = kw002-s06q002-r1-20260916
YMB_VERSION = 0.1.8
```

## 2. Exact returned Bridge envelope

```json
{"action":"start","job_id":"kw002-s06q002-r1-20260916","ok":true,"request_executed":false,"provider_calls":0,"progress":{"job_id":"kw002-s06q002-r1-20260916","control":"RUNNING","total":1,"counts":{"PENDING":1,"SUBMITTING":0,"WAITING":0,"COLLECTING":0,"RESULT_SAVED":0,"SUCCEEDED":0,"PARSE_FAILED":0,"FAILED":0,"UNKNOWN":0,"CANCELLED":0},"requests_started":0,"operations_accepted":0,"polls_started":0,"unresolved":1,"all_successful":false,"busy":false,"revision":0}}
```

## 3. Verified invariants

```text
ok = true
request_executed = false
provider_calls = 0
control = RUNNING
total = 1
PENDING = 1
requests_started = 0
operations_accepted = 0
polls_started = 0
unresolved = 1
all_successful = false
busy = false
revision = 0
```

The local start created only the fresh deferred job state. No Yandex provider request was executed.

## 4. Boundary after local start

```text
SECOND_LOCAL_START_ALLOWED = false
PROVIDER_SUBMISSIONS_ALLOWED_NOW = 0
PROVIDER_COLLECTIONS_ALLOWED_NOW = 0
SYNCHRONOUS_SEARCH_CALLS_ALLOWED = 0
WORDSTAT_CALLS_ALLOWED = 0
GENSEARCH_CALLS_ALLOWED = 0
AI_SEARCH_CALLS_ALLOWED = 0
S06Q003_RELEASED = false
```

Before any `submitN`, this evidence and the successor cursor must be remote-read back, then a separate exact-one-submit release must be published and remote-read back.

## 5. Verdict

```text
S06Q002_R1_LOCAL_START = PASS
LOCAL_START_PROVIDER_CALLS = 0
PROVIDER_SUBMIT_RELEASED = false
S06Q003_RELEASED = false
```
