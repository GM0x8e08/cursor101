# LatAm AI Demand Map — Build Plan

## Goal
Build an independent Airtable base ("LatAm AI Demand Map") that maps ~99 LatAm AI startups from the Hi Ventures AI 100 LatAm 2025 list, enriches each with public research, classifies them by neocloud-fit priority, and drafts contacts — so the user can interview the top ~20 to validate a LatAm inference / neocloud thesis.

This base is **independent** from the supply-side base "Compute Finance Research v2" (`appRmtDLFtJwdhLiL`). Different entity types, different schemas, no cross-base links. If a company ever appears in both, reference by name; do not hard-link.

## Why independent
- Supply base = who builds the compute market (index providers, neoclouds, chipmakers).
- Demand base = who buys inference in LatAm (AI application startups).
- The relationship is conceptual (the user's thesis: demand meets supply via a LatAm neocloud), not a data relationship. Keep decoupled until there's a real reason to couple (e.g., a signed customer).

## The three layers
1. **Directory + verification** — Agent A populates from the 99 rows, verifies each company is alive, rewrites description, sets status.
2. **Contacts + enrichment + classification** — Agent B drafts contacts (name, role, LinkedIn, Twitter, confidence) and enriches each company (funding, headcount, product type, inference workload) and classifies (5 signals + Priority Tier). User curates contacts.
3. **Interview findings** — User fills manually after interviews. Fields exist in the schema but stay empty until then.

## Two agents
- **Agent A — Build + populate layer 1.** Reads `01_schema.md` + the 99 rows. Creates the Airtable base, all 3 tables, all fields (layers 2 and 3 as empty fields ready for later). Populates Companies layer 1. Cheap model. One-shot.
- **Agent B — Contacts + enrichment + classification.** Reads `01_schema.md` + `02_classification.md` + the populated base. For each verified-active company: web research → enrichment fields + 1–3 drafted contacts + 5 classification signals + Priority Tier. Writes back to Airtable. Reasoning model with web access. Repeatable in batches of ~10.

## Model tiers
- Agent A: cheap/fast model (mechanical build + load).
- Agent B: reasoning model with web access (judgment: classification, contact relevance).

## Airtable API notes (from original migration)
- Use Zapier MCP raw request with `Content-Type: application/json` header for meta API calls.
- `multiSelect` field creation may fail via API → fall back to `singleLineText` (comma-separated) and note for UI conversion.
- `singleRecordLinks` field creation may fail → use `multipleRecordLinks` (holds one value).
- Default "Table 1" gets created with new bases → delete it after creating real tables.
- See `/workspace/migration/05_execution_log.md` for the full playbook from the original migration.

## File index
- `00_plan.md` — this file
- `01_schema.md` — full Airtable schema (3 tables, all fields, select options)
- `02_classification.md` — the 5 signals + Priority Tier + scoring rules + contact role priority
- `03_agent_prompts.md` — Agent A prompt + Agent B prompt + the bootstrap prompt for the new chat

## Workflow for the user (two separate chats, manual handoff)
1. Merge the PR for this branch into main (so the new agents can read the files from main).
2. Open chat 1 in Cursor. Paste the "PROMPT FOR AGENT A CHAT" from `03_agent_prompts.md`. Agent A builds the base + populates layer 1, then stops and reports the base ID.
3. Verify Agent A's base in Airtable (tables, fields, 99 records loaded).
4. Open chat 2 in Cursor (separate from chat 1). Paste the "PROMPT FOR AGENT B CHAT" from `03_agent_prompts.md`, with the base ID from Agent A's report pasted into the placeholder. Agent B runs in batches of 10, pausing for your verification between batches.
5. User curates contacts (layer 2) and conducts interviews (layer 3).

The two chats are independent. The only thing carried from chat 1 to chat 2 is the Airtable base ID. Everything else both agents read from the repo files.

## Source data
- Input CSV (committed to repo): `/workspace/latam_demand_map/data/latam_ai_100.csv`
- Original spreadsheet (not in repo; lives in the cloud agent uploads folder of the chat that received it): `AI_100_LatAm_2025_cf1d36e4_4fa9.xlsx`
- 99 rows, 5 columns: Company, Sector, Country, Website, Description
- Source: Hi Ventures — Venture-backed AI startups with $1M–10M in funding
- Distribution: Brazil 34, Mexico 31, Argentina 15, Chile 8, Colombia 4, Uruguay 3, Peru 2, Venezuela 1, Ecuador 1
- Sectors: Sales & Customer Support 19, Talent & Workforce 15, Finance 14, Healthcare 11, General Data Analysis 8, Retail & Ecommerce 7, Education 6, Logistics 6, General AI Platforms 5, Legal & Compliance 4, Sustainability & Agro 4
