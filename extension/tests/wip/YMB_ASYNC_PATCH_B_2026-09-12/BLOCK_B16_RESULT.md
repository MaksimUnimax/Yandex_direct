# B16 — popup, CodeMirror, navigation, extended memory and browser-profile restart

2026-09-12. Ветка wip/ymb-file-delivery-patch-a-2026-09-12.
**Описанная браузерная матрица выполнена. Ошибка прикрепления в другой диалог исправлена и перепроверена. Независимый полный PD gate не выполнен. RELEASE_ALLOWED = NO.**

## Продолжение и точный вход

Начальный live HEAD 625fdb7fc70d7c931269eee7e029c1d8f69dcae3. Прочитаны B15/cursor/coverage и обязательные resource/PD authorities. Взята готовая B15-сборка из artifact10297798297, run34695092346; outer SHA7e413dc26f1416f1dba2b9f9864502687f0a8a9b0b6aa8e11e5380cfa8530080,248604bytes,23внутренних hashes. Не пересобирались A/B1–B15. Первый B16 запуск проверял неизменённый B15 ZIP d4bdf57268ac904421797d7aad428c47981cee4c870bc549909696479f91ace9.

Код QA, запуск, реальные ошибки, ограниченное исправление, Node RED/GREEN и промежуточный cursor сохранялись в Git до итогов. Основная roadmap-ветка, extension/src и клиентские данные не менялись.

## Реальный navigation defect и исправление

Первый Chrome run34696587164 держал ответ последней части файла, переключал URL диалога через SPA history, затем возвращал уже полученную часть. Старый файл попадал в file input нового диалога:1change вместо0. Worker отклонял последующий mark по CONVERSATION_MISMATCH; Send не происходил. Это подтверждённое нарушение изоляции DOM, не реальная загрузка на сервер ChatGPT и не provider replay.

Корень: runtime/DOM element оставались живыми после SPA navigation. Их проверка не доказывала сохранение conversation ownership после await. Добавлен контроль подтверждённого conversation_key после получения/проверки частей, после ожидания commit и перед File/DataTransfer, composer и Send. Заменённый file input также отклоняется. Ошибка сохраняет durable outbox/evidence, не повторяет provider или attachment.

Изменён только file_delivery_content.js. Preimage baa1729159812f4c70e24498ee269ea7939f86ffb5094a19a5520eec9d47e9e7; postimage655702fa5025e2a4dc87b2d2bb6647cf3b9c69bee88f4017150b35e8f511a9f2. Остальные66файлов идентичны B15. Новых payload-копий, timers/observers, storage schemas, permissions, версии и сетевой активации нет.

## Отдельно — исправления тестовой fixture, не продукта

Первый popup-тест ошибочно ожидал включённый prefix с пустым сохранённым текстом. Существующий normalizer намеренно выключает такой prefix; fixture теперь заранее сохраняет непустой текст. Из-за раннего отказа AutoSend оставался OFF и влиял на CM-сценарий; CM теперь задаёт собственное состояние. Тестовая задержка последнего chunk не была одноразовой и блокировала следующие большие файлы; исправлена на одноразовую. Первые resource/profile timeouts поэтому не являются доказательством утечки. Исходные журналы сохранены, не переименованы в PASS. Первый xvfb cleanup warning отдельно от product assertions; owned Chrome процессов не оставалось.

## Точный повтор в настоящем Chrome

Run34697155008 завершён success. QA source97d808b71cd9f9242b3ee19f37210d2abb500f61, workflow commit65b202a2dedcca90a06354f20f2fbf5bfcc7b019. Среда: GitHub ephemeral runner, CfT152.0.7977.75/Puppeteer25.10.0, locked npm dependency tree из B15. Один CLI install на процесс, без изменения manifest.key. Три последовательных кампании создают/завершают только собственные профили. Локальные политики и профиль владельца не затронуты.

- **16/16 primary markers:** реальный content/Native Copy,1/10/32/64/64/64MiB через IDB->chunks->File/DataTransfer->ready->Send->ACK->cleanup; occupied composer; actual worker termination; полный10/100/500/1500item lifecycle.
- **10/10 supplemental markers:** прежний двойной Send, повреждённый chunk, reload без повторного attachment, настоящий restart посреди1500с полным raw reconciliation, ещё три64MiB с idle. Одна отдельная строка memory observations, не дополнительный PASS.
- **12/12 B16 markers:** две проверки настоящего popup (toggles/несохранённые поля и явные Save/reopen), PRE раньше Copy/смена native control/Manual OFF-ON, readonly-CM shape/full block/local start/detach, чужой диалог и64MiB, тот же navigation RED теперь0attachment/0Send, защита активной операции от Manual OFF,8полных64MiB cycles, закрытие/новый запуск Chrome с тем же выделенным профилем. В число12входят identity/cleanup, не12уникальных пользовательских функций. Восемь строк retained metrics — наблюдения, не PASS markers.

Readonly-CM DOM форма соответствует адаптеру, но настоящая библиотека CodeMirror не загружалась. Страница синтетическая, не текущий серверный UI ChatGPT. Реальные browser File/IDB/popup/extension messaging проверены; живого upload и запросов Яндекса нет.

В profile-сценарии Chrome действительно закрыт, затем создан новый PID и новая worker session. Сохранённый raw прочитан, готовое вложение не прикрепляется и не отправляется повторно, новая вкладка не получает незаметно права старой.

## Память — измеренные границы

Sum RSS дерева Chrome каждые250ms и в контрольных точках; общие страницы могут учитываться повторно. Это не private memory расширения. Peaks: primary1826084KiB, supplement1854732KiB, B16remaining2028924KiB (~1981.37MiB). Порог аварийной остановки2048MiB не достигнут, однако близость к этому порогу не скрывается. Forced GC не использован. После финального cleanup живых наблюдавшихся owned PID нет.

После восьми64MiB файлов с5s idle RSS(KiB):1843932,1687948,1889892,1670392,1670340,1868052,1677480,1670768. Рост не монотонный. Page JS heap после прогрева около14.0–14.7MB; DOM nodes58->57 и затем57; DOM event listeners во всех восьми точках7. File in-flight и Send in-flight множества пусты, ручной Send handler отсутствует после каждого цикла. Worker backing storage на отдельных точках доходил до70423551bytes, затем падал до1479690bytes без принудительного GC; данные не накапливались на64MiB за каждый цикл.

Это подтверждает ограниченность именно выполненной серии и отсутствие наблюдаемого накопления этих счётчиков, **не** абсолютную leak-free гарантию для любой страницы/машины или воспроизведение старого OOM владельца.

## Честная граница отмены

Для занятой64MiB доставки настоящий popup запрещает Manual OFF, а прямое сообщение возвращает MANUAL_OPERATION_ACTIVE и сохраняет outbox. Так проверена защита активной операции, **не пользовательская отмена файла**. В текущем кандидате отдельной UI-команды отмены файловой доставки нет. Тестовый clearOutbox не выдаётся за такую функцию. Navigation/dispose/reload останавливают повторные side effects, но не считаются решением всех вопросов пользовательского освобождения зависшей доставки.

## Зависимости и точная упаковка

| Изменённая связь | Выполнено на новом кандидате | Не заменяет |
|---|---|---|
| conversation identity -> awaited commit/chunk/hash -> DOM |10новых exact-function cases:2PASS8FAIL->10PASS; прежние9Send с необходимой identity fixture;19/19локально и CI | Все варианты реального сайта |
| content -> binary store -> File -> Send/ACK | Полный повтор primary+supplement file/resource matrix | Live ChatGPT upload |
| popup/Manual/nativeCopy/CM/navigation/owner |9содержательных B16 сценариев+identity/cleanup; без ослабления assertions | Полный independent PD-00..17 |
| профиль -> browser close/reopen -> raw/outbox | Реальное закрытие/новый запуск с сохранённым QA профилем | Power loss/OS crash |
| source -> package -> clean consumer |67files/66unchanged,61JS syntax; exact package local==CI;3negative producer cases | Final release decision/permission activation |

Новый внутренний ZIP223870bytes, SHA256dd6d1ef016d4df3d9b4789cd2806f4d0a36202f93c4655e196e2eeda439f7c73; tree83ae1351ab057f7cd768243c91060d2dc77e8fe0f5b378055437e47a110012b7. Использован прежний точный ZIP и packer с прежними69entries/metadata, изменён только один файл. Неверный исходный ZIP, diff и существующий output отклонены до записи:3/3. Node19:fail/cancel/skip0; CI66.411732ms. Все61JS прошли syntax.

## Постоянные источники и готовое продолжение

qa/B16_CORRECTION_INPUTS.tar.xz:8184bytes SHA219b105f09de867a9ccd804c6001183dbbba0805726bba39ce4908585359df11,blob907d8c2af66752c4ea1222e1c0029fd16b84a7d8. Содержит exact diff/producer/tests/RED/GREEN/fresh19 и hashes. CI прочитал эти закреплённые bytes и проверил до запуска. Producer SHA194364dfc5327aba566ec2e70b92e5b054ec091922e90b25d8f97572f582a090.

Готовый Actions artifact10299370922, run34697155008:261464bytes SHA987605e376ba0fafb6ef26adcaa42c350d41ccd826fd2d6a662ecaa3ddf9f638, retention до2026-12-11T13:42:11Z. Скачан обратно;26внутренних hashes и весь новый ZIP совпали. Внутри уже готовый исправленный пакет, исполняемые3browser QA/scripts и raw logs. Не пересобирать A/B1–B16. Старый B15 package после navigation defect не текущий.

evidence/B16_RAW_LOGS содержит2точные бинарные части+manifest+restore.py для полного журнала17076bytes SHA1fecb1a8a7966cdd8a3262ab056a5028bcd22977d4568f70feefaeb44afcf574. В архиве39members,38checksums; полные первый browser RED и три final browser/RSS/stdout/stderr, Node RED/GREEN и package negatives. Повторяющийся QA-код сохранён отдельно, в журнале его hashes. Consumer round-trip прошёл; повреждённая часть и перезапись отклонены2/2. Это архив журналов, не установочный код.

Следующее: свести итоговую исполнимую PD-карту по exact B16, явно разрешить контракт остановки/отмены зависшей доставки, проверить только реально недостающее, затем отдельная независимая Codex кампания. Не добавлять функции без подтверждённого обязательного пробела/дефекта и не перезапускать уже доказанные наборы на тех же байтах. Operation-host остаётся выключен; включение/авторизованная provider-проверка — отдельное решение. Нет owner-installable handoff.

Источники API, перепроверенные при подготовке: pptr.dev/guides/chrome-extensions; chromedevtools.github.io/devtools-protocol/tot/Memory/; developer.chrome.com/docs/extensions/develop/concepts/storage-and-cookies. Они обосновывают тестовые инструменты/семантику, а не безопасность нашего продукта; последняя подтверждается только указанными фактическими сценариями.

**RELEASE_ALLOWED = NO. INDEPENDENT_GATE = NOT_RUN.**
