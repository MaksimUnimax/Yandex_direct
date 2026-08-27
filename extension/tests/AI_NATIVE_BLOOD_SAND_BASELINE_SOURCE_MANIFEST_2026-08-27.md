# AI-native blood_sand — clean Pass A source manifest

Date: 2026-08-27

Status: **BASELINE INPUT MANIFEST FROZEN / PASS A NOT RUN IN THIS CONTEXT**

Purpose: define an Alice-free evidence package for the mandatory one-time comparison in `extension/docs/AI_NATIVE_BLOOD_SAND_REQUIRED_COMPARATIVE_GATE.md`.

## 1. Exact source authority

Repository:

```text
MaksimUnimax/blood_sand
```

Frozen source commit for this manifest:

```text
0da1fdfa65155fe0b22d67838d366e7d214ccbbe
```

The experiment may read exact files at that commit. Later unrelated commits must not silently alter Pass A input.

## 2. Pass A operating rule

Pass A answers:

> What would a strong ordinary SEO / semantic-core analysis decide from business evidence, human demand and ordinary Yandex Search, without seeing Alice evidence or Alice-derived conclusions?

Pass A is analysis performed by ChatGPT, not an automated extension score.

## 3. Allowed canonical inputs

### Business / product / customer context

Allowed where needed and where the file itself does not contain Alice-derived conclusions:

```text
marketing/RESEARCH_BASELINE_2026-08-01.md
marketing/research/CUSTOMER_EVIDENCE_AUTO_PENDANTS_2026-08-01.md
marketing/research/R1_SEMANTIC_MAP_PECHAT_VELESA_2026-08-01.md
```

These establish the business/product context before the later Alice research.

### Human-demand evidence

Canonical summary:

```text
marketing/research/R1_WORDSTAT_FINAL_REPORT_2026-08-12.md
```

Canonical supporting Wordstat datasets:

```text
marketing/data/normalized/wordstat/
marketing/data/raw/wordstat/
```

The baseline may use directly measured demand, precision, dynamics, region/device evidence and query-family observations. It must not infer Alice importance from frequency.

### Ordinary Yandex Search evidence

Canonical provider summary:

```text
marketing/research/R2_YANDEX_SEARCH_PRIMARY_SERP_2026-08-26.md
```

Canonical direct Search datasets:

```text
marketing/data/normalized/yandex_search/20260826__search__primary10__225.tsv
marketing/data/normalized/yandex_search/20260826__search__primary10__measurements.csv
marketing/data/normalized/yandex_search/20260826__search__primary10__summaries.csv
marketing/data/normalized/yandex_search/20260826__search__secondary_A1__obereg_po_znaku_zodiaka__225.csv
marketing/data/normalized/yandex_search/20260826__search__secondary_A2__pechat_velesa_znachenie__225.csv
marketing/data/normalized/yandex_search/20260826__search__secondary_A3__amulet_v_mashinu__225.csv
marketing/data/normalized/yandex_search/20260826__search__secondary_B1__vegvizir_znachenie__225.csv
marketing/data/normalized/yandex_search/20260826__search__secondary_B2__shlem_uzhasa_obereg__225.csv
```

Raw Search files under `marketing/data/raw/yandex_search/` are also allowed when needed to verify exact evidence.

### Browser ordinary-SERP evidence

Browser Search snapshots are allowed only when they contain ordinary Search/UI evidence and no Alice answer/content has been merged into the file.

Known ordinary browser SERP directory:

```text
marketing/data/raw/browser_serp/
```

Browser evidence must remain distinct from Search API evidence.

## 4. Explicitly forbidden in Pass A

Do **not** expose any of the following before Pass A is frozen:

```text
marketing/data/raw/alice/
marketing/data/normalized/alice/
marketing/research/R2_PRIMARY_SEARCH_ALICE_COMPARISON_2026-08-26.md
marketing/research/R2_YANDEX_SERP_ALICE_FINAL_REPORT_2026-08-26.md
marketing/research/R3_OPPORTUNITY_SCORING_2026-08-26.md
marketing/research/R3_OPPORTUNITY_OVERLAP_AND_JOB_BOUNDARIES_2026-08-26.md
marketing/research/R3_OPPORTUNITY_MAP_FINAL_2026-08-26.md
marketing/data/normalized/opportunity_map/
```

The following is also forbidden in Pass A unless a clean Alice-free projection is generated first:

```text
marketing/data/ledger/query_evidence_ledger.csv
```

Reason: the canonical ledger is a cross-surface artifact and can leak Alice-derived evidence/conclusions.

Any other document that quotes or summarizes Alice results, H/A/C/O values derived using Alice, final R3 decisions, or cross-surface conclusions is forbidden even if it is not listed above.

## 5. Known baseline facts that are allowed

These examples come from Wordstat/Search evidence and may legitimately influence Pass A:

- `славянские обереги`: large human demand; ordinary Search is commercial/category-first with strong specialist independent participation.
- `печать велеса`: meaningful demand; ordinary Search is strongly transactional/product-oriented and marketplace-heavy; explicit `значение` is a separately measured Search question.
- `оберег в машину`: ordinary Search is mixed commercial + choice/use-case.
- `подвеска на зеркало в машину`: ordinary Search is near-pure form-factor transaction and platform-heavy.
- `вегвизир`: ordinary Search mixes entity and commerce; `вегвизир значение` exists as a separate measured Search question.
- `талисман знак зодиака`: broad demand is heavily contaminated; ordinary Search is guide/selection-heavy with stones/jewelry contamination.
- `алатырь оберег`: ordinary Search is commercial-first with meaning support.
- `оберег велес`: ordinary Search is commercial-first with strong niche independent competition.
- generic automotive gift roots have real shopping demand but weak direct pendant-category fit in ordinary Search.

These are baseline observations, not Alice conclusions.

## 6. Anti-leakage status of the current ChatGPT conversation

The current conversation has already inspected and discussed canonical Alice-derived `blood_sand` conclusions.

Therefore:

```text
PASS_A_IN_CURRENT_CONVERSATION = INVALID_BASELINE_LEAKAGE
```

This is not a failure of the method or evidence. It simply means a valid independent Pass A must be produced in a clean analysis context that receives only this manifest's allowed inputs.

No false Pass A will be manufactured in the contaminated context.

## 7. Required clean Pass A output

The clean context must freeze at least:

```text
candidate clusters
intent per cluster
KEEP / INVESTIGATE / REJECT reasoning
priority
page-job recommendation
split / merge decisions
confidence
missing evidence
broad-demand contamination decisions
```

It must not mention Alice, AI-source evidence, H/A/C/O Alice importance, or final R3 outcomes.

Required output path after the independent run:

```text
extension/tests/AI_NATIVE_BLOOD_SAND_BASELINE_PASS_A_2026-08-27.md
```

## 8. Pass B source expansion

Only after Pass A is frozen, Pass B may add:

```text
marketing/data/raw/alice/
marketing/data/normalized/alice/
marketing/research/R2_PRIMARY_SEARCH_ALICE_COMPARISON_2026-08-26.md
marketing/research/R2_YANDEX_SERP_ALICE_FINAL_REPORT_2026-08-26.md
```

Then ChatGPT may build the AI-native result and compare it with the immutable baseline.

R3 final/opportunity artifacts should be used as an external consistency/reference check after Pass B decisions are independently written, not as a shortcut that predetermines the answer.

## 9. Product implication

This manifest unblocks honest execution of the methodology gate but does not block market-proven Phase 6 work.

```text
Alice-specific engineering → waits for valid comparative verdict
Semantic Core / batch-orchestration Phase 6 → may proceed now
```