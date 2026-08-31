import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PHRASE_MAP = ROOT / 'STEP_11_PHRASE_PAGE_MAP.tsv'
SUMMARY = ROOT / 'STEP_11_EFFECTIVE_CLUSTER_SUMMARY.tsv'
OWNERS = ROOT / 'STEP_11_PAGE_OWNERSHIP_CORRECTED.tsv'
HIST = ROOT / 'STEP_12_PHRASE_ACTION_MAP.tsv'
OUT_ASSIGN = ROOT / 'STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V2.tsv'
OUT_CORR = ROOT / 'STEP_12_STRUCTURAL_UNIT_CORRECTIONS.tsv'
OUT_UNITS = ROOT / 'STEP_12_STRUCTURAL_UNITS.tsv'
OUT_SALVAGE = ROOT / 'STEP_12_NO_PAGE_OUTSIDE_SALVAGE_REVIEW.tsv'
OUT_QA = ROOT / 'STEP_12_STRUCTURAL_UNIT_CORRECTION_QA.json'

HOME='https://okno-msk.ru/'
REHAU='https://okno-msk.ru/okna-rehau/'
ALU='https://okno-msk.ru/alyuminievye-okna/'
ALU_SLIDE='https://okno-msk.ru/alyuminievye-okna/razdvizhnye/'
ALU_HINGE='https://okno-msk.ru/alyuminievye-okna/raspashnye/'
BALCONY='https://okno-msk.ru/balkony-i-lodzhii/'
BALCONY_COLD='https://okno-msk.ru/balkony-i-lodzhii/holodnoe-osteklenie/'
BALCONY_PAN='https://okno-msk.ru/balkony-i-lodzhii/panoramnoe-osteklenie-balkona/'
BALCONY_HINGE='https://okno-msk.ru/balkony-i-lodzhii/raspashnoe-osteklenie-balkonov/'
VERANDA='https://okno-msk.ru/verandy/'
VERANDA_COLD='https://okno-msk.ru/verandy/holodnoe-osteklenie-verand/'
VERANDA_WARM='https://okno-msk.ru/verandy/teploe-osteklenie-verand/'
DOORS='https://okno-msk.ru/dveri-rehau/'
DOOR_BALCONY=DOORS+'balkonnye-dveri/'
DOOR_SLIDE=DOORS+'razdvizhnye-dveri/'
DOOR_ENTRANCE=DOORS+'vhodnye-dveri/'
ACCESS='https://okno-msk.ru/okna-rehau/aksessuary-dlya-okon/'
WINDOWSILL=ACCESS+'podokonniki/'
DRIP=ACCESS+'otlivy/'
HANDLES=ACCESS+'ruchki-na-okna/'
BARS=ACCESS+'raskladki-v-steklopakety-shprosy/'
BLINDS=ACCESS+'zhalyuzi/'
SECURITY=ACCESS+'protivovzlomnaya-furnitura/'
FINANCE='https://okno-msk.ru/uslugi/kredit-i-rassrochka/'
CALC='https://okno-msk.ru/calculator/'
INSTALL='https://okno-msk.ru/uslugi/ustanovka-okon/'
REPAIR='https://okno-msk.ru/uslugi/remont-okon/'
FINISH='https://okno-msk.ru/uslugi/otdelka-otkosov/'
PRIVATE='https://okno-msk.ru/okna-rehau/po-tipu-doma/okna-v-chastnyj-dom/'
P44='https://okno-msk.ru/okna-rehau/okna-po-serii-domov/p-44/'
PAN_INFO='https://okno-msk.ru/stati/panoramnoe-osteklenie-eto-dan-mode-ili-praktichnoe-reshenie/'
PORTFOLIO='https://okno-msk.ru/nashi-raboty/'
BEST='https://okno-msk.ru/stati/kakie-okna-samye-luchshie/'
GLASS='https://okno-msk.ru/stati/kak-vybrat-steklopaket-dlya-plastikovogo-okna/'
FRENCH='https://okno-msk.ru/okna-rehau/francuzskie-okna/'
COMPANY='https://okno-msk.ru/o-kompanii/'


def read_tsv(path):
    with path.open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f, delimiter='\t'))


def write_tsv(path, rows, fields):
    with path.open('w', encoding='utf-8', newline='') as f:
        w=csv.DictWriter(f, fieldnames=fields, delimiter='\t', lineterminator='\n'); w.writeheader(); w.writerows(rows)


def unit(unit_id, task, role='PENDING_ACTION_REEVALUATION', primary='', support='', state='IN_SCOPE', maturity='PENDING_STEP12_ACTION_REEVALUATION', reason='', intent=''):
    return {'unit_id':unit_id,'task':task,'role':role,'primary':primary,'support':support,'state':state,'maturity':maturity,'reason':reason,'intent':intent}


def contains_any(p, parts):
    return any(x in p for x in parts)

phrase_rows=read_tsv(PHRASE_MAP)
summary={r['cluster_id']:r for r in read_tsv(SUMMARY)}
owners={r['CLUSTER_ID']:r for r in read_tsv(OWNERS)}
hist_rows=read_tsv(HIST)
hist_by_phrase={r['phrase']:r for r in hist_rows}
if len(phrase_rows)!=2332 or len(hist_rows)!=2332 or len(hist_by_phrase)!=2332:
    raise RuntimeError('input accounting mismatch')

cluster_action={}
for r in hist_rows:
    if r['effective_cluster_id'] and r['cluster_structural_action'] and r['effective_cluster_id'] not in cluster_action:
        cluster_action[r['effective_cluster_id']]=r['cluster_structural_action']

# Known clear in-scope rescues from historically OUTSIDE/no-page groups.
PAN_OUTSIDE_RESCUE={
    'виды панорамных окон в квартире':'PANORAMIC_WINDOW_TECH_SELECTION_INFO',
    'панорамное окно на кухне':'PANORAMIC_DESIGN_USECASE_INFO',
    'панорамное окно с дверью в частном доме':'PANORAMIC_PRIVATE_HOUSE_USECASE',
    'панорамные окна в частном доме':'PANORAMIC_PRIVATE_HOUSE_USECASE',
    'панорамные окна на террасу в частном доме':'PANORAMIC_OUTDOOR_GLAZING',
}


def classify_mixed(cid,p):
    # D12-02: split mixed units before structural actions.
    if cid=='WINDOW_INSTALLATION_DIY_INFO':
        if 'двер' in p:
            return unit('PVC_DOOR_INSTALLATION_REMOVAL_DIY','learn/remove/install PVC doors yourself','SUPPORTING_CONTENT',DOORS,'',reason='Door DIY is a different object from PVC-window installation and must not be forced into one window-installation article.',intent='DIY_INFO')
        if 'алюмини' in p:
            return unit('ALUMINIUM_WINDOW_INSTALLATION_REMOVAL_DIY','learn/remove/install aluminium windows yourself','SUPPORTING_CONTENT',ALU,'',reason='Aluminium DIY is a different material/product task from PVC-window installation.',intent='DIY_INFO')
        if 'француз' in p:
            return unit('FRENCH_WINDOW_INSTALLATION_DIY','learn/alter/install French windows yourself','SUPPORTING_CONTENT',FRENCH,'',reason='French-window DIY is a distinct form/redevelopment task.',intent='DIY_INFO')
        return unit('PVC_WINDOW_INSTALLATION_DIY','learn/install or remove PVC windows yourself','NEW_INFORMATIONAL_CANDIDATE','PROPOSED_NEW:/stati/ustanovka-plastikovyh-okon-svoimi-rukami/',INSTALL,reason='Corrected coherent subset: PVC-window DIY installation/removal only.',intent='DIY_INFO')

    if cid=='WINDOW_REPAIR_DIY_INFO':
        if p=='французское окно своими руками':
            return unit('FRENCH_WINDOW_DIY_GENERAL','understand/do French-window work yourself','SUPPORTING_CONTENT',FRENCH,'',reason='Not a PVC-window repair task.',intent='DIY_INFO')
        if p=='самому пластиковые окна':
            return unit('AMBIGUOUS_PVC_DIY','ambiguous DIY intent around PVC windows','DEFERRED','', '',state='DEFERRED_PENDING_MISSING_EVIDENCE',maturity='DEFERRED_PENDING_MISSING_EVIDENCE',reason='Bare phrase has no stable terminal task.',intent='DIY_INFO')
        if 'регулиров' in p or 'отрегулировать' in p:
            return unit('PVC_WINDOW_ADJUSTMENT_DIY','adjust PVC/Rehau windows yourself','NEW_INFORMATIONAL_SUBUNIT_CANDIDATE','PROPOSED_NEW:/stati/remont-i-regulirovka-plastikovyh-okon-svoimi-rukami/',REPAIR,reason='Adjustment is coherent self-help subtask; may share one final guide with general repair only after page-boundary evidence.',intent='DIY_INFO')
        if 'стеклопакет' in p:
            return unit('GLASS_UNIT_REPAIR_DIY','understand whether/how glazing-unit repair can be done yourself','SUPPORTING_SAFETY_CONTENT',GLASS,REPAIR,reason='Glazing-unit repair is a specific component/safety subtask, not generic mechanism repair.',intent='DIY_INFO')
        if p=='как открыть пластиковое окно':
            return unit('PVC_WINDOW_OPERATION_DIY','understand how to open/operate a PVC window','SUPPORTING_CONTENT','',REPAIR,reason='Operation question is adjacent to troubleshooting but not itself repair.',intent='DIY_INFO')
        return unit('PVC_WINDOW_REPAIR_DIY_GENERAL','diagnose/repair common PVC-window problems yourself','NEW_INFORMATIONAL_SUBUNIT_CANDIDATE','PROPOSED_NEW:/stati/remont-i-regulirovka-plastikovyh-okon-svoimi-rukami/',REPAIR,reason='Corrected coherent self-help repair subset.',intent='DIY_INFO')

    if cid=='WINDOW_HARDWARE_INFO':
        if 'отзыв' in p:
            return unit('WINDOW_HARDWARE_BRAND_REVIEWS_INFO','read reviews of specific hardware brands','UNSERVABLE_NEUTRAL_REVIEW','', '',state='NO_STANDALONE_FIRST_PARTY',maturity='FINAL_WITHIN_STEP12_EVIDENCE',reason='Specific third-party brand reviews are not the same task as a general hardware guide and a first-party seller is not a neutral review source.',intent='INFO')
        if 'смаз' in p:
            return unit('WINDOW_HARDWARE_MAINTENANCE_INFO','learn how to lubricate/maintain window hardware','SUPPORTING_CONTENT','PROPOSED_NEW:/stati/remont-i-regulirovka-plastikovyh-okon-svoimi-rukami/',REPAIR,reason='Maintenance/lubrication is a care task, not product/brand selection.',intent='INFO')
        if 'узлы алюминиевых окон' in p:
            return unit('ALUMINIUM_WINDOW_COMPONENTS_INFO','understand aluminium-window components/nodes','SUPPORTING_CONTENT',ALU,'',reason='Aluminium-specific component information belongs to aluminium technical context.',intent='INFO')
        if contains_any(p,['резин','уплотнител','ручку']) and 'выб' in p:
            return unit('WINDOW_COMPONENT_SELECTION_INFO','choose common window components such as seals or handles','SUPPORTING_CONTENT','PROPOSED_NEW:/stati/okonnaya-furnitura-vidy-brendy-kak-vybrat/',ACCESS,reason='Component selection is a narrower subtask inside a broader hardware-selection guide.',intent='INFO')
        return unit('WINDOW_HARDWARE_SELECTION_GUIDE','understand window hardware types, brands, construction and selection','NEW_INFORMATIONAL_CANDIDATE','PROPOSED_NEW:/stati/okonnaya-furnitura-vidy-brendy-kak-vybrat/',ACCESS,reason='Corrected core explanatory/selection subset; brand-review and maintenance tasks are separated.',intent='INFO')

    if cid=='WINDOW_HARDWARE_SHOPPING':
        if contains_any(p,['замена ','заменить ','поменять ']) and contains_any(p,['фурнитур','уплотнител','резин']):
            return unit('WINDOW_COMPONENT_REPLACEMENT_SERVICE','order replacement of window hardware/seals/components','PRIMARY_EXISTING_SERVICE',REPAIR,'',reason='Explicit replacement/price phrases are service tasks and the existing repair page covers component replacement.',intent='SERVICE')
        if contains_any(p,['пена установки','клинья для установки','анкерная пластина','монтажная пластина']):
            return unit('WINDOW_INSTALLATION_MATERIALS_INFO','understand/buy installation materials for windows','SUPPORTING_CONTENT','PROPOSED_NEW:/stati/ustanovka-plastikovyh-okon-svoimi-rukami/',INSTALL,state='IN_SCOPE_ADJACENT',reason='Installation materials are an installation subtask, not a general hardware-store landing.',intent='INFO_OR_SHOPPING')
        if 'ручк' in p:
            if 'пластиков' in p and 'двер' in p:
                return unit('PVC_DOOR_HANDLE_ACCESSORY','choose/buy PVC-door handles','SUPPORTING_EXISTING_PAGE',DOORS,ACCESS,reason='Door-handle demand is a door accessory task, not generic window hardware.',intent='COMMERCIAL')
            if 'алюмини' in p:
                return unit('ALUMINIUM_WINDOW_HANDLE_ACCESSORY','choose/buy aluminium-window handles','SUPPORTING_EXISTING_PAGE',ALU,ACCESS,reason='Aluminium-handle demand is material-specific; no general marketplace is assumed.',intent='COMMERCIAL')
            return unit('WINDOW_HANDLES_ACCESSORY','choose/buy window handles','PRIMARY_EXISTING_PRODUCT',HANDLES,ACCESS,reason='Existing window-handles page is the explicit accessory destination.',intent='COMMERCIAL')
        if contains_any(p,['детский замок','блокиратор','противовзлом']):
            return unit('WINDOW_SAFETY_HARDWARE_ACCESSORY','choose/buy window safety/security hardware','SUPPORTING_EXISTING_PAGE',SECURITY,ACCESS,reason='Safety/security hardware is a specific accessory task; use existing security/accessory structure, not a general marketplace.',intent='COMMERCIAL')
        if contains_any(p,['смазк','масло для']) or p.startswith('масло '):
            return unit('WINDOW_HARDWARE_MAINTENANCE_INFO','learn/select lubricant for window hardware maintenance','SUPPORTING_CONTENT','PROPOSED_NEW:/stati/remont-i-regulirovka-plastikovyh-okon-svoimi-rukami/',REPAIR,reason='Lubricant demand is maintenance-oriented; a separate hardware shop is not verified.',intent='INFO_OR_SHOPPING')
        if contains_any(p,['лучш','производител','производство','что входит','части оконной','элементы оконной','оконная фурнитура отзывы']) and not contains_any(p,['купить','магазин','цена','оптом']):
            return unit('WINDOW_HARDWARE_SELECTION_GUIDE','understand window hardware types, brands, producers and selection','NEW_INFORMATIONAL_CANDIDATE','PROPOSED_NEW:/stati/okonnaya-furnitura-vidy-brendy-kak-vybrat/',ACCESS,reason='Informational hardware phrases were mixed into shopping; salvage to explicit information unit.',intent='INFO')
        if contains_any(p,['стекло на пластиковое окно цена','стекло для пластиковой двери']):
            return unit('WINDOW_OR_DOOR_GLASS_COMPONENT','replace/buy window or door glass component','SUPPORTING_SERVICE_OR_PRODUCT',REPAIR,DOORS,reason='Glass component demand is not general hardware shopping; exact primary page requires later page-fit review.',intent='COMMERCIAL_OR_SERVICE')
        return unit('AFTERMARKET_WINDOW_HARDWARE_SHOPPING_UNSUPPORTED','buy aftermarket window hardware/parts from a broad catalog','NO_STANDALONE_UNVERIFIED_CATALOG','', '',state='NO_STANDALONE_FIRST_PARTY',maturity='FINAL_WITHIN_STEP12_EVIDENCE',reason='Target site is not verified as a broad third-party hardware/parts marketplace.',intent='COMMERCIAL')

    if cid=='WINDOW_ACCESSORIES_SHOPPING':
        if 'подоконник' in p:
            if 'остекление балкона' in p:
                return unit('BALCONY_GLAZING_WINDOWSILL_OPTION','include/select a windowsill as part of balcony glazing','SUPPORTING_CONTENT',BALCONY,WINDOWSILL,reason='Balcony-with-windowsill is an object/service option, not standalone windowsill shopping.',intent='SERVICE_OR_SELECTION')
            return unit('WINDOWSILL_ACCESSORY','choose/buy windowsills for windows','PRIMARY_EXISTING_PRODUCT',WINDOWSILL,ACCESS,reason='Existing windowsill page is a specific accessory destination.',intent='COMMERCIAL')
        if 'отлив' in p:
            return unit('WINDOW_DRIP_CAP_ACCESSORY','choose/buy window drip caps','PRIMARY_EXISTING_PRODUCT',DRIP,ACCESS,reason='Existing drip-cap page is the specific accessory destination.',intent='COMMERCIAL')
        if 'шпрос' in p or 'раскладк' in p:
            return unit('WINDOW_DECORATIVE_BARS_ACCESSORY','choose/buy decorative glazing bars','PRIMARY_EXISTING_PRODUCT',BARS,ACCESS,reason='Existing decorative-bars page is the specific accessory destination.',intent='COMMERCIAL')
        if 'откос' in p:
            return unit('WINDOW_FINISHING_SERVICE','order/understand window slopes and surround finishing','PRIMARY_EXISTING_SERVICE',FINISH,'',reason='Slope phrases are finishing-service tasks, not general accessory shopping.',intent='SERVICE')
        if 'поменять стеклопакет' in p:
            return unit('GLASS_UNIT_REPLACEMENT_SERVICE','order glazing-unit replacement','PRIMARY_EXISTING_SERVICE',REPAIR,GLASS,reason='Explicit replacement is a repair/service task.',intent='SERVICE')
        if 'стеклопакет' in p:
            return unit('GLASS_UNIT_PRODUCT_SELECTION','understand/select glazing units','SUPPORTING_CONTENT',GLASS,REHAU,reason='Glazing-unit phrases are a product/selection subtask, not generic accessories.',intent='INFO_OR_COMMERCIAL')
        if 'профиль' in p:
            if 'алюмини' in p:
                return unit('ALUMINIUM_PROFILE_PRODUCT','choose/buy aluminium window profile/system','SUPPORTING_EXISTING_PAGE',ALU,'',reason='Aluminium profile demand belongs to the aluminium product family.',intent='COMMERCIAL')
            return unit('PVC_PROFILE_PRODUCT_SELECTION','choose/buy PVC/Rehau profile/system','SUPPORTING_EXISTING_PAGE',REHAU,'',reason='PVC/Rehau profile demand belongs to the main profile/product selection structure.',intent='COMMERCIAL_OR_INFO')
        if contains_any(p,['рама','створк']) and not 'раздвижные окна алюминиевые рама' in p:
            return unit('WINDOW_FRAME_SASH_COMPONENT','understand/replace frame or sash components','SUPPORTING_SERVICE_OR_PRODUCT',REPAIR,ACCESS,reason='Frame/sash components are not a general accessory-purchase task.',intent='COMMERCIAL_OR_SERVICE')
        if contains_any(p,['наличник','нащельник','добор','герметик','крепление']):
            return unit('WINDOW_FINISHING_ACCESSORY_COMPONENTS','choose finishing/installation accessory components','SUPPORTING_EXISTING_PAGE',ACCESS,FINISH,reason='Finishing/installation components are a narrower accessory subtask.',intent='COMMERCIAL')
        return unit('WINDOW_ACCESSORIES_GENERAL','choose/buy general supported window accessories','PRIMARY_EXISTING_HUB',ACCESS,'',reason='Remaining phrases fit the existing accessory hub after mixed component/service tasks are removed.',intent='COMMERCIAL')

    if cid=='GLAZING_PERMISSION_INFO':
        if 'котельн' in p:
            return unit('BOILER_ROOM_WINDOW_REQUIREMENTS_INFO','understand window requirements for a private-house boiler room','SUPPORTING_CONTENT',PRIVATE,'',state='IN_SCOPE_ADJACENT',maturity='DEFERRED_PENDING_CONTENT_FACT_VERIFICATION',reason='Boiler-room requirements are a private-house technical/legal subtask; factual requirements must be independently verified before publication.',intent='INFO')
        if 'фурнитура гост' in p:
            return unit('WINDOW_HARDWARE_STANDARD_INFO','understand standards/GOST for window hardware','SUPPORTING_CONTENT','PROPOSED_NEW:/stati/okonnaya-furnitura-vidy-brendy-kak-vybrat/',ACCESS,state='IN_SCOPE_ADJACENT',maturity='DEFERRED_PENDING_CONTENT_FACT_VERIFICATION',reason='Hardware standards belong with hardware information, not a generic glazing-permission page.',intent='INFO')
        if 'француз' in p:
            return unit('FRENCH_WINDOW_REDEVELOPMENT_PERMISSION_INFO','understand redevelopment/permission issues for French-window conversion','SUPPORTING_CONTENT',FRENCH,'',maturity='DEFERRED_PENDING_CONTENT_FACT_VERIFICATION',reason='French-window redevelopment is its own legal context.',intent='INFO')
        return unit('BALCONY_GLAZING_PERMISSION_INFO','understand whether balcony glazing requires permission','SUPPORTING_CONTENT',BALCONY,'',maturity='DEFERRED_PENDING_CONTENT_FACT_VERIFICATION',reason='Balcony permission questions belong in balcony glazing context; one generic legal page is unnecessary.',intent='INFO')

    if cid=='WOOD_WINDOWS_COMMERCIAL':
        if p=='пластиковые окна в деревянном доме':
            return unit('PRIVATE_HOUSE_PVC_WINDOWS_WOODEN_HOUSE','choose/buy PVC windows for a wooden house','PRIMARY_EXISTING_PRODUCT',PRIVATE,REHAU,reason='Explicit PVC-in-wooden-house query is not wooden-window product demand.',intent='COMMERCIAL')
        if p=='деревянные пластиковые окна':
            return unit('WOOD_VS_PVC_WINDOWS_AMBIGUOUS','ambiguous wooden-vs-PVC window intent','DEFERRED','', '',state='DEFERRED_PENDING_MISSING_EVIDENCE',maturity='DEFERRED_PENDING_MISSING_EVIDENCE',reason='Phrase does not prove wooden-window purchase.',intent='AMBIGUOUS')
        return unit('WOOD_WINDOWS_UNVERIFIED_PRODUCT','buy/understand wooden-window products','NO_STANDALONE_UNVERIFIED_PRODUCT','', '',state='NO_STANDALONE_UNVERIFIED_BUSINESS',maturity='FINAL_WITHIN_STEP12_EVIDENCE',reason='Wooden-window product offer is not verified on the current site.',intent='COMMERCIAL')

    if cid=='PANORAMIC_WINDOWS_COMMERCIAL':
        if p in {'закрой панорамное окно','открой панорамное окно','открытое панорамное окно'}:
            return unit('PANORAMIC_WINDOW_OPERATION_AMBIGUOUS','ambiguous operation/open-close request for panoramic windows','DEFERRED','', '',state='DEFERRED_PENDING_MISSING_EVIDENCE',maturity='DEFERRED_PENDING_MISSING_EVIDENCE',reason='Command-like phrase is not a stable purchase task.',intent='AMBIGUOUS')
        if 'балкон' in p or 'лоджи' in p:
            return unit('PANORAMIC_BALCONY_GLAZING','order/understand panoramic balcony/loggia glazing','PRIMARY_EXISTING_SERVICE',BALCONY_PAN,BALCONY,reason='Object-specific balcony panoramic demand has an existing dedicated landing.',intent='SERVICE')
        if contains_any(p,['веранд','террас','бесед']):
            return unit('PANORAMIC_OUTDOOR_GLAZING','order/plan panoramic glazing for veranda/terrace/gazebo','PRIMARY_EXISTING_SERVICE',VERANDA,'PROPOSED_NEW:/panoramnye-okna/',reason='Outdoor-object task is distinct from generic panoramic-window purchase and already has an outdoor glazing hub.',intent='SERVICE_OR_COMMERCIAL')
        if p=='панорамные окна пик':
            return unit('PANORAMIC_REAL_ESTATE_BRAND_QUERY','real-estate/developer-specific panoramic-window query','OUTSIDE','', '',state='OUTSIDE_SCOPE',maturity='FINAL_WITHIN_STEP12_EVIDENCE',reason='Developer/real-estate brand query is not a target window purchase task.',intent='OUTSIDE')
        if contains_any(p,['какие панорамные окна лучше','панорамные окна как называются','утепление панорамных окон','ограждение панорамных окон']):
            return unit('PANORAMIC_WINDOW_TECH_SELECTION_INFO','understand/select panoramic window types, safety and thermal properties','PRIMARY_EXISTING_INFO',PAN_INFO,'PROPOSED_NEW:/panoramnye-okna/',reason='Selection/technical task is distinct from transaction and has an existing explanatory article.',intent='INFO')
        if contains_any(p,['барбекю','зал с панорам','камин панорам','комната с панорам','красивые панорам','панорамные окна лес','панорамные окна на море','панорамное окно снаружи','одноэтажный с панорам','пристройка с панорам','панорамные окна и потолок','бытовка с панорам','кв с панорам']):
            return unit('PANORAMIC_DESIGN_INSPIRATION','view design/application inspiration for panoramic glazing','PRIMARY_EXISTING_PORTFOLIO',PORTFOLIO,PAN_INFO,reason='Design/inspiration use cases should not be counted as commercial demand for a new landing.',intent='INFO')
        return unit('PANORAMIC_WINDOWS_COMMERCIAL_CORE','buy/order/configure panoramic windows','NEW_COMMERCIAL_CANDIDATE','PROPOSED_NEW:/panoramnye-okna/',REHAU,reason='Corrected commercial core after removing object-specific, informational, inspiration and ambiguous phrases.',intent='COMMERCIAL')

    return None


def classify_outside_or_no_page(cid,p):
    if cid=='OUTSIDE_CURTAINS_BLINDS':
        if 'жалюз' in p or 'плиссе' in p:
            if 'ремонт жалюзи' in p:
                return unit('WINDOW_BLINDS_REPAIR_UNVERIFIED','repair window blinds','DEFERRED','',BLINDS,state='DEFERRED_PENDING_BUSINESS_TRUTH',maturity='DEFERRED_PENDING_MISSING_EVIDENCE',reason='Site has a blinds page but repair service is not verified.',intent='SERVICE')
            if contains_any(p,['установ','монтаж']):
                return unit('WINDOW_BLINDS_INSTALLATION','install window blinds','SUPPORTING_EXISTING_PAGE',BLINDS,'',maturity='PROVISIONAL_PENDING_PAGE_FIT_REFRESH',reason='Blinds are a verified site accessory; installation scope on the page must be refreshed before final role.',intent='SERVICE')
            return unit('WINDOW_BLINDS_SHOPPING_SELECTION','choose/buy blinds for windows','PRIMARY_EXISTING_PRODUCT',BLINDS,ACCESS,maturity='PROVISIONAL_PENDING_PAGE_FIT_REFRESH',reason='Persisted site inventory has an existing blinds page, so these phrases are not globally outside scope.',intent='COMMERCIAL_OR_INFO')
        return unit('CURTAINS_SHUTTERS_OUTSIDE_SCOPE','curtains/shutters not verified as target window-accessory offer','OUTSIDE','', '',state='OUTSIDE_SCOPE',maturity='FINAL_WITHIN_STEP12_EVIDENCE',reason='Curtain/shutter demand is distinct from the verified blinds accessory page.',intent='OUTSIDE')

    if cid=='OPEN_BALCONY_FINISHING' and p=='остекление открытого балкона':
        return unit('BALCONY_GLAZING_GENERAL','order glazing of an open balcony','PRIMARY_EXISTING_SERVICE',BALCONY,'',reason='This phrase asks for glazing, not finishing without glazing.',intent='SERVICE')

    if cid=='OUTSIDE_REAL_ESTATE_ARCHITECTURE' and p in PAN_OUTSIDE_RESCUE:
        u=PAN_OUTSIDE_RESCUE[p]
        if u=='PANORAMIC_WINDOW_TECH_SELECTION_INFO':
            return unit(u,'understand/select panoramic window types for an apartment','PRIMARY_EXISTING_INFO',PAN_INFO,'',reason='Window-centric informational query is salvageable from the historical real-estate cluster.',intent='INFO')
        if u=='PANORAMIC_DESIGN_USECASE_INFO':
            return unit(u,'see/plan panoramic-window use in a kitchen','PRIMARY_EXISTING_PORTFOLIO',PORTFOLIO,PAN_INFO,reason='Window-use/design query is not pure real-estate search.',intent='INFO')
        if u=='PANORAMIC_PRIVATE_HOUSE_USECASE':
            return unit(u,'plan panoramic windows for a private house','SUPPORTING_EXISTING_PAGE',PRIVATE,'PROPOSED_NEW:/panoramnye-okna/',reason='Window-centric private-house use case is in-scope adjacent demand.',intent='INFO_OR_COMMERCIAL')
        if u=='PANORAMIC_OUTDOOR_GLAZING':
            return unit(u,'plan/order panoramic glazing for a terrace','PRIMARY_EXISTING_SERVICE',VERANDA,'PROPOSED_NEW:/panoramnye-okna/',reason='Terrace glazing is an in-scope glazing task.',intent='SERVICE_OR_COMMERCIAL')

    if cid=='NAVIGATION_BRAND_SITE' and p=='пластиковые окна от производителя официальный сайт':
        return unit('GENERIC_WINDOW_MANUFACTURER_SITE_NAVIGATION','reach a window manufacturer/seller official site','PRIMARY_EXISTING_TRUST_COMMERCIAL',HOME,COMPANY,reason='Generic manufacturer-site intent is not necessarily navigation to the REHAU brand domain.',intent='NAVIGATIONAL_COMMERCIAL')

    if cid=='WINDOWSILL_REPAIR_SERVICE':
        if 'поменять подоконник' in p:
            return unit('WINDOWSILL_REPLACEMENT_SERVICE','order replacement/installation of a windowsill','PRIMARY_EXISTING_SERVICE',FINISH,WINDOWSILL,reason='Replacement is different from repair/restoration and fits current finishing/windowsill assets.',intent='SERVICE')
        return unit('WINDOWSILL_REPAIR_UNVERIFIED','repair/restore a windowsill','DEFERRED','',WINDOWSILL,state='DEFERRED_PENDING_BUSINESS_TRUTH',maturity='DEFERRED_PENDING_MISSING_EVIDENCE',reason='Repair/restoration service remains unverified.',intent='SERVICE')

    if cid=='MOSQUITO_NET_REPAIR_SERVICE':
        if p=='пластиковые окна ремонт установка москитной сетки':
            return unit('MOSQUITO_NET_INSTALLATION_SERVICE','order mosquito-net installation','PRIMARY_EXISTING_SERVICE',ACCESS+'moskitnye-setki/','',reason='Phrase explicitly includes installation, a verified current mosquito-net task.',intent='SERVICE')
        if 'замена сетки' in p:
            return unit('MOSQUITO_NET_REPLACEMENT_SUPPORT','replace a mosquito-net mesh/net','SUPPORTING_EXISTING_PAGE',ACCESS+'moskitnye-setki/','',maturity='PROVISIONAL_PENDING_BUSINESS_TRUTH',reason='Replacement is adjacent to manufacture/install page but repair/replacement service needs confirmation.',intent='SERVICE')
        return unit('MOSQUITO_NET_REPAIR_UNVERIFIED','repair mosquito nets','DEFERRED','',ACCESS+'moskitnye-setki/',state='DEFERRED_PENDING_BUSINESS_TRUTH',maturity='DEFERRED_PENDING_MISSING_EVIDENCE',reason='Standalone repair service is not verified.',intent='SERVICE')

    if cid=='OUTDOOR_GLAZING_SPECIALIZED_INFO':
        if 'жидкое стекло' in p:
            return unit('OUTDOOR_GLAZING_MATERIAL_AMBIGUOUS','ambiguous liquid-glass veranda glazing query','DEFERRED','',VERANDA,state='DEFERRED_PENDING_MISSING_EVIDENCE',maturity='DEFERRED_PENDING_MISSING_EVIDENCE',reason='Meaning is ambiguous and should not be forced into one specialized article.',intent='INFO')
        return unit('OUTDOOR_GLAZING_SPECIAL_TECH_INFO','understand special veranda glazing techniques/material choices','SUPPORTING_CONTENT',VERANDA,'',maturity='PROVISIONAL_PENDING_CONTENT_SCOPE',reason='Useful specialized information belongs in the outdoor glazing context without one mixed standalone page.',intent='INFO')

    if cid=='GLAZING_DIY_INFO':
        if 'балкон' in p:
            return unit('BALCONY_GLAZING_DIY_INFO','learn/do balcony glazing yourself','DEFERRED',BALCONY,'',state='IN_SCOPE_ADJACENT',maturity='DEFERRED_PENDING_DEMAND_SEARCH',reason='Useful DIY subtask is preserved explicitly; standalone page is not assumed.',intent='DIY_INFO')
        return unit('OUTDOOR_GLAZING_DIY_INFO','learn/do veranda/outdoor glazing yourself','DEFERRED',VERANDA,'',state='IN_SCOPE_ADJACENT',maturity='DEFERRED_PENDING_DEMAND_SEARCH',reason='Useful outdoor DIY subtask is preserved explicitly; standalone page is not assumed.',intent='DIY_INFO')

    if cid=='WINDOW_PRODUCT_VIDEO_INFO':
        if 'алюмини' in p:
            return unit('ALUMINIUM_WINDOW_VIDEO_CONTENT','view aluminium-window video information','SUPPORTING_CONTENT',ALU,PORTFOLIO,reason='Video is a content format on the relevant product page, not a standalone page.',intent='INFO')
        return unit('PVC_WINDOW_VIDEO_CONTENT','view PVC-window video information','SUPPORTING_CONTENT',REHAU,PORTFOLIO,reason='Video is a content format on the relevant product page, not a standalone page.',intent='INFO')

    if cid=='WINDOW_PRODUCT_REVIEWS_INFO':
        if 'рейтинг' in p:
            return unit('WINDOW_PRODUCT_RATING_COMPARISON_INFO','compare/rank window products','SUPPORTING_EXISTING_INFO',BEST,'',maturity='PROVISIONAL_PENDING_PAGE_FIT',reason='Rating wording belongs to comparison content rather than company testimonials.',intent='INFO')
        if 'grazio' in p:
            return unit('REHAU_GRAZIO_REVIEW_SUPPORT','read experience/review information about Rehau Grazio','SUPPORTING_PRODUCT_CONTENT',REHAU+'rehau-grazio/','',reason='Model-specific review need should be served transparently on/around the model page, not a fake neutral review page.',intent='INFO')
        if 'delight' in p:
            return unit('REHAU_DELIGHT_REVIEW_SUPPORT','read experience/review information about Rehau Delight','SUPPORTING_PRODUCT_CONTENT',REHAU,'',maturity='PROVISIONAL_PENDING_EXACT_MODEL_PAGE_REFRESH',reason='Model-specific review need is distinct from generic product ratings.',intent='INFO')
        if 'rehau' in p:
            return unit('REHAU_WINDOW_REVIEW_SUPPORT','read experience/review information about Rehau windows','SUPPORTING_PRODUCT_CONTENT',REHAU,'',reason='Brand-product review need can be supported transparently on brand/product pages; no neutral ranking claim.',intent='INFO')
        if 'француз' in p:
            return unit('FRENCH_WINDOW_REVIEW_SUPPORT','read experience/review information about French windows','SUPPORTING_PRODUCT_CONTENT',FRENCH,'',reason='Form-specific review need belongs near the French-window product context.',intent='INFO')
        if 'алюмини' in p:
            return unit('ALUMINIUM_WINDOW_REVIEW_SUPPORT','read experience/review information about aluminium windows','SUPPORTING_PRODUCT_CONTENT',ALU,'',reason='Material-specific review need belongs near aluminium product context.',intent='INFO')
        if 'двер' in p:
            return unit('PVC_DOOR_REVIEW_SUPPORT','read experience/review information about PVC doors','SUPPORTING_PRODUCT_CONTENT',DOORS,'',reason='Door review need belongs near PVC-door product context.',intent='INFO')
        return unit('PVC_WINDOW_REVIEW_SUPPORT','read experience/review information about PVC windows','SUPPORTING_PRODUCT_CONTENT',REHAU,'',reason='Generic product review need can be supported on product pages without pretending neutral ranking.',intent='INFO')

    # Historical generic provider/rating queries are consciously unservable as a neutral first-party ranking.
    if cid in {'BALCONY_GLAZING_PROVIDER_REVIEWS_INFO','WINDOW_PROVIDER_REVIEWS_INFO','OUTDOOR_GLAZING_REVIEWS_INFO'}:
        return unit(cid,'neutral provider/reputation comparison or generic reviews','UNSERVABLE_NEUTRAL_REVIEW','', '',state='NO_STANDALONE_FIRST_PARTY',maturity='FINAL_WITHIN_STEP12_EVIDENCE',reason='A first-party seller cannot truthfully act as a neutral ranking of competing providers.',intent='INFO')

    return None


def classify_historical_override(cid,p,h):
    uid=h['structural_unit_id']
    if not uid:
        return None
    if uid=='FINANCE_INSTALLMENT_EXISTING':
        base=owners[cid]['PRIMARY_OWNER_URL_IF_RESOLVED'] if cid in owners else ''
        return unit(f'{cid}__INSTALLMENT_CONDITION',f"{summary[cid]['user_task']} with instalment/credit condition",'SUPPORTING_CROSS_CUTTING_UTILITY',base,FINANCE,maturity='PROVISIONAL_PENDING_PRIMARY_VS_SUPPORT_SEARCH_CHECK',reason='Finance page is a verified supporting utility; first pass incorrectly made it the primary destination for every phrase containing finance wording.',intent=summary[cid]['intent_type'])
    if uid=='WINDOW_CALCULATOR_EXISTING':
        return unit('WINDOW_PRICE_ESTIMATION_CALCULATOR','calculate/estimate window price','PRIMARY_EXISTING_UTILITY',CALC,REHAU,reason='Explicit calculator/price-estimation task has a dedicated current utility.',intent='COMMERCIAL_INFO')
    if uid=='P44_WINDOWS_EXISTING':
        return unit('P44_WINDOWS_COMMERCIAL','buy/plan windows for P-44 house series','PRIMARY_EXISTING_PRODUCT',P44,REHAU,reason='Explicit house-series task has a dedicated current page.',intent='COMMERCIAL')
    if uid=='PRIVATE_HOUSE_WINDOWS_EXISTING':
        if contains_any(p,['котельн','ванн','вентиляц']):
            return unit('PRIVATE_HOUSE_SPECIAL_ROOM_WINDOWS','choose/plan windows for special rooms in a private house','SUPPORTING_EXISTING_PAGE',PRIVATE,'',maturity='PROVISIONAL_PENDING_CONTENT_SCOPE',reason='Special-room requirement is a subtask of private-house window planning, not a generic private-house purchase phrase.',intent='INFO_OR_COMMERCIAL')
        return unit('PRIVATE_HOUSE_WINDOWS_COMMERCIAL','buy/plan windows for a private house','PRIMARY_EXISTING_PRODUCT',PRIVATE,REHAU,reason='Explicit private-house window task has a dedicated current page.',intent='COMMERCIAL')
    if uid=='ALUMINIUM_SLIDING_EXISTING':
        if 'балкон' in p or 'лоджи' in p:
            primary=BALCONY_COLD if 'холод' in p else BALCONY
            return unit('BALCONY_ALUMINIUM_SLIDING_GLAZING','order aluminium sliding glazing for balcony/loggia','PROVISIONAL_OBJECT_VS_MATERIAL_PAGE',primary,ALU_SLIDE,maturity='PROVISIONAL_PENDING_SEARCH_BOUNDARY',reason='Object-specific balcony task should not be routed solely by the word sliding; object and material pages are both relevant.',intent='SERVICE')
        if contains_any(p,['веранд','террас','бесед']):
            primary=VERANDA_COLD if 'холод' in p else VERANDA
            return unit('OUTDOOR_ALUMINIUM_SLIDING_GLAZING','order aluminium sliding glazing for veranda/terrace/gazebo','PROVISIONAL_OBJECT_VS_MATERIAL_PAGE',primary,ALU_SLIDE,maturity='PROVISIONAL_PENDING_SEARCH_BOUNDARY',reason='Outdoor-object task should not be routed solely by opening-mode wording.',intent='SERVICE_OR_COMMERCIAL')
        return unit('ALUMINIUM_SLIDING_WINDOWS','buy/choose sliding aluminium windows','PRIMARY_EXISTING_PRODUCT',ALU_SLIDE,ALU,reason='Generic sliding-aluminium product task has a dedicated current child page.',intent='COMMERCIAL')
    if uid=='ALUMINIUM_HINGED_EXISTING':
        return unit('ALUMINIUM_HINGED_WINDOWS','buy/choose hinged/tilt-turn aluminium windows','PRIMARY_EXISTING_PRODUCT',ALU_HINGE,ALU,reason='Generic hinged-aluminium subtype has a dedicated current child page.',intent='COMMERCIAL')
    if uid=='BALCONY_PANORAMIC_EXISTING':
        return unit('PANORAMIC_BALCONY_GLAZING','order/understand panoramic balcony glazing','PRIMARY_EXISTING_SERVICE',BALCONY_PAN,BALCONY,reason='Existing dedicated panoramic-balcony landing.',intent='SERVICE')
    if uid=='BALCONY_HINGED_EXISTING':
        return unit('BALCONY_HINGED_GLAZING','order hinged balcony glazing','PRIMARY_EXISTING_SERVICE',BALCONY_HINGE,BALCONY,reason='Existing dedicated hinged-balcony landing.',intent='SERVICE')
    if uid=='VERANDA_WARM_EXISTING':
        return unit('VERANDA_WARM_GLAZING','order warm/year-round veranda glazing','PRIMARY_EXISTING_SERVICE',VERANDA_WARM,VERANDA,reason='Existing dedicated warm-veranda landing.',intent='SERVICE')
    if uid=='VERANDA_COLD_EXISTING':
        return unit('VERANDA_COLD_GLAZING','order cold/seasonal veranda glazing','PRIMARY_EXISTING_SERVICE',VERANDA_COLD,VERANDA,reason='Existing dedicated cold-veranda landing.',intent='SERVICE')
    if uid=='PVC_BALCONY_DOOR_EXISTING':
        return unit('PVC_BALCONY_DOORS_COMMERCIAL','buy/order PVC balcony doors','PRIMARY_EXISTING_PRODUCT',DOOR_BALCONY,DOORS,reason='Existing dedicated balcony-door child page.',intent='COMMERCIAL')
    if uid=='PVC_SLIDING_DOOR_EXISTING':
        return unit('PVC_SLIDING_DOORS_COMMERCIAL','buy/order sliding PVC doors','PRIMARY_EXISTING_PRODUCT',DOOR_SLIDE,DOORS,reason='Existing dedicated sliding-door child page.',intent='COMMERCIAL')
    if uid=='PVC_ENTRANCE_DOOR_EXISTING':
        return unit('PVC_ENTRANCE_DOORS_COMMERCIAL','buy/order entrance/exterior PVC doors','PRIMARY_EXISTING_PRODUCT',DOOR_ENTRANCE,DOORS,reason='Existing dedicated entrance-door child page.',intent='COMMERCIAL')
    if uid.startswith('REHAU_') and uid.endswith('_EXISTING'):
        target=h['target_or_new_page']
        model=uid.removeprefix('REHAU_').removesuffix('_EXISTING').title()
        return unit(f'REHAU_{model.upper()}_COMMERCIAL',f'buy/order Rehau {model} profile windows','PRIMARY_EXISTING_PRODUCT',target,REHAU,reason='Exact Rehau model phrase has a dedicated current model page.',intent='COMMERCIAL')
    if uid=='WINDOWSILL_EXISTING':
        if 'остекление балкона' in p:
            return unit('BALCONY_GLAZING_WINDOWSILL_OPTION','include/select a windowsill in balcony glazing','SUPPORTING_CONTENT',BALCONY,WINDOWSILL,reason='Object/service option should not be made primarily a windowsill-shopping query.',intent='SERVICE_OR_SELECTION')
        return unit('WINDOWSILL_ACCESSORY','choose/buy windowsills','PRIMARY_EXISTING_PRODUCT',WINDOWSILL,ACCESS,reason='Existing windowsill page.',intent='COMMERCIAL')
    if uid=='DRIP_CAP_EXISTING':
        return unit('WINDOW_DRIP_CAP_ACCESSORY','choose/buy drip caps','PRIMARY_EXISTING_PRODUCT',DRIP,ACCESS,reason='Existing drip-cap page.',intent='COMMERCIAL')
    if uid=='DECORATIVE_BARS_EXISTING':
        return unit('WINDOW_DECORATIVE_BARS_ACCESSORY','choose/buy decorative glazing bars','PRIMARY_EXISTING_PRODUCT',BARS,ACCESS,reason='Existing decorative-bars page.',intent='COMMERCIAL')
    if uid=='WINDOW_HANDLES_EXISTING':
        return unit('WINDOW_HANDLES_ACCESSORY','choose/buy window handles','PRIMARY_EXISTING_PRODUCT',HANDLES,ACCESS,reason='Existing window-handles page.',intent='COMMERCIAL')
    if uid=='BEST_WINDOWS_COMPARISON_EXISTING':
        if p=='лучшие панорамные окна':
            return unit('PANORAMIC_WINDOW_TECH_SELECTION_INFO','understand/select the best panoramic window options','PROVISIONAL_EXISTING_INFO',PAN_INFO,'PROPOSED_NEW:/panoramnye-okna/',maturity='PROVISIONAL_PENDING_PAGE_FIT',reason='Panoramic-specific selection should not be forced into a generic best-windows article by the word best.',intent='INFO')
        return unit('BEST_PVC_REHAU_WINDOWS_COMPARISON','compare/rank PVC/Rehau window options','PRIMARY_EXISTING_INFO',BEST,REHAU,reason='Existing comparison article fits explicit best/rating selection wording.',intent='INFO')
    return None

assign=[]
corrections=[]
salvage=[]
unit_members=defaultdict(list)
unit_meta={}

for r in phrase_rows:
    phrase=r['phrase']; cid=r['effective_cluster_id']; status=r['effective_assignment_status']; h=hist_by_phrase[phrase]
    if status=='SEARCH_REQUIRED':
        rec={
            'phrase':phrase,'original_effective_cluster_id':'','final_structural_unit_id':'','final_unit_task':'','intent_type':'','business_scope_state':'SEARCH_REQUIRED','unit_page_role':'DEFERRED','primary_page_candidate':'','supporting_page':'','recommendation_maturity':'DEFERRED_PENDING_UPSTREAM_RESOLUTION','assignment_origin':'UPSTREAM_SEARCH_REQUIRED','correction_reason':r['mapping_reason'],'historical_routing_override':'false','historical_target_or_new_page':'','historical_structural_unit_id':''
        }
        assign.append(rec); continue

    u=classify_mixed(cid,phrase)
    origin='MIXED_UNIT_CORRECTION' if u else ''
    if not u:
        u=classify_outside_or_no_page(cid,phrase)
        origin='OUTSIDE_NO_PAGE_SALVAGE_REVIEW' if u else ''
    if not u and h['routing_override']=='true':
        u=classify_historical_override(cid,phrase,h)
        origin='HISTORICAL_OVERRIDE_MATERIALIZED' if u else ''
    if not u:
        s=summary[cid]; o=owners[cid]
        target=o['PRIMARY_OWNER_URL_IF_RESOLVED']
        state='OUTSIDE_SCOPE' if s['business_fit']=='OUTSIDE' else 'IN_SCOPE'
        role='BASE_UNIT_PENDING_ACTION_REEVALUATION'
        maturity='PENDING_STEP12_ACTION_REEVALUATION'
        u=unit(cid,s['user_task'],role,target,'',state,maturity,'No structural-unit correction required in this semantic-repair pass; action will be re-evaluated later.',s['intent_type'])
        origin='UNCHANGED_BASE_UNIT'

    rec={
        'phrase':phrase,
        'original_effective_cluster_id':cid,
        'final_structural_unit_id':u['unit_id'],
        'final_unit_task':u['task'],
        'intent_type':u['intent'] or summary[cid]['intent_type'],
        'business_scope_state':u['state'],
        'unit_page_role':u['role'],
        'primary_page_candidate':u['primary'],
        'supporting_page':u['support'],
        'recommendation_maturity':u['maturity'],
        'assignment_origin':origin,
        'correction_reason':u['reason'],
        'historical_routing_override':h['routing_override'],
        'historical_target_or_new_page':h['target_or_new_page'],
        'historical_structural_unit_id':h['structural_unit_id'],
    }
    assign.append(rec)
    unit_members[u['unit_id']].append(rec)
    unit_meta[u['unit_id']]=u

    changed=(u['unit_id']!=cid or h['routing_override']=='true' or origin in {'MIXED_UNIT_CORRECTION','OUTSIDE_NO_PAGE_SALVAGE_REVIEW'})
    if changed:
        corrections.append({
            'phrase':phrase,'original_effective_cluster_id':cid,'historical_step12_structural_unit_id':h['structural_unit_id'],'historical_step12_target':h['target_or_new_page'],'corrected_structural_unit_id':u['unit_id'],'corrected_unit_task':u['task'],'corrected_primary_page_candidate':u['primary'],'corrected_supporting_page':u['support'],'corrected_page_role':u['role'],'corrected_business_scope_state':u['state'],'correction_reason':u['reason'],'correction_origin':origin,'review_status':'CANDIDATE_MATERIALIZED_PENDING_FULL_READBACK_REVIEW'
        })

    hist_cluster_action=cluster_action.get(cid,'')
    if hist_cluster_action in {'NO_STANDALONE_PAGE','OUTSIDE_SCOPE_NO_ACTION'}:
        if u['unit_id']!=cid or u['state'] not in {'NO_STANDALONE_FIRST_PARTY','NO_STANDALONE_UNVERIFIED_BUSINESS','OUTSIDE_SCOPE'}:
            disposition='SALVAGED_OR_EXPLICITLY_DEFERRED'
        elif u['state']=='OUTSIDE_SCOPE':
            disposition='OUTSIDE_CONFIRMED'
        else:
            disposition='NO_STANDALONE_CONFIRMED_UNSERVABLE_OR_UNVERIFIED'
        salvage.append({
            'phrase':phrase,'historical_cluster_id':cid,'historical_cluster_action':hist_cluster_action,'final_structural_unit_id':u['unit_id'],'final_business_scope_state':u['state'],'final_page_role':u['role'],'primary_page_candidate':u['primary'],'supporting_page':u['support'],'review_disposition':disposition,'review_reason':u['reason'],'review_status':'CANDIDATE_REVIEWED_BY_CORRECTION_LOGIC_PENDING_READBACK_AUDIT'
        })

# Unit summary.
units=[]
for uid, rows in sorted(unit_members.items()):
    meta=unit_meta[uid]
    source_clusters=sorted({r['original_effective_cluster_id'] for r in rows})
    origins=Counter(r['assignment_origin'] for r in rows)
    units.append({
        'structural_unit_id':uid,'phrase_count':len(rows),'source_effective_clusters':';'.join(source_clusters),'user_task':meta['task'],'intent_type':meta['intent'],'business_scope_state':meta['state'],'unit_page_role':meta['role'],'primary_page_candidate':meta['primary'],'supporting_page':meta['support'],'recommendation_maturity':meta['maturity'],'confidence':'PENDING_EVIDENCE_DERIVATION','assignment_origin_mix':';'.join(f'{k}:{v}' for k,v in sorted(origins.items())),'unit_reason':meta['reason']
    })

write_tsv(OUT_ASSIGN,assign,list(assign[0].keys()))
write_tsv(OUT_CORR,corrections,list(corrections[0].keys()))
write_tsv(OUT_UNITS,units,list(units[0].keys()))
write_tsv(OUT_SALVAGE,salvage,list(salvage[0].keys()))

# Candidate QA only. Semantic defects remain open until assistant reads/reviews persisted output.
override_rows=[r for r in assign if r['historical_routing_override']=='true']
override_materialized=sum(r['assignment_origin'] in {'HISTORICAL_OVERRIDE_MATERIALIZED','MIXED_UNIT_CORRECTION','OUTSIDE_NO_PAGE_SALVAGE_REVIEW'} for r in override_rows)
mandatory_original={'WINDOW_INSTALLATION_DIY_INFO','PANORAMIC_WINDOWS_COMMERCIAL','GLAZING_PERMISSION_INFO','WOOD_WINDOWS_COMMERCIAL','WINDOW_HARDWARE_INFO','WINDOW_REPAIR_DIY_INFO','WINDOW_HARDWARE_SHOPPING','WINDOW_ACCESSORIES_SHOPPING'}
remaining_mixed_as_single={cid for cid in mandatory_original if any(r['final_structural_unit_id']==cid for r in assign)}
qa={
    'status':'CANDIDATE_STRUCTURAL_UNITS_BUILT_REVIEW_REQUIRED',
    'source_phrase_rows':len(phrase_rows),
    'final_assignment_rows':len(assign),
    'assigned_structural_unit_rows':sum(bool(r['final_structural_unit_id']) for r in assign),
    'upstream_search_required_rows':sum(not r['final_structural_unit_id'] for r in assign),
    'final_structural_units':len(units),
    'correction_rows':len(corrections),
    'historical_override_rows':len(override_rows),
    'historical_override_rows_materialized_into_explicit_units':override_materialized,
    'historical_hidden_runtime_overrides_in_candidate_output':0,
    'historical_no_page_or_outside_review_rows':len(salvage),
    'salvaged_or_explicitly_deferred_from_no_page_or_outside':sum(r['review_disposition']=='SALVAGED_OR_EXPLICITLY_DEFERRED' for r in salvage),
    'outside_confirmed_rows':sum(r['review_disposition']=='OUTSIDE_CONFIRMED' for r in salvage),
    'no_standalone_confirmed_rows':sum(r['review_disposition']=='NO_STANDALONE_CONFIRMED_UNSERVABLE_OR_UNVERIFIED' for r in salvage),
    'mandatory_mixed_original_units_still_used_as_final_units':sorted(remaining_mixed_as_single),
    'default_high_confidence_rows':sum(r['confidence']=='HIGH' for r in units),
    'defects_closed_by_script_alone':[],
    'defects_candidate_for_closure_after_persisted_readback_review':['D12-01','D12-02','D12-08','D12-09','D12-12'],
}
if len(assign)!=2332 or len(override_rows)!=191 or override_materialized!=191 or qa['upstream_search_required_rows']!=19 or qa['default_high_confidence_rows']!=0:
    qa['status']='FAIL'
OUT_QA.write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(qa,ensure_ascii=False))
