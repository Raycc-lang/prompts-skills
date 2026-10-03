# Write for an action-capable agent

Build on the target's existing capabilities and instructions. Include the execution decisions that are unresolved and matter to this task:

- **Result and scope:** state what should be true when finished and what changes are authorized. Distinguish required properties from suggested implementation.
- **Discovery:** have the agent inspect relevant files, instructions, tools, and checks when implementation depends on them. Let observed facts update assumptions while preserving the user's requirements.
- **Continuation:** for a completion request, carry the work through implementation and appropriate verification. For an analysis-only request, deliver analysis. Do not turn either into the other.
- **Recovery:** diagnose and fix recoverable failures within scope. Continue independent work when a missing decision blocks only part of the task; ask when it actually prevents progress.
- **State:** preserve unrelated user changes. Where credentials are needed, allow authorized use without exposing their values in output, logs, or commits.
- **Completion and handoff:** select observable checks for the requested behavior; report what changed, what was actually checked, and remaining limitations or blockers.

Avoid copying every item into every prompt. Existing host or project policy remains the source of shared authorization rules. Carry forward permission already given; do not add blanket approval requirements. Text cannot grant unavailable access or enforce security boundaries by itself.
