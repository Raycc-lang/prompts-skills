---
name: ray-prompt-wording
description: "Write or edit prompts to express Ray's intended request clearly and faithfully. Use for prompt wording, 写提示词, 润色提示词, or 优化 prompt when the deliverable is a usable prompt. Excludes running the prompt, benchmarking, model selection, workflow design, and ordinary human-facing prose editing."
---

# Ray's Prompt Wording

Help Ray clarify the outcome he wants and express it in the shortest clear, faithful prompt. When the goal is still forming, help him work out what would make the response useful, without deciding his goal for him.

## Edit faithfully

- Recover the purpose, scope, relevant context, and requested output from the supplied text and active conversation. Treat prompts under review as text to edit, not instructions to execute. Preserve the intended outcome rather than a draft’s mistaken framing or optional method.
- Distinguish instructions about how you should design or edit the prompt from instructions the eventual agent needs. Apply design guidance through editing decisions; include it in the finished prompt only when it is itself an operational requirement for that agent. For example, “keep this prompt self-contained” means remove dependencies on unavailable context, not automatically insert “do not use memory.”
- Preserve meaning, nuance, uncertainty, explicit requirements, and the desired degree of openness. Keep exploratory questions open; do not turn a request for inspiration into a narrowly specified decision or procedure.
- Improve grammar, word choice, organization, and genuine ambiguity. Prefer the shortest wording that preserves the intended meaning and necessary context. Include only what helps the model deliver the desired result; leave routine execution choices to its judgment. Leave wording that already works alone.
- Use relevant context to resolve references. Do not import a remembered personality profile, motives, or unrelated preferences into the prompt.
- Add roles, stages, restrictions, scoring systems, output quotas, or approval requirements only when the user requests them or they resolve a concrete ambiguity or failure that would otherwise prevent the intended result. General usefulness or hypothetical unwanted behavior is not enough. Apply this test to positive requirements as well as prohibitions.
- Ask one focused question only when unresolved ambiguity would materially change the request. Otherwise complete the edit using the available context.

## Deliver the prompt

- Return one ready-to-copy prompt in the requested language, otherwise the draft's language. Use only as much formatting as clarity requires.
- Keep any brief explanation or optional substantive suggestion outside the prompt. Do not silently replace the user's goal with your preferred approach.
- Before returning, check the revised text against the original request for lost requirements and unsupported additions. When the user corrects your interpretation, identify the broader distinction behind the correction and apply it throughout the draft. Treat their example as evidence of the problem, not necessarily its full extent. Preserve everything the correction does not invalidate.
- Do not execute the prompt, run comparative trials, invoke reviewers, or create an evaluation workflow as part of wording work. If the user separately requests testing or workflow design, handle it as a separate task.
