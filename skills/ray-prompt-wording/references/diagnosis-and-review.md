# Diagnose and review by function

For a reported failure, inspect the actual prompt, delivered context, output, and available tool events. Locate the earliest visible difference from the intended behavior. If evidence is incomplete, separate observations from competing explanations; do not invent the model's hidden reasoning.

Choose the repair by the cause:

- Missing or truncated information: repair delivery, retrieval, or incomplete-input behavior.
- Conflicting instructions or examples: resolve their scope and priority.
- Correct format but wrong judgment: clarify the missing criterion or distinction.
- Tool, permission, or budget failure: repair the setup or identify a viable fallback.
- Inconsistent similar cases: inspect ambiguous conditions, examples, and variability; compare a nearby case that should produce a different action.
- Goal already met: preserve the behavior and make only the requested improvement.

Explain why the proposed change addresses the observed problem. Repair the responsible rule or condition rather than adding a warning for every incident. Keep detailed failure history in maintenance material.

For review or grading, compare the draft against the user's requirements, not a generic ideal prompt. Identify lost capabilities, changed meaning, unsupported assumptions, contradictions, unnecessary work, and failures of the output contract. Give concrete findings; avoid invented scores. Rewrite only when requested.

During any revision, account for each existing capability before removing it. Shorter wording is not evidence that the same behavior remains. Check examples, placeholders, resource links, and conditional paths as well as the main prose. Keep a detailed preservation map for substantial changes; show the user only the level of detail the request needs.
