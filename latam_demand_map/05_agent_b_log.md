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

### Next batch
- Batch 2 will fetch the next 10 Active companies with empty Classification Date (sorted by Company Name), starting after "Bircle". Awaiting user confirmation.
