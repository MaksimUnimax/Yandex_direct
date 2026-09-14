# Yandex Marketing Bridge — Search live acceptance

Date: 2026-09-14  
Version: 0.1.6  
Branch: `hotfix/ymb-file-delivery-p0-2026-09-14`  
Status: **PASS — no blocking functional defects found**

## Scope

Live functional acceptance of deferred/asynchronous Yandex Search, including provider-call accounting, batching, polling delay, normalization, export/pagination, control operations, budget/request guards, duplicate admission protection, idempotency, stale-revision protection, and persistence/recovery across page and extension runtime reloads.

## Live jobs exercised

- `live_search_smoke_20260914`
- `live_batch3_20260914`
- `live_control_20260914`
- `live_budget_cap_20260914`
- `live_duplicate_guard_20260914`
- `live_inflight_restart_20260914`

## Acceptance results

| Area | Result | Live evidence |
|---|---|---|
| Single async Search | PASS | `start` used 0 provider calls; `submit` used exactly 1 POST; early `collect` returned `NO_DUE_OPERATIONS` with 0 provider calls; due `collect` used exactly 1 provider GET and normalized the result to `SUCCEEDED`. |
| Batch submit/collect | PASS | Three queries produced exactly 3 provider POSTs and 3 unique operation IDs; `collectN` used exactly 3 provider GETs; final state `SUCCEEDED:3`. |
| Completed-job collect idempotency | PASS | Repeated collect after completion returned no due operation, made 0 provider calls, and did not change revision/counters. |
| Export integrity | PASS | Raw provider response and normalized SERP were both preserved. Full export and 2+1 paginated exports had no item loss or duplication. |
| Pause/resume | PASS | Submit while `PAUSED` returned `PAUSED` before network; `provider_calls:0`. Resume restored normal execution. |
| `cancelPending` mixed state | PASS | With `WAITING:1 + PENDING:2`, cancellation produced `WAITING:1 + CANCELLED:2` with 0 provider calls. The already accepted Yandex operation remained collectable and finished as `SUCCEEDED:1 + CANCELLED:2`. |
| Mixed-state export | PASS | Export contained one raw+normalized successful item and two cancelled items in correct index order. |
| `normalizeSaved` idempotency | PASS | Already normalized result returned `normalized:false`, `already_normalized:true`, made 0 provider calls, and left revision unchanged. |
| Stale export revision guard | PASS | Wrong revision returned `EXPORT_REVISION_CHANGED`, executed no provider request, and did not emit a stale export file. |
| Page reload persistence | PASS | After browser `Ctrl+R`, terminal job state, counters and revision were recovered exactly with 0 provider calls. |
| Terminal resubmit guard | PASS | Repeated submit on a completed batch returned `NO_PENDING_ITEMS`, made 0 provider calls, and did not alter counters/revision. |
| Budget cap | PASS | With two queries and `maxCostRub:0.04`, exactly one Search POST was allowed at the observed reservation of 30,500 microrub; the second was blocked before network with `BUDGET_LIMIT`. A later repeated submit remained blocked with 0 provider calls. |
| `maxRequests` validation + atomicity | PASS | Two queries with `maxRequests:1` were rejected locally before network. Follow-up `status` returned `ASYNC_JOB_NOT_FOUND`, proving no partial job was persisted. |
| Duplicate `jobId` protection | PASS | Repeated `start` returned `ASYNC_JOB_ALREADY_EXISTS` before network. Export confirmed the original query remained unchanged. |
| Extension/service-worker reload persistence | PASS | After Chrome extension Reload plus page reload, terminal job state was recovered exactly with 0 provider calls. |
| In-flight restart recovery | PASS | A `WAITING` job survived extension runtime reload with the same provider operation ID `spr8ld7332ijn4b0jorn`; no duplicate POST occurred. The same operation was then collected with exactly one GET and finished `SUCCEEDED`, `normalized:1`, `all_successful:true`. |

## Provider-call and cost safety

The live runs showed a reservation of **30,500 microrub (0.0305 RUB)** per started Search POST. Budget enforcement was verified both within one `submitN` call and across a later separate `submit` command. Paused, cancelled-pending, stale-export, idempotent-normalization, duplicate-job and completed-job guard paths all stopped before provider network execution.

## Non-blocking observations

- When the query count exceeds `maxRequests`, the current implementation returns the generic validation code `ASYNC_INTEGER_INVALID` rather than a more specific limit error. The safety behavior is correct: no job is created and no provider request is executed.
- Current file/composer delivery behavior was owner-accepted for continued work and is not treated as a blocker in this Search acceptance.

## Acceptance decision

**Yandex Search functionality in Yandex Marketing Bridge v0.1.6 is accepted for continued project work.**

No blocking functional defect was found in the live acceptance series. The tested implementation demonstrated bounded provider execution, durable state, correct export behavior, safe local guards, and recovery of an in-flight Yandex operation across extension runtime restart without duplicate submission.
