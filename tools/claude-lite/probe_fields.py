# -*- coding: utf-8 -*-
"""dump 思考请求的全部 SSE 事件类型，确认 thinking 块形式。"""
import sys, json, uuid as uuid_mod
from collections import Counter
sys.path.insert(0, r"c:\Users\Ray\Documents\Projects\prompts-skills\tools\claude-lite")
from claude_lite import ClaudeLite, BASE_URL

client = ClaudeLite.from_config()
org = client._ensure_org()

HARD = ("一个农夫要带狼、羊、白菜过河，船每次只能载农夫和其中一样。"
        "狼和羊单独在一起会吃羊，羊和白菜单独在一起会吃白菜。给出最少步骤方案。")

def dump(thinking_mode, effort):
    conv = str(uuid_mod.uuid4())
    client.session.post(
        f"{BASE_URL}/api/organizations/{org}/chat_conversations",
        headers=client._headers({"Accept": "application/json"}),
        json={"uuid": conv, "name": ""}, timeout=30)
    payload = {"prompt": HARD, "timezone": "Asia/Shanghai", "locale": "en-US",
               "model": "claude-sonnet-4-6", "attachments": [], "files": [],
               "thinking_mode": thinking_mode, "effort": effort}
    url = (f"{BASE_URL}/api/organizations/{org}"
           f"/chat_conversations/{conv}/completion")
    r = client.session.post(url, headers=client._headers(
        {"Referer": f"{BASE_URL}/chat/{conv}"}), json=payload,
        timeout=300, stream=True)
    print(f"\n===== thinking_mode={thinking_mode} effort={effort} HTTP {r.status_code}")
    types = Counter()
    samples = {}
    for raw in r.iter_lines():
        if not raw:
            continue
        line = raw.decode("utf-8", "ignore")
        if not line.startswith("data:"):
            continue
        ds = line[5:].strip()
        if not ds or ds == "[DONE]":
            continue
        try:
            d = json.loads(ds)
        except Exception:
            continue
        t = d.get("type")
        dt = d.get("delta", {}).get("type") if isinstance(d.get("delta"), dict) else None
        key = f"{t}/{dt}" if dt else t
        types[key] += 1
        if key not in samples:
            samples[key] = json.dumps(d, ensure_ascii=False)[:180]
    for k, c in types.most_common():
        print(f"  {k}  x{c}")
        print(f"     样例: {samples[k]}")

dump("extended", "max")
