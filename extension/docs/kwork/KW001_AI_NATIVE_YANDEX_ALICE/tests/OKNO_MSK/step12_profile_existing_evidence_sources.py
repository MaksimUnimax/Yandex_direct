import csv, json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'STEP_12_EXISTING_EVIDENCE_SCHEMA_PROFILE.md'
PREFIXES=('STEP_03R','STEP_04','STEP_05','STEP_06','STEP_08','STEP_09','STEP_11_SEARCH')


def tsv_profile(p):
    lines=p.read_text(encoding='utf-8').splitlines()
    data=[ln for ln in lines if ln.strip() and not ln.lstrip().startswith('#')]
    if not data:return {'header':[],'rows':0,'sample':[]}
    reader=csv.reader(data,delimiter='\t')
    header=next(reader,[]);rows=list(reader)
    return {'header':header,'rows':len(rows),'sample':rows[:2]}

entries=[]
for p in sorted(ROOT.iterdir()):
    if not p.is_file():continue
    if not p.name.startswith(PREFIXES):continue
    if p.suffix.lower()=='.tsv':
        try:
            prof=tsv_profile(p)
            entries.append((p.name,prof))
        except Exception as e:
            entries.append((p.name,{'header':['ERROR '+repr(e)],'rows':0,'sample':[]}))

lines=['# Step 12 correction — persisted evidence schema profile','',
'Purpose: determine what the already saved Wordstat/Search artifacts actually contain before using any field as evidence. Leading markdown/comment lines in TSV files are ignored when finding the real header.','']
for name,prof in entries:
    lines.append(f'## {name}')
    lines.append(f'- data rows: **{prof["rows"]}**')
    lines.append('- header:')
    lines.append('```text')
    lines.append('\t'.join(prof['header']))
    lines.append('```')
    if prof['sample']:
        lines.append('- first persisted data rows (schema inspection only):')
        lines.append('```text')
        for row in prof['sample']: lines.append('\t'.join(row))
        lines.append('```')
    lines.append('')
OUT.write_text('\n'.join(lines),encoding='utf-8')
print(json.dumps({'profiled_tsv_files':len(entries)},ensure_ascii=False))
