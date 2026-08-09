# LatAm Data-Center Inventory — Waves A & B

A facility-level inventory of LatAm data centers built for a regional
AI-inference / neo-cloud partnership map. The atomic unit is a **facility**
(one building/site); operators are rolled up separately.

- **Wave A — complete:** Brazil, Mexico, Colombia (343 facilities).
- **Wave B — complete:** Chile, Argentina, Peru (134 facilities).

## Deliverables

| File | What it is |
| --- | --- |
| `facilities_wave_A.csv` | 343 facilities, one row per building/site, fully scored & tagged |
| `operators_wave_A.csv` | 130 operators rolled up from the facilities |
| `gaps.md` | Wave A missing-field coverage, manual-research to-dos, caveats |
| `facilities_wave_B.csv` | 134 Wave B facilities (Chile 70, Argentina 49, Peru 15), scored & tagged |
| `operators_wave_B.csv` | 66 Wave B operators rolled up |
| `gaps_wave_B.md` | Wave B missing-field coverage, manual-research to-dos, caveats |

## Running a wave

The pipeline is parameterized by the `WAVE` env var (`A` default, or `B`) via
`config.py`. Wave A paths/outputs are unchanged. To (re)build a wave:

```bash
WAVE=B python3 crawl_markets.py       # country → market → facility URLs
WAVE=B python3 crawl_facilities.py    # scrape each facility (cached; skips already-fetched)
WAVE=B python3 parse_facilities.py    # markdown → structured JSON
WAVE=B python3 enrich.py              # datacenters.com profiles + Cloudscene metro density
WAVE=B python3 build_tables.py        # dedup, score, tag → facilities/operators CSV
WAVE=B python3 gen_gaps.py            # gaps_wave_B.md
```

Every facility row carries `source_url` + `scraped_at`. No fields were invented;
missing values are left blank / `Unclear` / `Unknown`.

## Sources (priority order)

1. **Primary — [datacentermap.com](https://www.datacentermap.com/):** every public
   facility *Overview* tab across all markets in the wave (country → market →
   facility crawl). Specs tabs require login and were **not** scraped.
2. **Enrich — [datacenters.com](https://www.datacenters.com/):** operator profiles
   for operators with relevance ≥4 or ≥3 facilities (AI/wholesale claims, blurbs).
3. **Enrich — [cloudscene.com](https://www.cloudscene.com/):** carrier/IX density
   (qualitative High/Med/Low) at metro level — Wave A: São Paulo, Querétaro,
   Bogotá; Wave B: Santiago (Chile country `/all` used as fallback when the city
   page rendered empty).

The sites are behind a Vercel anti-bot challenge, so pages were fetched via the
Firecrawl CLI (JS-rendered, cached to `.firecrawl/`, not committed).

## Geo scope

- **Wave A:** Brazil (232), Mexico (69), Colombia (42) = 343 facilities, 56 markets.
  Priority metros: São Paulo, Rio de Janeiro, Querétaro, Mexico City, Bogotá, Medellín.
- **Wave B:** Chile (70), Argentina (49), Peru (15) = 134 facilities, 20 markets.
  Priority metros: Santiago (explicit), plus Buenos Aires and Lima (primary hubs).

## Relevance scoring (1–5)

- **5** — multi-site LatAm colo/wholesale operator in a priority metro, MW known or clearly commercial colo.
- **4** — major colo/IX-dense site (Equinix-class) or known AI/wholesale player.
- **3** — mid-size commercial colo in a priority metro (or multi-site commercial colo / AI signal elsewhere).
- **2** — small/standalone commercial colo, or unclear leaseability in a priority metro.
- **1** — captive telco/government, tiny host, umbrella-campus duplicate, or unclear + outside priority metros.

Score-1 rows are kept and marked `exclude_from_outreach = True`.

`leaseable_signal` = Yes when colo/cabinets/wholesale are present, No for captive
gov/telco with no colo footprint, Unclear otherwise. `tags` ∈ {Wholesale, Colo,
Edge, Hyperscale, TelcoCaptive, GovCaptive, AIMention, MultiSiteOperator}.

## Reproduce

```bash
npm install -g firecrawl-cli          # keyless free tier works (rate-limited)
python3 crawl_markets.py              # country → market pages → facility_urls.json
python3 crawl_facilities.py           # scrape all 343 facility Overview pages (cached)
python3 parse_facilities.py           # -> data/facilities_raw.json
python3 build_tables.py               # -> facilities_wave_A.csv, operators_wave_A.csv
python3 enrich.py                     # -> data/enrichment.json (datacenters.com + cloudscene)
python3 build_tables.py               # rebuild with enrichment merged in
python3 gen_gaps.py                   # -> gaps.md
```

Scripts: `scraper.py` (cached, rate-limit-aware Firecrawl wrapper) is shared by the
crawlers. Intermediate JSON provenance lives in `data/`.

## Key caveats

- **MW is the biggest gap** — disclosed for only ~7% of facilities (Specs are
  login-gated). Portfolio-wide and "scalable up to" figures were excluded so
  operator-level capacity is never attributed to a single building.
- `operator_website` stores datacentermap's bot-protected `/visit/` redirect, not
  the resolved domain.
- `datacenters_com_url` on facilities is the operator's provider profile
  (operator-level match).
- AI/GPU tags reflect **marketing language only** — no GPU SKUs, utilization, or
  contract terms were inferred.

See `gaps.md` for the full list and the per-operator manual-research queue.
