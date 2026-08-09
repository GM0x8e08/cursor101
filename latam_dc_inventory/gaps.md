# Wave A Data-Center Inventory — Gaps & Data-Quality Notes

_Wave A = Brazil, Mexico, Colombia. Primary source: datacentermap.com (all public facility Overview tabs). Enrichment: datacenters.com (operator profiles) and cloudscene.com (metro connectivity for São Paulo, Querétaro, Bogotá only). Specs tabs on datacentermap require login and were not scraped._

## Coverage summary

- **Facilities captured:** 343 across 56 markets (Brazil 232, Mexico 69, Colombia 42).
- **Operators (roll-up):** 130.
- **Relevance distribution:** 5=123, 4=61, 3=66, 2=69, 1=24.
- **Leaseable signal:** Yes=300, Unclear=42, No=1.
- **Confidence:** Med=53, High=290.

## Priority-metro facility counts

- São Paulo: 70
- Rio de Janeiro: 24
- Querétaro: 20
- Mexico City: 16
- Bogotá: 33
- Medellín: 4

## Missing / thin fields (what could not be captured publicly)

- **IT capacity (MW):** disclosed for only **25/343** facilities (7%). MW is almost always on the login-gated Specs tab; where present it was parsed from the public Overview prose as the facility's critical/IT power. Portfolio-wide and 'scalable up to' figures were deliberately **excluded** to avoid attributing operator-level capacity to single buildings.
- **Certifications:** present for **55/343** facilities. Many pages list no certifications publicly; absence here does not mean the site is uncertified (often on Specs/behind login).
- **Services:** **43/343** facilities list no service icons at all on the public Overview (typically pre-launch, campus-umbrella, or captive listings). Their service booleans are all False and leaseability is 'Unclear' unless prose indicated otherwise.
- **City/address granularity:** 0 facilities lack a parsed city (address block absent or non-standard on the source page).
- **AI / GPU mentions:** flagged on **31/343** facilities from Overview prose plus operator datacenters.com profiles. This reflects *marketing language only* — no GPU SKUs, utilization, or contracted AI capacity were inferred (per anti-goals).
- **operator_website:** datacentermap masks outbound links behind a `/visit/` redirect that is itself bot-protected, so the field stores that redirect rather than the resolved domain. Resolve manually if a canonical URL is needed.
- **datacenters_com_url (facilities):** set to the operator's datacenters.com *provider profile* (operator-level match), not necessarily the individual building's datacenters.com page.

## Operators needing manual research (relevance ≥4 or ≥3 facilities)

| Operator | Wave A facilities | Max relevance | What to verify manually |
| --- | --- | --- | --- |
| Ascenty Data Centers | 28 | 5 | no public MW; parent unconfirmed |
| Equinix | 17 | 5 | no public MW; parent unconfirmed |
| Elea Data Centers | 14 | 5 | no public MW; parent unconfirmed |
| KIO Networks | 14 | 5 | parent unconfirmed |
| CloudHQ | 13 | 5 | parent unconfirmed |
| Cirion | 8 | 5 | no public MW; parent unconfirmed |
| TAKODA | 7 | 5 | no public MW; parent unconfirmed |
| Tecto Data Centers | 7 | 5 | parent unconfirmed |
| IPXON Networks | 6 | 5 | no public MW; parent unconfirmed |
| HostDime Global Corp | 5 | 5 | no public MW; parent unconfirmed |
| MTP | 5 | 5 | no public MW; parent unconfirmed |
| Megatelecom | 5 | 5 | no public MW; parent unconfirmed; no AI/GPU signal found |
| TELMEX Triara | 5 | 5 | no public MW; parent unconfirmed |
| IFXNetworks | 4 | 5 | no public MW; parent unconfirmed |
| Vivo | 4 | 5 | no public MW; parent unconfirmed |
| NextStream | 3 | 5 | parent unconfirmed |
| Sencinet | 3 | 5 | no public MW; parent unconfirmed |
| Ultranet Telecom | 3 | 5 | no public MW; parent unconfirmed; no AI/GPU signal found |
| Ada Infrastructure | 2 | 5 | no public MW; parent unconfirmed |
| Claro | 2 | 5 | no public MW; parent unconfirmed |
| InterNexa | 2 | 5 | no public MW |
| Kyndryl | 2 | 5 | no public MW; parent unconfirmed |
| S3 Simple Smart Speedy | 2 | 5 | no public MW; parent unconfirmed; no AI/GPU signal found |
| Telium Networks | 2 | 5 | no public MW; parent unconfirmed |
| Tigo | 2 | 5 | no public MW |
| Data Horizon Americas (DHAmericas) | 1 | 5 | no public MW; no AI/GPU signal found |
| RiverHook Village 18 | 2 | 4 | no public MW; parent unconfirmed |
| Angola Cables | 1 | 4 | no public MW; parent unconfirmed |
| Bleeding Edge | 1 | 4 | no public MW; parent unconfirmed |
| Ilkari | 1 | 4 | no public MW; parent unconfirmed |
| Microsoft | 3 | 3 | no public MW; parent unconfirmed |
| Marcatel | 4 | 2 | no public MW; parent unconfirmed |

## Enrichment gaps

- **datacenters.com:** no provider profile matched for 5 enriched operators: data-horizon-americas-dhamericas, megatelecom, riverhook-village-18, s3-simple-smart-speedy, ultranet-telecom. These need a manual datacenters.com / vendor-site lookup for AI/wholesale claims.
- **Cloudscene connectivity (metro-level, qualitative):** sao-paulo=High (254 network/service providers, 85 data centers listed (Cloudscene)); queretaro=Med (42 network/service providers, 28 data centers listed (Cloudscene)); bogota=Med (45 network/service providers, 32 data centers listed (Cloudscene)).
- Cloudscene was intentionally limited to São Paulo, Querétaro, Bogotá per scope; other priority metros (Rio de Janeiro, Mexico City, Medellín) have no carrier/IX density rating yet.

## Known caveats / suggested manual follow-ups

- **MW is the biggest gap.** For a capacity-based partnership map, pull MW/racks/PUE from operator sites, investor decks, or datacentermap Specs (login) for the top operators: Scala Data Centers, Ascenty Data Centers, Equinix, Elea Data Centers, KIO Networks, CloudHQ, ODATA, an Aligned Data Centers Company, Cirion, TAKODA, Tecto Data Centers.
- **Telco-owned colos** score high when they publicly offer colocation, but AI/neocloud partnership openness is uncertain — confirm commercial wholesale/AI appetite directly. Candidates flagged Low openness with a colo footprint: (none flagged).
- **Parent companies** were only auto-derived where stated on-page. Confirm ownership for the top operators via corporate filings / press.
- **Pre-launch facilities** (2025–2026 builds) show no services yet and are scored conservatively; revisit as they open.
