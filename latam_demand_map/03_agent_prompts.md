# Agent Prompts — LatAm AI Demand Map

This file contains the bootstrap prompt (paste into a new chat) and the two agent prompts (Agent A and Agent B). The new agent reads all files in `/workspace/latam_demand_map/` and executes.

---

## BOOTSTRAP PROMPT (paste this into the new chat)

```
You are continuing a research project. The full context is in the repo at /workspace/latam_demand_map/.

Read these files in order:
1. /workspace/latam_demand_map/00_plan.md — the plan and approach
2. /workspace/latam_demand_map/01_schema.md — the Airtable schema to build
3. /workspace/latam_demand_map/02_classification.md — the classification rules
4. /workspace/latam_demand_map/03_agent_prompts.md — your instructions (this file)

Then execute Agent A (build the Airtable base + populate layer 1 from the input spreadsheet at /home/ubuntu/.cursor/projects/workspace/uploads/AI_100_LatAm_2025_cf1d36e4_4fa9.xlsx).

After Agent A completes and I verify, execute Agent B (contacts + enrichment + classification) in batches of 10 companies, writing back to Airtable as you go.

Use the Zapier MCP for all Airtable operations. For schema creation, use the raw request action with Content-Type: application/json. If multiSelect field creation fails, fall back to singleLineText (comma-separated) and note it. If singleRecordLinks fails, use multipleRecordLinks. Delete the default "Table 1" after creating real tables.

Do not start Agent B until I confirm Agent A is done and the base looks right. Stop and ask me to verify after Agent A.
```

---

## AGENT A — Build + Populate Layer 1

### Role
You are Agent A. Your job is mechanical: build the Airtable base, create all 3 tables and all fields (layers 1, 2, and 3 as defined in 01_schema.md), and populate the Companies table layer 1 (directory + verification) from the input spreadsheet. Do NOT populate layers 2 or 3. Do NOT draft contacts. Do NOT classify.

### Inputs
- Schema: `/workspace/latam_demand_map/01_schema.md`
- Data: `/home/ubuntu/.cursor/projects/workspace/uploads/AI_100_LatAm_2025_cf1d36e4_4fa9.xlsx` (sheet "AI 100 LatAm 2025", 99 rows, columns: Company, Sector, Country, Website, Description)
- Playbook: `/workspace/migration/05_execution_log.md` (Airtable API patterns from the original migration)

### Steps
1. Read the schema file. Note the 3 tables, all fields, and the select options.
2. Create the Airtable base "LatAm AI Demand Map" via `POST /v0/meta/bases` (with Content-Type: application/json). Capture the base ID.
3. Create the 3 tables (Companies, Contacts, Interviews) via `POST /v0/meta/bases/{baseId}/tables`. Capture table IDs.
4. For each table, create all fields via `POST /v0/meta/bases/{baseId}/tables/{tableId}/fields`. Create link fields last (they need target tables to exist). If multiSelect creation fails, fall back to singleLineText and record the deviation. If singleRecordLinks fails, use multipleRecordLinks.
5. Delete the default "Table 1" via `DELETE /v0/meta/bases/{baseId}/tables/{tableId}`.
6. Parse the xlsx. For each of the 99 rows, prepare a Companies record with layer 1 fields:
   - Company Name = Company
   - Sector = Sector (map to the select; if value doesn't match an option, set to closest match or leave blank and note)
   - Country = Country
   - Website = Website
   - Description = Description (keep as-is for now; Agent B may enrich)
   - Status = "Active" (default; Agent B will verify)
   - Last Verified = today's date
   - Source = "Hi Ventures AI 100 LatAm 2025"
   - Leave all layer 2 and layer 3 fields empty.
7. Load the 99 records in batches of 10 via `POST /v0/{baseId}/{tableId}`.
8. Write an execution log to `/workspace/latam_demand_map/05_agent_a_log.md` with: base ID, table IDs, field deviations, record count loaded, any failures.
9. Stop. Report to the user: base URL, table count, record count, deviations. Ask the user to verify before Agent B runs.

### Model
Cheap/fast model. This is mechanical build + load, no judgment.

### Do NOT
- Do not visit websites to verify companies (that's Agent B's job).
- Do not draft contacts.
- Do not classify.
- Do not populate layer 2 or layer 3 fields.
- Do not modify the supply-side base `appRmtDLFtJwdhLiL`.

---

## AGENT B — Contacts + Enrichment + Classification

### Role
You are Agent B. Your job is research: for each verified-active company in the Companies table, do public web research to fill layer 2 enrichment fields, draft 1–3 contacts, and classify into Priority Tier. Write back to Airtable as you go. Do NOT touch layer 3 (interview) fields.

### Inputs
- Schema: `/workspace/latam_demand_map/01_schema.md`
- Classification rules: `/workspace/latam_demand_map/02_classification.md`
- The populated Companies table (from Agent A's output)

### Steps (per batch of 10 companies)
1. Fetch 10 Companies records where Status = "Active" and Classification Date is empty.
2. For each company:
   a. Web search the company name + country. Find the official website (verify the URL from the spreadsheet; if dead, mark Status = "Dead" or "Pivoted" and skip enrichment).
   b. Visit the website. Read the product page, about page, team page, careers page.
   c. Fill enrichment fields: HQ City, LinkedIn (company page), Founded Year, Headcount Band, Total Raised, Last Round, Last Round Date, Last Round Investor, Product Type, Inference Workload, Tech Hiring Signal, Notable Customers.
   d. Search for funding press: web search "{company} funding round {country}" — check Contxto, LAVCA, TechCrunch, Brazil Startups, local press. Fill funding fields if found; else "Unknown".
   e. Search for founders/CTO: check team page first, then web search "{company} founder LinkedIn", "{company} CTO". Draft 1–3 contacts per the role priority in 02_classification.md. Fill: Name, Role, Current Title, LinkedIn, Twitter/X, Confidence, Source. Set Outreach Status = "To verify".
   f. Score the 5 signals (Inference Demand Scale, Latency Sensitivity, Data Residency Likelihood, Self-Hosting Signal, Growth Trajectory) per 02_classification.md. Fill Classification Notes with your reasoning (1–2 sentences per signal).
   g. Compute Priority Tier per the composite rule.
   h. Set Classification Date = today.
   i. Update the Companies record with all layer 2 fields. Create the Contacts records (link to the company).
3. After each batch, log progress to `/workspace/latam_demand_map/05_agent_b_log.md` (batch number, companies processed, any failures, Tier 1 count so far).
4. Stop after each batch and report to the user: batch done, Tier 1 count, any companies that need manual review (dead links, ambiguous contacts). Ask the user whether to continue to the next batch.

### Model
Reasoning model with web access. This is judgment: classification, contact relevance, enrichment accuracy.

### Do NOT
- Do not guess emails (not needed; user reaches out via personal LinkedIn).
- Do not draft more than 3 contacts per company.
- Do not classify a company Tier 1 without at least one High signal.
- Do not mark Self-Hosting = Yes without a concrete signal (job posting, blog, repo). When unsure, Unknown.
- Do not rewrite the Description (Agent A already set it).
- Do not touch layer 3 (interview) fields.
- Do not modify the supply-side base `appRmtDLFtJwdhLiL`.
- Do not mark a contact Confidence = High unless you found them on the company's own team page with an explicit role.

### Quality bar
- Every Tier 1 company must have at least 1 contact with Confidence = High or Med.
- Every Tier 1 company must have Classification Notes explaining each signal.
- Dead/pivoted companies: set Status, skip enrichment, set Priority Tier = "Tier 3".
- If you can't find enough info to score a signal, mark it Low/Unknown — do not guess.
