from pathlib import Path

ROOT = Path(__file__).resolve().parent
report_path = ROOT / 'STEP_12_REPORT.md'
manifest_path = ROOT / 'JOB_MANIFEST.md'

report = report_path.read_text(encoding='utf-8')
old_row = '| 12 | Decide what pages to keep, strengthen, add, create or deliberately not create | 🟡 CURRENT / candidate built, GitHub readback pending |'
new_row = '| 12 | Decide what pages to keep, strengthen, add, create or deliberately not create | ✅ COMPLETE / PASS AFTER FULL STRUCTURAL ACTION AUDIT |'
if old_row in report:
    report = report.replace(old_row, new_row, 1)
elif new_row not in report:
    raise RuntimeError('unexpected Step12 roadmap row in report')
report_path.write_text(report, encoding='utf-8')

manifest = manifest_path.read_text(encoding='utf-8')
heading = 'Current job authorities:\n\n'
start = manifest.index(heading) + len(heading)
end = manifest.index('\nWhere older Step-09', start)
raw = manifest[start:end]
lines = []
for line in raw.splitlines():
    x = line.strip()
    if not x or x in {'```text', '```'}:
        continue
    if x not in lines:
        lines.append(x)

# Keep the primary flow first and append Step12 authorities after upstream authorities.
if 'JOB_FLOW.md' in lines:
    lines.remove('JOB_FLOW.md')
    lines.insert(0, 'JOB_FLOW.md')
step12 = [x for x in lines if x.startswith('STEP_12_')]
lines = [x for x in lines if not x.startswith('STEP_12_')] + step12
new_block = '```text\n' + '\n'.join(lines) + '\n```\n'
manifest = manifest[:start] + new_block + manifest[end:]
manifest_path.write_text(manifest, encoding='utf-8')

print('STEP12_FINAL_CONSISTENCY_REPAIRED')
