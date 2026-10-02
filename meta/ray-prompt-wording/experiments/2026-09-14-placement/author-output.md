A — 今天直接使用的 prompt：

```text
把下面的会议笔记整理成一份可以直接发给团队的更新，让大家清楚看到：
- 进展：完成了什么、有哪些明确结果。
- 待办：接下来做什么；笔记里有负责人或时间就写上，缺失但需要落实的标为“待确认”。
- 阻塞：什么问题影响了哪些工作，需要什么帮助或决定。

合并重复内容，保留影响行动的细节，语言简洁，格式以易读为准。区分已经确认的决定和仍在讨论的建议；不要把推测写成事实。没有提及的部分写“笔记未提及”。

会议笔记：
[粘贴笔记]
```

B — Split the instructions by when agents need them.

Place this in the repository’s root `AGENTS.md`, merging it with existing guidance:

```markdown
## Project requirements

All code must remain compatible with Python 3.12.

Lint command: `uv run ruff check .`. CI already enforces this check.

For monthly releases, load the `monthly-release` skill before preparing the release.
```

Keep the existing Ruff CI enforcement. No additional lint policy or duplicate CI configuration is needed.

Place this scoped draft in the host’s skill directory, for example `.agents/skills/monthly-release/SKILL.md` if that is the repository’s supported location:

```markdown
---
name: monthly-release
description: Prepare a monthly release by assessing migration compatibility and selecting the release approach. Use only for monthly releases.
---

Inspect the migration files included in the release and the code that depends on them.

Separate migrations into:
- Backward-compatible: existing deployed code can continue operating correctly after
  the migration.
- Breaking: the migration requires coordinated changes to deployed code, data, or
  consumers to continue operating correctly.

Explain each classification using the migration’s actual effects. Investigate unclear
cases before selecting the release approach; report any unresolved compatibility
question that prevents a decision.

If any migration is breaking, choose a staged release. Describe the sequence needed
to introduce compatible changes, migrate data or consumers, verify the transition,
and then remove obsolete structures or behavior.

If all migrations are backward-compatible, use the ordinary release approach.

Include the migration classifications, supporting evidence, and chosen release
sequence in the release plan.
```

This is a draft skill; its directory must match the target host’s skill discovery convention.

Put today’s task in the current prompt:

```text
Fix the typo in the documentation. Inspect the relevant text, make the correction,
and check that the wording and formatting read correctly. Report what changed.
```

If the typo’s location or intended correction is known, add it to that prompt. Today’s task does not activate the monthly release procedure.

C — Copyable agent prompt:

```text
Inspect this repository, discover which API models its configured provider supports
using the existing credential, update the relevant configuration, and probe the
selected models.

1. Read the applicable repository instructions and inspect how provider configuration,
   credentials, model selection, and API requests work. Identify the model roles and
   capabilities the application requires, along with relevant validation commands.

2. Use the configured provider’s supported discovery mechanism with the existing
   credential. If model listing is unavailable, use the provider’s authoritative
   documentation and targeted requests to establish available candidates. Distinguish
   advertised models, models listed for this credential, and models actually verified
   by a successful request.

3. Select models that meet the application’s required capabilities. Preserve existing
   selections where they are supported and suitable. Base replacements on the
   application’s existing requirements and preferences; ask for a decision only if an
   unresolved tradeoff materially blocks selection.

4. Update the relevant configuration and run its applicable local validation. Probe
   each selected model through the application’s actual request path where feasible,
   using a small request that exercises the capability required for its role.

5. Diagnose failed probes before changing selections. Distinguish configuration or
   request errors, authentication or access failures, unsupported models or features,
   and transient service failures. Repair recoverable issues within scope and repeat
   the affected checks. If completion remains blocked, report the specific blocker
   and which configuration changes and checks are complete.

Finish with the configuration changes, evidence for the selections, checks actually
run, and each selected model’s probe result. Clearly identify anything still
unverified.
```

Run **Deep with high effort**. Both candidates have the required tools; the deciding factors are the unfamiliar repository, dependent discovery and configuration steps, and possible API failure diagnosis. A one-line final diff does not reduce that execution burden.

A cheaper option is **Fast with low effort after discovery is complete**, when a handoff supplies the exact configuration change, verified model IDs, and probe commands. If the whole task becomes straightforward after initial inspection, Deep with low effort is also reasonable. These recommendations use the capabilities supplied in the request, not benchmark results.

All three deliverables are drafts reviewed for scope and consistency; no target-agent execution, installation, or external action was performed.
