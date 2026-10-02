# Instructions for action-capable agents

Load when the target can inspect a workspace, call tools, edit files, or change
external state. Establish the execution behavior the task needs, using the target's
existing instructions and capabilities as the starting point.

## Resolve the uncovered execution decisions

- **End state and scope:** state what must be true when finished and which changes
  are authorized. Distinguish required properties from suggested implementation.
- **Discovery:** when implementation details are uncertain, inspect the actual files,
  project instructions, tools, and checks. Let runtime evidence update assumptions
  while preserving explicit user requirements.
- **Continuation and recovery:** when completion is requested, carry the work through
  implementation and relevant verification. Diagnose and repair recoverable failures
  within scope; ask for a decision, permission, or input when it actually blocks work.
- **State boundaries:** preserve unrelated user changes. Where the task uses secrets,
  allow authorized use while keeping their values out of output, logs, and commits.
- **Completion:** choose observable checks that establish the requested behavior.
  Use failures to select repair, a valid fallback, or a specific blocked report.
- **Handoff:** report material changes, checks actually run, and remaining limitations.

Include the items that close a real gap in the task's operating context. Existing
project or host rules remain the source of shared policy; a prompt can refer to the
relevant command or procedure without reproducing it. Host authorization still governs
external cost, destructive actions, and work outside the user's granted scope.
