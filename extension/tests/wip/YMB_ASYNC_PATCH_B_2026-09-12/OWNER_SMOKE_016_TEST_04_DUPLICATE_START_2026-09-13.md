# OWNER SMOKE 0.1.6 — TEST-04 duplicate start

Date: 2026-09-13
Branch: `wip/ymb-file-delivery-patch-a-2026-09-12`
Build: Yandex Marketing Bridge 0.1.6
Job: `owner-smoke-016-01`

## Purpose
Verify that a duplicate `start` for an already existing deferred Search job fails closed before any provider request and does not schedule automatic retry.

## Owner-observed result

```text
YMB_ERROR_V1 {
  "bridge": "yandex-marketing-bridge",
  "version": "0.1.6",
  "status": "ERROR",
  "service": "search",
  "channel": "manual",
  "stage": "SEARCH_ASYNC_MANUAL",
  "code": "ASYNC_JOB_ALREADY_EXISTS",
  "message": "ASYNC_JOB_ALREADY_EXISTS",
  "recoverable": true,
  "request_executed": false,
  "automatic_retry": false,
  "run_id": null,
  "operation": "async.start",
  "autorun_continues": false,
  "timestamp": "2026-09-13T06:20:26.315Z",
  "operation_id": "manual-ffb321c5-5ca6-4e18-adf0-abc6972036ed"
}
```

## Classification

- expected error code: `ASYNC_JOB_ALREADY_EXISTS` — PASS
- request_executed: false — PASS
- automatic_retry: false — PASS
- service/channel: search/manual — PASS
- provider network initiated: NO according to returned execution provenance

`OWNER_SMOKE_TEST_04 = PASS`
