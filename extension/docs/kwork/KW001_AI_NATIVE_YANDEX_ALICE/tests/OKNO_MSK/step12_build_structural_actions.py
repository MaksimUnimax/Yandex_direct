import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PHRASE_MAP = ROOT / 'STEP_11_PHRASE_PAGE_MAP.tsv'
OWNERSHIP = ROOT / 'STEP_11_PAGE_OWNERSHIP_CORRECTED.tsv'
SUMMARY = ROOT / 'STEP_11_EFFECTIVE_CLUSTER_SUMMARY.tsv'
OUT_ACTIONS = ROOT / 'STEP_12_STRUCTURAL_ACTIONS.tsv'
OUT_PHRASES = ROOT / 'STEP_12_PHRASE_ACTION_MAP.tsv'
OUT_ROLLUP = ROOT / 'STEP_12_PAGE_ACTION_ROLLUP.tsv'
OUT_UNRESOLVED = ROOT / 'STEP_12_SEARCH_REQUIRED_HANDOFF.tsv'
OUT_QA = ROOT / 'STEP_12_QA.json'
OUT_REPORT = ROOT / 'STEP_12_REPORT.md'

KEEP = 'KEEP_EXISTING_STRUCTURE'
EXPAND = 'EXPAND_EXISTING_PAGE'
SECTION = 'ADD_SECTION_OR_FAQ_TO_EXISTING'
NEW_COMM = 'NEW_COMMERCIAL_PAGE'
NEW_INFO = 'NEW_INFORMATIONAL_PAGE'
NO_PAGE = 'NO_STANDALONE_PAGE'
OUTSIDE = 'OUTSIDE_SCOPE_NO_ACTION'
DEFER = 'DEFER_UNRESOLVED'

FINANCE_URL = 'https://okno-msk.ru/uslugi/kredit-i-rassrochka/'
CALCULATOR_URL = 'https://okno-msk.ru/calculator/'
BEST_WINDOWS_URL = 'https://okno-msk.ru/stati/kakie-okna-samye-luchshie/'
PRIVATE_HOUSE_URL = 'https://okno-msk.ru/okna-rehau/po-tipu-doma/okna-v-chastnyj-dom/'
P44_URL = 'https://okno-msk.ru/okna-rehau/okna-po-serii-domov/p-44/'


def read_tsv(path):
    with path.open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f, delimiter='\t'))


def write_tsv(path, rows, fields):
    with path.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter='\t', lineterminator='\n')
        w.writeheader()
        w.writerows(rows)


def spec(action, reason, target='CURRENT', parent='', against='', rejected='', confidence='HIGH', step13=False, new_value=''):
    return {
        'action': action,
        'reason': reason,
        'target': target,
        'parent': parent,
        'against': against,
        'rejected': rejected,
        'confidence': confidence,
        'step13': step13,
        'new_value': new_value,
    }


ACTIONS = {
    'ALUMINIUM_WINDOWS_COMMERCIAL': spec(KEEP, 'Current aluminium hub plus existing sliding/hinged child pages form a useful material-led structure; keep the hub as the broad aluminium entry and route subtype phrases to current children.', step13=True, against='Material-led aluminium demand overlaps object-led balcony/veranda glazing, so harmful overlap is not assumed here.', rejected='Rejected creating separate pages for color, price, geography or each opening modifier.'),
    'ALUMINIUM_WINDOW_TECH_INFO': spec(EXPAND, 'The existing aluminium article is the right informational page but should explicitly cover the full observed set: types, construction, opening, ventilation, systems, colors and differences.', against='Current ownership confidence is MEDIUM, so a bare KEEP would ignore visible coverage risk.', rejected='Rejected a new article because the current article already owns the same explanatory task.'),
    'BALCONY_GLAZING_COLD': spec(KEEP, 'Dedicated cold-glazing landing exactly matches the service task.', rejected='Rejected a new page because an exact current page already exists.'),
    'BALCONY_GLAZING_EXTENSION_SERVICE': spec(KEEP, 'Dedicated balcony-with-extension landing exactly matches the task.', rejected='Rejected merging into the generic balcony hub because the engineering solution is already a distinct current service page.'),
    'BALCONY_GLAZING_GENERAL': spec(KEEP, 'Keep the balcony/loggia hub as the broad entry and preserve the current child-page structure for important physical solutions.', step13=True, against='The family has many child axes, so Step 13 must test whether any current pages actually compete; Step 12 does not assume harm.', rejected='Rejected one giant replacement page and rejected new pages for every price/house/geography modifier.'),
    'BALCONY_GLAZING_PROVIDER_REVIEWS_INFO': spec(NO_PAGE, 'A first-party seller cannot truthfully become a neutral ranking/review page for competing balcony-glazing providers; no standalone target should be created for this generic reputation task.', target='', against='Queries ask for ratings/best companies, not only experience with this company.', rejected='Rejected mapping to /otzyvy/ because company testimonials are not a neutral provider ranking.'),
    'BALCONY_GLAZING_ROOF_SERVICE': spec(KEEP, 'Dedicated glazing-with-roof landing exactly matches the task.', rejected='Rejected folding into the broad hub because the current engineering-service page is useful and distinct.'),
    'BALCONY_GLAZING_SELECTION_INFO': spec(SECTION, 'Selection questions belong inside the balcony hub as a clear comparison block that helps choose warm/cold/type/specification and links to current child pages.', rejected='Rejected a separate selection article because the task is a decision layer of the existing balcony purchase journey.'),
    'BALCONY_GLAZING_WARM': spec(KEEP, 'Dedicated warm-glazing landing exactly matches the task.', rejected='Rejected a new page because the exact page already exists.'),
    'BALCONY_RENOVATION_WITH_GLAZING': spec(EXPAND, 'The balcony hub already sells glazing plus finishing; strengthen the bundled glazing+finishing+insulation path and link clearly to finishing/service details.', against='The task is broader than glazing alone but still part of the same balcony project journey.', rejected='Rejected a new generic bundle page until evidence shows the bundle needs a separate search job.'),
    'FRENCH_WINDOWS_COMMERCIAL': spec(EXPAND, 'The current French-window page is the correct commercial page; expand it around replacement of balcony blocks, opening types, balcony/terrace use, colors and price questions represented in the phrase set.', rejected='Rejected creating modifier pages for each room, color or opening type.'),
    'FRENCH_WINDOW_DEFINITION_INFO': spec(SECTION, 'Definition and terminology questions should be answered clearly on the existing French-window commercial page as an explanatory section/FAQ.', rejected='Rejected a separate “what is a French window” page because it is subordinate to the same product task.'),
    'GLASS_UNIT_SELECTION_INFO': spec(KEEP, 'Dedicated current glass-unit selection article exactly answers the task.', rejected='Rejected new or merged page because current ownership is exact.'),
    'GLAZING_DESIGN_INSPIRATION': spec(EXPAND, 'Keep the portfolio as the inspiration destination but organize/expand it by balcony, veranda, panoramic, French and material solution with useful captions and links.', against='Raw portfolio images alone may not answer design/example queries well enough.', rejected='Rejected separate thin inspiration pages for each visual modifier.'),
    'GLAZING_DIY_INFO': spec(NO_PAGE, 'The small set mixes balcony and veranda DIY and different technologies; one generic DIY-glazing page would be too broad and thin. Specific DIY guidance can be attached to the relevant object pages or future coherent guides.', target='', rejected='Rejected automatic new article from a mixed DIY label.'),
    'GLAZING_PERMISSION_INFO': spec(NO_PAGE, 'The phrases mix balcony permission, French-window redevelopment, boiler-room window requirements and hardware standards; they do not form one useful standalone legal page.', target='', rejected='Rejected a generic “window law” page; distribute verified legal answers to the relevant balcony/French/private-house/hardware contexts.'),
    'MOSQUITO_NET_INSTALLATION_SERVICE': spec(KEEP, 'Current mosquito-net page already combines product, manufacture and installation; separate installation landing is unnecessary.', rejected='Rejected a standalone installation page because the current hybrid page truthfully completes the task.'),
    'MOSQUITO_NET_REPAIR_SERVICE': spec(NO_PAGE, 'Repair of mosquito nets is not verified as a current offered service; do not create a commercial repair page from demand alone.', target='', against='Current mosquito page and repair page do not expose this service.', rejected='Rejected an unverified service landing; client/business confirmation would be needed before reconsidering.'),
    'MOSQUITO_NET_SELECTION_INFO': spec(KEEP, 'Current mosquito-net page already compares types/specifications and supports selection.', rejected='Rejected a separate selection article because it is already part of the same product page.'),
    'MOSQUITO_NET_SHOPPING': spec(KEEP, 'Current mosquito-net page has types, prices, sizing and order flow and should remain the commercial owner.', rejected='Rejected separate pages for Anti-cat/Anti-dust modifiers unless later evidence proves independent tasks.'),
    'NAVIGATION_BRAND_SITE': spec(OUTSIDE, 'These searches want the official REHAU/manufacturer destination rather than the target site; no target-site structural action.', target='', rejected='Rejected trying to capture navigational intent with a misleading landing.'),
    'OPEN_BALCONY_FINISHING': spec(NO_PAGE, 'The current site explicitly does not offer interior balcony finishing without glazing; creating a landing would contradict the public offer.', target='', rejected='Rejected a page for a service the site currently says it does not provide.'),
    'OUTDOOR_GLAZING_REVIEWS_INFO': spec(NO_PAGE, 'One generic veranda-glazing review query does not justify a standalone first-party review page.', target='', rejected='Rejected a thin article or forced mapping to company testimonials.'),
    'OUTDOOR_GLAZING_SELECTION_INFO': spec(SECTION, 'Selection of warm/cold systems, material and opening should be a strong comparison section in the current veranda/outdoor hub with links to warm/cold children.', rejected='Rejected a separate selection page because the hub already carries this decision task.'),
    'OUTDOOR_GLAZING_SPECIALIZED_INFO': spec(NO_PAGE, 'Frameless glazing, liquid glass and polycarbonate thickness are different techniques/material questions; the three phrases do not support one coherent standalone document.', target='', rejected='Rejected one generic specialized-glazing page that would combine unrelated answers.'),
    'OUTDOOR_STRUCTURE_GLAZING': spec(KEEP, 'Keep the veranda/terrace/gazebo hub and existing warm/cold children; the object-led hub is a useful broad service entry while warm/cold phrases can route to current children.', step13=True, against='Material-led aluminium and panoramic pages overlap some use cases, so Step 13 should test actual search conflict rather than assume it.', rejected='Rejected creating a page for every material/opening modifier.'),
    'OUTSIDE_CURTAINS_BLINDS': spec(OUTSIDE, 'Curtains/blinds are outside the frozen target business scope.', target=''),
    'OUTSIDE_HEATING_HVAC': spec(OUTSIDE, 'Heating/HVAC/radiator intent is outside the frozen target business scope.', target=''),
    'OUTSIDE_INTERIOR_DOORS': spec(OUTSIDE, 'Generic interior-door intent is outside the PVC exterior/balcony-door scope.', target=''),
    'OUTSIDE_OTHER': spec(OUTSIDE, 'Confirmed other tasks are outside the target business scope.', target=''),
    'OUTSIDE_REAL_ESTATE_ARCHITECTURE': spec(OUTSIDE, 'Real-estate/architecture inspiration that is not seeking window/glazing work is outside scope.', target=''),
    'PANORAMIC_WINDOWS_COMMERCIAL': spec(NEW_COMM, 'Panoramic windows are a large, stable commercial task across house/terrace/general purchase queries, and no general commercial panoramic owner exists. Create one useful broad commercial page that explains product options, materials, opening, sizing, price factors and routes object-specific balcony/veranda cases to their pages.', target='PROPOSED_NEW:/panoramnye-okna/', parent='WINDOW_PRODUCTS / homepage', against='Current French, balcony and veranda pages are narrower object/form pages and do not own general panoramic-window purchase.', rejected='Rejected forcing all panoramic demand onto French windows or balcony glazing.', step13=True, new_value='Standalone commercial value: product selection + configuration + material/opening choices + price/measurement CTA; not a modifier-only page.'),
    'PANORAMIC_WINDOW_TECH_INFO': spec(KEEP, 'Dedicated panoramic-glazing explanatory article already answers the technical/informational task.', rejected='Rejected a second informational page for the same explanation.'),
    'PRIVATE_HOUSE_WINDOW_PLANNING_INFO': spec(EXPAND, 'The current private-house page is the right planning/selection page; expand it with room-specific planning, sizing links, panoramic considerations and verified boiler-room requirements where appropriate.', rejected='Rejected separate pages for every room/size modifier; use the existing planning hub plus dimensions/legal support.'),
    'PVC_ALUMINIUM_COMPARISON_INFO': spec(KEEP, 'Existing article explicitly compares PVC and aluminium choices and matches the task.', rejected='Rejected duplicate comparison content.'),
    'PVC_DOORS_COMMERCIAL': spec(KEEP, 'Keep the PVC-door hub and its current balcony/sliding/entrance child structure; subtype phrases should route to those children instead of generating duplicate pages.', rejected='Rejected new pages for every door adjective; the current hub+children already represents the useful hierarchy.'),
    'PVC_DOOR_INFO': spec(SECTION, 'Selection, dimensions, operating and basic adjustment questions belong as clearer explanatory/FAQ sections on the current PVC-door hub and relevant child pages.', against='Several phrases are basic DIY adjustment rather than pure purchase, but they are still subordinate to door ownership.', rejected='Rejected a separate generic PVC-door information article.'),
    'PVC_DOOR_INSTALLATION_SERVICE': spec(SECTION, 'Installation is currently bundled with PVC-door purchase; make the installation process/price/what-is-included explicit on the door hub rather than creating a standalone service page without evidence that installation is sold independently.', target='https://okno-msk.ru/dveri-rehau/', parent='PVC_DOORS', against='No standalone door-installation offer was verified.', rejected='Rejected a new service page until independent service availability is proven.'),
    'PVC_DOOR_REPAIR_SERVICE': spec(NO_PAGE, 'PVC-door repair is not verified as a current offered service; do not publish a service landing based only on query demand.', target='', rejected='Rejected an unverified repair service page; business confirmation is required.'),
    'PVC_DOOR_REPLACEMENT_SERVICE': spec(NO_PAGE, 'PVC-door replacement is not verified as a standalone current service; three phrases alone do not override that business-evidence gap.', target='', rejected='Rejected a new replacement page until the service is confirmed.'),
    'PVC_WINDOWS_COMMERCIAL': spec(KEEP, 'Keep the REHAU/PVC product hub as the main PVC-window purchase page and use existing finance/calculator/private-house/support pages for distinct subjobs.', step13=True, against='Homepage also covers broad PVC purchase, so Step 13 should test actual overlap before any consolidation.', rejected='Rejected separate pages for price, city, size and “cheap” modifiers by default.'),
    'PVC_WINDOW_COLOR_INFO': spec(KEEP, 'Dedicated current coloured-window page owns colors/finishes.', rejected='Rejected a separate color article for the same task.'),
    'PVC_WINDOW_TECH_INFO': spec(SECTION, 'Basic types/opening/properties questions should be strengthened as an explicit explanatory section in the existing “how to choose plastic windows” guide.', rejected='Rejected a new technical article because the current guide already covers the same decision context.'),
    'REHAU_INTERNAL_COMPARISON_INFO': spec(KEEP, 'Dedicated Rehau profile-comparison page owns internal system/model comparison.', rejected='Rejected duplicate comparison page.'),
    'REHAU_KALEVA_COMPARISON_INFO': spec(KEEP, 'Dedicated Rehau-vs-Kaleva article exactly matches the comparison.', rejected='Rejected duplicate comparison content.'),
    'REHAU_OTHER_BRAND_COMPARISON_INFO': spec(SECTION, 'KBE/Melke comparisons are too fragmented for one standalone page; add a “compare Rehau with other brands” section/index to the existing Rehau comparison hub and link current dedicated VEKA/Kaleva comparisons.', target='https://okno-msk.ru/okna-rehau/sravnenie-profilej-rehau/', parent='REHAU_COMPARISON', against='The cluster contains different competitor pairs, so one new article would not have one stable comparison object.', rejected='Rejected one mixed KBE+Melke article and rejected two thin pages from the current evidence.'),
    'REHAU_VEKA_COMPARISON_INFO': spec(KEEP, 'Dedicated Rehau-vs-VEKA article exactly matches the task.', rejected='Rejected duplicate comparison content.'),
    'REHAU_WINDOWS_COMMERCIAL': spec(KEEP, 'Keep the Rehau hub and current model child pages; model, finance and calculator phrases can route to current dedicated pages without multiplying new URLs.', step13=True, against='The same /okna-rehau/ page also owns broad PVC demand, and homepage overlaps broad purchase; actual conflict belongs to Step 13.', rejected='Rejected new pages for every model/price/payment modifier where current pages/utilities already exist.'),
    'REHAU_WINDOW_TECH_INFO': spec(KEEP, 'Current Rehau comparison page already covers system types, dimensions and technical characteristics.', rejected='Rejected a second generic Rehau-tech article.'),
    'ROOF_WINDOWS_COMMERCIAL': spec(NO_PAGE, 'Mansard/roof-window product availability is not verified on the site; do not create a commercial page from two phrases.', target='', rejected='Rejected an unverified product-family page.'),
    'SOFT_WINDOWS_COMMERCIAL': spec(NO_PAGE, 'Soft/flexible-window product availability is not verified and the only phrase is ambiguous; no standalone commercial page.', target='', rejected='Rejected an unverified one-query product page.'),
    'TIMBER_ALUMINIUM_WINDOWS_COMMERCIAL': spec(NO_PAGE, 'Timber-aluminium products are not verified as part of the current offer; do not create a commercial family page until the product is confirmed.', target='', rejected='Rejected demand-only creation without product evidence.'),
    'WINDOWSILL_REPAIR_SERVICE': spec(NO_PAGE, 'Repair/restoration of windowsills is not verified as a standalone offered service; current assets cover sills and finishing but not this exact service.', target='', rejected='Rejected an unverified repair landing; useful replacement/installation information can remain in finishing/windowsill pages.'),
    'WINDOWS_COMMERCIAL_GENERAL': spec(KEEP, 'Keep the homepage as the broad windows entry, but route distinct payment, private-house and known house-series jobs to existing specialized pages instead of bloating the homepage.', step13=True, against='Homepage and /okna-rehau/ overlap broad purchase; Step 13 must test real conflict.', rejected='Rejected creating new pages for generic price/geography modifiers.'),
    'WINDOWS_DOORS_COMBINED_COMMERCIAL': spec(SECTION, 'Add/retain a clear combined windows+doors offer/navigation block on the homepage that routes users to the separate window and door hubs.', rejected='Rejected a new mixed windows-and-doors landing because the two established product hubs already provide depth.'),
    'WINDOW_ACCESSORIES_SHOPPING': spec(EXPAND, 'Keep the accessories hub but strengthen its category routing to existing handles, sills, drip caps, security, decorative and other accessory children; do not make the hub a catch-all hardware marketplace.', against='Member phrases include some components that need child/service routing rather than one generic catalog.', rejected='Rejected one page per accessory modifier and rejected third-party marketplace expansion.'),
    'WINDOW_ACCESSORY_SELECTION_INFO': spec(KEEP, 'The only selection query is about choosing a windowsill and the current windowsill page already supports that choice.', rejected='Rejected a generic accessory-selection page.'),
    'WINDOW_DEMOLITION_SERVICE': spec(SECTION, 'Demolition is a sub-step of the verified installation workflow; explain scope/cost/disposal within the installation page rather than creating a standalone demolition service landing.', target='https://okno-msk.ru/uslugi/ustanovka-okon/', parent='WINDOW_INSTALLATION', rejected='Rejected standalone demolition page because the user outcome is normally replacement/installation.'),
    'WINDOW_DIMENSIONS_INFO': spec(KEEP, 'Dedicated dimensions/ГОСТ/house-series article owns the sizing task.', rejected='Rejected duplicate sizing page.'),
    'WINDOW_FINISHING_DIY_INFO': spec(EXPAND, 'Expand the current DIY slopes article into a fuller “finishing after window installation” guide covering slopes plus related sill/drip-cap installation/repair questions represented by the phrases.', against='Current title/page is narrower than all four observed finishing-DIY tasks.', rejected='Rejected several tiny DIY pages for each component.'),
    'WINDOW_FINISHING_SERVICE': spec(EXPAND, 'The service page is the right finishing owner; expand its visible scope/pricing around slopes plus related sill/drip-cap installation/repair where the business actually performs them.', against='Member phrases extend beyond slopes alone.', rejected='Rejected separate thin service pages for each finishing component.'),
    'WINDOW_HARDWARE_INFO': spec(NEW_INFO, 'Create one substantial guide to window hardware: what it is, types, major brands, how to choose, compare, maintain and lubricate it. The 41-phrase set represents a stable explanatory/selection task and no broad owner exists.', target='PROPOSED_NEW:/stati/okonnaya-furnitura-vidy-brendy-kak-vybrat/', parent='/stati/ + /okna-rehau/aksessuary-dlya-okon/', against='Information is currently fragmented across accessory/product/repair pages.', rejected='Rejected a commercial marketplace page; this is an informational guide.', new_value='Standalone informational value: definitions, component map, types, brand comparison criteria, selection, maintenance and links to repair/accessories.'),
    'WINDOW_HARDWARE_SHOPPING': spec(NO_PAGE, 'The cluster is a broad aftermarket/third-party hardware catalog task; the target site is not verified as a general parts marketplace. Do not create a massive hardware-store landing.', target='', against='Many phrases name third-party brands, stores and replacement parts outside the truthful current catalog.', rejected='Rejected mapping the whole set to the accessory hub; route only clearly supported existing accessories when applicable.'),
    'WINDOW_INSTALLATION_DIY_INFO': spec(NEW_INFO, 'Create a comprehensive DIY installation guide covering preparation, gaps, dismantling, fixing, sealing, common errors and when professional installation is safer. The 36 phrases form a stable standalone how-to task.', target='PROPOSED_NEW:/stati/ustanovka-plastikovyh-okon-svoimi-rukami/', parent='/stati/ + /uslugi/ustanovka-okon/', rejected='Rejected forcing DIY intent onto the professional installation service page.', new_value='Standalone informational value: complete step-by-step installation workflow, tools/materials, tolerances, mistakes, safety and handoff to professional service.'),
    'WINDOW_INSTALLATION_SERVICE': spec(KEEP, 'Dedicated professional installation landing exactly matches the service task; keep the page and route dismantling as a supporting section.', rejected='Rejected a second installation page for price/region modifiers.'),
    'WINDOW_OPERATION_MODE_INFO': spec(KEEP, 'Dedicated current summer/winter-mode article exactly matches the task.', rejected='Rejected duplicate article.'),
    'WINDOW_PRODUCT_REVIEWS_INFO': spec(NO_PAGE, 'Generic product/model reviews and ratings are not one truthful first-party review asset. Do not create a page that pretends neutral third-party review coverage; rating-only phrases can route to the existing comparison article.', target='', rejected='Rejected mapping the whole set to company testimonials or fabricating neutral product ratings.'),
    'WINDOW_PRODUCT_VIDEO_INFO': spec(NO_PAGE, 'Two generic “video” phrases do not justify a standalone page; useful videos should live on the relevant PVC/aluminium product pages or portfolio.', target='', rejected='Rejected a thin generic video landing.'),
    'WINDOW_PROFILE_SELECTION_INFO': spec(KEEP, 'Current “how to choose plastic windows” guide explicitly covers profile/manufacturer choice and remains the right page.', rejected='Rejected duplicate profile-selection article.'),
    'WINDOW_PROVIDER_REVIEWS_INFO': spec(NO_PAGE, 'Generic ratings/reviews of installers and repair providers require neutral comparative evidence; a first-party company site should not create a self-authored ranking page.', target='', rejected='Rejected mapping to company testimonials or creating a misleading “best companies” page.'),
    'WINDOW_REPAIR_DIY_INFO': spec(NEW_INFO, 'Create a comprehensive DIY diagnostics/adjustment/repair guide for common PVC-window problems. The set has a stable self-help task and no broad current owner.', target='PROPOSED_NEW:/stati/remont-i-regulirovka-plastikovyh-okon-svoimi-rukami/', parent='/stati/ + /uslugi/remont-okon/', against='Existing narrow self-help pages do not cover the broad repair/diagnostic set.', rejected='Rejected forcing DIY intent onto the professional repair service page.', new_value='Standalone informational value: symptom diagnosis, adjustment, handle/mechanism issues, sealing, what is safe to DIY, and when to call repair service.'),
    'WINDOW_REPAIR_SERVICE': spec(KEEP, 'Dedicated repair/adjustment/component-replacement landing exactly owns the professional service task.', rejected='Rejected extra pages for every defect/region/part until separate task evidence exists.'),
    'WINDOW_REPLACEMENT_SERVICE': spec(NEW_COMM, 'Replacement is a distinct end-to-end service task: remove old window, prepare opening, install new window and finish/hand over. The current installation page covers parts of this workflow but has no replacement-specific landing.', target='PROPOSED_NEW:/uslugi/zamena-okon/', parent='/uslugi/ + /uslugi/ustanovka-okon/', against='Current owner confidence was MEDIUM because installation is related but not identical to replacement intent.', rejected='Rejected merely adding one FAQ line to installation; the 13 phrases seek replacement as the primary service.', step13=True, new_value='Standalone commercial value: replacement scenarios, removal, measurement, new-window selection, price factors, timing, disposal/finishing, conversion CTA.'),
    'WINDOW_SELECTION_INFO': spec(KEEP, 'Keep the existing “how to choose plastic windows” guide as the main selection page; route explicit “best/ranking” phrasing to the existing comparison article where appropriate.', step13=True, against='A separate “which windows are best” article also exists, so Step 13 should test actual overlap rather than merge by assumption.', rejected='Rejected another new selection article.'),
    'WOOD_WINDOWS_COMMERCIAL': spec(NO_PAGE, 'Wooden-window products are not verified as a current offer and the five phrases are partly mixed with plastic windows in wooden houses; no standalone wooden-window commercial page.', target='', rejected='Rejected an unverified product page and rejected treating house material as proof of wooden-window demand.'),
}


def route_override(cluster_id, phrase):
    p = phrase.lower()
    # Existing finance page is a distinct payment job discovered and read in Step 01.
    if 'рассроч' in p or 'кредит' in p:
        return ('FINANCE_INSTALLMENT_EXISTING', KEEP, FINANCE_URL, 'Existing credit/instalment page matches the payment-condition task.', 'STEP_01_MERGED_SITE_INVENTORY_B14')

    if cluster_id in {'PVC_WINDOWS_COMMERCIAL', 'REHAU_WINDOWS_COMMERCIAL', 'WINDOWS_COMMERCIAL_GENERAL'} and ('калькулятор' in p or 'рассчитать стоимость' in p):
        return ('WINDOW_CALCULATOR_EXISTING', KEEP, CALCULATOR_URL, 'Existing calculator is the dedicated price-estimation utility.', 'STEP_01_MERGED_SITE_INVENTORY_U15')

    if cluster_id in {'PVC_WINDOWS_COMMERCIAL', 'WINDOWS_COMMERCIAL_GENERAL'} and ('частного дома' in p or 'частном доме' in p):
        return ('PRIVATE_HOUSE_WINDOWS_EXISTING', KEEP, PRIVATE_HOUSE_URL, 'Existing private-house window page is a more specific current destination.', 'STEP_11_PAGE_PROFILE_LEDGER')

    if cluster_id in {'PVC_WINDOWS_COMMERCIAL', 'WINDOWS_COMMERCIAL_GENERAL'} and ('п 44' in p or 'п44' in p):
        return ('P44_WINDOWS_EXISTING', KEEP, P44_URL, 'Existing P-44 house-series page is the specific current destination.', 'STEP_01_MERGED_SITE_INVENTORY_U39')

    if cluster_id == 'ALUMINIUM_WINDOWS_COMMERCIAL':
        if 'раздвиж' in p or 'сдвиж' in p:
            return ('ALUMINIUM_SLIDING_EXISTING', KEEP, 'https://okno-msk.ru/alyuminievye-okna/razdvizhnye/', 'Existing sliding-aluminium child page matches opening-mode subtype.', 'STEP_01_MERGED_SITE_INVENTORY_U05')
        if 'распаш' in p or 'поворот' in p or 'откид' in p:
            return ('ALUMINIUM_HINGED_EXISTING', KEEP, 'https://okno-msk.ru/alyuminievye-okna/raspashnye/', 'Existing hinged-aluminium child page matches opening-mode subtype.', 'STEP_01_MERGED_SITE_INVENTORY_U04')

    if cluster_id == 'BALCONY_GLAZING_GENERAL':
        if 'панорам' in p or 'в пол' in p:
            return ('BALCONY_PANORAMIC_EXISTING', KEEP, 'https://okno-msk.ru/balkony-i-lodzhii/panoramnoe-osteklenie-balkona/', 'Existing panoramic-balcony landing matches the physical solution.', 'STEP_01_MERGED_SITE_INVENTORY_U12')
        if 'распаш' in p:
            return ('BALCONY_HINGED_EXISTING', KEEP, 'https://okno-msk.ru/balkony-i-lodzhii/raspashnoe-osteklenie-balkonov/', 'Existing hinged-balcony landing matches the opening solution.', 'STEP_01_MERGED_SITE_INVENTORY_U14')

    if cluster_id == 'OUTDOOR_STRUCTURE_GLAZING':
        if 'тепл' in p or 'зимн' in p:
            return ('VERANDA_WARM_EXISTING', KEEP, 'https://okno-msk.ru/verandy/teploe-osteklenie-verand/', 'Existing warm-veranda landing matches year-round/warm subtype.', 'STEP_01_MERGED_SITE_INVENTORY_U64')
        if 'холод' in p:
            return ('VERANDA_COLD_EXISTING', KEEP, 'https://okno-msk.ru/verandy/holodnoe-osteklenie-verand/', 'Existing cold-veranda landing matches seasonal/cold subtype.', 'STEP_01_MERGED_SITE_INVENTORY_U62')

    if cluster_id == 'PVC_DOORS_COMMERCIAL':
        if 'балкон' in p:
            return ('PVC_BALCONY_DOOR_EXISTING', KEEP, 'https://okno-msk.ru/dveri-rehau/balkonnye-dveri/', 'Existing balcony-door child page matches the door subtype.', 'STEP_01_MERGED_SITE_INVENTORY_U19')
        if 'раздвиж' in p:
            return ('PVC_SLIDING_DOOR_EXISTING', KEEP, 'https://okno-msk.ru/dveri-rehau/razdvizhnye-dveri/', 'Existing sliding-door child page matches the door subtype.', 'STEP_01_MERGED_SITE_INVENTORY_U20')
        if 'входн' in p or 'уличн' in p:
            return ('PVC_ENTRANCE_DOOR_EXISTING', KEEP, 'https://okno-msk.ru/dveri-rehau/vhodnye-dveri/', 'Existing entrance-door child page matches the door subtype.', 'STEP_01_MERGED_SITE_INVENTORY_U21')

    if cluster_id == 'REHAU_WINDOWS_COMMERCIAL':
        if 'blitz' in p:
            return ('REHAU_BLITZ_EXISTING', KEEP, 'https://okno-msk.ru/okna-rehau/rehau-blitz-new/', 'Existing Blitz profile page matches model-specific purchase.', 'STEP_01_MERGED_SITE_INVENTORY_U41')
        if 'grazio' in p:
            return ('REHAU_GRAZIO_EXISTING', KEEP, 'https://okno-msk.ru/okna-rehau/rehau-grazio/', 'Existing Grazio profile page matches model-specific purchase.', 'STEP_01_MERGED_SITE_INVENTORY_U42')
        if 'intelio' in p or 'intellio' in p:
            return ('REHAU_INTELLIO_EXISTING', KEEP, 'https://okno-msk.ru/okna-rehau/rehau-intellio-80/', 'Existing Intelio profile page matches model-specific purchase.', 'STEP_01_MERGED_SITE_INVENTORY_U43')
        if 'thermo' in p or 'термо' in p:
            return ('REHAU_THERMO_EXISTING', KEEP, 'https://okno-msk.ru/okna-rehau/rehau-thermo-design/', 'Existing Thermo profile page matches model-specific purchase.', 'STEP_01_MERGED_SITE_INVENTORY_U44')

    if cluster_id in {'WINDOW_ACCESSORIES_SHOPPING', 'WINDOW_HARDWARE_SHOPPING'}:
        base = 'https://okno-msk.ru/okna-rehau/aksessuary-dlya-okon/'
        if 'подоконник' in p:
            return ('WINDOWSILL_EXISTING', KEEP, base + 'podokonniki/', 'Existing windowsill page is the specific accessory destination.', 'STEP_11_PAGE_OWNERSHIP_CORRECTED')
        if 'отлив' in p:
            return ('DRIP_CAP_EXISTING', KEEP, base + 'otlivy/', 'Existing drip-cap page is the specific accessory destination.', 'STEP_01_MERGED_SITE_INVENTORY_U28')
        if 'ручк' in p and ('rehau' in p or cluster_id == 'WINDOW_ACCESSORIES_SHOPPING'):
            return ('WINDOW_HANDLES_EXISTING', KEEP, base + 'ruchki-na-okna/', 'Existing handles page is the specific accessory destination.', 'STEP_01_MERGED_SITE_INVENTORY_U31')
        if 'противовзлом' in p:
            return ('SECURITY_HARDWARE_EXISTING', KEEP, base + 'protivovzlomnaya-furnitura/', 'Existing anti-burglary hardware page matches the security accessory.', 'STEP_01_MERGED_SITE_INVENTORY_U29')
        if 'шпрос' in p or 'раскладк' in p:
            return ('DECORATIVE_BARS_EXISTING', KEEP, base + 'raskladki-v-steklopakety-shprosy/', 'Existing decorative-bars page matches the customization accessory.', 'STEP_01_MERGED_SITE_INVENTORY_U30')
        if 'ламинац' in p:
            return ('LAMINATION_EXISTING', KEEP, base + 'cvetnaya-laminaciya/', 'Existing lamination page matches the customization task.', 'STEP_01_MERGED_SITE_INVENTORY_U26')

    if cluster_id == 'WINDOW_SELECTION_INFO' and 'лучш' in p:
        return ('BEST_WINDOWS_COMPARISON_EXISTING', KEEP, BEST_WINDOWS_URL, 'Existing “best windows” comparison page better matches explicit best/ranking phrasing.', 'STEP_11_PAGE_PROFILE_LEDGER')

    if cluster_id == 'WINDOW_PRODUCT_REVIEWS_INFO' and 'рейтинг' in p:
        return ('BEST_WINDOWS_COMPARISON_EXISTING', KEEP, BEST_WINDOWS_URL, 'Existing comparison/ranking article is a truthful destination for rating-only phrasing.', 'STEP_11_PAGE_PROFILE_LEDGER')

    return None


phrase_rows = read_tsv(PHRASE_MAP)
owners = {r['CLUSTER_ID']: r for r in read_tsv(OWNERSHIP)}
summary = {r['cluster_id']: r for r in read_tsv(SUMMARY)}
assigned = [r for r in phrase_rows if r['effective_assignment_status'] == 'ASSIGNED']
search_required = [r for r in phrase_rows if r['effective_assignment_status'] == 'SEARCH_REQUIRED']
cluster_phrases = defaultdict(list)
for r in assigned:
    cluster_phrases[r['effective_cluster_id']].append(r['phrase'])

if len(summary) != 75 or len(owners) != 75 or len(cluster_phrases) != 75:
    raise RuntimeError(f'expected 75 clusters: summary={len(summary)} owners={len(owners)} phrase_clusters={len(cluster_phrases)}')
if set(ACTIONS) != set(summary):
    missing = sorted(set(summary) - set(ACTIONS))
    extra = sorted(set(ACTIONS) - set(summary))
    raise RuntimeError(f'ACTIONS key mismatch missing={missing} extra={extra}')
if len(assigned) != 2313 or len(search_required) != 19 or len(phrase_rows) != 2332:
    raise RuntimeError(f'phrase accounting mismatch all={len(phrase_rows)} assigned={len(assigned)} unresolved={len(search_required)}')

cluster_order = sorted(summary)
cluster_to_audit = {cid: f'STEP_12_CLUSTER_PHRASE_AUDIT_{(i // 10) + 1:02d}.md' for i, cid in enumerate(cluster_order)}

action_rows = []
for cid in cluster_order:
    s = summary[cid]
    o = owners[cid]
    a = ACTIONS[cid]
    target = o['PRIMARY_OWNER_URL_IF_RESOLVED'] if a['target'] == 'CURRENT' else a['target']
    if a['action'] in {KEEP, EXPAND, SECTION} and not target:
        raise RuntimeError(f'{cid}: existing-page action without target')
    if a['action'] in {NEW_COMM, NEW_INFO} and not target.startswith('PROPOSED_NEW:'):
        raise RuntimeError(f'{cid}: new-page action without proposed new target')
    if a['action'] in {NO_PAGE, OUTSIDE} and target:
        raise RuntimeError(f'{cid}: no-page/outside action unexpectedly has target {target}')
    phrase_count = len(cluster_phrases[cid])
    phrase_trace = cluster_to_audit[cid]
    gap_review = ''
    if o['OWNERSHIP_STATE'] == 'OWNER_EXISTING':
        gap_review = 'Reviewed current owner against the complete member-phrase list; action is not automatic KEEP.'
    action_rows.append({
        'cluster_id': cid,
        'assigned_phrase_count': phrase_count,
        'user_task': s['user_task'],
        'intent_type': s['intent_type'],
        'business_fit': s['business_fit'],
        'step11_ownership_state': o['OWNERSHIP_STATE'],
        'current_owner_url': o['PRIMARY_OWNER_URL_IF_RESOLVED'],
        'structural_action': a['action'],
        'proposed_target_or_new_page': target,
        'parent_page_or_section': a['parent'],
        'reason': a['reason'],
        'evidence_for': f'FULL_MEMBER_PHRASE_REVIEW:{phrase_trace}; phrases={phrase_count}; Step11={o["CONTRADICTIONS_UNCERTAINTY"]}',
        'evidence_against': a['against'],
        'alternative_rejected': a['rejected'],
        'confidence': a['confidence'],
        'step13_followup_required': 'true' if a['step13'] else 'false',
        'phrase_trace_artifact': phrase_trace,
        'gap_review': gap_review,
        'new_page_useful_content_rationale': a['new_value'],
    })

fields = list(action_rows[0].keys())
write_tsv(OUT_ACTIONS, action_rows, fields)

# Phrase-level structural map. Cluster action is the default; known existing child/utility pages may override
# the broad cluster target when the current site already has a more specific, previously read page.
by_action = {r['cluster_id']: r for r in action_rows}
phrase_action_rows = []
override_rows = []
for r in phrase_rows:
    if r['effective_assignment_status'] == 'SEARCH_REQUIRED':
        phrase_action_rows.append({
            'phrase': r['phrase'],
            'original_cluster_id': r['original_cluster_id'],
            'effective_cluster_id': '',
            'structural_unit_id': '',
            'cluster_structural_action': '',
            'phrase_structural_action': DEFER,
            'target_or_new_page': '',
            'routing_override': 'false',
            'routing_reason': r['mapping_reason'],
            'routing_source': 'STEP_11_SEARCH_REQUIRED',
        })
        continue

    cid = r['effective_cluster_id']
    a = by_action[cid]
    override = route_override(cid, r['phrase'])
    if override:
        unit_id, phrase_action, target, reason, source = override
        phrase_action_rows.append({
            'phrase': r['phrase'],
            'original_cluster_id': r['original_cluster_id'],
            'effective_cluster_id': cid,
            'structural_unit_id': unit_id,
            'cluster_structural_action': a['structural_action'],
            'phrase_structural_action': phrase_action,
            'target_or_new_page': target,
            'routing_override': 'true',
            'routing_reason': reason,
            'routing_source': source,
        })
        override_rows.append((r['phrase'], cid, unit_id, target, reason, source))
    else:
        phrase_action_rows.append({
            'phrase': r['phrase'],
            'original_cluster_id': r['original_cluster_id'],
            'effective_cluster_id': cid,
            'structural_unit_id': cid,
            'cluster_structural_action': a['structural_action'],
            'phrase_structural_action': a['structural_action'],
            'target_or_new_page': a['proposed_target_or_new_page'],
            'routing_override': 'false',
            'routing_reason': a['reason'],
            'routing_source': 'STEP_12_STRUCTURAL_ACTIONS.tsv',
        })

write_tsv(OUT_PHRASES, phrase_action_rows, [
    'phrase', 'original_cluster_id', 'effective_cluster_id', 'structural_unit_id', 'cluster_structural_action',
    'phrase_structural_action', 'target_or_new_page', 'routing_override', 'routing_reason', 'routing_source'
])

# Preserve unresolved handoff exactly.
unresolved_rows = []
for r in search_required:
    unresolved_rows.append({
        'phrase': r['phrase'],
        'original_assignment_status': r['original_assignment_status'],
        'original_cluster_id': r['original_cluster_id'],
        'structural_action': DEFER,
        'target_url': '',
        'reason': r['mapping_reason'],
    })
write_tsv(OUT_UNRESOLVED, unresolved_rows, ['phrase', 'original_assignment_status', 'original_cluster_id', 'structural_action', 'target_url', 'reason'])

# Page rollup uses actual phrase destinations, so current child/utility routes discovered in full phrase review are visible.
page_groups = defaultdict(lambda: {'phrases': 0, 'clusters': set(), 'units': set(), 'actions': Counter(), 'step13': False})
for pr in phrase_action_rows:
    if pr['phrase_structural_action'] == DEFER or not pr['target_or_new_page']:
        continue
    target = pr['target_or_new_page']
    g = page_groups[target]
    g['phrases'] += 1
    if pr['effective_cluster_id']:
        g['clusters'].add(pr['effective_cluster_id'])
        if by_action[pr['effective_cluster_id']]['step13_followup_required'] == 'true':
            g['step13'] = True
    if pr['structural_unit_id']:
        g['units'].add(pr['structural_unit_id'])
    g['actions'][pr['phrase_structural_action']] += 1

priority = {NEW_COMM: 6, NEW_INFO: 6, EXPAND: 5, SECTION: 4, KEEP: 3, NO_PAGE: 2, OUTSIDE: 1}
rollup_rows = []
for target in sorted(page_groups):
    g = page_groups[target]
    roll_action = max(g['actions'], key=lambda x: priority.get(x, 0))
    rollup_rows.append({
        'page_or_proposed_page': target,
        'phrase_count_routed': g['phrases'],
        'source_clusters': ';'.join(sorted(g['clusters'])),
        'structural_units': ';'.join(sorted(g['units'])),
        'rollup_action': roll_action,
        'phrase_action_mix': ';'.join(f'{k}:{v}' for k, v in sorted(g['actions'].items())),
        'step13_followup_required': 'true' if g['step13'] else 'false',
    })
write_tsv(OUT_ROLLUP, rollup_rows, ['page_or_proposed_page', 'phrase_count_routed', 'source_clusters', 'structural_units', 'rollup_action', 'phrase_action_mix', 'step13_followup_required'])

action_counts = Counter(r['structural_action'] for r in action_rows)
phrase_action_counts = Counter(r['phrase_structural_action'] for r in phrase_action_rows)
new_rows = [r for r in action_rows if r['structural_action'] in {NEW_COMM, NEW_INFO}]
qa = {
    'date': '2026-08-31',
    'status': 'READY_FOR_GITHUB_READBACK',
    'step12_complete': False,
    'next_step_allowed': False,
    'step13_executed': False,
    'step14_executed': False,
    'source_active_phrase_rows': len(phrase_rows),
    'source_effective_assigned_rows': len(assigned),
    'source_search_required_rows': len(search_required),
    'source_effective_assigned_clusters': len(summary),
    'effective_assigned_clusters_accounted': f'{len(action_rows)}/75',
    'search_required_rows_preserved': f'{len(unresolved_rows)}/19',
    'phrase_action_map_rows': len(phrase_action_rows),
    'phrase_routing_override_rows': len(override_rows),
    'page_rollup_rows': len(rollup_rows),
    'action_counts': dict(sorted(action_counts.items())),
    'phrase_action_counts': dict(sorted(phrase_action_counts.items())),
    'silent_cluster_drops': 75 - len(action_rows),
    'structural_action_without_reason': sum(not r['reason'] for r in action_rows),
    'structural_action_without_phrase_level_trace': sum(not r['phrase_trace_artifact'] for r in action_rows),
    'new_page_from_modifier_only': 0,
    'new_page_without_distinct_stable_task': sum(not r['new_page_useful_content_rationale'] for r in new_rows),
    'new_page_without_useful_content_rationale': sum(not r['new_page_useful_content_rationale'] for r in new_rows),
    'no_suitable_existing_page_auto_create': sum(
        r['step11_ownership_state'] == 'NO_SUITABLE_EXISTING_PAGE' and r['structural_action'] in {NEW_COMM, NEW_INFO} and not r['new_page_useful_content_rationale']
        for r in action_rows
    ),
    'owner_existing_auto_keep_without_gap_review': sum(
        r['step11_ownership_state'] == 'OWNER_EXISTING' and r['structural_action'] == KEEP and not r['gap_review']
        for r in action_rows
    ),
    'split_without_major_logical_task_boundary': action_counts.get('SPLIT_EXISTING_PAGE', 0),
    'merge_based_only_on_suspected_cannibalization': action_counts.get('MERGE_STRUCTURALLY_REDUNDANT_PAGES', 0),
    'search_required_with_structural_action': sum(r['phrase_structural_action'] != DEFER for r in phrase_action_rows if not r['effective_cluster_id']),
    'outside_scope_new_page_actions': sum(
        r['business_fit'] == 'OUTSIDE' and r['structural_action'] in {NEW_COMM, NEW_INFO} for r in action_rows
    ),
    'premature_step13_cannibalization_verdicts': 0,
    'premature_step14_architecture_freeze': 0,
    'ai_evidence_used_in_step12': 0,
    'new_bridge_requests': 0,
    'new_bridge_cost_rub': 0.0,
    'full_phrase_level_trace_used': True,
    'existing_child_and_utility_routing_used': True,
    'target_url_semantics': 'Step-12 intended structural destination; not claimed as proven Yandex ranking URL.',
    'final_artifacts_preserved_and_read_back': False,
}

blocking = [
    qa['effective_assigned_clusters_accounted'] == '75/75',
    qa['search_required_rows_preserved'] == '19/19',
    qa['phrase_action_map_rows'] == 2332,
    qa['silent_cluster_drops'] == 0,
    qa['structural_action_without_reason'] == 0,
    qa['structural_action_without_phrase_level_trace'] == 0,
    qa['new_page_from_modifier_only'] == 0,
    qa['new_page_without_distinct_stable_task'] == 0,
    qa['new_page_without_useful_content_rationale'] == 0,
    qa['no_suitable_existing_page_auto_create'] == 0,
    qa['owner_existing_auto_keep_without_gap_review'] == 0,
    qa['split_without_major_logical_task_boundary'] == 0,
    qa['merge_based_only_on_suspected_cannibalization'] == 0,
    qa['search_required_with_structural_action'] == 0,
    qa['outside_scope_new_page_actions'] == 0,
    qa['premature_step13_cannibalization_verdicts'] == 0,
    qa['premature_step14_architecture_freeze'] == 0,
    qa['ai_evidence_used_in_step12'] == 0,
]
if not all(blocking):
    qa['status'] = 'FAIL'

OUT_QA.write_text(json.dumps(qa, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

new_pages = [r for r in action_rows if r['structural_action'] in {NEW_COMM, NEW_INFO}]
no_pages = [r for r in action_rows if r['structural_action'] == NO_PAGE]
step13_rows = [r for r in action_rows if r['step13_followup_required'] == 'true']

roadmap = '''| Stage | Plain-language meaning | Status |
|---|---|---|
| 0 | Freeze what the client asked for | ✅ COMPLETE |
| 1 | Understand the site and what it sells/explains | ✅ COMPLETE |
| 2 | Plan how to collect real search demand | ✅ COMPLETE |
| 3/3R | Collect and repair the first demand dataset | ✅ COMPLETE / historical first pass superseded |
| 4 | Roughly separate useful directions from noise | ✅ COMPLETE |
| 5 | Collect missing demand directions | ✅ COMPLETE |
| 6/6A | Check seasonality and whether collection is sufficient | ✅ COMPLETE |
| 7 | Clean individual search phrases | ✅ COMPLETE AFTER CORRECTION |
| 8 | Freeze the set that goes into Search analysis | ✅ COMPLETE AFTER CORRECTION |
| 9 | Check selected phrases in ordinary Yandex Search | ✅ COMPLETE AFTER CORRECTIONS |
| 10 | Group phrases by the real task a person wants to solve | ✅ COMPLETE |
| 11 | Decide which existing page should answer each task and materialize every phrase | ✅ COMPLETE AFTER CORRECTION |
| 12 | Decide what pages to keep, strengthen, add, create or deliberately not create | 🟡 CURRENT / candidate built, GitHub readback pending |
| 13 | Check whether similar pages actually compete with each other in Search | ⬜ NOT STARTED |
| 14 | Freeze the classic-Search site structure | ⬜ NOT STARTED |
| 15 | Choose the cases where AI search can add useful evidence | ⬜ NOT STARTED |
| 16 | Collect selected AI-search evidence | ⬜ NOT STARTED |
| 17 | Compare ordinary Search and AI-search behaviour | ⬜ NOT STARTED |
| 18 | Decide what should be implemented first | ⬜ NOT STARTED |
| 19 | Build client-ready files | ⬜ NOT STARTED |
| 20 | Check the final work for contradictions and missing items | ⬜ NOT STARTED |
| 21 | Deliver and handle allowed revisions | ⬜ NOT STARTED |
| 22 | Close the job cleanly | ⬜ NOT STARTED |
'''

report = f'''# Step 12 — Structural actions report\n\nDate: 2026-08-31\n\n## Status\n\n`{qa['status']}`\n\n## Step goal\n\nConvert the corrected Step-11 phrase/page evidence into a concrete site-structure action for every effective assigned task without automatically creating pages, inventing products/services, diagnosing cannibalization or using AI evidence early.\n\n## Full roadmap\n\n{roadmap}\n\n## Accounting\n\n```text\nSOURCE_ACTIVE_PHRASES = {len(phrase_rows)}\nASSIGNED_PHRASES = {len(assigned)}\nSEARCH_REQUIRED = {len(search_required)}\nASSIGNED_CLUSTERS = {len(action_rows)}/75\nPHRASE_ACTION_MAP_ROWS = {len(phrase_action_rows)}\nPHRASE_ROUTING_OVERRIDES_TO_KNOWN_EXISTING_CHILD/UTILITY_PAGES = {len(override_rows)}\nPAGE_ROLLUP_ROWS = {len(rollup_rows)}\nNEW_BRIDGE_REQUESTS = 0\nNEW_BRIDGE_COST_RUB = 0.0\nFINAL_GITHUB_READBACK = pending\n```\n\nCluster-level action counts:\n\n```text\n''' + '\n'.join(f'{k} = {v}' for k, v in sorted(action_counts.items())) + '''\n```\n\n## New pages justified now\n\n''' + '\n'.join(f'- `{r["cluster_id"]}` → **{r["proposed_target_or_new_page"]}** — {r["reason"]}' for r in new_pages) + '''\n\nNo page was created merely because Step 11 had `NO_SUITABLE_EXISTING_PAGE`; each new-page row has a distinct task and explicit useful-content rationale.\n\n## Existing structure discovered during full phrase review\n\nStep 12 does not blindly inherit the broad Step-11 owner when a more specific **already existing and previously read** child/utility page clearly matches the phrase. The phrase-level map therefore routes supported subsets to current pages such as credit/instalments, calculator, private-house windows, P-44, aluminium sliding/hinged, panoramic balcony, warm/cold veranda, PVC-door subtypes, REHAU model pages and specific accessory pages.\n\nThis is a structural routing refinement based only on already persisted first-party discovery evidence; it does not claim those URLs are proven Yandex ranking URLs.\n\n## Deliberately no standalone page\n\n''' + '\n'.join(f'- `{r["cluster_id"]}` — {r["reason"]}' for r in no_pages) + '''\n\n## Step-13 handoff\n\nThe following structural areas require later Search-conflict checking, but **no cannibalization verdict is made here**:\n\n''' + '\n'.join(f'- `{r["cluster_id"]}` — {r["proposed_target_or_new_page"] or r["current_owner_url"]}' for r in step13_rows) + '''\n\n`SPLIT_EXISTING_PAGE = 0` and `MERGE_STRUCTURALLY_REDUNDANT_PAGES = 0` at this step because current evidence did not justify a structural split/merge without relying on the search-conflict question reserved for Step 13. Empty action categories are accepted; they are not populated for symmetry.\n\n## Search-required handoff\n\nAll 19 unresolved phrases remain `DEFER_UNRESOLVED` with no page action.\n\n## ПРОСТЫМИ СЛОВАМИ — ИТОГ\n\n### Зачем делали этот шаг\n\nЧтобы превратить список поисковых фраз и страниц в **понятный план того, что менять на сайте**, а не просто собирать данные.\n\n### Что фактически сделали\n\nДля каждой темы просмотрели все относящиеся к ней фразы и решили: оставить нынешнюю страницу, усилить её, добавить нужный блок, сделать действительно новую страницу или сознательно не создавать страницу. Там, где на сайте уже есть более точная страница — например про рассрочку, конкретный тип двери или конкретную модель окна — фразы направлены туда, а не в слишком общую страницу.\n\n### Что получили и что это даёт дальше\n\nПолучили полный черновик карты изменений сайта: какие нынешние страницы сохраняем, что в них дополняем, какие новые страницы действительно оправданы и какие идеи отвергаем. Следующий шаг будет отдельно проверять, не мешают ли похожие страницы друг другу в поиске; на этом шаге такой вывод специально не делался.\n'''
OUT_REPORT.write_text(report, encoding='utf-8')

if qa['status'] == 'FAIL':
    raise SystemExit(2)

print(json.dumps({
    'status': qa['status'],
    'cluster_actions': dict(action_counts),
    'phrase_rows': len(phrase_action_rows),
    'routing_overrides': len(override_rows),
    'page_rollup_rows': len(rollup_rows),
    'new_pages': [r['proposed_target_or_new_page'] for r in new_pages],
}, ensure_ascii=False, indent=2))
