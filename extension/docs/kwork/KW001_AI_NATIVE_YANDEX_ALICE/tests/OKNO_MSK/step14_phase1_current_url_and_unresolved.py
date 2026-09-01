from __future__ import annotations

import csv
import json
import re
import ssl
import time
import urllib.error
import urllib.parse
import urllib.request
from collections import defaultdict
from html.parser import HTMLParser
from pathlib import Path

BASE = Path(__file__).resolve().parent
DATE = "2026-09-01"
SITE_HOST = "okno-msk.ru"

ACTIONS = BASE / "STEP_12_STRUCTURAL_ACTIONS_CORRECTED_V6.tsv"
PHRASES = BASE / "STEP_12_PHRASE_ACTION_MAP_FINAL_V6.tsv"
LINKS = BASE / "STEP_12_INTERNAL_LINK_ACTIONS_V6.tsv"
CONFLICTS = BASE / "STEP_13_CONFLICT_DIAGNOSIS.tsv"
PAGE_EVIDENCE = BASE / "STEP_13_CURRENT_PAGE_EVIDENCE.tsv"
PAGE_EVIDENCE_EXT = BASE / "STEP_13_CURRENT_PAGE_EVIDENCE_EXTENSION.tsv"
STATE_PATH = BASE / "STEP_14_CURRENT_STATE.json"

OUT_URLS = BASE / "STEP_14_CURRENT_URL_RECHECK.tsv"
OUT_UNRESOLVED = BASE / "STEP_14_UNRESOLVED_REVIEW_PACKET.tsv"
OUT_QA = BASE / "STEP_14_PHASE1_QA_2026-09-01.json"


def read_tsv(path: Path):
    with path.open("r", encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f, delimiter="\t"))


def write_tsv(path: Path, rows, fields):
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=fields, delimiter="\t", lineterminator="\n")
        w.writeheader()
        for row in rows:
            w.writerow({k: row.get(k, "") for k in fields})


def normalize_url(raw: str) -> str:
    raw = (raw or "").strip()
    if not raw or raw.startswith("PROPOSED_NEW:"):
        return ""
    if not raw.startswith(("http://", "https://")):
        return ""
    p = urllib.parse.urlsplit(raw)
    host = (p.hostname or "").lower()
    if host.startswith("www."):
        host = host[4:]
    if host != SITE_HOST:
        return ""
    path = re.sub(r"/{2,}", "/", p.path or "/")
    if path != "/":
        path = path.rstrip("/")
    return urllib.parse.urlunsplit(("https", SITE_HOST, path, "", ""))


def split_urls(value: str):
    out = []
    for piece in (value or "").split(";"):
        u = normalize_url(piece)
        if u:
            out.append(u)
    return out


class TextProbe(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.in_title = False
        self.h_depth = 0
        self.title = []
        self.h1 = []

    def handle_starttag(self, tag, attrs):
        tag = tag.lower()
        if tag == "title":
            self.in_title = True
        elif tag == "h1":
            self.h_depth += 1

    def handle_endtag(self, tag):
        tag = tag.lower()
        if tag == "title":
            self.in_title = False
        elif tag == "h1" and self.h_depth:
            self.h_depth -= 1

    def handle_data(self, data):
        txt = " ".join(data.split())
        if not txt:
            return
        if self.in_title:
            self.title.append(txt)
        if self.h_depth:
            self.h1.append(txt)


def fetch_url(url: str):
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/151.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
        "Accept-Language": "ru-RU,ru;q=0.9,en;q=0.7",
        "Cache-Control": "no-cache",
    }
    last = None
    ctx = ssl.create_default_context()
    for attempt in range(1, 4):
        try:
            req = urllib.request.Request(url + "/" if url != "https://okno-msk.ru" and not url.endswith("/") else url, headers=headers)
            with urllib.request.urlopen(req, timeout=25, context=ctx) as resp:
                status = int(getattr(resp, "status", 200))
                final = normalize_url(resp.geturl()) or resp.geturl()
                ctype = resp.headers.get("Content-Type", "")
                body = resp.read(2_500_000)
                text = body.decode("utf-8", errors="replace")
                probe = TextProbe()
                try:
                    probe.feed(text)
                except Exception:
                    pass
                title = " ".join(probe.title)[:500]
                h1 = " ".join(probe.h1)[:500]
                host_ok = normalize_url(final) != ""
                live = status == 200 and host_ok and len(body) >= 500
                return {
                    "http_status": status,
                    "final_url": normalize_url(final) or final,
                    "content_type": ctype,
                    "content_bytes": len(body),
                    "title": title,
                    "h1": h1,
                    "live_state": "LIVE_PASS" if live else "LIVE_FAIL",
                    "attempts": attempt,
                    "error": "",
                }
        except urllib.error.HTTPError as e:
            last = f"HTTPError:{e.code}"
            status = e.code
            if status not in (429, 500, 502, 503, 504):
                break
        except Exception as e:
            last = f"{type(e).__name__}:{e}"
        time.sleep(1.0 * attempt)
    return {
        "http_status": status if 'status' in locals() else "",
        "final_url": "",
        "content_type": "",
        "content_bytes": 0,
        "title": "",
        "h1": "",
        "live_state": "LIVE_FAIL_CLOSED",
        "attempts": 3,
        "error": last or "unknown_error",
    }


actions = read_tsv(ACTIONS)
phrases = read_tsv(PHRASES)
links = read_tsv(LINKS)
conflicts = read_tsv(CONFLICTS)
page_rows = read_tsv(PAGE_EVIDENCE) + read_tsv(PAGE_EVIDENCE_EXT)

assert len(actions) == 168, f"expected 168 structural units, got {len(actions)}"
assert len(phrases) == 2332, f"expected 2332 phrase rows, got {len(phrases)}"
assert len(links) == 58, f"expected 58 link rows, got {len(links)}"
assert len(conflicts) == 21, f"expected 21 Step13 cases, got {len(conflicts)}"

page_evidence_by_url = {}
for r in page_rows:
    u = normalize_url(r.get("url", ""))
    if u:
        page_evidence_by_url[u] = r

url_sources = defaultdict(set)
critical_primary = set()
critical_link = set()

for r in actions:
    sid = r.get("structural_unit_id", "")
    for col in ("primary_page_candidate", "supporting_page", "intended_target_url", "current_yandex_relevant_url"):
        for u in split_urls(r.get(col, "")):
            url_sources[u].add(f"STEP12_ACTION:{sid}:{col}")
            if col in ("primary_page_candidate", "intended_target_url"):
                critical_primary.add(u)

for r in links:
    lid = r.get("link_action_id", "")
    for col in ("source_url", "target_url"):
        for u in split_urls(r.get(col, "")):
            url_sources[u].add(f"STEP12_LINK:{lid}:{col}:{r.get('link_action_state','')}")
            if r.get("link_action_state") == "IMPLEMENT":
                critical_link.add(u)

for r in conflicts:
    qf = r.get("case_id", "")
    for col in ("primary_owner", "supporting_or_other_url"):
        for u in split_urls(r.get(col, "")):
            url_sources[u].add(f"STEP13_CASE:{qf}:{col}")
            if col == "primary_owner":
                critical_primary.add(u)

for u, r in page_evidence_by_url.items():
    url_sources[u].add(f"STEP13_PAGE_EVIDENCE:{r.get('url_id','')}")

url_rows = []
for idx, url in enumerate(sorted(url_sources), 1):
    probe = fetch_url(url)
    ev = page_evidence_by_url.get(url, {})
    if url in critical_primary:
        criticality = "PRIMARY_OR_STEP13_OWNER"
    elif url in critical_link:
        criticality = "IMPLEMENT_LINK_ENDPOINT"
    else:
        criticality = "SUPPORTING_OR_CONTEXT"
    if probe["live_state"] == "LIVE_PASS" and ev:
        role_state = "PASS_LIVE_EXISTENCE__CURRENT_ROLE_EVIDENCE_PRESENT"
    elif probe["live_state"] == "LIVE_PASS":
        role_state = "PASS_LIVE_EXISTENCE__ROLE_FROM_STEP12_OR_STEP13_RELATION_ONLY"
    else:
        role_state = "FAIL_CLOSED__AFFECTED_FREEZE_MUST_BLOCK"
    url_rows.append({
        "url_recheck_id": f"UR{idx:03d}",
        "url": url,
        "criticality": criticality,
        "evidence_sources": ";".join(sorted(url_sources[url])),
        "http_status": probe["http_status"],
        "final_url": probe["final_url"],
        "live_state": probe["live_state"],
        "attempts": probe["attempts"],
        "content_bytes": probe["content_bytes"],
        "title": probe["title"],
        "h1": probe["h1"],
        "step13_page_role": ev.get("page_role", ""),
        "step13_primary_object": ev.get("primary_object", ""),
        "step13_primary_user_task": ev.get("primary_user_task", ""),
        "step13_freshness_state": ev.get("freshness_state", ""),
        "role_compatibility_state": role_state,
        "error": probe["error"],
    })

write_tsv(
    OUT_URLS,
    url_rows,
    [
        "url_recheck_id", "url", "criticality", "evidence_sources", "http_status", "final_url", "live_state",
        "attempts", "content_bytes", "title", "h1", "step13_page_role", "step13_primary_object",
        "step13_primary_user_task", "step13_freshness_state", "role_compatibility_state", "error",
    ],
)

unresolved = [r for r in phrases if r.get("structural_action") == "DEFER_UNRESOLVED"]
assert len(unresolved) == 19, f"expected 19 unresolved rows, got {len(unresolved)}"
unresolved_rows = []
for idx, r in enumerate(unresolved, 1):
    unresolved_rows.append({
        "unresolved_id": f"UNR{idx:02d}",
        "phrase": r.get("phrase", ""),
        "final_structural_unit_id": r.get("final_structural_unit_id", ""),
        "step12_structural_action": r.get("structural_action", ""),
        "step12_gap_type": r.get("gap_type", ""),
        "step12_optimization_readiness": r.get("optimization_readiness", ""),
        "step12_recommendation_maturity": r.get("recommendation_maturity", ""),
        "step12_final_confidence": r.get("final_confidence", ""),
        "architecture_material": "REVIEW_REQUIRED",
        "affected_freeze_unit": r.get("final_structural_unit_id", ""),
        "phase1_disposition": "PRESERVE_UNASSIGNED__NO_SILENT_ASSIGNMENT_OR_DROP",
        "review_reason": "S14-R09 requires explicit architecture_material=true/false before final freeze.",
    })

write_tsv(
    OUT_UNRESOLVED,
    unresolved_rows,
    [
        "unresolved_id", "phrase", "final_structural_unit_id", "step12_structural_action", "step12_gap_type",
        "step12_optimization_readiness", "step12_recommendation_maturity", "step12_final_confidence",
        "architecture_material", "affected_freeze_unit", "phase1_disposition", "review_reason",
    ],
)

live_pass = sum(r["live_state"] == "LIVE_PASS" for r in url_rows)
live_fail = len(url_rows) - live_pass
critical_fail = sum(
    r["live_state"] != "LIVE_PASS" and r["criticality"] in ("PRIMARY_OR_STEP13_OWNER", "IMPLEMENT_LINK_ENDPOINT")
    for r in url_rows
)

qa = {
    "date": DATE,
    "job": "OKNO_MSK",
    "step": 14,
    "phase": 1,
    "status": "PASS_PENDING_MANUAL_UNRESOLVED_CLASSIFICATION" if critical_fail == 0 else "FAIL_CLOSED_CURRENT_URL_RECHECK",
    "input_counts": {
        "active_phrases": len(phrases),
        "structural_units": len(actions),
        "step12_link_rows": len(links),
        "step13_cases": len(conflicts),
    },
    "current_url_recheck": {
        "unique_urls": len(url_rows),
        "live_pass": live_pass,
        "live_fail_or_indeterminate": live_fail,
        "critical_fail_closed": critical_fail,
    },
    "unresolved": {
        "expected": 19,
        "materialized": len(unresolved_rows),
        "architecture_material_review_required": len(unresolved_rows),
        "silent_assignment": 0,
        "silent_drop": 0,
    },
    "provider_calls_executed": 0,
    "provider_cost_rub": 0.0,
    "gensearch_or_alice_calls": 0,
    "step15_executed": False,
    "step16_executed": False,
    "next_action": "Review all 19 unresolved rows, set architecture_material true/false, then run final Step14 freeze."
}
OUT_QA.write_text(json.dumps(qa, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

state = json.loads(STATE_PATH.read_text(encoding="utf-8"))
state.update({
    "owner_authorization": True,
    "execution_started": True,
    "execution_complete": False,
    "status": "EXECUTION_PHASE1_COMPLETE__CURRENT_URL_RECHECK_MATERIALIZED__UNRESOLVED_REVIEW_REQUIRED" if critical_fail == 0 else "EXECUTION_PHASE1_FAIL_CLOSED__CURRENT_URL_RECHECK_BLOCKER",
    "provider_calls_authorized": False,
    "provider_calls_executed": 0,
    "provider_cost_rub_step14": 0.0,
})
state["mandatory_current_site_recheck"] = {
    "required_before_freeze": True,
    "executed": True,
    "affected_unit_fail_closed": True,
    "unique_urls_checked": len(url_rows),
    "live_pass": live_pass,
    "live_fail_or_indeterminate": live_fail,
    "critical_fail_closed": critical_fail,
}
state["next_required_action"] = qa["next_action"]
STATE_PATH.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

print("STEP14_PHASE1_COMPLETE", json.dumps({
    "urls": len(url_rows), "live_pass": live_pass, "critical_fail": critical_fail, "unresolved": len(unresolved_rows)
}, ensure_ascii=False))
