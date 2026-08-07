#!/usr/bin/env python3
"""Generate gaps.md: missing-field coverage and manual-research to-dos."""
import os
import csv
import json
from collections import Counter, defaultdict

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")

PRIORITY = {"São Paulo", "Rio de Janeiro", "Querétaro", "Mexico City", "Bogotá", "Medellín"}


def main():
    frows = list(csv.DictReader(open(os.path.join(ROOT, "facilities_wave_A.csv"), encoding="utf-8")))
    orows = list(csv.DictReader(open(os.path.join(ROOT, "operators_wave_A.csv"), encoding="utf-8")))
    raw = json.load(open(os.path.join(DATA, "facilities_raw.json"), encoding="utf-8"))
    enr = json.load(open(os.path.join(DATA, "enrichment.json"), encoding="utf-8"))

    n = len(frows)
    by_country = Counter(r["country"] for r in frows)
    by_metro = Counter(r["metro"] for r in frows)
    mw_n = sum(1 for r in frows if r["it_capacity_mw"])
    cert_n = sum(1 for r in frows if r["certifications"])
    ai_n = sum(1 for r in frows if "AIMention" in r["tags"])
    no_services = sum(1 for r in raw if not r.get("raw_services"))
    no_city = sum(1 for r in frows if not r["city"])
    lease = Counter(r["leaseable_signal"] for r in frows)
    conf = Counter(r["confidence"] for r in frows)
    scores = Counter(r["relevance_score"] for r in frows)

    # operators qualifying (rel>=4 or count>=3) missing key fields
    manual = []
    for o in orows:
        rel = int(o["max_relevance"]); fc = int(o["facility_count_wave_A"])
        if rel >= 4 or fc >= 3:
            miss = []
            if o["total_mw_known"] in ("0", "0.0", "") or o["mw_coverage_pct"] in ("0%",):
                miss.append("no public MW")
            if o["parent_company"] in ("Unknown", ""):
                miss.append("parent unconfirmed")
            if not o["ai_or_gpu_mentions"]:
                miss.append("no AI/GPU signal found")
            if miss:
                manual.append((o["operator_name"], fc, rel, "; ".join(miss)))

    dcom_ops = [op for op, v in enr["operators"].items() if not v.get("datacenters_com_url")]

    lines = []
    A = lines.append
    A("# Wave A Data-Center Inventory — Gaps & Data-Quality Notes\n")
    A("_Wave A = Brazil, Mexico, Colombia. Primary source: datacentermap.com "
      "(all public facility Overview tabs). Enrichment: datacenters.com (operator "
      "profiles) and cloudscene.com (metro connectivity for São Paulo, Querétaro, "
      "Bogotá only). Specs tabs on datacentermap require login and were not scraped._\n")

    A("## Coverage summary\n")
    A(f"- **Facilities captured:** {n} across {len(by_metro)} markets "
      f"(Brazil {by_country['Brazil']}, Mexico {by_country['Mexico']}, Colombia {by_country['Colombia']}).")
    A(f"- **Operators (roll-up):** {len(orows)}.")
    A(f"- **Relevance distribution:** " + ", ".join(f"{k}={scores.get(k,0)}" for k in ['5','4','3','2','1']) + ".")
    A(f"- **Leaseable signal:** " + ", ".join(f"{k}={v}" for k, v in lease.items()) + ".")
    A(f"- **Confidence:** " + ", ".join(f"{k}={v}" for k, v in conf.items()) + ".\n")

    A("## Priority-metro facility counts\n")
    for m in ["São Paulo", "Rio de Janeiro", "Querétaro", "Mexico City", "Bogotá", "Medellín"]:
        A(f"- {m}: {by_metro.get(m, 0)}")
    A("")

    A("## Missing / thin fields (what could not be captured publicly)\n")
    A(f"- **IT capacity (MW):** disclosed for only **{mw_n}/{n}** facilities ({round(100*mw_n/n)}%). "
      "MW is almost always on the login-gated Specs tab; where present it was parsed from the public "
      "Overview prose as the facility's critical/IT power. Portfolio-wide and 'scalable up to' figures "
      "were deliberately **excluded** to avoid attributing operator-level capacity to single buildings.")
    A(f"- **Certifications:** present for **{cert_n}/{n}** facilities. Many pages list no certifications "
      "publicly; absence here does not mean the site is uncertified (often on Specs/behind login).")
    A(f"- **Services:** **{no_services}/{n}** facilities list no service icons at all on the public "
      "Overview (typically pre-launch, campus-umbrella, or captive listings). Their service booleans are "
      "all False and leaseability is 'Unclear' unless prose indicated otherwise.")
    A(f"- **City/address granularity:** {no_city} facilities lack a parsed city (address block absent or "
      "non-standard on the source page).")
    A(f"- **AI / GPU mentions:** flagged on **{ai_n}/{n}** facilities from Overview prose plus operator "
      "datacenters.com profiles. This reflects *marketing language only* — no GPU SKUs, utilization, or "
      "contracted AI capacity were inferred (per anti-goals).")
    A("- **operator_website:** datacentermap masks outbound links behind a `/visit/` redirect that is "
      "itself bot-protected, so the field stores that redirect rather than the resolved domain. Resolve "
      "manually if a canonical URL is needed.")
    A("- **datacenters_com_url (facilities):** set to the operator's datacenters.com *provider profile* "
      "(operator-level match), not necessarily the individual building's datacenters.com page.\n")

    A("## Operators needing manual research (relevance ≥4 or ≥3 facilities)\n")
    A("| Operator | Wave A facilities | Max relevance | What to verify manually |")
    A("| --- | --- | --- | --- |")
    for name, fc, rel, miss in sorted(manual, key=lambda x: (-x[2], -x[1])):
        A(f"| {name} | {fc} | {rel} | {miss} |")
    A("")

    A("## Enrichment gaps\n")
    A(f"- **datacenters.com:** no provider profile matched for {len(dcom_ops)} enriched operators: "
      + ", ".join(sorted(dcom_ops)) + ". These need a manual datacenters.com / vendor-site lookup for "
      "AI/wholesale claims.")
    A("- **Cloudscene connectivity (metro-level, qualitative):** "
      + "; ".join(f"{k}={v.get('connectivity','?')} ({v.get('connectivity_detail','')})"
                  for k, v in enr["metros"].items()) + ".")
    A("- Cloudscene was intentionally limited to São Paulo, Querétaro, and Bogotá per scope; other "
      "priority metros (Rio de Janeiro, Mexico City, Medellín) have no carrier/IX density rating yet.\n")

    A("## Known caveats / suggested manual follow-ups\n")
    A("- **MW is the biggest gap.** For a capacity-based partnership map, pull MW/racks/PUE from operator "
      "sites, investor decks, or datacentermap Specs (login) for the top operators (Scala, Ascenty/Digital "
      "Realty, ODATA/Aligned, Equinix, CloudHQ, KIO, Cirion, Elea, TAKODA, Tecto).")
    A("- **Telco-owned colos** (Vivo/Telefónica, Claro, Tigo, TELMEX Triara, InterNexa) score high because "
      "they publicly offer colocation, but partnership openness for AI/neocloud is uncertain — confirm "
      "commercial wholesale/AI appetite directly.")
    A("- **Parent companies** were only auto-derived where stated on-page (e.g. ODATA→Aligned). Confirm "
      "ownership for Ascenty (Digital Realty), Scala (DigitalBridge), Cirion (Stonepeak/ex-Lumen), etc.")
    A("- **Pre-launch facilities** (e.g. Equinix SP7, several 2025–2026 builds) show no services yet and "
      "are scored conservatively; revisit as they open.")

    with open(os.path.join(ROOT, "gaps.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines) + "\n")
    print(f"Wrote gaps.md ({len(manual)} operators flagged for manual research)")


if __name__ == "__main__":
    main()
