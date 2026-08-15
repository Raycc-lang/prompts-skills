# -*- coding: utf-8 -*-
"""获取完整 bootstrap（app_start），提取 model_selector_config 的 effort/mode 选项。"""
import json
import sys

sys.path.insert(0, r"c:\Users\Ray\Documents\Projects\prompts-skills\tools\claude-lite")
from claude_lite import ClaudeLite, BASE_URL

client = ClaudeLite.from_config()
org = client._ensure_org()
print(f"org = {org}")

url = (
    f"{BASE_URL}/api/bootstrap/{org}/app_start"
    f"?statsig_hashing_algorithm=djb2&growthbook_format=sdk"
)
resp = client.session.get(
    url,
    headers=client._headers({"Accept": "application/json"}),
    timeout=60,
)
print(f"HTTP {resp.status_code}")
if resp.status_code != 200:
    print(resp.text[:500])
    sys.exit(1)

data = resp.json()
with open(r"c:\Users\Ray\Documents\Projects\prompts-skills\tools\claude-lite\bootstrap_full.json",
          "w", encoding="utf-8") as f:
    json.dump(data, f, ensure_ascii=False, indent=1)
print("顶层键:", list(data.keys()))

cfg = data.get("model_selector_config")
state = data.get("model_selector_state")
print("\n=== model_selector_state ===")
print(json.dumps(state, ensure_ascii=False, indent=1)[:1500])
print("\n=== model_selector_config (models) ===")
if cfg and "models" in cfg:
    for m in cfg["models"]:
        th = m.get("thinking") or {}
        print("-" * 60)
        print("id:", m.get("id"), "| name:", m.get("name"), "| section:", m.get("section"))
        if th:
            print("  thinking.mode:", th.get("mode"))
            print("  effort_options:", [e.get("id") for e in th.get("effort_options", [])])
            print("  mode_options:", [(e.get("id"), e.get("recommended")) for e in th.get("mode_options", [])])
            print("  always_on:", th.get("always_on"))
else:
    print(json.dumps(cfg, ensure_ascii=False)[:2000])
