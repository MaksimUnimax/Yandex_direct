#!/usr/bin/env python3
"""Apply owner-authorized Step20 defect corrections to derived Step19 data and builder."""
from __future__ import annotations

import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "step19_correction_materialized"


def read_tsv(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def write_tsv(path: Path, rows):
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), delimiter="\t", extrasaction="ignore")
        w.writeheader(); w.writerows(rows)


def read_csv(path: Path):
    with path.open(encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows):
    with path.open("w", encoding="utf-8-sig", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), extrasaction="ignore")
        w.writeheader(); w.writerows(rows)


def sha(path: Path):
    h = hashlib.sha256(); h.update(path.read_bytes()); return h.hexdigest()


def apply_overlay(rows, overlay, key="action_id"):
    ov = {r[key]: r for r in overlay}
    found = set()
    for row in rows:
        if row.get(key) in ov:
            found.add(row[key])
            for k, v in ov[row[key]].items():
                if k != key and v != "":
                    row[k] = v
    assert found == set(ov), (found, set(ov))
    return rows


action_overlay = read_tsv(ROOT / "STEP_19_STEP20_ACTION_VIEW_CORRECTION_OVERLAY.tsv")
priority_overlay = read_tsv(ROOT / "STEP_19_STEP20_PRIORITY_VIEW_CORRECTION_OVERLAY.tsv")
step18_overlay = read_tsv(ROOT / "STEP_18_STEP20_CURRENT_CONTENT_CORRECTION_OVERLAY.tsv")
assert {r["action_id"] for r in action_overlay} == {"S18-A012", "S18-A027"}
assert {r["action_id"] for r in priority_overlay} == {"S18-A012", "S18-A027"}
assert {r["action_id"] for r in step18_overlay} == {"S18-A012", "S18-A027"}

action_path = OUT / "STEP_19_05_PAGE_ACTION_MAP.tsv"
priority_path = OUT / "STEP_19_07_PRIORITY_ACTION_PLAN.tsv"
cal_path = OUT / "STEP_19_EXECUTION_CALIBRATION_BOARD_112.csv"
actions = apply_overlay(read_tsv(action_path), action_overlay)
priority = apply_overlay(read_tsv(priority_path), priority_overlay)
write_tsv(action_path, actions)
write_tsv(priority_path, priority)

corr = {r["action_id"]: r for r in step18_overlay}
cal = read_csv(cal_path)
touched = set()
for row in cal:
    aid = row.get("source_action_id")
    if aid in corr:
        c = corr[aid]; touched.add(aid)
        row["what_to_do"] = c["description"]
        row["dependency_role"] = c["dependency_role"]
        row["depends_on_action_ids"] = c["depends_on_action_ids"]
        row["recheck_or_blocker"] = c["recheck_trigger"]
        row["claim_boundary"] = c["limitations"]
assert touched == {"S18-A012", "S18-A027"}
write_csv(cal_path, cal)

a_by = {r["action_id"]: r for r in actions}
p_by = {r["action_id"]: r for r in priority}
aov = {r["action_id"]: r for r in action_overlay}
pov = {r["action_id"]: r for r in priority_overlay}
for aid in ("S18-A012", "S18-A027"):
    for field in ("priority", "client_action", "target_page_or_scope", "dependency_or_sequence", "do_not_do_boundary", "verification_or_recheck", "evidence_authority"):
        assert a_by[aid][field] == aov[aid][field], (aid, field)
    for field in ("analytical_priority", "client_readable_reason", "work_package_trace", "implementation_owner", "effort", "capacity", "expected_implementation_priority", "scheduling_state", "measurement_class_or_rule"):
        assert p_by[aid][field] == pov[aid][field], (aid, field)
cal_by = {r["source_action_id"]: r for r in cal if r["source_action_id"] in corr}
assert cal_by["S18-A012"]["what_to_do"] == corr["S18-A012"]["description"]
assert cal_by["S18-A027"]["what_to_do"] == corr["S18-A027"]["description"]
assert cal_by["S18-A027"]["depends_on_action_ids"] == "S18-A009"

qa_path = OUT / "STEP_19_CORRECTION_DATA_QA.json"
qa = json.loads(qa_path.read_text(encoding="utf-8"))
qa["step20_defect_correction"] = {
    "D20-002": "APPLIED_TO_A012_ACTION_PRIORITY_CALIBRATION",
    "D20-003": "APPLIED_TO_A027_ACTION_PRIORITY_CALIBRATION",
    "authority_overlay": "STEP_18_STEP20_CURRENT_CONTENT_CORRECTION_OVERLAY.tsv",
}
for p in (action_path, priority_path, cal_path):
    qa["outputs"][p.name] = {"bytes": p.stat().st_size, "sha256": sha(p)}
qa_path.write_text(json.dumps(qa, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

builder = ROOT / "step19_build_physical_client_package.py"
s = builder.read_text(encoding="utf-8")
if "from datetime import datetime" not in s:
    s = s.replace("from __future__ import annotations\n", "from __future__ import annotations\n\nfrom datetime import datetime\n")
s = s.replace('ws["A1"] = "OKNO-MSK — Step19 corrected client workbook"', 'ws["A1"] = "TEST/DEMO CASE — OKNO-MSK — Step19 corrected client workbook"')
if 'ws["A2"] = "TEST/DEMO CASE — mock commercial rehearsal; not an actual paid-client engagement."' not in s:
    marker = 'ws.row_dimensions[1].height = 28'
    patch = '''ws.row_dimensions[1].height = 28\nws.merge_cells("A2:H2")\nws["A2"] = "TEST/DEMO CASE — mock commercial rehearsal; not an actual paid-client engagement."\nws["A2"].font = Font(bold=True, color="9C0006")\nws["A2"].fill = warn_fill\nws["A2"].alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)\nws.row_dimensions[2].height = 34'''
    s = s.replace(marker, patch)
if 'wb.properties.title = "TEST/DEMO CASE — OKNO-MSK"' not in s:
    s = s.replace('wb = Workbook()\n', 'wb = Workbook()\nwb.properties.title = "TEST/DEMO CASE — OKNO-MSK"\nwb.properties.subject = "Mock commercial rehearsal / demonstration analysis"\nwb.properties.creator = ""\nwb.properties.lastModifiedBy = ""\n')

if 'doc.core_properties.title = "TEST/DEMO CASE — OKNO-MSK"' not in s:
    core = '''doc=Document()\ndoc.core_properties.title = "TEST/DEMO CASE — OKNO-MSK"\ndoc.core_properties.subject = "Mock commercial rehearsal / demonstration analysis"\ndoc.core_properties.author = ""\ndoc.core_properties.last_modified_by = ""\ndoc.core_properties.comments = ""\ndoc.core_properties.created = datetime(2026, 9, 3, 0, 0, 0)\ndoc.core_properties.modified = datetime(2026, 9, 3, 0, 0, 0)'''
    s = s.replace('doc=Document()', core)
else:
    s = s.replace('doc.core_properties.creator = ""', 'doc.core_properties.author = ""')
    s = s.replace('datetime(2026, 9, 3, tzinfo=timezone.utc)', 'datetime(2026, 9, 3, 0, 0, 0)')
    if 'doc.core_properties.comments = ""' not in s:
        s = s.replace('doc.core_properties.last_modified_by = ""', 'doc.core_properties.last_modified_by = ""\ndoc.core_properties.comments = ""')
if 'r=p.add_run("TEST/DEMO CASE — mock commercial rehearsal; not an actual paid-client engagement.")' not in s:
    marker = 'p=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER; p.add_run("Исправленный клиентский отчёт Step19").italic=True'
    patch = marker + '\np=doc.add_paragraph(); p.alignment=WD_ALIGN_PARAGRAPH.CENTER\nr=p.add_run("TEST/DEMO CASE — mock commercial rehearsal; not an actual paid-client engagement."); r.bold=True; r.font.color.rgb=RGBColor(156,0,6)'
    s = s.replace(marker, patch)
s = s.replace('story=[P("OKNO-MSK","CTitle"),P("Семантика, архитектура страниц и план действий под Yandex Search + bounded Search-vs-AI диагностику","CSub"),Spacer(1,6*mm)]', 'story=[P("TEST/DEMO CASE — OKNO-MSK","CTitle"),P("Mock commercial rehearsal; not an actual paid-client engagement.","CSub"),P("Семантика, архитектура страниц и план действий под Yandex Search + bounded Search-vs-AI диагностику","CSub"),Spacer(1,6*mm)]')
if '"distribution_identity"' not in s:
    s = s.replace('"non_fabrication":{"new_provider_calls":0,"new_paid_cost_rub":0.0,"committed_schedule":False,"numeric_targets_invented":False},', '"non_fabrication":{"new_provider_calls":0,"new_paid_cost_rub":0.0,"committed_schedule":False,"numeric_targets_invented":False},\n    "distribution_identity":{"test_demo_case":True,"mock_commercial_rehearsal":True,"actual_paid_client_engagement":False},')
for marker in (
    'TEST/DEMO CASE — OKNO-MSK',
    'doc.core_properties.author = ""',
    'doc.core_properties.comments = ""',
    'doc.core_properties.created = datetime(2026, 9, 3, 0, 0, 0)',
    '"distribution_identity"',
):
    assert marker in s, marker
builder.write_text(s, encoding="utf-8")

print("STEP18_STEP19_APPLY_STEP20_CORRECTIONS_PASS")
