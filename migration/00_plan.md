# Compute Finance Research — Airtable Migration Plan

## Goal
Migrate the existing Airtable base ("Compute Finance Research", `appOUiIsVbbm7MQ29`) into a **new, clean base** with the agreed 4-table relational schema. Use the existing base as the **input** (raw material to port from). **Do not modify the old base** — keep it as backup/reference.

The agent-intake workflow and dashboards are **deferred** to a later phase.

## Guiding principles
1. **Context lives in files, not chat.** Every decision is captured in this `/workspace/migration/` folder so any agent/session can load only what it needs.
2. **Tiered models.** Top-tier reasoning for design/judgment/entity-resolution; cheaper/faster models for mechanical execution against a precise spec; scripts (no model) for deterministic data prep.
3. **Old base preserved.** Nothing is deleted from the old base until the new one is verified.
4. **Human review checkpoints** between phases.

## Target schema (summary — full detail in `01_schema.md`)
Four tables, linked:
- **Articles** — Title, Key Takeaways, Date Published, URL, Type, Publisher (text), Author(s)→People, Companies Mentioned→Companies, Themes→(multi)
- **People** — Name, Current Title, Role (select, no "Author"), Primary Company→Companies, LinkedIn, X, Notes
- **Companies** — Name, Description, Primary Focus, Company Type (multi-select), Website, LinkedIn, X, Backers (free text), People→People, Articles (auto), Themes (multi), Tags (multi)
- **Themes** — Theme Name, Description, Articles (auto), Companies (auto)

No: geography, status, funding fields, My Take, My Thesis, Source-Org-as-company, Investors link, junction tables.

## The 4 themes (full mapping in `02_theme_mapping.md`)
1. **Physical Supply & Infrastructure** — chips, memory, power, datacenters, supply, buildout
2. **Compute Quality & Measurement** — silicon lottery, variance, performance benchmarking
3. **Pricing, Markets & Derivatives** — price indices, forward curves, derivatives, exchanges, market structure, asset-class framework
4. **Capital & Risk** — GPU-backed lending, residual value, backstops, valuation, financing

Tags (not themes): Regulation, DePIN/Crypto, Orchestration (company type).

## Phases
| # | Phase | Produces | Model tier |
|---|---|---|---|
| 0 | Spec files | this folder | top-tier (design) |
| 1 | Theme mapping | `02_theme_mapping.md` | top-tier (judgment) |
| 2 | Field/cleanup mapping | `03_field_mapping.md`, `04_people_companies_cleanup.md` | top-tier (judgment) |
| 3 | Data prep | `data/articles.json`, `people.json`, `companies.json`, `themes.json` (cleaned, ready to load) | script / cheap |
| 4 | Create new base + tables + fields | new Airtable base ID | needs Zapier MCP access |
| 5 | Load People + Companies | populated records | needs Zapier MCP access |
| 6 | Load + re-tag Articles (with links) | populated, linked articles | needs Zapier MCP access |
| 7 | Verify integrity; archive old | verification report | top-tier (review) |
| 8 | (Deferred) Agent intake + dashboards | — | later |

## Data quality of the existing base (baseline)
- Articles content: ~75% (titles, takeaways, dates, URLs good; Source-Org and Key-Data-Points fields misused)
- Companies: ~55% (identity fine; Investors links to Topics, People holds Twitter handles, funding mostly Unknown)
- People: ~35% (names + article links only; roles wrong, socials messy, 0% linked to companies)
- Topics content: ~80% reusable as prose; structure replaced (10→4)
- Overall as a relational map: ~55%. Content capture is the expensive part and is mostly done; the cheap part (re-linking, re-tagging, field fixes) is what's left.

## File index
- `00_plan.md` — this file (master plan)
- `01_schema.md` — exact 4-table schema (fields, types, select options, link directions) — TODO
- `02_theme_mapping.md` — 4 themes + 19-article assignment + old-topic→new-theme mapping — TODO
- `03_field_mapping.md` — old field → new field, with cleanup rules — TODO
- `04_people_companies_cleanup.md` — per-record fixes (roles, titles, company links, Backers) — TODO
- `data/*.json` — cleaned records ready to load — TODO
- `05_execution_log.md` — what was done, for audit — TODO

## Open questions for the user
1. New base name: "Compute Finance Research v2" — OK?
2. Confirm: defer intake + dashboards (phase 8) until migration is verified — OK?
3. Should delegated sub-agents be used for file-based data prep (phase 3), with Airtable writes (phases 4–6) kept in this session? (Pending verification of sub-agent MCP access.)
