# PHASE 1 — 0.1.1 LIVE TEST PLAN AND RESULT LEDGER

Date created: 2026-08-12
Candidate: `yandex-marketing-bridge-0.1.1-phase1-repair-candidate.zip`
Candidate SHA-256: `311353e2671052b7170e12db3e1318dfed4f59ccf945c7eda6ec59152ee3abfb`
Status: **ACTIVE TEST CAMPAIGN — PATCHING FORBIDDEN UNTIL LEDGER REVIEW**

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
- **Popup/UI/toggle/state-machine behavior** is tested in controlled browser/emulation by the assistant. The owner is not used as a manual click-through test runner for those checks.
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
| PRE-03 | Debug toggle persistence | PRE-RULE EVIDENCE / FAIL | Debug returned OFF after popup lifecycle unless an extra save action was used | Toggle-type settings must apply and persist immediately; no extra Save required |
| PRE-04 | Autorun start from popup | PRE-RULE EVIDENCE / FAIL | After attempted start, UI still showed `Run текущего диалога: Не запущен`, iteration 0 and counters 0/0/0 | One start action must create/start the current-conversation RUN |
| PRE-05 | `getRegionsTree` with missing credentials | PRE-RULE EVIDENCE | Returned `SKIPPED / NO_CREDENTIALS`, `request_executed:false` | No network request without credentials |
| PRE-06 | Real `getRegionsTree` | PRE-RULE EVIDENCE / PASS for request path | `HTTP 200`, `status:OK`, region tree returned | Real free Wordstat command path works |
| PRE-07 | Free-call charge semantics | PRE-RULE EVIDENCE / FAIL | `estimated_rub:0` with `charged:true` | A non-billable method must not report itself as charged |
| PRE-08 | Real `getTop` — phrase `печать велеса`, Russia, all devices, 100 | PRE-RULE EVIDENCE / PASS | `HTTP 200`, `status:OK`, results + associations returned | Core `getTop` request path works |
| PRE-09 | First monthly `getDynamics` attempt | PRE-RULE EVIDENCE / TEST ERROR | Yandex returned HTTP 400 because test used `toDate` on the first, not last, day of month | Test input error, not extension defect; no automatic retry occurred |
| PRE-10 | Corrected real monthly `getDynamics` | PRE-RULE EVIDENCE / PASS | `HTTP 200`, 12 monthly points returned | Core `getDynamics` request path works |
| PRE-11 | Real `getRegionsDistribution` | PRE-RULE EVIDENCE / PASS | `HTTP 200`, regional distribution returned | Core `getRegionsDistribution` request path works |

No further live command is to be issued until this ledger and the governing rule are committed to GitHub.

---

## 3. Full planned test matrix

### A. Build identity, installation and migration

| ID | Test | Acceptance condition | Status | Actual / evidence |
|---|---|---|---|---|
| A-01 | Candidate identity | Popup/runtime report version `0.1.1`; candidate hash matches governed artifact | NOT RUN | |
| A-02 | Same-folder upgrade compatibility | Existing compatible settings survive reload/upgrade | NOT RUN | |
| A-03 | New installation import path | Exported settings can be imported into another unpacked installation identity | NOT RUN | |
| A-04 | No runtime GitHub/job coupling | No `job_id`, repo, branch, commit or GitHub token required to execute Wordstat | NOT RUN | |
| A-05 | Secret containment | API key/folder secret never appears in ChatGPT result/error/debug payload | NOT RUN | |

### B. Popup controls and immediate state persistence — emulator/controlled browser

All ON/OFF controls in this class must commit immediately when switched. A separate Save click is not an acceptance requirement for a toggle.

| ID | Test | Acceptance condition | Status | Actual / evidence |
|---|---|---|---|---|
| B-01 | Debug toggle immediate persistence | Toggle → close popup → reopen; state preserved without Save | FAIL (pre-rule evidence) | Debug reverted OFF without extra Save |
| B-02 | Manual Wordstat toggle immediate persistence | Same immediate-persistence rule | NOT RUN | |
| B-03 | Auto Send toggle immediate persistence | Same immediate-persistence rule | NOT RUN | |
| B-04 | Any other boolean toggle in popup | Every toggle of same UI class persists immediately | NOT RUN | |
| B-05 | Text/credential fields | Explicit Save is required only where intentionally designed for text/credential commit | NOT RUN | |
| B-06 | Popup reopen state fidelity | Reopening popup reflects runtime/storage truth, not stale defaults | NOT RUN | |

### C. Reference UI plaques/toasts — emulator plus live confirmation where applicable

| ID | Test | Acceptance condition | Status | Actual / evidence |
|---|---|---|---|---|
| C-01 | Supported command Copy decoration | Supported `WORDSTAT_API_V1` local Copy is visibly decorated as the API action boundary | NOT RUN | |
| C-02 | Request-start plaque | Real operation shows reference-style `отправляю <method>` feedback | FAIL (pre-rule evidence for generic replacement UI) | Existing generic YMB notification is not acceptable |
| C-03 | Success plaque | Successful response shows reference-style `ответ получен` | NOT RUN | |
| C-04 | Error plaque | Error shows explicit reference-consistent error feedback, not a green generic success-style plaque | FAIL (pre-rule evidence) | Generic green YMB plaque observed |
| C-05 | Non-command Copy | Copying non-Wordstat content remains native copy only and never triggers Yandex | NOT RUN | |
| C-06 | Generic ChatGPT Copy response | Must never be treated as API authorization/trigger | NOT RUN | |
| C-07 | Double-click protection | Repeated/double local Copy cannot produce duplicate Yandex requests | NOT RUN | |
| C-08 | DOM mismatch fail-safe | If expected ChatGPT command DOM cannot be safely identified, no Yandex request is issued | NOT RUN | |

### D. Manual command execution — live ChatGPT command gates

| ID | Test | Acceptance condition | Status | Actual / evidence |
|---|---|---|---|---|
| D-01 | Unsupported method | Error auto-delivered; zero Yandex request | PASS (pre-rule evidence) | `UNSUPPORTED_METHOD`, `request_executed:false` |
| D-02 | `getRegionsTree` | Exactly one request; HTTP 200; result returns to same conversation | PASS (pre-rule evidence) | HTTP 200 |
| D-03 | `getTop` standard | Exactly one request; HTTP 200; result + associations | PASS (pre-rule evidence) | HTTP 200 |
| D-04 | `getDynamics` valid monthly range | Exactly one request; HTTP 200; expected monthly series | PASS (pre-rule evidence) | HTTP 200, 12 points |
| D-05 | `getRegionsDistribution` | Exactly one request; HTTP 200; regional distribution | PASS (pre-rule evidence) | HTTP 200 |
| D-06 | `getTop` filter propagation: Moscow + phone + 10 results | Envelope echoes exact filters; result respects request; one request only | PASS | 2026-08-12 live: `HTTP 200`, `status:OK`, command echoed `phrase:"оберег в машину"`, `numPhrases:10`, `regions:["213"]`, `devices:["DEVICE_PHONE"]`; exactly 10 results returned; request_id `09cb5b8a-94ea-4e2b-b8fa-6b90e081ee46` |
| D-07 | `getTop` boundary `numPhrases=1` | One result max, no parameter rewriting | PASS | 2026-08-12 live: `HTTP 200`, `status:OK`; command echoed `numPhrases:1`, `regions:["213"]`, `devices:["DEVICE_PHONE"]`; exactly one result returned; request_id `fda97b60-571e-4e82-a344-c388c077a898` |
| D-08 | Validation failure before network | Invalid local parameter yields error and `request_executed:false` | NOT RUN | |
| D-09 | Yandex HTTP 4xx path | One request, error returned to ChatGPT, no automatic retry | PASS only for pre-rule malformed Dynamics request; governed rerun still NOT RUN | Need controlled valid negative case |
| D-10 | Result delivery exactly once | Exactly one user-turn/result per successful command | NOT RUN | |

### E. Result/error envelope semantics

| ID | Test | Acceptance condition | Status | Actual / evidence |
|---|---|---|---|---|
| E-01 | Required identity fields | `bridge`, `version`, `service`, `operation`, `request_id` correct | NOT RUN | |
| E-02 | No obsolete `job_id` | `job_id` absent from runtime result/error contracts | NOT RUN | |
| E-03 | Executed flag semantics | `request_executed` accurately distinguishes local skip vs sent request | NOT RUN | |
| E-04 | Free-call charge semantics | `getRegionsTree`: `estimated_rub:0` and not reported as charged | FAIL (pre-rule evidence) | `charged:true` observed |
| E-05 | Paid estimate semantics | Paid method estimate matches freshly checked tariff for exact run | NOT RUN | |
| E-06 | HTTP status propagation | Yandex HTTP status preserved accurately | NOT RUN | |
| E-07 | Automatic retry field | Errors/unknown outcomes never claim an automatic retry that did not occur | NOT RUN | |
| E-08 | Secret redaction | No credentials/Authorization in normal or debug envelope | NOT RUN | |

### F. Debug and always-on error delivery

| ID | Test | Acceptance condition | Status | Actual / evidence |
|---|---|---|---|---|
| F-01 | Debug OFF error-to-chat | Error automatically arrives without operator log-copy step | PASS (pre-rule evidence for unsupported method) | |
| F-02 | Debug ON error-to-chat | Same error delivery still happens | NOT RUN | |
| F-03 | Debug ON additional diagnostics | Adds useful redacted diagnostics/state trace | NOT RUN | |
| F-04 | Debug OFF no extra diagnostics | Normal envelope remains concise while still delivering the error | NOT RUN | |
| F-05 | Debug secrecy | API key/token/Authorization never exposed | NOT RUN | |

### G. Autorun lifecycle — emulator for UI/state, live ChatGPT for command pickup

| ID | Test | Acceptance condition | Status | Actual / evidence |
|---|---|---|---|---|
| G-01 | Start Autorun | One start action creates current-conversation RUN and enters waiting state | FAIL (pre-rule evidence) | UI remained `Не запущен`, iteration 0 |
| G-02 | Autorun block pickup | With RUN active, next eligible command is captured without local Copy | BLOCKED | Blocked by G-01 |
| G-03 | Autorun result delivery | Result automatically returns to same conversation exactly once | BLOCKED | Blocked by G-01 |
| G-04 | Pause | Active RUN can be paused deterministically | BLOCKED | Blocked by G-01 |
| G-05 | Resume | Paused RUN resumes without new RUN identity or counter reset | BLOCKED | Blocked by G-01 |
| G-06 | Stop | Stop terminates RUN cleanly and prevents further auto-capture | BLOCKED | Blocked by G-01 |
| G-07 | Recoverable error continuation | Recoverable error reports to ChatGPT and RUN returns to waiting when safe | BLOCKED | Blocked by G-01 |
| G-08 | Duplicate/other tab ownership | Another conversation/tab cannot steal or duplicate execution ownership | NOT RUN | |
| G-09 | Reload recovery | Reload during safe waiting state restores controlled RUN state | NOT RUN | |

### H. RUN accounting and policy ceilings

| ID | Test | Acceptance condition | Status | Actual / evidence |
|---|---|---|---|---|
| H-01 | Attempt/executed/skipped counters | Counters update once per operation with correct classification | BLOCKED | Requires working Autorun RUN |
| H-02 | Request limit enforcement | Over-limit command is skipped before Yandex request | BLOCKED | Requires working Autorun RUN |
| H-03 | Cost limit enforcement | Over-cost command is skipped before Yandex request | BLOCKED | Requires working Autorun RUN |
| H-04 | Manual while RUN paused shares budget | Manual Copy cannot bypass paused RUN request/cost ceiling | BLOCKED | Requires working Autorun RUN |
| H-05 | Standalone Manual behavior | No invented job budget is required when no RUN exists | NOT RUN | |

### I. Unknown outcome, recovery and duplicate prevention — emulator/fault injection only unless owner explicitly authorizes risk

| ID | Test | Acceptance condition | Status | Actual / evidence |
|---|---|---|---|---|
| I-01 | Worker loss before irreversible request boundary | Safe recovery may retry only if request definitely never left | NOT RUN | |
| I-02 | Worker loss after irreversible boundary | `REQUEST_OUTCOME_UNKNOWN`, `request_executed:UNKNOWN`, no blind retry | NOT RUN | |
| I-03 | Unknown-outcome command fence | Identical command cannot be automatically reissued until reconciliation | NOT RUN | |
| I-04 | Durable error outbox | Staged/committed error survives reload and is delivered once | NOT RUN | |
| I-05 | Post-Send reconciliation | After committed Send boundary, recovery never clicks Send again blindly | NOT RUN | |

### J. Export / Import and backup integrity — emulator/controlled browser

| ID | Test | Acceptance condition | Status | Actual / evidence |
|---|---|---|---|---|
| J-01 | Export schema | Backup contains required metadata + settings + `contains_secrets:true` | NOT RUN | |
| J-02 | SHA-256 validation | Untouched backup accepted | NOT RUN | |
| J-03 | Tamper rejection | Modified backup rejected | NOT RUN | |
| J-04 | Cross-install restore | Credentials/settings restored in another unpacked identity | NOT RUN | |
| J-05 | Active RUN preservation | Import never replaces active execution state | NOT RUN | |
| J-06 | Secret containment | Backup secret values never enter ChatGPT/GitHub logs | NOT RUN | |

### K. Final regression/live closure

| ID | Test | Acceptance condition | Status | Actual / evidence |
|---|---|---|---|---|
| K-01 | All four Wordstat methods | `getTop`, `getDynamics`, `getRegionsDistribution`, `getRegionsTree` all have passing live evidence on patched candidate | NOT RUN | Current evidence belongs to pre-patch 0.1.1 candidate |
| K-02 | Manual reference UX | Copy decoration + start plaque + response plaque + one result + no duplicate request | NOT RUN | |
| K-03 | Autorun reference UX | Start + auto-capture + one request + one delivery + pause/resume/stop | BLOCKED | G-01 |
| K-04 | Debug contract | OFF and ON both auto-deliver errors; ON adds redacted detail only | NOT RUN | |
| K-05 | Toggle persistence | Every toggle-type setting persists immediately without Save | NOT RUN | |
| K-06 | Cost/accounting semantics | Free and paid methods report cost/charged state correctly | NOT RUN | |
| K-07 | Static/full regression after patch | Full source + packaged suite green; source/package identity checked | NOT RUN | Only after patch |
| K-08 | Final real-Chrome/current-ChatGPT acceptance | No unresolved mandatory FAIL/BLOCKED item remains | NOT RUN | |

---

## 4. Current defect register

This register is derived from observed FAILs and is not yet the patch specification.

| Defect | Source tests | Current observation |
|---|---|---|
| DEF-01 Reference plaque/toast parity broken | PRE-02, C-02, C-04 | Generic green `YMB:` notification replaces required reference-style feedback |
| DEF-02 Toggle persistence architecture wrong | PRE-03, B-01 | Debug toggle requires extra Save / does not persist immediately |
| DEF-03 Autorun cannot start | PRE-04, G-01 | No RUN created; iteration/counters remain zero |
| DEF-04 Free-call charge semantic wrong | PRE-07, E-04 | `getRegionsTree` returns `estimated_rub:0` with `charged:true` |

No patch is to be derived until the remaining planned tests are executed or explicitly marked blocked/waived by the owner.

---

## 5. Plan amendments

Append newly discovered test requirements here **before executing them**.

- None yet after creation of this governed ledger.

---

## 6. Patch derivation gate

When the campaign is complete:

1. Freeze the final FAIL/BLOCKED list.
2. Convert each confirmed defect into an explicit patch requirement mapped to test IDs.
3. Implement only against those documented requirements plus necessary structural fixes.
4. Add/adjust regression tests for each confirmed defect.
5. Build a new candidate.
6. Rerun affected emulator/static tests first.
7. Rerun mandatory real ChatGPT command gates on the new candidate.
8. Record all post-patch results in this document.
9. Only after no mandatory FAIL/BLOCKED remains may Phase 1 be marked LIVE PASS and Phase 2 Search be unlocked.