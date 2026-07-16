#!/usr/bin/env python3
"""Build load-ready JSON for the Compute Finance Research v2 Airtable base.

Outputs:
  data/companies.json  - 23 companies (pure investors a16z/DRW/Jump dropped -> Backers text only)
  data/people.json     - 26 people (cleaned roles/titles/primary-company by name)
  data/articles.json   - 19 articles (publisher derived, themes mapped, authors/companies by name)

Cross-table links are stored as NAME references here; resolved to record IDs during loading
(after each target table is created). Themes are already loaded -> theme IDs embedded.

Run: python3 build_load_data.py
"""
import json, os

OUT = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(OUT, exist_ok=True)

# Theme record IDs (already created in v2 base)
THEME = {
    "Physical": "recaVy3RP4F3pkout",
    "Quality": "recbeTp4pOiPyKZsT",
    "Pricing": "recL8qNIY2DXgYOkt",
    "Capital": "rechjPrNupEz4Fvty",
}

def x(handle):
    """Normalize a Twitter handle to an x.com URL. Returns None if empty."""
    if not handle or handle in ("Unknown", "unknown"):
        return None
    h = handle.strip().lstrip("@")
    if h.startswith("http"):
        return h
    return f"https://x.com/{h}" if h else None

# ---------------- COMPANIES (23; dropped a16z, DRW, Jump) ----------------
COMPANIES = [
    {"name": "Ornn", "type": "Index Provider, Exchange, Marketplace", "focus": "Compute Price Index",
     "desc": "Financial products for compute. Provides compute access (Ornn Compute), market measurement data (Ornn Data), and the OCPI (Ornn Compute Price Index) - a reference price for compute. Aims to make compute a priceable, financeable, and hedgeable commodity.",
     "web": "https://ornn.ai", "li": None, "x": None, "backers": "a16z ($33M seed)",
     "tags": "", "themes": [THEME["Pricing"]]},
    {"name": "Silicon Data", "type": "Index Provider", "focus": "GPU Market Data & Analytics",
     "desc": "Compute market intelligence platform providing real-time GPU price transparency, performance data, and standardized indexing for traders, financial institutions, and builders. Products include SiliconNavigator, SiliconMark, SiliconIndex, and SiliconPriceIQ.",
     "web": "https://silicondata.com", "li": "https://www.linkedin.com/company/silicon-data", "x": None,
     "backers": "DRW, Jump Trading ($4.7M seed)", "tags": "", "themes": [THEME["Quality"], THEME["Pricing"]]},
    {"name": "SF Compute", "type": "Neocloud/GPU Provider", "focus": "GPU Cloud Provider",
     "desc": "GPU cloud provider offering H100 and H200 compute at competitive prices. Provides on-demand GPU access with flexible contracts.",
     "web": "https://sfcompute.com/", "li": "https://www.linkedin.com/company/sf-compute/", "x": x("@sfcompute"),
     "backers": "NVIDIA, Roboflow, Datology, Liquid AI, MIT", "tags": "", "themes": [THEME["Physical"]]},
    {"name": "NVIDIA", "type": "Chipmaker, Investor/VC", "focus": "GPU Manufacturing",
     "desc": "GPU chip manufacturer. Backstop provider for neocloud debt.",
     "web": "https://nvidia.com", "li": None, "x": None, "backers": "", "tags": "",
     "themes": [THEME["Physical"], THEME["Capital"]]},
    {"name": "Architect", "type": "Exchange", "focus": "GPU Futures & Options Trading",
     "desc": "Compute derivatives exchange offering futures and options on GPU rental prices, including H100, H200, B200, B300 contracts. Enables hedging and speculation on compute prices.",
     "web": "https://architect.co/", "li": None, "x": None, "backers": "", "tags": "Derivatives & Trading",
     "themes": [THEME["Pricing"]]},
    {"name": "SemiAnalysis", "type": "Research Firm", "focus": "AI Infrastructure Research",
     "desc": "Research and advisory firm bridging semiconductors and business. Provides industry models (Accelerator, AI Cloud TCO, Datacenter), market intelligence, and consulting on AI compute infrastructure.",
     "web": "https://semianalysis.com", "li": "https://www.linkedin.com/company/semianalysis", "x": x("https://x.com/semianalysis1"),
     "backers": "", "tags": "", "themes": []},
    {"name": "Anagram", "type": "Research Firm", "focus": "Crypto Research",
     "desc": "Crypto research firm. Published semi-fungible compute assets paper.",
     "web": "https://anagram.xyz", "li": None, "x": None, "backers": "", "tags": "", "themes": []},
    {"name": "Variant Fund", "type": "Investor/VC", "focus": "Crypto Venture Capital",
     "desc": "Crypto venture fund. Published compute markets framework.",
     "web": "https://variant.fund", "li": None, "x": None, "backers": "", "tags": "", "themes": []},
    {"name": "VanEck", "type": "Investor/VC", "focus": "Asset Management",
     "desc": "Asset manager. Published framework for valuing bitcoin miners as AI infrastructure.",
     "web": "https://vaneck.com", "li": None, "x": None, "backers": "", "tags": "", "themes": [THEME["Capital"]]},
    {"name": "Apollo Global Management", "type": "Investor/VC", "focus": "Alternative Investments",
     "desc": "Alternative asset manager. Published on compute shortage.",
     "web": "https://apollo.com", "li": None, "x": None, "backers": "", "tags": "",
     "themes": [THEME["Physical"]]},
    {"name": "GPU Lease Index (GLRI)", "type": "Index Provider", "focus": "Cloud Pricing Comparison",
     "desc": "Provides bankable Time-to-Power intelligence and GPU lease pricing data. Offers market scorecards for datacenter sites (Texas, Georgia, Carolinas, Ohio/PJM) and speed-to-power watchlists.",
     "web": "https://gpuleaseindex.com", "li": None, "x": None, "backers": "",
     "tags": "Pricing & Indices, Derivatives & Trading", "themes": [THEME["Pricing"]]},
    {"name": "Axon Index", "type": "Index Provider", "focus": "GPU Pricing Benchmarks",
     "desc": "Settlement-grade GPU pricing index provider, offering standardized benchmarks for GPU rental pricing. Provides transparent, reliable pricing data for the compute market.",
     "web": "https://axonindex.com/", "li": "https://www.linkedin.com/company/axonindex/", "x": x("@AxonIndex"),
     "backers": "", "tags": "Pricing & Indices, Benchmarking, Settlement & Clearing", "themes": [THEME["Pricing"]]},
    {"name": "Anera Markets", "type": "Clearinghouse", "focus": "AI Risk Indices & Clearing",
     "desc": "Clearinghouse for AI risk, providing indices and financial products for managing AI market risks. Specializes in risk management for the AI and compute economy.",
     "web": "https://anera.markets/", "li": None, "x": None, "backers": "",
     "tags": "Pricing & Indices, Settlement & Clearing, Derivatives & Trading", "themes": [THEME["Capital"], THEME["Pricing"]]},
    {"name": "BitOoda", "type": "Broker", "focus": "Compute Brokerage & Market Infrastructure",
     "desc": "AI-native, agency-first brokerage and market infrastructure platform connecting compute, power, infrastructure, and capital into standardized markets.",
     "web": "https://bitooda.io/", "li": None, "x": None, "backers": "", "tags": "Brokerage",
     "themes": [THEME["Pricing"]]},
    {"name": "NativX", "type": "Exchange", "focus": "Compute Exchange Infrastructure",
     "desc": "Exchange infrastructure for compute, providing trading and settlement systems for GPU compute markets. Enables transparent pricing and trading of compute resources.",
     "web": "https://www.nativx.net/", "li": None, "x": None, "backers": "", "tags": "Settlement & Clearing",
     "themes": [THEME["Pricing"]]},
    {"name": "Thunder Compute", "type": "Neocloud/GPU Provider, Orchestration", "focus": "Free Compute Aggregation",
     "desc": "Systems lab commercializing GPU virtualization to increase GPU utilization. Team from Citadel Securities, Aquatic, and AWS. Offers cloud services to create step-change improvements in data center capacity.",
     "web": "https://thundercompute.com", "li": "https://www.linkedin.com/company/thundercompute", "x": x("https://x.com/thundercompute"),
     "backers": "", "tags": "Pricing & Indices, Energy & Power", "themes": [THEME["Physical"]]},
    {"name": "Exascale Labs", "type": "Neocloud/GPU Provider", "focus": "Advanced GPU Infrastructure",
     "desc": "AI infrastructure provider offering next-generation compute hardware including GB200s, B200s, H100s, H200s, and RTX5090s. Provides high-performance computing solutions for AI workloads.",
     "web": "https://www.exascalelabs.ai/", "li": None, "x": None, "backers": "", "tags": "",
     "themes": [THEME["Physical"]]},
    {"name": "GetDeploying", "type": "Marketplace/Comparison, Orchestration", "focus": "Cloud Provider Comparison",
     "desc": "Cloud provider comparison platform helping users find and compare different cloud and GPU providers. Provides detailed pricing, specs, and feature comparisons.",
     "web": "https://getdeploying.com/", "li": None, "x": None, "backers": "", "tags": "Pricing & Indices",
     "themes": [THEME["Pricing"]]},
    {"name": "CloudPrice", "type": "Marketplace/Comparison", "focus": "GPU Virtualization",
     "desc": "Cloud pricing comparison tool for Azure, AWS EC2, and GCP instances. Provides comprehensive VM specification and pricing data across regions and payment options.",
     "web": "https://cloudprice.net", "li": None, "x": None, "backers": "",
     "tags": "Compute Access, Pricing & Indices, Market Intelligence", "themes": [THEME["Pricing"]]},
    {"name": "AI Multiple", "type": "Research Firm", "focus": "GPU Lease Pricing",
     "desc": "AI research and analysis platform covering use cases, tools, hardware, and market trends. Includes GPU pricing index and cloud GPU provider comparisons.",
     "web": "https://aimultiple.com", "li": "https://www.linkedin.com/company/aimultiple", "x": x("https://x.com/aimultipleai"),
     "backers": "", "tags": "", "themes": []},
    {"name": "United Compute", "type": "Marketplace/Comparison", "focus": "AI Tools & Hardware Analysis",
     "desc": "Free aggregator of compute pricing information. Status: Launching soon.",
     "web": "https://unitedcompute.com", "li": None, "x": None, "backers": "", "tags": "",
     "themes": [THEME["Pricing"]]},
    {"name": "Arena AI", "type": "Research Firm", "focus": "AI Model Rankings & LLM Evaluation",
     "desc": "Official AI ranking and LLM leaderboard platform for comparing and evaluating AI models. Provides comprehensive benchmarks and performance metrics for AI systems.",
     "web": "https://arena.ai/", "li": "https://www.linkedin.com/company/arenaai/", "x": x("@arena"),
     "backers": "", "tags": "Model Evaluation", "themes": [THEME["Quality"]]},
    {"name": "Compute Desk", "type": "Index Provider", "focus": "GPU Compute Pricing",
     "desc": "Independent third-party aggregator combining rental price offers and private transactions into single values representing the cost of compute per accelerator.",
     "web": "https://computedesk.com", "li": None, "x": None, "backers": "",
     "tags": "Market Intelligence, Pricing & Indices", "themes": [THEME["Pricing"]]},
]

companies_out = [{
    "fields": {
        "Company Name": c["name"],
        "Description": c["desc"],
        "Primary Focus": c["focus"],
        "Company Type": c["type"],
        "Website": c["web"],
        "LinkedIn": c["li"],
        "X (Twitter)": c["x"],
        "Backers": c["backers"],
        "Tags": c["tags"],
        "Themes": c["themes"],  # theme record IDs
    }
} for c in COMPANIES]

# ---------------- PEOPLE (26) ----------------
# primary_company = company NAME (resolved to ID after companies created)
PEOPLE = [
    ("Brett Harrison", "Founder", "Founder & CEO", "Architect", None, "@BrettHarrison"),
    ("Carmen Li", "Founder", "Founder & CEO", "Silicon Data", None, None),
    ("Dylan Patel", "Researcher", "Lead Analyst", "SemiAnalysis", "https://www.linkedin.com/in/dylan-patel-semianalysis", "https://x.com/dylan522p"),
    ("Daniel Nishball", "Researcher", "Analyst", "SemiAnalysis", None, None),
    ("Ray Wang", "Researcher", None, "SemiAnalysis", None, None),
    ("Myron Xie", "Researcher", None, "SemiAnalysis", None, None),
    ("Theodora Diamandis", "Researcher", None, "Anagram", "https://www.linkedin.com/in/theodora-diamandis", None),
    ("Platon Slynko", "Researcher", None, "Silicon Data", None, None),
    ("Jason Cornick", "Researcher", None, "Silicon Data", None, None),
    ("Benjamin Cornick", "Researcher", None, "Silicon Data", None, None),
    ("Jay Lu", "Researcher", None, "Silicon Data", None, None),
    ("Laksh Sharma", "Researcher", None, "Silicon Data", None, None),
    ("Shou-Kai Cheng", "Researcher", None, "Silicon Data", None, None),
    ("Arthur O. Dias dos Santos", "Researcher", None, "Silicon Data", None, None),
    ("Caique Sobral", "Researcher", None, "Silicon Data", None, None),
    ("Daoxuan Xu", "Researcher", None, "Silicon Data", None, None),
    ("Xinxin Mei", "Researcher", None, "Silicon Data", None, None),
    ("Yifan Sun", "Researcher", None, "Silicon Data", None, None),
    ("Matthew Sigel", "Analyst", "Head of Digital Assets Research", "VanEck", None, None),
    ("Caleb Shack", "Investor", None, "Variant Fund", "https://www.linkedin.com/in/caleb-shack", "https://x.com/firstc0in"),
    ("Alana Levin", "Investor", None, "Variant Fund", "https://www.linkedin.com/in/alana-levin", "https://x.com/AlanaDLevin"),
    ("Ronit Jain", "Independent", None, None, "https://www.linkedin.com/in/ronitjain", None),
    ("Dave Friedman", "Independent", None, None, "https://www.linkedin.com/in/dave-friedman-5b5b5b5b", "@frieddave"),
    ("Conor Moore", "Independent", None, None, None, "@_ConorMoore"),
    ("0xturbanurban", "Independent", None, None, None, "https://x.com/0xturbanurban"),
    ("0xMetaLight", "Independent", None, None, None, "@0xMetaLight"),
]

people_out = [{
    "fields": {
        "Name": n,
        "Current Title": title,
        "Role": role,
        "Primary Company": [company] if company else [],  # NAME ref -> resolved to [ID] at load
        "LinkedIn": li,
        "X (Twitter)": x(tw),
        "Notes": None,
    }
} for (n, role, title, company, li, tw) in PEOPLE]

# ---------------- ARTICLES (19) ----------------
# authors / companies_mentioned = NAME lists (resolved to IDs at load)
# publisher derived from URL; themes = theme IDs (primary + bridges)
def publisher(url):
    if not url:
        return None
    u = url.lower()
    if "semianalysis.com" in u:
        return "SemiAnalysis"
    if "silicondata.com" in u:
        return "Silicon Data"
    if "vaneck.com" in u:
        return "VanEck"
    if "apollo.com" in u:
        return "Apollo"
    if "anagram.xyz" in u:
        return "Anagram"
    if "substack.com" in u:
        return "Substack"
    if "x.com" in u or "twitter.com" in u:
        return "X"
    return None

# (title, type, date, url, takeaways, author_names, company_names, theme_ids)
ARTICLES = [
    ("Semi-Fungible Assets and the Future of Compute Markets", "Research Paper", "2025-01-01",
     "https://blog.anagram.xyz/semi-fungible-assets-and-the-future-of-compute-markets/",
     "• Compute is a semi-fungible asset with heterogeneous characteristics\n• Traditional financial derivatives frameworks can be applied to compute markets\n• Crypto enables programmable, composable compute asset trading\n\nExplores treating compute (GPU/CPU) as a semi-fungible tradable asset class. Discusses how crypto can enable spot/futures markets for compute resources, formal pricing frameworks for semi-fungible assets, and implications for AI agents consuming compute at scale. Published by Anagram.",
     ["Theodora Diamandis"], [], [THEME["Pricing"]]),
    ("Traditional Power Markets Are The Analog (Thread by @0xturbanurban)", "Blog Post", "2025-04-01",
     "https://x.com/0xturbanurban/status/2047159953157214715",
     "• Traditional power markets provide a template for compute derivatives\n• Electricity markets have capacity (rights) and energy (delivery) layers\n• Compute markets lack standardization but are moving toward it\n\nThread comparing compute markets to traditional commodity/power markets. Breaks compute into three layers (the chip as capital asset, GPU-hours as fungible rental, tokens as branded fuel). Argues token pricing across providers (OpenAI, Anthropic, Google) is non-comparable due to proprietary tokenizers and non-stationary value. Draws parallels to electricity capacity vs. energy layers as a template for compute derivatives.",
     ["0xturbanurban"], [], [THEME["Pricing"]]),
    ("100,000 H100 Clusters: Power, Network Topology, Ethernet vs InfiniBand, Reliability, Failures, Checkpointing",
     "Industry Analysis", "2024-06-17", "https://newsletter.semianalysis.com/p/100000-h100-clusters-power-network",
     "• 100K GPU clusters face significant power and reliability challenges\n• Memory checkpointing is critical for fault tolerance\n• Network topology (InfiniBand vs Ethernet) impacts cluster performance\n\nSemiAnalysis deep-dive (Jun 2024) on building 100K+ H100 GPU clusters for frontier model training. Covers power requirements (>150MW, 1.59 TWh/year), network topology (InfiniBand vs Ethernet), fault recovery through memory reconstruction, rack layouts, and checkpointing. Contextualizes the race between OpenAI/Microsoft, xAI, and Meta to build massive training clusters costing $4B+ in server capex each.",
     ["Dylan Patel", "Daniel Nishball"], [], [THEME["Physical"]]),
    ("China's CXMT Is Set to Challenge DRAM Incumbents", "Industry Analysis", "2026-06-23",
     "https://newsletter.semianalysis.com/p/chinas-cxmt-is-set-to-challenge-dram",
     "• CXMT is challenging DRAM incumbents with state backing\n• HBM demand is driving memory shortages\n• China's semiconductor ambitions are accelerating despite export controls\n\nSemiAnalysis deep-dive (Jun 2026) on CXMT ahead of its STAR Market IPO, potentially the largest semiconductor IPO in China. Covers CXMT's history since 2016, technology transfer from Micron, founder Zhu Yiming's background, process node deficit vs. Samsung/SK Hynix/Micron, China's HBM ambitions, and memory supply implications from AI-driven demand.",
     ["Ray Wang", "Myron Xie", "Dylan Patel"], [], [THEME["Physical"]]),
    ("The Commoditization of Compute: Why GPU Infrastructure Needs a Derivatives Market", "Blog Post",
     "2026-06-29", "https://ronitrjain.substack.com/p/the-commoditization-of-compute-why",
     "• GPU infrastructure needs a derivatives market to manage price risk\n• Standardized contracts are essential for market liquidity\n• Compute is becoming a commodity with unique characteristics\n\nBy Ronit Jain (Jun 2026). Argues GPU compute qualifies for commoditization and needs a derivatives market. Covers structural conditions (measurement, basis risk management, standard contracts), maps market participants and risks, and surveys derivative instruments required. Introduces Pluto's product architecture for this market.",
     ["Ronit Jain"], ["Architect"], [THEME["Pricing"]]),
    ("Compute is the Commodity No One Knows How to Price", "Blog Post", "2026-02-04",
     "https://davefriedman.substack.com/p/compute-is-the-commodity-no-one-knows",
     "• Compute pricing is opaque and volatile\n• No forward curve exists for compute resources\n• Electricity markets offer lessons for compute market development\n\nBy Dave Friedman (Feb 2026). Draws parallels between electricity markets and compute markets. Argues the core problem is the absence of a forward curve for compute, which prevents proper GPU financing and hedging. Discusses H100 price collapse ($8 to $2-3/hr), CoreWeave's $14B+ debt financing, and why lenders can't underwrite GPU-backed loans without standardized pricing infrastructure.",
     ["Dave Friedman"], [], [THEME["Pricing"], THEME["Capital"]]),
    ("Compute Markets Framework: 5 Conditions for Futures Trading (Thread by @firstc0in)", "Blog Post",
     "2026-05-12", "https://x.com/firstc0in/status/2054314730182070565",
     "• 5 conditions needed for futures markets: fragmentation, volatility, settlement, standardization, no substitutes\n• Compute market currently meets only some conditions\n• Market is evolving but not yet mature for robust futures trading\n\nVariant framework for evaluating compute market readiness for futures trading. Outlines 5 preconditions: supply-side fragmentation, price volatility, physical settlement infrastructure, standardization, absence of substitutes. Scores current compute market: volatility (green), settlement infrastructure (green), substitutes (yellow), supply fragmentation (red), standardization (red). Concludes market not yet mature for robust futures market.",
     ["Caleb Shack", "Alana Levin"], [], [THEME["Pricing"]]),
    ("A Framework for Valuing Bitcoin Miners as AI Infrastructure", "Industry Analysis", "2024-11-01",
     "https://www.vaneck.com/us/en/blogs/digital-assets/matthew-sigel-a-framework-for-valuing-bitcoin-miners-as-ai-infrastructure/",
     "• Bitcoin miners can pivot to AI infrastructure, creating new revenue streams\n• Valuation framework compares mining hardware utility for both crypto and AI workloads\n• Hybrid miners may command premium valuations as AI compute demand grows\n\nVanEck research analyzing how Bitcoin mining companies can transition to AI infrastructure providers. Proposes valuation framework treating mining hardware as dual-use AI compute assets.",
     ["Matthew Sigel"], [], [THEME["Capital"], THEME["Physical"]]),
    ("Nvidia GPU Debt Backstop Unleashes the AI Project Trinity", "Industry Analysis", "2026-07-06",
     "https://newsletter.semianalysis.com/p/nvidia-gpu-debt-backstop-unleashes",
     "• Nvidia provides take-or-pay commitment (backstop) to Neoclouds as minimum revenue guarantee on GPU capacity\n• Over $7T in AI debt projected by 2029\n• Three-way partnership between Nvidia, Neoclouds, and data centers (AI Project Trinity) is essential for compute market growth\n\nAnalysis of Nvidia's debt backstop program that provides revenue guarantees to Neoclouds, enabling the AI Project Trinity of capital, offtake agreements, and datacenters. Critical for understanding how AI infrastructure debt is being structured and scaled.",
     [], ["NVIDIA"], [THEME["Capital"]]),
    ("Post by @0xMetaLight on Compute Markets", "Blog Post", None,
     "https://x.com/0xMetaLight/status/2074883460942959100",
     "• Social media post about compute markets\n• Content details unavailable due to scraping limitations\n• Author likely discusses crypto/compute intersection\n\nX/Twitter post by @0xMetaLight discussing compute markets. Specific content could not be retrieved due to temporary service unavailability.",
     ["0xMetaLight"], [], [THEME["Pricing"]]),
    ("Some Bitcoin Mines can be AI Data Centers; Most Can't", "Blog Post", "2026-07-06",
     "https://davefriedman.substack.com/p/some-bitcoin-mines-can-be-ai-data",
     "• Converting bitcoin mines to AI data centers is not as straightforward as commonly believed\n• Mining requires cheap, interruptible, geo-flexible power in remote locations\n• AI data centers have different power needs and infrastructure requirements\n\nDetailed analysis arguing that the crypto-miner-to-AI-data-center conversion narrative is overstated. Mining facilities have fundamentally different characteristics than what AI workloads require.",
     ["Dave Friedman"], [], [THEME["Physical"]]),
    ("The Growing Compute Shortage", "Industry Analysis", "2026-06-01",
     "https://www.apollo.com/wealth/insights-news/insights/2026/06/growing-compute-shortage",
     "• On-demand GPU capacity is effectively sold out, even older-generation chips seeing high rental rates\n• Constraints emerging across entire AI supply chain: GPUs scarce, memory prices surging, TSMC capacity sold out\n• Investment implications for AI infrastructure and compute markets\n\nApollo Global Management analysis of the growing compute shortage. Examines supply constraints across GPUs, memory, and foundry capacity, and their investment implications.",
     [], ["Apollo Global Management"], [THEME["Physical"]]),
    ("Overview of the Energy Economy (with Datacenters)", "Blog Post", "2026-06-29",
     "https://substack.com/home/post/p-204196486",
     "• Overview of how data-center demand is reshaping power prices\n• Examines intersection of energy economy and AI infrastructure\n• Likely covers implications for compute market economics\n\nNewsletter post providing an overview of how data-center demand is reshaping power prices in the energy economy. Connects energy market dynamics to AI infrastructure growth.",
     [], [], [THEME["Physical"]]),
    ("Post by Brett Harrison on Compute as Asset Class", "Blog Post", None,
     "https://x.com/BrettHarrison/status/2074866708553117896",
     "• Architect's thesis: compute will mature as a US exchange-traded asset class very quickly\n• Fulfilling US government mandate to \"accelerate the maturation of a healthy financial market for compute\"\n• Competition with incumbent players in compute derivatives space\n\nX/Twitter post by Brett Harrison (associated with Architect) discussing the maturation of compute as a US exchange-traded asset class and fulfilling government mandates for healthy compute financial markets.",
     ["Brett Harrison"], ["Architect"], [THEME["Pricing"]]),
    ("Post by @ConorMoore on Compute Market Segments", "Blog Post", "2026-07-01",
     "https://x.com/_ConorMoore/status/2074958391118590288",
     "• Identifies the \"Compute Middle Market\" as lower risk, higher returns\n• Estimates $2T in compute spend through 2030\n• Segments compute market: Hyperscale ($2bn+), Middle Market, and other tiers\n\nX/Twitter thread by Conor Moore analyzing the compute market structure, identifying a \"middle market\" segment with attractive risk-return characteristics and projecting massive capital expenditure through 2030.",
     ["Conor Moore"], [], [THEME["Pricing"]]),
    ("Building a Robust GPU Index", "Industry Analysis", None,
     "https://www.silicondata.com/blog/building-a-robust-gpu-index",
     "• Methodology for creating reliable GPU pricing indices\n• Approaches to ensure robustness in GPU market data\n• Framework for tracking and benchmarking GPU prices\n\nBlog post from Silicon Data discussing the methodology and approach to building reliable GPU pricing indices, likely covering data collection, validation, and benchmarking practices.",
     [], ["Silicon Data"], [THEME["Pricing"], THEME["Quality"]]),
    ("SiliconMark vs. InferenceX: Comparing AI Inference Benchmarking Frameworks", "Blog Post",
     "2026-03-04", "https://www.silicondata.com/blog/siliconmark-vs.-inferencex",
     "• Compares two AI inference benchmarking frameworks for smarter GPU procurement in 2026\n• SiliconMark focuses on hardware-centric validation and supports both inference and training benchmarks\n• InferenceX (formerly InferenceMax) focuses on LLM-specific inference optimization but is not publicly accessible\n\nDetailed technical comparison of two benchmarking frameworks. SiliconMark benchmarks your own cluster with public access, while InferenceX benchmarks only their own cluster. SiliconMark supports both inference and training workloads, while InferenceX is limited to inference only.",
     ["Platon Slynko"], ["Silicon Data"], [THEME["Quality"]]),
    ("Not All H100s Are Created Equal", "Blog Post", "2026-03-27",
     "https://davefriedman.substack.com/p/not-all-h100s-are-created-equal",
     "• Research from Silicon Data shows up to 38% performance variation within identical H100 GPUs\n• Individual chip identity is the dominant factor (32-73% of variance)\n• Lenders should require performance certificates before extending credit against GPU pools\n\nAnalysis of how identical H100 GPUs show significant performance variation (up to 38%) due to manufacturing differences and cloud provider configurations. Examines implications for GPU-backed lending and risk assessment.",
     ["Dave Friedman"], ["Silicon Data"], [THEME["Quality"], THEME["Capital"]]),
    ("Did You Win the GPU Cloud Lottery? Benchmarking from TFLOPS to Tokens/$", "Research Paper",
     "2026-03-22", "https://downloads.silicondata.com/documents/GPGPU26_SiliconData.pdf",
     "1. Measured 3,500+ physical GPUs across 11 cloud providers, finding up to 38% performance variation for the same GPU model\n2. Silicon lottery effects (manufacturing variability) dominate performance variation, not software factors\n3. Cloud providers amplify these effects through persistent, systematic second-order effects in their configurations\n\nLarge-scale measurement study of 3,500+ physical GPUs across 11 cloud providers. Found up to 38% performance variation for the same GPU model, with silicon lottery effects (manufacturing variability) dominating performance variation rather than software factors.",
     ["Platon Slynko", "Jay Lu", "Jason Cornick", "Laksh Sharma", "Shou-Kai Cheng", "Benjamin Cornick",
      "Arthur O. Dias dos Santos", "Caique Sobral", "Carmen Li", "Daoxuan Xu", "Xinxin Mei", "Yifan Sun"],
     ["Silicon Data"], [THEME["Quality"], THEME["Capital"]]),
]

articles_out = [{
    "fields": {
        "Title": t,
        "Key Takeaways": tk,
        "Date Published": d,
        "URL": url,
        "Type": ty,
        "Publisher": publisher(url),
        "Author(s)": a,          # NAME refs -> resolved to IDs at load
        "Companies Mentioned": cm,  # NAME refs -> resolved to IDs at load
        "Themes": th,            # theme IDs
    }
} for (t, ty, d, url, tk, a, cm, th) in ARTICLES]

# Strip None values (Airtable rejects explicit nulls in some fields)
def clean(records):
    out = []
    for r in records:
        f = {k: v for k, v in r["fields"].items() if v not in (None, "") or k in ("Date Published",)}
        # remove empty link lists
        f = {k: v for k, v in f.items() if not (isinstance(v, list) and len(v) == 0 and k != "Themes")}
        out.append({"fields": f})
    return out

with open(os.path.join(OUT, "companies.json"), "w") as f:
    json.dump(clean(companies_out), f, indent=2)
with open(os.path.join(OUT, "people.json"), "w") as f:
    json.dump(clean(people_out), f, indent=2)
with open(os.path.join(OUT, "articles.json"), "w") as f:
    json.dump(clean(articles_out), f, indent=2)

print(f"companies: {len(clean(companies_out))}")
print(f"people: {len(clean(people_out))}")
print(f"articles: {len(clean(articles_out))}")
print(f"\nTheme IDs: {THEME}")
print("\nCompany -> primary_company name references in people.json (resolve after companies created)")
print("Author/company name references in articles.json (resolve after people/companies created)")
