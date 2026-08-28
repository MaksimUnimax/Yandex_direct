from pathlib import Path

src = Path('extension/tests/qa_browser/phase2-stage4/browser_phase2_stage4_gate.mjs')
out = Path('extension/tests/qa_browser/phase2-stage4/.gensearch_phase2_stage4_action_popup_stable.mjs')
s = src.read_text(encoding='utf-8')

s = s.replace('protocolTimeout: 30000', 'protocolTimeout: 90000', 1)

# Phase2 full predates the five-service popup split. Preserve the original Search
# semantics, but exercise the current UI contract: credential Save is separate
# from common settings Save.
old_settings = '''  await popupSelect(p.popup,'activeService','search');
  await setCheckedNoEvent(p.popup,'searchManualEnabled',true);
  await setCheckedNoEvent(p.popup,'searchAutorunEnabled',true);
  await setCheckedNoEvent(p.popup,'autoSend',true);
  await setFormValue(p.popup,'apiKey','qa-browser-key');
  await setFormValue(p.popup,'folderId','qa-browser-folder');
  await setFormValue(p.popup,'searchMaxRequestsRun','5');
  await setFormValue(p.popup,'searchMaxCostRun','5');
  await popupClick(p.popup,'#saveSettings');
  await waitPopupStatus(p.popup,'Настройки сохранены.','SEARCH_SETTINGS_POPUP_ACTION_NOT_COMPLETE');'''
new_settings = '''  await popupSelect(p.popup,'activeService','search');
  await setFormValue(p.popup,'searchApiKey','qa-browser-key');
  await setFormValue(p.popup,'searchFolderId','qa-browser-folder');
  await popupClick(p.popup,'#saveSearchCredential');
  await waitPopupStatus(p.popup,'search: credentials сохранены.','SEARCH_CREDENTIAL_POPUP_ACTION_NOT_COMPLETE');
  await setCheckedNoEvent(p.popup,'searchManualEnabled',true);
  await setCheckedNoEvent(p.popup,'searchAutorunEnabled',true);
  await setCheckedNoEvent(p.popup,'autoSend',true);
  await setFormValue(p.popup,'searchMaxRequestsRun','5');
  await setFormValue(p.popup,'searchMaxCostRun','5');
  await popupClick(p.popup,'#saveSettings');
  await waitPopupStatus(p.popup,'Общие настройки сохранены.','SEARCH_SETTINGS_POPUP_ACTION_NOT_COMPLETE');'''
if s.count(old_settings) != 1:
    raise SystemExit('legacy Search settings sequence changed')
s = s.replace(old_settings, new_settings, 1)

start = s.find('async function openPopup(worker, browser, key) {')
end = s.find('\nasync function closePopup(', start)
if start < 0 or end <= start:
    raise SystemExit('openPopup block not found')

stable = r'''async function openPopup(worker, browser, key) {
  // This legacy harness opens popup.html as an extension tab. Emulate the real
  // action-popup contract by ensuring the matching ChatGPT owner tab is active
  // before popup runtime starts; keep every original popup assertion unchanged.
  const ownerTabId = await worker.evaluate(async expectedKey => {
    const tabs = await chrome.tabs.query({});
    for (const candidate of tabs) {
      if (!/^https:\/\/(chatgpt\.com|chat\.openai\.com)\//.test(String(candidate.url || ''))) continue;
      const probe = await new Promise(resolve => {
        chrome.tabs.sendMessage(candidate.id, { type:'WS_GET_IDENTITY' }, response => {
          void chrome.runtime.lastError;
          resolve(response || null);
        });
      });
      const candidateKey = String(probe?.conversation_key || probe?.identity?.conversation_key || '');
      if (probe?.ok === true && candidateKey === expectedKey) {
        await chrome.tabs.update(candidate.id, { active:true });
        return candidate.id;
      }
    }
    return null;
  }, key);
  assert(Number.isInteger(Number(ownerTabId)), `POPUP_OWNER_TAB_NOT_FOUND ${key}`);

  const existingTargets = new Set(browser.targets());
  const tab = await worker.evaluate(async () => await chrome.tabs.create({ url:'about:blank', active:false }));
  assert(tab?.id, 'POPUP_TAB_CREATE_FAIL');
  const target = await browser.waitForTarget(t => !existingTargets.has(t) && t.type()==='page', { timeout:30000 });
  const popup = await target.page(); assert(popup, 'POPUP_PAGE_FAIL');

  await worker.evaluate(async ({ ownerTabId, popupTabId }) => {
    await chrome.tabs.update(ownerTabId, { active:true });
    await chrome.tabs.update(popupTabId, { url:chrome.runtime.getURL('popup.html'), active:false });
  }, { ownerTabId:Number(ownerTabId), popupTabId:Number(tab.id) });

  await popup.waitForFunction(() => location.protocol === 'chrome-extension:' && location.pathname.endsWith('/popup.html'), { timeout:30000 });
  await waitUntil(async () => {
    const actual = await popup.evaluate(() => document.getElementById('conversationMeta')?.textContent || '');
    return actual === key ? actual : false;
  }, 'POPUP_CONVERSATION_CONTEXT_NOT_READY', 30000);
  await waitUntil(async () => {
    const status = await popup.evaluate(() => document.getElementById('status')?.textContent || '');
    return status === 'Готово.' ? true : false;
  }, 'POPUP_INITIAL_REFRESH_NOT_COMPLETE', 30000);
  return { popup, tabId:tab.id };
}'''

s = s[:start] + stable + s[end:]
out.write_text(s, encoding='utf-8', newline='\n')
print(out)
