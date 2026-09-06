# Packaging a skill

Load when turning the procedure into a distributable folder. Structure serves the
work: use the sections that make the runner's next decision clear.

## Install unit

```text
skills/<name>/
  SKILL.md          # entrypoint: purpose, decisions, resource-loading cues
  references/       # optional knowledge, examples, schemas, task-specific guides
  scripts/          # optional executable helpers with dependencies and invocation
  assets/           # optional templates or other inputs used to produce artifacts

meta/<name>/        # outside install unit: evidence, revisions, evaluation fixtures
```

Copy the entire skill folder when installing. Resolve bundled resources relative
to the skill, and task outputs relative to the chosen workspace. Document a genuine
host dependency instead of pretending every implementation is portable.

For consolidation, inventory what the existing workflow reads and executes. Preserve
useful knowledge and executable assets, including private knowledge when the user
requests a private package. Keep archives and authoring records outside the install
unit. Verify relocation rather than relying only on a search for absolute paths.

## Optional starting structure

```markdown
---
name: "<folder-name>"
description: "<What it accomplishes>. Use when <recognizable requests>. <Relevant boundary, if ambiguous>."
---

# <Name>

<Useful outcome and any essential context.>

## Procedure

1. <Inspect the input that determines the approach; load a reference if needed.>
2. <Choose the action using explicit criteria; give the alternative when they fail.>
3. <Produce the result and check it using criteria appropriate to the task.>

## Example or supporting material

<Include when it clarifies a difficult choice; link larger material with a loading cue.>
```

The skeleton is not a required output schema. A reference lookup skill may need
a selection guide rather than a sequence.
Leave out sections that do not help the runner. Do not expose authoring questions,
provenance tables, or evaluation rubrics as user-facing output by default.

## Description

On hosts that expose name/description before loading the body, those fields carry
the routing cues. Name the task and likely user wording. Add adjacent exclusions
where confusion is plausible; avoid enumerating every conceivable non-use.

- Useful: "Automate repeated Excel transformations with Python. Use for converting
  formulas into scripts or batch-processing workbooks; excludes controlling a live
  Excel window."
- Weak: "A helpful data productivity skill."

For bilingual use, include the user's actual trigger phrases when useful. This
repository also permits `when_to_use`; keep essential cues in `description` for
hosts that ignore the extra field. Follow the target host's supported frontmatter.

Describe boundaries as tasks. An explicit dependency on another skill is acceptable
when required and available: state why it is needed and what to do if unavailable.
Persistent misrouting may come from the host's selection policy or library rather
than the text. Test selection in the actual library before claiming a routing fix.
