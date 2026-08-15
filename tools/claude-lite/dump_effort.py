# -*- coding: utf-8 -*-
import json

data = json.load(open(
    r"c:\Users\Ray\Documents\Projects\prompts-skills\tools\claude-lite\bootstrap_dump.json",
    encoding="utf-8"))

gb = data.get("growthbook", {}).get("features", {})
for key, feat in gb.items():
    val = feat.get("value")
    if isinstance(val, dict) and isinstance(val.get("models"), list):
        print(f"### feature: {key}")
        for m in val["models"]:
            print("\n" + json.dumps(m, ensure_ascii=False, indent=1))
