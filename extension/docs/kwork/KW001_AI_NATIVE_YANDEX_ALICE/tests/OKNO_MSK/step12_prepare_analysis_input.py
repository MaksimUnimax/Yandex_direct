import csv
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
PHRASE_MAP = ROOT / 'STEP_11_PHRASE_PAGE_MAP.tsv'
OWNERSHIP = ROOT / 'STEP_11_PAGE_OWNERSHIP_CORRECTED.tsv'
SUMMARY = ROOT / 'STEP_11_EFFECTIVE_CLUSTER_SUMMARY.tsv'
INDEX = ROOT / 'STEP_12_CLUSTER_PHRASE_AUDIT_INDEX.md'
SEARCH_REQUIRED = ROOT / 'STEP_12_SEARCH_REQUIRED_INPUT.md'


def read_tsv(path):
    with path.open(encoding='utf-8', newline='') as f:
        return list(csv.DictReader(f, delimiter='\t'))

phrases = read_tsv(PHRASE_MAP)
owners = {r['CLUSTER_ID']: r for r in read_tsv(OWNERSHIP)}
summary = {r['cluster_id']: r for r in read_tsv(SUMMARY)}
assigned = [r for r in phrases if r['effective_assignment_status'] == 'ASSIGNED']
search_required = [r for r in phrases if r['effective_assignment_status'] == 'SEARCH_REQUIRED']
by_cluster = defaultdict(list)
for r in assigned:
    by_cluster[r['effective_cluster_id']].append(r)

if len(assigned) != 2313:
    raise RuntimeError(f'expected 2313 assigned, got {len(assigned)}')
if len(search_required) != 19:
    raise RuntimeError(f'expected 19 SEARCH_REQUIRED, got {len(search_required)}')
if len(by_cluster) != 75:
    raise RuntimeError(f'expected 75 effective clusters, got {len(by_cluster)}')
if set(by_cluster) != set(summary):
    raise RuntimeError('cluster set mismatch between phrase map and summary')
if set(by_cluster) != set(owners):
    raise RuntimeError('cluster set mismatch between phrase map and ownership')

clusters = sorted(by_cluster)
chunk_size = 10
chunk_files = []
for i in range(0, len(clusters), chunk_size):
    chunk = clusters[i:i+chunk_size]
    n = i // chunk_size + 1
    out = ROOT / f'STEP_12_CLUSTER_PHRASE_AUDIT_{n:02d}.md'
    chunk_files.append(out.name)
    parts = [f'# Step 12 — cluster phrase audit input {n:02d}\n']
    for cid in chunk:
        s = summary[cid]
        o = owners[cid]
        rows = sorted(by_cluster[cid], key=lambda r: r['phrase'])
        parts += [
            f'## {cid}\n',
            f'- assigned phrases: **{len(rows)}**\n',
            f'- user task: {s["user_task"]}\n',
            f'- intent: {s["intent_type"]}\n',
            f'- business fit: {s["business_fit"]}\n',
            f'- Step-11 state: {o["OWNERSHIP_STATE"]}\n',
            f'- current owner: {o["PRIMARY_OWNER_URL_IF_RESOLVED"] or "NONE"}\n',
            f'- ownership confidence: {o["OWNERSHIP_CONFIDENCE"]}\n',
            f'- Step-11 rationale: {o["CONTRADICTIONS_UNCERTAINTY"]}\n',
            '- all member phrases:\n',
        ]
        parts.extend(f'  - {r["phrase"]}\n' for r in rows)
        parts.append('\n')
    out.write_text(''.join(parts), encoding='utf-8')

idx = [
    '# Step 12 — cluster phrase audit index\n\n',
    'Derived only from persisted Step-11 final artifacts; no new provider/Codex acquisition.\n\n',
    '```text\n',
    f'TOTAL_EFFECTIVE_CLUSTERS = {len(by_cluster)}\n',
    f'TOTAL_ASSIGNED_PHRASES = {len(assigned)}\n',
    f'TOTAL_SEARCH_REQUIRED = {len(search_required)}\n',
    f'CHUNK_FILES = {len(chunk_files)}\n',
    '```\n\n',
    'Files:\n',
]
idx.extend(f'- `{name}`\n' for name in chunk_files)
INDEX.write_text(''.join(idx), encoding='utf-8')

sr = ['# Step 12 — unresolved phrase input\n\n', 'These phrases receive no structural action until their meaning is resolved.\n\n']
for r in sorted(search_required, key=lambda x: x['phrase']):
    sr.append(f'- {r["phrase"]} — {r["mapping_reason"]}\n')
SEARCH_REQUIRED.write_text(''.join(sr), encoding='utf-8')

print({'clusters': len(by_cluster), 'assigned': len(assigned), 'search_required': len(search_required), 'chunks': len(chunk_files)})
