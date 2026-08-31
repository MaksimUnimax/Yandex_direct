import csv, json
from pathlib import Path

R = Path(__file__).resolve().parent
OUT = R / 'STEP_12_THIRD_AUDIT_SEARCH_SOURCE_INVENTORY.tsv'
rows=[]
for p in sorted(R.iterdir()):
    if not p.is_file() or not (p.name.startswith('STEP_09') or p.name.startswith('STEP_11')):
        continue
    if p.suffix.lower() not in {'.tsv','.csv','.json','.jsonl'}:
        continue
    rec={'file':p.name,'suffix':p.suffix.lower(),'size_bytes':p.stat().st_size,'row_count':'','columns_or_keys':'','sample_keys':''}
    try:
        if p.suffix.lower() in {'.tsv','.csv'}:
            delim='\t' if p.suffix.lower()=='.tsv' else ','
            with p.open(encoding='utf-8',newline='') as f:
                rd=csv.DictReader(f,delimiter=delim)
                cnt=0; sample=None
                for r in rd:
                    cnt+=1
                    if sample is None: sample=r
                rec['row_count']=cnt
                rec['columns_or_keys']=' | '.join(rd.fieldnames or [])
                if sample:
                    rec['sample_keys']=' | '.join(f'{k}={str(sample.get(k,""))[:80]}' for k in (rd.fieldnames or [])[:8])
        elif p.suffix.lower()=='.json':
            obj=json.loads(p.read_text(encoding='utf-8'))
            if isinstance(obj,list):
                rec['row_count']=len(obj)
                if obj and isinstance(obj[0],dict):
                    rec['columns_or_keys']=' | '.join(obj[0].keys())
            elif isinstance(obj,dict):
                rec['row_count']=1
                rec['columns_or_keys']=' | '.join(obj.keys())
        else:
            cnt=0; keys=[]
            for line in p.read_text(encoding='utf-8').splitlines():
                if not line.strip(): continue
                obj=json.loads(line); cnt+=1
                if not keys and isinstance(obj,dict): keys=list(obj.keys())
            rec['row_count']=cnt; rec['columns_or_keys']=' | '.join(keys)
    except Exception as e:
        rec['columns_or_keys']='PARSE_ERROR:' + repr(e)
    rows.append(rec)

fields=['file','suffix','size_bytes','row_count','columns_or_keys','sample_keys']
with OUT.open('w',encoding='utf-8',newline='') as f:
    w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)
print(json.dumps({'files':len(rows),'output':OUT.name},ensure_ascii=False))
