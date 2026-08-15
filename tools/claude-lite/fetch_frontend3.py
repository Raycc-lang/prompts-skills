# -*- coding: utf-8 -*-
import os
import re
import sys

sys.path.insert(0, r"c:\Users\Ray\Documents\Projects\prompts-skills\tools\claude-lite")
from claude_lite import ClaudeLite

OUT = r"c:\Users\Ray\Documents\Projects\prompts-skills\tools\claude-lite\_claude_js"
os.makedirs(OUT, exist_ok=True)

with open(r"c:\Users\Ray\Documents\Projects\prompts-skills\tools\claude-lite\_claude_new.html",
          encoding="utf-8", errors="ignore") as f:
    html = f.read()

urls = set(re.findall(r'(?:src|href)="(https://assets-proxy[^"]+\.js[^"]*)"', html))
print(f"下载 {len(urls)} 个 bundle ...")

client = ClaudeLite.from_config()
names = []
for u in sorted(urls):
    name = u.split("/")[-1].split("?")[0]
    path = os.path.join(OUT, name)
    if os.path.exists(path) and os.path.getsize(path) > 0:
        names.append(name)
        continue
    try:
        r = client.session.get(u, timeout=120)
        if r.status_code == 200:
            with open(path, "w", encoding="utf-8", errors="ignore") as f:
                f.write(r.text)
            names.append(name)
        else:
            print(f"  {name}: HTTP {r.status_code}")
    except Exception as e:
        print(f"  {name}: {e}")

print(f"共 {len(names)} 个文件")

KEYWORDS = ["paprika_mode", "paprikaMode", "thinking_modes",
            "adaptive_thinking", "enabled_full_thinking",
            "thinking_effort", "effort_level", "reasoning_effort"]
print("\n=== 关键词命中 ===")
for name in names:
    with open(os.path.join(OUT, name), encoding="utf-8",
              errors="ignore") as f:
        text = f.read()
    hits = [(kw, text.count(kw)) for kw in KEYWORDS if kw in text]
    if hits:
        print(f"  {name}: {hits}")
