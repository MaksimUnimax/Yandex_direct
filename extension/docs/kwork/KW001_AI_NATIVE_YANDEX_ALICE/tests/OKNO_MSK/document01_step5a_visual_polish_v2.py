from pathlib import Path
import hashlib, json, subprocess
from docx import Document
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
REL = ROOT / 'OKNO_MSK_RESEARCH_RELEASE_STEP05A_PROPAGATED_2026-09-09'
SRC = REL / 'sources/01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-09.md'
DOCX = REL / 'editable/01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-09.docx'
PDF = REL / '01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-09.pdf'
MANIFEST = REL / 'RELEASE_MANIFEST_2026-09-09.json'
QA = ROOT / 'DOCUMENT_01_STEP05A_COMPETITOR_VISUAL_QA_2026-09-09.json'
COMPETITORS = ['mosokna.ru','i-okna.ru','msk.okna-servise.com','okna-moskva.ru','oknafactoria.ru','okna-germany.ru','fabrikaokon.ru','aluminarium.ru','elit-balkon.ru']


def sha256(path): return hashlib.sha256(path.read_bytes()).hexdigest()


def polish_table():
    doc = Document(DOCX)
    target = next((t for t in doc.tables if t.rows and t.rows[0].cells[0].text.strip() == 'Конкурент'), None)
    assert target is not None
    prev = target._tbl.getprevious()
    if prev is not None and prev.tag == qn('w:p'):
        pPr = prev.find(qn('w:pPr'))
        if pPr is not None and pPr.find(qn('w:pageBreakBefore')) is not None:
            target._tbl.getparent().remove(prev)
    trPr = target.rows[0]._tr.get_or_add_trPr()
    for old in list(trPr.findall(qn('w:tblHeader'))): trPr.remove(old)
    h = OxmlElement('w:tblHeader'); h.set(qn('w:val'),'true'); trPr.append(h)
    doc.save(DOCX)


def rebuild_pdf():
    if PDF.exists(): PDF.unlink()
    subprocess.run(['libreoffice','--headless','--convert-to','pdf','--outdir',str(REL),str(DOCX)], check=True)
    assert PDF.exists() and PDF.stat().st_size > 10000


def verify_pdf():
    r=PdfReader(str(PDF)); texts=[p.extract_text() or '' for p in r.pages]; joined='\n'.join(texts)
    assert len(texts) == 8, len(texts)
    for c in COMPETITORS: assert c in joined, c
    assert 'mosokna.ru' in texts[0]
    assert 'Конкурент' in texts[1] and 'Проверено страниц' in texts[1]
    assert 'aluminarium.ru' in texts[1] and 'elit-balkon.ru' in texts[1] and '44' in texts[1]
    return len(texts)


def refresh_manifest():
    data=json.loads(MANIFEST.read_text(encoding='utf-8'))
    targets={'01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-09.pdf':PDF,'editable/01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-09.docx':DOCX,'sources/01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-09.md':SRC}
    seen=set()
    for item in data['artifacts']:
        if item['path'] in targets:
            p=targets[item['path']]; item['bytes']=p.stat().st_size; item['sha256']=sha256(p); seen.add(item['path'])
    assert seen==set(targets)
    data.pop('report01_visual_competitor_table_together',None)
    data['report01_visual_competitor_table_repeat_header']=True
    MANIFEST.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')


def write_qa(pages):
    result={'schema':'OKNO_MSK_DOCUMENT01_STEP05A_COMPETITOR_VISUAL_QA_V2','date':'2026-09-09','status':'PASS','pdf_pages':pages,'competitor_table_natural_split':True,'competitor_table_header_repeated_on_page_2':True,'no_sparse_trailing_page':True,'source_sha256':sha256(SRC),'docx_sha256':sha256(DOCX),'pdf_sha256':sha256(PDF),'manifest_sha256':sha256(MANIFEST)}
    QA.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8'); print(json.dumps(result,ensure_ascii=False,indent=2))


def main():
    source_before=sha256(SRC); polish_table(); rebuild_pdf(); pages=verify_pdf(); assert sha256(SRC)==source_before; refresh_manifest(); write_qa(pages)

if __name__=='__main__': main()
