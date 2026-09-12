# B9 — объединение файловой доставки и отложенного Search

Дата: 2026-09-12. Статус: **единое исходное дерево собрано для QA; доступные Node-проверки выполнены; это НЕ разрешённый релиз**.
**RELEASE_ALLOWED = NO. ZIP для установки владельцу не выдавать.**

## Продолжение и входные байты

После обрыва прочитан live HEAD `fc89ba5766373bd6abbdfac58b7c3670f58b0702`. Сначала сохранён актуальный cursor B8, затем закрыт B8 checkpoint. B8 восстановлен штатным materializer; 84 проверки и 1/10/32/64/64/64 MiB Node-диагностика действительно повторены. Их результаты находятся в отдельном `BLOCK_B8_RESULT.md`; они не переименовываются в B9 Chrome PASS.

Исходный owner ZIP 0.1.4: SHA-256 `b812c4c54d1054d63a24ea852e1721e813d133172487c9872bac347998e3e53f`, 53 файла. Полное дерево baseline проверяется по SHA-256 списка всех файлов `6092555d37a1fa0145d71ae0bf0f76eb0b9c9596a4be7a1e0e7c2a0b9325aa36`.

Сохранённые WIP-источники извлечены из read-only GitHub Actions snapshot точного ref. 96 файлов сверены с Git blob SHA. Ничего из старых этапов не написано заново по памяти; исходные A/B1–B8 snapshots не заменялись.

## Что сделано

Создан воспроизводимый `qa/prepare_b9.py`, соединяющий:

- точную owner 0.1.4;
- сохранённый Patch A и его content-script patch;
- B3 дополнение поэлементного store;
- B4 строгий normalizer;
- B5 общий policy/legacy guard и четыре точных legacy delta;
- B6 trusted binding с сохранённым B7 изменением статуса;
- B8 protocol/Manual worker postimages и bounded exporter;
- новый B9 порядок загрузки.

Результат — **67 файлов, 61 production JS**. Manifest не получает новый operation-host и alarms. В тестовом дереве не меняется версия ради видимости готового релиза. Установочный архив не собирался. Общая roadmap-ветка, данные Kwork-заказов и `extension/src` не изменялись.

Единственное новое production-изменение B9 — `candidate/b9/phase3_service_worker_bootstrap.js`. Новые QA helper/тесты/materializer не входят в production tree.

## Реально найденная ошибка объединения — RED/GREEN

Наивное соединение прежних bootstrap-фрагментов загружало async worker раньше Search batch и Patch A file-aware outbox. Его autoInstall захватывал ещё отсутствующий artifactStore. Формальная готовность внутренних объектов не означала работоспособность экспорта: полный Manual start выполнялся, но exportPage возвращал `ASYNC_EXPORT_NOT_READY`.

Это воспроизведённый дефект новой композиции, НЕ заявление о воспроизведении исходного зависания компьютера владельца.

Исправлено: после основных сервисов и общего Search admission загружается обычный Search batch, затем artifact store/file-delivery wrapper, затем async store/protocol/transport/normalizer/runtime/exporter и последним async Manual worker.

В новой матрице полного worker до исправления: **20 тестов, 15 PASS / 5 FAIL**. Один корень затронул порядок загрузки, export, сохранённые raw/results и две downstream attachment-проверки. После изменения только bootstrap все 20 прошли. Точный diff сохранён в `evidence/B9_BOOTSTRAP_RED_TO_GREEN.diff`.

RED bootstrap SHA-256: `cd4d8106af584d8265056b5a43ef05adea1c9326ec48be8f785b9790a2159b5e`.
GREEN bootstrap SHA-256: `5a47f5f5e0c3305b72a6b776593df1065dba8ae319543f545014407d7ae012c5`.

## Что именно проверено

### Полный worker в Node VM: 20/20

В отличие от прежних отдельных factory-тестов, `b9_full_worker_harness.mjs` исполняет весь настоящий сохранённый worker и его importScripts-цепочку. Chrome storage/tabs/messages, IndexedDB и fetch представлены явно обозначенными fixtures. Это НЕ установленный Chrome.

Проверены: загрузка инициализированных модулей без startup provider calls; единственный responder WS/YMB; Manual start -> реальный поэлементный store -> экспорт -> настоящий Patch A binary store -> outbox -> подтверждение -> cleanup; сохранность запросов, raw ответа, нормализованных URL и исходной записи после удаления файла доставки; неправильная вкладка; отключённый Manual; другой сервис; непривязанный диалог; недоступный operation-host; чтение одного chunk и checksum; attachment state transitions; обычный короткий текст и перевод большого текста в файл.

Выполнены также шесть старых Manual-путей через полный dispatcher: Search.search, Search.genSearch, Wordstat.getRegionsTree, Webmaster.listHosts, Metrika.listCounters, Direct.listCampaigns. Каждый совершил ровно один вызов тестового fetch; тестовые секреты не попали в отчёт. Это покрывает названные сценарии, а НЕ все методы этих сервисов.

Точный сохраняемый тест после адаптации имени импортируемого QA helper: **20/20 PASS**, 1117.133791 ms. Из заново восстановленной QA-папки: **20/20 PASS**, 1051.602187 ms. Skipped/cancelled/failed = 0.

### Регрессия модулей на тех же B9 production-байтах: 254/254

Заново выполнены сохранённые тесты, а не просуммированы старые PASS:

- B3 store/runtime/edge: 43;
- B4 normalizer: 60;
- B5 policy/legacy/counter fragments: 85;
- B6 binding: 18;
- protocol/transport: 48.

Первый общий прогон: **254/254 PASS**. Затем этот же запуск воспроизведён сохранённым `qa/b9_regression_campaign.py`: **254/254 PASS, exit 0**, 3328.090601 ms. Все файлы тестов закреплены хэшами, production берётся из exact B9 candidate. В этих тестах IDB, сеть, некоторые settings/run/context остаются fixtures; caller-тесты исполняют точные фрагменты. Они не являются полной браузерной регрессией.

### Статические проверки и точность восстановления

- 61/61 production JS прошли `node --check`.
- manifest.json/package.json разбираются.
- Все ссылки manifest на content/background файлы существуют; ссылки popup на CSS/JS существуют.
- 29 входных source/test/helper файлов закреплены хэшами в `B9_INPUTS_SHA256.json`.
- Все 67 файлов свежего output совпали с проверенным исходным кандидатом.
- Materializer отказал при непустом output и неверном baseline до создания нового output: 2/2.
- Remote readback семи новых production/test/materializer/manifest/diff файлов: 7/7 Git blob SHA совпали с локальными проверенными байтами на ref `5a82e73cae984d435625f1c7d6e46b05aacef4a4`.

## Явное разрешение расхождений идентичности

Ранее обнаруженное несовпадение B7 report/фактического worker остаётся документированным в `B8_IDENTITY_RECONCILIATION.md`. Использованы фактические Git-байты, не выдуманный файл по неверному hash.

При сверке Patch A найдена ровно одна дополнительная LF в сохранённом bootstrap: 3306 bytes, SHA `b5b9843bbd3d0d848929252b536c38382a02e1b5dceeba06942e4286b42ec44e`. Удаление ровно последнего LF даёт объявленный исходный hash `ad926d9c046616508f8e71be2f1725a6a3a0afa6afa9643b461acf87545cc918`, 3305 bytes. Materializer делает только это проверяемое восстановление и затем подтверждает 57/57 A-файлов. Другие нормализации окончания строк не выполняются. Сохранённый A snapshot не переписан; итоговый B9 bootstrap новый и проверен отдельно.

## Dependency-impact matrix

| Изменение / зависимость | Доказательство в этом блоке | Что ещё не доказано |
|---|---|---|
| Bootstrap -> все worker imports | Полная реальная importScripts-цепочка, RED/GREEN, no duplicate module/startup fetch | Реальный MV3 lifetime/startup |
| Async worker -> A file-aware outbox/store | start/export/chunk/ack/cleanup настоящих JS через fake IDB | DOM attachment, фактический upload и Chrome память |
| Shared guard -> старые provider paths | Шесть full Manual сценариев + 85 повторённых B5 assertions | Все реальные Autorun/batch/Check пути в одной установленной сборке |
| Binding -> Manual/tab/conversation | Full preflight и 18 повторённых binding checks | Реальная навигация вкладок/гонки Chrome |
| Поэлементные данные и normalizer | Full saved-result export, B3/B4 regression | Disk durability и реальный большой набор IDB |
| Manifest/popup/content sources | Файлы/ссылки/JS syntax; permission остаётся disabled | Живой ChatGPT DOM и полная content-script доставка |
| Exact reconstruction | 53 baseline, 57 A, 67 B9; hash manifests и отказ неверным входам | Финальная installable ZIP identity ещё не создавалась |

## Сохранение и воспроизведение

Полный новый TAP на 20 случаев: `evidence/B9_FRESH_FULL.tap`, SHA `2adfc8ecd785f74e5df6a4633454447cd11df699c6af96f698177491e69c651f`.

`evidence/B9_TEST_RESULTS.json` содержит все 20 новых assertion, пять исходных FAIL, hashes/code identities, результаты свежего прогона и 254-case regression. Полный 50,484-byte TAP 254-проверок сейчас локальный; его SHA `5849ddb20f7ce9ff7a476d926167cb442586a6f22ad35c9420a119c97ee085a0` сохранён в JSON. Здесь НЕ утверждается, что сам этот большой TAP опубликован. `b9_regression_campaign.py` сохраняет его при каждом воспроизводимом запуске.

```text
python qa/prepare_b9.py <exact-owner014-directory> <new-empty-b9-qa>
YMB_FULL=<new-empty-b9-qa>/candidate/full YMB_IDB_FIXTURE=<new-empty-b9-qa>/qa/idb_artifact_fixture.mjs node --test <new-empty-b9-qa>/qa/b9_full_worker.test.mjs
python qa/b9_regression_campaign.py <exact-owner014-directory> <new-empty-b9-qa> <new-empty-logs>
```

Полный candidate-tree manifest SHA-256: `d1fc4f49718f023f1bc1a6a3ec921fa7253d63b805cedadff6fbcf2e70180612`.

## Следующая точка

Не начинать A/B1–B9 заново. Восстановить единый B9-кандидат. Продолжить оставшиеся исполнимые проверки полных Manual/Autorun/batch/Check и deferred submit/collect на контролируемых ответах, включая ошибки записи/доставки и остановку после ошибки. Проверить content discovery/интеграционные контракты без ложного DOM PASS. Реальные permissions/provider/live проверки оставлять отдельными и не включать платный маршрут ради красивого теста.

Браузерная блокировка ранее записана; в этом блоке её не обходили и не гоняли повторно. Нового Chrome/real-IDB/combined-memory PASS нет. Независимый финальный pre-delivery gate и итоговый ZIP не выполнены.

**Новых реальных provider calls: 0. RELEASE_ALLOWED = NO.**

## Простыми словами

Файловая доставка и новый поиск теперь собраны в одно проверяемое дерево, а не только в отдельные модули. Совместная проверка действительно поймала ошибку загрузки; она исправлена до выдачи. Полный worker выполняет локальную выгрузку через сохранённый файловый механизм, а названные старые функции проходят повторные проверки. Код, тесты и восстановление уже сохранены. Это всё ещё не доказанная безопасная сборка для установки.
