# Step 12 correction — persisted evidence schema profile

Purpose: determine what the already saved Wordstat/Search artifacts actually contain before using any field as evidence. Leading markdown/comment lines in TSV files are ignored when finding the real header.

## STEP_03R_S01_RAW_NORMALIZED.tsv
- data rows: **218**
- header:
```text
section	phrase	count
```
- first persisted data rows (schema inspection only):
```text
result	пластиковые окна	152131
result	пластиковые окна москва	17295
```

## STEP_03R_S02_RAW_NORMALIZED.tsv
- data rows: **220**
- header:
```text
section	phrase	count
```
- first persisted data rows (schema inspection only):
```text
result	окна rehau	2465
result	пластиковые окна rehau	676
```

## STEP_03R_S03_RAW_NORMALIZED.tsv
- data rows: **144**
- header:
```text
section	phrase	count
```
- first persisted data rows (schema inspection only):
```text
result	французские окна	1453
result	французская штора на окно	119
```

## STEP_03R_S04_RAW_NORMALIZED.tsv
- data rows: **29**
- header:
```text
section	phrase	count
```
- first persisted data rows (schema inspection only):
```text
result	окно п 44	252
result	дом п 44 окна	96
```

## STEP_03R_S05_RAW_NORMALIZED.tsv
- data rows: **215**
- header:
```text
section	phrase	count
```
- first persisted data rows (schema inspection only):
```text
result	пластиковые двери	27229
result	пластиковые двери входные	4482
```

## STEP_03R_S06_RAW_NORMALIZED.tsv
- data rows: **218**
- header:
```text
section	phrase	count
```
- first persisted data rows (schema inspection only):
```text
result	остекление балкона	11505
result	остекление балконов в москве	2050
```

## STEP_03R_S07_RAW_NORMALIZED.tsv
- data rows: **19**
- header:
```text
section	phrase	count
```
- first persisted data rows (schema inspection only):
```text
result	остекление балкона с крышей	48
result	остекление балкона с крышей цена	10
```

## STEP_03R_S08_RAW_NORMALIZED.tsv
- data rows: **0**
- header:
```text
section	phrase	count
```

## STEP_03R_S09_RAW_NORMALIZED.tsv
- data rows: **13**
- header:
```text
section	phrase	count
```
- first persisted data rows (schema inspection only):
```text
result	пластиковые окна в митино	63
result	ремонт пластиковых окон в митино	13
```

## STEP_03R_S10_RAW_NORMALIZED.tsv
- data rows: **192**
- header:
```text
section	phrase	count
```
- first persisted data rows (schema inspection only):
```text
result	остекление веранды	1373
result	остекление веранды и террасы	198
```

## STEP_03R_S11_RAW_NORMALIZED.tsv
- data rows: **216**
- header:
```text
section	phrase	count
```
- first persisted data rows (schema inspection only):
```text
result	алюминиевые окна	10354
result	алюминиевые раздвижные окна	1297
```

## STEP_03R_S12_RAW_NORMALIZED.tsv
- data rows: **17**
- header:
```text
section	phrase	count
```
- first persisted data rows (schema inspection only):
```text
result	аксессуары для пластиковых окон	29
result	для пластикового окна аксессуары gu	13
```

## STEP_03R_S13_RAW_NORMALIZED.tsv
- data rows: **216**
- header:
```text
section	phrase	count
```
- first persisted data rows (schema inspection only):
```text
result	установка пластиковых окон	15510
result	пластиковые окна цена с установкой	4681
```

## STEP_03R_S14_RAW_NORMALIZED.tsv
- data rows: **217**
- header:
```text
section	phrase	count
```
- first persisted data rows (schema inspection only):
```text
result	ремонт пластиковых окон	4382
result	ремонт пластиковых окон в москве	1474
```

## STEP_03R_S15_RAW_NORMALIZED.tsv
- data rows: **211**
- header:
```text
section	phrase	count
```
- first persisted data rows (schema inspection only):
```text
result	цены на пластиковые окна	2023
result	цена на пластиковые окна с установкой	378
```

## STEP_03R_S16_RAW_NORMALIZED.tsv
- data rows: **81**
- header:
```text
section	phrase	count
```
- first persisted data rows (schema inspection only):
```text
result	окна в рассрочку	507
result	пластиковые окна в рассрочку	212
```

## STEP_03R_S17_RAW_NORMALIZED.tsv
- data rows: **49**
- header:
```text
section	phrase	count
```
- first persisted data rows (schema inspection only):
```text
result	как выбрать пластиковые окна	254
result	как правильно выбрать пластиковые окна	85
```

## STEP_03R_S18_RAW_NORMALIZED.tsv
- data rows: **140**
- header:
```text
section	phrase	count
```
- first persisted data rows (schema inspection only):
```text
result	пластиковые окна от производителя	1589
result	недорогие окна пластиковые от производителя	763
```

## STEP_05_P2_01_RAW_NORMALIZED.tsv
- data rows: **217**
- header:
```text
section	phrase	count
```
- first persisted data rows (schema inspection only):
```text
result	оконная фурнитура	1459
result	оконная фурнитура для окон	193
```

## STEP_05_P2_02_RAW_NORMALIZED.tsv
- data rows: **216**
- header:
```text
section	phrase	count
```
- first persisted data rows (schema inspection only):
```text
result	панорамные окна	9273
result	дом с панорамными окнами	1103
```

## STEP_05_P2_03_RAW_NORMALIZED.tsv
- data rows: **21**
- header:
```text
section	phrase	count
```
- first persisted data rows (schema inspection only):
```text
result	остекление балкона с выносом	95
result	остекление балкона с выносом подоконника	20
```

## STEP_05_P2_04_RAW_NORMALIZED.tsv
- data rows: **96**
- header:
```text
section	phrase	count
```
- first persisted data rows (schema inspection only):
```text
result	окна для частного дома	479
result	размер окон для частного дома	196
```

## STEP_06_D1_RAW_DYNAMICS.tsv
- data rows: **24**
- header:
```text
request_id	phrase	method	period	fromDate	toDate	region	devices	date	count	share
```
- first persisted data rows (schema inspection only):
```text
wordstat-c2786f94-e5d7-45e0-b852-883c94dad9b3	пластиковые окна	getDynamics	PERIOD_MONTHLY	2024-08-01T00:00:00Z	2026-07-31T23:59:59Z	213	DEVICE_ALL	2024-08-01T00:00:00Z	177698	0.015707043487400735
wordstat-c2786f94-e5d7-45e0-b852-883c94dad9b3	пластиковые окна	getDynamics	PERIOD_MONTHLY	2024-08-01T00:00:00Z	2026-07-31T23:59:59Z	213	DEVICE_ALL	2024-09-01T00:00:00Z	201453	0.016231872574892527
```

## STEP_06_D2_RAW_DYNAMICS.tsv
- data rows: **24**
- header:
```text
date	count	share	request_id	phrase	period	region	device
```
- first persisted data rows (schema inspection only):
```text
2024-08-01T00:00:00Z	19003	0.00167970909853277	wordstat-dde1f9a7-23be-4408-ab7e-053c3f0908dd	остекление балконов	PERIOD_MONTHLY	213	DEVICE_ALL
2024-09-01T00:00:00Z	16783	0.0013522733214418315	wordstat-dde1f9a7-23be-4408-ab7e-053c3f0908dd	остекление балконов	PERIOD_MONTHLY	213	DEVICE_ALL
```

## STEP_06_D3_RAW_DYNAMICS.tsv
- data rows: **24**
- header:
```text
phrase	period	fromDate	toDate	region	device	request_id	date	count	share
```
- first persisted data rows (schema inspection only):
```text
остекление веранды	PERIOD_MONTHLY	2024-08-01T00:00:00Z	2026-07-31T23:59:59Z	213	DEVICE_ALL	wordstat-ee5a1805-6ed8-4393-b9a3-f09e2294fab5	2024-08-01T00:00:00Z	2323	0.00020533411755468216
остекление веранды	PERIOD_MONTHLY	2024-08-01T00:00:00Z	2026-07-31T23:59:59Z	213	DEVICE_ALL	wordstat-ee5a1805-6ed8-4393-b9a3-f09e2294fab5	2024-09-01T00:00:00Z	1567	0.00012625944674369004
```

## STEP_06_D4_RAW_DYNAMICS.tsv
- data rows: **24**
- header:
```text
date	count	share	phrase	request_id	period	region	device
```
- first persisted data rows (schema inspection only):
```text
2024-08-01T00:00:00Z	435	0.000038450426662198335	окна для частного дома	wordstat-98c82797-78b7-4a29-8432-56ea549d17ef	PERIOD_MONTHLY	213	DEVICE_ALL
2024-09-01T00:00:00Z	478	0.00003851436856635854	окна для частного дома	wordstat-98c82797-78b7-4a29-8432-56ea549d17ef	PERIOD_MONTHLY	213	DEVICE_ALL
```

## STEP_08_NONEXACT_DUPLICATE_HANDOFF.tsv
- data rows: **18**
- header:
```text
candidate_group	method	signature	group_size	phrase	corrected_status	corrected_reason	source_ids	step08_state	step08_member_disposition	step08_member_next_route	step08_duplicate_resolution_route
```
- first persisted data rows (schema inspection only):
```text
DUP-0001	STRICT_ORDERLESS_TOKEN_BAG	provedal алюминиевые окна	2	алюминиевые окна provedal	KEEP	POSITIVE_CORE_ALUMINIUM_WINDOW_INTENT	S11	UNRESOLVED_DUPLICATE_CANDIDATE	CORE_CANDIDATE	ORDINARY_SEARCH_ELIGIBLE	ORDINARY_SEARCH_BEFORE_ANY_NONEXACT_MERGE
DUP-0001	STRICT_ORDERLESS_TOKEN_BAG	provedal алюминиевые окна	2	алюминиевые окна проведал	KEEP	POSITIVE_CORE_ALUMINIUM_WINDOW_INTENT	S11	UNRESOLVED_DUPLICATE_CANDIDATE	CORE_CANDIDATE	ORDINARY_SEARCH_ELIGIBLE	ORDINARY_SEARCH_BEFORE_ANY_NONEXACT_MERGE
```

## STEP_08_REVIEW_RESOLUTION_ROUTES.tsv
- data rows: **1118**
- header:
```text
phrase	corrected_reason	semantic_confidence	source_occurrences	result_occurrences	association_occurrences	max_result_count	max_association_count	source_ids	provenance	search_stage_disposition	next_resolution_route	route_reason
```
- first persisted data rows (schema inspection only):
```text
6 6 с панорамными окнами	AMBIGUOUS_NUMERIC_OR_FRAGMENT_INTENT	LOW	1	1	0	31	0	P2-02	P2-02:result:31	REVIEW_SEARCH	REVIEW_SEARCH	ORDINARY_SEARCH_NEEDED_TO_RESOLVE_INTENT_RELEVANCE_OR_BOUNDARY
951 1450 оконная фурнитура	RETAINED_BUSINESS_BOUNDARY_NEEDS_SEARCH	MEDIUM	1	1	0	10	0	P2-01	P2-01:result:10	REVIEW_SEARCH	REVIEW_SEARCH	ORDINARY_SEARCH_NEEDED_TO_RESOLVE_INTENT_RELEVANCE_OR_BOUNDARY
```

## STEP_08_SEARCH_STAGE_SEMANTIC_SET.tsv
- data rows: **2840**
- header:
```text
phrase	historical_status	historical_reason	corrected_status	corrected_reason	semantic_confidence	source_occurrences	result_occurrences	association_occurrences	max_result_count	max_association_count	source_ids	provenance	search_stage_disposition	next_resolution_route	route_reason
```
- first persisted data rows (schema inspection only):
```text
1 пластиковые окна	EXCLUDE_MECHANICAL	MALFORMED_OR_TRUNCATED	EXCLUDE_MECHANICAL	RETAINED_MALFORMED_OR_TRUNCATED	HIGH	1	1	0	619	0	S01	S01:result:619	EXCLUDED_PRESERVED	NO_ACTIVE_SEARCH_ROUTE	ACCEPTED_STEP07C_EXCLUSION_PRESERVED_FOR_AUDIT
1 установка пластиковых окон	KEEP	SUPPORTED_WINDOW_OR_GLAZING_TASK	EXCLUDE_MECHANICAL	POST_AUDIT_MALFORMED_OR_FRAGMENT	HIGH	1	1	0	83	0	S13	S13:result:83	EXCLUDED_PRESERVED	NO_ACTIVE_SEARCH_ROUTE	ACCEPTED_STEP07C_EXCLUSION_PRESERVED_FOR_AUDIT
```

## STEP_09_EVIDENCE_QUESTION_DECISIONS.tsv
- data rows: **75**
- header:
```text
probe_id	query	observed_serp_job	dominant_result_type	step10_handoff	confidence	evidence_scope
```
- first persisted data rows (schema inspection only):
```text
SP09-001	аксессуары для пластиковых окон	ACCESSORY_SHOPPING	ECOMMERCE_CATEGORY_PRODUCT	BOUNDARY_ACCESSORIES_NOT_GENERIC_WINDOW_SERVICE	HIGH	DIRECT_QUERY_ONLY__NO_UNPROBED_TRANSFER
SP09-002	алюминиевые окна fapim	HARDWARE_BRAND_SHOPPING	ECOMMERCE_CATEGORY_PRODUCT	BOUNDARY_HARDWARE_BRAND	HIGH	DIRECT_QUERY_ONLY__NO_UNPROBED_TRANSFER
```

## STEP_09_REVIEW_SEARCH_COVERAGE.tsv
- data rows: **944**
- header:
```text
phrase	corrected_reason	source_ids	direct_probe_id	direct_query	coverage_state	pre_serp_transfer_allowed
```
- first persisted data rows (schema inspection only):
```text
6 6 с панорамными окнами	AMBIGUOUS_NUMERIC_OR_FRAGMENT_INTENT	P2-02			UNRESOLVED_UNPROBED	false
951 1450 оконная фурнитура	RETAINED_BUSINESS_BOUNDARY_NEEDS_SEARCH	P2-01			UNRESOLVED_UNPROBED	false
```

## STEP_09_SEARCH_PROBE_MANIFEST.tsv
- data rows: **75**
- header:
```text
probe_id	query	probe_roles	sampling_stratum_ids	sampling_stratum_row_count	corrected_reasons	source_ids	duplicate_group_ids	step1_boundary_ids	selection_basis	semantic_qa_status	pre_serp_transfer_allowed
```
- first persisted data rows (schema inspection only):
```text
SP09-001	аксессуары для пластиковых окон	REVIEW_STRATIFIED_SAMPLE	SAMPLE_RETAINED_BUSINESS_BOUNDARY_NEEDS_SEARCH__S12	5	RETAINED_BUSINESS_BOUNDARY_NEEDS_SEARCH	S12			DIVERSITY_SAMPLE_ONLY__NOT_INTENT_REPRESENTATIVE	PASS_INITIAL_TRANCHE_ONLY	false
SP09-002	алюминиевые окна fapim	REVIEW_STRATIFIED_SAMPLE	SAMPLE_HARDWARE_BRAND_INTENT_NEEDS_BUSINESS_FIT	5	HARDWARE_BRAND_INTENT_NEEDS_BUSINESS_FIT	S11			DIVERSITY_SAMPLE_ONLY__NOT_INTENT_REPRESENTATIVE	PASS_INITIAL_TRANCHE_ONLY	false
```

## STEP_09_SERP_COMPARISONS.tsv
- data rows: **8**
- header:
```text
comparison_id	group_id	query_a	query_b	top_n_a	top_n_b	exact_url_overlap	exact_url_overlap_share_of_10	dominant_job_a	dominant_job_b	step09_conclusion	step10_handoff	threshold_policy
```
- first persisted data rows (schema inspection only):
```text
CMP-0001	DUP-0001	алюминиевые окна provedal	алюминиевые окна проведал	10	10	7	0.70	PROVEDAL_ALUMINIUM_WINDOWS	PROVEDAL_ALUMINIUM_WINDOWS	STRONG_DIRECT_SERP_COMPATIBILITY	CLUSTER_TOGETHER_CANDIDATE	NO_UNIVERSAL_NUMERIC_THRESHOLD__MANUAL_INTENT_CHECK_REQUIRED
CMP-0002	DUP-0002	provedal остекление веранды	проведал остекление веранды	10	10	5	0.50	PROVEDAL_VERANDA_GLAZING	PROVEDAL_VERANDA_GLAZING	MATERIAL_DIRECT_SERP_COMPATIBILITY	CLUSTER_TOGETHER_CANDIDATE	NO_UNIVERSAL_NUMERIC_THRESHOLD__MANUAL_INTENT_CHECK_REQUIRED
```

## STEP_09_SERP_R2_PROJECTION_RAW_PART_01.tsv
- data rows: **190**
- header:
```text
query_index	query_text	item_id	region	rank	url	domain	title
```
- first persisted data rows (schema inspection only):
```text
2	алюминиевые окна fapim	kw001-okno-msk-search-step09-20260829-r2:2a5f9668f7f606c4	213	1	https://www.e-fapim.ru/okonnaya-furnitura/dlya-povorotnykh-i-otkidnykh-alyuminievykh-okon/	www.e-fapim.ru	Фурнитура для поворотных и откидных алюминиевых окон
2	алюминиевые окна fapim	kw001-okno-msk-search-step09-20260829-r2:2a5f9668f7f606c4	213	2	https://www.e-fapim.ru/okonnaya-furnitura/	www.e-fapim.ru	Оконная фурнитура в розницу и оптом. Продажа комплектующих...
```

## STEP_09_SERP_R2_PROJECTION_RAW_PART_02.tsv
- data rows: **190**
- header:
```text
query_index	query_text	item_id	region	rank	url	domain	title
```
- first persisted data rows (schema inspection only):
```text
21	остекление балконов деревянными рамами	kw001-okno-msk-search-step09-20260829-r2:c15db062493304ee	213	1	https://www.oknarosta.ru/derevyannoe-osteklenie-balkonov/	www.oknarosta.ru	Деревянное остекление балконов и лоджий – недорого...
21	остекление балконов деревянными рамами	kw001-okno-msk-search-step09-20260829-r2:c15db062493304ee	213	2	https://balconia.ru/osteklenie-balkonov-i-lodzhij-derevyannymi-ramami/	balconia.ru	Остекление балконов и лоджий деревянными окнами в Москве
```

## STEP_09_SERP_R2_PROJECTION_RAW_PART_03.tsv
- data rows: **190**
- header:
```text
query_index	query_text	item_id	region	rank	url	domain	title
```
- first persisted data rows (schema inspection only):
```text
40	шторы на пластиковые окна фото цены	kw001-okno-msk-search-step09-20260829-r2:b908213a882f68f5	213	1	https://primedecorshop.ru/catalog/rulonnaya-shtora-mini-blackout-svetootrazhayushchiy-playn-kremovyy-90kh170/	primedecorshop.ru	Рулонная штора mini blackout светоотражающий...
40	шторы на пластиковые окна фото цены	kw001-okno-msk-search-step09-20260829-r2:b908213a882f68f5	213	2	https://primedecorshop.ru/catalog/rulonnye-shtory/rulonnye-shtory-iz-tkani/?ybaip=1	primedecorshop.ru	Рулонные шторы из ткани на окна | Купить по выгодной цене на...
```

## STEP_09_SERP_R2_PROJECTION_RAW_PART_04.tsv
- data rows: **170**
- header:
```text
query_index	query_text	item_id	region	rank	url	domain	title
```
- first persisted data rows (schema inspection only):
```text
59	как выбрать пластиковые окна	kw001-okno-msk-search-step09-20260829-r2:330684f3bfee4739	213	1	https://www.ozon.ru/club/article/kak-vybrat-plastikovye-okna-osnovnye-kriterii-16303437/	www.ozon.ru	Как выбрать пластиковые окна: параметры для... — Ozon Клуб
59	как выбрать пластиковые окна	kw001-okno-msk-search-step09-20260829-r2:330684f3bfee4739	213	2	https://www.vseinstrumenti.ru/publication/kak-vybrat-plastikovye-okna-976/	www.vseinstrumenti.ru	Как выбрать пластиковые окна? – интернет-магазин...
```

## STEP_09_SERP_RESULTS.tsv
- data rows: **10**
- header:
```text
query	region	rank	url	domain	title	snippet	modtime	request_id	item_id	http_status	response_format	request_executed	estimated_cost_rub
```
- first persisted data rows (schema inspection only):
```text
аксессуары для пластиковых окон	213	1	https://www.ozon.ru/category/furnitura-dlya-plastikovyh-okon/	www.ozon.ru	Фурнитура для пластиковых окон купить на OZON по низкой цене	Фурнитура для пластиковых окон – покупайте на OZON по выгодным ценам! Быстрая и бесплатная доставка. Оригинальные товары, гарантия, бонусы, рассрочка и кэшбэк. Распродажи, скидки и акции. Огромный ассортимент.	20220707T004238	search-batch-06923ff5-1455-4ca9-99f3-d8778976c96a	kw001-okno-msk-search-step09-20260829:ca2ccadf3fb1cddc	200	FORMAT_XML	true	0.488
аксессуары для пластиковых окон	213	2	https://online-shop.rhsolutions.ru/products/ruchka-okonnaya-rehau-camea-dlya-plastikovyh-okon-dlya-balkonnoiy-dveri-antracit-temno-seraya-6-391160	online-shop.rhsolutions.ru	Ручка оконная рехау CAMEA, античное золото	Аксессуар для окон по индивидуальным размерам. … Ручка оконная РЕХАУ MEDEA для пластиковых окон / для балконной двери, черная, шрифт 40мм.	20260206T103327	search-batch-06923ff5-1455-4ca9-99f3-d8778976c96a	kw001-okno-msk-search-step09-20260829:ca2ccadf3fb1cddc	200	FORMAT_XML	true	0.488
```

## STEP_11_SEARCH_PROJECTION_RECOVERY_01_000_019_2026-08-30.tsv
- data rows: **200**
- header:
```text
QUERY_ORDINAL	QUERY_TEXT	REGION	RANK	URL	DOMAIN	TITLE	TARGET_DOMAIN_IN_OBSERVED_TOP10
```
- first persisted data rows (schema inspection only):
```text
1	окна москва купить	213	1	https://www.okna-moskva.ru/series/	www.okna-moskva.ru	Пластиковые окна в квартиру: цены на окна ПВХ по типам домов...	false
1	окна москва купить	213	2	https://www.mosokna.ru/plastikovye-okna/vidy-okon/dvuhstvorchatoe-okno	www.mosokna.ru	Двустворчатые пластиковые окна с установкой — купить...	false
```
