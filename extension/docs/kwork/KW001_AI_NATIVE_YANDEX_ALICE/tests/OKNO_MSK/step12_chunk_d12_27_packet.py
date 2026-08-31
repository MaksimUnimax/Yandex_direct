import csv,json
from pathlib import Path
R=Path(__file__).resolve().parent
P=R/'STEP_12_D12_27_MIXED_UNIT_PACKET.tsv'
with P.open(encoding='utf-8',newline='') as f:rows=list(csv.DictReader(f,delimiter='\t'))
for old in R.glob('STEP_12_D12_27_REVIEW_CHUNK_*.tsv'):old.unlink()
chunks=[]
for i in range(0,len(rows),12):
    part=rows[i:i+12];name=f'STEP_12_D12_27_REVIEW_CHUNK_{i//12+1:02d}.tsv';p=R/name
    fields=['row_no','phrase','final_structural_unit_id','final_unit_task','original_effective_cluster_id']
    out=[]
    for j,r in enumerate(part,start=i+1):out.append({'row_no':j,'phrase':r['phrase'],'final_structural_unit_id':r['final_structural_unit_id'],'final_unit_task':r['final_unit_task'],'original_effective_cluster_id':r['original_effective_cluster_id']})
    with p.open('w',encoding='utf-8',newline='') as f:w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(out)
    chunks.append(name)
(R/'STEP_12_D12_27_REVIEW_CHUNKS.json').write_text(json.dumps({'total_rows':len(rows),'chunk_size':12,'chunks':chunks},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'total_rows':len(rows),'chunks':chunks},ensure_ascii=False))
