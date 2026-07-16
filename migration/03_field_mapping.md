# Field Mapping — Old → New (with cleanup rules)

## Articles
| Old field | New field | Rule |
|---|---|---|
| Title | Title | direct copy |
| Key Takeaways | Key Takeaways | direct copy (keep 3-bullet + description) |
| Date Published | Date Published | direct copy (normalize to date type) |
| URL | URL | direct copy |
| Type | Type | map to new select |
| Source Organization (linked, holds "Global"/"Asia"/"Americas") | Publisher (free text) | DERIVE from URL domain/known publisher: semianalysis.com→"SemiAnalysis"; silicondata.com→"Silicon Data"; vaneck.com→"VanEck"; apollo.com→"Apollo"; substack.com→"Substack"; x.com→"X"; anagram.xyz→"Anagram". Drop geography values. |
| Author(s) (link) | Author(s) (link → People) | re-link to new People (find-or-create by name) |
| Related Companies (link) | Companies Mentioned (link → Companies) | re-link to new Companies (find-or-create by name) |
| Related Topics (link) | Themes (link → Themes) | RE-TAG to new 4 themes per 02_theme_mapping.md (do NOT carry old topic links) |
| Key Data Points (holds topic names) | DROP | misused; themes now handled by Themes link |
| My Take | DROP | deferred |
| Geography | DROP | |
| Status | DROP | |
| Read Status | DROP | |
| Date Read | DROP | |

## People
| Old field | New field | Rule |
|---|---|---|
| Name | Name | direct copy |
| Role (holds "Author"/"Researcher, Author") | Role (select) | REWRITE: remove "Author"; set professional role per 04 cleanup |
| (none) | Current Title | ADD: e.g. "Founder & CEO" where known |
| (none) | Primary Company (link → Companies) | ADD: link to company where known (currently 0% populated) |
| LinkedIn (sometimes two URLs in one cell) | LinkedIn | SPLIT: one URL per person; assign each URL to the correct person |
| Twitter | X (Twitter) | same split rule |
| Notes | Notes | keep; move any URLs in Notes into LinkedIn/X fields |
| Articles (auto-reverse) | Articles Authored (auto) | automatic |

## Companies
| Old field | New field | Rule |
|---|---|---|
| Company Name | Company Name | direct copy |
| Description | Description | direct copy |
| Primary Focus | Primary Focus | direct copy |
| Company Type (multi) | Company Type (multi) | map to new select; allow multi (NVIDIA = Chipmaker + Investor/VC) |
| Website | Website | direct copy |
| LinkedIn | LinkedIn | direct copy |
| Twitter | X (Twitter) | direct copy |
| Investors (link to Topics — BROKEN) | Backers (free text) | REPLACE: fill from known funding data (Ornn→"a16z ($33M seed)"; Silicon Data→"DRW, Jump Trading ($4.7M seed)"; SF Compute→"NVIDIA, Roboflow, Datology, Liquid AI, MIT"). Drop the broken link. |
| People (holds Twitter handles — BROKEN) | People (link → People) | RE-LINK: replace Twitter handles with real Person records (Architect→Brett Harrison; SemiAnalysis→Dylan Patel et al.; Silicon Data→Carmen Li, Platon Slynko + co-authors) |
| Articles (auto) | Articles (auto) | automatic |
| Articles 2 (duplicate) | DROP | duplicate |
| Tags (multi) | Tags (multi) | keep; add Regulation/DePIN/Orchestration as needed |
| Status | DROP | |
| Funding Raised | DROP | deferred; deal facts → Backers text or future junction table |
| Geography | DROP | |

## Themes (from old Topics)
| Old field | New field | Rule |
|---|---|---|
| Topic Name | Theme Name | new 4 names |
| Description | Description | port/refine from old topic descriptions |
| My Thesis | DROP | deferred |
| Type (Gap/Trend/Established) | DROP | nascent market, speculative |
| Articles (link) | Articles (auto) | re-tag per 02 |
| Companies (link) | Companies (auto) | re-link per themes |
| Related Articles (text) | DROP | redundant |
| Related Companies (text) | DROP | redundant |

## Link recreation approach
Linked records can't be copied directly between bases. Sequence:
1. Create People and Companies first (with names + cleaned fields).
2. Create Articles; link Author(s) and Companies Mentioned by matching names to the created People/Companies.
3. Create Themes; then set Themes on Articles/Companies per 02.
4. Entity resolution: exact name match first; fuzzy match with human confirm for ambiguous cases.

## Publisher derivation table (for Articles)
| URL domain | Publisher text |
|---|---|
| newsletter.semianalysis.com / semianalysis.com | SemiAnalysis |
| silicondata.com | Silicon Data |
| vaneck.com | VanEck |
| apollo.com | Apollo |
| anagram.xyz / blog.anagram.xyz | Anagram |
| *.substack.com / substack.com | Substack (or the specific substack name) |
| x.com / twitter.com | X |
| Other | derive from domain; else leave blank |
