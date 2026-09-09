# MK01 / OKNO_MSK — QA report

Статус: **G0–G11 PASS / G12 PENDING FINAL QA-BUNDLE REMOTE READBACK**

Дата: **2026-09-09**  
Текущая materialization authority: `MK01_MATERIALIZATION_MANIFEST_2026-09-09.json`  
Независимый машинный отчёт: `MK01_REHEARSAL_QA_2026-09-09.json`

Phase 5 пока не объявляется завершённой: G12 будет переведён в PASS только после commit/push/readback исправленного workbook, QA bundle и method corrections.

## Итоговые счётчики

```text
source occurrences = 2965
source universe = 2840
working core = 2185
review / uncertain = 187
excluded = 468
semantic groups = 59
working groups = 54
outside groups = 5
saved Search decisions = 75
Search decisions joined to exact universe phrases = 66
Search control anchors outside universe = 9
Step5A contamination = 0
provider calls during rehearsal = 0
```

## Независимый machine QA

Полный валидатор выполнен после последней пересборки:

```text
runner = validate_mk01_rehearsal.py
checks_total = 50
checks_passed = 50
checks_failed = 0
status = PASS
```

Проверены exact phrase-set joins, occurrence accounting, статусная партиция, Search 75=66+9, Step5A delta, outside-task projection, 59 cluster contracts, representative membership, XLSX ZIP/readback, порядок и видимость 7 листов, row counts, таблицы/фильтры, freeze panes, ширины, ошибки формул, язык display-слоя, неожиданные URL и downstream headers.

## G0–G12

| Gate | Результат | Фактическое доказательство |
|---|---|---|
| G0 Scope / Yandex-only | **PASS** | `MOCK_CLIENT_ORDER.md` фиксирует существующий сайт, Москву, 16 направлений и только MK01. XLSX не содержит Google-данных, competitor additions, page ownership или AI conclusions; отрицательные границы явно объяснены. |
| G1 Acquisition / persistence | **PASS** | Сохранено 18+4 Wordstat-пакета и 2965 occurrence-строк с role/count/source provenance. Raw/normalized authorities и checkpoints перечислены в `SOURCE_AUTHORITY_AUDIT.md`; HTTP success не использован как единственный критерий. Rehearsal provider calls = 0. |
| G2 Accounting | **PASS** | 2965 occurrence − 125 повторных наблюдений = 2840 unique. 2840 = 2185 working + 187 review + 468 excluded. Phrase-set difference Step08→output = 0; duplicate keys = 0; сумма `Исходных наблюдений` = 2965. |
| G3 Semantic cleanup | **PASS** | Corrected row-level authority содержит 4 manual semantic saturation passes и 72 QA cases без failures; default KEEP=false, low-frequency exclusion=false, association auto-keep=false. Дополнительно вручную проверены 15 контрастных строк пяти финальных состояний; результаты ниже. |
| G4 Targeted Search | **PASS WITH RECORDED LIMIT** | 75 exact queries, 750 TOP-10 rows и 75 decisions сохранены. Независимая сверка: 66 exact queries существуют в universe, 9 — control anchors вне него; новые строки не созданы. Для R2 сохранён полный normalized TOP-10, но не полный per-item raw XML/request-ID ledger; ограничение прямо показано и не закрыто повторным платным сбором. |
| G5 Clustering semantic | **PASS** | 2840 assignment rows; 2332 active rows полностью независимо reviewed; 927 correction rows применены и повторно проверены; active accounted = 2319 assigned + 13 Search-required. 59/59 contracts имеют members/task/intent/boundary; target count=false; representatives — реальные члены. 134 OUTSIDE rows отделены от рабочего ядра. |
| G6 Deliverable data | **PASS** | XLSX с 7 обязательными views создан из текущих authorities. Working subset=2185, review=187, excluded=468, all=2840. Ни один из 134 членов пяти OUTSIDE clusters не попал в working sheet. Integrated 2856 не использован. |
| G7 Wordstat metrics | **PASS** | На листах используются «Число запросов — популярные/похожие» и пояснение: Москва, все устройства, без операторов; это относительный показатель, не exact frequency, unique market volume или traffic forecast. Cluster sum прямо помечен не объёмом рынка. |
| G8 Russian recipient language | **PASS** | Все 7 названий листов, основные headers/status/reasons/tasks/intents — русские. Английский `provenance` удалён из клиентского словаря; технические ID остаются только в явно помеченных аудиторских колонках. Machine scan запрещённых внутренних статусов = 0. |
| G9 Workbook physical / visual | **PASS** | XLSX повторно импортирован; 7/7 листов отрендерены. Таблицы и filters есть на 6 data sheets; freeze panes: `C6/C6/B6/B6/B6/A6`; формульных ошибок до export и после import = 0; critical hidden sheets/columns = 0. Первый лист и рабочий-first порядок групп перепроверены после исправлений. |
| G10 Recipient task | **PASS** | Отдельный walkthrough в `RECIPIENT_REVIEW.md`: из файла без репозитория определяются scope/region, полный набор, active core, группы, uncertainty, exclusions/reasons, значение показателей, next step и excluded product work. |
| G11 Provider reuse | **PASS** | До действий выполнен source-authority audit. Все данные построены из сохранённых Wordstat/Search authorities. Новых Wordstat/Search/GenSearch/Alice/Webmaster/Metrika/Direct/Google calls = 0. |
| G12 Persistence / remote readback | **PENDING** | Materialization block `c2d728b8f0411a933909bb51bf3c5fc78fd4d6a8` был прочитан с remote, но последующие QA fixes изменили workbook/manifest/method. Gate будет закрыт только после публикации и readback текущего полного набора. |

## G3 — контрастная ручная проверка строк

| Итоговый статус | Контрольная фраза | Проверка решения |
|---|---|---|
| Рабочее ядро | `пластиковые окна` | главный продуктовый коммерческий спрос; включение обосновано |
| Рабочее ядро | `установка трехстворчатого пластикового окна` | сервисная задача установки; корректная группа |
| Рабочее ядро | `что такое французское окно в квартире фото` | информационная задача примеров/дизайна; смежная, не смешана с покупкой |
| Исключено при очистке | `пластиковые окна бу` | used/marketplace вне зафиксированного предложения |
| Исключено при очистке | `ремонт пластиковых окон в донецке днр` | другой регион вне московского scope |
| Исключено при очистке | `французские фильмы` | устойчиво посторонний смысл |
| Исключено после clustering | `шторы на пластиковые окна` | coherent task, но предложение штор не подтверждено; не active core |
| Исключено после clustering | `дом из бруса с панорамными окнами` | задача архитектурной идеи/недвижимости, а не заказа окна |
| Исключено после clustering | `французские занавески на окна` | задача штор, несмотря на общие токены |
| Нужна Search-проверка | `пластиковые окна комарова` | сущность/география не определяется надёжно по фразе |
| Нужна Search-проверка | `без алюминиевой окна` | искажённая формулировка с неясной задачей |
| Нужна Search-проверка | `rehau окна 2` | числовой хвост не даёт устойчивого смысла |
| Проверка отложена | `анкерные пластины для окон пвх` | association-only; возможная комплектующая, но немедленное evidence не обосновано |
| Проверка отложена | `оконная рама` | широкая association-only формулировка; предложение/задача не доказаны |
| Проверка отложена | `шторы на лоджию` | вероятно посторонняя задача, но preserved deferred authority не переписана без нового evidence |

Во всех 15 случаях частотность не использована как самостоятельное решение. Контроль включает high/medium/zero demand и основные, смежные, scope, irrelevant, malformed и association-only классы.

## Исправленные FAIL-состояния

1. **Search projection count**: первоначальный валидатор нашёл только 66 joins при общем числе 75 decisions. Root cause: 9 probes были control anchors вне universe. Manifest, методика, execution log и QA теперь фиксируют `75 = 66 + 9`.
2. **Active-core membership**: 2319 технически assigned строк включали 134 строки пяти clusters с `business_fit=OUTSIDE`. Рабочее ядро теперь содержит только 2185 CORE/ADJACENT строк; 134 сохранены как exclusions after clustering.
3. **Первый лист**: поздняя настройка ширины шага перезаписывала ширину той же worksheet column и делала summary нечитаемым. Геометрия определена один раз для всего листа, после чего он повторно отрендерен.
4. **Recipient vocabulary/order**: удалён необъяснённый термин `provenance`; рабочие группы поставлены перед исключёнными в cluster summary.

После исправлений независимый набор из 50 проверок выполнен полностью: **50 PASS / 0 FAIL**. G12 остаётся единственным незакрытым gate до remote readback текущей версии.
