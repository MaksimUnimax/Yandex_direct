# PHASE 1 — 0.1.1 LIVE TEST PLAN AND RESULT LEDGER

Date created: 2026-08-12
Candidate: `yandex-marketing-bridge-0.1.1-phase1-repair-candidate.zip`
Candidate SHA-256: `311353e2671052b7170e12db3e1318dfed4f59ccf945c7eda6ec59152ee3abfb`
Owner-interrupted DEF-01 patch candidate: `yandex-marketing-bridge-0.1.1-phase1-plaque-parity-candidate.zip`
Patch candidate SHA-256: `c0e3c36eaac1ebfa81ee44ca8cc376282b9aed601cd07cc596a6c235cfffb976`
Status: **ACTIVE TEST CAMPAIGN — OWNER-INTERRUPTED DEF-01 PATCH CHECKPOINT; LIVE RERUN PENDING**

## 1. Governing test method

This document is the authoritative Phase 1 live-test plan and result ledger.

From this checkpoint forward:

1. The complete planned test set is written here **before additional testing continues**.
2. Every executed test is updated here with status, actual behavior, expected behavior and evidence/notes.
3. Newly discovered tests may be added only in `Plan amendments` before they are executed.
4. No implementation patch is started while the campaign is still discovering defects, unless the owner explicitly interrupts the campaign and orders an immediate patch.
5. After the planned campaign is complete, the patch scope is derived from the FAIL list in this document.
6. After patching, all affected tests plus the required regression set are rerun and the same ledger is updated with the post-patch result.
7. A Phase 1 LIVE PASS cannot be declared from static/unit/emulation evidence alone. Real ChatGPT-command gates remain mandatory.

### Execution-channel rule

- **Real command/API behavior** is tested in the current ChatGPT conversation through actual `WORDSTAT_API_V1` commands.
- Maximum one executable Yandex command per assistant turn.
- Before every command that can execute a real Yandex request, current official Yandex pricing is freshly verified and the exact estimated cost is stated.
- While live command tests remain, every result-review turn immediately supplies the next required command/test instead of stopping at commentary.
- If the owner must do anything beyond the ordinary send/command flow, that action must be displayed as a prominent bold heading before the next command so it cannot be missed.
- **Popup/UI/toggle/state-machine behavior** is tested in controlled browser/emulation by the assistant. The owner is not used as a manual click-through test runner for repetitive checks; owner interaction is requested only when a real current-Chrome gate cannot be reproduced by emulation.
- Static/unit/regression tests are supporting evidence, not a substitute for live command gates.

### Result statuses

- `NOT RUN` — planned, not yet executed.
- `PASS` — actual behavior matches the acceptance condition.
- `FAIL` — extension behavior violates the acceptance condition.
- `BLOCKED` — cannot currently execute because another required capability is broken.
- `TEST ERROR` — the test input/procedure was wrong; this is not an extension failure.
- `PRE-RULE EVIDENCE` — live evidence obtained before this governed ledger was created; retained as factual evidence but not represented as having followed this procedure.

---

## 2. Pre-rule live evidence carried into this ledger

These observations occurred before the governed test method above was adopted.

| ID | Test | Status | Actual | Expected / conclusion |
|---|---|---|---|---|
| PRE-01 | Manual unsupported method, Debug OFF | PRE-RULE EVIDENCE / PASS for delivery | `YMB_ERROR_V1`, `UNSUPPORTED_METHOD`, `request_executed:false` automatically arrived in ChatGPT | Always-on error-to-chat path works for this case |
| PRE-02 | Error toast/reference UI parity | PRE-RULE EVIDENCE / FAIL | Generic green `YMB:` success-style notification was shown for an error/reporting path | Reference-style operation/error plaques only; no invented generic green YMB toast |
| PRE-03 | Debug toggle persistence | PRE-RULE EVIDENCE / FAIL | Debug returned OFF without extra Save |
| PRE-04 | Autorun start from popup | PRE-RULE EVIDENCE / FAIL | Popup remained `Не запущен`, iteration 0 | One start action must create current-conversation RUN |
| PRE-05 | `getRegionsTree` with missing credentials | PRE-RULE EVIDENCE | `SKIPPED / NO_CREDENTIALS`, `request_executed:false` | No network request without credentials |
| PRE-06 | Real `getRegionsTree` | PRE-RULE EVIDENCE / PASS | HTTP 200, tree returned | Real free Wordstat path works |
| PRE-07 | Free-call charge semantics | PRE-RULE EVIDENCE / FAIL | `estimated_rub:0`, `charged:true` | Free call must not claim charged |
| PRE-08 | Real `getTop` | PRE-RULE EVIDENCE / PASS | HTTP 200 | Core path works |
| PRE-09 | First monthly `getDynamics` attempt | PRE-RULE EVIDENCE / TEST ERROR | Invalid test date, HTTP 400 | Test input error |
| PRE-10 | Corrected real monthly `getDynamics` | PRE-RULE EVIDENCE / PASS | HTTP 200, 12 points | Core path works |
| PRE-11 | Real `getRegionsDistribution` | PRE-RULE EVIDENCE / PASS | HTTP 200 | Core path works |

---

## 3. Full planned test matrix

### A. Build identity, installation and migration

| ID | Test | Acceptance condition | Status | Actual / evidence |
|---|---|---|---|---|
| A-01 | Candidate identity | Version/hash match | PASS | Candidate identity confirmed |
| A-02 | Same-folder upgrade compatibility | Existing compatible settings survive reload/upgrade | PASS | 2026-08-12 controlled same-storage worker reload: API key, Folder ID, Auto Send, Debug, policy ceilings, Manual mode, report-prefix state and auto-start prompt survived; focused A-02 1/1 PASS |
| A-03 | New installation import path | Exported settings can be imported into another unpacked installation identity | PASS | 2026-08-12 controlled distinct runtime identities A→B: API key, Folder ID, Auto Send, Debug and Wordstat ceilings restored; `imported:true`; focused A-03 1/1 PASS |
| A-04 | No runtime GitHub/job coupling | No job/repo/branch/commit/GitHub token runtime requirement | PASS | Governed Manual commands ran standalone with `run_id:null` |
| A-05 | Secret containment | Secrets never appear in result/error/debug payload | PASS | Real Debug-ON payload and normal outputs secret-free |

### B. Popup controls and immediate state persistence

| ID | Test | Acceptance condition | Status | Actual / evidence |
|---|---|---|---|---|
| B-01 | Debug toggle immediate persistence | Toggle persists without Save | FAIL (pre-rule evidence) | Debug reverted OFF without extra Save |
| B-02 | Manual Wordstat toggle immediate persistence | Same | PASS | Controlled emulation: backend false→true; fresh popup ON |
| B-03 | Auto Send toggle immediate persistence | Same | FAIL | No persistence message; backend unchanged; fresh popup OFF |
| B-04 | Any other boolean toggle in popup | Same | FAIL | Autorun/report-prefix booleans do not commit immediately |
| B-05 | Text/credential fields | Save only where intended | PASS | Folder ID unsaved edit disappears; Save persists |
| B-06 | Popup reopen state fidelity | Reopen reflects storage/runtime truth | PASS | Controlled emulation PASS |

### C. Reference UI plaques/toasts

| ID | Test | Acceptance condition | Status | Actual / evidence |
|---|---|---|---|---|
| C-01 | Supported command Copy decoration | Supported local Copy visibly decorated | PASS | Owner confirmed all command Copies highlighted; request path executed |
| C-02 | Request-start plaque | Reference-style `отправляю <method>` | FAIL (installed candidate; post-patch emulation PASS) | Installed-base fail; plaque-patch emulation green; live patched rerun pending |
| C-03 | Success plaque | Reference-style `ответ получен` | NOT RUN (live; post-patch emulation PASS) | Emulation green; live patched rerun pending |
| C-04 | Error plaque | Reference-consistent error feedback | FAIL (installed candidate; post-patch emulation PASS) | Installed-base fail; plaque-patch emulation green; live patched rerun pending |
| C-05 | Non-command Copy | Native copy only, no Yandex | PASS | Governed real-Chrome `ничего` after non-command Copy |
| C-06 | Generic ChatGPT Copy response | Never API trigger | PASS | Governed real-Chrome `ничего` after generic response Copy |
| C-07 | Double-click protection | Rapid pair cannot duplicate Yandex request | PASS | Four clicks as two rapid pairs produced exactly two requests total; one per pair |
| C-08 | DOM mismatch fail-safe | Unsafe/ambiguous DOM => no request | PASS | Controlled emulation: ambiguous/orphan/mismatched paths fail closed; 1/1 PASS |

### D. Manual command execution — live

| ID | Test | Acceptance condition | Status | Actual / evidence |
|---|---|---|---|---|
| D-01 | Unsupported method | Error auto-delivered; zero request | PASS (pre-rule evidence) | `UNSUPPORTED_METHOD`, false |
| D-02 | `getRegionsTree` | One request, HTTP 200, same conversation | PASS | request `5afde028-66f9-488f-bbdf-e30649432d24` |
| D-03 | `getTop` standard | HTTP 200 | PASS (pre-rule evidence) | PASS |
| D-04 | `getDynamics` valid | HTTP 200 | PASS (pre-rule evidence) | PASS |
| D-05 | `getRegionsDistribution` | HTTP 200 | PASS (pre-rule evidence) | PASS |
| D-06 | filter propagation | Exact filters/results | PASS | Governed live PASS |
| D-07 | `numPhrases=1` | Exactly one result | PASS | Governed live PASS |
| D-08 | validation failure | local false/no request | PASS | `INVALID_NUM_PHRASES`, false |
| D-09 | HTTP 4xx | One request, no retry | PASS | HTTP 400, true, retry false |
| D-10 | exactly-once result delivery | One user turn/result | PASS | request `5bebe196-2a48-47c2-b52d-c447a9406338` |
| D-11 | Recovery after post-request delivery failure | Fresh command recovers without replay | PASS | Two subsequent free commands delivered normally; failed request not replayed |

### E. Envelope semantics

| ID | Test | Acceptance condition | Status | Actual / evidence |
|---|---|---|---|---|
| E-01 | identity fields | Correct | PASS | PASS |
| E-02 | no job_id | Absent | PASS | PASS |
| E-03 | executed flag semantics | Explicitly accurate | FAIL | Successful results omit `request_executed` |
| E-04 | free-call charge semantics | free => not charged | FAIL | `getRegionsTree` reports `charged:true` |
| E-05 | paid estimate | tariff-consistent | PASS | getTop 0.02 |
| E-06 | HTTP status | preserved | PASS | 400/200 preserved |
| E-07 | automatic retry | accurate/no blind retry | PASS | PASS |
| E-08 | secret redaction | no credentials | PASS | PASS |

### F. Debug / always-on error delivery

| ID | Test | Acceptance condition | Status | Actual / evidence |
|---|---|---|---|---|
| F-01 | Debug OFF error-to-chat | Auto-delivered | PASS | Governed live |
| F-02 | Debug ON error-to-chat | Auto-delivered | PASS | Governed real Chrome |
| F-03 | Debug ON diagnostics | Extra redacted trace | PASS | `debug_logs` present |
| F-04 | Debug OFF concise | no extra trace | PASS | PASS |
| F-05 | Debug secrecy | no secrets | PASS | PASS |

### G. Autorun lifecycle

| ID | Test | Acceptance condition | Status | Actual / evidence |
|---|---|---|---|---|
| G-01 | Start Autorun | creates RUN/waiting | FAIL | Live popup stayed not started; backend start emulation separately works |
| G-02 | pickup | auto capture | BLOCKED | G-01 |
| G-03 | result delivery | exactly once | BLOCKED | G-01 |
| G-04 | pause | deterministic | BLOCKED | G-01 |
| G-05 | resume | same RUN/counters | BLOCKED | G-01 |
| G-06 | stop | clean stop | BLOCKED | G-01 |
| G-07 | recoverable error continuation | report + return waiting | PASS | Controlled emulation |
| G-08 | duplicate/other tab ownership | other tab cannot steal | PASS | Five non-owner tab cases 5/5 PASS |
| G-09 | reload recovery | safe waiting state restored | PASS | Same RUN/watch/baseline restored; no fetch; 1/1 PASS |

### H. RUN accounting / policy

| ID | Test | Acceptance condition | Status | Actual / evidence |
|---|---|---|---|---|
| H-01 | counters | correct once-per-op | PASS | Controlled |
| H-02 | request limit | block before request | PASS | Controlled |
| H-03 | cost limit | block before request | PASS | Controlled |
| H-04 | paused Manual shares budget | cannot bypass | PASS | Controlled |
| H-05 | standalone Manual | no invented budget | PASS | Governed live |

### I. Unknown outcome / recovery

| ID | Test | Acceptance condition | Status | Actual / evidence |
|---|---|---|---|---|
| I-01 | Worker loss before irreversible boundary | Retry/execute only if definitely unsent | PASS | Corrected controlled test: waiting state restored with zero fetch; first post-restart command exactly one fetch; I-02/I-03 fence ambiguous states. Earlier bad harness assertion was TEST ERROR and superseded. |
| I-02 | after irreversible boundary | UNKNOWN/no blind retry | PASS | Controlled fault injection |
| I-03 | unknown-outcome command fence | identical command cannot auto reissue | PASS | Controlled 1/1; fetch count unchanged |
| I-04 | durable error outbox | survives/reports once | PASS | Controlled |
| I-05 | post-Send reconciliation | no blind second Send | PASS | Controlled |

### J. Export / Import and backup integrity

| ID | Test | Acceptance condition | Status | Actual / evidence |
|---|---|---|---|---|
| J-01 | export schema | metadata/settings/contains_secrets | PASS | Controlled |
| J-02 | SHA-256 validation | untouched accepted | PASS | Controlled |
| J-03 | tamper rejection | modified rejected | PASS | Controlled |
| J-04 | Cross-install restore | Credentials/settings restored in another unpacked identity | TEST ERROR | 2026-08-12 first focused J-04 procedure used the wrong storage key names for report-prefix/auto-start state (`ymb_report_prefixes`/`ymb_auto_start_prompts` instead of runtime keys). Import itself returned `imported:true` and credential/global assertions passed, but the test then dereferenced a non-existent wrong-key object and stopped with `TypeError`. This is a test-procedure error, not product evidence; corrected rerun required. |
| J-05 | Active RUN preservation | import never replaces active RUN | PASS | Controlled |
| J-06 | Secret containment | backup secrets never enter ChatGPT/GitHub logs | NOT RUN | |

### K. Final closure

| ID | Test | Acceptance condition | Status | Actual / evidence |
|---|---|---|---|---|
| K-01 | All four Wordstat methods | patched candidate live evidence | NOT RUN | Pre-patch evidence only |
| K-02 | Manual reference UX | full manual UX | NOT RUN | plaque-patch emulation green; live pending |
| K-03 | Autorun reference UX | full autorun UX | BLOCKED | G-01 |
| K-04 | Debug contract | post-patch live OFF/ON | NOT RUN | current candidate evidence exists; final rerun pending |
| K-05 | Toggle persistence | all toggles immediate | NOT RUN | current B failures |
| K-06 | cost/accounting | free/paid correct | NOT RUN | E-04 fail |
| K-07 | static/full regression | full suite/package identity | PASS (DEF-01 patch checkpoint) | 313/313 source + 313/313 ZIP; byte identity/syntax/JSON green |
| K-08 | final real Chrome | no mandatory unresolved | NOT RUN | |

---

## 4. Current defect register

| Defect | Source tests | Current observation |
|---|---|---|
| DEF-01 Reference plaque/toast parity broken | PRE-02, C-02, C-04 | **PATCHED UNDER OWNER INTERRUPTION; POST-PATCH EMULATION PASS / LIVE RERUN PENDING.** |
| DEF-02 Toggle persistence architecture wrong | PRE-03, B-01, B-03, B-04 | Debug/Auto Send/Autorun/report-prefix booleans do not persist immediately |
| DEF-03 Autorun cannot start | PRE-04, G-01 | live popup cannot create RUN; backend core start works in emulation |
| DEF-04 Free-call charge semantic wrong | PRE-07, E-04 | free getRegionsTree reports charged true |
| DEF-05 Successful-result executed flag missing | D-10, D-02, E-03 | success envelopes omit request_executed |
| DEF-06 Manual post-request delivery readiness failure | C-07 incident, D-11 | one HTTP200 request later failed delivery readiness; subsequent commands recover; deterministic already-executed recovery still required |

Owner explicitly interrupted the campaign on 2026-08-12 and ordered immediate DEF-01 plaque-only patch. This is the rule-4 exception for DEF-01 only.

---

## 5. Plan amendments

- 2026-08-12 — Add D-11 after C-07 delivery incident; use free getRegionsTree and require recovery without replay.
- 2026-08-12 — Owner interrupted campaign for immediate DEF-01 plaque-only repair; existing C-02/C-03/C-04/K-07 cover it.

---

## 6. Patch derivation gate

When campaign is complete: freeze FAIL/BLOCKED; derive mapped patch requirements; implement only documented scope; add regressions; build new candidate; rerun emulator/static; rerun mandatory live gates; record post-patch results; only then Phase 1 LIVE PASS / Phase 2 unlock.