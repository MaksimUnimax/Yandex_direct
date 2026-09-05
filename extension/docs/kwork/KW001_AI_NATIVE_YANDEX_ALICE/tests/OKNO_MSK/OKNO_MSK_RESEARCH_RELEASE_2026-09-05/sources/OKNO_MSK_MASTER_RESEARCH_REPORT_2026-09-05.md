# OKNO_MSK — мастер-отчёт пересобранного исследования

**Дата:** 2026-09-05  
**Статус:** STAGE 08 MASTER RESEARCH TRUTH / QA PASS  
**Роль документа:** единая полная исследовательская версия, от которой должны производиться клиентский отчёт, руководство SEO-специалиста, AI-документ и таблицы  
**Новые Yandex/Wordstat/GenSearch/Alice/provider-вызовы в Stages 3–8:** 0  
**Новая платная стоимость:** 0 ₽

## 1. Введение: почему исследование пересобрано

Исходная работа была значительно глубже, чем показывал прежний клиентский пакет. В репозитории сохранились модель бизнеса и сайта, корпус спроса, очистка и группировка семантики, обычные наблюдения выдачи Яндекса, назначения страниц, структурные решения, диагностика пересечений, Search-only архитектура, восемь выборочных AI-кейсов и реестр действий. Однако клиентская упаковка потеряла существенную часть объяснения и доказательств.

Критический дефект был не только редакционным. В 69 строках исправился канонический идентификатор семантической единицы, но зависимые поля сохранили старую задачу/намерение/бизнес-границу/роль страницы. Затем клиентские таблицы не материализовали исправленный идентификатор. Поэтому старый пакет отозван как текущая истина, но сохранён как историческое доказательство.

Пересборка восстанавливает цепочку:

**спрос → задача пользователя → Search-доказательство → семантическая единица → владелец страницы → структурное решение → AI-проверка → действие → реализационная спецификация → клиентский продукт**.

## 2. Цель и критерий успеха

Цель — не «улучшить таблицу», а дать клиенту полноценный продукт:

1. объяснить, что исследовано и на каких данных;
2. показать, что на сайте уже правильно;
3. показать, что требует изменения или уточнения;
4. дать исполнимые инструкции там, где доказательств достаточно;
5. сохранить неопределённость там, где доказательств недостаточно;
6. отдельно показать вклад обычного поиска и вклад AI;
7. обеспечить одну общую аналитическую истину для всех клиентских представлений.

## 3. Бизнес и границы объекта

Публичная модель — производственно-монтажный бизнес по пластиковым и алюминиевым окнам, дверям, балконам/лоджиям, верандам/террасам, замеру, расчёту, доставке, монтажу и сервису. Типовой путь клиента:

**задача остекления → выбор системы/конфигурации → расчёт/консультация → бесплатный замер → смета/договор → изготовление → доставка/монтаж → гарантия/сервис**.

Основные семейства:

- пластиковые окна / REHAU;
- ПВХ-двери;
- балконы и лоджии;
- веранды, террасы и беседки;
- алюминиевые окна / холодное остекление;
- монтаж и ремонт;
- образовательные и сравнительные материалы;
- доверие, примеры работ и калькулятор;
- географические страницы как отдельное поперечное измерение.

Исследование не делает частные выводы о прибыли, конверсии, доступности конкретного бренда, производственной мощности или историческом вреде каннибализации без соответствующих данных.

**Источник:** `BUSINESS_AND_PAGE_MODEL.md`.

## 4. Входные данные и метод

### 4.1. Спрос

Исходный уникальный корпус — 2 840 фраз. Итоговая семантическая власть Stage 05 сохраняет каждую исходную строку:

- 2 313 назначенных фраз;
- 19 активных `SEARCH_REQUIRED`;
- 174 `REVIEW_DEFERRED`;
- 334 `EXCLUDED_PRESERVED`.

Внутри назначенного множества 42 фразы относятся к 20 структурным единицам `HOLD`. Исключённые и отложенные фразы не удалены: их состояние и линия происхождения сохранены.

### 4.2. Обычный Яндекс

Сохранены 75 точных наблюдений Step 09. Для каждого фиксируются запрос, наблюдаемая задача выдачи, доминирующий тип результата, handoff и граница доказательства. Затем 21 материальное семейство рассматривалось как отдельный вопрос владения/пересечения.

Правило доказательства:

- точный запрос доказывает наблюдение только для этого запроса;
- нормализованная проекция не равна сырому телу провайдера;
- отсутствие URL в выдаче не равно отсутствию страницы на сайте;
- Search не доказывает конверсию, исторический вред или стабильную долгосрочную позицию.

### 4.3. Текущий сайт

Ранний инвентарь не считался вечной властью. Позднее независимое обнаружение добавило 21 материальный топологический дельта-факт и сменило владельцев там, где существовала более точная текущая страница. После Stage 05 14 реализационно-чувствительных страниц были повторно открыты 2026-09-05.

### 4.4. AI

AI-кейсы были выборочными, а не заменой обычному Search. Для каждого восстановлены причина выбора, замороженное Search-only решение, ответ, источники, сравнение, вердикт, эффект и ограничение. Факт запроса сам по себе не считается ценностью.

### 4.5. Коррекция

Для 69 переassignments Stage 05 применяет атомарную коррекцию:

**новая каноническая единица → её задача/intent/scope/role/owner → все потребители**.

Проверка сравнивает строку с контрактом новой целевой единицы, а не только с новым ID.

## 5. Что установлено о спросе и семантике

Итоговая модель содержит 168 структурных единиц. Распределение структурных действий:

- `KEEP_EXISTING_STRUCTURE`: 73
- `ROUTE_TO_EXISTING_PAGE_AS_SUBTASK`: 46
- `DEFER_PENDING_EVIDENCE`: 20
- `NO_STANDALONE_PAGE`: 14
- `OUTSIDE_SCOPE_NO_ACTION`: 7
- `ADD_SECTION_OR_FAQ_TO_EXISTING`: 6
- `EXPAND_EXISTING_PAGE`: 2

Это означает, что работа в основном не требует массового создания новых посадочных страниц. Большая часть спроса либо уже имеет подходящего владельца, либо должна быть маршрутизирована как подзадача существующей страницы. 20 единиц остаются на HOLD, а 15 не оправдывают отдельную страницу по сохранённому доказательству.

### Материальные исправления владельцев

Поздняя текущая топология позволила точно закрепить:

- отделку открытого балкона за `/balkony-i-lodzhii/otdelka-balkonov`;
- общее раздвижное алюминиевое остекление балкона за `/balkony-i-lodzhii/razdvizhnye-okna-na-balkon`;
- окна в деревянном доме за `/okna-rehau/po-tipu-doma/okna-v-derevyannyj-dom`;
- коммерческий выбор стеклопакета за `/okna-rehau/steklopakety-dlya-plastikovykh-okon`;
- раздвижные окна веранды за `/verandy/razdvizhnye-okna-na-verandu`.

Широкие страницы при этом не удаляются: они остаются владельцами общих задач или поддерживающими узлами.

## 6. Страницы, пересечения и каннибализация

Исследование различает:

- связанные страницы;
- текущее пересечение задач;
- историческую конкуренцию;
- доказанный вред.

Эти состояния не взаимозаменяемы. Для трёх пар/семейств осталась необходимость различить роли:

- broad panoramic vs `/okna-rehau/panoramnye-okna-rehau`;
- private-house primary vs cottage/country-house page;
- product-integrated REHAU comparison vs отдельная статья сравнения.

До появления более сильного доказательства запрещены merge/delete/redirect и утверждение о вреде. Это не дефект завершения отчёта, а честная ограниченная рекомендация.

## 7. Результат обычного Search

Обычный Яндекс был основным источником для понимания намерения и ожидаемого типа посадочной страницы. Он помог:

- отделить покупку аксессуаров/фурнитуры от услуги по окнам;
- отделить отделку открытого балкона от остекления;
- увидеть коммерческие, информационные и гибридные задачи;
- сохранить объектно-ориентированного владельца для балкона/веранды, когда материал является характеристикой решения;
- разделять общую страницу и узкого специалиста;
- не превращать каждое уточнение запроса в новый URL.

Матрица `RESEARCH_REBUILD_STAGE_07_SEARCH_CASE_EXPLANATION_2026-09-05.tsv` показывает для каждого из 21 семейства вопрос до Search, сохранённое наблюдение, Search-only решение и запрет на чрезмерное обобщение.

## 8. Результат AI-проверки

| Кейс | Запрос | Вердикт | Архитектурный эффект | Действие |
|---|---|---|---|---|
| C15-004 | панорамные алюминиевые окна | DE_RISK | NO_ARCHITECTURE_CHANGE | S18-A030 — проверить и при необходимости усилить panoramic-aluminium subsection; новая страница не нужна. |
| C15-006 | алюминиевые окна для веранды | DE_RISK | NO_ARCHITECTURE_CHANGE | Явного действия не создавать; сохранить /verandy как общий владелец. |
| C15-007 | панорамное остекление балкона | DE_RISK | NO_ARCHITECTURE_CHANGE | Положительный RETAIN: сохранить specialist balcony page; материальный content gap не доказан. |
| C15-010 | установка подоконника на пластиковые окна | NO_CHANGE | NO_ARCHITECTURE_CHANGE | NO_ACTION: сохранить hybrid product/service/how-to owner и professional fallback. |
| C15-013 | французские панорамные окна | DE_RISK | NO_ARCHITECTURE_CHANGE | S18-A009 — после свежей проверки усилить French-vs-panoramic distinction и selection depth на существующей странице. |
| C15-018 | замена окна на пластиковое цена москва | NO_CHANGE | NO_ARCHITECTURE_CHANGE | NO_ACTION: сохранить replacement specialist; content gap по использованным источникам не доказан. |
| C15-019 | как открыть пластиковое окно | NO_CHANGE | NO_ARCHITECTURE_CHANGE | NO_ACTION: не расширять узкую troubleshooting-статью под двусмысленный запрос. |
| C15-020 | лучшие пластиковые окна | INSUFFICIENT | NO_ARCHITECTURE_CHANGE | S18-A031 — проверить свежесть рейтинга и методику сравнения; архитектурную иерархию не менять. |

Сводка:

- `CHANGE`: 0;
- `DE_RISK`: 4;
- `NO_CHANGE`: 3;
- `INSUFFICIENT`: 1;
- архитектурных изменений: 0.

AI не доказал необходимость новой страницы. Его реальная ценность — снижение риска неверной смены владельца и выявление ограниченных кандидатов глубины существующего контента:

- панорамный алюминий — уточнить выбор тёплого/холодного сценария и проектные ограничения;
- французские окна — пояснить конфигурации и отличие от панорамного;
- «лучшие окна» — обновить дату/метод рейтинга;
- в остальных кейсах сохранить текущего владельца, не создавать действие либо оставить недостаточность явно.

## 9. AS-IS → TO-BE и рекомендации

| ID | Приоритет | Объект | Целевое состояние | Готовность |
|---|---|---|---|---|
| S18-A001 | P1_HIGH | https://okno-msk.ru/balkony-i-lodzhii/otdelka-balkonov | Use the discovered standalone balcony-finishing page as exact owner; retain broad balcony page for bundled glazing+renovation. | READY_ROUTING |
| S18-A002 | P1_HIGH | https://okno-msk.ru/balkony-i-lodzhii/razdvizhnye-okna-na-balkon | Use dedicated sliding-balcony page for sliding-only intent; retain cold-glazing owner when cold intent is explicit. | READY_ROUTING |
| S18-A003 | P1_HIGH | https://okno-msk.ru/okna-rehau/panoramnye-okna-rehau | Differentiate broad panoramic owner from newly discovered same-task commercial page; preserve broad owner pending stronger evidence. | NOT_READY__ROLE_DIFFERENTIATION_PENDING |
| S18-A004 | P1_HIGH | https://okno-msk.ru/okna-rehau/po-tipu-doma/okna-dlya-kottedzhej-i-zagorodnyh-domov | Differentiate private-house primary from cottage/country-house same-task page; preserve frozen primary and avoid destructive consolidation. | NOT_READY__ROLE_DIFFERENTIATION_PENDING |
| S18-A005 | P1_HIGH | https://okno-msk.ru/okna-rehau/po-tipu-doma/okna-v-derevyannyj-dom | Route wooden-house PVC intent to exact existing specialist; retain broad private-house page as support. | READY_ROUTING |
| S18-A006 | P1_HIGH | https://okno-msk.ru/okna-rehau/steklopakety-dlya-plastikovykh-okon | Route commercial glass-unit selection to exact product hub while keeping informational glass-unit need separate. | READY_ROUTING |
| S18-A007 | P1_HIGH | https://okno-msk.ru/stati/sravnenie-profilej-rehau | Differentiate product-integrated Rehau comparison owner from same-task article; preserve current product-integrated primary. | NOT_READY__ROLE_DIFFERENTIATION_PENDING |
| S18-A008 | P1_HIGH | https://okno-msk.ru/verandy/razdvizhnye-okna-na-verandu | Use exact sliding-veranda page for explicit sliding intent; retain /verandy for general non-sliding glazing. | READY_ROUTING |
| S18-A009 | P1_HIGH | https://okno-msk.ru/okna-rehau/francuzskie-okna | Strengthen existing French-window page for verified configuration/replacement needs and concise French-vs-panoramic selection depth. | READY_CONTENT_BOUNDED |
| S18-A010 | P1_HIGH | https://okno-msk.ru/okna-rehau/po-tipu-doma/okna-v-chastnyj-dom | Add standard/non-standard opening dimensions and sizing guidance, explaining why individual measurement overrides generic standards. | READY_CONTENT_BOUNDED |
| S18-A011 | P1_HIGH | https://okno-msk.ru/stati/kak-vybrat-plastikovye-okna | Expand selection guide with hardware construction/parts, broader queried-brand comparison and Accado/Vorne/Futurus coverage. | NOT_READY__BRAND_AVAILABILITY_CONFIRMATION |
| S18-A012 | P1_HIGH | https://okno-msk.ru/dveri-rehau | Retain the current door price/price-estimation guidance; strengthen only the still-missing door-specific professional installation scope/process, including what the service covers and how the installation service is explained on the accepted PVC-door page. | READY_CONTENT_BOUNDED |
| S18-A013 | P2_MEDIUM | https://okno-msk.ru/alyuminievye-okna/provedal | Add Provedal hub as support for aluminium/cold sliding tasks while retaining generic owners. | READY_SUPPORT_ROUTING |
| S18-A014 | P2_MEDIUM | https://okno-msk.ru/balkony-i-lodzhii/francuzskoe-osteklenie-balkona | Add balcony-specific French page as intersection support while retaining French and panoramic-balcony primaries. | READY_SUPPORT_ROUTING |
| S18-A015 | P2_MEDIUM | https://okno-msk.ru/balkony-i-lodzhii/holodnoe-panoramnoe-osteklenie-balkona | Add cold+panoramic balcony specialist for exact intersection; retain generic primaries outside it. | READY_SUPPORT_ROUTING |
| S18-A016 | P2_MEDIUM | https://okno-msk.ru/balkony-i-lodzhii/osteklenie-profilem-provedal | Add exact Provedal balcony support while retaining broad/cold primaries according to intent. | READY_SUPPORT_ROUTING |
| S18-A017 | P2_MEDIUM | https://okno-msk.ru/okna-rehau/izgotovlenie-steklopaketov-na-zakaz | Add existing custom glass-unit manufacturing specialist as routed subtask under glass-unit commercial family. | READY_SUPPORT_ROUTING |
| S18-A018 | P2_MEDIUM | https://okno-msk.ru/okna-rehau/po-tipu-doma/okna-na-kuhnyu | Add kitchen-window page as room-specific support; do not split aggregate room unit solely from this page. | READY_SUPPORT_ROUTING |
| S18-A019 | P2_MEDIUM | https://okno-msk.ru/okna-rehau/tipovye-razmery | Add commercial standard-size hub as support while retaining informational dimensions owner. | READY_SUPPORT_ROUTING |
| S18-A020 | P2_MEDIUM | https://okno-msk.ru/okna-rehau/tipovye-razmery/katalog-tipovyh-okon | Add typed-window catalog as commercial support while retaining informational dimensions owner. | READY_SUPPORT_ROUTING |
| S18-A021 | P2_MEDIUM | https://okno-msk.ru/stati/kak-vybrat-plastikovye-okna-v-kvartiru | Add apartment-specific selection guide as narrow support while retaining broad/best-windows owners. | READY_SUPPORT_ROUTING |
| S18-A022 | P2_MEDIUM | https://okno-msk.ru/stati/kakoj-profil-i-firma-luchshe | Add narrow profile/manufacturer comparison article as support while retaining broad selection ownership. | READY_SUPPORT_ROUTING |
| S18-A023 | P2_MEDIUM | https://okno-msk.ru/stati/steklopakety-osobennosti-i-vidy | Add glass-unit types/features article as informational support; keep commercial glass-unit hub distinct. | READY_SUPPORT_ROUTING |
| S18-A024 | P2_MEDIUM | https://okno-msk.ru/stati/vidy-i-tipy-ostekleniya-verandy-plyusy-i-minusy | Add veranda glazing types/choice article as informational support while retaining /verandy as commercial primary. | READY_SUPPORT_ROUTING |
| S18-A025 | P2_MEDIUM | https://okno-msk.ru/verandy/bezramnoe-osteklenie-verandy | Add exact frameless-veranda specialist for explicit frameless intent; retain /verandy for general glazing. | READY_SUPPORT_ROUTING |
| S18-A026 | P2_MEDIUM | https://okno-msk.ru/stati/plyusy-i-minusy-ostekleniya-alyuminievymi-oknami | Add aluminium-specific ventilation, micro-ventilation and ventilation-valve guidance to accepted technical article. | READY_CONTENT_BOUNDED |
| S18-A027 | P2_MEDIUM | https://okno-msk.ru/okna-rehau/francuzskie-okna | Do not add a duplicate basic French-window definition. If terminology remains ambiguous, fold only residual naming/distinction guidance for French vs panoramic and imitation/partition/block terminology into the broader S18-A009 French-window content work. | NO_SEPARATE_CHANGE__COMBINE_A009 |
| S18-A028 | P2_MEDIUM | https://okno-msk.ru/dveri-rehau | Add clear width/height/standard-size guidance and concise selection criteria to current PVC-door page. | READY_CONTENT_BOUNDED |
| S18-A029 | P2_MEDIUM | https://okno-msk.ru/nashi-raboty | Improve portfolio discoverability with meaningful labels/categories/filters for balcony, veranda, panoramic and French examples. | READY_CONTENT_BOUNDED |
| S18-A030 | P2_MEDIUM | QF004 accepted aluminium owner/support pages; see Step17 ledger | Verify and if needed strengthen panoramic-aluminium subsection for warm/cold suitability, large-format/project constraints and selection criteria; no new page. | READY_CONTENT_BOUNDED |
| S18-A031 | P2_MEDIUM | https://okno-msk.ru/stati/kakie-okna-samye-luchshie | Verify/update date-sensitive ranking evidence, state comparison criteria clearly and keep profile/model distinctions explicit; no split/consolidation from this case. | READY_CONTENT_BOUNDED |
| S18-A032 | P2_MEDIUM | 15 IMPLEMENT rows in STEP_14_INTERNAL_LINK_ARCHITECTURE.tsv | Implement 15 accepted contextual internal-link handoffs; keep other 43 rows deferred/not-applicable. | READY_LINK_BATCH |
| S18-A033 | P3_LATER | 46 ROUTE_TO_EXISTING_PAGE_AS_SUBTASK rows in STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V6.tsv | Implement accepted route-to-existing-page relationships for all 46 current route units, applying Step14A overlays as higher precedence. | READY_ROUTING_BATCH |
| S18-A034 | HOLD | 20 DEFER_PENDING_EVIDENCE rows in STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V6.tsv | Keep all 20 DEFER_PENDING_EVIDENCE structural units on HOLD; do not invent pages/content/service claims until each named gap is resolved. | HOLD__EVIDENCE_REQUIRED |

Главные группы работ:

1. **Исправление семантического владения и маршрутизации.** Использовать точных текущих специалистов без дублирующих URL.
2. **Различение ролей страниц.** Три overlap-кейса остаются NOT_READY для разрушительных действий.
3. **Контент существующих страниц.** Французские окна, размеры частного дома и дверей, монтаж дверей, вентиляция алюминиевого остекления, портфолио, панорамный алюминий и метод рейтинга.
4. **Фурнитура.** Расширение сравнительной части допускается только после подтверждения реального ассортимента брендов.
5. **Внутренние ссылки.** 15 точных контекстных переходов готовы.
6. **Подзадачи.** 46 структурных единиц готовы к маршрутизации на существующие страницы.
7. **HOLD.** 20 единиц остаются без изобретённой страницы/контента.

Полные поля AS-IS, доказательство, TO-BE, блок, темы, вопросы, пример, критерии приёмки и запреты находятся в `RESEARCH_REBUILD_STAGE_06_AS_IS_TO_BE_IMPLEMENTATION_SPECIFICATIONS_2026-09-05.tsv`.

## 10. Положительные результаты: что не менять

- Не создавать новые страницы только потому, что семантическая таблица должна выглядеть полной.
- Сохранить `/verandy` как общего владельца остекления веранды; узкие страницы использовать по явному sliding/frameless намерению.
- Сохранить отдельные specialist-страницы, найденные поздней текущей инвентаризацией.
- Не объявлять связанные страницы каннибализацией без доказанного вреда.
- Не дублировать уже существующую ценовую часть на странице дверей.
- Не дублировать базовое определение французского окна; остаточное различие включить в одну работу S18-A009.
- Сохранить `NO_CHANGE`, `DE_RISK`, `HOLD` и `UNRESOLVED` как полноценные результаты.

## 11. Ограничения и неопределённость

Сохраняются:

- 19 фраз `SEARCH_REQUIRED`;
- 174 `REVIEW_DEFERRED`;
- 20 структурных единиц HOLD;
- три overlap-кейса, где destructive action не разрешён;
- подтверждение доступности дополнительных брендов фурнитуры;
- отсутствие private Webmaster/Metrika/конверсионных данных;
- неполная raw fidelity части исторического обычного Search;
- отсутствие consumer Alice; сохранённый AI-корпус — точечный GenSearch proxy;
- PP-19 остаётся ограниченным из-за отсутствия окончательно замороженной продающей Kwork-карточки и одобренного demo-пакета.

Эти ограничения не блокируют выпуск исследовательского продукта, потому что рекомендации и запреты сформулированы в пределах имеющихся доказательств. Они блокируют только более сильные утверждения.

## 12. Трассируемость и канонические власти

- продукт и PP: `RESEARCH_REBUILD_STAGE_01_PRODUCT_PROMISE_AND_ACCEPTANCE_MATRIX_2026-09-04.md`;
- полный аудит старой цепочки: `RESEARCH_REBUILD_STAGE_02_FULL_AUDIT_2026-09-04.md`;
- AI causal ledger: `RESEARCH_REBUILD_STAGE_03_AI_CAUSAL_LEDGER_2026-09-05.tsv`;
- disposition: `RESEARCH_REBUILD_STAGE_04_FINAL_DEFECT_RECOVERY_REGISTER_2026-09-05.tsv`;
- семантика: `RESEARCH_REBUILD_STAGE_05_FINAL_SEMANTIC_MASTER_2026-09-05.tsv`;
- единицы: `RESEARCH_REBUILD_STAGE_05_CANONICAL_UNIT_AUTHORITY_2026-09-05.tsv`;
- действия: `RESEARCH_REBUILD_STAGE_05_CANONICAL_ACTION_AUTHORITY_2026-09-05.tsv`;
- неопределённость: `RESEARCH_REBUILD_STAGE_05_RESIDUAL_UNCERTAINTY_REGISTER_2026-09-05.tsv`;
- implementation specs: `RESEARCH_REBUILD_STAGE_06_AS_IS_TO_BE_IMPLEMENTATION_SPECIFICATIONS_2026-09-05.tsv`;
- Search/AI/positive/uncertainty evidence: `RESEARCH_REBUILD_STAGE_07_EVIDENCE_REGISTER_2026-09-05.tsv`.

## 13. Заключение

Старое исследование в основном не было пустым или ошибочным; оно было плохо материализовано, а одна коррекционная цепочка действительно сломала семантическую целостность. Пересборка исправила каноническую семантику, назначила точных текущих владельцев, сохранила честную неопределённость и превратила действия в реализационные спецификации.

Практический итог — улучшать существующую архитектуру и контент, а не создавать массово новые страницы. AI не меняет Search-only архитектуру, но в отдельных случаях уменьшает риск и уточняет, какой контент усилить. Клиентские версии должны производиться только из этого мастер-слоя и его структурных властей.
