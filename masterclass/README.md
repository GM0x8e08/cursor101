# Masterclass in Digital Infrastructure & Neocloud Opportunities

A self-paced, interactive 5-module course on how the internet's "plumbing" works in Latin
America and how an entrepreneur without an IT background — and without owning any pipes —
can spot and capture a "neocloud" opportunity. The EdgeUno model (asset-light, AS 7195,
content localization, the "breaker" mindset) is the recurring case study.

## How to take the course

No installation, no dependencies, no server required.

1. Open `index.html` in any modern browser (double-click it, or drag it into a browser window).
2. Click **Start Module 1** and read the three short lessons (about 4 minutes each).
3. Take the **Knowledge Check** at the end of the module — 5 challenging questions.
4. Score **4/5 or better** to unlock the next module. Wrong answers come with explanations
   showing exactly where your knowledge is lagging, so retakes are learning, not guessing.
5. Your progress saves automatically in the browser (localStorage). Close the tab and come
   back anytime; use **Reset progress** in the sidebar to start over.

Optionally, serve it locally instead of opening the file directly:

```bash
cd masterclass
python3 -m http.server 8080
# then visit http://localhost:8080
```

## Course design

- **Explain the "Why":** every technical concept is paired with a gold **Follow the money**
  callout explaining who pays whom and why the margin exists.
- **EdgeUno case study:** blue **EdgeUno lens** callouts apply each concept to the
  AS 7195 / asset-light playbook.
- **Entrepreneurial lens:** purple **Entrepreneur's takeaway** callouts translate each
  concept into a move a non-technical "jack of all trades" can make.
- **Gated progression:** modules unlock only after passing the previous knowledge check,
  enforcing a firm grasp before advancing.

## Syllabus

| # | Module | Core questions |
|---|--------|----------------|
| 1 | The Internet's Nervous System | AS numbers & AS 7195, the global routing table, transit vs. peering, cross-connects, the "Miami Problem" and content localization |
| 2 | The Physics of Data | DWDM and selling "waves" to hyperscalers, LATAM submarine/terrestrial cables, why an Andes chokepoint is both risk and product, latency as money |
| 3 | The Neocloud & Asset-Light Strategy | Managing $50M+ of infrastructure without owning it (IRUs), colo + owned GPUs margin stacking, when asset-light flips to asset-owner |
| 4 | Emerging Verticals | Edge AI inference & data sovereignty, the Web3 validator/RPC opportunity, the Megaport/PacketFabric software-defined shift |
| 5 | Spotting the Opportunity | The "human gap" (talent businesses), the channel-partner model for "power on / power off" customers, the five-question Opportunity Filter |

## Project structure

```
masterclass/
├── index.html      # App shell — open this file
├── css/style.css   # Styling (dark, distraction-free reading theme)
└── js/
    ├── content.js  # All course content: 15 lessons + 25 quiz questions
    └── app.js      # Navigation, quiz grading, module gating, progress persistence
```

Plain HTML/CSS/JavaScript — no build step, no frameworks, no network access needed.
