from pathlib import Path
import re
import argparse
from docx import Document
from docx.shared import Pt, Mm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.section import WD_SECTION
from docx.oxml import OxmlElement
from docx.oxml.ns import qn
from docx.opc.constants import RELATIONSHIP_TYPE as RT

parser = argparse.ArgumentParser(description='Build recipient document 01 from the approved owner-facing Markdown source.')
parser.add_argument('source_md', type=Path)
parser.add_argument('output_docx', type=Path)
args = parser.parse_args()
MD = args.source_md
OUT = args.output_docx
text = MD.read_text(encoding='utf-8')
lines = text.splitlines()

doc = Document()
sec = doc.sections[0]
sec.page_width = Mm(210)
sec.page_height = Mm(297)
sec.top_margin = Mm(17)
sec.bottom_margin = Mm(16)
sec.left_margin = Mm(18)
sec.right_margin = Mm(18)

styles = doc.styles
normal = styles['Normal']
normal.font.name = 'Liberation Sans'
normal.font.size = Pt(10.2)
normal.paragraph_format.space_after = Pt(4)
normal.paragraph_format.line_spacing = 1.08
for sty_name, size in [('Title', 20), ('Heading 1', 15), ('Heading 2', 12.5), ('Heading 3', 11.2)]:
    st = styles[sty_name]
    st.font.name = 'Liberation Sans'
    st.font.size = Pt(size)
    st.font.bold = True
    st.paragraph_format.space_before = Pt(10 if sty_name != 'Title' else 0)
    st.paragraph_format.space_after = Pt(5)
    if sty_name.startswith('Heading'):
        st.paragraph_format.keep_with_next = True

# Custom relationship hyperlink helper.
def add_hyperlink(paragraph, text, url, bold=False):
    part = paragraph.part
    rid = part.relate_to(url, RT.HYPERLINK, is_external=True)
    hyperlink = OxmlElement('w:hyperlink')
    hyperlink.set(qn('r:id'), rid)
    new_run = OxmlElement('w:r')
    rPr = OxmlElement('w:rPr')
    if bold:
        b = OxmlElement('w:b'); rPr.append(b)
    color = OxmlElement('w:color'); color.set(qn('w:val'), '0563C1'); rPr.append(color)
    u = OxmlElement('w:u'); u.set(qn('w:val'), 'single'); rPr.append(u)
    rFonts = OxmlElement('w:rFonts'); rFonts.set(qn('w:ascii'),'Liberation Sans'); rFonts.set(qn('w:hAnsi'),'Liberation Sans'); rPr.append(rFonts)
    new_run.append(rPr)
    t = OxmlElement('w:t'); t.text = text; new_run.append(t)
    hyperlink.append(new_run)
    paragraph._p.append(hyperlink)

inline_re = re.compile(r'(\*\*.*?\*\*|\[[^\]]+\]\([^)]+\))')

def add_inline(paragraph, s):
    pos=0
    for m in inline_re.finditer(s):
        if m.start()>pos:
            r=paragraph.add_run(s[pos:m.start()]); r.font.name='Liberation Sans'; r.font.size=Pt(10.2)
        token=m.group(0)
        if token.startswith('**'):
            r=paragraph.add_run(token[2:-2]); r.bold=True; r.font.name='Liberation Sans'; r.font.size=Pt(10.2)
        else:
            mm=re.match(r'\[([^\]]+)\]\(([^)]+)\)',token)
            add_hyperlink(paragraph, mm.group(1), mm.group(2))
        pos=m.end()
    if pos<len(s):
        r=paragraph.add_run(s[pos:]); r.font.name='Liberation Sans'; r.font.size=Pt(10.2)

# First line title handled specially.
i=0
if lines and lines[0].startswith('# '):
    p=doc.add_paragraph(style='Title')
    p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_after=Pt(7)
    r=p.add_run(lines[0][2:]); r.font.name='Liberation Sans'; r.font.size=Pt(20); r.bold=True
    i=1

# add subtle subtitle for product differentiator after first metadata paragraphs
# Regular parsing follows.
while i < len(lines):
    line = lines[i]
    if not line.strip():
        i += 1
        continue
    # Markdown table
    if line.startswith('|') and i+1 < len(lines) and re.match(r'^\|[-: |]+\|$', lines[i+1].strip()):
        headers=[c.strip() for c in line.strip().strip('|').split('|')]
        i += 2
        rows=[]
        while i < len(lines):
            if not lines[i].strip():
                i += 1
                continue
            if lines[i].startswith('|'):
                rows.append([c.strip() for c in lines[i].strip().strip('|').split('|')])
                i += 1
                continue
            break
        table=doc.add_table(rows=1, cols=len(headers))
        table.alignment=WD_TABLE_ALIGNMENT.CENTER
        table.style='Table Grid'
        hdr_cells=table.rows[0].cells
        for j,h in enumerate(headers):
            hdr_cells[j].text=h
            for p in hdr_cells[j].paragraphs:
                p.paragraph_format.space_after=Pt(0)
                for r in p.runs:
                    r.bold=True; r.font.name='Liberation Sans'; r.font.size=Pt(8.2)
        trPr=table.rows[0]._tr.get_or_add_trPr(); hdr=OxmlElement('w:tblHeader'); hdr.set(qn('w:val'),'true'); trPr.append(hdr)
        for row in rows:
            cells=table.add_row().cells
            for j,val in enumerate(row[:len(headers)]):
                cells[j].text=val
            trPr=cells[0]._tc.getparent().get_or_add_trPr(); cs=OxmlElement('w:cantSplit'); trPr.append(cs)
            for cell in cells:
                cell.vertical_alignment=WD_CELL_VERTICAL_ALIGNMENT.CENTER
                for p in cell.paragraphs:
                    p.paragraph_format.space_after=Pt(0)
                    p.paragraph_format.line_spacing=1.0
                    for r in p.runs:
                        r.font.name='Liberation Sans'; r.font.size=Pt(8.0)
        doc.add_paragraph('').paragraph_format.space_after=Pt(1)
        continue
    if line.startswith('### '):
        p=doc.add_paragraph(line[4:], style='Heading 2')
        p.paragraph_format.keep_with_next=True
        i += 1; continue
    if line.startswith('## '):
        title=line[3:]
        p=doc.add_paragraph(title, style='Heading 1')
        p.paragraph_format.keep_with_next=True
        i += 1; continue
    if line.startswith('- '):
        p=doc.add_paragraph(style='List Bullet')
        add_inline(p,line[2:])
        p.paragraph_format.space_after=Pt(3)
        i += 1; continue
    p=doc.add_paragraph()
    add_inline(p,line)
    p.paragraph_format.space_after=Pt(4)
    i += 1

# Footer
for section in doc.sections:
    p=section.footer.paragraphs[0]
    p.alignment=WD_ALIGN_PARAGRAPH.CENTER
    p.text='Исследование сайта «Окно Москва»'
    for r in p.runs:
        r.font.name='Liberation Sans'; r.font.size=Pt(8)

# Metadata removal / basic core props.
doc.core_properties.title='ОКНО МОСКВА — исследование спроса и поисковой выдачи Яндекса'
doc.core_properties.subject='Обычный и генеративный поиск Яндекса; рекомендации по сайту'
doc.core_properties.author=''
doc.core_properties.last_modified_by=''

doc.save(OUT)
print(OUT)
