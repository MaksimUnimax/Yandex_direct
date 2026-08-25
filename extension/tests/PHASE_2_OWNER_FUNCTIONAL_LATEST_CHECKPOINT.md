# Phase 2 owner functional latest checkpoint

Date: 2026-08-25
Status: COMPLETE — owner Manual Search functional run closed

This is the compact durable continuation pointer for owner functional testing.
Update cadence during active testing was once per 4 completed tests.

## Completed blocks

Runs 17–20: PASS

- Run 17: invalid `sortMode` -> `INVALID_ENUM`, no provider request.
- Run 18: invalid `sortOrder` -> `INVALID_ENUM`, no provider request.
- Run 19: invalid `groupMode` -> final intended attempt `INVALID_ENUM`, no provider request. Before completion, premature attempts were blocked by `MANUAL_OPERATION_ACTIVE` and then `DELIVERY_IN_PROGRESS`; both had `request_executed=false`.
- Run 20: invalid `fixTypoMode` -> `INVALID_ENUM`, no provider request.

Runs 21–24: CLOSED

- Run 21: invalid `searchType` -> `INVALID_ENUM`, `request_executed=false`, no provider request. PASS.
- Run 22: intentionally unterminated JSON -> `COMMAND_DISCOVERY / UNTERMINATED_JSON`, `request_executed=false`, no provider request. PASS. The originally predicted `INVALID_JSON` expectation was corrected because discovery rejects an unclosed object earlier than command validation.
- Run 23: planned "Manual mode OFF + send Manual command" owner test -> NOT APPLICABLE / BAD TEST DESIGN. Turning Manual mode off removes the normal owner Manual dispatch path itself, so the test cannot be executed through the intended UI path. This is not a product failure.
- Run 24: popup/settings persistence -> PASS by established repeated owner use. The owner had already closed and reopened the popup many times during the functional campaign without losing the imported active Search configuration; no extra synthetic repetition is required.

## Patch backlog discovered during this campaign

When lifecycle state already means a new Manual command cannot be admitted, the Yandex action button must be disabled/non-clickable in advance.

At minimum this applies to:

- `MANUAL_OPERATION_ACTIVE`
- `DELIVERY_IN_PROGRESS`

Required patch behavior:

- disable the Yandex action button while either blocking state is active;
- prevent dispatch rather than accepting the click and only then returning the guard error;
- keep backend/manual-admission guards as fail-closed defense in depth;
- re-enable only after lifecycle completion is positively observed;
- do not reset worker timers, delivery timers or unrelated runtime state to refresh button availability;
- regression: `blocked -> click impossible -> lifecycle completes -> clickable again`.

This patch is now queued in `extension/docs/ROADMAP.md` as the next governed inter-phase product patch before Phase 3 implementation.

## Final owner functional status

```text
PHASE_2_OWNER_MANUAL_SEARCH_FUNCTIONAL_RUN = COMPLETE
REAL_OWNER_SEARCH_PROVIDER_PATH = PASS / HTTP 200
LOCAL_DISCOVERY_VALIDATION_POLICY_GUARDS = PASS across exercised cases
FURTHER_REPETITIVE_MANUAL_SEARCH_VALIDATION = NOT REQUIRED
NEXT_GOVERNED_PRODUCT_WORK = LIFECYCLE_GUARD_BUTTON_GATING_PATCH
AFTER_PATCH = PHASE_3_WEBMASTER_GOVERNED_REQUIREMENT_RECONSTRUCTION
```

The accepted Phase-2 artifact remains unchanged. Any implementation of the lifecycle button patch must create a new governed candidate and pass the applicable gate before owner handoff.
