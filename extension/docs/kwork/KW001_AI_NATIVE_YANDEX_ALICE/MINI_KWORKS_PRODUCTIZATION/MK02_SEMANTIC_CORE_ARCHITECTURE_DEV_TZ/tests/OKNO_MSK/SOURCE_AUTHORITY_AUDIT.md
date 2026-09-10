# MK02 / OKNO_MSK — аудит источников и приоритета данных

Дата аудита: **2026-09-10**  
Режим: **MK02 base / preserved evidence / Yandex-only / provider calls = 0**  
Начальный remote HEAD работы: `76d1bf8f9a11b90b183a593b36c7ae1cfff760c3`  
Первый фактически применённый после проверки параллельного движения HEAD: `87ff76d62ead7782756898f2319208bc195d5d86`

## 1. Результат аудита

Точная семантическая основа MK02 доказана: **2 840 уникальных фраз до Step5A**. Первичная row-level authority — `STEP_08_SEARCH_STAGE_SEMANTIC_SET.tsv`; принятый MK01-only слой задаёт текущие продуктовые статусы `2 185 / 187 / 468` и `59` групп. Для владения, структуры и ТЗ используются pre-Step5A Stage-5/6 authorities и независимые поздние публичные evidence overlays. Интегрированный массив на 2 856 строк не используется.

Поздняя дата доказательства не считается загрязнением сама по себе. Решения повторно допускаются в MK02 только тогда, когда их фактическое основание относится к нативным 2 840 строкам и не создано шестнадцатью конкурентными добавлениями.

## 2. Точная семантическая authority

| Параметр | Значение |
|---|---|
| Полный repo path | `extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK/STEP_08_SEARCH_STAGE_SEMANTIC_SET.tsv` |
| Строк данных | **2 840** |
| Уникальные фразы | **2 840** |
| SHA-256 | `73f52fd48ae925573b9739292b8c8893a8db40014775859c9630367703873d1f` |
| Source commit | `976f6169bee2b32eabe8a18c6fc3d7034b3889fc` |
| Commit message | `KW001 OKNO: regenerate Step 08 after route-method correction [kw001-step08-route-correction-output]` |
| Состояние относительно Step5A | pre-Step5A |

Схема исходника:

```text
phrase
historical_status
historical_reason
corrected_status
corrected_reason
semantic_confidence
source_occurrences
result_occurrences
association_occurrences
max_result_count
max_association_count
source_ids
provenance
search_stage_disposition
next_resolution_route
route_reason
```

Файл является pre-Step5A authority не по имени или дате, а по сочетанию доказательств:

1. содержит ровно 2 840 уникальных исходных фраз;
2. сохранён до появления отдельной 16-row Step5A delta;
3. `RESEARCH_REBUILD_STAGE_05_FINAL_SEMANTIC_MASTER_2026-09-05.tsv` содержит те же 2 840 фраз без потерь;
4. post-Step5A QA механически подтверждает `2840 + 16 = 2856` и field-exact идентичность всех 2 840 нативных строк;
5. отдельный accepted MK01 rehearsal построен из этого universe и подтвердил продуктовую проекцию: рабочее ядро 2 185, проверка 187, исключено 468.

## 3. Реестр источников

| Объект решения | Источник | Класс | Проверка / граница |
|---|---|---|---|
| Полный нативный universe | `tests/OKNO_MSK/STEP_08_SEARCH_STAGE_SEMANTIC_SET.tsv` | **PRIMARY AUTHORITY** | 2 840 строк; SHA и commit указаны выше |
| Текущий MK01 продуктовый статус, группы и row provenance | `MINI_KWORKS_PRODUCTIZATION/MK01_SEMANTIC_CORE_CLUSTERING/tests/OKNO_MSK/MK01_SEMANTIC_UNIVERSE_2026-09-09.tsv.gz` | **CURRENT ACCEPTED OVERLAY** | 2 840 строк; 2 185 working, 187 review, 468 excluded; 59 групп |
| Нативная phrase→unit/owner/role проекция | `tests/OKNO_MSK/RESEARCH_REBUILD_STAGE_05_FINAL_SEMANTIC_MASTER_2026-09-05.tsv` | **PRIMARY AUTHORITY** | 2 840 строк; SHA `94c8…1fa2`; commit `a505c50b…`; pre-Step5A |
| Канонические задачи/структурные единицы | `tests/OKNO_MSK/RESEARCH_REBUILD_STAGE_05_CANONICAL_UNIT_AUTHORITY_2026-09-05.tsv` | **PRIMARY AUTHORITY** | 168 строк; SHA `060ac8…2abd`; pre-Step5A |
| Канонические действия | `tests/OKNO_MSK/RESEARCH_REBUILD_STAGE_05_CANONICAL_ACTION_AUTHORITY_2026-09-05.tsv` | **PRIMARY AUTHORITY** | 34 строки; SHA `357ed0…2b8`; pre-Step5A |
| Прочитанное состояние страниц для действий | `tests/OKNO_MSK/RESEARCH_REBUILD_STAGE_06_CURRENT_SITE_VALIDATION_2026-09-05.tsv` | **PRIMARY AUTHORITY** | 14 строк; сохранённые публичные чтения, дата наблюдения сохраняется |
| As-is/to-be specs | `tests/OKNO_MSK/RESEARCH_REBUILD_STAGE_06_AS_IS_TO_BE_IMPLEMENTATION_SPECIFICATIONS_2026-09-05.tsv` | **PRIMARY AUTHORITY** | 34 строки; исходная связь действия и evidence |
| Исправленная готовность и клиентские формулировки | `tests/OKNO_MSK/RESEARCH_REBUILD_POST_RELEASE_SHARED_IMPLEMENTATION_AUTHORITY_CORRECTED_2026-09-05.tsv` | **CURRENT ACCEPTED OVERLAY** | 34 строки; SHA `396474…6010`; исправляет готовность без нового исследования |
| Внутренние связи | `tests/OKNO_MSK/RESEARCH_REBUILD_STAGE_06_INTERNAL_LINK_SPECIFICATIONS_2026-09-05.tsv` | **PRIMARY AUTHORITY** | 15 рекомендуемых связей; статус рекомендации отделён от as-is |
| Сохранённая ordinary Yandex Search evidence для ownership | `tests/OKNO_MSK/STEP_11_SEARCH_*`, `STEP_11_POST_AUDIT_CORRECTIONS.tsv` | **REUSABLE INDEPENDENT EVIDENCE** | только сохранённые запросы/результаты; новых обращений нет |
| Кандидаты страниц и page reads | `STEP_11_CLUSTER_PAGE_CANDIDATES.tsv`, `STEP_11_CODEX_PAGE_PROFILE_LEDGER.tsv`, принятые overlays | **REUSABLE INDEPENDENT EVIDENCE** | используется как evidence, но не как финальная authority без поздних исправлений |
| Структурный диагноз | `STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V6.tsv` и принятые correction gates | **REUSABLE INDEPENDENT EVIDENCE** | источник Stage-5 unit/action authority; старые версии не имеют приоритета |
| Competing-page universe | `STEP_13_FINAL_PAIR_ACCOUNTING.json`, `STEP_13_QUERY_FAMILY_CASES.tsv`, `STEP_13_*EVIDENCE*`, `STEP_13_ACCEPTANCE_2026-09-01.md` | **REUSABLE INDEPENDENT EVIDENCE** | 199 effective pairs / 21 query-family cases; base-public claims only |
| Private Yandex history | не сохранена как доступная доказательная authority | **EVIDENCE GAP** | исторический вред не заявляется; destructive action не выводится |
| Заморозка Search-архитектуры | `STEP_14_SEARCH_ONLY_ARCHITECTURE_FREEZE.tsv` | **PRIMARY AUTHORITY** | 35 записей; Search-only, без AI |
| Прочтённые критичные URL | `STEP_14_CURRENT_URL_RECHECK.tsv` | **REUSABLE INDEPENDENT EVIDENCE** | 59 URL; snapshot 2026-09-01 |
| Независимая текущая discovery/topology | `STEP_14A_CURRENT_SITE_RECONCILIATION_TRANSPORT.json` + chunks, `STEP_14A_RECONCILIATION_QA_2026-09-02.json` | **CURRENT ACCEPTED OVERLAY** | 2 683 current public URLs; 2 624 reconciled; queue terminal; snapshot 2026-09-02 |
| Материальные новые текущие страницы | `STEP_14A_ARCHITECTURE_DELTA.tsv` | **CURRENT ACCEPTED OVERLAY** | 21/21 reconciled; 0 CREATE; 0 destructive actions |
| Буквальное состояние проверяемых ссылок | `STEP_14A_RUN9_INTERNAL_LINK_AS_IS_RECONCILIATION.tsv` | **CURRENT ACCEPTED OVERLAY** | 15 связей: 9 present, 6 absent planned, 0 unknown |
| Evidence meaning/locator | `RESEARCH_REBUILD_STAGE_07_EVIDENCE_REGISTER_2026-09-05.tsv` | **REUSABLE INDEPENDENT EVIDENCE** | 95 строк; не заменяет само доказательство |
| Клиентская action authority | corrected shared implementation + Stage-6 link specs + literal link overlay | **CURRENT ACCEPTED OVERLAY** | готовность перепроецируется в состояния MK02; расписание не выдумывается |

## 4. Порядок приоритета

```text
MK01 accepted semantic product status
→ pre-Step5A Stage-5 phrase/unit/action authority
→ accepted current-site and implementation correction overlays
→ preserved independent Search/page/topology evidence
→ older ledgers and narrative reports only as cross-check
```

Старый downstream active count `2332` не может повторно активировать строки, которые MK01-only rehearsal уже поместил в `review` или `excluded`. В MK02 активной семантической границей служит принятое рабочее ядро 2 185 строк, а не исторический статус `ASSIGNED` в полном KW-001.

## 5. Cross-check only / superseded / forbidden

### CROSS-CHECK ONLY

- `STEP_11_PHRASE_PAGE_MAP.tsv` и старые cluster summaries: полезны для lineage, но имеют прежнюю 2 332-row активную границу.
- narrative reports полного KW-001 и клиентский release 2026-09-05: проверяют объяснения, но не становятся MK02 authority.
- `STEP_14A_RUN9_CHATGPT_RECONCILIATION_2026-09-02.md`: подтверждает topology 15/15, но его partial discovery state superseded Run10 closure.

### SUPERSEDED / FORBIDDEN AS CURRENT AUTHORITY

- ранние `STEP_11_PAGE_OWNERSHIP.tsv` и версии Step12 до accepted corrections;
- промежуточные partial/fail state files, когда их исправляет более поздний принятый overlay;
- client PDF/DOCX/XLSX полного KW-001: не копируются и не определяют границы MK02;
- AI/Alice/GenSearch/Neuro artifacts и архитектурные выводы следующих стадий.

### STEP5A-CONTAMINATED FOR MK02 BASE

- `STEP_05A_POST_STEP09_DOWNSTREAM_REFRESH_2026-09-09/POST_STEP09_FINAL_SEMANTIC_MASTER_2856.tsv`;
- post-Step5A client release на 2 856 строк;
- все 16 delta phrase rows и 7 delta-direction решений;
- post-Step5A unit `phrase_count` для шести затронутых единиц.

Эти файлы используются только для отрицательной проверки contamination и field-exact сравнения нативных строк.

## 6. Freshness и claim boundary

- Семантика и Search evidence — сохранённые снимки исходного исследования конца августа — начала сентября 2026 года.
- Run10 current-site discovery — снимок **2026-09-02**: 2 683 URL, terminal queue, 0 silent skip; это operational completeness принятого crawler-метода, а не математическое доказательство отсутствия недоступных URL.
- GEO-поддомены вне московской main-host architecture freeze.
- Отсутствие private Webmaster history ограничивает выводы о вредной исторической каннибализации.
- Новые provider calls в rehearsal: **0**.

## 7. Gate conclusion

```text
NATIVE_UNIVERSE_PROVED = 2840
NATIVE_UNIQUE_PHRASES = 2840
MK01_WORKING_BOUNDARY = 2185
STEP5A_ADDITIONS_ADMITTED = 0
DOWNSTREAM_AUTHORITY_SELECTED_BY_CONTENT_AND_PRECEDENCE = true
CURRENT_SITE_OVERLAY_IS_INDEPENDENT_EVIDENCE = true
PRIVATE_HISTORY_AVAILABLE = false
NEW_PROVIDER_CALLS = 0
SOURCE_AUTHORITY_GATE = PASS
```

