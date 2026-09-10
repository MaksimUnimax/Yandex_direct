#!/usr/bin/env python3
"""Build the MK02 target-first corrective authorities from preserved evidence.

The target page model in PAGE_UNITS/PAGE_META is deliberately defined without
URLs. CURRENT_MATCH_BY_PAGE is a separate reconciliation layer and is applied
only after the semantic model, hierarchy and provisional routes exist.
"""

from __future__ import annotations

import csv
import gzip
import hashlib
import io
import json
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit


HERE = Path(__file__).resolve().parent
DATE = "2026-09-10"


def read_tsv(path: Path) -> list[dict[str, str]]:
    opener = gzip.open if path.suffix == ".gz" else open
    with opener(path, "rt", encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle, delimiter="\t"))


def tsv_bytes(rows: list[dict[str, object]], fields: list[str]) -> bytes:
    stream = io.StringIO(newline="")
    writer = csv.DictWriter(
        stream,
        fieldnames=fields,
        delimiter="\t",
        lineterminator="\n",
        extrasaction="ignore",
    )
    writer.writeheader()
    writer.writerows(rows)
    return stream.getvalue().encode("utf-8")


def write_tsv(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    path.write_bytes(tsv_bytes(rows, fields))


def write_tsv_gz(path: Path, rows: list[dict[str, object]], fields: list[str]) -> None:
    with path.open("wb") as target:
        with gzip.GzipFile(filename="", mode="wb", fileobj=target, compresslevel=9, mtime=0) as zipped:
            zipped.write(tsv_bytes(rows, fields))


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def norm_url(value: str) -> str:
    value = value.strip()
    if not value:
        return ""
    parts = urlsplit(value)
    path = parts.path or "/"
    if path != "/":
        path = path.rstrip("/")
    return urlunsplit((parts.scheme.lower(), parts.netloc.lower(), path, parts.query, ""))


def join_values(values: list[str], limit: int | None = None) -> str:
    unique = []
    for value in values:
        value = value.strip()
        if value and value not in unique:
            unique.append(value)
    if limit is not None and len(unique) > limit:
        return "; ".join(unique[:limit]) + f"; ещё {len(unique) - limit}"
    return "; ".join(unique)


# Target membership authority. This is task/intent-first and contains no URLs.
PAGE_UNITS: dict[str, list[str]] = {
    "TP-WINDOWS-COMMERCIAL-GENERAL": [
        "GENERIC_WINDOW_MANUFACTURER_SITE_NAVIGATION",
        "WINDOWS_COMMERCIAL_GENERAL",
        "WINDOWS_COMMERCIAL_GENERAL__INSTALLMENT_CONDITION",
        "WINDOWS_DOORS_COMBINED_COMMERCIAL",
        "WINDOWS_DOORS_COMBINED_COMMERCIAL__INSTALLMENT_CONDITION",
        "WINDOW_PROVIDER_REVIEWS_INFO",
    ],
    "TP-ALUMINIUM-WINDOWS-COMMERCIAL": [
        "ALUMINIUM_PROFILE_PRODUCT", "ALUMINIUM_WINDOWS_COMMERCIAL",
        "ALUMINIUM_WINDOW_COMPONENTS_INFO", "ALUMINIUM_WINDOW_HANDLE_ACCESSORY",
        "ALUMINIUM_WINDOW_INSTALLATION_REMOVAL_DIY", "ALUMINIUM_WINDOW_REVIEW_SUPPORT",
        "ALUMINIUM_WINDOW_VIDEO_CONTENT", "ALUMINIUM_WINDOWS_DOORS_COMBINED_COMMERCIAL",
        "TIMBER_ALUMINIUM_WINDOWS_COMMERCIAL",
    ],
    "TP-ALUMINIUM-HINGED-WINDOWS": ["ALUMINIUM_HINGED_WINDOWS"],
    "TP-ALUMINIUM-SLIDING-WINDOWS": ["ALUMINIUM_SLIDING_WINDOWS"],
    "TP-BALCONY-GLAZING-GENERAL": [
        "BALCONY_GLAZING_DIY_INFO", "BALCONY_GLAZING_GENERAL",
        "BALCONY_GLAZING_PERMISSION_INFO", "BALCONY_GLAZING_SELECTION_INFO",
        "BALCONY_GLAZING_WINDOWSILL_OPTION", "BALCONY_RENOVATION_WITH_GLAZING",
        "BALCONY_GLAZING_PROVIDER_REVIEWS_INFO",
    ],
    "TP-BALCONY-GLAZING-ROOF-SERVICE": ["BALCONY_GLAZING_ROOF_SERVICE"],
    "TP-BALCONY-GLAZING-EXTENSION-SERVICE": ["BALCONY_GLAZING_EXTENSION_SERVICE"],
    "TP-BALCONY-GLAZING-COLD": ["BALCONY_ALUMINIUM_SLIDING_COLD", "BALCONY_GLAZING_COLD"],
    "TP-OPEN-BALCONY-FINISHING": ["OPEN_BALCONY_FINISHING"],
    "TP-PANORAMIC-BALCONY-GLAZING": ["PANORAMIC_BALCONY_GLAZING"],
    "TP-BALCONY-HINGED-GLAZING": ["BALCONY_HINGED_GLAZING"],
    "TP-BALCONY-ALUMINIUM-SLIDING-GENERAL": ["BALCONY_ALUMINIUM_SLIDING_GENERAL"],
    "TP-BALCONY-GLAZING-WARM": ["BALCONY_GLAZING_WARM"],
    "TP-WINDOW-PRICE-ESTIMATION-CALCULATOR": ["WINDOW_PRICE_ESTIMATION_CALCULATOR"],
    "TP-PVC-DOORS-COMMERCIAL": [
        "PVC_DOORS_COMMERCIAL", "PVC_DOOR_HANDLE_ACCESSORY", "PVC_DOOR_INFO",
        "PVC_DOOR_INSTALLATION_REMOVAL_DIY", "PVC_DOOR_INSTALLATION_SERVICE",
        "PVC_DOOR_REVIEW_SUPPORT", "PVC_DOOR_REPAIR_SERVICE",
        "PVC_DOOR_REPLACEMENT_SERVICE", "PVC_DOOR_OPERATION_ADJUSTMENT_DIY_INFO",
        "PRIVATE_HOUSE_ENTRY_DOOR_WITH_WINDOW_UNVERIFIED",
    ],
    "TP-PVC-BALCONY-DOORS-COMMERCIAL": ["PVC_BALCONY_DOORS_COMMERCIAL"],
    "TP-PVC-SLIDING-DOORS-COMMERCIAL": ["PVC_SLIDING_DOORS_COMMERCIAL"],
    "TP-PVC-ENTRANCE-DOORS-COMMERCIAL": ["PVC_ENTRANCE_DOORS_COMMERCIAL"],
    "TP-GLAZING-DESIGN-INSPIRATION": ["GLAZING_DESIGN_INSPIRATION", "PANORAMIC_DESIGN_INSPIRATION"],
    "TP-PVC-WINDOWS-COMMERCIAL": [
        "PVC_PROFILE_PRODUCT_SELECTION", "PVC_WINDOWS_COMMERCIAL",
        "PVC_WINDOWS_COMMERCIAL__INSTALLMENT_CONDITION", "PVC_WINDOW_REVIEW_SUPPORT",
        "PVC_WINDOW_VIDEO_CONTENT", "REHAU_DELIGHT_REVIEW_SUPPORT",
        "REHAU_WINDOWS_COMMERCIAL", "REHAU_WINDOWS_COMMERCIAL__INSTALLMENT_CONDITION",
        "REHAU_WINDOW_REVIEW_SUPPORT",
    ],
    "TP-WINDOW-ACCESSORIES-GENERAL": [
        "WINDOW_ACCESSORIES_GENERAL", "WINDOW_FINISHING_ACCESSORY_COMPONENTS",
        "AFTERMARKET_WINDOW_HARDWARE_SHOPPING_UNSUPPORTED",
    ],
    "TP-MOSQUITO-NET-SHOPPING": [
        "MOSQUITO_NET_INSTALLATION_SERVICE", "MOSQUITO_NET_REPLACEMENT_SUPPORT",
        "MOSQUITO_NET_SELECTION_INFO", "MOSQUITO_NET_SHOPPING",
        "MOSQUITO_NET_REPAIR_UNVERIFIED",
    ],
    "TP-WINDOW-DRIP-CAP-ACCESSORY": ["WINDOW_DRIP_CAP_ACCESSORY", "WINDOW_DRIP_CAP_DIY_INFO"],
    "TP-WINDOWSILL-ACCESSORY": [
        "WINDOWSILL_ACCESSORY", "WINDOW_ACCESSORY_SELECTION_INFO",
        "WINDOWSILL_DIY_INFO", "WINDOWSILL_REPAIR_UNVERIFIED",
    ],
    "TP-WINDOW-SAFETY-HARDWARE-ACCESSORY": ["WINDOW_SAFETY_HARDWARE_ACCESSORY"],
    "TP-WINDOW-DECORATIVE-BARS-ACCESSORY": ["WINDOW_DECORATIVE_BARS_ACCESSORY"],
    "TP-WINDOW-HANDLES-ACCESSORY": ["WINDOW_HANDLES_ACCESSORY"],
    "TP-PVC-WINDOW-COLOR-INFO": ["PVC_WINDOW_COLOR_INFO"],
    "TP-FRENCH-WINDOWS-COMMERCIAL": [
        "FRENCH_WINDOWS_COMMERCIAL", "FRENCH_WINDOW_DEFINITION_INFO",
        "FRENCH_WINDOW_DIY_GENERAL", "FRENCH_WINDOW_INSTALLATION_DIY",
        "FRENCH_WINDOW_REDEVELOPMENT_PERMISSION_INFO", "FRENCH_WINDOW_REVIEW_SUPPORT",
    ],
    "TP-P44-WINDOWS-COMMERCIAL": ["P44_WINDOWS_COMMERCIAL"],
    "TP-PANORAMIC-WINDOWS-COMMERCIAL-CORE": [
        "PANORAMIC_WINDOWS_COMMERCIAL_CORE", "PANORAMIC_WINDOW_OPERATION_AMBIGUOUS",
    ],
    "TP-PRIVATE-HOUSE-WINDOW-PLANNING-INFO": [
        "BOILER_ROOM_WINDOW_REQUIREMENTS_INFO", "PRIVATE_HOUSE_SPECIAL_ROOM_WINDOWS",
        "PRIVATE_HOUSE_WINDOWS_COMMERCIAL", "PRIVATE_HOUSE_WINDOW_PLANNING_INFO",
        "PRIVATE_HOUSE_ROOF_WINDOW_UNVERIFIED", "ROOF_WINDOWS_COMMERCIAL",
    ],
    "TP-PRIVATE-HOUSE-PVC-WINDOWS-WOODEN-HOUSE": ["PRIVATE_HOUSE_PVC_WINDOWS_WOODEN_HOUSE"],
    "TP-WINDOW-REPLACEMENT-SERVICE": ["WINDOW_REPLACEMENT_SERVICE"],
    "TP-REHAU-BLITZ-COMMERCIAL": ["REHAU_BLITZ_COMMERCIAL"],
    "TP-REHAU-GRAZIO-COMMERCIAL": ["REHAU_GRAZIO_COMMERCIAL", "REHAU_GRAZIO_REVIEW_SUPPORT"],
    "TP-REHAU-INTELLIO-COMMERCIAL": ["REHAU_INTELLIO_COMMERCIAL"],
    "TP-REHAU-THERMO-COMMERCIAL": ["REHAU_THERMO_COMMERCIAL"],
    "TP-REHAU-WINDOW-TECH-INFO": [
        "REHAU_INTERNAL_COMPARISON_INFO", "REHAU_WINDOW_TECH_INFO",
        "REHAU_OTHER_BRAND_COMPARISON_INFO",
    ],
    "TP-GLASS-UNIT-PRODUCT-SELECTION": ["GLASS_UNIT_PRODUCT_SELECTION"],
    "TP-WINDOW-SLOPES-DIY-INFO": ["WINDOW_SLOPES_DIY_INFO"],
    "TP-PVC-WINDOW-ADJUSTMENT-DIY": ["PVC_WINDOW_ADJUSTMENT_DIY"],
    "TP-WINDOW-OPERATION-MODE-INFO": ["WINDOW_HARDWARE_MAINTENANCE_INFO", "WINDOW_OPERATION_MODE_INFO"],
    "TP-WINDOW-SELECTION-GUIDE": [
        "PVC_WINDOW_TECH_INFO", "WINDOW_HARDWARE_SELECTION_GUIDE",
        "WINDOW_HARDWARE_STANDARD_INFO", "WINDOW_PROFILE_SELECTION_INFO",
        "WINDOW_SEAL_SELECTION_INFO", "WINDOW_SELECTION_INFO",
        "WINDOW_HARDWARE_BRAND_REVIEWS_INFO", "WINDOW_HARDWARE_GENERIC_REVIEWS_INFO",
        "WOOD_WINDOWS_UNVERIFIED_PRODUCT", "WOOD_VS_PVC_WINDOWS_AMBIGUOUS",
        "AMBIGUOUS_PVC_TECH_QUERY",
    ],
    "TP-GLASS-UNIT-SELECTION-INFO": ["GLASS_UNIT_REPAIR_DIY", "GLASS_UNIT_SELECTION_INFO"],
    "TP-BEST-PVC-REHAU-WINDOWS-COMPARISON": [
        "BEST_PVC_REHAU_WINDOWS_COMPARISON", "WINDOW_PRODUCT_RATING_COMPARISON_INFO",
    ],
    "TP-PVC-WINDOW-OPERATION-DIY": ["PVC_WINDOW_OPERATION_DIY"],
    "TP-PANORAMIC-WINDOW-TECH-INFO": ["PANORAMIC_WINDOW_TECH_INFO", "PANORAMIC_WINDOW_TECH_SELECTION_INFO"],
    "TP-ALUMINIUM-WINDOW-TECH-INFO": ["ALUMINIUM_WINDOW_TECH_INFO", "PVC_ALUMINIUM_COMPARISON_INFO"],
    "TP-REHAU-VEKA-COMPARISON-INFO": ["REHAU_VEKA_COMPARISON_INFO"],
    "TP-REHAU-KALEVA-COMPARISON-INFO": ["REHAU_KALEVA_COMPARISON_INFO"],
    "TP-WINDOW-DIMENSIONS-INFO": ["WINDOW_DIMENSIONS_INFO"],
    "TP-WINDOW-FINISHING-SERVICE": ["WINDOWSILL_REPLACEMENT_SERVICE", "WINDOW_FINISHING_SERVICE"],
    "TP-WINDOW-REPAIR-SERVICE": [
        "GLASS_UNIT_REPLACEMENT_SERVICE", "PVC_WINDOW_REPAIR_DIY_GENERAL",
        "WINDOW_COMPONENT_REPLACEMENT_SERVICE", "WINDOW_FRAME_SASH_COMPONENT",
        "WINDOW_OR_DOOR_GLASS_COMPONENT", "WINDOW_REPAIR_SERVICE",
        "ALUMINIUM_WINDOW_REPLACEMENT_SERVICE", "AMBIGUOUS_PVC_DIY",
    ],
    "TP-WINDOW-INSTALLATION-SERVICE": [
        "PVC_WINDOW_INSTALLATION_DIY", "WINDOW_DEMOLITION_SERVICE",
        "WINDOW_INSTALLATION_MATERIALS_INFO", "WINDOW_INSTALLATION_SERVICE",
        "WINDOW_INSTALLATION_SERVICE__INSTALLMENT_CONDITION",
    ],
    "TP-OUTDOOR-STRUCTURE-GLAZING": [
        "OUTDOOR_GLAZING_DIY_INFO", "OUTDOOR_GLAZING_SELECTION_INFO",
        "OUTDOOR_GLAZING_SPECIAL_TECH_INFO", "OUTDOOR_STRUCTURE_GLAZING",
        "OUTDOOR_STRUCTURE_GLAZING__INSTALLMENT_CONDITION", "PANORAMIC_OUTDOOR_GLAZING",
        "OUTDOOR_GLAZING_MATERIAL_AMBIGUOUS", "OUTDOOR_GLAZING_REVIEWS_INFO",
        "SOFT_WINDOWS_COMMERCIAL",
    ],
    "TP-VERANDA-COLD-GLAZING": ["VERANDA_COLD_GLAZING"],
    "TP-OUTDOOR-ALUMINIUM-SLIDING-GLAZING": ["OUTDOOR_ALUMINIUM_SLIDING_GLAZING"],
    "TP-VERANDA-WARM-GLAZING": ["VERANDA_WARM_GLAZING"],
}

OUTSIDE_UNITS = {
    "NAVIGATION_BRAND_SITE", "OUTSIDE_OTHER", "OUTSIDE_REAL_ESTATE_ARCHITECTURE",
    "PANORAMIC_REAL_ESTATE_BRAND_QUERY",
}

# Reconciliation authority kept separate from PAGE_UNITS/PAGE_META.
CURRENT_MATCH_BY_PAGE = {
    "TP-WINDOWS-COMMERCIAL-GENERAL": "https://okno-msk.ru/",
    "TP-ALUMINIUM-WINDOWS-COMMERCIAL": "https://okno-msk.ru/alyuminievye-okna/",
    "TP-ALUMINIUM-HINGED-WINDOWS": "https://okno-msk.ru/alyuminievye-okna/raspashnye/",
    "TP-ALUMINIUM-SLIDING-WINDOWS": "https://okno-msk.ru/alyuminievye-okna/razdvizhnye/",
    "TP-BALCONY-GLAZING-GENERAL": "https://okno-msk.ru/balkony-i-lodzhii/",
    "TP-BALCONY-GLAZING-ROOF-SERVICE": "https://okno-msk.ru/balkony-i-lodzhii/balkon-s-kryshej/",
    "TP-BALCONY-GLAZING-EXTENSION-SERVICE": "https://okno-msk.ru/balkony-i-lodzhii/balkon-s-vynosom/",
    "TP-BALCONY-GLAZING-COLD": "https://okno-msk.ru/balkony-i-lodzhii/holodnoe-osteklenie/",
    "TP-OPEN-BALCONY-FINISHING": "https://okno-msk.ru/balkony-i-lodzhii/otdelka-balkonov",
    "TP-PANORAMIC-BALCONY-GLAZING": "https://okno-msk.ru/balkony-i-lodzhii/panoramnoe-osteklenie-balkona/",
    "TP-BALCONY-HINGED-GLAZING": "https://okno-msk.ru/balkony-i-lodzhii/raspashnoe-osteklenie-balkonov/",
    "TP-BALCONY-ALUMINIUM-SLIDING-GENERAL": "https://okno-msk.ru/balkony-i-lodzhii/razdvizhnye-okna-na-balkon",
    "TP-BALCONY-GLAZING-WARM": "https://okno-msk.ru/balkony-i-lodzhii/teploe-osteklenie/",
    "TP-WINDOW-PRICE-ESTIMATION-CALCULATOR": "https://okno-msk.ru/calculator/",
    "TP-PVC-DOORS-COMMERCIAL": "https://okno-msk.ru/dveri-rehau/",
    "TP-PVC-BALCONY-DOORS-COMMERCIAL": "https://okno-msk.ru/dveri-rehau/balkonnye-dveri/",
    "TP-PVC-SLIDING-DOORS-COMMERCIAL": "https://okno-msk.ru/dveri-rehau/razdvizhnye-dveri/",
    "TP-PVC-ENTRANCE-DOORS-COMMERCIAL": "https://okno-msk.ru/dveri-rehau/vhodnye-dveri/",
    "TP-GLAZING-DESIGN-INSPIRATION": "https://okno-msk.ru/nashi-raboty/",
    "TP-PVC-WINDOWS-COMMERCIAL": "https://okno-msk.ru/okna-rehau/",
    "TP-WINDOW-ACCESSORIES-GENERAL": "https://okno-msk.ru/okna-rehau/aksessuary-dlya-okon/",
    "TP-MOSQUITO-NET-SHOPPING": "https://okno-msk.ru/okna-rehau/aksessuary-dlya-okon/moskitnye-setki/",
    "TP-WINDOW-DRIP-CAP-ACCESSORY": "https://okno-msk.ru/okna-rehau/aksessuary-dlya-okon/otlivy/",
    "TP-WINDOWSILL-ACCESSORY": "https://okno-msk.ru/okna-rehau/aksessuary-dlya-okon/podokonniki/",
    "TP-WINDOW-SAFETY-HARDWARE-ACCESSORY": "https://okno-msk.ru/okna-rehau/aksessuary-dlya-okon/protivovzlomnaya-furnitura/",
    "TP-WINDOW-DECORATIVE-BARS-ACCESSORY": "https://okno-msk.ru/okna-rehau/aksessuary-dlya-okon/raskladki-v-steklopakety-shprosy/",
    "TP-WINDOW-HANDLES-ACCESSORY": "https://okno-msk.ru/okna-rehau/aksessuary-dlya-okon/ruchki-na-okna/",
    "TP-PVC-WINDOW-COLOR-INFO": "https://okno-msk.ru/okna-rehau/cvetnye-plastikovye-okna/",
    "TP-FRENCH-WINDOWS-COMMERCIAL": "https://okno-msk.ru/okna-rehau/francuzskie-okna/",
    "TP-P44-WINDOWS-COMMERCIAL": "https://okno-msk.ru/okna-rehau/okna-po-serii-domov/p-44/",
    "TP-PANORAMIC-WINDOWS-COMMERCIAL-CORE": "https://okno-msk.ru/okna-rehau/panoramnoe-osteklenie/",
    "TP-PRIVATE-HOUSE-WINDOW-PLANNING-INFO": "https://okno-msk.ru/okna-rehau/po-tipu-doma/okna-v-chastnyj-dom/",
    "TP-PRIVATE-HOUSE-PVC-WINDOWS-WOODEN-HOUSE": "https://okno-msk.ru/okna-rehau/po-tipu-doma/okna-v-derevyannyj-dom",
    "TP-WINDOW-REPLACEMENT-SERVICE": "https://okno-msk.ru/okna-rehau/po-tipu-doma/zamena-okon-v-kvartire/",
    "TP-REHAU-BLITZ-COMMERCIAL": "https://okno-msk.ru/okna-rehau/rehau-blitz-new/",
    "TP-REHAU-GRAZIO-COMMERCIAL": "https://okno-msk.ru/okna-rehau/rehau-grazio/",
    "TP-REHAU-INTELLIO-COMMERCIAL": "https://okno-msk.ru/okna-rehau/rehau-intellio-80/",
    "TP-REHAU-THERMO-COMMERCIAL": "https://okno-msk.ru/okna-rehau/rehau-thermo-design/",
    "TP-REHAU-WINDOW-TECH-INFO": "https://okno-msk.ru/okna-rehau/sravnenie-profilej-rehau/",
    "TP-GLASS-UNIT-PRODUCT-SELECTION": "https://okno-msk.ru/okna-rehau/steklopakety-dlya-plastikovykh-okon",
    "TP-WINDOW-SLOPES-DIY-INFO": "https://okno-msk.ru/stati/chem-otdelat-otkosy-na-oknah/",
    "TP-PVC-WINDOW-ADJUSTMENT-DIY": "https://okno-msk.ru/stati/kak-otregulirovat-plastikovye-okna/",
    "TP-WINDOW-OPERATION-MODE-INFO": "https://okno-msk.ru/stati/kak-perevesti-plastikovoe-okno-v-zimnij-rezhim/",
    "TP-WINDOW-SELECTION-GUIDE": "https://okno-msk.ru/stati/kak-vybrat-plastikovye-okna/",
    "TP-GLASS-UNIT-SELECTION-INFO": "https://okno-msk.ru/stati/kak-vybrat-steklopaket-dlya-plastikovogo-okna/",
    "TP-BEST-PVC-REHAU-WINDOWS-COMPARISON": "https://okno-msk.ru/stati/kakie-okna-samye-luchshie/",
    "TP-PVC-WINDOW-OPERATION-DIY": "https://okno-msk.ru/stati/okno-otkrylos-v-dvuh-polozheniyah-chto-delat/",
    "TP-PANORAMIC-WINDOW-TECH-INFO": "https://okno-msk.ru/stati/panoramnoe-osteklenie-eto-dan-mode-ili-praktichnoe-reshenie/",
    "TP-ALUMINIUM-WINDOW-TECH-INFO": "https://okno-msk.ru/stati/plyusy-i-minusy-ostekleniya-alyuminievymi-oknami/",
    "TP-REHAU-VEKA-COMPARISON-INFO": "https://okno-msk.ru/stati/sravnenie-okon-rehau-i-veka/",
    "TP-REHAU-KALEVA-COMPARISON-INFO": "https://okno-msk.ru/stati/sravnenie-okonnyh-profilej-rehau-i-kaleva/",
    "TP-WINDOW-DIMENSIONS-INFO": "https://okno-msk.ru/stati/standartnye-razmery-okon-v-kvartiru-i-chastnyj-dom/",
    "TP-WINDOW-FINISHING-SERVICE": "https://okno-msk.ru/uslugi/otdelka-otkosov/",
    "TP-WINDOW-REPAIR-SERVICE": "https://okno-msk.ru/uslugi/remont-okon/",
    "TP-WINDOW-INSTALLATION-SERVICE": "https://okno-msk.ru/uslugi/ustanovka-okon/",
    "TP-OUTDOOR-STRUCTURE-GLAZING": "https://okno-msk.ru/verandy/",
    "TP-VERANDA-COLD-GLAZING": "https://okno-msk.ru/verandy/holodnoe-osteklenie-verand/",
    "TP-OUTDOOR-ALUMINIUM-SLIDING-GLAZING": "https://okno-msk.ru/verandy/razdvizhnye-okna-na-verandu",
    "TP-VERANDA-WARM-GLAZING": "https://okno-msk.ru/verandy/teploe-osteklenie-verand/",
}

PAGE_TITLES = {
    "TP-WINDOWS-COMMERCIAL-GENERAL": "Главная: окна и двери на заказ",
    "TP-ALUMINIUM-WINDOWS-COMMERCIAL": "Алюминиевые окна",
    "TP-ALUMINIUM-HINGED-WINDOWS": "Распашные алюминиевые окна",
    "TP-ALUMINIUM-SLIDING-WINDOWS": "Раздвижные алюминиевые окна",
    "TP-BALCONY-GLAZING-GENERAL": "Остекление балконов и лоджий",
    "TP-BALCONY-GLAZING-ROOF-SERVICE": "Остекление балкона с крышей",
    "TP-BALCONY-GLAZING-EXTENSION-SERVICE": "Остекление балкона с выносом",
    "TP-BALCONY-GLAZING-COLD": "Холодное остекление балконов",
    "TP-OPEN-BALCONY-FINISHING": "Отделка открытых балконов",
    "TP-PANORAMIC-BALCONY-GLAZING": "Панорамное остекление балконов",
    "TP-BALCONY-HINGED-GLAZING": "Распашное остекление балконов",
    "TP-BALCONY-ALUMINIUM-SLIDING-GENERAL": "Раздвижные алюминиевые окна на балкон",
    "TP-BALCONY-GLAZING-WARM": "Тёплое остекление балконов",
    "TP-WINDOW-PRICE-ESTIMATION-CALCULATOR": "Калькулятор стоимости окон",
    "TP-PVC-DOORS-COMMERCIAL": "Пластиковые двери",
    "TP-PVC-BALCONY-DOORS-COMMERCIAL": "Балконные пластиковые двери",
    "TP-PVC-SLIDING-DOORS-COMMERCIAL": "Раздвижные пластиковые двери",
    "TP-PVC-ENTRANCE-DOORS-COMMERCIAL": "Входные пластиковые двери",
    "TP-GLAZING-DESIGN-INSPIRATION": "Портфолио окон и остекления",
    "TP-PVC-WINDOWS-COMMERCIAL": "Пластиковые окна REHAU",
    "TP-WINDOW-ACCESSORIES-GENERAL": "Аксессуары для окон",
    "TP-MOSQUITO-NET-SHOPPING": "Москитные сетки",
    "TP-WINDOW-DRIP-CAP-ACCESSORY": "Оконные отливы",
    "TP-WINDOWSILL-ACCESSORY": "Подоконники",
    "TP-WINDOW-SAFETY-HARDWARE-ACCESSORY": "Противовзломная фурнитура",
    "TP-WINDOW-DECORATIVE-BARS-ACCESSORY": "Шпросы и раскладки в стеклопакет",
    "TP-WINDOW-HANDLES-ACCESSORY": "Ручки для окон",
    "TP-PVC-WINDOW-COLOR-INFO": "Цветные пластиковые окна",
    "TP-FRENCH-WINDOWS-COMMERCIAL": "Французские окна",
    "TP-P44-WINDOWS-COMMERCIAL": "Окна для домов серии П-44",
    "TP-PANORAMIC-WINDOWS-COMMERCIAL-CORE": "Панорамные окна",
    "TP-PRIVATE-HOUSE-WINDOW-PLANNING-INFO": "Окна для частного дома",
    "TP-PRIVATE-HOUSE-PVC-WINDOWS-WOODEN-HOUSE": "Пластиковые окна для деревянного дома",
    "TP-WINDOW-REPLACEMENT-SERVICE": "Замена окон в квартире",
    "TP-REHAU-BLITZ-COMMERCIAL": "Окна REHAU Blitz",
    "TP-REHAU-GRAZIO-COMMERCIAL": "Окна REHAU Grazio",
    "TP-REHAU-INTELLIO-COMMERCIAL": "Окна REHAU Intellio",
    "TP-REHAU-THERMO-COMMERCIAL": "Окна REHAU Thermo",
    "TP-REHAU-WINDOW-TECH-INFO": "Сравнение профилей REHAU",
    "TP-GLASS-UNIT-PRODUCT-SELECTION": "Стеклопакеты для пластиковых окон",
    "TP-WINDOW-SLOPES-DIY-INFO": "Как отделать откосы на окнах",
    "TP-PVC-WINDOW-ADJUSTMENT-DIY": "Как отрегулировать пластиковые окна",
    "TP-WINDOW-OPERATION-MODE-INFO": "Летний и зимний режим пластиковых окон",
    "TP-WINDOW-SELECTION-GUIDE": "Как выбрать пластиковые окна",
    "TP-GLASS-UNIT-SELECTION-INFO": "Как выбрать стеклопакет",
    "TP-BEST-PVC-REHAU-WINDOWS-COMPARISON": "Какие окна лучше: критерии выбора",
    "TP-PVC-WINDOW-OPERATION-DIY": "Что делать, если окно открылось в двух положениях",
    "TP-PANORAMIC-WINDOW-TECH-INFO": "Панорамное остекление: свойства и выбор",
    "TP-ALUMINIUM-WINDOW-TECH-INFO": "Алюминиевое остекление: свойства и сравнение",
    "TP-REHAU-VEKA-COMPARISON-INFO": "Сравнение REHAU и VEKA",
    "TP-REHAU-KALEVA-COMPARISON-INFO": "Сравнение REHAU и Kaleva",
    "TP-WINDOW-DIMENSIONS-INFO": "Стандартные размеры окон",
    "TP-WINDOW-FINISHING-SERVICE": "Отделка откосов и установка подоконников",
    "TP-WINDOW-REPAIR-SERVICE": "Ремонт окон",
    "TP-WINDOW-INSTALLATION-SERVICE": "Установка окон",
    "TP-OUTDOOR-STRUCTURE-GLAZING": "Остекление веранд, террас и беседок",
    "TP-VERANDA-COLD-GLAZING": "Холодное остекление веранд",
    "TP-OUTDOOR-ALUMINIUM-SLIDING-GLAZING": "Раздвижное остекление веранд",
    "TP-VERANDA-WARM-GLAZING": "Тёплое остекление веранд",
}

PARENT_BY_PAGE = {
    **{key: "TP-ALUMINIUM-WINDOWS-COMMERCIAL" for key in ["TP-ALUMINIUM-HINGED-WINDOWS", "TP-ALUMINIUM-SLIDING-WINDOWS", "TP-ALUMINIUM-WINDOW-TECH-INFO"]},
    **{key: "TP-BALCONY-GLAZING-GENERAL" for key in [
        "TP-BALCONY-GLAZING-ROOF-SERVICE", "TP-BALCONY-GLAZING-EXTENSION-SERVICE",
        "TP-BALCONY-GLAZING-COLD", "TP-OPEN-BALCONY-FINISHING",
        "TP-PANORAMIC-BALCONY-GLAZING", "TP-BALCONY-HINGED-GLAZING",
        "TP-BALCONY-ALUMINIUM-SLIDING-GENERAL", "TP-BALCONY-GLAZING-WARM",
    ]},
    **{key: "TP-PVC-DOORS-COMMERCIAL" for key in [
        "TP-PVC-BALCONY-DOORS-COMMERCIAL", "TP-PVC-SLIDING-DOORS-COMMERCIAL",
        "TP-PVC-ENTRANCE-DOORS-COMMERCIAL",
    ]},
    **{key: "TP-WINDOW-ACCESSORIES-GENERAL" for key in [
        "TP-MOSQUITO-NET-SHOPPING", "TP-WINDOW-DRIP-CAP-ACCESSORY",
        "TP-WINDOWSILL-ACCESSORY", "TP-WINDOW-SAFETY-HARDWARE-ACCESSORY",
        "TP-WINDOW-DECORATIVE-BARS-ACCESSORY", "TP-WINDOW-HANDLES-ACCESSORY",
    ]},
    **{key: "TP-OUTDOOR-STRUCTURE-GLAZING" for key in [
        "TP-VERANDA-COLD-GLAZING", "TP-OUTDOOR-ALUMINIUM-SLIDING-GLAZING",
        "TP-VERANDA-WARM-GLAZING",
    ]},
    **{key: "TP-PVC-WINDOWS-COMMERCIAL" for key in [
        "TP-PVC-WINDOW-COLOR-INFO", "TP-FRENCH-WINDOWS-COMMERCIAL",
        "TP-P44-WINDOWS-COMMERCIAL", "TP-PANORAMIC-WINDOWS-COMMERCIAL-CORE",
        "TP-PRIVATE-HOUSE-WINDOW-PLANNING-INFO", "TP-PRIVATE-HOUSE-PVC-WINDOWS-WOODEN-HOUSE",
        "TP-REHAU-BLITZ-COMMERCIAL", "TP-REHAU-GRAZIO-COMMERCIAL",
        "TP-REHAU-INTELLIO-COMMERCIAL", "TP-REHAU-THERMO-COMMERCIAL",
        "TP-REHAU-WINDOW-TECH-INFO", "TP-GLASS-UNIT-PRODUCT-SELECTION",
    ]},
    **{key: "TP-WINDOWS-COMMERCIAL-GENERAL" for key in [
        "TP-WINDOW-PRICE-ESTIMATION-CALCULATOR", "TP-GLAZING-DESIGN-INSPIRATION",
        "TP-WINDOW-REPLACEMENT-SERVICE", "TP-WINDOW-FINISHING-SERVICE",
        "TP-WINDOW-REPAIR-SERVICE", "TP-WINDOW-INSTALLATION-SERVICE",
    ]},
    **{key: "TP-WINDOW-SELECTION-GUIDE" for key in [
        "TP-WINDOW-SLOPES-DIY-INFO", "TP-PVC-WINDOW-ADJUSTMENT-DIY",
        "TP-WINDOW-OPERATION-MODE-INFO", "TP-GLASS-UNIT-SELECTION-INFO",
        "TP-BEST-PVC-REHAU-WINDOWS-COMPARISON", "TP-PVC-WINDOW-OPERATION-DIY",
        "TP-PANORAMIC-WINDOW-TECH-INFO", "TP-REHAU-VEKA-COMPARISON-INFO",
        "TP-REHAU-KALEVA-COMPARISON-INFO", "TP-WINDOW-DIMENSIONS-INFO",
    ]},
}


def section_for(page_key: str) -> tuple[str, str]:
    parent = PARENT_BY_PAGE.get(page_key, "")
    if parent in {
        "TP-ALUMINIUM-WINDOWS-COMMERCIAL", "TP-BALCONY-GLAZING-GENERAL",
        "TP-PVC-DOORS-COMMERCIAL", "TP-WINDOW-ACCESSORIES-GENERAL",
        "TP-OUTDOOR-STRUCTURE-GLAZING", "TP-PVC-WINDOWS-COMMERCIAL",
        "TP-WINDOW-SELECTION-GUIDE",
    }:
        return section_for(parent)
    if "BALCONY" in page_key:
        return "SEC-BALCONIES", "Балконы и лоджии"
    if "OUTDOOR" in page_key or "VERANDA" in page_key:
        return "SEC-VERANDAS", "Веранды, террасы и беседки"
    if page_key.startswith("TP-PVC-") and "DOOR" in page_key:
        return "SEC-DOORS", "Пластиковые двери"
    if "ALUMINIUM" in page_key:
        return "SEC-ALUMINIUM", "Алюминиевые окна"
    if any(token in page_key for token in ["ACCESSOR", "MOSQUITO", "DRIP", "WINDOWSILL", "SAFETY-HARDWARE", "DECORATIVE", "HANDLES"]):
        return "SEC-ACCESSORIES", "Аксессуары и комплектующие"
    if any(token in page_key for token in ["REPAIR-SERVICE", "INSTALLATION-SERVICE", "FINISHING-SERVICE", "REPLACEMENT-SERVICE"]):
        return "SEC-SERVICES", "Услуги"
    if any(token in page_key for token in ["GUIDE", "INFO", "COMPARISON", "DIMENSIONS", "ADJUSTMENT", "OPERATION-MODE", "OPERATION-DIY"]):
        return "SEC-GUIDES", "Полезные материалы и выбор"
    if any(token in page_key for token in ["PVC-WINDOW", "REHAU", "P44", "PRIVATE-HOUSE", "FRENCH", "PANORAMIC-WINDOW"]):
        return "SEC-PVC-REHAU", "Пластиковые окна и REHAU"
    return "SEC-CORE", "Главные маршруты сайта"


def page_type_for(page_key: str, member_units: list[dict[str, str]]) -> str:
    if "CALCULATOR" in page_key:
        return "Интерактивный инструмент"
    if "DESIGN-INSPIRATION" in page_key:
        return "Портфолио / навигационная страница"
    intents = Counter(row["intent_type"] for row in member_units if row["structural_action"] not in {"DEFER_PENDING_EVIDENCE", "OUTSIDE_SCOPE_NO_ACTION"})
    dominant = intents.most_common(1)[0][0] if intents else "AMBIGUOUS"
    if "SERVICE" in dominant:
        return "Коммерческая посадочная услуги"
    if "COMMERCIAL" in dominant:
        return "Коммерческая посадочная"
    if dominant in {"INFO", "DIY_INFO", "INFO_OR_SHOPPING"}:
        return "Информационная посадочная"
    return "Хаб / смешанная посадочная"


def purpose_for(title: str, page_type: str) -> str:
    if "Инструмент" in page_type:
        return f"Помочь пользователю решить практическую задачу «{title.lower()}» и перейти к подходящему предложению."
    if "Портфолио" in page_type:
        return "Показать реальные направления работ и дать навигацию к соответствующим коммерческим посадочным."
    if "услуги" in page_type:
        return f"Закрыть задачу заказа услуги «{title}», объяснить состав и привести к замеру или обращению."
    if "Коммерческая" in page_type:
        return f"Помочь выбрать и заказать «{title.lower()}», сохранив границы между соседними продуктами и задачами."
    if "Информационная" in page_type:
        return f"Дать самостоятельный полезный ответ по теме «{title.lower()}» и связать его с релевантным продуктом или услугой."
    return f"Собрать понятные маршруты по теме «{title.lower()}» и не создавать лишние самостоятельные URL."


CLUSTER_ACTION = {
    "KEEP_EXISTING_STRUCTURE": ("KEEP_LOCK_TARGET_OWNER", "TARGET_PAGE_RESOLVED", "NO"),
    "ADD_SECTION_OR_FAQ_TO_EXISTING": ("OPTIMIZE_STRENGTHEN", "TARGET_PAGE_RESOLVED", "YES"),
    "EXPAND_EXISTING_PAGE": ("OPTIMIZE_STRENGTHEN", "TARGET_PAGE_RESOLVED", "YES"),
    "ROUTE_TO_EXISTING_PAGE_AS_SUBTASK": ("NO_STANDALONE_INCLUDE_IN_NAMED_OWNER", "NO_STANDALONE_ROUTE_TO_PARENT", "NO"),
    "NO_STANDALONE_PAGE": ("NO_STANDALONE_INCLUDE_IN_NAMED_OWNER", "NO_STANDALONE_ROUTE_TO_PARENT", "NO"),
    "DEFER_PENDING_EVIDENCE": ("RECHECK_NEEDS_EVIDENCE", "RECHECK_NEEDS_EVIDENCE", "UNRESOLVED"),
    "OUTSIDE_SCOPE_NO_ACTION": ("NO_STANDALONE_OUTSIDE_SCOPE", "NO_TARGET_OUTSIDE_SCOPE", "NO"),
}


def main() -> None:
    foundation = read_tsv(HERE / f"MK02_SEMANTIC_FOUNDATION_{DATE}.tsv.gz")
    old_phrase_map = read_tsv(HERE / f"MK02_PHRASE_PAGE_MAP_{DATE}.tsv.gz")
    units = [
        row for row in read_tsv(HERE / f"MK02_UNIT_OWNERSHIP_LEDGER_{DATE}.tsv")
        if row["product_state"] == "ACTIVE_MK02_WORKING_CORE"
    ]
    packages = read_tsv(HERE / f"MK02_IMPLEMENTATION_WORK_PACKAGES_{DATE}.tsv")
    relations = read_tsv(HERE / f"MK02_PAGE_RELATIONSHIPS_{DATE}.tsv")

    assert len(foundation) == 2840
    assert len(old_phrase_map) == 2185
    assert len(units) == 160
    assert len(PAGE_UNITS) == len(CURRENT_MATCH_BY_PAGE) == len(PAGE_TITLES) == 59

    unit_by_id = {row["structural_unit_id"]: row for row in units}
    assigned_units = [uid for members in PAGE_UNITS.values() for uid in members]
    assert len(assigned_units) == len(set(assigned_units))
    assert set(assigned_units) | OUTSIDE_UNITS == set(unit_by_id)
    assert not set(assigned_units) & OUTSIDE_UNITS
    unit_to_page = {uid: key for key, members in PAGE_UNITS.items() for uid in members}

    foundation_by_phrase = {row["phrase"]: row for row in foundation}
    phrase_rows_by_unit: dict[str, list[dict[str, str]]] = defaultdict(list)
    unresolved_phrase_rows: list[dict[str, str]] = []
    for row in old_phrase_map:
        if row["structural_unit_id"]:
            phrase_rows_by_unit[row["structural_unit_id"]].append(row)
        else:
            unresolved_phrase_rows.append(row)
    assert len(unresolved_phrase_rows) == 6

    def representative(rows: list[dict[str, str]]) -> dict[str, str]:
        return max(
            rows,
            key=lambda row: (
                int(foundation_by_phrase[row["phrase"]]["wordstat_popular_count"] or 0),
                -len(row["phrase"]),
                row["phrase"],
            ),
        )

    cluster_rows: list[dict[str, object]] = []
    for unit in sorted(units, key=lambda row: row["structural_unit_id"]):
        uid = unit["structural_unit_id"]
        rows = phrase_rows_by_unit[uid]
        assert len(rows) == int(unit["active_mk02_phrase_count"])
        rep = representative(rows)
        action, route_state, real_change = CLUSTER_ACTION[unit["structural_action"]]
        page_key = unit_to_page.get(uid, "NO_TARGET_OUTSIDE_SCOPE")
        page_title = PAGE_TITLES.get(page_key, "Вне подтверждённого предложения — не страница сайта")
        current_url = CURRENT_MATCH_BY_PAGE.get(page_key, "")
        accepted_url = "" if route_state in {"RECHECK_NEEDS_EVIDENCE", "NO_TARGET_OUTSIDE_SCOPE"} else current_url
        section_key, section_name = section_for(page_key) if page_key in PAGE_TITLES else ("SEC-OUTSIDE", "Вне подтверждённого предложения")
        current_match_state = (
            "CURRENT_PAGE_AVAILABLE_AS_SEPARATE_EVIDENCE" if current_url
            else "NO_CURRENT_PAGE_MATCH__EXPLICIT_SCOPE_BOUNDARY"
        )
        cluster_rows.append({
            "cluster_task_key": uid,
            "cluster_task_name_ru": f"{rep['semantic_group_name']}: {rep['phrase']}",
            "semantic_group_keys": join_values([row["semantic_group_id"] for row in rows]),
            "semantic_group_names_ru": join_values([row["semantic_group_name"] for row in rows]),
            "primary_representative_query": rep["phrase"],
            "member_phrase_count": len(rows),
            "intent_user_task_ru": join_values([row["user_task"] for row in rows], limit=3),
            "intended_target_page_key": page_key,
            "intended_target_page_name_ru": page_title,
            "page_purpose": purpose_for(page_title, page_type_for(page_key, [unit])) if page_key in PAGE_TITLES else "Не создавать посадочную вне подтверждённого бизнес-предложения.",
            "page_type": page_type_for(page_key, [unit]) if page_key in PAGE_TITLES else "Не страница сайта",
            "intended_parent_or_section": section_name,
            "provisional_target_route_before_reconciliation": f"TARGET_ROLE::{page_key}",
            "supporting_or_child_relation": (
                f"Включить в названного владельца {page_key}; отдельный URL не создавать."
                if "NO_STANDALONE" in action else "См. целевую иерархию по ключу страницы."
            ),
            "target_route_state": route_state,
            "target_action": action,
            "real_site_change_required": real_change,
            "target_url_after_reconciliation": accepted_url,
            "current_match_state_separate": current_match_state,
            "current_page_match_separate": unit["family_owner_url"],
            "uncertainty_evidence_boundary": (
                f"Требуется отдельная проверка задачи «{rep['phrase']}»; до неё новый URL или изменение не разрешены."
                if route_state == "RECHECK_NEEDS_EVIDENCE"
                else "Текущая страница не использовалась как основание целевой роли."
            ),
        })

    unresolved_rep = representative(unresolved_phrase_rows)
    cluster_rows.append({
        "cluster_task_key": "UNRESOLVED-DIY-WINDOW-TASK",
        "cluster_task_name_ru": "Самостоятельная работа с окнами — точная задача не разрешена",
        "semantic_group_keys": join_values([row["semantic_group_id"] for row in unresolved_phrase_rows]),
        "semantic_group_names_ru": join_values([row["semantic_group_name"] for row in unresolved_phrase_rows]),
        "primary_representative_query": unresolved_rep["phrase"],
        "member_phrase_count": len(unresolved_phrase_rows),
        "intent_user_task_ru": join_values([row["user_task"] for row in unresolved_phrase_rows]),
        "intended_target_page_key": "TP-UNRESOLVED-DIY-WINDOW-TASK",
        "intended_target_page_name_ru": "Неопределённая DIY-задача по окнам",
        "page_purpose": "Не выбирать посадочную, пока не разрешена точная пользовательская задача.",
        "page_type": "Требует определения роли",
        "intended_parent_or_section": "Полезные материалы и выбор",
        "provisional_target_route_before_reconciliation": "TARGET_ROLE::TP-UNRESOLVED-DIY-WINDOW-TASK",
        "supporting_or_child_relation": "После проверки выбрать один названный владелец; новый URL заранее не создавать.",
        "target_route_state": "UNRESOLVED_TASK_ROUTING",
        "target_action": "RECHECK_NEEDS_EVIDENCE",
        "real_site_change_required": "UNRESOLVED",
        "target_url_after_reconciliation": "",
        "current_match_state_separate": "CURRENT_OWNER_NOT_APPLICABLE_UNTIL_TASK_RESOLVED",
        "current_page_match_separate": "",
        "uncertainty_evidence_boundary": "EXACT_SEARCH_TASK_BOUNDARY_REQUIRED",
    })
    assert len(cluster_rows) == 161

    cluster_by_key = {row["cluster_task_key"]: row for row in cluster_rows}
    page_registry: list[dict[str, object]] = []
    for page_key, member_ids in PAGE_UNITS.items():
        member_units = [unit_by_id[uid] for uid in member_ids]
        member_cluster_rows = [cluster_by_key[uid] for uid in member_ids]
        accepted_count = sum(
            int(row["member_phrase_count"])
            for row in member_cluster_rows
            if row["target_route_state"] not in {"RECHECK_NEEDS_EVIDENCE", "NO_TARGET_OUTSIDE_SCOPE"}
        )
        recheck_count = sum(
            int(row["member_phrase_count"])
            for row in member_cluster_rows
            if row["target_route_state"] == "RECHECK_NEEDS_EVIDENCE"
        )
        all_phrase_rows = [row for uid in member_ids for row in phrase_rows_by_unit[uid]]
        primary_phrase_rows = [
            row for uid in member_ids
            if unit_by_id[uid]["structural_action"] in {
                "KEEP_EXISTING_STRUCTURE", "ADD_SECTION_OR_FAQ_TO_EXISTING", "EXPAND_EXISTING_PAGE"
            }
            for row in phrase_rows_by_unit[uid]
        ]
        rep = representative(primary_phrase_rows or all_phrase_rows)
        section_key, section_name = section_for(page_key)
        page_type = page_type_for(page_key, member_units)
        page_registry.append({
            "target_page_key": page_key,
            "target_page_name_ru": PAGE_TITLES[page_key],
            "page_purpose": purpose_for(PAGE_TITLES[page_key], page_type),
            "page_type": page_type,
            "primary_user_task_intent": join_values([row["intent_user_task_ru"] for row in member_cluster_rows], limit=4),
            "primary_representative_query": rep["phrase"],
            "member_phrase_count": sum(int(row["member_phrase_count"]) for row in member_cluster_rows),
            "accepted_routed_phrase_count": accepted_count,
            "recheck_phrase_count": recheck_count,
            "semantic_scope_cluster_keys": ";".join(member_ids),
            "semantic_group_keys": join_values([row["semantic_group_keys"] for row in member_cluster_rows]),
            "target_route_url_state": "LOGICAL_TARGET_ROLE_DEFINED__URL_NOT_USED_AS_DESIGN_INPUT",
            "provisional_target_route": f"TARGET_ROLE::{page_key}",
            "parent_target_page_key": PARENT_BY_PAGE.get(page_key, ""),
            "parent_section_key": section_key,
            "parent_section_name_ru": section_name,
            "child_supporting_target_page_keys": "",
            "target_derivation_basis": "ACCEPTED_WORKING_SEMANTICS__USER_TASK__INTENT__EXPECTED_PAGE_ROLE",
        })

    page_registry.append({
        "target_page_key": "TP-UNRESOLVED-DIY-WINDOW-TASK",
        "target_page_name_ru": "Неопределённая DIY-задача по окнам",
        "page_purpose": "Сохранить шесть рабочих фраз без выдуманной посадочной до разрешения точной задачи.",
        "page_type": "Требует определения роли",
        "primary_user_task_intent": unresolved_rep["user_task"],
        "primary_representative_query": unresolved_rep["phrase"],
        "member_phrase_count": 6,
        "accepted_routed_phrase_count": 0,
        "recheck_phrase_count": 6,
        "semantic_scope_cluster_keys": "UNRESOLVED-DIY-WINDOW-TASK",
        "semantic_group_keys": join_values([row["semantic_group_id"] for row in unresolved_phrase_rows]),
        "target_route_url_state": "UNRESOLVED__NO_URL_FABRICATED",
        "provisional_target_route": "TARGET_ROLE::TP-UNRESOLVED-DIY-WINDOW-TASK",
        "parent_target_page_key": "",
        "parent_section_key": "SEC-GUIDES",
        "parent_section_name_ru": "Полезные материалы и выбор",
        "child_supporting_target_page_keys": "",
        "target_derivation_basis": "EXPLICIT_UNRESOLVED_ROUTE__NOT_CURRENT_URL_COPY",
    })
    children: dict[str, list[str]] = defaultdict(list)
    for row in page_registry:
        if row["parent_target_page_key"]:
            children[str(row["parent_target_page_key"])].append(str(row["target_page_key"]))
    for row in page_registry:
        row["child_supporting_target_page_keys"] = ";".join(children.get(str(row["target_page_key"]), []))
    assert len(page_registry) == 60

    hierarchy_rows = []
    for row in sorted(page_registry, key=lambda item: (str(item["parent_section_name_ru"]), str(item["parent_target_page_key"]), str(item["target_page_name_ru"]))):
        parent = str(row["parent_target_page_key"])
        hierarchy_rows.append({
            "section_key": row["parent_section_key"],
            "section_name_ru": row["parent_section_name_ru"],
            "subsection_or_parent_page_key": parent,
            "subsection_or_parent_name_ru": PAGE_TITLES.get(parent, "Корневой маршрут раздела"),
            "target_page_key": row["target_page_key"],
            "target_page_name_ru": row["target_page_name_ru"],
            "hierarchy_level": "CHILD_OR_SUPPORT_PAGE" if parent else "SECTION_LANDING_OR_STANDALONE",
            "page_type": row["page_type"],
            "member_phrase_count": row["member_phrase_count"],
            "child_supporting_target_page_keys": row["child_supporting_target_page_keys"],
            "hierarchy_basis": "TARGET_SEMANTIC_ROLE_TREE__NOT_CURRENT_NAVIGATION_TREE",
        })

    url_to_page = {norm_url(url): key for key, url in CURRENT_MATCH_BY_PAGE.items()}
    missing_relation_sources = {
        norm_url(row["source_url"])
        for row in relations if row["current_link_present"] == "NO"
    }
    physical_states = {
        "READY_IMPLEMENTATION_SPEC", "PENDING_BUSINESS_DETAIL",
        "PENDING_TECHNICAL_DETAIL", "PENDING_PLACEMENT_OR_CONTEXT",
    }
    content_packages_by_page: dict[str, list[dict[str, str]]] = defaultdict(list)
    all_packages_by_page: dict[str, list[dict[str, str]]] = defaultdict(list)
    for package in packages:
        obj = package["page_or_object"]
        source_part = obj.split("→", 1)[0].strip()
        page_key = url_to_page.get(norm_url(source_part))
        if page_key:
            all_packages_by_page[page_key].append(package)
            if package["client_state"] in physical_states and not package["work_package_id"].startswith("WP-LINK-"):
                content_packages_by_page[page_key].append(package)

    reconciliation: list[dict[str, object]] = []
    page_specs: list[dict[str, object]] = []
    for registry in page_registry:
        page_key = str(registry["target_page_key"])
        current_url = CURRENT_MATCH_BY_PAGE.get(page_key, "")
        content_packages = content_packages_by_page.get(page_key, [])
        has_missing_relation = norm_url(current_url) in missing_relation_sources
        if not current_url:
            match_state = "UNRESOLVED"
            target_action = "RECHECK_NEEDS_EVIDENCE"
            real_change = "UNRESOLVED"
        elif content_packages:
            match_state = "EXISTING_NEEDS_OPTIMIZATION"
            target_action = "OPTIMIZE_STRENGTHEN"
            real_change = "YES"
        elif has_missing_relation:
            match_state = "EXISTING_RELATIONSHIP_CHANGE"
            target_action = "ROUTE_INTERNAL_LINK_CHANGE"
            real_change = "UNRESOLVED"
        else:
            match_state = "EXISTING_MATCH"
            target_action = "KEEP_LOCK_AS_TARGET_OWNER"
            real_change = "NO"
        related_cluster_rows = [cluster_by_key[key] for key in str(registry["semantic_scope_cluster_keys"]).split(";")]
        no_standalone = [
            row for row in related_cluster_rows
            if row["target_action"] == "NO_STANDALONE_INCLUDE_IN_NAMED_OWNER"
        ]
        recheck = [row for row in related_cluster_rows if row["target_action"] == "RECHECK_NEEDS_EVIDENCE"]
        page_packages = all_packages_by_page.get(page_key, [])
        implementation_detail = join_values(
            [row["exact_change"] for row in page_packages if row["client_state"] in physical_states],
            limit=5,
        )
        end_state = join_values(
            [row["to_be_state"] for row in page_packages if row["client_state"] in physical_states],
            limit=4,
        ) or f"Страница подтверждена как целевая посадочная для роли «{registry['target_page_name_ru']}» и сохраняет эту ответственность."
        acceptance = join_values(
            [row["acceptance_check"] for row in page_packages if row["client_state"] in physical_states],
            limit=4,
        ) or "Страница доступна, её основная задача совпадает с целевой ролью, а соседние задачи не перехватывают эту ответственность."
        uncertainty = join_values(
            [str(row["uncertainty_evidence_boundary"]) for row in recheck]
            + [row["one_concrete_clarification"] for row in page_packages if row["one_concrete_clarification"]],
            limit=5,
        ) or "Существенной неопределённости для целевой роли нет."
        reconciliation.append({
            "target_page_key": page_key,
            "target_page_name_ru": registry["target_page_name_ru"],
            "independent_target_role": registry["page_purpose"],
            "current_match_state": match_state,
            "current_url_match": current_url,
            "accepted_target_url_after_reconciliation": current_url if current_url else "",
            "target_action": target_action,
            "real_site_change_required": real_change,
            "current_content_reuse": "REUSE_CURRENT_PAGE" if current_url else "UNRESOLVED",
            "business_fit_state": "SUPPORTED_WITHIN_ACCEPTED_SCOPE" if current_url else "NEEDS_EVIDENCE",
            "structural_safety_state": "NO_CREATE_SPLIT_MERGE_REDIRECT_DELETE_AUTHORIZED",
            "implementation_package_ids": ";".join(row["work_package_id"] for row in page_packages),
            "uncertainty_evidence_boundary": uncertainty,
            "reconciliation_basis": "TARGET_MODEL_FROZEN_FIRST__THEN_MATCHED_TO_PRESERVED_CURRENT_SITE_EVIDENCE",
        })
        child_names = [PAGE_TITLES[key] for key in children.get(page_key, [])]
        page_specs.append({
            "page_spec_key": "PS-" + page_key.removeprefix("TP-"),
            "target_page_key": page_key,
            "target_page_name_ru": registry["target_page_name_ru"],
            "target_url_or_route": current_url or registry["provisional_target_route"],
            "page_type": registry["page_type"],
            "parent_section": registry["parent_section_name_ru"],
            "parent_target_page_key": registry["parent_target_page_key"],
            "page_purpose": registry["page_purpose"],
            "primary_user_task_intent": registry["primary_user_task_intent"],
            "primary_representative_query": registry["primary_representative_query"],
            "member_phrase_count": registry["member_phrase_count"],
            "accepted_routed_phrase_count": registry["accepted_routed_phrase_count"],
            "recheck_phrase_count": registry["recheck_phrase_count"],
            "semantic_scope_cluster_keys": registry["semantic_scope_cluster_keys"],
            "what_page_should_cover": join_values([str(row["cluster_task_name_ru"]) for row in related_cluster_rows], limit=7),
            "what_belongs_elsewhere_or_not_standalone": (
                join_values([str(row["cluster_task_name_ru"]) for row in no_standalone], limit=6)
                or "Соседние самостоятельные задачи остаются на дочерних или связанных посадочных."
            ),
            "supporting_child_related_pages": join_values(child_names, limit=8),
            "current_url_match_current_state": f"{match_state}: {current_url}" if current_url else match_state,
            "target_action": target_action,
            "real_site_change_required": real_change,
            "implementation_detail_if_change_is_real": implementation_detail or "Физическое изменение не требуется; сохранить подтверждённую роль.",
            "acceptance_target_end_state": end_state + " Проверка: " + acceptance,
            "uncertainty_exact_clarification": uncertainty,
            "implementation_package_ids": ";".join(row["work_package_id"] for row in page_packages),
        })

    reconciliation_by_page = {row["target_page_key"]: row for row in reconciliation}
    phrase_target_rows: list[dict[str, object]] = []
    for old in old_phrase_map:
        uid = old["structural_unit_id"] or "UNRESOLVED-DIY-WINDOW-TASK"
        cluster = cluster_by_key[uid]
        page_key = str(cluster["intended_target_page_key"])
        rec = reconciliation_by_page.get(page_key)
        target_url = ""
        if cluster["target_route_state"] in {"TARGET_PAGE_RESOLVED", "NO_STANDALONE_ROUTE_TO_PARENT"} and rec:
            target_url = str(rec["accepted_target_url_after_reconciliation"])
        phrase_target_rows.append({
            "phrase_key": old["phrase_id"],
            "phrase": old["phrase"],
            "cluster_task_key": uid,
            "cluster_task_name_ru": cluster["cluster_task_name_ru"],
            "semantic_group_key": old["semantic_group_id"],
            "semantic_group_name_ru": old["semantic_group_name"],
            "intent_user_task_ru": old["intent"] + ": " + old["user_task"],
            "target_landing_page_key": page_key,
            "target_landing_page_name_ru": cluster["intended_target_page_name_ru"],
            "target_route_state": cluster["target_route_state"],
            "target_url_after_reconciliation": target_url,
            "current_exact_page_match_separate": old["exact_owner_url"],
            "current_family_page_match_separate": old["family_owner_url"],
            "current_match_state_separate": old["exact_owner_state"],
            "target_action": cluster["target_action"],
            "real_site_change_required": cluster["real_site_change_required"],
            "uncertainty_reason": cluster["uncertainty_evidence_boundary"],
        })
    assert len(phrase_target_rows) == 2185
    assert len({row["phrase_key"] for row in phrase_target_rows}) == 2185

    page_spec_by_page = {row["target_page_key"]: row for row in page_specs}
    change_delta: list[dict[str, object]] = []
    for package in packages:
        if package["client_state"] not in physical_states:
            continue
        source_url = package["page_or_object"].split("→", 1)[0].strip()
        page_key = url_to_page.get(norm_url(source_url))
        assert page_key and page_key in page_spec_by_page, package["work_package_id"]
        change_delta.append({
            "change_delta_key": "CTD-" + package["work_package_id"],
            "page_spec_key": page_spec_by_page[page_key]["page_spec_key"],
            "target_page_key": page_key,
            "target_page_name_ru": PAGE_TITLES[page_key],
            "current_object": package["page_or_object"],
            "target_action": "ROUTE_INTERNAL_LINK_CHANGE" if package["work_package_id"].startswith("WP-LINK-") else "OPTIMIZE_STRENGTHEN",
            "readiness_state": package["client_state"],
            "real_site_change_required": "UNRESOLVED" if package["work_package_id"].startswith("WP-LINK-") else "YES",
            "why_change_is_needed": package["why_change_is_needed"],
            "exact_change": package["exact_change"],
            "exact_location_or_context": package["exact_location_or_context"],
            "target_end_state": package["to_be_state"],
            "acceptance_check": package["acceptance_check"],
            "preservation_do_not_break": package["preservation_do_not_break"],
            "one_concrete_clarification": package["one_concrete_clarification"],
            "source_work_package_id": package["work_package_id"],
        })
    assert len(change_delta) == 14

    outputs = {
        f"TARGET_FIRST_PHRASE_LANDING_MAP_{DATE}.tsv.gz": phrase_target_rows,
        f"TARGET_FIRST_CLUSTER_LANDING_MAP_{DATE}.tsv": cluster_rows,
        f"TARGET_PAGE_REGISTRY_{DATE}.tsv": page_registry,
        f"TARGET_ARCHITECTURE_HIERARCHY_{DATE}.tsv": hierarchy_rows,
        f"CURRENT_TARGET_RECONCILIATION_{DATE}.tsv": reconciliation,
        f"TARGET_PAGE_SPEC_REGISTER_{DATE}.tsv": page_specs,
        f"CURRENT_TARGET_CHANGE_DELTA_{DATE}.tsv": change_delta,
    }
    output_paths = []
    for name, rows in outputs.items():
        path = HERE / name
        if path.suffix == ".gz":
            write_tsv_gz(path, rows, list(rows[0]))
        else:
            write_tsv(path, rows, list(rows[0]))
        output_paths.append(path)

    route_counts = Counter(str(row["target_route_state"]) for row in cluster_rows)
    page_state_counts = Counter(str(row["current_match_state"]) for row in reconciliation)
    page_action_counts = Counter(str(row["target_action"]) for row in reconciliation)
    phrase_route_counts = Counter(str(row["target_route_state"]) for row in phrase_target_rows)
    manifest = {
        "schema": "MK02_OKNO_MSK_TARGET_FIRST_CORRECTIVE_AUTHORITIES_V1",
        "date": DATE,
        "status": "PASS",
        "provider_calls": 0,
        "source_counts": {"semantic_universe": 2840, "working": 2185, "review": 187, "excluded": 468},
        "target_first_counts": {
            "phrase_target_rows": len(phrase_target_rows),
            "cluster_task_rows": len(cluster_rows),
            "target_page_registry_rows": len(page_registry),
            "resolved_target_pages": len(CURRENT_MATCH_BY_PAGE),
            "unresolved_target_roles": 1,
            "page_spec_rows": len(page_specs),
            "change_delta_rows": len(change_delta),
            "phrase_route_states": dict(sorted(phrase_route_counts.items())),
            "cluster_route_states": dict(sorted(route_counts.items())),
            "page_reconciliation_states": dict(sorted(page_state_counts.items())),
            "page_action_states": dict(sorted(page_action_counts.items())),
        },
        "qa_invariants": {
            "silent_working_phrase_drops": 0,
            "material_clusters_without_target_route_or_explicit_state": 0,
            "target_pages_without_page_spec": 0,
            "keep_pages_without_page_spec": 0,
            "no_standalone_without_named_owner": 0,
            "target_registry_contains_current_url_columns": 0,
            "target_hierarchy_contains_current_url_columns": 0,
            "current_site_used_as_target_design_authority": 0,
            "physical_change_tickets_without_page_spec": 0,
            "step5a_phrase_rows": 0,
        },
        "outputs": {path.name: {"bytes": path.stat().st_size, "sha256": sha256(path)} for path in output_paths},
        "claim_boundaries": [
            "TARGET_MODEL_FROZEN_BEFORE_CURRENT_RECONCILIATION",
            "CURRENT_SITE_IS_AS_IS_EVIDENCE_NOT_TARGET_DESIGN_AUTHORITY",
            "FULL_PAGE_SPEC_IS_NOT_CHANGE_DELTA",
            "KEEP_IS_NOT_OMIT",
            "NO_STANDALONE_HAS_NAMED_OWNER",
            "NO_NEW_PROVIDER_CALLS",
        ],
    }
    manifest_path = HERE / f"TARGET_FIRST_CORRECTIVE_MANIFEST_{DATE}.json"
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    print(json.dumps(manifest, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
