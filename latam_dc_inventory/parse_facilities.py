#!/usr/bin/env python3
"""Parse cached DataCenterMap facility overview markdown into structured records.

Extracts only what is publicly present on the Overview tab. Never invents data;
uses null / "Unknown" for missing fields. Records source_url + scraped_at.
"""
import os
import re
import json
import glob
import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")
FAC_DIR = os.path.join(ROOT, ".firecrawl", "facilities")

COUNTRY_DISPLAY = {"brazil": "Brazil", "mexico": "Mexico", "colombia": "Colombia"}

# Service labels shown on DCM overview when the facility offers them.
SERVICE_LABELS = [
    "Suites",
    "Cages",
    "Footprints",
    "Private Cabinets",
    "Partial Cabinets",
    "Individual Servers",
    "Remote Hands",
    "Bare Metal Servers",
    "Public Cloud Servers",
]
# Map DCM label -> required boolean field
SERVICE_FIELD_MAP = {
    "Cages": "colo_cages",
    "Private Cabinets": "private_cabinets",
    "Partial Cabinets": "partial_cabinets",
    "Bare Metal Servers": "bare_metal",
    "Remote Hands": "remote_hands",
    "Public Cloud Servers": "public_cloud",
}
# labels that indicate leaseable colocation footprint
COLO_LABELS = {"Suites", "Cages", "Footprints", "Private Cabinets", "Partial Cabinets"}

CERT_TOKEN_RE = re.compile(
    r"(Tier\s?(?:[0-9]+|IV|III|II|I|V)"
    r"|ISO\s?\d{4,5}(?::\d{4})?"
    r"|SOC\s?[0-9]"
    r"|PCI[\s-]?DSS"
    r"|PCI"
    r"|HIPAA"
    r"|LEED"
    r"|TIA[\s-]?942"
    r"|NABERS"
    r"|SSAE\s?\d+"
    r"|Uptime Institute)",
    re.IGNORECASE,
)

MW_RE = re.compile(r"(\d+(?:[.,]\d+)?)\s*(?:MW|megawatt|mega-watt)s?\b", re.IGNORECASE)

AI_PATTERNS = [
    (r"\bartificial intelligence\b", "artificial intelligence"),
    (r"\bA\.?I\.?\b(?:[\s-]?(?:ready|inference|training|workload|factory|cloud))?", "AI"),
    (r"\bGPU[s]?\b", "GPU"),
    (r"\bHPC\b", "HPC"),
    (r"high[\s-]performance computing", "high-performance computing"),
    (r"\bmachine learning\b", "machine learning"),
    (r"accelerated computing", "accelerated computing"),
    (r"\bNVIDIA\b", "NVIDIA"),
    (r"supercomput", "supercomputing"),
    (r"liquid[\s-]cool", "liquid cooling"),
]

COUNTRY_LINE_RE = re.compile(r"^(?:([A-Za-zÀ-ÿ .]{1,25}),\s*)?(Brazil|Mexico|Colombia)\s*$")
POSTAL_CITY_RE = re.compile(r"^\s*(\d{4,6}(?:-\d{2,3})?)?\s*(.*\S)?\s*$")


def norm_cert(tok: str) -> str:
    t = re.sub(r"\s+", " ", tok.strip())
    # normalise ISO27001 -> ISO 27001, Tier3 -> Tier 3
    m = re.match(r"(ISO)\s?(\d.*)", t, re.I)
    if m:
        return f"ISO {m.group(2)}"
    m = re.match(r"(Tier)\s?([0-9]+|IV|III|II|I|V)", t, re.I)
    if m:
        return f"Tier {m.group(2).upper() if not m.group(2).isdigit() else m.group(2)}"
    m = re.match(r"(SOC)\s?(\d)", t, re.I)
    if m:
        return f"SOC {m.group(2)}"
    if re.match(r"PCI[\s-]?DSS", t, re.I):
        return "PCI-DSS"
    if t.upper() == "PCI":
        return "PCI-DSS"
    return t


def parse_file(path: str):
    with open(path, encoding="utf-8", errors="replace") as f:
        raw = f.read()
    lines = raw.split("\n")

    slug = os.path.basename(path)[:-3]  # strip .md
    parts = slug.split("__")
    country_slug = parts[0]
    market_slug = parts[1] if len(parts) > 1 else ""
    country = COUNTRY_DISPLAY.get(country_slug, country_slug.title())
    market = market_slug.replace("-", " ").title()

    facility_url = "https://www.datacentermap.com/" + slug.replace("__", "/") + "/"
    scraped_at = (
        datetime.datetime.fromtimestamp(os.path.getmtime(path), datetime.timezone.utc)
        .replace(microsecond=0)
        .strftime("%Y-%m-%dT%H:%M:%SZ")
    )

    rec = {
        "facility_name": None,
        "site_code": None,
        "operator_name": None,
        "operator_slug": None,
        "operator_parent_hint": None,
        "operator_hq": None,
        "operator_total_dc": None,
        "country": country,
        "metro": market,
        "city": None,
        "state": None,
        "address": None,
        "postal_code": None,
        "it_capacity_mw": None,
        "colo_cages": False,
        "private_cabinets": False,
        "partial_cabinets": False,
        "bare_metal": False,
        "remote_hands": False,
        "public_cloud": False,
        "raw_services": [],
        "certifications": [],
        "nearest_facilities": [],
        "operator_website": None,
        "facility_url": facility_url,
        "ai_mentions": [],
        "wholesale_mention": False,
        "colo_mention": False,
        "gov_captive_mention": False,
        "description_present": False,
        "scraped_at": scraped_at,
    }

    # --- facility name: first level-1 heading ---
    name_idx = None
    for i, ln in enumerate(lines):
        if ln.startswith("# ") and not ln.startswith("## "):
            rec["facility_name"] = ln[2:].strip()
            name_idx = i
            break
    if name_idx is None:
        return rec  # sparse / non-facility page

    # --- operator name + slug: first /c/<slug>/ link after the heading ---
    op_link_idx = None
    for i in range(name_idx + 1, len(lines)):
        m = re.search(r"\[([^\]]+)\]\(https://www\.datacentermap\.com/c/([^)/]+)/\)", lines[i])
        if m:
            rec["operator_name"] = m.group(1).strip()
            rec["operator_slug"] = m.group(2).strip()
            op_link_idx = i
            break

    # --- Visit Website link ---
    visit_idx = None
    for i, ln in enumerate(lines):
        m = re.search(r"\[Visit Website\]\((https://www\.datacentermap\.com/visit/[^)]+)\)", ln)
        if m:
            rec["operator_website"] = m.group(1)
            visit_idx = i
            break

    # --- address block: content lines between operator link and Visit Website ---
    if op_link_idx is not None:
        end = visit_idx if visit_idx is not None else min(op_link_idx + 8, len(lines))
        block = []
        for ln in lines[op_link_idx + 1:end]:
            s = ln.strip()
            if not s or s.startswith("![") or s.startswith("["):
                continue
            block.append(s)
        # locate country/state line
        country_i = None
        for j, s in enumerate(block):
            cm = COUNTRY_LINE_RE.match(s)
            if cm:
                if cm.group(1):
                    rec["state"] = cm.group(1).strip()
                country_i = j
                break
        if block:
            rec["address"] = block[0]
        if country_i is not None and country_i >= 1:
            pc_line = block[country_i - 1]
            pm = POSTAL_CITY_RE.match(pc_line)
            if pm:
                rec["postal_code"] = pm.group(1)
                city = pm.group(2)
                if city:
                    rec["city"] = city.strip()
        elif len(block) >= 2:
            # no explicit country line matched; assume 2nd line is postal+city
            pm = POSTAL_CITY_RE.match(block[1])
            if pm:
                rec["postal_code"] = pm.group(1)
                if pm.group(2):
                    rec["city"] = pm.group(2).strip()

    # --- services: contiguous labels right after the 'Request Quote' tab ---
    rq_idx = None
    for i, ln in enumerate(lines):
        if re.search(r"\[Request Quote\]\(https://www\.datacentermap\.com/[^)]+/quote/\)", ln):
            rq_idx = i
            break
    if rq_idx is not None:
        for ln in lines[rq_idx + 1:]:
            s = ln.strip()
            if not s:
                continue
            if s in SERVICE_LABELS:
                rec["raw_services"].append(s)
                continue
            break  # first non-service line = description
    for s in rec["raw_services"]:
        if s in SERVICE_FIELD_MAP:
            rec[SERVICE_FIELD_MAP[s]] = True

    # --- Pricing & Services marker delimits the overview body ---
    ps_idx = None
    for i, ln in enumerate(lines):
        if ln.strip() == "Pricing & Services":
            ps_idx = i
            break
    body_end = ps_idx if ps_idx is not None else len(lines)

    # --- description / prose region (after services, before Pricing & Services) ---
    prose_start = rq_idx + 1 if rq_idx is not None else name_idx + 1
    prose_lines = []
    for ln in lines[prose_start:body_end]:
        s = ln.strip()
        if not s or s.startswith("![") or s in SERVICE_LABELS:
            continue
        prose_lines.append(s)
    prose = "\n".join(prose_lines)
    rec["description_present"] = len(prose) > 120

    # --- certifications: the content line just before 'Pricing & Services' ---
    if ps_idx is not None:
        j = ps_idx - 1
        while j > name_idx:
            s = lines[j].strip()
            if not s or s.startswith("!["):
                j -= 1
                continue
            if CERT_TOKEN_RE.search(s) and len(s) < 80:
                toks = [norm_cert(t) for t in CERT_TOKEN_RE.findall(s)]
                seen = set()
                for t in toks:
                    if t.lower() not in seen:
                        seen.add(t.lower())
                        rec["certifications"].append(t)
            break

    # --- IT capacity MW from name + prose ---
    hay = (rec["facility_name"] or "") + "\n" + prose
    mws = [float(m.group(1).replace(",", ".")) for m in MW_RE.finditer(hay)]
    if mws:
        rec["it_capacity_mw"] = max(mws)

    # --- keyword signals from prose ---
    low = prose.lower()
    for pat, label in AI_PATTERNS:
        if re.search(pat, prose, re.IGNORECASE):
            if label not in rec["ai_mentions"]:
                rec["ai_mentions"].append(label)
    if re.search(r"wholesale|build[\s-]to[\s-]suit|hyperscale", low):
        rec["wholesale_mention"] = True
    if re.search(r"colocation|\bcolo\b|carrier[\s-]neutral", low):
        rec["colo_mention"] = True
    if re.search(
        r"government[\s-]owned|owned by the government|\bmilitar|armed forces|"
        r"ministry of|federal police|government data cent|captive (?:facility|data cent)|"
        r"exclusively for (?:the )?government|national security agency",
        low,
    ):
        rec["gov_captive_mention"] = True

    # --- nearest facilities table ---
    near = []
    in_table = False
    for i in range(len(lines)):
        if lines[i].strip().startswith("Nearest Data Centers"):
            in_table = True
            continue
        if in_table:
            row = lines[i].strip()
            if not row.startswith("|"):
                if near:
                    break
                continue
            cells = [c.strip() for c in row.strip("|").split("|")]
            if len(cells) < 2 or cells[0] in ("Distance", "---"):
                continue
            dist = cells[0]
            nm = re.match(r"\[([^\]]+)\]", cells[1])
            if nm:
                near.append(f"{nm.group(1)} ({dist})")
            if len(near) >= 5:
                break
    rec["nearest_facilities"] = near

    # --- operator roll-up block (## Operator ...) ---
    op_block = raw
    sc = re.search(r"Site Code:\s*([^\n]+)", raw)
    if sc:
        rec["site_code"] = sc.group(1).strip()
    hq = re.search(r"Headquartered in\s+([^\n]+)", raw)
    if hq:
        rec["operator_hq"] = hq.group(1).strip().rstrip(".")
    tot = re.search(r"Data Centers\\?\s*\\?\s*(\d+)\]\(https://www\.datacentermap\.com/c/", raw)
    if tot:
        rec["operator_total_dc"] = int(tot.group(1))

    return rec


def main():
    files = sorted(glob.glob(os.path.join(FAC_DIR, "*.md")))
    records = []
    empty = []
    for p in files:
        rec = parse_file(p)
        if not rec.get("facility_name"):
            empty.append(os.path.basename(p))
            continue
        records.append(rec)
    with open(os.path.join(DATA, "facilities_raw.json"), "w") as f:
        json.dump(records, f, indent=2, ensure_ascii=False)
    print(f"Parsed {len(records)} facilities from {len(files)} files; empty/failed: {len(empty)}")
    if empty:
        print("Empty:", empty[:20])


if __name__ == "__main__":
    main()
