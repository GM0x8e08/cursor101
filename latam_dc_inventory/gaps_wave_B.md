> ## ⚠️ STATUS: PARTIAL / PENDING RE-CRAWL
>
> Wave B is **incomplete**. **81 of 134** discovered facilities were
> captured before the **Firecrawl keyless free-tier quota was exhausted** (~500+ scrapes
> across Wave A + Wave B in one session; every request now returns the keyless rate-limit
> error). The crawl is alphabetical by URL, so Argentina completed, Chile is partial
> (throttled mid-Santiago), and Peru was not reached.
>
> **53 facilities still to capture** (concentrated in priority metros Santiago & Lima):
>
> | Country | Market | Missing |
> | --- | --- | --- |
> | Chile | santiago | 34 |
> | Peru | lima | 14 |
> | Chile | valparaiso | 3 |
> | Chile | temuco | 1 |
> | Peru | tacna | 1 |
>
> **To complete:** add a `FIRECRAWL_API_KEY` (Cursor Dashboard > Cloud Agents > Secrets)
> *or* wait for the keyless quota to reset, then re-run. Cached pages are skipped, so only
> the missing facilities are fetched:
>
> ```bash
> WAVE=B python3 crawl_facilities.py   # fetches only the missing (captured pages skip)
> WAVE=B python3 parse_facilities.py
> WAVE=B python3 enrich.py             # full datacenters.com + Santiago Cloudscene
> WAVE=B python3 build_tables.py
> WAVE=B python3 gen_gaps.py
> ```
>
> **Enrichment note:** overlapping multinational operators (Cirion, Equinix, Ascenty, ODATA,
> KIO/IFXNetworks, Claro, IPXON, Actis, Kyndryl, Sencinet) reuse their Wave A datacenters.com
> profiles. Santiago Cloudscene connectivity and Chile/Peru-only operator profiles are
> deferred to the re-crawl. Full missing-URL list: `data/wave_B_missing_urls.json`.

# Wave B Data-Center Inventory — Gaps & Data-Quality Notes

_Wave B = Chile, Argentina, Peru. Primary source: datacentermap.com (all public facility Overview tabs). Enrichment: datacenters.com (operator profiles) and cloudscene.com (metro connectivity for Santiago only). Specs tabs on datacentermap require login and were not scraped._

## Coverage summary

- **Facilities captured:** 81 across 16 markets (Chile 32, Argentina 49, Peru 0).
- **Operators (roll-up):** 48.
- **Relevance distribution:** 5=28, 4=2, 3=32, 2=11, 1=8.
- **Leaseable signal:** Yes=62, Unclear=19.
- **Confidence:** High=59, Med=22.

## Priority-metro facility counts

- Santiago: 26
- Buenos Aires: 32
- Lima: 0

## Missing / thin fields (what could not be captured publicly)

- **IT capacity (MW):** disclosed for only **3/81** facilities (4%). MW is almost always on the login-gated Specs tab; where present it was parsed from the public Overview prose as the facility's critical/IT power. Portfolio-wide and 'scalable up to' figures were deliberately **excluded** to avoid attributing operator-level capacity to single buildings.
- **Certifications:** present for **10/81** facilities. Many pages list no certifications publicly; absence here does not mean the site is uncertified (often on Specs/behind login).
- **Services:** **19/81** facilities list no service icons at all on the public Overview (typically pre-launch, campus-umbrella, or captive listings). Their service booleans are all False and leaseability is 'Unclear' unless prose indicated otherwise.
- **City/address granularity:** 0 facilities lack a parsed city (address block absent or non-standard on the source page).
- **AI / GPU mentions:** flagged on **1/81** facilities from Overview prose plus operator datacenters.com profiles. This reflects *marketing language only* — no GPU SKUs, utilization, or contracted AI capacity were inferred (per anti-goals).
- **operator_website:** datacentermap masks outbound links behind a `/visit/` redirect that is itself bot-protected, so the field stores that redirect rather than the resolved domain. Resolve manually if a canonical URL is needed.
- **datacenters_com_url (facilities):** set to the operator's datacenters.com *provider profile* (operator-level match), not necessarily the individual building's datacenters.com page.

## Operators needing manual research (relevance ≥4 or ≥3 facilities)

| Operator | Wave A facilities | Max relevance | What to verify manually |
| --- | --- | --- | --- |
| Cirion | 6 | 5 | no public MW; parent unconfirmed |
| EdgeConneX | 5 | 5 | no public MW; parent unconfirmed; no AI/GPU signal found |
| Claro | 4 | 5 | no public MW; parent unconfirmed |
| Equinix | 4 | 5 | parent unconfirmed |
| GTD Chile | 4 | 5 | no public MW; parent unconfirmed; no AI/GPU signal found |
| Telecom Argentina | 4 | 5 | no public MW; parent unconfirmed; no AI/GPU signal found |
| Advantun | 3 | 5 | no public MW; parent unconfirmed; no AI/GPU signal found |
| NextStream | 3 | 5 | no public MW; parent unconfirmed |
| IPXON Networks | 2 | 5 | no public MW; parent unconfirmed |
| ODATA, an Aligned Data Centers Company | 2 | 5 | no public MW |
| Ascenty Data Centers | 1 | 4 | no public MW; parent unconfirmed |

## Enrichment gaps

- **datacenters.com:** no provider profile matched for 0 enriched operators: . These need a manual datacenters.com / vendor-site lookup for AI/wholesale claims.
- **Cloudscene connectivity (metro-level, qualitative):** .
- Cloudscene was intentionally limited to Santiago per scope; other priority metros (Buenos Aires, Lima) have no carrier/IX density rating yet.

## Known caveats / suggested manual follow-ups

- **MW is the biggest gap.** For a capacity-based partnership map, pull MW/racks/PUE from operator sites, investor decks, or datacentermap Specs (login) for the top operators: Cirion, EdgeConneX, Claro, Equinix, GTD Chile, Telecom Argentina, Advantun, NextStream, IPXON Networks, ODATA, an Aligned Data Centers Company.
- **Telco-owned colos** score high when they publicly offer colocation, but AI/neocloud partnership openness is uncertain — confirm commercial wholesale/AI appetite directly. Candidates flagged Low openness with a colo footprint: (none flagged).
- **Parent companies** were only auto-derived where stated on-page. Confirm ownership for the top operators via corporate filings / press.
- **Pre-launch facilities** (2025–2026 builds) show no services yet and are scored conservatively; revisit as they open.
