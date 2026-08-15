# -*- coding: utf-8 -*-
import os
import re
from collections import Counter

OUT = r"c:\Users\Ray\Documents\Projects\prompts-skills\tools\claude-lite\_claude_js"
urls = Counter()

for name in sorted(os.listdir(OUT)):
    with open(os.path.join(OUT, name), encoding="utf-8",
              errors="ignore") as f:
        text = f.read()
    for m in re.finditer(r'["\'`/](api/[a-z0-9_/${}.-]+)', text):
        u = m.group(1)
        if any(k in u for k in ("model", "selector", "setting", "bootstrap")):
            urls[u] += 1

for u, n in urls.most_common(40):
    print(f"{n:4d}  {u}")
