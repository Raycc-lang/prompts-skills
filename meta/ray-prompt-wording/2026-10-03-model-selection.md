# Restore model and reasoning-level selection

Recorded: 2026-10-03 (Asia/Shanghai).

## Correction and scope

Ray identified the exclusion of model selection as a mistake and requested restoration and improvement of the old guidance in both the installed skill and GitHub. The earlier scope reduction conflated choosing an execution setup with running prompts or benchmarking them. This correction supersedes the model-selection exclusion described in the 2026-10-02 rename notes; the narrower wording purpose, outcome clarification, brevity preference, and execution boundary remain.

## Changes and rationale

- Include concrete-task model and thinking-level requests in the description and repository routing. Add a conditional reference from SKILL.md and align UI metadata and README.
- Restore the old capability-before-difficulty distinction and separate model choice from effort. Assess the task the prompt will perform, not how easy its wording is.
- Reduce the old guide to 472 words. Replace a broad mapping of tool use, long tasks, and unfamiliar work to high effort with task-dependent starting points. Compare combined model/effort choices, starting from supported defaults; keep separate speed, reasoning-mode, and response-length controls distinct.
- Respect quality, speed, cost, and subscription usage priorities. Check current official product facts and available account evidence rather than hard-code model rankings or assume API controls apply everywhere.
- Give one primary recommendation with a brief reason. Keep it outside the prompt, respect settled choices, and supply advice alone when that is all the user requested. Selection does not silently change settings or launch tests.

Sources checked: the archived model-and-effort-selection.md; the existing evidence, revision, and rename records; Ray's explicit correction; OpenAI's [model guide](https://openai.com/index/practical-guide-building-gpt-6/), [model selection guidance](https://developers.openai.com/api/docs/guides/model-selection), and [reasoning guide](https://developers.openai.com/api/docs/guides/reasoning). Official guidance supports balancing capability, quality, time and usage, and checking product-specific settings. These are practitioner recommendations and user requirements, not empirical validation of this skill.

## Checks and behavioral sample

The installed package passed quick_validate.py, diff whitespace checks, and reference/UI/icon checks. Final package contents are compared across both destinations.

One fresh agent was given the candidate package path and two independent requests, without the author's explanation or expected answers. The supplied hypothetical catalog, rather than public model facts, governed selection. Neither target task was executed.

**A — open choice and uncertain diagnosis.** Request: write a prompt to diagnose intermittent queue backlog using a repository, read-only logs and tests, with evidence and a proposed fix; recommend a model/effort. Swift was described as fast and good at bounded tasks, with tools and low/medium/high; Deep as stronger at conflicting evidence and unfamiliar code, with tools and low/medium/high/max. Both had sufficient context and medium defaults. Quality took priority over speed.

Actual recommendation: Deep, high effort, based on uncertainty and unfamiliar code; no clear reason to start at max. Actual prompt:

> Diagnose the intermittent queue backlog using the repository, read-only logs, and available tests. Identify the cause, support the diagnosis with evidence, state any remaining uncertainty, and propose a fix.

**B — settled choice and wording only.** Request: shorten a repetitive meeting-summary prompt while retaining decisions, action items, owners and deadlines where stated; Swift at low was already chosen.

Actual output:

> Briefly summarize the meeting notes below, identifying decisions, action items, and their owners and deadlines where stated.

No unsolicited model advice accompanied B.

These outputs exercise the restored recommendation and settled-choice boundary. They are a small candidate-only smoke test, not an old-versus-new benchmark, proof of reliable host selection, or evidence about real models' relative performance. Current-product verification and actual account availability were not behaviorally tested by this fictional catalog.
