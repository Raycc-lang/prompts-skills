# Choose a model and reasoning level

Recommend a setup for the task the prompt will run, not for the effort of wording it.

## Establish the available choices

Use the user's named candidates and target product. Check current official documentation for model capabilities, supported reasoning levels, defaults, and relevant limits; use available session evidence for account access. Chat, Work, Codex, and API options can differ. Do not substitute API pricing or settings for a subscription product's usage and controls.

Resolve missing context from the conversation first. Ask a focused question only when the answer changes the recommendation; otherwise state the assumption and give a useful provisional choice. If current facts cannot be verified, distinguish a model-class recommendation from confirmed availability. Do not invent permanent rankings or precise performance gains.

## Match the model to the task

Check required tools, modalities, context capacity, and execution environment first. Then judge the actual difficulty: depth of reasoning, ambiguous evidence, dependent decisions, context to keep consistent, and how hard errors are to detect or repair. Prompt length, output length, and number of tool calls are weak proxies.

Choose among capable models using the user's quality, speed, cost or usage priorities. Favor an efficient model for bounded work with easy checks; favor stronger or specialized capability when nuanced judgment, diagnosis, or difficult recovery drives success. If quality takes priority, do not automatically optimize for the cheapest option. Consider likely retries and rework as well as the first run.

## Choose reasoning effort separately

Start from the model's supported default and adjust to the task. Treat these as starting points, not fixed assignments:

- **Low:** direct transformations, extraction, or routine execution with clear checks.
- **Medium:** several constraints, moderate analysis, or planning with manageable uncertainty.
- **High:** difficult diagnosis, conflicting evidence, or interacting decisions that need sustained reasoning.
- **Extra-high / maximum:** unusually demanding work where added reasoning plausibly justifies its delay and usage; prefer evidence from prior attempts when available.

Use the target product's actual labels. A stronger model at lower effort may be preferable to a weaker model at maximum effort; compare the combined setup. Tool use, long runtime, or importance alone does not determine the level. Keep reasoning effort distinct from response length and separate speed or reasoning-mode controls.

When an attempt fails, distinguish insufficient reasoning from missing evidence, tools, permissions, or an unclear goal. Fix the actual bottleneck. More thinking cannot supply missing access or guarantee correctness.

## Give a usable recommendation

Name one primary model and supported reasoning setting, then briefly explain the decisive task features and trade-off. Add an alternative or an escalation condition only when it helps the choice. Separate verified product facts from your judgment. Keep advice outside the prompt; recommend rather than silently changing settings. Do not turn selection advice into an automatic benchmark or execution workflow.
