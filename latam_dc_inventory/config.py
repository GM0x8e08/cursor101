#!/usr/bin/env python3
"""Wave configuration so the crawl/parse/build pipeline works for any wave.

Select the wave with the WAVE env var (default "A"). Wave A paths are kept
identical to the originally-shipped run for reproducibility.
"""
import os

WAVES = {
    "A": {
        "countries": ["brazil", "mexico", "colombia"],
        "priority_slugs": {
            "sao-paulo", "rio-de-janeiro", "queretaro", "mexico-city", "bogota", "medellin",
        },
        "priority_display": [
            "São Paulo", "Rio de Janeiro", "Querétaro", "Mexico City", "Bogotá", "Medellín",
        ],
        "cloudscene": {
            "sao-paulo": ("Sao Paulo Brazil", "https://cloudscene.com/market/data-centers-in-brazil/sao-paulo"),
            "queretaro": ("Queretaro Mexico", "https://cloudscene.com/market/data-centers-in-mexico/queretaro"),
            "bogota": ("Bogota Colombia", "https://cloudscene.com/market/data-centers-in-colombia/bogota"),
        },
        "fac_dir": ".firecrawl/facilities",
        "market_urls": "data/market_urls.txt",
        "facility_urls": "data/facility_urls.json",
        "raw": "data/facilities_raw.json",
        "enrichment": "data/enrichment.json",
        "facilities_csv": "facilities_wave_A.csv",
        "operators_csv": "operators_wave_A.csv",
        "gaps": "gaps.md",
        "enrich_dir": ".firecrawl/enrich",
    },
    "B": {
        "countries": ["chile", "argentina", "peru"],
        # Santiago is the explicit Wave B priority; Buenos Aires and Lima are the
        # other primary commercial hubs, treated as priority metros by analogy.
        "priority_slugs": {"santiago", "buenos-aires", "lima"},
        "priority_display": ["Santiago", "Buenos Aires", "Lima"],
        "cloudscene": {
            "santiago": ("Santiago Chile", "https://cloudscene.com/market/data-centers-in-chile/santiago"),
        },
        "fac_dir": ".firecrawl/facilities_b",
        "market_urls": "data/market_urls_wave_B.txt",
        "facility_urls": "data/facility_urls_wave_B.json",
        "raw": "data/facilities_raw_wave_B.json",
        "enrichment": "data/enrichment_wave_B.json",
        "facilities_csv": "facilities_wave_B.csv",
        "operators_csv": "operators_wave_B.csv",
        "gaps": "gaps_wave_B.md",
        "enrich_dir": ".firecrawl/enrich_b",
    },
}

WAVE = os.environ.get("WAVE", "A")
CFG = WAVES[WAVE]
FCOUNT_COL = "facility_count_wave_" + WAVE
