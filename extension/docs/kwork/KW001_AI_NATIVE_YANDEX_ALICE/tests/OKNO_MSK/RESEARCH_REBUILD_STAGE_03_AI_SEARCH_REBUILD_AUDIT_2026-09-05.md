# Stage 3. Отдельный аудит AI-search пересборки OKNO_MSK

Дата: 2026-09-05  
Статус: COMPLETE / GITHUB READBACK REQUIRED  
Единица исполнения: STAGE_3_AI_SEARCH_REBUILD_AUDIT  
Новые provider-вызовы: 0  
Новая стоимость: 0 ₽

## 1. Итог

AI-слой прежнего исследования был реальным, но узким и не менял архитектуру сайта. Из 25 предварительных кандидатов до AI были отобраны восемь кейсов; по ним сохранены девять verbatim GenSearch-ответов. Итоговый доказанный delta:

| Вердикт | Кейсов | Значение |
|---|---:|---|
| CHANGE | 0 | Ни одна page/architecture responsibility не была изменена AI. |
| DE_RISK | 4 | AI независимо поддержал Search-only boundary или снизил риск ошибочной смены владельца. |
| NO_CHANGE | 3 | AI не дал основания менять решение; это положительный аналитический результат. |
| INSUFFICIENT | 1 | Архитектурный вывод честно оставлен нерешённым. |

Практический AI-вклад: три ограниченных content-кандидата — `S18-A009`, `S18-A030`, `S18-A031`. Остальные кейсы дают explicit retain/no-action/insufficient. Канонический вывод: `AI_NATIVE_VALUE != FACT_OF_AI_REQUESTS`.

## 2. Метод и границы

Аудит восстановлен только из сохранённого корпуса: Search-only freeze, preregistered selection, raw GenSearch, direct Search, source/page validation, Step-17 comparison и Step-18 actions. Новых запросов не выполнялось.

Каждый кейс проверен по цепочке: почему выбран → решение до AI → Search evidence → сохранённый AI response/source set → comparison → verdict → architecture/content/priority effect → action/no-action → client meaning → limitation.

Ограничения общие для всех кейсов:

- GenSearch API proxy не называется потребительской Алисой;
- exact-query snapshot не переносится автоматически на семейство;
- одиночный снимок не доказывает долгосрочную стабильность;
- порядок/число source entries не считается ranking;
- AI не гарантирует цитирование, рост трафика или конверсию;
- отсутствие target domain в GenSearch не доказывает отсутствие/непригодность страницы.

## 3. Полный causal audit по кейсам

### C15-004 — панорамные алюминиевые окна

- **Почему выбран:** Test whether generative synthesis materially shifts responsibility from aluminium commercial/product ownership toward explanatory panoramic-selection content.
- **Search-only решение до AI:** Ordinary Search is strongly commercial/product-led; aluminium commercial owner is primary, panoramic information supports. Step14A also surfaced /okna-rehau/panoramnye-okna-rehau as a broad panoramic same-task commercial competitor.
- **Обычный Search:** STEP_13_SEARCH_RESULT_03_PANORAMIC_ALUMINIUM_WINDOWS_2026-08-31.json. Наблюдённая задача: Evaluate/select and buy panoramic aluminium windows in Moscow.
- **Сохранённый AI response:** Explanatory/specification synthesis; four used sources have commercial panoramic/aluminium product/manufacturer context by URL/title; refined query exact.
- **Raw authority:** `STEP_16_C15-004_INITIAL_GENSEARCH_RAW_VERBATIM.txt`
- **Использованные/наблюдавшиеся источники:** l-okna.ru/panoramnyie-alyuminievyie-okna; al-solution.ru/production/panoramnye-okna; oknarosta.ru/aluminievye-okna/panoramnye; alutech.ru/.../panoramnye-okna
- **Search ↔ AI comparison:** task=SAME_CORE_TASK__AI_MORE_EXPLANATORY; commerciality=SEARCH_MORE_TRANSACTIONAL__AI_EXPLANATORY_WITH_COMMERCIAL_SOURCE_BASE; specificity=SAME_EXACT_QUERY; source_role=SPECIALIST_COMMERCIAL_SOURCES_COMPLEMENT_EXISTING_BROADER_OWNER
- **Поддержанный вывод:** AI does not challenge ownership, but the V2 content layer reveals a within-page expansion candidate that the first pass incorrectly omitted. Current owner is commercially source-worthy for the core job, but specialist external sources expose a plausible opportunity to strengthen panoramic-specific explanatory/specification depth inside the existing owner.
- **Что не доказано:** Exact-query GenSearch proxy only; no consumer-Alice, family-wide or long-term-stability claim; source order/count not used as rank.
- **Вердикт:** `DE_RISK`
- **Архитектурный эффект:** `NO_ARCHITECTURE_CHANGE`
- **Контентный эффект:** `CONTENT_EXPANSION_CANDIDATE`
- **Downstream action/no-action:** S18-A030 — проверить и при необходимости усилить panoramic-aluminium subsection; новая страница не нужна.
- **Клиентский смысл:** AI подтвердил правильного владельца и дал ограниченный кандидат глубины контента.
- **Evidence trace:** STEP_13_SEARCH_RESULT_03_PANORAMIC_ALUMINIUM_WINDOWS_2026-08-31.json | STEP_16_C15-004_INITIAL_GENSEARCH_RAW_VERBATIM.txt | STEP_16_OBSERVATIONS_CORRECTED_V2_2026-09-02.json#C15-004 | STEP_17_DIRECT_PAGE_VALIDATION_LEDGER.tsv#V17-001..V17-005

### C15-006 — алюминиевые окна для веранды

- **Почему выбран:** Test whether AI keeps use-case-first responsibility or systematically narrows the query to material/mechanism specialists.
- **Search-only решение до AI:** Ordinary Search favors the veranda/terrace use-case hub. Step14A adds informational veranda-choice support, an exact sliding-veranda specialist and a frameless-veranda specialist.
- **Обычный Search:** STEP_13_SEARCH_RESULT_05_ALUMINIUM_WINDOWS_VERANDA_2026-08-31.json. Наблюдённая задача: Choose/order aluminium glazing for a veranda or terrace.
- **Сохранённый AI response:** Veranda use case plus aluminium properties and warm/cold systems; used-source set mixes aluminium-for-veranda and broader veranda/terrace glazing by URL/title.
- **Raw authority:** `STEP_16_C15-006_INITIAL_GENSEARCH_RAW_VERBATIM.txt`
- **Использованные/наблюдавшиеся источники:** l-okna.ru/alyuminievyie-okna-dlya-verand; vipfabrikaokon.ru/osteklenie-verandy-i-terrasy
- **Search ↔ AI comparison:** task=SAME_USECASE_TASK; commerciality=AI_MORE_EXPLANATORY__NO_OWNERSHIP_SHIFT; specificity=SAME_EXACT_QUERY__NO_MECHANISM_NARROWING; source_role=UNRESOLVED_FOR_CONTENT_LAYER__NOT_NEEDED_FOR_ARCH_VERDICT
- **Поддержанный вывод:** Direct Search and GenSearch preserve veranda-first responsibility; content-source-worthiness remains conservatively insufficient because material used-source content was not directly validated. INSUFFICIENT_FOR_MATERIAL_CONTENT_GAP_DECISION; current target alignment is proven, but no direct used-source content pair supports a safe no-gap or expansion claim.
- **Что не доказано:** Exact-query GenSearch proxy only; no source hierarchy from order/count; content layer intentionally insufficient rather than inferred.
- **Вердикт:** `DE_RISK`
- **Архитектурный эффект:** `NO_ARCHITECTURE_CHANGE`
- **Контентный эффект:** `INSUFFICIENT`
- **Downstream action/no-action:** Явного действия не создавать; сохранить /verandy как общий владелец.
- **Клиентский смысл:** AI снизил риск ошибочной смены владельца; новое действие не оправдано.
- **Evidence trace:** STEP_13_SEARCH_RESULT_05_ALUMINIUM_WINDOWS_VERANDA_2026-08-31.json | STEP_16_C15-006_INITIAL_GENSEARCH_RAW_VERBATIM.txt | STEP_16_OBSERVATIONS_CORRECTED_V2_2026-09-02.json#C15-006 | STEP_17_DIRECT_PAGE_VALIDATION_LEDGER.tsv#V17-006

### C15-007 — панорамное остекление балкона

- **Почему выбран:** Stable specialist-owner control. Detect whether the AI surface spuriously collapses a strongly specific balcony task into broad panoramic responsibility.
- **Search-only решение до AI:** Retry succeeded; 9/10 saved Search results were balcony/loggia-specific and the broad panoramic result was rank 10. Dedicated panoramic-balcony specialist is frozen primary.
- **Обычный Search:** STEP_13_SEARCH_RESULT_QF007_RETRY_1_PANORAMIC_BALCONY_2026-09-01.json. Наблюдённая задача: Evaluate/order panoramic glazing specifically for a balcony or loggia.
- **Сохранённый AI response:** Answer remains balcony panoramic/French glazing; all five used sources are balcony/loggia-specific by URL/title; refined query exact.
- **Raw authority:** `STEP_16_C15-007_INITIAL_GENSEARCH_RAW_VERBATIM.txt`
- **Использованные/наблюдавшиеся источники:** svetokna.ru/.../panoramnoe; sbalkonom.ru/.../panoramnoe-osteklenie; melke.ru/balkony/frantsuzkoe-osteklenie; okna-vinchelli.ru/.../panoramnoe-osteklenie-balkonov-i-lodzhiy; mosokna.ru/balkony-lodzhii/francuzskoe-osteklenie
- **Search ↔ AI comparison:** task=SAME_BALCONY_SPECIFIC_TASK; commerciality=SAME_COMMERCIAL_INFORMATIONAL_BLEND; specificity=SAME_BALCONY_SPECIFICITY; source_role=SUPPORTIVE_BALCONY_SPECIFIC_SOURCES__NO_BROAD_COLLAPSE
- **Поддержанный вывод:** No control break is observed and the current specialist also covers the directly compared source-worthiness dimensions. Current target already covers the decision-relevant dimensions that made the directly read external source useful for this exact task.
- **Что не доказано:** Single exact-query run; not temporal stability; GenSearch != consumer Alice; no rank inference from source order.
- **Вердикт:** `DE_RISK`
- **Архитектурный эффект:** `NO_ARCHITECTURE_CHANGE`
- **Контентный эффект:** `NO_MATERIAL_CONTENT_GAP_OBSERVED`
- **Downstream action/no-action:** Положительный RETAIN: сохранить specialist balcony page; материальный content gap не доказан.
- **Клиентский смысл:** AI подтвердил specialist-owner и отсутствие материального core-task gap.
- **Evidence trace:** STEP_13_SEARCH_RESULT_QF007_RETRY_1_PANORAMIC_BALCONY_2026-09-01.json | STEP_16_C15-007_INITIAL_GENSEARCH_RAW_VERBATIM.txt | STEP_16_OBSERVATIONS_CORRECTED_V2_2026-09-02.json#C15-007 | PUBLIC_DIRECT_READ_2026-09-03:svetokna panoramic balcony + okno-msk panoramic balcony

### C15-010 — установка подоконника на пластиковые окна

- **Почему выбран:** Test whether AI resolves the mixed SERP primarily as object/product selection, professional service, or DIY/how-to responsibility.
- **Search-only решение до AI:** Saved SERP mixes professional installation and DIY guidance; the windowsill object page is the frozen owner and finishing service is supporting context.
- **Обычный Search:** STEP_13_SEARCH_RESULT_07_WINDOWSILL_INSTALLATION_2026-08-31.json. Наблюдённая задача: Install a PVC windowsill, spanning professional installation and DIY/how-to execution.
- **Сохранённый AI response:** Both same-query observations are procedural installation/how-to oriented; second run broadens used-source mix to include one professional installation-service page.
- **Raw authority:** `STEP_16_C15-010_INITIAL_GENSEARCH_RAW_VERBATIM.txt + STEP_16_C15-010_CONFIRMATION_GENSEARCH_RAW_VERBATIM.txt`
- **Использованные/наблюдавшиеся источники:** oknastar.ru/stati/ustanovka-podokonnika-na-pvh-okna; lemanapro.ru/.../kak-ustanovit-plastikovyy-podokonnik; okna-building.ru/uslugi/ustanovka-podokonnika
- **Search ↔ AI comparison:** task=AI_MORE_PROCEDURAL_PRESENTATION__SAME_INSTALLATION_TASK; commerciality=AI_MORE_HOW_TO__CURRENT_SITE_RETAINS_PRODUCT_AND_SERVICE_LAYER; specificity=SAME_OBJECT_AND_EXACT_ACTION; source_role=HOW_TO_AND_SERVICE_ROLES_BOTH_DIRECTLY_VALIDATED
- **Поддержанный вывод:** The reproduced AI procedural direction is real but does not require different ownership because the frozen owner already represents the installation task and service bridge. The current owner already contains the same procedural-plus-service dimensions that make the observed GenSearch sources useful; the V2 evidence does not prove a material within-page gap.
- **Что не доказано:** Short-window reproduction only; not long-term stability or consumer Alice; no ranking claim.
- **Вердикт:** `NO_CHANGE`
- **Архитектурный эффект:** `NO_ARCHITECTURE_CHANGE`
- **Контентный эффект:** `NO_MATERIAL_CONTENT_GAP_OBSERVED`
- **Downstream action/no-action:** NO_ACTION: сохранить hybrid product/service/how-to owner и professional fallback.
- **Клиентский смысл:** AI показал процедурную форму ответа, но текущая hybrid page уже покрывает задачу.
- **Evidence trace:** STEP_13_SEARCH_RESULT_07_WINDOWSILL_INSTALLATION_2026-08-31.json | STEP_16_C15-010_INITIAL_GENSEARCH_RAW_VERBATIM.txt | STEP_16_C15-010_CONFIRMATION_GENSEARCH_RAW_VERBATIM.txt | STEP_16_OBSERVATIONS_CORRECTED_V2_2026-09-02.json#C15-010 | STEP_17_DIRECT_PAGE_VALIDATION_LEDGER.tsv#V17-007..V17-011

### C15-013 — французские панорамные окна

- **Почему выбран:** Test whether generative interpretation preserves a distinct French-window taxonomy or collapses it into generic panoramic/floor-to-ceiling glazing.
- **Search-only решение до AI:** French-specific pages dominate the saved SERP for the exact cross-labelled French/panoramic formulation; general panoramic remains broader support. Step14A adds a French-balcony intersection page and a same-task broad panoramic competitor.
- **Обычный Search:** STEP_13_SEARCH_RESULT_09_FRENCH_PANORAMIC_WINDOWS_2026-09-01.json. Наблюдённая задача: Understand/evaluate French windows as a distinct floor-to-ceiling/window-door concept with panoramic overlap.
- **Сохранённый AI response:** Answer explicitly preserves French-window concept; three used sources are French-window-specific by URL/title; generic panoramic source returned but used=false.
- **Raw authority:** `STEP_16_C15-013_INITIAL_GENSEARCH_RAW_VERBATIM.txt`
- **Использованные/наблюдавшиеся источники:** holzen.ru/.../french-wooden-windows; oknarosta.ru/blog/okna/frantsuzskie-okna-sozdaem-effektnoe-panoramnoe-osteklenie; okna-vinchelli.ru/katalog/bolshie-frantsuzskie-okna
- **Search ↔ AI comparison:** task=SAME_FRENCH_SPECIFIC_TASK; commerciality=AI_MORE_EXPLANATORY__SEARCH_MIXED_COMMERCIAL_INFORMATIONAL; specificity=SAME_FRENCH_SPECIFICITY; source_role=EXPLANATORY_FRENCH_SOURCE_DEPTH_COMPLEMENTS_COMMERCIAL_OWNER
- **Поддержанный вывод:** AI independently preserves French taxonomy; V2 additionally identifies a bounded content-depth opportunity without changing page responsibility. Architecture is correctly French-specific, but explanatory selection depth is a plausible within-page source-worthiness opportunity on the existing owner.
- **Что не доказано:** Exact-query GenSearch proxy only; no consumer-Alice or rank inference; used=false generic panoramic source is not treated as lower ranked.
- **Вердикт:** `DE_RISK`
- **Архитектурный эффект:** `NO_ARCHITECTURE_CHANGE`
- **Контентный эффект:** `CONTENT_EXPANSION_CANDIDATE`
- **Downstream action/no-action:** S18-A009 — после свежей проверки усилить French-vs-panoramic distinction и selection depth на существующей странице.
- **Клиентский смысл:** AI подтвердил отдельную French taxonomy и подсветил возможную глубину объяснения.
- **Evidence trace:** STEP_13_SEARCH_RESULT_09_FRENCH_PANORAMIC_WINDOWS_2026-09-01.json | STEP_16_C15-013_INITIAL_GENSEARCH_RAW_VERBATIM.txt | STEP_16_OBSERVATIONS_CORRECTED_V2_2026-09-02.json#C15-013 | STEP_17_DIRECT_PAGE_VALIDATION_LEDGER.tsv#V17-012 | PUBLIC_DIRECT_READ_2026-09-03:oknarosta French-window guide

### C15-018 — замена окна на пластиковое цена москва

- **Почему выбран:** Stable transactional control. Detect whether AI over-generalizes a clear replacement transaction into generic installation, broad product selection or informational guidance.
- **Search-only решение до AI:** Saved Search contains multiple replacement-specific commercial pages plus generic installation pages; replacement intent remains the specific ownership boundary.
- **Обычный Search:** STEP_13_SEARCH_RESULT_14_WINDOW_REPLACEMENT_PRICE_MOSCOW_2026-09-01.json. Наблюдённая задача: Price and order replacement of an existing window with a PVC window in Moscow.
- **Сохранённый AI response:** Answer remains replacement-price framed but used evidence mixes replacement-specific and broad turnkey/window-price pages; refined queries include both generic turnkey and exact replacement wording.
- **Raw authority:** `STEP_16_C15-018_INITIAL_GENSEARCH_RAW_VERBATIM.txt`
- **Использованные/наблюдавшиеся источники:** mosokna.ru; n-okna.ru/services/zamena-okon; i-okna.ru; msk.okna-servise.com/pod-klyuch; plastika-okon.ru/okna/prices; fabrikaokon.ru/okna.html
- **Search ↔ AI comparison:** task=SAME_REPLACEMENT_PRICE_TASK__AI_SUPPORTING_QUERY_BROADENS; commerciality=SAME_COMMERCIAL_PRICE_ORIENTATION; specificity=ANSWER_REPLACEMENT_SPECIFIC__SOURCE_ACQUISITION_SOMEWHAT_BROADER; source_role=MIXED_COMMERCIAL_SUPPORT__NO_HIERARCHY_INFERRED
- **Поддержанный вывод:** The architecture boundary remains replacement-specific, but V2 refuses to overstate content source-worthiness from unvalidated used-source content. INSUFFICIENT_FOR_MATERIAL_CONTENT_GAP_DECISION; target role is sound, but content parity/gap must not be inferred.
- **Что не доказано:** Single exact-query run; broad sources do not prove generic ownership; no source order/count rank inference.
- **Вердикт:** `NO_CHANGE`
- **Архитектурный эффект:** `NO_ARCHITECTURE_CHANGE`
- **Контентный эффект:** `INSUFFICIENT`
- **Downstream action/no-action:** NO_ACTION: сохранить replacement specialist; content gap по использованным источникам не доказан.
- **Клиентский смысл:** AI не изменил replacement boundary; недостаточно данных для content-gap claim.
- **Evidence trace:** STEP_13_SEARCH_RESULT_14_WINDOW_REPLACEMENT_PRICE_MOSCOW_2026-09-01.json | STEP_16_C15-018_INITIAL_GENSEARCH_RAW_VERBATIM.txt | STEP_16_OBSERVATIONS_CORRECTED_V2_2026-09-02.json#C15-018 | STEP_17_DIRECT_PAGE_VALIDATION_LEDGER.tsv#V17-013

### C15-019 — как открыть пластиковое окно

- **Почему выбран:** Use AI refined queries and answer orientation to discriminate whether the query belongs to emergency opening, two-position troubleshooting, or general adjustment.
- **Search-only решение до AI:** Saved SERP for the probe is dominated by opening a PVC window from outside/emergency access, so it does not strongly adjudicate the frozen two-position-vs-adjustment pair.
- **Обычный Search:** STEP_13_SEARCH_RESULT_15_HOW_TO_OPEN_PLASTIC_WINDOW_2026-09-01.json. Наблюдённая задача: Ambiguous how-to query dominated by outside/emergency opening, with a minority troubleshooting/operation interpretation.
- **Сохранённый AI response:** Answer mixes jammed/two-position troubleshooting with outside/emergency opening; used sources also mix both directions.
- **Raw authority:** `STEP_16_C15-019_INITIAL_GENSEARCH_RAW_VERBATIM.txt`
- **Использованные/наблюдавшиеся источники:** okna-magnit.ru/blog/ne-otkryvaetsya-plastikovoe-okno-chto-delat; galwin.ru/.../kak-otkryt-plastikovoe-okno-snaruzhi; plastika-okon.ru/about/articles/kak-otkryt-okno-pvh-snaruzhi
- **Search ↔ AI comparison:** task=MIXED_ON_BOTH_SURFACES; commerciality=NO_MATERIAL_CHANGE; specificity=AMBIGUOUS_ON_BOTH_SURFACES; source_role=MIXED_EMERGENCY_AND_TROUBLESHOOTING__NO_SINGLE_OWNER_SIGNAL
- **Поддержанный вывод:** Both surfaces reproduce ambiguity; under the preregistered condition the correct decision is to preserve the cautious boundary and avoid forcing content expansion from an unstable intent. NOT_APPLICABLE_FOR_TARGET_CONTENT_EXPANSION_FROM_THIS_PROBE; the exact query is not a safe single-page content brief for the two-position article.
- **Что не доказано:** Exact-query ambiguity preserved; no user-job-family generalization; no consumer-Alice claim.
- **Вердикт:** `NO_CHANGE`
- **Архитектурный эффект:** `NO_ARCHITECTURE_CHANGE`
- **Контентный эффект:** `NOT_APPLICABLE`
- **Downstream action/no-action:** NO_ACTION: не расширять узкую troubleshooting-статью под двусмысленный запрос.
- **Клиентский смысл:** AI сохранил неоднозначность, поэтому правильный результат — не расширять страницу догадкой.
- **Evidence trace:** STEP_13_SEARCH_RESULT_15_HOW_TO_OPEN_PLASTIC_WINDOW_2026-09-01.json | STEP_16_C15-019_INITIAL_GENSEARCH_RAW_VERBATIM.txt | STEP_16_OBSERVATIONS_CORRECTED_V2_2026-09-02.json#C15-019 | STEP_17_DIRECT_PAGE_VALIDATION_LEDGER.tsv#V17-014

### C15-020 — лучшие пластиковые окна

- **Почему выбран:** Test whether AI source use/refined queries preserve distinct best-windows, broad selection and profile-comparison responsibilities or expose unresolved same-task competition.
- **Search-only решение до AI:** Saved SERP is informational/ranking/comparison-led; best-windows article is the specific primary and how-to-choose is broad support. Step14A adds apartment-selection, profile/manufacturer-comparison and a same-task Rehau comparison competitor.
- **Обычный Search:** STEP_13_SEARCH_RESULT_16_BEST_PLASTIC_WINDOWS_2026-09-01.json. Наблюдённая задача: Compare/rank the best plastic windows, profile systems and manufacturers.
- **Сохранённый AI response:** Answer is ranking/profile/brand comparison; used sources span those topics; no OKNO_MSK page is used.
- **Raw authority:** `STEP_16_C15-020_INITIAL_GENSEARCH_RAW_VERBATIM.txt`
- **Использованные/наблюдавшиеся источники:** dzen.ru/...; okna2-0.ru/blog/reyting-okonnyh-brendov-2025; mosokna.ru/stati/kakoy-profil-dlya-okon-luchshe-top-proizvoditeley-025-2026
- **Search ↔ AI comparison:** task=SAME_RANKING_COMPARISON_JOB; commerciality=SAME_INFORMATIONAL_COMPARISON_ORIENTATION; specificity=AI_NARROWS_PARTLY_TO_CURRENT_YEAR_PROFILE_MODEL_RANKING; source_role=EXTERNAL_RANKING_AND_PROFILE_SOURCES_USED__TARGET_DOMAIN_ROLE_UNOBSERVED
- **Поддержанный вывод:** The first-pass INSUFFICIENT architecture verdict remains correct, while V2 can still surface a non-architectural content improvement candidate from directly read ranking sources. A bounded content candidate exists around freshness, explicit comparison criteria and transparent ranking methodology, but the target-site hierarchy among best/selection/profile pages remains unvalidated.
- **Что не доказано:** One external-source GenSearch snapshot cannot establish competition/hierarchy among OKNO_MSK pages; no source-order rank inference.
- **Вердикт:** `INSUFFICIENT`
- **Архитектурный эффект:** `NO_ARCHITECTURE_CHANGE`
- **Контентный эффект:** `CONTENT_EXPANSION_CANDIDATE`
- **Downstream action/no-action:** S18-A031 — проверить свежесть рейтинга и методику сравнения; архитектурную иерархию не менять.
- **Клиентский смысл:** AI не доказал архитектуру, но поддержал bounded freshness/methodology content check.
- **Evidence trace:** STEP_13_SEARCH_RESULT_16_BEST_PLASTIC_WINDOWS_2026-09-01.json | STEP_16_C15-020_INITIAL_GENSEARCH_RAW_VERBATIM.txt | STEP_16_OBSERVATIONS_CORRECTED_V2_2026-09-02.json#C15-020 | STEP_17_DIRECT_PAGE_VALIDATION_LEDGER.tsv#V17-015 | PUBLIC_DIRECT_READ_2026-09-03:okna2-0 ranking + mosokna profile comparison

## 4. Search ↔ AI decision delta

| Кейс | Search-only baseline | AI verdict | Architecture | Content/action |
|---|---|---|---|---|
| C15-004 | Ordinary Search is strongly commercial/product-led; aluminium commercial owner is primary, panoramic information supports. Step14A also surfaced /okna-rehau/panoramnye-okna-rehau a | DE_RISK | NO_ARCHITECTURE_CHANGE | S18-A030 — проверить и при необходимости усилить panoramic-aluminium subsection; новая страница не нужна. |
| C15-006 | Ordinary Search favors the veranda/terrace use-case hub. Step14A adds informational veranda-choice support, an exact sliding-veranda specialist and a frameless-veranda specialist. | DE_RISK | NO_ARCHITECTURE_CHANGE | Явного действия не создавать; сохранить /verandy как общий владелец. |
| C15-007 | Retry succeeded; 9/10 saved Search results were balcony/loggia-specific and the broad panoramic result was rank 10. Dedicated panoramic-balcony specialist is frozen primary. | DE_RISK | NO_ARCHITECTURE_CHANGE | Положительный RETAIN: сохранить specialist balcony page; материальный content gap не доказан. |
| C15-010 | Saved SERP mixes professional installation and DIY guidance; the windowsill object page is the frozen owner and finishing service is supporting context. | NO_CHANGE | NO_ARCHITECTURE_CHANGE | NO_ACTION: сохранить hybrid product/service/how-to owner и professional fallback. |
| C15-013 | French-specific pages dominate the saved SERP for the exact cross-labelled French/panoramic formulation; general panoramic remains broader support. Step14A adds a French-balcony in | DE_RISK | NO_ARCHITECTURE_CHANGE | S18-A009 — после свежей проверки усилить French-vs-panoramic distinction и selection depth на существующей странице. |
| C15-018 | Saved Search contains multiple replacement-specific commercial pages plus generic installation pages; replacement intent remains the specific ownership boundary. | NO_CHANGE | NO_ARCHITECTURE_CHANGE | NO_ACTION: сохранить replacement specialist; content gap по использованным источникам не доказан. |
| C15-019 | Saved SERP for the probe is dominated by opening a PVC window from outside/emergency access, so it does not strongly adjudicate the frozen two-position-vs-adjustment pair. | NO_CHANGE | NO_ARCHITECTURE_CHANGE | NO_ACTION: не расширять узкую troubleshooting-статью под двусмысленный запрос. |
| C15-020 | Saved SERP is informational/ranking/comparison-led; best-windows article is the specific primary and how-to-choose is broad support. Step14A adds apartment-selection, profile/manuf | INSUFFICIENT | NO_ARCHITECTURE_CHANGE | S18-A031 — проверить свежесть рейтинга и методику сравнения; архитектурную иерархию не менять. |

AI не создал новые страницы, не санкционировал merge/delete/redirect и не изменил frozen owners. Его ценность — независимое снижение риска в четырёх кейсах, три обоснованных no-change, сохранение неопределённости в одном кейсе и три bounded content candidates.

## 5. Что передаётся дальше

Stage 4 должен получить все восемь causal records как отдельные dispositions, не сводя AI к числу запросов. Stage 7 должен показать Search evidence и AI delta раздельно. Stage 6 обязан превратить только три поддержанных content candidates в implementation specs после current-page verification; остальные кейсы должны остаться explicit no-action/retain/insufficient.

## 6. QA и приемка

- выбранные кейсы: 8/8;
- raw AI observations: 9/9;
- preregistered baseline/selection recovered: 8/8;
- Search evidence trace: 8/8;
- terminal verdict: 8/8;
- architecture effect: 8/8;
- content/action or explicit no-action: 8/8;
- client-visible implication: 8/8;
- claim boundary: 8/8;
- invented architecture changes: 0;
- new provider calls: 0;
- paid cost in Stage 3: 0 ₽.

Итог: `STAGE_3_COMPLETE__AI_CAUSAL_CHAIN_REBUILT__NO_NEW_PROVIDER_CALLS__READY_FOR_STAGE_4`.
