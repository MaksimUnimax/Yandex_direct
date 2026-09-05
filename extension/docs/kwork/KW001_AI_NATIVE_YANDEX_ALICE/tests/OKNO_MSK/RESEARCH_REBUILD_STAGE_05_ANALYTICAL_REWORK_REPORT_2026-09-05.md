# Stage 5. Реальная аналитическая пересборка OKNO_MSK

Дата: 2026-09-05  
Статус: COMPLETE / GITHUB READBACK REQUIRED  
Новые provider-вызовы: 0  
Новая стоимость: 0 ₽

## 1. Результат

Создана одна текущая аналитическая truth layer для всего demand universe: 2 840 уникальных фраз. Старый V7 не скопирован. Для каждой из 2 313 назначенных фраз финальная structural unit присоединена к полному canonical target contract, после чего применён higher-precedence Step14A current-site overlay.

Главный дефект Stage 2 устранён:

```text
CORRECTED ID
+ CANONICAL TASK
+ CANONICAL INTENT
+ CANONICAL BUSINESS SCOPE
+ CANONICAL PAGE ROLE
+ CURRENT PRIMARY/SUPPORTING PAGES
+ STRUCTURAL ACTION
= ONE ATOMIC SEMANTIC STATE
```

69 explicit correction rows применены: D12-27 — 20, D12-30 — 49. Неприменённых correction rows: 0. Assigned rows с несоответствием target-unit contract: 0.

## 2. Accounting единого semantic master

| Состояние | Строк |
|---|---:|
| ASSIGNED | 2 271 |
| ASSIGNED_HOLD | 42 |
| SEARCH_REQUIRED | 19 |
| REVIEW_DEFERRED | 174 |
| EXCLUDED_PRESERVED | 334 |
| **Всего** | **2 840** |

Активный phrase universe: 2 332 = 2 313 assigned + 19 SEARCH_REQUIRED. Ни одна deferred/search-required/hold строка не была молча объявлена resolved.

## 3. Атомарная семантическая коррекция

Источник назначения — correction ledgers и V7 unit ID. Источник производных полей — только `STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V6.tsv` по final unit ID, а не старые row metadata V7.

| Контроль | Результат |
|---|---:|
| explicit correction rows | 69 |
| correction ID mismatch | 0 |
| assigned target-contract mismatch | 0 |
| unmapped active rows | 0 |
| stale task/intent/scope/role after rebuild | 0 |

Проверочные примеры:

| Фраза | Final unit | Canonical task | Scope | Final page/state |
|---|---|---|---|---|
| дом с французскими окнами | GLAZING_DESIGN_INSPIRATION | view glazing/window design ideas, photos or examples | IN_SCOPE | https://okno-msk.ru/nashi-raboty/ |
| как открыть пластиковую дверь | PVC_DOOR_OPERATION_ADJUSTMENT_DIY_INFO | operate/adjust PVC doors yourself | DEFERRED_PENDING_MISSING_EVIDENCE | ASSIGNED_HOLD |
| ремонт балкона без остекления | OPEN_BALCONY_FINISHING | finish/renovate an open balcony without glazing as the primary job | IN_SCOPE | https://okno-msk.ru/balkony-i-lodzhii/otdelka-balkonov |
| алюминиевые окна для частного дома | ALUMINIUM_WINDOWS_COMMERCIAL | buy/order aluminium windows | IN_SCOPE | https://okno-msk.ru/alyuminievye-okna/ |
| замена алюминиевых окон | ALUMINIUM_WINDOW_REPLACEMENT_SERVICE | professional aluminium-window replacement | DEFERRED_PENDING_BUSINESS_TRUTH | ASSIGNED_HOLD |
| почему пластиковых окнах | AMBIGUOUS_PVC_TECH_QUERY | resolve malformed/incomplete PVC-window technical query | DEFERRED_PENDING_MISSING_EVIDENCE | ASSIGNED_HOLD |
| французский навес над окнами | OUTSIDE_REAL_ESTATE_ARCHITECTURE | real-estate/architecture/project inspiration not seeking window/glazing work | OUTSIDE_SCOPE | ASSIGNED |

## 4. Current-site topology overlay

Step14A не оставлен приложением: он материализован в canonical unit authority.

| Unit | Step14A | Final primary | Consequence |
|---|---|---|---|
| BALCONY_ALUMINIUM_SLIDING_GENERAL | D14A006 | https://okno-msk.ru/balkony-i-lodzhii/razdvizhnye-okna-na-balkon | Exact sliding-only balcony owner; cold-explicit stays cold specialist. |
| GLASS_UNIT_PRODUCT_SELECTION | D14A007;D14A012;D14A018 | https://okno-msk.ru/okna-rehau/steklopakety-dlya-plastikovykh-okon | Exact commercial hub primary; manufacturing/info specialists support. |
| OPEN_BALCONY_FINISHING | D14A005 | https://okno-msk.ru/balkony-i-lodzhii/otdelka-balkonov | Fresh discovery proved exact standalone service owner. |
| OUTDOOR_ALUMINIUM_SLIDING_GLAZING | D14A021 | https://okno-msk.ru/verandy/razdvizhnye-okna-na-verandu | Exact sliding veranda/terrace specialist primary. |
| PRIVATE_HOUSE_PVC_WINDOWS_WOODEN_HOUSE | D14A011 | https://okno-msk.ru/okna-rehau/po-tipu-doma/okna-v-derevyannyj-dom | Exact wooden-house specialist supersedes broad fallback. |

Дополнительные Step14A pages сохранены как support/competitor topology; same-task candidates не превращены в merge/delete/redirect без доказательства вреда.

## 5. Canonical action authority

Создан единый 34-row action authority из Step18 с обязательным применением Step20 correction overlays.

- `S18-A012`: Retain the current door price/price-estimation guidance; strengthen only the still-missing door-specific professional installation scope/process, including what the service covers and how the installation service is explained on the accepted PVC-door page.
- Boundary: Do not recreate or duplicate the existing price factors/calculator/measurer guidance; internal standalone-installation priority remains unknown; no traffic/conversion claim.
- `S18-A027`: Do not add a duplicate basic French-window definition. If terminology remains ambiguous, fold only residual naming/distinction guidance for French vs panoramic and imitation/partition/block terminology into the broader S18-A009 French-window content work.
- Boundary: No separate duplicate definition block; coordinate with S18-A009; close this package as no-separate-change if the broader edit already resolves the residual terminology distinction.

Следовательно, старые client contradictions не являются частью новой authority. Все поздние отчёты и data views обязаны читать этот набор.

## 6. Residual uncertainty

Создан отдельный uncertainty register:

| State | Records |
|---|---:|
| REVIEW_DEFERRED | 174 |
| SEARCH_REQUIRED | 19 |
| HOLD structural units | 20 |
| LOW_CONFIDENCE outside hold | 2 |
| CURRENT_OVERLAP_RECHECK | 6 |

HOLD не означает нерелевантность. CURRENT_OVERLAP не означает доказанную каннибализацию. Переход к resolved допустим только через evidence + decision source + lineage + downstream materialization.

## 7. Что изменилось и что сохранено

Изменилось:

- исправленные unit assignments теперь имеют полностью перестроенные semantic metadata;
- пять exact owner updates Step14A встроены в current page truth;
- A012/A027 читаются только в исправленной Step20 формулировке;
- все 2 840 строк имеют один final state и claim boundary.

Сохранено:

- 0 новых страниц;
- 0 destructive actions;
- Search-only архитектура и осторожные ownership boundaries;
- 199 pair outcomes без доказанной вредной каннибализации;
- все deferred/unresolved/hold states;
- AI не изменяет architecture master.

## 8. QA

```json
{
  "date": "2026-09-05",
  "stage": 5,
  "status": "PASS",
  "source_rows": 2840,
  "unique_phrases": 2840,
  "master_rows": 2840,
  "master_state_counts": {
    "EXCLUDED_PRESERVED": 334,
    "ASSIGNED": 2271,
    "SEARCH_REQUIRED": 19,
    "ASSIGNED_HOLD": 42,
    "REVIEW_DEFERRED": 174
  },
  "step11_rows": 2332,
  "v7_rows": 2332,
  "assigned_rows": 2313,
  "structural_units": 168,
  "explicit_correction_rows_unique": 69,
  "explicit_correction_failures": 0,
  "assigned_target_contract_failures": 0,
  "unmapped_active_rows": 0,
  "uncertainty_register_rows": 221,
  "uncertainty_state_counts": {
    "SEARCH_REQUIRED": 19,
    "REVIEW_DEFERRED": 174,
    "HOLD": 20,
    "LOW_CONFIDENCE": 2,
    "CURRENT_OVERLAP_RECHECK": 6
  },
  "step14a_exact_owner_overrides": 5,
  "action_authority_rows": 34,
  "step20_action_overlays_applied": 2,
  "new_page_actions": 0,
  "destructive_actions": 0,
  "new_provider_calls": 0,
  "new_paid_cost_rub": 0,
  "next_stage": 6
}
```

Итог: `STAGE_5_COMPLETE__ONE_FINAL_SEMANTIC_MASTER_ACCEPTED__UNCERTAINTY_PRESERVED__READY_FOR_STAGE_6`.
