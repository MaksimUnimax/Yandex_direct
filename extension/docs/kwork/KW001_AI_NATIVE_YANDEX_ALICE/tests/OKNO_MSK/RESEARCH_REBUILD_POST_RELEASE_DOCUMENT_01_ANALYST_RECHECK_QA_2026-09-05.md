# OKNO_MSK — deterministic QA документа №01 после owner recheck correction

**Дата:** 2026-09-05  
**Результат:** `PASS`  
**Объём:** только recipient document №01; №02/№03 не переоценивались

## Итог

- QF: 21/21 PASS after correction; corrected cards: 9 (8 routing + QF003 traceability); unresolved: 0.
- QF evidence classes: 16 stored representative + exact Stage-13; 1 Stage-5 exact-title without stored representative; 4 true family-only.
- Search: 75/75 exact observations remain exact-query scoped.
- AI: 8/8 causal chains contain before-AI, observation, delta, verdict, architecture effect, action and limitation.
- Actions: 7 fully READY physical changes; 1 partial S18-A012; 19 analytical mappings; 4 evidence rechecks.
- Markdown/DOCX/PDF material-content equivalence: PASS.

## Gates

| Gate | Result | Detail |
|---|---|---|
| `ACTION_UNIVERSE` | `PASS` | rows=34 |
| `READY_REAL_SITE_COUNT` | `PASS` | ready=['S18-A009', 'S18-A010', 'S18-A026', 'S18-A028', 'S18-A029', 'S18-A030', 'S18-A031'] |
| `PARTIAL_BUSINESS_DETAIL_COUNT` | `PASS` | partial=['S18-A012'] |
| `ANALYTICAL_MAPPING_COUNT` | `PASS` | Counter({'READY_ANALYTICAL_MAPPING': 19, 'READY': 7, 'NOT_READY__EVIDENCE_REQUIRED': 4, 'READY_PARTIAL__BUSINESS_DETAIL_REQUIRED': 1, 'NO_SEPARATE_CHANGE__COMBINE_A009': 1, 'PENDING_DETAIL__PLACEMENT_NOT_PROVEN': 1, 'HOLD__EVIDENCE_REQUIRED': 1}) |
| `NOT_READY_RECHECK_COUNT` | `PASS` | Counter({'READY_ANALYTICAL_MAPPING': 19, 'READY': 7, 'NOT_READY__EVIDENCE_REQUIRED': 4, 'READY_PARTIAL__BUSINESS_DETAIL_REQUIRED': 1, 'NO_SEPARATE_CHANGE__COMBINE_A009': 1, 'PENDING_DETAIL__PLACEMENT_NOT_PROVEN': 1, 'HOLD__EVIDENCE_REQUIRED': 1}) |
| `QF_VISIBILITY` | `PASS` | count=21 |
| `QF001_EXACT_ROW` | `PASS` | алюминиевые окна на балкон |
| `QF001_EXACT_OWNER` | `PASS` | https://okno-msk.ru/alyuminievye-okna/ |
| `QF001_UNIT` | `PASS` | ALUMINIUM_WINDOWS_COMMERCIAL |
| `QF001_STATE` | `PASS` | state + uncertainty |
| `QF001_UNIT_AUTHORITY` | `PASS` | https://okno-msk.ru/alyuminievye-okna/ |
| `QF001_DISTINCTION` | `PASS` | explicit exact/family boundary |
| `QF001_EVIDENCE_BASIS` | `PASS` | visible evidence bridge |
| `QF001_NO_PHYSICAL_ACTION` | `PASS` | analytical/site boundary |
| `QF002_EXACT_ROW` | `PASS` | холодное алюминиевое остекление балконов |
| `QF002_EXACT_OWNER` | `PASS` | https://okno-msk.ru/balkony-i-lodzhii/holodnoe-osteklenie/ |
| `QF002_UNIT` | `PASS` | BALCONY_GLAZING_COLD |
| `QF002_STATE` | `PASS` | state + uncertainty |
| `QF002_UNIT_AUTHORITY` | `PASS` | https://okno-msk.ru/balkony-i-lodzhii/holodnoe-osteklenie/ |
| `QF002_EVIDENCE_BASIS` | `PASS` | visible evidence bridge |
| `QF002_NO_PHYSICAL_ACTION` | `PASS` | analytical/site boundary |
| `QF003_TITLE_EXACT_ROW` | `PASS` | алюминиевые окна для частного дома |
| `QF003_TITLE_EXACT_OWNER` | `PASS` | https://okno-msk.ru/alyuminievye-okna/ |
| `QF003_TITLE_UNIT` | `PASS` | ALUMINIUM_WINDOWS_COMMERCIAL |
| `QF003_TITLE_STATE` | `PASS` | state + uncertainty |
| `QF003_TITLE_SUPPORT` | `PASS` | https://okno-msk.ru/alyuminievye-okna/provedal |
| `QF003_TITLE_ACTION` | `PASS` | KEEP_EXISTING_STRUCTURE |
| `QF003_TITLE_UNIT_AUTHORITY` | `PASS` | https://okno-msk.ru/alyuminievye-okna/ |
| `QF003_MISSING_REP_PROVENANCE` | `PASS` | missing stored representative provenance visible |
| `QF003_SEMANTIC_IS_NOT_SEARCH` | `PASS` | semantic assignment kept separate from Search |
| `QF003_NOT_FALSE_FAMILY_ONLY` | `PASS` | known exact authority must not be suppressed |
| `QF003_EVIDENCE_BASIS` | `PASS` | visible evidence bridge |
| `QF003_NO_PHYSICAL_ACTION` | `PASS` | analytical/site boundary |
| `QF004_EXACT_ROW` | `PASS` | панорамные алюминиевые окна |
| `QF004_EXACT_OWNER` | `PASS` | https://okno-msk.ru/alyuminievye-okna/ |
| `QF004_UNIT` | `PASS` | ALUMINIUM_WINDOWS_COMMERCIAL |
| `QF004_STATE` | `PASS` | state + uncertainty |
| `QF004_UNIT_AUTHORITY` | `PASS` | https://okno-msk.ru/alyuminievye-okna/ |
| `QF004_EVIDENCE_BASIS` | `PASS` | visible evidence bridge |
| `QF004_NO_PHYSICAL_ACTION` | `PASS` | analytical/site boundary |
| `QF005_EXACT_ROW` | `PASS` | установка алюминиевых окон |
| `QF005_EXACT_OWNER` | `PASS` | https://okno-msk.ru/uslugi/ustanovka-okon/ |
| `QF005_UNIT` | `PASS` | WINDOW_INSTALLATION_SERVICE |
| `QF005_STATE` | `PASS` | state + uncertainty |
| `QF005_UNIT_AUTHORITY` | `PASS` | https://okno-msk.ru/uslugi/ustanovka-okon/ |
| `QF005_DISTINCTION` | `PASS` | explicit exact/family boundary |
| `QF005_EVIDENCE_BASIS` | `PASS` | visible evidence bridge |
| `QF005_NO_PHYSICAL_ACTION` | `PASS` | analytical/site boundary |
| `QF006_EXACT_ROW` | `PASS` | алюминиевые окна для веранды |
| `QF006_EXACT_OWNER` | `PASS` | https://okno-msk.ru/alyuminievye-okna/ |
| `QF006_UNIT` | `PASS` | ALUMINIUM_WINDOWS_COMMERCIAL |
| `QF006_STATE` | `PASS` | state + uncertainty |
| `QF006_UNIT_AUTHORITY` | `PASS` | https://okno-msk.ru/alyuminievye-okna/ |
| `QF006_DISTINCTION` | `PASS` | explicit exact/family boundary |
| `QF006_EVIDENCE_BASIS` | `PASS` | visible evidence bridge |
| `QF006_NO_PHYSICAL_ACTION` | `PASS` | analytical/site boundary |
| `QF007_EXACT_ROW` | `PASS` | панорамное остекление балкона |
| `QF007_EXACT_OWNER` | `PASS` | https://okno-msk.ru/balkony-i-lodzhii/panoramnoe-osteklenie-balkona/ |
| `QF007_UNIT` | `PASS` | PANORAMIC_BALCONY_GLAZING |
| `QF007_STATE` | `PASS` | state + uncertainty |
| `QF007_UNIT_AUTHORITY` | `PASS` | https://okno-msk.ru/balkony-i-lodzhii/panoramnoe-osteklenie-balkona/ |
| `QF007_EVIDENCE_BASIS` | `PASS` | visible evidence bridge |
| `QF007_NO_PHYSICAL_ACTION` | `PASS` | analytical/site boundary |
| `QF008_NO_EXACT_INVENTED` | `PASS` | family-only boundary |
| `QF008_EVIDENCE_BASIS` | `PASS` | visible evidence bridge |
| `QF008_NO_PHYSICAL_ACTION` | `PASS` | analytical/site boundary |
| `QF009_NO_EXACT_INVENTED` | `PASS` | family-only boundary |
| `QF009_EVIDENCE_BASIS` | `PASS` | visible evidence bridge |
| `QF009_NO_PHYSICAL_ACTION` | `PASS` | analytical/site boundary |
| `QF010_EXACT_ROW` | `PASS` | установка подоконника на пластиковые окна |
| `QF010_EXACT_OWNER` | `PASS` | https://okno-msk.ru/uslugi/otdelka-otkosov/ |
| `QF010_UNIT` | `PASS` | WINDOW_FINISHING_SERVICE |
| `QF010_STATE` | `PASS` | state + uncertainty |
| `QF010_UNIT_AUTHORITY` | `PASS` | https://okno-msk.ru/uslugi/otdelka-otkosov/ |
| `QF010_DISTINCTION` | `PASS` | explicit exact/family boundary |
| `QF010_EVIDENCE_BASIS` | `PASS` | visible evidence bridge |
| `QF010_NO_PHYSICAL_ACTION` | `PASS` | analytical/site boundary |
| `QF011_NO_EXACT_INVENTED` | `PASS` | family-only boundary |
| `QF011_EVIDENCE_BASIS` | `PASS` | visible evidence bridge |
| `QF011_NO_PHYSICAL_ACTION` | `PASS` | analytical/site boundary |
| `QF012_EXACT_ROW` | `PASS` | ремонт ручки на пластиковом окне |
| `QF012_EXACT_OWNER` | `PASS` | https://okno-msk.ru/uslugi/remont-okon/ |
| `QF012_UNIT` | `PASS` | WINDOW_REPAIR_SERVICE |
| `QF012_STATE` | `PASS` | state + uncertainty |
| `QF012_UNIT_AUTHORITY` | `PASS` | https://okno-msk.ru/uslugi/remont-okon/ |
| `QF012_EVIDENCE_BASIS` | `PASS` | visible evidence bridge |
| `QF012_NO_PHYSICAL_ACTION` | `PASS` | analytical/site boundary |
| `QF013_EXACT_ROW` | `PASS` | французские панорамные окна |
| `QF013_EXACT_OWNER` | `PASS` | https://okno-msk.ru/okna-rehau/panoramnoe-osteklenie/ |
| `QF013_UNIT` | `PASS` | PANORAMIC_WINDOWS_COMMERCIAL_CORE |
| `QF013_STATE` | `PASS` | state + uncertainty |
| `QF013_UNIT_AUTHORITY` | `PASS` | https://okno-msk.ru/okna-rehau/panoramnoe-osteklenie/ |
| `QF013_DISTINCTION` | `PASS` | explicit exact/family boundary |
| `QF013_EVIDENCE_BASIS` | `PASS` | visible evidence bridge |
| `QF013_NO_PHYSICAL_ACTION` | `PASS` | analytical/site boundary |
| `QF014_EXACT_ROW` | `PASS` | французские окна в частном доме |
| `QF014_EXACT_OWNER` | `PASS` | https://okno-msk.ru/okna-rehau/francuzskie-okna/ |
| `QF014_UNIT` | `PASS` | FRENCH_WINDOWS_COMMERCIAL |
| `QF014_STATE` | `PASS` | state + uncertainty |
| `QF014_UNIT_AUTHORITY` | `PASS` | https://okno-msk.ru/okna-rehau/francuzskie-okna/ |
| `QF014_EVIDENCE_BASIS` | `PASS` | visible evidence bridge |
| `QF014_NO_PHYSICAL_ACTION` | `PASS` | analytical/site boundary |
| `QF015_EXACT_ROW` | `PASS` | установка французского окна |
| `QF015_EXACT_OWNER` | `PASS` | https://okno-msk.ru/uslugi/ustanovka-okon/ |
| `QF015_UNIT` | `PASS` | WINDOW_INSTALLATION_SERVICE |
| `QF015_STATE` | `PASS` | state + uncertainty |
| `QF015_UNIT_AUTHORITY` | `PASS` | https://okno-msk.ru/uslugi/ustanovka-okon/ |
| `QF015_DISTINCTION` | `PASS` | explicit exact/family boundary |
| `QF015_EVIDENCE_BASIS` | `PASS` | visible evidence bridge |
| `QF015_NO_PHYSICAL_ACTION` | `PASS` | analytical/site boundary |
| `QF016_EXACT_ROW` | `PASS` | панорамные окна в частном доме |
| `QF016_EXACT_OWNER` | `PASS` | https://okno-msk.ru/okna-rehau/po-tipu-doma/okna-v-chastnyj-dom/ |
| `QF016_UNIT` | `PASS` | PANORAMIC_PRIVATE_HOUSE_USECASE |
| `QF016_STATE` | `PASS` | state + uncertainty |
| `QF016_UNIT_AUTHORITY` | `PASS` | https://okno-msk.ru/okna-rehau/po-tipu-doma/okna-v-chastnyj-dom/ |
| `QF016_DISTINCTION` | `PASS` | explicit exact/family boundary |
| `QF016_EVIDENCE_BASIS` | `PASS` | visible evidence bridge |
| `QF016_NO_PHYSICAL_ACTION` | `PASS` | analytical/site boundary |
| `QF017_EXACT_ROW` | `PASS` | панорамные окна на террасу |
| `QF017_EXACT_OWNER` | `PASS` | https://okno-msk.ru/verandy/ |
| `QF017_UNIT` | `PASS` | PANORAMIC_OUTDOOR_GLAZING |
| `QF017_STATE` | `PASS` | state + uncertainty |
| `QF017_UNIT_AUTHORITY` | `PASS` | https://okno-msk.ru/verandy/ |
| `QF017_DISTINCTION` | `PASS` | explicit exact/family boundary |
| `QF017_EVIDENCE_BASIS` | `PASS` | visible evidence bridge |
| `QF017_NO_PHYSICAL_ACTION` | `PASS` | analytical/site boundary |
| `QF018_EXACT_ROW` | `PASS` | замена окна на пластиковое цена москва |
| `QF018_EXACT_OWNER` | `PASS` | https://okno-msk.ru/okna-rehau/po-tipu-doma/zamena-okon-v-kvartire/ |
| `QF018_UNIT` | `PASS` | WINDOW_REPLACEMENT_SERVICE |
| `QF018_STATE` | `PASS` | state + uncertainty |
| `QF018_UNIT_AUTHORITY` | `PASS` | https://okno-msk.ru/okna-rehau/po-tipu-doma/zamena-okon-v-kvartire/ |
| `QF018_EVIDENCE_BASIS` | `PASS` | visible evidence bridge |
| `QF018_NO_PHYSICAL_ACTION` | `PASS` | analytical/site boundary |
| `QF019_EXACT_ROW` | `PASS` | как открыть пластиковое окно |
| `QF019_EXACT_OWNER` | `PASS` | https://okno-msk.ru/stati/okno-otkrylos-v-dvuh-polozheniyah-chto-delat/ |
| `QF019_UNIT` | `PASS` | PVC_WINDOW_OPERATION_DIY |
| `QF019_STATE` | `PASS` | state + uncertainty |
| `QF019_UNIT_AUTHORITY` | `PASS` | https://okno-msk.ru/stati/okno-otkrylos-v-dvuh-polozheniyah-chto-delat/ |
| `QF019_EVIDENCE_BASIS` | `PASS` | visible evidence bridge |
| `QF019_NO_PHYSICAL_ACTION` | `PASS` | analytical/site boundary |
| `QF020_EXACT_ROW` | `PASS` | лучшие пластиковые окна |
| `QF020_EXACT_OWNER` | `PASS` | https://okno-msk.ru/stati/kakie-okna-samye-luchshie/ |
| `QF020_UNIT` | `PASS` | BEST_PVC_REHAU_WINDOWS_COMPARISON |
| `QF020_STATE` | `PASS` | state + uncertainty |
| `QF020_UNIT_AUTHORITY` | `PASS` | https://okno-msk.ru/stati/kakie-okna-samye-luchshie/ |
| `QF020_EVIDENCE_BASIS` | `PASS` | visible evidence bridge |
| `QF020_NO_PHYSICAL_ACTION` | `PASS` | analytical/site boundary |
| `QF021_NO_EXACT_INVENTED` | `PASS` | family-only boundary |
| `QF021_EVIDENCE_BASIS` | `PASS` | visible evidence bridge |
| `QF021_NO_PHYSICAL_ACTION` | `PASS` | analytical/site boundary |
| `QF_STORED_REPRESENTATIVE_WITH_EXACT_STAGE13` | `PASS` | ['QF001', 'QF002', 'QF004', 'QF005', 'QF006', 'QF007', 'QF010', 'QF012', 'QF013', 'QF014', 'QF015', 'QF016', 'QF017', 'QF018', 'QF019', 'QF020'] |
| `QF_TITLE_EXACT_NO_STORED_REPRESENTATIVE` | `PASS` | ['QF003'] |
| `QF_TRUE_FAMILY_ONLY` | `PASS` | ['QF008', 'QF009', 'QF011', 'QF021'] |
| `QF_RESOLUTION_CLASS_UNIVERSE` | `PASS` | 16 + 1 + 4 |
| `QF_CORRECTED_SET` | `PASS` | fixed=['QF001', 'QF003', 'QF005', 'QF006', 'QF010', 'QF013', 'QF015', 'QF016', 'QF017'] |
| `QF_UNRESOLVED` | `PASS` | [] |
| `SEARCH_75_VISIBILITY` | `PASS` | authority=75 report=75 |
| `SP09-001_SCOPE` | `PASS` | аксессуары для пластиковых окон |
| `SP09-002_SCOPE` | `PASS` | алюминиевые окна fapim |
| `SP09-003_SCOPE` | `PASS` | балкон без остекления |
| `SP09-004_SCOPE` | `PASS` | безрамное остекление веранды |
| `SP09-005_SCOPE` | `PASS` | демонтаж остекления балкона |
| `SP09-006_SCOPE` | `PASS` | дерево алюминиевые окна |
| `SP09-007_SCOPE` | `PASS` | деревянные окна для частного дома |
| `SP09-008_SCOPE` | `PASS` | дом с панорамными окнами |
| `SP09-009_SCOPE` | `PASS` | как выбрать шторы на пластиковые окна |
| `SP09-010_SCOPE` | `PASS` | комплект для окна алюминиевые |
| `SP09-011_SCOPE` | `PASS` | крыльцо для частного дома окна |
| `SP09-012_SCOPE` | `PASS` | окна rehau 70 |
| `SP09-013_SCOPE` | `PASS` | окна rehau kbe |
| `SP09-014_SCOPE` | `PASS` | окна rehau официальный |
| `SP09-015_SCOPE` | `PASS` | окна rehau провисли |
| `SP09-016_SCOPE` | `PASS` | окна пластиковые москитная |
| `SP09-017_SCOPE` | `PASS` | окна стеклопакеты rehau |
| `SP09-018_SCOPE` | `PASS` | оконная фурнитура отзывы |
| `SP09-019_SCOPE` | `PASS` | остекление балкона с выносом подоконника |
| `SP09-020_SCOPE` | `PASS` | остекление балкона с крышей цена |
| `SP09-021_SCOPE` | `PASS` | остекление балконов деревянными рамами |
| `SP09-022_SCOPE` | `PASS` | остекление балконов конструкция |
| `SP09-023_SCOPE` | `PASS` | остекление веранды фото |
| `SP09-024_SCOPE` | `PASS` | панорамные деревянные окна |
| `SP09-025_SCOPE` | `PASS` | панорамные окна лес |
| `SP09-026_SCOPE` | `PASS` | пластиковые двери видео |
| `SP09-027_SCOPE` | `PASS` | пластиковые двери межкомнатные |
| `SP09-028_SCOPE` | `PASS` | пластиковые двери старый |
| `SP09-029_SCOPE` | `PASS` | пластиковые окна в халва рассрочка |
| `SP09-030_SCOPE` | `PASS` | пластиковые окна район |
| `SP09-031_SCOPE` | `PASS` | почему алюминиевые окна |
| `SP09-032_SCOPE` | `PASS` | ремонт квартиры пластиковые окна |
| `SP09-033_SCOPE` | `PASS` | ремонт пластиковых окон район |
| `SP09-034_SCOPE` | `PASS` | ремонт пластиковых окон телефон |
| `SP09-035_SCOPE` | `PASS` | ремонт подоконников пластиковых окон |
| `SP09-036_SCOPE` | `PASS` | установка пластиковых окон деревянном |
| `SP09-037_SCOPE` | `PASS` | установка пластиковых окон размером |
| `SP09-038_SCOPE` | `PASS` | французские мягкие окна |
| `SP09-039_SCOPE` | `PASS` | цены материала на пластиковые окна |
| `SP09-040_SCOPE` | `PASS` | шторы на пластиковые окна фото цены |
| `SP09-041_SCOPE` | `PASS` | provedal остекление веранды |
| `SP09-042_SCOPE` | `PASS` | алюминиевые окна provedal |
| `SP09-043_SCOPE` | `PASS` | алюминиевые окна проведал |
| `SP09-044_SCOPE` | `PASS` | окна rehau в рассрочку |
| `SP09-045_SCOPE` | `PASS` | окна рехау в рассрочку |
| `SP09-046_SCOPE` | `PASS` | оконная фурнитура rehau |
| `SP09-047_SCOPE` | `PASS` | оконная фурнитура рехау |
| `SP09-048_SCOPE` | `PASS` | пластиковые окна rehau |
| `SP09-049_SCOPE` | `PASS` | пластиковые окна от производителя rehau |
| `SP09-050_SCOPE` | `PASS` | пластиковые окна рехау |
| `SP09-051_SCOPE` | `PASS` | пластиковые окна рехау от производителя |
| `SP09-052_SCOPE` | `PASS` | пошаговая установка пластиковых окон |
| `SP09-053_SCOPE` | `PASS` | проведал остекление веранды |
| `SP09-054_SCOPE` | `PASS` | ремонт пластиковых окон в одинцове |
| `SP09-055_SCOPE` | `PASS` | ремонт пластиковых окон в одинцово |
| `SP09-056_SCOPE` | `PASS` | установка пластиковых окон пошагово |
| `SP09-057_SCOPE` | `PASS` | rehau thermo окна |
| `SP09-058_SCOPE` | `PASS` | алюминиевые окна москва |
| `SP09-059_SCOPE` | `PASS` | как выбрать пластиковые окна |
| `SP09-060_SCOPE` | `PASS` | какой профиль rehau выбрать |
| `SP09-061_SCOPE` | `PASS` | окна rehau москва |
| `SP09-062_SCOPE` | `PASS` | остекление балкона п 46 |
| `SP09-063_SCOPE` | `PASS` | остекление балкона с выносом |
| `SP09-064_SCOPE` | `PASS` | остекление балкона с крышей |
| `SP09-065_SCOPE` | `PASS` | остекление балконов москва |
| `SP09-066_SCOPE` | `PASS` | остекление беседки |
| `SP09-067_SCOPE` | `PASS` | остекление веранды |
| `SP09-068_SCOPE` | `PASS` | остекление террасы |
| `SP09-069_SCOPE` | `PASS` | пластиковые двери москва |
| `SP09-070_SCOPE` | `PASS` | пластиковые окна митино |
| `SP09-071_SCOPE` | `PASS` | пластиковые окна москва |
| `SP09-072_SCOPE` | `PASS` | пластиковые окна от производителя |
| `SP09-073_SCOPE` | `PASS` | теплое остекление балкона |
| `SP09-074_SCOPE` | `PASS` | установка пластиковых окон москва |
| `SP09-075_SCOPE` | `PASS` | холодное остекление балкона |
| `AI_8_VISIBILITY` | `PASS` | authority=8 report=8 |
| `C15-004_CAUSAL_CHAIN` | `PASS` | all causal labels |
| `C15-004_VERDICT` | `PASS` | DE_RISK |
| `C15-004_CURRENT_EXACT_OWNER` | `PASS` | https://okno-msk.ru/alyuminievye-okna/ |
| `C15-006_CAUSAL_CHAIN` | `PASS` | all causal labels |
| `C15-006_VERDICT` | `PASS` | DE_RISK |
| `C15-006_CURRENT_EXACT_OWNER` | `PASS` | https://okno-msk.ru/alyuminievye-okna/ |
| `C15-007_CAUSAL_CHAIN` | `PASS` | all causal labels |
| `C15-007_VERDICT` | `PASS` | DE_RISK |
| `C15-007_CURRENT_EXACT_OWNER` | `PASS` | https://okno-msk.ru/balkony-i-lodzhii/panoramnoe-osteklenie-balkona/ |
| `C15-010_CAUSAL_CHAIN` | `PASS` | all causal labels |
| `C15-010_VERDICT` | `PASS` | NO_CHANGE |
| `C15-010_CURRENT_EXACT_OWNER` | `PASS` | https://okno-msk.ru/uslugi/otdelka-otkosov/ |
| `C15-013_CAUSAL_CHAIN` | `PASS` | all causal labels |
| `C15-013_VERDICT` | `PASS` | DE_RISK |
| `C15-013_CURRENT_EXACT_OWNER` | `PASS` | https://okno-msk.ru/okna-rehau/panoramnoe-osteklenie/ |
| `C15-018_CAUSAL_CHAIN` | `PASS` | all causal labels |
| `C15-018_VERDICT` | `PASS` | NO_CHANGE |
| `C15-018_CURRENT_EXACT_OWNER` | `PASS` | https://okno-msk.ru/okna-rehau/po-tipu-doma/zamena-okon-v-kvartire/ |
| `C15-019_CAUSAL_CHAIN` | `PASS` | all causal labels |
| `C15-019_VERDICT` | `PASS` | NO_CHANGE |
| `C15-019_CURRENT_EXACT_OWNER` | `PASS` | https://okno-msk.ru/stati/okno-otkrylos-v-dvuh-polozheniyah-chto-delat/ |
| `C15-020_CAUSAL_CHAIN` | `PASS` | all causal labels |
| `C15-020_VERDICT` | `PASS` | INSUFFICIENT |
| `C15-020_CURRENT_EXACT_OWNER` | `PASS` | https://okno-msk.ru/stati/kakie-okna-samye-luchshie/ |
| `ACTION_S18-A001_MAP` | `PASS` | S18-A001 |
| `ACTION_S18-A002_MAP` | `PASS` | S18-A002 |
| `ACTION_S18-A003_MAP` | `PASS` | S18-A003 |
| `ACTION_S18-A004_MAP` | `PASS` | S18-A004 |
| `ACTION_S18-A005_MAP` | `PASS` | S18-A005 |
| `ACTION_S18-A006_MAP` | `PASS` | S18-A006 |
| `ACTION_S18-A007_MAP` | `PASS` | S18-A007 |
| `ACTION_S18-A008_MAP` | `PASS` | S18-A008 |
| `ACTION_S18-A009_MAP` | `PASS` | S18-A009 |
| `ACTION_S18-A010_MAP` | `PASS` | S18-A010 |
| `ACTION_S18-A011_MAP` | `PASS` | S18-A011 |
| `ACTION_S18-A012_MAP` | `PASS` | S18-A012 |
| `ACTION_S18-A013_MAP` | `PASS` | S18-A013 |
| `ACTION_S18-A014_MAP` | `PASS` | S18-A014 |
| `ACTION_S18-A015_MAP` | `PASS` | S18-A015 |
| `ACTION_S18-A016_MAP` | `PASS` | S18-A016 |
| `ACTION_S18-A017_MAP` | `PASS` | S18-A017 |
| `ACTION_S18-A018_MAP` | `PASS` | S18-A018 |
| `ACTION_S18-A019_MAP` | `PASS` | S18-A019 |
| `ACTION_S18-A020_MAP` | `PASS` | S18-A020 |
| `ACTION_S18-A021_MAP` | `PASS` | S18-A021 |
| `ACTION_S18-A022_MAP` | `PASS` | S18-A022 |
| `ACTION_S18-A023_MAP` | `PASS` | S18-A023 |
| `ACTION_S18-A024_MAP` | `PASS` | S18-A024 |
| `ACTION_S18-A025_MAP` | `PASS` | S18-A025 |
| `ACTION_S18-A026_MAP` | `PASS` | S18-A026 |
| `ACTION_S18-A027_MAP` | `PASS` | S18-A027 |
| `ACTION_S18-A028_MAP` | `PASS` | S18-A028 |
| `ACTION_S18-A029_MAP` | `PASS` | S18-A029 |
| `ACTION_S18-A030_MAP` | `PASS` | S18-A030 |
| `ACTION_S18-A031_MAP` | `PASS` | S18-A031 |
| `ACTION_S18-A032_MAP` | `PASS` | S18-A032 |
| `ACTION_S18-A033_MAP` | `PASS` | S18-A033 |
| `ACTION_S18-A034_MAP` | `PASS` | S18-A034 |
| `A012_FALSE_READY_REMOVED` | `PASS` | {'action_id': 'S18-A012', 'priority': 'P1_HIGH', 'target_object': 'https://okno-msk.ru/dveri-rehau', 'implementation_mode': 'CONTENT_BLOCK_PARTIAL', 'real_site_change': 'PARTIAL', 'recipient_state': 'READY_PARTIAL__BUSINESS_DETAIL_REQUIRED', 'description_ru': 'Сохранить существующие цену, калькулятор и путь к замеру; добавить только нейтральное объяснение роли профессионального монтажа, а фактический состав услуги раскрывать после подтверждения компанией.', 'current_state_ru': 'Страница уже содержит цену, калькулятор, замер и упоминание монтажа/сложности установки. Сохранённые данные не фиксируют фактический состав стандартной услуги компании, исключения из неё или обязанности клиента.', 'evidence_meaning_ru': 'Текущая страница подтверждает тему монтажа и необходимость понятного перехода к профессиональному процессу, но не подтверждает договорный состав услуги. Поэтому безопасна только нейтральная READY-часть; фактические границы услуги не готовы к публикации.', 'evidence_locator': 'Stage06 implementation specification #S18-A012; current-page validation CV005; owner recheck OR-02', 'target_state_ru': 'Сохранить цену, калькулятор и CTA к замеру/консультации. Можно нейтрально объяснить, что профессиональный монтаж является отдельным этапом проекта и что точный состав работ подтверждается после замера; конкретные включения, исключения и обязанности клиента публикуются только после бизнес-подтверждения.', 'exact_location_ru': 'Короткий поясняющий блок после цен/калькулятора либо перед формой бесплатного замера; перечень состава услуги пока не публиковать.', 'exact_instruction_ru': 'Сохранить существующую ценовую часть. Добавить только нейтральный переход к профессиональному монтажу и консультации/замеру без перечисления неподтверждённых операций. Отдельно запросить у компании фактический состав услуги до публикации перечня «входит / не входит / должен подготовить клиент».', 'queries_ru': 'балконное окно с дверью пластиковое цена установкой / установка пластикового окна с балконной дверью / установка пластиковой балконной двери / установка пластиковой двери / установка пластиковой двери цена / установка пластиковых дверей москва / установка пластиковых дверей цена москва / установка пластиковых окон и дверей', 'topics_ru': 'роль профессионального монтажа; индивидуальное уточнение состава после замера; консультация', 'questions_ru': 'Где уточнить фактический состав монтажа? На каком этапе он подтверждается для конкретного заказа?', 'implementation_example_ru': 'Нейтральная форма: «Профессиональный монтаж — отдельный этап проекта. Точный состав работ и условия для вашего проёма специалист подтвердит после замера».', 'dependencies': 'BUSINESS_CONFIRMATION_FOR_COMPANY_SPECIFIC_SERVICE_SCOPE', 'do_not_break_ru': 'Не публиковать как факт состав услуги, исключения, обязанности клиента, демонтаж/вывоз, отделку или гарантийные условия без подтверждения компании.', 'acceptance_ru': 'Цена, калькулятор и CTA сохранены; новый текст не обещает конкретных операций, исключений, подготовки клиента, вывоза, отделки или гарантийных условий; company-specific перечень явно остаётся PENDING_BUSINESS_DETAIL до документированного подтверждения.', 'ready_scope_ru': 'Сохранить цену/калькулятор/замер; пояснить роль профессионального монтажа и направить к консультации, не перечисляя состав работ.', 'pending_business_detail_ru': 'Нужно подтверждение компании: какие операции входят и не входят; что готовит клиент; демонтаж/вывоз; откосы/отделка; герметизация и регулировка как обязательства; точные гарантийные и сервисные границы.', 'authority_lineage': 'Stage05 semantic/action truth -> post-release implementation correction 2026-09-05'} |
| `A012_BUSINESS_BOUNDARY_VISIBLE` | `PASS` | split visible |
| `SUMMARY_COUNTS` | `PASS` | 7 ready + 1 partial + 19 analytical + 4 recheck |
| `POSITIVE_KEEP_VISIBLE` | `PASS` | KEEP/NO_CHANGE |
| `UNCERTAINTY_REOPEN_VISIBLE` | `PASS` | states and reopen rules |
| `DOCX_CONTENT_EQUIVALENCE` | `PASS` | all material endpoints and corrected states |
| `PDF_CONTENT_EQUIVALENCE` | `PASS` | all material endpoints and corrected states |

`DOCUMENT_01_ANALYST_RECHECK = PASS`  
`DOCUMENT_01_OWNER_REVIEW = PENDING`
