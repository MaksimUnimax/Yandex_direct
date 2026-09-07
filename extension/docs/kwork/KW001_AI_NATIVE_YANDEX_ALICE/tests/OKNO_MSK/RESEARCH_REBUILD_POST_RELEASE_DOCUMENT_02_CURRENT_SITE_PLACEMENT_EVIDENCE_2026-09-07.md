# Report №02 — current-site placement evidence for second owner-review correction

Checked: **2026-09-07**  
Scope: public pages of `okno-msk.ru` used only to verify current headings, block order, exact insertion locations and visible portfolio objects.  
Provider acquisition calls: **0**.

This is repository evidence. Internal action IDs are retained here for traceability and are prohibited in the client-facing Markdown, DOCX and PDF.

## Ready action placement checks

| Internal action | Public page | Verified current preceding block | Verified current following block | Exact client instruction | Result |
|---|---|---|---|---|---|
| S18-A009 | https://okno-msk.ru/okna-rehau/francuzskie-okna | `Особенности французского остекления` | `Преимущества панорамных конструкций` | Insert immediately between those two sections. | PASS |
| S18-A010 | https://okno-msk.ru/okna-rehau/po-tipu-doma/okna-v-chastnyj-dom | `С нами купить окна для частного дома просто` | `Калькулятор окон для частного дома` | Insert immediately between those two sections. | PASS |
| S18-A026 | https://okno-msk.ru/stati/plyusy-i-minusy-ostekleniya-alyuminievymi-oknami | `Недостатки алюминиевых окон` | `Советы по остеклению балкона алюминиевым профилем` | Insert immediately between those two sections. | PASS |
| S18-A028 | https://okno-msk.ru/dveri-rehau | `Виды дверных створок` | `Фурнитура` | Insert immediately between those two sections. The later price and calculator blocks remain untouched. | PASS |
| S18-A029 | https://okno-msk.ru/nashi-raboty | H1 `Наши работы` | first visible portfolio card | Place filters immediately under H1 and before the first card; apply to the full 19-page collection. | PASS |
| S18-A030 | https://okno-msk.ru/alyuminievye-okna/ | `Особенности профилей Provedal` | `Выбор цвета по шкале RAL` | Insert immediately between those two sections. | PASS |
| S18-A031 | https://okno-msk.ru/stati/kakie-okna-samye-luchshie | `Рейтинг производителей оконных профилей` | existing producer list | Replace the exact current lead-in `В этом году рейтинг возглавляют:` directly before the list and add the historical-method boundary there. | PASS |

## Partial action placement check

| Internal action | Public page | Verified current preceding block | Verified current following block | Safe publishable location | Result |
|---|---|---|---|---|---|
| S18-A012 | https://okno-msk.ru/dveri-rehau | price paragraph in `Цены на ПВХ-двери Рехау`, ending with the estimate/free-measurement path | `Калькулятор дверей` | Add only the neutral installation-role sentence after the price paragraph and before the calculator heading. Company-specific inclusions remain blocked. | PASS |

## Portfolio inventory and mapping evidence

- The live portfolio contains **19 pages**.
- Pages 1–18 contain **12 visible cards each**; page 19 contains **8**.
- Total currently visible portfolio objects: **224**.
- Every card is mapped to `Все работы`.
- Additional categories are assigned only from direct words in the current visible card title; multiple categories are allowed.
- A card without an additional direct title signal remains only in `Все работы`.
- The category `Французские решения` is not supported by the current 224 titles and is excluded.
- The complete page/position/title/category mapping is preserved in `RESEARCH_REBUILD_POST_RELEASE_DOCUMENT_02_PORTFOLIO_MAPPING_EVIDENCE_2026-09-07.tsv`.

Current category totals:

| Client category | Current mapped cards |
|---|---:|
| Все работы | 224 |
| Балконы и лоджии | 116 |
| Веранды | 14 |
| Панорамное остекление | 13 |
| Алюминиевые конструкции | 7 |
| Тёплое остекление | 32 |
| Холодное остекление | 46 |

## Freshness conclusion

All seven ready-action pages and the partial-action location were read from the current public site on 2026-09-07. The final locations above supersede ambiguous placement wording preserved in older implementation authorities. No ordinary Yandex Search, Alice/GenSearch, Wordstat, Metrika, Direct or Webmaster private-data acquisition was performed.
