"""QA-only bounded process-settlement diagnostic. Product bytes MUST stay unchanged.
Usage: b17_cleanup_recheck.py DOWNLOADED_B17_EVIDENCE NEW_OUTPUT.mjs
"""
from pathlib import Path
import sys, hashlib, json
root, out = map(Path, sys.argv[1:])
assert not out.exists()
h = lambda b: hashlib.sha256(b).hexdigest()
pkg = (root/'candidate-b17-internal.zip').read_bytes()
assert len(pkg) == 225660 and h(pkg) == '1560599adfcfdb2c3180ec9103005b1584bcd39709b8fc45e233f6c1bdd11ee1'
raw = (root/'tests/b16.generated.mjs').read_bytes()
assert h(raw) == '7505a79f955673c7f122b18c0c64ee3dd49de3696d27dbdfb92c3ee9fce49390'
for line in (root/'SHA256SUMS').read_text().splitlines():
    digest, name = line.split('  ', 1)
    if name == 'tests/b16.generated.mjs': assert h(raw) == digest
source = raw.decode()
assert source.count('\nfinally{clearInterval(monitor);clearTimeout(deadline);') == 1
prefix, old_cleanup = source.rsplit('\nfinally{', 1)
assert old_cleanup.endswith('process.exitCode=1;}\n')
assert "'b20b74351d95becd67f32994e3e00899e9208b8c32c778a306f73f6703bfe508'" in prefix
replacement = r'''
finally {
 clearInterval(monitor); clearTimeout(deadline);
 if (browser) try { await browser.close(); } catch {}
 const alive = () => {
  const rows = [];
  for (const p of observedPids) try {
   const text = fs.readFileSync('/proc/'+p+'/stat','utf8');
   const fields = text.slice(text.lastIndexOf(')')+2).split(' ');
   if (fields[0] !== 'Z') {
    let command = ''; try { command = fs.readFileSync('/proc/'+p+'/cmdline','utf8').replaceAll('\0',' ').slice(0,240); } catch {}
    rows.push({pid:p,state:fields[0],ppid:Number(fields[1]),start_ticks:fields[19],command});
   }
  } catch {}
  return rows;
 };
 const began = Date.now(); const initial = alive(); let remaining = initial;
 emit({case:'owned_cleanup_immediate_snapshot',status:'RECORDED',remaining:initial,settlement_limit_ms:2000});
 while (remaining.length && Date.now()-began < 2000) {
  await delay(100); remaining = alive();
  emit({case:'owned_cleanup_settlement_sample',status:'RECORDED',remaining,elapsed_ms:Date.now()-began});
 }
 emit({case:'owned_browser_cleanup',status:remaining.length?'FAIL':'PASS',remaining,
  initial_alive:initial.length,settlement_ms:Date.now()-began,settlement_limit_ms:2000,
  forced_kill:false,peak_owned_rss_kib:peak,resource_stop:resourceStop,failed,release_allowed:false});
 if (remaining.length || failed || resourceStop) process.exitCode=1;
}
'''
result = (prefix + replacement).encode()
assert result.decode().split('\nfinally {')[0] == prefix
out.write_bytes(result)
print(json.dumps({'input_test_sha256':h(raw),'output_test_sha256':h(result),'product_sha256':h(pkg),'product_assertion_prefix_unchanged':True,'change':'cleanup diagnostic only; final zero-live-PID assertion retained; bounded2s/no kill'},indent=2))
