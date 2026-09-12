# B16 — подтверждённый navigation defect и отдельные QA ошибки

2026-09-12. Точный B15 ZIP d4bdf57268ac904421797d7aad428c47981cee4c870bc549909696479f91ace9. Первый browser run 34696587164, artifact10298732359, 19541 bytes, SHA256 c59c55a3f34281a8191e810f033125685c75c4adb4aa175d5e2f607efe880d21. Скачан обратно, внутренние hashes проверены.

## FAIL_PRODUCT: файл старого диалога попадает в новый до отклонённого ACK

Сценарий держит только ответ последней части в тестовом transport, делает SPA history navigation, затем возвращает уже полученную часть. В настоящем Chrome DataTransfer/change сработал один раз в новом диалоге вместо нуля. Поздний WS_MARK_ATTACHMENT_READY отклонён worker по CONVERSATION_MISMATCH, но сам файл уже попал в другое поле. Это не отправка provider и не доказанная загрузка на сервер ChatGPT, однако изоляция DOM уже нарушена.

Корень: file_delivery_content проверял живость runtime/element, но не текущую принадлежность диалогу после await. SPA может сохранить те же DOM элементы. Нужен контроль conversation_key на границах ответов/хэширования и непосредственно перед File/DataTransfer/composer/Send. Отказ оставляет durable outbox, без повторной покупки/прикрепления.

Точные функции дополнительно воспроизведены в Node: 10 assertions, 2 PASS / 8 FAIL, cancelled0. Ограниченный локальный кандидат меняет только file_delivery_content.js; те же 10 дают PASS. Это ещё не повторная browser-приёмка.

## Не смешивать с ошибками QA

1. Тест popup ожидал включённый prefix при пустом сохранённом тексте. Существующий normalizer выключает пустой prefix; исправляется начальная fixture (непустой уже сохранённый текст), а не production.
2. После неудачной popup assertion fixture оставила Auto Send OFF; последующий CM-сценарий дошёл до claimed outbox, но тест ожидал auto-send. Следующий запуск задаёт своё состояние независимо.
3. Тестовый перехват последней части не был одноразовым и повторно задержал часть следующего большого файла. Resource/profile timeouts этого запуска не являются доказательством утечки или нового дефекта продукта. Нужна одноразовая инъекция и повтор реально неисполненных сценариев.
4. xvfb-run сообщил cleanup warning после завершения Chrome. В product логе owned processes=0; это не product memory FAIL.

## Точная матрица ограниченного исправления

Changed file -> fetchArtifact / processClaimed / stageMarker / processReady / commitAndClick -> после await и до DOM side effects -> текущий confirmed conversation key + runtime/element liveness. Shared storage, provider, manifest, permissions, version и остальные66файлов не меняются. Новых payload копий/таймеров/observers нет.

Обязательно: те же navigation/late-commit Node и browser assertions; прежние9send assertions с только недостающим identity fixture; полная затронутая file1/10/32/64/64/64 и supplemental restart/corruption matrix на новом exact ZIP; B16 popup/CM/ownership/repeated metrics/profile. Не выдавать прежний B15 package как текущий после найденного дефекта.

RELEASE_ALLOWED = NO
NEXT = сохранить точный diff/tests; перепроверить исправленный пакет в Chrome.
