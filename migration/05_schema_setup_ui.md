# Schema Setup Guide — Airtable UI

## Why this is manual
Autonomous base/schema creation via Zapier failed (Airtable returned HTTP 500 on base creation — the Zapier Airtable connection lacks the `schema.bases:write` scope needed to create bases/tables/fields). It can read and create **records**, but not create **schema**. So the schema is created manually in the Airtable UI (~15 min). Once the schema exists, the agent loads ALL records + links via Zapier.

## Step 1 — Create the base
- In Airtable, in the **"Compute Finance Research"** workspace, click **Add base → Start from scratch**.
- Name it: **Compute Finance Research v2**

## Step 2 — Create 4 tables
Rename the default table to **Articles**, then add three more tables: **People**, **Companies**, **Themes**. Delete any extra default tables.

## Step 3 — Add fields to each table
The first field is the primary field (keep it as single line text).

### Articles
| Field | Type | Options |
|---|---|---|
| Title | Single line text | (primary) |
| Key Takeaways | Long text | |
| Date Published | Date | ISO (YYYY-MM-DD) |
| URL | URL | |
| Type | Single select | Research Paper · Industry Analysis · Blog Post · Newsletter · Social Media Thread · Podcast · Other |
| Publisher | Single line text | |
| Author(s) | Link to another record → People | allow multiple |
| Companies Mentioned | Link to another record → Companies | allow multiple |
| Themes | Link to another record → Themes | allow multiple |

### People
| Field | Type | Options |
|---|---|---|
| Name | Single line text | (primary) |
| Current Title | Single line text | |
| Role | Single select | Founder · CEO · Executive · Analyst · Researcher · Investor · Journalist · Engineer · Independent |
| Primary Company | Link to another record → Companies | single (do NOT allow multiple) |
| LinkedIn | URL | |
| X (Twitter) | URL | |
| Notes | Long text | |

### Companies
| Field | Type | Options |
|---|---|---|
| Company Name | Single line text | (primary) |
| Description | Long text | |
| Primary Focus | Single line text | |
| Company Type | Multiple select | Index Provider · Exchange · Neocloud/GPU Provider · Marketplace/Comparison · Research Firm · Investor/VC · Chipmaker · Broker · Lender · Clearinghouse · Orchestration · DePIN |
| Website | URL | |
| LinkedIn | URL | |
| X (Twitter) | URL | |
| Backers | Single line text | |
| People | Link to another record → People | (Airtable auto-creates this as the reverse of People.Primary Company — use that one) |
| Articles | Link to another record → Articles | (auto-created reverse of Articles.Companies Mentioned — rename it to "Articles") |
| Themes | Link to another record → Themes | allow multiple |
| Tags | Multiple select | Regulation · DePIN/Crypto · Orchestration · Settlement · Benchmarking · Forward Curve · Silicon Lottery |

### Themes
| Field | Type | Options |
|---|---|---|
| Theme Name | Single line text | (primary) |
| Description | Long text | |
| Articles | Link to another record → Articles | (auto-created reverse of Articles.Themes — rename to "Articles") |
| Companies | Link to another record → Companies | (auto-created reverse of Companies.Themes — rename to "Companies") |

## Notes on link fields
- When you create a link field, **Airtable auto-creates a reverse field** on the target table. Create each relationship **once** (in the direction listed above) and let Airtable make the reverse.
- Rename any auto-created reverse field to match the names in this guide.
- The 5 relationships:
  1. Articles ↔ People (create "Author(s)" on Articles → People)
  2. Articles ↔ Companies (create "Companies Mentioned" on Articles → Companies)
  3. Articles ↔ Themes (create "Themes" on Articles → Themes)
  4. People ↔ Companies (create "Primary Company" on People → Companies)
  5. Companies ↔ Themes (create "Themes" on Companies → Themes)

## Step 4 — Share the new base ID
After creating the schema, copy the new base ID from the URL (it looks like `appXXXXXXXXXXXXX`) and share it with the agent. The agent will then load all records + links via Zapier.
