# Phase 6 Semantic Core / batch orchestration — baseline freeze

Date: 2026-08-27

Status: **P6-00 PASS / BASELINE FROZEN / PRODUCT IMPLEMENTATION NOT YET CHANGED**

## Exact authority

```text
repository = MaksimUnimax/Yandex_direct
Phase 6 branch = phase6/semantic-core-batch-orchestration-2026-08-27
branch base main = 112e4cd565ba16215f288a9e3a34b7e9f79e9d72
main root tree = fa8875b373dc0db7afb87cacb2c0f4614e944744
extension tree = cdd36c69c33389d84f48efd5c94d81d0c88c2d09
extension/src tree = edf1c2d3494ebbc53ae778d23be1457eb885b605
```

The Phase-6 branch was created directly from that exact live main commit.

## Phase 5 preservation

The Phase-6 baseline `extension/src` is exactly the accepted/closed Phase-5 product tree:

```text
accepted Phase-5 src tree = edf1c2d3494ebbc53ae778d23be1457eb885b605
Phase-6 baseline src tree = edf1c2d3494ebbc53ae778d23be1457eb885b605
identity = PASS
```

Therefore Phase 6 starts from the accepted Direct closure and does not fork from a stale pre-Direct product.

## Existing primitives selected for reuse

Architecture audit found reusable invariants already present in the accepted source:

### `shared/autorun_model.js`

- persisted run statuses;
- delivery claim/commit/confirm phases;
- pause/stop semantics;
- recovery decisions;
- `REQUEST_OUTCOME_UNKNOWN_NO_RETRY` fail-closed behavior after worker-session loss during a request.

### `shared/wordstat_protocol.js`

- trusted normalized Wordstat commands;
- command fingerprint helper;
- bounded `getTop` up to 2000 phrases;
- result envelope with `run_id`, `job_id`, `request_executed`, `automatic_retry` fields.

### `service_worker.js` / shared models

- Chrome local persisted run state;
- per-service policy admission;
- request/cost ledger;
- service ownership / active-service isolation;
- existing Manual/Autorun lifecycle.

## Design conclusion

Phase 6 must **extend/reuse** the existing transaction/recovery architecture.

It must not create an independent second provider lifecycle with different retry semantics.

The new pure batch-job model will sit above trusted provider commands and provide deterministic per-item state. Runtime integration will then map each admitted item to the existing provider execution path.

## P6-01 PASS criteria

```text
reusable lifecycle found = YES
unknown-outcome fail-closed invariant found = YES
trusted Wordstat command normalization found = YES
cost/request policy model found = YES
separate new lifecycle required = NO
```

Next step:

```text
P6-02/P6-03
write batch-job state/fingerprint/recovery tests
→ only then add the pure model implementation
```