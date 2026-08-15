# -*- coding: utf-8 -*-
"""用 curl_cffi 会话抓 claude.ai 前端 JS bundle，找 thinking payload 构造。"""
import os
import re
import sys

sys.path.insert(0, r"c:\Users\Ray\Documents\Projects\prompts-skills\tools\claude-lite")
from claude_lite import ClaudeLite, BASE_URL

OUT = r"c:\Users\Ray\Documents\Projects\prompts-skills\tools\claude-lite\_claude_js"
os.makedirs(OUT, exist_ok=True)

client = ClaudeLite.from_config()
resp = client.session.get(
    BASE_URL + "/new",
    headers=client._headers({"Accept": "text/html"}),
    timeout=60,
)
print(f"GET /new -> HTTP {resp.status_code}, {len(resp.text)} chars")
html = resp.text
if "challenge-platform" in html or "Just a moment" in html:
    print("!! 仍被 Cloudflare 拦截")
    sys.exit(1)

urls = set(re.findall(r'src="([^"]+\.js[^"]*)"', html))
urls |= set(re.findall(r'href="([^"]+\.js[^"]*)"', html))
print(f"找到 {len(urls)} 个 JS URL")

bundles = []
for u in sorted(urls):
    if u.startswith("/"):
        u = BASE_URL + u
    name = u.split("/")[-1].split("?")[0]
    try:
        r = client.session.get(u, timeout=60)
        if r.status_code == 200:
            path = os.path.join(OUT, name)
            with open(path, "w", encoding="utf-8", errors="ignore") as f:
                f.write(r.text)
            bundles.append((name, len(r.text)))
    except Exception as e:
        print(f"  下载失败 {name}: {e}")

for name, size in bundles:
    print(f"  {name}: {size}")

# 在所有 bundle 里找 paprika / thinking payload 线索
print("\n=== 搜索 paprika_mode / thinking 相关 ===")
for name, _ in bundles:
    path = os.path.join(OUT, name)
    with open(path, encoding="utf-8", errors="ignore") as f:
        text = f.read()
    for kw in ("paprika_mode", "paprikaMode", "thinking_modes",
               "adaptive_thinking", "enabled_full_thinking"):
        n = text.count(kw)
        if n:
            print(f"  {name}: '{kw}' x{n}")
