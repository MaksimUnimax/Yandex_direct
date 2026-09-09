# MK01 STEP 01 — CURRENT SITE / BUSINESS MODEL

## PURPOSE
Build a current, scoped model of what the existing public business offers and the vocabulary needed for relevance and clustering.

## WHY THIS STEP EXISTS
Semantic collection without business context over-collects adjacent demand; one discovery pass also cannot prove site completeness forever.

## INPUTS
Frozen order, public site URL, included/excluded directions.

## REQUIRED EVIDENCE
Current public pages sufficient to understand offer, terminology and material business boundaries; client business facts where only the client can resolve them.

## METHOD
Read the current public site, record timestamp/source, identify material offer families and vocabulary, note coverage limitations and contradictions. Use additional current discovery only when completeness is material to the decision.

## OUTPUTS
Timestamped Level-2 site/business/domain profile used by acquisition, cleanup and clustering.

## SOURCE KW-001 AUTHORITY
Step1 lessons + `CURRENT_SITE_FRESHNESS_AND_EXISTENCE_GATE.md`.

## KNOWN FAILURE CLASSES
E02 — discovery success treated as complete current site.

## ROOT CAUSES
A successful crawl/read route was mistaken for proof that nothing else exists and that the snapshot remains current.

## NON-REPEAT CONTROLS
`DISCOVERY SUCCESS != DISCOVERY COMPLETENESS`; timestamp the profile; never use a stale closed inventory as sole proof of current absence.

## CLAIM BOUNDARIES
The profile constrains semantic relevance; it is not an SEO audit or architecture decision.

## UNKNOWN / BLOCKER BEHAVIOR
If the site is unavailable or the offer cannot be understood enough to judge relevance, block downstream collection or preserve the affected business fact as UNKNOWN pending client clarification.

## PASS GATE
Current public evidence and scope are sufficient for acquisition; limitations/contradictions are explicit; no unsupported completeness claim.

## CLIENT-FACING MEANING
«Перед сбором изучаю действующий сайт и реальные услуги/товары, чтобы не наполнять ядро запросами, которые бизнес не обслуживает.»
