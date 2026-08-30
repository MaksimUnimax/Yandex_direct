#!/usr/bin/env python3
from __future__ import annotations

import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
FULL = ROOT / "STEP_10_FRESH_R1_PASS3_FULL_REVIEW.tsv"
QA = ROOT / "STEP_10_FRESH_R1_PASS3_QA.json"
OUT_RULE = ROOT / "STEP_10_FRESH_R1_PASS3_RULE_SAMPLES.tsv"
OUT_CLUSTER = ROOT / "STEP_10_FRESH_R1_PASS3_CLUSTER_SAMPLES.tsv"
OUT_COUNTS = ROOT / "STEP_10_FRESH_R1_PASS3_DECISION_COUNTS.tsv"
OUT_FLAGS = ROOT / "STEP_10_FRESH_R1_PASS3_CONTRADICTION_FLAGS.tsv"


def write_tsv(path: Path, fields: list[str], rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
        w.writeheader()
        w.writerows(rows)


def evenly_spaced(items: list[dict[str, str]], limit: int) -> list[dict[str, str]]:
    if len(items) <= limit:
        return items
    if limit <= 1:
        return [items[0]]
    indexes = []
    for i in range(limit):
        idx = round(i * (len(items) - 1) / (limit - 1))
        if idx not in indexes:
            indexes.append(idx)
    return [items[i] for i in indexes]


def rule_samples(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["audit_rule"]].append(row)
    out: list[dict[str, str]] = []
    for rule, members in sorted(grouped.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        chosen = evenly_spaced(members, 10)
        for rank, row in enumerate(chosen, 1):
            out.append({
                "audit_rule": rule,
                "rule_count": str(len(members)),
                "sample_rank": str(rank),
                "qa_row": row["qa_row"],
                "phrase": row["phrase"],
                "audit_expected_status": row["audit_expected_status"],
                "audit_cluster_id": row["audit_cluster_id"],
                "pass2_assignment_status": row["pass2_assignment_status"],
                "pass2_cluster_id": row["pass2_cluster_id"],
                "review_outcome": row["review_outcome"],
                "error_class": row["error_class"],
            })
    return out


def cluster_samples(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    grouped: dict[tuple[str, str], list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[(row["audit_expected_status"], row["audit_cluster_id"] or "<NONE>")].append(row)
    out: list[dict[str, str]] = []
    for key, members in sorted(grouped.items(), key=lambda kv: (-len(kv[1]), kv[0])):
        by_rule: dict[str, list[dict[str, str]]] = defaultdict(list)
        for row in members:
            by_rule[row["audit_rule"]].append(row)

        chosen: list[dict[str, str]] = []
        # First guarantee rule diversity inside each cluster.
        for rule, rule_members in sorted(by_rule.items(), key=lambda kv: (-len(kv[1]), kv[0])):
            chosen.append(rule_members[len(rule_members) // 2])
            if len(chosen) >= 12:
                break
        # Then fill with evenly spaced rows across the full cluster population.
        if len(chosen) < 12:
            seen = {row["qa_row"] for row in chosen}
            for row in evenly_spaced(members, 24):
                if row["qa_row"] not in seen:
                    chosen.append(row)
                    seen.add(row["qa_row"])
                if len(chosen) >= 12:
                    break

        for rank, row in enumerate(chosen, 1):
            out.append({
                "audit_expected_status": key[0],
                "audit_cluster_id": key[1],
                "cluster_count": str(len(members)),
                "distinct_rule_count": str(len(by_rule)),
                "sample_rank": str(rank),
                "qa_row": row["qa_row"],
                "phrase": row["phrase"],
                "audit_rule": row["audit_rule"],
                "pass2_assignment_status": row["pass2_assignment_status"],
                "pass2_cluster_id": row["pass2_cluster_id"],
                "review_outcome": row["review_outcome"],
                "error_class": row["error_class"],
            })
    return out


def decision_counts(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    counts = Counter(
        (
            row["audit_expected_status"],
            row["audit_cluster_id"] or "<NONE>",
            row["source_disposition"],
            row["review_outcome"],
        )
        for row in rows
    )
    return [
        {
            "audit_expected_status": key[0],
            "audit_cluster_id": key[1],
            "source_disposition": key[2],
            "review_outcome": key[3],
            "row_count": str(count),
        }
        for key, count in sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))
    ]


def contradiction_flags(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    flags: list[dict[str, str]] = []

    commercial_clusters = {
        "WINDOWS_COMMERCIAL_GENERAL",
        "PVC_WINDOWS_COMMERCIAL",
        "REHAU_WINDOWS_COMMERCIAL",
        "ALUMINIUM_WINDOWS_COMMERCIAL",
        "WOOD_WINDOWS_COMMERCIAL",
        "TIMBER_ALUMINIUM_WINDOWS_COMMERCIAL",
        "SOFT_WINDOWS_COMMERCIAL",
        "FRENCH_WINDOWS_COMMERCIAL",
        "PANORAMIC_WINDOWS_COMMERCIAL",
        "ROOF_WINDOWS_COMMERCIAL",
        "WINDOWS_DOORS_COMBINED_COMMERCIAL",
        "PVC_DOORS_COMMERCIAL",
    }

    def add(row: dict[str, str], code: str, detail: str) -> None:
        flags.append({
            "flag_code": code,
            "qa_row": row["qa_row"],
            "phrase": row["phrase"],
            "audit_expected_status": row["audit_expected_status"],
            "audit_cluster_id": row["audit_cluster_id"],
            "audit_rule": row["audit_rule"],
            "flag_detail": detail,
        })

    for row in rows:
        q = row["phrase"].lower().replace("ё", "е")
        cluster = row["audit_cluster_id"]
        rule = row["audit_rule"]

        # These flags are deliberately over-inclusive review aids, not automatic errors.
        if cluster in commercial_clusters and any(token in q for token in ("ремонт", "почин", "регулиров", "не закры", "не откры", "провис", "просел")):
            add(row, "COMMERCIAL_WITH_REPAIR_CUE", "commercial assignment contains an explicit repair/fault cue")
        if cluster in commercial_clusters and any(token in q for token in ("своими руками", "самостоятельно", "пошагов", "инструкция", "как установить", "как снять", "как заменить")):
            add(row, "COMMERCIAL_WITH_DIY_CUE", "commercial assignment contains an explicit DIY/procedural cue")
        if cluster in commercial_clusters and any(token in q for token in ("отзывы", "отзыв", "рейтинг", "какие лучше", "что лучше", "сравн")):
            add(row, "COMMERCIAL_WITH_DECISION_CUE", "commercial assignment contains review/ranking/comparison wording")
        if cluster in commercial_clusters and any(token in q for token in ("что такое", "что значит", "это какие", "как называется")):
            add(row, "COMMERCIAL_WITH_DEFINITION_CUE", "commercial assignment contains a definition cue")
        if cluster == "WINDOW_HARDWARE_SHOPPING" and any(token in q for token in ("какая лучше", "какой лучше", "какие лучше", "отзывы", "рейтинг", "сравн", "виды", "как устро")):
            add(row, "HARDWARE_SHOPPING_WITH_INFO_CUE", "hardware shopping assignment contains an information/selection cue")
        if cluster == "WINDOW_ACCESSORIES_SHOPPING" and any(token in q for token in ("как выбрать", "какой лучше", "какая лучше", "виды", "что такое")):
            add(row, "ACCESSORY_SHOPPING_WITH_INFO_CUE", "accessory shopping assignment contains an information/selection cue")
        if cluster == "BALCONY_GLAZING_ROOF_SERVICE" and "без крыши" in q:
            add(row, "ROOF_SERVICE_WITH_NEGATION", "roof-service assignment explicitly negates the roof")
        if cluster == "BALCONY_RENOVATION_WITH_GLAZING" and "без остекления" in q:
            add(row, "GLAZING_BUNDLE_WITH_NEGATION", "glazing bundle explicitly says without glazing")
        if cluster == "OUTSIDE_REAL_ESTATE_ARCHITECTURE" and any(token in q for token in ("купить окно", "заказать окно", "цена окна", "стоимость окна", "установка окна", "ремонт окна")):
            add(row, "OUTSIDE_ARCHITECTURE_WITH_WINDOW_TRANSACTION", "outside architecture assignment contains direct window transaction/service wording")
        if cluster == "OUTSIDE_CURTAINS_BLINDS" and not any(token in q for token in ("штор", "жалюз", "занавес", "карниз", "плиссе")) and rule != "DIRECT_SERP_EXACT_OVERRIDE":
            add(row, "CURTAIN_CLUSTER_WITHOUT_CURTAIN_TERM", "outside curtain/blind assignment lacks an obvious curtain/blind term")
        if cluster == "OUTSIDE_HEATING_HVAC" and not any(token in q for token in ("радиатор", "батар", "конвектор", "отоплен", "кондиционер", "теплый пол")) and rule != "DIRECT_SERP_EXACT_OVERRIDE":
            add(row, "HEATING_CLUSTER_WITHOUT_HEATING_TERM", "outside heating assignment lacks an obvious heating/HVAC term")

    return flags


def main() -> None:
    qa = json.loads(QA.read_text(encoding="utf-8"))
    with FULL.open(encoding="utf-8", newline="") as f:
        rows = list(csv.DictReader(f, delimiter="\t"))
    if len(rows) != 2332 or qa["pass3_rows_reviewed"] != 2332:
        raise RuntimeError(f"Pass3 decision sample source mismatch: rows={len(rows)} qa={qa['pass3_rows_reviewed']}")
    if qa["rule_version"] != "PASS3_R1_INDEPENDENT_SEMANTIC_AUDIT_V3":
        raise RuntimeError(f"decision samples require audit V3, got {qa['rule_version']}")

    r_samples = rule_samples(rows)
    c_samples = cluster_samples(rows)
    counts = decision_counts(rows)
    flags = contradiction_flags(rows)

    write_tsv(
        OUT_RULE,
        [
            "audit_rule", "rule_count", "sample_rank", "qa_row", "phrase",
            "audit_expected_status", "audit_cluster_id", "pass2_assignment_status",
            "pass2_cluster_id", "review_outcome", "error_class",
        ],
        r_samples,
    )
    write_tsv(
        OUT_CLUSTER,
        [
            "audit_expected_status", "audit_cluster_id", "cluster_count", "distinct_rule_count",
            "sample_rank", "qa_row", "phrase", "audit_rule", "pass2_assignment_status",
            "pass2_cluster_id", "review_outcome", "error_class",
        ],
        c_samples,
    )
    write_tsv(
        OUT_COUNTS,
        ["audit_expected_status", "audit_cluster_id", "source_disposition", "review_outcome", "row_count"],
        counts,
    )
    write_tsv(
        OUT_FLAGS,
        ["flag_code", "qa_row", "phrase", "audit_expected_status", "audit_cluster_id", "audit_rule", "flag_detail"],
        flags,
    )

    print(f"PASS3_RULE_SAMPLE_ROWS={len(r_samples)}")
    print(f"PASS3_CLUSTER_SAMPLE_ROWS={len(c_samples)}")
    print(f"PASS3_DECISION_COUNT_ROWS={len(counts)}")
    print(f"PASS3_CONTRADICTION_FLAG_ROWS={len(flags)}")


if __name__ == "__main__":
    main()
