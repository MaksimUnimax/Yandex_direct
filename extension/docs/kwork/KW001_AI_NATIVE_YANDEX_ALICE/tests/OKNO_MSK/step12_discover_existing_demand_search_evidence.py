import csv, json
from pathlib import Path

ROOT=Path(__file__).resolve().parent
OUT=ROOT/'STEP_12_EXISTING_DEMAND_SEARCH_EVIDENCE_INVENTORY.md'
TOKENS=('wordstat','step_03','step_04','step_05','step_06','step_08','step_09','search','serp','ranked','probe','normalized')

entries=[]
for p in sorted(ROOT.iterdir()):
    if not p.is_file(): continue
    name=p.name.lower()
    if not any(t in name for t in TOKENS): continue
    if p.name==OUT.name: continue
    info={'name':p.name,'suffix':p.suffix.lower(),'size':p.stat().st_size,'rows':'','header':'','json_keys':'','note':''}
    try:
        if p.suffix.lower() in {'.tsv','.csv'}:
            delim='\t' if p.suffix.lower()=='.tsv' else ','
            with p.open(encoding='utf-8',newline='') as f:
                r=csv.reader(f,delimiter=delim)
                header=next(r,[])
                n=sum(1 for _ in r)
            info['rows']=str(n);info['header']=' | '.join(header)
        elif p.suffix.lower()=='.json':
            obj=json.loads(p.read_text(encoding='utf-8'))
            if isinstance(obj,dict): info['json_keys']=' | '.join(list(obj.keys())[:40])
            elif isinstance(obj,list): info['rows']=str(len(obj));info['json_keys']='LIST'
        elif p.suffix.lower()=='.md':
            text=p.read_text(encoding='utf-8')
            info['note']='markdown; chars='+str(len(text))
    except Exception as e:
        info['note']='parse_error='+repr(e)
    entries.append(info)

lines=['# Step 12 correction — existing demand/Search evidence inventory','',
'Purpose: identify already persisted demand and ordinary-Search evidence before considering any new provider call for D12-03/D12-10.','',
'This inventory reports file names/schema/counts only. It does not assume what a field means until its producing step/method provenance is checked.','',
'| File | Type | Rows | Size | Header / JSON keys | Note |','|---|---|---:|---:|---|---|']
for e in entries:
    schema=e['header'] or e['json_keys']
    lines.append(f"| `{e['name']}` | {e['suffix']} | {e['rows']} | {e['size']} | {schema.replace('|','/')} | {e['note']} |")
lines+=['',f'candidate_files = {len(entries)}','',
'Next: inspect the producing-step authority for promising files before using any frequency/result field as demand or Search evidence.']
OUT.write_text('\n'.join(lines)+'\n',encoding='utf-8')
print(json.dumps({'candidate_files':len(entries)},ensure_ascii=False))
