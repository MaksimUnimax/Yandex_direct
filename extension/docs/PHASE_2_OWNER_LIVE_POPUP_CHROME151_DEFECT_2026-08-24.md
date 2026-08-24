# Phase 2 owner-live defect — Chrome 151 action-popup autosize

Date: 2026-08-24  
Status: **CONFIRMED PRODUCT/UI DEFECT — PHASE 2 REOPENED AT POPUP GEOMETRY LAYER**

## Exact affected candidate

```text
source: 0ee1d38f8d28cfccceb5a07f9606fa715261bc27
artifact SHA-256: d58b5bd20921e9492a90b687ae3910c7049ddff17741da44ba832369eb1c0f16
artifact bytes: 170734
files: 65
ZIP entries: 68
```

The complete controlled pre-delivery campaign on this artifact remains valid evidence for the assertions it actually executed, but owner-live exposed a browser-owned popup geometry defect that the gate did not measure.

## Owner-live symptom

On opening the extension action popup, the popup is unstable/jumps and is not practically usable.

No real Search provider request was required to expose the defect. The Phase-2 live Search acceptance therefore has not begun at the irreversible provider boundary.

## Exact local product trigger

Affected `extension/src/popup.css` contains:

```css
body { margin: 0; width: 430px; max-width: 100vw; ... }
main { padding: 14px; }
```

There is no explicit root popup height bound and no dedicated internal root scroller. `popup.html` contains the complete Wordstat + Search + diagnostics/settings form and is intrinsically far taller than 600 px.

## Current upstream Chromium fact

Chrome action popups have a documented maximum size of `800 x 600` px:

```text
https://developer.chrome.com/docs/extensions/reference/api/action
```

Chromium issue `541684116`, filed for Chrome 151, records the current regression:

```text
[Extensions] Action popup expands from 316px to 800px when content height exceeds 600px
https://issues.chromium.org/issues/541684116
```

The issue reproduces on Chrome `151.0.7922.x`. When popup content exceeds the 600 px height limit, the action-popup autosize path can report the expanded root scroll width and inflate the popup host toward 800 px.

The Yandex Marketing Bridge exact candidate satisfies the triggering condition: narrow intended width + unbounded content far taller than 600 px.

## Why the previous browser gate missed this

The Stage-4 browser harness function named `openPopup()` did not open the native browser action popup. It executed:

```js
chrome.tabs.create({ url: chrome.runtime.getURL('popup.html'), active:false })
```

and then tested that extension page as a normal inactive browser tab.

That venue correctly exercised real popup JavaScript/worker transactions, but it could not exercise the Chrome action-popup host autosizing code. Therefore B-01/B-02/B-03 PASS did not prove native toolbar-popup geometry stability.

This is a gate-coverage blind spot plus a real product CSS defect, not evidence that Search/provider logic failed.

## Focused repair

Repair branch:

```text
fix/phase2-popup-chrome151-autosize-2026-08-24
```

Focused PR:

```text
#11 Fix Chrome 151 action popup autosize regression
```

Production change is intentionally limited to `extension/src/popup.css`:

```text
root popup viewport = 430 x 560
html/body overflow = hidden
main height = 100%
main overflow-y = auto
main overflow-x = hidden
```

This keeps the native action popup below the Chromium 600 px autosize boundary and moves the long settings form into an internal vertical scroller.

No worker, Search protocol/provider, credential, policy, Manual/Autorun, content-script or delivery behavior is intentionally changed.

## New mandatory regression

Static guard:

```text
extension/tests/popup_chrome151_geometry_recovery.test.mjs
```

Browser-owned focused gate:

```text
extension/tests/qa_browser/popup_chrome151_geometry_gate.mjs
```

Unlike the old Stage-4 popup helper, the new gate invokes the real:

```text
chrome.action.openPopup()
```

and inspects the native action-popup target on Chrome for Testing `151.0.7922.47`.

The focused QA must establish on the same Chrome build:

```text
old exact 0ee1d38 source: regression reproduced
fixed branch: narrow stable popup + internal scrolling
```

## Lifecycle consequence

The prior `d58b5bd...` artifact must not be handed back to the owner as accepted after this defect report.

Any production-byte repair creates a new candidate. Required path:

```text
focused Chrome-151 popup regression PASS
→ complete affected/source regression
→ refreeze a new exact artifact
→ complete governed pre-delivery gate on the new exact artifact
→ only then resume owner-live Search
```

Do not issue another paid owner-live Search command before the repaired candidate closes the controlled gate.
