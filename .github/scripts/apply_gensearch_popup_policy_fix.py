from pathlib import Path

popup = Path('extension/src/popup.js')
s = popup.read_text(encoding='utf-8')
old = '''  function searchPolicyFromForm() {
    return {
      autorun_enabled: $("searchAutorunEnabled").checked,
      manual_enabled: $("searchManualEnabled").checked,
      allowed_methods: ["search"],
      max_requests_per_run: asPositiveInt("searchMaxRequestsRun", 100),
      max_cost_rub_per_run: Math.max(0, asNumber("searchMaxCostRun", 10)),
      method_cost_rub: { search: Math.max(0, asNumber("costSearch", 0.488)) },
      tariff_checked_at: $("searchTariffCheckedAt").value.trim(),
      tariff_source: $("searchTariffSource").value.trim()
    };
  }'''
new = '''  function searchPolicyFromForm() {
    const current = lastState?.search_policy || {};
    const currentMethods = Array.isArray(current.allowed_methods) ? current.allowed_methods.map(String) : [];
    const genSearchEnabled = currentMethods.length ? currentMethods.includes("genSearch") : true;
    const currentGenSearchCost = Number(current.method_cost_rub?.genSearch);
    return {
      autorun_enabled: $("searchAutorunEnabled").checked,
      manual_enabled: $("searchManualEnabled").checked,
      // Common Save must not silently disable a method that this popup does not
      // expose as a toggle. Preserve the authoritative GenSearch enablement state;
      // an explicit stored disable remains disabled.
      allowed_methods: genSearchEnabled ? ["search", "genSearch"] : ["search"],
      max_requests_per_run: asPositiveInt("searchMaxRequestsRun", 100),
      max_cost_rub_per_run: Math.max(0, asNumber("searchMaxCostRun", 10)),
      method_cost_rub: {
        search: Math.max(0, asNumber("costSearch", 0.488)),
        genSearch: Number.isFinite(currentGenSearchCost) && currentGenSearchCost >= 0 ? currentGenSearchCost : 5.08
      },
      tariff_checked_at: $("searchTariffCheckedAt").value.trim(),
      tariff_source: $("searchTariffSource").value.trim()
    };
  }'''
if s.count(old) != 1:
    raise SystemExit('searchPolicyFromForm source changed')
popup.write_text(s.replace(old, new, 1), encoding='utf-8', newline='\n')

test = Path('extension/tests/qa_browser/gensearch_browser_runtime.mjs')
s = test.read_text(encoding='utf-8')
needle = '''  const fetchesAfter = await workerEval(workerClient, 'globalThis.__YMB_GENSEARCH_FETCHES');
  assert.equal(fetchesAfter.length, 1);
  console.log('GENSEARCH_BROWSER_REAL_YANDEX_REQUESTS=0');
  console.log('AI_NATIVE_GENSEARCH_BROWSER_RUNTIME_PASS');'''
replacement = '''  // A normal common-settings Save must preserve the current GenSearch policy
  // state even though the popup does not expose a GenSearch enable/disable toggle.
  await workerEval(workerClient, `(async () => {
    await chrome.storage.local.set({
      ymb_search_policy: {
        autorun_enabled: false,
        manual_enabled: true,
        allowed_methods: ['search', 'genSearch'],
        max_requests_per_run: 100,
        max_cost_rub_per_run: 10,
        method_cost_rub: { search: 0.488, genSearch: 5.08 },
        tariff_checked_at: '2026-08-28',
        tariff_source: 'https://aistudio.yandex.ru/docs/ru/search-api/pricing.html'
      }
    });
    return true;
  })()`);

  const popup = await browser.newPage();
  await popup.goto(`chrome-extension://${qa.extensionId}/popup.html`, { waitUntil: 'load', timeout: 15000 });
  await popup.waitForFunction(() => document.getElementById('status')?.textContent === 'Готово.', { timeout: 15000 });
  await popup.click('#saveSettings');
  await popup.waitForFunction(() => document.getElementById('status')?.textContent === 'Общие настройки сохранены.', { timeout: 15000 });
  let savedSearchPolicy = await workerEval(workerClient, `chrome.storage.local.get('ymb_search_policy').then(x => x.ymb_search_policy)`);
  assert.deepEqual(savedSearchPolicy.allowed_methods, ['search', 'genSearch']);
  assert.equal(savedSearchPolicy.method_cost_rub.genSearch, 5.08);
  console.log('GENSEARCH_BROWSER_POPUP_SAVE_PRESERVES_ENABLED_PASS');

  await workerEval(workerClient, `(async () => {
    const row = (await chrome.storage.local.get('ymb_search_policy')).ymb_search_policy;
    await chrome.storage.local.set({ ymb_search_policy: { ...row, allowed_methods: ['search'] } });
    return true;
  })()`);
  await popup.reload({ waitUntil: 'load', timeout: 15000 });
  await popup.waitForFunction(() => document.getElementById('status')?.textContent === 'Готово.', { timeout: 15000 });
  await popup.click('#saveSettings');
  await popup.waitForFunction(() => document.getElementById('status')?.textContent === 'Общие настройки сохранены.', { timeout: 15000 });
  savedSearchPolicy = await workerEval(workerClient, `chrome.storage.local.get('ymb_search_policy').then(x => x.ymb_search_policy)`);
  assert.deepEqual(savedSearchPolicy.allowed_methods, ['search']);
  assert.equal(savedSearchPolicy.method_cost_rub.genSearch, 5.08);
  console.log('GENSEARCH_BROWSER_POPUP_SAVE_PRESERVES_EXPLICIT_DISABLE_PASS');
  await popup.close();

  const fetchesAfter = await workerEval(workerClient, 'globalThis.__YMB_GENSEARCH_FETCHES');
  assert.equal(fetchesAfter.length, 1);
  console.log('GENSEARCH_BROWSER_REAL_YANDEX_REQUESTS=0');
  console.log('AI_NATIVE_GENSEARCH_BROWSER_RUNTIME_PASS');'''
if s.count(needle) != 1:
    raise SystemExit('GenSearch browser marker block changed')
test.write_text(s.replace(needle, replacement, 1), encoding='utf-8', newline='\n')

print('GENSEARCH_POPUP_POLICY_PATCH_APPLIED')
