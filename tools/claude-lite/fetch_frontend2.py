# -*- coding: utf-8 -*-
import re
import sys

sys.path.insert(0, r"c:\Users\Ray\Documents\Projects\prompts-skills\tools\claude-lite")
from claude_lite import ClaudeLite, BASE_URL

client = ClaudeLite.from_config()
resp = client.session.get(
    BASE_URL + "/new",
    headers=client._headers({"Accept": "text/html"}),
    timeout=60,
)
html = resp.text
print(f"HTTP {resp.status_code}, {len(html)} chars")
print("--- 前 500 字符 ---")
print(html[:500])
print("--- 关键词检查 ---")
for kw in ("challenge-platform", "Just a moment", "_next/static",
           "window.__remixContext", "buildManifest"):
    print(f"  '{kw}': {html.count(kw)}")

with open(r"c:\Users\Ray\Documents\Projects\prompts-skills\tools\claude-lite\_claude_new.html",
          "w", encoding="utf-8", errors="ignore") as f:
    f.write(html)

urls = set(re.findall(r'(?:src|href)="([^"]+\.js[^"]*)"', html))
print(f"\nJS URLs ({len(urls)}):")
for u in sorted(urls)[:40]:
    print("  ", u)
