# -*- coding: utf-8 -*-
"""探测 claude.ai 账号可用模型与 thinking 配置。"""
import json
import sys

sys.path.insert(0, r"c:\Users\Ray\Documents\Projects\prompts-skills\tools\claude-lite")
from claude_lite import ClaudeLite, BASE_URL

client = ClaudeLite.from_config()
org = client._ensure_org()
print(f"org = {org}")

# 1. bootstrap
resp = client.session.get(
    BASE_URL + "/api/bootstrap",
    headers=client._headers({"Accept": "application/json"}),
    timeout=30,
)
print(f"\n=== /api/bootstrap -> HTTP {resp.status_code} ===")
if resp.status_code == 200:
    data = resp.json()
    with open(r"c:\Users\Ray\Documents\Projects\prompts-skills\tools\claude-lite\bootstrap_dump.json",
              "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=1)
    print("顶层键:", list(data.keys()))
    text = json.dumps(data, ensure_ascii=False)
    # 找所有和模型/思考相关的键值
    import re
    for kw in ("model", "thinking", "effort", "reason"):
        hits = set(re.findall(rf'"[^"]*{kw}[^"]*"\s*:', text, re.I))
        if hits:
            print(f"\n-- 含 '{kw}' 的键 ({len(hits)}):")
            for h in sorted(hits)[:40]:
                print("  ", h.strip())
