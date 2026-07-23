# Agent B Execution Log

## Batch 1 — completed 2026-07-23

Base ID: `app1uMeDFdCUWRHQl`
Companies table: `tblHcz2TRsrcqkahK`
Contacts table: `tbl7HfGmVtR9TTIyi`

### Companies processed (10)

| # | Company | Country | Sector | Status | Priority Tier | Inference | Latency | Residency | Self-Host | Growth | Contacts |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Allie | Mexico | General Data Analysis | Active | Tier 2 | Med | High | Med | Unknown | High | 3 |
| 2 | Anastasia | Chile | Logistics Mobility & Ops | Active | Tier 2 | Med | Low | Med | Unknown | Med | 2 |
| 3 | AnyoneAI | Argentina | Education | Active | Tier 3 | Low | Low | Low | Unknown | Med | 0 |
| 4 | Aravita | Brazil | Sustainability & Agro | Active | Tier 2 | Med | Low | Low | Unknown | Med | 2 |
| 5 | Arkham | Mexico | Finance | Active | Tier 2 | Med | Med | High | Unknown | High | 2 |
| 6 | Assis | Brazil | Sales & Customer Support | Active | **Tier 1** | High | High | Med | Unknown | Med | 2 |
| 7 | Atlas | Argentina | Talent & Workforce | **Acquired** | Tier 3 | Low | Low | Med | Unknown | Low | 0 |
| 8 | Avedian | Argentina | Healthcare | Active | Tier 2 | Med | Med | High | Unknown | High | 1 |
| 9 | Bemagro | Brazil | Sustainability & Agro | Active | Tier 2 | Med | Low | Low | Unknown | High | 2 |
| 10 | Bircle | Argentina | Sales & Customer Support | Active | Tier 3 | Low | High | Low | Unknown | Med | 0 |

### Tier 1 count so far: 1 (Assis)

### Contacts created: 14
- Allie: Alex Sandoval (Founder), Nicolás Degiorgis (CTO), Alejandro Cadavid (Head of AI)
- Anastasia: Felipe Saxton Sánchez (Founder), Pablo Zegers (Head of AI/ML)
- Aravita: Marco Perlman (Founder), Bruno Schrappe (CTO)
- Arkham: Mau Sepulveda (Founder), Hector Monárrez (CTO)
- Assis: Raphael Machioni (Founder), Vagner Dutra (CTO)
- Avedian: Guillermo Tabares (Founder)
- Bemagro: Johann Coelho (Founder), Ricardo Horita (CTO)

### Companies needing manual review

1. **Allie** — CSV website `allie.ai` returns 403 to WebFetch; live site is `allie-ai.com`. CSV description ("AI copilot for admin tasks") is outdated — company pivoted to manufacturing AI (FactoryGPT). LinkedIn URL guessed as `linkedin.com/company/allie-ai` (not directly verified). Recommend user verify LinkedIn + confirm pivot.
2. **Aravita** — CSV website `aravata.com` is a domain for sale (typo). Corrected to `aravita.com` in Airtable. User should confirm.
3. **Arkham** — CSV website `arkham.mx` timed out; live site is `arkham.tech`. Corrected in Airtable. HQ listed as Mexico City but AI Tracker lists Miami — user may want to confirm.
4. **Avedian** — CSV website `avedian.com`; live site is `avedian.tech`. Corrected in Airtable. HQ now Tulsa, OK (US) with Córdoba ops — user may want to confirm Argentina vs US HQ.
5. **Assis** — CSV website `assis.ai`; live site is `assis.co`. Corrected in Airtable. Classified Tier 1 (voice AI agents = High inference + High latency). Only 2 contacts drafted (CFO João Bergamo skipped per non-technical-role rule). User may want to add CFO if finance-ops decision-maker matters.
6. **Atlas** — Marked Status = "Acquired" (by Remote, per Endeavor/TechCrunch Feb 2024). No enrichment, no contacts. User may want to remove from active pipeline or keep for reference.
7. **Anastasia** — Headcount Band = Unknown (not found in public sources). Total Raised ~$5M is approximate (multiple rounds, latest round details not found). User may want to verify.
8. **Bircle** — Classified Tier 3 (pre-seed $100K → Inference=Low per rules) but product profile (voice/chat AI agents, High latency) is prime neocloud target. User may want to upgrade if inference scale is larger than public signals suggest.

### Deviations / notes
- All company LinkedIn URLs are best-guess patterns (`linkedin.com/company/<slug>`) since direct LinkedIn company page lookups were not always confirmable via web search. User should verify before outreach.
- No emails guessed (per rules).
- No contact marked Confidence = High (none were found on a company's own team page WITH a captured LinkedIn link simultaneously; most found via press/web search → Med).
- Layer 3 (interview) fields untouched.
- Airtable raw PATCH/POST required `Content-Type: application/json` header (first attempt without it failed validation).

### Failures
- None. All 10 Companies updates and 14 Contacts creations returned HTTP 200.

### User feedback applied (after batch 1 review)

- **Allie**: LinkedIn corrected to `https://www.linkedin.com/company/allieai` (user-confirmed; my original `allie-ai` slug was wrong).
- **Arkham**: LinkedIn corrected to `https://www.linkedin.com/company/arkham-technologies` (my original `arkham-tech` was wrong); HQ City updated to "Palo Alto, CA (founders ex-Konfio, Mexico)"; Total Raised updated to "$7M" (per LinkedIn, was $4.5M).
- **Avedian**: HQ City set to "Córdoba, Argentina (legal HQ: Tulsa, OK)" per user preference (user wants origin/team city, not legal HQ). LinkedIn `linkedin.com/company/avediantech` kept — verified correct per LinkedIn's own posts; if user still sees "unavailable" it may be a LinkedIn login-wall issue.
- **Anastasia**: Headcount Band cleared to blank (was "Unknown") per user preference. Total Raised corrected to "$1.4M" (per LinkedIn, was "~$5M" estimate).
- **Atlas**: Confirmed dropped from active pipeline (Status = Acquired; excluded from future batches by Status=Active filter).
- **Bircle** (user referred to as "Perco"): Upgraded Tier 3 → Tier 2, Inference Low → Med per user direction ("high in variance"). 2 founder contacts added (Marcos Lozada Freytes, José Romero Victorica).

### Proactive corrections (LinkedIn/headcount verification pass)
- **Assis**: LinkedIn corrected to `linkedin.com/company/assis-app` (my `assis-ai` slug was a different, wrong education company).
- **Bemagro**: Headcount Band corrected 11–50 → 51–200 (per LinkedIn, 80–90 employees); Inference Demand upgraded Med → High (now meets all three High criteria: $10M+, 50+ headcount, imaging). Tier stays 2 (Low latency/residency).
- Verified correct (no change): Anastasia (`anastasia-ai`), AnyoneAI (`school/anyone-ai`), Aravita (`aravita`), Avedian (`avediantech`), Bemagro (`bemagroag`).

### Manual-review count discussion
- Batch 1 flagged 8/10 for manual review — user questioned whether this is acceptable.
- Going forward, Agent B will flag only genuine blockers (dead links, wrong company match, status changes, missing critical data) and fold minor uncertainties into Classification Notes instead of flagging. Target: ≤3 flags per batch of 10.

### Next batch
- Batch 2 will fetch the next 10 Active companies with empty Classification Date (sorted by Company Name), starting after "Bircle". Awaiting user confirmation.

---

## Batch 2 — completed 2026-07-23

### Companies processed (10)
| # | Company | Country | Sector | Status | Priority Tier | Inference | Latency | Residency | Self-Host | Growth | Contacts |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 1 | Birdie | Mexico (CSV) / Palo Alto (actual) | Logistics Mobility & Ops (CSV) / CX Analytics (actual) | Active | Tier 2 | Med | Low | Med | Unknown | Med | 2 |
| 2 | Carecode | Brazil | Sales & Customer Support | Active | **Tier 1** | Med | High | High | Unknown | High | 2 |
| 3 | Cedalio | Argentina | General Data Analysis & Business Automation | Active | Tier 2 | Med | Low | Med | Unknown | Med | 2 |
| 4 | Cenit | Chile | Finance | Active | Tier 2 | Med | Med | High | Unknown | High | 2 |
| 5 | Chambas AI | Mexico | Talent & Workforce Management | Active | Tier 3 | Low | Med | Med | Unknown | High | 0 |
| 6 | Cloud Humans | Brazil | Talent & Workforce Management | Active | Tier 2 | Med | High | Med | Unknown | Med | 3 |
| 7 | Comp | Brazil | Talent & Workforce Management | Active | Tier 2 | High | Med | Med | Unknown | High | 2 |
| 8 | Crook | Mexico | Healthcare | Active (unverified) | Tier 3 | Low | Low | Med | Unknown | Low | 0 |
| 9 | Dapta | Colombia | Sales & Customer Support | Active | **Tier 1** | High | High | Low | Unknown | High | 1 |
| 10 | Darwin Ai | Brazil | General AI Platforms | Active | **Tier 1** | High | High | Med | Unknown | High | 2 |

### Tier 1 count so far: 4 (Assis from batch 1 + Carecode, Dapta, Darwin Ai from batch 2)

### Contacts created: 16
- Birdie: Alexandre Hadade (Founder), Everton Cherman (CTO)
- Carecode: Thomaz Srougi (Founder), Pedro Magalhães (CTO)
- Cedalio: Luciana Reznik (Founder), Guido Marucci Blas (CTO)
- Cenit: Andrés Liberman (Founder), Ronny González (Founder/CPO)
- Cloud Humans: Ian Kraskoff (Founder), Bruno Cecatto (Founder), Felipe Serra (Founder)
- Comp: Christophe Gerlach (Founder), Pedro Bobrow (Founder)
- Dapta: Nicolas Rojas Niño (Founder — High confidence, found on LinkedIn)
- Darwin Ai: Lautaro Schiaffino (Founder), Ezequiel Sculli (Founder)

### Companies needing manual review (3 — within target ≤3)

1. **Birdie** — CSV tags Country=Mexico, Sector=Logistics Mobility & Ops, but website `birdie.ai` and description match the **Palo Alto/Brazil CX analytics company** (founded 2018 by Alexandre Hadade, Patrícia Osorio, Rodrigo Pantigas, Everton Cherman; SoftBank LatAm Fund backed). There IS a separate Mexico-based Birdie (founded 2023, supply chain traceability) but its website is NOT `birdie.ai`. User should confirm which company is intended and correct Country/Sector if needed.
2. **Cenit** — CSV description ("AI infrastructure for banks and fintechs to build financial products") does NOT match the actual product on `cenit.ai` (AI mobile app for tax management for freelancers/SMEs in Chile, founded by ex-Betterfly team, Hi Ventures led $1.8M seed Nov 2025). User should confirm description should be updated.
3. **Crook** — CANNOT VERIFY. Website `crookhealth.com` returns 403 Forbidden. No matching company found in Crunchbase, news, or LinkedIn searches. CSV description ("AI health assistant that connects patients with doctors and manages medical records") suggests healthcare AI but no public presence exists. User should confirm company exists or provide correct name/website.

### Deviations / notes
- All company LinkedIn URLs are best-guess patterns (`linkedin.com/company/<slug>`) verified where possible via web search. User should verify before outreach.
- Individual contact LinkedIn URLs are best-guess slugs (`linkedin.com/in/<firstname lastname>`), except Nicolas Rojas Niño (`/in/nicolasimagine`) which was found directly on his LinkedIn profile (High confidence).
- No emails guessed (per rules).
- Only 1 contact marked Confidence = High (Nicolas Rojas Niño, Dapta — found directly on LinkedIn). All others Med (found via press/web search).
- Layer 3 (interview) fields untouched.
- Airtable raw PATCH/POST required `Content-Type: application/json` header AND body passed as JSON string (not object) — earlier attempt with object body failed validation.

### Classification reasoning highlights
- **Carecode (Tier 1)**: Med Inference + High Latency (voice) + High Residency (healthcare/LGPD) + High Growth. Meets Tier 1 rule "Med Inference AND Latency=High AND Residency=High". Backed by a16z + QED.
- **Dapta (Tier 1)**: High Inference (voice AI at scale — 30,000+ companies across 37 countries) + High Latency (voice) + High Growth (12x revenue). Meets Tier 1 rule "High Inference AND (Latency=High OR Residency=High)".
- **Darwin Ai (Tier 1)**: High Inference ($7M funding, voice AI at scale — 300+ clients, $2M+ ARR) + High Latency (voice) + High Growth. Meets Tier 1 rule "High Inference AND (Latency=High OR Residency=High)".
- **Comp (Tier 2, not Tier 1)**: High Inference ($17.25M Series A, AI-native HR product) but Med Latency + Med Residency. Does NOT meet Tier 1 rule "High Inference AND (Latency=High OR Residency=High)". Classified Tier 2 — one High signal without scale.
- **Cenit (Tier 2)**: Med Inference + Med Latency + High Residency (tax data) + High Growth. One High signal (Residency) without scale (Med Inference) → Tier 2.
- **Chambas AI (Tier 3)**: Low Inference (pre-seed $500K, <11 headcount, AI chatbot is a feature). Per rules, Inference=Low → Tier 3.
- **Crook (Tier 3)**: Cannot verify — marked Low/Unknown across all signals, Tier 3.

### Failures
- None. All 10 Companies updates (3 PATCH calls) and 16 Contacts creations (2 POST calls) returned HTTP 200.

### Next batch
- Batch 3 will fetch the next 10 Active companies with empty Classification Date (sorted by Company Name), starting after "Darwin Ai". Awaiting user confirmation.

---

## Batch 2 — user feedback applied (2026-07-23)

### Corrections made per user feedback

1. **Birdie** — User confirmed CSV refers to the **Mexico-based Birdie** (birdie.mx), NOT the Palo Alto/Brazil CX analytics company (birdie.ai). CSV had wrong website and description (both belonged to the Palo Alto Birdie). Updated:
   - Website: `birdie.ai` → `birdie.mx`
   - HQ City: "Palo Alto, CA" → "Mexico City, Mexico"
   - LinkedIn: `linkedin.com/company/usebirdie` → `linkedin.com/company/birdietech`
   - Founded Year: 2018 → 2022
   - Headcount Band: 11–50 (unchanged)
   - Total Raised: "$7-10M" → "$500K"
   - Last Round: "Seed" → "Pre-Seed"
   - Last Round Date: 2022-09-01 → 2023-01-01
   - Last Round Investor: SoftBank LatAm Fund → "Sente Ventures, 500 LATAM, Techstars, BuenTrip Ventures, 500 Global"
   - Product Type: Batch → Hybrid
   - Inference Workload: Text → Text, Image
   - Notable Customers: "P&G, Samsung" → "Import companies in MX, CO, CL, PE (200K+ customs docs processed)"
   - Inference Demand Scale: Med → Low (pre-seed $500K, AI is a feature for document validation)
   - Latency Sensitivity: Low → Med (real-time tracking + batch document validation)
   - Priority Tier: **Tier 2 → Tier 3** (Low Inference per rules)
   - Deleted 2 wrong contacts: Alexandre Hadade (Founder), Everton Cherman (CTO) — these belong to the Palo Alto Birdie, not the Mexico Birdie.
   - No new contacts created (Tier 3 = no contacts per rules).

2. **Cenit** — User requested description update. Updated Description from "AI infrastructure for banks and fintechs to build financial products" to "AI-powered mobile app for tax management (SII integration) for freelancers and SMEs in Chile and Mexico. Calculates, declares, and pays taxes with one click; tracks income, expenses, invoices in real time." (Description is normally Agent A's field, but user explicitly requested this correction.)

3. **Crook → Rook** — User identified that the CSV name "Crook" is wrong; the correct company is **Rook** (tryrook.io). Updated:
   - Company Name: "Crook" → "Rook"
   - Website: `crookhealth.com` → `tryrook.io`
   - Description: Updated to "B2B SaaS API and SDK platform for integrating wearable and health data from 400+ devices into applications. Rebranded from RookMotion to ROOK in 2023."
   - HQ City: blank → "Spring, TX (with Mexico team presence)"
   - LinkedIn: blank → `linkedin.com/company/tryrookio`
   - Founded Year: blank → 2019
   - Headcount Band: blank → 11–50
   - Total Raised: blank → "$1.7M"
   - Last Round: blank → "Pre-Seed"
   - Last Round Date: blank → 2023-03-16
   - Last Round Investor: blank → "NuFund Venture Group (lead), AlliedVC, CrossOceanFund, Harvard Business Fund, Hilltop Venture Partners, InstaVC, IrieVC, IQ Ventures, Liebenthal, Mana Ventures, MCMA VC, Stadia Ventures, Techstars, TheSageHouse, Pankaj Kedia"
   - Product Type: blank → Batch
   - Inference Workload: blank → Text, Embeddings
   - Notable Customers: blank → "Trainingym, Gentherm, PEAR Health Labs, NASM, Novos Lab, Physmodo, Advanta Health Solutions"
   - Inference Demand Scale: Low → Med (data transformation API, $1.7M funding)
   - Latency Sensitivity: Low → Med (API calls)
   - Data Residency Likelihood: Med → High (health data, HIPAA-type regulation)
   - Growth Trajectory: Low → Med (last funding March 2023)
   - Priority Tier: **Tier 3 → Tier 2** (Med Inference + High Residency without scale)
   - Created 2 new contacts: Marco Benitez (Founder/CEO), Daniel Martinez Aguilar (CTO)

### Updated Batch 2 totals after corrections
- **Tier 1: 3** (Carecode, Dapta, Darwin Ai) — unchanged
- **Tier 2: 5** (Cedalio, Cenit, Cloud Humans, Comp, **Rook**) — Birdie dropped to Tier 3, Rook added from Tier 3
- **Tier 3: 2** (Chambas AI, **Birdie**) — Crook→Rook upgraded to Tier 2, Birdie downgraded from Tier 2
- **Contacts: 16** (unchanged net: -2 Birdie Palo Alto contacts deleted, +2 Rook contacts added)

### Tier 1 count so far (cumulative across batches): 4
- Batch 1: Assis
- Batch 2: Carecode, Dapta, Darwin Ai

### Note on Birdie CSV discrepancy
The CSV entry for Birdie had Country=Mexico and Sector=Logistics Mobility & Ops (which match the Mexico Birdie), but Website=birdie.ai and Description="AI-powered customer-feedback and product-analytics platform" (which match the Palo Alto/Brazil Birdie). This was a CSV data-entry error where the wrong website/description was paired with the correct country/sector. User confirmed the Mexico Birdie (birdie.mx, supply chain) is the intended company. Website and Description updated accordingly.
