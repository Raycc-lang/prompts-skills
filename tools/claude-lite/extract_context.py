# -*- coding: utf-8 -*-
"""提取 bundle 中 paprika_mode / effort_level 的上下文。"""
import os
import re
import sys

OUT = r"c:\Users\Ray\Documents\Projects\prompts-skills\tools\claude-lite\_claude_js"
FILES = ["shared-6-DJaaMO0k.js", "shared-5-C8kpLJS6.js",
         "shared-8-7xGXiF-4.js", "shared-11-Cf_S8uLi.js",
         "shared-2-DXSb6bXE.js", "shared-3-V5hPpzsf.js"]
KW = sys.argv[1] if len(sys.argv) > 1 else "paprika_mode"
WIDTH = int(sys.argv[2]) if len(sys.argv) > 2 else 400

for name in FILES:
    path = os.path.join(OUT, name)
    if not os.path.exists(path):
        continue
    with open(path, encoding="utf-8", errors="ignore") as f:
        text = f.read()
    idxs = [m.start() for m in re.finditer(re.escape(KW), text)]
    if not idxs:
        continue
    print(f"\n{'='*70}\n### {name} — '{KW}' x{len(idxs)}\n{'='*70}")
    for i, pos in enumerate(idxs[:12]):
        snippet = text[max(0, pos - WIDTH // 2):pos + WIDTH // 2]
        snippet = snippet.replace("\n", " ")
        print(f"\n--- [{i}] @{pos} ---")
        print(snippet)
