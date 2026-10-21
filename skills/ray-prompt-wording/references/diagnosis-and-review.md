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

If the delivered instructions already specify the failed behavior clearly and the evidence reveals no ambiguity, omission, or conflict to repair, say so. Do not manufacture a wording defect or infer a hidden model cause. Identify the next discriminating check only when useful, such as inspecting delivered context or comparing behavior on matched inputs. An optional wording polish can still satisfy a separate editing request, but do not present it as a demonstrated behavioral repair. Missing agent objectives or completion criteria remain design gaps when their absence changes what work the agent should perform or when it should stop.

For review or grading, compare the draft against the user's requirements, not a generic ideal prompt. Identify lost capabilities, changed meaning, unsupported assumptions, contradictions, unnecessary work, and failures of the output contract. Give concrete findings; avoid invented scores. Rewrite only when requested.

During any revision, account for each existing capability before removing it. Shorter wording is not evidence that the same behavior remains. Check examples, placeholders, resource links, and conditional paths as well as the main prose. Keep a detailed preservation map for substantial changes; show the user only the level of detail the request needs.
