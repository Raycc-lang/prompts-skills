---
name: ray-prompt-wording
description: "Design, revise, diagnose, or review Ray's model instructions while preserving intent and keeping wording concise. Use for 写提示词, 润色提示词, 优化 prompt, one-off or reusable prompts, agent instructions, independent-analysis prompts, instruction placement, and model/reasoning-level selection. Handle prompt evaluations when requested; ordinary human-facing prose and full skill-package construction belong elsewhere."
---

# Ray's Prompt Wording

Help Ray clarify the outcome he wants and give the model the instructions it needs to achieve it. Prefer the shortest clear, faithful wording that preserves useful capabilities and necessary context.

## Understand the request

- Identify whether the user wants a prompt, revision, diagnosis, review, evaluation, or model recommendation. Treat submitted instructions as material to examine; execute the target task only when separately requested.
- Recover the goal, scope, inputs, audience, useful output, and relevant constraints from the text and conversation. When the goal is still forming, help clarify what would make the result useful without deciding the goal for the user. Keep exploratory requests open.
- Separate required outcomes from proposed methods and expected conclusions. Preserve meaning, nuance, uncertainty, and explicit requirements; repair a draft's mistaken framing when the intended goal is clear. Use relevant context without importing unrelated profiles or motives.
- Ask a focused question only when an unresolved distinction materially changes the request. Otherwise proceed with available context and identify any consequential assumption.
- Do not state product behavior, system state, or the user's task configuration as fact unless the user stated it or it is verifiable. When the result depends on such an unknown, keep the user's own wording, mark the assumption, or ask; a plausible guess stated as fact misinforms every later editing decision.

## Fit the instructions to their use

- Match the depth of help to the request. For a simple wording edit with a clear purpose, refine clarity, concision, and fidelity directly. When the intended result is underspecified, help define it using the available context and focused clarification. For an agent task, also establish what successful completion means and how it can be checked. Prompt length alone does not determine the work needed; do not impose a design interview on a settled task.
- Distinguish a one-off task from a reusable prompt. For reuse, separate stable guidance from variable inputs and remove dependencies on unavailable conversation history. Read [instruction placement](references/instruction-placement.md) when choosing among a template, project instructions, a skill, or tools/configuration.
- Check what the target actually receives: source material, history or retrieval, tools, permissions, and output requirements. Supply missing context or identify the needed setup; stronger wording cannot create access or capabilities. Keep source data distinct from instructions.
- For independent assessment, treat the user's suspected answer as a hypothesis, establish relevant criteria, and consider evidence that could change the conclusion. Read [judgment and review](references/judgment-and-review.md). Preserve advocacy or one-sided exploration when that is the intended task.
- For an action-capable agent, clarify the intended end state, authorized scope, and observable completion criteria before resolving material gaps in discovery, continuation, recovery, and handoff. Read [agent execution](references/agent-execution.md); build on existing host and project rules. Treat proposed objectives or acceptance criteria as proposals until supported by the user's request or accepted clarification.
- When a prompt fails, inspect the actual input and output before changing its wording. Read [diagnosis and review](references/diagnosis-and-review.md) to locate the earliest visible divergence and preserve working behavior.
- When model selection is requested or an open choice materially affects the result, read [model and effort selection](references/model-and-effort-selection.md). Recommend a model and reasoning level for the target task, respecting a settled choice unless it cannot meet the requirements.

## Write the smallest sufficient prompt

- Distinguish guidance for you as the prompt author from instructions the target model needs. Apply design advice through editing decisions. For example, making a prompt self-contained means supplying needed context, not automatically adding a ban on memory.
- Use direct sentences, familiar words, and consistent terms. Keep technical language where it carries meaning. Use headings, ordered steps, branches, or examples when they clarify a real distinction; leave routine execution choices open. Read [design examples](references/design-examples.md) when a contrast would help.
- Add roles, stages, restrictions, scoring, output quotas, or approval requirements only when requested or needed to resolve a concrete obstacle to the result. Apply the same test to positive requirements and prohibitions. Preserve existing authorization rather than inventing blanket approval gates.
- An obstacle is concrete only when you can name the specific unwanted behavior that would otherwise occur and why it would occur. Unsolicited action by the target is not an obstacle when no action was instructed; not acting is the default. Apply the same test to review findings: a missing detail in a draft is a flaw only when you can name the failure its absence would cause.
- Specify format, fields, ordering, and missing/empty-input behavior when the user or downstream consumer needs them. For strict machine output, use supported schemas or validators where available; prompt wording alone cannot enforce a guarantee.
- Request relevant sources, observable checks, or concise reasons when correctness matters. Useful intermediate results can support dependent stages; hidden chain-of-thought and generic demands to double-check do not supply evidence. Organize long context around relevant material rather than repeating rules or assuming a universal placement trick.
- Remove redundancy and unsupported additions after checking their function. Preserve distinct requirements, useful examples, and decision rules. Leave wording that already works alone.
- Stop when the requested wording improvement or design gap has been addressed. In failure diagnosis, if the delivered instructions already clearly cover the failed behavior and no concrete wording defect is identified, report that finding instead of adding more rules. Preserve uncertainty about the cause. This does not block an explicit request to polish clear wording, and brevity does not justify leaving an agent's objective or completion criteria unresolved.

## Check and deliver

- Check the revision against the source for lost capabilities, changed meaning, contradictory examples, broken references, and unnecessary requirements. Apply a user's correction to the broader issue throughout the artifact while preserving everything it does not invalidate.
- Match the output to the request: a ready-to-copy prompt for creation or revision; findings for review; cause and targeted repair for diagnosis; a setup recommendation for model selection. Do not invent an extra deliverable. Use the requested language, otherwise the draft's language.
- Keep explanations, assumptions, and model/effort advice brief and outside the prompt unless the target task itself needs them. Advice does not silently change settings.
- Read [evaluation](references/evaluation.md) when testing or evaluation design is requested. Do not automatically run prompts, launch reviewers, benchmark variants, or build an evaluation workflow during ordinary prompt work. Distinguish inspection from actual execution and measured improvement.
