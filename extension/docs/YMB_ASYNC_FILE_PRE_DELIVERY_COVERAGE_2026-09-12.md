# YMB async/file patch — дополнение к покрытию pre-delivery gate

Дата: 2026-09-12. Ветка: `wip/ymb-file-delivery-patch-a-2026-09-12`.

Это рабочая карта покрытия для объединённого кандидата B12, **не отчёт успешного финального gate**. Она применяется вместе с `CODEX_PRE_DELIVERY_FULL_REGRESSION_GATE.md` и `YMB_PATCH_DEPENDENCY_AND_RESOURCE_SAFETY_RULE.md`, не отменяя ни одного требования. Все PD-00…PD-17 остаются в матрице.

В development разрешены сфокусированные проверки. Независимый полный gate выполняется отдельно после заморозки точного кандидата. Все browser-owned требования остаются browser-owned; fixture не становится Chrome PASS.

## Точные исполнимые наборы

Пути тестов ниже — относительно `extension/tests/wip/YMB_ASYNC_PATCH_B_2026-09-12/qa/`. `prepare_b12.py` использует точный сохранённый B11 и меняет только две README. `b12_available_campaign.py` проверяет hashes входов/кандидата, выполняет набор полных функций с B12-контрактами, затем сохранённые модульные и export-наборы. Он не называется Codex gate и не делает сетевых обращений к провайдеру.

Квалифицированный browser harness для итогового B12 в этой сессии не запущен. Его нельзя заменить счётчиками unit-тестов. Сохранённый source-snapshot содержит исторические отчёты Patch A, но не полный набор исполнимых браузерных harness-файлов: отсутствие файла в этом снимке не означает, что его нет в другом workspace. Перед независимой проверкой надо восстановить последний подтверждённый harness, а не изобретать новый или просить владельца переносить QA-файлы.

## Карта всех разделов

| Раздел | Доступное доказательство | Открытая часть |
|---|---|---|
| PD-00 — Authority, freeze and exact identity | **available**: prepare_b12.py + B12_INPUTS.json; 138 remote input blobs; 67 final files | An independent campaign must freeze its own exact candidate/package; this is development evidence. |
| PD-01 — Complete source regression suite | **partial**: b12_available_campaign.py: 99 full/contract, 254 module, 84 export | These intersecting patch suites are not the entire extension/tests source suite. Inventory and execute the full current suite before final PASS. |
| PD-02 — Static, syntax and manifest integrity | **available**: b12_contract.test.mjs manifest case; 61 node --check; 2 JSON parse; README correction | Final package path set and release version must be checked again after deliberate permission/version changes. |
| PD-03 — Package/reconstruction integrity | **not_run**: prepare_b12.py exact source reconstruction; wrong/nonempty input refusal | No installable ZIP exists. Source-tree equality is not package-byte equality. Final canonical packaging and fresh extraction remain mandatory. |
| PD-04 — Runtime installation and MV3 lifecycle | **blocked**: Earlier BROWSER_BOUNDARY.json; no new browser test | Requires qualified controlled Chrome installation/worker restart. Node importScripts is not MV3 lifetime proof. |
| PD-05 — Popup/settings behavior | **blocked**: Existing popup sources unchanged; worker settings fixtures in B5/B6 | No qualified actual-popup toggle/Save/reopen campaign on this candidate. |
| PD-06 — Manual action surface / ChatGPT DOM binding | **blocked**: B10 content-function checks are supplemental only | Actual PRE/CodeMirror, independent Yandex control, native Copy lifecycle, placement and plaques require browser harness. |
| PD-07 — Manual full-block discovery and content→worker behavior | **partial**: b7_worker.test.mjs through export campaign; b9_full_worker; b10_content_contract | Real external-button event, bound DOM block capture and content→worker integration remain browser-owned. |
| PD-08 — Wordstat protocol / all Phase-1 operations | **partial**: b9_full_worker.test.mjs covers getRegionsTree; B5 preserved neighbor dispatch | All getTop/getDynamics/getRegionsDistribution faults and complete original Wordstat protocol suites are not certified by the patch-only snapshot. |
| PD-09 — Policy, credentials, cost and accounting | **partial**: b5_policy/b5_legacy/b5_callers; b10_deferred/legacy; b11_batch_faults | Real IDB contention, settings changes and installed run persistence require final integrated gate. Current Search numbers are estimates, not invoice reconciliation. |
| PD-10 — Autorun lifecycle | **partial**: b10_legacy and b11_batch_faults full worker controlled scenarios | Installed popup/command pickup/visible plaques/reload lifecycle are unverified. Deferred Autorun intentionally unsupported. |
| PD-11 — Manual delivery FSM, durability and duplicate prevention | **partial**: b9_full_worker; b10_deferred/content; b11_reparse; b8_worker/artifact | Controlled outbox ACK is not actual Send→Microphone/DOM/file upload proof. Browser failure/cancel/resource matrix remains open. |
| PD-12 — Debug/error contract | **partial**: b5_legacy/transport; full-worker errors and secret assertions in B9-B12 | Complete Debug OFF/ON report-shape matrix for every existing service is not certified by these focused tests. |
| PD-13 — Conversation/tab/ownership isolation | **partial**: b6_binding; b9_full_worker; b10_content/deferred; b11_reparse | Actual duplicate tabs, navigation, cross-PRE/assistant DOM isolation still requires controlled Chrome. |
| PD-14 — Export/import, migration and persistence | **partial**: b8_export/artifact/worker + b11_reparse; Patch A historical backup report kept separate | Export pages are not a settings backup. Full import/export/legacy wsmb compatibility and cross-install/upgrade persistence remain final-gate work. |
| PD-15 — Security/provider-surface containment | **partial**: b12_contract rejects URLs/auth/unsupported operations; protocol/transport and B5 regressions | These cases are not complete page/popup/backup secret-exposure coverage. All executed requests use fixtures, real provider count 0. |
| PD-16 — Future-service phase locks | **available**: B12 full-worker absent-host tests; B9 tests already-enabled legacy services | Apply existing gate sentence about enabled phases: old services are enabled in owner014. New deferred submit/collect locked. Recognition alone never authorizes activation. |
| PD-17 — Final artifact cleanliness/evidence | **not_run**: All B12 raw logs/identities preserved; no candidate mutation during tests | No independent final-gate verdict or final installable artifact. Mandatory missing sections prevent PASS. |

## Новые обязательные случаи для async/file изменения

К существующим PD-09/11/14/15/16 добавляются: раздельная отправка и получение Operation; общий допуск обычного и отложенного поиска; UNKNOWN без повтора POST; сохранение исходного ответа до разбора; локальный normalizeSaved; ограниченные exportPage с revision; delivery-outbox и удаление только доставочного файла; обязательная недоступность submit/collect без host permission. Эти случаи покрываются названными B3–B12 тестами в Node, но не закрывают реальные MV3/IDB/DOM/память.

В PD-16 старое условие «будущие сервисы выключены» применяется по фактическим включённым фазам. Owner014 уже содержит обычный Search/GenSearch/Вебмастер/Метрика/Директ. Возвращать их в Phase 1 ради старого текста запрещено; им нужна функциональная регрессия. Новый отложенный сетевой маршрут пока выключен намеренно.

## Ресурсная граница

Для итогового объединения остаются реальные файловые циклы 1/10/32/64 MiB с повторами и batch 10/100/500/1500, cleanup/cancel/reload, измерение процесса Chrome и утечек, IDB durability. Исторические Node sample и Patch A browser results не присваиваются всему B12.

**RELEASE_ALLOWED = NO. INDEPENDENT_PRE_DELIVERY_GATE = NOT_RUN.** Проверка доступного не означает отмену недоступных обязательных проверок.
