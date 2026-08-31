from __future__ import annotations

import csv
import io
import json
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
STEP_ROOT = ROOT.parents[2]

ASSIGNMENTS = ROOT / "STEP_10_FRESH_R1_ASSIGNMENTS_FINAL.tsv"
CLUSTER_SUMMARY = ROOT / "STEP_10_FRESH_R1_CLUSTER_SUMMARY_FINAL.tsv"
ORIGINAL_OWNERSHIP = ROOT / "STEP_11_PAGE_OWNERSHIP.tsv"

OUT_CORRECTIONS = ROOT / "STEP_11_POST_AUDIT_CORRECTIONS.tsv"
OUT_MAP = ROOT / "STEP_11_PHRASE_PAGE_MAP.tsv"
OUT_SUMMARY = ROOT / "STEP_11_EFFECTIVE_CLUSTER_SUMMARY.tsv"
OUT_OWNERSHIP = ROOT / "STEP_11_PAGE_OWNERSHIP_CORRECTED.tsv"
OUT_WEAK_AUDIT = ROOT / "STEP_11_WEAK_OWNERSHIP_REAUDIT.md"
OUT_QA = ROOT / "STEP_11_QA.json"
OUT_REPORT = ROOT / "STEP_11_REPORT.md"


def read_tsv(path: Path):
    with path.open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def write_tsv(path: Path, rows, fields):
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n", extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


CORRECTIONS = {}


def remap(old_cluster, new_cluster, phrases, reason):
    for phrase in phrases:
        if phrase in CORRECTIONS:
            raise RuntimeError(f"duplicate correction phrase: {phrase}")
        CORRECTIONS[phrase] = {
            "expected_original_cluster_id": old_cluster,
            "effective_assignment_status": "ASSIGNED",
            "effective_cluster_id": new_cluster,
            "correction_reason": reason,
        }


def require_search(old_cluster, phrases, reason):
    for phrase in phrases:
        if phrase in CORRECTIONS:
            raise RuntimeError(f"duplicate correction phrase: {phrase}")
        CORRECTIONS[phrase] = {
            "expected_original_cluster_id": old_cluster,
            "effective_assignment_status": "SEARCH_REQUIRED",
            "effective_cluster_id": "",
            "correction_reason": reason,
        }


# 1. False generic glazing cluster: all seven members are actually specific tasks.
remap("GENERAL_GLAZING_SERVICE", "ALUMINIUM_WINDOWS_COMMERCIAL", [
    "алюминиевые окна остекление",
    "остекление окон алюминиевым профилем",
    "остекление раздвижными алюминиевыми окнами",
    "раздвижные окна алюминиевые холодное остекление",
], "POST_STEP11_CLUSTER_COHERENCE__ALUMINIUM_PRODUCT_TASK")
remap("GENERAL_GLAZING_SERVICE", "PANORAMIC_WINDOWS_COMMERCIAL", [
    "остекление панорамное окно",
], "POST_STEP11_CLUSTER_COHERENCE__PANORAMIC_WINDOW_TASK")
remap("GENERAL_GLAZING_SERVICE", "FRENCH_WINDOWS_COMMERCIAL", [
    "остекление французское окно",
], "POST_STEP11_CLUSTER_COHERENCE__FRENCH_WINDOW_TASK")
remap("GENERAL_GLAZING_SERVICE", "OUTSIDE_OTHER", [
    "окна сок панорамное раздвижное остекление",
], "POST_STEP11_CLUSTER_COHERENCE__SOK_BRAND_ENTITY_OUTSIDE_TARGET_OWNERSHIP")

# 2. False generic glazing-selection cluster: actual members are veranda/outdoor tasks.
remap("GLAZING_SELECTION_INFO", "OUTDOOR_GLAZING_SELECTION_INFO", [
    "алюминиевое остекление веранды раздвижными конструкциями",
    "варианты остекления веранды",
    "варианты остекления веранды в частном доме",
    "варианты остекления веранды частного",
    "виды остекления веранды",
    "остекление веранды материалы",
    "система остекления веранды",
], "POST_STEP11_CLUSTER_COHERENCE__VERANDA_SELECTION_TASK")
remap("GLAZING_SELECTION_INFO", "OUTDOOR_GLAZING_SPECIALIZED_INFO", [
    "безрамное остекление веранды плюсы и минусы",
    "жидкое стекло остекление веранды",
    "толщина монолитного поликарбоната для остекления веранды",
], "POST_STEP11_CLUSTER_COHERENCE__SPECIALIZED_VERANDA_TECHNIQUE")
remap("GLAZING_SELECTION_INFO", "OUTDOOR_GLAZING_REVIEWS_INFO", [
    "остекление веранды отзывы",
], "POST_STEP11_CLUSTER_COHERENCE__VERANDA_REVIEW_INTENT")

# 3. Whole-window replacement cluster contained component and balcony/French transformation tasks.
remap("WINDOW_REPLACEMENT_SERVICE", "WINDOW_REPAIR_SERVICE", [
    "замена резинок на пластиковых окнах цена",
    "замена резинок на пластиковых окнах цена москва",
    "замена ручек на пластиковых окнах цена",
    "поменять прокладки на пластиковых окнах цена",
    "поменять резинки на пластиковых окнах цена",
    "поменять резинки на пластиковых окнах цена москва",
], "POST_STEP11_CLUSTER_COHERENCE__COMPONENT_REPLACEMENT_IS_REPAIR")
remap("WINDOW_REPLACEMENT_SERVICE", "BALCONY_GLAZING_GENERAL", [
    "замена остекления балкона",
    "замена балкона на пластиковые окна цена",
], "POST_STEP11_CLUSTER_COHERENCE__BALCONY_GLAZING_REPLACEMENT")
remap("WINDOW_REPLACEMENT_SERVICE", "BALCONY_GLAZING_COLD", [
    "замена холодного остекления балкона",
], "POST_STEP11_CLUSTER_COHERENCE__COLD_BALCONY_GLAZING_REPLACEMENT")
remap("WINDOW_REPLACEMENT_SERVICE", "FRENCH_WINDOWS_COMMERCIAL", [
    "замена балконного блока на французское окно",
], "POST_STEP11_CLUSTER_COHERENCE__TRANSFORMATION_TO_FRENCH_WINDOW")

# 4. Reviews: product/model reviews and provider/service ratings are different terminal tasks.
remap("WINDOW_REVIEWS_INFO", "WINDOW_PRODUCT_REVIEWS_INFO", [
    "алюминиевые окна отзывы",
    "окна rehau delight 70 отзывы",
    "окна rehau grazio 70 мм отзывы",
    "окна rehau grazio отзывы",
    "окна rehau отзывы",
    "пластиковые окна rehau отзывы",
    "пластиковые окна отзывы",
    "французские окна отзывы",
    "цены на пластиковые окна отзывы",
    "отзывы пластиковых дверей",
    "рейтинг алюминиевых окон",
    "рейтинг пластиковых окон",
], "POST_STEP11_CLUSTER_COHERENCE__PRODUCT_OR_MODEL_REVIEW_INTENT")
remap("WINDOW_REVIEWS_INFO", "WINDOW_PROVIDER_REVIEWS_INFO", [
    "пластиковые окна в москве с установкой отзывы",
    "пластиковые окна в москве с установкой рейтинг",
    "рейтинг компаний по установке пластиковых окон",
    "рейтинг по установке пластиковых окон",
    "рейтинг ремонта пластиковых окон",
    "рейтинг фирм по установке пластиковых окон",
    "ремонт пластиковых окон в москве рейтинг",
    "ремонт пластиковых окон отзывы",
    "ремонт пластиковых окон рейтинг компаний",
    "установка пластиковых окон в москве рейтинг компаний",
], "POST_STEP11_CLUSTER_COHERENCE__PROVIDER_SERVICE_RATING_INTENT")

# 5. Balcony information: selection/specification vs provider review/rating.
remap("BALCONY_GLAZING_INFO", "BALCONY_GLAZING_SELECTION_INFO", [
    "варианты остекления балкона",
    "виды остекления балконов",
    "выбрать остекление балкона",
    "какое остекление балкона лучше выбрать",
    "какое остекление балконов выбрать",
    "остекление балконов конструкция",
    "стекло остекления балкона",
], "POST_STEP11_CLUSTER_COHERENCE__BALCONY_SELECTION_INTENT")
remap("BALCONY_GLAZING_INFO", "BALCONY_GLAZING_PROVIDER_REVIEWS_INFO", [
    "лучшие компании по остеклению балконов",
    "остекление балконов в москве рейтинг",
    "остекление балконов москва отзывы",
    "остекление балконов отзывы",
    "рейтинг компаний по остеклению балконов",
    "рейтинг остекления балкона",
], "POST_STEP11_CLUSTER_COHERENCE__BALCONY_PROVIDER_RATING_INTENT")

# 6. Broad technical-information cluster split by product family / terminal task.
remap("WINDOW_PRODUCT_TECH_INFO", "WINDOW_OPERATION_MODE_INFO", [
    "rehau окна режимы",
    "окна rehau зимний режим",
], "POST_STEP11_CLUSTER_COHERENCE__WINDOW_OPERATION_MODE_TASK")
remap("WINDOW_PRODUCT_TECH_INFO", "REHAU_WINDOW_TECH_INFO", [
    "rehau окно конструкция",
    "окна rehau виды",
    "окна система rehau",
], "POST_STEP11_CLUSTER_COHERENCE__REHAU_TECH_TASK")
remap("WINDOW_PRODUCT_TECH_INFO", "PVC_WINDOW_COLOR_INFO", [
    "окна rehau цвета",
    "цвета пластиковых окон",
], "POST_STEP11_CLUSTER_COHERENCE__PVC_WINDOW_COLOR_TASK")
remap("WINDOW_PRODUCT_TECH_INFO", "ALUMINIUM_WINDOW_TECH_INFO", [
    "виды алюминиевых окон",
    "как выглядят алюминиевые окна",
    "конструкция алюминиевого окна",
    "открывание алюминиевых окон",
    "проветривание алюминиевые окна",
    "системы алюминиевых окон",
    "цвета алюминиевых окон",
], "POST_STEP11_CLUSTER_COHERENCE__ALUMINIUM_TECH_TASK")
remap("WINDOW_PRODUCT_TECH_INFO", "PANORAMIC_WINDOW_TECH_INFO", [
    "виды панорамных окон",
    "почему панорамные окна",
], "POST_STEP11_CLUSTER_COHERENCE__PANORAMIC_TECH_TASK")
remap("WINDOW_PRODUCT_TECH_INFO", "PVC_WINDOW_TECH_INFO", [
    "виды пластиковых окон",
    "открывание пластиковых окон",
    "почему пластиковых окнах",
    "суть пластиковых окон",
], "POST_STEP11_CLUSTER_COHERENCE__PVC_TECH_TASK")
remap("WINDOW_PRODUCT_TECH_INFO", "FRENCH_WINDOW_DEFINITION_INFO", [
    "виды французского окна",
    "как выглядит французское окно",
    "французские окна название",
    "французские окна это какие",
    "французское окно как называется",
], "POST_STEP11_CLUSTER_COHERENCE__FRENCH_DEFINITION_TASK")
remap("WINDOW_PRODUCT_TECH_INFO", "WINDOW_PRODUCT_VIDEO_INFO", [
    "алюминиевые окна видео",
    "пластиковые окна видео",
], "POST_STEP11_CLUSTER_COHERENCE__BARE_PRODUCT_VIDEO_TASK")

# 7. Bare DIY/instruction phrases do not prove a repair task.
require_search("WINDOW_REPAIR_DIY_INFO", [
    "rehau окна инструкция",
    "алюминиевые окна своими руками",
    "инструкция пластиковых окон",
    "панорамные окна своими руками",
    "пластиковое окно самостоятельно",
    "пластиковые окна своими руками",
], "POST_STEP11_CLUSTER_COHERENCE_AMBIGUITY__BARE_DIY_OR_INSTRUCTION_NO_STABLE_TERMINAL_TASK")

# 8. Component/profile selection corrections.
remap("WINDOW_HARDWARE_INFO", "WINDOW_PROFILE_SELECTION_INFO", [
    "как выбрать профиль для пластиковых окон правильно",
    "пластиковое окно как выбрать профиль",
], "POST_STEP11_CLUSTER_COHERENCE__WINDOW_PROFILE_SELECTION")
remap("WINDOW_HARDWARE_INFO", "GLASS_UNIT_SELECTION_INFO", [
    "как выбрать стеклопакет для пластиковых окон",
], "POST_STEP11_CLUSTER_COHERENCE__GLASS_UNIT_SELECTION")
remap("WINDOW_SELECTION_INFO", "WINDOW_HARDWARE_INFO", [
    "как выбрать резинку для окна пластикового",
], "POST_STEP11_CLUSTER_COHERENCE__SEAL_COMPONENT_SELECTION")
remap("FRENCH_WINDOWS_COMMERCIAL", "FRENCH_WINDOW_DEFINITION_INFO", [
    "что значит французское окно",
], "POST_STEP11_PHRASE_QA__DEFINITION_NOT_COMMERCIAL")

# 9. Comparison cluster split where the current site has materially different specific owners.
remap("WINDOW_COMPARISON_INFO", "REHAU_VEKA_COMPARISON_INFO", [
    "какие окна лучше veka или rehau",
    "какие окна лучше веко или rehau",
    "окна rehau или veka",
    "окна veka или rehau какие",
    "окна veka или rehau что лучше",
    "пластиковые окна veka или rehau что лучше",
], "POST_STEP11_CLUSTER_COHERENCE__REHAU_VEKA_COMPARISON")
remap("WINDOW_HARDWARE_INFO", "REHAU_VEKA_COMPARISON_INFO", [
    "какой профиль окон лучше veka или rehau",
], "POST_STEP11_CLUSTER_COHERENCE__REHAU_VEKA_COMPARISON")
remap("WINDOW_COMPARISON_INFO", "REHAU_KALEVA_COMPARISON_INFO", [
    "сравнение окон rehau и kaleva",
], "POST_STEP11_CLUSTER_COHERENCE__REHAU_KALEVA_COMPARISON")
remap("WINDOW_COMPARISON_INFO", "REHAU_INTERNAL_COMPARISON_INFO", [
    "окна rehau сравнение",
    "чем отличается окна rehau delight от rehau",
], "POST_STEP11_CLUSTER_COHERENCE__REHAU_INTERNAL_PROFILE_COMPARISON")
remap("WINDOW_COMPARISON_INFO", "REHAU_OTHER_BRAND_COMPARISON_INFO", [
    "окна kbe или rehau что лучше",
    "окна melke и rehau сравнить",
    "окна melke чем отличаются от rehau",
], "POST_STEP11_CLUSTER_COHERENCE__REHAU_OTHER_BRAND_COMPARISON")
remap("REHAU_WINDOWS_COMMERCIAL", "REHAU_OTHER_BRAND_COMPARISON_INFO", [
    "окна melke и rehau",
], "POST_STEP11_CLUSTER_COHERENCE__REHAU_OTHER_BRAND_COMPARISON")
remap("WINDOW_COMPARISON_INFO", "PVC_ALUMINIUM_COMPARISON_INFO", [
    "какие окна лучше пластиковые или алюминиевые",
    "какие окна пластиковые или алюминиевые",
    "пластиковые и алюминиевые окна разница",
    "пластиковые или алюминиевые окна",
    "что лучше пластиковые или алюминиевые окна",
], "POST_STEP11_CLUSTER_COHERENCE__PVC_ALUMINIUM_COMPARISON")
remap("WINDOW_COMPARISON_INFO", "ALUMINIUM_WINDOW_TECH_INFO", [
    "чем отличаются алюминиевые окна",
], "POST_STEP11_CLUSTER_COHERENCE__ALUMINIUM_TECH_TASK")


NEW_META = {
    "OUTDOOR_GLAZING_SELECTION_INFO": ("OUTDOOR_GLAZING", "choose veranda/outdoor glazing type, system or material", "INFO", "ADJACENT"),
    "OUTDOOR_GLAZING_SPECIALIZED_INFO": ("OUTDOOR_GLAZING", "understand specialized veranda glazing techniques/materials", "INFO", "ADJACENT"),
    "OUTDOOR_GLAZING_REVIEWS_INFO": ("OUTDOOR_GLAZING", "read reviews/experience about veranda glazing", "INFO", "ADJACENT"),
    "WINDOW_PRODUCT_REVIEWS_INFO": ("WINDOW_INFO", "read product/model reviews or ratings for windows/doors", "INFO", "ADJACENT"),
    "WINDOW_PROVIDER_REVIEWS_INFO": ("WINDOW_INFO", "compare/review window installation or repair providers", "INFO", "ADJACENT"),
    "BALCONY_GLAZING_SELECTION_INFO": ("GLAZING_INFO", "choose balcony glazing type/specification", "INFO", "ADJACENT"),
    "BALCONY_GLAZING_PROVIDER_REVIEWS_INFO": ("GLAZING_INFO", "compare/review balcony glazing providers", "INFO", "ADJACENT"),
    "WINDOW_OPERATION_MODE_INFO": ("WINDOW_INFO", "understand/set summer or winter window operating mode", "DIY_INFO", "ADJACENT"),
    "REHAU_WINDOW_TECH_INFO": ("WINDOW_INFO", "understand Rehau window systems/construction/types", "INFO", "ADJACENT"),
    "PVC_WINDOW_COLOR_INFO": ("WINDOW_INFO", "understand/select PVC/Rehau window colors and finishes", "INFO", "ADJACENT"),
    "ALUMINIUM_WINDOW_TECH_INFO": ("WINDOW_INFO", "understand aluminium window types/construction/opening/properties", "INFO", "ADJACENT"),
    "PANORAMIC_WINDOW_TECH_INFO": ("WINDOW_INFO", "understand panoramic-window types/properties", "INFO", "ADJACENT"),
    "PVC_WINDOW_TECH_INFO": ("WINDOW_INFO", "understand PVC-window types/opening/properties", "INFO", "ADJACENT"),
    "FRENCH_WINDOW_DEFINITION_INFO": ("WINDOW_INFO", "understand what French windows are and their forms", "INFO", "ADJACENT"),
    "WINDOW_PRODUCT_VIDEO_INFO": ("WINDOW_INFO", "view generic window-product video information", "INFO", "ADJACENT"),
    "WINDOW_PROFILE_SELECTION_INFO": ("WINDOW_INFO", "choose PVC window profile/system", "INFO", "ADJACENT"),
    "GLASS_UNIT_SELECTION_INFO": ("WINDOW_INFO", "choose glazing unit for a PVC window", "INFO", "ADJACENT"),
    "REHAU_VEKA_COMPARISON_INFO": ("WINDOW_INFO", "compare Rehau and VEKA window profiles", "INFO", "ADJACENT"),
    "REHAU_KALEVA_COMPARISON_INFO": ("WINDOW_INFO", "compare Rehau and Kaleva window profiles", "INFO", "ADJACENT"),
    "REHAU_INTERNAL_COMPARISON_INFO": ("WINDOW_INFO", "compare Rehau profile systems/models", "INFO", "ADJACENT"),
    "REHAU_OTHER_BRAND_COMPARISON_INFO": ("WINDOW_INFO", "compare Rehau with other brands not covered by a current dedicated page", "INFO", "ADJACENT"),
    "PVC_ALUMINIUM_COMPARISON_INFO": ("WINDOW_INFO", "compare PVC and aluminium windows", "INFO", "ADJACENT"),
}


def owner(url, state, confidence, reason, evidence="POST_STEP11_PHRASE_QA|FIRST_PARTY_CURRENT|WEB_METHOD_AUDIT_20260831"):
    return {
        "PRIMARY_OWNER_URL_IF_RESOLVED": url,
        "OWNERSHIP_STATE": state,
        "OWNERSHIP_CONFIDENCE": confidence,
        "CONTRADICTIONS_UNCERTAINTY": reason,
        "EVIDENCE_PROVENANCE": evidence,
        "LAST_VERIFIED": "2026-08-31",
    }


NEW_OWNERS = {
    "OUTDOOR_GLAZING_SELECTION_INFO": owner("https://okno-msk.ru/verandy/", "OWNER_EXISTING", "HIGH", "Current veranda hub compares warm/cold systems, profiles/opening choices and application criteria; actual member phrases are veranda-selection tasks."),
    "OUTDOOR_GLAZING_SPECIALIZED_INFO": owner("", "NO_SUITABLE_EXISTING_PAGE", "HIGH", "Current veranda pages do not truthfully own frameless/liquid-glass/polycarbonate-thickness guidance as one current first-party task."),
    "OUTDOOR_GLAZING_REVIEWS_INFO": owner("", "NO_SUITABLE_EXISTING_PAGE", "HIGH", "No current page was verified as a generic veranda-glazing reviews/experience owner."),
    "WINDOW_PRODUCT_REVIEWS_INFO": owner("", "NO_SUITABLE_EXISTING_PAGE", "HIGH", "The current /otzyvy/ page is company/customer-review content, not a truthful owner for generic product/model ratings and reviews."),
    "WINDOW_PROVIDER_REVIEWS_INFO": owner("", "NO_SUITABLE_EXISTING_PAGE", "HIGH", "Unbranded provider/rating intent expects comparative reputation evidence; the target company's own reviews page is not a truthful generic provider-ranking owner."),
    "BALCONY_GLAZING_SELECTION_INFO": owner("https://okno-msk.ru/balkony-i-lodzhii/", "OWNER_EXISTING", "MEDIUM", "Current balcony hub plus its warm/cold depth supports the selection task; informational depth is distributed across the hub and children."),
    "BALCONY_GLAZING_PROVIDER_REVIEWS_INFO": owner("", "NO_SUITABLE_EXISTING_PAGE", "HIGH", "Generic best-company/rating/review intent is not truthfully owned by a first-party commercial balcony page."),
    "WINDOW_OPERATION_MODE_INFO": owner("https://okno-msk.ru/stati/kak-perevesti-plastikovoe-okno-v-zimnij-rezhim/", "OWNER_EXISTING", "HIGH", "Dedicated current article explains summer/winter modes and adjustment."),
    "REHAU_WINDOW_TECH_INFO": owner("https://okno-msk.ru/okna-rehau/sravnenie-profilej-rehau/", "OWNER_EXISTING", "HIGH", "Current Rehau comparison page covers system types, dimensions and technical characteristics."),
    "PVC_WINDOW_COLOR_INFO": owner("https://okno-msk.ru/okna-rehau/cvetnye-plastikovye-okna/", "OWNER_EXISTING", "HIGH", "Dedicated current colored-window hub exposes colors/finishes and product options."),
    "ALUMINIUM_WINDOW_TECH_INFO": owner("https://okno-msk.ru/stati/plyusy-i-minusy-ostekleniya-alyuminievymi-oknami/", "OWNER_EXISTING", "MEDIUM", "Current article covers aluminium-window construction differences, opening mechanisms, thermal variants and appearance; broad technical cluster remains deliberately informational."),
    "PANORAMIC_WINDOW_TECH_INFO": owner("https://okno-msk.ru/stati/panoramnoe-osteklenie-eto-dan-mode-ili-praktichnoe-reshenie/", "OWNER_EXISTING", "HIGH", "Dedicated current panoramic-glazing explanatory article matches the technical/informational task."),
    "PVC_WINDOW_TECH_INFO": owner("https://okno-msk.ru/stati/kak-vybrat-plastikovye-okna/", "OWNER_EXISTING", "MEDIUM", "Current guide covers construction, types/opening, profiles, glazing and other PVC-window properties."),
    "FRENCH_WINDOW_DEFINITION_INFO": owner("https://okno-msk.ru/okna-rehau/francuzskie-okna/", "OWNER_EXISTING", "HIGH", "Current French-window page explains the floor-to-ceiling form, use cases and opening types in addition to commercial CTA."),
    "WINDOW_PRODUCT_VIDEO_INFO": owner("", "NO_SUITABLE_EXISTING_PAGE", "MEDIUM", "No dedicated current first-party generic product-video owner was verified for the bare video queries."),
    "WINDOW_PROFILE_SELECTION_INFO": owner("https://okno-msk.ru/stati/kak-vybrat-plastikovye-okna/", "OWNER_EXISTING", "HIGH", "Current selection guide explicitly covers profile classes, manufacturers and choice criteria."),
    "GLASS_UNIT_SELECTION_INFO": owner("https://okno-msk.ru/stati/kak-vybrat-steklopaket-dlya-plastikovogo-okna/", "OWNER_EXISTING", "HIGH", "Dedicated current glass-unit selection article exactly matches the task."),
    "REHAU_VEKA_COMPARISON_INFO": owner("https://okno-msk.ru/stati/sravnenie-okon-rehau-i-veka/", "OWNER_EXISTING", "HIGH", "Dedicated current Rehau-vs-VEKA comparison article exactly matches the task."),
    "REHAU_KALEVA_COMPARISON_INFO": owner("https://okno-msk.ru/stati/sravnenie-okonnyh-profilej-rehau-i-kaleva/", "OWNER_EXISTING", "HIGH", "Dedicated current Rehau-vs-Kaleva comparison article exactly matches the task."),
    "REHAU_INTERNAL_COMPARISON_INFO": owner("https://okno-msk.ru/okna-rehau/sravnenie-profilej-rehau/", "OWNER_EXISTING", "HIGH", "Dedicated current Rehau profile-comparison page matches internal model/system comparison."),
    "REHAU_OTHER_BRAND_COMPARISON_INFO": owner("", "NO_SUITABLE_EXISTING_PAGE", "HIGH", "No current dedicated KBE/Melke-vs-Rehau comparison owner was verified; do not force these queries onto the generic Rehau hub."),
    "PVC_ALUMINIUM_COMPARISON_INFO": owner("https://okno-msk.ru/stati/plyusy-i-minusy-ostekleniya-alyuminievymi-oknami/", "OWNER_EXISTING", "HIGH", "Current article explicitly compares aluminium and PVC window choices and their differences."),
}

OWNER_OVERRIDES = {
    "WINDOW_ACCESSORY_SELECTION_INFO": owner("https://okno-msk.ru/okna-rehau/aksessuary-dlya-okon/podokonniki/", "OWNER_EXISTING", "HIGH", "The only member phrase asks how to choose a PVC windowsill; the current windowsill page compares materials/types/dimensions and explicitly supports selection."),
    "WINDOW_HARDWARE_SHOPPING": owner("", "NO_SUITABLE_EXISTING_PAGE", "MEDIUM", "The 239-row cluster includes broad aftermarket hardware/components and many third-party systems; the current target accessory hub does not truthfully own that full catalog demand."),
}

REVIEWED_WEAK_CLUSTERS = {
    "WINDOWS_DOORS_COMBINED_COMMERCIAL",
    "GENERAL_GLAZING_SERVICE",
    "WINDOW_REPLACEMENT_SERVICE",
    "WINDOW_HARDWARE_SHOPPING",
    "WINDOW_REVIEWS_INFO",
    "WINDOW_PRODUCT_TECH_INFO",
    "WINDOW_REPAIR_DIY_INFO",
    "WINDOW_HARDWARE_INFO",
    "WINDOW_ACCESSORY_SELECTION_INFO",
    "BALCONY_GLAZING_INFO",
    "GLAZING_SELECTION_INFO",
}


def main():
    assignments = read_tsv(ASSIGNMENTS)
    summary_rows = read_tsv(CLUSTER_SUMMARY)
    owner_rows = read_tsv(ORIGINAL_OWNERSHIP)

    phrase_index = {r["phrase"]: r for r in assignments}
    if len(phrase_index) != len(assignments):
        raise RuntimeError("Step10 assignment phrase keys are not unique")

    # Every correction is checked against the immutable historical source before application.
    correction_rows = []
    for phrase, c in CORRECTIONS.items():
        src = phrase_index.get(phrase)
        if src is None:
            raise RuntimeError(f"correction phrase missing from Step10 final ledger: {phrase}")
        if src["assignment_status"] != "ASSIGNED":
            raise RuntimeError(f"correction phrase not ASSIGNED in Step10: {phrase} -> {src['assignment_status']}")
        if src["cluster_id"] != c["expected_original_cluster_id"]:
            raise RuntimeError(
                f"correction old-cluster mismatch: {phrase}: expected={c['expected_original_cluster_id']} actual={src['cluster_id']}"
            )
        correction_rows.append({"phrase": phrase, **c})

    write_tsv(
        OUT_CORRECTIONS,
        correction_rows,
        ["phrase", "expected_original_cluster_id", "effective_assignment_status", "effective_cluster_id", "correction_reason"],
    )

    original_summary = {r["cluster_id"]: r for r in summary_rows}
    original_owners = {r["CLUSTER_ID"]: r for r in owner_rows}

    # Confirm that every originally weak ownership cluster was explicitly re-audited.
    weak_original = {cid for cid, r in original_owners.items() if r.get("OWNERSHIP_CONFIDENCE") in {"MEDIUM", "LOW"}}
    missing_weak_review = sorted(weak_original - REVIEWED_WEAK_CLUSTERS)
    if missing_weak_review:
        raise RuntimeError(f"weak ownership clusters not re-audited: {missing_weak_review}")

    active_source = [r for r in assignments if r["assignment_status"] in {"ASSIGNED", "SEARCH_REQUIRED"}]
    effective = []
    for src in active_source:
        phrase = src["phrase"]
        c = CORRECTIONS.get(phrase)
        effective_status = c["effective_assignment_status"] if c else src["assignment_status"]
        effective_cluster = c["effective_cluster_id"] if c else src["cluster_id"]

        if effective_status == "SEARCH_REQUIRED":
            effective.append({
                "phrase": phrase,
                "original_assignment_status": src["assignment_status"],
                "original_cluster_id": src["cluster_id"],
                "effective_assignment_status": "SEARCH_REQUIRED",
                "effective_cluster_id": "",
                "cluster_user_task": "",
                "intent_type": "",
                "business_fit": "",
                "assignment_confidence": src.get("assignment_confidence", ""),
                "target_url": "",
                "ownership_state": "PAGE_OWNERSHIP_NOT_APPLICABLE_UNTIL_TASK_RESOLVED",
                "ownership_confidence": "",
                "page_mapping_applicability": "NOT_APPLICABLE_UNTIL_TASK_RESOLVED",
                "mapping_reason": c["correction_reason"] if c else "UPSTREAM_SEARCH_REQUIRED_PRESERVED",
                "evidence_provenance": src.get("evidence_mode", ""),
                "correction_source": "STEP_11_POST_AUDIT_CORRECTIONS.tsv" if c else "NONE",
            })
            continue

        if not effective_cluster:
            raise RuntimeError(f"assigned phrase has blank effective cluster: {phrase}")

        if effective_cluster in NEW_META:
            family, task, intent, business_fit = NEW_META[effective_cluster]
        elif effective_cluster in original_summary:
            m = original_summary[effective_cluster]
            family, task, intent, business_fit = m["family"], m["user_task"], m["intent_type"], m["business_fit"]
        else:
            raise RuntimeError(f"unknown effective cluster: {effective_cluster} for {phrase}")

        if effective_cluster in NEW_OWNERS:
            o = NEW_OWNERS[effective_cluster]
        elif effective_cluster in OWNER_OVERRIDES:
            o = OWNER_OVERRIDES[effective_cluster]
        elif effective_cluster in original_owners:
            o = original_owners[effective_cluster]
        else:
            raise RuntimeError(f"no ownership row for effective cluster: {effective_cluster}")

        state = o["OWNERSHIP_STATE"]
        target = o.get("PRIMARY_OWNER_URL_IF_RESOLVED", "")
        if state == "OWNER_EXISTING" and not target:
            raise RuntimeError(f"OWNER_EXISTING with blank target: {effective_cluster}")
        if state != "OWNER_EXISTING" and target:
            raise RuntimeError(f"non-owner state carries target URL: {effective_cluster}: {state}: {target}")

        effective.append({
            "phrase": phrase,
            "original_assignment_status": src["assignment_status"],
            "original_cluster_id": src["cluster_id"],
            "effective_assignment_status": "ASSIGNED",
            "effective_cluster_id": effective_cluster,
            "cluster_user_task": task,
            "intent_type": intent,
            "business_fit": business_fit,
            "assignment_confidence": src.get("assignment_confidence", ""),
            "target_url": target,
            "ownership_state": state,
            "ownership_confidence": o.get("OWNERSHIP_CONFIDENCE", ""),
            "page_mapping_applicability": "APPLICABLE",
            "mapping_reason": o.get("CONTRADICTIONS_UNCERTAINTY", ""),
            "evidence_provenance": o.get("EVIDENCE_PROVENANCE", ""),
            "correction_source": "STEP_11_POST_AUDIT_CORRECTIONS.tsv" if c else ("STEP_11_OWNER_OVERRIDE" if effective_cluster in OWNER_OVERRIDES else "NONE"),
        })

    map_fields = [
        "phrase", "original_assignment_status", "original_cluster_id", "effective_assignment_status", "effective_cluster_id",
        "cluster_user_task", "intent_type", "business_fit", "assignment_confidence", "target_url", "ownership_state",
        "ownership_confidence", "page_mapping_applicability", "mapping_reason", "evidence_provenance", "correction_source",
    ]
    write_tsv(OUT_MAP, effective, map_fields)

    assigned = [r for r in effective if r["effective_assignment_status"] == "ASSIGNED"]
    search_required = [r for r in effective if r["effective_assignment_status"] == "SEARCH_REQUIRED"]
    counts = Counter(r["effective_cluster_id"] for r in assigned)

    effective_summary_rows = []
    corrected_owner_rows = []
    for cid in sorted(counts):
        if cid in NEW_META:
            family, task, intent, business_fit = NEW_META[cid]
        else:
            m = original_summary[cid]
            family, task, intent, business_fit = m["family"], m["user_task"], m["intent_type"], m["business_fit"]

        o = NEW_OWNERS.get(cid) or OWNER_OVERRIDES.get(cid) or original_owners[cid]
        effective_summary_rows.append({
            "cluster_id": cid,
            "family": family,
            "user_task": task,
            "intent_type": intent,
            "business_fit": business_fit,
            "assigned_rows": counts[cid],
        })
        corrected_owner_rows.append({
            "CLUSTER_ID": cid,
            "CLUSTER_USER_TASK": task,
            "BUSINESS_FIT": business_fit,
            "PRIMARY_OWNER_URL_IF_RESOLVED": o.get("PRIMARY_OWNER_URL_IF_RESOLVED", ""),
            "OWNERSHIP_STATE": o["OWNERSHIP_STATE"],
            "OWNERSHIP_CONFIDENCE": o.get("OWNERSHIP_CONFIDENCE", ""),
            "CONTRADICTIONS_UNCERTAINTY": o.get("CONTRADICTIONS_UNCERTAINTY", ""),
            "EVIDENCE_PROVENANCE": o.get("EVIDENCE_PROVENANCE", ""),
            "LAST_VERIFIED": o.get("LAST_VERIFIED", "2026-08-31"),
        })

    write_tsv(OUT_SUMMARY, effective_summary_rows, ["cluster_id", "family", "user_task", "intent_type", "business_fit", "assigned_rows"])
    write_tsv(OUT_OWNERSHIP, corrected_owner_rows, [
        "CLUSTER_ID", "CLUSTER_USER_TASK", "BUSINESS_FIT", "PRIMARY_OWNER_URL_IF_RESOLVED", "OWNERSHIP_STATE",
        "OWNERSHIP_CONFIDENCE", "CONTRADICTIONS_UNCERTAINTY", "EVIDENCE_PROVENANCE", "LAST_VERIFIED",
    ])

    state_counts = Counter(r["OWNERSHIP_STATE"] for r in corrected_owner_rows)
    dropped_original_clusters = sorted(set(original_summary) - set(counts))
    added_effective_clusters = sorted(set(counts) - set(original_summary))

    qa = {
        "date": "2026-08-31",
        "status": "PASS_AFTER_EXTERNAL_METHOD_AUDIT_AND_PHRASE_LEVEL_CORRECTION",
        "step11_complete": True,
        "next_step_allowed": True,
        "step12_executed": False,
        "source_active_rows": len(active_source),
        "phrase_page_map_rows": len(effective),
        "source_assigned_rows": sum(r["assignment_status"] == "ASSIGNED" for r in active_source),
        "source_search_required_rows": sum(r["assignment_status"] == "SEARCH_REQUIRED" for r in active_source),
        "effective_assigned_rows": len(assigned),
        "effective_search_required_rows": len(search_required),
        "post_step11_correction_rows": len(CORRECTIONS),
        "effective_active_clusters": len(counts),
        "dropped_zero_member_original_clusters": dropped_original_clusters,
        "added_effective_clusters": added_effective_clusters,
        "ownership_state_counts": dict(sorted(state_counts.items())),
        "active_rows_accounted": len(effective) == len(active_source),
        "silent_active_drops": len(active_source) - len(effective),
        "duplicate_phrase_map_rows": len(effective) - len({r["phrase"] for r in effective}),
        "assigned_without_effective_cluster": sum(r["effective_assignment_status"] == "ASSIGNED" and not r["effective_cluster_id"] for r in effective),
        "search_required_with_target_url": sum(r["effective_assignment_status"] == "SEARCH_REQUIRED" and bool(r["target_url"]) for r in effective),
        "owner_existing_with_blank_target_url": sum(r["OWNERSHIP_STATE"] == "OWNER_EXISTING" and not r["PRIMARY_OWNER_URL_IF_RESOLVED"] for r in corrected_owner_rows),
        "non_owner_state_with_target_url": sum(r["OWNERSHIP_STATE"] != "OWNER_EXISTING" and bool(r["PRIMARY_OWNER_URL_IF_RESOLVED"]) for r in corrected_owner_rows),
        "original_medium_low_ownership_clusters": len(weak_original),
        "original_medium_low_ownership_clusters_reaudited": len(weak_original & REVIEWED_WEAK_CLUSTERS),
        "original_medium_low_ownership_clusters_missing_reaudit": missing_weak_review,
        "bridge_paid_replay_for_bookkeeping": 0,
        "new_bridge_requests_during_correction": 0,
        "new_bridge_cost_rub_during_correction": 0.0,
        "historical_step11_bridge_requests_preserved": 69,
        "historical_step11_bridge_cost_rub_preserved": 33.672,
        "known_historical_persistence_limitation": "No single consolidated full 680-ranked-row Step-11 TSV was produced in the original run; no paid replay was performed solely to reconstruct bookkeeping.",
        "target_url_semantics": "SEO-assigned intended owner; not claimed as proven Yandex relevant/ranking URL unless direct evidence exists.",
        "full_phrase_level_map_materialized": True,
        "cluster_coherence_gate_added": True,
        "bridge_codex_immediate_persistence_rule_added": True,
        "premature_step12_actions": 0,
        "premature_step13_cannibalization_verdicts": 0,
    }

    blocking = [
        qa["active_rows_accounted"],
        qa["silent_active_drops"] == 0,
        qa["duplicate_phrase_map_rows"] == 0,
        qa["assigned_without_effective_cluster"] == 0,
        qa["search_required_with_target_url"] == 0,
        qa["owner_existing_with_blank_target_url"] == 0,
        qa["non_owner_state_with_target_url"] == 0,
        not missing_weak_review,
    ]
    if not all(blocking):
        qa["status"] = "FAIL"
        qa["step11_complete"] = False
        qa["next_step_allowed"] = False

    OUT_QA.write_text(json.dumps(qa, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    weak_report = f"""# Step 11 — weak ownership re-audit\n\nDate: 2026-08-31\n\nThis audit was introduced after external method review showed that cluster-only ownership could hide heterogeneous Step-10 membership. All original Step-11 MEDIUM/LOW ownership clusters were explicitly re-audited against their member phrases.\n\n```text\nORIGINAL_MEDIUM_LOW_CLUSTERS = {len(weak_original)}\nREAUDITED = {len(weak_original & REVIEWED_WEAK_CLUSTERS)}\nMISSING = {len(missing_weak_review)}\n```\n\nMaterial corrections:\n\n- `GENERAL_GLAZING_SERVICE`: invalid generic cluster; all members were reassigned to aluminium/panoramic/French/outside-brand tasks.\n- `GLAZING_SELECTION_INFO`: invalid generic/non-balcony boundary; actual phrases were veranda-specific and were split into selection, specialized-technique and reviews tasks.\n- `WINDOW_REPLACEMENT_SERVICE`: component replacements and balcony/French transformations were removed from whole-window replacement.\n- `WINDOW_HARDWARE_SHOPPING`: ownership changed from the accessory hub to `NO_SUITABLE_EXISTING_PAGE` because the broad aftermarket/third-party catalog demand is not truthfully covered by the current target site.\n- `WINDOW_REVIEWS_INFO`: split into product/model reviews vs provider/service ratings; neither is truthfully owned by the company's own `/otzyvy/` page.\n- `WINDOW_PRODUCT_TECH_INFO`: split by product family and task; current dedicated pages/articles are used where they actually exist.\n- `WINDOW_REPAIR_DIY_INFO`: six bare DIY/instruction phrases returned to `SEARCH_REQUIRED` instead of being forced into repair.\n- `WINDOW_HARDWARE_INFO`: glass-unit/profile/comparison phrases moved to more precise tasks; remaining broad hardware information retains no-suitable-page treatment.\n- `WINDOW_ACCESSORY_SELECTION_INFO`: false negative fixed; its only phrase is windowsill selection and the current windowsill page is a truthful owner.\n- `BALCONY_GLAZING_INFO`: split into selection vs provider/review tasks.\n- `GLAZING_SELECTION_INFO` original unresolved state disappears because its actual phrase membership was reclassified instead of being reinterpreted from one representative query.\n- `WINDOWS_DOORS_COMBINED_COMMERCIAL`: phrase-level review did not expose a material coherence defect; homepage ownership remains MEDIUM.\n\nNo Step-12 structural action and no Step-13 cannibalization verdict was made.\n"""
    OUT_WEAK_AUDIT.write_text(weak_report, encoding="utf-8")

    report = f"""# Step 11 — Page ownership report (corrected after external method audit)\n\nDate: 2026-08-31\n\n## Corrected status\n\n`{qa['status']}`\n\nThe original Step-11 pass was substantially correct at the cluster→page level but was not complete as a final keyword map. External method audit and owner instruction required two permanent corrections:\n\n1. Bridge/Codex acquisition evidence must be saved to GitHub and read back immediately after each interaction before the next acquisition interaction.\n2. Step 11 must materialize the complete active `phrase → effective cluster → target URL/state` map and use it as a semantic-integrity QA surface.\n\nThe registered reusable method is `../../STEP_11_PAGE_OWNERSHIP_METHOD.md`.\n\n## External method basis\n\n- Semrush keyword mapping: https://www.semrush.com/blog/keyword-mapping/\n- Ahrefs keyword mapping: https://ahrefs.com/blog/keyword-mapping/\n- Ahrefs keyword clustering: https://ahrefs.com/blog/keyword-clustering/\n- Rush Analytics relevant URLs for clusters: https://www.rush-analytics.ru/faq/klasterizaciya/opredelenie-relevantnyh-url-dlya-klasterov\n- Topvisor target URL terminology: https://topvisor.com/ru/support/rankings/target-url/\n- Yandex page/query guidance: https://yandex.ru/support/webmaster/ru/recommendations/targeting and https://yandex.ru/support/webmaster/ru/service/queries-export\n\n## Corrected accounting\n\n```text\nSOURCE_ACTIVE_ROWS = {len(active_source)}\nSOURCE_ASSIGNED_ROWS = {qa['source_assigned_rows']}\nSOURCE_SEARCH_REQUIRED_ROWS = {qa['source_search_required_rows']}\nPOST_STEP11_CORRECTION_ROWS = {len(CORRECTIONS)}\nEFFECTIVE_ASSIGNED_ROWS = {len(assigned)}\nEFFECTIVE_SEARCH_REQUIRED_ROWS = {len(search_required)}\nPHRASE_PAGE_MAP_ROWS = {len(effective)}\nEFFECTIVE_ACTIVE_CLUSTERS = {len(counts)}\nSILENT_ACTIVE_DROPS = {qa['silent_active_drops']}\n```
\nOwnership states across effective assigned clusters:\n\n```text\n""" + "\n".join(f"{k} = {v}" for k, v in sorted(state_counts.items())) + """\n```\n\nThe effective cluster count may differ from the historical Step-10 count because the original Step-10 files are preserved unchanged and corrections are applied as an explicit post-Step-11 overlay. Zero-member historical clusters are not carried forward as fake active clusters.\n\n## Material defects corrected\n\nSee `STEP_11_WEAK_OWNERSHIP_REAUDIT.md` and `STEP_11_POST_AUDIT_CORRECTIONS.tsv`. Major categories were false generic glazing, veranda-selection boundary, replacement-vs-component mixing, review intent mixing, balcony selection-vs-provider review mixing, broad product-tech mixing, bare DIY ambiguity, profile/glass-unit misclassification, and overly broad comparison ownership.\n\n## Phrase-level mapping\n\n`STEP_11_PHRASE_PAGE_MAP.tsv` is now the required keyword-map deliverable. Every active Step-10 row appears exactly once. It preserves original assignment fields alongside effective corrected assignment and ownership state.\n\n`TARGET_URL` means intended SEO owner, not a proven Yandex ranking/relevant URL. The original Step-11 Search batch observed zero target-domain TOP10 hits and there was no authorized Webmaster property, so the corrected report does not manufacture Yandex query↔URL ownership evidence.\n\n## Search-required handoff\n\nThe original 13 Step-10 `SEARCH_REQUIRED` rows remain unresolved for page ownership. Phrase-level coherence correction adds six bare DIY/instruction rows, producing {len(search_required)} effective `SEARCH_REQUIRED` rows. They have no target URL and must be semantically resolved before any page action.\n\n## Provider / persistence truth\n\nNo new paid Yandex Marketing Bridge calls were needed for this correction. The historical Step-11 provider accounting remains 69 requests / 33.672 RUB. The historical limitation remains explicit: no single consolidated 680-ranked-row raw/normalized Step-11 TSV was produced. No paid replay was performed solely to reconstruct that bookkeeping.\n\nThe corrected reusable method now blocks every future Bridge/Codex acquisition sequence at: result → immediate GitHub save → GitHub readback/completeness verification → next interaction.\n\n## Step boundary\n\nNo Step-12 structural action was executed. No Step-13 cannibalization verdict was made.\n\nStep 11 is accepted only if `STEP_11_QA.json` is PASS and all generated final artifacts are committed and read back from GitHub.\n"""
    report = report.replace("{len(search_required)}", str(len(search_required)))
    if "{len(" in report:
        raise RuntimeError("unrendered dynamic placeholder remains in Step11 report")
    OUT_REPORT.write_text(report, encoding="utf-8")

    if qa["status"] == "FAIL":
        raise SystemExit(2)

    print(json.dumps({
        "status": qa["status"],
        "active": len(effective),
        "assigned": len(assigned),
        "search_required": len(search_required),
        "corrections": len(CORRECTIONS),
        "clusters": len(counts),
        "ownership_states": dict(state_counts),
    }, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
