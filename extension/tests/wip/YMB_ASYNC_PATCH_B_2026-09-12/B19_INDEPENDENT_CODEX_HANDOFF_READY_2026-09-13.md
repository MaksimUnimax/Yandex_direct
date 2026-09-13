# B19 — independent Codex handoff readiness checkpoint

Date: 2026-09-13
Status: **CHATGPT-OWNED PRE-GATE PREPARATION COMPLETE / INDEPENDENT CODEX NOT RUN**

This checkpoint is QA/process evidence only. It does not constitute independent acceptance and does not unlock release or owner installable handoff.

## Frozen candidate

- product version: `0.1.6`
- install ZIP: `Yandex-Marketing-Bridge-0.1.6.zip`
- install ZIP SHA-256: `81d47a540abb2c2847ab34f47060b812061ce2dc43237643ab8f7707d5e634e2`
- install ZIP bytes: `220045`
- extracted product tree SHA-256: `b87246c1377cda57cb9135f92814ec6885a1b607a9539be3a27bbc2fb1918b86`
- product files: `67`
- exact Actions source: run `34737506830`, artifact `10311695957`, `ymb-0.1.6-final-owner-candidate`

Latest local exact-ZIP recheck immediately before this checkpoint:

- byte count: `220045` — PASS
- SHA-256: `81d47a540abb2c2847ab34f47060b812061ce2dc43237643ab8f7707d5e634e2` — PASS
- ZIP integrity: `PASS`, no compressed-data errors

## Pre-Codex authorities now ready

1. permanent full regression gate: `extension/docs/CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md`
2. dependency/resource safety rule: `extension/docs/YMB_PATCH_DEPENDENCY_AND_RESOURCE_SAFETY_RULE.md`
3. exact artifact consumer readback: `B19_PRE_CODEX_TRANSPORT_READBACK_2026-09-13.md`
4. B19-specific executable PD map: `B19_FINAL_PD_EXECUTION_MAP.md`
5. updated independent Codex prompt: `B19_INDEPENDENT_CODEX_GATE_PROMPT.md`
6. current continuation cursor: `CONTINUATION_CURSOR_2026-09-12.json`

B19-specific PD map commit:
`a348c28d938d5ceefaac1c10edb413122ca34e30`

Updated Codex prompt commit:
`7abd4a9d47390403b734ae5a7539d7031d4b71be`

Pre-Codex cursor commit before this checkpoint:
`b8a7b89f2215957d3cf5a8e58e0dc4e41b0fb163`

## B18/B19 conflict resolved

The obsolete B18 PD-16 assumption that `operation.api.cloud.yandex.net` must be disabled has been explicitly superseded for B19.

B19 expected boundary:

- Search host enabled;
- Operation host enabled;
- deferred Search Manual-only;
- `chrome.alarms` absent;
- no background deferred polling;
- fixed Search POST / Operation GET lifecycle;
- persisted operation id before later paid work;
- raw result persistence before normalization;
- `UNKNOWN` means no automatic resubmit;
- injected host/API-key/folder values fail closed.

The independent prompt now makes `B19_FINAL_PD_EXECUTION_MAP.md` mandatory and forbids restoring the obsolete B18 disabled-operation-host state.

## Post-freeze branch diff audit

Frozen package workflow commit used as diff base:
`1b44ff384d9e398e6b7bd74a0cca570a2c3071cd`

Current pre-checkpoint branch HEAD audited:
`b8a7b89f2215957d3cf5a8e58e0dc4e41b0fb163`

Git compare result:

- status: ahead
- commits after frozen package base: `8`
- changed paths: `5`
- `extension/src` changed paths: `0`
- product-file changes: `0`

Changed paths were only:

- `extension/tests/wip/YMB_ASYNC_PATCH_B_2026-09-12/B19_FINAL_PACKAGE_GATE_CHECKPOINT.md`
- `extension/tests/wip/YMB_ASYNC_PATCH_B_2026-09-12/B19_FINAL_PD_EXECUTION_MAP.md`
- `extension/tests/wip/YMB_ASYNC_PATCH_B_2026-09-12/B19_INDEPENDENT_CODEX_GATE_PROMPT.md`
- `extension/tests/wip/YMB_ASYNC_PATCH_B_2026-09-12/B19_PRE_CODEX_TRANSPORT_READBACK_2026-09-13.md`
- `extension/tests/wip/YMB_FILE_DELIVERY_PATCH_A_2026-09-12/CONTINUATION_CURSOR_2026-09-12.json`

Therefore all work after the frozen package base is QA/evidence/cursor work only. The exact product candidate remains the immutable ZIP/tree stated above.

## Independent gate boundary

Independent Codex campaign status: `NOT_RUN`.

No later hidden independent run was found after the original B19 prompt checkpoint.

Independent campaign must:

- use the exact Actions artifact directly, with no owner file transport;
- execute every enabled `PD-00..PD-17` from the B19-specific map;
- use synthetic/controlled provider fixtures only;
- make real provider calls: `0`;
- use owner credentials/profile: `NO`;
- make production edits: `0`;
- return one final classification: `PASS`, `FAIL_PRODUCT`, `FAIL_ARTIFACT`, or `FAIL_HARNESS`;
- never return overall PASS with any enabled `NOT_RUN`.

## Release state

```text
CHATGPT_PRE_GATE_PREPARATION = COMPLETE
B19_FINAL_PD_MAP = READY
INDEPENDENT_CODEX_PROMPT = READY
EXACT_ARTIFACT_TRANSPORT_READBACK = PASS
PRODUCT_BYTES_AFTER_FREEZE_CHANGED = NO
INDEPENDENT_CODEX_GATE = NOT_RUN
RELEASE_ALLOWED = NO
OWNER_INSTALLABLE_HANDOFF = FORBIDDEN
```

Next unit is exactly one independent full Codex `PD-00..PD-17` campaign. No B9-B19 development work is to be restarted unless that independent campaign returns a product failure requiring a bounded correction.
