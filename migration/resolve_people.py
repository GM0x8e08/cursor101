#!/usr/bin/env python3
"""Resolve People's 'Primary Company' name references to company record IDs,
then batch into load files of 10. Also save the company ID map for later use."""
import json, os

OUT = os.path.join(os.path.dirname(__file__), "data")
os.makedirs(OUT, exist_ok=True)

COMPANY_IDS = {
    "Ornn": "rec9RlxWgNGahkbLN",
    "Silicon Data": "recGE3j6S1LFWiMFF",
    "SF Compute": "rec9vgKqhKjB1XaGj",
    "NVIDIA": "recbI7URltDqxGK62",
    "Architect": "rec7lX0mGiZnodpRd",
    "SemiAnalysis": "recNIS4Atxglq9UyA",
    "Anagram": "recDj4Gk3wi0kFkH6",
    "Variant Fund": "reckZhwBBgH6VFbxT",
    "VanEck": "recATk5zeamHivdgD",
    "Apollo Global Management": "recjnaL1NhRXu9PB7",
    "GPU Lease Index (GLRI)": "recMkd9GwgrEyF5AW",
    "Axon Index": "recvnTAYXYGr9ZrHC",
    "Anera Markets": "rec7RaxR0Ombw38Wf",
    "BitOoda": "recpKubDL7POhGnaJ",
    "NativX": "reciFFqKfpSUDCuhf",
    "Thunder Compute": "recybmSJZM9fkQbO0",
    "Exascale Labs": "recUQoEI5BRDdcT4q",
    "GetDeploying": "receWbw2UuIAgkAhx",
    "CloudPrice": "recC8T97fJ7KJ2YqO",
    "AI Multiple": "recs0IeALa2BKDuUO",
    "United Compute": "recH1gHAI7dNwendE",
    "Arena AI": "recvuCZefet6BxUQ1",
    "Compute Desk": "reczR3KSrWIu3GWrr",
}

json.dump(COMPANY_IDS, open(os.path.join(OUT, "company_ids.json"), "w"), indent=2)

people = json.load(open(os.path.join(OUT, "people.json")))
resolved = []
missing = []
for rec in people:
    f = dict(rec["fields"])
    pc = f.get("Primary Company", [])
    if pc:
        name = pc[0] if isinstance(pc, list) else pc
        if name in COMPANY_IDS:
            f["Primary Company"] = [COMPANY_IDS[name]]
        else:
            missing.append(name)
            f.pop("Primary Company", None)
    resolved.append({"fields": f})

if missing:
    print("WARNING: companies not found for:", missing)

# batch into 10s
for i, start in enumerate(range(0, len(resolved), 10)):
    batch = {"records": resolved[start:start+10]}
    fn = os.path.join(OUT, f"load_people_{i+1}.json")
    json.dump(batch, open(fn, "w"))
    print(f"{fn}: {len(batch['records'])} records")

print(f"total people resolved: {len(resolved)}")
print(f"people with Primary Company link: {sum(1 for r in resolved if r['fields'].get('Primary Company'))}")
