# B20 — Stage B scope-recovery blocker — 2026-09-13

## Current state

- `BRANCH = wip/ymb-async-popup-monitor-2026-09-13`
- `PRE_BLOCKER_HEAD = 48518805e300f55b7a50921c917122a59647bb65`
- `BASELINE = 666251c91dce8cb8a1bed414130409e043a1374b`
- `STAGE_A_READ_ONLY_POPUP_MONITOR = PASS`
- `STAGE_A_REAL_CHROME = PASS`
- `STAGE_A_PROVIDER_CALLS = 0`
- `QUALIFIED_STAGE_A_SOURCE = 466da55096bb5c36fd07c6601aba1389a6f1414e`
- `QUALIFIED_STAGE_A_EXTENSION_SRC_TREE_SHA256 = c8901b164d1a9c499c229cd9eeaf93e534e7f07ab0ea2b4400497be4fca154ba`
- `STAGE_B = BLOCKED_SCOPE_AUTHORITY_NOT_RECOVERED`
- `PROVIDER_CALLS_AFTER_STAGE_A = 0`

## Why this blocker exists

The prior staged plan explicitly separated the work:

1. Stage A = read-only deferred Search popup monitoring;
2. buttons / provider-action were not to be touched until Stage A had passed its own tests and allowlist gate;
3. Stage B was not to start before Stage A PASS.

Stage A is now evidence-backed PASS, but the exact previously agreed Stage B definition is not present in the current branch authorities and could not be recovered from the available persisted conversation/library context.

The missing authority is material: without it, implementing guessed controls could change provider execution, state transitions, cost behavior, recovery or ownership rules.

Therefore Stage B must not be inferred from older B17/B18/B19 pause/resume documents or from generic deferred Search capabilities.

## Scope protected while blocked

Until the exact Stage B authority is recovered, do not modify or add behavior in:

- deferred Search submit/collect provider actions;
- automatic/background polling;
- service worker async runtime;
- Search transport;
- request/cost admission;
- operation ownership/recovery;
- file delivery;
- composer Send;
- credentials;
- manifest host permissions;
- billing policy;
- provider protocol.

Do not add popup buttons whose action semantics are not backed by the missing Stage B definition.

## Stage A production delta remains the only accepted product delta

From baseline `666251c91dce8cb8a1bed414130409e043a1374b`, Stage A changed only:

1. `extension/src/popup.html`
2. `extension/src/popup_search_async_monitor.js`

QA-only workflow:

- `.github/workflows/ymb-async-popup-monitor-stage-a.yml`

Stage-A checkpoint:

- `B20_ASYNC_POPUP_MONITOR_STAGE_A_2026-09-13.md`

## Recovery work already attempted

The recovery pass searched:

- current GitHub branch and B20 artifacts;
- recent persisted file-library conversation material;
- exact phrases around `Stage A`, `Stage B`, `read-only monitor`, `buttons`, and `provider-action`;
- prior personal-context recovery for the staged popup-monitor plan.

No exact Stage B file/action/test allowlist was found.

Older deferred Search, B17 pause, B18 qualification and B19 network-enable authorities remain useful historical safety context only. They are not promoted to the missing Stage B execution authority.

## Exact next legal action

Recover the original Stage B definition from the owner-visible conversation or another explicit authority source.

Only after that source is available may the implementation proceed through:

`READ AUTHORITY -> DECLARE EXACT ALLOWLIST -> CODE -> TEST -> COMMIT -> REMOTE READBACK`

No provider call is authorized by this blocker document.
