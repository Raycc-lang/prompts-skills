---
name: "skill-name"
description: "One sentence on what this does, then one on when to use it. Include the words a user would actually say. If a sibling skill covers an adjacent case, name it here so the agent routes correctly."
---

# Skill Name

One or two lines on the point of this skill — the outcome it produces, not a
restatement of the description.

## When this applies

- Concrete trigger case
- Another trigger case

Not for: <the adjacent case, and which skill handles it instead>

## Preconditions

What must hold before applying. Check these first; if one fails, say so and stop.
Omit this section if there are none.

## Procedure

1. First step, stated as an action.
2. Second step. Mark any step that must adapt to context, and how.
3. Final step — runtime check: verify the result in the world (run it, observe
   output, or execute a test), never by rereading.

## Output

What a good result looks like. Be specific about format, length, and what must
always be included.

## Notes

- Edge cases, failure modes, things to avoid; which parts adapt and when to
  abandon the skill.
- Provenance: for each non-obvious rule, note its source — an observed success
  or failure, a user requirement, a platform contract, or an external spec.
  Rules without a recorded source cannot be safely revised or deprecated later.
- Portability: mark which steps are portable procedure, which are tool- or
  environment-specific, and which are local workarounds for a known model
  weakness (label those — a patch tuned to a weak model can hurt stronger ones).
- Large reference material goes in `references/` and is read only when needed —
  keep this file short so it's cheap to load.
