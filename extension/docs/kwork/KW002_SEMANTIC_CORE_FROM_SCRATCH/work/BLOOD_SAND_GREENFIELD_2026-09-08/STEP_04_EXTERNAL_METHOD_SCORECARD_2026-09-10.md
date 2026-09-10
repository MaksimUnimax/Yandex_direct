# STEP 04 — external-method scorecard

```text
AUDIT_VERDICT = REWORK_REQUIRED
QUALITY_SCORE_100 = 87/100
QUALITY_SCORE_10 = 8.7/10

A = 15/15
B = 18/20
C = 12/15
D = 12/15
E = 9/10
F = 13/15
G = 5/5
H = 3/5
TOTAL = 87/100 = 8.7/10

HARD_FAILS = NONE
MATERIAL_DEFECT_COUNT = 8
MINOR_DEFECT_COUNT = 2
FAMILY_ROWS_CHANGE_REQUIRED = F010,F011,F015,F017,F022,F025,F032
QUEUE_ROWS_CHANGE_REQUIRED = E004,E007,E014,E017
```

## Явные вычеты

| Категория | Макс. | Балл | Вычет | Основание |
| --- | ---: | ---: | ---: | --- |
| A. Полнота + provenance | 15 | 15 | 0 | 79/79, 25 979 occurrences, семейные run/seed/carrier locators и точная арифметика сохранены. |
| B. Business grounding + scope | 20 | 18 | -2 | F025 пропустил явный car-use; F017/F022 содержат неподтверждённые out-of-scope member decisions. |
| C. Semantic coherence | 15 | 12 | -3 | F010 umbrella, F011 false member, F015 слишком узкий label относительно состава. |
| D. Ambiguity/entity collisions | 15 | 12 | -3 | Bare “счастливый амулет” и “талисман кота” принудительно отнесены к OOS вместо mixed. |
| E. Noise + frequency discipline | 10 | 9 | -1 | Частотностных ошибок нет, но F011 показывает вероятный substring/token shortcut. |
| F. Coverage + expansion queue | 15 | 13 | -2 | F032 — низкоценный exact-form gap; E004/E017 и E007/E014 дублируются. |
| G. Step boundaries | 5 | 5 | 0 | Final cleanup/clustering/page/IA не выполнялись. |
| H. QA/reproducibility | 5 | 3 | -2 | Нет долговечной occurrence→family карты/правил, поэтому exact partition не реплицируется независимо. |

## TOP_5_STRENGTHS

1. 79/79 источников и полное числовое reconciliation 25 979 occurrences.
2. Контекстное разделение vehicle models, games, media, places, AUM и astrology.
3. Ноль low-frequency-only rejections и high-volume-only acceptances.
4. Реальная неоднозначность в основном оставлена видимой.
5. Строго соблюдена граница до final SERP clustering/page design.

## TOP_5_DEFECTS_OR_LIMITATIONS

1. Отсутствует occurrence-level partition ledger.
2. F011 содержит явную media-фразу в effects/audience.
3. F017/F022 принудительно отклоняют bare ambiguous phrases.
4. F025 теряет явный car-use member; F032 делает из покрытого синонима отдельный gap.
5. Две пары expansion rows дублируют один и тот же information need.

Жёстких fail-условий нет: не обнаружены silent source loss, sealed-source use, low-frequency-only rejection, систематический blacklist, premature page clustering или invented business facts. Вердикт `REWORK_REQUIRED` вызван совокупностью конкретных material semantic/queue/reproducibility defects, а не hard fail.
