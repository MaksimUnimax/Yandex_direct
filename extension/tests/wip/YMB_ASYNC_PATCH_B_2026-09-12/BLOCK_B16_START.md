# B16 — оставшееся браузерное покрытие, начало

2026-09-12. Live base: 625fdb7fc70d7c931269eee7e029c1d8f69dcae3. Прочитана B15 coverage authority и сохранённые resource/PD правила.

Уже имеющийся готовый B15 artifact проверен локально: 248604 bytes, SHA256 7e413dc26f1416f1dba2b9f9864502687f0a8a9b0b6aa8e11e5380cfa8530080, все 23 внутренних hashes совпали. Точный ZIP d4bdf57268ac904421797d7aad428c47981cee4c870bc549909696479f91ace9, 223544 bytes. Production tree 7b4db94a527778722ee9bbd7b0d131789128dcaee78451f5886a7bddf1ae183a. Нет повторной сборки A/B1–B15, новых функций или production-правок.

## Следующая ограниченная работа

На доказанном single-install GitHub CfT/Puppeteer venue проверить: popup toggle/Save/reopen; PRE/readonly-CodeMirror и независимость native Copy; mutation/navigation/ownership; явная отмена большой доставки; длительнее повторные файловые циклы с RSS, JS heap, DOM/listener counters; закрытие и запуск того же выделенного профиля для проверки сохранности. Сценарии используют сохранённые fixture и launcher. Не использовать профиль владельца, реальные credentials, provider calls или live upload.

QA будет сохранять отдельный результат каждого сценария. FAIL_HARNESS/неверное предположение fixture не превращать в product bug. Если обнаружен реальный дефект — сохранить RED до bounded correction и повторить затронутые зависимости. Старые scoped PASS не называть новой независимой приёмкой.

## Scope / зависимости

На старте меняется только QA: точные bytes/manifest неизменны. Проверяемые связи: popup->settings->worker; DOM adapter->external control->Manual ownership; content->outbox->File->ACK/cancel; storage->whole-browser restart; per-cycle retained memory. Обязательные независимый gate и activation decisions не отменяются.

Официальные источники перепроверены: pptr.dev/guides/chrome-extensions (popup и content realms), chromedevtools.github.io/devtools-protocol/tot/Memory/ (DOM counters; не использовать prepareForLeakDetection как незаметный GC), developer.chrome.com/docs/extensions/develop/concepts/storage-and-cookies (origin/persistence). Источники обосновывают тестовый API, не безопасность продукта.

RELEASE_ALLOWED = NO
CURRENT = B16_IN_PROGRESS
NEXT = сохранить исполняемые QA-сценарии и запуск на готовом B15 artifact.
