# B15 — основной браузерный прогон сохранён, дополнение продолжается

Run 34694622852, workflow commit 87295afe266f9c58d166e71c2b9d0f3047ef20c9. Artifact 10297707924 скачан и проверен: 19957 bytes, SHA256 3017ac5718c43422b0e461e6a106dc2ec0e3c0c44f7e0e9786188ee4715f78c1. Все внутренние SHA256SUMS совпали; stdout/stderr и effective QA scripts сохранены. Chromium152.0.7977.75 / Puppeteer25.10.0.

После замены только двойного способа установки на один исторический CLI-механизм No SW больше не возник; все 16 markers PASS, failed=0, errors=[], owned processes left=0. Это подтверждает работоспособность исправленного QA launcher, но не доказывает единственную возможную причину прежнего Chrome dispatcher error. Фailing run 34694466079 сохранён отдельно.

Пакет e260f35b1d7decf02c18c46103b4072de68270c2bce09e2f51f7462941c48f97 не пересобран, все 67 production-файлов неизменны до/после.

## Достигнутые assertions

- Настоящий content script на controlled chatgpt.com DOM: native Copy не запускает команду; двойное нажатие Яндекс запускает ровно один local Manual request, Send и ACK.
- Полная attachment-цепочка 1/10/32/64/64/64 MiB через реальную extension messaging, IndexedDB, File/DataTransfer и DOM. Ровно один input/change/Send/ACK на файл. Все байты считаны File.stream и проверены x-pattern; chunk calls=4/40/128/256/256/256. После каждого ACK meta отсутствует, chunks=0. Это controlled upload fixture, не настоящий сервер ChatGPT.
- Чужой текст composer не перезаписывается. При auto-send off нет автоматической отправки; явный Send завершает доставку.
- WebWorker.close действительно завершил старый target. Новая worker session отличается. Сохранённый raw остался, interrupted submission стал UNKNOWN, новый submit запрещён. Уже прикреплённый файл не прикрепился повторно; ручной Send/ACK завершил доставку после restart.
- Реальная IDB: полный цикл 10/100/500/1500 записей. Все индексы и SUCCEEDED сверены полностью. Reads=134/1304/6508/19518; writes=151/1501/7501/22501; max job JSON 597/609/615/626 chars. Время=90/897/4539/13430ms. Сетевые исходы искусственные, платных запросов нет.

## Память — только измеренный факт

Суммарный RSS дерева Chrome, sampled250ms: peak1930144KiB (~1884.9MiB), аварийный предел2048MiB не достигнут. После трёх 64MiB циклов1814324/1614612/1850124KiB. После actual worker restart1329496KiB. Принудительный GC не использовался. Общая RSS учитывает весь тестовый Chrome и может повторно учитывать shared pages. Эти наблюдения не объявлены полным доказательством отсутствия утечек.

Осталось внутри текущего блока: отдельные controlled failure/cancel/page-reload и pause/cancel/restart large-job сценарии, усиленное наблюдение repeated-file cleanup. Успешные неизменённые assertions не отменять и не переписывать. Production-изменения только после конкретного воспроизведённого дефекта. Independent PD gate по-прежнему отдельно.

RELEASE_ALLOWED = NO. LIVE_PROVIDER_CALLS = 0. USER_PROFILE_TOUCHED = false.
