#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

BASE = Path(__file__).resolve().parent
ASSIGN = BASE / "STEP_10_CLUSTER_ASSIGNMENTS.tsv"
OUT = BASE / "STEP_10_UNRESOLVED_ADVERSARIAL_AUDIT.tsv"
OUT_JSON = BASE / "STEP_10_UNRESOLVED_ADVERSARIAL_AUDIT.json"


def n(s: str) -> str:
    return " ".join((s or "").casefold().replace("ё", "е").split())


def anym(p: str, markers) -> bool:
    return any(m in p for m in markers)


def audit_unresolved(r: dict[str, str]) -> list[tuple[str, str]]:
    if r["cluster_evidence_state"] != "SEARCH_REQUIRED":
        return []
    p = n(r["phrase"])
    out: list[tuple[str, str]] = []

    if r["step09_probe_id"]:
        out.append(("DIRECT_SERP_LEFT_UNRESOLVED", "Exact Step-09 evidence exists; verify that unresolved state is intentionally mixed rather than a missing semantic class"))

    windowish = anym(p, ("окн", "окон", "стеклопак", "остеклен"))
    doorish = "двер" in p and anym(p, ("пластик", "пвх"))

    if windowish and anym(p, ("частного дома", "частный дом", "в частном доме", "для дома")):
        if anym(p, ("купить", "заказать", "цена", "цены", "стоимость", "пвх", "пластиков")):
            out.append(("UNRESOLVED_STRONG_PRIVATE_HOUSE_COMMERCIAL", "Private-house window phrase contains explicit product/price/material demand"))
        if anym(p, ("варианты", "виды", "какие окна", "лучшие окна", "образцы", "как выбрать", "выбрать")):
            out.append(("UNRESOLVED_STRONG_PRIVATE_HOUSE_SELECTION", "Private-house window phrase contains explicit selection/types wording"))

    if doorish and anym(p, ("как открыть", "как закрыть", "как снять", "как вставить", "как разобрать", "как называется", "что такое", "ширина", "высота", "размер", "габарит", "как установить")):
        out.append(("UNRESOLVED_STRONG_PVC_DOOR_INFORMATION", "Plastic-door phrase contains an explicit operation/definition/dimension/installation-information action"))

    if "панорам" in p and windowish:
        if anym(p, ("фото", "дизайн", "дизайны", "красив", "интерьер")):
            out.append(("UNRESOLVED_STRONG_PANORAMIC_INSPIRATION", "Panoramic-window phrase contains explicit design/photo/inspiration wording"))
        if anym(p, ("дом ", "дома ", "домик", "квартира", "комната", "кухня", "зал ", "лофт", "беседк", "бытовк", "барбекю", "баня", "гостиная", "апартамент", "веранда", "терраса", "лесу", "в лес")) and not anym(p, ("купить", "заказать", "цена", "стоимость")):
            out.append(("UNRESOLVED_STRONG_PANORAMIC_CONTEXT", "Panoramic-window phrase has a clear building/interior context without purchase wording"))
        if anym(p, ("виды", "варианты", "плюсы", "минусы", "лучшие", "какие", "как выбрать", "сравн", "почему")):
            out.append(("UNRESOLVED_STRONG_PANORAMIC_INFORMATION", "Panoramic-window phrase contains explicit informational/selection wording"))

    if "остеклен" in p and anym(p, ("плюсы", "минусы", "сравн", "что лучше", "какое лучше", "виды", "варианты", "как выбрать", "выбрать остекление")):
        out.append(("UNRESOLVED_STRONG_GLAZING_SELECTION", "Glazing phrase contains explicit comparison/selection wording"))

    return out


def main() -> None:
    with ASSIGN.open("r", encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))

    flagged = []
    counts = Counter()
    unresolved = 0
    for r in rows:
        if r["cluster_evidence_state"] != "SEARCH_REQUIRED":
            continue
        unresolved += 1
        for code, reason in audit_unresolved(r):
            counts[code] += 1
            flagged.append({
                "audit_code": code,
                "phrase": r["phrase"],
                "step09_probe_id": r["step09_probe_id"],
                "observed_serp_job": r["observed_serp_job"],
                "dominant_result_type": r["dominant_result_type"],
                "reason": reason,
            })

    fields = ["audit_code", "phrase", "step09_probe_id", "observed_serp_job", "dominant_result_type", "reason"]
    with OUT.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
        w.writeheader(); w.writerows(flagged)

    summary = {
        "status": "AUDIT_GENERATED__MANUAL_REVIEW_REQUIRED",
        "search_required_rows_scanned": unresolved,
        "flagged_rows": len({x["phrase"] for x in flagged}),
        "flagged_records": len(flagged),
        "audit_counts": dict(sorted(counts.items())),
        "meaning": "This audit looks for likely false SEARCH_REQUIRED states. Flags are review targets, not automatic cluster assignments.",
    }
    OUT_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(summary, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
