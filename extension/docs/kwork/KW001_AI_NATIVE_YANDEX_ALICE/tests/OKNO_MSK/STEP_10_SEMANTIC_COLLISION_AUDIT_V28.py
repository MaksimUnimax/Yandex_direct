#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from collections import Counter

import STEP_10_SEMANTIC_COLLISION_AUDIT as old
import STEP_10_SEMANTIC_COLLISION_AUDIT_V24 as v24


ASSIGNED = {"SEMANTIC_SUPPORTED_NO_DIRECT_SERP", "SERP_SUPPORTED"}


def n(s: str) -> str:
    return " ".join((s or "").casefold().replace("ё", "е").split())


def has(p: str, *parts: str) -> bool:
    return any(x in p for x in parts)


def audit_v28(r: dict[str, str]) -> list[tuple[str, str]]:
    out = list(v24.audit_v24(r))
    if r.get("cluster_evidence_state") not in ASSIGNED:
        return out

    p = n(r.get("phrase", ""))
    cid = r.get("cluster_id", "")
    intent = r.get("intent_orientation", "")

    curtains = has(p, "жалюз", "штор", "занавес")
    if curtains and cid not in {
        "OUTSIDE_CURTAINS", "OUTSIDE_CURTAINS_INSTALLATION",
        "OUTSIDE_CURTAINS_SELECTION_INFO", "OUTSIDE_CURTAINS_REPAIR_SERVICE",
        "DESIGN_INSPIRATION",
    }:
        out.append(("V28_CURTAIN_TASK_MISMATCH", "Curtain/blind head task escaped the dedicated outside-curtain taxonomy"))

    if has(p, "как выбрать москит", "противомоскитная сетка") and "как выбрать" in p and cid != "MOSQUITO_NET_SELECTION_INFO":
        out.append(("V28_MOSQUITO_SELECTION_MISMATCH", "Explicit mosquito-net selection must not remain ecommerce product demand"))
    if has(p, "ремонт москит", "ремонт сетки для пластиковых", "замена сетки на пластиковых") and cid != "MOSQUITO_NET_REPAIR_SERVICE":
        out.append(("V28_MOSQUITO_REPAIR_MISMATCH", "Explicit mosquito/protection-net repair or replacement needs its service task"))

    if p == "регулировка пластиковых дверей своими руками" and cid != "PVC_DOOR_REPAIR_DIY":
        out.append(("V28_DOOR_DIY_REPAIR_MISMATCH", "DIY door regulation is repair, not installation"))
    if p == "как поменять пластиковое окно" and cid != "WINDOW_REPLACEMENT_DIY":
        out.append(("V28_WINDOW_REPLACEMENT_DIY_MISMATCH", "Procedural whole-window replacement must not be ordinary operation"))

    if p in {"замена остекления балкона", "замена холодного остекления балкона"} and cid != "BALCONY_GLAZING_REPLACEMENT_SERVICE":
        out.append(("V28_BALCONY_GLAZING_REPLACEMENT_MISMATCH", "Replacement of existing balcony glazing is distinct from first-time glazing"))

    if p == "установка пластиковых окон размером" and cid != "WINDOW_MEASUREMENT_INFO":
        out.append(("V28_DIRECT_MEASUREMENT_CONTRADICTION", "Direct Step-09 evidence identified a measurement-information job"))
    if r.get("step09_probe_id") and r.get("dominant_result_type") in {"INFORMATION_GUIDE", "VIDEO_DIY"} and intent.startswith("COMMERCIAL"):
        out.append(("V28_DIRECT_INFORMATION_VS_COMMERCIAL", "Direct Step-09 informational SERP cannot pass as an ordinary commercial cluster member"))

    if has(p, "профиль для пластиковых окон", "профиль пластиковой двери", "профиль пластиковых окон rehau", "узлы алюминиевых окон", "панель для пластиковой двери", "добор для пластиковых окон") and cid not in {"WINDOW_HARDWARE", "WINDOW_ACCESSORY_SELECTION_INFO"}:
        out.append(("V28_COMPONENT_HEAD_MISMATCH", "Explicit component/profile head object was swallowed by a whole-product family"))

    if has(p, "адрес установки", "балконы остекление адрес", "номер ремонта", "ремонт пластиковых окон адрес", "окна пластиковые с установкой телефоны") and cid != "WINDOW_SERVICE_NAVIGATION":
        out.append(("V28_SERVICE_NAVIGATION_MISMATCH", "Explicit address/phone service-navigation wording must not remain the service action itself"))
    if has(p, "rehau", "рехау") and has(p, "сайт", "дилер", "офис", "партнер", "rehau ru") and cid != "REHAU_NAVIGATION":
        out.append(("V28_REHAU_NAVIGATION_MISMATCH", "Explicit Rehau entity/site/dealer navigation must not remain product demand"))

    if p in {"окно пластиковое закрыто", "открытое пластиковое окно", "пластиковое окно внутри", "пластиковое окно снаружи", "пластиковые окна улица", "самому пластиковые окна", "после установки пластиковых окон"}:
        out.append(("V28_CONTEXT_FRAGMENT_FORCED", "Known state/context fragment is still force-clustered"))

    if p == "размеры окон для частного дома фото" and cid != "WINDOW_DIMENSIONS_INFO":
        out.append(("V28_DIMENSIONS_PHOTO_PRECEDENCE", "Dimension head task was swallowed by photo/design marker"))

    if has(p, "оконная фурнитура виды", "как называется оконная фурнитура", "как устроена оконная фурнитура") and cid == "WINDOW_HARDWARE":
        out.append(("V28_HARDWARE_INFO_SWALLOWED", "Explicit hardware information/selection wording remains ecommerce hardware"))

    if p == "алюминиевое остекление веранды раздвижными конструкциями" and cid != "VERANDA_GLAZING":
        out.append(("V28_VERANDA_GLAZING_TECH_SWALLOW", "Veranda glazing service was swallowed by technical-information marker"))

    return out


def main() -> None:
    with old.ASSIGN.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))

    flagged = []
    counts = Counter()
    for r in rows:
        if r.get("input_disposition") not in {"CORE_CANDIDATE", "REVIEW_SEARCH"}:
            continue
        for code, reason in audit_v28(r):
            counts[code] += 1
            flagged.append({
                "collision_code": code,
                "phrase": r.get("phrase", ""),
                "cluster_id": r.get("cluster_id", ""),
                "user_task": r.get("user_task", ""),
                "evidence_state": r.get("cluster_evidence_state", ""),
                "step09_probe_id": r.get("step09_probe_id", ""),
                "reason": reason,
            })

    fields = ["collision_code", "phrase", "cluster_id", "user_task", "evidence_state", "step09_probe_id", "reason"]
    with old.OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
        w.writeheader(); w.writerows(flagged)

    summary = {
        "status": "PASS" if not flagged else "FAIL__MANUAL_REVIEW_REQUIRED",
        "audit_version": "V28",
        "active_rows_scanned": sum(r.get("input_disposition") in {"CORE_CANDIDATE", "REVIEW_SEARCH"} for r in rows),
        "flagged_rows": len({x["phrase"] for x in flagged}),
        "flagged_records": len(flagged),
        "collision_counts": dict(sorted(counts.items())),
        "meaning": "V28 adds manual-QA-discovered action/head-object/navigation/direct-evidence checks on top of V24. Zero flags is necessary but still not sufficient for final manual semantic acceptance.",
    }
    old.OUT_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    if flagged:
        for row in flagged:
            print("V28_COLLISION_FLAG", json.dumps(row, ensure_ascii=False))
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    if flagged:
        raise SystemExit("V28 semantic collision hard gate failed")


if __name__ == "__main__":
    main()
