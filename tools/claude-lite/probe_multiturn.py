# -*- coding: utf-8 -*-
"""验证多轮机制：第二轮只发新消息 + conversation_id，不重发 protocol/历史。"""
import sys, os
sys.path.insert(0, r"c:\Users\Ray\Documents\Projects\prompts-skills\tools\claude-lite")
from claude_lite import ClaudeLite

ROOT = r"c:\Users\Ray\Documents\Projects\prompts-skills"
protocol = open(os.path.join(ROOT, "prompts", "English-learning", "expression-partner-v3.md"), encoding="utf-8").read()

turn1_input = (
    "QUESTION / TASK: 同事提议把发布会改到周五，我不同意，想当面说明并给出替代方案\n"
    "SETTING AND AUDIENCE: 项目组周会，五六个人，都是共事多年的同事\n"
    "RAW RESPONSE: 我觉得周五不太好，因为很多同事 zhou五下午有固定的接送安排，"
    "attendance 会低。要不我们kan一下周四，或者把时间改到上午？\n"
    "INTENDED POINT OR EMPHASIS: 我的替代方案是认真考虑过的，不是随便挑刺"
)

client = ClaudeLite.from_config()
reply1, conv_id = client.chat(protocol + "\n\n" + turn1_input, model="claude-sonnet-4-6")
print("=" * 20, "TURN 1 (protocol + 输入块)", "=" * 20)
print(reply1[:600])
print("... [省略] ...\n")

reply2, _ = client.chat(
    "I'll go with version 2, but cut it to about half the length.",
    model="claude-sonnet-4-6",
    conversation_id=conv_id,
)
print("=" * 20, "TURN 2 (仅一句选择 + conv_id)", "=" * 20)
print(reply2[:900])
