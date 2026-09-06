from pathlib import Path
import re, hashlib
from docx import Document
from docx.shared import Cm, Pt
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.enum.style import WD_STYLE_TYPE

ROOT = Path(__file__).resolve().parent
REL = ROOT / 'OKNO_MSK_RESEARCH_RELEASE_CORRECTED_2026-09-05'
SRC = REL / 'sources/01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-05.md'
DOCX = REL / 'editable/01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-05.docx'
TITLE = 'ОКНО МОСКВА — https://okno-msk.ru/ — исследование спроса в Яндексе: обычная выдача и выдача Алисы'


def sha256(path):
    h = hashlib.sha256(); h.update(path.read_bytes()); return h.hexdigest()


def set_cell_shading(cell, fill):
    tcPr = cell._tc.get_or_add_tcPr(); shd = tcPr.find(qn('w:shd'))
    if shd is None:
        shd = OxmlElement('w:shd'); tcPr.append(shd)
    shd.set(qn('w:fill'), fill)


def set_cell_margins(cell, top=90, start=90, bottom=90, end=90):
    tcPr = cell._tc.get_or_add_tcPr(); tcMar = tcPr.first_child_found_in('w:tcMar')
    if tcMar is None:
        tcMar = OxmlElement('w:tcMar'); tcPr.append(tcMar)
    for m, v in [('top', top), ('start', start), ('bottom', bottom), ('end', end)]:
        node = tcMar.find(qn(f'w:{m}'))
        if node is None:
            node = OxmlElement(f'w:{m}'); tcMar.append(node)
        node.set(qn('w:w'), str(v)); node.set(qn('w:type'), 'dxa')


def set_cant_split(row):
    trPr = row._tr.get_or_add_trPr(); trPr.append(OxmlElement('w:cantSplit'))


def add_page_number(p):
    p.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    r = p.add_run('Страница '); r.font.name = 'Liberation Sans'; r.font.size = Pt(8)
    a = OxmlElement('w:fldChar'); a.set(qn('w:fldCharType'), 'begin')
    b = OxmlElement('w:instrText'); b.set(qn('xml:space'), 'preserve'); b.text = ' PAGE '
    c = OxmlElement('w:fldChar'); c.set(qn('w:fldCharType'), 'end')
    r._r.append(a); r._r.append(b); r._r.append(c)


def add_runs(p, s):
    for part in re.split(r'(\*\*.*?\*\*)', s):
        if not part:
            continue
        if part.startswith('**') and part.endswith('**'):
            r = p.add_run(part[2:-2]); r.bold = True
        else:
            r = p.add_run(part)
        r.font.name = 'Liberation Sans'


def build_docx():
    text = SRC.read_text(encoding='utf-8'); lines = text.splitlines()
    assert lines[0] == '# ' + TITLE

    forbidden = [
        'генеративный', 'нейросетевой', 'Алиса/ИИ', '`count`', 'исходных строк',
        '## Приложение.', 'Полный список 75 проверенных', 'Главное за одну минуту',
        'Как использовать результаты', 'полный объём этого этапа', 'для владельца сайта',
        'владельцу сайта', 'владелец бизнеса', 'После пересборки ядра',
        'В работе пересобрано поисковое ядро', 'Задача работы — пересобрать поисковое ядро',
        'Специализированная страница панорамного остекления балкона соответствует спросу',
        'Общая страница веранды и раздел алюминиевых окон выполняют разные роли',
        'Страница замены окна и общая страница монтажа'
    ]
    low = text.lower()
    for bad in forbidden:
        assert bad.lower() not in low, bad

    required = [
        'https://okno-msk.ru/',
        'Задача работы — собрать и проверить поисковое ядро сайта для Москвы',
        'уже хорошо оптимизирован под выявленный спрос как в обычной выдаче Яндекса, так и в выдаче Алисы',
        '2 415 поисковых фраз', 'ещё 550 фраз', '2 965 поисковых фраз',
        'числовой показатель спроса', 'частотность в широком соответствии',
        '2 840 уникальных поисковых фраз', '2 332 активные поисковые фразы',
        '2 313', '19', '168 групп поискового спроса', '75', '25 тем',
        'полностью проверили 8', 'шесть тем', 'два контрольных запроса', '16 тем',
        '34 значимых вывода', 'полностью пересобирать существующее распределение ядра по сайту не требуется',
        '## Что дала проверка выдачи Алисы'
    ]
    for marker in required:
        assert marker in text, marker

    assert text.count('**Почему это важно:**') == 7
    assert text.count('**Что рекомендуется сделать:**') == 7
    assert len(re.findall(r'^\|\s*\d+\s*\|', text, re.M)) == 0

    alice_queries = [
        'панорамные алюминиевые окна', 'алюминиевые окна для веранды', 'панорамное остекление балкона',
        'установка подоконника на пластиковые окна', 'французские панорамные окна',
        'замена окна на пластиковое цена москва', 'как открыть пластиковое окно', 'лучшие пластиковые окна'
    ]
    for q in alice_queries:
        assert f'| {q} |' in text, q

    DOCX.parent.mkdir(parents=True, exist_ok=True)
    doc = Document(); sec = doc.sections[0]
    sec.page_width = Cm(21); sec.page_height = Cm(29.7)
    sec.top_margin = Cm(1.65); sec.bottom_margin = Cm(1.55)
    sec.left_margin = Cm(1.8); sec.right_margin = Cm(1.8)
    sec.header_distance = Cm(.7); sec.footer_distance = Cm(.7)

    styles = doc.styles
    normal = styles['Normal']; normal.font.name = 'Liberation Sans'; normal.font.size = Pt(10.4)
    normal.paragraph_format.space_after = Pt(6); normal.paragraph_format.line_spacing = 1.08
    for name, size, before, after in [('Title', 18.5, 0, 12), ('Heading 1', 15.5, 14, 7), ('Heading 2', 12.5, 11, 5), ('Heading 3', 11.2, 9, 4)]:
        st = styles[name]; st.font.name = 'Liberation Sans'; st.font.size = Pt(size); st.font.bold = True
        st.paragraph_format.space_before = Pt(before); st.paragraph_format.space_after = Pt(after); st.paragraph_format.keep_with_next = True
    if 'Callout' not in styles:
        s = styles.add_style('Callout', WD_STYLE_TYPE.PARAGRAPH); s.font.name = 'Liberation Sans'; s.font.size = Pt(10.2)
        s.paragraph_format.left_indent = Cm(.35); s.paragraph_format.right_indent = Cm(.35); s.paragraph_format.space_before = Pt(5); s.paragraph_format.space_after = Pt(7)

    hp = sec.header.paragraphs[0]; hp.text = 'ОКНО МОСКВА · обычная выдача Яндекса и выдача Алисы'; hp.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    for r in hp.runs:
        r.font.name = 'Liberation Sans'; r.font.size = Pt(7.5)
    add_page_number(sec.footer.paragraphs[0])

    i = 0
    while i < len(lines):
        line = lines[i]
        if not line.strip():
            i += 1; continue
        if line.startswith('# '):
            p = doc.add_paragraph(style='Title'); p.add_run(line[2:]); i += 1; continue
        if line.startswith('## '):
            doc.add_paragraph(line[3:], style='Heading 1'); i += 1; continue
        if line.startswith('### '):
            doc.add_paragraph(line[4:], style='Heading 2'); i += 1; continue
        if line.startswith('|'):
            tls = []
            while i < len(lines) and (lines[i].startswith('|') or not lines[i].strip()):
                if lines[i].startswith('|'):
                    tls.append(lines[i])
                i += 1
            rows = []
            for tl in tls:
                cols = [c.strip() for c in tl.strip().strip('|').split('|')]
                if all(set(c) <= set('-: ') for c in cols):
                    continue
                rows.append(cols)
            if not rows:
                continue
            assert len(rows[0]) == 4 and rows[0][0] == 'Запрос', rows[0]
            for row in rows[1:]:
                t = doc.add_table(rows=1, cols=1); t.alignment = WD_TABLE_ALIGNMENT.CENTER; set_cant_split(t.rows[0])
                c = t.cell(0, 0); set_cell_shading(c, 'F2F4F6'); set_cell_margins(c, 140, 150, 140, 150)
                p = c.paragraphs[0]; rr = p.add_run(row[0]); rr.bold = True; rr.font.name = 'Liberation Sans'; rr.font.size = Pt(10.6)
                for label, val in [('Почему выбрали', row[1]), ('Что показала проверка выдачи Алисы', row[2]), ('Что это значит для сайта', row[3])]:
                    pp = c.add_paragraph(); pp.paragraph_format.space_after = Pt(2); pp.paragraph_format.keep_together = True
                    a = pp.add_run(label + ': '); a.bold = True; a.font.name = 'Liberation Sans'; a.font.size = Pt(9.2)
                    b = pp.add_run(val); b.font.name = 'Liberation Sans'; b.font.size = Pt(9.2)
                doc.add_paragraph().paragraph_format.space_after = Pt(1)
            continue
        if line.startswith('- '):
            p = doc.add_paragraph(style='Normal'); p.paragraph_format.left_indent = Cm(.45); p.paragraph_format.first_line_indent = Cm(-.25); p.paragraph_format.space_after = Pt(3)
            p.add_run('• '); add_runs(p, line[2:]); i += 1; continue
        if re.match(r'^\d+\. ', line):
            m = re.match(r'^(\d+)\. (.*)', line); p = doc.add_paragraph(style='Normal')
            p.paragraph_format.left_indent = Cm(.5); p.paragraph_format.first_line_indent = Cm(-.32); p.paragraph_format.space_after = Pt(3)
            r = p.add_run(m.group(1) + '. '); r.bold = True; r.font.name = 'Liberation Sans'; add_runs(p, m.group(2)); i += 1; continue

        para = [line]; i += 1
        while i < len(lines) and lines[i].strip() and not lines[i].startswith(('#', '|', '- ')) and not re.match(r'^\d+\. ', lines[i]):
            para.append(lines[i]); i += 1
        s = ' '.join(x.strip() for x in para); p = doc.add_paragraph(style='Normal')
        if s.startswith('**Сайт →'):
            p.style = 'Callout'
            pPr = p._p.get_or_add_pPr(); shd = OxmlElement('w:shd'); shd.set(qn('w:fill'), 'F2F4F6'); pPr.append(shd)
        add_runs(p, s)

    props = doc.core_properties
    props.title = TITLE; props.author = ''; props.last_modified_by = ''; props.subject = 'Исследовательский отчёт для заказчика'; props.comments = ''
    doc.save(DOCX)


if __name__ == '__main__':
    build_docx()
    print('DOCUMENT_01_COMMISSIONER_DOCX_BUILD_PASS', DOCX, sha256(DOCX))
