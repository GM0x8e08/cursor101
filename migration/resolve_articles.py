#!/usr/bin/env python3
"""Resolve Articles' 'Author(s)' -> people IDs and 'Companies Mentioned' -> company IDs,
then batch into load files of 10."""
import json, os

OUT = os.path.join(os.path.dirname(__file__), "data")

PEOPLE_IDS = {
    "Brett Harrison": "reca1VkIanK5SFOn8",
    "Carmen Li": "recbryT7hWZk1US8S",
    "Dylan Patel": "recCiHTaSNGtWylav",
    "Daniel Nishball": "rec0axVfRmtwoh7RA",
    "Ray Wang": "recubAHeArDW1L2z3",
    "Myron Xie": "rec2KpnC3N9FCPrG2",
    "Theodora Diamandis": "recCWMMwRhWFonwSc",
    "Platon Slynko": "recaWU8PMbF4qXM5J",
    "Jason Cornick": "recxKB5rQkOgCtFJD",
    "Benjamin Cornick": "recCiPrpuKDbpMaKr",
    "Jay Lu": "recSfhM3GfBSgCJxz",
    "Laksh Sharma": "recMuFhokGbTFACOz",
    "Shou-Kai Cheng": "rec0TGcA52sGpzppa",
    "Arthur O. Dias dos Santos": "recWKBcdYj1FqX3g5",
    "Caique Sobral": "recPGSRAXGISPp4IN",
    "Daoxuan Xu": "recSf3cdf5mOwYuuM",
    "Xinxin Mei": "recTCQJYNpXCyM9Jb",
    "Yifan Sun": "rec5U3iWYew0R4KSt",
    "Matthew Sigel": "recPE5Wbm6pSrXd50",
    "Caleb Shack": "recsLTxzkkREXdrF9",
    "Alana Levin": "recOAqIx1xc8iAzOJ",
    "Ronit Jain": "reckrkAJk8VIrN9qG",
    "Dave Friedman": "recP103D71Ma7V2tQ",
    "Conor Moore": "recVR0RNMDftTkPRu",
    "0xturbanurban": "rec0bBbCmO3ERssre",
    "0xMetaLight": "reckrOQREvBo30yhu",
}
COMPANY_IDS = json.load(open(os.path.join(OUT, "company_ids.json")))

json.dump(PEOPLE_IDS, open(os.path.join(OUT, "people_ids.json"), "w"), indent=2)

articles = json.load(open(os.path.join(OUT, "articles.json")))
resolved = []
miss_authors, miss_companies = [], []
for rec in articles:
    f = dict(rec["fields"])
    authors = f.get("Author(s)", [])
    if authors:
        ids = []
        for a in authors:
            if a in PEOPLE_IDS:
                ids.append(PEOPLE_IDS[a])
            else:
                miss_authors.append(a)
        f["Author(s)"] = ids
    cm = f.get("Companies Mentioned", [])
    if cm:
        ids = []
        for c in cm:
            if c in COMPANY_IDS:
                ids.append(COMPANY_IDS[c])
            else:
                miss_companies.append(c)
        f["Companies Mentioned"] = ids
    resolved.append({"fields": f})

if miss_authors:
    print("WARNING authors not found:", miss_authors)
if miss_companies:
    print("WARNING companies not found:", miss_companies)

for i, start in enumerate(range(0, len(resolved), 10)):
    batch = {"records": resolved[start:start+10]}
    fn = os.path.join(OUT, f"load_articles_{i+1}.json")
    json.dump(batch, open(fn, "w"))
    print(f"{fn}: {len(batch['records'])} records")

print(f"total articles resolved: {len(resolved)}")
print(f"articles with authors: {sum(1 for r in resolved if r['fields'].get('Author(s)'))}")
print(f"articles with companies mentioned: {sum(1 for r in resolved if r['fields'].get('Companies Mentioned'))}")
