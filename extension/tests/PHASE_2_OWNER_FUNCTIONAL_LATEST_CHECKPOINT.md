# Phase 2 owner functional latest checkpoint

Date: 2026-08-25
Status: ACTIVE

This is the compact durable continuation pointer for owner functional testing.
Update cadence: once per 4 completed tests.

## Completed block

Runs 17–20: PASS

- Run 17: invalid `sortMode` -> `INVALID_ENUM`, no provider request.
- Run 18: invalid `sortOrder` -> `INVALID_ENUM`, no provider request.
- Run 19: invalid `groupMode` -> final intended attempt `INVALID_ENUM`, no provider request. Before completion, premature attempts were blocked by `MANUAL_OPERATION_ACTIVE` and then `DELIVERY_IN_PROGRESS`; both had `request_executed=false`.
- Run 20: invalid `fixTypoMode` -> `INVALID_ENUM`, no provider request.

## Patch backlog discovered during this block

When lifecycle state already means a new Manual command cannot be admitted, the Yandex action button must be disabled/non-clickable in advance.

At minimum this applies to:

- `MANUAL_OPERATION_ACTIVE`
- `DELIVERY_IN_PROGRESS`

Backend admission guards remain as fail-closed defense in depth. Re-enabling the button must happen only after lifecycle completion is positively observed. Do not reset worker timers or unrelated runtime state just to refresh button availability.

This is a future patch requirement. Do not mutate the currently accepted Phase-2 artifact for this note alone.

## Resume pointer

```text
COMPLETED = runs 1–20
NEXT = run 21 / invalid searchType enum
CADENCE = 1 run = 1 command
REPO_CHECKPOINT_CADENCE = every 4 completed tests
```

## Run 21 — next

```text
SEARCH_API_V1
{
  "method": "search",
  "queryText": "купить ноутбук",
  "searchType": "SEARCH_TYPE_UNKNOWN",
  "page": 0,
  "groupsOnPage": 5
}
```

Expected:

```text
YMB_ERROR_V1
stage = COMMAND_VALIDATION
code = INVALID_ENUM
request_executed = false
automatic_retry = false
```

## Planned next block

- Run 21: invalid `searchType` -> local `INVALID_ENUM`.
- Run 22: malformed JSON after `SEARCH_API_V1` -> local parsing error.
- Run 23: conversation Manual mode OFF + valid Search -> Manual admission must block before provider.
- Run 24: close/reopen popup and verify imported settings/credentials persistence without issuing a provider request.

After Run 24, update this checkpoint once with results for Runs 21–24 and advance NEXT to Run 25.
