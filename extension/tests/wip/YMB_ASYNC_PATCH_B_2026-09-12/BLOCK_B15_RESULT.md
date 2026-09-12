# B15 — настоящая файловая доставка, перезапуск и 1500 записей

Дата: 2026-09-12. Ветка: wip/ymb-file-delivery-patch-a-2026-09-12.
**Названная браузерная матрица выполнена. Найденный двойной Send исправлен и перепроверен. Это не независимый полный PD gate. RELEASE_ALLOWED = NO.**

## 1. Точный вход и сохранение

Начальный live HEAD f31baa4f578f66330aeb0fad23942487eff0f639. Прочитаны cursor B14, обязательные resource/PD правила и сохранённый launcher. Использован уже готовый скачанный B14 bundle, run34692833348/artifact10298216105, SHA256 4c5fb564fcb3fa586f6e779e7120f89ca5ee352a4bf8fdd59e335db8a45018b9. Все пять внутренних hashes проверены. A/B1–B13 не переписывались и не пересобирались цепочкой materializers.

Исходный пакет:223380 bytes, SHA256 e260f35b1d7decf02c18c46103b4072de68270c2bce09e2f51f7462941c48f97; дерево f591b39a381993c44284561236b9c5a278761db3d6b04059c59974e037c33f47.

Код QA, fixture, workflows, первичные результаты, конкретный RED, исправление и cursor сохранялись отдельными коммитами до этого итогового отчёта. Основная roadmap-ветка, extension/src и клиентские данные не изменялись. Реальных ключей и запросов Яндекса нет.

## 2. Отдельная ошибка тестового запуска

Первый run34694466079 остановился на Chrome dispatcher `No SW` до новых DOM/file assertions. Он сохранён как FAIL_HARNESS, не дефект продукта. В launcher одновременно применялись enableExtensions:[path] и CLI --load-extension; официальный исходник Puppeteer25.10 показывает, что array дополнительно вызывает installExtension. QA-only b15_single_install.py оставляет один исторически использовавшийся CLI-механизм. Следующий run34694622852 прошёл все16 markers. Это подтверждённо работающая исправленная конфигурация; единственность причины предыдущего Chrome error не доказана. Production при этом не менялся.

Локальный административно блокированный Chrome не запускался, его политики не обходились. Использован доказанный отдельный GitHub-hosted Chrome for Testing152.0.7977.75 / Puppeteer25.10.0.

## 3. Реальный дефект двойного Send и ограниченное исправление

Дополнительный run34694861037 воспроизвёл: два быстрых ручных нажатия Send при готовом файле вызывали2 WS_COMMIT_ATTACHMENT_SEND и2 DOM Send. File/DataTransfer change и ACK оставались по одному. Это actual product assertion 2 != 1 в настоящем Chrome с controlled DOM, не OOM и не повторный provider.

Причина: file_delivery_content.js не блокировал повторный вход в commitAndClick во время await и не отличал already_committed от нового разрешения кликнуть. Оба обработчика вызывали button.click после ответа.

Изменён **ровно один production-файл — file_delivery_content.js**. Добавлен небольшой send_in_flight Set по delivery_id, который очищается в finally. Второй вход не посылает второй commit; already_committed только наблюдается; запоздалый ответ уничтоженному runtime или отсоединённой кнопке не вызывает клик. Нового payload, provider, storage schema, polling или таймера нет. Остальные66файлов идентичны прежним. Permissions, версия и сетевая активация не менялись.

Preimage SHA256 c8fcf6d36a0573b9134b90edc35efdf988b8d178e3649bc3d116c7c02cf262bf.
Postimage SHA256 baa1729159812f4c70e24498ee269ea7939f86ffb5094a19a5520eec9d47e9e7.
Diff:evidence/B15_SEND_GATE.diff, SHA256 7d15e8edfb11275e9d5a6a7bb934c79adfa2c8d47589b246d6c38a73788fee72.

Целевые9 Node/VM assertions на точных функциях: исходник3PASS/6FAIL, исправление9/9. В первом черновике fixture оставила2 promises pending; исправлено завершение fixture, финальный RED имеет0cancelled. Оба журнала сохранены. Эти проверки дополняют, а не заменяют browser RED/GREEN.

## 4. Полный повтор затронутой браузерной матрицы на новом пакете

Run34695092346, source223aa0ec762f5789062daefe865dec54d2a8e348. Реальные content script, extension messaging, worker и IndexedDB; DOM страница синтетическая, provider outcomes искусственные. Никакого настоящего upload на ChatGPT или обращения к личному профилю.

### Основной прогон — 16 PASS markers

- Native Copy не запускает Bridge; двойное нажатие Яндекс запускает один локальный start, один Send и ACK.
- Полная цепочка stage -> IDB -> 256KiB chunks -> File/DataTransfer -> ready -> Send -> ACK -> cleanup на1/10/32/64/64/64MiB. Один input/change/Send/ACK на файл. File.stream реально прочитал все байты и проверил ожидаемый x-pattern. Chunk messages4/40/128/256/256/256. Meta отсутствует и chunks=0 после каждого завершения.
- Занятый пользовательским текстом composer не перезаписывается. При auto-send off отправки нет до явного клика.
- WebWorker.close действительно завершил target. После нового worker session сохранены raw и UNKNOWN, новая отправка запрещена. Уже готовое вложение не прикрепляется повторно; ручная отправка завершается после restart.
- В реальной IndexedDB выполнен полный поэлементный цикл10/100/500/1500. Итоговые индексы/статусы сверены полностью. Это локальные записи с синтетическими результатами, не1500запросов Яндекса.

| Items | Time ms | Reads | Writes | Max job JSON chars |
|---|---:|---:|---:|---:|
|10|88|134|151|597|
|100|881|1304|1501|609|
|500|4384|6508|7501|615|
|1500|13109|19518|22501|626|

### Дополнение — 10 PASS markers и отдельная строка наблюдений

Тот же ранее падавший двойной Send теперь даёт ровно1commit/1click. Повреждённая часть останавливает доставку до DataTransfer, не запрашивается повторно автоматически. После reload с исчезнувшим DOM-вложением нет повторного attachment/send; сохранённый файл удерживается до явного test cleanup. Test cleanup не выдаётся за проверку пользовательской кнопки отмены.

Настоящий worker restart посреди1500 items сохраняет750полных raw, переводит1SUBMITTING в UNKNOWN и отменяет749pending. Все1500индексов и все750raw перечитаны. Учтённые751попытка не обнуляются, replay отсутствует. Проверены pause/resume перед работой и cancelPending после восстановления.

Ещё три64MiB file cycles выполнены с5секундами idle после каждого. Принудительного GC нет. Два browser-прогона последовательны, каждый создаёт и завершает только собственный Chrome. Во всех финальных logs failed=0, errors=[], remaining owned processes=0. Числа markers включают identity/cleanup и не выдаются за количество уникальных функций.

## 5. Память — факты и ограничения

Измерялась сумма RSS дерева процессов Chrome каждые250ms и в контрольных точках. Это весь QA Chrome с дочерними процессами, не отдельная private memory расширения; shared pages могут считаться дважды.

Максимум основного прогона1905960KiB (~1861MiB), дополнительного1827840KiB (~1785MiB). Аварийный предел2048MiB не достигнут. После трёх64MiB основного прогона1639196/1645288/1900844KiB; эти три точки растут, поэтому они НЕ объявляются доказательством отсутствия утечки. В дополнительном прогоне после5s idle:1516936/1711108/1644052KiB; рост не монотонный. После actual worker restart RSS существенно снижается. Нельзя переносить эти измерения на все реальные страницы и компьютеры или заявлять всеобщую leak-free гарантию.

Доказаны: полный завершившийся объём, ограничения чтений/малых метаданных, отсутствие full-store read per chunk в проверенной цепочке, удаление доставочных IDB данных, ограничение аварийного теста и отсутствие оставшихся owned процессов. Непроверенные resource/PD случаи остаются открытыми.

## 6. Зависимости и упаковка

| Затронутая связь | Доказательство после исправления | Граница |
|---|---|---|
| Manual/AutoSend -> async commit -> click |9Node cases + real browser single/double Send; delayed/disposed/disconnected Node replies|Реальный сервер ChatGPT не использовался|
| Content -> outbox -> chunk transport -> File/DOM -> ACK |Полная повторная file matrix и corrupt-chunk/reload|Все виды файлов/DOM/ошибок не объявлены покрытыми|
| Content recovery -> новый worker -> IDB |Actual target close, existing attachment watch-only,750/1500partial state/raw|Не power-loss/OS-crash durability|
| Новые метаданные -> ресурсы |Set очищен; реальная file/resource матрица повторена; нет новых payload copies|Не универсальное отсутствие всех утечек|
| Exact package -> installed tree |67file hashes до/после, один diff,66unchanged,61JS syntax|Независимый полный PD gate ещё впереди|

Новый internal QA ZIP:223544bytes, SHA256 d4bdf57268ac904421797d7aad428c47981cee4c870bc549909696479f91ace9.
Дерево:7b4db94a527778722ee9bbd7b0d131789128dcaee78451f5886a7bddf1ae183a.

qa/b15_prepare_fix.py применяет только exact diff поверх уже готового B14ZIP. Сохраняются все69канонических ZIP entries и их метаданные/порядок/сжатие, кроме закономерно изменившихся CRC/размеров единственного файла. Две локальные сборки и CI дают один ZIP. Неверный исходный ZIP, повреждённый diff и существующий output отвергаются до записи:3/3. QA не вносится внутрь production.

CI artifact10297798297 скачан обратно:248604bytes, SHA256 7e413dc26f1416f1dba2b9f9864502687f0a8a9b0b6aa8e11e5380cfa8530080. Проверены23внутренние контрольные суммы, архив и полное совпадение ZIP с локальными байтами. Там находится готовый исправленный пакет и полные новые журналы; срок хранения до2026-12-11T12:57:40Z. Старый B14bundle остаётся источником готового QA workspace, не production-кандидатом после исправления.

## 7. Постоянное сохранение и следующий шаг

evidence/B15_ALL_RAW_LOGS.tar.xz содержит43файла,42внутренние контрольные суммы: первый NoSW, исходный primary PASS, supplemental product RED, исправленные оба browser-прогона/RSS/stdout/stderr, точные QA-target records, Node RED/GREEN и отрицательные package checks. SHA256 d5bbb3828c31d649d917e7357e8dfd9c2fbdf418259ff4f7d40899841f3d3a9f,13736bytes, Git blob83816b4ccf836392dba69be25da568ed355bf07e. Это полные журналы, не установочный код. Исходники/diffs/fixtures/workflows также сохранены в Git.

Продолжать с новым готовым exact пакетом. Не возвращаться к разработкеA/B1–B14, не выдавать старый e260-пакет после найденного дефекта. B16 — окончательная карта ещё не пройденных PD требований и подготовка/выполнение независимой приёмки в уже работающем venue, без новых функций. Остаток не скрывать: полный popup/CodeMirror/navigation/security matrix, оставшиеся применимые cancel/resource/перезапуск-браузера случаи, независимый Codex verdict и разрешённая активация отложенного сетевого маршрута. Текущий operation-host выключен.

Источники проверки QA: официальный Puppeteer25.10 BrowserLauncher.ts/WebWorker.ts; Chrome guide test-serviceworker-termination-with-puppeteer. Они поддерживают способ запуска/остановки; безопасность конкретного кандидата оценивается по его собственным логам. Более ранние тесты не переименованы в независимый gate.

**RELEASE_ALLOWED = NO. INDEPENDENT_GATE = NOT_RUN. USER_PROFILE_TOUCHED = false. REAL_PROVIDER_CALLS = 0.**
