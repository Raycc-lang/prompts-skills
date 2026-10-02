# Ray’s Prompt Wording — rename and design notes

Recorded: 2026-10-02 (Asia/Shanghai).

This is maintenance documentation, outside the installable skill. It records why the skill changed, what changed, and what the available evidence does and does not establish.

## Current identity and purpose

- Display title: **Ray’s Prompt Wording**.
- Skill name and GitHub folder: `ray-prompt-wording`, `skills/ray-prompt-wording/`.
- Former name and folder: `prompt-engineering`, `skills/prompt-engineering/`.
- Deliverable: a usable prompt that expresses Ray’s intended request clearly and faithfully.

## Earlier rename and simplification

The installed personal skill had already been renamed before this update; GitHub still held the broad Prompt Engineering version. The earlier installed change is recorded on 2026-10-01 in Asia/Shanghai time. This update documents that earlier decision and brings the GitHub source into line with it, rather than presenting the rename as a new decision made today.

Ray wanted help wording the prompt he intended. The older name and package also covered diagnosis, grading, model and reasoning-effort selection, instruction placement, execution workflows, and evaluation. That scope overstated this skill’s intended role and could turn a wording request into a larger project.

Ray reported that previous use seemed to improve formatting more than the substantive result, while questioning whether the evaluation criteria were adequate. That is user feedback about usefulness, not a controlled finding that the skill had no effect. He also rejected automatically running a prompt repeatedly as part of a wording task.

The earlier revision therefore narrowed the entrypoint and description to faithful prompt wording; retained meaning, nuance, uncertainty, openness, and useful clarification; and removed runtime routing to the broad execution, evaluation, judgment, model-selection, and worked-example references. Separately requested testing or workflow design remains a separate task.

## What prompted the 2026-10-02 changes

In an English-coaching prompt revision, the assistant loaded the wording skill but still:

1. Preserved a draft’s word-finding framing after the intended goal was broader improvement of expression.
2. Copied the user’s instruction about designing a stateless prompt into the finished prompt, adding prohibitions about memory, profiles, and other hypothetical behavior.
3. Made local repairs after corrections but left related author-context wording, including a reference to previous feedback.

The user accepted a later, simpler revision and requested updates to both the installed skill and GitHub, with this rationale recorded. The examples show failures in that conversation; they do not establish a precise internal cause or a general failure rate.

The existing skill already prohibited unsupported restrictions and required corrections across the draft. Those failures were not solely missing instructions. The distinction between guidance for the prompt writer and instructions for the eventual agent was less explicit.

## Instruction changes and reasons

| Change | Reason |
|---|---|
| Preserve the intended outcome rather than a draft’s mistaken framing or optional method. | Faithful editing should preserve the user’s goal, not lock in a draft’s implementation choice. |
| Separate prompt-design guidance from operational instructions for the eventual agent. | Apply design decisions through the artifact rather than copying the authoring discussion into it. |
| Add the example that a self-contained prompt should remove unavailable-context dependencies, rather than automatically add a memory prohibition. | Make the distinction recognizable without importing the whole incident into runtime instructions. |
| Admit added roles, stages, restrictions, quotas, scoring, and approvals only when requested or needed to resolve a concrete obstacle to the intended result. | Potential usefulness or imagined unwanted behavior does not justify more requirements. |
| Apply the same admission test to positive requirements and prohibitions. | Rephrasing an unnecessary ban positively does not make it useful. |
| Interpret corrections at the level of the broader distinction and apply them throughout the draft. | A cited sentence may illustrate a class of errors, rather than exhaust the correction. Preserve unaffected content. |

The revised skill remains concise. Its existing scope, faithful-editing guidance, clarification policy, and delivery instructions are otherwise retained. Its description and UI name remain aligned with the narrower task.

## Repository and installation changes

- Publish identical current `SKILL.md`, UI metadata, and icon files in the installed personal package and `skills/ray-prompt-wording/`.
- Rename `meta/prompt-engineering/` to `meta/ray-prompt-wording/`, preserving the historical records and experiments.
- Preserve the former runtime under `legacy-runtime/` here, with its old entrypoint renamed to `entrypoint.md`. It is historical material, not an active skill.
- Update README discovery and installation examples, AGENTS routing, and the skill-authoring description’s reference to the wording skill.
- Keep historical terminology inside dated records. Those records describe the versions that existed then, not the current runtime contract.
- Do not change unrelated English-learning prompts or deploy to other agents’ local installations as part of this update.

## Validation and limits

Validation for this update covers the skill’s frontmatter and naming, agreement between the personal and GitHub package files, UI/resource paths, active references to the renamed skill, preservation of historical files, and diff whitespace. The final deployed content is checked after saving both destinations.

The change is grounded in explicit user corrections and inspection of the actual instruction text. No new target-prompt executions, independent behavioral trials, or old-versus-new benchmark were run. Structural validation and the user’s acceptance of a revised coaching prompt do not establish that the updated skill reliably prevents these failures in future sessions.
