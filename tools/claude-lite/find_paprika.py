# -*- coding: utf-8 -*-
import json

data = json.load(open(
    r"c:\Users\Ray\Documents\Projects\prompts-skills\tools\claude-lite\bootstrap_dump.json",
    encoding="utf-8"))


def walk(obj, path=""):
    if isinstance(obj, dict):
        for k, v in obj.items():
            p = f"{path}.{k}" if path else k
            if "paprika" in k.lower() and "models_config" not in path:
                print(f"{p} = {json.dumps(v, ensure_ascii=False)[:200]}")
            walk(v, p)
    elif isinstance(obj, list):
        for i, v in enumerate(obj):
            walk(v, f"{path}[{i}]")


walk(data)

# account.settings 全量
print("\n=== account.settings ===")
print(json.dumps(data["account"].get("settings", {}),
                 ensure_ascii=False, indent=1)[:1500])
