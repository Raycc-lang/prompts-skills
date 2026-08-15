# -*- coding: utf-8 -*-
import re

path = r"c:\Users\Ray\Documents\Projects\prompts-skills\tools\claude-lite\_claude_js\shared-8-7xGXiF-4.js"
with open(path, encoding="utf-8", errors="ignore") as f:
    text = f.read()

# 找 Ls / As / wl / lf 等模式映射函数
for fn in ("function Ls", "function As", "function wl", "function lf",
           "function nl", "function Ms", "function tr", "function vr",
           "function uo", "function hf"):
    for m in re.finditer(re.escape(fn), text):
        pos = m.start()
        print(f"--- {fn} @{pos} ---")
        print(text[pos:pos + 320].replace("\n", " "))
        print()
        break

# "extended" 字符串相关
print("=== 'extended' 附近 ===")
for m in list(re.finditer(r'"extended"', text))[:6]:
    pos = m.start()
    print(text[max(0, pos - 150):pos + 150].replace("\n", " "))
    print()
