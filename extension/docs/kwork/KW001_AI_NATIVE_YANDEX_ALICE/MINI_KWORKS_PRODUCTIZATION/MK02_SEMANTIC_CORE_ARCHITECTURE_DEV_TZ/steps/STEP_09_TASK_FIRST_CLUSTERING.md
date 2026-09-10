# MK02 STEP 09 — TASK / INTENT-FIRST CLUSTERING

## PURPOSE
Group accepted/active phrases into coherent user-task units suitable for later page-ownership and architecture decisions.

## WHY THIS STEP EXISTS
MK02 architecture inherits cluster boundaries. If clusters are built by visible words, current URLs or a target count, every later owner/action/TZ decision can be wrong even when accounting is perfect.

## INPUTS
Frozen semantic universe; accepted phrases; bounded Search observations where used; current business/site profile; preserved unresolved cases.

## REQUIRED EVIDENCE
Whole phrase; terminal user task; expected result/page role; intent; business fit; Search evidence when material; current domain constraints.

## METHOD
Cluster by stable user task / expected result first. Lexical similarity is only a clue. Different commercial/service/informational/DIY/review or object/lifecycle tasks split when materially different. Allow domain-specific rules only when tied to current job evidence. Do not target a predetermined cluster count. Keep unresolved phrases outside fabricated cluster membership. If a cluster is corrected, rebuild all derived task/intent/business-fit fields and summaries atomically.

## OUTPUTS
Cluster contracts; phrase assignments; human task/intent descriptions; representative phrases; boundary notes; semantic QA; unresolved handoff.

## SOURCE KW-001 AUTHORITY
KW-001 Step10 clustering methods; MK01 Step09.

## KNOWN FAILURE CLASSES
S16 token-driven clustering; S17 domain rules stripped; S18 target count invented; S19 ID-only correction; M11-03 representative phrase trusted over members.

## ROOT CAUSES
Presentation convenience, lexical similarity and internal IDs replaced explicit user-task falsification.

## NON-REPEAT CONTROLS
Whole-phrase task review; current domain profile; no target count; representative must be real accepted member but never substitutes for member review; atomic correction propagation; independent semantic QA.

## CLAIM BOUNDARIES
A cluster is a coherent user-task unit for analysis. It is not automatically one URL, a new page, or a physical site change.

## UNKNOWN / BLOCKER BEHAVIOR
Ambiguous phrases remain review/deferred/Search-required; mixed units are split or kept unresolved rather than forced coherent.

## PASS GATE
All accepted rows accounted; cluster contracts have stable task/intent/business-fit meaning; no mixed material terminal tasks left unreviewed; no target-count logic; correction-derived fields coherent; semantic QA PASS.

## CLIENT-FACING MEANING
«Запросы объединяются не просто по одинаковым словам, а по тому, что человек реально хочет получить. Это основа, на которой дальше можно безопасно решать, какая страница должна отвечать за каждую тему.»
