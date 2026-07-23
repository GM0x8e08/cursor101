# Execution Log — Compute Finance Research v2 Migration

## Status: COMPLETE

## What was done

### Schema (built in new base "Compute Finance Research v2", `appRmtDLFtJwdhLiL`)
- 4 tables: Themes (`tblLrxaMXMzdtjFCn`), Articles (`tblhE20tDTpCb5ekz`), People (`tblCvQBStXqDtRq0v`), Companies (`tblSb9Uy6y03AxeOZ`)
- All non-link fields including singleSelects (Articles.Type with 7 options, People.Role with 9 options)
- 5 linked-record relationships (multipleRecordLinks) with auto-created reverse fields (Themes.Articles, Themes.Companies, People.Articles, Companies.Articles, Companies.People)
- Default "Table 1" deleted
- Built via Airtable Metadata API through Zapier's raw request action (Content-Type: application/json header required)

### Data loaded
- **4 Themes** — Physical Supply & Infrastructure, Compute Quality & Measurement, Pricing Markets & Derivatives, Capital & Risk
- **23 Companies** — pure investors (a16z, DRW, Jump Trading) dropped as rows → kept as Backers text; Company Type & Tags stored as comma-separated text; Themes linked
- **26 People** — roles cleaned ("Author" removed); 21 linked to Primary Company; socials split/normalized; Current Title set where known (e.g., Brett Harrison → Founder & CEO at Architect; Carmen Li → Founder & CEO at Silicon Data)
- **19 Articles** — Publisher derived from URL; Author(s)/Companies Mentioned/Themes linked; multi-theme bridges where applicable (e.g., "Compute is the Commodity" → Pricing + Capital)

### Verification
- Raw API GET confirms links populated with valid record IDs:
  - "Semi-Fungible Assets" → Author recCWMMwRhWFonwSc (Theodora Diamandis), Theme recL8qNIY2DXgYOkt (Pricing)
  - "Conor Moore post" → Author recVR0RNMDftTkPRu (Conor Moore), Theme recL8qNIY2DXgYOkt (Pricing)
- Forward links verified on Articles and People; reverse links auto-populated by Airtable.
- Note: Zapier's `get_all_records` action mis-reports link counts as 0 in its summarized output — use raw API GET for accurate link verification.

## Deviations from original spec (Airtable API limitations via Zapier)
1. **Company Type & Tags** = single-line text (comma-separated), NOT multiSelect — `multiSelect` field creation was rejected by the API. Data preserved; upgradeable to multi-select in the Airtable UI (Airtable parses comma-separated values into options on field-type conversion).
2. **Primary Company** on People = `multipleRecordLinks` (holds one value), not `singleRecordLinks` — `singleRecordLinks` creation was rejected. Functionally identical for a single value.
3. Pure investors (a16z, DRW, Jump Trading) dropped as company rows → appear only in Backers text fields.
4. United Compute reclassified to Marketplace/Comparison (from Research Firm).
5. Arena AI kept as a Company (LLM-eval provider).

## Old base preserved
Old base "Compute Finance Research" (`appOUiIsVbbm7MQ29`) is untouched and kept as backup/reference.

## Files produced (in /workspace/migration/)
- Specs: 00_plan.md, 01_schema.md, 02_theme_mapping.md, 03_field_mapping.md, 04_people_companies_cleanup.md, 05_schema_setup_ui.md, 05_execution_log.md
- Scripts: build_load_data.py, resolve_people.py, resolve_articles.py
- Data: data/companies.json, people.json, articles.json, company_ids.json, people_ids.json, load_*.json batches

## Next steps (deferred — phase 8)
- Agent intake workflow (article URL → structured extraction → Airtable write with find-or-create entity resolution)
- Airtable Interfaces dashboards (Company profile, Theme overview, Article gallery, People directory)
- Optional polish: convert Company Type & Tags to multi-select in UI; add Investments junction table if deal metadata needed; add My Thesis to Themes when ready; enrich Companies Mentioned on articles (currently only the clearly-mentioned ones were ported).

---

## Post-migration data-quality fixes (Jul 2026)

### Fixes applied via Airtable API (Zapier raw request PATCH)
1. **Ornn** (`rec9RlxWgNGahkbLN`) — Company Type changed from `["Index Provider","Exchange","Marketplace"]` to `["Index Provider","Exchange","Marketplace/Comparison"]`. Removes use of the duplicate bare "Marketplace" option.
2. **Article: "Nvidia GPU Debt Backstop…"** (`recKp5lxhgZdXNX3j`) — Author(s) set to `["rec0axVfRmtwoh7RA"]` (Daniel Nishball). Verified via WebFetch of the SemiAnalysis URL (bylines: Daniel Nishball, Cheang Kang Wen, Zane Fong, +5; only Nishball is an existing Person record).
3. **Article: "Building a Robust GPU Index"** (`recenCmxFORQX6cJB`) — Author(s) set to `["recbryT7hWZk1US8S"]` (Carmen Li). Verified via WebFetch of the Silicon Data blog URL ("Written by Carmen Li, Founder at Silicon Data").
4. **Article: "Compute is the New Liquidity"** (`recrzon0VgP9JsfSR`) — Publisher changed from "LinkedIn" to "LinkedIn Pulse" (more specific; URL is a linkedin.com/pulse/… post by Perceptron Network).
5. **Person: Conor Moore** (`recVR0RNMDftTkPRu`) — Primary Company changed from `["rec5Yxf55YVJmpTB4","recJQOfq3fbahwADO"]` (Permian Labs + USD.AI) to `["rec5Yxf55YVJmpTB4"]` (Permian Labs only). He is COO & Co-Founder of Permian Labs; USD.AI is a product of Permian Labs, not a separate employer.
6. **Company Type field description** updated to "Company type classification (multi-select)".

### Fixes that require manual action in the Airtable UI (API blocked)
The Zapier connection's token lacks permission to create new select options, and the meta API PATCH for `options.choices` returns 422 via Zapier's raw request tool. Table deletion returns 404. The following must be done manually in the Airtable UI:

1. **Add 3 new Company Type options** (the user confirmed "DePIN" and "AI Lab"; "Insurance/Valuation" was in the original recommendation for Barkr):
   - `DePIN`
   - `AI Lab`
   - `Insurance/Valuation`
2. **Remove the bare `Marketplace` option** (id `seljWvjKH3GgIuH92`) from Company Type — no records use it anymore (Ornn was the only one, now updated to "Marketplace/Comparison").
3. **Delete "Table 1"** (`tbljJegqHucX5i5tc`) — the default empty table. API DELETE on the meta endpoint returns 404 via Zapier.
4. **Backfill Company Type on 5 companies** (after the new options are added):
   - DeepSeek (`recDMkyS2UyLtcnnC`) → `AI Lab`
   - xAI (`reciSPltuUfzNAPiw`) → `AI Lab`
   - Virtuals Protocol (`recLyjRFAlTYVrsoM`) → `DePIN`
   - Bittensor (`rectI7ASFWkyUSlNV`) → `DePIN`
   - Barkr (`recfCSq0KIUEiGOiK`) → `Insurance/Valuation`

### Explanations for user questions
- **Marketplace vs Marketplace/Comparison duplicate (point 3):** Two separate options existed in the Company Type field — bare "Marketplace" and "Marketplace/Comparison". Ornn was the only record using the bare one. Fix: Ornn updated to "Marketplace/Comparison"; the bare option should be manually removed from the field config.
- **Backfill company type (point 5):** 5 company records have no Company Type value because no existing option fits them (DeepSeek/xAI are AI labs; Virtuals Protocol/Bittensor are DePIN; Barkr is a valuation/insurance provider). The new options must be created first, then the records can be tagged.
- **@0xMetaLight stub (point 7):** Article `recHex4GaGfmXOoKk` ("Post by @0xMetaLight on Compute Markets") has placeholder Key Takeaways because the X/Twitter post could not be scraped (403 Forbidden from X). Options: re-attempt scraping later, replace with a manually-written summary, or delete the record if the source isn't valuable.
- **Poe Zhao / Hello China Tech (point 8):** Hello China Tech is NOT in the Companies table — it only appears as the Publisher (free text) of article `reckBhy0RFESHJMe0` ("Who Owns China's Token Factories?"). This is correct: publishers are free text, not linked company records. Poe Zhao (`recRtPR97AYjDi1ED`) is the author, with Role "Researcher". No action needed unless the user wants to reclassify him as "Journalist".
- **Mercatus author:** Mercatus articles (`recMDwrXJjIEQYxbO`, `recZ5hU4L2OsaAL4u`, `recm8hCWiTfFm7szk`) don't list individual authors on their website. Author(s) field is left empty for these — acceptable per the schema (Author is optional).
- **Mercatus title typo (point E):** Reviewed all 3 Mercatus article titles; no obvious typo found. Need user clarification on which title/field has the typo.
- **"Overview of the Energy Economy" publisher:** Article `reciDCQkTIXkhsldS` has a generic Substack URL (`substack.com/home/post/p-204196486`) that doesn't identify the specific publication. Publisher is "Substack" (generic) — can't be refined without accessing the article behind the redirect.
