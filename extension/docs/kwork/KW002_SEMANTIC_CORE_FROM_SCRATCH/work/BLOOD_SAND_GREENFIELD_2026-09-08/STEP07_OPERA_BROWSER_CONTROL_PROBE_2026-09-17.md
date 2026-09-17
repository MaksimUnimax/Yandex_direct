# KW-002 / BLOOD & SAND — STEP07 OPERA BROWSER CONTROL PROBE

Date: 2026-09-17
Scope: Main Chat browser-control evidence only
Purpose: distinguish real target-site blocking from Attempt-1 Work/runtime false inaccessibility.

## Result

Attempt 1 classified 31/32 competitors as zero-inspected and most relevant URLs as inaccessible. Main Chat then performed a browser-first control probe through the owner's connected Opera Browser Connector.

The control proves that Work/runtime inaccessibility cannot be treated as target-site closure.

### Browser-accessible / readable in Opera

- `ru.wikipedia.org` — public article `Амулет` loaded and its rendered content/accessibility tree was readable. Relevant semantic branches visible included `оберег`, `апотропей`, `талисман`, use on body/clothing/vehicles/dwellings, protection use, pregnancy/evil-eye material, and linked amulet types.
- `slavyanskieoberegi.ru` — homepage fully loaded with rich public taxonomy. Visible relevant categories/branches included `Амулеты`, `Кольца и перстни`, `Чертоги`, `Руны`, `Скандинавские обереги`, `Велес`, `Алатырь`, `Молвинец`, `Звезда Руси`, `Перун`, knowledge-base links and blog surfaces.
- `sibpodkova.ru` — homepage loaded and rendered normally. Site is primarily equestrian/horse-riding commerce; therefore the browser probe raises a scope/Step06-relevance question rather than an access problem.
- `artvaza.ru` — homepage loaded and rendered normally. Public catalog/taxonomy readable; site is broad gifts/interior/decor with branches such as `Фэн-шуй`, but much of the site appears unrelated to the frozen amulet/talisman theme. Again this is a scope/relevance issue, not access failure.
- `happywitch.ru` — homepage loaded and rendered normally. Strong relevant public taxonomy/content visible including `Амулеты и талисманы`, magic/esoteric goods, runes, stones for attracting love, ritual goods, incense and related blog/product surfaces.
- `simvolroda.ru` — homepage loaded and rendered normally. Strong relevant public taxonomy visible including `Обереги`, `Чертоги по дате рождения`, `Кольца и перстни`, `Молоты и топорики`, `Знания славян`, product pages and manual-made Slavic amulets.
- `oum.ru` — homepage loaded and rendered normally. Public yoga/mantra/related informational content was readable; relevance must be bounded by Step06 evidence and Step07 scope rather than assumed from site-wide content.

### Browser-level blocked/problematic in Opera

- `wildberries.ru` — site rendered an explicit browser-level message: `Возможно, нужно выключить VPN` / page load failed, so this is genuine current browser-access blocking evidence for this environment.
- `runarium.ru` — Opera showed a privacy/certificate error page; this is genuine browser-level access failure evidence for this snapshot.
- `ozon.ru` — Opera initially returned a no-connection page in this control session; this remains a target/browser-session access problem requiring later normal retry, not semantic closure.

## Key conclusion

```text
ATTEMPT1_WORK_INACCESSIBLE
!=
TARGET_SITE_INACCESSIBLE
```

Multiple sites marked by Attempt 1 as zero-inspected / inaccessible are demonstrably accessible through a normal browser. Therefore the Attempt-1 coverage ledger cannot be used as authority for semantic completion or target-site inaccessibility.

The recovery executor must distinguish:

```text
TARGET_BLOCK
TARGET_HTTP/NETWORK RESULT
BROWSER_ACCESSIBLE
EXECUTION_ENVIRONMENT_FAILURE
```

and must not convert tool/proxy/runtime failures into competitor closure.

## Downstream implications

1. Step07 Attempt 1 remains rejected/incomplete.
2. Browser-recovery acquisition is required before Step07 semantic rework.
3. Accessible competitors must be browser-collected at full bounded scope, not merely marked reachable.
4. Broad/possibly off-theme domains such as `sibpodkova.ru`, `artvaza.ru`, `oum.ru` need Step07 scope treatment based on Step06 evidence; accessibility does not make all site content relevant.
5. `wildberries.ru`, `runarium.ru`, `ozon.ru` retain browser-level retry/block evidence and must not be bypassed.
6. Step08 remains blocked until browser recovery + full Step07 semantic rework are accepted.
