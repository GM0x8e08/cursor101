# Schema — LatAm AI Demand Map

Base name: **LatAm AI Demand Map**
Three tables: Companies, Contacts, Interviews. No junction tables. No cross-base links.

## Table 1: Companies

Primary field: Company Name.

### Layer 1 — Directory + verification (Agent A populates)
| Field | Type | Notes |
|---|---|---|
| Company Name | Single line text | primary |
| Sector | Single select | Healthcare · Sales & Customer Support · Talent & Workforce Management · Finance · General Data Analysis & Business Automation · Retail & Ecommerce · Education · Logistics Mobility & Ops · General AI Platforms · Legal & Compliance · Sustainability & Agro |
| Country | Single select | Brazil · Mexico · Argentina · Chile · Colombia · Uruguay · Peru · Venezuela · Ecuador |
| Website | URL | verified by Agent A |
| Description | Long text | rewritten by Agent A from website visit |
| Status | Single select | Active · Pivoted · Dead · Acquired · Unknown |
| Last Verified | Date | when Agent A verified |
| Source | Single line text | "Hi Ventures AI 100 LatAm 2025" |

### Layer 2 — Enrichment (Agent B populates)
| Field | Type | Notes |
|---|---|---|
| HQ City | Single line text | |
| LinkedIn | URL | company LinkedIn page |
| Founded Year | Number | |
| Headcount Band | Single select | 1–10 · 11–50 · 51–200 · 201–500 · 500+ · Unknown |
| Total Raised | Single line text | free text, e.g. "$5M" |
| Last Round | Single line text | e.g. "Series A" |
| Last Round Date | Date | |
| Last Round Investor | Single line text | e.g. "Kaszek, monashees" |
| Product Type | Single select | Real-time · Batch · Hybrid · Unknown |
| Inference Workload | Multi-select (or singleLineText fallback) | Text · Image · Video · Audio · Multimodal · Embeddings · Training |
| Tech Hiring Signal | Single select | Yes · No · Unknown |
| Notable Customers | Single line text | |

### Layer 2 — Classification (Agent B populates)
| Field | Type | Notes |
|---|---|---|
| Inference Demand Scale | Single select | High · Med · Low |
| Latency Sensitivity | Single select | High · Med · Low |
| Data Residency Likelihood | Single select | High · Med · Low |
| Self-Hosting Signal | Single select | Yes · No · Unknown |
| Growth Trajectory | Single select | High · Med · Low |
| Priority Tier | Single select | Tier 1 · Tier 2 · Tier 3 |
| Classification Notes | Long text | Agent B's reasoning |
| Classification Date | Date | |

### Layer 3 — Interview findings (User populates)
| Field | Type | Notes |
|---|---|---|
| Interview Status | Single select | Not started · Scheduled · Completed · Declined |
| Interview Date | Date | |
| Inference Workload Confirmed | Multi-select | Text · Image · Video · Audio · Multimodal · Embeddings · Training |
| Primary Model(s) Used | Single line text | e.g. "GPT-4o, Llama 3.1 70B" |
| Primary Model Provider | Multi-select | OpenAI · Anthropic · Google · AWS Bedrock · Azure · self-hosted · Together · Fireworks · Other |
| Usage Volume | Single line text | e.g. "50M tokens/day" |
| Latency Sensitivity Confirmed | Single select | High · Med · Low |
| Current Sourcing | Single select | API direct · Cloud-hosted open models · Self-hosted cloud GPU · Self-hosted on-prem · Hybrid |
| Monthly Spend Band | Single select | <$1K · $1–10K · $10–100K · $100K–1M · $1M+ |
| Pain Points | Multi-select | Latency · Cost · Reliability · Data residency · Compliance · Sovereignty · Model availability · Talent |
| Data Residency Constraint | Single select | Yes-country · Yes-region · No · Unknown |
| Would Use LatAm Neocloud | Single select | Yes · No · Maybe · Need more info |
| Why/Why Not | Long text | |
| Price Ceiling vs Current | Single line text | e.g. "would switch at 20% discount" |
| Latency Requirement | Single line text | e.g. "<100ms TTFT for voice" |
| Switching Cost | Long text | |
| Interview Notes | Long text | |

## Table 2: Contacts

Primary field: Name. Layer 2 — drafted by Agent B, curated by user.

| Field | Type | Notes |
|---|---|---|
| Name | Single line text | primary |
| Role | Single select | Founder · CEO · CTO · COO · Head of AI/ML · Head of Eng · Head of Infra · Other |
| Company | Link → Companies (multi, holds one) | |
| Current Title | Single line text | e.g. "CTO & Co-founder" |
| LinkedIn | URL | |
| Twitter/X | URL | |
| Confidence | Single select | High · Med · Low |
| Source | Single select | Team page · Press · Web search · LinkedIn · Other |
| Outreach Status | Single select | Not started · To verify · Verified · Contacted · Responded · Interviewed · Declined |
| Outreach Method | Single select | LinkedIn · Twitter · Warm intro · Event · Other |
| Last Contact | Date | |
| Notes | Long text | |

## Table 3: Interviews (optional — can merge into Companies layer 3)

If the user wants one interview per company, layer 3 fields on Companies suffice. If multiple interviews per company, add this table:

| Field | Type | Notes |
|---|---|---|
| Company | Link → Companies | |
| Contact | Link → Contacts | |
| Interview Date | Date | |
| Interviewer | Single line text | |
| (all layer 3 fields from Companies above) | | duplicated here for multi-interview |

**Recommendation:** start with layer 3 on Companies (one interview per company). Add the Interviews table only if you re-interview.

## Controlled vocabularies (select options)

### Sector (11)
Healthcare, Sales & Customer Support, Talent & Workforce Management, Finance, General Data Analysis & Business Automation, Retail & Ecommerce, Education, Logistics Mobility & Ops, General AI Platforms, Legal & Compliance, Sustainability & Agro

### Country (9)
Brazil, Mexico, Argentina, Chile, Colombia, Uruguay, Peru, Venezuela, Ecuador

### Priority Tier (3)
- **Tier 1** — interview now. High inference demand + high latency sensitivity OR high data residency + scale signal.
- **Tier 2** — maybe later. Some signal but not all three.
- **Tier 3** — skip. Too small, API-only, no latency/residency pain.

## Build notes / API workarounds
- Create base via `POST /v0/meta/bases` with `Content-Type: application/json`.
- Create tables via `POST /v0/meta/bases/{baseId}/tables`.
- Create fields via `POST /v0/meta/bases/{baseId}/tables/{tableId}/fields`.
- If `multiSelect` creation fails → fall back to `singleLineText` (comma-separated), note for UI conversion.
- If `singleRecordLinks` creation fails → use `multipleRecordLinks` (holds one value).
- Default "Table 1" is created with new bases → delete via `DELETE /v0/meta/bases/{baseId}/tables/{tableId}` after real tables exist.
- Load records via `POST /v0/{baseId}/{tableId}` (batch up to 10 per call).
- See `/workspace/migration/05_execution_log.md` for the full playbook.
