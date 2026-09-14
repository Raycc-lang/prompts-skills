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

Use `prompt-engineering` to design prompts and decide whether guidance belongs
in a prompt, project context, or skill. Use `skill-authoring` for creating,
diagnosing, revising, or reviewing skill packages; standalone wording edits use
`prompt-engineering`.
Their own maintenance records live at `meta/skill-authoring/` and
`meta/prompt-engineering/`.

## Deployment

Sync on demand to the other agents Ray uses, for example:

- `~/.agents/skills/`
- `~/.workbuddy/skills/`
- `~/.evox/agent/skills/` (leave the host-added file `.evox-skill-source.json` untouched)
