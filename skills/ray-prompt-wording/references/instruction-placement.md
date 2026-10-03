# Choose the form and home

Use the user's requested deliverable. When its form is open, choose by how long the instructions remain useful and which tasks need them:

- **One-off prompt:** include this task's facts, inputs, and desired result directly.
- **Reusable prompt template:** keep stable instructions and name the changing inputs with clear placeholders, such as `{{notes}}`. Include the context future runs need; avoid references to this conversation. A repeated task does not automatically need a skill.
- **Project instructions:** place stable facts, requirements, and pointers needed across project tasks in scoped AGENTS.md or the host equivalent. Inspect existing guidance before duplicating or contradicting it.
- **Skill:** use for reusable procedures or knowledge that should load only for a recognizable task class. Route full package construction to skill authoring when available; otherwise describe the required package work without pretending it is installed.
- **Tools or configuration:** use schemas, validators, formatters, tests, or permissions for requirements they can enforce. Keep relevant commands and recovery decisions in instructions.
- **Maintenance records:** keep source evidence, design rationale, and failure history outside the target's routine prompt.

Split mixed needs across the appropriate homes. A monthly release procedure can be a skill while a supported-runtime requirement belongs in project context. Keep today's specific fix in its prompt. Recommending placement does not authorize editing every location.

For reusable instructions, check both an ordinary input and a relevant change in input that should change the action. Preserve useful variation instead of hard-coding one example. Add missing-input behavior only where it affects use.
