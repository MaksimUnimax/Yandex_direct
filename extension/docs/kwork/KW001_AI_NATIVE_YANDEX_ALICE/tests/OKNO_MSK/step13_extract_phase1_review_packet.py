import csv, json
from pathlib import Path
from urllib.parse import urlsplit

R = Path(__file__).resolve().parent
SRC = R / 'STEP_12_STEP13_CANDIDATE_PAIRS_V6.tsv'
OUT_PAIRS = R / 'STEP_13_PAIR_INPUT_NORMALIZED.tsv'
OUT_URLS = R / 'STEP_13_UNIQUE_URLS.tsv'
OUT_QA = R / 'STEP_13_PHASE1_REVIEW_PACKET_QA.json'
CHUNK_SIZE = 15


def read_tsv(path):
    with path.open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f, delimiter='\t'))


def write_tsv(path, rows, fields):
    with path.open('w', encoding='utf-8', newline='') as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter='\t', lineterminator='\n')
        w.writeheader()
        w.writerows(rows)


def norm_url(v):
    v=(v or '').strip()
    if not v: return ''
    p=urlsplit(v)
    path=(p.path or '/').rstrip('/') or '/'
    return f'https://{p.netloc.lower().removeprefix("www.")}{path}'

pairs = read_tsv(SRC)
assert len(pairs) == 195, len(pairs)
seen_ids=set()
normalized=[]
url_to_pairs={}
for r in pairs:
    pid=r['pair_id'].strip()
    assert pid and pid not in seen_ids, pid
    seen_ids.add(pid)
    a=norm_url(r['page_a']); b=norm_url(r['page_b'])
    assert a and b and a != b
    x={
        'pair_id':pid,
        'page_a':a,
        'page_b':b,
        'derivation_routes':r.get('derivation_routes',''),
        'source_effective_clusters':r.get('source_effective_clusters',''),
        'relation_structural_units':r.get('relation_structural_units',''),
        'adjacent_task':r.get('adjacent_task',''),
        'member_evidence':r.get('member_evidence',''),
        'normal_overlap_rationale':r.get('normal_overlap_rationale',''),
        'step12_future_search_flag':r.get('later_direct_search_check_needed',''),
        'step12_search_reason':r.get('search_check_reason',''),
        'derivation_origin':r.get('derivation_origin','')
    }
    normalized.append(x)
    for u in (a,b):
        url_to_pairs.setdefault(u,[]).append(pid)

fields=list(normalized[0].keys())
write_tsv(OUT_PAIRS, normalized, fields)

url_rows=[]
for i,u in enumerate(sorted(url_to_pairs),1):
    url_rows.append({
        'url_id':f'U{i:03d}',
        'url':u,
        'path':urlsplit(u).path or '/',
        'pair_count':len(url_to_pairs[u]),
        'pair_ids':';'.join(sorted(url_to_pairs[u]))
    })
write_tsv(OUT_URLS,url_rows,['url_id','url','path','pair_count','pair_ids'])

# Remove old chunks created by prior local reruns if any.
for old in R.glob('STEP_13_PAIR_REVIEW_CHUNK_*.tsv'):
    old.unlink()

chunks=[]
for start in range(0,len(normalized),CHUNK_SIZE):
    chunk=normalized[start:start+CHUNK_SIZE]
    idx=start//CHUNK_SIZE+1
    p=R/f'STEP_13_PAIR_REVIEW_CHUNK_{idx:02d}.tsv'
    write_tsv(p,chunk,fields)
    chunks.append(p.name)

qa={
    'date':'2026-08-31',
    'status':'STEP13_PHASE1_REVIEW_PACKET_READY',
    'input_pairs':len(pairs),
    'normalized_pairs':len(normalized),
    'unique_pair_ids':len(seen_ids),
    'unique_urls':len(url_rows),
    'chunk_size':CHUNK_SIZE,
    'chunks':len(chunks),
    'chunk_files':chunks,
    'provider_calls':0,
    'step13_search_executed':False,
    'silent_pair_drops':len(pairs)-len(normalized)
}
OUT_QA.write_text(json.dumps(qa,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(qa,ensure_ascii=False,indent=2))
