# Wave B Data-Center Inventory — Gaps & Data-Quality Notes

_Wave B = Chile, Argentina, Peru. Primary source: datacentermap.com (all public facility Overview tabs). Enrichment: datacenters.com (operator profiles) and cloudscene.com (metro connectivity for Santiago only). Specs tabs on datacentermap require login and were not scraped._

## Coverage summary

- **Facilities captured:** 134 across 20 markets (Chile 70, Argentina 49, Peru 15).
- **Operators (roll-up):** 66.
- **Relevance distribution:** 5=67, 4=3, 3=42, 2=14, 1=8.
- **Leaseable signal:** Yes=112, Unclear=22.
- **Confidence:** High=108, Med=26.

## Priority-metro facility counts

- Santiago: 60
- Buenos Aires: 32
- Lima: 14

## Missing / thin fields (what could not be captured publicly)

- **IT capacity (MW):** disclosed for only **6/134** facilities (4%). MW is almost always on the login-gated Specs tab; where present it was parsed from the public Overview prose as the facility's critical/IT power. Portfolio-wide and 'scalable up to' figures were deliberately **excluded** to avoid attributing operator-level capacity to single buildings.
- **Certifications:** present for **22/134** facilities. Many pages list no certifications publicly; absence here does not mean the site is uncertified (often on Specs/behind login).
- **Services:** **22/134** facilities list no service icons at all on the public Overview (typically pre-launch, campus-umbrella, or captive listings). Their service booleans are all False and leaseability is 'Unclear' unless prose indicated otherwise.
- **City/address granularity:** 0 facilities lack a parsed city (address block absent or non-standard on the source page).
- **AI / GPU mentions:** flagged on **1/134** facilities from Overview prose plus operator datacenters.com profiles. This reflects *marketing language only* — no GPU SKUs, utilization, or contracted AI capacity were inferred (per anti-goals).
- **operator_website:** datacentermap masks outbound links behind a `/visit/` redirect that is itself bot-protected, so the field stores that redirect rather than the resolved domain. Resolve manually if a canonical URL is needed.
- **datacenters_com_url (facilities):** set to the operator's datacenters.com *provider profile* (operator-level match), not necessarily the individual building's datacenters.com page.

## Operators needing manual research (relevance ≥4 or ≥3 facilities)

| Operator | Wave A facilities | Max relevance | What to verify manually |
| --- | --- | --- | --- |
| GTD Chile | 10 | 5 | parent unconfirmed |
| Cirion | 8 | 5 | no public MW; parent unconfirmed |
| NextStream | 7 | 5 | no public MW; parent unconfirmed |
| Equinix | 6 | 5 | parent unconfirmed |
| Scala Data Centers | 6 | 5 | no public MW |
| Claro | 5 | 5 | no public MW; parent unconfirmed |
| EdgeConneX | 5 | 5 | no public MW; parent unconfirmed |
| IFXNetworks | 4 | 5 | no public MW; parent unconfirmed |
| IPXON Networks | 4 | 5 | no public MW; parent unconfirmed |
| Telecom Argentina | 4 | 5 | no public MW; parent unconfirmed |
| Advantun | 3 | 5 | no public MW; parent unconfirmed |
| Ascenty Data Centers | 3 | 5 | no public MW; parent unconfirmed |
| Sonda S.A. | 3 | 5 | no public MW; parent unconfirmed |
| WIN Empresas | 3 | 5 | no public MW; parent unconfirmed |
| Anacondaweb S.A. | 2 | 5 | no public MW; parent unconfirmed |
| InterNexa | 2 | 5 | no public MW |
| Latincloud | 2 | 5 | no public MW; parent unconfirmed; no AI/GPU signal found |
| ODATA, an Aligned Data Centers Company | 2 | 5 | no public MW |
| Ufinet | 2 | 5 | no public MW; parent unconfirmed |

## Enrichment gaps

- **datacenters.com:** no provider profile matched for 1 enriched operators: latincloud. These need a manual datacenters.com / vendor-site lookup for AI/wholesale claims.
- **Cloudscene connectivity (metro-level, qualitative):** santiago=Med (57 network/service providers, 59 data centers listed (Cloudscene) [fallback: country /all; city page https://cloudscene.com/market/data-centers-in-chile/santiago was empty]).
- Cloudscene was intentionally limited to Santiago per scope; other priority metros (Buenos Aires, Lima) have no carrier/IX density rating yet.

## Known caveats / suggested manual follow-ups

- **MW is the biggest gap.** For a capacity-based partnership map, pull MW/racks/PUE from operator sites, investor decks, or datacentermap Specs (login) for the top operators: GTD Chile, Cirion, NextStream, Equinix, Scala Data Centers, Claro, EdgeConneX, IFXNetworks, IPXON Networks, Telecom Argentina.
- **Telco-owned colos** score high when they publicly offer colocation, but AI/neocloud partnership openness is uncertain — confirm commercial wholesale/AI appetite directly. Candidates flagged Low openness with a colo footprint: (none flagged).
- **Parent companies** were only auto-derived where stated on-page. Confirm ownership for the top operators via corporate filings / press.
- **Pre-launch facilities** (2025–2026 builds) show no services yet and are scored conservatively; revisit as they open.
