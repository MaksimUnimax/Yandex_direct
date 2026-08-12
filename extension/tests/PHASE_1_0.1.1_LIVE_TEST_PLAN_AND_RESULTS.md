# PHASE 1 — 0.1.1 LIVE TEST PLAN AND RESULT LEDGER

Date created: 2026-08-12
Candidate: `yandex-marketing-bridge-0.1.1-phase1-repair-candidate.zip`
Candidate SHA-256: `311353e2671052b7170e12db3e1318dfed4f59ccf945c7eda6ec59152ee3abfb`
Owner-interrupted DEF-01 patch candidate: `yandex-marketing-bridge-0.1.1-phase1-plaque-parity-candidate.zip`
Patch candidate SHA-256: `c0e3c36eaac1ebfa81ee44ca8cc376282b9aed601cd07cc596a6c235cfffb976`
Status: **PRE-PATCH TEST CAMPAIGN COMPLETE — FAIL/BLOCKED SET FROZEN; PATCH REQUIREMENTS DERIVED**

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
| A-01 | Candidate identity | Popup/runtime report version `0.1.1`; candidate hash matches governed artifact | PASS | Controlled candidate check: manifest/package/runtime version `0.1.1`; SHA-256 of installed candidate archive rechecked as `311353e2671052b7170e12db3e1318dfed4f59ccf945c7eda6ec59152ee3abfb` |
| A-02 | Same-folder upgrade compatibility | Existing compatible settings survive reload/upgrade | PASS | 2026-08-12 controlled same-storage/same-folder worker reload on plaque-patch candidate: API key, Folder ID, Auto Send OFF, Debug ON, custom Wordstat request/cost ceilings, Manual mode, report-prefix state and auto-start prompt all survived into a fresh worker context backed by the same persisted storage. `publicSettingsState` reproduced Folder ID, Auto Send, Debug and policy limit values. Focused A-02 test passed 1/1. |
| A-03 | New installation import path | Exported settings can be imported into another unpacked installation identity | PASS | 2026-08-12 controlled cross-install emulation on plaque-patch candidate: settings were exported from runtime identity `phase1-extension-A` and imported into a distinct fresh runtime identity `phase1-extension-B`. API key, Folder ID, Auto Send OFF, Debug ON and custom Wordstat request/cost ceilings were restored successfully; import returned `imported:true`. Focused A-03 test passed 1/1. |
| A-04 | No runtime GitHub/job coupling | No `job_id`, repo, branch, commit or GitHub token required to execute Wordstat | PASS | Multiple governed standalone Manual commands executed successfully with `run_id:null` and without `job_id`/repo/branch/commit/GitHub runtime fields or gates |
| A-05 | Secret containment | API key/folder secret never appears in ChatGPT result/error/debug payload | PASS | 2026-08-12 governed real-Chrome Debug-ON error arrived with full `debug_logs`; inspection found no API key, OAuth token, `Authorization` header/value` or credential-storage secret in the delivered payload. Normal governed outputs were also secret-free |

### B. Popup controls and immediate state persistence — emulator/controlled browser

All ON/OFF controls in this class must commit immediately when switched. A separate Save click is not an acceptance requirement for a toggle.

| ID | Test | Acceptance condition | Status | Actual / evidence |
|---|---|---|---|---|
| B-01 | Debug toggle immediate persistence | Toggle → close popup → reopen; state preserved without Save | FAIL (pre-rule evidence) | Debug reverted OFF without extra Save |
| B-02 | Manual Wordstat toggle immediate persistence | Same immediate-persistence rule | PASS | 2026-08-12 controlled popup emulation: toggling Manual emitted `WS_SET_MANUAL_MODE`; shared backend changed `manual_mode:false→true`; fresh popup instance reopened with Manual ON without Save |
| B-03 | Auto Send toggle immediate persistence | Same immediate-persistence rule | FAIL | 2026-08-12 controlled popup emulation: toggling Auto Send emitted no settings message; backend remained `auto_send:false`; fresh popup reopened OFF despite visible toggle having been changed ON |
| B-04 | Any other boolean toggle in popup | Every toggle of same UI class persists immediately | FAIL | Controlled popup emulation: `wordstatAutorunEnabled` emitted no persistence message and reopened OFF; `reportPrefixEnabled` changed locally but backend was unchanged and fresh popup reopened to stored value. Same defect class as Debug/Auto Send |
| B-05 | Text/credential fields | Explicit Save is required only where intentionally designed for text/credential commit | PASS | Controlled popup emulation using Folder ID: unsaved edit disappeared on reopen; edit followed by Save persisted and appeared in a fresh popup instance |
| B-06 | Popup reopen state fidelity | Reopening popup reflects runtime/storage truth, not stale defaults | PASS | Controlled popup emulation: fresh popup rendered persisted backend truth; Manual ON survived because backend changed, while unsaved boolean edits reverted to stored values |

### C. Reference UI plaques/toasts — emulator plus final live closure where applicable

| ID | Test | Acceptance condition | Status | Actual / evidence |
|---|---|---|---|---|
| C-01 | Supported command Copy decoration | Supported `WORDSTAT_API_V1` local Copy is visibly decorated as the API action boundary | PASS | 2026-08-12 governed real Chrome: owner explicitly confirmed that supported command Copy controls are visibly highlighted/decorated (`Все выделено`); C-01 `getRegionsTree` block was therefore recognized as the API action boundary. The same action executed successfully as request_id `85085824-b4e9-4584-ba52-cb4610e6ec13`. |
| C-02 | Request-start plaque | Real operation shows reference-style `отправляю <method>` feedback | FAIL (installed candidate; post-patch emulation PASS) | Pre-rule live installed-base evidence remains FAIL. Owner-interrupted DEF-01 patch preserves the exact reference renderer and controlled emulation confirms the patched request-start plaque. Final K-02 real-Chrome closure remains pending on the consolidated patched candidate. |
| C-03 | Success plaque | Successful response shows reference-style `ответ получен` | PASS (post-patch emulation; final K-02 live pending) | Owner explicitly required plaque wording/appearance to be validated in emulation rather than repetitive manual UI clicking. Controlled DEF-01 patch emulation confirms the reference success plaque; final consolidated-candidate live UX is deferred to K-02. |
| C-04 | Error plaque | Error shows explicit reference-consistent error feedback, not a green generic success-style plaque | FAIL (installed candidate; post-patch emulation PASS) | Pre-rule installed-base evidence remains FAIL. Owner-interrupted DEF-01 patch removes invented user-facing YMB/Yandex Marketing Bridge toast labels from Wordstat Phase 1 paths and renders error delivery with reference error tone. Final K-02/K-04 real-Chrome closure remains pending on the consolidated candidate. |
| C-05 | Non-command Copy | Copying non-Wordstat content remains native copy only and never triggers Yandex | PASS | 2026-08-12 governed real-Chrome: owner clicked local Copy once on a non-command text block `YMB_C05_NON_COMMAND_COPY_TEST`, waited about five seconds, and reported `ничего`; no `WORDSTAT_RESULT_V1`, `YMB_ERROR_V1` or other Wordstat/Yandex execution output appeared. |
| C-06 | Generic ChatGPT Copy response | Must never be treated as API authorization/trigger | PASS | 2026-08-12 governed real-Chrome: owner clicked the generic ChatGPT `Copy`/`Копировать ответ` control for the entire assistant response rather than the local command-block Copy, waited about five seconds, and reported `ничего`; no Wordstat/Yandex result, error or request output appeared. |
| C-07 | Double-click protection | Repeated/double local Copy cannot produce duplicate Yandex requests | PASS | 2026-08-12 governed real Chrome: owner performed four Copy clicks as two rapid double-click pairs separated by a pause. Debug evidence shows exactly two Yandex requests total: request `504d27be-fe8a-4a0e-bb0a-8f228c5c9d7b` for the first pair and request `1e7bbdfc-f67e-4079-868f-95ef58db574d` for the second pair. Therefore each rapid pair collapsed to one request; no second request was produced within either pair. The second pair separately exposed a delivery-readiness failure after the request completed. |
| C-08 | DOM mismatch fail-safe | If expected ChatGPT command DOM cannot be safely identified, no Yandex request is issued | PASS | 2026-08-12 controlled content emulation on the plaque-patch candidate: ambiguous local Copy candidates resolve to `null`; orphan Copy has no binding; conversation DOM/identity mismatch returns `CONVERSATION_NOT_CONFIRMED`; focused test `content copy locality ranking, manual root ordering, cleanup and MutationObserver branches execute` passed 1/1 with no executable Yandex transport. |

### D. Manual command execution — live ChatGPT command gates

| ID | Test | Acceptance condition | Status | Actual / evidence |
|---|---|---|---|---|
| D-01 | Unsupported method | Error auto-delivered; zero Yandex request | PASS (pre-rule evidence) | `UNSUPPORTED_METHOD`, `request_executed:false` |
| D-02 | `getRegionsTree` | Exactly one request; HTTP 200; result returns to same conversation | PASS | 2026-08-12 governed live: `getRegionsTree` returned once to this conversation with `HTTP 200`, `status:OK`, region tree payload and request_id `5afde028-66f9-488f-bbdf-e30649432d24` |
| D-03 | `getTop` standard | Exactly one request; HTTP 200; result + associations | PASS (pre-rule evidence) | HTTP 200 |
| D-04 | `getDynamics` valid monthly range | Exactly one request; HTTP 200; expected monthly series | PASS (pre-rule evidence) | HTTP 200, 12 points |
| D-05 | `getRegionsDistribution` | Exactly one request; HTTP 200; regional distribution | PASS (pre-rule evidence) | HTTP 200 |
| D-06 | `getTop` filter propagation: Moscow + phone + 10 results | Envelope echoes exact filters; result respects request; one request only | PASS | 2026-08-12 live: `HTTP 200`, `status:OK`, command echoed `phrase:"оберег в машину"`, `numPhrases:10`, `regions:["213"]`, `devices:["DEVICE_PHONE"]`; exactly 10 results returned; request_id `09cb5b8a-94ea-4e2b-b8fa-6b90e081ee46` |
| D-07 | `getTop` boundary `numPhrases=1` | One result max, no parameter rewriting | PASS | 2026-08-12 live: `HTTP 200`, `status:OK`; command echoed `numPhrases:1`, `regions:["213"]`, `devices:["DEVICE_PHONE"]`; exactly one result returned; request_id `fda97b60-571e-4e82-a344-c388c077a898` |
| D-08 | Validation failure before network | Invalid local parameter yields error and `request_executed:false` | PASS | 2026-08-12 live: `numPhrases:0` rejected locally with `YMB_ERROR_V1`, `stage:MANUAL_COMMAND_PARSE`, `code:INVALID_NUM_PHRASES`, `request_executed:false`, `automatic_retry:false`; no Yandex request executed; timestamp `2026-08-12T11:33:30.690Z` |
| D-09 | Yandex HTTP 4xx path | One request, error returned to ChatGPT, no automatic retry | PASS | 2026-08-12 governed live negative test: intentionally server-invalid monthly `getDynamics` passed local parsing and produced exactly one Yandex response `HTTP 400`; result returned to ChatGPT with `status:ERROR`, `request_executed:true`, `automatic_retry:false`; Yandex error `InvalidArgument: The to field value should be the last day of the month`; request_id `b6237a6d-f933-4a2f-9929-eda537a8a409` |
| D-10 | Result delivery exactly once | Exactly one user-turn/result per successful command | PASS | 2026-08-12 governed live: one `getTop` command produced one visible `WORDSTAT_RESULT_V1` user-turn with request_id `5bebe196-2a48-47c2-b52d-c447a9406338`; no duplicate user-turn/result with that request_id observed |
| D-11 | Recovery after post-request delivery failure | After `DELIVERY_SEND_TARGET_NOT_READY_BEFORE_COMMIT` on a completed request, a fresh subsequent Manual command must still execute and deliver normally without replaying the failed request | PASS | Governed real-Chrome recovery confirmed twice after failed-delivery request `1e7bbdfc-f67e-4079-868f-95ef58db574d`: first fresh `getRegionsTree` returned `status:OK`, `HTTP 200`, request_id `644570e1-816b-441f-906d-932c29fec7d9`; second fresh confirmation returned `status:OK`, `HTTP 200`, `elapsed_ms:475`, request_id `8f6ff02d-93ea-4b1d-b804-2d1879965e63`, `run_id:null`. No replay/result for the failed request appeared in the conversation. Existing free-call `charged:true` defect remains separately tracked by E-04/DEF-04. |

### E. Result/error envelope semantics
| ID | Test | Acceptance condition | Status | Actual / evidence |
|---|---|---|---|---|
| E-01 | Required identity fields | `bridge`, `version`, `service`, `operation`, `request_id` correct | PASS | D-10 result reports `yandex-marketing-bridge`, `0.1.1`, `wordstat`, `getTop`, unique request_id `5bebe196-2a48-47c2-b52d-c447a9406338` |
| E-02 | No obsolete `job_id` | `job_id` absent from runtime result/error contracts | PASS | Governed successful and error envelopes contain no `job_id` field |
| E-03 | Executed flag semantics | `request_executed` accurately distinguishes local skip vs sent request | FAIL | Local validation D-08 correctly reports `false` and HTTP-4xx D-09 reports `true`, but successful executed D-10 and governed successful `getRegionsTree` D-02 omit `request_executed` entirely; successful sent requests are therefore not explicitly distinguishable by this field |
| E-04 | Free-call charge semantics | `getRegionsTree`: `estimated_rub:0` and not reported as charged | FAIL | 2026-08-12 governed live confirmation: successful free `getRegionsTree` returned `HTTP 200`, `estimated_rub:0` but incorrectly `charged:true`; request_id `5afde028-66f9-488f-bbdf-e30649432d24` |
| E-05 | Paid estimate semantics | Paid method estimate matches freshly checked tariff for exact run | PASS | D-10 `getTop` reports `estimated_rub:0.02`, matching the freshly checked 20 RUB / 1000-request tariff stated immediately before execution |
| E-06 | HTTP status propagation | Yandex HTTP status preserved accurately | PASS | Governed D-09 propagated `HTTP 400`; governed D-10 and D-02 propagated `HTTP 200` |
| E-07 | Automatic retry field | Errors/unknown outcomes never claim an automatic retry that did not occur | PASS | Governed D-08/D-09/F-04 errors report `automatic_retry:false`; controlled fault injection after service-worker loss during `REQUESTING` produced `REQUEST_OUTCOME_UNKNOWN_NO_RETRY` and no Yandex replay |
| E-08 | Secret redaction | No credentials/Authorization in normal or debug envelope | PASS | Governed real-Chrome Debug-ON `YMB_ERROR_V1` contained extensive diagnostics but no API key, OAuth token, `Authorization` secret or credential-storage value; normal live result/error envelopes were also secret-free |

### F. Debug and always-on error delivery

| ID | Test | Acceptance condition | Status | Actual / evidence |
|---|---|---|---|---|
| F-01 | Debug OFF error-to-chat | Error automatically arrives without operator log-copy step | PASS | 2026-08-12 governed live: unsupported method automatically delivered `YMB_ERROR_V1` to this ChatGPT conversation with `request_executed:false`; no manual diagnostics/log copy needed; timestamp `2026-08-12T11:48:18.482Z` |
| F-02 | Debug ON error-to-chat | Same error delivery still happens | PASS | 2026-08-12 governed real-Chrome: after Debug was enabled and saved, unsupported method automatically delivered `YMB_ERROR_V1` to the same conversation; `request_executed:false`; timestamp `2026-08-12T12:04:03.276Z` |
| F-03 | Debug ON additional diagnostics | Adds useful redacted diagnostics/state trace | PASS | Same governed live Debug-ON error included a populated `debug_logs` array with service-worker/content-script request and delivery state; Debug-OFF governed control omitted it |
| F-04 | Debug OFF no extra diagnostics | Normal envelope remains concise while still delivering the error | PASS | Same governed Debug-OFF error contained normal fields only and no `debug_logs`/extra diagnostic trace while still auto-delivering to ChatGPT |
| F-05 | Debug secrecy | API key/token/Authorization never exposed | PASS | Governed real-Chrome Debug-ON payload contained no API key, OAuth token or Authorization secret; controlled emulation independently confirmed configured-key redaction |

### G. Autorun lifecycle — emulator for UI/state, live ChatGPT for command pickup

| ID | Test | Acceptance condition | Status | Actual / evidence |
|---|---|---|---|---|
| G-01 | Start Autorun | One start action creates current-conversation RUN and enters waiting state | FAIL | Pre-rule real popup remained `Не запущен`, iteration 0. Controlled worker emulation separately proves `WS_AUTO_START` backend can finalize to `waiting_command`, isolating the observed live failure to popup/policy/integration rather than the core start state transition |
| G-02 | Autorun block pickup | With RUN active, next eligible command is captured without local Copy | BLOCKED | Blocked by live G-01 |
| G-03 | Autorun result delivery | Result automatically returns to same conversation exactly once | BLOCKED | Blocked by live G-01 |
| G-04 | Pause | Active RUN can be paused deterministically | BLOCKED | Blocked by live G-01 |
| G-05 | Resume | Paused RUN resumes without new RUN identity or counter reset | BLOCKED | Blocked by live G-01 |
| G-06 | Stop | Stop terminates RUN cleanly and prevents further auto-capture | BLOCKED | Blocked by live G-01 |
| G-07 | Recoverable error continuation | Recoverable error reports to ChatGPT and RUN returns to waiting when safe | PASS | Controlled worker emulation: recoverable Autorun error queues chat error and returns RUN to `WAITING_COMMAND` without blind retry. Real current-Chrome confirmation blocked by G-01 |
| G-08 | Duplicate/other tab ownership | Another conversation/tab cannot steal or duplicate execution ownership | PASS | 2026-08-12 controlled ownership emulation on plaque-patch candidate: five duplicate-tab cases (tabs 2–6) all PASS; each `WS_CONTENT_READY` from a non-owner tab returned `owner:false`, preserved `owner_tab_id:1`, and did not take over the live delivery owner. Focused `differential ownership` suite passed 5/5. |
| G-09 | Reload recovery | Reload during safe waiting state restores controlled RUN state | PASS | 2026-08-12 controlled service-worker/content-ready reload emulation on plaque-patch candidate: a persisted `run-1` in `waiting_command` with `watch-safe-1` survived worker/content restart; `WS_CONTENT_READY` returned the same RUN id/status, same owner tab, same watch id and assistant baseline, `rebound:false`, `recovery:null`; no fetch or execution occurred. Focused G-09 test passed 1/1. |

### H. RUN accounting and policy ceilings

| ID | Test | Acceptance condition | Status | Actual / evidence |
|---|---|---|---|---|
| H-01 | Attempt/executed/skipped counters | Counters update once per operation with correct classification | PASS | Controlled RUN emulation: allowed request increments attempted/executed once; cost- or request-limited and paused-RUN blocked operations increment attempted/skipped without incrementing executed |
| H-02 | Request limit enforcement | Over-limit command is skipped before Yandex request | PASS | Controlled RUN emulation: request-limit test blocked the next request before fetch |
| H-03 | Cost limit enforcement | Over-cost command is skipped before Yandex request | PASS | Controlled RUN emulation: cost-limit test blocked paid `getTop` before fetch |
| H-04 | Manual while RUN paused shares budget | Manual Copy cannot bypass paused RUN request/cost ceiling | PASS | Controlled paused-RUN emulation: Manual paid request was blocked by shared cost ceiling; allowed variant reserved/recorded the same RUN budget |
| H-05 | Standalone Manual behavior | No invented job budget is required when no RUN exists | PASS | Governed D-06 through D-10 ran standalone with `run_id:null`; no Job ID or invented Job budget was required |

### I. Unknown outcome, recovery and duplicate prevention — emulator/fault injection only unless owner explicitly authorizes risk

| ID | Test | Acceptance condition | Status | Actual / evidence |
|---|---|---|---|---|
| I-01 | Worker loss before irreversible request boundary | Safe recovery may retry only if request definitely never left | PASS | 2026-08-12 corrected controlled fault-injection/emulation on plaque-patch candidate: worker/content restart from durable `waiting_command` state (no request worker session, no request start, no command fingerprint) restored the RUN with `recovery:null` and zero fetches; the first post-restart eligible command was then accepted and produced exactly one fetch / one executed request. This proves execution is permitted from a definitely-unsent pre-request state, while I-02/I-03 separately fence ambiguous post-boundary states from retry. Focused corrected test passed 1/1. The preceding incorrect harness assertion was recorded as TEST ERROR and superseded by this corrected rerun. |
| I-02 | Worker loss after irreversible boundary | `REQUEST_OUTCOME_UNKNOWN`, `request_executed:UNKNOWN`, no blind retry | PASS | Controlled fault injection: service-worker session loss during `REQUESTING` returns `request_outcome_unknown` / `REQUEST_OUTCOME_UNKNOWN_NO_RETRY`; Yandex is not retried and last-error execution state is `UNKNOWN` |
| I-03 | Unknown-outcome command fence | Identical command cannot be automatically reissued until reconciliation | PASS | 2026-08-12 controlled unknown-outcome fence emulation on plaque-patch candidate: RUN carried the same command fingerprint with `last_error.request_executed:"UNKNOWN"`; re-presenting the identical `WORDSTAT_API_V1` returned `REQUEST_OUTCOME_UNKNOWN_NO_RETRY`, queued the recoverable error, kept Autorun controllable, and fetch count remained unchanged. Focused test passed 1/1. |
| I-04 | Durable error outbox | Staged/committed error survives reload and is delivered once | PASS | Controlled recovery tests: error delivery follows claim → committed → confirmed; duplicate commit cannot grant a second Send; `WS_CONTENT_READY` exposes pending recovery without replaying Yandex |
| I-05 | Post-Send reconciliation | After committed Send boundary, recovery never clicks Send again blindly | PASS | Controlled content reconciliation tests execute committed/recovery branches without replay; duplicate/recovered delivery remains reconciliation-only after the irreversible Send boundary |

### J. Export / Import and backup integrity — emulator/controlled browser

| ID | Test | Acceptance condition | Status | Actual / evidence |
|---|---|---|---|---|
| J-01 | Export schema | Backup contains required metadata + settings + `contains_secrets:true` | PASS | Controlled Export test produced the governed secret-bearing settings backup schema |
| J-02 | SHA-256 validation | Untouched backup accepted | PASS | Controlled Export/Import test validates checksum and accepts untouched backup |
| J-03 | Tamper rejection | Modified backup rejected | PASS | Controlled checksum test rejects tampered backup |
| J-04 | Cross-install restore | Credentials/settings restored in another unpacked identity | PASS | 2026-08-12 corrected controlled cross-install restore on plaque-patch candidate: backup exported with `extension_id:j04-source-extension` and imported into distinct `j04-target-extension`; `imported:true`. Restored API key, Folder ID, Auto Send OFF, Debug ON, Wordstat request/cost ceilings, Manual mode, report-prefix config, auto-start prompt and conversation binding. Focused corrected J-04 test passed 1/1. The preceding wrong-key harness assertion was TEST ERROR and is superseded by this rerun. |
| J-05 | Active RUN preservation | Import never replaces active execution state | PASS | Controlled import test preserves active RUN while restoring settings |
| J-06 | Secret containment | Backup secret values never enter ChatGPT/GitHub logs | PASS | 2026-08-12 controlled export/import secrecy test with unique secret markers: backup intentionally contained API key and Folder ID, but source and target ChatGPT-facing error-delivery queues, diagnostics and content-send message traces contained neither secret value nor `Authorization`. Import completed successfully. Focused J-06 test passed 1/1. Backup storage itself remains intentionally secret-bearing by design. |

### K. Final regression/live closure

| ID | Test | Acceptance condition | Status | Actual / evidence |
|---|---|---|---|---|
| K-01 | All four Wordstat methods | `getTop`, `getDynamics`, `getRegionsDistribution`, `getRegionsTree` all have passing live evidence on patched candidate | NOT RUN | Current evidence belongs to pre-consolidated-patch candidate |
| K-02 | Manual reference UX | Copy decoration + start plaque + response plaque + one result + no duplicate request | NOT RUN | DEF-01 emulation green; final consolidated-candidate live confirmation pending |
| K-03 | Autorun reference UX | Start + auto-capture + one request + one delivery + pause/resume/stop | BLOCKED | G-01 must be repaired by consolidated patch |
| K-04 | Debug contract | OFF and ON both auto-deliver errors; ON adds redacted detail only | NOT RUN | Mandatory consolidated-candidate rerun pending |
| K-05 | Toggle persistence | Every toggle-type setting persists immediately without Save | NOT RUN | B-01/B-03/B-04 feed patch requirement PR-02 |
| K-06 | Cost/accounting semantics | Free and paid methods report cost/charged state correctly | NOT RUN | E-03/E-04 feed PR-04/PR-05 |
| K-07 | Static/full regression after patch | Full source + packaged suite green; source/package identity checked | PASS (DEF-01 patch checkpoint only) | DEF-01-only checkpoint was green; consolidated patch requires a fresh K-07 rerun |
| K-08 | Final real-Chrome/current-ChatGPT acceptance | No unresolved mandatory FAIL/BLOCKED item remains | NOT RUN | |

---

## 4. Current defect register

This register is the frozen pre-patch defect set.

| Defect | Source tests | Current observation |
|---|---|---|
| DEF-01 Reference plaque/toast parity broken | PRE-02, C-02, C-04 | **ALREADY PATCHED UNDER OWNER INTERRUPTION; POST-PATCH EMULATION PASS.** Carry this fix unchanged into consolidated candidate and verify in K-02/K-04. |
| DEF-02 Toggle persistence architecture wrong | PRE-03, B-01, B-03, B-04 | Debug, Auto Send, Wordstat Autorun policy and report-prefix boolean controls do not persist immediately; Manual is the working counterexample because it has an immediate runtime action |
| DEF-03 Autorun cannot start | PRE-04, G-01 | Live popup never creates RUN. Controlled backend start reaches `waiting_command`, narrowing defect to popup/policy/integration path |
| DEF-04 Free-call charge semantic wrong | PRE-07, E-04 | Governed live `getRegionsTree` confirms `estimated_rub:0` with incorrect `charged:true`; request_id `5afde028-66f9-488f-bbdf-e30649432d24` |
| DEF-05 Successful-result executed flag missing | D-10, D-02, E-03 | Successful sent `WORDSTAT_RESULT_V1` envelopes omit `request_executed`, while local skips and HTTP-error results include it; execution semantics are inconsistent |
| DEF-06 Manual post-request delivery readiness failure | C-07 incident, D-11 | On the second double-click pair, Yandex request `1e7bbdfc-f67e-4079-868f-95ef58db574d` completed HTTP 200, then delivery failed with `DELIVERY_SEND_TARGET_NOT_READY_BEFORE_COMMIT`, `request_executed:true`, `automatic_retry:false`. Subsequent fresh commands recover, but the already-executed result must be durably recoverable without another Yandex request. |

---

## 5. Plan amendments

Append newly discovered test requirements here **before executing them**.

- 2026-08-12 — Add `D-11 Recovery after post-request delivery failure` after C-07 incident. The incidental failure is already evidence for DEF-06; D-11 is the first governed follow-up and is added before execution. Use free `getRegionsTree`; acceptance requires a fresh request to deliver normally without replaying request `1e7bbdfc-f67e-4079-868f-95ef58db574d`.
- 2026-08-12 — Owner explicitly interrupted the remaining campaign and ordered immediate DEF-01 plaque repair with controlled emulation, not repetitive owner UI clicking. No new test ID was introduced: existing C-02/C-03/C-04 and K-07 cover the patch. Scope is limited to reference toast/plaque renderer parity and labels/tones; no other defect is patched in this interruption.

---

## 6. Frozen patch requirements derived from the campaign

The pre-patch campaign is complete. No additional implementation scope may be invented from memory; the consolidated patch is limited to the frozen defects below plus structural changes strictly necessary to satisfy them.

### PR-01 — Preserve the already-completed DEF-01 plaque repair

Mapped defects/tests: `DEF-01`, `C-02`, `C-03`, `C-04`, final `K-02`, `K-04`.

- Carry forward the owner-interrupted reference-plaque patch without reintroducing invented `YMB:`/`Yandex Marketing Bridge:` user-facing plaques.
- Plaque renderer/style remains the reference implementation; only operation-specific text/tone may vary where already governed.
- Revalidate by controlled UI emulation first; final consolidated-candidate real Chrome closure is K-02/K-04.

### PR-02 — Immediate persistence for every toggle-class control

Mapped defects/tests: `DEF-02`, `B-01`, `B-03`, `B-04`, final `K-05`.

- Debug, Auto Send, Wordstat Autorun policy and report-prefix enabled state must apply and persist on the toggle action itself.
- Closing/reopening popup must reproduce the new state without Save.
- Toggle persistence must not implicitly commit unsaved text/credential fields; those remain governed by B-05 explicit Save semantics.
- Manual Wordstat's already-working immediate persistence behavior remains unchanged.

### PR-03 — Restore popup Autorun start/lifecycle integration

Mapped defects/tests: `DEF-03`, `G-01` through `G-06`, final `K-03`.

- One Start action in the popup must operate against the confirmed current ChatGPT conversation and create/start exactly one RUN.
- Start must not depend on a stale unsaved Autorun-policy toggle; PR-02 persistence and Start ordering must make the backend's already-proven `WS_AUTO_START` transition reachable from the popup.
- Once started, popup/current-conversation integration must expose the same RUN identity/counters and allow pause, resume and stop without accidental replacement/reset.
- Do not weaken existing ownership, budget, recovery or unknown-outcome fences proven by G-07/G-08/G-09/H/I.

### PR-04 — Correct free-call charge semantics

Mapped defects/tests: `DEF-04`, `E-04`, final `K-06`.

- `getRegionsTree` remains estimated cost 0 and must report `charged:false` on both successful and error/skip envelopes where no billable charge applies.
- Paid methods retain their governed tariff estimate semantics.
- Cost/accounting counters and policy ceilings must remain consistent with the corrected envelope field.

### PR-05 — Make successful execution semantics explicit

Mapped defects/tests: `DEF-05`, `E-03`, final `K-01`, `K-06`.

- Every successful response returned after a Yandex request was actually sent must contain `request_executed:true`.
- Local validation/policy skips remain `false`; unknown irreversible outcomes remain `UNKNOWN`; HTTP-error requests already sent remain `true`.
- No `job_id` or runtime GitHub coupling may be introduced.

### PR-06 — Durable recovery for already-executed Manual delivery failure

Mapped defects/tests: `DEF-06`, C-07 incident, `D-11`, `I-04`, `I-05`, final `K-02`, `K-08`.

- If Yandex already returned and ChatGPT Send target is temporarily not ready **before delivery commit**, preserve the completed operation/result as durable delivery state instead of losing the result.
- Recovery may retry/reconcile only the ChatGPT delivery contour. It must never replay the Yandex request for that operation.
- An irreversible Send boundary must remain fenced exactly as already proven by I-04/I-05; no blind second Send after commit.
- A later content-ready/recovery cycle must be able to resume the preserved delivery deterministically, exactly once.
- Error reporting remains automatic and recoverable, with secrets redacted.

### Consolidated patch verification order

1. Implement PR-01 through PR-06 only.
2. Add focused regression/emulation coverage for each repaired defect before any new live command.
3. Run affected tests: B-01/B-03/B-04, C-02/C-03/C-04, G-01 through G-09, E-03/E-04, D-11 recovery contour, I-04/I-05 and all J regressions.
4. Run full source + packaged regression and source/package identity (`K-07`).
5. Build one consolidated patched candidate.
6. Only then begin K-01/K-02/K-03/K-04/K-05/K-06/K-08 real-current-Chrome closure, with the pricing/one-command-per-turn rule still in force.
7. Phase 1 LIVE PASS and Phase 2 unlock require zero unresolved mandatory FAIL/BLOCKED items.