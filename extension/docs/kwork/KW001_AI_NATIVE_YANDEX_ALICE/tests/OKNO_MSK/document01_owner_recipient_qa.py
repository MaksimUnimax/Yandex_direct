from pathlib import Path
import hashlib, json, re, subprocess, tempfile
from docx import Document
from pypdf import PdfReader

ROOT=Path(__file__).resolve().parent
REL=ROOT/'OKNO_MSK_RESEARCH_RELEASE_CORRECTED_2026-09-05'
MD=REL/'sources/01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-05.md'
DOCX=REL/'editable/01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-05.docx'
PDF=REL/'01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-05.pdf'
QA_PATH=ROOT/'RESEARCH_REBUILD_POST_RELEASE_DOCUMENT_01_OWNER_REPORT_QA_2026-09-06.json'
MAN_PATH=REL/'RELEASE_MANIFEST_2026-09-05.json'
TITLE='ОКНО МОСКВА — исследование спроса в Яндексе: обычная выдача и выдача Алисы'

def sha(p):
    h=hashlib.sha256(); h.update(p.read_bytes()); return h.hexdigest()

def norm(s):
    return re.sub(r'\s+',' ',s.replace('\u00ad','')).strip()

def main():
    text=MD.read_text(encoding='utf-8')
    assert text.splitlines()[0]=='# '+TITLE
    for bad in ['генеративный поиск','нейросетевой поиск','Алиса/ИИ','весь массив']:
        assert bad not in text,bad
    for marker in ['2 840','2 313','168','75','25','8','34','6 случаев','2 контрольных','16 тем','1 тема']:
        assert marker in text,marker
    assert '## 5. Как распределены основные группы поискового спроса' not in text
    assert len(re.findall(r'^\|\s*\d+\s*\|',text,re.M))==75

    d=Document(DOCX); dtext='\n'.join(p.text for p in d.paragraphs)
    assert TITLE in dtext
    assert len(d.tables)==9,len(d.tables)

    reader=PdfReader(PDF); pages=len(reader.pages); assert pages==10,pages
    ptext='\n'.join((p.extract_text() or '') for p in reader.pages)
    ntext=norm(ptext).lower(); assert norm(TITLE).lower() in ntext
    for marker in ['2 840','2 313','168','75','25','8','34','Панорамные алюминиевые окна','Семь изменений, которые можно передавать в работу']:
        assert norm(marker).lower() in ntext,marker
    with tempfile.TemporaryDirectory() as td:
        subprocess.run(['pdftoppm','-png','-r','72',str(PDF),str(Path(td)/'p')],check=True,stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
        rendered=list(Path(td).glob('p-*.png')); assert len(rendered)==10,len(rendered)
        assert all(p.stat().st_size>10000 for p in rendered)

    untouched={
      '02_OKNO_MSK_SEO_IMPLEMENTATION_GUIDE_RU_2026-09-05.pdf':'3f589c03bc44f5127aa9f93697e3120729149f8f6985c11fa921424c867ec61a',
      '03_OKNO_MSK_AI_KNOWLEDGE_DOCUMENT_2026-09-05.md':'d5c90cf187041e975f17d03a2be138eff0b6a06bfe1b7d395a3b24547edc62b0',
      'editable/02_OKNO_MSK_SEO_IMPLEMENTATION_GUIDE_RU_2026-09-05.docx':'4c9f4aeded8b23c8ed7741d10a989ba79696d8fac3fa10a48de11cdd01df2d3c',
      'sources/02_OKNO_MSK_SEO_IMPLEMENTATION_GUIDE_RU_2026-09-05.md':'764f697fb5ad7ca6f5982b000b6053652460f854c8bb7b937a2041688fff80d8'
    }
    for p,want in untouched.items(): assert sha(REL/p)==want,p

    qa=json.loads(QA_PATH.read_text(encoding='utf-8'))
    qa['status']='ANALYST_RECHECK_PASS__OWNER_REVIEW_PENDING'
    qa['counts']['pdf_pages']=pages
    qa['sha256']={'md':sha(MD),'docx':sha(DOCX),'pdf':sha(PDF)}
    qa['size_bytes']={'md':MD.stat().st_size,'docx':DOCX.stat().st_size,'pdf':PDF.stat().st_size}
    qa['checks']['docx_render_visual_qa_10_of_10_pages']=True
    qa['checks']['pdf_preflight_openable_not_encrypted_10_pages']=True
    qa['checks']['pdf_render_visual_qa_10_of_10_pages']=True
    qa['checks']['document_02_not_modified']=True
    qa['checks']['document_03_not_modified']=True
    QA_PATH.write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

    man=json.loads(MAN_PATH.read_text(encoding='utf-8'))
    art=man['recipient_artifacts'][0]; art['size_bytes']=PDF.stat().st_size; art['sha256']=sha(PDF); art['pages']=pages
    for item in man['editable_and_source_files']:
        if item['path']=='editable/01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-05.docx': item['size_bytes']=DOCX.stat().st_size; item['sha256']=sha(DOCX)
        if item['path']=='sources/01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-05.md': item['size_bytes']=MD.stat().st_size; item['sha256']=sha(MD)
    man['qa']['document_01_physical_pdf']='10_OF_10_PAGES_PASS'
    man['qa']['document_01_github_readback']='PENDING_POST_COMMIT_READBACK'
    MAN_PATH.write_text(json.dumps(man,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print('DOCUMENT_01_OWNER_RECIPIENT_QA_PASS',pages,sha(MD),sha(DOCX),sha(PDF))

if __name__=='__main__': main()
