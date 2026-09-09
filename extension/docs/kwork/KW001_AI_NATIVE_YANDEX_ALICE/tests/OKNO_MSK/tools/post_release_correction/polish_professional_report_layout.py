from __future__ import annotations

import hashlib
import json
import re
import shutil
import subprocess
from pathlib import Path
from pypdf import PdfReader

ROOT = Path('extension/docs/kwork/KW001_AI_NATIVE_YANDEX_ALICE/tests/OKNO_MSK')
REL = ROOT / 'OKNO_MSK_RESEARCH_RELEASE_STEP05A_PROPAGATED_2026-09-09'
R1_MD = REL / 'sources/01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-09.md'
R1_DOCX = REL / 'editable/01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-09.docx'
R1_PDF = REL / '01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-09.pdf'
R2_MD = REL / 'sources/02_OKNO_MSK_VNEDRENIE_REKOMENDATSII_RU_2026-09-09.md'
R2_DOCX = REL / 'editable/02_OKNO_MSK_VNEDRENIE_REKOMENDATSII_RU_2026-09-09.docx'
R2_PDF = REL / '02_OKNO_MSK_VNEDRENIE_REKOMENDATSII_RU_2026-09-09.pdf'
TRACKER = REL / '05_OKNO_MSK_IMPLEMENTATION_TRACKER_2026-09-09.xlsx'
MANIFEST = REL / 'RELEASE_MANIFEST_2026-09-09.json'
STATE = ROOT / 'RESEARCH_REPORT_REBUILD_CURRENT_STATE_CLIENT_CLEANUP_2026-09-08.json'
BASE_QA = ROOT / 'REPORTS_01_02_PROFESSIONAL_REPACKAGE_QA_2026-09-09.json'
LAYOUT_QA = ROOT / 'REPORTS_01_02_PROFESSIONAL_LAYOUT_QA_2026-09-09.json'
RECEIPT = ROOT / 'REPORTS_01_02_PROFESSIONAL_REPACKAGE_RECEIPT_2026-09-09.md'
R1_RENDER = Path('/tmp/report01-prof-polished-render')
R2_RENDER = Path('/tmp/report02-prof-polished-render')
TRACKER_SHA = 'f71696785b1a04037e3d56a80eed9e697733a9fc03a67dc9a03c7aa566e13719'


def sha(path: Path) -> str:
    h = hashlib.sha256(); h.update(path.read_bytes()); return h.hexdigest()


def cells(line: str) -> list[str]:
    return [x.strip() for x in line.strip().strip('|').split('|')]


def replace_tables(text: str, which: str) -> str:
    lines = text.splitlines(); out: list[str] = []; i = 0
    while i < len(lines):
        if i + 1 < len(lines) and lines[i].startswith('|') and lines[i + 1].startswith('|---'):
            header = cells(lines[i]); j = i + 2; rows: list[list[str]] = []
            while j < len(lines) and lines[j].startswith('|'):
                rows.append(cells(lines[j])); j += 1
            if which == 'r1' and header == ['Показатель', 'Итог']:
                out += [f'- **{r[0]}:** {r[1]}' for r in rows]
            elif which == 'r1' and header == ['Проверка', 'Страница', 'Что нужно получить']:
                for n, r in enumerate(rows, 1):
                    out += [f'### {n}. {r[0]}', '', f'**Страница:** {r[1]}', '', 'Результат проверки фиксируется как отдельное решение по роли страницы, структуре или ассортименту в рабочей книге №05.', '']
            elif which == 'r1' and header == ['Запрос', 'Почему выбрали', 'Что показала проверка выдачи Алисы', 'Что это значит для сайта']:
                for n, r in enumerate(rows, 1):
                    out += [f'### {n}. {r[0]}', '', f'**Почему выбрали:** {r[1]}', '', f'**Что показала выдача Алисы:** {r[2]}', '', f'**Что это значит для сайта:** {r[3]}', '']
            elif which == 'r1' and header == ['Конкурент', 'Проверено страниц']:
                for r in rows:
                    if 'Итого' in r[0]:
                        out += ['', f'**Итого проверено:** {r[1]} страницы.', '']
                    else:
                        out += [f'- **{r[0]}:** {r[1]} страниц']
            elif which == 'r2' and header[:3] == ['Очередь', 'Готовность', 'Задача']:
                groups = {1: [], 2: [], 3: []}
                for r in rows: groups[int(r[0])].append(r)
                labels = {1: 'Очередь 1 — можно внедрять сейчас', 2: 'Очередь 2 — сначала закрыть уточнение', 3: 'Очередь 3 — сначала выполнить проверку'}
                for q in (1, 2, 3):
                    out += [f'### {labels[q]}', '']
                    for r in groups[q]:
                        out += [f'- **{r[2]}**', f'  - Страница: {r[3]}', f'  - Кто нужен: {r[4]}', f'  - Объём: {r[5]}', f'  - Зависимость: {r[6]}']
                    out += ['']
            elif which == 'r2' and header == ['Поисковая фраза', 'Основная страница', 'Роль']:
                for n, r in enumerate(rows, 1):
                    out += [f'{n}. **{r[0]}**', f'   - Основная страница: {r[1]}', f'   - Роль: {r[2]}']
            elif which == 'r2' and header == ['Поисковая фраза', 'Тематический маршрут', 'Что нужно подтвердить']:
                for n, r in enumerate(rows, 1):
                    out += [f'{n}. **{r[0]}**', f'   - Тематический маршрут: {r[1]}', f'   - Нужно подтвердить: {r[2]}']
            else:
                raise RuntimeError(f'unhandled table {which}: {header}')
            i = j
        else:
            out.append(lines[i]); i += 1
    return '\n'.join(out) + '\n'


def deautolink(text: str) -> str:
    # Keep URL text visible but prevent LibreOffice from appending a broken hyperlink marker in PDF.
    pat = re.compile(r'(?<![`(])https://[^\s`]+')
    def repl(m: re.Match) -> str:
        s = m.group(0); trail = ''
        while s and s[-1] in '.,;:':
            trail = s[-1] + trail; s = s[:-1]
        return f'`{s}`{trail}'
    return pat.sub(repl, text)


def build(md: Path, current_docx: Path, out_pdf: Path, render_dir: Path) -> tuple[int, str, str]:
    tmp_docx = Path('/tmp') / ('polished-' + current_docx.name)
    tmp_pdf_dir = Path('/tmp') / ('polished-pdf-' + current_docx.stem)
    shutil.rmtree(tmp_pdf_dir, ignore_errors=True); tmp_pdf_dir.mkdir(parents=True)
    subprocess.run(['pandoc', str(md), '--from=gfm', '--to=docx', '--reference-doc', str(current_docx), '-o', str(tmp_docx)], check=True)
    subprocess.run(['libreoffice', '--headless', '--convert-to', 'pdf', '--outdir', str(tmp_pdf_dir), str(tmp_docx)], check=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
    built_pdf = tmp_pdf_dir / (tmp_docx.stem + '.pdf')
    if not built_pdf.exists(): raise RuntimeError(f'PDF not generated: {built_pdf}')
    shutil.copy2(tmp_docx, current_docx); shutil.copy2(built_pdf, out_pdf)
    shutil.rmtree(render_dir, ignore_errors=True); render_dir.mkdir(parents=True)
    subprocess.run(['pdftoppm', '-png', '-r', '150', str(out_pdf), str(render_dir / 'page')], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    pages = len(PdfReader(out_pdf).pages)
    return pages, sha(current_docx), sha(out_pdf)


def main() -> None:
    if sha(TRACKER) != TRACKER_SHA: raise RuntimeError('implementation tracker hash changed')
    r1 = deautolink(replace_tables(R1_MD.read_text(encoding='utf-8'), 'r1'))
    r2 = deautolink(replace_tables(R2_MD.read_text(encoding='utf-8'), 'r2'))
    R1_MD.write_text(r1, encoding='utf-8'); R2_MD.write_text(r2, encoding='utf-8')
    if any(line.startswith('|') for line in r1.splitlines()): raise RuntimeError('Report01 table rows remain')
    if any(line.startswith('|') for line in r2.splitlines()): raise RuntimeError('Report02 table rows remain')
    if '3 изменения можно передавать в работу сейчас' not in r1: raise RuntimeError('Report01 ready count lost')
    if '5 изменений требуют уточнения до внедрения' not in r1: raise RuntimeError('Report01 clarification count lost')
    if '## 1. Сводный план внедрения' not in r2: raise RuntimeError('Report02 summary lost')
    if 'Очередь 1 — можно внедрять сейчас' not in r2 or 'Очередь 2 — сначала закрыть уточнение' not in r2 or 'Очередь 3 — сначала выполнить проверку' not in r2: raise RuntimeError('Report02 queues lost')
    if r2.count('Роль: Семантическое назначение без физического изменения') != 9: raise RuntimeError('Report02 exact assignment rows lost')
    if r2.count('Нужно подтвердить:') != 7: raise RuntimeError('Report02 unresolved rows lost')
    p1, d1, q1 = build(R1_MD, R1_DOCX, R1_PDF, R1_RENDER)
    p2, d2, q2 = build(R2_MD, R2_DOCX, R2_PDF, R2_RENDER)
    if not 8 <= p1 <= 14: raise RuntimeError(f'Report01 page count unexpected: {p1}')
    if not 7 <= p2 <= 13: raise RuntimeError(f'Report02 page count unexpected: {p2}')
    pdf1_text = '\n'.join((p.extract_text() or '') for p in PdfReader(R1_PDF).pages)
    pdf2_text = '\n'.join((p.extract_text() or '') for p in PdfReader(R2_PDF).pages)
    if re.search(r'https://\S+X(?:\s|$)', pdf1_text) or re.search(r'https://\S+X(?:\s|$)', pdf2_text): raise RuntimeError('broken URL marker remains in PDF')
    qa = {
        'schema': 'OKNO_MSK_REPORTS_01_02_PROFESSIONAL_LAYOUT_QA_V1', 'date': '2026-09-09', 'status': 'PASS',
        'wide_markdown_tables_remaining': 0, 'tracker_sha256': TRACKER_SHA,
        'report01': {'pages': p1, 'markdown_sha256': sha(R1_MD), 'docx_sha256': d1, 'pdf_sha256': q1, 'rendered_pages': len(list(R1_RENDER.glob('page-*.png')))},
        'report02': {'pages': p2, 'markdown_sha256': sha(R2_MD), 'docx_sha256': d2, 'pdf_sha256': q2, 'rendered_pages': len(list(R2_RENDER.glob('page-*.png')))},
        'broken_url_marker_hits': 0, 'provider_calls': 0, 'remote_visual_readback': 'PENDING'
    }
    LAYOUT_QA.write_text(json.dumps(qa, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    if BASE_QA.exists():
        base = json.loads(BASE_QA.read_text(encoding='utf-8')); base['layout_polish'] = qa; base['remote_visual_readback'] = 'PENDING_LAYOUT_RECHECK'; BASE_QA.write_text(json.dumps(base, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    if MANIFEST.exists():
        m = json.loads(MANIFEST.read_text(encoding='utf-8')); m['professional_layout_polish'] = {'status':'PASS','wide_pdf_tables_removed':True,'report01_pages':p1,'report02_pages':p2,'tracker_sha256':TRACKER_SHA,'remote_visual_readback':'PENDING'}; m['status']='REPORTS_01_02_PROFESSIONAL_REPACKAGE__LAYOUT_QA_PASS__REMOTE_VISUAL_READBACK_PENDING'; MANIFEST.write_text(json.dumps(m, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    if STATE.exists():
        s = json.loads(STATE.read_text(encoding='utf-8')); s['state']='REPORTS_01_02_PROFESSIONAL_REPACKAGE__LAYOUT_QA_PASS__REMOTE_VISUAL_READBACK_PENDING'; s.setdefault('professional_packaging',{})['layout_polish']=qa; s['next_action']='REMOTE_VISUAL_READBACK_REPORTS_01_02_PROFESSIONAL_PACKAGE__DO_NOT_START_DOCUMENT_03'; STATE.write_text(json.dumps(s, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    with RECEIPT.open('a', encoding='utf-8') as f:
        f.write(f'\n## Финальная полировка PDF-композиции\n\n- Широкие Markdown-таблицы убраны из PDF и заменены компактными очередями/карточками.\n- Полная рабочая детализация сохранена в книге №05.\n- Report №01: {p1} стр.; Report №02: {p2} стр.\n- URL-marker defects: 0.\n- Layout QA: PASS.\n- Remote visual readback: PENDING.\n')
    print('PROFESSIONAL_LAYOUT_POLISH_PASS', p1, p2, q1, q2, TRACKER_SHA)

if __name__ == '__main__': main()
