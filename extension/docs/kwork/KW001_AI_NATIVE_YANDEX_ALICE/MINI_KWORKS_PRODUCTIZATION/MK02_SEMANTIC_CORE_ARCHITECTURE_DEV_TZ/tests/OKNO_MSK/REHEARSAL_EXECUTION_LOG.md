# MK02 / OKNO_MSK — журнал автономного выполнения

Дата: **2026-09-10**  
Режим: **preserved-evidence replay; MK02-only; Yandex-only**  
Новые provider calls: **0**

Этот журнал описывает фактически выполненные операции MK02. Ссылка на исходный KW-001 не заменяет доказательство: для каждого шага указан конкретный сохранённый источник и новый MK02 output.

## Общая сверка после Step 13

```text
source universe = 2840
working core = 2185
review / uncertain = 187
excluded = 468
2840 = 2185 + 187 + 468
total semantic groups = 59
working groups = 54
outside groups = 5
active phrase→page rows = 2185
active structural units = 160
preserved unit ledger = 168
Step5A additions admitted = 0
current public topology nodes = 2683
target existing family-owner pages = 59
provider calls during rehearsal = 0
```

## Step 00 — заказ, scope и ограничения

- **Input:** сохранённый OKNO_MSK business/site context; текущий `CLIENT_INPUT_CONTRACT.md`.
- **Authority:** публичный сайт `https://okno-msk.ru/`, Москва, сохранённый order/business context; неизвестные ограничения не заменены догадками.
- **Операция:** спроецирован заказ только на MK02; зафиксированы включённые направления, Yandex-only, отсутствие Step5A/Google/AI/MK03/MK04/MK06 и состояние private inputs.
- **Output:** `MOCK_CLIENT_ORDER.md`.
- **Accounting:** 1 сайт, 1 основной регион, 16 направлений; protected URL/CMS/производственный график — не предоставлены.
- **Uncertainty:** `NONE KNOWN FROM PRESERVED INPUT` не означает отсутствия технических ограничений.
- **QA:** **PASS** — pre-start contract заполнен без секрета и без выдуманного факта.

## Step 01 — текущая модель сайта и бизнеса

- **Input:** сохранённые page reads, Step14 recheck и Run10 discovery.
- **Authority:** `STEP_14_CURRENT_URL_RECHECK.tsv` (59), `STEP_14A_CURRENT_SITE_RECONCILIATION_TRANSPORT.json` + 9 chunks (2 624), `STEP_14A_RECONCILIATION_QA_2026-09-02.json`.
- **Операция:** восстановлен независимый current-node ledger; известный upstream не использован как доказательство собственной полноты.
- **Output:** `MK02_CURRENT_SITE_TOPOLOGY_2026-09-10.tsv.gz`.
- **Accounting:** `59 + 2624 = 2683` уникальных путей; Run10: 21 material, 1 932 non-material, 671 out-of-scope, 0 unclassified.
- **Uncertainty:** snapshot 2026-09-02; operational completeness принятого crawl-метода, не математическая исчерпываемость; GEO subdomains вне main-host scope.
- **QA:** **PASS** — decoded SHA `d7329636…fc6a`; 2 683/2 683 уникальны.

## Step 02 — план bounded Wordstat acquisition

- **Input:** order scope, source seed/provenance identifiers в pre-Step5A semantic authority.
- **Authority:** source IDs и occurrence provenance в `STEP_08_SEARCH_STAGE_SEMANTIC_SET.tsv`; accepted MK01 source audit.
- **Операция:** проверено, что приобретённый universe соответствует направлению заказа и уже имеет durable provenance. Для rehearsal новый acquisition plan не запускал провайдера; сохранённый plan projection ограничен нативным universe.
- **Output:** input/hash section `MK02_STEPS_00_13_MANIFEST_2026-09-10.json` и provenance columns semantic foundation.
- **Accounting:** 2 840/2 840 phrases имеют source lineage; seed не трактован как автоматически валидный ключ.
- **Uncertainty:** исторический acquisition plan не превращён в новый запрос; фактическая свежесть соответствует исходному снимку.
- **QA:** **PASS** — Step5A seed/delta phrases в input = 0.

## Step 03 — сохранённое evidence спроса

- **Input:** 2 840-row `STEP_08_SEARCH_STAGE_SEMANTIC_SET.tsv`.
- **Authority:** SHA-256 `73f52fd4…73d1f`, source commit `976f6169…`.
- **Операция:** выполнен полный join с accepted MK01 statuses по exact phrase; перенесены occurrence counts, source IDs, тип Wordstat evidence и provenance.
- **Output:** `MK02_SEMANTIC_FOUNDATION_2026-09-10.tsv.gz`.
- **Accounting:** source 2 840 = output 2 840; unique 2 840; missing join 0; duplicate phrase 0.
- **Uncertainty:** сохранённые Wordstat evidence fields не объявлены текущим live-показателем на 2026-09-10.
- **QA:** **PASS** — provider calls rehearsal 0; provenance не сведён к одному числу частотности.

## Step 04 — консервативный triage

- **Input:** accepted row statuses и причины MK01.
- **Authority:** `MK01_SEMANTIC_UNIVERSE_2026-09-09.tsv.gz`.
- **Операция:** сохранены рабочие, review и две разные exclusion стадии; частотность не использовалась как автоматический фильтр.
- **Output:** status/reason columns semantic foundation.
- **Accounting:** working 2 185; post-row-clean exclusion 334; post-group exclusion 134; deferred 174; Search-required 13.
- **Uncertainty:** `174 + 13 = 187` не исчезают и не получают silent KEEP.
- **QA:** **PASS** — `2185 + 334 + 134 + 174 + 13 = 2840`.

## Step 05 — targeted second acquisition / stop

- **Input:** сохранённый union semantic evidence исходного проекта.
- **Authority:** pre-Step5A Step08 authority и accepted MK01 rehearsal; отдельная Step5A delta используется только отрицательно.
- **Операция:** подтверждено, что нативный продуктовый universe уже закрыт сохранённым acquisition; новые вызовы не нужны для replay. Конкурентная 16-row expansion не допущена.
- **Output:** `STEP5A_DOWNSTREAM_CONTAMINATION_AUDIT.md` и manifest contamination state.
- **Accounting:** `2840 + 0 = 2840`; post-Step5A 2 856 rejected as input.
- **Uncertainty:** отсутствующее доказательство не восполнялось fresh acquisition.
- **QA:** **PASS** — exact prohibited phrase intersection = 0.

## Step 06 — построчная очистка

- **Input:** native source rows + accepted MK01 row decisions.
- **Authority:** accepted MK01 universe; source Step08 provenance.
- **Операция:** exact-phrase join, сохранение decision basis/uncertainty; исключённые строки оставлены в полном output.
- **Output:** full semantic foundation.
- **Accounting:** 2 840 строк получили явный product status; default KEEP = 0; silent data loss = 0.
- **Uncertainty:** 187 review rows сохранены отдельными состояниями.
- **QA:** **PASS**.

## Step 07 — freeze universe и routes

- **Input:** результат Step06.
- **Authority:** `MK02_SEMANTIC_FOUNDATION_2026-09-10.tsv.gz`; `MK02_STEPS_00_13_MANIFEST_2026-09-10.json`.
- **Операция:** зафиксированы один universe, продуктовый статус, Search route и lineage.
- **Output:** deterministic gzip authority + hashes.
- **Accounting:** 2 840 unique; working flag yes 2 185/no 655.
- **Uncertainty:** review/excluded остаются доступны для аудита, но не активируются downstream.
- **QA:** **PASS**.

## Step 08 — targeted ordinary Yandex Search для semantic boundaries

- **Input:** сохранённые exact-query Search datasets и accepted MK01 resolution.
- **Authority:** structured Step11 recovery, Step13 16 Search results и MK01 `Проверка в Яндексе`/route fields.
- **Операция:** повторно использованы только persisted results; owner URL не выводился из target URL и не переносился на непроверенное семейство.
- **Output:** `observed_search_relevant_url` и explicit observation-state columns в phrase map.
- **Accounting:** сохранённые ordinary Search queries reused: 69 Step11 + 16 Step13 = 85; exact structured query совпал с 25 active phrases; target host observed URLs для этих exact rows = 0.
- **Uncertainty:** 187 review/uncertain сохранены; fresh Search = 0.
- **QA:** **PASS** — representative query не объявлен доказательством всего cluster.

## Step 09 — task/intent-first clustering

- **Input:** cleaned semantic foundation.
- **Authority:** accepted MK01 group/task/intent columns; pre-Step5A Stage-5 structural-unit lineage как downstream cross-check.
- **Операция:** сохранены product groups без lexical reclustering и без целевого количества групп.
- **Output:** group/task/intent fields semantic foundation; downstream unit join.
- **Accounting:** 59 total groups; 54 working; 5 outside; 2 185 working rows.
- **Uncertainty:** `Не назначен` относится к review/excluded routing; не превращён в кластер.
- **QA:** **PASS** — task/intent boundary отделена от URL architecture.

## Step 10 — владение страницами и полная phrase→page map

- **Input:** 2 185 accepted working rows, pre-Step5A 2 840-row Stage-5 master, 59 candidate ledgers.
- **Authority:** Stage-5 final semantic master/unit authority; Step11 candidate/read/Search evidence; current Step14A overlays where applicable.
- **Операция:** построена одна строка на каждую active phrase; exact owner, family owner, supporting pages и observed Search URL разделены; blank target сохранён у unresolved/no-page.
- **Output:** `MK02_PHRASE_PAGE_MAP_2026-09-10.tsv.gz`, `MK02_UNIT_OWNERSHIP_LEDGER_2026-09-10.tsv`, `MK02_OWNERSHIP_CANDIDATE_LEDGER_2026-09-10.tsv`.
- **Accounting:** 2 185 rows = 1 647 `OWNER_EXISTING` + 518 `NO_SUITABLE_EXISTING_PAGE` + 14 outside + 6 owner unresolved; family owner nonblank 1 882; support nonblank 1 015; candidate comparisons 105 across 59 ledgers.
- **Uncertainty:** 6 active Search-required rows имеют пустой unit/target; 518 no-suitable rows не стали CREATE.
- **QA:** **PASS** — no target fabrication, no duplicate phrase, complete active coverage.

## Step 11 — structural/content-routing diagnosis

- **Input:** active ownership map, 168 preserved units, current-content/evidence fields.
- **Authority:** pre-Step5A Stage-5 unit/action authorities, `STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V6.tsv`, accepted current overlays.
- **Операция:** активная граница пересчитана из MK01 working core; 8 historical units без active phrases оставлены cross-check-only. Для 160 active units действие отделено от диагноза и evidence.
- **Output:** `MK02_STRUCTURAL_ACTIONS_2026-09-10.tsv`, active slice unit ledger.
- **Accounting:** KEEP 70; route/mapping 45; defer 19; no standalone 14; outside/no action 4; add section/FAQ 6; expand 2; всего 160. CREATE/SPLIT/MERGE/redirect/delete = 0.
- **Uncertainty:** 19 units deferred; content evidence insufficient/not assessed сохранено, а не повышено до READY.
- **QA:** **PASS** — phrase count не использован как page justification; action не является собственным evidence.

## Step 12 — competing-page safety

- **Input:** effective pair universe, query-family cases, saved Search/current-page evidence.
- **Authority:** Step13 final pair accounting, 21-case diagnosis/remediation, accepted base-public policy.
- **Операция:** материализованы 21 case с раздельными relation/current signal/history/harm полями; недоступная private history сохранена явным gap.
- **Output:** `MK02_COMPETING_PAGE_CASES_2026-09-10.tsv`.
- **Accounting:** 195 base pairs + 4 freshness extensions = 199 effective pairs; 21 cases; private history reused 0; proven harmful impact 0; destructive authorization 0.
- **Uncertainty:** историческая конкуренция и вред не доказаны без private query×URL history.
- **QA:** **PASS_BASE_PUBLIC_EVIDENCE_MODE**.

## Step 13 — current-vs-target Search architecture

- **Input:** 160 active units, 59 current rechecks, Run10 2 624 current-minus rows, 21 material deltas, 15 raw internal-link evidence rows.
- **Authority:** Step14 freeze + Step14A final closure and decoded current-site ledger.
- **Операция:** отдельно построены current nodes и target units; выполнена 21-row page delta reconciliation; literal links отделены от рекомендаций. Один source duplicate pair (`IL0038`/`IL0047`) агрегирован в одну видимую relation с сохранением двух source IDs.
- **Output:** `MK02_CURRENT_SITE_TOPOLOGY_2026-09-10.tsv.gz`, `MK02_TARGET_SEARCH_ARCHITECTURE_2026-09-10.tsv`, `MK02_CURRENT_TARGET_DELTA_2026-09-10.tsv`, `MK02_PAGE_RELATIONSHIPS_2026-09-10.tsv`.
- **Accounting:** current nodes 2 683; target units 160; unique existing family-owner pages 59; unit→support relations 103; 21 page deltas; 15 raw link rows = 14 distinct visible pairs; literal present 9 raw/8 distinct, absent planned 6; combined visible deltas 35.
- **Uncertainty:** six absent links не получают READY placement; snapshot date preserved; sitemap limitation preserved.
- **QA:** **PASS** — target != current; known URL list did not prove completeness; duplicate visible pair removed without loss of source IDs.

## Step 14 — implementation specifications

- **Input:** 34 corrected implementation-action rows, 15 raw internal-link evidence rows, 160 active structural units, accepted current/target architecture and competing-page safety state.
- **Authority:** `STEP_18_IMPLEMENTATION_ACTION_AUTHORITY_CORRECTED_2026-09-03.tsv`, `STEP_18_INTERNAL_LINK_IMPLEMENTATION_AUTHORITY_2026-09-03.tsv`, current page reads/owners and accepted Step14A overlays.
- **Операция:** аналитические действия преобразованы в самостоятельные work packages; accounting batch `S18-A032` исключён как ложная «работа» и заменён 14 уникальными page-pair пакетами. READY разрешён только при полноте 12 обязательных полей и одном точном месте. Независимый A–U-контроль понизил четыре исходных READY с альтернативным местом «X или Y» до `PENDING_PLACEMENT_OR_CONTEXT`; график и приоритеты не изобретались.
- **Output:** `MK02_IMPLEMENTATION_WORK_PACKAGES_2026-09-10.tsv`, `MK02_CLARIFICATIONS_NO_CHANGE_HOLD_2026-09-10.tsv`, `MK02_IMPLEMENTATION_ACCEPTANCE_2026-09-10.tsv`, `MK02_ACCEPTANCE_MEASUREMENT_INTERFACE_2026-09-10.tsv`, manifest.
- **Accounting:** 47 packages = 3 READY + 1 business detail + 10 placement/context + 4 recheck + 19 mapping-only + 9 no-site-change + 1 HOLD; acceptance rows 3; Yandex-only measurement classes 6.
- **Uncertainty:** private history, шесть мест ссылок и четыре точных места контентных блоков не доказаны; один business fact не предоставлен. Эти строки не повышены до READY.
- **QA:** **PASS after correction** — READY complete 3/3; ambiguous READY placement 0; placeholder 0; duplicate visible pairs 0; Step5A action IDs 0; invented owner/effort/capacity/timing 0.

## Step 15 — client materialization / final QA / readback

- **Input:** semantic, ownership, current/target, delta, package, clarification, relationship and acceptance authorities.
- **Authority:** current `DELIVERABLE_SPEC.md`; client-visible A–U requirements; accepted outputs Steps 00–14.
- **Операция:** материализованы три logical narrative views и 13-sheet XLSX candidate; клиентская терминология отделена от internal IDs; книга пересчитана, экспортирована, повторно импортирована и отрисована по каждому листу.
- **Output:** `CLIENT_CANDIDATE_PACKAGE_README.md`, `CLIENT_CANDIDATE_ANALYTICAL_REPORT.md`, `CLIENT_CANDIDATE_IMPLEMENTATION_PLAN.md`, `OKNO_MSK_MK02_CLIENT_CANDIDATE_2026-09-10.xlsx`, workbook build report.
- **Accounting:** 13 sheets; universe 2 840; core 2 185; groups 54; mapping 2 185; current relevant pages 80; target units 160; deltas 35; packages 47; clarifications/no-change/HOLD 44; relations 14; READY acceptance 3.
- **Uncertainty:** это физический package candidate для Phase 6, а не замороженный commercial split; current-site freshness ограничена 2026-09-02.
- **QA:** **PASS** — 13/13 renders visually inspected, formula errors before/after import 0, internal-code scan 0; independent validator 21/21; A–U failures 0; recipient review PASS; G0–G15 PASS. Corrected QA/data/XLSX remote-read back at `c76314eb23cff27c64c0a58d89d6fd911979c873`.
