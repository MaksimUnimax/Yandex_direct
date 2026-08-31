import csv, re
from pathlib import Path
from urllib.parse import urlsplit

R=Path(__file__).resolve().parent
PAIR=R/'STEP_13_PAIR_INPUT_NORMALIZED.tsv'
PAGE=R/'STEP_13_CURRENT_PAGE_EVIDENCE.tsv'
OUT=R/'STEP_13_PAIR_REVIEW_COMPACT.tsv'
CHUNK=15


def read(p):
    with p.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f,delimiter='\t'))
def write(p,rows,fields):
    with p.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)

def norm(u):
    p=urlsplit((u or '').strip());path=(p.path or '/').rstrip('/') or '/';return f'https://{p.netloc.lower().removeprefix("www.")}{path}'
def is_parent(a,b):
    pa=urlsplit(a).path.rstrip('/')+'/';pb=urlsplit(b).path.rstrip('/')+'/'
    return pa!=pb and (pa.startswith(pb) or pb.startswith(pa))
def short_evidence(s):
    # Keep at most four representative phrases/groups, compactly.
    parts=[re.sub(r'\s+',' ',x.strip()) for x in (s or '').split('||') if x.strip()]
    out=[]
    for p in parts[:4]:
        if len(p)>180:p=p[:177]+'...'
        out.append(p)
    return ' || '.join(out)

pairs=read(PAIR);pages=read(PAGE)
assert len(pairs)==195 and len(pages)==47
by={norm(r['url']):r for r in pages}
rows=[]
for r in pairs:
    a=norm(r['page_a']);b=norm(r['page_b']);assert a in by and b in by,(a,b)
    A=by[a];B=by[b]
    if is_parent(a,b): shape='PATH_HIERARCHY'
    elif A['page_role']=='PRODUCT_MODEL' and B['page_role']=='PRODUCT_MODEL':shape='SIBLING_PRODUCT_MODELS'
    elif A['page_role'].endswith('SUBTYPE') and B['page_role'].endswith('SUBTYPE'):shape='SIBLING_SUBTYPES'
    elif ('INFORMATION' in A['intent_mode'] or 'DIY' in A['intent_mode']) and ('COMMERCIAL' in B['intent_mode'] or 'SERVICE' in B['intent_mode']):shape='MIXED_INTENT_INFO_VS_COMMERCIAL'
    elif ('INFORMATION' in B['intent_mode'] or 'DIY' in B['intent_mode']) and ('COMMERCIAL' in A['intent_mode'] or 'SERVICE' in A['intent_mode']):shape='MIXED_INTENT_INFO_VS_COMMERCIAL'
    else:shape='CROSS_ROLE_OR_OBJECT'
    rows.append({
      'pair_id':r['pair_id'],'page_a':a,'a_role':A['page_role'],'a_object':A['primary_object'],'a_task':A['primary_user_task'],
      'page_b':b,'b_role':B['page_role'],'b_object':B['primary_object'],'b_task':B['primary_user_task'],
      'relation_shape':shape,'derivation_routes':r['derivation_routes'],'relation_structural_units':r['relation_structural_units'],
      'adjacent_task':r['adjacent_task'],'query_examples':short_evidence(r['member_evidence']),
      'normal_overlap_rationale':r['normal_overlap_rationale'],'step12_search_reason':r['step12_search_reason']})
fields=list(rows[0].keys());write(OUT,rows,fields)
for old in R.glob('STEP_13_PAIR_REVIEW_COMPACT_CHUNK_*.tsv'):old.unlink()
for start in range(0,len(rows),CHUNK):
    write(R/f'STEP_13_PAIR_REVIEW_COMPACT_CHUNK_{start//CHUNK+1:02d}.tsv',rows[start:start+CHUNK],fields)
print('STEP13_COMPACT_REVIEW_READY',len(rows),len(list(R.glob('STEP_13_PAIR_REVIEW_COMPACT_CHUNK_*.tsv'))))
