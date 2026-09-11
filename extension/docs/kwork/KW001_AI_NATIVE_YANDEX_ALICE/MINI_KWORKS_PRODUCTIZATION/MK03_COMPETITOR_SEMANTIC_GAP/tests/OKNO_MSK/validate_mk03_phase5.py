#!/usr/bin/env python3
"""Quality-contract validator for the isolated MK03 Phase-5 rehearsal."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import zipfile
from collections import Counter
from pathlib import Path


HERE = Path(__file__).resolve().parent
DATE = "2026-09-11"


def read_tsv(name: str) -> list[dict[str, str]]:
    with (HERE / name).open(encoding="utf-8-sig", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


class Checks:
    def __init__(self) -> None:
        self.passed: list[str] = []
        self.failed: list[str] = []

    def require(self, name: str, condition: bool, detail: str = "") -> None:
        if condition:
            self.passed.append(name)
        else:
            self.failed.append(f"{name}: {detail}" if detail else name)


def validate(authorities_only: bool) -> dict[str, object]:
    c = Checks()
    discovery = read_tsv(f"MK03_DISCOVERY_QUERY_FAMILY_AUTHORITY_{DATE}.tsv")
    domains = read_tsv(f"MK03_COMPETITOR_DISCOVERY_REGISTER_{DATE}.tsv")
    pages = read_tsv(f"MK03_COMPETITOR_PAGE_EVIDENCE_{DATE}.tsv")
    provenance = read_tsv(f"MK03_COMPETITOR_DERIVED_CANDIDATE_PROVENANCE_{DATE}.tsv")
    manifest = read_tsv(f"MK03_WORDSTAT_EVIDENCE_MANIFEST_{DATE}.tsv")
    normalized = read_tsv(f"MK03_NORMALIZED_CANDIDATE_AUTHORITY_{DATE}.tsv")
    matrix = read_tsv(f"MK03_EXACT_QUERY_COMPETITOR_SEARCH_MATRIX_{DATE}.tsv")
    gaps = read_tsv(f"MK03_GAP_DECISION_REGISTER_{DATE}.tsv")
    opportunities = read_tsv(f"MK03_BOUNDED_OPPORTUNITY_REGISTER_{DATE}.tsv")
    accounting = json.loads((HERE / f"MK03_ACQUISITION_FINAL_ACCOUNTING_{DATE}.json").read_text(encoding="utf-8"))
    receipt = json.loads((HERE / f"MK03_PROVIDER_REUSE_RECEIPT_{DATE}.json").read_text(encoding="utf-8"))

    c.require("discovery_query_count_75", len(discovery) == 75, str(len(discovery)))
    c.require("discovery_rows_unique", len({r["discovery_query_id"] for r in discovery}) == 75)
    c.require("discovery_trace_no_blank", all(r["query"] and r["discovery_family"] and r["claim_boundary"] for r in discovery))
    c.require("observed_domain_count_237", len(domains) == 237, str(len(domains)))
    c.require("accepted_competitors_9", sum(r["accepted_actual_competitor"] == "YES" for r in domains) == 9)
    c.require("accepted_competitors_are_direct", all(r["competitor_class"] == "DIRECT_BUSINESS_COMPETITOR" for r in domains if r["accepted_actual_competitor"] == "YES"))
    c.require("competitor_pages_44", len(pages) == 44, str(len(pages)))
    c.require("competitor_pages_accessible_or_redirected", all(r["http_or_browser_access_state"] in {"ACCESSIBLE", "REDIRECTED_ACCESSIBLE"} for r in pages))
    c.require("competitor_page_boundaries", all(r["claim_boundary"] for r in pages))
    c.require("candidate_occurrences_92", len(provenance) == 92, str(len(provenance)))
    c.require("candidate_occurrence_ids_unique", len({r["seed_id"] for r in provenance}) == 92)
    c.require("wordstat_manifest_14", len(manifest) == 14, str(len(manifest)))
    c.require("wordstat_reuse_only", all(r["acquisition_mode"] == "PRESERVED_EVIDENCE_REUSE" and r["new_provider_call_in_this_phase"] == "NO" for r in manifest))
    c.require("empty_wordstat_not_zero", all(r["result_interpretation"] == "UNKNOWN_NOT_ZERO" and not r["total_count"] for r in manifest if r["empty_result_flag"] == "true"))
    c.require("normalized_wordstat_rows_160", len(normalized) == 160, str(len(normalized)))
    c.require("normalized_rows_have_count", all(r["returned_count"].isdigit() for r in normalized))
    c.require("accepted_phrase_count_16", sum(r["phase5_terminal_phrase_state"] == "CONFIRMED_GAP_PHRASE" for r in normalized) == 16)
    c.require("exact_query_domain_matrix_81", len(matrix) == 81, str(len(matrix)))
    c.require("matrix_9_by_9", len({r["deduplicated_direction_id"] for r in matrix}) == 9 and len({r["selected_competitor_domain"] for r in matrix}) == 9)
    c.require("selective_serp_success_scope_63", sum(r["tested_pair_state"] == "EXACT_QUERY_DOMAIN_PAIR_TESTED" for r in matrix) == 63)
    c.require("unknown_pairs_not_tested_18", sum(r["tested_pair_state"] == "OUTCOME_UNKNOWN_NOT_TESTED" for r in matrix) == 18)
    c.require("gap_directions_43", len(gaps) == 43, str(len(gaps)))
    c.require("gap_direction_ids_unique", len({r["direction_id"] for r in gaps}) == 43)
    terminal = Counter(r["terminal_state"] for r in gaps)
    c.require("terminal_states_exact", terminal == Counter({"ALREADY_COVERED": 23, "HOLD_EVIDENCE": 10, "CONFIRMED_GAP": 7, "REJECT_OFF_SCOPE": 3}), str(dict(terminal)))
    c.require("one_terminal_state_each", all(r["terminal_state"] in {"CONFIRMED_GAP", "ALREADY_COVERED", "REJECT_OFF_SCOPE", "HOLD_EVIDENCE"} for r in gaps))
    c.require("confirmed_have_wordstat", all(r["representative_query_individual_wordstat"].isdigit() and int(r["accepted_phrase_count"]) >= 1 for r in gaps if r["terminal_state"] == "CONFIRMED_GAP"))
    c.require("confirmed_have_search", all(r["search_evidence_state"] == "SUCCEEDED" for r in gaps if r["terminal_state"] == "CONFIRMED_GAP"))
    c.require("holds_not_promoted", all(r["page_or_implementation_decision"] == "NONE__OUT_OF_SCOPE" for r in gaps if r["terminal_state"] == "HOLD_EVIDENCE"))
    c.require("no_page_decisions", all(r["page_or_implementation_decision"] == "NONE__OUT_OF_SCOPE" for r in gaps))
    c.require("opportunities_7", len(opportunities) == 7, str(len(opportunities)))
    c.require("opportunities_only_confirmed", {r["direction_id"] for r in opportunities} == {r["direction_id"] for r in gaps if r["terminal_state"] == "CONFIRMED_GAP"})
    c.require("opportunities_bounded", all(r["bounded_opportunity"] and r["preservation_constraints"] and r["required_owner_validation"] for r in opportunities))
    c.require("no_auto_create", all(r["page_creation_state"] == "NOT_DECIDED" for r in opportunities))
    c.require("attention_not_schedule", all("not schedule" in r["claim_boundary"] for r in opportunities))
    c.require("accounting_matches", accounting["terminal_direction_counts"] == dict(sorted(terminal.items())))
    c.require("source_accounting_750", accounting["preserved_evidence"]["discovery_top10_rows"] == 750)
    c.require("provider_calls_zero", accounting["new_provider_calls"]["total"] == 0 and receipt["new_provider_calls_total"] == 0)
    c.require("silent_drops_zero", accounting["silent_drops"] == 0 and sum(terminal.values()) == 43)
    c.require("page_creation_decisions_zero", accounting["page_creation_decisions"] == 0)

    artifact = {}
    if not authorities_only:
        package = HERE / f"CLIENT_DELIVERY_PHASE_5_MK03_OKNO_MSK_{DATE}"
        files = sorted(p for p in package.iterdir() if p.is_file()) if package.exists() else []
        c.require("client_package_exists", package.exists())
        c.require("client_package_exactly_3_files", len(files) == 3, str([p.name for p in files]))
        xlsx = next((p for p in files if p.suffix.lower() == ".xlsx"), None)
        pdf = next((p for p in files if p.suffix.lower() == ".pdf"), None)
        md = next((p for p in files if p.suffix.lower() == ".md"), None)
        c.require("client_package_one_xlsx", xlsx is not None)
        c.require("client_package_one_pdf", pdf is not None)
        c.require("client_package_one_handoff", md is not None)
        if xlsx:
            c.require("xlsx_zip_valid", zipfile.is_zipfile(xlsx))
            with zipfile.ZipFile(xlsx) as archive:
                names = archive.namelist()
                c.require("xlsx_has_workbook", "xl/workbook.xml" in names)
                c.require("xlsx_has_styles", "xl/styles.xml" in names)
                c.require("xlsx_has_tables", any(n.startswith("xl/tables/") for n in names))
                xml = b"\n".join(archive.read(n) for n in names if n.endswith(".xml"))
                c.require("xlsx_no_formula_errors", not any(token in xml for token in [b"#REF!", b"#DIV/0!", b"#VALUE!", b"#NAME?"]))
            artifact["xlsx"] = {"path": str(xlsx), "sha256": sha256(xlsx), "bytes": xlsx.stat().st_size}
        if pdf:
            c.require("pdf_signature", pdf.read_bytes().startswith(b"%PDF-"))
            artifact["pdf"] = {"path": str(pdf), "sha256": sha256(pdf), "bytes": pdf.stat().st_size}
        if md:
            handoff = md.read_text(encoding="utf-8")
            c.require("handoff_states_limitations", all(token in handoff for token in ["7", "23", "3", "10", "огранич"]))
            artifact["handoff"] = {"path": str(md), "sha256": sha256(md), "bytes": md.stat().st_size}

    return {
        "status": "PASS" if not c.failed else "FAIL",
        "mode": "AUTHORITIES_ONLY" if authorities_only else "FINAL_PACKAGE",
        "pass_count": len(c.passed),
        "fail_count": len(c.failed),
        "passed_checks": c.passed,
        "failed_checks": c.failed,
        "artifacts": artifact,
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--authorities-only", action="store_true")
    parser.add_argument("--write-report", action="store_true")
    args = parser.parse_args()
    report = validate(args.authorities_only)
    print(json.dumps(report, ensure_ascii=False, indent=2))
    if args.write_report:
        suffix = "AUTHORITIES" if args.authorities_only else "FINAL"
        (HERE / f"MK03_PHASE5_{suffix}_MACHINE_QA_{DATE}.json").write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    raise SystemExit(0 if report["status"] == "PASS" else 1)


if __name__ == "__main__":
    main()
