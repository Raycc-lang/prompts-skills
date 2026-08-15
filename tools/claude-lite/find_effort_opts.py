# -*- coding: utf-8 -*-
import os
import re

OUT = r"c:\Users\Ray\Documents\Projects\prompts-skills\tools\claude-lite\_claude_js"
patterns = ["effort_options", "mode_options", "model_selector",
            '"xhigh"', '"low"', "recommended"]

for name in sorted(os.listdir(OUT)):
    with open(os.path.join(OUT, name), encoding="utf-8",
              errors="ignore") as f:
        text = f.read()
    hits = {p: text.count(p) for p in patterns if p in text}
    if hits:
        print(f"{name}: {hits}")

# 找 effort_options 的定义上下文
print("\n=== effort_options 上下文 ===")
for name in sorted(os.listdir(OUT)):
    with open(os.path.join(OUT, name), encoding="utf-8",
              errors="ignore") as f:
        text = f.read()
    for m in list(re.finditer("effort_options", text))[:3]:
        pos = m.start()
        print(f"\n--- {name} @{pos} ---")
        print(text[max(0, pos - 300):pos + 300].replace("\n", " "))
