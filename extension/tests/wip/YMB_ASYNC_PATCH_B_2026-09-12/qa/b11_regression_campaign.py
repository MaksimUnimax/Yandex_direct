"""Run preserved 254 module assertions on exact B11; no Chrome/provider proof.
Usage: python qa/b11_regression_campaign.py OWNER014 B11_QA EMPTY_LOG_DIR
"""
from pathlib import Path
import hashlib
ROOT = Path(__file__).resolve().parent.parent
p = ROOT / 'qa/b9_regression_campaign.py'
data = p.read_bytes()
if hashlib.sha256(data).hexdigest() != 'd3749aa59ab394ba2595337fb760dfc3e0cdcb926f7c7a2206f53e6252ca3d09':
    raise ValueError('Preserved regression runner changed')
old = 'd1fc4f49718f023f1bc1a6a3ec921fa7253d63b805cedadff6fbcf2e70180612'
new = '5fd8a55e980fa54fe5371a51070e9e899307319c8f1ee3255fdc0857b31ebd26'
text = data.decode()
if text.count(old) != 1:
    raise ValueError('Unexpected tree guard')
text = text.replace(old, new).replace('Wrong B9 candidate','Wrong B11 candidate')
exec(compile(text,str(p),'exec'),{'__name__':'__main__','__file__':str(p)})
