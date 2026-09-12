# B17 — единая карта подготовки финальной приёмки

Кандидат: tree b20b74351d95becd67f32994e3e00899e9208b8c32c778a306f73f6703bfe508; внутренний ZIP1560599adfcfdb2c3180ec9103005b1584bcd39709b8fc45e233f6c1bdd11ee1. Это карта исполнимых источников и оставшихся квалификаций, **не PASS независимого gate**. Исходный PD-00…17 и ресурсное правило не изменены.

## Где брать точные входы

Готовый пакет и четыре browser scripts — artifact10299402884, run34699125356. Первичный финальный cleanup FAIL находится там и не скрывается; его диагностический повтор — отдельный workflow ymb-b17-cleanup-recheck.yml. Продукт между запусками одинаков.

B14 artifact10298216105/run34692833348 используется только как сохранённый QA workspace. Его старый production ZIP не является кандидатом. Для full-worker тестов задаются YMB_FULL на текущую распаковку, YMB_IDB_FIXTURE на qa/qa/idb_artifact_fixture.mjs, YMB_HARNESS на qa/qa/b10_full_worker_harness.mjs. Последний аргумент обязателен для b13_missing_coverage.test.mjs.

Код B17 находится в двух exact diffs и qa/B17_QA_INPUTS.tar.xz. В браузере тестируется скачанный уже собранный пакет, не новый ручной пересказ исходников. Названия ниже относительны каталогу tests внутри ready artifact либо qa/qa внутри сохранённого Node workspace.

## Все обязательные разделы

| PD | Конкретный исполнимый источник | Что ещё нельзя объявить закрытым |
|---|---|---|
|00|IDENTITY.json +67file hash inventory + canonical ZIP checks|Единая независимая фиксация финального кандидата|
|01|19исходных non-WIP suites по original_inventory.tsv; b9/b10/b11/b12/b13 full-worker; B1–B8 module/export наборы; новые b17_worker/content|Единый полный запуск всех актуальных исходных/patch suites на окончательном кандидате. B17 development subsets не подменяют его|
|02|61node--check; manifest/package JSON; b12_contract; exact path inventory|Release-version/permission решение и проверка конечного пакета после него|
|03|b17_prepare, IDENTITY.json, локальный/CI ZIP roundtrip, negative input checks|Применение byte-complete packaging к окончательному owner-target и независимая fresh-extraction проверка|
|04|b15_browser_qualification actual worker.close; b16.generated full Chrome close/reopen|Единая independent campaign, без переноса старого PASS|
|05|b16.generated real_popup_toggles_do_not_save_unsaved_fields и real_popup_explicit_save_text_and_dedicated_secret|Полная матрица присутствующих popup/service controls и isolation должна быть привязана к конечному runner, не только двум названным случаям|
|06|b15 nativeCopy; b16 PRE_before_Copy и readonly_CodeMirror_mutation_detach; bodyposition/identity|Все ещё поддерживаемые DOM adapters, ambiguity/fallback и четыре stable plaque ключа должны быть сопоставлены с recovered browser harness; CMshape не называется настоящей библиотекой|
|07|b9 full discovery; b15 real external action; b16 full CM block|Полная malformed/multi-command/source-order матрица именно content→worker в браузере, а не только Node parsing|
|08|b13_missing_coverage все4Wordstat метода/Check/batch; исходные protocol suites|Повтор полного набора в independent campaign; без реальных provider requests|
|09|b5 shared-admission, b10_deferred/legacy, b11_batch_faults; b17_worker pause vsSend FIFO/UNKNOWN|Единая точная policy/counter/scope матрица и независимое выполнение|
|10|b10_legacy/b11_batch_faults controlled worker Autorun; recovered phase2-stage4 browser scripts|Полный фактический popup→RUN→pickup→delivery→pause/resume/stop→reload и стабильный autorun-state. Это конкретный оставшийся browser-qualified блок|
|11|b15 normal/watch-only/occupied/duplicate/corruption; b16navigation; b17_browser девять содержательных pause-сценариев (точные case names в журнале); b17_worker/content|Пауза не отменяет provider, не удаляет evidence и не освобождает неопределённый Manual-lock. Полный текстовый Manual path иfile path входят в финальный gate вместе|
|12|b13_missing_coverage DebugON/OFF redaction/diagnostics; b10/b11errors|Разбор/политика/credentials/delivery/UNKNOWN и стабильные видимые error plaques для всех включённых services в одной кампании|
|13|b16 foreign_conversation/SPA/profile; b17 foreign_tab/durable_pause; b6binding|Все cross-PRE/cross-assistant/ambiguous binding cases из исходного gate, не только один foreigntab|
|14|b13full backup/checksum/legacy import; b8export/artifact; B15/B16real IDB/restart; B17pause|Отдельная точная cross-install restore и same-folder upgrade квалификация; B16одинprofile не равно cross-install|
|15|b12injection; b13backup redaction; b16page secrets; b17wrongowner/legacycommit/ACK fences|Сводная complete security matrix на финальном кандидате; никаких настоящих ключей|
|16|b12нет operation-host; B15/B16initializer providerEnabled=false; B17не меняет permissions|Новый отложенный сетевой маршрут пока выключен. Его включение — отдельное разрешённое изменение/проверка, не текстовый обход из команды|
|17|Exact hashes before/after, полные raw logs, archive SHA, scope/error classification|Только независимый полный verdict может разрешить handoff; developer CI не называется CodexPASS|

## Ограниченный остаток, без нового feature-scope

1. Подготовить один параметризованный конечный runner: полный исходный suite + patch suites, без old-target hashes, без mutation production и без уменьшения assertions.
2. Квалифицировать конкретные недостающие browser assertions из PD05/06/07/10/12/13/14, переиспользуя recovered scripts, а не строя очередной функционал продукта. Любой обнаруженный реальный дефект исправляется отдельно с новым exact target.
3. Решение о конечной версии и сетевом разрешении не прятать в QA. Сохранить zero-real-provider policy gate; реальная авторизация не подменяется fixtures.
4. После полной исполнимой карты — отдельная независимая Codex-кампания и owner acceptance. Пользователь не переносит QA файлы. Пока условия gate не выполнены, QA prompt не выдаётся.

Уже пройденные development сценарии не нужно снова конструировать. Они хранятся как код и evidence на exact source. Повтор всех включённых проверок один раз при final freeze обязателен; повторное выдумывание продукта — нет.

RELEASE_ALLOWED=NO. INDEPENDENT_GATE=NOT_RUN. FINAL_GATE_READY=false.
