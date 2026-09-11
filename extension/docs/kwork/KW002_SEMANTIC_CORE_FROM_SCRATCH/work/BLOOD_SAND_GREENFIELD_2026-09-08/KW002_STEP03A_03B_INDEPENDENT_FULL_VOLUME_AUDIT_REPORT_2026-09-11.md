# KW-002 Blood & Sand — independent methodology and full-volume Step03A/03B return audit

Date: 2026-09-11  
Repository: `MaksimUnimax/Yandex_direct`  
Branch: `roadmap/kwork-productization-2026-08-28`  
Live remote authority audited: `a0d662851c2f26d7a219ec7efb7d7e37e640dce3`  
Job root: `extension/docs/kwork/KW002_SEMANTIC_CORE_FROM_SCRATCH/work/BLOOD_SAND_GREENFIELD_2026-09-08`

## A. Executive verdict

**FINAL VERDICT: `CRITICAL_REWORK_REQUIRED`.**

Step03A independently passes. Its NFC/whitespace/case comparison key is conservative; exact deduplication is correct; all 25,979 RAW occurrences are recoverable through lineage; none of the three word-order/implicit groups was collapsed.

Step03B does not pass. Mechanical completeness concealed systematic semantic defects in both directions:

- **758 / 6,752 current AUTO_EXCLUDED identities (11.2263%) are not safe exclusions** under a high-precision exclusion policy: 14 should be KEEP and 744 must be restored to HOLD pending sufficient context.
- **286 / 5,074 current KEEP identities (5.6366%) are not safe keeps**: 79 are explicit foreign intents and 207 require HOLD.
- **666 / 12,750 HOLD identities (5.2235%) are resolution opportunities** using already frozen evidence: 298 to KEEP and 368 to EXCLUDE. The other 12,084 remain genuine uncertainty and should survive.
- Corrected audited partition: **KEEP 5,100; HOLD 13,035; EXCLUDE 6,441**.
- All transitions reconcile to **24,576 normalized identities and 25,979 RAW occurrences; zero silent loss**.

The critical defect is not data loss in storage. It is unsupported semantic destruction caused by broad single-pattern exclusions and an incomplete positive-token fallback. The correction is a **full-volume, rule-only Step03B reprocess**. Step03A does not need reprocessing; no provider calls are required.

## B. Sources researched with URLs and dates

The sources below were located and checked independently on 2026-09-11. “Current/undated” means the page exposes no publication date suitable for citation.

| ID | Source | Publisher | Publication/update date | Methodological claim supported | Scope |
|---|---|---|---|---|---|
| S01 | [Unicode Standard Annex #15: Unicode Normalization Forms, rev. 57](https://www.unicode.org/reports/tr15/tr15-57.html) | Unicode Consortium | 2025-07-30 | NFC preserves canonical equivalence; NFKC applies compatibility mappings and must not be blindly applied where semantic distinctions can matter. | General technical standard |
| S02 | [Операторы Вордстата](https://yandex.ru/support2/wordstat/ru/content/operators) | Яндекс | Current/undated | `!` fixes word form and `[]` fixes word order; Yandex therefore exposes word order as a demand distinction rather than a universally disposable property. | Yandex-specific |
| S03 | [Подбор поисковых запросов и анализ рынка β](https://yandex.ru/support/webmaster/ru/service/queries-selection) | Яндекс Вебмастер | Current/undated | Minus words filter non-target context; the service finds additional/non-obvious queries and supplies demand/competition/cluster signals. | Yandex-specific |
| S04 | [Какие аспекты влияют на ранжирование в Поиске и попадание в ответы Алисы AI](https://yandex.ru/support/webmaster/ru/epos) | Яндекс Вебмастер | Current/undated | Relevance is correspondence to the real user task; a useful page helps the user solve, choose or order. | Yandex-specific |
| S05 | [Яндекс Вордстат — справка](https://yandex.ru/support2/wordstat/ru/) | Яндекс | Current/undated | Wordstat is demand evidence: query statistics, regional popularity, dynamics and related searches. | Yandex-specific |
| S06 | [Структура сайта](https://yandex.ru/support/webmaster/ru/recommendations/site-structure) | Яндекс Вебмастер | Current/undated | Site sections and linking should be clear; duplicate/technical pages do not provide unique value. | Yandex-specific |
| S07 | [Удаление неявных дублей](https://topvisor.com/ru/support/implicit-duplicates/) | Topvisor | 2026-03-23 | Implicit duplicates use stemming plus heuristics/context; ignoring word order and stop words is configurable; frequency is not part of duplicate identity. | General SEO practice |
| S08 | [Поиск неявных дублей](https://www.key-collector.ru/docs/tools/implicit-duplicates/) | Key Collector | Current/undated | Exact and word-order/form-independent duplicate modes are distinct and require configurable rules rather than blind merging. | General SEO practice |
| S09 | [Как чистить семантическое ядро, какие запросы удалять и почему](https://journal.topvisor.com/ru/seo-kitchen/how-to-understand-from-which-requests-clean-the-core/) | Topvisor Journal | 2025-04-04 | Clean obvious non-target/junk progressively; word order can change meaning; SERP helps resolve intent; low/zero volume is not a universal deletion rule. | General SEO practice |
| S10 | [Keyword Intent: What It Is and How to Use It](https://ahrefs.com/blog/keyword-intent/) | Ahrefs | 2026-03-13 | Informational, commercial, transactional and navigational are useful but mixed intent exists; ambiguous cases require SERP review and volume alone is not the first filter. | General SEO practice |
| S11 | [How To Do Keyword Clustering the Easy Way](https://ahrefs.com/blog/keyword-clustering/) | Ahrefs | 2023-10-31 | Same/similar SERPs are evidence of shared intent; one page can target multiple compatible keywords; clustering methods remain imperfect. | General SEO practice |
| S12 | [How to Do Keyword Clustering & Why It Helps SEO](https://www.semrush.com/blog/keyword-clustering/) | Semrush | 2025-10-29 | Cluster queries with the same intent on one page; competitor research can fill vocabulary gaps; SERP similarity and page type matter. | General SEO practice |
| S13 | [What Is Search Intent? How to Identify It & Optimize for It](https://www.semrush.com/blog/search-intent/) | Semrush | 2024-11-21 | Intent categories can overlap; context and the actual result-page composition should inform classification and page format. | General SEO practice |

Official Yandex evidence takes precedence for Yandex demand and user-task concepts. Ahrefs/Semrush/Topvisor/Key Collector are used as general methodology support, not as Blood & Sand demand evidence.

## C. External best-practice synthesis

### C1. Text/query normalization

NFC is appropriate for canonical Unicode equivalence without compatibility folding. NFKC can erase meaningful distinctions (for example, superscripts, fractions or styled compatibility characters), so it should not be the default for arbitrary query text [S01]. Whitespace trimming/collapse and case-folding are safe for an **identity comparison key** only when the original text remains stored.

Exact duplicates may collapse only when the conservative normalized keys are identical and all occurrence provenance remains attached. Implicit duplicates are hypotheses. Same tokens in another order cannot be collapsed automatically: Yandex Wordstat explicitly provides a word-order operator [S02], and professional duplicate tools make word-order ignoring optional [S07, S08].

### C2. Semantic-core sanitation

Sanitation should be staged:

1. remove malformed/technical noise and explicit foreign referents;
2. apply context-aware minus-word logic;
3. retain collisions and multi-meaning queries;
4. defer unresolved intent to family/SERP evidence;
5. only then decide delivery and priority.

A minus word or blacklist token is evidence, not a verdict. “Лада”, “серия”, “банк”, “дом”, “читать” and stems such as `футбол*` all have collisions in this corpus. Low or zero volume is not an exclusion rule: it can affect evidence budget or priority, but not business truth [S03, S07, S09].

### C3. Search intent

Informational, commercial, transactional and navigational labels are helpful coarse categories, but real queries can be mixed [S10, S13]. Lexical heuristics can identify obvious cases; they cannot safely resolve all ambiguous ones. Step03B should therefore preserve `HOLD_AMBIGUOUS`/`SERP_REQUIRED_LATER` instead of equating “informational-looking” with rejection. Yandex's user-task framing makes actual task satisfaction the target [S04].

### C4. Family triage

Broad family categorization is useful to expose collision zones, quantify evidence gaps and schedule later work. It is not final query-level clustering. A family can contain multiple intents and page types; its label cannot silently overwrite a contradictory phrase-level referent.

### C5. Demand expansion

Synonyms, non-obvious queries and competitor vocabulary are discovery inputs. Yandex's query-selection tooling explicitly supports additional queries [S03]. Competitor text can add candidate vocabulary [S12], but it does not prove Yandex demand or business fit. Discovered terms require current demand validation and frozen-assortment checking before acceptance.

### C6. SERP-based clustering

Overlapping ranked URLs are evidence that engines see similar user tasks [S11, S12]. A fixed overlap threshold is not sufficient by itself: mixed-intent SERPs, dominant result types and intent drift can break a mechanical threshold. Reproducibility requires query, engine, region, device, collection time, depth/rank and ranked URL evidence.

### C7. Query-to-page mapping

One query does not imply one page. Compatible primary/secondary phrases can belong to a shared category, product, landing or informational page [S11, S12]. Page type must match the dominant task/result type. Thin near-duplicates and cannibalizing pages should be prevented [S06].

## D. MAIN_CHATGPT_VS_WORK_METHODOLOGY_RECONCILIATION

| # | Main ChatGPT conclusion | Independent finding | Status | Evidence | KW002 consequence |
|---:|---|---|---|---|---|
| 1 | Step03A should be conservative/lossless: NFC, whitespace, case comparison, exact dedup; aggressive compatibility folding unsafe. | Confirmed technically and mechanically. | AGREE | S01; full 25,979-row audit | Keep Step03A unchanged. |
| 2 | Same-token/different-order queries must not automatically collapse. | Confirmed; Wordstat and duplicate tools treat order as an explicit/configurable property. | AGREE | S02, S07, S08 | Preserve all three implicit groups in HOLD. |
| 3 | Step03B should optimize for high-precision exclusion: clear off-topic exclude, clear business keep, uncertainty hold. | Confirmed, but implementation violated it through broad early regexes. | AGREE | S03, S09, S10; transition audit | Reprocess all Step03B identities with collision-aware ordering. |
| 4 | Step03B is not final intent classification. | Confirmed. | AGREE | S04, S10, S13 | Generic information/media tokens cannot alone cause rejection. |
| 5 | Low frequency alone is not a valid exclusion criterion. | Confirmed. | AGREE | S07, S09, S10 | Preserve low/zero demand as evidence/priority fields, not sanitation verdicts. |
| 6 | Family triage should resolve contextual families before expensive row-level work, but is not final clustering. | Family triage is useful, but “resolve” must mean prioritize/contextualize, not propagate one family verdict to every phrase. | PARTIAL | S11, S12; corrected Step04 cross-check | Use family context as a guardrail and evidence budget, retain phrase-level exceptions. |
| 7 | Competitor vocabulary needs demand validation before becoming final demand. | Confirmed. | AGREE | S03, S05, S12 | Step07 adds candidates; Step08 validates them. |
| 8 | Nuanced intent should use actual SERP evidence where lexical interpretation is insufficient. | Confirmed. | AGREE | S04, S10, S11, S13 | Route unresolved collisions to SERP_REQUIRED_LATER. |
| 9 | Final clustering should combine task/intent, SERP overlap and page/result type. | Confirmed. | AGREE | S04, S11, S12, S13 | Step13 must not cluster on lexical similarity alone. |
| 10 | Query-to-page mapping should be cluster/task based, not one phrase per page. | Confirmed. | AGREE | S06, S11, S12 | Step14 must group compatible queries and prevent cannibalization. |
| 11 | Selecting delivery/Search scope before SERP may discard valuable ambiguity before the needed evidence exists. | Risk confirmed. The selection must be an evidence-budget queue, not a relevance verdict. | AGREE | S04, S10, S11 | Step11 must preserve deferred rows and guarantee collision/family coverage. |

## E. Step03A full-volume audit

### E1. Scope and mechanical reproduction

- RAW files traversed: 96; bytes: 2,136,069.
- RAW occurrences reconstructed: 25,979.
- Results: 24,722; associations: 1,257.
- Unique occurrence IDs: 25,979.
- RAW-to-accepted occurrence authority mismatches: 0.
- Normalized identities: 24,576.
- Normalization-key mismatches across all ledger rows: 0.
- Pool aggregation/provenance mismatches: 0.
- RAW lineage loss: 0.

### E2. Semantic safety

- NFC: appropriate and correctly applied.
- Case folding: comparison-only. `canonical_phrase` retains the first normalized observed form; every original variant remains in `raw_phrase_variants` and each occurrence in `all_raw_occurrence_ids`.
- Whitespace: leading/trailing and repeated whitespace only.
- Digits/punctuation: not stripped. The pool contains 2,383 digit-bearing and 46 punctuation-bearing canonical rows; all matched the first-source canonicalization. No hyphen-bearing canonical row occurred in this universe.
- Exact duplicate groups: 1,181.
- Collapsed exact duplicate occurrences: 1,403.
- Every collapsed occurrence retains its raw ID and provenance.
- No supposedly exact group contained a different conservative normalized key.
- Implicit groups: 3; accepted/collapsed: 0; HOLD: 3.
- No undisclosed digit, punctuation, hyphen, word-order, stemming, stop-word or compatibility normalization was found.
- Counterfactual NFKC introduced no additional cross-key collision in this particular corpus, but that does not make blind NFKC methodologically safe [S01].

**Independent Step03A verdict: PASS.**

## F. Step03B full-volume audit

All 24,576 identities were independently assigned KEEP, HOLD or EXCLUDE using frozen client evidence and a high-precision exclusion policy. The audit did not infer a global verdict from a sample. The full row overlay stores phrase, current state/reason, audit state/verdict/basis/confidence, raw count/IDs and Step04 family context.

| State | Current | Audited | Difference |
|---|---:|---:|---:|
| KEEP | 5,074 | 5,100 | +26 |
| HOLD | 12,750 | 13,035 | +285 |
| EXCLUDE | 6,752 | 6,441 | -311 |
| Total | 24,576 | 24,576 | 0 |

The small net changes hide 1,710 row-level transitions. The dangerous result is not simply “too many” or “too few” rows; it is incorrect membership in all three states.

The most important code defects are ordered broad exclusions before collision checks, and a broad positive fallback after an incomplete blacklist. The current regexes include `футбол\w*`, `банк\w*`, `купить.*дом`, generic media actions, generic game/model stems, and vehicle brands before catalog checks. Conversely, named games such as Hollow Knight/Elden/PoE and several vehicle-part terms were absent from the negative guards, so a product token defaulted them into KEEP.

**Independent Step03B verdict: FAIL.**

## G. Reason-code precision table

Precision below is the proportion whose EXCLUDE outcome remained confirmed; “same-outcome rule defect” counts remain EXCLUDE but reveal an unsafe/misleading rule. Counts are normalized identities; RAW counts show lineage-weighted impact.

| Current reason | Rows | Confirmed EXCLUDE | Same outcome, rule defect | → KEEP | → HOLD | Estimated precision | RAW total / confirmed / →KEEP / →HOLD | Systematic defect | Safe unchanged |
|---|---:|---:|---:|---:|---:|---:|---|---|---|
| `EXCLUDE_EXPLICIT_ASTROLOGY_INFORMATION` | 2,219 | 1,901 | 0 | 4 | 314 | 85.6692% | 2,669 / 2,320 / 4 / 345 | YES | NO |
| `EXCLUDE_EXPLICIT_FOREIGN_ENTITY` | 74 | 38 | 12 | 0 | 36 | 51.3514% | 75 / 39 / 0 / 36 | YES | NO |
| `EXCLUDE_EXPLICIT_GAME` | 242 | 204 | 0 | 0 | 38 | 84.2975% | 246 / 207 / 0 / 39 | YES | NO |
| `EXCLUDE_EXPLICIT_MEDIA` | 1,667 | 1,385 | 26 | 0 | 282 | 83.0834% | 1,682 / 1,395 / 0 / 287 | YES | NO |
| `EXCLUDE_EXPLICIT_ORGANIZATION` | 9 | 8 | 1 | 0 | 1 | 88.8889% | 9 / 8 / 0 / 1 | YES | NO |
| `EXCLUDE_EXPLICIT_PERSON` | 23 | 23 | 0 | 0 | 0 | 100% | 23 / 23 / 0 / 0 | NO | YES |
| `EXCLUDE_EXPLICIT_PLACE` | 340 | 320 | 0 | 8 | 12 | 94.1176% | 340 / 320 / 8 / 12 | YES | NO |
| `EXCLUDE_EXPLICIT_RELIGIOUS_PRACTICE` | 120 | 120 | 0 | 0 | 0 | 100% | 127 / 127 / 0 / 0 | NO | YES |
| `EXCLUDE_EXPLICIT_VEHICLE_OR_MODEL` | 554 | 525 | 1 | 2 | 27 | 94.7653% | 562 / 530 / 2 / 30 | YES | NO |
| `EXCLUDE_LEXICAL_GARBAGE` | 1,225 | 1,191 | 0 | 0 | 34 | 97.2245% | 1,229 / 1,195 / 0 / 34 | YES | NO |
| `EXCLUDE_TECHNICAL_NOISE` | 65 | 65 | 0 | 0 | 0 | 100% | 65 / 65 / 0 / 0 | NO | YES |
| `EXCLUDE_UNRELATED_PRODUCT` | 214 | 214 | 0 | 0 | 0 | 100% | 216 / 216 / 0 / 0 | NO | YES |

Representative confirmed exclusions include explicit horoscope/compatibility tasks, explicit books/chapters/films, named games, Chery Amulet/Renault Talisman parts, industrial AUMA queries, explicit people/places, perfume/phone/tomato products and explicit prayer text. Representative failures are detailed below and fully enumerated in the row overlay.

## H. Astrology/zodiac collision audit

The frozen assortment contains all 12 zodiac signs and “Античность”/“Символы” variants. The current astrology rule nevertheless runs before adequate catalog collision logic.

- Current AUTO_EXCLUDED: 2,219.
- Confirmed explicit astrology information: 1,901.
- Must become KEEP: 4.
- Must become HOLD: 314.
- Estimated exclusion precision: 85.6692%.

Correctly excluded examples: `гороскоп по знакам зодиака`, `какой знак зодиака`, `звезда в созвездии льва`.

False exclusions to KEEP: `кулон дева знак зодиака с камнем`, `лев знак зодиака камень для мужчин купить`, `камень для знака зодиака рыбы браслет`, `телец знак зодиака женщина подвеска`.

Unsafe exclusions requiring HOLD include `камни по знаку зодиака` and similar stone/sign collisions. The audit does not assert that all such rows belong in final delivery; it asserts that lexical astrology evidence alone is insufficient to destroy them before later business/SERP resolution.

## I. Religious-product collision audit

The current 120 `EXCLUDE_EXPLICIT_RELIGIOUS_PRACTICE` identities are all confirmed: their actual phrases express prayer, icon, church, mantra or other practice without a sufficiently supported physical product referent. Examples include `молитва оберегающая` and `сильные оберегающие молитвы`.

The broader universe still contains two important preserved collision groups:

- 147 product-versus-religious-practice identities;
- 28 frozen catalog-name-versus-religious-text identities.

These correctly belong in HOLD unless physical product/commercial evidence is explicit. The rule must continue to recognize `Спаси и Сохрани`, `Молитва Иоанн Златоуст`, `Ом/Аум` and their inflections as frozen catalog evidence. The absence of a false exclusion inside the current 120 does not justify deleting those collision exceptions.

## J. Vehicle/product collision audit

The client explicitly sells automobile-use talismans/rosaries. At the same time, Chery Amulet and Renault Talisman are foreign vehicle/model intents.

- Current vehicle AUTO_EXCLUDED: 554.
- Confirmed explicit model/part: 525.
- Must become KEEP: 2.
- Must become HOLD: 27.
- Estimated precision: 94.7653%.

Correct exclusion: `чери амулет`, `амулет а15`, explicit engine/part/paint/model queries.

KEEP: `четки в машину знак lada` (supported automobile-use product); `звезда лада купить` (frozen catalog name plus commerce).

HOLD: `звезда лада значение`, `оберег звезда лада`, product-name/vehicle-paint collisions. The branch order must test the frozen “Звезда Лады” title and automobile-use product context before generic brand rejection.

The positive fallback also missed explicit vehicle parts: current KEEP contains `амулет датчики`, `датчик температуры амулет`, `диски амулет` and related rows. These contribute to the 79 KEEP→EXCLUDE defects.

## K. Unrelated-product audit

All 214 current `EXCLUDE_UNRELATED_PRODUCT` identities (216 RAW occurrences) are confirmed. Examples: perfume/Blue Talisman, phone, tomato/seed, medicine, furniture, clothing and local-entity collisions not represented in the frozen assortment.

The reason can remain, but only as an explicit phrase-level class. It must not become a generic “not in current keyword list” catch-all. Physical object words can be ambiguous, and the frozen catalog remains the authority.

## L. Entity/media/game/place/person audit

### Entity/organization/person

- Person: 23/23 confirmed explicit blogger/writer/athlete queries.
- Organization: 8/9 confirmed; `как любить знак зодиака рыбы яндекс дзен` requires HOLD because organization regex is not the right evidence. The bank-card zodiac sticker remains excluded as an unrelated product but exposes a reason-code defect from `банк\w*`.
- Foreign entity/sport: only 38/74 remain confirmed under the high-precision reason; 36 require HOLD. `футбол\w*` also matches `футболка`, so the rule is unsafe even where the final unrelated-product outcome remains EXCLUDE.

### Media

Of 1,667 current media exclusions, 1,385 remain excluded and 282 require HOLD. Explicit works, chapters, films, books, songs and proven digital-consumption patterns are safe exclusions. Bare `читать`, `смотреть`, `слушать`, `скачать` or `серия` with a product term is not enough by itself. Examples requiring HOLD: `амулет читать`, `серия амулет`, `астрал амулет` without further decisive media context.

### Game

Of 242 current game exclusions, 204 remain excluded and 38 require HOLD. Named games and explicit in-game tasks are safe. Generic `игра`, `мод`, `id` and model-like stems require context. Separately, the previous KEEP fallback missed 79 explicit foreign identities overall, including Hollow Knight, Elden Ring, PoE and vehicle parts.

### Place

Of 340 current place exclusions, 320 remain excluded, 8 should be KEEP and 12 HOLD. The unsafe rule is `купить.*дом|дом.*купить`: `оберег дома купить` and `оберег домовой купить` are product queries, not property purchases. Product marketplace queries such as `купить амулет на авито` also must not be destroyed merely because the marketplace is not the client's current sales channel.

## M. Complete transition matrix

### Normalized identities

| CURRENT_STATE → AUDIT_STATE | KEEP | HOLD | EXCLUDE | Current total |
|---|---:|---:|---:|---:|
| KEEP | 4,788 | 207 | 79 | 5,074 |
| HOLD | 298 | 12,084 | 368 | 12,750 |
| EXCLUDE | 14 | 744 | 5,994 | 6,752 |
| Audited total | 5,100 | 13,035 | 6,441 | 24,576 |

### RAW occurrences through lineage

| CURRENT_STATE → AUDIT_STATE | KEEP | HOLD | EXCLUDE | Current total |
|---|---:|---:|---:|---:|
| KEEP | 4,945 | 211 | 80 | 5,236 |
| HOLD | 304 | 12,828 | 368 | 13,500 |
| EXCLUDE | 14 | 784 | 6,445 | 7,243 |
| Audited total | 5,263 | 13,823 | 6,893 | 25,979 |

`NORMALIZED_TRANSITION_TOTAL = 24576`  
`RAW_TRANSITION_TOTAL = 25979`  
`SILENT_LOSS = 0`

## N. False-exclusion / false-keep metrics

- Unsafe current exclusions: 758/6,752 = **11.2263%**.
  - Direct false exclusions to KEEP: 14 = 0.2073% of AUTO_EXCLUDED.
  - Unsupported destructive exclusions requiring HOLD: 744 = 11.0190%.
- Unsafe current keeps: 286/5,074 = **5.6366%**.
  - Clear false keeps to EXCLUDE: 79 = 1.5570%.
  - Unsupported keeps requiring HOLD: 207 = 4.0796%.
- State changes: 1,710/24,576 identities = 6.9580%.
- RAW occurrences affected: 1,761/25,979 = 6.7786%.

“False exclusion” here intentionally includes rows that must be restored to HOLD. The audit is not claiming those 744 are final business keywords; it is finding that their current deletion is unsupported.

## O. HOLD quality assessment

The HOLD mechanism is methodologically correct and preserved most uncertainty safely, but the current implementation is uneven.

- HOLD→KEEP: 298 (2.3373%). Most are explicit zodiac product/object terms already supported by the frozen assortment.
- HOLD→EXCLUDE: 368 (2.8863%). Most are explicit game/media/place/entity tasks that can be resolved without SERP.
- HOLD→HOLD: 12,084 (94.7765%). These remain genuine unresolved catalog-name, zodiac/stone, entity/title, product-information or insufficient-context cases.

Verdict: **HOLD_POLICY_AUDIT = FAIL** because systematic rules push clear business rows into HOLD and leave clear foreign rows there. The remedy is not aggressive deletion; it is deterministic resolution where evidence is conclusive and continued preservation everywhere else.

## P. Pipeline Step04–14 methodology audit

| Step | Legitimate decision | Must not decide yet | Sufficient evidence | Uncertainty to preserve | Reduce / preserve / add | Exact PASS condition |
|---|---|---|---|---|---|---|
| 03A normalization | Conservative identity and exact dedup | Semantic equivalence, intent, cluster | Full RAW + Unicode-safe rules | Word order, morphology, homonyms | Reduce exact duplicates; preserve every occurrence | Exhaustive mapping, zero lineage loss, no implicit auto-collapse |
| 03B sanitation | High-confidence noise/off-topic vs clear business vs HOLD | Final intent, page, delivery, priority | Frozen business/catalog + explicit phrase context | All collisions/mixed meanings | Reduce only confirmed noise; preserve HOLD | Exhaustive partition; exclusion precision gate; zero open business collision |
| 04 family triage | Broad families, collision zones, expansion gaps | Final query-level cluster/intent | Corrected Step03B + frozen business | Mixed members and family exceptions | Summarize families; preserve row lineage | Every occurrence assigned; family totals reconcile; no family verdict overrides phrase evidence |
| 05 targeted expansion | Acquire approved coverage gaps | Competitor truth, final inclusion | Approved queue + current Wordstat receipts | Empty/weak demand and variants | Add demand observations; preserve call lineage | Queue exhausted/closed; no unapproved calls; evidence persisted |
| 06 competitor discovery | Identify current Yandex competitors/result types | Accept their vocabulary as demand | Current ordinary Yandex SERP by region/device/time | Mixed/non-commerce competitors | Add competitor candidates; preserve ranked evidence | Coverage and provenance complete for selected discovery queries |
| 07 competitor semantic expansion | Extract vocabulary/concepts from qualified competitors | Treat mentions as accepted demand | Current competitor pages/search evidence | Vocabulary with unknown demand/fit | Add candidates only; preserve source URL/location | Every term has source lineage and no automatic demand status |
| 08 demand validation | Validate competitor-derived candidates in Yandex demand | Delete solely for low/zero volume | Current Wordstat + frozen business | Low/zero/seasonal/ambiguous terms | Promote validated; hold unresolved; preserve failures | Every candidate has validation state, region/time/source |
| 09 candidate master | Union and conservative dedup of all allowed candidate sources | Final intent/cluster/page | All validated sources + lineage | Source conflicts and unresolved meaning | Reduce exact duplicates; add validated expansions | One exhaustive master with zero source/lineage loss |
| 10 nuanced relevance/intent/task | Phrase-level relevance and provisional user task | Final SERP cluster/page architecture without SERP | Frozen business + lexical context + SERP where already required | Mixed intent and uncertain task | Reduce only proven irrelevant; preserve SERP_REQUIRED_LATER | Every row has evidence-backed state and uncertainty flag |
| 11 Search-stage selection/freeze | Allocate a reproducible SERP evidence budget | Treat unselected as irrelevant or final-excluded | Risk, family, value and uncertainty strata | All unqueried ambiguity | Reduce only active collection queue; preserve full candidate register | Every row is pre-SERP-excluded, selected, or deferred-without-rejection; collision coverage guaranteed |
| 12 ordinary Yandex SERP evidence | Capture ranked result and page-type evidence | Final cluster from one lexical rule/one rank | Query + region + device + time + depth + URLs/types | Mixed SERPs and drift | Add reproducible SERP evidence; preserve snapshots | Required selected set complete; no missing metadata or truncation |
| 13 SERP + task-first clustering | Group compatible tasks using overlap/result type | One-page-per-query or fixed threshold alone | Step10 task + Step12 SERP overlap/types | Mixed/borderline clusters | Reduce to cluster representations; preserve membership/evidence | All selected queries assigned/held; overlap rationale reproducible; exceptions explicit |
| 14 query→page ownership / Search-only IA | Assign cluster to category/product/landing/info page | Invent pages from one keyword or commercial cap | Cluster task, dominant SERP/page type, assortment/site constraints | Unowned or multi-owner ambiguity | Reduce to ownership plan; preserve full query lineage | No silent unowned queries; page-type fit; cannibalization/thin-page checks pass |

## Q. Step11-before-SERP circularity assessment

**Risk: confirmed.** If Step11 uses lexical relevance, frequency, a delivery cap or first-N selection as a final gate, ambiguous high-value queries can be removed before Step12 obtains the SERP evidence needed to resolve them. That is circular.

Corrected evidence-budget approach:

1. **Pre-SERP exclusions:** only high-confidence off-topic rows that already pass the corrected Step03B precision gate.
2. **Mandatory collision tier:** every business collision class and every rule-risk class receives SERP representatives or full coverage according to its size/risk; no row becomes excluded merely because it is not queried.
3. **Family/task coverage tier:** cover every family, tentative task and result-type hypothesis, with explicit region/device/time/depth fields.
4. **Value tier:** use demand, business potential and information gain to order remaining evidence collection, never as relevance truth.
5. **Deferred tier:** unqueried rows remain `SERP_REQUIRED_LATER`/deferred, not rejected.
6. **Propagation constraint:** propagate a SERP conclusion only inside a demonstrably homogeneous group; mixed or threshold-edge groups retain uncertainty.
7. **Freeze receipt:** record selection reason, budget, coverage, exclusions, deferrals and the exact unqueried population.

The commercial delivery cap controls packaging effort; it does not define business relevance or Yandex demand truth.

## R. Fresh self-score of previous filtering work

The prior 96/100 is not reused. Scores below are based on this audit.

| Dimension | Score /10 | Evidence | Defect | Severity |
|---|---:|---|---|---|
| NORMALIZATION_SAFETY | 10 | NFC/whitespace/case-key reproduced on all rows | None found | None |
| RAW_LINEAGE_INTEGRITY | 10 | 25,979/25,979 occurrences and IDs reconcile | None found | None |
| EXACT_DEDUP_CORRECTNESS | 10 | 1,181 groups; 1,403 collapses; zero mismatches | None found | None |
| IMPLICIT_DEDUP_SAFETY | 10 | 3 groups; 0 accepted; all HOLD | None found | None |
| SANITATION_RULE_PRECISION | 6 | 11.2263% unsafe exclusions | Broad early patterns | Critical |
| FALSE_EXCLUSION_CONTROL | 5 | 14→KEEP and 744→HOLD | Unsupported destruction of demand | Critical |
| FALSE_KEEP_CONTROL | 7 | 79→EXCLUDE and 207→HOLD | Incomplete negative guards + positive-token fallback | Major |
| AMBIGUITY_HANDLING | 6 | HOLD exists and preserves 12,084 genuine cases | 666 resolvable HOLD plus 744 missing HOLD | Critical |
| BUSINESS_ASSORTMENT_ALIGNMENT | 5 | Frozen catalog used | Zodiac, auto-use and “Звезда Лады” collisions mishandled | Critical |
| LOW_FREQUENCY_BIAS_CONTROL | 10 | No frequency rule in classifier | None found | None |
| REASON_CODE_QUALITY | 5 | Counts/reasons present | Prefix/order errors and wrong-class outcomes | Major |
| FULL_VOLUME_COVERAGE | 10 | 24,576 identities audited/processed | None mechanical | None |
| REPRODUCIBILITY | 9 | Deterministic generator and lineage | Semantic regex rationale insufficiently regression-tested | Moderate |
| DOWNSTREAM_SAFETY | 4 | Step04 reconciliation exists | Incorrect 03B states contaminate later family/evidence selection | Critical |
| METHOD_SOURCE_SUPPORT | 6 | Internal rules documented | Original sanitation rules lacked adequate external collision/intent support | Major |

Total: 113/150 = **75.33/100**, rounded project score **75/100**.  
`QUALITY_SCORE_10 = 7.5`.

Acceptance requires ≥90/100, every critical dimension ≥9/10 and zero open critical semantic defects. None of those three conditions is met.

## S. PASS / REWORK verdict

`CRITICAL_REWORK_REQUIRED`

Required correction type:

- `FULL STEP03B REPROCESS`
- rule-only, full-volume reclassification of all 24,576 normalized identities;
- `STEP03A_REPROCESS = false`;
- provider calls = 0;
- regenerate Step03B state authorities, QA/funnel, then reconcile corrected Step04;
- do not start Step05.

The exact row-level blast radius and target state are frozen in the audit overlay. A separate canonical correction handoff accompanies this report.

## T. Exact next action

Main ChatGPT should review/accept the audit rubric and correction handoff. If accepted, issue a new execution release for a **full Step03B rule-only reprocess** against the unchanged Step03A universe, then require mechanical and semantic return QA plus Step04 reconciliation. Do not use provider calls and do not advance Step05.

## Audit artifact identities

- `KW002_STEP03A_03B_INDEPENDENT_FULL_VOLUME_AUDIT_OVERLAY_2026-09-11.tsv` — 24,576 rows; SHA-256 `db9b79dda64b205f0b0bef273f70f221f183d9389eca3e67e651e93ea269d669`.
- `KW002_STEP03A_03B_REASON_CODE_AUDIT_2026-09-11.tsv` — 12 reason rows; SHA-256 `050af71b8e431408c2f406e984416dc4c605038a5ad9f0ac103772f2f9310b31`.
- `KW002_STEP03A_03B_FULL_AUDIT_METRICS_2026-09-11.json` — complete count and integrity metrics.
- `KW002_STEP03B_CANONICAL_CORRECTION_HANDOFF_2026-09-11.md` — correction contract; no data rewrite performed in this pass.

## Machine-readable markers

EXTERNAL_METHOD_RESEARCH = PASS  
STEP03A_FULL_VOLUME_AUDIT = PASS  
STEP03B_FULL_VOLUME_AUDIT = FAIL  
AUTO_EXCLUDED_FULL_AUDIT = FAIL  
HOLD_POLICY_AUDIT = FAIL  
BUSINESS_COLLISION_AUDIT = FAIL  
MAIN_CHATGPT_RECONCILIATION = COMPLETE  
FALSE_EXCLUSION_COUNT = 758  
FALSE_KEEP_COUNT = 286  
QUALITY_SCORE_100 = 75  
QUALITY_SCORE_10 = 7.5  
FINAL_VERDICT = CRITICAL_REWORK_REQUIRED  
STEP04_ALLOWED = false  
STEP05_ALLOWED = false
