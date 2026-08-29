#!/usr/bin/env python3
from __future__ import annotations

import csv
import hashlib
import json
import re
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROUTES = BASE / "STEP_08_REVIEW_RESOLUTION_ROUTES.tsv"
DUPS = BASE / "STEP_08_NONEXACT_DUPLICATE_HANDOFF.tsv"
SEMANTIC_QA = BASE / "STEP_09_INITIAL_TRANCHE_SEMANTIC_QA.json"
MANIFEST = BASE / "STEP_09_SEARCH_PROBE_MANIFEST.tsv"
COVERAGE = BASE / "STEP_09_REVIEW_SEARCH_COVERAGE.tsv"
QA = BASE / "STEP_09_SEARCH_PROBE_MANIFEST_QA.json"
COMMAND = BASE / "STEP_09_SEARCH_BATCH_START_COMMAND.txt"
RECON = BASE / "STEP_09_SEARCH_PROBE_MANIFEST_RECONCILIATION.md"

MAX_REQUESTS = 80
MAX_COST_RUB = 39.04
UNIT_COST_RUB = 0.488
REGION = "213"
JOB_ID = "kw001-okno-msk-search-step09-20260829"

SOURCE_ORDER = [
    "S01", "S02", "S03", "S04", "S05", "S06", "S07", "S08", "S09", "S10", "S11", "S12", "S13", "S14", "S15", "S16", "S17", "S18",
    "P2-01", "P2-02", "P2-03", "P2-04",
]
SOURCE_RANK = {s: i for i, s in enumerate(SOURCE_ORDER)}
SOURCE_SEEDS = {
    "S01": "пластиковые окна", "S02": "окна rehau", "S03": "французские окна", "S04": "окна п 44",
    "S05": "пластиковые двери", "S06": "остекление балконов", "S07": "остекление балкона с крышей",
    "S08": "остекление балкона п 46", "S09": "пластиковые окна митино", "S10": "остекление веранды",
    "S11": "алюминиевые окна", "S12": "аксессуары для пластиковых окон", "S13": "установка пластиковых окон",
    "S14": "ремонт пластиковых окон", "S15": "цены на пластиковые окна", "S16": "окна в рассрочку",
    "S17": "как выбрать пластиковые окна", "S18": "пластиковые окна от производителя",
    "P2-01": "оконная фурнитура", "P2-02": "панорамные окна", "P2-03": "остекление балкона с выносом",
    "P2-04": "окна для частного дома",
}

# These are direct comparison/control queries, not inferred representatives of an acquisition source.
BOUNDARY_ANCHORS = [
    ("Q1_GENERIC_VS_REHAU", "пластиковые окна москва"),
    ("Q1_GENERIC_VS_REHAU", "окна rehau москва"),
    ("Q2_PROFILE_SELECTION", "какой профиль rehau выбрать"),
    ("Q2_PROFILE_SELECTION", "rehau thermo окна"),
    ("Q3_BALCONY_SEGMENTATION", "остекление балконов москва"),
    ("Q3_BALCONY_SEGMENTATION", "теплое остекление балкона"),
    ("Q3_BALCONY_SEGMENTATION", "холодное остекление балкона"),
    ("Q3_BALCONY_SEGMENTATION", "остекление балкона с крышей"),
    ("Q3_BALCONY_SEGMENTATION", "остекление балкона с выносом"),
    ("Q3_BALCONY_SEGMENTATION", "остекление балкона п 46"),
    ("Q4_ALUMINIUM_VS_COLD", "алюминиевые окна москва"),
    ("Q5_VERANDA_TERRACE_GAZEBO", "остекление веранды"),
    ("Q5_VERANDA_TERRACE_GAZEBO", "остекление террасы"),
    ("Q5_VERANDA_TERRACE_GAZEBO", "остекление беседки"),
    ("Q6_MANUFACTURER", "пластиковые окна от производителя"),
    ("Q7_GEO", "пластиковые окна митино"),
    ("CORE_DOORS", "пластиковые двери москва"),
    ("CORE_INSTALLATION", "установка пластиковых окон москва"),
    ("CORE_SELECTION", "как выбрать пластиковые окна"),
]


def read_tsv(path: Path):
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def source_ids(text: str):
    found = re.findall(r"(?:P2-\d{2}|S\d{2})", text or "")
    return sorted(set(found), key=lambda x: SOURCE_RANK.get(x, 999))


def primary_source(row):
    ids = source_ids(row.get("source_ids", ""))
    return ids[0] if ids else "UNKNOWN"


def tokens(text: str):
    return set(re.findall(r"[0-9a-zа-яё]+", (text or "").lower()))


def sampling_score(row, source):
    """Sampling diversity heuristic only. It MUST NOT be interpreted as intent/cluster evidence."""
    seed = tokens(SOURCE_SEEDS.get(source, ""))
    phrase = tokens(row["phrase"])
    overlap = len(seed & phrase)
    union = max(1, len(seed | phrase))
    lexical_jaccard = overlap / union
    result_backed = int(row.get("result_occurrences") or 0) > 0
    max_count = int(row.get("max_result_count") or 0)
    return (lexical_jaccard, result_backed, max_count, -len(row["phrase"]), row["phrase"])


review_rows = [r for r in read_tsv(ROUTES) if r.get("search_stage_disposition") == "REVIEW_SEARCH"]
assert len(review_rows) == 944, f"Expected 944 REVIEW_SEARCH rows, got {len(review_rows)}"
reason_counts = Counter(r["corrected_reason"] for r in review_rows)
assert len(reason_counts) == 23, f"Expected 23 REVIEW_SEARCH reasons, got {len(reason_counts)}"

# IMPORTANT CORRECTION:
# corrected_reason and acquisition source are sampling strata only.
# They are NOT evidence families, SERP clusters, user-task clusters, or transfer authorities.
broad_reason = "RETAINED_BUSINESS_BOUNDARY_NEEDS_SEARCH"
sampling_strata = defaultdict(list)
for row in review_rows:
    if row["corrected_reason"] == broad_reason:
        sid = f"SAMPLE_{broad_reason}__{primary_source(row)}"
    else:
        sid = f"SAMPLE_{row['corrected_reason']}"
    sampling_strata[sid].append(row)

probes = []


def add_probe(query, role, sampling_stratum_id="", reason="", source="", dup="", boundary="", basis="", stratum_rows=0):
    query = " ".join((query or "").split()).strip()
    if not query:
        raise AssertionError("Empty query")
    existing = next((p for p in probes if p["query"].casefold() == query.casefold()), None)
    if existing:
        def merge(field, value):
            if not value:
                return
            current = [x for x in existing[field].split("|") if x]
            for x in str(value).split("|"):
                if x and x not in current:
                    current.append(x)
            existing[field] = "|".join(current)
        merge("probe_roles", role)
        merge("sampling_stratum_ids", sampling_stratum_id)
        merge("corrected_reasons", reason)
        merge("source_ids", source)
        merge("duplicate_group_ids", dup)
        merge("step1_boundary_ids", boundary)
        merge("selection_basis", basis)
        existing["sampling_stratum_row_count"] = str(int(existing["sampling_stratum_row_count"]) + int(stratum_rows or 0))
        return existing
    p = {
        "probe_id": "",
        "query": query,
        "probe_roles": role,
        "sampling_stratum_ids": sampling_stratum_id,
        "sampling_stratum_row_count": str(int(stratum_rows or 0)),
        "corrected_reasons": reason,
        "source_ids": source,
        "duplicate_group_ids": dup,
        "step1_boundary_ids": boundary,
        "selection_basis": basis,
        "semantic_qa_status": "",
        "pre_serp_transfer_allowed": "false",
    }
    probes.append(p)
    return p


# 40 diverse REVIEW_SEARCH direct samples. No non-probed row is represented by these samples.
for sid in sorted(sampling_strata):
    members = sampling_strata[sid]
    if sid.startswith(f"SAMPLE_{broad_reason}__"):
        src = sid.rsplit("__", 1)[1]
    else:
        src_counts = Counter(primary_source(r) for r in members)
        src = sorted(src_counts, key=lambda s: (-src_counts[s], SOURCE_RANK.get(s, 999), s))[0]
    sample = max(members, key=lambda r: sampling_score(r, src))
    add_probe(
        sample["phrase"],
        "REVIEW_STRATIFIED_SAMPLE",
        sampling_stratum_id=sid,
        reason=sample["corrected_reason"],
        source=src,
        basis="DIVERSITY_SAMPLE_ONLY__NOT_INTENT_REPRESENTATIVE",
        stratum_rows=len(members),
    )

# All active duplicate variants remain mandatory direct comparisons.
dup_rows = read_tsv(DUPS)
active_dup_groups = defaultdict(list)
for row in dup_rows:
    if row.get("step08_duplicate_resolution_route") == "ORDINARY_SEARCH_BEFORE_ANY_NONEXACT_MERGE":
        active_dup_groups[row["candidate_group"]].append(row)
assert len(active_dup_groups) == 8, f"Expected 8 active duplicate groups, got {len(active_dup_groups)}"
for gid in sorted(active_dup_groups):
    members = active_dup_groups[gid]
    assert len(members) >= 2
    for row in members:
        add_probe(
            row["phrase"],
            "NONEXACT_DUPLICATE_VARIANT",
            reason=row.get("corrected_reason", ""),
            source="|".join(source_ids(row.get("source_ids", ""))),
            dup=gid,
            basis="DIRECT_DUPLICATE_VARIANT_COMPARISON",
        )

# Declared Step-01/core comparison anchors.
for boundary, query in BOUNDARY_ANCHORS:
    add_probe(
        query,
        "STEP1_BOUNDARY_OR_CORE_ANCHOR",
        boundary=boundary,
        basis="DIRECT_BOUNDARY_OR_CONTROL_QUERY",
    )

role_order = {"REVIEW_STRATIFIED_SAMPLE": 0, "NONEXACT_DUPLICATE_VARIANT": 1, "STEP1_BOUNDARY_OR_CORE_ANCHOR": 2}
probes.sort(key=lambda p: (min(role_order.get(x, 9) for x in p["probe_roles"].split("|")), p["query"].casefold()))
for index, probe in enumerate(probes, 1):
    probe["probe_id"] = f"SP09-{index:03d}"

# Manual semantic QA is bound to the exact ordered query list. Machine selection cannot self-accept.
semantic_qa = json.loads(SEMANTIC_QA.read_text(encoding="utf-8"))
ordered_queries = [p["query"] for p in probes]
query_hash = hashlib.sha256(json.dumps(ordered_queries, ensure_ascii=False, separators=(",", ":")).encode("utf-8")).hexdigest()
semantic_qa_pass = (
    semantic_qa.get("status") == "PASS_AS_INITIAL_BOUNDED_TRANCHE_ONLY"
    and int(semantic_qa.get("reviewed_probe_count", -1)) == len(probes)
    and semantic_qa.get("ordered_query_list_sha256") == query_hash
    and semantic_qa.get("pre_serp_transfer_allowed") is False
    and semantic_qa.get("full_944_serp_coverage_claim_allowed") is False
)
for probe in probes:
    probe["semantic_qa_status"] = "PASS_INITIAL_TRANCHE_ONLY" if semantic_qa_pass else "FAIL_OR_STALE"

# REVIEW_SEARCH traceability: only exact queried phrases are DIRECT_PROBE.
# Every other row remains unresolved. No pre-SERP evidence transfer is encoded.
probe_by_query = {p["query"].casefold(): p for p in probes}
coverage_rows = []
for row in review_rows:
    probe = probe_by_query.get(row["phrase"].casefold())
    coverage_rows.append({
        "phrase": row["phrase"],
        "corrected_reason": row["corrected_reason"],
        "source_ids": row.get("source_ids", ""),
        "direct_probe_id": probe["probe_id"] if probe else "",
        "direct_query": probe["query"] if probe else "",
        "coverage_state": "DIRECT_PROBE" if probe else "UNRESOLVED_UNPROBED",
        "pre_serp_transfer_allowed": "false",
    })

direct_review_rows = sum(1 for row in coverage_rows if row["coverage_state"] == "DIRECT_PROBE")
unresolved_review_rows = len(coverage_rows) - direct_review_rows
traceability_complete = len(coverage_rows) == 944
pre_serp_transfer_links = 0

unique_queries = len({p["query"].casefold() for p in probes})
assert unique_queries == len(probes), "Probe query dedupe failure"
cap_ok = len(probes) <= MAX_REQUESTS
estimated_cost = round(len(probes) * UNIT_COST_RUB, 3)
budget_ok = estimated_cost <= MAX_COST_RUB + 1e-9
provider_allowed = bool(traceability_complete and cap_ok and budget_ok and semantic_qa_pass and pre_serp_transfer_links == 0)

with MANIFEST.open("w", encoding="utf-8", newline="") as f:
    fields = [
        "probe_id", "query", "probe_roles", "sampling_stratum_ids", "sampling_stratum_row_count",
        "corrected_reasons", "source_ids", "duplicate_group_ids", "step1_boundary_ids", "selection_basis",
        "semantic_qa_status", "pre_serp_transfer_allowed",
    ]
    writer = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(probes)

with COVERAGE.open("w", encoding="utf-8", newline="") as f:
    fields = list(coverage_rows[0].keys())
    writer = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
    writer.writeheader()
    writer.writerows(coverage_rows)

qa = {
    "status": "PASS_INITIAL_TRANCHE_GATE" if provider_allowed else "FAIL",
    "review_search_rows": len(review_rows),
    "review_search_reasons": len(reason_counts),
    "review_search_reason_counts": dict(sorted(reason_counts.items())),
    "review_sampling_strata_count": len(sampling_strata),
    "active_duplicate_groups": len(active_dup_groups),
    "probe_count": len(probes),
    "direct_review_search_rows": direct_review_rows,
    "unresolved_unprobed_review_search_rows": unresolved_review_rows,
    "traceability_rows": len(coverage_rows),
    "traceability_complete": traceability_complete,
    "full_serp_evidence_coverage": False,
    "pre_serp_transfer_links": pre_serp_transfer_links,
    "semantic_sample_qa_pass": semantic_qa_pass,
    "ordered_query_list_sha256": query_hash,
    "max_requests_ceiling": MAX_REQUESTS,
    "unit_cost_rub": UNIT_COST_RUB,
    "estimated_cost_rub": estimated_cost,
    "max_cost_rub": MAX_COST_RUB,
    "request_cap_ok": cap_ok,
    "budget_cap_ok": budget_ok,
    "provider_execution_allowed": provider_allowed,
    "provider_execution_scope": "INITIAL_BOUNDED_TRANCHE_ONLY",
    "provider_requests_executed_during_build": 0,
    "provider_cost_rub_during_build": 0,
    "region": REGION,
}
QA.write_text(json.dumps(qa, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

if provider_allowed:
    payload = {
        "action": "start",
        "jobId": JOB_ID,
        "queries": ordered_queries,
        "searchType": "SEARCH_TYPE_RU",
        "region": REGION,
        "groupsOnPage": 10,
        "maxRequests": len(probes),
        "maxCostRub": MAX_COST_RUB,
        "confirmBillable": True,
    }
    COMMAND.write_text("SEARCH_BATCH_API_V1\n" + json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
else:
    COMMAND.write_text(
        "BLOCKED_BEFORE_PROVIDER\n"
        f"probe_count={len(probes)}\n"
        f"semantic_sample_qa_pass={str(semantic_qa_pass).lower()}\n"
        f"traceability_complete={str(traceability_complete).lower()}\n"
        f"estimated_cost_rub={estimated_cost}\n",
        encoding="utf-8",
    )

recon = f"""# KW-001 / OKNO-MSK — Step 09 initial Search tranche reconciliation\n\nDate: 2026-08-29\nStatus: **CORRECTED AFTER SEMANTIC-MANIFEST AUDIT**\n\n```text\nREVIEW_SEARCH_ROWS = {len(review_rows)}\nREVIEW_SEARCH_REASONS = {len(reason_counts)}\nREVIEW_SAMPLING_STRATA = {len(sampling_strata)}\nACTIVE_DUPLICATE_GROUPS = {len(active_dup_groups)}\nPROBE_COUNT = {len(probes)}\nDIRECT_REVIEW_SEARCH_ROWS = {direct_review_rows}\nUNRESOLVED_UNPROBED_REVIEW_SEARCH_ROWS = {unresolved_review_rows}\nTRACEABILITY_COMPLETE = {str(traceability_complete).lower()}\nFULL_SERP_EVIDENCE_COVERAGE = false\nPRE_SERP_TRANSFER_LINKS = 0\nSEMANTIC_SAMPLE_QA_PASS = {str(semantic_qa_pass).lower()}\nMAX_REQUESTS = {MAX_REQUESTS}\nESTIMATED_COST_RUB = {estimated_cost}\nMAX_COST_RUB = {MAX_COST_RUB}\nPROVIDER_EXECUTION_ALLOWED = {str(provider_allowed).lower()}\nPROVIDER_EXECUTION_SCOPE = INITIAL_BOUNDED_TRANCHE_ONLY\nPROVIDER_REQUESTS_EXECUTED_DURING_BUILD = 0\nPROVIDER_COST_RUB_DURING_BUILD = 0\n```\n\n## Corrected interpretation\n\nThe previous builder incorrectly treated `corrected_reason` and acquisition source as if they created transferable SERP evidence families. They do not.\n\nThe 40 REVIEW_SEARCH selections are now only **stratified direct samples** used to obtain diverse first-tranche evidence. They may resolve the exact queried phrase and help identify further questions, but they do not pre-resolve or represent the other rows in the same cleanup-reason/source stratum.\n\nEvery non-probed REVIEW_SEARCH row is explicitly `UNRESOLVED_UNPROBED`. Evidence transfer may occur only after observed SERP evidence and a separate analytical transfer decision.\n\nAll eight active non-exact duplicate groups still contribute both variants for direct comparison. Step-01/core anchors remain direct comparison controls.\n\n`traceability_complete=true` means all 944 rows are still present in the ledger. It does **not** mean full Search evidence coverage.\n"""
RECON.write_text(recon, encoding="utf-8")

if not provider_allowed:
    raise SystemExit(2)

print(json.dumps(qa, ensure_ascii=False, indent=2))
