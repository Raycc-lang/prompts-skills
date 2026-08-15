# -*- coding: utf-8 -*-
import re

p = r"c:\Users\Ray\Documents\Projects\prompts-skills\tools\claude-lite\_claude_js\shared-0-C7AWzcH7.js"
s = open(p, encoding="utf-8", errors="ignore").read()
for m in re.finditer(r'\bep\s*=', s):
    a = max(0, m.start() - 40)
    b = min(len(s), m.end() + 300)
    print(s[a:b].replace("\n", " "))
    print("---")
