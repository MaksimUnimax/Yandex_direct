# Patch B, block B1 — per-item storage and state contract

Date: 2026-09-12. Status: IMPLEMENTED / DETERMINISTIC TESTS PASSED / REAL IDB AND RESOURCE VALIDATION BLOCKED. Not a release.

## Continuity

Live WIP branch was read at `af421242389206acc4ffa64a37d17577070efbf9`, newer than the earlier chat checkpoint. That commit records Patch A acceptance for integration only. Patch A candidate2 and its exact-target recorded results were preserved. No Patch A source was rewritten. No Kwork job state or shared roadmap branch was edited.

The exact local owner baseline ZIP was rechecked: `b812c4c54d1054d63a24ea852e1721e813d133172487c9872bac347998e3e53f`.

## Implemented source

`candidate/shared/search_async_store.js`

SHA-256: `4145cbc91865c3151a34f8958640c6351bf6cb23a3a74441920d3517d483cba4`.
Git blob confirmed by remote readback: `43c170f7afc8332fb956436d94357e0049c8e4f7`.

Separate IndexedDB database with jobs, items, results and attempt records. There is no chrome.storage job-map and no per-transition clone of all queries/results. A transition reads and writes one item and small job counters. Creation/cancellation necessarily traverses the requested set once. Page output is bounded at 100 item records. Provider responses are stored independently, before normalization can mark success. Failed normalization retains the raw result.

Submission intent, job budget reservation, attempt identity and item state are written together. Interrupted submission becomes UNKNOWN and does not authorize re-submission. Interrupted read can return to WAITING on the same saved operation. An unknown submission does not destroy other already-accepted operations. Cancellation affects unsent items, leaving known operation IDs recoverable.

## Dependency impact and evidence

| Changed part | Affected dependency | Evidence now | Still required |
|---|---|---|---|
| New store | IndexedDB transactions/indexes | Source syntax and deterministic API test double | Real Chromium IDB scheduling, durability and faults |
| Claim/settle/recover | Attempt ownership, budget counters, crash states | 15 functional cases below | Actual service-worker restart integration |
| Cancellation | Pending/accepted item separation | Functional cancellation cases | UI/worker integration |
| Page/read result | Item accounting and bounded output | 251-item paging and complete state reconciliation | Full browser scale and resource matrix |
| Existing services | No manifest/import/provider/credentials changes in this block | Existing production files untouched | Integration regression after runtime is connected |

## Actual RED to GREEN

Initial source SHA-256: `9226950473771c40f131f6fa080d96402f8da7e2a62826c5a124aa9bcdf2012a`.
15 deterministic cases executed; 13 passed, 2 failed:

1. Reusing an already-settled attempt token could claim the next item. Fixed by a separate indexed attempt record written in the same claim transaction. Duplicate token now grants no new execution.
2. Cancellation could be changed to PAUSED and then resumed. Fixed by rejecting pause/resume after cancellation; already accepted operation results remain collectible.

The same 15 cases then passed on the final source hash above. Syntax also passed with Node v22.16.0.

Test cases:

- create_duplicate_and_owner — PASS
- concurrent_claim_exactly_one — PASS
- repeated_attempt_never_admits_second_item — PASS
- budget_exhaustion_and_get_independence — PASS
- unknown_submit_recovery_is_fail_closed — PASS
- collect_survives_another_unknown_submit — PASS
- poll_cooldown_and_network_read_error — PASS
- interrupted_collect_restores_only_get — PASS
- raw_first_parse_failure_local_repair_and_duplicate_commit — PASS
- failure_not_empty_success — PASS
- raw_and_state_transaction_abort — PASS
- operation_identity_collision_rolls_back — PASS
- pause_cancel_and_known_operations_preserved — PASS
- cancel_cannot_be_cleared_through_pause — PASS
- validation_and_paging_bounds — PASS

These results were obtained using `qa/run_store_logic.mjs` and the explicitly labelled deterministic transaction double `qa/idb_test_double.mjs`. They prove tested state logic only. They do NOT prove actual IndexedDB scheduling, disk durability, browser memory, resource safety or installed-extension behavior.

## Actual browser attempt and hard boundary

A fresh validation-owned Chromium 144.0.7559.96 was launched. Navigation to the isolated localhost QA fixture was rejected with `net::ERR_BLOCKED_BY_ADMINISTRATOR` before any product assertion executed. Read-only policy inspection showed `URLBlocklist: ["*"]` and `ExtensionInstallBlocklist: ["*"]`.

Classification: BLOCKED_ENVIRONMENT. Policies were not modified or bypassed. No browser-resource PASS is claimed. The validation browser left no running process. Additional plugin discovery did not provide an installed extension-QA executor. Node results are not a substitute for this missing proof.

## Next exact actions

Continue with the separate async request/Operation protocol and its deterministic contracts while the browser boundary remains open. Before acceptance, run the real IDB and 10/100/500/1500 resource/recovery matrix in an authorized qualified environment. Then complete provider adapter, existing lifecycle integration, global policy/cost reconciliation, export and final regression. Do not install or release this standalone WIP module.

RELEASE_ALLOWED = NO
OWNER_ZIP_HANDOFF = FORBIDDEN
NEW_PROVIDER_CALLS = 0

## Sources checked again for this block

- https://w3c.github.io/IndexedDB/ — transaction/index semantics and completion versus request success.
- https://developer.chrome.com/docs/extensions/develop/concepts/service-workers/lifecycle — worker termination requires persisted recovery state.
- https://aistudio.yandex.ru/ru/docs/search-api/api-ref/WebSearchAsync/search — submission returns an Operation, not necessarily search results.
- https://aistudio.yandex.ru/ru/docs/search-api/api-ref/Operation/get — read by operation ID; completion may contain error or response.

## Простыми словами

Существующая файловая часть не переделывалась. Для отложенного поиска написано отдельное хранилище по запросам вместо огромного общего объекта. Два дефекта нового кода пойманы тестами и исправлены до выдачи: повтор одного разрешения на отправку и отмена через паузу. Проверка логики проходит; проверка настоящего браузера в текущей среде заблокирована политикой. Поэтому сборку владельцу выдавать по-прежнему нельзя.
