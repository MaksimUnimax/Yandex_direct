"""Run the preserved 254 assertions on EXACT B10, not on B9 or arbitrary bytes.
Usage: python qa/b10_regression_campaign.py OWNER014 B10_QA EMPTY_LOG_DIR
Only the pinned candidate tree identity is retargeted; test code/hash guards unchanged.
"""
from pathlib import Path
import hashlib
ROOT = Path(__file__).resolve().parent.parent
SOURCE_SHA = 'd3749aa59ab394ba2595337fb760dfc3e0cdcb926f7c7a2206f53e6252ca3d09'
OLD_TREE = 'd1fc4f49718f023f1bc1a6a3ec921fa7253d63b805cedadff6fbcf2e70180612'
NEW_TREE = '191b3ed1222733cb9d3aed805b53084829740d10ad906c5246d2cf185fc9ae94'
p = ROOT / 'qa/b9_regression_campaign.py'
data = p.read_bytes()
if hashlib.sha256(data).hexdigest() != SOURCE_SHA:
    raise ValueError('Preserved regression campaign changed')
text = data.decode('utf-8')
if text.count(OLD_TREE) != 1:
    raise ValueError('Unexpected candidate guard layout')
text = text.replace(OLD_TREE, NEW_TREE).replace('Wrong B9 candidate', 'Wrong B10 candidate')
# __file__ deliberately remains the pinned original, so all test paths/hashes stay intact.
exec(compile(text, str(p), 'exec'), {'__name__': '__main__', '__file__': str(p)})
