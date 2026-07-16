# Schema — Compute Finance Research v2

Four tables, linked. No junction tables. No geography, status, funding fields, My Take, My Thesis.

## Articles
| Field | Type | Notes |
|---|---|---|
| Title | Single line text | |
| Key Takeaways | Long text | 3 bullet points + description (keep current format) |
| Date Published | Date | |
| URL | URL | |
| Type | Single select | Research Paper · Industry Analysis · Blog Post · Newsletter · Social Media Thread · Podcast · Other |
| Publisher | Single line text (free text) | e.g. "SemiAnalysis", "Substack", "X", "Bloomberg". Replaces the linked Source Organization. |
| Author(s) | Link → People (multi) | |
| Companies Mentioned | Link → Companies (multi) | who the article is about |
| Themes | Link → Themes (multi) | 1–4 of the 4 themes |

Dropped from old: Source Organization (linked) → Publisher (text); Key Data Points (misused); My Take; Geography; Status; Read Status; Date Read.

## People
| Field | Type | Notes |
|---|---|---|
| Name | Single line text | |
| Current Title | Single line text | e.g. "Founder & CEO", "Lead Analyst" |
| Role | Single select | Founder · CEO · Executive · Analyst · Researcher · Investor · Journalist · Engineer · Independent. **No "Author".** |
| Primary Company | Link → Companies (single) | where they work now |
| LinkedIn | URL | one URL only (split double-URL cells) |
| X (Twitter) | URL | one URL only |
| Notes | Long text | optional |
| Articles Authored | Link → Articles (auto-reverse) | |

Dropped from old: Role "Author" value; double-URL socials (split).

## Companies
| Field | Type | Notes |
|---|---|---|
| Company Name | Single line text | |
| Description | Long text | |
| Primary Focus | Single line text | one-line tagline |
| Company Type | Multi select | Index Provider · Exchange · Neocloud/GPU Provider · Marketplace/Comparison · Research Firm · Investor/VC · Chipmaker · Broker · Lender · Clearinghouse · Orchestration · DePIN |
| Website | URL | |
| LinkedIn | URL | |
| X (Twitter) | URL | |
| Backers | Single line text (free text) | e.g. "a16z ($33M seed)". Replaces the Investors link. |
| People | Link → People (multi) | team/leaders (real Person records, not Twitter handles) |
| Articles | Link → Articles (auto-reverse) | |
| Themes | Link → Themes (multi) | |
| Tags | Multi select | Regulation · DePIN/Crypto · Orchestration · Settlement · Benchmarking · Forward Curve · Silicon Lottery (open set) |

Dropped from old: Status; Funding Raised; Funding Stage; Last Round Date; Founded Year; Geography; Headcount; Investors (link) → Backers (text); Articles 2 (duplicate); People field holding Twitter handles → repoint to real People.

## Themes
| Field | Type | Notes |
|---|---|---|
| Theme Name | Single line text | |
| Description | Long text | |
| Articles | Link → Articles (auto-reverse) | |
| Companies | Link → Companies (auto-reverse) | |

Dropped from old: My Thesis (deferred); Type/Gap-Trend-Established (nascent market, speculative); Layer (redundant — the 4 themes ARE the layers); Related Articles/Companies (text, redundant).

## Controlled vocabularies (select options)
- **Article Type:** Research Paper, Industry Analysis, Blog Post, Newsletter, Social Media Thread, Podcast, Other
- **Person Role:** Founder, CEO, Executive, Analyst, Researcher, Investor, Journalist, Engineer, Independent
- **Company Type:** Index Provider, Exchange, Neocloud/GPU Provider, Marketplace/Comparison, Research Firm, Investor/VC, Chipmaker, Broker, Lender, Clearinghouse, Orchestration, DePIN
- **Tags:** Regulation, DePIN/Crypto, Orchestration, Settlement, Benchmarking, Forward Curve, Silicon Lottery (open set — add as needed)

## Build notes (actual schema as created in Airtable)
- Base: "Compute Finance Research v2" (`appRmtDLFtJwdhLiL`)
- Table IDs: Themes `tblLrxaMXMzdtjFCn` · Articles `tblhE20tDTpCb5ekz` · People `tblCvQBStXqDtRq0v` · Companies `tblSb9Uy6y03AxeOZ`

Deviations from the original spec (due to Airtable API limitations via Zapier's raw request):
1. **Company Type** and **Tags** on Companies are **single-line text** (comma-separated values), NOT multi-select. Airtable's API rejected `multiSelect` field creation via this path (even minimal). Data stored as comma-separated strings (e.g. "Chipmaker, Investor/VC"). Upgradeable to multi-select in the Airtable UI in two clicks (Airtable parses existing values into options on field-type conversion).
2. **Primary Company** on People is `multipleRecordLinks` (holds one value), not single — Airtable's API rejected `singleRecordLinks` creation. Functionally identical for a single value.
3. All 5 relationships are wired with forward + auto-created reverse fields. Reverse field names: Themes.Articles, Themes.Companies, People.Articles, Companies.Articles, Companies.People.
4. Select fields that worked: `singleSelect` (Articles.Type with 7 options, People.Role with 9 options) — all options retained.
5. Default "Table 1" — deletion pending (cleanup).
