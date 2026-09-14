# KW-002 Step06 — S06Q001 SUBMIT ACCEPTED EVIDENCE

Date: 2026-09-14
Status: **PROVIDER SUBMISSION ACCEPTED / WAITING / RESULT NOT YET COLLECTED**

## Query identity

```text
QUERY_ID = S06Q001
QUERY_TEXT = амулет
JOB_ID = kw002-s06q001-20260914
TRANSPORT = DEFERRED_ASYNC
```

Release authority:
`STEP_06_S06Q001_EXECUTION_RELEASE_2026-09-14.md`

## Exact Bridge result returned after submitN

```json
{"action":"submitN","job_id":"kw002-s06q001-20260914","ok":true,"request_executed":true,"provider_calls":1,"processed":1,"normalized":0,"bounded_stop":false,"last":{"outcome":"accepted","code":null,"index":0,"operation_id":"spr2q2fbfldmt6poichd"},"progress":{"job_id":"kw002-s06q001-20260914","control":"RUNNING","total":1,"counts":{"PENDING":0,"SUBMITTING":0,"WAITING":1,"COLLECTING":0,"RESULT_SAVED":0,"SUCCEEDED":0,"PARSE_FAILED":0,"FAILED":0,"UNKNOWN":0,"CANCELLED":0},"requests_started":1,"operations_accepted":1,"polls_started":0,"unresolved":1,"all_successful":false,"busy":false,"revision":2}}
```

## Reconciled execution truth

```text
REQUEST_EXECUTED = true
PROVIDER_CALLS_THIS_COMMAND = 1
PROVIDER_CALLS_STEP06_TOTAL_SO_FAR = 1
PROCESSED = 1
NORMALIZED = 0
OUTCOME = accepted
ITEM_INDEX = 0
OPERATION_ID = spr2q2fbfldmt6poichd
ITEM_STATE = WAITING
REQUESTS_STARTED = 1
OPERATIONS_ACCEPTED = 1
POLLS_STARTED = 0
UNRESOLVED = 1
REVISION = 2
RESULT_SAVED = 0
SUCCEEDED = 0
FAILED = 0
UNKNOWN = 0
CANCELLED = 0
```

This is a successful deferred provider acceptance, not a completed Search result and not zero-result evidence.

## Anti-duplicate boundary

- Do not call submit/submitN again for this job.
- Do not create another job for S06Q001.
- Preserve operation ID `spr2q2fbfldmt6poichd` and collect only through that lifecycle.
- No S06Q002 release exists.
- Automatic retry is forbidden.

## Next safe action

After this evidence is published and remote-read back, and after the deferred minimum collection delay has elapsed, exactly one explicit `collectN count=1` may be released for `kw002-s06q001-20260914`.

If collection remains WAITING, persist the new poll truth and do not resubmit. If a result is received, preserve every returned normalized result row and provenance before any next query release.
