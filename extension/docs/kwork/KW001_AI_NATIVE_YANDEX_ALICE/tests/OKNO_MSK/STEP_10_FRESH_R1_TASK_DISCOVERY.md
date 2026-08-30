# KW-001 / OKNO-MSK — STEP 10 FRESH R1 TASK DISCOVERY

Date: 2026-08-30
Status: **PASS 1 COMPLETE / TAXONOMY NORMALIZED FOR FREEZE**

## 1. Pass boundary

This is a fresh full discovery pass over the frozen Step-08 semantic set with Step-09 direct evidence used only where it exists.

Forbidden inputs during discovery:

```text
old Step-10 V39 taxonomy/assignments/count
blind independent 84 taxonomy/assignments/count
any target cluster count
```

Coverage:

```text
exact phrase rows read = 2840/2840
active Step-10 rows read = 2332/2332
silent drops = 0
```

The purpose of Pass 1 is to discover stable user-task families and modifier dimensions before row assignment. It does not correct individual rows and does not map tasks to pages.

## 2. Granularity axis discovered from the full pass

The stable primary axis is:

```text
PRODUCT / OBJECT
+ USER ACTION OR EXPECTED RESULT
+ INFORMATIONAL RESULT WHEN MATERIAL
```

The following are normally attributes inside a task rather than cluster creators:

```text
geo
price
installment / finance
seller/manufacturer source wording
brand/model/profile
size
house series
building type
material where it does not create a distinct product object
style/system names
frequency
lexical form
```

Therefore the fresh taxonomy intentionally does **not** create clusters such as:

```text
PVC_WINDOWS_GEO
PVC_WINDOWS_MANUFACTURER
WINDOW_FINANCE
HOUSE_SERIES_WINDOWS_COMMERCIAL
BALCONY_GLAZING_WOOD
PROVEDAL_ONLY_CLUSTER
```

Those dimensions are retained as row attributes/modifiers when relevant.

## 3. Material split tests that survived Pass 1

### Product/object splits

Stable distinct product jobs were observed for:

```text
generic windows
PVC windows
Rehau product-family commercial search
aluminium windows
wooden windows
timber-aluminium windows
soft windows
French windows
panoramic windows
roof/mansard windows
PVC doors
combined windows+doors
```

The Rehau commercial family is an explicit exception to the normal brand-as-modifier rule because the Step-09 direct evidence and the full phrase population show a recurring branded product-family shopping job. Rehau profile/model numbers remain modifiers inside that family rather than additional clusters.

Timber-aluminium windows remain separate because Step-09 direct evidence supports a distinct hybrid product/material object. By contrast, material words inside balcony/veranda glazing do not automatically create separate tasks.

### Lifecycle/action splits

The full pass supports material distinction between:

```text
buy/order product
order glazing service
professional installation
professional repair
replacement
demolition/dismantling
professional finishing
DIY/how-to
selection
comparison
reviews
technical/definition information
dimensions/sizing
measurement
care/maintenance
navigation
```

These actions have different expected results, so they are valid task boundaries when the phrase meaning actually expresses them.

### Balcony glazing

Stable service boundary:

```text
BALCONY_GLAZING_GENERAL
BALCONY_GLAZING_WARM
BALCONY_GLAZING_COLD
BALCONY_GLAZING_EXTENSION_SERVICE
BALCONY_GLAZING_ROOF_SERVICE
BALCONY_RENOVATION_WITH_GLAZING
```

Reasoning:

- warm vs cold materially changes the required thermal/result state;
- extension/outset adds construction scope;
- a roof adds construction scope;
- bundled renovation+glazing has a broader deliverable than glazing alone.

Not split automatically:

```text
wood/aluminium/PVC material
Provedal or other system/brand
house series
Moscow/district/city
French/panoramic styling
```

These remain modifiers unless a row's primary meaning is actually another product task.

### Veranda / terrace / gazebo / porch

The full pass shows the same underlying service job — glazing an outdoor structure — repeated across closely related structure names. The fresh taxonomy therefore uses one task:

```text
OUTDOOR_STRUCTURE_GLAZING
```

with `structure_type` preserving veranda / terrace / gazebo / porch. System/material variants such as frameless, soft, polycarbonate, sliding, accordion, guillotine or Provedal do not automatically create new Step-10 tasks.

Where a phrase primarily asks to buy a distinct product such as soft windows, the product task wins and the structure remains a modifier.

### Open balcony finishing

Step-09 direct evidence separates open-balcony finishing from glazing. It remains a distinct adjacent task:

```text
OPEN_BALCONY_FINISHING
```

### Components/accessories

The full pass supports stable task families for:

```text
window hardware shopping
window accessory shopping
mosquito-net shopping
mosquito-net installation
mosquito-net repair
hardware/accessory information
mosquito-net selection information
```

Component names inside generic window repair do not automatically create repair microclusters. A component-specific service is split only when the service result itself is materially distinct; windowsill repair is retained on that basis.

## 4. Information-task normalization

Product-specific wording is not enough to create a separate informational cluster. For example:

```text
Rehau comparison -> WINDOW_COMPARISON_INFO + brand modifier
Rehau selection -> WINDOW_SELECTION_INFO + brand modifier
panoramic definition/technology -> WINDOW_PRODUCT_TECH_INFO + product modifier
French-window dimensions -> WINDOW_DIMENSIONS_INFO + product modifier
aluminium-window why/how/property -> WINDOW_PRODUCT_TECH_INFO + product modifier
```

A dedicated branded navigational destination remains separate:

```text
NAVIGATION_BRAND_SITE
```

because the expected result is reaching an official/branded destination rather than reading product information.

## 5. Finance, geo, manufacturer and house-series normalization

The full phrase pass repeatedly showed these dimensions across otherwise identical tasks.

Frozen rule:

```text
finance/installment -> modifier
geo -> modifier
manufacturer/direct-from-manufacturer -> seller/source modifier
house series -> context modifier
```

They must not create Step-10 tasks on their own.

Examples of the consequence:

```text
PVC windows + Moscow -> PVC_WINDOWS_COMMERCIAL
PVC windows + installment -> PVC_WINDOWS_COMMERCIAL
PVC windows + manufacturer -> PVC_WINDOWS_COMMERCIAL
balcony glazing + house series -> BALCONY_GLAZING_* according to actual glazing result
Rehau + installment -> REHAU_WINDOWS_COMMERCIAL
```

## 6. Outside-scope normalization

The fresh pass intentionally avoids constructing a detailed SEO taxonomy inside outside-business demand.

Stable outside families are limited to:

```text
OUTSIDE_CURTAINS_BLINDS
OUTSIDE_HEATING_HVAC
OUTSIDE_REAL_ESTATE_ARCHITECTURE
OUTSIDE_INTERIOR_DOORS
OUTSIDE_USED_MARKET
OUTSIDE_OTHER
```

Actions such as selection/install/repair inside curtains do not create multiple Step-10 outside clusters. They remain attributes of the outside family.

`OUTSIDE_OTHER` is not an uncertainty bucket. It is used only after a row is semantically confirmed outside scope. Uncertainty must use a row-level unresolved/search-required state instead of creating taxonomy.

## 7. Step-09 direct evidence incorporated without transfer

Direct evidence was used only for the probed cases. Material observations include:

```text
mosquito nets = accessory shopping job
window hardware/components = accessory job
open balcony finishing != glazing
balcony demolition = distinct action
soft windows = distinct product
wooden windows = distinct product
French windows = distinct product/form job
panoramic windows = distinct product/form job
aluminium windows = distinct product job
PVC doors = distinct product job
warm/cold balcony glazing = materially different results
balcony extension/roof = materially different construction scope
Rehau official/site wording = navigational job
Rehau vs KBE = comparison job
Rehau repair = repair action with brand modifier
curtains/blinds = outside core window/glazing job
interior plastic doors can cross outside the target scope
used products = outside used-market intent
timber-aluminium windows = distinct hybrid product
```

The seven duplicate pairs labelled `CLUSTER_TOGETHER_CANDIDATE` and the one low-overlap boundary pair remain evidence inputs, not universal numeric rules. No overlap percentage is treated as a general threshold.

No evidence from a directly probed phrase is silently transferred to the 899 unprobed REVIEW_SEARCH rows.

## 8. Semantic defect candidates observed during Pass 1

Pass 1 deliberately did not correct row classification. It did collect independent later-QA candidates, including examples such as:

```text
оконная фурнитура бренды
оконная фурнитура марки
оконные блоки фурнитурой
остекление балкона работу
остекление крыши веранды
пластиковые окна брусбокс это rehau
пластиковые окна старый
сверление пластикового окна
узлы алюминиевых окон
от комаров на окна пластиковые
пластиковые окна без ремонта
пластиковые окна без установки москва
```

These are **QA candidates only**, not a claimed complete error ledger and not corrections made during discovery. The complete row-level semantic error ledger belongs to independent Pass 3 after frozen-taxonomy assignment.

## 9. Taxonomy-freeze result

The normalized fresh taxonomy contains **62 stable task IDs**. This number is an output of the full discovery/normalization pass, not a target and not a comparison goal.

Critical normalization outcomes:

```text
NO PVC_WINDOWS_GEO cluster
NO PVC_WINDOWS_MANUFACTURER cluster
NO WINDOW_FINANCE cluster
NO house-series commercial cluster
NO BALCONY_GLAZING_WOOD cluster
NO Provedal-only cluster
NO per-structure veranda/terrace/gazebo/porch split
NO multi-cluster outside-curtain microtaxonomy
```

The taxonomy is frozen for Pass 2. During Pass 2 a row may be assigned only to an existing frozen task or to a governed unresolved/deferred/excluded state. Pass 2 may not create a 63rd cluster.

## 10. Pass-1 verdict

```text
PASS1_FULL_SOURCE_REVIEW = PASS_2840_OF_2840
PASS1_ACTIVE_REVIEW = PASS_2332_OF_2332
PASS1_TASK_DISCOVERY = COMPLETE
PASS1_TAXONOMY_NORMALIZATION = COMPLETE
FRESH_TAXONOMY_CLUSTER_COUNT = 62
TARGET_CLUSTER_COUNT_USED = false
OLD_STEP10_INPUT_USED = false
BLIND84_INPUT_USED = false
TAXONOMY_READY_FOR_PASS2 = true
```
