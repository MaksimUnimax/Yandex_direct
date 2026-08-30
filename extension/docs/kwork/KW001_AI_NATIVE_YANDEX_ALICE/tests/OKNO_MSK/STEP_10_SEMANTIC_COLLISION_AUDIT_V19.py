#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
import re
from collections import Counter

import STEP_10_SEMANTIC_COLLISION_AUDIT as old
import STEP_10_SEMANTIC_COLLISION_AUDIT_V15 as v15


def n(s: str) -> str:
    return " ".join((s or "").casefold().replace("ё", "е").split())


def anym(p: str, markers) -> bool:
    return any(m in p for m in markers)


def audit_v19(r: dict[str, str]) -> list[tuple[str, str]]:
    cid = r["cluster_id"]
    p = n(r["phrase"])
    out: list[tuple[str, str]] = []

    for code, reason in v15.audit_v15(r):
        # Manually adjudicated false positives in the inherited lexical audit.
        if code == "PRIVATE_HOUSE_SELECTION_TOKEN_MISMATCH" and anym(p, ("выбираем", "выбрать", "выбор", "форм")):
            continue
        if code == "PRIVATE_HOUSE_PRODUCT_CONTEXT_MISMATCH" and anym(p, ("частных домов", "частном доме")):
            continue
        if code == "PRIVATE_HOUSE_REQUIREMENTS_WITHOUT_REQUIREMENT_MARKER" and anym(p, ("котельн", "газов", "площадь")):
            continue
        if code == "V15_HARDWARE_TOKEN_MISMATCH" and anym(p, ("накладк", "уплотн", "замок", "створк", "решетк")):
            continue
        if code == "TASK_TOKEN_MISMATCH":
            if cid == "OUTSIDE_REAL_ESTATE" and anym(p, ("кв ", "одноэтажн", "пристройк", "спальн")):
                continue
            if cid == "WINDOW_HARDWARE" and anym(p, ("решетк", "створк", "замок", "накладк", "уплотн")):
                continue
            if cid == "WINDOW_DIMENSIONS_INFO":
                dim_pattern = bool(re.search(r"\b\d+(?:[.,]\d+)?\s*(?:на|x|х)\s*\d+(?:[.,]\d+)?\b", p))
                pan_decimal = bool(re.search(r"(?:панорам\w*\s+окн\w*|окн\w*\s+панорам\w*)\s+\d+[.,]\d+\b", p))
                if dim_pattern or pan_decimal:
                    continue
        if code == "PANORAMIC_WITHOUT_PURCHASE_SIGNAL" and anym(
            p,
            (
                "раздвиж", "в пол", "открывающ", "с двер", "стеклопак", "треугольн", "стеклянн",
                "на балкон", "на лоджи", "на террас", "под ключ", "производ", "москв", "подмосков",
                "для загородного дома", "для частного дома", "в частном доме",
            ),
        ):
            continue
        out.append((code, reason))

    # V19 non-repeat controls for the real errors found during manual adjudication.
    if cid == "WINDOW_DIMENSIONS_INFO" and anym(p, ("готов", "москит", "антикошка", "сетка на", "сетку на")):
        out.append(("V19_DIMENSIONS_SWALLOWED_PRODUCT_OR_ACCESSORY", "dimension cluster swallowed a ready-made product or mosquito/protection accessory"))
    if cid == "WINDOW_REPAIR" and anym(p, ("отмыть", "очистить", "жидкий пластик", "средство для ремонта")):
        out.append(("V19_REPAIR_SWALLOWED_CARE_OR_MATERIAL", "repair service swallowed cleaning/care or repair-material demand"))
    if cid == "PRIVATE_HOUSE_WINDOWS_COMMERCIAL" and anym(p, ("панорам", "француз", "для крыши", "мансард", "формы")):
        out.append(("V19_PRIVATE_HOUSE_SWALLOWED_SPECIFIC_TASK", "generic private-house cluster swallowed a more specific window type/roof/types task"))
    if cid == "FRENCH_WINDOWS_COMMERCIAL" and anym(p, ("замена", "заменить", "поменять", "ремонт", "регулир")):
        out.append(("V19_FRENCH_PRODUCT_SWALLOWED_ACTION", "French product cluster swallowed an explicit replacement/repair action"))

    return out


def main() -> None:
    with old.ASSIGN.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))

    flagged = []
    counts = Counter()
    for r in rows:
        if r["input_disposition"] not in {"CORE_CANDIDATE", "REVIEW_SEARCH"}:
            continue
        for code, reason in audit_v19(r):
            counts[code] += 1
            flagged.append({
                "collision_code": code,
                "phrase": r["phrase"],
                "cluster_id": r["cluster_id"],
                "user_task": r["user_task"],
                "evidence_state": r["cluster_evidence_state"],
                "step09_probe_id": r["step09_probe_id"],
                "reason": reason,
            })

    fields = ["collision_code", "phrase", "cluster_id", "user_task", "evidence_state", "step09_probe_id", "reason"]
    with old.OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
        w.writeheader(); w.writerows(flagged)

    summary = {
        "status": "PASS" if not flagged else "FAIL__MANUAL_REVIEW_REQUIRED",
        "audit_version": "V19",
        "active_rows_scanned": sum(r["input_disposition"] in {"CORE_CANDIDATE", "REVIEW_SEARCH"} for r in rows),
        "flagged_rows": len({x["phrase"] for x in flagged}),
        "flagged_records": len(flagged),
        "collision_counts": dict(sorted(counts.items())),
        "meaning": "V19 manually-adjudicated collision gate. Zero flags is necessary but still not sufficient for final manual semantic acceptance.",
    }
    old.OUT_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if flagged:
        for row in flagged:
            print("V19_COLLISION_FLAG", json.dumps(row, ensure_ascii=False))
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if flagged:
        raise SystemExit("V19 collision hard gate failed")


if __name__ == "__main__":
    main()
