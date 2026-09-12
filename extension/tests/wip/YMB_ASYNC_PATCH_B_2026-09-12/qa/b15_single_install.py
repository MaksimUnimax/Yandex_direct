"""QA-only B15 launcher correction; never edits the extension/package.
The saved B14-derived launcher combined enableExtensions=[path] (which invokes
Browser.installExtension) AND --load-extension=path. Use the already historical
boolean enableExtensions + CLI path only. Preserve the original failing script.
"""
from pathlib import Path
import hashlib
p=Path(__file__).with_name('b15_browser_qualification.mjs')
b=p.read_bytes()
assert hashlib.sha256(b).hexdigest()=='b464224139ac2fe0ff7e194f76d4e38e1c5ec9ef144f075df3aafb9d3ec9423d'
needle=b'enableExtensions:[root],protocolTimeout:120000'
assert b.count(needle)==1
new=b.replace(needle,b'enableExtensions:true,protocolTimeout:120000')
p.write_bytes(new)
print('QA_ONLY_SINGLE_INSTALL',hashlib.sha256(new).hexdigest())
