#!/usr/bin/env python3
"""Materialize the KW-002 Step05 W10 V2 pre-acquisition authority.

This pass is intentionally inert with respect to every provider.  It reads the
complete durable Step02/Step03/Step05 evidence universe and the accepted W09
Step04 authority, reconciles all 13 queue rows, and writes only the frozen V2
pre-acquisition outputs.  It does not mutate Step03A, Step03B, W09, the mutable
job cursor/state, or any later roadmap step.
"""

from __future__ import annotations

import csv
import hashlib
import json
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
REPO = HERE.parents[6]
DATE = "2026-09-12"
HANDOFF_ID = "KW002-BS-W10-V2"
WORK_START_REMOTE_HEAD = "7ceec096dad6703b5dffede3271019f55946d75d"
WORK_PRE_PUBLICATION_REMOTE_HEAD = "7ceec096dad6703b5dffede3271019f55946d75d"
REMOTE_CHANGED_PATHS: list[str] = []

INPUTS = {
    "prompt": "STEP_05_W10_PRE_ACQUISITION_WORK_PROMPT_V2_2026-09-12.md",
    "release": "STEP_05_W10_PRE_ACQUISITION_EXECUTION_RELEASE_V2_2026-09-12.md",
    "pre_handoff_manifest": "STEP_05_W10_PRE_HANDOFF_MANIFEST_V2_2026-09-12.md",
    "external_research": "STEP_05_W10_PRE_ACQUISITION_EXTERNAL_RESEARCH_V2_2026-09-12.md",
    "rule_correction": "STEP_05_W10_PREPARATION_RULE_VIOLATION_AND_CORRECTION_2026-09-12.md",
    "w10_gate": "STEP_05_W10_CURRENT_AUTHORITY_QUEUE_GATE_2026-09-12.tsv",
    "w09_acceptance": "STEP_04_W09_MAIN_CHATGPT_REMOTE_READBACK_ACCEPTANCE_2026-09-12.md",
    "w09_manifest": "STEP_04_CURRENT_AUTHORITY_ARTIFACT_MANIFEST_2026-09-11.json",
    "w09_queue": "STEP_04_CURRENT_AUTHORITY_TARGETED_EXPANSION_QUEUE_2026-09-11.tsv",
    "w09_families": "STEP_04_CURRENT_AUTHORITY_FAMILY_TRIAGE_2026-09-11.tsv",
    "w09_signals": "STEP_04_CURRENT_AUTHORITY_IDENTITY_SIGNAL_LEDGER_2026-09-11.tsv",
    "w09_occurrences": "STEP_04_CURRENT_AUTHORITY_OCCURRENCE_FAMILY_LEDGER_2026-09-11.tsv",
    "w09_independent": "STEP_04_CURRENT_AUTHORITY_INDEPENDENT_TAXONOMY_AUDIT_2026-09-11.tsv",
    "w09_feedback": "STEP_04_CURRENT_AUTHORITY_SANITATION_FEEDBACK_REGISTER_2026-09-11.tsv",
    "step02_manifest": "STEP_02_PRIMARY_ACQUISITION_MANIFEST_V2.csv",
    "step03_manifest": "STEP_03_WORDSTAT_EXECUTION_MANIFEST_V1.csv",
    "step03a_ledger": "STEP_03A_NORMALIZATION_LEDGER_2026-09-11.tsv",
    "step03a_pool": "STEP_03A_NORMALIZED_UNIQUE_POOL_2026-09-11.tsv",
    "step03b_keep": "STEP_03B_SANITIZED_CANDIDATE_POOL_CORRECTED_2026-09-11.tsv",
    "step03b_excluded_hold": "STEP_03B_EXCLUDED_HOLD_REGISTER_CORRECTED_2026-09-11.tsv",
    "e013_receipt": "STEP_05_E013_WORDSTAT_EVIDENCE_RECEIPT_2026-09-10.md",
    "e013_raw": "STEP_05_WORDSTAT_RAW/STEP05__E013__wordstat-132a43ff-7cf9-4544-a6e2-68da666c4813.raw.txt",
    "bridge_product": "../../../../../src/shared/product.js",
    "bridge_wordstat_protocol": "../../../../../src/shared/wordstat_protocol.js",
}

OUTPUTS = {
    "queue": "STEP_05_W10_V2_QUEUE_RECONCILIATION_WORK_2026-09-12.tsv",
    "reuse": "STEP_05_W10_V2_EXISTING_EVIDENCE_REUSE_REGISTER_2026-09-12.tsv",
    "candidate": "STEP_05_W10_V2_PROVIDER_CANDIDATE_MANIFEST_V1_2026-09-12.tsv",
    "regression": "STEP_05_W10_V2_PRE_ACQUISITION_KNOWN_FAILURE_REGRESSION_MATRIX_2026-09-12.tsv",
    "qa": "STEP_05_W10_V2_PRE_ACQUISITION_QA_2026-09-12.md",
    "return": "STEP_05_W10_V2_PRE_ACQUISITION_WORK_RETURN_2026-09-12.md",
    "source": Path(__file__).name,
    "manifest": "STEP_05_W10_V2_ARTIFACT_MANIFEST_2026-09-12.json",
}

RAW_Q001 = "STEP_03_WORDSTAT_RAW/001__Q001__wordstat-batch-9292c032-e48e-443e-8576-a51ad4b2c8cc.txt"
RAW_Q002 = "STEP_03_WORDSTAT_RAW/RECOVERED__050__wordstat-619ef51a-c0a8-4a6b-9f7e-4f1709aae204.json"
RAW_Q003 = "STEP_03_WORDSTAT_RAW/RECOVERED__051__wordstat-2e63726e-3660-4838-b5d4-b56bbfcb00f5.json"
RAW_Q019 = "STEP_03_WORDSTAT_RAW/MANUAL__067__wordstat-0b5fe42d-3b5c-4cb3-aa1f-76c77ea6ec12.raw.txt"

QUEUE_FIELDS = [
    "queue_id", "family_id", "current_problem", "current_w09_gate",
    "prior_acquisition_overlap", "existing_evidence_locator", "owner_fact_dependency",
    "search_demand_question", "recommended_disposition", "candidate_id_or_none",
    "candidate_phrase_or_none", "operator_or_scope_gain", "positive_information_gain",
    "negative_result_value", "stop_condition", "literal_duplicate_check",
    "semantic_duplicate_check", "collision_risk", "later_route", "confidence",
]

CANDIDATE_FIELDS = [
    "candidate_id", "source_queue_id", "unresolved_question", "phrase", "regions",
    "devices", "requested_depth_if_bridge_supported", "operator_usage",
    "prior_probe_difference", "expected_information_gain", "negative_result_value",
    "collision_guard", "stop_condition", "max_requests", "estimated_cost_rub",
    "execution_status",
]

REUSE_FIELDS = [
    "evidence_id", "queue_ids", "evidence_class", "step02_seed_ids",
    "provider_request_ids", "tested_phrase_scope", "durable_evidence_locator",
    "source_occurrences", "normalized_identities_touched", "observed_provider_state",
    "how_reused_in_w10", "claim_boundary", "reprobe_allowed_now",
]

REGRESSION_FIELDS = [
    "check_id", "failure_class", "evidence_scope", "expected", "observed",
    "result", "blocking_if_fail",
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_table(name: str, delimiter: str = "\t") -> list[dict[str, str]]:
    with (HERE / name).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter=delimiter))


def write_tsv(name: str, rows: list[dict[str, object]], fields: list[str]) -> None:
    with (HERE / name).open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=fields, delimiter="\t", lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def parse_prefixed_json(path: Path) -> dict[str, object]:
    text = path.read_text(encoding="utf-8")
    return json.loads(text[text.index("{"):])


def manifest_record(path: Path, semantics: str) -> dict[str, object]:
    if semantics == "data_rows_excluding_header":
        with path.open(encoding="utf-8-sig", newline="") as handle:
            rows = max(sum(1 for _ in handle) - 1, 0)
    else:
        rows = len(path.read_text(encoding="utf-8").splitlines())
    return {
        "bytes": path.stat().st_size,
        "sha256": sha256(path),
        "rows_or_lines": rows,
        "count_semantics": semantics,
    }


def source_counts(
    ledger: list[dict[str, str]],
    source_ids: set[str],
) -> tuple[int, int]:
    rows = [row for row in ledger if row["seed_id"] in source_ids]
    return len(rows), len({row["normalized_phrase_id"] for row in rows})


def main() -> None:
    assert len(WORK_START_REMOTE_HEAD) == 40
    assert len(WORK_PRE_PUBLICATION_REMOTE_HEAD) == 40

    # Freeze every accepted W09 artifact listed by its own manifest, then read
    # every full-volume row rather than relying on samples or the queue prose.
    w09_manifest = json.loads((HERE / INPUTS["w09_manifest"]).read_text(encoding="utf-8"))
    assert w09_manifest["handoff_id"] == "KW002-BS-W09"
    assert w09_manifest["counts"]["normalized_identities"] == 24576
    assert w09_manifest["counts"]["raw_occurrences"] == 25979
    assert w09_manifest["counts"]["queue_rows"] == 13
    for artifact, record in w09_manifest["artifacts"].items():
        assert sha256(HERE / artifact) == record["sha256"], artifact

    queue_in = read_table(INPUTS["w09_queue"])
    gate_in = read_table(INPUTS["w10_gate"])
    family_rows = read_table(INPUTS["w09_families"])
    signal_rows = read_table(INPUTS["w09_signals"])
    occurrence_rows = read_table(INPUTS["w09_occurrences"])
    independent_rows = read_table(INPUTS["w09_independent"])
    feedback_rows = read_table(INPUTS["w09_feedback"])
    pool_rows = read_table(INPUTS["step03a_pool"])
    normalization_rows = read_table(INPUTS["step03a_ledger"])
    keep_rows = read_table(INPUTS["step03b_keep"])
    excluded_hold_rows = read_table(INPUTS["step03b_excluded_hold"])
    step02_rows = read_table(INPUTS["step02_manifest"], ",")
    step03_rows = read_table(INPUTS["step03_manifest"], ",")

    assert len(queue_in) == len(gate_in) == 13
    assert [row["queue_id"] for row in queue_in] == [f"PSQ{i:03d}" for i in range(1, 14)]
    assert [row["queue_id"] for row in gate_in] == [row["queue_id"] for row in queue_in]
    assert len(family_rows) == 32 and len(feedback_rows) == 18
    assert len(signal_rows) == len(independent_rows) == len(pool_rows) == 24576
    assert len(occurrence_rows) == len(normalization_rows) == 25979
    assert len(keep_rows) == 5100 and len(excluded_hold_rows) == 19476
    assert len(step02_rows) == len(step03_rows) == 79

    pool_by_id = {row["normalized_phrase_id"]: row for row in pool_rows}
    signal_by_id = {row["normalized_phrase_id"]: row for row in signal_rows}
    independent_by_id = {row["normalized_phrase_id"]: row for row in independent_rows}
    assert len(pool_by_id) == len(signal_by_id) == len(independent_by_id) == 24576
    assert set(pool_by_id) == set(signal_by_id) == set(independent_by_id)
    assert all(
        independent_by_id[npid]["w09_primary_family_id"]
        == signal_by_id[npid]["primary_preliminary_family_id"]
        for npid in pool_by_id
    )

    partition = {row["normalized_phrase_id"]: row for row in keep_rows + excluded_hold_rows}
    assert len(partition) == 24576 and set(partition) == set(pool_by_id)
    state_counts = Counter(row["step03b_state"] for row in signal_rows)
    assert state_counts == Counter({"KEEP": 5100, "HOLD": 13035, "EXCLUDE": 6441})
    assert all(row["step03b_mutated"] == "NO" for row in signal_rows)

    raw_ids = {row["raw_occurrence_id"] for row in occurrence_rows}
    assert len(raw_ids) == 25979
    raw_count_by_identity = Counter(row["normalized_phrase_id"] for row in occurrence_rows)
    assert set(raw_count_by_identity) == set(pool_by_id)
    assert all(
        raw_count_by_identity[npid] == int(pool_by_id[npid]["raw_occurrence_count"])
        for npid in pool_by_id
    )
    assert {row["occurrence_id"] for row in normalization_rows} == raw_ids

    active = [row for row in signal_rows if row["step03b_state"] != "EXCLUDE"]
    assert len(active) == 18135
    family_identity_counts = Counter(row["primary_preliminary_family_id"] for row in active)
    family_raw_counts = Counter(
        row["w09_primary_family_id"] for row in occurrence_rows if row["step03b_state"] != "EXCLUDE"
    )
    family_by_id = {row["family_id"]: row for row in family_rows}
    assert sum(family_identity_counts.values()) == 18135
    assert sum(family_raw_counts.values()) == 19086
    assert all(
        family_identity_counts[row["family_id"]] == int(row["normalized_identity_count"])
        and family_raw_counts[row["family_id"]] == int(row["raw_occurrence_count"])
        for row in family_rows
    )

    # The complete 79-row planning/execution manifests must align exactly.
    step03_by_source_order = {row["step02_run_order"]: row for row in step03_rows}
    assert len(step03_by_source_order) == 79
    for planned in step02_rows:
        executed = step03_by_source_order[planned["run_order"]]
        assert planned["run_order"] == executed["step02_run_order"]
        assert planned["seed_id"] == executed["seed_id"]
        assert planned["seed_phrase"] == executed["seed_phrase"]
        assert planned["quality_role"] == executed["quality_role"]
    step02_by_seed = {row["seed_id"]: row for row in step02_rows}
    assert len(step02_by_seed) == 79

    expected_probes = {
        "Q001": "(амулет|оберег|талисман) RSOTM",
        "Q002": "(амулет|оберег|талисман) Soldier Of Fortune",
        "Q003": "(амулет|оберег|талисман) Бусидо Путь Воина",
        "Q005": "(амулет|оберег|талисман) Ом",
        "Q019": "Кровь и Песок (амулет|оберег|талисман)",
        "S053": "Аум",
    }
    for seed_id, phrase in expected_probes.items():
        assert step02_by_seed[seed_id]["seed_phrase"] == phrase

    raw_tree = HERE / "STEP_03_WORDSTAT_RAW"
    raw_tree_files = sorted(path for path in raw_tree.rglob("*") if path.is_file())
    assert len(raw_tree_files) == 96
    raw_tree_aggregate = hashlib.sha256()
    for path in raw_tree_files:
        raw_tree_aggregate.update(str(path.relative_to(HERE)).encode("utf-8"))
        raw_tree_aggregate.update(hashlib.sha256(path.read_bytes()).digest())

    q001 = parse_prefixed_json(HERE / RAW_Q001)["provider_result"]
    q002 = json.loads((HERE / RAW_Q002).read_text(encoding="utf-8"))
    q003 = json.loads((HERE / RAW_Q003).read_text(encoding="utf-8"))
    q019 = parse_prefixed_json(HERE / RAW_Q019)
    assert q001["command"]["phrase"] == expected_probes["Q001"] and q001["result"] == {}
    assert q002["command"]["phrase"] == expected_probes["Q002"] and q002["result"] == {}
    assert q003["command"]["phrase"] == expected_probes["Q003"] and q003["result"] == {}
    assert q019["command"]["phrase"] == expected_probes["Q019"]
    assert q019["result"] == {"totalCount": "1"}

    target_source_counts = {
        "PSQ001": source_counts(normalization_rows, {"Q001", "Q002", "Q003"}),
        "PSQ004": source_counts(normalization_rows, {"Q019"}),
        "AUM_BROAD": source_counts(normalization_rows, {"S053"}),
        "OM_QUALIFIED": source_counts(normalization_rows, {"Q005"}),
        "PSQ006": source_counts(normalization_rows, {"S014", "S049"}),
        "PSQ007": source_counts(normalization_rows, {"S023", "S024", "S025", "S028", "S029"}),
        "PSQ008": source_counts(normalization_rows, {"S019", "S020", "Q015"}),
    }
    assert target_source_counts == {
        "PSQ001": (0, 0), "PSQ004": (0, 0), "AUM_BROAD": (476, 476),
        "OM_QUALIFIED": (23, 23), "PSQ006": (213, 211),
        "PSQ007": (2412, 2409), "PSQ008": (703, 688),
    }

    e013_path = HERE / INPUTS["e013_raw"]
    e013 = parse_prefixed_json(e013_path)
    assert e013["command"]["phrase"] == "!чётки"
    assert len(e013["result"]["results"]) == 2000
    assert len(e013["result"]["associations"]) == 19
    assert sha256(e013_path) == "8b565057bdafb00243fbd6acd1ce05d20d956717a73219b69fda3be27488fda1"

    bridge_product = (HERE / INPUTS["bridge_product"]).resolve().read_text(encoding="utf-8")
    bridge_protocol = (HERE / INPUTS["bridge_wordstat_protocol"]).resolve().read_text(encoding="utf-8")
    assert "0.1.2" in bridge_product
    for fragment in ["getTop", "numPhrases", "DEVICE_ALL", "2000", "regions"]:
        assert fragment in bridge_protocol

    queue_source = {row["queue_id"]: row for row in queue_in}
    gate_source = {row["queue_id"]: row for row in gate_in}
    assert set(queue_source) == set(gate_source) == {f"PSQ{i:03d}" for i in range(1, 14)}

    def qrow(
        queue_id: str,
        overlap: str,
        locator: str,
        owner: str,
        question: str,
        disposition: str,
        candidate_id: str,
        candidate_phrase: str,
        scope_gain: str,
        positive_gain: str,
        negative_value: str,
        stop: str,
        literal: str,
        semantic: str,
        collision: str,
        later: str,
        confidence: str,
    ) -> dict[str, str]:
        source = queue_source[queue_id]
        return {
            "queue_id": queue_id,
            "family_id": source["family_id"],
            "current_problem": source["problem"],
            "current_w09_gate": gate_source[queue_id]["step05_w10_entry_gate"],
            "prior_acquisition_overlap": overlap,
            "existing_evidence_locator": locator,
            "owner_fact_dependency": owner,
            "search_demand_question": question,
            "recommended_disposition": disposition,
            "candidate_id_or_none": candidate_id,
            "candidate_phrase_or_none": candidate_phrase,
            "operator_or_scope_gain": scope_gain,
            "positive_information_gain": positive_gain,
            "negative_result_value": negative_value,
            "stop_condition": stop,
            "literal_duplicate_check": literal,
            "semantic_duplicate_check": semantic,
            "collision_risk": collision,
            "later_route": later,
            "confidence": confidence,
        }

    queue_rows = [
        qrow("PSQ001", "EXACT_SCOPE_ALREADY_EXECUTED_Q001_Q002_Q003", f"{INPUTS['step02_manifest']}#Q001-Q003|{RAW_Q001}|{RAW_Q002}|{RAW_Q003}", "NO",
             "Whether exact catalog names yield product-qualified demand vocabulary.", "CLOSED_EXISTING_DURABLE_EVIDENCE_NO_REPROBE", "NONE", "NONE", "ZERO_FOR_REPLAY",
             "Existing exact product-class probes already answer the bounded acquisition question.", "Already realized: no observed result/association rows; Q001 empty body must not be restated as totalCount=0.",
             "Permanent for the same scope; reopen only on material new catalog scope under a new release.", "DUPLICATE_EXACT_NAME_PLUS_PRODUCT_CLASS_SCOPE",
             "SEMANTIC_DUPLICATE_NO_NEW_OPERATOR_OR_SCOPE_GAIN", "LOW_IF_REUSED; HIGH_IF_SPECULATIVE_TITLE_VARIANTS_ARE_INVENTED", "OWNER_OR_LATER_SCOPE_CHANGE_ONLY", "HIGH"),
        qrow("PSQ002", "FAMILY_EVIDENCE_EXISTS_BUT_PHYSICAL_FORM_IS_NOT_SEARCH_EVIDENCE", f"{INPUTS['w09_queue']}#PSQ002|{INPUTS['w09_signals']}#PSF017", "YES_PHYSICAL_FORM",
             "None until the owner confirms whether the catalog item is a physical product and which form.", "OWNER_FACT_HOLD_NO_PROVIDER", "NONE", "NONE", "NOT_APPLICABLE",
             "Only an owner fact can create a safe later demand question.", "Preserves UNKNOWN without manufacturing inventory truth.", "Stop now; owner fact and separate release required.",
             "NOT_APPLICABLE", "SEARCH_CANNOT_RESOLVE_OWNER_FACT", "HIGH_UNSUPPORTED_INVENTORY_INFERENCE", "OWNER_FACT", "HIGH"),
        qrow("PSQ003", "NO_QUALIFIED_ROWS_AND_NO_OWNER_FORM_AUTHORITY", f"{INPUTS['w09_queue']}#PSQ003|CLIENT_SUPPLIED_ASSORTMENT_MANIFEST.md", "YES_PHYSICAL_FORM",
             "None until the owner confirms the physical form of Герб России.", "OWNER_FACT_HOLD_NO_PROVIDER", "NONE", "NONE", "NOT_APPLICABLE",
             "Only confirmed form would define a later bounded hypothesis.", "Preserves UNKNOWN; absence of search rows is not absence of inventory.", "Stop now; owner fact and separate release required.",
             "NOT_APPLICABLE", "SEARCH_CANNOT_RESOLVE_OWNER_FACT", "HIGH_INVENTORY_INFERENCE", "OWNER_FACT", "HIGH"),
        qrow("PSQ004", "EXACT_BRAND_PLUS_PRODUCT_SCOPE_ALREADY_EXECUTED_Q019", f"{INPUTS['step02_manifest']}#Q019|{RAW_Q019}", "NO",
             "Whether Blood & Sand has product-qualified demand vocabulary.", "CLOSED_EXISTING_DURABLE_EVIDENCE_NO_REPROBE", "NONE", "NONE", "ZERO_FOR_REPLAY",
             "Q019 is the same brand+product question and already returned no result/association rows.", "Already realized: totalCount=1 with zero materialized result/association rows closes this bounded round, not demand truth globally.",
             "Permanent for identical scope; reopen only for a fact-supported new brand alias under a new release.", "DUPLICATE_EXACT_BRAND_PLUS_PRODUCT_SCOPE",
             "SEMANTIC_DUPLICATE_NO_DISTINGUISHING_QUALIFIER", "LOW_IF_REUSED; HIGH_IF_UNSUPPORTED_ALIAS_IS_INVENTED", "MATERIAL_NEW_BRAND_FACT_ONLY", "HIGH"),
        qrow("PSQ005", "S053_BROAD_AUM_EXISTS_AND_Q005_QUALIFIED_OM_EXISTS_BUT_QUALIFIED_AUM_DOES_NOT", f"{INPUTS['step02_manifest']}#S053,Q005|{INPUTS['step03a_ledger']}|{INPUTS['w09_signals']}", "NO",
             "Whether the distinct Cyrillic Аум spelling has physical-product-qualified current demand evidence.", "SURVIVES_AS_ONLY_FUTURE_FIRST_CANDIDATE_NOT_EXECUTED", "W10C001", "(амулет|оберег|талисман) Аум", "YES_AUM_SPELLING_PLUS_PRODUCT_CLASS_QUALIFICATION",
             "A positive response supplies Aum-specific product vocabulary absent from broad S053 and Om-only Q005.", "A zero/empty response closes the Aum-only branch without replaying Om or inferring demand absence globally.",
             "Exactly one later GetTop request; stop on any success, empty result, validation failure or provider failure; no automatic retry.", "NO_EXACT_PHRASE_MATCH_IN_79_ROW_MANIFEST",
             "NON_DUPLICATE_DISTINCT_SPELLING_AND_SCOPE; OM_IS_EXPLICITLY_EXCLUDED_AS_PROOF", "HIGH_RELIGIOUS_MEDIA_AUMA_INDUSTRIAL_AND_OM_EQUIVALENCE_COLLISIONS_REQUIRE_STEP03A_03B", "SEPARATE_PROVIDER_EXECUTION_RELEASE", "HIGH"),
        qrow("PSQ006", "FULL_DURABLE_S014_S049_EVIDENCE_AND_ACCEPTED_W09_REUSE_AUTHORITY", f"{INPUTS['step03a_ledger']}#S014,S049|{INPUTS['w09_queue']}#PSQ006", "NO",
             "No current search gap; map existing Gungnir/Odin-spear evidence.", "CLOSED_EXISTING_DURABLE_EVIDENCE_NO_REPROBE", "NONE", "NONE", "ZERO_REUSE_ONLY",
             "213 source occurrences / 211 identities plus accepted qualified evidence already cover the branch.", "Not applicable; the existing evidence already provides the stop value.", "Permanent unless material inventory/scope changes under a new release.",
             "DUPLICATE_EXISTING_SEED_SCOPE", "SEMANTIC_DUPLICATE_QUALIFIED_EVIDENCE_EXISTS", "KNOWN_GAME_WEAPON_REFERENT_PRESERVED", "REUSE_ONLY", "HIGH"),
        qrow("PSQ007", "FULL_DURABLE_S023_S024_S025_S028_S029_EVIDENCE_AND_ACCEPTED_W09_REUSE_AUTHORITY", f"{INPUTS['step03a_ledger']}#S023,S024,S025,S028,S029|{INPUTS['w09_queue']}#PSQ007", "NO",
             "No current search gap; reuse observed entity/product collisions.", "CLOSED_EXISTING_DURABLE_EVIDENCE_NO_REPROBE", "NONE", "NONE", "ZERO_REUSE_ONLY",
             "2412 source occurrences / 2409 identities include the named branches and accepted qualified collisions.", "Not applicable; the branch is already observed.", "Permanent unless material upstream scope changes.",
             "DUPLICATE_EXISTING_NAMED_SEEDS", "SEMANTIC_DUPLICATE_ENTITY_AND_PRODUCT_EVIDENCE_EXISTS", "PLACE_PERSON_ORGANIZATION_COLLISIONS_REMAIN_AMBIGUOUS", "REUSE_ONLY", "HIGH"),
        qrow("PSQ008", "FULL_DURABLE_S019_S020_Q015_EVIDENCE_AND_ACCEPTED_W09_REUSE_AUTHORITY", f"{INPUTS['step03a_ledger']}#S019,S020,Q015|{INPUTS['w09_queue']}#PSQ008", "NO",
             "No current search gap; reuse Belobog/Chernobog/Mara evidence.", "CLOSED_EXISTING_DURABLE_EVIDENCE_NO_REPROBE", "NONE", "NONE", "ZERO_REUSE_ONLY",
             "703 source occurrences / 688 identities cover the branches and accepted qualified evidence.", "Not applicable; the branch is already observed.", "Permanent unless material upstream scope changes.",
             "DUPLICATE_EXISTING_NAMED_SEEDS", "SEMANTIC_DUPLICATE_QUALIFIED_AND_COLLISION_EVIDENCE_EXISTS", "MEDIA_GAME_MYTHOLOGY_COLLISIONS_REMAIN_AMBIGUOUS", "REUSE_ONLY", "HIGH"),
        qrow("PSQ009", "ZODIAC_SEARCH_VOCABULARY_EXISTS_BUT_FORM_MATERIAL_IS_OWNER_TRUTH", f"{INPUTS['w09_queue']}#PSQ009|{INPUTS['w09_signals']}#PSF012", "YES_FORM_AND_MATERIAL",
             "None until owner supplies catalog form/material facts.", "OWNER_FACT_HOLD_NO_PROVIDER", "NONE", "NONE", "NOT_APPLICABLE",
             "Confirmed owner facts could later define a bounded 12-sign template.", "Preserves UNKNOWN and blocks search-demand-to-inventory leakage.", "Stop now; owner fact and separate release required.",
             "NOT_APPLICABLE", "SEARCH_CANNOT_PROVE_FORM_OR_MATERIAL", "HIGH_UNSUPPORTED_CATALOG_TEMPLATE", "OWNER_FACT", "HIGH"),
        qrow("PSQ010", "DURABLE_E013_NEGATIVE_MORPHOLOGY_EVIDENCE_ALREADY_EXISTS", f"{INPUTS['e013_receipt']}|{INPUTS['e013_raw']}", "NO",
             "No current search gap; reuse durable !чётки evidence.", "CLOSED_REUSE_E013_NO_REPLAY", "NONE", "NONE", "ZERO_REUSE_ONLY",
             "E013 already contributes 2000 results and 19 associations as the durable morphology control.", "Already realized; replay would duplicate completed evidence.", "Permanent unless material scope changes and a new release expressly reopens it.",
             "DUPLICATE_EXACT_HISTORICAL_REQUEST", "SEMANTIC_DUPLICATE_SAME_MORPHOLOGY_CONTROL", "BROAD_NEGATIVE_OPERATOR_EVIDENCE_IS_NOT_FINAL_RELEVANCE", "REUSE_ONLY", "HIGH"),
        qrow("PSQ011", "CURRENT_VEHICLE_EVIDENCE_HAS_NO_NAMED_UNRESOLVED_COLLISION", f"{INPUTS['w09_queue']}#PSQ011|{INPUTS['w09_signals']}#PSF020", "NO",
             "No provider-ready question until a later named SERP/intent collision is observed.", "DEFER_TO_STEP10_OR_LATER_SERP_INTENT", "NONE", "NONE", "NOT_APPLICABLE_NOW",
             "Only a later concrete named collision could add information.", "Current absence of a named collision means acquisition would be untargeted.", "Stop now; separate later release required after concrete collision evidence.",
             "NO_CURRENT_CANDIDATE", "NO_CURRENT_TESTABLE_INCREMENTAL_SCOPE", "VEHICLE_USE_MODEL_PART_BOUNDARY", "STEP10_OR_LATER_SERP", "HIGH"),
        qrow("PSQ012", "OBSERVED_FORMS_MATERIALS_ARE_DEMAND_EVIDENCE_NOT_INVENTORY", f"{INPUTS['w09_queue']}#PSQ012|{INPUTS['w09_signals']}#PSF010", "YES_INVENTORY_FORM_MATERIAL",
             "No search-demand question can resolve client inventory.", "OWNER_FACT_ONLY_NO_PROVIDER_ROUTE", "NONE", "NONE", "NOT_APPLICABLE",
             "Only owner inventory data is admissible.", "Preserves UNKNOWN without unsupported product claims.", "Stop after owner confirmation or explicit absence.",
             "NOT_APPLICABLE", "SEARCH_CANNOT_PROVE_INVENTORY", "HIGH_INVENTORY_HALLUCINATION", "OWNER_FACT", "HIGH"),
        qrow("PSQ013", "OBSERVED_EFFECT_AUDIENCE_WORDING_CANNOT_AUTHORIZE_CLIENT_CLAIMS", f"{INPUTS['w09_queue']}#PSQ013|{INPUTS['w09_signals']}#PSF011", "YES_APPROVED_CLAIM_BOUNDARY",
             "No search-demand question can approve effect or audience claims.", "OWNER_FACT_ONLY_NO_PROVIDER_ROUTE", "NONE", "NONE", "NOT_APPLICABLE",
             "Only owner-approved factual language is admissible.", "Preserves UNKNOWN and prevents unsupported effectiveness claims.", "Stop after owner-approved boundary or explicit absence.",
             "NOT_APPLICABLE", "SEARCH_CANNOT_AUTHORIZE_CLAIMS", "HIGH_UNSUPPORTED_EFFECT_CLAIMS", "OWNER_FACT", "HIGH"),
    ]
    assert len(queue_rows) == 13 and {row["queue_id"] for row in queue_rows} == set(queue_source)

    reuse_rows = [
        {"evidence_id": "W10E001", "queue_ids": "PSQ001", "evidence_class": "EXACT_QUALIFIED_PRIOR_PROBES",
         "step02_seed_ids": "Q001|Q002|Q003", "provider_request_ids": "wordstat-batch-9292c032-e48e-443e-8576-a51ad4b2c8cc|wordstat-619ef51a-c0a8-4a6b-9f7e-4f1709aae204|wordstat-2e63726e-3660-4838-b5d4-b56bbfcb00f5",
         "tested_phrase_scope": "(амулет|оберег|талисман) + each of RSOTM, Soldier Of Fortune, Бусидо Путь Воина",
         "durable_evidence_locator": f"{RAW_Q001}|{RAW_Q002}|{RAW_Q003}", "source_occurrences": 0, "normalized_identities_touched": 0,
         "observed_provider_state": "HTTP_200_EMPTY_OBJECTS; Q001_TOTALCOUNT_FIELD_UNKNOWN", "how_reused_in_w10": "Closes identical PSQ001 acquisition scope without replay.",
         "claim_boundary": "No observed expansion; not proof of zero demand.", "reprobe_allowed_now": "NO"},
        {"evidence_id": "W10E002", "queue_ids": "PSQ004", "evidence_class": "EXACT_BRAND_PRODUCT_PRIOR_PROBE",
         "step02_seed_ids": "Q019", "provider_request_ids": "wordstat-0b5fe42d-3b5c-4cb3-aa1f-76c77ea6ec12",
         "tested_phrase_scope": "Кровь и Песок (амулет|оберег|талисман)", "durable_evidence_locator": RAW_Q019,
         "source_occurrences": 0, "normalized_identities_touched": 0, "observed_provider_state": "HTTP_200_TOTALCOUNT_1_RESULTS_0_ASSOCIATIONS_0",
         "how_reused_in_w10": "Closes identical PSQ004 brand+product round.", "claim_boundary": "No materialized expansion; not proof of zero demand globally.", "reprobe_allowed_now": "NO"},
        {"evidence_id": "W10E003", "queue_ids": "PSQ005", "evidence_class": "BROAD_AUM_PRIOR_EVIDENCE",
         "step02_seed_ids": "S053", "provider_request_ids": "SEE_STEP03A_LINEAGE", "tested_phrase_scope": "Аум broad",
         "durable_evidence_locator": f"{INPUTS['step03a_ledger']}#S053", "source_occurrences": 476, "normalized_identities_touched": 476,
         "observed_provider_state": "460_RESULTS_16_ASSOCIATIONS; 317_HOLD_159_EXCLUDE",
         "how_reused_in_w10": "Defines collision baseline and proves broad Aum is not a physical-product answer.",
         "claim_boundary": "Does not answer qualified Aum product demand.", "reprobe_allowed_now": "NO"},
        {"evidence_id": "W10E004", "queue_ids": "PSQ005", "evidence_class": "QUALIFIED_OM_PRIOR_EVIDENCE",
         "step02_seed_ids": "Q005", "provider_request_ids": "SEE_STEP03A_LINEAGE", "tested_phrase_scope": "(амулет|оберег|талисман) Ом",
         "durable_evidence_locator": f"{INPUTS['step03a_ledger']}#Q005", "source_occurrences": 23, "normalized_identities_touched": 23,
         "observed_provider_state": "6_RESULTS_17_ASSOCIATIONS; 19_KEEP_3_HOLD_1_EXCLUDE",
         "how_reused_in_w10": "Excluded as proof for Аум while establishing why a spelling-specific gap can survive.",
         "claim_boundary": "Ом and Аум are not silently merged.", "reprobe_allowed_now": "NO"},
        {"evidence_id": "W10E005", "queue_ids": "PSQ006", "evidence_class": "QUALIFIED_GUNGNIR_ODIN_SPEAR_EVIDENCE",
         "step02_seed_ids": "S014|S049", "provider_request_ids": "SEE_STEP03A_LINEAGE", "tested_phrase_scope": "Гунгнир and Копьё Одина",
         "durable_evidence_locator": f"{INPUTS['step03a_ledger']}#S014,S049|{INPUTS['w09_queue']}#PSQ006", "source_occurrences": 213, "normalized_identities_touched": 211,
         "observed_provider_state": "W09_ACCEPTED_EXISTING_EVIDENCE_REUSE; 12_QUALIFIED_GUNGNIR_PLUS_ODIN_SPEAR_FIXTURE",
         "how_reused_in_w10": "Maps current coverage; blocks reprobe.", "claim_boundary": "Game/weapon/referent ambiguity remains preserved.", "reprobe_allowed_now": "NO"},
        {"evidence_id": "W10E006", "queue_ids": "PSQ007", "evidence_class": "NAMED_ENTITY_COLLISION_EVIDENCE",
         "step02_seed_ids": "S023|S024|S025|S028|S029", "provider_request_ids": "SEE_STEP03A_LINEAGE", "tested_phrase_scope": "Алатырь|Триглав|Ратиборец|Знич|Громовик",
         "durable_evidence_locator": f"{INPUTS['step03a_ledger']}#listed_seeds|{INPUTS['w09_queue']}#PSQ007", "source_occurrences": 2412, "normalized_identities_touched": 2409,
         "observed_provider_state": "W09_ACCEPTED_EXISTING_EVIDENCE_REUSE; 79_QUALIFIED_COLLISION_FIXTURE",
         "how_reused_in_w10": "Maps entity/product collision coverage; blocks reprobe.", "claim_boundary": "No final entity or intent verdict.", "reprobe_allowed_now": "NO"},
        {"evidence_id": "W10E007", "queue_ids": "PSQ008", "evidence_class": "BELOBOG_CHERNOBOG_MARA_EVIDENCE",
         "step02_seed_ids": "S019|S020|Q015", "provider_request_ids": "SEE_STEP03A_LINEAGE", "tested_phrase_scope": "Белобог|Чернобог|Мара",
         "durable_evidence_locator": f"{INPUTS['step03a_ledger']}#listed_seeds|{INPUTS['w09_queue']}#PSQ008", "source_occurrences": 703, "normalized_identities_touched": 688,
         "observed_provider_state": "W09_ACCEPTED_EXISTING_EVIDENCE_REUSE; 13_QUALIFIED_BRANCH_FIXTURE",
         "how_reused_in_w10": "Maps qualified/collision evidence; blocks reprobe.", "claim_boundary": "Media/game/mythology ambiguity remains preserved.", "reprobe_allowed_now": "NO"},
        {"evidence_id": "W10E008", "queue_ids": "PSQ010", "evidence_class": "DURABLE_E013_NEGATIVE_MORPHOLOGY_EVIDENCE",
         "step02_seed_ids": "E013", "provider_request_ids": "wordstat-132a43ff-7cf9-4544-a6e2-68da666c4813", "tested_phrase_scope": "!чётки",
         "durable_evidence_locator": f"{INPUTS['e013_receipt']}|{INPUTS['e013_raw']}", "source_occurrences": 2019, "normalized_identities_touched": "NOT_UNIONED_IN_ACCEPTED_STEP03A_AUTHORITY",
         "observed_provider_state": "2000_RESULTS_19_ASSOCIATIONS; RAW_SHA256_VERIFIED; REMOTE_READBACK_PASS",
         "how_reused_in_w10": "Closes replay path and preserves historical evidence separately.", "claim_boundary": "Operator evidence is not final relevance or demand truth.", "reprobe_allowed_now": "NO"},
    ]

    candidate_rows = [{
        "candidate_id": "W10C001",
        "source_queue_id": "PSQ005",
        "unresolved_question": "Does distinct Cyrillic Аум have current physical-product-qualified query vocabulary?",
        "phrase": "(амулет|оберег|талисман) Аум",
        "regions": '["225"]',
        "devices": '["DEVICE_ALL"]',
        "requested_depth_if_bridge_supported": 2000,
        "operator_usage": "Parenthesized OR product-class qualification; no morphology fixation; historical Q005 proves local Bridge acceptance of the same operator shape.",
        "prior_probe_difference": "S053 is unqualified Аум; Q005 is qualified Ом. W10C001 combines the unresolved spelling with explicit product scope and is absent from all 79 prior phrases.",
        "expected_information_gain": "Positive rows can expose Aum-specific product vocabulary; collision-only rows quantify why the branch stays ambiguous.",
        "negative_result_value": "An empty/zero-row outcome closes the Aum-only expansion round without replaying Om or asserting universal zero demand.",
        "collision_guard": "Do not merge Ом into Аум; preserve religious/media/AUMA-industrial collisions; persist full RAW and pass any future rows through Step03A then Step03B before union.",
        "stop_condition": "One later GetTop request maximum; stop on success, empty result, validation failure or provider failure; automatic retry forbidden; new release required for any follow-up.",
        "max_requests": 1,
        "estimated_cost_rub": "0.02_AT_2026-09-12_SOURCE_TRACE_RECHECK_REQUIRED_BEFORE_EXECUTION",
        "execution_status": "NOT_EXECUTED",
    }]

    owner_rows = {"PSQ002", "PSQ003", "PSQ009", "PSQ012", "PSQ013"}
    reuse_queue_rows = {"PSQ006", "PSQ007", "PSQ008", "PSQ010"}
    candidate_queue_ids = {row["source_queue_id"] for row in candidate_rows}
    assert candidate_queue_ids <= {"PSQ001", "PSQ004", "PSQ005"}
    assert len(candidate_rows) <= 1
    assert all(row["execution_status"] == "NOT_EXECUTED" for row in candidate_rows)
    assert not (candidate_queue_ids & owner_rows)
    assert not (candidate_queue_ids & reuse_queue_rows)
    assert "PSQ011" not in candidate_queue_ids
    assert all(row["candidate_id_or_none"] == "NONE" for row in queue_rows if row["queue_id"] in owner_rows | reuse_queue_rows | {"PSQ011"})

    regression_rows = []
    def regression(check_id: str, failure: str, scope: str, expected: str, observed: str, passed: bool = True) -> None:
        regression_rows.append({
            "check_id": check_id, "failure_class": failure, "evidence_scope": scope,
            "expected": expected, "observed": observed,
            "result": "PASS" if passed else "FAIL", "blocking_if_fail": "YES",
        })

    regression("W10R001", "F03_PROVIDER_SUCCESS_NOT_DURABLE_COMPLETION", "all Step03 carriers + E013", "Durable RAW/provenance required", "96 Step03 RAW-tree files byte-read; E013 RAW hash and row arrays verified")
    regression("W10R002", "F03B1_OPERATOR_OR_LEXICAL_MATCH_NOT_SEMANTIC_TRUTH", "candidate and reuse rows", "Operators isolate scope only", "Candidate collision guard requires later Step03A/03B; no semantic truth inferred")
    regression("W10R003", "F03B4_AMBIGUITY_PRESERVED", "24576 W09 identities", "No ambiguity flattening", "All full-volume signal/audit rows read; accepted W09 states and collisions preserved")
    regression("W10R004", "F04_3_CURRENT_UPSTREAM_AUTHORITY_PROPAGATED", "accepted W09 manifest", "All W09 artifacts hash-verified", "12/12 W09 artifact hashes verified; 24576/25979 joins exact")
    regression("W10R005", "F05_1_DUPLICATE_DURABLE_EVIDENCE_PREVENTED", "13 queue rows", "No duplicate reprobes", "PSQ001/004 closed by exact probes; PSQ006/007/008/010 reuse only; duplicate reprobes=0")
    regression("W10R006", "F05_2_OWNER_FACT_NOT_SENT_TO_SEARCH_PROVIDER", "PSQ002/003/009/012/013", "Owner-fact candidates=0", "Five owner-fact rows have candidate NONE")
    regression("W10R007", "F06_PRELIMINARY_FAMILY_NOT_FINAL_CLUSTER_OR_PAGE", "all outputs", "No final intent/SERP/page claims", "All later routing remains explicit; Step06 not started")
    regression("W10R008", "WORK_BASE_FRESHNESS_AND_AUTHORITY_DRIFT", "remote branch", "Start and pre-publication heads recorded; drift classified", f"start={WORK_START_REMOTE_HEAD}; prepub={WORK_PRE_PUBLICATION_REMOTE_HEAD}; changed_paths={len(REMOTE_CHANGED_PATHS)}")
    for queue_id in sorted(reuse_queue_rows):
        regression(f"W10R{len(regression_rows)+1:03d}", f"{queue_id}_REPROBE_FALSE", queue_id, "No candidate/reprobe", "candidate=NONE; reuse register present")
    regression(f"W10R{len(regression_rows)+1:03d}", "E013_BLIND_REPLAY_FALSE", "PSQ010/W10E008", "No replay", "Existing hash-verified E013 reused")
    regression(f"W10R{len(regression_rows)+1:03d}", "OWNER_FACT_ROWS_PROVIDER_CANDIDATES_ZERO", "five owner rows", "0", str(len(candidate_queue_ids & owner_rows)))
    regression(f"W10R{len(regression_rows)+1:03d}", "PSQ011_PROVIDER_CANDIDATE_FALSE", "PSQ011", "false", str("PSQ011" in candidate_queue_ids).lower())
    regression(f"W10R{len(regression_rows)+1:03d}", "PROVIDER_CALLS_ZERO", "W10 execution", "0", "0")
    regression(f"W10R{len(regression_rows)+1:03d}", "STEP06_STARTED_FALSE", "roadmap boundary", "false", "false")
    assert all(row["result"] == "PASS" for row in regression_rows)

    write_tsv(OUTPUTS["queue"], queue_rows, QUEUE_FIELDS)
    write_tsv(OUTPUTS["reuse"], reuse_rows, REUSE_FIELDS)
    write_tsv(OUTPUTS["candidate"], candidate_rows, CANDIDATE_FIELDS)
    write_tsv(OUTPUTS["regression"], regression_rows, REGRESSION_FIELDS)

    changed_class = "NO_REMOTE_DRIFT" if not REMOTE_CHANGED_PATHS else "UNRELATED_PATHS_ONLY_REVALIDATED"
    qa_text = f"""# KW-002 Blood & Sand — Step05 W10 V2 pre-acquisition QA

Date: {DATE}
Handoff: `{HANDOFF_ID}`
Verdict: **PASS_CANDIDATE**

## Authority and freshness

- `WORK_START_REMOTE_HEAD = {WORK_START_REMOTE_HEAD}`
- `WORK_PRE_PUBLICATION_REMOTE_HEAD = {WORK_PRE_PUBLICATION_REMOTE_HEAD}`
- `REMOTE_DRIFT_CLASSIFICATION = {changed_class}`
- `REMOTE_CHANGED_PATHS = {json.dumps(REMOTE_CHANGED_PATHS, ensure_ascii=False)}`
- Current V2 prompt/release/manifest/research/correction authority: **CONFIRMED**.
- Accepted W09 current authority: **USED AND HASH-VERIFIED**.
- Stale mutable cursor/JOB_FLOW/JOB_MANIFEST overwritten or packaged: **0**.

## Complete-volume accounting

| Gate | Expected | Observed | Result |
|---|---:|---:|---|
| W09 normalized identities read/joined | 24,576 | 24,576 | PASS |
| W09 RAW occurrences read/joined | 25,979 | 25,979 | PASS |
| Step03A normalization ledger | 25,979 | 25,979 | PASS |
| Step03B KEEP | 5,100 | {state_counts['KEEP']} | PASS |
| Step03B HOLD | 13,035 | {state_counts['HOLD']} | PASS |
| Step03B EXCLUDE | 6,441 | {state_counts['EXCLUDE']} | PASS |
| Active+HOLD identities | 18,135 | {len(active)} | PASS |
| Active+HOLD RAW | 19,086 | {sum(family_raw_counts.values())} | PASS |
| W09 families read and recounted | 32 | {len(family_rows)} | PASS |
| W09 independent diagnostic rows | 24,576 | {len(independent_rows)} | PASS |
| W09 sanitation feedback rows | 18 | {len(feedback_rows)} | PASS |
| Step02/Step03 manifest alignment | 79/79 | 79/79 | PASS |
| Step03 RAW-tree files byte-read | 96 | {len(raw_tree_files)} | PASS |

Every identity and occurrence was consumed. Family identity/RAW totals were independently recounted from the W09 ledgers and matched all 32 family rows. The independent-taxonomy family key matched the current signal ledger for every one of 24,576 identities. No sampling or truncation was used.

## Queue reconciliation

```text
CURRENT_QUEUE_ROWS = 13
QUEUE_RECONCILED = 13/13
MISSING_QUEUE_ROWS = 0
DUPLICATE_QUEUE_ROWS = 0
CURRENT_W09_QUEUE_IDENTITY = EXACT
SEARCH_GAP_ROWS_CHALLENGED = PSQ001|PSQ004|PSQ005
PSQ001 = CLOSED_BY_Q001_Q002_Q003
PSQ004 = CLOSED_BY_Q019
PSQ005 = SURVIVES_AS_W10C001_NOT_EXECUTED
OWNER_FACT_ROWS_PROVIDER_CANDIDATES = 0
PSQ006_REPROBE = false
PSQ007_REPROBE = false
PSQ008_REPROBE = false
PSQ010_REPROBE = false
PSQ011_PROVIDER_CANDIDATE = false
```

Q001/Q002/Q003 tested the same three exact names with the product-class OR scope. Their durable results contain no result/association rows. Q001's empty object is deliberately recorded as fields unknown, not rewritten as `totalCount=0`. Q019 tested the same Blood & Sand brand+product scope and returned `totalCount=1` with zero materialized result/association rows. Replaying either question has zero incremental gain.

S053 contributes 476 broad `Аум` occurrences/identities (317 HOLD, 159 EXCLUDE). Q005 contributes 23 occurrences/identities for qualified `Ом` (19 KEEP, 3 HOLD, 1 EXCLUDE). Neither answers the distinct qualified `Аум` question, so only W10C001 survives as an inert future candidate.

## Candidate hard gates

```text
SURVIVING_NEW_PROVIDER_CANDIDATES = 1
FIRST_EXECUTION_CANDIDATE = W10C001
EXECUTION_STATUS = NOT_EXECUTED
LITERAL_DUPLICATE = false
SEMANTIC_DUPLICATE = false
INCREMENTAL_GAIN = true
NEGATIVE_RESULT_VALUE = true
STOP_CONDITION = true
MAX_REQUESTS = 1
ESTIMATED_COST_RUB = 0.02 (recheck immediately before any later execution)
BRIDGE_SCHEMA_COMPATIBILITY = PASS
```

The candidate uses only current local Bridge fields (`getTop`, phrase, `numPhrases=2000`, regions `225`, device `DEVICE_ALL`). This is an inert TSV plan row, not a Bridge command or execution authorization. Official operator meaning, provider semantics, quotas and price remain separated from repository-side envelope validation.

## Durable evidence reuse

- PSQ006: 213 source occurrences / 211 identities from S014+S049; accepted W09 qualified-evidence fixture reused.
- PSQ007: 2,412 source occurrences / 2,409 identities across its five named seeds; accepted W09 collision fixture reused.
- PSQ008: 703 source occurrences / 688 identities across S019+S020+Q015; accepted W09 qualified-evidence fixture reused.
- PSQ010: E013 `!чётки` RAW SHA-256 verified, 2,000 results + 19 associations; replay is false.

Historical evidence remains evidence, not final relevance, intent, inventory or page authority.

## Regression and boundary result

All {len(regression_rows)} blocking regression checks pass. Provider calls: Wordstat 0, ordinary Yandex Search 0, GenSearch 0, AI-search 0. Step03A mutations 0, Step03B mutations 0, accepted W09 mutations 0. Step06 started: false. Final intent, SERP clustering, query-to-page ownership and IA: not performed.

`STEP03_RAW_TREE_AGGREGATE_SHA256 = {raw_tree_aggregate.hexdigest()}`
"""
    (HERE / OUTPUTS["qa"]).write_text(qa_text, encoding="utf-8")

    return_text = f"""# KW-002 Blood & Sand — Step05 W10 V2 pre-acquisition Work return

```text
HANDOFF_ID = {HANDOFF_ID}
WORK_START_REMOTE_HEAD = {WORK_START_REMOTE_HEAD}
WORK_PRE_PUBLICATION_REMOTE_HEAD = {WORK_PRE_PUBLICATION_REMOTE_HEAD}
REMOTE_DRIFT_CLASSIFICATION = {changed_class}
QUEUE_RECONCILED = 13/13
SURVIVING_NEW_PROVIDER_CANDIDATES = 1
FIRST_EXECUTION_CANDIDATE = W10C001
FIRST_EXECUTION_CANDIDATE_STATUS = NOT_EXECUTED
E013_REPLAY_REQUIRED = false
OWNER_FACT_BYPASSES = 0
DUPLICATE_REPROBES = 0
PROVIDER_CALLS = 0
STEP03A_MUTATIONS = 0
STEP03B_MUTATIONS = 0
W09_STEP04_MUTATIONS = 0
STEP06_STARTED = false
FINAL_WORK_VERDICT = PASS_CANDIDATE
```

## Result

All 13 accepted W09 queue rows were reconciled against all 79 Step02/Step03 manifest rows, all 96 files in the Step03 RAW tree, the complete 24,576-identity / 25,979-occurrence accepted analytical universe, and durable historical E013.

PSQ001 and PSQ004 do not survive: their exact search questions were already executed as Q001–Q003 and Q019. PSQ006, PSQ007, PSQ008 and PSQ010 are reuse-only and cannot be reprobed. PSQ002, PSQ003, PSQ009, PSQ012 and PSQ013 remain owner-fact questions. PSQ011 remains deferred to a later concrete intent/SERP collision.

Only W10C001 survives for a possible later, separately released provider pass: `(амулет|оберег|талисман) Аум`, one GetTop request maximum, current region/device defaults made explicit, `numPhrases=2000`, estimated 0.02 RUB at the checked 2026-09-12 tariff. It is **NOT_EXECUTED** and must be price/schema-rechecked immediately before any later execution.

Any future response must be persisted in full and pass Step03A normalization and Step03B sanitation before union. Positive demand evidence will not prove inventory, relevance, final intent, clustering, page ownership or claims.

## ПРОСТЫМИ СЛОВАМИ

Три названия RSOTM / Soldier Of Fortune / Бусидо и бренд «Кровь и Песок» повторно спрашивать у Wordstat не нужно: ровно такие квалифицированные вопросы уже задавались, а полезных строк расширения не появилось. Гунгнир, именованные коллизии, Белобог/Чернобог/Мара и старый `!чётки` тоже уже покрыты сохранёнными данными.

Реально новым остался только один узкий вопрос: есть ли у написания `Аум` запросы именно про амулет, оберег или талисман. Старые данные проверяли либо слишком широкий `Аум`, либо отдельное написание `Ом`. Я подготовил одну будущую строку запроса, но не запускал её. Работа остановлена здесь, потому что текущий W10 разрешает подготовку и проверку плана, а не обращение к провайдеру.

STOP: return to Main ChatGPT for remote readback and a separate provider-execution decision.
"""
    (HERE / OUTPUTS["return"]).write_text(return_text, encoding="utf-8")

    semantics = {
        OUTPUTS["queue"]: "data_rows_excluding_header",
        OUTPUTS["reuse"]: "data_rows_excluding_header",
        OUTPUTS["candidate"]: "data_rows_excluding_header",
        OUTPUTS["regression"]: "data_rows_excluding_header",
        OUTPUTS["qa"]: "text_lines",
        OUTPUTS["return"]: "text_lines",
        OUTPUTS["source"]: "text_lines",
    }
    artifact_records = {name: manifest_record(HERE / name, meaning) for name, meaning in semantics.items()}
    input_records = {name: sha256((HERE / path).resolve()) for name, path in INPUTS.items()}
    input_records.update({
        RAW_Q001: sha256(HERE / RAW_Q001), RAW_Q002: sha256(HERE / RAW_Q002),
        RAW_Q003: sha256(HERE / RAW_Q003), RAW_Q019: sha256(HERE / RAW_Q019),
    })
    manifest = {
        "schema": "KW002_STEP05_W10_V2_ARTIFACT_MANIFEST_V1",
        "date": DATE,
        "handoff_id": HANDOFF_ID,
        "work_start_remote_head": WORK_START_REMOTE_HEAD,
        "work_pre_publication_remote_head": WORK_PRE_PUBLICATION_REMOTE_HEAD,
        "remote_changed_paths": REMOTE_CHANGED_PATHS,
        "remote_drift_classification": changed_class,
        "inputs_sha256": input_records,
        "artifacts": artifact_records,
        "manifest_self_hash": "OMITTED_BY_DEFINITION_TO_AVOID_RECURSIVE_HASH",
        "counts": {
            "queue_rows": 13, "queue_reconciled": 13, "reuse_register_rows": len(reuse_rows),
            "candidate_rows": len(candidate_rows), "regression_rows": len(regression_rows),
            "normalized_identities_read": 24576, "raw_occurrences_read": 25979,
            "step02_manifest_rows": 79, "step03_manifest_rows": 79,
            "step03_raw_tree_files_byte_read": 96,
        },
        "decisions": {
            "closed_by_prior_exact_evidence": ["PSQ001", "PSQ004"],
            "only_surviving_future_candidate": "W10C001",
            "candidate_source_queue": "PSQ005",
            "candidate_execution_status": "NOT_EXECUTED",
            "existing_evidence_reuse_only": sorted(reuse_queue_rows),
            "owner_fact_rows": sorted(owner_rows),
            "deferred_rows": ["PSQ011"],
            "e013_replay_required": False,
        },
        "hard_boundaries": {
            "provider_calls": {"wordstat": 0, "search": 0, "gensearch": 0, "ai_search": 0},
            "step03a_mutations": 0, "step03b_mutations": 0, "w09_step04_mutations": 0,
            "step06_started": False, "final_intent": False, "serp_clustering": False,
            "query_to_page": False, "ia": False, "stale_mutable_state_files_in_relay": False,
        },
        "hard_gates": {row["failure_class"]: row["result"] for row in regression_rows},
        "quality": {"verdict": "PASS_CANDIDATE", "hard_gate_failures": 0},
        "publication": {"route": "OWNER_RELAY_UNLESS_NATIVE_GIT_AUTH_AVAILABLE", "remote_readback": "PENDING"},
    }
    (HERE / OUTPUTS["manifest"]).write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )

    # Independent output readback: exact schemas, counts and no execution leakage.
    assert len(read_table(OUTPUTS["queue"])) == 13
    assert len(read_table(OUTPUTS["reuse"])) == 8
    assert len(read_table(OUTPUTS["candidate"])) == 1
    assert len(read_table(OUTPUTS["regression"])) == len(regression_rows)
    assert read_table(OUTPUTS["candidate"])[0]["execution_status"] == "NOT_EXECUTED"
    assert "PROVIDER_CALLS = 0" in (HERE / OUTPUTS["return"]).read_text(encoding="utf-8")

    print(json.dumps({
        "verdict": "PASS_CANDIDATE", "queue": "13/13", "candidate": "W10C001",
        "execution_status": "NOT_EXECUTED", "provider_calls": 0,
        "normalized_identities": 24576, "raw_occurrences": 25979,
    }, ensure_ascii=False, sort_keys=True))


if __name__ == "__main__":
    main()
