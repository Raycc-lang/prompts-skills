# AGENTS.md — prompts-skills

## What this repo is

The source of truth for Ray's agent skills and prompts.

## meta/ — maintenance records, not part of the skill

`meta/<skill-name>/` holds the scaffolding used to maintain a skill: evidence
(the empirical basis for rules), provenance, and revision notes. This material is used only when **creating or modifying a
skill**; the model running the skill doesn't need it. Therefore:

- **Never install meta/ when installing a skill.** The install unit is the
  `skills/<name>/` folder itself — copy it wholesale. Since meta/ sits outside
  the skill folder, it naturally never travels with the skill: no exclusion
  logic is needed, and don't copy it into any runtime skill directory.
- The skill proper (`SKILL.md` + `references/`) carries only what the runner
  needs: no evidence citation tags (e.g. `[F3]`), no inline provenance, no
  portability markers in the body. All of that goes to `meta/<skill-name>/`.
- Before changing a skill rule, check the matching evidence and notes in
  `meta/<skill-name>/` first: why the rule exists, and which changes have
  already been rejected.

## Entry points for modifying skills

Use `ray-prompt-wording` (Ray’s Prompt Wording) to design, revise, diagnose, or
review model instructions; distinguish one-off and reusable use; choose instruction
placement; and recommend a model and reasoning level. It includes guidance for
independent analysis and agentic tasks. Prompt evaluation is available when requested;
ordinary prompt work does not automatically execute the target task or run benchmarks.
Use `skill-authoring` for full skill-package construction, deployment, and runtime
or routing diagnosis after the required capability and placement are understood.
Their maintenance records live at `meta/skill-authoring/` and
`meta/ray-prompt-wording/`.

## Deployment

Sync on demand to the other agents Ray uses, for example:

- `~/.agents/skills/`
- `~/.workbuddy/skills/`
- `~/.evox/agent/skills/` (leave the host-added file `.evox-skill-source.json` untouched)
