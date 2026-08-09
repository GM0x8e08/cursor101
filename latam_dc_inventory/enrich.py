#!/usr/bin/env python3
"""Enrichment pass (runs after Wave A facilities exist).

For operators with relevance >=4 OR facility_count >=3:
  - scrape their DataCenterMap operator page (/c/<slug>/) for real website,
    parent, global DC count and AI/wholesale text;
  - find + scrape their datacenters.com profile for AI/wholesale claims.
For priority metros (Sao Paulo, Queretaro, Bogota) only:
  - find + scrape the Cloudscene market page and rate carrier/IX density.

Writes data/enrichment.json consumed by build_tables.py. Everything cached.
"""
import os
import re
import json
import subprocess
import csv
from scraper import scrape, slug_for
from config import CFG, FCOUNT_COL

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")
ENR_DIR = os.path.join(ROOT, CFG["enrich_dir"])

AI_KEYWORDS = [
    "artificial intelligence", "ai ", " ai", "gpu", "hpc",
    "high-performance computing", "high performance computing", "machine learning",
    "accelerated", "nvidia", "supercomput", "liquid cool", "inference", "training",
]
WHOLESALE_KEYWORDS = ["wholesale", "build-to-suit", "build to suit", "hyperscale"]


def fc_search(query, limit=5):
    out = os.path.join(ENR_DIR, "search__" + re.sub(r"[^a-z0-9]+", "_", query.lower())[:60] + ".json")
    os.makedirs(ENR_DIR, exist_ok=True)
    if not os.path.exists(out):
        for attempt in range(4):
            proc = subprocess.run(
                ["firecrawl", "search", query, "--limit", str(limit), "-o", out, "--json"],
                capture_output=True, text=True, timeout=120,
            )
            combined = (proc.stdout + proc.stderr).lower()
            if os.path.exists(out) and "rate limit" not in combined and "429" not in combined:
                break
            import time
            time.sleep(6 * (attempt + 1))
    try:
        d = json.load(open(out))
    except Exception:
        return []
    urls = []
    web = (d.get("data") or {}).get("web") or d.get("web") or []
    for item in web:
        u = item.get("url")
        if u:
            urls.append(u)
    return urls


def extract_ai_wholesale(text):
    low = text.lower()
    ai_terms = sorted({k.strip() for k in AI_KEYWORDS if k.strip() and k in low
                       and k.strip() not in ("ai",)})
    if re.search(r"\bai\b|a\.i\.", low):
        ai_terms.append("AI")
    wh = [k for k in WHOLESALE_KEYWORDS if k in low]
    return sorted(set(ai_terms)), sorted(set(wh))


def snippet(text, terms, n=260):
    low = text.lower()
    for t in terms:
        i = low.find(t)
        if i >= 0:
            s = max(0, i - 80)
            return re.sub(r"\s+", " ", text[s:s + n]).strip()
    return ""


def enrich_operators(qualifying):
    ops = {}
    for slug, name in qualifying:
        entry = {}
        # (a) DCM operator page
        dcm_url = f"https://www.datacentermap.com/c/{slug}/"
        dcm_out = os.path.join(ENR_DIR, "op__" + slug + ".md")
        if scrape(dcm_url, dcm_out):
            txt = open(dcm_out, encoding="utf-8", errors="replace").read()
            # operator website is masked behind a DCM /visit/ redirect
            m = re.search(r"\[Visit Website\]\((https://www\.datacentermap\.com/visit/[^)]+)\)", txt)
            if m:
                entry["website_redirect"] = m.group(1)
            tk = re.search(r"Ticker:\s*\$?([A-Z.:]+)", txt)
            if tk:
                entry["ticker"] = tk.group(1)
            hq = re.search(r"Headquartered in\s+([^\n]+)", txt)
            if hq:
                # keep only the first clause (avoid trailing prose)
                h = re.split(r"[.,]| and | it | which |\bfounded\b", hq.group(1).strip())[0].strip()
                entry["hq"] = hq.group(1).strip().rstrip(".")[:120]
            # parent hints: "part of / owned by / subsidiary of / a X company"
            pm = re.search(r"(?:part of|owned by|subsidiary of|a subsidiary of|founded by|backed by)\s+([A-Z][\w&.,'\- ]{2,40})", txt)
            if pm:
                entry["parent"] = pm.group(1).strip().rstrip(".")
            ai_terms, wh = extract_ai_wholesale(txt)
            if ai_terms:
                entry["ai_terms"] = ai_terms
            entry["dcm_operator_url"] = dcm_url
        # (b) datacenters.com profile
        urls = fc_search(f"{name} data center site:datacenters.com", limit=5)
        dcom = next((u for u in urls if "datacenters.com" in u), None)
        if dcom:
            dcom_out = os.path.join(ENR_DIR, "dcom__" + slug_for(dcom.rstrip("/")) + ".md")
            if scrape(dcom, dcom_out):
                dtxt = open(dcom_out, encoding="utf-8", errors="replace").read()
                entry["datacenters_com_url"] = dcom
                ai_terms, wh = extract_ai_wholesale(dtxt)
                claims = []
                if ai_terms:
                    claims.append("AI/GPU terms: " + ", ".join(ai_terms))
                    entry["ai_terms"] = sorted(set(entry.get("ai_terms", [])) | set(ai_terms))
                if wh:
                    claims.append("wholesale/hyperscale terms: " + ", ".join(wh))
                sn = snippet(dtxt, ["wholesale", "hyperscale", "artificial intelligence", "gpu", "colocation"]) 
                if sn:
                    claims.append("blurb: " + sn)
                if claims:
                    entry["claims"] = " | ".join(claims)
        ops[slug] = entry
        print(f"  enriched operator {slug}: {list(entry.keys())}", flush=True)
    return ops


def rate_density(text):
    # crude qualitative rating from counts on a Cloudscene market page.
    # counts appear either as "254 Service Providers" or "Service Providers (254)".
    def count(*pats):
        best = 0
        for pat in pats:
            for m in re.finditer(pat, text, re.I):
                best = max(best, int(m.group(1).replace(",", "")))
        return best
    providers = count(
        r"([\d,]+)\s+(?:network|service)\s+providers?",
        r"(?:network|service)\s+providers?\s*\(([\d,]+)\)",
    )
    fabrics = count(
        r"([\d,]+)\s+(?:cloud|network)?\s*fabrics?",
        r"(?:cloud|network)?\s*fabrics?\s*\(([\d,]+)\)",
    )
    dcs = count(
        r"([\d,]+)\s+data\s+cent",
        r"data\s+centers?\s*\(([\d,]+)\)",
    )
    score = providers + fabrics
    if providers >= 80 or score >= 120:
        level = "High"
    elif providers >= 25 or score >= 40:
        level = "Med"
    elif providers > 0 or dcs > 0:
        level = "Low"
    else:
        level = "Unknown"
    detail = f"{providers} network/service providers, {dcs} data centers listed (Cloudscene)"
    return level, detail


def _country_all_url(market_url: str) -> str | None:
    """Derive .../data-centers-in-<country>/all from a city market URL."""
    m = re.search(r"(https://cloudscene\.com/market/data-centers-in-[a-z-]+)/", market_url)
    if m:
        return m.group(1) + "/all"
    return None


def enrich_metros():
    # Cloudscene market pages follow /market/data-centers-in-<country>/<city>
    # Some city pages (e.g. Santiago) render only chrome without login; fall back
    # to the country /all page which still exposes provider/DC counts.
    metros = CFG["cloudscene"]
    out = {}
    for slug, (q, direct) in metros.items():
        candidates = [direct]
        country_all = _country_all_url(direct)
        if country_all and country_all not in candidates:
            candidates.append(country_all)
        entry = {}
        for cs in candidates:
            cs_out = os.path.join(ENR_DIR, "cs__" + slug + ".md")
            # force re-fetch when retrying a fallback URL after a thin first hit
            force = bool(entry) or (cs != direct)
            if not scrape(cs, cs_out, force=force):
                continue
            txt = open(cs_out, encoding="utf-8", errors="replace").read()
            level, detail = rate_density(txt)
            entry = {"cloudscene_url": cs, "connectivity": level, "connectivity_detail": detail}
            if level != "Unknown":
                if cs != direct:
                    entry["connectivity_detail"] += f" [fallback: country /all; city page {direct} was empty]"
                break
        if not entry:
            urls = fc_search(f"{q} data centers market site:cloudscene.com", limit=6)
            cs = next((u for u in urls if "cloudscene.com" in u and "/market/" in u), None) \
                or next((u for u in urls if "cloudscene.com" in u), None)
            if cs:
                cs_out = os.path.join(ENR_DIR, "cs__" + slug + ".md")
                if scrape(cs, cs_out, force=True):
                    txt = open(cs_out, encoding="utf-8", errors="replace").read()
                    level, detail = rate_density(txt)
                    entry = {"cloudscene_url": cs, "connectivity": level, "connectivity_detail": detail}
        out[slug] = entry
        print(f"  enriched metro {slug}: {entry.get('connectivity','n/a')}", flush=True)
    return out


def main():
    # qualifying operators from the roll-up
    qualifying = []
    op_csv = os.path.join(ROOT, CFG["operators_csv"])
    slug_by_name = {}
    with open(os.path.join(ROOT, CFG["raw"]), encoding="utf-8") as f:
        for r in json.load(f):
            if r.get("operator_slug") and r.get("operator_name"):
                slug_by_name.setdefault(r["operator_name"], r["operator_slug"])
    with open(op_csv, encoding="utf-8") as f:
        for o in csv.DictReader(f):
            if int(o["max_relevance"]) >= 4 or int(o[FCOUNT_COL]) >= 3:
                slug = slug_by_name.get(o["operator_name"])
                if slug:
                    qualifying.append((slug, o["operator_name"]))
    # dedupe
    seen = set()
    qualifying = [(s, n) for s, n in qualifying if not (s in seen or seen.add(s))]
    print(f"Qualifying operators for enrichment: {len(qualifying)}")

    ops = enrich_operators(qualifying)
    metros = enrich_metros()
    with open(os.path.join(ROOT, CFG["enrichment"]), "w") as f:
        json.dump({"operators": ops, "metros": metros}, f, indent=2, ensure_ascii=False)
    print("Wrote", CFG["enrichment"])


if __name__ == "__main__":
    main()
