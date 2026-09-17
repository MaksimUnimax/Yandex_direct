# KW-002 / BLOOD & SAND — STEP07 OPERA BROWSER CONTROL PROBE

Date: 2026-09-17
Scope: Main Chat browser-control evidence only
Purpose: distinguish real target-site blocking from Attempt-1 Work/runtime false inaccessibility.

## Result

Attempt 1 classified 31/32 competitors as zero-inspected and most relevant URLs as inaccessible. Main Chat then performed repeated browser-first control probes through the owner's connected Opera Browser Connector, including a second pass after the owner manually opened additional competitor tabs.

The control proves that Work/runtime inaccessibility cannot be treated as target-site closure.

### Browser-accessible / readable in Opera

- `ru.wikipedia.org` — public article `Амулет` loaded and its rendered content/accessibility tree was readable. Relevant semantic branches visible included `оберег`, `апотропей`, `талисман`, use on body/clothing/vehicles/dwellings, protection use, pregnancy/evil-eye material, and linked amulet types.
- `slavyanskieoberegi.ru` — homepage fully loaded with rich public taxonomy. Visible relevant categories/branches included `Амулеты`, `Кольца и перстни`, `Чертоги`, `Руны`, `Скандинавские обереги`, `Велес`, `Алатырь`, `Молвинец`, `Звезда Руси`, `Перун`, knowledge-base links and blog surfaces.
- `radugakamnya.ru` — owner-opened tab was fully readable through Opera Connector. Public taxonomy included `Природные кристаллы и минералы`, `Сувениры из камня`, `Украшения из Камня Жемчуга Янтаря`, `Чокеры`, `Бусины`, stone/mineral branches such as аметист/оникс/малахит/яшма/селенит/обсидиан/змеевик/нефрит and related catalog surfaces. This is a confirmed false-negative against Attempt-1 zero-inspected/inaccessible handling.
- `sibpodkova.ru` — homepage loaded and rendered normally. Site is primarily equestrian/horse-riding commerce; therefore the browser probe raises a scope/Step06-relevance question rather than an access problem.
- `artvaza.ru` — homepage loaded and rendered normally. Public catalog/taxonomy readable; site is broad gifts/interior/decor with branches such as `Фэн-шуй`, but much of the site appears unrelated to the frozen amulet/talisman theme. Again this is a scope/relevance issue, not access failure.
- `happywitch.ru` — homepage loaded and rendered normally. Strong relevant public taxonomy/content visible including `Амулеты и талисманы`, magic/esoteric goods, runes, stones for attracting love, ritual goods, incense and related blog/product surfaces.
- `simvolroda.ru` — homepage loaded and rendered normally. Strong relevant public taxonomy visible including `Обереги`, `Чертоги по дате рождения`, `Кольца и перстни`, `Молоты и топорики`, `Знания славян`, product pages and manual-made Slavic amulets.
- `oum.ru` — homepage loaded and rendered normally. Public yoga/mantra/related informational content was readable; relevance must be bounded by Step06 evidence and Step07 scope rather than assumed from site-wide content.

### Browser-level blocked/problematic / connector-limited in Opera

- `wildberries.ru` — rechecked in the second pass. The site still rendered an explicit browser-level message: `Возможно, нужно выключить VPN` / page load failed. This is genuine current browser-access blocking evidence for this environment.
- `ozon.ru` — Opera initially returned a no-connection page in the control session. This remains a browser-session access problem requiring later normal retry, not semantic closure.
- `runarium.ru` — IMPORTANT SECOND-PASS CORRECTION. HTTPS previously showed a privacy/certificate error, but the owner manually opened `http://runarium.ru/` and Opera displayed a normal page title: `Все о скандинавской мифологии и рунах`. Opera Browser Connector itself refuses `tab-content` and screenshot actions on that HTTP URL with `This URL is blocked and pages cannot be accessed through actions`. Therefore the correct evidence state is **not target-site unavailable**. It is: browser tab visibly opens over HTTP, while the connector security policy blocks machine reading of the insecure HTTP page. Browser-capable recovery executors should retry the HTTP route if their own security policy permits normal public navigation; otherwise classify the inability as execution-environment/tool policy, not target closure.

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
CONNECTOR_SECURITY_POLICY_BLOCK
EXECUTION_ENVIRONMENT_FAILURE
```

and must not convert tool/proxy/runtime/security-policy failures into competitor closure.

## Downstream implications

1. Step07 Attempt 1 remains rejected/incomplete.
2. Browser-recovery acquisition is required before Step07 semantic rework.
3. Accessible competitors must be browser-collected at full bounded scope, not merely marked reachable.
4. Broad/possibly off-theme domains such as `sibpodkova.ru`, `artvaza.ru`, `oum.ru` need Step07 scope treatment based on Step06 evidence; accessibility does not make all site content relevant.
5. `radugakamnya.ru` is now positively confirmed browser-readable and must be recovered, not retained as inaccessible.
6. `runarium.ru` must no longer be summarized simply as target-inaccessible: HTTPS certificate failure and HTTP user-visible accessibility must be kept separate from Connector HTTP-action blocking.
7. `wildberries.ru` retains a genuine current browser-level VPN block; `ozon.ru` retains a browser-session retry requirement. No bypass is allowed.
8. Step08 remains blocked until browser recovery + full Step07 semantic rework are accepted.
