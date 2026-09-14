# KW-002 Step06 — S06Q001 DEFERRED COLLECTION RELEASE

Date: 2026-09-14
Status: **EXACTLY ONE COLLECT ATTEMPT RELEASED / NO RESUBMIT / NO NEXT QUERY**

## Basis

- `S06Q001` provider submission was accepted exactly once.
- Durable submit evidence: `STEP_06_S06Q001_SUBMIT_ACCEPTED_EVIDENCE_2026-09-14.md`.
- Existing deferred provider operation is in `WAITING` state and its identity is preserved in that evidence authority.
- Submit and start are now forbidden for this job.

## Timing correction

The Bridge submit result does not expose a provider creation timestamp. Therefore no analytical claim is made that the five-minute deferred processing window has definitely elapsed.

Current accepted v0.1.6 runtime code provides the safe timing guard instead: before a collect network request, runtime calls the durable store `peekNext(... kind=collect, now=clock())`. If there is no due operation, runtime returns `NO_DUE_OPERATIONS` with `request_executed=false` before credentials, claim, policy reservation, transport, or provider GET.

Therefore an explicit collect command is safe even if it is early: early execution performs zero provider network calls and does not alter the accepted submit lifecycle.

## Exact released command

```text
SEARCH_ASYNC_BATCH_API_V1 {"action":"collectN","jobId":"kw002-s06q001-20260914","count":1}
```

## Allowed outcomes

1. `NO_DUE_OPERATIONS` + `request_executed=false` + provider calls 0: persist timing truth; do not resubmit. A later collect requires a new explicit release/current-state check.
2. Provider GET executes and operation remains `WAITING`: persist poll truth and same operation identity; do not resubmit; next collect requires a new explicit release.
3. Provider GET executes and result is received: preserve raw/result state and complete normalized result envelope/every returned result row before any S06Q002 release.
4. Provider/read/persistence/normalization uncertainty: persist exact failure state and stop; no blind retry.

## Hard boundary

```text
COLLECT_ATTEMPTS_RELEASED_NOW = 1
SUBMIT_ATTEMPTS_RELEASED_NOW = 0
S06Q002_RELEASED = false
STEP07_STARTED = false
AUTOMATIC_RETRY_ALLOWED = false
```
