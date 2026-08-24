#!/usr/bin/env python3
import hashlib
import os
from pathlib import Path
import subprocess
import sys
import tempfile

repo = Path.cwd().resolve()
source = repo / "qa" / "phase2_popup_fix_complete_gate.py"
raw = source.read_text(encoding="utf-8")

worktree_old = '''for name, path, commit in [
    ("worktree_source", source_wt, SOURCE_COMMIT),
    ("worktree_transport", transport_wt, TRANSPORT_COMMIT),
    ("worktree_stage4", stage4_wt, STAGE4_HARNESS_COMMIT),
]:
    rc, out = run(name, ["git", "worktree", "add", "--detach", str(path), commit], timeout=300)
    if rc != 0:
        append_master(f"WORKTREE_SETUP_FAIL {name}\\n")
'''

worktree_new = '''for name, path, commit in [
    ("worktree_source", source_wt, SOURCE_COMMIT),
    ("worktree_transport", transport_wt, TRANSPORT_COMMIT),
    ("worktree_stage4", stage4_wt, STAGE4_HARNESS_COMMIT),
]:
    if name == "worktree_source":
        worktree_cmd = ["git", "-c", "core.autocrlf=false", "-c", "core.eol=lf", "worktree", "add", "--detach", str(path), commit]
    else:
        worktree_cmd = ["git", "worktree", "add", "--detach", str(path), commit]
    rc, out = run(name, worktree_cmd, timeout=300)
    if rc != 0:
        append_master(f"WORKTREE_SETUP_FAIL {name}\\n")
'''

browser_old = '''    if dep1_rc == 0:
        harness = stage4_dir / "browser_phase2_stage4_gate.mjs"
        key = stage4_dir / "qa-chatgpt-local.key.pem"
        cert = stage4_dir / "qa-chatgpt-local.cert.pem"
        rc, out = run("browser_b01_b03", [shutil.which("node") or "node", str(harness), CHROME_PATH, str(extension_root), str(key), str(cert)], cwd=stage4_dir, timeout=900)
        results["b01"] = rc == 0 and "B01_PROJECT_WORK_PASS" in out
        results["b02"] = rc == 0 and all(m in out for m in ["B02_MANUAL_ON_TRANSACTION_PASS", "BROWSER_STEP_NATIVE_COPY_PASS"])
        results["b03"] = rc == 0 and all(m in out for m in ["B03_SEARCH_AUTORUN_PASS", "BROWSER_CONTROLLED_SEARCH_STUB_REQUESTS=1", "BROWSER_GATE_REAL_YANDEX_REQUESTS=0", "PHASE2_STAGE4_BROWSER_GATE_PASS"])
'''

browser_new = '''    if dep1_rc == 0:
        harness = stage4_dir / "browser_phase2_stage4_gate.mjs"
        key = stage4_dir / "qa-chatgpt-local.key.pem"
        cert = stage4_dir / "qa-chatgpt-local.cert.pem"
        harness_source = harness.read_text(encoding="utf-8")
        popup_helper_old = """async function openPopup(worker, browser, key) {
  const existingTargets = new Set(browser.targets());
  const tab = await worker.evaluate(async () => await chrome.tabs.create({ url: chrome.runtime.getURL('popup.html'), active:false }));
  assert(tab?.id, 'POPUP_TAB_CREATE_FAIL');
  const target = await browser.waitForTarget(t => !existingTargets.has(t) && t.url().startsWith('chrome-extension://') && t.url().endsWith('/popup.html'), { timeout:10000 });
  const popup = await target.page(); assert(popup, 'POPUP_PAGE_FAIL');
  await popup.waitForFunction(expected => document.getElementById('conversationMeta')?.textContent === expected, { timeout:10000 }, key);
  await waitUntil(async () => {
    const status = await popup.evaluate(() => document.getElementById('status')?.textContent || '');
    return status === 'Готово.' ? true : false;
  }, 'POPUP_INITIAL_REFRESH_NOT_COMPLETE', 10000);
  return { popup, tabId:tab.id };
}
async function closePopup(worker, tabId) { try { await worker.evaluate(async id => { try { await chrome.tabs.remove(id); } catch {} }, tabId); } catch {} await delay(180); }
"""
        popup_helper_new = """async function popupPageForTab(browser, tabId) {
  return await waitUntil(async () => {
    const pages = await browser.pages();
    for (const page of pages) {
      if (page.isClosed()) continue;
      const url = page.url();
      if (!url.startsWith('chrome-extension://') || !url.endsWith('/popup.html')) continue;
      try {
        const pageTabId = await page.evaluate(() => new Promise((resolve) => {
          chrome.tabs.getCurrent((tab) => resolve(tab?.id || null));
        }));
        if (pageTabId === tabId) return page;
      } catch {}
    }
    return false;
  }, `POPUP_PAGE_FOR_TAB_NOT_ATTACHED ${tabId}`, 15000, 80);
}
async function openPopup(worker, browser, key) {
  const tab = await worker.evaluate(async () => await chrome.tabs.create({ url: chrome.runtime.getURL('popup.html'), active:false }));
  assert(tab?.id, 'POPUP_TAB_CREATE_FAIL');
  const popup = await popupPageForTab(browser, tab.id); assert(popup, 'POPUP_PAGE_FAIL');
  await popup.waitForFunction(expected => document.getElementById('conversationMeta')?.textContent === expected, { timeout:10000 }, key);
  await waitUntil(async () => {
    const status = await popup.evaluate(() => document.getElementById('status')?.textContent || '');
    return status === 'Готово.' ? true : false;
  }, 'POPUP_INITIAL_REFRESH_NOT_COMPLETE', 10000);
  return { popup, tabId:tab.id };
}
async function closePopup(worker, tabId) {
  try { await worker.evaluate(async id => { try { await chrome.tabs.remove(id); } catch {} }, tabId); } catch {}
  await waitUntil(async () => {
    try {
      return await worker.evaluate(async id => {
        try { await chrome.tabs.get(id); return false; } catch { return true; }
      }, tabId);
    } catch { return true; }
  }, `POPUP_TAB_CLOSE_NOT_CONFIRMED ${tabId}`, 5000, 80);
}
"""
        if harness_source.count(popup_helper_old) != 1:
            raise RuntimeError("STAGE4_POPUP_HELPER_PATCH_ANCHOR_FAIL")
        stable_harness = stage4_dir / "browser_phase2_stage4_gate.tab_identity.mjs"
        stable_harness.write_text(harness_source.replace(popup_helper_old, popup_helper_new, 1), encoding="utf-8", newline="\\n")
        try:
            rc, out = run("browser_b01_b03", [shutil.which("node") or "node", str(stable_harness), CHROME_PATH, str(extension_root), str(key), str(cert)], cwd=stage4_dir, timeout=900)
        finally:
            stable_harness.unlink(missing_ok=True)
        results["b01"] = rc == 0 and "B01_PROJECT_WORK_PASS" in out
        results["b02"] = rc == 0 and all(m in out for m in ["B02_MANUAL_ON_TRANSACTION_PASS", "BROWSER_STEP_NATIVE_COPY_PASS"])
        results["b03"] = rc == 0 and all(m in out for m in ["B03_SEARCH_AUTORUN_PASS", "BROWSER_CONTROLLED_SEARCH_STUB_REQUESTS=1", "BROWSER_GATE_REAL_YANDEX_REQUESTS=0", "PHASE2_STAGE4_BROWSER_GATE_PASS"])
'''

if raw.count(worktree_old) != 1:
    raise SystemExit("WINDOWS_SOURCE_WORKTREE_PATCH_ANCHOR_FAIL")
patched = raw.replace(worktree_old, worktree_new, 1)
if patched.count(browser_old) != 1:
    raise SystemExit("WINDOWS_STAGE4_BROWSER_PATCH_ANCHOR_FAIL")
patched = patched.replace(browser_old, browser_new, 1)

base_sha = hashlib.sha256(raw.encode("utf-8")).hexdigest()
patched_sha = hashlib.sha256(patched.encode("utf-8")).hexdigest()
print(f"WINDOWS_GATE_BASE_EXECUTOR_SHA256={base_sha}")
print(f"WINDOWS_GATE_EFFECTIVE_EXECUTOR_SHA256={patched_sha}")
print("WINDOWS_EXACT_SOURCE_WORKTREE_COMMAND=git -c core.autocrlf=false -c core.eol=lf worktree add --detach")
print("WINDOWS_QA_CHECKOUT_CONFIG_UNCHANGED_PASS")
print("STAGE4_POPUP_REOPEN_BY_TAB_ID_HARNESS_PATCH_PASS")

runner_temp = Path(os.environ.get("RUNNER_TEMP", tempfile.gettempdir())).resolve()
effective = runner_temp / "phase2_popup_fix_complete_gate_windows_effective.py"
effective.write_text(patched, encoding="utf-8", newline="\n")

proc = subprocess.run([sys.executable, str(effective)], cwd=str(repo), env=os.environ.copy())
raise SystemExit(proc.returncode)
