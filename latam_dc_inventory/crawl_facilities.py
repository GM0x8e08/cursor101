#!/usr/bin/env python3
"""Scrape every discovered Wave A facility overview page (cached + resilient)."""
import os
import json
from scraper import scrape, slug_for
from config import CFG

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")
FAC_DIR = os.path.join(ROOT, CFG["fac_dir"])


def main():
    with open(os.path.join(ROOT, CFG["facility_urls"])) as f:
        facs = json.load(f)
    urls = sorted(facs.keys())
    ok, failed = 0, []
    for i, url in enumerate(urls, 1):
        out = os.path.join(FAC_DIR, slug_for(url) + ".md")
        status = "cached" if os.path.exists(out) else "fetch"
        print(f"[facility {i}/{len(urls)}] ({status}) {url}", flush=True)
        if scrape(url, out):
            ok += 1
        else:
            failed.append(url)
    print(f"\nFacilities scraped OK: {ok}/{len(urls)}; failed: {len(failed)}")
    with open(os.path.join(DATA, "facility_scrape_failed_" + CFG["facilities_csv"].replace(".csv", "") + ".json"), "w") as f:
        json.dump(failed, f, indent=2)


if __name__ == "__main__":
    main()
