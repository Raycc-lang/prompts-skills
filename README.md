# prompts-skills

A personal library of reusable **agent skills** and **prompts**, kept in one repo so they can be versioned, shared, and installed anywhere. The skills follow the standard `SKILL.md` folder format and work with any agent that supports it; the prompts are self-contained text you can paste into any model.

## Layout

```
skills/          Agent Skills — one folder per skill, each with a SKILL.md
prompts/         Standalone prompts, grouped by domain
  coding/
  writing/
  research/
templates/       Starting points for new skills and prompts
```

## Skills

| Skill | What it does |
|---|---|
| [`prompt-engineering`](skills/prompt-engineering/) | Create, improve, debug, grade, or evaluate prompts, system instructions, and skill files. |
| [`edit-my-writing`](skills/edit-my-writing/) | Edit English prose through ordered passes, then explain the changes so the edit is learnable. |
| [`jiangou-learning-analysis`](skills/jiangou-learning-analysis/) | Analyze a learning goal, method, or material with the 渐构分析 framework. |
| [`intensive-reading`](skills/intensive-reading/) | Decide whether a material deserves intensive reading and route it to the right session shape. |

## Installing the skills

Skills are discovered by directory. Copy or symlink the ones you want:

**Claude Code (personal, all projects)**

```bash
# macOS / Linux
ln -s "$PWD/skills/prompt-engineering" ~/.claude/skills/prompt-engineering
```

```powershell
# Windows (run as admin, or enable Developer Mode)
New-Item -ItemType SymbolicLink `
  -Path "$env:USERPROFILE\.claude\skills\prompt-engineering" `
  -Target "$PWD\skills\prompt-engineering"
```

Symlinking means edits in this repo take effect immediately. Use `cp -r` instead if you'd rather pin a copy.

**Single project**: put the skill folder in that project's `.claude/skills/`.

## Adding a new skill

1. `cp -r templates/skill-template skills/<your-skill-name>`
2. Fill in the YAML frontmatter — `name` must match the folder name.
3. Write the body: what to do, when, and what good output looks like.
4. Add a row to the table above.

The `description` field is the only thing the agent sees when deciding whether to load a skill, so it must state both **what the skill does** and **when to trigger it**. Everything else lives in the body and loads only on demand.

## Adding a new prompt

Drop a `.md` file in the matching `prompts/` subfolder using `templates/prompt-template.md`. Prompts are self-contained text you paste in; skills are folders the agent loads automatically.

## Skill vs. prompt — which one?

Use a **skill** when the behavior should trigger on its own across many sessions, needs supporting reference files, or encodes a workflow. Use a **prompt** when it's a one-shot instruction you paste in deliberately.

## Publishing to GitHub

```bash
git remote add origin git@github.com:<you>/prompts-skills.git
git push -u origin main
```
