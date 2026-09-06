from pathlib import Path

ROOT = Path(__file__).resolve().parent
P = ROOT / 'document01_build_commissioner_report.py'
s = P.read_text(encoding='utf-8')

# Historical workflow hook retained as a non-mutating compatibility guard.
for marker in [
    "TITLE = 'ОКНО МОСКВА — поисковое ядро сайта: спрос, обычный Яндекс и ответы Алисы'",
    "('Что показал ответ Алисы', row[2])",
    "'2 840 после очистки — это число уникальных поисковых формулировок'",
    "text.count('**Почему это важно:**') == 7"
]:
    assert marker in s, marker

print('DOCUMENT_01_CURRENT_BUILDER_GUARD_PASS')
