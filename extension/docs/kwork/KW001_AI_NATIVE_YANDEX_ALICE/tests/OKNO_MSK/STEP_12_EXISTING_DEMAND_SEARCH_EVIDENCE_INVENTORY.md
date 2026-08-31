# Step 12 correction — existing demand/Search evidence inventory

Purpose: identify already persisted demand and ordinary-Search evidence before considering any new provider call for D12-03/D12-10.

This inventory reports file names/schema/counts only. It does not assume what a field means until its producing step/method provenance is checked.

| File | Type | Rows | Size | Header / JSON keys | Note |
|---|---|---:|---:|---|---|
| `STEP_03R_BATCH_START_CHECKPOINT.md` | .md |  | 1714 |  | markdown; chars=1712 |
| `STEP_03R_BATCH_START_RAW.json` | .json |  | 2118 | bridge / version / service / operation / job_id / run_id / status / reason / command / progress / item / provider_result / cost_estimate / policy / request_executed / automatic_retry |  |
| `STEP_03R_FINAL_RECONCILIATION_2026-08-29.md` | .md |  | 3906 |  | markdown; chars=3903 |
| `STEP_03R_S01_CHECKPOINT_2026-08-29.md` | .md |  | 2468 |  | markdown; chars=2436 |
| `STEP_03R_S01_DELIVERY_LITERAL_METADATA_2026-08-29.md` | .md |  | 1494 |  | markdown; chars=1492 |
| `STEP_03R_S01_RAW_NORMALIZED.tsv` | .tsv | 231 | 14829 | # KW-001 / OKNO-MSK — STEP 03R S01 COMPLETE NORMALIZED PROVIDER ROWS |  |
| `STEP_03R_S01_RAW_PROVIDER_RESULT_2026-08-29.json` | .json |  | 20217 | bridge / version / service / operation / request_id / run_id / job_id / status / reason / cost_estimate / policy / command / http_status / elapsed_ms / result / request_executed / automatic_retry |  |
| `STEP_03R_S01_S09_TSV_REPAIR_AUDIT_2026-08-29.md` | .md |  | 5351 |  | markdown; chars=5181 |
| `STEP_03R_S02_CHECKPOINT_2026-08-29.md` | .md |  | 2353 |  | markdown; chars=2343 |
| `STEP_03R_S02_RAW_NORMALIZED.tsv` | .tsv | 233 | 12058 | # KW-001 / OKNO-MSK — STEP 03R S02 COMPLETE NORMALIZED PROVIDER ROWS |  |
| `STEP_03R_S02_RAW_PROVIDER_RESULT_2026-08-29.json` | .json |  | 17544 | bridge / version / service / operation / request_id / run_id / job_id / status / reason / cost_estimate / policy / command / http_status / elapsed_ms / result / request_executed / automatic_retry |  |
| `STEP_03R_S03_CHECKPOINT_2026-08-29.md` | .md |  | 2268 |  | markdown; chars=2236 |
| `STEP_03R_S03_RAW_NORMALIZED.tsv` | .tsv | 157 | 9835 | # KW-001 / OKNO-MSK — STEP 03R S03 COMPLETE NORMALIZED PROVIDER ROWS |  |
| `STEP_03R_S03_RAW_PROVIDER_RESULT_2026-08-29.json` | .json |  | 13597 | bridge / version / service / operation / request_id / run_id / job_id / status / reason / cost_estimate / policy / command / http_status / elapsed_ms / result / request_executed / automatic_retry |  |
| `STEP_03R_S04_CHECKPOINT_2026-08-29.md` | .md |  | 2000 |  | markdown; chars=1988 |
| `STEP_03R_S04_RAW_NORMALIZED.tsv` | .tsv | 42 | 1941 | # KW-001 / OKNO-MSK — STEP 03R S04 COMPLETE NORMALIZED PROVIDER ROWS |  |
| `STEP_03R_S04_RAW_PROVIDER_RESULT_2026-08-29.json` | .json |  | 3049 | bridge / version / service / operation / request_id / run_id / job_id / status / reason / cost_estimate / policy / command / http_status / elapsed_ms / result / request_executed / automatic_retry |  |
| `STEP_03R_S05_CHECKPOINT_2026-08-29.md` | .md |  | 1830 |  | markdown; chars=1796 |
| `STEP_03R_S05_RAW_NORMALIZED.tsv` | .tsv | 228 | 15242 | # KW-001 / OKNO-MSK — STEP 03R S05 COMPLETE NORMALIZED PROVIDER ROWS |  |
| `STEP_03R_S05_RAW_PROVIDER_RESULT_2026-08-29.json` | .json |  | 20638 | bridge / version / service / operation / request_id / run_id / job_id / status / reason / cost_estimate / policy / command / http_status / elapsed_ms / result / request_executed / automatic_retry |  |
| `STEP_03R_S06_CHECKPOINT_2026-08-29.md` | .md |  | 1922 |  | markdown; chars=1884 |
| `STEP_03R_S06_RAW_NORMALIZED.tsv` | .tsv | 231 | 15645 | # KW-001 / OKNO-MSK — STEP 03R S06 COMPLETE NORMALIZED PROVIDER ROWS |  |
| `STEP_03R_S06_RAW_PROVIDER_RESULT_2026-08-29.json` | .json |  | 21095 | bridge / version / service / operation / request_id / run_id / job_id / status / reason / cost_estimate / policy / command / http_status / elapsed_ms / result / request_executed / automatic_retry |  |
| `STEP_03R_S07_CHECKPOINT_2026-08-29.md` | .md |  | 1241 |  | markdown; chars=1215 |
| `STEP_03R_S07_RAW_NORMALIZED.tsv` | .tsv | 32 | 1720 | # KW-001 / OKNO-MSK — STEP 03R S07 COMPLETE NORMALIZED PROVIDER ROWS |  |
| `STEP_03R_S07_RAW_PROVIDER_RESULT_2026-08-29.json` | .json |  | 2618 | bridge / version / service / operation / request_id / run_id / job_id / status / reason / cost_estimate / policy / command / http_status / elapsed_ms / result / request_executed / automatic_retry |  |
| `STEP_03R_S08_CHECKPOINT_2026-08-29.md` | .md |  | 1839 |  | markdown; chars=1819 |
| `STEP_03R_S08_RAW_NORMALIZED.tsv` | .tsv | 16 | 531 | # KW-001 / OKNO-MSK — STEP 03R S08 COMPLETE NORMALIZED PROVIDER ROWS |  |
| `STEP_03R_S08_RAW_PROVIDER_RESULT_2026-08-29.json` | .json |  | 958 | bridge / version / service / operation / request_id / run_id / job_id / status / reason / cost_estimate / policy / command / http_status / elapsed_ms / result / request_executed / automatic_retry |  |
| `STEP_03R_S09_CHECKPOINT_2026-08-29.md` | .md |  | 2869 |  | markdown; chars=2846 |
| `STEP_03R_S09_RAW_NORMALIZED.tsv` | .tsv | 26 | 1431 | # KW-001 / OKNO-MSK — STEP 03R S09 COMPLETE NORMALIZED PROVIDER ROWS |  |
| `STEP_03R_S09_RAW_PROVIDER_RESULT_2026-08-29.json` | .json |  | 2581 | bridge / version / service / operation / request_id / run_id / job_id / status / reason / cost_estimate / policy / command / http_status / elapsed_ms / result / request_executed / automatic_retry |  |
| `STEP_03R_S10_CHECKPOINT_2026-08-29.md` | .md |  | 2623 |  | markdown; chars=2498 |
| `STEP_03R_S10_RAW_NORMALIZED.tsv` | .tsv | 205 | 14450 | # KW-001 / OKNO-MSK — STEP 03R S10 COMPLETE NORMALIZED PROVIDER ROWS |  |
| `STEP_03R_S10_RAW_PROVIDER_RESULT_2026-08-29.json` | .json |  | 19243 | bridge / version / service / operation / request_id / run_id / job_id / status / reason / cost_estimate / policy / command / http_status / elapsed_ms / result / request_executed / automatic_retry |  |
| `STEP_03R_S11_CHECKPOINT_2026-08-29.md` | .md |  | 2993 |  | markdown; chars=2857 |
| `STEP_03R_S11_PRE_PROVIDER_FAILURE_2026-08-29.md` | .md |  | 1872 |  | markdown; chars=1801 |
| `STEP_03R_S11_RAW_NORMALIZED.tsv` | .tsv | 229 | 14792 | # KW-001 / OKNO-MSK — STEP 03R S11 COMPLETE NORMALIZED PROVIDER ROWS |  |
| `STEP_03R_S11_RAW_PROVIDER_RESULT_2026-08-29.json` | .json |  | 20170 | bridge / version / service / operation / request_id / run_id / job_id / status / reason / cost_estimate / policy / command / http_status / elapsed_ms / result / request_executed / automatic_retry |  |
| `STEP_03R_S12_CHECKPOINT_2026-08-29.md` | .md |  | 2106 |  | markdown; chars=2040 |
| `STEP_03R_S12_RAW_NORMALIZED.tsv` | .tsv | 30 | 1645 | # KW-001 / OKNO-MSK — STEP 03R S12 COMPLETE NORMALIZED PROVIDER ROWS |  |
| `STEP_03R_S12_RAW_PROVIDER_RESULT_2026-08-29.json` | .json |  | 2497 | bridge / version / service / operation / request_id / run_id / job_id / status / reason / cost_estimate / policy / command / http_status / elapsed_ms / result / request_executed / automatic_retry |  |
| `STEP_03R_S13_CHECKPOINT_2026-08-29.md` | .md |  | 2446 |  | markdown; chars=2342 |
| `STEP_03R_S13_RAW_NORMALIZED.tsv` | .tsv | 229 | 18941 | # KW-001 / OKNO-MSK — STEP 03R S13 COMPLETE NORMALIZED PROVIDER ROWS |  |
| `STEP_03R_S13_RAW_PROVIDER_RESULT_2026-08-29.json` | .json |  | 24308 | bridge / version / service / operation / request_id / run_id / job_id / status / reason / cost_estimate / policy / command / http_status / elapsed_ms / result / request_executed / automatic_retry |  |
| `STEP_03R_S14_CHECKPOINT_2026-08-29.md` | .md |  | 2408 |  | markdown; chars=2294 |
| `STEP_03R_S14_RAW_NORMALIZED.tsv` | .tsv | 230 | 17086 | # KW-001 / OKNO-MSK — STEP 03R S14 COMPLETE NORMALIZED PROVIDER ROWS |  |
| `STEP_03R_S14_RAW_PROVIDER_RESULT_2026-08-29.json` | .json |  | 20830 | bridge / version / service / operation / request_id / run_id / job_id / status / reason / cost_estimate / policy / command / http_status / elapsed_ms / result / request_executed / automatic_retry |  |
| `STEP_03R_S15_CHECKPOINT_2026-08-29.md` | .md |  | 2529 |  | markdown; chars=2407 |
| `STEP_03R_S15_RAW_NORMALIZED.tsv` | .tsv | 224 | 16994 | # KW-001 / OKNO-MSK — STEP 03R S15 COMPLETE NORMALIZED PROVIDER ROWS |  |
| `STEP_03R_S15_RAW_PROVIDER_RESULT_2026-08-29.json` | .json |  | 20672 | bridge / version / service / operation / request_id / run_id / job_id / status / reason / cost_estimate / policy / command / http_status / elapsed_ms / result / request_executed / automatic_retry |  |
| `STEP_03R_S16_CHECKPOINT_2026-08-29.md` | .md |  | 2393 |  | markdown; chars=2297 |
| `STEP_03R_S16_RAW_NORMALIZED.tsv` | .tsv | 94 | 5600 | # KW-001 / OKNO-MSK — STEP 03R S16 COMPLETE NORMALIZED PROVIDER ROWS |  |
| `STEP_03R_S16_RAW_PROVIDER_RESULT_2026-08-29.json` | .json |  | 7187 | bridge / version / service / operation / request_id / run_id / job_id / status / reason / cost_estimate / policy / command / http_status / elapsed_ms / result / request_executed / automatic_retry |  |
| `STEP_03R_S17_CHECKPOINT_2026-08-29.md` | .md |  | 1945 |  | markdown; chars=1888 |
| `STEP_03R_S17_RAW_NORMALIZED.tsv` | .tsv | 62 | 4178 | # KW-001 / OKNO-MSK — STEP 03R S17 COMPLETE NORMALIZED PROVIDER ROWS |  |
| `STEP_03R_S17_RAW_PROVIDER_RESULT_2026-08-29.json` | .json |  | 5234 | bridge / version / service / operation / request_id / run_id / job_id / status / reason / cost_estimate / policy / command / http_status / elapsed_ms / result / request_executed / automatic_retry |  |
| `STEP_03R_S18_CHECKPOINT_2026-08-29.md` | .md |  | 2600 |  | markdown; chars=2489 |
| `STEP_03R_S18_RAW_NORMALIZED.tsv` | .tsv | 153 | 13461 | # KW-001 / OKNO-MSK — STEP 03R S18 COMPLETE NORMALIZED PROVIDER ROWS |  |
| `STEP_03R_S18_RAW_PROVIDER_RESULT_2026-08-29.json` | .json |  | 15973 | bridge / version / service / operation / request_id / run_id / job_id / status / reason / cost_estimate / policy / command / http_status / elapsed_ms / result / request_executed / automatic_retry |  |
| `STEP_03R_WORDSTAT_REPAIR_MANIFEST_2026-08-29.md` | .md |  | 7979 |  | markdown; chars=7632 |
| `STEP_03_ACCEPTANCE.md` | .md |  | 4414 |  | markdown; chars=4335 |
| `STEP_03_CHECKPOINT_S07.md` | .md |  | 1736 |  | markdown; chars=1489 |
| `STEP_03_CHECKPOINT_S08.md` | .md |  | 1733 |  | markdown; chars=1693 |
| `STEP_03_CHECKPOINT_S11.md` | .md |  | 2124 |  | markdown; chars=1864 |
| `STEP_03_CHECKPOINT_S12.md` | .md |  | 1618 |  | markdown; chars=1436 |
| `STEP_03_COMPLETION_CORRECTION_2026-08-29.md` | .md |  | 3524 |  | markdown; chars=3518 |
| `STEP_03_ITEM_S06_CHECKPOINT.md` | .md |  | 2576 |  | markdown; chars=2314 |
| `STEP_03_S10_CHECKPOINT.md` | .md |  | 1865 |  | markdown; chars=1598 |
| `STEP_03_S13_CHECKPOINT.md` | .md |  | 1284 |  | markdown; chars=1248 |
| `STEP_03_S14_CHECKPOINT.md` | .md |  | 1192 |  | markdown; chars=1171 |
| `STEP_03_WORDSTAT_PASS1_CHECKPOINT_05.md` | .md |  | 2074 |  | markdown; chars=1805 |
| `STEP_03_WORDSTAT_PASS1_CHECKPOINT_S09.md` | .md |  | 1790 |  | markdown; chars=1667 |
| `STEP_03_WORDSTAT_PASS1_EXECUTION_LOG.md` | .md |  | 10768 |  | markdown; chars=9995 |
| `STEP_03_WORDSTAT_PASS1_PREFLIGHT.md` | .md |  | 7001 |  | markdown; chars=6335 |
| `STEP_03_WORDSTAT_PASS1_S15_CHECKPOINT.md` | .md |  | 2202 |  | markdown; chars=1966 |
| `STEP_03_WORDSTAT_PASS1_S16_CHECKPOINT.md` | .md |  | 2080 |  | markdown; chars=1918 |
| `STEP_03_WORDSTAT_PASS1_S17_CHECKPOINT.md` | .md |  | 2371 |  | markdown; chars=2094 |
| `STEP_03_WORDSTAT_PASS1_S18_CHECKPOINT.md` | .md |  | 2682 |  | markdown; chars=2394 |
| `STEP_04A_WORDSTAT_COVERAGE_AND_EXPANSION_REVALIDATION_2026-08-29.md` | .md |  | 10773 |  | markdown; chars=10236 |
| `STEP_04_ACCEPTANCE.md` | .md |  | 3899 |  | markdown; chars=3701 |
| `STEP_04_METHOD_REVIEW_CORRECTION.md` | .md |  | 4827 |  | markdown; chars=4605 |
| `STEP_04_PROGRESSIVE_CLEANUP_1.md` | .md |  | 19633 |  | markdown; chars=18758 |
| `STEP_05_ACCEPTANCE.md` | .md |  | 8652 |  | markdown; chars=8444 |
| `STEP_05_EXECUTION_LOG.md` | .md |  | 1785 |  | markdown; chars=1635 |
| `STEP_05_FINAL_BATCH_STATUS.md` | .md |  | 1309 |  | markdown; chars=1233 |
| `STEP_05_P2_01_CHECKPOINT.md` | .md |  | 2700 |  | markdown; chars=2359 |
| `STEP_05_P2_01_RAW_NORMALIZED.tsv` | .tsv | 230 | 14399 | # KW-001 / OKNO-MSK — STEP 05 P2-01 COMPLETE NORMALIZED PROVIDER ROWS |  |
| `STEP_05_P2_02_CHECKPOINT.md` | .md |  | 2658 |  | markdown; chars=2177 |
| `STEP_05_P2_02_RAW_NORMALIZED.tsv` | .tsv | 229 | 14499 | # KW-001 / OKNO-MSK — STEP 05 P2-02 COMPLETE NORMALIZED PROVIDER ROWS |  |
| `STEP_05_P2_03_CHECKPOINT.md` | .md |  | 1646 |  | markdown; chars=1456 |
| `STEP_05_P2_03_RAW_NORMALIZED.tsv` | .tsv | 34 | 1982 | # KW-001 / OKNO-MSK — STEP 05 P2-03 COMPLETE NORMALIZED PROVIDER ROWS |  |
| `STEP_05_P2_04_RAW_NORMALIZED.tsv` | .tsv | 109 | 7549 | # KW-001 / OKNO-MSK — STEP 05 P2-04 COMPLETE NORMALIZED PROVIDER ROWS |  |
| `STEP_05_PRE_STEP_REVIEW.md` | .md |  | 9584 |  | markdown; chars=9087 |
| `STEP_05_WORDSTAT_PASS2_MANIFEST.md` | .md |  | 4517 |  | markdown; chars=4241 |
| `STEP_05_WORDSTAT_PASS2_P2_04_CHECKPOINT.md` | .md |  | 3394 |  | markdown; chars=2819 |
| `STEP_06_ACCEPTANCE.md` | .md |  | 4746 |  | markdown; chars=4606 |
| `STEP_06_D1_CHECKPOINT.md` | .md |  | 2114 |  | markdown; chars=2097 |
| `STEP_06_D1_RAW_DYNAMICS.tsv` | .tsv | 24 | 5136 | request_id / phrase / method / period / fromDate / toDate / region / devices / date / count / share |  |
| `STEP_06_D2_CHECKPOINT.md` | .md |  | 2076 |  | markdown; chars=2056 |
| `STEP_06_D2_DELIVERY_INCIDENT.md` | .md |  | 1402 |  | markdown; chars=1351 |
| `STEP_06_D2_RAW_DYNAMICS.tsv` | .tsv | 24 | 3957 | date / count / share / request_id / phrase / period / region / device |  |
| `STEP_06_D3_CHECKPOINT.md` | .md |  | 1550 |  | markdown; chars=1529 |
| `STEP_06_D3_RAW_DYNAMICS.tsv` | .tsv | 24 | 4935 | phrase / period / fromDate / toDate / region / device / request_id / date / count / share |  |
| `STEP_06_D4_CHECKPOINT.md` | .md |  | 2079 |  | markdown; chars=2052 |
| `STEP_06_D4_RAW_DYNAMICS.tsv` | .tsv | 24 | 4052 | date / count / share / phrase / request_id / period / region / device |  |
| `STEP_06_DYNAMICS_MANIFEST.md` | .md |  | 2996 |  | markdown; chars=2866 |
| `STEP_06_DYNAMICS_SYNTHESIS.md` | .md |  | 3768 |  | markdown; chars=3614 |
| `STEP_06_PRE_STEP_REVIEW.md` | .md |  | 10508 |  | markdown; chars=10281 |
| `STEP_08_METHOD_POSTMORTEM_AND_CORRECTION_2026-08-29.md` | .md |  | 6820 |  | markdown; chars=6796 |
| `STEP_08_NONEXACT_DUPLICATE_HANDOFF.tsv` | .tsv | 18 | 5483 | candidate_group / method / signature / group_size / phrase / corrected_status / corrected_reason / source_ids / step08_state / step08_member_disposition / step08_member_next_route / step08_duplicate_resolution_route |  |
| `STEP_08_REVIEW_RESOLUTION_ROUTES.tsv` | .tsv | 1118 | 259837 | phrase / corrected_reason / semantic_confidence / source_occurrences / result_occurrences / association_occurrences / max_result_count / max_association_count / source_ids / provenance / search_stage_disposition / next_resolution_route / route_reason |  |
| `STEP_08_SEARCH_STAGE_FREEZE_ACCEPTANCE_2026-08-29.md` | .md |  | 6793 |  | markdown; chars=6789 |
| `STEP_08_SEARCH_STAGE_FREEZE_BUILD.py` | .py |  | 12671 |  |  |
| `STEP_08_SEARCH_STAGE_FREEZE_PRE_STEP_REVIEW_2026-08-29.md` | .md |  | 12020 |  | markdown; chars=11603 |
| `STEP_08_SEARCH_STAGE_FREEZE_RECONCILIATION.md` | .md |  | 3332 |  | markdown; chars=3330 |
| `STEP_08_SEARCH_STAGE_SEMANTIC_SET.tsv` | .tsv | 2840 | 761344 | phrase / historical_status / historical_reason / corrected_status / corrected_reason / semantic_confidence / source_occurrences / result_occurrences / association_occurrences / max_result_count / max_association_count / source_ids / provenance / search_stage_disposition / next_resolution_route / route_reason |  |
| `STEP_09_COLLECTION_METHOD_AND_IMMEDIATE_PERSISTENCE_POSTMORTEM_2026-08-29.md` | .md |  | 10172 |  | markdown; chars=10142 |
| `STEP_09_CURRENT_STATE_AND_EXECUTION_PROTOCOL_2026-08-29.md` | .md |  | 11111 |  | markdown; chars=11077 |
| `STEP_09_EVIDENCE_QUESTION_DECISIONS.tsv` | .tsv | 75 | 13202 | probe_id / query / observed_serp_job / dominant_result_type / step10_handoff / confidence / evidence_scope |  |
| `STEP_09_INITIAL_TRANCHE_SEMANTIC_QA.json` | .json |  | 2567 | date / authority_sync_revision / status / reviewed_probe_count / ordered_query_list_sha256 / roles / pre_serp_transfer_allowed / nonprobed_review_search_state / full_944_serp_coverage_claim_allowed / provider_execution_scope / manual_semantic_review_notes |  |
| `STEP_09_LIVE_CANARY_AND_BATCH_EXECUTION_CORRECTION_2026-08-29.md` | .md |  | 12012 |  | markdown; chars=11891 |
| `STEP_09_LIVE_R2_PROJECTION_RECEIPT_2026-08-29.md` | .md |  | 6435 |  | markdown; chars=5920 |
| `STEP_09_METHOD_POSTMORTEM_AND_CORRECTION_2026-08-29.md` | .md |  | 15511 |  | markdown; chars=15422 |
| `STEP_09_NEXTN_LIVE_CHUNK_VALIDATION_2026-08-29.md` | .md |  | 3445 |  | markdown; chars=3443 |
| `STEP_09_ORDINARY_YANDEX_SEARCH_PRE_STEP_REVIEW_2026-08-29.md` | .md |  | 21964 |  | markdown; chars=21282 |
| `STEP_09_REVIEW_SEARCH_COVERAGE.tsv` | .tsv | 944 | 131869 | phrase / corrected_reason / source_ids / direct_probe_id / direct_query / coverage_state / pre_serp_transfer_allowed |  |
| `STEP_09_SEARCH_ACCEPTANCE_2026-08-29.md` | .md |  | 9231 |  | markdown; chars=9225 |
| `STEP_09_SEARCH_BATCH_START_COMMAND.txt` | .txt |  | 4605 |  |  |
| `STEP_09_SEARCH_PROBE_MANIFEST.tsv` | .tsv | 75 | 17883 | probe_id / query / probe_roles / sampling_stratum_ids / sampling_stratum_row_count / corrected_reasons / source_ids / duplicate_group_ids / step1_boundary_ids / selection_basis / semantic_qa_status / pre_serp_transfer_allowed |  |
| `STEP_09_SEARCH_PROBE_MANIFEST_BUILD.py` | .py |  | 16717 |  |  |
| `STEP_09_SEARCH_PROBE_MANIFEST_QA.json` | .json |  | 2260 | status / review_search_rows / review_search_reasons / review_search_reason_counts / review_sampling_strata_count / active_duplicate_groups / probe_count / direct_review_search_rows / unresolved_unprobed_review_search_rows / traceability_rows / traceability_complete / full_serp_evidence_coverage / pre_serp_transfer_links / semantic_sample_qa_pass / ordered_query_list_sha256 / max_requests_ceiling / unit_cost_rub / estimated_cost_rub / max_cost_rub / request_cap_ok / budget_cap_ok / provider_execution_allowed / provider_execution_scope / provider_requests_executed_during_build / provider_cost_rub_during_build / region |  |
| `STEP_09_SEARCH_PROBE_MANIFEST_RECONCILIATION.md` | .md |  | 1664 |  | markdown; chars=1662 |
| `STEP_09_SEARCH_RECONCILIATION.md` | .md |  | 9349 |  | markdown; chars=9347 |
| `STEP_09_SERP_COMPARISONS.tsv` | .tsv | 8 | 2730 | comparison_id / group_id / query_a / query_b / top_n_a / top_n_b / exact_url_overlap / exact_url_overlap_share_of_10 / dominant_job_a / dominant_job_b / step09_conclusion / step10_handoff / threshold_policy |  |
| `STEP_09_SERP_R2_PROJECTION_INDEX.md` | .md |  | 3935 |  | markdown; chars=3893 |
| `STEP_09_SERP_R2_PROJECTION_RAW_PART_01.tsv` | .tsv | 190 | 58126 | query_index / query_text / item_id / region / rank / url / domain / title |  |
| `STEP_09_SERP_R2_PROJECTION_RAW_PART_02.tsv` | .tsv | 190 | 61923 | query_index / query_text / item_id / region / rank / url / domain / title |  |
| `STEP_09_SERP_R2_PROJECTION_RAW_PART_03.tsv` | .tsv | 190 | 58967 | query_index / query_text / item_id / region / rank / url / domain / title |  |
| `STEP_09_SERP_R2_PROJECTION_RAW_PART_04.tsv` | .tsv | 170 | 49240 | query_index / query_text / item_id / region / rank / url / domain / title |  |
| `STEP_09_SERP_RESULTS.tsv` | .tsv | 10 | 9458 | query / region / rank / url / domain / title / snippet / modtime / request_id / item_id / http_status / response_format / request_executed / estimated_cost_rub |  |
| `STEP_10_USER_TASK_SERP_CLUSTERING_BUILD.py` | .py |  | 35808 |  |  |
| `STEP_10_USER_TASK_SERP_CLUSTERING_PRE_STEP_REVIEW_2026-08-29.md` | .md |  | 19663 |  | markdown; chars=19572 |
| `STEP_10_USER_TASK_SERP_CLUSTERING_RUN.py` | .py |  | 18633 |  |  |
| `STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V10.py` | .py |  | 6943 |  |  |
| `STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V11.py` | .py |  | 4850 |  |  |
| `STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V12.py` | .py |  | 2600 |  |  |
| `STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V13.py` | .py |  | 3172 |  |  |
| `STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V14.py` | .py |  | 3451 |  |  |
| `STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V15.py` | .py |  | 23295 |  |  |
| `STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V16.py` | .py |  | 1888 |  |  |
| `STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V17.py` | .py |  | 3211 |  |  |
| `STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V18.py` | .py |  | 3063 |  |  |
| `STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V19.py` | .py |  | 9417 |  |  |
| `STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V2.py` | .py |  | 978 |  |  |
| `STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V20.py` | .py |  | 19692 |  |  |
| `STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V21.py` | .py |  | 1622 |  |  |
| `STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V22.py` | .py |  | 1132 |  |  |
| `STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V23.py` | .py |  | 6951 |  |  |
| `STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V24.py` | .py |  | 3318 |  |  |
| `STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V25.py` | .py |  | 4010 |  |  |
| `STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V26.py` | .py |  | 2711 |  |  |
| `STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V27.py` | .py |  | 10073 |  |  |
| `STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V28.py` | .py |  | 19853 |  |  |
| `STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V29.py` | .py |  | 14734 |  |  |
| `STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V3.py` | .py |  | 11937 |  |  |
| `STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V30.py` | .py |  | 1717 |  |  |
| `STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V31.py` | .py |  | 3536 |  |  |
| `STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V32.py` | .py |  | 1014 |  |  |
| `STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V33.py` | .py |  | 1996 |  |  |
| `STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V34.py` | .py |  | 25689 |  |  |
| `STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V35.py` | .py |  | 1185 |  |  |
| `STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V36.py` | .py |  | 1468 |  |  |
| `STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V38.py` | .py |  | 12210 |  |  |
| `STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V39.py` | .py |  | 7153 |  |  |
| `STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V4.py` | .py |  | 7974 |  |  |
| `STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V5.py` | .py |  | 4256 |  |  |
| `STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V6.py` | .py |  | 5748 |  |  |
| `STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V7.py` | .py |  | 4728 |  |  |
| `STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V8.py` | .py |  | 2688 |  |  |
| `STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V9.py` | .py |  | 14082 |  |  |
| `STEP_11_SEARCH_BATCH_CHUNK_002_CHECKPOINT_2026-08-30.json` | .json |  | 3899 | observed_at / job_id / bridge_reported_version / operation / requested_count / attempted_steps / confirmed_provider_executions / provider_execution_count_exact / stopped_early / progress_after_chunk / chunk_queries / target_domain_top10_hits_in_chunk / interpretation_boundary |  |
| `STEP_11_SEARCH_BATCH_CHUNK_003_CHECKPOINT_2026-08-30.json` | .json |  | 4094 | observed_at / job_id / bridge_reported_version / operation / requested_count / attempted_steps / confirmed_provider_executions / provider_execution_count_exact / stopped_early / progress_after_chunk / chunk_queries / target_domain_top10_hits_in_chunk / interpretation_boundary |  |
| `STEP_11_SEARCH_BATCH_CHUNK_004_CHECKPOINT_2026-08-30.json` | .json |  | 4169 | observed_at / job_id / bridge_reported_version / operation / requested_count / attempted_steps / confirmed_provider_executions / provider_execution_count_exact / stopped_early / progress_after_chunk / chunk_queries / target_domain_top10_hits_in_chunk / interpretation_boundary |  |
| `STEP_11_SEARCH_BATCH_CHUNK_005_CHECKPOINT_2026-08-30.json` | .json |  | 4034 | observed_at / job_id / bridge_reported_version / operation / requested_count / attempted_steps / confirmed_provider_executions / provider_execution_count_exact / stopped_early / progress_after_chunk / chunk_queries / target_domain_top10_hits_in_chunk / interpretation_boundary |  |
| `STEP_11_SEARCH_BATCH_CHUNK_006_CHECKPOINT_2026-08-30.json` | .json |  | 4187 | observed_at / job_id / bridge_reported_version / operation / requested_count / attempted_steps / confirmed_provider_executions / provider_execution_count_exact / stopped_early / progress_after_chunk / chunk_queries / target_domain_top10_hits_in_chunk / interpretation_boundary |  |
| `STEP_11_SEARCH_BATCH_CHUNK_007_FINAL_CHECKPOINT_2026-08-30.json` | .json |  | 3536 | observed_at / job_id / bridge_reported_version / operation / requested_count / attempted_steps / confirmed_provider_executions / provider_execution_count_exact / stopped_early / progress_after_chunk / chunk_queries / target_domain_top10_hits_in_chunk / batch_target_domain_top10_hits_observed / interpretation_boundary |  |
| `STEP_11_SEARCH_BATCH_CHUNK_01_RECEIPT_2026-08-30.json` | .json |  | 2897 | observed_at / bridge_reported_version / job_id / operation / requested_count / attempted_steps / confirmed_provider_executions / provider_execution_count_exact / status / progress_after_chunk / queries / target_domain / target_domain_top10_query_hits / interpretation_boundary |  |
| `STEP_11_SEARCH_BATCH_FINAL_RECONCILIATION_2026-08-30.json` | .json |  | 1428 | observed_at / target_domain / region / batch_job_id / bridge_reported_version / canary / batch / fresh_search_total / provider_accounting_reconciles / request_count_reconciles / cost_reconciles / interpretation_boundary |  |
| `STEP_11_SEARCH_BATCH_START_RECEIPT_2026-08-30.json` | .json |  | 5231 | observed_at / bridge_reported_version / service / operation / job_id / status / request_executed / automatic_retry / command / progress / policy / interpretation_boundary |  |
| `STEP_11_SEARCH_CANARY_2026-08-30.json` | .json |  | 2691 | observed_at / bridge_reported_version / service / operation / request_id / query / region / http_status / request_executed / estimated_cost_rub / result_count / target_domain / target_domain_in_top10 / results / interpretation_boundary |  |
| `STEP_11_SEARCH_PROJECTION_RAW_02_020_067_2026-08-30.txt` | .txt |  | 117633 |  |  |
| `STEP_11_SEARCH_PROJECTION_RECOVERY_01_000_019_2026-08-30.tsv` | .tsv | 211 | 45778 | QUERY_ORDINAL / QUERY_TEXT / REGION / RANK / URL / DOMAIN / TITLE / TARGET_DOMAIN_IN_OBSERVED_TOP10 |  |
| `STEP_11_SEARCH_PROJECTION_RECOVERY_RECONCILIATION_2026-08-30.json` | .json |  | 2298 | observed_at / job_id / target_domain / region / bridge_reported_version / batch_execution / projection_recovery / fresh_search_with_canary / interpretation_boundary |  |
| `STEP_11_SEARCH_RAW_CAPTURE_GAP_AND_RECOVERY_2026-08-30.md` | .md |  | 3133 |  | markdown; chars=3130 |
| `STEP_11_SEARCH_RAW_PROVIDER_CHUNK_007_2026-08-30.json` | .json |  | 59360 | source / observed_at / bridge_reported_version / service / operation / job_id / chunk_requested_count / chunk_attempted_steps / confirmed_provider_executions / progress_after_chunk / items / interpretation_boundary |  |
| `STEP_11_UNCLUSTERED_SEARCH_REQUIRED_HANDOFF.tsv` | .tsv | 13 | 4121 | QUERY / OBSERVED_TASK / LIKELY_EXISTING_CLUSTER / RESOLUTION_STATUS / DIRECT_SEARCH_SIGNAL / OWNERSHIP_APPLICABILITY |  |
| `STEP_11_WEBMASTER_BRIDGE_PROBE_2026-08-30.md` | .md |  | 2124 |  | markdown; chars=2120 |
| `STEP_12_SEARCH_REQUIRED_HANDOFF.tsv` | .tsv | 19 | 2636 | phrase / original_assignment_status / original_cluster_id / structural_action / target_url / reason |  |
| `STEP_12_SEARCH_REQUIRED_INPUT.md` | .md |  | 2021 |  | markdown; chars=1626 |
| `step12_discover_existing_demand_search_evidence.py` | .py |  | 2418 |  |  |

candidate_files = 201

Next: inspect the producing-step authority for promising files before using any frequency/result field as demand or Search evidence.
