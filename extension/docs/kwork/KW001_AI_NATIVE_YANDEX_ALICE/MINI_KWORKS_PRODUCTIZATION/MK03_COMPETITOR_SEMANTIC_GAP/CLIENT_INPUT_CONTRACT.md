# MK03 — CLIENT INPUT CONTRACT

Status: **PHASE 2 PASS / V1**

## Required start input

For an existing public site the standard required input is only:

```text
PUBLIC SITE URL
TARGET REGION
```

The analyst inspects the public site to understand visible products, services, sections and current coverage. Do not make the client manually repeat facts already available on the site.

## Optional inputs

Useful but not mandatory:

- competitor names/domains the client already knows — treated as hints, not automatic Search-competitor truth;
- existing semantic core/export — used as a comparison input only if its freshness/provenance is sufficient;
- specific business constraints or excluded directions not visible on the public site;
- optional owned Yandex data when separately authorized and material.

## Clarification rule

Ask for business clarification only when the public site leaves a genuine ambiguity that can materially change a gap decision.

One ambiguity -> one concrete question.

Do not block the whole order because optional inputs are absent.

## Secrets / private access

Base MK03 requires no passwords, analytics credentials or private account access.

Do not request secrets in chat. Optional private Yandex evidence follows the project private-access policy and is not a base-package dependency.

## Incomplete-input behavior

- URL unavailable/unreadable -> scope cannot be responsibly reconciled against current client coverage; mark blocked until a usable public target exists.
- region missing -> ask for target region because Yandex Search/Wordstat evidence is region-sensitive.
- competitor list missing -> not a blocker; discover real organic competitors from Yandex.
- semantic core missing -> not automatically a blocker; MK03's acquisition/gap method uses current site + competitor-derived demand evidence, subject to the product limits.
- business ambiguity -> preserve HOLD/PENDING clarification for affected decisions only.

## Client-facing scope statement

Work is performed for Yandex: ordinary Yandex Search, Yandex Wordstat and public client/competitor pages. Google tools/evidence are not part of V1.
