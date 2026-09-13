# OWNER SMOKE 0.1.6 — TEST-02 STATUS/READBACK

Date: 2026-09-13
Candidate: Yandex-Marketing-Bridge-0.1.6.zip
Candidate SHA-256: 81d47a540abb2c2847ab34f47060b812061ce2dc43237643ab8f7707d5e634e2

## Command

SEARCH_ASYNC_BATCH_API_V1
{"action":"status","jobId":"owner-smoke-016-01"}

## Owner-observed result

SEARCH_ASYNC_BATCH_RESULT_V1 {"action":"status","job_id":"owner-smoke-016-01","ok":true,"request_executed":false,"provider_calls":0,"progress":{"job_id":"owner-smoke-016-01","control":"RUNNING","total":1,"counts":{"PENDING":1,"SUBMITTING":0,"WAITING":0,"COLLECTING":0,"RESULT_SAVED":0,"SUCCEEDED":0,"PARSE_FAILED":0,"FAILED":0,"UNKNOWN":0,"CANCELLED":0},"requests_started":0,"operations_accepted":0,"polls_started":0,"unresolved":1,"all_successful":false,"busy":false,"revision":0}}

## Classification

TEST_02_STATUS_READBACK = PASS
REQUEST_EXECUTED = false
PROVIDER_CALLS = 0
STATE_PRESERVED_FROM_START = PASS
PENDING = 1
REQUESTS_STARTED = 0
OPERATIONS_ACCEPTED = 0
POLLS_STARTED = 0
UNKNOWN = 0
REVISION = 0

This confirms that status/readback is local and does not initiate Yandex provider traffic.
