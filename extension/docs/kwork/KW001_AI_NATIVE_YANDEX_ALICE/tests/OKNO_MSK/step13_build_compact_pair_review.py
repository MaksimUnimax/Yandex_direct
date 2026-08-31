import csv, re
from pathlib import Path
from urllib.parse import urlsplit

R=Path(__file__).resolve().parent
PAIR=R/'STEP_13_PAIR_INPUT_NORMALIZED.tsv'
PAGE=R/'STEP_13_CURRENT_PAGE_EVIDENCE.tsv'
OUT=R/'STEP_13_PAIR_REVIEW_COMPACT.tsv'
CHUNK=25


def read(p):
    with p.open(encoding='utf-8',newline='') as f:return list(csv.DictReader(f,delimiter='\t'))
def write(p,rows,fields):
    with p.open('w',encoding='utf-8',newline='') as f:
        w=csv.DictWriter(f,fieldnames=fields,delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rows)

def norm(u):
    p=urlsplit((u or '').strip());path=(p.path or '/').rstrip('/') or '/';return f'https://{p.netloc.lower().removeprefix("www.")}{path}'
def slug(u):
    p=urlsplit(u).path.rstrip('/') or '/';return p
def is_parent(a,b):
    pa=urlsplit(a).path.rstrip('/')+'/';pb=urlsplit(b).path.rstrip('/')+'/'
    return pa!=pb and (pa.startswith(pb) or pb.startswith(pa))
def clip(s,n):
    s=re.sub(r'\s+',' ',(s or '').strip())
    return s if len(s)<=n else s[:n-3]+'...'
def first_example(s):
    parts=[re.sub(r'\s+',' ',x.strip()) for x in (s or '').split('||') if x.strip()]
    return clip(parts[0] if parts else '',120)

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
      'pair_id':r['pair_id'],'a_path':slug(a),'a_role':A['page_role'],'a_object':clip(A['primary_object'],45),'a_task':clip(A['primary_user_task'],90),
      'b_path':slug(b),'b_role':B['page_role'],'b_object':clip(B['primary_object'],45),'b_task':clip(B['primary_user_task'],90),
      'relation_shape':shape,'derivation_routes':clip(r['derivation_routes'],75),'relation_structural_units':clip(r['relation_structural_units'],150),
      'query_example':first_example(r['member_evidence']),'step12_search_reason':clip(r['step12_search_reason'],100)})
fields=list(rows[0].keys());write(OUT,rows,fields)
for old in R.glob('STEP_13_PAIR_REVIEW_COMPACT_CHUNK_*.tsv'):old.unlink()
for start in range(0,len(rows),CHUNK):
    write(R/f'STEP_13_PAIR_REVIEW_COMPACT_CHUNK_{start//CHUNK+1:02d}.tsv',rows[start:start+CHUNK],fields)
print('STEP13_COMPACT_REVIEW_READY',len(rows),len(list(R.glob('STEP_13_PAIR_REVIEW_COMPACT_CHUNK_*.tsv'))))
