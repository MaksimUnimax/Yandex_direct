from pathlib import Path

ROOT = Path(__file__).resolve().parent
TARGET = ROOT / 'step12_independent_final_qa.py'
text = TARGET.read_text(encoding='utf-8')

replacements = [
    (
        "from collections import Counter, defaultdict\nfrom pathlib import Path\n",
        "from collections import Counter, defaultdict\nfrom itertools import combinations\nfrom pathlib import Path\n",
    ),
    (
        "UNITS = ROOT / 'STEP_12_STRUCTURAL_UNITS_V5.tsv'\nACTIONS = ROOT / 'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V2.tsv'\n",
        "UNITS = ROOT / 'STEP_12_STRUCTURAL_UNITS_V5.tsv'\nACTIONS_V1 = ROOT / 'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V1.tsv'\nACTIONS = ROOT / 'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V2.tsv'\n",
    ),
    (
        "def norm_page(v):\n    v = (v or '').strip()\n    if not v:\n        return ''\n    if v.startswith('PROPOSED_NEW:'):\n        return 'https://okno-msk.ru' + v.split(':', 1)[1]\n    return v\n\n\ndef actual_text(v):\n",
        "def norm_page(v):\n    v = (v or '').strip()\n    if not v:\n        return ''\n    if v.startswith('PROPOSED_NEW:'):\n        return 'https://okno-msk.ru' + v.split(':', 1)[1]\n    return v\n\n\ndef split_multi(v):\n    return [x.strip() for x in (v or '').split('||') if x.strip()]\n\n\ndef actual_text(v):\n",
    ),
    (
        "units = read(UNITS)\nactions = read(ACTIONS)\nfinal_map = read(FINAL_MAP)\n",
        "units = read(UNITS)\nactions_v1 = read(ACTIONS_V1)\nactions = read(ACTIONS)\nfinal_map = read(FINAL_MAP)\n",
    ),
    (
        "action_by = {r['structural_unit_id']: r for r in actions}\nunit_by = {r['structural_unit_id']: r for r in units}\n",
        "action_v1_by = {r['structural_unit_id']: r for r in actions_v1}\naction_by = {r['structural_unit_id']: r for r in actions}\nunit_by = {r['structural_unit_id']: r for r in units}\n",
    ),
    (
        "# Pair graph is a candidate universe only.\npair_id_dups = sum(v > 1 for v in Counter(r['pair_id'] for r in pairs).values())\nadd_check('Q030', 'PAIR_GRAPH', len(pairs), 189, len(pairs) == 189, 'COMPUTED_FROM_DATA', 'STEP_12_STEP13_CANDIDATE_PAIRS.tsv', 'Count persisted deterministic candidate pairs.')\nadd_check('Q031', 'PAIR_GRAPH', pair_id_dups, 0, pair_id_dups == 0, 'COMPUTED_FROM_DATA', 'STEP_12_STEP13_CANDIDATE_PAIRS.tsv', 'Count duplicate pair IDs.')\n",
        "# Pair graph is a candidate universe only. Recompute the expected pair-key\n# universe independently from V1 routing inputs instead of asserting a historical count.\nsource_uids = defaultdict(set)\nfor r in assign:\n    uid = r['final_structural_unit_id']\n    src = r['original_effective_cluster_id']\n    if uid and src:\n        source_uids[src].add(uid)\n\nexpected_pair_keys = set()\nfor uid, r in action_v1_by.items():\n    a = norm_page(r['primary_page_candidate'])\n    bpage = norm_page(r['supporting_page'])\n    if a and bpage and a != bpage:\n        expected_pair_keys.add(tuple(sorted((a, bpage))))\nfor src, uids in source_uids.items():\n    pages = sorted({norm_page(action_v1_by[uid]['primary_page_candidate']) for uid in uids if uid in action_v1_by and norm_page(action_v1_by[uid]['primary_page_candidate'])})\n    expected_pair_keys.update(tuple(sorted(pair)) for pair in combinations(pages, 2))\nfor h in hierarchy:\n    candidate = norm_page(h['proposed_url'])\n    for raw in split_multi(h.get('mandatory_inbound_links')) + split_multi(h.get('mandatory_outbound_links')):\n        other = norm_page(raw)\n        if candidate and other and candidate != other:\n            expected_pair_keys.add(tuple(sorted((candidate, other))))\n\nactual_pair_keys = [tuple(sorted((norm_page(r['page_a']), norm_page(r['page_b'])))) for r in pairs]\nactual_pair_key_set = set(actual_pair_keys)\nmissing_expected_pairs = sorted(expected_pair_keys - actual_pair_key_set)\nextra_actual_pairs = sorted(actual_pair_key_set - expected_pair_keys)\npair_id_dups = sum(v > 1 for v in Counter(r['pair_id'] for r in pairs).values())\nadd_check('Q030', 'PAIR_GRAPH', len(pairs), len(expected_pair_keys), len(pairs) == len(expected_pair_keys), 'COMPUTED_FROM_DATA', 'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V1.tsv | STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V5.tsv | STEP_12_NEW_PAGE_HIERARCHY_PLAN.tsv | STEP_12_STEP13_CANDIDATE_PAIRS.tsv', 'Independently recompute expected pair-key count from V1 primary/supporting edges, shared-source multi-primary routes, and hierarchy edges.')\nadd_check('Q030M', 'PAIR_GRAPH', len(missing_expected_pairs), 0, not missing_expected_pairs, 'COMPUTED_FROM_DATA', 'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V1.tsv | STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V5.tsv | STEP_12_NEW_PAGE_HIERARCHY_PLAN.tsv | STEP_12_STEP13_CANDIDATE_PAIRS.tsv', 'Set-difference expected pair keys minus persisted pair keys.')\nadd_check('Q030E', 'PAIR_GRAPH', len(extra_actual_pairs), 0, not extra_actual_pairs, 'COMPUTED_FROM_DATA', 'STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V1.tsv | STEP_12_STRUCTURAL_UNIT_ASSIGNMENTS_V5.tsv | STEP_12_NEW_PAGE_HIERARCHY_PLAN.tsv | STEP_12_STEP13_CANDIDATE_PAIRS.tsv', 'Set-difference persisted pair keys minus independently recomputed expected pair keys.')\nadd_check('Q031', 'PAIR_GRAPH', pair_id_dups, 0, pair_id_dups == 0, 'COMPUTED_FROM_DATA', 'STEP_12_STEP13_CANDIDATE_PAIRS.tsv', 'Count duplicate pair IDs.')\n",
    ),
]

for old, new in replacements:
    count = text.count(old)
    if count != 1:
        raise RuntimeError(f'Expected exactly one patch anchor, found {count}: {old[:100]!r}')
    text = text.replace(old, new)

if "len(pairs), 189" in text:
    raise RuntimeError('Historical fixed pair-count assertion still present')
if "Q030M" not in text or "Q030E" not in text:
    raise RuntimeError('Dynamic pair set-difference checks missing after patch')
if "ACTIONS_V1" not in text or "expected_pair_keys" not in text:
    raise RuntimeError('Independent pair recomputation inputs missing after patch')

TARGET.write_text(text, encoding='utf-8')
print('STEP12_D12_05_DYNAMIC_PAIR_QA_PATCH_PASS')
