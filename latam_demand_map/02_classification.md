# Classification & Contact Rules — LatAm AI Demand Map

Agent B reads this file before classifying companies and drafting contacts.

## The 5 signals

Each signal is scored High / Med / Low (or Yes/No/Unknown for self-hosting). Score from public research only — do not guess. If evidence is thin, mark Low or Unknown.

### 1. Inference Demand Scale
How much inference the company likely consumes.
- **High** — funded ($5M+), 50+ headcount, product is inference-heavy (imaging, video, voice, LLM chat at scale), vertical known for heavy compute (healthcare imaging, fintech risk).
- **Med** — funded ($1–5M), 11–50 headcount, product uses inference but it's not the core moat (SaaS with AI features).
- **Low** — pre-seed or <11 headcount, AI is a feature not the product, low usage volume.
- **Source:** funding data (Crunchbase, press), headcount (LinkedIn company page or jobs), product description, vertical.

### 2. Latency Sensitivity
Whether the product needs real-time inference.
- **High** — voice, video, real-time chat, live recommendations, gaming, autonomous systems. User waits for output.
- **Med** — near-real-time (search, summarization, document Q&A with seconds-level tolerance).
- **Low** — batch (credit scoring, document processing, training, embeddings generation, async workflows).
- **Source:** product page, demo videos, use case description. Keywords: "real-time", "live", "voice", "video", "instant" → High. "batch", "async", "overnight", "pipeline" → Low.

### 3. Data Residency Likelihood
Whether the company's customers require data to stay in-country.
- **High** — verticals with regulation: healthcare (patient data), finance (financial data, central bank rules), government, legal/compliance, education (student data in some countries). Also B2B enterprise selling to regulated buyers.
- **Med** — enterprise SaaS where some customers care but not all.
- **Low** — consumer apps, generic productivity, horizontal SaaS.
- **Source:** vertical, customer type (enterprise vs consumer), country (Brazil LGPD, Mexico, Argentina have data laws), privacy policy.

### 4. Self-Hosting Signal
Whether the company likely self-hosts open models (vs. API-only).
- **Yes** — job postings for ML infra, platform engineer, MLOps, GPU, Kubernetes, vLLM, TGI, Triton. Engineering blog posts about serving. Open-source model mentions.
- **No** — job postings only for prompt engineers, API integrations, no infra roles. Product is a thin wrapper on OpenAI/Anthropic.
- **Unknown** — can't tell from public signals.
- **Source:** careers page, job boards (LinkedIn jobs, Indeed, Workana), engineering blog, GitHub repos.
- **Why it matters:** self-hosters are more likely to consider a neocloud (they already manage infra). API-only shops are harder to displace.

### 5. Growth Trajectory
Whether the company is scaling fast (future demand).
- **High** — raised a round in the last 12 months, headcount growing (multiple open roles), product expansion signals.
- **Med** — raised 12–24 months ago, stable headcount.
- **Low** — no recent funding, headcount flat or shrinking, product quiet.
- **Source:** funding date, headcount trend (LinkedIn company page shows growth), press activity, product release cadence.

## Priority Tier (composite)

- **Tier 1 — interview now.** Any of:
  - Inference Demand Scale = High AND (Latency Sensitivity = High OR Data Residency = High)
  - Inference Demand Scale = Med AND Latency Sensitivity = High AND Data Residency = High
  - Self-Hosting Signal = Yes AND Inference Demand Scale = Med or High
- **Tier 2 — maybe later.** Med signals across the board, or one High signal without scale.
- **Tier 3 — skip.** Inference Demand Scale = Low, OR API-only with no latency/residency pain, OR Status ≠ Active.

Target: ~15–25 companies in Tier 1. If Tier 1 is larger than 25, raise the bar (require 2+ High signals). If smaller than 15, lower the bar (accept 1 High signal + Med scale).

## Contact role priority

For each Tier 1 + Tier 2 company, draft 1–3 contacts in this priority order. Stop when you have 1–3; don't add low-relevance people.

1. **Founder** (if listed on team page or press) — for early-stage, the founder often is the decision-maker on infra.
2. **CTO** — for funded startups, the CTO usually owns infra decisions.
3. **Head of AI / ML / Data Science** — if they have one, they own model serving.
4. **Head of Engineering / Infra / Platform** — owns the stack.
5. **CEO** — only if founder/CTO not findable (CEO may be non-technical).

Skip: sales, marketing, ops, HR, product (non-technical PM). They don't decide inference infra.

## Confidence scoring per contact

- **High** — found on company team page with explicit role + LinkedIn link.
- **Med** — found via press (funding announcement naming the founder/CTO) or web search with clear match.
- **Low** — guessed from a name found in passing, or ambiguous match (common name, multiple people).

Mark Low honestly. The user verifies Tier 1 contacts manually before outreach anyway.

## Contact fields to populate (Agent B draft)

- Name, Role, Current Title, LinkedIn, Twitter/X, Confidence, Source
- Leave Outreach Status = "To verify" for all drafted contacts.
- The user moves to "Verified" after checking, then "Contacted" after outreach.

## What NOT to do

- Do not guess emails. The user reaches out via personal LinkedIn; emails are not needed.
- Do not draft more than 3 contacts per company.
- Do not classify a company Tier 1 without at least one High signal.
- Do not mark Self-Hosting = Yes without a concrete signal (job posting, blog, repo). When unsure, Unknown.
- Do not rewrite the Description (Agent A already did). Only add enrichment fields.
- Do not touch layer 3 (interview) fields — those are the user's.
