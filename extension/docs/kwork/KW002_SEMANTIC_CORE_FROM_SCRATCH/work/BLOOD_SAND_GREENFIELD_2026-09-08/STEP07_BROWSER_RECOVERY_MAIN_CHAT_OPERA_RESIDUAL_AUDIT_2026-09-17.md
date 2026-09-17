# KW-002 / BLOOD & SAND — STEP07 MAIN CHAT OPERA RESIDUAL AUDIT

Date: 2026-09-17
Status: **BROWSER OUTCOME CLOSURE PASS / DURABLE PAGE-EVIDENCE MATERIALIZATION STILL REQUIRED**

## 1. Scope

Authority: `STEP07_BROWSER_RECOVERY_RESIDUAL_CORRECTION_SET_2026-09-17.csv`.

Only rows with `browser_retry_required=true` were retried through the owner-connected Opera Browser Connector.

```text
FROZEN_BROWSER_RETRY_ROWS = 90
URL_UNIVERSE_EXPANDED = false
WORDSTAT_CALLS = 0
YANDEX_SEARCH_PROVIDER_CALLS = 0
AI_SEARCH_OR_GENSEARCH_CALLS = 0
STEP08_STARTED = false
SEMANTIC_CANDIDATE_CLASSIFICATION = false
```

This pass used normal public browser navigation only. No CAPTCHA, anti-bot, login, security or robots bypass was performed.

## 2. Final Opera browser outcomes

```text
RECOVERED_READABLE = 70
TARGET_CAPTCHA_OR_ANTI_BOT = 20
EXECUTION_ENVIRONMENT_FAILURE = 0
UNRESOLVED_DYNAMIC_CONTENT = 0
TOTAL = 90
```

Therefore, at the URL-outcome level:

```text
FINAL_RESIDUAL_ACQUISITION_GAPS = 0
BROWSER_OUTCOME_CLOSURE = PASS
```

Important boundary:

```text
BROWSER_OUTCOME_CLOSURE PASS
!= FULL DURABLE PAGE-EVIDENCE MATERIALIZATION PASS
!= STEP07 BROWSER RECOVERY ACCEPTED YET
```

The 70 readable pages still require their rendered candidate-bearing page evidence to be durably materialized before the accepted recovery package can be rebuilt and semantic Work released.

## 3. Exact recovered IDs — 70

### Wildberries — 5 readable

```text
R9-S07U000008
R9-S07U000010
R9-S07U000014
R9-S07U000016
R9-S07U000018
```

Observed normal rendered category pages included:

- `Амулет и оберег`;
- `Домашний оберег на удачу`;
- `Обереги и амулеты славянские`;
- `Подкова настоящая`;
- `Символ ом`.

### Yandex Market — 20 readable

```text
R9-S07U000051
R9-S07U000052
R9-S07U000053
R9-S07U000054
R9-S07U000055
R9-S07U000056
R9-S07U000057
R9-S07U000058
R9-S07U000059
R9-S07U000060
R9-S07U000062
R9-S07U000063
R9-S07U000064
R9-S07U000065
R9-S07U000066
R9-S07U000067
R9-S07U000068
R9-S07U000069
R9-S07U000071
R9-S07U000073
```

Normal rendered categories/search result pages were observed with matching query/category headings and product results.

### Livemaster — 11 readable

```text
R9-S07U000074
R9-S07U000075
R9-S07U000076
R9-S07U000077
R9-S07U000078
R9-S07U000079
R9-S07U000080
R9-S07U000081
R9-S07U000082
R9-S07U000083
R9-S07U000084
```

Normal rendered marketplace/article pages were observed, including `Славянские обереги`, `Талисман удачи`, `Краткое описание и амулетные значения рун Старшего Футарка`, `Символ ОМ`, `Обережная вышивка`, `Славянские символы`, and `Амулеты, талисманы, обереги — в чем разница`.

### Avito — 8 readable

```text
R9-S07U000085
R9-S07U000088
R9-S07U000089
R9-S07U000090
R9-S07U000091
R9-S07U000092
R9-S07U000093
R9-S07U000094
```

Opera rendered normal Avito search pages rather than the Codex Browser Use safety block. Readable query result headings included:

- `Будда статуэтка бронза`;
- `Молот тора серебро`;
- `Молот тора`;
- `Мусульманский оберег`;
- `Мьёльнир`;
- `Подкова для лошади`;
- `Статуэтка будды`;
- `Статуэтка будды: объявления в Москве`.

### Joom — 2 readable

```text
R9-S07U000097
R9-S07U000098
```

Normal rendered category/product content was readable.

### ru.wikipedia.org — 1 readable

```text
R9-S07U000118
```

`Христианская символика` rendered as normal article content.

### ru.ruwiki.ru — 8 readable

```text
R9-S07U000119
R9-S07U000120
R9-S07U000122
R9-S07U000123
R9-S07U000124
R9-S07U000125
R9-S07U000127
R9-S07U000128
```

All eight normal article pages rendered after ordinary wait; no bypass was used.

### kartaslov.ru — 4 readable

```text
R9-S07U000155
R9-S07U000159
R9-S07U000396
R9-S07U001526
```

Normal public pages for `писание`, `Фома`, `дом`, and `нашла коса на камень` were readable. The site's ordinary `НАУЧИ БОТА!` / `Лампобот` contribution widget is page UI, not an access challenge.

### sibpodkova.ru — 3 readable

```text
R9-S07U001903
R9-S07U001904
R9-S07U001905
```

Homepage, `Кузница`, and `Подковы` rendered normally.

### azbyka.ru — 4 readable

```text
R9-S07U001947
R9-S07U001948
R9-S07U001949
R9-S07U001950
```

The pages rendered normal article content. `https://azbyka.ru/krest` initially showed a DDoS-Guard browser-verification title, then completed the ordinary browser verification automatically and rendered the article without any bypass. Final state is readable content, not target block.

### goroskop365.ru — 4 readable

```text
R9-S07U001959
R9-S07U001960
R9-S07U001961
R9-S07U001962
```

Normal public rune/guidance pages rendered, including the rune section and pages for `Альгиз`, `Феху`, and `Отал`.

## 4. Exact legitimate target blocks — 20

### Wildberries VPN target page — 18

Every ID below was navigated individually. Opera reached a Wildberries-branded target page stating in substance:

```text
Возможно, нужно выключить VPN
Не смогли загрузить страницу: попробуйте выключить VPN.
```

No bypass was attempted.

```text
R9-S07U000001
R9-S07U000002
R9-S07U000003
R9-S07U000004
R9-S07U000005
R9-S07U000006
R9-S07U000007
R9-S07U000009
R9-S07U000011
R9-S07U000012
R9-S07U000013
R9-S07U000015
R9-S07U000017
R9-S07U000019
R9-S07U000020
R9-S07U000021
R9-S07U000022
R9-S07U000023
```

Final class: `TARGET_CAPTCHA_OR_ANTI_BOT` / target VPN block evidence.

### AliExpress verification target page — 2

Fresh-tab retries for both exact URLs reached AliExpress target verification pages with title:

```text
Пройдите проверку
```

and AliExpress `/_____tmd_____/punish?x5secdata=...` challenge URLs.

No verification/CAPTCHA/anti-bot bypass was attempted.

```text
R9-S07U000095
R9-S07U000096
```

Final class: `TARGET_CAPTCHA_OR_ANTI_BOT`.

Earlier Opera `ERR_TIMED_OUT` observations are superseded by these later successful target-level challenge observations.

## 5. Reconciliation

```text
WILDBERRIES = 5 readable + 18 target block = 23
MARKET = 20 readable
LIVEMASTER = 11 readable
AVITO = 8 readable
ALIEXPRESS = 2 target block
JOOM = 2 readable
RU_WIKIPEDIA = 1 readable
RUWIKI = 8 readable
KARTASLOV = 4 readable
SIBPODKOVA = 3 readable
AZBYKA = 4 readable
GOROSKOP365 = 4 readable

READABLE = 70
TARGET_BLOCK = 20
ENVIRONMENT_FAILURE = 0
UNRESOLVED = 0
TOTAL = 90
```

## 6. Next required action

Do not rerun these 90 URLs through Codex Browser Use.

Next complete unit:

```text
MATERIALIZE DURABLE RENDERED PAGE EVIDENCE FOR THE 70 READABLE OPERA PAGES
+ MERGE THE 20 TARGET-BLOCK OUTCOMES
+ REBUILD FINAL 7-FILE BROWSER-RECOVERY PACKAGE
+ RUN MAIN CHAT RETURN QA
```

Until the 70 readable page-evidence records are durably materialized and the final package reconciles:

```text
STEP07_BROWSER_RECOVERY_ACCEPTED = false
STEP07_SEMANTIC_REWORK = BLOCKED
STEP08 = BLOCKED_NOT_STARTED
```
