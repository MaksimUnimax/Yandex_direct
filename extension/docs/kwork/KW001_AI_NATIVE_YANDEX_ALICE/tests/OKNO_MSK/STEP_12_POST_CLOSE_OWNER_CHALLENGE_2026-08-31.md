# Step 12 — post-close owner challenge

Date: 2026-08-31
Status: **REOPEN STEP 12 / OWNER CHALLENGE MATERIAL**

## Why this file exists

After the previously accepted Step-12 final readback, the owner challenged three recommendations from a business-owner perspective. Fresh first-party verification exposed material problems that invalidate the current `STEP12_COMPLETE` status until corrected.

The purpose of this file is durability: these findings must not depend on chat context and must be visible to a later run before Step 13.

## D12-16 — existing panoramic commercial page missed before CREATE

### What the accepted Step 12 said

Proposed a new commercial page:

`PROPOSED_NEW:/panoramnye-okna/`

for the panoramic-windows commercial core.

### Fresh first-party finding

The current main domain already has a full commercial landing:

`https://okno-msk.ru/okna-rehau/panoramnoe-osteklenie/`

Current first-party page evidence includes:
- H1 `Панорамные пластиковые окна`;
- price from 13,900 RUB/m2;
- order / free-measurement CTAs;
- explicit company offer and installation statements;
- product/profile options;
- calculator, FAQ and related panoramic use cases.

The accepted Step-01 merged inventory contained panoramic balcony and panoramic informational pages but did not contain this general commercial landing.

### Why this is a method failure

`NO_PAGE_IN_ACCEPTED_INVENTORY != CURRENT_PAGE_DOES_NOT_EXIST`.

A CREATE action must perform a final exact first-party existence check using the task, synonyms and likely URL families immediately before creating a new-page recommendation. An older discovery inventory is evidence, not a permanent proof of absence.

### Corrective direction

Withdraw `CREATE /panoramnye-okna/`. Re-open the panoramic structural unit against the existing `/okna-rehau/panoramnoe-osteklenie/` page and later examine its boundaries with panoramic balcony, veranda/terrace, sliding panoramic, apartment/house panoramic pages and the informational article.

Status: **OPEN**

---

## D12-17 — search demand was allowed to override owner commercial objective for installation DIY

### What the accepted Step 12 said

Proposed:

`PROPOSED_NEW:/stati/ustanovka-plastikovyh-okon-svoimi-rukami/`

### Fresh first-party finding

The existing installation service page explicitly positions professional installation as the desired outcome and states that the company does not recommend self-installation because of technical, quality and safety risks. It sells professional installation and warranty.

### Why this is a method failure

A stable informational user task and real search demand do not by themselves prove that the business should satisfy the task with a neutral enabling DIY guide.

Structural action selection must include an explicit **OWNER_COMMERCIAL_OBJECTIVE / DESIRED_USER_OUTCOME** check. Informational demand may be served with content that answers the question while supporting the business model (for example, risks, ГОСТ requirements, common errors, what professional installation includes), instead of enabling the user to avoid the core paid service.

### Corrective direction

Withdraw the current standalone step-by-step DIY-installation candidate. Re-evaluate whether the demand should be served by expanding `/uslugi/ustanovka-okon/` or by a business-aligned informational article such as `Можно ли установить пластиковое окно самостоятельно: требования, ошибки и риски`, with a professional-installation handoff.

Status: **OPEN**

---

## D12-18 — broad DIY repair candidate ignored existing DIY content and paid-repair boundary

### What the accepted Step 12 said

Proposed:

`PROPOSED_NEW:/stati/remont-i-regulirovka-plastikovyh-okon-svoimi-rukami/`

for multiple repair/adjustment subunits.

### Fresh first-party finding

The site already publishes substantial low-risk DIY adjustment content, including:
- `/stati/kak-otregulirovat-plastikovye-okna/`;
- `/stati/kak-perevesti-plastikovoe-okno-v-zimnij-rezhim/`;
- other maintenance/self-help articles.

At the same time, the company sells professional repair/regulation and explicitly reserves complex/risky work for specialists.

### Why this is a method failure

The proposed page merged two different business outcomes:
- low-risk self-help that the site's editorial strategy already allows;
- professional repair tasks that are a paid service.

It also failed the final exact-content reuse test because existing articles already cover a material part of the proposed page.

### Corrective direction

Withdraw the broad new `repair + adjustment DIY` page as currently framed. Re-evaluate the phrase set against existing self-help articles and the repair service page. Prefer expansion/diagnostic routing where appropriate, with an explicit boundary `what the user can safely do -> when to call a professional`.

Status: **OPEN**

---

## Immediate state consequence

Until D12-16, D12-17 and D12-18 are corrected and independently revalidated:

```text
STEP12_COMPLETE = false
STEP13_BLOCKED = true
STEP13_EXECUTED = false
NEXT_STEP_ALLOWED = false
```

The previously closed D12-01..D12-15 history remains preserved; these are newly discovered post-close defects, not a rewrite of prior provenance.
