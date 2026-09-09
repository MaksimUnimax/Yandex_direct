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


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def add_page_break_before_competitor_table():
    doc = Document(DOCX)
    target = None
    for table in doc.tables:
        if table.rows and table.rows[0].cells and table.rows[0].cells[0].text.strip() == 'Конкурент':
            target = table
            break
    assert target is not None, 'competitor table not found'

    prev = target._tbl.getprevious()
    already = False
    if prev is not None and prev.tag == qn('w:p'):
        pPr = prev.find(qn('w:pPr'))
        already = pPr is not None and pPr.find(qn('w:pageBreakBefore')) is not None
    if not already:
        p = OxmlElement('w:p')
        pPr = OxmlElement('w:pPr')
        pb = OxmlElement('w:pageBreakBefore')
        pPr.append(pb)
        p.append(pPr)
        target._tbl.addprevious(p)
        doc.save(DOCX)


def rebuild_pdf():
    if PDF.exists():
        PDF.unlink()
    subprocess.run(['libreoffice','--headless','--convert-to','pdf','--outdir',str(REL),str(DOCX)], check=True)
    assert PDF.exists() and PDF.stat().st_size > 10000


def verify_pdf():
    reader = PdfReader(str(PDF))
    texts = [(p.extract_text() or '') for p in reader.pages]
    joined = '\n'.join(texts)
    assert len(texts) >= 8
    for c in COMPETITORS:
        assert c in joined, c
    # The competitor table must no longer be split between page 1 and page 2.
    assert 'mosokna.ru' not in texts[0], 'competitor table still starts on page 1'
    assert all(c in texts[1] for c in COMPETITORS), 'competitor table does not stay together on page 2'
    assert '44' in texts[1]
    return len(texts), texts


def refresh_manifest():
    data = json.loads(MANIFEST.read_text(encoding='utf-8'))
    targets = {
        '01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-09.pdf': PDF,
        'editable/01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-09.docx': DOCX,
        'sources/01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-09.md': SRC,
    }
    seen = set()
    for item in data['artifacts']:
        if item['path'] in targets:
            p = targets[item['path']]
            item['bytes'] = p.stat().st_size
            item['sha256'] = sha256(p)
            seen.add(item['path'])
    assert seen == set(targets)
    data['report01_visual_competitor_table_together'] = True
    MANIFEST.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')


def write_qa(pages):
    result = {
        'schema': 'OKNO_MSK_DOCUMENT01_STEP05A_COMPETITOR_VISUAL_QA_V1',
        'date': '2026-09-09',
        'status': 'PASS',
        'pdf_pages': pages,
        'competitor_table_starts_page': 2,
        'competitor_table_all_9_same_page': True,
        'source_sha256': sha256(SRC),
        'docx_sha256': sha256(DOCX),
        'pdf_sha256': sha256(PDF),
        'manifest_sha256': sha256(MANIFEST),
    }
    QA.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))


def main():
    source_before = sha256(SRC)
    add_page_break_before_competitor_table()
    rebuild_pdf()
    pages, _ = verify_pdf()
    assert sha256(SRC) == source_before, 'source changed during visual polish'
    refresh_manifest()
    write_qa(pages)


if __name__ == '__main__':
    main()
