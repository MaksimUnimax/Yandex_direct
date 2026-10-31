# Аудит массового Wordstat: код версии 0.1.14 и GitHub

**Дата:** 31.10.2026. **Режим:** READ-ONLY SOURCE REVIEW, без установки/изменения расширения и без нового запроса к Wordstat.  
**Источник:** предоставленный архив `Yandex-Marketing-Bridge-0.1.14-ChatGPT-Chat-FIX(1).zip`; сопоставление с `MaksimUnimax/Yandex_direct`, ветка `main`. Сам факт ответа Bridge ранее подтвердил установленную версию 0.1.14. В `main` manifest всё ещё показывает 0.1.1, поэтому для фактического поведения установленной версии основное доказательство — ZIP 0.1.14.

## Вывод

**Да, в ручном режиме обычные `WORDSTAT_API_V1` команды можно поместить в один кодовый блок и выполнить одним нажатием «Яндекс».** Source `service_worker.js`: `discoverManualBlockItems(blockText)` обнаруживает несколько маркеров; `executeManualBlock(...)` выполняет `for (const item of preflight.items)` и ждёт каждый `executeServiceCommand`, а затем собирает ответы в один доставляемый отчёт. Эти команды выполняются **последовательно, один HTTP-запрос на одну фразу**, не одним массовым HTTP-запросом. `WORDSTAT_API_V1` — именно одиночный `phrase`, не массив `phrases`. 

**Но существующий `WORDSTAT_BATCH_API_V1` job не позволяет выдать много `next` одним блоком в установленной 0.1.14.** Source `shared/wordstat_batch_protocol.js`: действия только `start`, `next`, `status`, `pause`, `resume`, `cancel`. `start` сохраняет до 500 фраз и лимиты; `shared/wordstat_batch_runtime.js` осуществляет один `Model.claimNext` и один `executeWordstat` на один `next`. Source `wordstat_batch_worker_transport.js:107-115`: если в Manual-блоке есть batch-маркер, количество найденных команд должно равняться ровно 1; иначе ошибка `BATCH_SINGLE_COMMAND_REQUIRED`.

Есть альтернативный файл `wordstat_batch_worker_integration.js`, в котором имеется цикл по нескольким batch-командам, **но этот файл НЕ импортирован в `phase3_service_worker_bootstrap.js`** установленного архива и не является доказательством действующей функции. Реально импортируется `wordstat_batch_worker_transport.js`. Аналогично отдельное наличие `wordstat_batch_content_integration.js` не означает его подключения.

Источники GitHub:
- https://github.com/MaksimUnimax/Yandex_direct/blob/main/extension/src/service_worker.js (Manual discovery/execution).
- https://github.com/MaksimUnimax/Yandex_direct/blob/main/extension/src/wordstat_batch_worker_transport.js (ограничение `BATCH_SINGLE_COMMAND_REQUIRED`).
- https://github.com/MaksimUnimax/Yandex_direct/blob/main/extension/src/phase3_service_worker_bootstrap.js (реальная загрузка).
- https://github.com/MaksimUnimax/Yandex_direct/blob/main/extension/src/shared/wordstat_batch_protocol.js (перечень действий).
- https://github.com/MaksimUnimax/Yandex_direct/blob/main/extension/src/shared/wordstat_batch_runtime.js (один item за next).
- https://github.com/MaksimUnimax/Yandex_direct/blob/main/extension/src/shared/wordstat_protocol.js (одна фраза в обычном getTop).
- https://github.com/MaksimUnimax/Yandex_direct/blob/main/extension/docs/PHASE_6_SEMANTIC_CORE_BUILDER_REQUIREMENTS_AND_PLAN.md (назначение durable batch).

## Проверка без внешних вызовов

В локальном JS VM загружены действующие `shared/service_registry.js`, `shared/wordstat_protocol.js`, `shared/wordstat_batch_protocol.js`, `shared/block_command_discovery.js` и `shared/wordstat_batch_transport.js`. Блок из **14 обычных команд** распознан как **14 корректных Wordstat getTop**, с правильной первой и последней фразой, без ошибки. Два `WORDSTAT_BATCH_API_V1 {"action":"next",...}` распознаются как две batch-команды, на которые действующий worker выдаёт `BATCH_SINGLE_COMMAND_REQUIRED`. Проверена лишь логика исходников, **не проводился живой многострочный Manual-вызов**.

Дополнительно модель `shared/provider_batch_job_model.js` прогнана на синтетическом задании: `cancel` сохраняет статус `SUCCEEDED` первого item, остальные `PENDING` переводит в `CANCELLED`, и не делает provider request.

## ВАЖНО: текущее реальное состояние и переход

У нас уже существует **реальное задание `microproducts-f1-wave01-20261031`**: 15 фраз, первая `O01.2-Q1` измерена (GetTop `totalCount=3`, ответ и request_id сохранены), 14 `PENDING`, `succeeded=1`, `requests_started=1`, оценка расходов 0,02 ₽. **Не запускать одновременно сохранённую очередь через `next` и обычные команды для тех же 14 фраз.**

Для перехода к массовому однокнопочному Manual без изменения кода расширения:
1. Выполнить и ДОЖДАТЬСЯ подтверждённого результата операции `cancel` **у существующего job_id** (не пересоздавать start). Ожидаемая логика модели: 1 SUCCEEDED сохранится, 14 PENDING станут CANCELLED. Проверить фактический отчёт; нельзя считать отмену состоявшейся только по этой инструкции. Локальная команда отмены без провайдера: `WORDSTAT_BATCH_API_V1 {"action":"cancel","jobId":"microproducts-f1-wave01-20261031"}`.
2. Только после подтверждения `status=CANCELLED` и `pending=0` допустимо нажимать «Яндекс» под ОДНИМ блоком с 14 обычными `WORDSTAT_API_V1` командами ниже. Это новая Manual-операция **вне прежнего durable batch-job**. Расход ориентировочно 14×0,02=0,28 ₽ по штатной политике; уже полученное 0,02 не пересчитывать. Запросы не выполнялись подготовкой этого документа.
3. Сохранить все полученные отчёты с разными request_id по исходным ID `O04.1-Q1 ... O41.2-Q1`. При частичной или неясной доставке НЕ повторять весь блок слепо: выяснить, что успело выполниться, и затем адресно решить, что делать с остатком.

**Ограничения обходного пути:** прямые `WORDSTAT_API_V1` не обновляют очередь прежнего `WORDSTAT_BATCH_API_V1`, не наследуют его `maxRequests=15` и `maxCostRub=1`, а также его долговременную защиту от дублей/восстановление по каждому item. Обычная Manual-операция блокирует параллельный запуск в том же диалоге, но при прерывании большого блока нужно сверять реальные результаты. Много команд могут создать большой отчёт; при сомнениях делить на 2 блока по 7, чтобы уменьшить риск потери/обрыва и упростить повторную проверку. Это те же 14 разных фраз, не дополнительные вызовы.

Долгосрочно при сотнях/тысячах запросов целесообразнее исправить сам Bridge отдельным согласованным заданием: безопасная команда `batch.runMany` или `batch.drain`, выполняющая N элементов с сохранением durable checkpoint, лимитов, отмены и остановки при UNKNOWN. **Сейчас в 0.1.14 такого действия нет, исходники продукта не изменялись.**

## Подготовленный блок 14 обычных запросов — НЕ НАЖИМАТЬ ДО ПОДТВЕРЖДЁННОЙ ОТМЕНЫ

```text
WORDSTAT_API_V1 {"method":"getTop","phrase":"сравнить спецификации","numPhrases":50,"regions":["225"],"devices":["DEVICE_ALL"]}
WORDSTAT_API_V1 {"method":"getTop","phrase":"журнал замечаний стройконтроля","numPhrases":50,"regions":["225"],"devices":["DEVICE_ALL"]}
WORDSTAT_API_V1 {"method":"getTop","phrase":"расчет кромки по деталировке","numPhrases":50,"regions":["225"],"devices":["DEVICE_ALL"]}
WORDSTAT_API_V1 {"method":"getTop","phrase":"учет хранения шин","numPhrases":50,"regions":["225"],"devices":["DEVICE_ALL"]}
WORDSTAT_API_V1 {"method":"getTop","phrase":"учет моточасов мотоцикла","numPhrases":50,"regions":["225"],"devices":["DEVICE_ALL"]}
WORDSTAT_API_V1 {"method":"getTop","phrase":"учет ремонта самокатов","numPhrases":50,"regions":["225"],"devices":["DEVICE_ALL"]}
WORDSTAT_API_V1 {"method":"getTop","phrase":"учет возвратной тары","numPhrases":50,"regions":["225"],"devices":["DEVICE_ALL"]}
WORDSTAT_API_V1 {"method":"getTop","phrase":"проверка удержаний вайлдберриз","numPhrases":50,"regions":["225"],"devices":["DEVICE_ALL"]}
WORDSTAT_API_V1 {"method":"getTop","phrase":"учет саженцев в питомнике","numPhrases":50,"regions":["225"],"devices":["DEVICE_ALL"]}
WORDSTAT_API_V1 {"method":"getTop","phrase":"список закупки кондитера","numPhrases":50,"regions":["225"],"devices":["DEVICE_ALL"]}
WORDSTAT_API_V1 {"method":"getTop","phrase":"учет отработок занятий","numPhrases":50,"regions":["225"],"devices":["DEVICE_ALL"]}
WORDSTAT_API_V1 {"method":"getTop","phrase":"учет лабораторных образцов","numPhrases":50,"regions":["225"],"devices":["DEVICE_ALL"]}
WORDSTAT_API_V1 {"method":"getTop","phrase":"сбор заказов школьного фотографа","numPhrases":50,"regions":["225"],"devices":["DEVICE_ALL"]}
WORDSTAT_API_V1 {"method":"getTop","phrase":"учет аренды звукового оборудования","numPhrases":50,"regions":["225"],"devices":["DEVICE_ALL"]}
```

Этот блок лишь подготовлен и проверен парсером в изоляции. НЕ запускался. Первую, уже измеренную фразу `учет заказов зуботехнической лаборатории` намеренно исключили, чтобы не оплачивать повтор.
