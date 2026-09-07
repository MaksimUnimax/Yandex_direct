from pathlib import Path

ROOT = Path(__file__).resolve().parent
SRC = ROOT / 'OKNO_MSK_RESEARCH_RELEASE_CORRECTED_2026-09-05/sources/01_OKNO_MSK_CLIENT_RESEARCH_REPORT_RU_2026-09-05.md'
text = SRC.read_text(encoding='utf-8')

# Historical grammar cleanup only. The authoritative Alice-first customer contract
# is materialized by patch_document01_final_customer_contract.py before this hook.
text = text.replace(
    'Выдача Алисы была дополнительно проверена по восьми выбранным темам и помогли точнее сформулировать часть рекомендаций.',
    'Выдачу Алисы проверили по восьми выбранным темам; это помогло точнее сформулировать часть рекомендаций.'
)

assert 'Выдача Алисы была дополнительно проверена по восьми выбранным темам и помогли' not in text
assert 'Главная задача кворка — пересобрать и проверить поисковое ядро' in text
assert 'Восемь карточек ниже — не весь объём работы с Алисой' in text
SRC.write_text(text, encoding='utf-8')
print('DOCUMENT_01_FINAL_POLISH_PASS')
