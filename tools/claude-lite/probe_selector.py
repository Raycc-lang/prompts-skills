# -*- coding: utf-8 -*-
import json
import sys

sys.path.insert(0, r"c:\Users\Ray\Documents\Projects\prompts-skills\tools\claude-lite")
from claude_lite import ClaudeLite, BASE_URL

client = ClaudeLite.from_config()
org = client._ensure_org()

for surface in ("chat", "cowork", "code"):
    url = f"{BASE_URL}/api/organizations/{org}/model_selector_state/{surface}"
    resp = client.session.get(
        url, headers=client._headers({"Accept": "application/json"}),
        timeout=30)
    print(f"=== {surface} -> HTTP {resp.status_code} ===")
    if resp.status_code != 200:
        print(resp.text[:200])
        continue
    data = resp.json()
    with open(rf"c:\Users\Ray\Documents\Projects\prompts-skills\tools\claude-lite\selector_{surface}.json",
              "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print("顶层键:", list(data.keys()) if isinstance(data, dict) else type(data))
