from pathlib import Path


def replace_once(text, old, new, label):
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{label}: expected one match, got {count}")
    return text.replace(old, new, 1)


def replace_between(text, start, end, replacement, label):
    a = text.find(start)
    if a < 0:
        raise SystemExit(f"{label}: start marker not found")
    b = text.find(end, a)
    if b < 0:
        raise SystemExit(f"{label}: end marker not found")
    return text[:a] + replacement.rstrip() + "\n\n" + text[b:]


current_path = Path("extension/docs/CURRENT_STATE.md")
current = current_path.read_text(encoding="utf-8")
current = replace_once(
    current,
    "Status: **PHASES 0–6 CLOSED — O-001 COMPARATIVE GATE PASS — GENSEARCH PRODUCTION HAND ACCEPTED — PHASE 8 BULK SERP/TOP/RANK = ACTIVE NEXT ENGINEERING PHASE**",
    "Status: **PHASES 0–8 CLOSED — O-001 COMPARATIVE GATE PASS — GENSEARCH + BULK SERP/TOP/RANK HANDS ACCEPTED IN MAIN — PHASE 9 GOOGLE GAP = NEXT RESEARCH PHASE**",
    "current-status",
)
section7 = '''## 7. Phase 8 — Bulk SERP / TOP-overlap / rank evidence CLOSED / IN MAIN

Phase 8 is accepted and no longer an active development phase.

Production protocol:

```text
SEARCH_BATCH_API_V1
SEARCH_BATCH_RESULT_V1
service = search
queries[] up to 500
start/status/pause/resume/cancel/projection/overlapPage = 0 provider requests
one explicit next = at most one ordinary Search provider request
```

Accepted product identity:

```text
source authority = 0377d6e1f176d4b7ddd8553c0099e02a4f1e8716
extension tree = 446fed6970c5fec627be34c3893800dc4511c6c9
extension/src tree = bdad1e87a2537d8646e480ca23f8068c3dced17e
freeze run = 33143237276 / SUCCESS
frozen ZIP sha256 = 8f6ba92dbe1f592a62c66cd250ed942e261f56deffbe87117371bd9c481e6332
```

Owner-live acceptance:

```text
job = p8-owner-live-2026-08-28
queries = 2
successful provider requests = 2
requests_started = 2
estimated_cost_rub = 0.976
automatic_retry = false
outcome_unknown = 0
status/projection/overlapPage provider requests = 0
```

Observed deterministic evidence included `market.yandex.ru` at best observed rank 3 for `печать велеса`, `ru.wikipedia.org` at rank 1 for `алатырь`, and pairwise TOP-10 domain overlap `shared_count=0`, `union_count=15`, `jaccard=0`.

Production integration:

```text
main integration commit = ebd697e5733a7d40d13401d4c02b82a75711231c
postmerge gate = 33144396638 / SUCCESS
Node regression = 118/118
controlled browser real Yandex requests = 0
product immutability = PASS
```

Final authority:
`extension/tests/PHASE8_SEARCH_BATCH_FINAL_ACCEPTANCE_2026-08-28.md`

**PHASE8_SEARCH_BATCH_FINAL_ACCEPTANCE_PASS**

---

## 8. Authorized autonomous next sequence

```text
Phase 8 = CLOSED / IN MAIN
→ Phase 9 research: official/stable/legal Google organic evidence options
→ evaluate source quality, cost, privacy and ToS before freezing any provider contract
→ do not implement a Google hand before provider research and a test-first contract
→ preserve the current five-service registry unless a governed architecture decision explicitly changes it
```

Phase 10 crawler/importer evidence work remains lower priority than Phase 9 provider research.

---

## 9. Open blockers

```text
Phase 6 = NONE / PASS
O-001 comparative methodology gate = NONE / PASS
GenSearch repeatable official hand = NONE / ACCEPTED
Phase 8 bulk SERP/TOP/rank = NONE / PASS / IN MAIN
owner action now = NONE
next engineering = Phase 9 Google organic provider research
```

No further Phase-8 owner ceremony is required.
'''
start7 = "## 7. Phase 8 — Bulk SERP / TOP-overlap / rank evidence ACTIVE NEXT"
a = current.find(start7)
if a < 0:
    raise SystemExit("current-phase8: start marker not found")
current = current[:a] + section7
current_path.write_text(current, encoding="utf-8")

roadmap_path = Path("extension/docs/ROADMAP.md")
roadmap = roadmap_path.read_text(encoding="utf-8")
phase8 = '''# PHASE 8 — Bulk SERP / TOP-overlap / rank evidence

**Status: PASS / CLOSED / IN MAIN.**

Accepted production hand:

```text
SEARCH_BATCH_API_V1
service = search
queries[] up to 500
one explicit next <= one ordinary Search provider request
durable per-query checkpoint/result evidence
local projection + sampled target-domain rank
local paged TOP/domain overlap
OUTCOME_UNKNOWN => no automatic replay
```

Accepted identity and gates:

```text
source authority = 0377d6e1f176d4b7ddd8553c0099e02a4f1e8716
extension tree = 446fed6970c5fec627be34c3893800dc4511c6c9
extension/src tree = bdad1e87a2537d8646e480ca23f8068c3dced17e
freeze run = 33143237276 / SUCCESS
candidate ZIP sha256 = 8f6ba92dbe1f592a62c66cd250ed942e261f56deffbe87117371bd9c481e6332
owner-live = PHASE8_SEARCH_BATCH_OWNER_LIVE_PASS
main integration = ebd697e5733a7d40d13401d4c02b82a75711231c
postmerge run = 33144396638 / SUCCESS
Node regression = 118/118
controlled browser real Yandex requests = 0
```

Owner-live used two real ordinary Search queries. `start` made zero provider requests; two explicit `next` calls produced exactly two successful provider requests; `status`, `projection` and `overlapPage` remained local-only with `requests_started=2` and total estimated cost `0.976 RUB`.

Final semantic clustering/page split decisions remain ChatGPT work rather than hidden threshold logic.

Final authority:
`extension/tests/PHASE8_SEARCH_BATCH_FINAL_ACCEPTANCE_2026-08-28.md`
'''
roadmap = replace_between(
    roadmap,
    "# PHASE 8 — Bulk SERP / TOP-overlap / rank evidence",
    "# PHASE 9 — Google organic gap",
    phase8 + "\n---\n\n# PHASE 9 — Google organic gap",
    "roadmap-phase8",
)
market = '''# MARKET-DISCOVERY AUTHORITY

Canonical matrix:

`extension/docs/FREELANCE_ORDER_CAPABILITY_MATRIX.md`

Current product conclusion:

```text
mass-market base = Semantic Core Builder
premium differentiated method = AI-Native Semantic Rebuild with selective GenSearch evidence
bulk ordinary-Search/TOP evidence hand = ACCEPTED / IN MAIN
next highest-leverage engineering = Phase 9 Google organic provider research
```

---

# CURRENT ACTIVE ORDER

```text
DONE: Phases 0–8 closed
DONE: Gate A O-001 comparative methodology PASS
DONE: Phase 7 GenSearch validated, frozen, integrated and postmerge verified
DONE: Phase 8 Search batch/TOP/rank frozen, owner-live accepted, integrated and postmerge verified

NOW:
Phase 9 Google organic provider research — official/stable/legal acquisition options first

THEN:
Provider/contract decision only after research; Phase 10 crawler/importer remains lower priority
```

No project-owner action is currently required.
'''
market_start = roadmap.find("# MARKET-DISCOVERY AUTHORITY")
if market_start < 0:
    raise SystemExit("roadmap-market: start marker not found")
roadmap = roadmap[:market_start] + market
roadmap_path.write_text(roadmap, encoding="utf-8")

plan_path = Path("extension/docs/PHASE_8_BULK_SERP_TOP_RANK_REQUIREMENTS_AND_PLAN.md")
plan = plan_path.read_text(encoding="utf-8")
plan = replace_once(
    plan,
    "Status: **REQUIREMENTS READY / IMPLEMENTATION AUTHORIZED AFTER EXACT-MAIN BASELINE + TEST-FIRST CONTRACT**",
    "Status: **PASS / CLOSED / IN MAIN**",
    "plan-status",
)
if "## 19. Final closure" in plan:
    raise SystemExit("plan-final-closure already present")
plan = plan.rstrip() + '''\n\n## 19. Final closure\n\n```text\nPHASE8_SEARCH_BATCH_FINAL_ACCEPTANCE_PASS\nsource authority = 0377d6e1f176d4b7ddd8553c0099e02a4f1e8716\nextension tree = 446fed6970c5fec627be34c3893800dc4511c6c9\nextension/src tree = bdad1e87a2537d8646e480ca23f8068c3dced17e\nfreeze run = 33143237276 / SUCCESS\nfrozen ZIP sha256 = 8f6ba92dbe1f592a62c66cd250ed942e261f56deffbe87117371bd9c481e6332\nowner-live job = p8-owner-live-2026-08-28\nowner-live real provider requests = 2\nowner-live automatic retries = 0\nowner-live estimated cost = 0.976 RUB\nmain integration = ebd697e5733a7d40d13401d4c02b82a75711231c\npostmerge gate = 33144396638 / SUCCESS\npostmerge Node regression = 118/118\npostmerge controlled browser real Yandex requests = 0\n```\n\nPhase 8 is closed. No further owner-live ceremony is required.\n'''
plan_path.write_text(plan, encoding="utf-8")

acceptance = Path("extension/tests/PHASE8_SEARCH_BATCH_FINAL_ACCEPTANCE_2026-08-28.md")
if acceptance.exists():
    raise SystemExit("final acceptance file already exists")
acceptance.write_text('''# Phase 8 Search Batch final acceptance — 2026-08-28\n\nStatus: `PHASE8_SEARCH_BATCH_FINAL_ACCEPTANCE_PASS`\n\n## Frozen product authority\n\n```text\nsource = 0377d6e1f176d4b7ddd8553c0099e02a4f1e8716\nextension = 446fed6970c5fec627be34c3893800dc4511c6c9\nextension/src = bdad1e87a2537d8646e480ca23f8068c3dced17e\nfreeze run = 33143237276 / SUCCESS\ncandidate ZIP sha256 = 8f6ba92dbe1f592a62c66cd250ed942e261f56deffbe87117371bd9c481e6332\n```\n\n## Owner-live\n\n```text\njob = p8-owner-live-2026-08-28\nqueries = печать велеса | алатырь\nstart provider requests = 0\nnext calls = 2\nsuccessful provider requests = 2\nrequests_started = 2\nsucceeded = 2\noutcome_unknown = 0\nautomatic_retry = false\nestimated_cost_rub = 0.976\nstatus provider requests = 0\nprojection provider requests = 0\noverlapPage provider requests = 0\n```\n\nObserved target-domain rank evidence:\n- `печать велеса`: `market.yandex.ru` best observed TOP-10 rank = 3;\n- `алатырь`: `ru.wikipedia.org` best observed TOP-10 rank = 1.\n\nObserved pairwise TOP-10 domain evidence:\n\n```text\nleft = печать велеса\nright = алатырь\nleft_domain_count = 7\nright_domain_count = 8\nshared_count = 0\nunion_count = 15\njaccard = 0\nleft_containment = 0\nright_containment = 0\n```\n\n## Production integration\n\n```text\nmain integration = ebd697e5733a7d40d13401d4c02b82a75711231c\npostmerge workflow = 33144396638 / SUCCESS\nNode regression = 118/118\ncontrolled installed-extension browser = PASS\nproduct immutability = PASS\nreal_yandex_requests in controlled browser = 0\n```\n\nNo sixth service was created. Search batch remains orchestration within `service=search` and uses ordinary Search only.\n\n`PHASE8_SEARCH_BATCH_FINAL_ACCEPTANCE_PASS`\n''', encoding="utf-8")

print("PHASE8_CLOSE_PATCH_READY")
