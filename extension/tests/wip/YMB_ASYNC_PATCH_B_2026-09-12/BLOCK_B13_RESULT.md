# B13 — полный исходный набор тестов и недостающее покрытие

Дата: 2026-09-12. Ветка: `wip/ymb-file-delivery-patch-a-2026-09-12`.
**Доступная development-проверка закончена. Независимый финальный gate и Chrome/resource приёмка не выполнены. RELEASE_ALLOWED = NO.**

## 1. Продолжение и точный вход

Начальный live HEAD — `1aafee85d8534ab08848c217efa517a8a2cbec23`. Прочитаны cursor B12, обязательные patch/resource правила, полный PD gate и карта покрытия. Owner014 ZIP: 159963 bytes, SHA-256 `b812c4c54d1054d63a24ea852e1721e813d133172487c9872bac347998e3e53f`, 53 файла.

Существующий read-only workflow получил весь исходный extension/tests, source/reference и документацию на закреплённом ref; 2431 файла сверены с Git blob inventory. Сохранённые materializers восстановили B12 — это применение сохранённых байтов, не повторная разработка.

Вход B12: `73e6ed85bfd843bf2590a2d1a44a9d04224ce5f63563d127bcd35c2ad092eeec`.
Итог B13: `f591b39a381993c44284561236b9c5a278761db3d6b04059c59974e037c33f47`, 67 файлов.

Основная roadmap-ветка, extension/src и данные заказов не изменялись. Код/deltas, найденные ошибки, результаты и промежуточные checkpoints сохранялись до этого отчёта.

## 2. Что теперь проверено из исходного набора

Проинвентаризированы все 158 tracked файлов extension/tests вне WIP: 18 Node suites из package script, 1 дополнительный Node suite, 8 browser harness scripts, 2 исторических campaign runners, 1 runtime fixture и 128 документов/evidence. Полный список с ролью каждого файла сохранён в `qa/original_inventory.tsv` внутри QA-архива; aggregate hash всех 158 исходных файлов — `68f6e345c2e417fb9100cf9ef166b8047e5cffa13a286bc5a6e2e4a0cbb840af`.

На исходном B12 все 18 suites дали 118/118, дополнительный Direct suite — 14/14. Это именно исходные тесты, а не сумма уже знакомых WIP PASS. После двух исправлений ниже те же поведенческие требования проверены на B13.

## 3. Два унаследованных дефекта Wordstat

### HTTP 200 с некорректным JSON

Фактический cloud provider превращал неразбираемый JSON в null и затем выдавал успешный результат Wordstat. Четыре проверки полного Manual-пути воспроизвели это и на B12, и на неизменённой owner014. Добавлена только проверка JSON-object envelope после успешного HTTP: null, массив, scalar или повреждённый JSON возвращают безопасную ошибку INVALID_WORDSTAT_RESPONSE с request_executed=true и без повтора. Корректный объект с отсутствующими optional полями, в том числе {}, не запрещён. Search/GenSearch и прежние HTTP error paths не изменены.

### Пакетный Wordstat обходил текущий provider/credentials

Реальный batch worker вызывал старый executeWordstatCommand напрямую. При наличии только отдельной текущей записи credentials получался API_KEY_MISSING; при наличии устаревшего legacy ключа отправлялся именно он. Оба сценария воспроизведены на исходной owner014 с искусственными ключами.

Один вызов заменён на уже существующий executeServiceCommand(WORDSTAT, command, metadata). Сохраняются прежние admission, checkpoints, request IDs, стоимость, счётчики и ownership. Нового provider или fallback ключа не создано.

Это **два старых дефекта owner014**, не два новых async-регресса и не воспроизведение прежнего OOM компьютера владельца.

## 4. Ограниченный production-scope и зависимости

Изменены ровно два файла, остальные 65 совпадают с B12:

- shared/phase3_provider_runtime.js — Wordstat-only response guard.
- wordstat_batch_worker_transport.js — одна строка маршрутизации через единый provider.

Никаких новых payload копий, storage schemas, таймеров или циклов не добавлено. Patch A file store/transfer, Search async runtime/policy, manifest, host permissions и версия не менялись.

| Зависимость | Выполненная проверка | Открытая граница |
|---|---|---|
| Wordstat provider -> четыре метода -> Manual/error delivery | Все методы, параметры, URL, dedicated credentials, HTTP 401/403/429/500, UNKNOWN, JSON object/scalars/read failure | Реальный API/ключ не использовался |
| Batch worker -> общий provider -> Check/Manual/Autorun | Dedicated-vs-legacy credentials, batch success/failure/UNKNOWN, one boundary, delivery/ack; Check invalid response | Установленный worker/real IDB не проверены |
| Debug OFF/ON и диагностика | Ошибки видимы в обоих режимах, redaction, opt-in запись, предел 200 и очистка | Реальный popup/DOM не проверены |
| Backup/import/migration | V3 checksum/версия, все пять credentials, отказ при активном run/Manual, legacy миграция, повторный worker; backup намеренно содержит секреты, публичные ответы — нет | Реальные дисковые/браузерные миграции не доказаны |
| Прежние Search/Direct/соседние службы/экспорт | Исходные suites + повторённые 99/254/84 на точном B13 | Это development evidence, не независимый полный gate |
| Exact source/materializer | 67/67, 61 JS, 2 JSON, два отказа неверным входам | Финальный installable ZIP отсутствует |

## 5. Реальные результаты и честная граница старых тестов

Среда Node v22.16.0, полные настоящие worker/module исходники; Chrome API, IDB, время и provider-сеть представлены fixtures. Реальных provider calls = 0. Известная блокировка браузера не обходилась и не проверялась повторным запуском.

- Основные исходные suites: **118/118**.
- Дополнительный исходный Direct suite: **14/14**.
- Новое полное покрытие Wordstat/Debug/backup: **78/78**, 751.532905 ms.
- Сохранённый full/contract набор: **99/99**, 2322.791831 ms.
- Сохранённые модули: **254/254**, 1009.928663 ms.
- Manual/export/Patch A: **84/84**, 266.909047 ms.
- Все итоговые запуски: failed/skipped/cancelled = 0.
- Статика: **61/61 JS**, два JSON. Свежая идентичность: **67/67**.
- Materializer отказал непустому output и неправильному B12 до записи: **2/2**.

Эти результаты получены сохранённым portable runner из свежего exact B13. Кандидат оставался неизменным. Наборы частично пересекаются; не складывать их как число уникальных функций.

**Три старых test-файла потребовали явной QA-only адаптации к намеренно изменённому вызову.** Два изолированных harness теперь предоставляют executeServiceCommand, проверяют service == wordstat и передают управление прежней fixture. Одна source-marker assertion требует новую строку вместо удалённой legacy-строки. Поведенческие assertions не удалены/ослаблены. Первичный неадаптированный B13 запуск 111/118 с семью ошибками сохранён, а не переименован в PASS. Остальные исходные тесты не менялись.

Финальные 78 assertions на неизменённом B12: 57 PASS / 21 FAIL — последствия двух найденных корней, не 21 независимый дефект. На исправленном B13: 78/78. В раннем тестовом черновике два поиска слов null/true по всему отчёту ошибочно ловили легальные metadata; QA исправлен на точное безопасное сообщение. Этот черновой журнал сохранён отдельно от product RED.

Запуск исходных suites ограничен двумя процессами, 10 сек/test и 25 сек/process, Node heap 256 MiB. QA guard запрещает случайные fetch/http/https/net/tls/dgram вызовы; намеренные test fixtures сохраняются. Это не OS sandbox и не измерение памяти Chrome.

## 6. Browser harness найден, но старый PASS не перенесён

Восстановлены 8 browser scripts и 2 campaign runners с hashes, известными invocation shapes и prerequisite в `qa/browser_harness_recovery.json` внутри QA-архива. Прочитаны PHASE5_DIRECT_R2_CODEX_COMPLETE_PASS_2026-08-27 и PHASE8_SEARCH_BATCH_FINAL_ACCEPTANCE_2026-08-28.

Эти успешные отчёты относятся к старым точным кандидатам. Старый полный runner содержит старый frozen target, а отдельный Search browser harness меняет тестовый manifest.key. Их нельзя слепо выдать за проверку B13. Ни одного нового Chrome/DOM/real-IDB/resource PASS в этом блоке нет.

## 7. Сохранение, полные журналы и восстановление

Кодовые deltas: B13_WORDSTAT_RESPONSE.diff и B13_WORDSTAT_BATCH_ROUTE.diff. Их pre/post SHA и все QA inputs закреплены в B13_INPUTS.json (SHA `d9ba56c114becbd0945e20de523f1a53dd6150d94a7ec17f1fd5b6b88ac7d3a8`).

`qa/B13_QA_INPUTS.tar.xz` — 9620 bytes, SHA `63fab734f99c7bedae6c34b19b42957299eeac34572f2714d93e7d4550ba146b`, Git blob dd480492552c00129171515cd38fa7d5a57009a5. Содержит исполняемый новый тест, сеть-guard, полный inventory, harness map, три точных QA adaptation diffs и внутренние hashes. Это не установочное расширение.

`qa/prepare_b13.py` — SHA `97beb82b83fef17b54662f39b8e7a245b015403341d2fa4a4756780cb328864c`.
`qa/b13_available_campaign.py` — SHA `79a48c45900c9587c9f11d696065f8501a9cbc3d9f28c73ec8d764310cc92651`.
Шесть source/delta/test/materializer/manifest файлов прочитаны обратно на ec402575a31274ac418efbabb49f083166a34387; Git blob совпали с локальными проверенными байтами.

Полные журналы опубликованы как восемь точных бинарных частей в `evidence/B13_RAW_LOGS/`. Это транспорт исходного архива, не пересоздание или сокращение логов. MANIFEST.json и restore.py собирают точный B13_RAW_LOGS.tar.xz: **45312 bytes**, SHA **abd3a1c68e1e356afda0b8cf7d3863de83849d4515ca8d63219affc810a9b019**. Проверены 168 members, 167 внутренних hashes, отказ повреждённой части и запрет перезаписи. Архив содержит полные исходные/финальные TAP, stderr, RED, QA draft failures, original inventory и results. Owner не используется для переноса QA-файлов.

```text
python qa/prepare_b13.py EXACT_B12_QA EMPTY_B13_QA
python qa/b13_available_campaign.py EXACT_SOURCE_REPO OWNER014 EXACT_B13_QA EMPTY_LOGS
python evidence/B13_RAW_LOGS/restore.py NEW_EVIDENCE_OUTPUT.tar.xz
```

## 8. Следующая точка и ограничения

A/B1–B13 не строить заново. Использовать сохранённый B13. Полная инвентаризация оригинальных тестов закрыта; следующая работа — подготовка точной финальной квалификации и исполнение оставшихся доступных PD требований по восстановленному harness, а не ещё один цикл новых функций. Не объявлять development-run независимой Codex приёмкой.

Открыты: реальный Chrome/DOM/MV3/IDB и combined-memory; точная разрешённая activation/provider capability; независимый полный PD gate; финальная упаковка/identity. Сетевой deferred host всё ещё выключен. Сам факт найденного старого browser runner не устраняет текущую административную блокировку.

**RELEASE_ALLOWED = NO. INDEPENDENT_GATE = NOT_RUN. INSTALLABLE_ZIP = NOT_CREATED.**

Простыми словами: весь исходный Node-набор теперь проверен. Дополнительная проверка выявила два старых дефекта Wordstat; они исправлены точечно, зависимости перепроверены, исходники и полные журналы сохранены. Безопасность установленного Chrome этим не доказана.
