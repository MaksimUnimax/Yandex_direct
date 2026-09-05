# Руководство SEO-специалиста по внедрению исследования OKNO_MSK

**Дата:** 2026-09-05  
**Статус:** STAGE 10 IMPLEMENTATION GUIDE / QA PASS  
**Источник истины:** Stage 05 canonical authorities + Stage 06 implementation specifications  
**Важно:** аналитическое действие не равно готовой технической задаче. Выполнять можно только строки со статусом `READY_*`; `NOT_READY` и `HOLD` остаются ограничениями.

## 1. Как пользоваться руководством

1. Сначала обновить семантическое владение в рабочих таблицах/CMS-задачах на текущую каноническую власть.
2. Не создавать новый URL, если действие говорит о маршрутизации, поддерживающей странице или контентном блоке.
3. До публикации проверить текущий URL, H1/назначение и отсутствие нового конфликта.
4. Внедрять блок строго на целевой странице и сохранять существующую полезную информацию.
5. После каждого действия проверять критерии приёмки и зависимые клиентские представления.
6. `NOT_READY` нельзя переименовывать в «готово» без нового доказательства и переходной линии.
7. Merge/delete/redirect запрещены там, где не доказан вред.

## 2. Очерёдность

### Волна A — каноническое владение

S18-A001, A002, A005, A006, A008. Это исправления владельца/маршрута без новой страницы.

### Волна B — поддерживающие страницы и маршрутизация

S18-A013..A025, A033. Эти работы добавляют точный путь к существующей странице, но не дробят архитектуру.

### Волна C — контентные улучшения

S18-A009, A010, A012, A026, A028, A029, A030, A031. Выполнять в пределах описанного блока.

### Волна D — внутренние ссылки

S18-A032: 15 контекстных переходов после проверки источника и цели.

### Отдельный контроль

- S18-A003, A004, A007 — NOT_READY: сначала различить роли текущих страниц.
- S18-A011 — NOT_READY: подтвердить реальный ассортимент брендов.
- S18-A027 — отдельную задачу не делать, включить остаток в A009.
- S18-A034 — HOLD: не создавать страницы/контент до устранения именованного пробела.

## 3. Спецификации действий

### S18-A001 — OWNER_STATE_UPDATE

- **Состояние спецификации:** `READY_ROUTING`
- **Приоритет:** `P1_HIGH`
- **Целевая страница/объект:** https://okno-msk.ru/balkony-i-lodzhii/otdelka-balkonov
- **AS-IS:** Сохранённое текущее состояние: Use the discovered standalone balcony-finishing page as exact owner; retain broad balcony page for bundled glazing+renovation.
- **Доказательство:** STEP_14A_ARCHITECTURE_DELTA.tsv
- **Почему требуется действие:** Fresh discovery invalidated older no-standalone state and proves an existing specialist owner.
- **TO-BE:** Use the discovered standalone balcony-finishing page as exact owner; retain broad balcony page for bundled glazing+renovation.
- **Точное место:** Семантическое владение, хлебные крошки и контекстные ссылки; контент не переписывать без отдельного дефекта.
- **Темы:** Задача пользователя: finish/renovate an open balcony without glazing as the primary job; order bundled balcony renovation plus glazing
- **Фразы-примеры:** балкон без остекления | балкон без остекления цена | балкон под ключ без остекления | балкон под ключ без остекления цена | обшивка балкона без остекления | отделка балкона без остекления | отделка балкона без остекления под ключ | отделка балкона без остекления цена | отделка балкона без остекления цена москва | отделка балкона под ключ москва без остекления
- **Вопросы, на которые должен ответить блок:** Какая страница отвечает на точную задачу? Как пользователь переходит к следующему релевантному действию?
- **Внутренние связи:** Preserve canonical owner/support relationships from Stage 05
- **Пример реализации:** Использовать осмысленную ссылку/якорь по задаче, не создавая дублирующую посадочную страницу.
- **Критерии приёмки:** Целевая страница/объект и каноническое действие совпадают с текущей властью; нет противоречащего клиентского представления.
- **Зависимости:** NONE
- **Запрещённое утверждение/действие:** No private performance history; no traffic-loss claim.
- **Подтверждение клиента:** NO
- **Владелец, трудоёмкость, ёмкость и срок:** не назначены и не выдуманы.

### S18-A002 — OWNER_SPECIALIST_UPDATE

- **Состояние спецификации:** `READY_ROUTING`
- **Приоритет:** `P1_HIGH`
- **Целевая страница/объект:** https://okno-msk.ru/balkony-i-lodzhii/razdvizhnye-okna-na-balkon
- **AS-IS:** Сохранённое текущее состояние: Use dedicated sliding-balcony page for sliding-only intent; retain cold-glazing owner when cold intent is explicit.
- **Доказательство:** STEP_14A_ARCHITECTURE_DELTA.tsv
- **Почему требуется действие:** Exact current specialist should govern the narrow task before downstream routing.
- **TO-BE:** Use dedicated sliding-balcony page for sliding-only intent; retain cold-glazing owner when cold intent is explicit.
- **Точное место:** Семантическое владение, хлебные крошки и контекстные ссылки; контент не переписывать без отдельного дефекта.
- **Темы:** Задача пользователя: order aluminium sliding glazing for balcony/loggia; order cold aluminium sliding glazing for balcony/loggia; order cold balcony/loggia glazing
- **Фразы-примеры:** алюминиевые окна лоджию раздвижные | алюминиевые окна на балкон раздвижные цена | алюминиевые раздвижные окна на балкон | окно балконное алюминиевое раздвижное | раздвижные окна на балкон алюминиевые холодное | замена холодного остекления балкона | окна балкон холодное остекление | остекление балкона холодное раздвижное | остекление холодного балкона окна алюминиевые холодные | раздвижные алюминиевые окна на балкон холодное остекление
- **Вопросы, на которые должен ответить блок:** Какая страница отвечает на точную задачу? Как пользователь переходит к следующему релевантному действию?
- **Внутренние связи:** Preserve canonical owner/support relationships from Stage 05
- **Пример реализации:** Использовать осмысленную ссылку/якорь по задаче, не создавая дублирующую посадочную страницу.
- **Критерии приёмки:** Целевая страница/объект и каноническое действие совпадают с текущей властью; нет противоречащего клиентского представления.
- **Зависимости:** NONE
- **Запрещённое утверждение/действие:** No private performance evidence.
- **Подтверждение клиента:** NO
- **Владелец, трудоёмкость, ёмкость и срок:** не назначены и не выдуманы.

### S18-A003 — ROLE_DIFFERENTIATION_RECHECK

- **Состояние спецификации:** `NOT_READY__ROLE_DIFFERENTIATION_PENDING`
- **Приоритет:** `P1_HIGH`
- **Целевая страница/объект:** https://okno-msk.ru/okna-rehau/panoramnye-okna-rehau
- **AS-IS:** Сохранённое текущее состояние: Differentiate broad panoramic owner from newly discovered same-task commercial page; preserve broad owner pending stronger evidence.
- **Доказательство:** STEP_14A_ARCHITECTURE_DELTA.tsv
- **Почему требуется действие:** Two materially overlapping current commercial pages need role clarity before implementation.
- **TO-BE:** Differentiate broad panoramic owner from newly discovered same-task commercial page; preserve broad owner pending stronger evidence.
- **Точное место:** На целевом объекте согласно типу действия.
- **Темы:** Задача пользователя: buy/order/configure panoramic windows; understand/select panoramic window types, safety, thermal and suitability options
- **Фразы-примеры:** большие панорамные окна | высокие панорамные окна | готовые панорамные окна | дача с панорамными окнами | заказать панорамное окно | летние панорамные окна | маленькое панорамное окно | окна панорамные цена для загородного | окно панорамное 2.5 | окно панорамное 2.5 метра
- **Вопросы, на которые должен ответить блок:** Какая страница отвечает на точную задачу? Как пользователь переходит к следующему релевантному действию?
- **Внутренние связи:** Preserve canonical owner/support relationships from Stage 05
- **Пример реализации:** Следовать каноническому описанию действия.
- **Критерии приёмки:** Действие не публикуется как готовое; неопределённость и запрещённые разрушительные операции сохранены.
- **Зависимости:** NONE
- **Запрещённое утверждение/действие:** No historical harm claim; merge/delete/redirect forbidden.
- **Подтверждение клиента:** NO
- **Владелец, трудоёмкость, ёмкость и срок:** не назначены и не выдуманы.

### S18-A004 — ROLE_DIFFERENTIATION_RECHECK

- **Состояние спецификации:** `NOT_READY__ROLE_DIFFERENTIATION_PENDING`
- **Приоритет:** `P1_HIGH`
- **Целевая страница/объект:** https://okno-msk.ru/okna-rehau/po-tipu-doma/okna-dlya-kottedzhej-i-zagorodnyh-domov
- **AS-IS:** Сохранённое текущее состояние: Differentiate private-house primary from cottage/country-house same-task page; preserve frozen primary and avoid destructive consolidation.
- **Доказательство:** STEP_14A_ARCHITECTURE_DELTA.tsv
- **Почему требуется действие:** Fresh discovery found a same-task competitor to the frozen private-house owner.
- **TO-BE:** Differentiate private-house primary from cottage/country-house same-task page; preserve frozen primary and avoid destructive consolidation.
- **Точное место:** На целевом объекте согласно типу действия.
- **Темы:** Задача пользователя: buy/plan windows for a private house; plan/specify windows for a private house
- **Фразы-примеры:** крыльцо для частного дома окна | купить пластиковые окна для частного дома | окна в пол для частного дома | окна для частного дома купить | окна для частного дома цена | окна пвх для частного дома | окно полукруглое для частного дома | пластиковые окна для частного дома цена | стандарты пластиковых окон для частного дома | форма пластиковых окон для частного дома
- **Вопросы, на которые должен ответить блок:** Какая страница отвечает на точную задачу? Как пользователь переходит к следующему релевантному действию?
- **Внутренние связи:** Preserve canonical owner/support relationships from Stage 05
- **Пример реализации:** Следовать каноническому описанию действия.
- **Критерии приёмки:** Действие не публикуется как готовое; неопределённость и запрещённые разрушительные операции сохранены.
- **Зависимости:** NONE
- **Запрещённое утверждение/действие:** No historical harm/conversion claim; destructive consolidation forbidden.
- **Подтверждение клиента:** NO
- **Владелец, трудоёмкость, ёмкость и срок:** не назначены и не выдуманы.

### S18-A005 — OWNER_SPECIALIST_UPDATE

- **Состояние спецификации:** `READY_ROUTING`
- **Приоритет:** `P1_HIGH`
- **Целевая страница/объект:** https://okno-msk.ru/okna-rehau/po-tipu-doma/okna-v-derevyannyj-dom
- **AS-IS:** Сохранённое текущее состояние: Route wooden-house PVC intent to exact existing specialist; retain broad private-house page as support.
- **Доказательство:** STEP_14A_ARCHITECTURE_DELTA.tsv
- **Почему требуется действие:** Exact specialist is stronger than prior broad routing.
- **TO-BE:** Route wooden-house PVC intent to exact existing specialist; retain broad private-house page as support.
- **Точное место:** Семантическое владение, хлебные крошки и контекстные ссылки; контент не переписывать без отдельного дефекта.
- **Темы:** Задача пользователя: choose/buy PVC windows for a wooden house; buy/plan windows for a private house
- **Фразы-примеры:** пластиковые окна в деревянном доме | крыльцо для частного дома окна | купить пластиковые окна для частного дома | окна в пол для частного дома | окна для частного дома купить | окна для частного дома цена | окна пвх для частного дома | окно полукруглое для частного дома | пластиковые окна для частного дома цена | стандарты пластиковых окон для частного дома
- **Вопросы, на которые должен ответить блок:** Какая страница отвечает на точную задачу? Как пользователь переходит к следующему релевантному действию?
- **Внутренние связи:** Preserve canonical owner/support relationships from Stage 05
- **Пример реализации:** Использовать осмысленную ссылку/якорь по задаче, не создавая дублирующую посадочную страницу.
- **Критерии приёмки:** Целевая страница/объект и каноническое действие совпадают с текущей властью; нет противоречащего клиентского представления.
- **Зависимости:** NONE
- **Запрещённое утверждение/действие:** No private performance evidence.
- **Подтверждение клиента:** NO
- **Владелец, трудоёмкость, ёмкость и срок:** не назначены и не выдуманы.

### S18-A006 — ROUTING_OWNER_UPDATE

- **Состояние спецификации:** `READY_ROUTING`
- **Приоритет:** `P1_HIGH`
- **Целевая страница/объект:** https://okno-msk.ru/okna-rehau/steklopakety-dlya-plastikovykh-okon
- **AS-IS:** Сохранённое текущее состояние: Route commercial glass-unit selection to exact product hub while keeping informational glass-unit need separate.
- **Доказательство:** STEP_14A_ARCHITECTURE_DELTA.tsv
- **Почему требуется действие:** Fresh discovery supplies the exact commercial owner missing from older routing.
- **TO-BE:** Route commercial glass-unit selection to exact product hub while keeping informational glass-unit need separate.
- **Точное место:** Семантическое владение, хлебные крошки и контекстные ссылки; контент не переписывать без отдельного дефекта.
- **Темы:** Задача пользователя: understand/select glazing units; choose glazing unit for a PVC window
- **Фразы-примеры:** окна стеклопакеты rehau | панорамное окно стеклопакет | стеклопакет на пластиковое окно цена | стеклопакеты для пластиковых окон | стеклопакеты французские окна | как выбрать стеклопакет для пластиковых окон
- **Вопросы, на которые должен ответить блок:** Какая страница отвечает на точную задачу? Как пользователь переходит к следующему релевантному действию?
- **Внутренние связи:** Preserve canonical owner/support relationships from Stage 05
- **Пример реализации:** Использовать осмысленную ссылку/якорь по задаче, не создавая дублирующую посадочную страницу.
- **Критерии приёмки:** Целевая страница/объект и каноническое действие совпадают с текущей властью; нет противоречащего клиентского представления.
- **Зависимости:** NONE
- **Запрещённое утверждение/действие:** No performance or revenue claim.
- **Подтверждение клиента:** NO
- **Владелец, трудоёмкость, ёмкость и срок:** не назначены и не выдуманы.

### S18-A007 — ROLE_DIFFERENTIATION_RECHECK

- **Состояние спецификации:** `NOT_READY__ROLE_DIFFERENTIATION_PENDING`
- **Приоритет:** `P1_HIGH`
- **Целевая страница/объект:** https://okno-msk.ru/stati/sravnenie-profilej-rehau
- **AS-IS:** Сохранённое текущее состояние: Differentiate product-integrated Rehau comparison owner from same-task article; preserve current product-integrated primary.
- **Доказательство:** STEP_14A_ARCHITECTURE_DELTA.tsv
- **Почему требуется действие:** Fresh discovery found a second same-task comparison page requiring explicit role separation.
- **TO-BE:** Differentiate product-integrated Rehau comparison owner from same-task article; preserve current product-integrated primary.
- **Точное место:** На целевом объекте согласно типу действия.
- **Темы:** Задача пользователя: compare Rehau profile systems/models; understand Rehau window systems/construction/types
- **Фразы-примеры:** окна rehau сравнение | чем отличается окна rehau delight от rehau | rehau окно конструкция | окна rehau виды | окна система rehau
- **Вопросы, на которые должен ответить блок:** Какая страница отвечает на точную задачу? Как пользователь переходит к следующему релевантному действию?
- **Внутренние связи:** Preserve canonical owner/support relationships from Stage 05
- **Пример реализации:** Следовать каноническому описанию действия.
- **Критерии приёмки:** Действие не публикуется как готовое; неопределённость и запрещённые разрушительные операции сохранены.
- **Зависимости:** NONE
- **Запрещённое утверждение/действие:** No merge/delete/canonical action authorized; no historical harm claim.
- **Подтверждение клиента:** NO
- **Владелец, трудоёмкость, ёмкость и срок:** не назначены и не выдуманы.

### S18-A008 — OWNER_SPECIALIST_UPDATE

- **Состояние спецификации:** `READY_ROUTING`
- **Приоритет:** `P1_HIGH`
- **Целевая страница/объект:** https://okno-msk.ru/verandy/razdvizhnye-okna-na-verandu
- **AS-IS:** Сохранённое текущее состояние: Use exact sliding-veranda page for explicit sliding intent; retain /verandy for general non-sliding glazing.
- **Доказательство:** STEP_14A_ARCHITECTURE_DELTA.tsv
- **Почему требуется действие:** Exact specialist ownership should be fixed before generic veranda routing/links.
- **TO-BE:** Use exact sliding-veranda page for explicit sliding intent; retain /verandy for general non-sliding glazing.
- **Точное место:** Семантическое владение, хлебные крошки и контекстные ссылки; контент не переписывать без отдельного дефекта.
- **Темы:** Задача пользователя: order aluminium sliding glazing for veranda/terrace/gazebo; order glazing of veranda/terrace/gazebo/porch
- **Фразы-примеры:** алюминиевое остекление веранды раздвижными конструкциями | алюминиевые окна для веранды и террасы раздвижные | алюминиевые окна раздвижные для террасы цены | алюминиевые раздвижные окна для беседки | алюминиевые раздвижные окна для веранды в можайске | алюминиевые раздвижные окна для веранды цена | окна раздвижные алюминиевые для веранды | provedal остекление веранды | vidno pro раздвижное остекление террас веранд беседок | алюминиевое остекление веранды
- **Вопросы, на которые должен ответить блок:** Какая страница отвечает на точную задачу? Как пользователь переходит к следующему релевантному действию?
- **Внутренние связи:** Preserve canonical owner/support relationships from Stage 05
- **Пример реализации:** Использовать осмысленную ссылку/якорь по задаче, не создавая дублирующую посадочную страницу.
- **Критерии приёмки:** Целевая страница/объект и каноническое действие совпадают с текущей властью; нет противоречащего клиентского представления.
- **Зависимости:** NONE
- **Запрещённое утверждение/действие:** No private performance evidence.
- **Подтверждение клиента:** NO
- **Владелец, трудоёмкость, ёмкость и срок:** не назначены и не выдуманы.

### S18-A009 — CONTENT_ENHANCEMENT

- **Состояние спецификации:** `READY_CONTENT_BOUNDED`
- **Приоритет:** `P1_HIGH`
- **Целевая страница/объект:** https://okno-msk.ru/okna-rehau/francuzskie-okna
- **AS-IS:** Действующая страница уже объясняет базовую сущность французского окна и содержит конфигурационно-ценовой контекст; различие «французское / панорамное» раскрыто недостаточно явно.
- **Доказательство:** STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V6.tsv;STEP_17_CASE_COMPARISON_LEDGER_V2_FINAL.tsv
- **Почему требуется действие:** High-demand commercial owner has a directly observed narrow gap; AI supports explanatory depth without ownership change.
- **TO-BE:** Strengthen existing French-window page for verified configuration/replacement needs and concise French-vs-panoramic selection depth.
- **Точное место:** После вводного определения, до ценовых/конфигурационных блоков.
- **Темы:** критерии французского окна; отличие от панорамного остекления; замена балконного блока; конфигурации; границы терминов
- **Фразы-примеры:** балконный блок французское окно | большие французские окна | высокие французские окна | замена балконного блока на французское окно | остекление французское окно | пластиковые окна французское окно | сколько стоят французские окна | стоимость французского окна | французские балконные окна | французские окна
- **Вопросы, на которые должен ответить блок:** Когда окно считается французским? Чем оно отличается от панорамного? Что можно заменить без изменения проёма?
- **Внутренние связи:** Preserve canonical owner/support relationships from Stage 05
- **Пример реализации:** Добавить компактную таблицу: термин → обязательный признак → типичная задача → когда нужен замер/согласование.
- **Критерии приёмки:** Базовое определение не дублируется; различия сформулированы без обещаний разрешимости перепланировки; сохранены CTA и существующая ценовая информация.
- **Зависимости:** NONE
- **Запрещённое утверждение/действие:** One exact-query AI snapshot; candidate is not proof every topic is absent.
- **Подтверждение клиента:** NO
- **Владелец, трудоёмкость, ёмкость и срок:** не назначены и не выдуманы.

### S18-A010 — CONTENT_ENHANCEMENT

- **Состояние спецификации:** `READY_CONTENT_BOUNDED`
- **Приоритет:** `P1_HIGH`
- **Целевая страница/объект:** https://okno-msk.ru/okna-rehau/po-tipu-doma/okna-v-chastnyj-dom
- **AS-IS:** Страница продаёт остекление частного дома и направляет на замер, но не даёт ясной модели стандартного и нестандартного проёма.
- **Доказательство:** STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V6.tsv
- **Почему требуется действие:** Substantial planning task has a revalidated current-page content gap while owner is correct.
- **TO-BE:** Add standard/non-standard opening dimensions and sizing guidance, explaining why individual measurement overrides generic standards.
- **Точное место:** В блоке выбора/замера перед калькулятором или заявкой.
- **Темы:** типовые и нетиповые размеры; ограничения открывания; роль конструкции дома; индивидуальный замер; почему общий стандарт не заменяет проект
- **Фразы-примеры:** варианты окон для частного дома | виды окон для частного дома фото | виды пластиковых окон для частного дома | виды пластиковых окон для частного дома фото | выбираем окна для частного дома | высота окон для частного дома | как выбрать окна пластиковые для частного дома | какие выбрать пластиковые окна для частного дома | какие окна выбрать для частного дома | какие окна для частного дома
- **Вопросы, на которые должен ответить блок:** Какие размеры считать ориентировочными? Когда проём нестандартный? Почему замер важнее каталожного размера?
- **Внутренние связи:** Preserve canonical owner/support relationships from Stage 05
- **Пример реализации:** Сделать таблицу «ситуация → что проверяет замерщик → что влияет на конфигурацию», без фиктивных универсальных чисел.
- **Критерии приёмки:** Есть практическое объяснение стандартности; нет выдуманных нормативов; индивидуальный замер явно является окончательным источником размеров.
- **Зависимости:** NONE
- **Запрещённое утверждение/действие:** No conversion/performance evidence; no traffic guarantee.
- **Подтверждение клиента:** NO
- **Владелец, трудоёмкость, ёмкость и срок:** не назначены и не выдуманы.

### S18-A011 — CONTENT_EXPANSION

- **Состояние спецификации:** `NOT_READY__BRAND_AVAILABILITY_CONFIRMATION`
- **Приоритет:** `P1_HIGH`
- **Целевая страница/объект:** https://okno-msk.ru/stati/kak-vybrat-plastikovye-okna
- **AS-IS:** Гайд уже содержит раздел о фурнитуре и называет Siegenia Aubi, Roto, Maco и Winkhaus; запрошенные Accado/Vorne/Futurus на странице не обнаружены.
- **Доказательство:** STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V6.tsv
- **Почему требуется действие:** Accepted owner retains a coherent 28-phrase decision task with directly observed missing hardware depth.
- **TO-BE:** Expand selection guide with hardware construction/parts, broader queried-brand comparison and Accado/Vorne/Futurus coverage.
- **Точное место:** Раздел «Фурнитура».
- **Темы:** конструкция и функции фурнитуры; проверяемые различия брендов; доступность брендов в текущем ассортименте
- **Фразы-примеры:** accado или vorne фурнитура оконная лучше | futurus фурнитура оконная производитель | как называется оконная фурнитура | как устроена оконная фурнитура | какая бывает оконная фурнитура | какая оконная фурнитура лучше | какая оконная фурнитура лучше рото или зигения | конструкция оконной фурнитуры | логотипы оконной фурнитуры | лучшая оконная фурнитура
- **Вопросы, на которые должен ответить блок:** Какие элементы влияют на герметичность и безопасность? Какие функции реально доступны? Какие бренды компания действительно поставляет?
- **Внутренние связи:** Preserve canonical owner/support relationships from Stage 05
- **Пример реализации:** Сравнительную таблицу брендов публиковать только после подтверждения ассортимента и характеристик из актуального каталога/коммерческого источника.
- **Критерии приёмки:** До подтверждения ассортимента неподтверждённые бренды не объявлены доступными; существующие бренды и функции описаны с источником/датой.
- **Зависимости:** NONE
- **Запрещённое утверждение/действие:** No internal business priority/conversion data; comparisons must remain evidence-based/current.
- **Подтверждение клиента:** NO
- **Владелец, трудоёмкость, ёмкость и срок:** не назначены и не выдуманы.

### S18-A012 — CONTENT_ENHANCEMENT

- **Состояние спецификации:** `READY_CONTENT_BOUNDED`
- **Приоритет:** `P1_HIGH`
- **Целевая страница/объект:** https://okno-msk.ru/dveri-rehau
- **AS-IS:** Страница уже содержит цену, калькулятор, замер и упоминания монтажа/сложности установки, но не раскрывает дверной монтаж как понятный процесс и состав услуги.
- **Доказательство:** STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V6.tsv
- **Почему требуется действие:** Professional installation remains a proven service task, but Step20 current-page QA showed price/price-estimation guidance is already materially present; only the remaining installation-process depth is still supported as a content gap.
- **TO-BE:** Retain the current door price/price-estimation guidance; strengthen only the still-missing door-specific professional installation scope/process, including what the service covers and how the installation service is explained on the accepted PVC-door page.
- **Точное место:** Новый короткий блок после цен/калькулятора либо перед формой бесплатного замера.
- **Темы:** этапы замера и установки; подготовка проёма; крепление/герметизация; регулировка; приёмка; что входит и не входит
- **Фразы-примеры:** балконное окно с дверью пластиковое цена установкой | установка пластикового окна с балконной дверью | установка пластиковой балконной двери | установка пластиковой двери | установка пластиковой двери цена | установка пластиковых дверей москва | установка пластиковых дверей цена москва | установка пластиковых окон и дверей
- **Вопросы, на которые должен ответить блок:** Что входит в монтаж? Что проверяется после установки? Что должен подготовить клиент?
- **Внутренние связи:** Preserve canonical owner/support relationships from Stage 05
- **Пример реализации:** Добавить чек-лист «замер → согласование комплектации → монтаж → регулировка → приёмка/гарантия»; цены не дублировать.
- **Критерии приёмки:** Существующие цены сохранены; состав и границы услуги ясны; нет обещаний работ, не подтверждённых компанией.
- **Зависимости:** NONE
- **Запрещённое утверждение/действие:** Do not recreate or duplicate the existing price factors/calculator/measurer guidance; internal standalone-installation priority remains unknown; no traffic/conversion claim.
- **Подтверждение клиента:** CONDITIONAL_IF_SERVICE_SCOPE_CHANGED
- **Владелец, трудоёмкость, ёмкость и срок:** не назначены и не выдуманы.

### S18-A013 — SUPPORT_ROUTING

- **Состояние спецификации:** `READY_SUPPORT_ROUTING`
- **Приоритет:** `P2_MEDIUM`
- **Целевая страница/объект:** https://okno-msk.ru/alyuminievye-okna/provedal
- **AS-IS:** Сохранённое текущее состояние: Add Provedal hub as support for aluminium/cold sliding tasks while retaining generic owners.
- **Доказательство:** STEP_14A_ARCHITECTURE_DELTA.tsv
- **Почему требуется действие:** Exact material/system support improves routing without replacing generic owners.
- **TO-BE:** Add Provedal hub as support for aluminium/cold sliding tasks while retaining generic owners.
- **Точное место:** Семантическое владение, хлебные крошки и контекстные ссылки; контент не переписывать без отдельного дефекта.
- **Темы:** Задача пользователя: buy/order aluminium windows; choose/buy aluminium window profile/system; order cold aluminium sliding glazing for balcony/loggia
- **Фразы-примеры:** алюминиевое окно наружное | алюминиевые балконные окна | алюминиевые вертикальные окна | алюминиевые витражные окна | алюминиевые накладки на окна | алюминиевые окна | алюминиевые окна alutech | алюминиевые окна provedal | алюминиевые окна schuco | алюминиевые окна алютех
- **Вопросы, на которые должен ответить блок:** Какая страница отвечает на точную задачу? Как пользователь переходит к следующему релевантному действию?
- **Внутренние связи:** Preserve canonical owner/support relationships from Stage 05
- **Пример реализации:** Использовать осмысленную ссылку/якорь по задаче, не создавая дублирующую посадочную страницу.
- **Критерии приёмки:** Целевая страница/объект и каноническое действие совпадают с текущей властью; нет противоречащего клиентского представления.
- **Зависимости:** NONE
- **Запрещённое утверждение/действие:** No performance claim.
- **Подтверждение клиента:** NO
- **Владелец, трудоёмкость, ёмкость и срок:** не назначены и не выдуманы.

### S18-A014 — SUPPORT_ROUTING

- **Состояние спецификации:** `READY_SUPPORT_ROUTING`
- **Приоритет:** `P2_MEDIUM`
- **Целевая страница/объект:** https://okno-msk.ru/balkony-i-lodzhii/francuzskoe-osteklenie-balkona
- **AS-IS:** Сохранённое текущее состояние: Add balcony-specific French page as intersection support while retaining French and panoramic-balcony primaries.
- **Доказательство:** STEP_14A_ARCHITECTURE_DELTA.tsv
- **Почему требуется действие:** Exact intersection support improves task handoff without changing primaries.
- **TO-BE:** Add balcony-specific French page as intersection support while retaining French and panoramic-balcony primaries.
- **Точное место:** Семантическое владение, хлебные крошки и контекстные ссылки; контент не переписывать без отдельного дефекта.
- **Темы:** Задача пользователя: buy/order French windows; order/understand panoramic balcony/loggia glazing
- **Фразы-примеры:** балконный блок французское окно | большие французские окна | высокие французские окна | замена балконного блока на французское окно | остекление французское окно | пластиковые окна французское окно | сколько стоят французские окна | стоимость французского окна | французские балконные окна | французские окна
- **Вопросы, на которые должен ответить блок:** Какая страница отвечает на точную задачу? Как пользователь переходит к следующему релевантному действию?
- **Внутренние связи:** Preserve canonical owner/support relationships from Stage 05
- **Пример реализации:** Использовать осмысленную ссылку/якорь по задаче, не создавая дублирующую посадочную страницу.
- **Критерии приёмки:** Целевая страница/объект и каноническое действие совпадают с текущей властью; нет противоречащего клиентского представления.
- **Зависимости:** NONE
- **Запрещённое утверждение/действие:** No performance claim.
- **Подтверждение клиента:** NO
- **Владелец, трудоёмкость, ёмкость и срок:** не назначены и не выдуманы.

### S18-A015 — SUPPORT_ROUTING

- **Состояние спецификации:** `READY_SUPPORT_ROUTING`
- **Приоритет:** `P2_MEDIUM`
- **Целевая страница/объект:** https://okno-msk.ru/balkony-i-lodzhii/holodnoe-panoramnoe-osteklenie-balkona
- **AS-IS:** Сохранённое текущее состояние: Add cold+panoramic balcony specialist for exact intersection; retain generic primaries outside it.
- **Доказательство:** STEP_14A_ARCHITECTURE_DELTA.tsv
- **Почему требуется действие:** Specific intersection support is useful after primary boundaries are fixed.
- **TO-BE:** Add cold+panoramic balcony specialist for exact intersection; retain generic primaries outside it.
- **Точное место:** Семантическое владение, хлебные крошки и контекстные ссылки; контент не переписывать без отдельного дефекта.
- **Темы:** Задача пользователя: order/understand panoramic balcony/loggia glazing; order cold balcony/loggia glazing; order cold aluminium sliding glazing for balcony/loggia
- **Фразы-примеры:** остекление балкона в пол | панорамное остекление балкона | панорамные окна на балконе | панорамные окна на лоджии | замена холодного остекления балкона | окна балкон холодное остекление | остекление балкона холодное раздвижное | остекление холодного балкона окна алюминиевые холодные | раздвижные алюминиевые окна на балкон холодное остекление | холодное алюминиевое остекление балконов
- **Вопросы, на которые должен ответить блок:** Какая страница отвечает на точную задачу? Как пользователь переходит к следующему релевантному действию?
- **Внутренние связи:** Preserve canonical owner/support relationships from Stage 05
- **Пример реализации:** Использовать осмысленную ссылку/якорь по задаче, не создавая дублирующую посадочную страницу.
- **Критерии приёмки:** Целевая страница/объект и каноническое действие совпадают с текущей властью; нет противоречащего клиентского представления.
- **Зависимости:** NONE
- **Запрещённое утверждение/действие:** No performance claim.
- **Подтверждение клиента:** NO
- **Владелец, трудоёмкость, ёмкость и срок:** не назначены и не выдуманы.

### S18-A016 — SUPPORT_ROUTING

- **Состояние спецификации:** `READY_SUPPORT_ROUTING`
- **Приоритет:** `P2_MEDIUM`
- **Целевая страница/объект:** https://okno-msk.ru/balkony-i-lodzhii/osteklenie-profilem-provedal
- **AS-IS:** Сохранённое текущее состояние: Add exact Provedal balcony support while retaining broad/cold primaries according to intent.
- **Доказательство:** STEP_14A_ARCHITECTURE_DELTA.tsv
- **Почему требуется действие:** Material/mechanism support is valid but not a primary-boundary correction.
- **TO-BE:** Add exact Provedal balcony support while retaining broad/cold primaries according to intent.
- **Точное место:** Семантическое владение, хлебные крошки и контекстные ссылки; контент не переписывать без отдельного дефекта.
- **Темы:** Задача пользователя: order cold aluminium sliding glazing for balcony/loggia; order cold balcony/loggia glazing; choose/buy aluminium window profile/system
- **Фразы-примеры:** раздвижные окна на балкон алюминиевые холодное | замена холодного остекления балкона | окна балкон холодное остекление | остекление балкона холодное раздвижное | остекление холодного балкона окна алюминиевые холодные | раздвижные алюминиевые окна на балкон холодное остекление | холодное алюминиевое остекление балконов | холодное остекление балкона | холодное остекление балкона алюминиевым профилем | холодное остекление балкона москва цена
- **Вопросы, на которые должен ответить блок:** Какая страница отвечает на точную задачу? Как пользователь переходит к следующему релевантному действию?
- **Внутренние связи:** Preserve canonical owner/support relationships from Stage 05
- **Пример реализации:** Использовать осмысленную ссылку/якорь по задаче, не создавая дублирующую посадочную страницу.
- **Критерии приёмки:** Целевая страница/объект и каноническое действие совпадают с текущей властью; нет противоречащего клиентского представления.
- **Зависимости:** NONE
- **Запрещённое утверждение/действие:** No performance claim.
- **Подтверждение клиента:** NO
- **Владелец, трудоёмкость, ёмкость и срок:** не назначены и не выдуманы.

### S18-A017 — SUPPORT_ROUTING

- **Состояние спецификации:** `READY_SUPPORT_ROUTING`
- **Приоритет:** `P2_MEDIUM`
- **Целевая страница/объект:** https://okno-msk.ru/okna-rehau/izgotovlenie-steklopaketov-na-zakaz
- **AS-IS:** Сохранённое текущее состояние: Add existing custom glass-unit manufacturing specialist as routed subtask under glass-unit commercial family.
- **Доказательство:** STEP_14A_ARCHITECTURE_DELTA.tsv
- **Почему требуется действие:** Verified specialist supports a real subtask without a new page.
- **TO-BE:** Add existing custom glass-unit manufacturing specialist as routed subtask under glass-unit commercial family.
- **Точное место:** Семантическое владение, хлебные крошки и контекстные ссылки; контент не переписывать без отдельного дефекта.
- **Темы:** Задача пользователя: understand/select glazing units
- **Фразы-примеры:** окна стеклопакеты rehau | панорамное окно стеклопакет | стеклопакет на пластиковое окно цена | стеклопакеты для пластиковых окон | стеклопакеты французские окна
- **Вопросы, на которые должен ответить блок:** Какая страница отвечает на точную задачу? Как пользователь переходит к следующему релевантному действию?
- **Внутренние связи:** Preserve canonical owner/support relationships from Stage 05
- **Пример реализации:** Использовать осмысленную ссылку/якорь по задаче, не создавая дублирующую посадочную страницу.
- **Критерии приёмки:** Целевая страница/объект и каноническое действие совпадают с текущей властью; нет противоречащего клиентского представления.
- **Зависимости:** NONE
- **Запрещённое утверждение/действие:** No performance claim.
- **Подтверждение клиента:** NO
- **Владелец, трудоёмкость, ёмкость и срок:** не назначены и не выдуманы.

### S18-A018 — SUPPORT_ROUTING

- **Состояние спецификации:** `READY_SUPPORT_ROUTING`
- **Приоритет:** `P2_MEDIUM`
- **Целевая страница/объект:** https://okno-msk.ru/okna-rehau/po-tipu-doma/okna-na-kuhnyu
- **AS-IS:** Сохранённое текущее состояние: Add kitchen-window page as room-specific support; do not split aggregate room unit solely from this page.
- **Доказательство:** STEP_14A_ARCHITECTURE_DELTA.tsv
- **Почему требуется действие:** Narrow room support improves routing without broader architecture change.
- **TO-BE:** Add kitchen-window page as room-specific support; do not split aggregate room unit solely from this page.
- **Точное место:** Семантическое владение, хлебные крошки и контекстные ссылки; контент не переписывать без отдельного дефекта.
- **Темы:** Задача пользователя: choose/plan windows for special rooms in a private house; buy/order PVC windows
- **Фразы-примеры:** купить окно для газовой котельной частного дома | окна для кухни частном доме | окна для санузла в частном доме | окно для ванной в частном доме | окно для ванной комнаты в частном доме | окно для вентиляции в частном доме | окно для газовой котельной частного дома | окно для котельной в частном доме | окно для котельной в частном доме купить | размер окна для санузла в частном доме
- **Вопросы, на которые должен ответить блок:** Какая страница отвечает на точную задачу? Как пользователь переходит к следующему релевантному действию?
- **Внутренние связи:** Preserve canonical owner/support relationships from Stage 05
- **Пример реализации:** Использовать осмысленную ссылку/якорь по задаче, не создавая дублирующую посадочную страницу.
- **Критерии приёмки:** Целевая страница/объект и каноническое действие совпадают с текущей властью; нет противоречащего клиентского представления.
- **Зависимости:** NONE
- **Запрещённое утверждение/действие:** No performance claim.
- **Подтверждение клиента:** NO
- **Владелец, трудоёмкость, ёмкость и срок:** не назначены и не выдуманы.

### S18-A019 — SUPPORT_ROUTING

- **Состояние спецификации:** `READY_SUPPORT_ROUTING`
- **Приоритет:** `P2_MEDIUM`
- **Целевая страница/объект:** https://okno-msk.ru/okna-rehau/tipovye-razmery
- **AS-IS:** Сохранённое текущее состояние: Add commercial standard-size hub as support while retaining informational dimensions owner.
- **Доказательство:** STEP_14A_ARCHITECTURE_DELTA.tsv
- **Почему требуется действие:** Separates commercial sizing route from informational dimensions.
- **TO-BE:** Add commercial standard-size hub as support while retaining informational dimensions owner.
- **Точное место:** Семантическое владение, хлебные крошки и контекстные ссылки; контент не переписывать без отдельного дефекта.
- **Темы:** Задача пользователя: find window/product dimensions and sizing information; buy/order PVC windows
- **Фразы-примеры:** алюминиевое окно размеры | алюминиевые окна ширина | алюминиевый м2 окно | высота панорамных окон | высота пластиковых окон | высота французских окон | окна rehau 70 мм | окна rehau grazio 70 мм | окна rehau размеры | окна серия п 44 размеры
- **Вопросы, на которые должен ответить блок:** Какая страница отвечает на точную задачу? Как пользователь переходит к следующему релевантному действию?
- **Внутренние связи:** Preserve canonical owner/support relationships from Stage 05
- **Пример реализации:** Использовать осмысленную ссылку/якорь по задаче, не создавая дублирующую посадочную страницу.
- **Критерии приёмки:** Целевая страница/объект и каноническое действие совпадают с текущей властью; нет противоречащего клиентского представления.
- **Зависимости:** NONE
- **Запрещённое утверждение/действие:** No performance claim.
- **Подтверждение клиента:** NO
- **Владелец, трудоёмкость, ёмкость и срок:** не назначены и не выдуманы.

### S18-A020 — SUPPORT_ROUTING

- **Состояние спецификации:** `READY_SUPPORT_ROUTING`
- **Приоритет:** `P2_MEDIUM`
- **Целевая страница/объект:** https://okno-msk.ru/okna-rehau/tipovye-razmery/katalog-tipovyh-okon
- **AS-IS:** Сохранённое текущее состояние: Add typed-window catalog as commercial support while retaining informational dimensions owner.
- **Доказательство:** STEP_14A_ARCHITECTURE_DELTA.tsv
- **Почему требуется действие:** Catalog support improves commercial handoff from sizing information.
- **TO-BE:** Add typed-window catalog as commercial support while retaining informational dimensions owner.
- **Точное место:** Семантическое владение, хлебные крошки и контекстные ссылки; контент не переписывать без отдельного дефекта.
- **Темы:** Задача пользователя: find window/product dimensions and sizing information; buy/order PVC windows
- **Фразы-примеры:** алюминиевое окно размеры | алюминиевые окна ширина | алюминиевый м2 окно | высота панорамных окон | высота пластиковых окон | высота французских окон | окна rehau 70 мм | окна rehau grazio 70 мм | окна rehau размеры | окна серия п 44 размеры
- **Вопросы, на которые должен ответить блок:** Какая страница отвечает на точную задачу? Как пользователь переходит к следующему релевантному действию?
- **Внутренние связи:** Preserve canonical owner/support relationships from Stage 05
- **Пример реализации:** Использовать осмысленную ссылку/якорь по задаче, не создавая дублирующую посадочную страницу.
- **Критерии приёмки:** Целевая страница/объект и каноническое действие совпадают с текущей властью; нет противоречащего клиентского представления.
- **Зависимости:** NONE
- **Запрещённое утверждение/действие:** No performance claim.
- **Подтверждение клиента:** NO
- **Владелец, трудоёмкость, ёмкость и срок:** не назначены и не выдуманы.

### S18-A021 — SUPPORT_ROUTING

- **Состояние спецификации:** `READY_SUPPORT_ROUTING`
- **Приоритет:** `P2_MEDIUM`
- **Целевая страница/объект:** https://okno-msk.ru/stati/kak-vybrat-plastikovye-okna-v-kvartiru
- **AS-IS:** Сохранённое текущее состояние: Add apartment-specific selection guide as narrow support while retaining broad/best-windows owners.
- **Доказательство:** STEP_14A_ARCHITECTURE_DELTA.tsv
- **Почему требуется действие:** Narrow context support improves information routing without changing broad ownership.
- **TO-BE:** Add apartment-specific selection guide as narrow support while retaining broad/best-windows owners.
- **Точное место:** Семантическое владение, хлебные крошки и контекстные ссылки; контент не переписывать без отдельного дефекта.
- **Темы:** Задача пользователя: choose windows/products
- **Фразы-примеры:** как выбрать качественные пластиковые окна | как выбрать окно пластиковое в квартиру правильно | как выбрать окно пластиковое для дома | как выбрать пластиковое окно рекомендации эксперта | как выбрать пластиковые окна | как выбрать пластиковые окна для квартиры | как выбрать пластиковые окна для частного | как выбрать пластиковые окна какие | как выбрать пластиковые окна рекомендации | как выбрать размер пластикового окна
- **Вопросы, на которые должен ответить блок:** Какая страница отвечает на точную задачу? Как пользователь переходит к следующему релевантному действию?
- **Внутренние связи:** Preserve canonical owner/support relationships from Stage 05
- **Пример реализации:** Использовать осмысленную ссылку/якорь по задаче, не создавая дублирующую посадочную страницу.
- **Критерии приёмки:** Целевая страница/объект и каноническое действие совпадают с текущей властью; нет противоречащего клиентского представления.
- **Зависимости:** NONE
- **Запрещённое утверждение/действие:** No performance claim.
- **Подтверждение клиента:** NO
- **Владелец, трудоёмкость, ёмкость и срок:** не назначены и не выдуманы.

### S18-A022 — SUPPORT_ROUTING

- **Состояние спецификации:** `READY_SUPPORT_ROUTING`
- **Приоритет:** `P2_MEDIUM`
- **Целевая страница/объект:** https://okno-msk.ru/stati/kakoj-profil-i-firma-luchshe
- **AS-IS:** Сохранённое текущее состояние: Add narrow profile/manufacturer comparison article as support while retaining broad selection ownership.
- **Доказательство:** STEP_14A_ARCHITECTURE_DELTA.tsv
- **Почему требуется действие:** Specific comparison support does not supersede broad owners.
- **TO-BE:** Add narrow profile/manufacturer comparison article as support while retaining broad selection ownership.
- **Точное место:** Семантическое владение, хлебные крошки и контекстные ссылки; контент не переписывать без отдельного дефекта.
- **Темы:** Задача пользователя: choose PVC window profile/system; choose windows/products
- **Фразы-примеры:** как выбрать профиль для пластиковых окон правильно | пластиковое окно как выбрать профиль | как выбрать качественные пластиковые окна | как выбрать окно пластиковое в квартиру правильно | как выбрать окно пластиковое для дома | как выбрать пластиковое окно рекомендации эксперта | как выбрать пластиковые окна | как выбрать пластиковые окна для квартиры | как выбрать пластиковые окна для частного | как выбрать пластиковые окна какие
- **Вопросы, на которые должен ответить блок:** Какая страница отвечает на точную задачу? Как пользователь переходит к следующему релевантному действию?
- **Внутренние связи:** Preserve canonical owner/support relationships from Stage 05
- **Пример реализации:** Использовать осмысленную ссылку/якорь по задаче, не создавая дублирующую посадочную страницу.
- **Критерии приёмки:** Целевая страница/объект и каноническое действие совпадают с текущей властью; нет противоречащего клиентского представления.
- **Зависимости:** NONE
- **Запрещённое утверждение/действие:** No performance claim.
- **Подтверждение клиента:** NO
- **Владелец, трудоёмкость, ёмкость и срок:** не назначены и не выдуманы.

### S18-A023 — SUPPORT_ROUTING

- **Состояние спецификации:** `READY_SUPPORT_ROUTING`
- **Приоритет:** `P2_MEDIUM`
- **Целевая страница/объект:** https://okno-msk.ru/stati/steklopakety-osobennosti-i-vidy
- **AS-IS:** Сохранённое текущее состояние: Add glass-unit types/features article as informational support; keep commercial glass-unit hub distinct.
- **Доказательство:** STEP_14A_ARCHITECTURE_DELTA.tsv
- **Почему требуется действие:** Improves separation between informational selection and commercial product intent.
- **TO-BE:** Add glass-unit types/features article as informational support; keep commercial glass-unit hub distinct.
- **Точное место:** Семантическое владение, хлебные крошки и контекстные ссылки; контент не переписывать без отдельного дефекта.
- **Темы:** Задача пользователя: choose glazing unit for a PVC window; understand/select glazing units
- **Фразы-примеры:** как выбрать стеклопакет для пластиковых окон | окна стеклопакеты rehau | панорамное окно стеклопакет | стеклопакет на пластиковое окно цена | стеклопакеты для пластиковых окон | стеклопакеты французские окна
- **Вопросы, на которые должен ответить блок:** Какая страница отвечает на точную задачу? Как пользователь переходит к следующему релевантному действию?
- **Внутренние связи:** Preserve canonical owner/support relationships from Stage 05
- **Пример реализации:** Использовать осмысленную ссылку/якорь по задаче, не создавая дублирующую посадочную страницу.
- **Критерии приёмки:** Целевая страница/объект и каноническое действие совпадают с текущей властью; нет противоречащего клиентского представления.
- **Зависимости:** NONE
- **Запрещённое утверждение/действие:** No performance claim.
- **Подтверждение клиента:** NO
- **Владелец, трудоёмкость, ёмкость и срок:** не назначены и не выдуманы.

### S18-A024 — SUPPORT_ROUTING

- **Состояние спецификации:** `READY_SUPPORT_ROUTING`
- **Приоритет:** `P2_MEDIUM`
- **Целевая страница/объект:** https://okno-msk.ru/stati/vidy-i-tipy-ostekleniya-verandy-plyusy-i-minusy
- **AS-IS:** Сохранённое текущее состояние: Add veranda glazing types/choice article as informational support while retaining /verandy as commercial primary.
- **Доказательство:** STEP_14A_ARCHITECTURE_DELTA.tsv
- **Почему требуется действие:** Direct informational specialist supports selection without changing commercial ownership.
- **TO-BE:** Add veranda glazing types/choice article as informational support while retaining /verandy as commercial primary.
- **Точное место:** Семантическое владение, хлебные крошки и контекстные ссылки; контент не переписывать без отдельного дефекта.
- **Темы:** Задача пользователя: understand special veranda glazing techniques/material choices; order glazing of veranda/terrace/gazebo/porch
- **Фразы-примеры:** безрамное остекление веранды плюсы и минусы | толщина монолитного поликарбоната для остекления веранды | provedal остекление веранды | vidno pro раздвижное остекление террас веранд беседок | алюминиевое остекление веранды | алюминиевое остекление веранды даче | алюминиевое остекление веранды и террасы | алюминиевое остекление веранды на даче цена | алюминиевое остекление веранды цена | алюминиевые остекление веранды и террасы цена
- **Вопросы, на которые должен ответить блок:** Какая страница отвечает на точную задачу? Как пользователь переходит к следующему релевантному действию?
- **Внутренние связи:** Preserve canonical owner/support relationships from Stage 05
- **Пример реализации:** Использовать осмысленную ссылку/якорь по задаче, не создавая дублирующую посадочную страницу.
- **Критерии приёмки:** Целевая страница/объект и каноническое действие совпадают с текущей властью; нет противоречащего клиентского представления.
- **Зависимости:** NONE
- **Запрещённое утверждение/действие:** No performance claim.
- **Подтверждение клиента:** NO
- **Владелец, трудоёмкость, ёмкость и срок:** не назначены и не выдуманы.

### S18-A025 — SUPPORT_ROUTING

- **Состояние спецификации:** `READY_SUPPORT_ROUTING`
- **Приоритет:** `P2_MEDIUM`
- **Целевая страница/объект:** https://okno-msk.ru/verandy/bezramnoe-osteklenie-verandy
- **AS-IS:** Сохранённое текущее состояние: Add exact frameless-veranda specialist for explicit frameless intent; retain /verandy for general glazing.
- **Доказательство:** STEP_14A_ARCHITECTURE_DELTA.tsv
- **Почему требуется действие:** Exact mechanism support improves routing while general owner remains valid.
- **TO-BE:** Add exact frameless-veranda specialist for explicit frameless intent; retain /verandy for general glazing.
- **Точное место:** Семантическое владение, хлебные крошки и контекстные ссылки; контент не переписывать без отдельного дефекта.
- **Темы:** Задача пользователя: order glazing of veranda/terrace/gazebo/porch; understand special veranda glazing techniques/material choices
- **Фразы-примеры:** provedal остекление веранды | vidno pro раздвижное остекление террас веранд беседок | алюминиевое остекление веранды | алюминиевое остекление веранды даче | алюминиевое остекление веранды и террасы | алюминиевое остекление веранды на даче цена | алюминиевое остекление веранды цена | алюминиевые остекление веранды и террасы цена | алюминиевый профиль для остекления веранды | безрамное остекление веранды
- **Вопросы, на которые должен ответить блок:** Какая страница отвечает на точную задачу? Как пользователь переходит к следующему релевантному действию?
- **Внутренние связи:** Preserve canonical owner/support relationships from Stage 05
- **Пример реализации:** Использовать осмысленную ссылку/якорь по задаче, не создавая дублирующую посадочную страницу.
- **Критерии приёмки:** Целевая страница/объект и каноническое действие совпадают с текущей властью; нет противоречащего клиентского представления.
- **Зависимости:** NONE
- **Запрещённое утверждение/действие:** No performance claim.
- **Подтверждение клиента:** NO
- **Владелец, трудоёмкость, ёмкость и срок:** не назначены и не выдуманы.

### S18-A026 — CONTENT_ENHANCEMENT

- **Состояние спецификации:** `READY_CONTENT_BOUNDED`
- **Приоритет:** `P2_MEDIUM`
- **Целевая страница/объект:** https://okno-msk.ru/stati/plyusy-i-minusy-ostekleniya-alyuminievymi-oknami
- **AS-IS:** Статья подробно сравнивает тёплый/холодный алюминий и упоминает вентиляцию лишь обобщённо; отдельной практической модели воздухообмена не обнаружено.
- **Доказательство:** STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V6.tsv
- **Почему требуется действие:** Correct owner retains a narrow revalidated information gap.
- **TO-BE:** Add aluminium-specific ventilation, micro-ventilation and ventilation-valve guidance to accepted technical article.
- **Точное место:** После раздела недостатков или в советах по остеклению.
- **Темы:** проветривание; микропроветривание при совместимой фурнитуре; клапаны; конденсат; отличие жилого и сезонного помещения
- **Фразы-примеры:** виды алюминиевых окон | как выглядят алюминиевые окна | конструкция алюминиевого окна | открывание алюминиевых окон | проветривание алюминиевые окна | системы алюминиевых окон | цвета алюминиевых окон | чем отличаются алюминиевые окна
- **Вопросы, на которые должен ответить блок:** Когда естественного проветривания недостаточно? Какие варианты зависят от конструкции створки? Что не исправляет холодный профиль?
- **Внутренние связи:** Preserve canonical owner/support relationships from Stage 05
- **Пример реализации:** Таблица «условие эксплуатации → риск → доступный способ вентиляции → ограничение».
- **Критерии приёмки:** Не обещана функция, которой нет в выбранной системе; холодный профиль не представлен как жилое решение; рекомендации привязаны к типу открывания.
- **Зависимости:** NONE
- **Запрещённое утверждение/действие:** No private performance data.
- **Подтверждение клиента:** NO
- **Владелец, трудоёмкость, ёмкость и срок:** не назначены и не выдуманы.

### S18-A027 — CONTENT_ENHANCEMENT

- **Состояние спецификации:** `NO_SEPARATE_CHANGE__COMBINE_A009`
- **Приоритет:** `P2_MEDIUM`
- **Целевая страница/объект:** https://okno-msk.ru/okna-rehau/francuzskie-okna
- **AS-IS:** Базовое определение французского окна уже присутствует в основной странице.
- **Доказательство:** STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V6.tsv
- **Почему требуется действие:** Step20 current-page QA confirmed that a concise French-window/in-floor definition is already materially present; only residual naming/distinction guidance remains potentially useful and should be handled inside the broader French content action.
- **TO-BE:** Do not add a duplicate basic French-window definition. If terminology remains ambiguous, fold only residual naming/distinction guidance for French vs panoramic and imitation/partition/block terminology into the broader S18-A009 French-window content work.
- **Точное место:** Отдельный блок не создавать; остаточное уточнение включить в S18-A009.
- **Темы:** остаточная терминология: французское, панорамное, имитация/перегородка/балконный блок
- **Фразы-примеры:** виды французского окна | имитация французского окна | как выглядит французское окно | перегородка французское окно | французские окна название | французские окна это какие | французский блок окно | французский тип окон | французское окно как называется | что значит французское окно
- **Вопросы, на которые должен ответить блок:** Какие термины описывают конструкцию, а какие — визуальный эффект?
- **Внутренние связи:** Preserve canonical owner/support relationships from Stage 05
- **Пример реализации:** Одна примечательная строка/мини-словарь внутри блока S18-A009.
- **Критерии приёмки:** Нет отдельной дублирующей статьи или блока; терминология согласована с S18-A009.
- **Зависимости:** S18-A009
- **Запрещённое утверждение/действие:** No separate duplicate definition block; coordinate with S18-A009; close this package as no-separate-change if the broader edit already resolves the residual terminology distinction.
- **Подтверждение клиента:** NO
- **Владелец, трудоёмкость, ёмкость и срок:** не назначены и не выдуманы.

### S18-A028 — CONTENT_ENHANCEMENT

- **Состояние спецификации:** `READY_CONTENT_BOUNDED`
- **Приоритет:** `P2_MEDIUM`
- **Целевая страница/объект:** https://okno-msk.ru/dveri-rehau
- **AS-IS:** Страница дверей называет габариты проёма фактором цены и типовой блок, но не даёт понятной ориентации по ширине/высоте и критериям выбора.
- **Доказательство:** STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V6.tsv
- **Почему требуется действие:** Correct owner has a direct current-page dimension/selection gap.
- **TO-BE:** Add clear width/height/standard-size guidance and concise selection criteria to current PVC-door page.
- **Точное место:** После видов дверных створок, до цен.
- **Темы:** ширина/высота как проектные параметры; типовой и индивидуальный блок; порог; направление открывания; стеклопакет/сэндвич
- **Фразы-примеры:** высота пластиковой двери | как называется пластиковая дверь | лучшие пластиковые двери | пластиковые входные двери фото | пластиковые двери фото | размер пластиковой двери | цвета пластиковых дверей | ширина пластиковой двери
- **Вопросы, на которые должен ответить блок:** Какие размеры ориентировочные? Что меняет конфигурацию? Когда обязателен индивидуальный замер?
- **Внутренние связи:** Preserve canonical owner/support relationships from Stage 05
- **Пример реализации:** Таблица «параметр → на что влияет → что фиксируется после замера», без универсальных цифр без источника.
- **Критерии приёмки:** Критерии выбора понятны; каталожная ориентация не выдана за окончательный размер; связь с замером сохранена.
- **Зависимости:** NONE
- **Запрещённое утверждение/действие:** No private performance data; coordinate with S18-A012.
- **Подтверждение клиента:** NO
- **Владелец, трудоёмкость, ёмкость и срок:** не назначены и не выдуманы.

### S18-A029 — CONTENT_EXPANSION

- **Состояние спецификации:** `READY_CONTENT_BOUNDED`
- **Приоритет:** `P2_MEDIUM`
- **Целевая страница/объект:** https://okno-msk.ru/nashi-raboty
- **AS-IS:** Портфолио содержит реальные примеры, но текстовые фильтры/категории для ключевых типов работ не обнаружены.
- **Доказательство:** STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V6.tsv
- **Почему требуется действие:** Large inspiration task is served by portfolio but lacks usable taxonomy for accepted design families.
- **TO-BE:** Improve portfolio discoverability with meaningful labels/categories/filters for balcony, veranda, panoramic and French examples.
- **Точное место:** Над списком/сеткой работ.
- **Темы:** балконы; веранды; панорамное; французское; материал/тип открывания; жилое/сезонное
- **Фразы-примеры:** алюминиевое остекление веранды фото | алюминиевые окна фото | безрамное остекление веранды фото | варианты французских окон | дизайн кухни с панорамными окнами | дизайн остекления веранды в доме | дизайны панорамных окон | дом с французскими окнами | дома с панорамными окнами фото | интерьер с панорамными окнами
- **Вопросы, на которые должен ответить блок:** Как быстро найти похожий объект? Какой тип решения показан?
- **Внутренние связи:** Preserve canonical owner/support relationships from Stage 05
- **Пример реализации:** Фильтры с доступным текстовым состоянием и подписи карточек «тип объекта / система / задача».
- **Критерии приёмки:** Каждая категория ведёт к реально существующим работам; пустые фильтры не публикуются; фильтры доступны без JS-only смысла.
- **Зависимости:** NONE
- **Запрещённое утверждение/действие:** No measured conversion impact or known implementation effort.
- **Подтверждение клиента:** NO
- **Владелец, трудоёмкость, ёмкость и срок:** не назначены и не выдуманы.

### S18-A030 — CONTENT_RECHECK_AND_ENHANCEMENT

- **Состояние спецификации:** `READY_CONTENT_BOUNDED`
- **Приоритет:** `P2_MEDIUM`
- **Целевая страница/объект:** QF004 accepted aluminium owner/support pages; see Step17 ledger
- **AS-IS:** Основная алюминиевая страница раскрывает холодный профиль, крупные конструкции, способы открывания и применение, но отдельного сценария выбора панорамного алюминиевого решения не обнаружено.
- **Доказательство:** STEP_17_CASE_COMPARISON_LEDGER_V2_FINAL.tsv;STEP_17_V3_SCOPE_CONFIDENCE_LEDGER.tsv
- **Почему требуется действие:** Validated specialist sources expose plausible within-page depth opportunity while owner remains valid.
- **TO-BE:** Verify and if needed strengthen panoramic-aluminium subsection for warm/cold suitability, large-format/project constraints and selection criteria; no new page.
- **Точное место:** После способов открывания или сравнения профилей.
- **Темы:** панорамный формат; тёплый/холодный сценарий; крупный проём; вес/нагрузка; статический/проектный расчёт; выбор системы
- **Фразы-примеры:** алюминиевое окно наружное | алюминиевые балконные окна | алюминиевые вертикальные окна | алюминиевые витражные окна | алюминиевые накладки на окна | алюминиевые окна | алюминиевые окна alutech | алюминиевые окна provedal | алюминиевые окна schuco | алюминиевые окна алютех
- **Вопросы, на которые должен ответить блок:** Когда алюминий подходит для большого остекления? Когда нужен тёплый профиль? Какие ограничения определяет проект?
- **Внутренние связи:** Preserve canonical owner/support relationships from Stage 05
- **Пример реализации:** Добавить блок «панорамное алюминиевое остекление: 5 вопросов до расчёта», без создания нового URL.
- **Критерии приёмки:** Новый URL не создаётся; блок не обещает применимость без замера/проекта; холодный и тёплый сценарии не смешаны.
- **Зависимости:** NONE
- **Запрещённое утверждение/действие:** Candidate is not proof all topics are absent; one exact-query AI snapshot; no new page.
- **Подтверждение клиента:** NO
- **Владелец, трудоёмкость, ёмкость и срок:** не назначены и не выдуманы.

### S18-A031 — CONTENT_RECHECK_AND_ENHANCEMENT

- **Состояние спецификации:** `READY_CONTENT_BOUNDED`
- **Приоритет:** `P2_MEDIUM`
- **Целевая страница/объект:** https://okno-msk.ru/stati/kakie-okna-samye-luchshie
- **AS-IS:** Статья продолжает называть рейтинг 2024 года «в этом году», хотя сайт уже показывает 2026; критерии перечислены, но метод и дата списка не объяснены.
- **Доказательство:** STEP_17_CASE_COMPARISON_LEDGER_V2_FINAL.tsv;STEP_17_V3_SCOPE_CONFIDENCE_LEDGER.tsv
- **Почему требуется действие:** Direct ranking sources support freshness/methodology content check though architecture evidence is insufficient.
- **TO-BE:** Verify/update date-sensitive ranking evidence, state comparison criteria clearly and keep profile/model distinctions explicit; no split/consolidation from this case.
- **Точное место:** Раздел «Рейтинг производителей оконных профилей».
- **Темы:** дата актуальности; критерии; источник/метод сравнения; модель vs бренд; пределы рейтинга
- **Фразы-примеры:** лучшие пластиковые окна | лучшие пластиковые окна rehau | окна rehau какие лучше | рейтинг алюминиевых окон | рейтинг пластиковых окон
- **Вопросы, на которые должен ответить блок:** По каким критериям сформирован список? На какую дату? Какие характеристики сравниваются?
- **Внутренние связи:** Preserve canonical owner/support relationships from Stage 05
- **Пример реализации:** Заменить безусловный «рейтинг» на датированное сравнение по объявленным критериям либо подтвердить список актуальными источниками.
- **Критерии приёмки:** Нет формулировки «в этом году» с устаревшей датой; дата и критерии видимы; рекламное мнение не выдано за независимый рейтинг.
- **Зависимости:** NONE
- **Запрещённое утверждение/действие:** No target-domain AI role observed; one snapshot cannot establish hierarchy or justify split/merge.
- **Подтверждение клиента:** NO
- **Владелец, трудоёмкость, ёмкость и срок:** не назначены и не выдуманы.

### S18-A032 — INTERNAL_LINK_IMPLEMENTATION_BATCH

- **Состояние спецификации:** `READY_LINK_BATCH`
- **Приоритет:** `P2_MEDIUM`
- **Целевая страница/объект:** 15 IMPLEMENT rows in STEP_14_INTERNAL_LINK_ARCHITECTURE.tsv
- **AS-IS:** Сохранённое текущее состояние: Implement 15 accepted contextual internal-link handoffs; keep other 43 rows deferred/not-applicable.
- **Доказательство:** STEP_14_INTERNAL_LINK_ARCHITECTURE.tsv
- **Почему требуется действие:** Accepted links should be implemented after owner/specialist role corrections are reflected.
- **TO-BE:** Implement 15 accepted contextual internal-link handoffs; keep other 43 rows deferred/not-applicable.
- **Точное место:** На целевом объекте согласно типу действия.
- **Темы:** Задача пользователя: 
- **Фразы-примеры:** N/A — batch or non-phrase action
- **Вопросы, на которые должен ответить блок:** Какая страница отвечает на точную задачу? Как пользователь переходит к следующему релевантному действию?
- **Внутренние связи:** See Stage 06 link specification
- **Пример реализации:** Следовать каноническому описанию действия.
- **Критерии приёмки:** Целевая страница/объект и каноническое действие совпадают с текущей властью; нет противоречащего клиентского представления.
- **Зависимости:** S18-A001;S18-A002;S18-A003;S18-A004;S18-A005;S18-A006;S18-A007;S18-A008
- **Запрещённое утверждение/действие:** Effort unknown; only 15 accepted edges authorized, not 43 deferred/not-applicable rows.
- **Подтверждение клиента:** NO
- **Владелец, трудоёмкость, ёмкость и срок:** не назначены и не выдуманы.

### S18-A033 — ROUTING_IMPLEMENTATION_BATCH

- **Состояние спецификации:** `READY_ROUTING_BATCH`
- **Приоритет:** `P3_LATER`
- **Целевая страница/объект:** 46 ROUTE_TO_EXISTING_PAGE_AS_SUBTASK rows in STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V6.tsv
- **AS-IS:** Сохранённое текущее состояние: Implement accepted route-to-existing-page relationships for all 46 current route units, applying Step14A overlays as higher precedence.
- **Доказательство:** STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V6.tsv;STEP_14_REPORT.md;STEP_14A_ARCHITECTURE_DELTA.tsv
- **Почему требуется действие:** Valid broad routing follows higher-urgency exact owner/boundary corrections and content work.
- **TO-BE:** Implement accepted route-to-existing-page relationships for all 46 current route units, applying Step14A overlays as higher precedence.
- **Точное место:** Семантическое владение, хлебные крошки и контекстные ссылки; контент не переписывать без отдельного дефекта.
- **Темы:** Задача пользователя: 
- **Фразы-примеры:** N/A — batch or non-phrase action
- **Вопросы, на которые должен ответить блок:** Какая страница отвечает на точную задачу? Как пользователь переходит к следующему релевантному действию?
- **Внутренние связи:** See Stage 06 routing specification
- **Пример реализации:** Использовать осмысленную ссылку/якорь по задаче, не создавая дублирующую посадочную страницу.
- **Критерии приёмки:** Целевая страница/объект и каноническое действие совпадают с текущей властью; нет противоречащего клиентского представления.
- **Зависимости:** S18-A001;S18-A002;S18-A005;S18-A006;S18-A008;S18-A013;S18-A014;S18-A015;S18-A016;S18-A017;S18-A018;S18-A019;S18-A020;S18-A021;S18-A022;S18-A023;S18-A024;S18-A025
- **Запрещённое утверждение/действие:** One batch action accounts for 46 source units; exact membership remains in source ledger.
- **Подтверждение клиента:** NO
- **Владелец, трудоёмкость, ёмкость и срок:** не назначены и не выдуманы.

### S18-A034 — HOLD_RECHECK_BATCH

- **Состояние спецификации:** `HOLD__EVIDENCE_REQUIRED`
- **Приоритет:** `HOLD`
- **Целевая страница/объект:** 20 DEFER_PENDING_EVIDENCE rows in STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V6.tsv
- **AS-IS:** Сохранённое текущее состояние: Keep all 20 DEFER_PENDING_EVIDENCE structural units on HOLD; do not invent pages/content/service claims until each named gap is resolved.
- **Доказательство:** STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V6.tsv
- **Почему требуется действие:** Upstream records explicitly lack business truth, owner policy, normative evidence or stable task evidence; low demand is not the reason.
- **TO-BE:** Keep all 20 DEFER_PENDING_EVIDENCE structural units on HOLD; do not invent pages/content/service claims until each named gap is resolved.
- **Точное место:** На целевом объекте согласно типу действия.
- **Темы:** Задача пользователя: 
- **Фразы-примеры:** N/A — batch or non-phrase action
- **Вопросы, на которые должен ответить блок:** Какая страница отвечает на точную задачу? Как пользователь переходит к следующему релевантному действию?
- **Внутренние связи:** Preserve canonical owner/support relationships from Stage 05
- **Пример реализации:** Следовать каноническому описанию действия.
- **Критерии приёмки:** Целевая страница/объект и каноническое действие совпадают с текущей властью; нет противоречащего клиентского представления.
- **Зависимости:** NONE
- **Запрещённое утверждение/действие:** HOLD is not rejection or low value; required evidence/client truth remains unknown by row.
- **Подтверждение клиента:** CONDITIONAL_BY_ROW
- **Владелец, трудоёмкость, ёмкость и срок:** не назначены и не выдуманы.


## 4. Точные внутренние ссылки

| ID | Откуда | Куда | Смысл перехода |
|---|---|---|---|
| LNK001 | https://okno-msk.ru/alyuminievye-okna/razdvizhnye | https://okno-msk.ru/balkony-i-lodzhii/holodnoe-osteklenie | Sliding-aluminium mechanism to cold balcony-glazing specialist remains a useful current handoff. |
| LNK002 | https://okno-msk.ru/alyuminievye-okna/razdvizhnye | https://okno-msk.ru/balkony-i-lodzhii | Sliding-aluminium mechanism to balcony/loggia service hub remains current and relevant. |
| LNK003 | https://okno-msk.ru/okna-rehau | https://okno-msk.ru/stati/kak-vybrat-steklopaket-dlya-plastikovogo-okna | Commercial Rehau/PVC owner to glazing-unit selection guide. |
| LNK004 | https://okno-msk.ru/alyuminievye-okna/razdvizhnye | https://okno-msk.ru/verandy | Sliding-aluminium mechanism to veranda/terrace glazing hub. |
| LNK005 | https://okno-msk.ru/okna-rehau/panoramnoe-osteklenie | https://okno-msk.ru/stati/panoramnoe-osteklenie-eto-dan-mode-ili-praktichnoe-reshenie | Panoramic commercial page to panoramic decision/information guide. |
| LNK006 | https://okno-msk.ru/uslugi/kredit-i-rassrochka | https://okno-msk.ru/okna-rehau | Finance terms to PVC/Rehau product family. |
| LNK007 | https://okno-msk.ru/uslugi/remont-okon | https://okno-msk.ru/stati/okno-otkrylos-v-dvuh-polozheniyah-chto-delat | Repair service to exact two-position troubleshooting context. |
| LNK008 | https://okno-msk.ru/uslugi/remont-okon | https://okno-msk.ru/stati/kak-otregulirovat-plastikovye-okna | Retain only in adjustment/simple-handle contexts; not a blanket broad-repair DIY handoff. |
| LNK009 | https://okno-msk.ru/uslugi/kredit-i-rassrochka | https://okno-msk.ru/okna-rehau | Finance terms to Rehau product family. |
| LNK010 | https://okno-msk.ru/uslugi/kredit-i-rassrochka | https://okno-msk.ru/ | Finance terms back to provider/product hub. |
| LNK011 | https://okno-msk.ru/stati/kak-vybrat-plastikovye-okna | https://okno-msk.ru/okna-rehau/aksessuary-dlya-okon/ruchki-na-okna | General window-selection context to exact handle specialist. |
| LNK012 | https://okno-msk.ru/stati/kak-vybrat-plastikovye-okna | https://okno-msk.ru/okna-rehau/aksessuary-dlya-okon | Hardware-selection content to accessory family hub. |
| LNK013 | https://okno-msk.ru/uslugi/kredit-i-rassrochka | https://okno-msk.ru/uslugi/ustanovka-okon | Finance terms to professional installation service. |
| LNK014 | https://okno-msk.ru/okna-rehau/po-tipu-doma/zamena-okon-v-kvartire | https://okno-msk.ru/uslugi/ustanovka-okon | Replacement workflow to installation service. |
| LNK015 | https://okno-msk.ru/okna-rehau/aksessuary-dlya-okon | https://okno-msk.ru/okna-rehau/aksessuary-dlya-okon/protivovzlomnaya-furnitura | Accessory family hub to exact security-hardware specialist. |

Общие требования:

- ссылка должна быть видимой и контекстной;
- анкор описывает задачу, а не механически повторяет ключ;
- целевая страница открывается и отвечает на задачу;
- ссылка не создаёт противоречие с каноническим владельцем;
- другие 43 исторические строки не внедряются автоматически.

## 5. Маршрутизация 46 подзадач

| Структурная единица | Задача пользователя | Основная страница | Поддерживающие страницы |
|---|---|---|---|
| ALUMINIUM_PROFILE_PRODUCT | choose/buy aluminium window profile/system | https://okno-msk.ru/alyuminievye-okna/ | https://okno-msk.ru/alyuminievye-okna/provedal;https://okno-msk.ru/balkony-i-lodzhii/osteklenie-profilem-provedal |
| ALUMINIUM_WINDOW_COMPONENTS_INFO | understand aluminium-window components/nodes | https://okno-msk.ru/alyuminievye-okna/ | — |
| ALUMINIUM_WINDOW_HANDLE_ACCESSORY | choose/buy aluminium-window handles | https://okno-msk.ru/alyuminievye-okna/ | https://okno-msk.ru/okna-rehau/aksessuary-dlya-okon/ |
| ALUMINIUM_WINDOW_INSTALLATION_REMOVAL_DIY | learn/remove/install aluminium windows yourself | https://okno-msk.ru/alyuminievye-okna/ | — |
| ALUMINIUM_WINDOW_REVIEW_SUPPORT | read experience/review information about aluminium windows | https://okno-msk.ru/alyuminievye-okna/ | — |
| ALUMINIUM_WINDOW_VIDEO_CONTENT | view aluminium-window video information | https://okno-msk.ru/alyuminievye-okna/ | https://okno-msk.ru/nashi-raboty/ |
| BALCONY_ALUMINIUM_SLIDING_COLD | order cold aluminium sliding glazing for balcony/loggia | https://okno-msk.ru/balkony-i-lodzhii/holodnoe-osteklenie/ | https://okno-msk.ru/alyuminievye-okna/razdvizhnye/;https://okno-msk.ru/alyuminievye-okna/provedal;https://okno-msk.ru/balkony-i-lodzhii/holodnoe-panoramnoe-osteklenie-balkona;https://okno-msk.ru/balkony-i-lodzhii/osteklenie-profilem-provedal |
| BALCONY_ALUMINIUM_SLIDING_GENERAL | order aluminium sliding glazing for balcony/loggia | https://okno-msk.ru/balkony-i-lodzhii/razdvizhnye-okna-na-balkon | https://okno-msk.ru/balkony-i-lodzhii/holodnoe-osteklenie;https://okno-msk.ru/alyuminievye-okna/razdvizhnye |
| BALCONY_GLAZING_PERMISSION_INFO | understand whether balcony glazing requires permission | https://okno-msk.ru/balkony-i-lodzhii/ | — |
| BALCONY_GLAZING_WINDOWSILL_OPTION | include/select a windowsill as part of balcony glazing | https://okno-msk.ru/balkony-i-lodzhii/ | https://okno-msk.ru/okna-rehau/aksessuary-dlya-okon/podokonniki/ |
| BOILER_ROOM_WINDOW_REQUIREMENTS_INFO | understand window requirements for a private-house boiler room | https://okno-msk.ru/okna-rehau/po-tipu-doma/okna-v-chastnyj-dom/ | — |
| FRENCH_WINDOW_DIY_GENERAL | understand/do French-window work yourself | https://okno-msk.ru/okna-rehau/francuzskie-okna/ | — |
| FRENCH_WINDOW_INSTALLATION_DIY | learn/alter/install French windows yourself | https://okno-msk.ru/okna-rehau/francuzskie-okna/ | — |
| FRENCH_WINDOW_REDEVELOPMENT_PERMISSION_INFO | understand redevelopment/permission issues for French-window conversion | https://okno-msk.ru/okna-rehau/francuzskie-okna/ | — |
| FRENCH_WINDOW_REVIEW_SUPPORT | read experience/review information about French windows | https://okno-msk.ru/okna-rehau/francuzskie-okna/ | — |
| GLASS_UNIT_PRODUCT_SELECTION | understand/select glazing units | https://okno-msk.ru/okna-rehau/steklopakety-dlya-plastikovykh-okon | https://okno-msk.ru/okna-rehau/izgotovlenie-steklopaketov-na-zakaz;https://okno-msk.ru/stati/steklopakety-osobennosti-i-vidy |
| GLASS_UNIT_REPAIR_DIY | understand whether/how glazing-unit repair can be done yourself | https://okno-msk.ru/stati/kak-vybrat-steklopaket-dlya-plastikovogo-okna/ | https://okno-msk.ru/uslugi/remont-okon/ |
| MOSQUITO_NET_REPLACEMENT_SUPPORT | replace a mosquito-net mesh/net | https://okno-msk.ru/okna-rehau/aksessuary-dlya-okon/moskitnye-setki/ | — |
| OUTDOOR_ALUMINIUM_SLIDING_GLAZING | order aluminium sliding glazing for veranda/terrace/gazebo | https://okno-msk.ru/verandy/razdvizhnye-okna-na-verandu | https://okno-msk.ru/verandy;https://okno-msk.ru/alyuminievye-okna/razdvizhnye |
| OUTDOOR_GLAZING_SPECIAL_TECH_INFO | understand special veranda glazing techniques/material choices | https://okno-msk.ru/verandy/ | https://okno-msk.ru/stati/vidy-i-tipy-ostekleniya-verandy-plyusy-i-minusy;https://okno-msk.ru/verandy/bezramnoe-osteklenie-verandy |
| OUTDOOR_STRUCTURE_GLAZING__INSTALLMENT_CONDITION | order glazing of veranda/terrace/gazebo/porch with instalment/credit condition | https://okno-msk.ru/verandy/ | https://okno-msk.ru/uslugi/kredit-i-rassrochka/ |
| PANORAMIC_WINDOW_TECH_SELECTION_INFO | understand/select panoramic window types, safety, thermal and suitability options | https://okno-msk.ru/stati/panoramnoe-osteklenie-eto-dan-mode-ili-praktichnoe-reshenie/ | https://okno-msk.ru/okna-rehau/panoramnoe-osteklenie/;https://okno-msk.ru/okna-rehau/panoramnye-okna-rehau |
| PRIVATE_HOUSE_SPECIAL_ROOM_WINDOWS | choose/plan windows for special rooms in a private house | https://okno-msk.ru/okna-rehau/po-tipu-doma/okna-v-chastnyj-dom/ | https://okno-msk.ru/okna-rehau/po-tipu-doma/okna-na-kuhnyu |
| PVC_DOOR_HANDLE_ACCESSORY | choose/buy PVC-door handles | https://okno-msk.ru/dveri-rehau/ | https://okno-msk.ru/okna-rehau/aksessuary-dlya-okon/ |
| PVC_DOOR_INSTALLATION_REMOVAL_DIY | learn/remove/install PVC doors yourself | https://okno-msk.ru/dveri-rehau/ | — |
| PVC_DOOR_REVIEW_SUPPORT | read experience/review information about PVC doors | https://okno-msk.ru/dveri-rehau/ | — |
| PVC_PROFILE_PRODUCT_SELECTION | choose/buy PVC/Rehau profile/system | https://okno-msk.ru/okna-rehau/ | — |
| PVC_WINDOWS_COMMERCIAL__INSTALLMENT_CONDITION | buy/order PVC windows with instalment/credit condition | https://okno-msk.ru/okna-rehau/ | https://okno-msk.ru/uslugi/kredit-i-rassrochka/ |
| PVC_WINDOW_OPERATION_DIY | understand how to open/operate a PVC window | https://okno-msk.ru/stati/okno-otkrylos-v-dvuh-polozheniyah-chto-delat/ | https://okno-msk.ru/uslugi/remont-okon/ |
| PVC_WINDOW_REVIEW_SUPPORT | read experience/review information about PVC windows | https://okno-msk.ru/okna-rehau/ | — |
| PVC_WINDOW_VIDEO_CONTENT | view PVC-window video information | https://okno-msk.ru/okna-rehau/ | https://okno-msk.ru/nashi-raboty/ |
| REHAU_DELIGHT_REVIEW_SUPPORT | read experience/review information about Rehau Delight | https://okno-msk.ru/okna-rehau/ | — |
| REHAU_GRAZIO_REVIEW_SUPPORT | read experience/review information about Rehau Grazio | https://okno-msk.ru/okna-rehau/rehau-grazio/ | — |
| REHAU_WINDOWS_COMMERCIAL__INSTALLMENT_CONDITION | buy/order Rehau window products with instalment/credit condition | https://okno-msk.ru/okna-rehau/ | https://okno-msk.ru/uslugi/kredit-i-rassrochka/ |
| REHAU_WINDOW_REVIEW_SUPPORT | read experience/review information about Rehau windows | https://okno-msk.ru/okna-rehau/ | — |
| WINDOWS_COMMERCIAL_GENERAL__INSTALLMENT_CONDITION | buy/order generic windows with instalment/credit condition | https://okno-msk.ru/ | https://okno-msk.ru/uslugi/kredit-i-rassrochka/ |
| WINDOWS_DOORS_COMBINED_COMMERCIAL__INSTALLMENT_CONDITION | buy/order combined window-and-door products with instalment/credit condition | https://okno-msk.ru/ | https://okno-msk.ru/uslugi/kredit-i-rassrochka/ |
| WINDOW_BLINDS_INSTALLATION | install window blinds | https://okno-msk.ru/okna-rehau/aksessuary-dlya-okon/zhalyuzi/ | — |
| WINDOW_FINISHING_ACCESSORY_COMPONENTS | choose finishing/installation accessory components | https://okno-msk.ru/okna-rehau/aksessuary-dlya-okon/ | https://okno-msk.ru/uslugi/otdelka-otkosov/ |
| WINDOW_FRAME_SASH_COMPONENT | understand/replace frame or sash components | https://okno-msk.ru/uslugi/remont-okon/ | https://okno-msk.ru/okna-rehau/aksessuary-dlya-okon/ |
| WINDOW_HARDWARE_MAINTENANCE_INFO | learn/select maintenance and lubrication for window hardware | https://okno-msk.ru/stati/kak-perevesti-plastikovoe-okno-v-zimnij-rezhim/ | https://okno-msk.ru/uslugi/remont-okon/ |
| WINDOW_INSTALLATION_MATERIALS_INFO | understand/buy installation materials for windows | https://okno-msk.ru/uslugi/ustanovka-okon/ | — |
| WINDOW_INSTALLATION_SERVICE__INSTALLMENT_CONDITION | professional window installation with instalment/credit condition | https://okno-msk.ru/uslugi/ustanovka-okon/ | https://okno-msk.ru/uslugi/kredit-i-rassrochka/ |
| WINDOW_OR_DOOR_GLASS_COMPONENT | replace/buy window or door glass component | https://okno-msk.ru/uslugi/remont-okon/ | https://okno-msk.ru/dveri-rehau/ |
| WINDOW_PRODUCT_RATING_COMPARISON_INFO | compare/rank window products | https://okno-msk.ru/stati/kakie-okna-samye-luchshie/ | — |
| WINDOW_SAFETY_HARDWARE_ACCESSORY | choose/buy window safety/security hardware | https://okno-msk.ru/okna-rehau/aksessuary-dlya-okon/protivovzlomnaya-furnitura/ | https://okno-msk.ru/okna-rehau/aksessuary-dlya-okon/ |

Для каждой строки:

- не создавать самостоятельную страницу только из-за наличия подзадачи;
- отразить задачу на основной странице либо дать контекстный переход;
- использовать более поздний Step14A overlay при конфликте со старой таблицей;
- во всех клиентских и рабочих представлениях показывать одного владельца.

## 6. Шаблон приёмки контентной работы

Для каждой готовой контентной задачи проверить:

- AS-IS подтверждён на текущей странице;
- блок размещён в указанной логической позиции;
- раскрыты обязательные темы и вопросы;
- пример не содержит неподтверждённых характеристик;
- сохранены существующие цена/CTA/полезные блоки;
- нет дублирования соседней страницы;
- внутренние ссылки соответствуют роли;
- ограничения и необходимость замера/проекта видимы;
- дата и метод указаны для временно чувствительных сравнений;
- опубликованный результат не шире доказательства.

## 7. Шаблон приёмки владения и маршрута

- каноническая единица совпадает с Stage 05;
- task/intent/business scope/page role/owner взяты из той же целевой единицы;
- старый ID и старые производные поля отсутствуют во всех текущих клиентах;
- широкая и узкая страницы не перепутаны;
- supporting page не объявлена primary без отдельного решения;
- нет новой страницы и разрушительного действия, если их нет в власти.

## 8. Что не заполнять догадками

В этом исследовании не назначены:

- исполнитель;
- часы;
- календарный срок;
- внутренняя бизнес-ценность;
- фактическая доступность неподтверждённого бренда;
- ожидаемый трафик или конверсия.

Эти поля должен добавить владелец проекта после подтверждения ресурсов и бизнеса. Их отсутствие не отменяет аналитическую рекомендацию, но не позволяет считать частную задачу полностью спланированной.

## 9. Итоговая проверка после внедрения

1. Сверить все изменённые строки с Stage 05 semantic master.
2. Пройти 15 ссылок источник → цель.
3. Проверить 46 маршрутов подзадач.
4. Проверить готовые контентные блоки по индивидуальным критериям.
5. Убедиться, что три overlap-кейса и брендовая проверка не закрыты без доказательства.
6. Убедиться, что HOLD/SEARCH_REQUIRED/DEFERRED не исчезли.
7. Проверить согласованность клиентского отчёта, этого руководства, AI-документа и workbook.
