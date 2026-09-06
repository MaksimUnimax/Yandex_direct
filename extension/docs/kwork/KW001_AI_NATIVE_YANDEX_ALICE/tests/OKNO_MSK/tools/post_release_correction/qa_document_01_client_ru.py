#!/usr/bin/env python3
from __future__ import annotations
import argparse, hashlib, json, re, subprocess, tempfile, zipfile
from pathlib import Path

LATIN = re.compile(r'[A-Za-z]+')
SOURCE_NATIVE_LATIN = {'REHAU','rehau','Provedal','provedal','KBE','kbe','Accado','Vorne','Futurus','fapim','Thermo','thermo'}

EXPECTED_BRAND_QUERY_ROWS = {
    2:'алюминиевые окна fapim',
    12:'окна rehau 70',
    13:'окна rehau kbe',
    14:'окна rehau официальный',
    15:'окна rehau провисли',
    17:'окна стеклопакеты rehau',
    41:'provedal остекление веранды',
    42:'алюминиевые окна provedal',
    43:'алюминиевые окна проведал',
    44:'окна rehau в рассрочку',
    45:'окна рехау в рассрочку',
    46:'оконная фурнитура rehau',
    47:'оконная фурнитура рехау',
    48:'пластиковые окна rehau',
    49:'пластиковые окна от производителя rehau',
    50:'пластиковые окна рехау',
    51:'пластиковые окна рехау от производителя',
    53:'проведал остекление веранды',
    57:'rehau thermo окна',
    60:'какой профиль rehau выбрать',
    61:'окна rehau москва',
}
EXPECTED_BRAND_PROSE = ['REHAU','Provedal','KBE','Accado','Vorne','Futurus']

FORBIDDEN_PROCESS = [
    'гитхаб', 'коммит', 'чекпоинт', 'генератор', 'проверка отчёта',
    'пересборк', 'исправленный выпуск', 'внутренних файлов проекта',
    'вызовы при исправлении', 'история исправления', 'служебная трасса',
]
KEY_PHRASES = [
    'Семь изменений, которые можно внедрять',
    'Одна частично готовая работа',
    'Четыре вопроса, где изменения пока запрещены',
    'Двадцать одно спорное семейство запросов',
    'Восемь проверок поискового помощника',
    'Все 75 сохранённых наблюдений обычного Яндекса',
    'Полная карта 34 решений',
    'Неопределённость и условия повторного открытия',
    'Приоритет действий владельца',
]

def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()

def visible_md(text: str) -> str:
    text = re.sub(r'\]\([^)]*\)', ']', text)
    text = re.sub(r'[`#*|\[\]]', ' ', text)
    return text

def extract_docx_text(path: Path) -> str:
    with zipfile.ZipFile(path) as z:
        xml='\n'.join(z.read(n).decode('utf-8','ignore') for n in z.namelist()
                      if n.endswith('.xml') and ('document.xml' in n or 'header' in n or 'footer' in n))
    vals=re.findall(r'<w:t(?:\s[^>]*)?>(.*?)</w:t>', xml)
    return ' '.join(vals)

def extract_pdf(path: Path) -> tuple[str,int]:
    # Prefer pypdf, fall back to pdftotext/pdfinfo.
    try:
        from pypdf import PdfReader
        reader=PdfReader(str(path))
        return '\n'.join((p.extract_text() or '') for p in reader.pages), len(reader.pages)
    except Exception:
        with tempfile.TemporaryDirectory() as td:
            out=Path(td)/'x.txt'
            subprocess.run(['pdftotext', str(path), str(out)], check=True)
            text=out.read_text(encoding='utf-8', errors='ignore')
            info=subprocess.check_output(['pdfinfo', str(path)], text=True, encoding='utf-8', errors='ignore')
            m=re.search(r'^Pages:\s*(\d+)', info, re.M)
            return text, int(m.group(1)) if m else 0

def section(text: str, start: str, end: str) -> str:
    a=text.index(start)
    b=text.index(end, a+len(start))
    return text[a:b]

def count_md_table_rows(block: str) -> int:
    return sum(1 for ln in block.splitlines() if re.match(r'^\|\s*\d+\s*\|', ln))

def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--markdown', required=True)
    ap.add_argument('--docx', required=True)
    ap.add_argument('--pdf', required=True)
    ap.add_argument('--visual-pages-pass', type=int, default=0)
    args=ap.parse_args()
    mdp, dxp, pdfp = map(Path, [args.markdown,args.docx,args.pdf])
    md=mdp.read_text(encoding='utf-8')
    vm=visible_md(md)
    dx=extract_docx_text(dxp)
    pf,pages=extract_pdf(pdfp)

    latin={
        'markdown_visible': sorted(set(LATIN.findall(vm))),
        'docx_visible': sorted(set(LATIN.findall(dx))),
        'pdf_visible': sorted(set(LATIN.findall(pf))),
    }
    forbidden_latin={k: sorted(set(v)-SOURCE_NATIVE_LATIN) for k,v in latin.items()}
    forbidden={k: [p for p in FORBIDDEN_PROCESS if p in v.casefold()] for k,v in
               [('markdown_visible',vm),('docx_visible',dx),('pdf_visible',pf)]}
    family_block=section(md,'## 7. Двадцать одно спорное семейство запросов','## 8. Восемь проверок поискового помощника')
    assistant_block=section(md,'## 8. Восемь проверок поискового помощника','## 9. Все 75 сохранённых наблюдений обычного Яндекса')
    obs_block=section(md,'## 9. Все 75 сохранённых наблюдений обычного Яндекса','## 10. Полная карта 34 решений')
    action_block=section(md,'## 10. Полная карта 34 решений','## 11. Неопределённость и условия повторного открытия')
    # Independent regression check: exact evidence rows with Latin/source-native brand spellings
    # must stay byte-for-byte in the client table. This prevents "Russian-only" cleanup
    # from silently rewriting real brands or exact query strings.
    obs_rows={}
    for ln in obs_block.splitlines():
        m=re.match(r'^\|\s*(\d+)\s*\|\s*(.*?)\s*\|', ln)
        if m:
            obs_rows[int(m.group(1))]=m.group(2).strip()
    brand_query_spelling_ok=all(obs_rows.get(n)==q for n,q in EXPECTED_BRAND_QUERY_ROWS.items())
    brand_prose_preserved=all(x in vm and x in dx and x in pf for x in EXPECTED_BRAND_PROSE)
    counts={
        'families': sum(1 for x in family_block.splitlines() if x.startswith('### ')),
        'assistant_cases': sum(1 for x in assistant_block.splitlines() if x.startswith('### ')),
        'observations': count_md_table_rows(obs_block),
        'actions': count_md_table_rows(action_block),
    }
    def norm_ws(value: str) -> str:
        # Layout engines may insert line/page breaks inside a visible heading.
        # Compare recipient-visible heading text after whitespace normalization only;
        # do not relax or rewrite the actual required wording.
        return ' '.join(str(value or '').split())

    visible_norm=[norm_ws(vm), norm_ws(dx), norm_ws(pf)]
    key_presence={q: all(norm_ws(q) in t for t in visible_norm) for q in KEY_PHRASES}
    internal_ascii_markers=[]
    for pattern in [r'S18-A\d+',r'QF\d+',r'SP09',r'C15-',r'STAGE',r'STEP',r'READY',r'HOLD',r'AI\b',r'CMS\b',r'URL\b']:
        if re.search(pattern, vm, re.I): internal_ascii_markers.append(pattern)
    checks={
        'forbidden_internal_latin_zero': all(not x for x in forbidden_latin.values()),
        'source_native_latin_preserved': brand_prose_preserved,
        'verbatim_brand_query_spelling_preserved': brand_query_spelling_ok,
        'process_narrative_zero': all(not x for x in forbidden.values()),
        'internal_ascii_markers_zero': not internal_ascii_markers,
        'families_21': counts['families']==21,
        'assistant_cases_8': counts['assistant_cases']==8,
        'observations_75': counts['observations']==75,
        'actions_34': counts['actions']==34,
        'key_sections_equivalent': all(key_presence.values()),
        'pdf_pages_nonzero': pages>0,
        'visual_all_pages_pass': args.visual_pages_pass==pages and pages>0,
    }
    result={
        'status':'PASS' if all(checks.values()) else 'FAIL',
        'checks':checks,
        'counts':counts,
        'pdf_pages':pages,
        'source_native_latin_tokens':latin,
        'forbidden_internal_latin_tokens':forbidden_latin,
        'forbidden_process_hits':forbidden,
        'internal_ascii_markers':internal_ascii_markers,
        'brand_query_spelling_rows':{str(k):obs_rows.get(k) for k in EXPECTED_BRAND_QUERY_ROWS},
        'key_section_presence_all_three':key_presence,
        'sha256':{'markdown':sha256(mdp),'docx':sha256(dxp),'pdf':sha256(pdfp)},
        'size_bytes':{'markdown':mdp.stat().st_size,'docx':dxp.stat().st_size,'pdf':pdfp.stat().st_size},
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))
    raise SystemExit(0 if result['status']=='PASS' else 1)

if __name__=='__main__': main()
