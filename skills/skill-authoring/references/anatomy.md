# Skill anatomy

Skeleton for the artifact this skill produces, plus description examples.
Load this when authoring; SKILL.md carries the rules.

## Folder layout

```
skills/<skill-name>/
  SKILL.md              # frontmatter + procedure; stays short
  references/           # heavy material, loaded on demand
    evidence.md         # optional: findings the rules rest on
    notes.md            # persistent revision knowledge — phenomenon, root cause,
                        # current rule, rejected changes; created per Revise trigger
    ...                 # optional: guides, templates, schemas
```

`name` in the frontmatter must match the folder name.

## SKILL.md skeleton

```markdown
---
name: "<folder-name>"
description: "<What it does, in verbs.> Use when the user <trigger cases, in the
words they would actually say>. Not for <adjacent case, in the user's words>."
when_to_use: "<The full boundary: when to load this skill and when not to —
state the adjacent cases it does not cover, as cases, never as the name of
another skill.>"
---

# <Skill Name>

One or two lines: the outcome this skill produces — not a restatement of the
description.

## When this applies

- Concrete trigger case
- Another trigger case

Not for: <adjacent case>.

## Preconditions

What must hold before applying. Check these first; if one fails, say so and stop
rather than executing steps whose assumptions are broken.

## Procedure

1. Step, stated as an action.
2. Step. Mark steps that must adapt to context, and how.
3. ...
N. Runtime check: verify the result in the world — run it, observe output, or
   execute a test. Never "reread and confirm."

## Pitfalls

- Symptom → cause → avoidance. (Provenance: the traceable source — the run,
  requirement, or contract that produced this.)

## Notes

- Which parts are invariant and which adapt; when to abandon the skill.
- Heavy reference material lives in `references/`.
```

Every section is optional except frontmatter, title, procedure, and the runtime
check. Never emit a section to fill the skeleton — "nothing to report" is legal.
This repo's `templates/skill-template/SKILL.md` follows this skeleton; keep the
two aligned when either changes. Working budget: bodies in this evidence base
average 45–129 lines [W6]; past which material usually belongs in `references/`.

## Description examples

The description is the only text the router sees. It must separate this skill
from its neighbors using likely user wording.

**Works** — verbs, trigger language, explicit boundary:

> "Convert spreadsheet workflows into verified openpyxl/pandas scripts. Use when
> the user asks to automate an Excel task, convert formulas to Python, or batch
> process .xlsx files. For reading or explaining a spreadsheet by hand, no skill
> is needed."

**Fails** — vague, no trigger words, no boundary:

> "A helpful skill for working with data files and making the user more
> productive with spreadsheets."

**Fails** — overlaps a sibling with no stated boundary, guaranteeing mis-routing:

> "Improves prompts and helps write skills."

Bilingual users: include both languages' trigger words when both occur
(e.g., "写技能 / author a skill").

Pair the description with `when_to_use` (this repo's convention): the
description carries the routing triggers; `when_to_use` carries the full
boundary in sentence form, including negatives. Hosts that do not
read `when_to_use` ignore it harmlessly — but do not rely on that: any wording
the router must see stays in the description.

## Test proposal template

Attach to every authored or distilled skill:

- **Task 1 (typical):** <representative request> — pass when <observable result>.
- **Task 2 (edge):** <boundary case from the scope section> — pass when the skill
  either handles it or explicitly declines.

### External routing test

Routing can only be tested outside the skill, after installation. Run it in a real
session and record outcomes:

- At least three positive phrasings, in the user's languages.
- At least two near-boundary negatives that should route elsewhere.
- At least one confuser per adjacent case named in the non-triggers.
- For each case: expected skill, observed skill, miss or false alarm.
- Record the sibling set and library size the test ran against — results are
  library-relative, and usage precision degrades as pools grow [F5].

Description design improves discrimination but cannot control the retriever,
candidate generation, or selection policy; treat persistent mis-routing in a large
library as a library problem, not a wording problem (design judgment; no cited
study measures the description-vs-retriever tradeoff).
