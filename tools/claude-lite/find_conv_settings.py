# -*- coding: utf-8 -*-
import re, glob, os

d = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_claude_js")
for p in glob.glob(os.path.join(d, "*.js")):
    s = open(p, encoding="utf-8", errors="ignore").read()
    # 找发送 {settings: 的 mutation，以及 chat_conversations settings 端点
    for m in list(re.finditer(r"chat_conversations[^\n]{0,80}settings", s))[:5]:
        a = max(0, m.start() - 150)
        b = min(len(s), m.end() + 150)
        print("#A", os.path.basename(p), s[a:b].replace("\n", " "))
        print()
    for m in list(re.finditer(r"settings[^\n]{0,40}chat_conversations", s))[:5]:
        a = max(0, m.start() - 150)
        b = min(len(s), m.end() + 150)
        print("#B", os.path.basename(p), s[a:b].replace("\n", " "))
        print()
