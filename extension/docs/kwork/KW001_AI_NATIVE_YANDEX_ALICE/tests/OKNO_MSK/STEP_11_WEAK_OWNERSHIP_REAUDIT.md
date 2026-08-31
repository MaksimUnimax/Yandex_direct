# Step 11 — weak ownership re-audit

Date: 2026-08-31

This audit was introduced after external method review showed that cluster-only ownership could hide heterogeneous Step-10 membership. All original Step-11 MEDIUM/LOW ownership clusters were explicitly re-audited against their member phrases.

```text
ORIGINAL_MEDIUM_LOW_CLUSTERS = 11
REAUDITED = 11
MISSING = 0
```

Material corrections:

- `GENERAL_GLAZING_SERVICE`: invalid generic cluster; all members were reassigned to aluminium/panoramic/French/outside-brand tasks.
- `GLAZING_SELECTION_INFO`: invalid generic/non-balcony boundary; actual phrases were veranda-specific and were split into selection, specialized-technique and reviews tasks.
- `WINDOW_REPLACEMENT_SERVICE`: component replacements and balcony/French transformations were removed from whole-window replacement.
- `WINDOW_HARDWARE_SHOPPING`: ownership changed from the accessory hub to `NO_SUITABLE_EXISTING_PAGE` because the broad aftermarket/third-party catalog demand is not truthfully covered by the current target site.
- `WINDOW_REVIEWS_INFO`: split into product/model reviews vs provider/service ratings; neither is truthfully owned by the company's own `/otzyvy/` page.
- `WINDOW_PRODUCT_TECH_INFO`: split by product family and task; current dedicated pages/articles are used where they actually exist.
- `WINDOW_REPAIR_DIY_INFO`: six bare DIY/instruction phrases returned to `SEARCH_REQUIRED` instead of being forced into repair.
- `WINDOW_HARDWARE_INFO`: glass-unit/profile/comparison phrases moved to more precise tasks; remaining broad hardware information retains no-suitable-page treatment.
- `WINDOW_ACCESSORY_SELECTION_INFO`: false negative fixed; its only phrase is windowsill selection and the current windowsill page is a truthful owner.
- `BALCONY_GLAZING_INFO`: split into selection vs provider/review tasks.
- `GLAZING_SELECTION_INFO` original unresolved state disappears because its actual phrase membership was reclassified instead of being reinterpreted from one representative query.
- `WINDOWS_DOORS_COMBINED_COMMERCIAL`: phrase-level review did not expose a material coherence defect; homepage ownership remains MEDIUM.

No Step-12 structural action and no Step-13 cannibalization verdict was made.
