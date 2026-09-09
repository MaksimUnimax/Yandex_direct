# MK01 — PHASE 9 KWORK CARD QA

Status: **PASS / CARD TEXT RECONCILED TO XLSX + PDF CLIENT PACKAGE**

Market/card guidance refreshed 2026-09-09. No provider calls. No semantic data changes.

## QA ledger

| ID | Check | Result |
|---|---|---|
| C01 | Title contains clear service keyword «семантическое ядро» | PASS |
| C02 | Title avoids forced «для Яндекса» construction | PASS |
| C03 | Category matches existing-site product | PASS |
| C04 | Base price = 12,000 ₽ | PASS |
| C05 | Base delivery = 5 days | PASS |
| C06 | Site/region limits = 1/1 | PASS |
| C07 | Business directions <=10 stated | PASS |
| C08 | Governed phrase capacity <=1,500 stated correctly | PASS |
| C09 | Search capacity <=40 conditional | PASS |
| C10 | Seven-sheet XLSX described | PASS |
| C11 | Mandatory PDF report described | PASS |
| C12 | PDF purpose/content explained in client language | PASS |
| C13 | Handoff is message, not TXT report | PASS |
| C14 | Required buyer inputs complete | PASS |
| C15 | Private Yandex access/passwords not required | PASS |
| C16 | Yandex-only boundary explicit | PASS |
| C17 | Google excluded | PASS |
| C18 | Competitor Step5A not leaked | PASS |
| C19 | Query→URL / architecture / cannibalization / TZ not leaked | PASS |
| C20 | Alice/Neuro/AI not leaked | PASS |
| C21 | Wordstat metric not overclaimed | PASS |
| C22 | Rankings/traffic/leads/sales not guaranteed | PASS |
| C23 | +500 phrase add-on = 4,000 ₽ / +2 days | PASS |
| C24 | +10 Search add-on = 1,500 ₽ / +1 day | PASS |
| C25 | Over-capacity behavior prevents silent truncation | PASS |
| C26 | Existing-site-only mode explicit | PASS |
| C27 | Client-facing body contains no repo jargon | PASS |
| C28 | FAQ covers final delivery as XLSX + PDF | PASS |

Final: **28 PASS / 0 FAIL**.

## Final Phase 9 state

```text
CARD TEXT = READY
PRICE / LIMITS = RECONCILED
CLIENT INPUT BLOCK = READY
FAQ = READY
ADD-ONS = READY
DELIVERY = XLSX + PDF + HANDOFF MESSAGE
PUBLIC INTERNAL-JARGON LEAKAGE = 0
VISUAL = DEFERRED BY OWNER
```
