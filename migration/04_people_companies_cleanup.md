# Per-Record Cleanup — People & Companies

## People (26 → cleanup)

Rules: remove "Author" from Role; set professional Role + Current Title + Primary Company where known; split double-URL socials; move URLs out of Notes.

| Name | New Role | Current Title | Primary Company | LinkedIn | X | Notes |
|---|---|---|---|---|---|---|
| Brett Harrison | Founder | Founder & CEO | Architect | (find) | @BrettHarrison | |
| Carmen Li | Founder | Founder & CEO | Silicon Data | (find) | (find) | Founder of Silicon Data |
| Dylan Patel | Researcher | Lead Analyst | SemiAnalysis | /in/dylan-patel-semianalysis | @dylan522p | |
| Daniel Nishball | Researcher | Analyst | SemiAnalysis | FIX (currently Dylan's) | FIX (currently Dylan's) | |
| Ray Wang | Researcher | Analyst | SemiAnalysis | (find) | (find) | |
| Myron Xie | Researcher | Analyst | SemiAnalysis | (find) | (find) | |
| Theodora Diamandis | Researcher | Researcher | Anagram | /in/theodora-diamandis | | |
| Platon Slynko | Researcher | Researcher | Silicon Data | (find) | (find) | |
| Jason Cornick | Researcher | | Silicon Data | | | GPU Cloud Lottery co-author |
| Benjamin Cornick | Researcher | | Silicon Data | | | |
| Jay Lu | Researcher | | Silicon Data | | | |
| Laksh Sharma | Researcher | | Silicon Data | | | |
| Shou-Kai Cheng | Researcher | | Silicon Data | | | |
| Arthur O. Dias dos Santos | Researcher | | Silicon Data | | | |
| Caique Sobral | Researcher | | Silicon Data | | | |
| Daoxuan Xu | Researcher | | Silicon Data | | | |
| Xinxin Mei | Researcher | | Silicon Data | | | |
| Yifan Sun | Researcher | | Silicon Data | | | |
| Matthew Sigel | Analyst | Head of Digital Assets Research | VanEck | (find) | (find) | currently "Unknown" — fill |
| Caleb Shack | Investor | Investor | Variant Fund | /in/caleb-shack | @firstc0in | SPLIT from Alana's shared cell |
| Alana Levin | Investor | Investor | Variant Fund | /in/alana-levin | @AlanaDLevin | SPLIT from Caleb's shared cell |
| Ronit Jain | Independent | | | /in/ronitjain | | |
| Dave Friedman | Independent | | | /in/dave-friedman-5b5b5b5b | @frieddave | |
| Conor Moore | Independent | | | | @_ConorMoore | |
| 0xturbanurban | Independent | | | | @0xturbanurban | |
| 0xMetaLight | Independent | | | | @0xMetaLight | |

"Independent" = no tracked company (independent writer/commenter). "(find)" = value not in current data; to be looked up during cleanup or left blank.

## Companies (26 → ~23)

### Decision point: drop pure-investor companies
Per the "Backers as free text, no investor-entity bloat" principle, **drop pure investors that have no authors and no captured articles**:
- **DROP:** Andreessen Horowitz (a16z), DRW, Jump Trading Group. They appear only as Backers text.
- **KEEP** investors that are employers of authors or publishers of captured content: Variant Fund (employs Caleb/Alana), VanEck (employs Sigel), Apollo (published Growing Compute Shortage). Tag them Investor/VC.

### Company cleanup table
| Company | Company Type | Backers (text) | People (links) | Notes |
|---|---|---|---|---|
| Ornn | Index Provider, Exchange, Marketplace | a16z ($33M seed) | (none yet) | ICE futures partnership |
| Silicon Data | Index Provider | DRW, Jump Trading ($4.7M seed) | Carmen Li, Platon Slynko (+ co-authors) | |
| SF Compute | Neocloud/GPU Provider | NVIDIA, Roboflow, Datology, Liquid AI, MIT | (none yet) | |
| NVIDIA | Chipmaker, Investor/VC | (public) | (none) | |
| Architect | Exchange | (unknown) | Brett Harrison | |
| SemiAnalysis | Research Firm | (unknown) | Dylan Patel, Daniel Nishball, Ray Wang, Myron Xie | |
| Anagram | Research Firm | (unknown) | Theodora Diamandis | |
| Variant Fund | Investor/VC | (unknown) | Caleb Shack, Alana Levin | |
| VanEck | Investor/VC | (public) | Matthew Sigel | |
| Apollo Global Management | Investor/VC, Research Firm | (public) | (none) | published Growing Compute Shortage |
| GPU Lease Index (GLRI) | Index Provider | (unknown) | (none) | |
| Axon Index | Index Provider | (unknown) | (none) | |
| Anera Markets | Clearinghouse, Index Provider | (unknown) | (none) | |
| BitOoda | Broker | (unknown) | (none) | |
| NativX | Exchange | (unknown) | (none) | |
| Thunder Compute | Neocloud/GPU Provider, Orchestration | (unknown) | (none) | |
| Exascale Labs | Neocloud/GPU Provider | (unknown) | (none) | |
| GetDeploying | Marketplace/Comparison, Orchestration | (unknown) | (none) | |
| CloudPrice | Marketplace/Comparison | (unknown) | (none) | |
| AI Multiple | Research Firm | (unknown) | (none) | |
| United Compute | Marketplace/Comparison | (unknown) | (none) | reclassified from Research Firm |
| Arena AI | Research Firm | (unknown) | (none) | LLM eval — may not fit; see decision point |
| Compute Desk | Index Provider | (unknown) | (none) | |

### Resolved decisions
1. **Drop pure investors (a16z, DRW, Jump)** → Backers text only. ✅ Confirmed.
2. **Arena AI** → KEEP as a Company (LLM-eval provider; relevant company in the space). ✅ Confirmed.
3. **AI Multiple** → KEEP as Research Firm. **United Compute** → KEEP, reclassify Company Type to Marketplace/Comparison (it's a "free aggregator of compute pricing," not a research firm in the SemiAnalysis sense). ✅ Resolved.
4. **New base name** → "Compute Finance Research v2". ✅ Confirmed.
