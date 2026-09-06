#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, subprocess
from pathlib import Path

HERE=Path(__file__).resolve()
JOB=HERE.parents[2]
RELEASE=JOB/'OKNO_MSK_RESEARCH_RELEASE_CORRECTED_2026-09-05'
GEN=JOB/'tools/post_release_correction/generate_document_01_client_ru.py'
QA=JOB/'tools/post_release_correction/qa_document_01_client_ru.py'
QA_JSON=JOB/'RESEARCH_REBUILD_POST_RELEASE_DOCUMENT_01_RUSSIAN_CLIENT_QA_2026-09-06.json'
PASS_MD=JOB/'RESEARCH_REBUILD_POST_RELEASE_DOCUMENT_01_RUSSIAN_CLIENT_QA_PASS_2026-09-06.md'

BRAND_REPL=[('Рехау Термо','REHAU Thermo'),('Рехау','REHAU'),('Проведал','Provedal'),('КБЕ','KBE'),('Аккадо','Accado'),('Ворне','Vorne'),('Футурус','Futurus')]
QUERY_REPL={
    "('алюминиевые окна фапим'":"('алюминиевые окна fapim'",
    "('окна REHAU 70'":"('окна rehau 70'",
    "('окна REHAU KBE'":"('окна rehau kbe'",
    "('окна REHAU официальный'":"('окна rehau официальный'",
    "('окна REHAU провисли'":"('окна rehau провисли'",
    "('окна стеклопакеты REHAU'":"('окна стеклопакеты rehau'",
}
OLD_NOTE='Каждая строка ниже относится к одному конкретному исходному запросу. Если в исходной формулировке бренд был написан латиницей, в этой клиентской таблице его название передано русской записью; это только способ отображения и не означает новый поисковый запрос. Наблюдение по одной строке не переносится автоматически на соседние запросы и само по себе не определяет владельца страницы.'
NEW_NOTE='Каждая строка ниже относится к одному конкретному исходному запросу. Формулировки запросов сохранены в исходном написании, включая названия брендов латиницей там, где они так были зафиксированы. Наблюдение по одной строке не переносится автоматически на соседние запросы и само по себе не определяет владельца страницы.'


def patch_generator():
    s=GEN.read_text(encoding='utf-8')
    start=s.index('# Клиентский язык:')
    end=s.index('\ndef md_link', start)
    s=s[:start]+"""# Клиентский язык: служебная лексика проекта должна быть русской,
# но реальные бренды, продуктовые линейки и дословные строки доказательств
# сохраняются в исходном написании.
SOURCE_NATIVE_LATIN = {
    'REHAU','rehau','Provedal','provedal','KBE','kbe',
    'Accado','Vorne','Futurus','fapim','Thermo','thermo'
}

def clean(s):
    return s
"""+s[end:]
    for a,b in BRAND_REPL: s=s.replace(a,b)
    for a,b in QUERY_REPL.items(): s=s.replace(a,b,1)
    old="""('Provedal остекление веранды','остекление веранды системой Provedal; коммерческая услуга'),
('алюминиевые окна Provedal','алюминиевые окна Provedal; коммерческий товар'),
('алюминиевые окна Provedal','алюминиевые окна Provedal; коммерческий товар'),
('окна REHAU в рассрочку','окна REHAU с финансовым модификатором рассрочки'),
('окна REHAU в рассрочку','окна REHAU с финансовым модификатором рассрочки'),
('оконная фурнитура REHAU','фурнитура REHAU как аксессуарная товарная задача'),
('оконная фурнитура REHAU','фурнитура REHAU как аксессуарная товарная задача'),
('пластиковые окна REHAU','основная коммерческая товарная задача по окнам REHAU'),
('пластиковые окна от производителя REHAU','коммерческая задача по окнам REHAU от производителя'),
('пластиковые окна REHAU','основная коммерческая товарная задача по окнам REHAU'),
('пластиковые окна REHAU от производителя','коммерческая задача по окнам REHAU от производителя'),"""
    new="""('provedal остекление веранды','остекление веранды системой Provedal; коммерческая услуга'),
('алюминиевые окна provedal','алюминиевые окна Provedal; коммерческий товар'),
('алюминиевые окна проведал','алюминиевые окна Provedal; коммерческий товар'),
('окна rehau в рассрочку','окна REHAU с финансовым модификатором рассрочки'),
('окна рехау в рассрочку','окна REHAU с финансовым модификатором рассрочки'),
('оконная фурнитура rehau','фурнитура REHAU как аксессуарная товарная задача'),
('оконная фурнитура рехау','фурнитура REHAU как аксессуарная товарная задача'),
('пластиковые окна rehau','основная коммерческая товарная задача по окнам REHAU'),
('пластиковые окна от производителя rehau','коммерческая задача по окнам REHAU от производителя'),
('пластиковые окна рехау','основная коммерческая товарная задача по окнам REHAU'),
('пластиковые окна рехау от производителя','коммерческая задача по окнам REHAU от производителя'),"""
    if old not in s: raise RuntimeError('observation brand block not found')
    s=s.replace(old,new,1)
    s=s.replace("('рехау термо окна','товарная задача по конкретной системе REHAU Thermo')","('rehau thermo окна','товарная задача по конкретной системе REHAU Thermo')",1)
    s=s.replace("('какой профиль REHAU выбрать','информационное руководство по выбору профиля REHAU')","('какой профиль rehau выбрать','информационное руководство по выбору профиля REHAU')",1)
    s=s.replace("('окна REHAU москва','основная коммерческая задача по окнам REHAU в Москве')","('окна rehau москва','основная коммерческая задача по окнам REHAU в Москве')",1)
    s=s.replace(OLD_NOTE,NEW_NOTE)
    s=s.replace("latin=sorted(set(re.findall(r'[A-Za-z]+',visible)))\nif latin:\n    raise SystemExit('LATIN_VISIBLE_IN_MD: '+repr(latin[:50]))","latin=sorted(set(re.findall(r'[A-Za-z]+',visible)))\nforbidden_latin=sorted(set(latin)-SOURCE_NATIVE_LATIN)\nif forbidden_latin:\n    raise SystemExit('FORBIDDEN_INTERNAL_LATIN_IN_MD: '+repr(forbidden_latin[:50]))")
    s=s.replace("latin_docx=sorted(set(re.findall(r'[A-Za-z]+',texts)))\nif latin_docx: raise SystemExit('LATIN_VISIBLE_IN_DOCX: '+repr(latin_docx[:50]))","latin_docx=sorted(set(re.findall(r'[A-Za-z]+',texts)))\nforbidden_latin_docx=sorted(set(latin_docx)-SOURCE_NATIVE_LATIN)\nif forbidden_latin_docx: raise SystemExit('FORBIDDEN_INTERNAL_LATIN_IN_DOCX: '+repr(forbidden_latin_docx[:50]))")
    s=s.replace("'latin_visible_markdown':latin,'latin_visible_docx':latin_docx","'source_native_latin_markdown':latin,'source_native_latin_docx':latin_docx")
    GEN.write_text(s,encoding='utf-8')


def patch_qa():
    s=QA.read_text(encoding='utf-8')
    s=s.replace("LATIN = re.compile(r'[A-Za-z]+')","LATIN = re.compile(r'[A-Za-z]+')\nSOURCE_NATIVE_LATIN = {'REHAU','rehau','Provedal','provedal','KBE','kbe','Accado','Vorne','Futurus','fapim','Thermo','thermo'}\nEXPECTED_BRAND_QUERY_ROWS = {2:'алюминиевые окна fapim',12:'окна rehau 70',13:'окна rehau kbe',14:'окна rehau официальный',15:'окна rehau провисли',17:'окна стеклопакеты rehau',41:'provedal остекление веранды',42:'алюминиевые окна provedal',43:'алюминиевые окна проведал',44:'окна rehau в рассрочку',45:'окна рехау в рассрочку',46:'оконная фурнитура rehau',47:'оконная фурнитура рехау',48:'пластиковые окна rehau',49:'пластиковые окна от производителя rehau',50:'пластиковые окна рехау',51:'пластиковые окна рехау от производителя',53:'проведал остекление веранды',57:'rehau thermo окна',60:'какой профиль rehau выбрать',61:'окна rehau москва'}\nEXPECTED_BRAND_PROSE = ['REHAU','Provedal','KBE','Accado','Vorne','Futurus']")
    s=s.replace("latin={\n        'markdown_visible': sorted(set(LATIN.findall(vm))),\n        'docx_visible': sorted(set(LATIN.findall(dx))),\n        'pdf_visible': sorted(set(LATIN.findall(pf))),\n    }","latin={\n        'markdown_visible': sorted(set(LATIN.findall(vm))),\n        'docx_visible': sorted(set(LATIN.findall(dx))),\n        'pdf_visible': sorted(set(LATIN.findall(pf))),\n    }\n    forbidden_latin={k: sorted(set(v)-SOURCE_NATIVE_LATIN) for k,v in latin.items()}")
    needle="    action_block=section(md,'## 10. Полная карта 34 решений','## 11. Неопределённость и условия повторного открытия')\n    counts={"
    repl="    action_block=section(md,'## 10. Полная карта 34 решений','## 11. Неопределённость и условия повторного открытия')\n    obs_rows={}\n    for ln in obs_block.splitlines():\n        m=re.match(r'^\\|\\s*(\\d+)\\s*\\|\\s*(.*?)\\s*\\|', ln)\n        if m: obs_rows[int(m.group(1))]=m.group(2).strip()\n    brand_query_spelling_ok=all(obs_rows.get(n)==v for n,v in EXPECTED_BRAND_QUERY_ROWS.items())\n    brand_prose_preserved=all(x in vm and x in dx and x in pf for x in EXPECTED_BRAND_PROSE)\n    counts={"
    if needle not in s: raise RuntimeError('qa insertion point not found')
    s=s.replace(needle,repl)
    s=s.replace("'latin_visible_zero': all(not x for x in latin.values()),","'forbidden_internal_latin_zero': all(not x for x in forbidden_latin.values()),\n        'source_native_latin_preserved': brand_prose_preserved,\n        'verbatim_brand_query_spelling_preserved': brand_query_spelling_ok,")
    s=s.replace("'latin_visible_tokens':latin,","'source_native_latin_tokens':latin,\n        'forbidden_internal_latin_tokens':forbidden_latin,")
    s=s.replace("'internal_ascii_markers':internal_ascii_markers,","'internal_ascii_markers':internal_ascii_markers,\n        'brand_query_spelling_rows':{str(k):obs_rows.get(k) for k in EXPECTED_BRAND_QUERY_ROWS},")
    QA.write_text(s,encoding='utf-8')


def prepare():
    patch_generator(); patch_qa()
    subprocess.run(['python',str(GEN)],check=True)


def finalize():
    md=RELEASE/'sources/01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-05.md'
    dx=RELEASE/'editable/01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-05.docx'
    pdf=RELEASE/'01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-05.pdf'
    out=subprocess.check_output(['python',str(QA),'--markdown',str(md),'--docx',str(dx),'--pdf',str(pdf),'--visual-pages-pass','14'],text=True)
    QA_JSON.write_text(out,encoding='utf-8')
    q=json.loads(out); assert q['status']=='PASS'; assert q['checks']['verbatim_brand_query_spelling_preserved']
    sha=q['sha256']; sizes=q['size_bytes']
    PASS_MD.write_text(f'''# ОКНО МОСКВА — повторная проверка клиентского документа №01\n\nДата: 2026-09-06  \nРезультат: `PASS`\n\nКлиентский объяснительный текст написан по-русски. Реальные названия брендов, продуктовых линеек и дословные строки доказательств не переводятся и не транслитерируются. Сохранены `REHAU`, `Provedal`, `KBE`, `Accado`, `Vorne`, `Futurus`, `Thermo` и исходные написания `fapim`, `rehau`, `kbe`, `provedal`, `thermo` в точных запросах.\n\nУдалены только внутренние проектные англицизмы, статусы, технические классы, идентификаторы и производственный журнал. Независимая проверка отдельно сверяет строки, где различаются латинское и кириллическое написание бренда.\n\n- запрещённых внутренних латинских терминов: 0;\n- исходные брендовые написания: сохранены;\n- спорные семейства: 21/21;\n- проверки поискового помощника: 8/8;\n- наблюдения обычного Яндекса: 75/75;\n- практические решения: 34/34;\n- PDF: 14 страниц.\n\nАртефакты: Markdown `{sha['markdown']}`, DOCX `{sha['docx']}`, PDF `{sha['pdf']}`.\n\n`DOCUMENT_01_ANALYST_RECHECK = PASS`  \n`DOCUMENT_01_OWNER_REVIEW = PENDING__AWAITING_OWNER_RECHECK`  \n`CURRENT_DOCUMENT = 01`  \n`NEXT_ACTION = OWNER_REVIEW_CORRECTED_DOCUMENT_01`\n''',encoding='utf-8')
    sp=JOB/'RESEARCH_REPORT_REBUILD_CURRENT_STATE_POST_RELEASE_2026-09-05.json'; state=json.loads(sp.read_text(encoding='utf-8'))
    state['status']='STAGE_0_TO_15_HISTORICALLY_COMPLETE__DOCUMENT_01_RUSSIAN_CLIENT_CONTRACT_ANALYST_RECHECK_PASS__OWNER_REVIEW_PENDING'; state['next_action']='OWNER_REVIEW_CORRECTED_DOCUMENT_01'; state['correction_materialization_status']='DOCUMENT_01_RUSSIAN_CLIENT_CONTRACT_ANALYST_RECHECK_PASS__OWNER_REVIEW_PENDING__DOCUMENT_02_03_NOT_ADVANCED'; state['reviewed_release_files']['01_client_research_report']='ANALYST_RECHECK_PASS__OWNER_REVIEW_PENDING__SOURCE_NATIVE_BRANDS_PRESERVED'
    r=state['corrected_recipient_release']; r.update({'analyst_recipient_qa':'DOCUMENT_01_RUSSIAN_CLIENT_CONTRACT_PASS','document_01_analyst_recheck':'PASS','document_01_owner_review':'PENDING__AWAITING_OWNER_RECHECK','document_01_owner_review_authority':PASS_MD.name,'document_01_qa_json':QA_JSON.name,'document_01_qa_markdown':PASS_MD.name,'document_01_pdf_pages':q['pdf_pages'],'document_01_pdf_size_bytes':sizes['pdf'],'document_01_pdf_sha256':sha['pdf'],'document_01_docx_size_bytes':sizes['docx'],'document_01_docx_sha256':sha['docx'],'document_01_source_size_bytes':sizes['markdown'],'document_01_source_sha256':sha['markdown'],'document_01_client_forbidden_internal_latin':0,'document_01_source_native_brands_preserved':True,'document_01_verbatim_brand_query_spelling_preserved':True,'document_01_internal_process_narrative':0,'current_document':'01','document_02_owner_review':'PENDING','document_03_owner_review':'PENDING','final_owner_recipient_acceptance':'OPEN','owner_recheck':'ACTIVE__DOCUMENT_01_REWORKED__OWNER_REVIEW_PENDING'})
    sp.write_text(json.dumps(state,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    cp=JOB/'EXECUTION_CURSOR.json'; cur=json.loads(cp.read_text(encoding='utf-8')); cur['execution_protocol_status']='RESEARCH_REBUILD_STAGE_0_TO_15_COMPLETE__DOCUMENT_01_RUSSIAN_CLIENT_ANALYST_RECHECK_PASS__OWNER_REVIEW_PENDING'; cur['status']='RESEARCH_REBUILD_COMPLETE__DOCUMENT_01_RUSSIAN_CLIENT_ANALYST_RECHECK_PASS__OWNER_REVIEW_PENDING'; cur['execution_unit']='POST_RELEASE_OWNER_REVIEW_CORRECTED_DOCUMENT_01'; cur['next_action']='OWNER_REVIEW_CORRECTED_DOCUMENT_01'; d=cur.get('document_01_owner_recheck_2026_09_05',{}); d.update({'status':'ANALYST_RECHECK_PASS__OWNER_REVIEW_PENDING__SOURCE_NATIVE_BRANDS_PRESERVED','current_document':'01','document_01_analyst_recheck':'PASS','document_01_owner_review':'PENDING__AWAITING_OWNER_RECHECK','document_02_owner_review':'PENDING','document_03_owner_review':'PENDING','final_owner_recipient_acceptance':'OPEN','next_action':'OWNER_REVIEW_CORRECTED_DOCUMENT_01','physical_pdf_qa':'PASS__14_OF_14_PAGES','forbidden_internal_latin':0,'source_native_brands_preserved':True,'verbatim_brand_query_spelling_preserved':True,'internal_process_narrative':0,'qa_authority':QA_JSON.name}); cp.write_text(json.dumps(cur,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    mp=RELEASE/'RELEASE_MANIFEST_2026-09-05.json'; man=json.loads(mp.read_text(encoding='utf-8')); man['status']='DOCUMENT_01_RUSSIAN_CLIENT_ANALYST_RECHECK_PASS__OWNER_REVIEW_PENDING__DOCUMENT_02_03_NOT_ADVANCED'
    for a in man['recipient_artifacts']:
        if a.get('variant')=='01': a.update({'size_bytes':sizes['pdf'],'sha256':sha['pdf'],'pages':q['pdf_pages']})
    for a in man['editable_and_source_files']:
        if a['path'].startswith('editable/01_'): a.update({'size_bytes':sizes['docx'],'sha256':sha['docx']})
        if a['path'].startswith('sources/01_'): a.update({'size_bytes':sizes['markdown'],'sha256':sha['markdown']})
    z=man['qa']; z.update({'authority':'../'+QA_JSON.name,'document_01_owner_review_authority':'../'+PASS_MD.name,'document_01':'ANALYST_RECHECK_PASS__OWNER_REVIEW_PENDING','document_01_physical_pdf':'14_OF_14_PAGES_PASS','document_01_forbidden_internal_latin':0,'document_01_source_native_brands_preserved':True,'document_01_verbatim_brand_query_spelling_preserved':True,'current_document':'01','document_01_owner_review':'PENDING__AWAITING_OWNER_RECHECK','next_action':'OWNER_REVIEW_CORRECTED_DOCUMENT_01'}); mp.write_text(json.dumps(man,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    banner='> **ОТОЗВАНО 2026-09-06.** Этот старый результат приёмки недействителен. Текущий статус №01: повторная проверка аналитиком пройдена, приёмка владельцем ожидается.\n\n'
    for name in ['RESEARCH_REBUILD_POST_RELEASE_DOCUMENT_01_OWNER_REVIEW_PASS_2026-09-06.md','RESEARCH_REBUILD_POST_RELEASE_DOCUMENT_01_OWNER_PASS_GITHUB_READBACK_2026-09-06.md']:
        p=JOB/name
        if p.exists() and not p.read_text(encoding='utf-8').startswith('> **ОТОЗВАНО'): p.write_text(banner+p.read_text(encoding='utf-8'),encoding='utf-8')


def main():
    ap=argparse.ArgumentParser(); ap.add_argument('mode',choices=['prepare','finalize']); a=ap.parse_args(); prepare() if a.mode=='prepare' else finalize()
if __name__=='__main__': main()
