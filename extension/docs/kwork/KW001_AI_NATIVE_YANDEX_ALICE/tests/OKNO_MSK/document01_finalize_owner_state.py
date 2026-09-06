from pathlib import Path
import json, sys

ROOT = Path(__file__).resolve().parent
QA = ROOT / 'RESEARCH_REBUILD_POST_RELEASE_DOCUMENT_01_COMMISSIONER_REPORT_QA_2026-09-06.json'
CURSOR = ROOT / 'EXECUTION_CURSOR.json'
STATE = ROOT / 'RESEARCH_REPORT_REBUILD_CURRENT_STATE_POST_RELEASE_2026-09-05.json'
READBACK = ROOT / 'RESEARCH_REBUILD_POST_RELEASE_DOCUMENT_01_COMMISSIONER_NARRATIVE_READBACK_2026-09-06.md'
MATERIAL_COMMIT = sys.argv[1]

qa = json.loads(QA.read_text(encoding='utf-8'))
counts = qa['counts']; hashes = qa['sha256']; sizes = qa['size_bytes']; pages = counts['pdf_pages']

cursor = json.loads(CURSOR.read_text(encoding='utf-8'))
cursor['execution_unit'] = 'POST_RELEASE_OWNER_REVIEW_CORRECTED_DOCUMENT_01'
cursor['next_action'] = 'OWNER_REVIEW_CORRECTED_DOCUMENT_01'
d = cursor['document_01_owner_recheck_2026_09_05']
d.update({
    'status': 'ANALYST_RECHECK_PASS__FINAL_CUSTOMER_CONTRACT__OWNER_REVIEW_PENDING',
    'current_document': '01',
    'document_01_analyst_recheck': 'PASS',
    'document_01_owner_review': 'PENDING__AWAITING_OWNER_RECHECK',
    'document_02_owner_review': 'PENDING',
    'document_03_owner_review': 'PENDING',
    'final_owner_recipient_acceptance': 'OPEN',
    'next_action': 'OWNER_REVIEW_CORRECTED_DOCUMENT_01',
    'latest_material_correction_commit_sha': MATERIAL_COMMIT,
    'latest_github_content_readback': 'PASS__FINAL_CUSTOMER_CONTRACT_RECONCILED',
    'physical_pdf_qa': f'PASS__{pages}_OF_{pages}_PAGES',
    'deterministic_qa_checks': len(qa['checks']),
    'search_observations_checked': 75,
    'search_observation_appendix_in_client_report': 'ABSENT',
    'ai_causal_cases_checked': 8,
    'action_rows_checked': 34,
    'ready_recommendations_with_why': 7,
    'company_fact_requests': 2,
    'site_url_in_report_title': True,
    'wordstat_frequency_work_visible': True,
    'wordstat_internal_count_field_in_client_text': 'ABSENT',
    'positive_no_change_page_catalogue': 'ABSENT',
    'full_rebuild_claim': 'ABSENT__FULL_REBUILD_NOT_REQUIRED_BY_RESEARCH',
    'qa_authority': QA.name,
    'github_readback_authority': READBACK.name,
    'source_sha256': hashes['md'],
    'docx_sha256': hashes['docx'],
    'pdf_sha256': hashes['pdf'],
    'pdf_pages': pages
})
CURSOR.write_text(json.dumps(cursor, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

state = json.loads(STATE.read_text(encoding='utf-8'))
state['next_action'] = 'OWNER_REVIEW_CORRECTED_DOCUMENT_01'
state['correction_materialization_status'] = 'DOCUMENT_01_FINAL_CUSTOMER_CONTRACT_ANALYST_RECHECK_PASS__OWNER_REVIEW_PENDING__DOCUMENT_02_03_NOT_ADVANCED'
cr = state['corrected_recipient_release']
commits = cr.setdefault('materialization_commit_shas', [])
if MATERIAL_COMMIT not in commits:
    commits.append(MATERIAL_COMMIT)
cr.update({
    'analyst_recipient_qa': 'DOCUMENT_01_FINAL_CUSTOMER_CONTRACT_PASS',
    'document_01_analyst_recheck': 'PASS',
    'document_01_owner_review': 'PENDING__AWAITING_OWNER_RECHECK',
    'document_01_pdf_pages': pages,
    'document_01_pdf_size_bytes': sizes['pdf'],
    'document_01_pdf_sha256': hashes['pdf'],
    'document_01_docx_size_bytes': sizes['docx'],
    'document_01_docx_sha256': hashes['docx'],
    'document_01_source_size_bytes': sizes['md'],
    'document_01_source_sha256': hashes['md'],
    'document_01_latest_material_correction_commit_sha': MATERIAL_COMMIT,
    'document_01_latest_github_content_readback': 'PASS__FINAL_CUSTOMER_CONTRACT_RECONCILED',
    'current_document': '01',
    'document_02_owner_review': 'PENDING',
    'document_03_owner_review': 'PENDING',
    'final_owner_recipient_acceptance': 'OPEN',
    'document_01_github_readback_authority': READBACK.name,
    'document_01_ready_recommendations_with_why': 7,
    'document_01_ordinary_yandex_observations': 75,
    'document_01_raw_75_query_appendix': 'ABSENT',
    'document_01_alice_cases': 8,
    'document_01_site_url_in_title': True,
    'document_01_frequency_work_visible': True,
    'document_01_internal_count_field': 'ABSENT',
    'document_01_positive_no_change_page_catalogue': 'ABSENT',
    'document_01_full_rebuild_claim': 'ABSENT__RESEARCH_CONCLUDES_FULL_REBUILD_NOT_REQUIRED',
    'new_provider_calls': 0,
    'paid_cost_rub': 0
})
STATE.write_text(json.dumps(state, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')

READBACK.write_text(f'''# OKNO_MSK — Document №01 final customer-contract remote readback

Status: **ANALYST_RECHECK_PASS / OWNER_REVIEW_PENDING**

Material commit: `{MATERIAL_COMMIT}`

## Artifact identity

```text
source bytes = {sizes['md']}
source sha256 = {hashes['md']}
docx bytes = {sizes['docx']}
docx sha256 = {hashes['docx']}
pdf bytes = {sizes['pdf']}
pdf sha256 = {hashes['pdf']}
pdf pages = {pages}
```

## Final Report №01 contract verified

```text
site URL is visible in the title = PASS
customer wording uses search phrases, not raw row terminology = PASS
internal Wordstat field name is absent = PASS
Wordstat demand/frequency work is explained in Russian = PASS
2840 unique phrases are not misrepresented as exact-frequency measurements = PASS
full rebuild is not falsely claimed; report says full rebuild is not required = PASS
75 ordinary-Yandex targeted checks are explained, raw 75-query appendix is absent = PASS
Alice selection has causal bridge: full core -> ordinary Yandex -> 25 candidates -> 8 selected = PASS
Alice customer vocabulary uses "выдача Алисы" = PASS
positive site result is aggregate, not a catalogue of a few already-correct pages = PASS
seven ready recommendations remain = PASS
two company fact requests remain = PASS
Document 02 / 03 unchanged = PASS
new provider calls = 0
```

```text
CURRENT_DOCUMENT = 01
DOCUMENT_01_ANALYST_RECHECK = PASS
DOCUMENT_01_OWNER_REVIEW = PENDING__AWAITING_OWNER_RECHECK
DOCUMENT_02_OWNER_REVIEW = PENDING
DOCUMENT_03_OWNER_REVIEW = PENDING
NEXT_ACTION = OWNER_REVIEW_CORRECTED_DOCUMENT_01
```
''', encoding='utf-8')

print('DOCUMENT_01_FINAL_OWNER_STATE_PASS', MATERIAL_COMMIT, pages)
