# -*- coding: utf-8 -*-
import json

d = json.load(open(r"c:\Users\Ray\Documents\Projects\prompts-skills\tools\claude-lite\bootstrap_full.json", encoding="utf-8"))
cfg = d["model_selector_config"]

for surface in cfg:
    if surface.get("id") != "chat":
        continue
    print(f"===== surface: {surface['id']} =====")
    for m in surface["models"]:
        th = m.get("thinking") or {}
        eff = [e["id"] for e in th.get("effort_options", [])]
        modes = [e["id"] for e in th.get("mode_options", [])]
        dis = m.get("disabled_reason", {}).get("type") if m.get("disabled_reason") else None
        print(f"\n{m['id']}  ({m.get('name')})")
        print(f"  section={m.get('section')}  disabled={m.get('disabled')}  reason={dis}")
        print(f"  thinking.type={th.get('type')}")
        print(f"  effort_options={eff}")
        print(f"  mode_options={modes}")
