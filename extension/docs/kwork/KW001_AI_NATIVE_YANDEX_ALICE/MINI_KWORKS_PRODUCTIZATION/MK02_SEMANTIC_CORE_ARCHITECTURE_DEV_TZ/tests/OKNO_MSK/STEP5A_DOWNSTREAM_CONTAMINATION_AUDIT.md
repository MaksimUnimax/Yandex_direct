# MK02 / OKNO_MSK — аудит причинного загрязнения downstream-решений Step5A

Дата: **2026-09-10**  
Режим: **MK02 base; competitor Step5A excluded**

## 1. Проверяемая гипотеза

Механическое удаление 16 строк недостаточно. Нужно доказать, не изменили ли конкурентные добавления границу задачи, владельца, структурное действие, competing-page вывод, архитектуру, связь или implementation task для нативных 2 840 фраз.

Проверка разделяет два утверждения:

```text
LATE ARTIFACT DATE != STEP5A CONTAMINATION
STEP5A-CAUSED DECISION != MK02 BASE DECISION
```

## 2. Доказанный Step5A delta

Post-Step5A QA сохраняет точную причинную дельту:

- baseline: **2 840** фраз;
- competitor additions: **16** фраз;
- integrated universe: **2 856** фраз;
- направлений delta: **7**;
- нативных строк, изменивших хотя бы одно поле: **0**;
- потерянных нативных строк: **0**;
- новых физических изменений сайта из delta: **0**;
- новых страниц из delta: **0**;
- новых destructive actions из delta: **0**.

Машинная сверка текущего репозитория повторно сравнила `RESEARCH_REBUILD_STAGE_05_FINAL_SEMANTIC_MASTER_2026-09-05.tsv` с `POST_STEP09_FINAL_SEMANTIC_MASTER_2856.tsv`: все 2 840 нативных строк присутствуют и field-exact идентичны.

## 3. Шестнадцать запрещённых для MK02-base фраз

1. армирование оконного профиля;
2. балконы под офис;
3. гидроизоляция балконной плиты открытого балкона;
4. гидроизоляция для открытого балкона;
5. гидроизоляция открытого балкона в частном доме;
6. гидроизоляция открытого деревянного балкона;
7. как сделать гидроизоляцию на открытом балконе;
8. лучшая гидроизоляция для открытого балкона;
9. многофункциональный стеклопакет что это;
10. солнцезащитное стекло в стеклопакете;
11. солнцезащитный стеклопакет;
12. солнцезащитный стеклопакет rehau;
13. ударопрочный стеклопакет;
14. шумоизоляция крыши балкона изнутри от дождя;
15. шумоизоляция крыши балкона от дождя;
16. шумоизоляция на крышу балкона.

## 4. Проверка по downstream-классам

| Класс | Что сравнивалось | Результат причинной проверки | Решение для MK02 base |
|---|---|---|---|
| Semantic rows | 2 840-row Stage-5 master против 2 856-row post-Step5A master | 2 840/2 840 field-exact; изменённых нативных строк 0 | взять pre-Step5A 2 840; исключить 16 delta |
| Cluster / unit boundary | 168 pre-Step5A unit rows против 168 post-Step5A rows | ID-set неизменен; у шести units изменился только `phrase_count` | взять pre-Step5A units и counts |
| Exact owner | 16 delta ownership rows | только новые фразы: 9 existing, 7 unresolved; нативные owners не менялись | исключить 16 rows; сохранить нативных owners |
| Family owner / supporting | 16 delta routing fields | маршруты добавлены только новым фразам | не переносить delta routing как MK02 результат |
| CREATE | 7 direction decisions | во всех семи `REJECTED_NOT_JUSTIFIED`; CREATE=0 | причинно новых CREATE нет |
| SPLIT / MERGE / redirect | delta action + overlap + architecture | изменений нет; destructive action=0 | нативная pre-Step5A authority сохраняется |
| Structural action | pre/post unit comparison и 7 delta action rows | нативные action fields не изменились; delta — mapping/hold | использовать pre-Step5A unit/action authority |
| Competing-page case | 7 Step13 delta overlap decisions | все `NO_NEW_CONFLICT_TRIGGER`; remediation — сохранить структуру | не добавлять новые case rows; native Step13 reusable |
| Target architecture | 7 Step14 delta rows | только существующий owner/family route; new URL=0 | исключить delta rows; native target сохраняется |
| Internal-link relation | delta authorities | Step5A не создал link recommendation | использовать независимые pre-Step5A links |
| Implementation task | Step18 delta readiness | 6 analytical mappings + 1 pending evidence; physical change=0 | исключить все 7 delta items из base work packages |
| Later current-site evidence | Run10 discovery и 21-page reconciliation | собрано позже, но относится к существующим URL и нативным units; не порождено 16 фразами | переиспользовать как independent evidence с датой снимка |
| Corrected Report №02 readiness | 34 pre-Step5A action IDs | исправляет форму/готовность существующих действий, не добавляет Step5A topics | переиспользовать как accepted overlay |

## 5. Изменившиеся unit counts, которые нельзя переносить

| Structural unit | До Step5A | После Step5A | Разница |
|---|---:|---:|---:|
| `BALCONY_GLAZING_ROOF_SERVICE` | 6 | 9 | +3 |
| `BALCONY_RENOVATION_WITH_GLAZING` | 14 | 15 | +1 |
| `GLASS_UNIT_PRODUCT_SELECTION` | 5 | 9 | +4 |
| `GLASS_UNIT_SELECTION_INFO` | 1 | 2 | +1 |
| `OPEN_BALCONY_FINISHING` | 12 | 18 | +6 |
| `WINDOW_PROFILE_SELECTION_INFO` | 2 | 3 | +1 |

Сумма изменений равна 16. В MK02 materialization берутся именно pre-Step5A counts.

## 6. Независимые поздние доказательства

Поздние Run10/Step14A данные допустимы не из-за даты, а потому что доказывают отдельный факт: фактически обнаруженные текущие URL, текущий page state и literal link state. Они применимы к нативным units независимо от конкурентных добавлений. Их использование не переносит в MK02 ни одну из 16 фраз и не создаёт новую задачу.

Аналогично corrected implementation authority сохраняет прежние 34 action IDs и исправляет только передачу задания исполнителю. Она не является новым исследованием и не меняет semantic input.

## 7. Что исключается или перепроизводится

- integrated 2 856-row semantic master — исключён;
- 16 phrase rows — исключены из всех joins и клиентских views;
- семь delta-direction actions — исключены;
- post-Step5A `phrase_count` шести units — заменён pre-Step5A count;
- post-Step5A release XLSX/PDF/DOCX — не используется как клиентский output;
- нативная phrase→page map строится заново на принятой MK01 working boundary 2 185, а не копируется из старого 2 332-row downstream активного множества;
- каждая готовая site-change задача должна иметь pre-Step5A action ID и независимое evidence; иначе — blank/pending/HOLD.

## 8. Итог

```text
BASE_NATIVE_ROWS = 2840
INTEGRATED_ROWS_REJECTED_AS_BASE = 2856
STEP5A_ADDITIONS_IDENTIFIED = 16
STEP5A_ADDITIONS_IN_MK02_INPUT = 0
NATIVE_ROWS_CHANGED_BY_STEP5A = 0
NATIVE_UNIT_BOUNDARIES_CHANGED = 0
NATIVE_OWNER_DECISIONS_CHANGED = 0
NATIVE_STRUCTURAL_ACTIONS_CHANGED = 0
NATIVE_COMPETING_PAGE_CASES_CHANGED = 0
NATIVE_TARGET_ARCHITECTURE_CHANGED = 0
NATIVE_PHYSICAL_WORK_PACKAGES_CHANGED = 0
STEP5A_CONTAMINATION_AFTER_PROJECTION = 0
CONTAMINATION_GATE = PASS
```

