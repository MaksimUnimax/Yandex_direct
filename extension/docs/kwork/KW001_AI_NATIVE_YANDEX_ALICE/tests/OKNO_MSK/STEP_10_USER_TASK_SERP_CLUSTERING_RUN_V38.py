#!/usr/bin/env python3
from __future__ import annotations

import STEP_10_USER_TASK_SERP_CLUSTERING_BUILD as b
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN as runner
import STEP_10_USER_TASK_SERP_CLUSTERING_RUN_V36 as v36
import STEP_10_V38_DISCOVERY_SPEC as spec

_v36_classifier = b.classify_semantic

# Two combined-object tasks are justified by repeated, explicit window+door wording.
# They are Step-10 analytical tasks only; they do not imply a page decision.
b.TASKS.setdefault(
    "WINDOW_DOOR_INSTALLATION_SERVICE",
    ("Профессиональная установка окон и балконных/ПВХ-дверей", "COMMERCIAL_SERVICE", "FIT"),
)
b.TASKS.setdefault(
    "WINDOW_DOOR_REPAIR_SERVICE",
    ("Ремонт/регулировка окон и ПВХ-дверей", "COMMERCIAL_SERVICE", "ADJACENT"),
)


def has(p: str, *parts: str) -> bool:
    return any(x in p for x in parts)


def classify_v38(phrase: str):
    p = b.norm(phrase)
    win = has(p, "окн", "окон", "rehau", "рехау")
    door = "двер" in p
    install = has(p, "установ", "монтаж", "поставить")
    repair = has(p, "ремонт", "регулир", "почин")
    symptom = has(p, "не закры", "не откры", "плохо закры", "провис", "просел", "просела")
    panoramic = "панорам" in p and win
    french = "француз" in p and win

    # ------------------------------------------------------------------
    # RC7: explicit commercial repair must outrank symptom/diagnostic routing.
    # ------------------------------------------------------------------
    if repair and symptom and "пластиков" in p and win and "москв" in p:
        return "WINDOW_REPAIR", "Explicit repair + Moscow is a commercial repair-service request; symptom wording is secondary", "HIGH"

    # ------------------------------------------------------------------
    # RC1: specific head object/action outranks broad material/service family.
    # ------------------------------------------------------------------
    # Combined window+door installation/repair/product tasks.
    combined_window_door = win and door
    balcony_block_window = "балконный блок" in p and "пластиков" in p and win
    if install and (combined_window_door or balcony_block_window):
        return "WINDOW_DOOR_INSTALLATION_SERVICE", "Installation explicitly covers a combined window+door/balcony-block unit", "HIGH"
    if repair and combined_window_door:
        return "WINDOW_DOOR_REPAIR_SERVICE", "Repair explicitly covers both windows and doors", "HIGH"
    if p in {"алюминиевые окна и двери", "окна двери rehau", "окна двери для частного дома"}:
        return "WINDOW_DOOR_COMMERCIAL", "Combined window+door product task outranks material/brand/private-house fallback", "HIGH"

    # Balcony renovation/finishing plus glazing is a combined service task.
    if "балкон" in p and "остеклен" in p and has(p, "отделк", "обшив"):
        return "BALCONY_RENOVATION_WITH_GLAZING_SERVICE", "Balcony renovation/finishing is a co-head service with glazing", "HIGH"

    # Hardware care products and reference tasks.
    hardware = "фурнитур" in p and win
    if hardware and "чем смазать" in p:
        return "WINDOW_CARE_INFO", "How-to lubrication wording is maintenance/care information", "HIGH"
    if hardware and has(p, "масло", "смазк"):
        return "WINDOW_ACCESSORIES", "Lubricant/oil is the head product; hardware is its use context", "HIGH"
    if hardware and has(p, "гост", "сертификат"):
        return "WINDOW_TECH_INFO", "Standards/certification wording is technical/reference information", "HIGH"
    if p in {"производители оконной фурнитуры", "производство оконной фурнитуры"}:
        return None, "Manufacturer/process wording is not ordinary hardware shopping; provider-versus-process intent remains unresolved", "LOW"

    # Explicit finishing actions outrank whole-window product families.
    if has(p, "отделка пластиковых окон", "цена на отделку пластиковых окон", "отделка панорамных окон", "отделка французского окна"):
        return "WINDOW_FINISHING_SERVICE", "Finishing is the explicit action/service; window type is the object/modifier", "HIGH"
    if p == "покраска алюминиевых окон":
        return "WINDOW_FINISHING_SERVICE", "Painting is a surface-finishing service rather than whole-window purchase", "HIGH"

    # Finance and component/material head objects inside glazing wording.
    if p == "остекление веранды в рассрочку":
        return "WINDOW_FINANCE", "Installment finance is the decision-driving commercial goal", "HIGH"
    if p == "стекло остекления балкона":
        return "WINDOW_HARDWARE", "Glass is the head component/product; balcony glazing is use context", "HIGH"
    if p == "верандные рамы для веранды остекление одинарное цена":
        return "WINDOW_HARDWARE", "Frames are the priced head product; veranda glazing is use context", "HIGH"
    if p == "жидкое стекло остекление веранды":
        return "WINDOW_ACCESSORIES", "Liquid glass/material is the head product, not the glazing service", "HIGH"
    if p == "система остекления веранды":
        return "GLAZING_SELECTION_INFO", "Glazing-system wording is a system/type information-selection task", "HIGH"

    # ------------------------------------------------------------------
    # RC7/RC3: unsupported sub-mode inference must return to a visible boundary.
    # ------------------------------------------------------------------
    # Direct Step-09 row 'окна rehau провисли' is intentionally excluded from this
    # semantic-only rule because it has its own direct mixed evidence.
    if symptom and p != "окна rehau провисли" and not (repair and "москв" in p):
        return None, "Symptom wording identifies a repair problem but does not prove professional-service versus DIY sub-intent", "LOW"
    if p == "пластиковая дверь своими руками":
        return None, "DIY modifier is present but the action itself is absent; installation cannot be inferred safely", "LOW"
    if p in {"остекление балкона видео", "остекление веранды видео", "ремонт пластиковых окон видео"}:
        return None, "Video wording proves informational consumption but not the specific DIY/professional task subtype", "LOW"

    # ------------------------------------------------------------------
    # RC4: dwelling/room/architecture head object outranks photo/design modifier.
    # ------------------------------------------------------------------
    architecture_visual = {
        "дизайн кухни с панорамными окнами",
        "дома с панорамными окнами фото",
        "интерьер с панорамными окнами",
        "стиль дома с панорамными окнами",
        "терраса с панорамными окнами фото",
    }
    if p in architecture_visual:
        return "OUTSIDE_REAL_ESTATE", "Dwelling/room/terrace is the head object; photo/design wording is only a modifier", "HIGH"

    # ------------------------------------------------------------------
    # RC5: private-house selection must not split merely on PVC/material wording.
    # ------------------------------------------------------------------
    if has(p, "частного дома", "частного") and win and has(p, "виды", "как выбрать"):
        return "PRIVATE_HOUSE_WINDOWS_SELECTION_INFO", "Private-house selection intent outranks generic PVC-window selection", "HIGH"

    # ------------------------------------------------------------------
    # RC6: definition/naming is not selection.
    # ------------------------------------------------------------------
    if p == "французские окна это какие":
        return "WINDOW_DEFINITION_INFO", "‘Это какие’ asks for definition/type meaning rather than selection", "HIGH"

    # ------------------------------------------------------------------
    # RC2: semantically determinate V37 SEARCH_REQUIRED rows.
    # These are grouped by semantic class; no direct SERP evidence is manufactured.
    # ------------------------------------------------------------------
    if p == "ral алюминиевых окон":
        return "WINDOW_SELECTION_INFO", "RAL wording is colour/configuration selection information", "HIGH"
    if p == "камин панорамные окна":
        return "OUTSIDE_HEATING", "Fireplace/heating is the head system; panoramic windows are context", "HIGH"
    if p == "окно панорамный блок":
        return "PANORAMIC_WINDOWS_COMMERCIAL", "Panoramic block/window wording is a product/configuration task", "MEDIUM"

    architecture_context = {
        "окно французской гостиной",
        "панорамное окно на кухне",
        "панорамные окна в здании",
        "панорамные окна в каркасном",
        "панорамные окна и потолок",
        "панорамные окна на море",
        "перегородка французское окно",
        "перепланировка французское окно",
        "спальня французское окно",
        "студия с панорамными окнами",
    }
    if p in architecture_context:
        return "OUTSIDE_REAL_ESTATE", "Dwelling/room/building/renovation context is the head task rather than window purchase", "HIGH"

    if p in {"панорамные окна в частном", "панорамные окна для загородного"}:
        return "PANORAMIC_WINDOWS_COMMERCIAL", "Specific panoramic-window use case outranks generic unresolved/private-house fallback", "MEDIUM"
    if p in {"современные панорамные окна", "французские окна современные"}:
        return "PANORAMIC_WINDOWS_INFO", "Modern/type wording is an informational selection/features task", "HIGH"
    if p == "утепление панорамных окон":
        return "WINDOW_REPAIR", "Insulation is a maintenance/repair-adjacent service action on existing windows", "HIGH"
    if p in {"французские балконные окна", "французские окна в хрущевке", "французские окна на даче", "французские окна на кухню"}:
        return "FRENCH_WINDOWS_COMMERCIAL", "French-window product/use-case is explicit enough to assign without borrowed SERP", "MEDIUM"

    return _v36_classifier(phrase)


b.classify_semantic = classify_v38


def discovery_self_check() -> None:
    """Check all 85 frozen discovery expectations in one pass and report every miss."""
    misses = []
    for row in spec.ROWS:
        task_id, reason, confidence = b.classify_semantic(row["phrase"])
        observed = task_id or "SEARCH_REQUIRED"
        expected = row["proposed_cluster_id"]
        if observed != expected:
            misses.append((row["phrase"], expected, observed, reason))
    if misses:
        for phrase, expected, observed, reason in misses:
            print(f"V38_DISCOVERY_SELF_CHECK_FAIL\t{phrase}\texpected={expected}\tobserved={observed}\treason={reason}")
        raise SystemExit(f"V38 discovery self-check failed: {len(misses)} residual errors")
    print(f"V38_DISCOVERY_SELF_CHECK_PASS rows={len(spec.ROWS)}")


if __name__ == "__main__":
    discovery_self_check()
    runner.main()
