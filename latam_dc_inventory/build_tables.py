#!/usr/bin/env python3
"""Build facilities + operators tables from parsed facility records.

Applies dedup, relevance scoring, tags, leaseable_signal, confidence, and the
operator roll-up. Merges optional enrichment (datacenters.com / cloudscene).
Writes facilities_wave_A.csv and operators_wave_A.csv.
"""
import os
import re
import json
import csv
import unicodedata

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")

PRIORITY_METRO_SLUGS = {
    "sao-paulo", "rio-de-janeiro", "queretaro", "mexico-city", "bogota", "medellin",
}
PRIORITY_METRO_DISPLAY = {
    "São Paulo", "Rio de Janeiro", "Querétaro", "Mexico City", "Bogotá", "Medellín",
}

# Known major / hyperscale-class colo & wholesale operators active in LatAm.
KNOWN_MAJORS = {
    "equinix", "ascenty-data-centers", "ascenty", "odata-an-aligned-data-centers-company",
    "odata", "aligned", "scala-data-centers", "scala", "cirion", "elea-digital",
    "elea-data-centers", "nabiax", "edgeconnex", "digital-realty", "kio", "kio-networks",
    "tecto", "hostdime", "vtal", "takoda", "angola-cables", "datacenter1",
    "layer-9", "layer9", "sonda", "gorila", "cirion-technologies",
}
# Telco operators (captive unless they clearly sell colo footprint).
TELCO_NAMES = {
    "vivo", "claro", "tim", "telefonica", "telefónica", "oi", "algar", "algar-telecom",
    "telmex", "axtel", "megacable", "etb", "tigo", "movistar", "entel", "gtd",
    "internexa", "america-movil", "at&t", "izzi", "totalplay", "une",
}
HYPERSCALE_HINT = re.compile(r"hyperscale|build[\s-]to[\s-]suit|wholesale", re.I)


def strip_accents(s):
    return "".join(c for c in unicodedata.normalize("NFKD", s) if not unicodedata.combining(c))


def norm(s):
    if not s:
        return ""
    return re.sub(r"[^a-z0-9]+", " ", strip_accents(s).lower()).strip()


def is_telco(op_name, op_slug):
    n = norm(op_name)
    s = (op_slug or "").lower()
    for t in TELCO_NAMES:
        tn = norm(t)
        if tn and (tn in n.split() or tn == n or tn in s):
            return True
    return False


def has_colo(rec):
    if any(rec.get(k) for k in ("colo_cages", "private_cabinets", "partial_cabinets")):
        return True
    if "Suites" in rec.get("raw_services", []) or "Footprints" in rec.get("raw_services", []):
        return True
    return bool(rec.get("colo_mention"))


def market_slug_of(rec):
    # derive from facility_url .../<country>/<market>/<facility>/
    m = re.match(r"https://www\.datacentermap\.com/([^/]+)/([^/]+)/", rec["facility_url"])
    return m.group(2) if m else ""


def dedup_key(rec):
    op = rec.get("operator_slug") or norm(rec.get("operator_name"))
    sc = rec.get("site_code")
    if sc:
        return (op, "sc:" + norm(sc))
    return (op, "ad:" + norm(rec.get("address")))


def derive_parent(rec):
    name = rec.get("operator_name") or ""
    # patterns like "ODATA, an Aligned Data Centers Company" / "Foo (Bar)"
    m = re.search(r",?\s+an?\s+(.+?)\s+company", name, re.I)
    if m:
        return m.group(1).strip()
    m = re.search(r"\(([^)]+)\)", name)
    if m:
        return m.group(1).strip()
    return None


def load_enrichment():
    path = os.path.join(DATA, "enrichment.json")
    if os.path.exists(path):
        with open(path) as f:
            return json.load(f)
    return {"operators": {}, "metros": {}}


def main():
    with open(os.path.join(DATA, "facilities_raw.json"), encoding="utf-8") as f:
        recs = json.load(f)
    enrich = load_enrichment()

    # ---------- dedup ----------
    seen = {}
    for r in recs:
        k = dedup_key(r)
        r["_dupkey"] = k
        if k in seen:
            seen[k]["_dupcount"] += 1
            r["_is_dup"] = True
            r["_dup_of"] = seen[k]["facility_url"]
            r["_dupcount"] = 0
        else:
            r["_is_dup"] = False
            r["_dup_of"] = None
            r["_dupcount"] = 0
            seen[k] = r

    # ---------- operator pre-aggregation (for multi-site signal) ----------
    op_facs = {}
    for r in recs:
        op = r.get("operator_slug") or norm(r.get("operator_name")) or "unknown"
        op_facs.setdefault(op, []).append(r)

    def multi_site_latam(r):
        op = r.get("operator_slug") or norm(r.get("operator_name")) or "unknown"
        cnt = len([x for x in op_facs[op] if not x["_is_dup"]])
        return cnt >= 2 or (r.get("operator_total_dc") or 0) >= 3

    # ---------- per-facility scoring / tags ----------
    for r in recs:
        mslug = market_slug_of(r)
        r["_market_slug"] = mslug
        priority = mslug in PRIORITY_METRO_SLUGS
        r["_priority_metro"] = priority
        colo = has_colo(r)
        telco = is_telco(r.get("operator_name"), r.get("operator_slug"))
        gov = bool(r.get("gov_captive_mention"))
        op_slug = (r.get("operator_slug") or "").lower()
        known_big = op_slug in KNOWN_MAJORS or (r.get("operator_total_dc") or 0) >= 20
        ai = bool(r.get("ai_mentions"))
        wholesale = bool(r.get("wholesale_mention"))
        ai_wholesale_player = ai or wholesale
        mw_known = r.get("it_capacity_mw") is not None
        ms = multi_site_latam(r)
        captive = (telco and not colo) or (gov and not colo)

        # tags
        tags = []
        if wholesale:
            tags.append("Wholesale")
        if colo:
            tags.append("Colo")
        blob = norm((r.get("facility_name") or "") + " " + (r.get("operator_name") or ""))
        if "edge" in blob:
            tags.append("Edge")
        if wholesale or "hyperscale" in norm(" ".join(r.get("ai_mentions", []))) or known_big and wholesale:
            if "Hyperscale" not in tags:
                tags.append("Hyperscale")
        if telco and not colo:
            tags.append("TelcoCaptive")
        if gov:
            tags.append("GovCaptive")
        if ai:
            tags.append("AIMention")
        if ms:
            tags.append("MultiSiteOperator")
        r["_tags"] = tags

        # leaseable signal
        if colo or wholesale:
            leaseable = "Yes"
        elif captive:
            leaseable = "No"
        else:
            leaseable = "Unclear"
        r["_leaseable"] = leaseable

        # relevance
        score, reason = 1, ""
        if r["_is_dup"]:
            score, reason = 1, "Duplicate listing of an already-captured site (campus noise)."
        elif captive:
            score, reason = 1, ("Captive %s site with no public colocation footprint."
                                % ("government/military" if gov else "telco"))
        elif not colo and not wholesale:
            # non-commercial / unclear leaseability
            if priority and (known_big or ai_wholesale_player):
                score, reason = 3, "In priority metro with major-operator/AI signal but colo footprint unclear."
            else:
                score, reason = 2 if priority else 1, (
                    "Commercial status unclear; no public colo/wholesale signal"
                    + ("." if priority else ", outside priority metro.")
                )
        else:
            # commercial colo / wholesale present
            if priority:
                if ms and (mw_known or colo):
                    score, reason = 5, "Multi-site LatAm colo/wholesale operator in a priority metro with known MW or clear commercial colo."
                elif known_big:
                    score, reason = 4, "Major colo/IX-dense operator (Equinix-class) in a priority metro."
                elif ai_wholesale_player:
                    score, reason = 4, "Known AI/wholesale player with commercial colo in a priority metro."
                else:
                    score, reason = 3, "Mid-size commercial colocation in a priority metro."
            else:
                if known_big or ai_wholesale_player:
                    score, reason = 4, "Major or AI/wholesale colo operator (commercial colo) though outside a priority metro."
                elif ms:
                    score, reason = 3, "Multi-site commercial colo operator outside priority metros."
                else:
                    score, reason = 2, "Small/standalone commercial colo outside priority metros."
        r["_score"] = score
        r["_reason"] = reason
        r["_exclude"] = score == 1

        # confidence
        signals = sum([
            bool(r.get("operator_name")),
            bool(r.get("address")),
            bool(r.get("raw_services")),
            bool(r.get("certifications")) or bool(r.get("description_present")),
        ])
        r["_confidence"] = "High" if signals >= 4 else ("Med" if signals >= 2 else "Low")

    # ---------- write facilities CSV ----------
    fac_fields = [
        "facility_name", "site_code", "operator_name", "operator_parent", "country",
        "metro", "city", "address", "it_capacity_mw", "colo_cages", "private_cabinets",
        "partial_cabinets", "bare_metal", "remote_hands", "public_cloud",
        "certifications", "leaseable_signal", "nearest_facilities", "operator_website",
        "facility_url", "datacenters_com_url", "cloudscene_url", "relevance_score",
        "relevance_reason", "tags", "confidence", "exclude_from_outreach",
        "scraped_at", "source_url", "notes",
    ]
    fac_rows = []
    for r in recs:
        op = r.get("operator_slug") or norm(r.get("operator_name"))
        op_enr = enrich.get("operators", {}).get(op, {})
        metro_enr = enrich.get("metros", {}).get(r["_market_slug"], {})
        notes = []
        if r["_dupcount"]:
            notes.append(f"{r['_dupcount']} sibling listing(s) share operator+address (campus).")
        if r["_is_dup"]:
            notes.append(f"Duplicate of {r['_dup_of']}.")
        if r.get("operator_hq"):
            notes.append(f"Operator HQ: {r['operator_hq']}.")
        if r.get("operator_total_dc"):
            notes.append(f"Operator lists {r['operator_total_dc']} DCs globally on DCM.")
        if r.get("raw_services"):
            notes.append("Services offered: " + ", ".join(r["raw_services"]) + ".")
        if metro_enr.get("connectivity"):
            notes.append(f"Metro connectivity (Cloudscene): {metro_enr['connectivity']}.")
        if op_enr.get("claims"):
            notes.append("datacenters.com: " + op_enr["claims"])
        fac_rows.append({
            "facility_name": r.get("facility_name"),
            "site_code": r.get("site_code") or "",
            "operator_name": r.get("operator_name"),
            "operator_parent": derive_parent(r) or "",
            "country": r.get("country"),
            "metro": r.get("metro"),
            "city": r.get("city") or "",
            "address": r.get("address") or "",
            "it_capacity_mw": r.get("it_capacity_mw") if r.get("it_capacity_mw") is not None else "",
            "colo_cages": r.get("colo_cages"),
            "private_cabinets": r.get("private_cabinets"),
            "partial_cabinets": r.get("partial_cabinets"),
            "bare_metal": r.get("bare_metal"),
            "remote_hands": r.get("remote_hands"),
            "public_cloud": r.get("public_cloud"),
            "certifications": "; ".join(r.get("certifications", [])),
            "leaseable_signal": r["_leaseable"],
            "nearest_facilities": "; ".join(r.get("nearest_facilities", [])),
            "operator_website": r.get("operator_website") or "",
            "facility_url": r.get("facility_url"),
            "datacenters_com_url": op_enr.get("datacenters_com_url", ""),
            "cloudscene_url": metro_enr.get("cloudscene_url", ""),
            "relevance_score": r["_score"],
            "relevance_reason": r["_reason"],
            "tags": ", ".join(r["_tags"]),
            "confidence": r["_confidence"],
            "exclude_from_outreach": r["_exclude"],
            "scraped_at": r.get("scraped_at"),
            "source_url": r.get("facility_url"),
            "notes": " ".join(notes),
        })

    fac_rows.sort(key=lambda x: (-x["relevance_score"], x["country"], x["metro"], str(x["operator_name"])))
    with open(os.path.join(DATA, "facilities_wave_A.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fac_fields)
        w.writeheader()
        w.writerows(fac_rows)

    # ---------- operator roll-up ----------
    op_fields = [
        "operator_name", "parent_company", "countries_present", "facility_count_wave_A",
        "total_mw_known", "mw_coverage_pct", "has_colo_wholesale", "ai_or_gpu_mentions",
        "max_relevance", "partnership_openness_guess", "priority_for_outreach", "source_urls",
    ]
    op_rows = []
    for op, group in op_facs.items():
        live = [x for x in group if not x["_is_dup"]]
        if not live:
            live = group
        name = live[0].get("operator_name") or op
        parent = next((derive_parent(x) for x in live if derive_parent(x)), None)
        countries = sorted({x.get("country") for x in live if x.get("country")})
        fcount = len(live)
        mws = [x["it_capacity_mw"] for x in live if x.get("it_capacity_mw") is not None]
        total_mw = round(sum(mws), 1) if mws else 0
        coverage = round(100.0 * len(mws) / fcount, 0) if fcount else 0
        colo_wh = any(has_colo(x) or x.get("wholesale_mention") for x in live)
        ai_terms = sorted({t for x in live for t in x.get("ai_mentions", [])})
        op_enr = enrich.get("operators", {}).get(op, {})
        if op_enr.get("ai_terms"):
            ai_terms = sorted(set(ai_terms) | set(op_enr["ai_terms"]))
        max_rel = max(x["_score"] for x in live)
        telco = is_telco(name, op)
        gov = any(x.get("gov_captive_mention") for x in live)
        known_big = op in KNOWN_MAJORS or (live[0].get("operator_total_dc") or 0) >= 20
        # openness heuristic
        if colo_wh and (max_rel >= 4 or ai_terms or known_big):
            openness = "High"
        elif colo_wh:
            openness = "Med"
        elif telco or gov:
            openness = "Low"
        else:
            openness = "Unknown"
        priority = "Yes" if (max_rel >= 4 or (fcount >= 3 and colo_wh)) else "No"
        srcs = [x["facility_url"] for x in live]
        if op_enr.get("datacenters_com_url"):
            srcs.append(op_enr["datacenters_com_url"])
        op_rows.append({
            "operator_name": name,
            "parent_company": parent or op_enr.get("parent") or "Unknown",
            "countries_present": ", ".join(countries),
            "facility_count_wave_A": fcount,
            "total_mw_known": total_mw,
            "mw_coverage_pct": f"{int(coverage)}%",
            "has_colo_wholesale": colo_wh,
            "ai_or_gpu_mentions": ", ".join(ai_terms) if ai_terms else "",
            "max_relevance": max_rel,
            "partnership_openness_guess": openness,
            "priority_for_outreach": priority,
            "source_urls": " | ".join(srcs),
        })

    op_rows.sort(key=lambda x: (-x["max_relevance"], -x["facility_count_wave_A"], str(x["operator_name"])))
    with open(os.path.join(DATA, "operators_wave_A.csv"), "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=op_fields)
        w.writeheader()
        w.writerows(op_rows)

    print(f"facilities rows: {len(fac_rows)} | operators: {len(op_rows)}")
    from collections import Counter
    print("score dist:", dict(sorted(Counter(x['relevance_score'] for x in fac_rows).items())))
    print("dups:", sum(1 for r in recs if r['_is_dup']))


if __name__ == "__main__":
    main()
