from pathlib import Path

ROOT = Path(__file__).resolve().parent
TARGET = ROOT / 'step12_build_step13_pairs_and_maturity_v2.py'

text = TARGET.read_text(encoding='utf-8')
old = """    'new_page_hierarchy_rows_expected': len(hierarchy),
    'new_page_hierarchy_rows_materialized_in_actions': sum(
        norm_page(r['primary_page_candidate']) in hierarchy_by_page
        and r['hierarchy_clarity'].startswith('MATERIALIZED_')
        for r in v2
    ),
"""
new = """    'new_page_hierarchy_rows_expected': len(hierarchy),
    'new_page_hierarchy_owner_action_rows': sum(
        norm_page(r['primary_page_candidate']) in hierarchy_by_page
        and r['hierarchy_clarity'].startswith('MATERIALIZED_')
        for r in v2
    ),
    'new_page_hierarchy_rows_materialized_in_actions': len({
        norm_page(r['primary_page_candidate'])
        for r in v2
        if norm_page(r['primary_page_candidate']) in hierarchy_by_page
        and r['hierarchy_clarity'].startswith('MATERIALIZED_')
    }),
"""

if text.count(old) != 1:
    raise RuntimeError(f'Expected exactly one old hierarchy metric block, found {text.count(old)}')

patched = text.replace(old, new)
if patched == text:
    raise RuntimeError('Patch produced no change')
if "'new_page_hierarchy_owner_action_rows'" not in patched:
    raise RuntimeError('Diagnostic owner-action row metric missing after patch')
if "'new_page_hierarchy_rows_materialized_in_actions': len({" not in patched:
    raise RuntimeError('Unique candidate-page metric missing after patch')

TARGET.write_text(patched, encoding='utf-8')
print('STEP12_D12_05_UNIQUE_HIERARCHY_METRIC_PATCH_PASS')
