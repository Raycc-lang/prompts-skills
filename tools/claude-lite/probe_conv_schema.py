# -*- coding: utf-8 -*-
"""实测通过 PATCH 对话设置 paprika_mode，观察 effective_thinking_mode。"""
import sys, json, uuid as uuid_mod
sys.path.insert(0, r"c:\Users\Ray\Documents\Projects\prompts-skills\tools\claude-lite")
from claude_lite import ClaudeLite, BASE_URL

client = ClaudeLite.from_config()
org = client._ensure_org()
H = client._headers({"Accept": "application/json"})

def new_conv():
    conv = str(uuid_mod.uuid4())
    client.session.post(
        f"{BASE_URL}/api/organizations/{org}/chat_conversations",
        headers=H, json={"uuid": conv, "name": ""}, timeout=30)
    return conv

def get_etm(conv):
    g = client.session.get(
        f"{BASE_URL}/api/organizations/{org}/chat_conversations/{conv}"
        f"?rendering_mode=raw", headers=H, timeout=30)
    d = g.json()
    return d.get("effective_thinking_mode"), d.get("settings", {}).get("paprika_mode")

def patch(conv, body, label):
    r = client.session.patch(
        f"{BASE_URL}/api/organizations/{org}/chat_conversations/{conv}",
        headers=H, json=body, timeout=30)
    etm, pm = get_etm(conv)
    print(f"[{label}] PATCH {r.status_code} -> etm={etm} settings.paprika={pm}"
          + ("" if r.status_code < 400 else f" body={r.text[:120]}"))

conv = new_conv()
print("初始:", get_etm(conv))
patch(conv, {"settings": {"paprika_mode": "extended"}}, "settings.paprika_mode")
patch(conv, {"paprika_mode": "extended"}, "top-level paprika_mode")
