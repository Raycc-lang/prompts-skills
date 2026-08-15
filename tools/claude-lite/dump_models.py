# -*- coding: utf-8 -*-
import json
import re

data = json.load(open(
    r"c:\Users\Ray\Documents\Projects\prompts-skills\tools\claude-lite\bootstrap_dump.json",
    encoding="utf-8"))
cfg = data["account"]["memberships"][0]["organization"][
    "claude_ai_bootstrap_models_config"]

print("=== 全部模型配置 ===")
for m in cfg:
    tm = m.get("thinking_modes", [])
    tms = ", ".join(f"{t.get('id')}/{t.get('mode')}" for t in tm)
    flags = []
    if m.get("inactive"):
        flags.append("inactive")
    if m.get("overflow"):
        flags.append("overflow")
    print(f"{m['model']:40s} | {m.get('name',''):18s} | "
          f"paprika={m.get('paprika_modes')} | modes=[{tms}] | {' '.join(flags)}")

print()
text = json.dumps(data, ensure_ascii=False)
print("=== paprika 相关键 ===")
hits = sorted(set(re.findall(r'"[^"]*paprika[^"]*"\s*:', text, re.I)))
for h in hits[:20]:
    print("  ", h.strip())

# 找 sonnet-4-6 的完整条目
print()
print("=== claude-sonnet-4-6 完整条目 ===")
for m in cfg:
    if m["model"] == "claude-sonnet-4-6":
        print(json.dumps(m, ensure_ascii=False, indent=1))
