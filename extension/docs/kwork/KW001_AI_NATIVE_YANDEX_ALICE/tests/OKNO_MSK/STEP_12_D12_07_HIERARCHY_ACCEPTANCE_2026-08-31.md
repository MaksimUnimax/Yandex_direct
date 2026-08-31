# Step 12 — D12-07 hierarchy acceptance

Date: 2026-08-31
Scope: D12-07 only. Step 12 remains in correction until all open defects are verified.

## What was wrong in the first run

The first Step-12 pass proposed five new URLs, but it mostly stopped at the proposed address and a loose parent label. That is insufficient because a useful new page is not just a URL. It has to occupy a real place in the site: users need a discoverable way to reach it, it must connect to the verified existing product/service/article structure, and it must lead onward to the more specific page or action that completes the user task.

A proposed URL without that structure can become an orphan page, duplicate an existing path, or silently replace a more specific page. It also makes the recommendation impossible to implement reliably.

## Corrected method and why

For each proposed page Step 12 now requires all of the following before hierarchy can be called materialized:

1. **Primary parent or navigation location.** This answers where the page belongs in the existing site, rather than placing it wherever its URL happens to look convenient.
2. **Mandatory inbound links from verified existing pages.** This proves how users and crawlers can discover the page from tasks that already exist on the site.
3. **Mandatory outbound links to verified existing specialist/service/utility pages.** This prevents the new page from pretending to own every narrower task.
4. **Plain user journey role.** This explains what a person does before, on, and after the page.
5. **Orphan prevention condition.** A new page is not accepted merely because a parent label is written; at least one concrete inbound and outbound route must exist.
6. **Preservation of unresolved evidence.** A good hierarchy does not prove that a separate page is needed in Yandex. If Search/business boundary evidence is still missing, it remains missing and confidence cannot be upgraded just because the linking plan is good.

This order matters. First we establish the user's task and candidate page. Then we fit it into the verified existing site. Only after that can later architecture work freeze a final structure. Doing hierarchy before semantic/evidence correction would simply give a neat location to the wrong page.

## Accepted hierarchy roles

### Panoramic windows

Candidate: `/panoramnye-okna/`.

It is intentionally **not** forced under only REHAU or only aluminium while the broad material scope remains conditional. It receives contextual inbound routes from the verified PVC, aluminium, balcony-panoramic, veranda and panoramic-information contexts, then sends users to the narrower material/object/French-window/calculator paths. Search page-boundary evidence is still missing, therefore hierarchy does not promote the candidate above MEDIUM by itself.

### Window replacement service

Candidate: `/uslugi/zamena-okon/`.

It belongs in the verified `/uslugi/` service family and must be reachable from installation, repair and product-selection contexts. It must route onward to installation, repair-vs-replace, finishing, payment and price-estimation paths. This describes a real service journey, but the standalone Search boundary remains unprobed, so the page remains provisional.

### Window hardware guide

Candidate: `/stati/okonnaya-furnitura-vidy-brendy-kak-vybrat/`.

It belongs in `/stati/` and acts as an explanatory bridge between repair and concrete supported hardware pages. Generic and brand-review intent remains explicitly excluded after D12-02. The hierarchy does not rescue the weak evidence: the guide can still become `NO_STANDALONE_PAGE` if later page-boundary review does not support it.

### DIY window installation guide

Candidate: `/stati/ustanovka-plastikovyh-okon-svoimi-rukami/`.

It belongs in `/stati/`, has a natural cross-link to the professional installation service, and routes onward to finishing, product choice and the calculator. This is the strongest information-page candidate because direct Step-9 queries already showed a procedural-information-guide task. Even here the global Step-12 QA must derive confidence; hierarchy itself never assigns HIGH by default.

### DIY repair/adjustment guide

Candidate: `/stati/remont-i-regulirovka-plastikovyh-okon-svoimi-rukami/`.

It belongs in `/stati/`, is linked from the verified professional repair context, and routes users to repair and supported hardware when self-repair is unsuitable. Direct Search page-boundary evidence remains absent, so the candidate remains provisional.

## QA result

`STEP_12_NEW_PAGE_HIERARCHY_QA.json` records:

- candidates: 5/5;
- explicit parent/navigation location: 5/5;
- mandatory inbound routes: 5/5;
- mandatory outbound routes: 5/5;
- orphan candidates: 0;
- existing link targets checked against the Step-1 inventory: PASS;
- broad panoramic page forced under one material family: false;
- hardware reviews reintroduced into guide: false;
- four material Search gaps preserved as gaps: 4/4;
- hierarchy auto-promoting confidence: false;
- new Bridge requests/cost: 0 / 0 RUB.

## Verdict

**D12-07 NEW_PAGE_HIERARCHY = VERIFIED_FIXED.**

This does not mean all five pages are finally approved. It means the first-run hierarchy defect is fixed: every candidate now has an implementable site role, while its remaining evidence gaps are still visible.

## Простыми словами

**Зачем исправляли:** раньше мы придумали адреса новых страниц, но этого мало — страница должна реально жить внутри сайта, а не висеть отдельно.

**Что сделали:** для каждой из пяти идей определили, откуда на неё должен попадать человек, где она находится в структуре и куда она должна вести дальше. При этом не спрятали сомнения: если Яндекс ещё не подтверждает отдельную страницу, она всё равно остаётся предварительной.

**Что получили:** пять новых страниц теперь можно обсуждать как часть реального сайта, а не как список придуманных URL. Но окончательное решение о спорных страницах всё ещё зависит от оставшихся проверок Step 12.
