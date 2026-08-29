#!/usr/bin/env python3
from __future__ import annotations
import csv, json, re
from collections import Counter, defaultdict
from pathlib import Path

BASE = Path(__file__).resolve().parent
ROUTES = BASE / "STEP_08_REVIEW_RESOLUTION_ROUTES.tsv"
DUPS = BASE / "STEP_08_NONEXACT_DUPLICATE_HANDOFF.tsv"
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
    "S01","S02","S03","S04","S05","S06","S07","S08","S09","S10","S11","S12","S13","S14","S15","S16","S17","S18",
    "P2-01","P2-02","P2-03","P2-04"
]
SOURCE_RANK = {s:i for i,s in enumerate(SOURCE_ORDER)}
SOURCE_SEEDS = {
    "S01":"пластиковые окна","S02":"окна rehau","S03":"французские окна","S04":"окна п 44",
    "S05":"пластиковые двери","S06":"остекление балконов","S07":"остекление балкона с крышей",
    "S08":"остекление балкона п 46","S09":"пластиковые окна митино","S10":"остекление веранды",
    "S11":"алюминиевые окна","S12":"аксессуары для пластиковых окон","S13":"установка пластиковых окон",
    "S14":"ремонт пластиковых окон","S15":"цены на пластиковые окна","S16":"окна в рассрочку",
    "S17":"как выбрать пластиковые окна","S18":"пластиковые окна от производителя",
    "P2-01":"оконная фурнитура","P2-02":"панорамные окна","P2-03":"остекление балкона с выносом",
    "P2-04":"окна для частного дома",
}

BOUNDARY_ANCHORS = [
    ("Q1_GENERIC_VS_REHAU","пластиковые окна москва"),
    ("Q1_GENERIC_VS_REHAU","окна rehau москва"),
    ("Q2_PROFILE_SELECTION","какой профиль rehau выбрать"),
    ("Q2_PROFILE_SELECTION","rehau thermo окна"),
    ("Q3_BALCONY_SEGMENTATION","остекление балконов москва"),
    ("Q3_BALCONY_SEGMENTATION","теплое остекление балкона"),
    ("Q3_BALCONY_SEGMENTATION","холодное остекление балкона"),
    ("Q3_BALCONY_SEGMENTATION","остекление балкона с крышей"),
    ("Q3_BALCONY_SEGMENTATION","остекление балкона с выносом"),
    ("Q3_BALCONY_SEGMENTATION","остекление балкона п 46"),
    ("Q4_ALUMINIUM_VS_COLD","алюминиевые окна москва"),
    ("Q5_VERANDA_TERRACE_GAZEBO","остекление веранды"),
    ("Q5_VERANDA_TERRACE_GAZEBO","остекление террасы"),
    ("Q5_VERANDA_TERRACE_GAZEBO","остекление беседки"),
    ("Q6_MANUFACTURER","пластиковые окна от производителя"),
    ("Q7_GEO","пластиковые окна митино"),
    ("CORE_DOORS","пластиковые двери москва"),
    ("CORE_INSTALLATION","установка пластиковых окон москва"),
    ("CORE_SELECTION","как выбрать пластиковые окна"),
]

def read_tsv(path: Path):
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))

def source_ids(text: str):
    found = re.findall(r"(?:P2-\d{2}|S\d{2})", text or "")
    return sorted(set(found), key=lambda x: SOURCE_RANK.get(x, 999))

def primary_source(row):
    ids = source_ids(row.get("source_ids",""))
    return ids[0] if ids else "UNKNOWN"

def tokens(text: str):
    return set(re.findall(r"[0-9a-zа-яё]+", (text or "").lower()))

def centrality(row, source):
    seed = tokens(SOURCE_SEEDS.get(source,""))
    phrase = tokens(row["phrase"])
    overlap = len(seed & phrase)
    union = max(1, len(seed | phrase))
    jaccard = overlap / union
    result_backed = int(row.get("result_occurrences") or 0) > 0
    max_count = int(row.get("max_result_count") or 0)
    return (jaccard, result_backed, -abs(len(phrase)-max(1,len(seed))), max_count, -len(row["phrase"]), row["phrase"])

rows = [r for r in read_tsv(ROUTES) if r.get("search_stage_disposition") == "REVIEW_SEARCH"]
assert len(rows) == 944, f"Expected 944 REVIEW_SEARCH rows, got {len(rows)}"
reason_counts = Counter(r["corrected_reason"] for r in rows)
assert len(reason_counts) == 23, f"Expected 23 REVIEW_SEARCH reasons, got {len(reason_counts)}"

broad_reason = "RETAINED_BUSINESS_BOUNDARY_NEEDS_SEARCH"
groups = defaultdict(list)
for row in rows:
    if row["corrected_reason"] == broad_reason:
        qid = f"RS_{broad_reason}__{primary_source(row)}"
    else:
        qid = f"RS_{row['corrected_reason']}"
    groups[qid].append(row)

probes = []
question_to_probe = {}

def add_probe(query, obligation, question_id="", reason="", source="", dup="", boundary="", basis="", review_rows=0):
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
        merge("obligation_types", obligation)
        merge("evidence_question_ids", question_id)
        merge("corrected_reasons", reason)
        merge("source_ids", source)
        merge("duplicate_group_ids", dup)
        merge("step1_boundary_ids", boundary)
        merge("selection_basis", basis)
        existing["review_row_count"] = str(int(existing["review_row_count"]) + int(review_rows or 0))
        if question_id:
            question_to_probe[question_id] = existing
        return existing
    p = {
        "probe_id":"",
        "query":query,
        "obligation_types":obligation,
        "evidence_question_ids":question_id,
        "review_row_count":str(int(review_rows or 0)),
        "corrected_reasons":reason,
        "source_ids":source,
        "duplicate_group_ids":dup,
        "step1_boundary_ids":boundary,
        "selection_basis":basis,
    }
    probes.append(p)
    if question_id:
        question_to_probe[question_id] = p
    return p

for qid in sorted(groups):
    members = groups[qid]
    if qid.startswith(f"RS_{broad_reason}__"):
        src = qid.rsplit("__",1)[1]
    else:
        src_counts = Counter(primary_source(r) for r in members)
        src = sorted(src_counts, key=lambda s:(-src_counts[s], SOURCE_RANK.get(s,999), s))[0]
    rep = max(members, key=lambda r: centrality(r, src))
    add_probe(
        rep["phrase"], "REVIEW_SEARCH_REPRESENTATIVE", qid,
        reason=rep["corrected_reason"], source=src,
        basis="REASON_PLUS_SOURCE" if rep["corrected_reason"] == broad_reason else "CORRECTED_REASON",
        review_rows=len(members),
    )

dup_rows = read_tsv(DUPS)
active_dup_groups = defaultdict(list)
for r in dup_rows:
    if r.get("step08_duplicate_resolution_route") == "ORDINARY_SEARCH_BEFORE_ANY_NONEXACT_MERGE":
        active_dup_groups[r["candidate_group"]].append(r)
assert len(active_dup_groups) == 8, f"Expected 8 active duplicate groups, got {len(active_dup_groups)}"
for gid in sorted(active_dup_groups):
    members = active_dup_groups[gid]
    assert len(members) >= 2
    for r in members:
        add_probe(
            r["phrase"], "NONEXACT_DUPLICATE_VARIANT",
            question_id=f"DUPQ_{gid}",
            reason=r.get("corrected_reason",""),
            source="|".join(source_ids(r.get("source_ids",""))),
            dup=gid, basis="ACTIVE_DUPLICATE_VARIANT",
        )

for boundary, query in BOUNDARY_ANCHORS:
    add_probe(query, "STEP1_BOUNDARY_OR_CORE_ANCHOR", question_id=f"BOUNDARY_{boundary}",
              boundary=boundary, basis="STEP1_FIXED_ANCHOR")

order = {"REVIEW_SEARCH_REPRESENTATIVE":0, "NONEXACT_DUPLICATE_VARIANT":1, "STEP1_BOUNDARY_OR_CORE_ANCHOR":2}
probes.sort(key=lambda p:(min(order.get(x,9) for x in p["obligation_types"].split("|")), p["query"].casefold()))
for i,p in enumerate(probes,1):
    p["probe_id"] = f"SP09-{i:03d}"

question_to_probe = {}
for p in probes:
    for qid in filter(None,p["evidence_question_ids"].split("|")):
        question_to_probe[qid] = p

coverage_rows = []
for r in rows:
    src = primary_source(r)
    qid = f"RS_{broad_reason}__{src}" if r["corrected_reason"] == broad_reason else f"RS_{r['corrected_reason']}"
    p = question_to_probe.get(qid)
    if not p:
        raise AssertionError(f"No representative probe for {qid}: {r['phrase']}")
    direct = r["phrase"].casefold() == p["query"].casefold()
    coverage_rows.append({
        "phrase":r["phrase"],
        "corrected_reason":r["corrected_reason"],
        "source_ids":r.get("source_ids",""),
        "evidence_question_id":qid,
        "representative_probe_id":p["probe_id"],
        "representative_query":p["query"],
        "coverage_status":"DIRECT_PROBE" if direct else "REPRESENTED_BY_QUESTION_UNRESOLVED",
    })

unique_queries = len({p["query"].casefold() for p in probes})
assert unique_queries == len(probes), "Probe query dedupe failure"
coverage_ok = len(coverage_rows) == 944 and all(r["representative_probe_id"] for r in coverage_rows)
cap_ok = len(probes) <= MAX_REQUESTS
estimated_cost = round(len(probes) * UNIT_COST_RUB, 3)
budget_ok = estimated_cost <= MAX_COST_RUB + 1e-9

with MANIFEST.open("w",encoding="utf-8",newline="") as f:
    fields = ["probe_id","query","obligation_types","evidence_question_ids","review_row_count","corrected_reasons","source_ids","duplicate_group_ids","step1_boundary_ids","selection_basis"]
    w=csv.DictWriter(f,fieldnames=fields,delimiter="\t",lineterminator="\n"); w.writeheader(); w.writerows(probes)
with COVERAGE.open("w",encoding="utf-8",newline="") as f:
    fields=list(coverage_rows[0].keys()); w=csv.DictWriter(f,fieldnames=fields,delimiter="\t",lineterminator="\n"); w.writeheader(); w.writerows(coverage_rows)

qa = {
    "status":"PASS" if (coverage_ok and cap_ok and budget_ok) else "FAIL",
    "review_search_rows":len(rows),
    "review_search_reasons":len(reason_counts),
    "review_search_reason_counts":dict(sorted(reason_counts.items())),
    "evidence_question_count":len(groups),
    "active_duplicate_groups":len(active_dup_groups),
    "probe_count":len(probes),
    "max_requests_ceiling":MAX_REQUESTS,
    "unit_cost_rub":UNIT_COST_RUB,
    "estimated_cost_rub":estimated_cost,
    "max_cost_rub":MAX_COST_RUB,
    "coverage_rows":len(coverage_rows),
    "coverage_complete":coverage_ok,
    "request_cap_ok":cap_ok,
    "budget_cap_ok":budget_ok,
    "provider_execution_allowed":bool(coverage_ok and cap_ok and budget_ok),
    "provider_requests_executed_during_build":0,
    "provider_cost_rub_during_build":0,
    "region":REGION,
}
QA.write_text(json.dumps(qa,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")

if qa["provider_execution_allowed"]:
    payload = {
        "action":"start",
        "jobId":JOB_ID,
        "queries":[p["query"] for p in probes],
        "searchType":"SEARCH_TYPE_RU",
        "region":REGION,
        "groupsOnPage":10,
        "maxRequests":len(probes),
        "maxCostRub":MAX_COST_RUB,
        "confirmBillable":True,
    }
    COMMAND.write_text("SEARCH_BATCH_API_V1\n"+json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
else:
    COMMAND.write_text(
        "BLOCKED_BEFORE_PROVIDER\n"
        f"probe_count={len(probes)}\nmax_requests={MAX_REQUESTS}\n"
        f"estimated_cost_rub={estimated_cost}\nmax_cost_rub={MAX_COST_RUB}\n",
        encoding="utf-8",
    )

recon = f"""# KW-001 / OKNO-MSK — Step 09 Search probe manifest reconciliation

Date: 2026-08-29

```text
REVIEW_SEARCH_ROWS = {len(rows)}
REVIEW_SEARCH_REASONS = {len(reason_counts)}
EVIDENCE_QUESTIONS = {len(groups)}
ACTIVE_DUPLICATE_GROUPS = {len(active_dup_groups)}
PROBE_COUNT = {len(probes)}
MAX_REQUESTS = {MAX_REQUESTS}
UNIT_COST_RUB = {UNIT_COST_RUB}
ESTIMATED_COST_RUB = {estimated_cost}
MAX_COST_RUB = {MAX_COST_RUB}
COVERAGE_COMPLETE = {str(coverage_ok).lower()}
REQUEST_CAP_OK = {str(cap_ok).lower()}
BUDGET_CAP_OK = {str(budget_ok).lower()}
PROVIDER_EXECUTION_ALLOWED = {str(qa['provider_execution_allowed']).lower()}
PROVIDER_REQUESTS_EXECUTED_DURING_BUILD = 0
PROVIDER_COST_RUB_DURING_BUILD = 0
```

Every `REVIEW_SEARCH` row is preserved in `STEP_09_REVIEW_SEARCH_COVERAGE.tsv`.
Rows not directly probed stay explicitly `REPRESENTED_BY_QUESTION_UNRESOLVED`; this manifest does not resolve them by inference.
The broad boundary reason is split by acquisition source so its 575 rows are not collapsed into one query.
All eight active non-exact duplicate groups contribute both observed variants before any merge.
The provider command is emitted only if the 80-request and 39.04-RUB hard gates pass.
"""
RECON.write_text(recon,encoding="utf-8")

if not qa["provider_execution_allowed"]:
    raise SystemExit(f"STEP09_MANIFEST_BLOCKED: probes={len(probes)} estimated_cost={estimated_cost}")
print(json.dumps(qa,ensure_ascii=False,indent=2))
