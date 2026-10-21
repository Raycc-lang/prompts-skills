# Write for an action-capable agent

Build on the target's existing capabilities and instructions. Include the execution decisions that are unresolved and matter to this task:

- **Result and scope:** translate the intended objective into an observable end state and identify the authorized changes. Recover these from the request and context; ask about consequential unresolved choices or offer labeled proposals without silently choosing the user's priorities. Distinguish required properties from suggested implementation. A task such as "improve this app" may need objective clarification even when its wording is concise.
- **Discovery:** have the agent inspect relevant files, instructions, tools, and checks when implementation depends on them. Let observed facts update assumptions while preserving the user's requirements.
- **Continuation:** for a completion request, carry the work through implementation and appropriate verification. For an analysis-only request, deliver analysis. Do not turn either into the other.
- **Recovery:** diagnose and fix recoverable failures within scope. Continue independent work when a missing decision blocks only part of the task; ask when it actually prevents progress.
- **State:** preserve unrelated user changes. Where credentials are needed, allow authorized use without exposing their values in output, logs, or commits.
- **Completion and handoff:** define evidence that would establish the intended result, using checks proportional to the task. Distinguish a produced artifact, verified behavior, and any separately authorized publication or submission. An attempted action or passing unrelated test does not establish completion. Define how to report partial results or an unavailable check; report what changed, what was actually checked, and remaining limitations or blockers.

Avoid copying every item into every prompt. Existing host or project policy remains the source of shared authorization rules. Carry forward permission already given; do not add blanket approval requirements. Text cannot grant unavailable access or enforce security boundaries by itself.
