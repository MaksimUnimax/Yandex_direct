# B14 — точная упаковка, передача QA и работающий настоящий Chrome

Дата: 2026-09-12. Ветка: wip/ymb-file-delivery-patch-a-2026-09-12.
**Квалификация пакета и ограниченного браузерного пути выполнена. Полный независимый PD gate не выполнен. RELEASE_ALLOWED = NO.**

## Точный вход и сохранность

Начальный live HEAD: c828c2ea2a7e412207f7cf7078f48b30919435c5. Прочитаны cursor, B13, обе карты покрытия и обязательные resource/PD правила. Производственное дерево B13: f591b39a381993c44284561236b9c5a278761db3d6b04059c59974e037c33f47, 67 файлов/61 JS. Все 67 файлов остаются прежними. Ни одной новой функции или production-правки в B14 нет. Manifest, версия, permissions, credentials и данные заказов не менялись.

Точные исходники восстановлены существующим read-only workflow и сохранёнными materializers, не переписаны. Обнаружено, что все 53 исходных owner014 файла уже существуют как Git blobs; они закреплены деревом 72bc1d60b8763448d24ff72c2352bbe5b5551bd6 в qa/b14_inputs/owner014. Их SHA проверяются по прежнему baseline manifest. Теперь отсутствие загруженного ZIP в новом чате не заставляет искать его или просить владельца переносить файлы.

## Упаковка и точная передача

Переиспользован канонический packer из qa/e13a-exact-reconstruction-v3, blob 171a3c99d0c3fb5454a5bc5423c7b4cc5e2da576; SHA256 fc0555f8ae60b67e2128e994127398ee0ccd9438b13b57fffd80b1834b62dd62. Его pack/make_info не изменены. Wrapper задаёт только новый корень и число файлов. Метаданные ZIP/порядок/права/сжатие фиксированы старой проверенной реализацией.

Создан **внутренний QA ZIP**, не разрешённая сборка для владельца:

- 223380 bytes, SHA256 e260f35b1d7decf02c18c46103b4072de68270c2bce09e2f51f7462941c48f97;
- 67 файлов; корень ymb-b13-internal-qa-not-for-installation;
- две сборки совпали; после распаковки все 67 файлов совпали с B13;
- 14 проверок guard прошли: повреждение/усечение, лишние и дублирующиеся пути, traversal, неверные байты/метаданные, неправильное дерево и symlink отвергаются;
- сохранённый B13 runner заново прошёл на распакованном пакете: original132, Wordstat/Debug/backup78, full99, modules254, export84. Наборы пересекаются, это не число уникальных функций.

Одна ошибка QA: при первом staging забыли корневой QA_INPUTS_README.txt, и старый runner остановился до product assertions. Исправлен wrapper, который сохраняет все корневые QA-файлы; отдельная проверка проверяет их hashes. Production и старые assertions не изменялись.

Затем та же квалификация реально выполнена на GitHub Actions: run 34692833348, pinned source 652cf5ab4e203fbc2ca87492037ae9d12cf3b221. Python3.12.3/Node22.16.0 дали тот же ZIP, что локальная Python3.13. Все названные suites и 14 guards прошли. Artifact 10298216105 скачан обратно; проверены outer SHA, 5 внутренних hashes, ZIP и 67 файлов, exact QA workspace и полные журналы.

Bundle: 487812 bytes, SHA256 4c5fb564fcb3fa586f6e779e7120f89ca5ee352a4bf8fdd59e335db8a45018b9. Внутри complete-logs.tar.xz со 134 полными файлами журналов и exact-qa-workspace.tar.xz. Retention до 2026-12-11T12:07:52Z; это не заявление о вечном хранении Actions. Скрипты/исходные Git objects/контрольные точки находятся в Git постоянно. Следующее продолжение скачивает этот готовый workspace, а не заново собирает A/B1–B13.

## Настоящий браузер больше не исключён из доступных проверок

Локальная административная блокировка не обходилась и локальный Chrome повторно не запускался. Вместо этого квалифицирован **другой разрешённый venue — одноразовый GitHub-hosted runner**, уже использованный для QA. В нём запущен один свежий Chrome for Testing 152.0.7977.75 через Puppeteer25.10.0. Launcher основан на восстановленных browser scripts; актуальный официальный Puppeteer API разрешает загрузку точного пути. Старое изменение manifest.key не переносилось: ID определяется по реально загруженному worker, файл manifest не меняется.

Run 34693351244 действительно завершился успешно. Перед запуском скачан уже существующий exact ZIP из run 34692833348, а не пересобран другой кандидат. Проверены хэши до/после. Реальные ключи не устанавливались, внешние DNS-запросы браузера запрещены; после подключения поставлен дополнительный fetch-guard. User-профиль и компьютер не затрагивались. Workflow имеет только read permissions.

Фактически выполнены:

- настоящий MV3 worker загрузил общую binding, async integration и artifact store; deferred network остаётся отключён;
- настоящий IndexedDB прошёл локальный сценарий двух items: WAITING + UNKNOWN после явной имитации прерывания, запрет новой submit и запрет чужого owner;
- файл создан, прочитан по частям, проверен SHA256 и удалён в реальной IndexedDB на 1/10/32/64/64/64 MiB;
- чтений chunks соответственно 4/40/128/256/256/256, ровно одно чтение записи на часть; максимум 262144 bytes;
- после каждого цикла meta отсутствует и число оставшихся chunks равно нулю;
- браузер завершён; живых наблюдавшихся owned PID не осталось.

Всего 11 отдельных PASS markers. Это ограниченная browser qualification, не все PD sections.

## Что измерено по памяти

Измерялся **суммарный RSS дерева процессов Chrome**, каждые 250ms и в контрольных точках. Он включает сам браузер и дочерние процессы; общие страницы могут учитываться несколько раз. Это не эксклюзивная память расширения и не пиковая private memory.

После готовности worker: 1014240 KiB (~990.47 MiB). Максимальная наблюдавшаяся сумма: 1380432 KiB (~1348.08 MiB). После трёх 64-MiB циклов: 1183060 / 1153572 / 1154448 KiB (~1155.33 / 1126.54 / 1127.39 MiB). Ограничение аварийной остановки теста 1536 MiB не достигнуто. Принудительный GC не использовался.

В этих трёх повторениях нет монотонного роста после каждого завершения. **Это не доказательство отсутствия всех утечек и не воспроизведение старого OOM владельца.** Здесь не выполнялись File/DataTransfer/content delivery, загрузка на ChatGPT, cancel/reload, настоящий worker termination или batch10/100/500/1500. Их полный resource gate остаётся открытым. Local state.recover с двумя workerId не выдаётся за реальное завершение процесса worker.

## Зависимости и доказательства

| Зависимость | Новое доказательство B14 | Открытая часть |
|---|---|---|
| Source -> canonical ZIP -> fresh extraction | 67 identities, metadata guard, deterministic local/CI package | Любые будущие version/permission/product edits требуют нового exact candidate |
| Git artifact -> fresh consumer -> reusable QA | Exact downloaded ZIP/workspace, 5 hashes, actual suites | Artifact retention ограничен; не заменяет independent acceptance |
| Real Chrome -> MV3 imports -> binding/store | Exact installed extension and ready objects | Full lifecycle, popup and DOM still required |
| Binary artifact -> real IDB -> chunks -> delete | Six measured cycles, checksums, no full-store read per chunk, cleanup | Полная цепочка File/DataTransfer/DOM и crash/cancel/reload |
| Per-item Search storage | Two-item real transaction/owner/UNKNOWN smoke | Полный large-job matrix и disk/restart durability |
| QA harness/dependencies | Puppeteer25.10 + CfT152 actually executed; lockfile archived | Full controlled DOM scenarios and independent Codex matrix |

## Сохранённые результаты и продолжение

QA code: b14_qualify.py, b14_package_test.py, b14_browser_venue.mjs. Pipeline definitions: ymb-b14-internal-qualification.yml и ymb-b14-browser-venue.yml. Промежуточные checkpoints и cursor записаны до следующего material block.

Browser evidence artifact 10298391517: 8124 bytes, SHA256 81eb38f26adadc303ad6a61b19d0807c336766410a8d30290779f209bb3de803; скачан, checksum-файлы проверены. Retention до 2026-12-11T12:19:18Z. В нём полный browser.jsonl, RSS samples, stdout/stderr, dependency lock и hashes. Дополнительно полные browser/RSS JSONL сохранены прямо в Git как B14_BROWSER.jsonl и B14_BROWSER_RSS.jsonl. Сводка B14_TEST_RESULTS.json содержит точные boundaries и обе run/artifact identity.

Новый доказанный launcher: qa/b14_browser_venue.mjs, SHA256 5da712a74db24e4a5baa59d5b0956ce9d6116e4cdf62d5d0333de65d59c8ff97. Не возвращаться к тезису «браузер вообще недоступен»: local venue блокирован, GitHub venue теперь доказан. Не переносить scoped PASS на непроверенные DOM/worker/batch случаи.

Следующий блок B15: использовать exact downloaded workspace/package и этот рабочий Chrome venue для недостающих controlled DOM/file delivery, worker restart и большой IDB/batch/resource матрицы. Не писать новые функции без фактического дефекта. Full independent Codex gate остаётся отдельно; QA prompt не выдан, поскольку все обязательные сценарии ещё не квалифицированы. Permission activation/provider capability и окончательный owner-release остаются отдельными требованиями.

Источники сверки: https://pptr.dev/guides/chrome-extensions ; https://pptr.dev/supported-browsers ; https://developer.chrome.com/docs/extensions/develop/concepts/service-workers/lifecycle ; канонический packer Git blob 171a3c99d0c3fb5454a5bc5423c7b4cc5e2da576. Официальный API поддерживает способ запуска/доступ к worker, но не доказывает безопасность нашего кода; её ограниченное доказательство — реальные журналы этого кандидата.

**RELEASE_ALLOWED = NO. INDEPENDENT_GATE = NOT_RUN. INTERNAL_QA_ZIP = CREATED_AND_VERIFIED. OWNER_INSTALLABLE_HANDOFF = FORBIDDEN.**
