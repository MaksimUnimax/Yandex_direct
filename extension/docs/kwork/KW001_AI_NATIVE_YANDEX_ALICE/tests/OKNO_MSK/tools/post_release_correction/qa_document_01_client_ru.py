#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re, subprocess, tempfile, zipfile
from pathlib import Path

LATIN = re.compile(r'[A-Za-z]+')
SOURCE_NATIVE_LATIN = {'REHAU','rehau','Provedal','provedal','KBE','kbe','Accado','Vorne','Futurus','fapim','Thermo','thermo'}
EXPECTED_BRAND_QUERY_ROWS = {
    2:'алюминиевые окна fapim', 12:'окна rehau 70', 13:'окна rehau kbe',
    14:'окна rehau официальный', 15:'окна rehau провисли', 17:'окна стеклопакеты rehau',
    41:'provedal остекление веранды', 42:'алюминиевые окна provedal',
    43:'алюминиевые окна проведал', 44:'окна rehau в рассрочку',
    45:'окна рехау в рассрочку', 46:'оконная фурнитура rehau',
    47:'оконная фурнитура рехау', 48:'пластиковые окна rehau',
    49:'пластиковые окна от производителя rehau', 50:'пластиковые окна рехау',
    51:'пластиковые окна рехау от производителя', 53:'проведал остекление веранды',
    57:'rehau thermo окна', 60:'какой профиль rehau выбрать', 61:'окна rehau москва',
}
EXPECTED_BRAND_PROSE = ['REHAU','Provedal','KBE','Accado','Vorne','Futurus']

FORBIDDEN_PROCESS = [
    'гитхаб','коммит','чекпоинт','генератор','проверка отчёта','пересборк',
    'исправленный выпуск','внутренних файлов проекта','вызовы при исправлении',
    'история исправления','служебная трасса',
]
FORBIDDEN_CLIENT_FRAMING = [
    'Одна частично готовая работа',
    'Четыре вопроса, где изменения пока запрещены',
    'Двадцать одно спорное семейство запросов',
    'Неопределённость и условия повторного открытия',
    'Не создавать новые страницы по девятнадцати аналитическим назначениям',
    'Главный результат исследования — не расширение сайта любой ценой',
    'Связанные страницы не следует автоматически считать конкурирующими',
    'Эти проверки были дополнительным слоем',
    'семейный разбор',
    'аналитическое назначение',
    'физическое изменение запрещено',
    'правильное действие — ничего физически не менять',
    'спорных случаях',
    'разрушительные действия',
    'каннибализац',
    'не перестраивать всё целиком',
    'Новая страница не нужна',
    'Изменения не требуются',
    'Доказательств недостаточно',
    'не дал оснований создавать новое действие',
    'содержательный пробел, требующий отдельной работы, не доказан',
    'Расширять страницу только из-за ответа помощника не нужно',
    'нельзя расширять узкую инструкцию догадкой',
    'Ответ не доказал новую иерархию страниц',
]
REQUIRED_HEADINGS = [
    'Краткий вывод',
    'Что на сайте уже работает правильно',
    'Семь приоритетных улучшений существующих страниц',
    'Что уточнить у компании для двух следующих улучшений',
    'Как распределены основные группы поискового спроса',
    'Дополнительная проверка восьми важных тем',
    'Что передать в работу в первую очередь',
    'Что было проверено',
    'Приложение 1. Что показала выдача Яндекса по 75 конкретным запросам',
    'Приложение 2. Сводная карта результатов исследования',
    'Границы применения выводов',
]
CARD_LABELS = [
    'Что обнаружено:', 'Почему это важно:', 'Что рекомендуется сделать:',
    'Где:', 'Что сохранить:', 'Как должен выглядеть результат:', 'Как проверить:'
]


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def visible_md(text: str) -> str:
    text=re.sub(r'\]\([^)]*\)',']',text)
    text=re.sub(r'[`#*|\[\]]',' ',text)
    return text

def extract_docx_text(path: Path) -> str:
    with zipfile.ZipFile(path) as z:
        xml='\n'.join(z.read(n).decode('utf-8','ignore') for n in z.namelist()
                      if n.endswith('.xml') and ('document.xml' in n or 'header' in n or 'footer' in n))
    return ' '.join(re.findall(r'<w:t(?:\s[^>]*)?>(.*?)</w:t>',xml))

def extract_pdf(path: Path) -> tuple[str,int]:
    try:
        from pypdf import PdfReader
        r=PdfReader(str(path))
        return '\n'.join((p.extract_text() or '') for p in r.pages), len(r.pages)
    except Exception:
        with tempfile.TemporaryDirectory() as td:
            out=Path(td)/'x.txt'
            subprocess.run(['pdftotext',str(path),str(out)],check=True)
            text=out.read_text(encoding='utf-8',errors='ignore')
            info=subprocess.check_output(['pdfinfo',str(path)],text=True,encoding='utf-8',errors='ignore')
            m=re.search(r'^Pages:\s*(\d+)',info,re.M)
            return text,int(m.group(1)) if m else 0

def section(text:str,start:str,end:str)->str:
    a=text.index(start); b=text.index(end,a+len(start)); return text[a:b]

def count_md_table_rows(block:str)->int:
    return sum(1 for ln in block.splitlines() if re.match(r'^\|\s*\d+\s*\|',ln))

def norm_ws(v:str)->str:
    return ' '.join(str(v or '').split())


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--markdown',required=True); ap.add_argument('--docx',required=True); ap.add_argument('--pdf',required=True)
    ap.add_argument('--visual-pages-pass',type=int,default=0)
    args=ap.parse_args()
    mdp,dxp,pdfp=map(Path,[args.markdown,args.docx,args.pdf])
    md=mdp.read_text(encoding='utf-8'); vm=visible_md(md); dx=extract_docx_text(dxp); pf,pages=extract_pdf(pdfp)
    visible={'markdown_visible':vm,'docx_visible':dx,'pdf_visible':pf}
    latin={k:sorted(set(LATIN.findall(v))) for k,v in visible.items()}
    forbidden_latin={k:sorted(set(v)-SOURCE_NATIVE_LATIN) for k,v in latin.items()}
    process_hits={k:[p for p in FORBIDDEN_PROCESS if p.casefold() in v.casefold()] for k,v in visible.items()}
    framing_hits={k:[p for p in FORBIDDEN_CLIENT_FRAMING if p.casefold() in v.casefold()] for k,v in visible.items()}

    summary_block=section(md,'## Краткий вывод','## 1. Что на сайте уже работает правильно')
    ready_block=section(md,'## 2. Семь приоритетных улучшений существующих страниц','## 3. Что уточнить у компании для двух следующих улучшений')
    business_block=section(md,'## 3. Что уточнить у компании для двух следующих улучшений','## 4. Как распределены основные группы поискового спроса')
    family_block=section(md,'## 4. Как распределены основные группы поискового спроса','## 5. Дополнительная проверка восьми важных тем')
    assistant_block=section(md,'## 5. Дополнительная проверка восьми важных тем','## 6. Что передать в работу в первую очередь')
    priority_block=section(md,'## 6. Что передать в работу в первую очередь','## 7. Что было проверено')
    obs_block=section(md,'## Приложение 1. Что показала выдача Яндекса по 75 конкретным запросам','## Приложение 2. Сводная карта результатов исследования')
    action_block=section(md,'## Приложение 2. Сводная карта результатов исследования','## Границы применения выводов')

    obs_rows={}
    for ln in obs_block.splitlines():
        m=re.match(r'^\|\s*(\d+)\s*\|\s*(.*?)\s*\|',ln)
        if m: obs_rows[int(m.group(1))]=m.group(2).strip()
    brand_query_spelling_ok=all(obs_rows.get(n)==q for n,q in EXPECTED_BRAND_QUERY_ROWS.items())
    brand_prose_preserved=all(x in vm and x in dx and x in pf for x in EXPECTED_BRAND_PROSE)

    ready_cards=[x for x in ready_block.split('\n### ') if x.strip() and not x.startswith('## 2.')]
    ready_heading_count=sum(1 for x in ready_block.splitlines() if x.startswith('### '))
    label_counts={label:ready_block.count(label) for label in CARD_LABELS}
    ready_labels_complete=ready_heading_count==7 and all(c==7 for c in label_counts.values())

    counts={
        'ready_recommendations':ready_heading_count,
        'business_inputs':sum(1 for x in business_block.splitlines() if x.startswith('### ')),
        'demand_groups':sum(1 for x in family_block.splitlines() if x.startswith('### ')),
        'assistant_cases':sum(1 for x in assistant_block.splitlines() if x.startswith('### ')),
        'observations':count_md_table_rows(obs_block),
        'results':count_md_table_rows(action_block),
    }

    heading_presence={h:all(norm_ws(h) in norm_ws(v) for v in visible.values()) for h in REQUIRED_HEADINGS}
    internal_ascii=[]
    for pattern in [r'S18-A\d+',r'QF\d+',r'SP09',r'C15-',r'STAGE',r'STEP',r'READY',r'HOLD',r'AI\b',r'CMS\b',r'URL\b']:
        if re.search(pattern,vm,re.I): internal_ascii.append(pattern)

    summary_forbidden=[p for p in ['частично','запрещ','спорн','аналитическ','неопредел','ничего не','не создавать новые страницы','не перестраивать'] if p in summary_block.casefold()]
    priority_negative=[p for p in ['не создавать','не объединять','не удалять','не внедрять','ничего не делать','запрещ'] if p in priority_block.casefold()]
    why_specific=ready_block.count('Почему это важно:')==7
    owner_first_order=(md.index('## 1. Что на сайте уже работает правильно') < md.index('## 7. Что было проверено') and md.index('## 2. Семь приоритетных улучшений существующих страниц') < md.index('## 7. Что было проверено'))
    assistant_negative=[p for p in ['Новая страница не нужна','Изменения не требуются','Доказательств недостаточно','не дал оснований создавать новое действие','не доказан','не нужно','нельзя расширять','не доказал новую иерархию'] if p.casefold() in assistant_block.casefold()]

    checks={
        'forbidden_internal_latin_zero':all(not x for x in forbidden_latin.values()),
        'source_native_latin_preserved':brand_prose_preserved,
        'verbatim_brand_query_spelling_preserved':brand_query_spelling_ok,
        'process_narrative_zero':all(not x for x in process_hits.values()),
        'owner_value_framing_forbidden_zero':all(not x for x in framing_hits.values()),
        'internal_ascii_markers_zero':not internal_ascii,
        'required_headings_all_three':all(heading_presence.values()),
        'ready_recommendations_7':counts['ready_recommendations']==7,
        'ready_cards_have_why_and_full_chain':ready_labels_complete and why_specific,
        'business_inputs_2':counts['business_inputs']==2,
        'demand_groups_21':counts['demand_groups']==21,
        'assistant_cases_8':counts['assistant_cases']==8,
        'observations_75':counts['observations']==75,
        'results_34':counts['results']==34,
        'executive_summary_not_uncertainty_led':not summary_forbidden,
        'priority_plan_has_no_negative_pseudo_actions':not priority_negative,
        'owner_value_sections_precede_methodology':owner_first_order,
        'assistant_cases_use_positive_client_framing':not assistant_negative,
        'pdf_pages_nonzero':pages>0,
        'visual_all_pages_pass':args.visual_pages_pass==pages and pages>0,
    }
    result={
        'status':'PASS' if all(checks.values()) else 'FAIL',
        'checks':checks,'counts':counts,'pdf_pages':pages,
        'card_label_counts':label_counts,
        'source_native_latin_tokens':latin,
        'forbidden_internal_latin_tokens':forbidden_latin,
        'forbidden_process_hits':process_hits,
        'forbidden_client_framing_hits':framing_hits,
        'internal_ascii_markers':internal_ascii,
        'executive_summary_forbidden_hits':summary_forbidden,
        'priority_negative_pseudo_action_hits':priority_negative,
        'assistant_negative_framing_hits':assistant_negative,
        'brand_query_spelling_rows':{str(k):obs_rows.get(k) for k in EXPECTED_BRAND_QUERY_ROWS},
        'required_heading_presence_all_three':heading_presence,
        'sha256':{'markdown':sha256(mdp),'docx':sha256(dxp),'pdf':sha256(pdfp)},
        'size_bytes':{'markdown':mdp.stat().st_size,'docx':dxp.stat().st_size,'pdf':pdfp.stat().st_size},
    }
    print(json.dumps(result,ensure_ascii=False,indent=2))
    raise SystemExit(0 if result['status']=='PASS' else 1)

if __name__=='__main__': main()
