#!/usr/bin/env python3
"""Scrape all Wave A market pages, then extract every facility URL."""
import os
import re
import json
from scraper import scrape, slug_for

ROOT = os.path.dirname(os.path.abspath(__file__))
DATA = os.path.join(ROOT, "data")
MKT_DIR = os.path.join(ROOT, ".firecrawl", "markets")

COUNTRIES = {"brazil", "mexico", "colombia"}

# 3-segment facility path: /country/market/facility/  (facility slug is last)
FAC_RE = re.compile(
    r"https://www\.datacentermap\.com/(brazil|mexico|colombia)/([a-z0-9-]+)/([a-z0-9-]+)/"
)
# subpages that are NOT facility overviews
NON_FACILITY_LAST = {"specs", "ecosystem", "location", "gallery", "quote"}


def main():
    with open(os.path.join(DATA, "market_urls.txt")) as f:
        market_urls = [l.strip() for l in f if l.strip()]

    facility_urls = {}  # url -> {country, market}
    ok, failed = 0, []
    for i, url in enumerate(market_urls, 1):
        slug = slug_for(url)
        out = os.path.join(MKT_DIR, slug + ".md")
        print(f"[market {i}/{len(market_urls)}] {url}", flush=True)
        if scrape(url, out):
            ok += 1
        else:
            failed.append(url)
            continue
        with open(out, encoding="utf-8", errors="replace") as fh:
            txt = fh.read()
        for m in FAC_RE.finditer(txt):
            country, market, last = m.group(1), m.group(2), m.group(3)
            if last in NON_FACILITY_LAST:
                continue
            furl = m.group(0)
            facility_urls.setdefault(furl, {"country": country, "market": market})

    print(f"\nMarkets scraped OK: {ok}/{len(market_urls)}; failed: {failed}")
    print(f"Unique facility URLs discovered: {len(facility_urls)}")

    with open(os.path.join(DATA, "facility_urls.json"), "w") as f:
        json.dump(facility_urls, f, indent=2, sort_keys=True)
    with open(os.path.join(DATA, "market_scrape_failed.json"), "w") as f:
        json.dump(failed, f, indent=2)


if __name__ == "__main__":
    main()
