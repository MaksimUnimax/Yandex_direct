# MK01 / OKNO_MSK — rehearsal metrics for future Phase 8

Статус: **MEASURED / NO PRICE OR COMMERCIAL LIMIT INVENTED**

Дата: **2026-09-09**

Эти числа описывают один фактически выполненный пилот. Они не являются готовым тарифом, SLA или универсальным лимитом пакета.

## Объём результата

| Метрика | Факт |
|---|---:|
| Public-site URLs в сохранённом discovery | 64 |
| Wordstat seed/probe requests исходного проекта | 22 |
| Wordstat occurrence-строки | 2965 |
| Уникальные точные фразы | 2840 |
| Схлопнутые повторные occurrence-наблюдения | 125 |
| Фразы с несколькими наблюдениями | 101 |
| Рабочее ядро | 2185 |
| На проверку / с неопределённостью | 187 |
| Исключено всего | 468 |
| Исключено при очистке | 334 |
| Исключено после task clustering как outside task | 134 |
| Active rows для clustering | 2332 |
| Итоговые смысловые группы | 59 |
| Рабочие группы | 54 |
| Outside-task группы | 5 |
| Exact Search probes исходного проекта | 75 |
| Нормализованные Search TOP-10 строки | 750 |
| Search decisions, присоединённые к universe | 66 |
| Search control anchors вне universe | 9 |
| Step5A additions в результате | 0 |

## Реально выполненные операционные единицы

Единицы неоднородны, поэтому они не складываются в искусственное «число операций». Для экономики нужно учитывать каждую размерность отдельно.

| Операционный класс | Измеренный объём | Характер работы |
|---|---:|---|
| Order/scope freeze | 1 заказ, 16 направлений | аналитический контроль |
| Public-site discovery | 64 URL | частично автоматизируется; business interpretation требует review |
| Acquisition planning | 18 initial seeds + 4 second-pass probes | аналитический выбор и stop logic |
| Wordstat provider execution | 22 requests | автоматизируется при сохранении каждого результата |
| Wordstat normalization/persistence | 2965 occurrence rows | автоматизируется |
| Exact-text dedupe | 2965→2840 | автоматизируется; non-exact merge не автоматизируется |
| First triage | 1 corpus / 18 source families | аналитический review |
| Row-level cleanup | 2840 phrase decisions | основной аналитический объём; 4 saturation passes + 72 QA cases в preserved authority |
| Semantic routing | 2840 route decisions | частично автоматизируется, но SEARCH/DEFER review нужен |
| Ordinary Yandex Search | 75 exact requests | provider execution автоматизируется; question design/conclusion требуют review |
| Search normalization | 750 TOP-10 rows | автоматизируется при немедленном persistence |
| Task-first clustering | 2332 active rows | аналитический bottleneck |
| Independent clustering audit | 2332 rows reviewed | аналитический bottleneck |
| Cluster corrections | 927 affected rows, 1 consolidated batch | rule-level correction + regression |
| Client materialization | 1 XLSX / 7 sheets + 2 tabular audit artifacts | автоматизируется из authority |
| Machine QA | 50 checks | автоматизируется |
| Visual recipient QA | 7 rendered sheets | human review; automation помогает, но не заменяет |

## Автоматизируемые операции

- schema validation, exact normalization and occurrence retention;
- count/set/hash reconciliation;
- source→phrase provenance join;
- deterministic Russian status/reason mapping after analytical authority is frozen;
- working/review/excluded partition and outside-task exclusion;
- cluster membership counts, representative membership checks and summaries;
- XLSX generation, tables, filters, freeze panes and bounded inspections;
- Step5A contamination test;
- ZIP/readability/formula/internal-code scans;
- commit payload identity and remote blob readback.

## Операции, требующие аналитического review

- scope and real business-offer interpretation;
- information-gain justification for seeds and second acquisition;
- positive KEEP evidence and ambiguous REVIEW decisions;
- choosing which ambiguity warrants ordinary Search;
- interpreting exact Search results without family-wide transfer;
- user-task boundaries and domain-specific cluster contracts;
- resolving outside-task vs adjacent-useful business fit;
- representative phrase suitability;
- recipient-language and usability review.

## Bottlenecks пилота

1. **Row-level semantics**: 2840 governed phrases; frequency/association rules cannot replace meaning review.
2. **Task-first clustering**: 2332 active rows independently reviewed; 927 rows required consolidated correction/recheck.
3. **Evidence-safe Search**: 75 exact probes created 750 observations; 66/9 join/control distinction had to be restored explicitly.
4. **Recipient materialization**: structural XLSX validity did not catch worksheet-width conflict, group ordering or an internal English term; human render review remained necessary.
5. **Persistence discipline**: the original Search run preserved normalized coverage but lost full per-item raw fidelity for 74 items; a new order must persist/read back each useful chunk before continuing.

## Provider calls

### Выполнено во время этого rehearsal

```text
Wordstat = 0
ordinary Yandex Search = 0
GenSearch / Alice = 0
Webmaster / Metrika / Direct = 0
Google = 0
all external SEO provider APIs = 0
```

### Фактически использованные категории в сохранённом исходном проекте

| Категория | Requests | Сохранённая стоимость исходного выполнения |
|---|---:|---:|
| Yandex Wordstat, первый проход | 18 | 0,36 ₽ |
| Yandex Wordstat, точечный второй проход | 4 | 0,08 ₽ |
| Ordinary Yandex Search, exact TOP-10 | 75 | 36,60 ₽ |
| Всего провайдерских request units, использованных MK01 evidence | 97 | 37,04 ₽ |

Стоимость приведена только как readback исходных execution logs и не является ценой услуги.

### Что потребуется в реальном новом заказе

- актуальный публичный site discovery;
- bounded Wordstat first pass по утверждённому manifest;
- conditional second Wordstat pass только при доказанном information gap;
- ordinary Yandex Search только для material Search-resolvable ambiguity;
- никаких обязательных Webmaster/Metrika/Direct/Google/AI calls в base MK01.

Количество будущих запросов нельзя принимать равным 22/75 автоматически: оно определяется текущим scope, доказанным приростом и числом материальных неопределённостей.

## Ручная проверка

Из сохранённых authorities:

```text
row-level cleanup universe = 2840 rows
manual semantic saturation passes = 4
cleanup QA cases = 72
active clustering rows independently reviewed = 2332
cluster error/correction impact rows = 927
cluster impact recheck failures = 0
recipient sheets visually reviewed = 7
additional Phase-5 contrast cleanup sample = 15 rows
```

Не следует складывать 2840, 2332 и 927 как независимые уникальные фразы: это перекрывающиеся этапы проверки одного corpus.

## Размер клиентского результата

| Artifact | Размер |
|---|---:|
| XLSX, 7 листов | 648 049 bytes |
| Полный audit universe, `TSV.GZ` | 148 768 bytes |
| Cluster summary TSV | 62 171 bytes |

Полный распакованный universe содержит 2841 строку файла: 1 header + 2840 data rows.

## Проблемы масштабирования

- количество unique phrases растёт быстрее, чем безопасный semantic review;
- broad seeds резко увеличивают association/noise volume;
- число Search probes зависит от ambiguity, а не только от общего числа фраз;
- новый регион требует отдельного evidence context и может изменить routing;
- большой cluster correction set требует atomic rebuild, а не ручных исправлений workbook;
- большее число языков/сегментов увеличивает display mapping и recipient QA;
- сырые инспекционные dumps могут быть на порядок больше deliverable, поэтому сохраняются bounded receipts, а не дублирующие 50+ MB sidecars.

## Параметры будущего коммерческого лимита

Phase 8 должен оценивать как минимум:

1. число исследуемых сайтов/доменов и URL discovery;
2. число регионов;
3. число frozen business directions;
4. maximum initial Wordstat requests;
5. maximum conditional second-pass requests и критерий information gain;
6. maximum occurrence rows и unique phrase rows;
7. число строк, требующих аналитической очистки;
8. число material Search questions/requests;
9. число active rows и cluster contracts для task-first review;
10. число клиентских revisions после freeze;
11. обязательный уровень raw persistence/readback;
12. число deliverable views/languages и объём recipient QA.

**Цена и лимиты в Phase 5 не назначены.** Основание для Phase 8 — приведённые measured workload dimensions, а не произвольное число фраз.
