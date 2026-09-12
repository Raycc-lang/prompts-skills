# Choosing a model and reasoning effort

Load this when the user asks which model, agent mode, or reasoning/thinking level
should run a prompt, or when the execution choice is still open and materially affects
cost, latency, or the chance of completing the task correctly. Keep the recommendation
outside the copyable prompt unless the prompt itself controls model routing.

## 1. Separate capability from difficulty

Check hard requirements first. A model is not a candidate if it lacks a needed tool,
context window, modality, structured-output feature, coding/agent environment, or other
execution capability. More reasoning effort cannot repair a missing capability, missing
input, or unavailable permission.

Then assess the task itself. Use the factors that actually create work rather than
judging by prompt length or the apparent size of the final edit:

- **Reasoning depth:** direct transformation versus diagnosis, planning, architecture,
  trade-offs, or several coupled constraints.
- **Uncertainty:** whether the answer is already in the input or must be discovered by
  inspecting a workspace, searching sources, probing APIs, or interpreting failures.
- **Action horizon:** one response versus a sequence of tool calls, edits, tests, and
  recovery steps whose later choices depend on earlier results.
- **Context burden:** small self-contained input versus many files, long context, mixed
  evidence, or state that must remain consistent across steps.
- **Verification and consequence:** how easy mistakes are to detect and undo, and how
  expensive a weak first attempt would be in time, money, external side effects, or
  rework.

A task can be hard even when the code change is tiny. For example, a configuration edit
that first requires repository inspection, live capability discovery, secret handling,
and end-to-end verification has a higher execution burden than its diff size suggests.

## 2. Choose the model by the bottleneck

When the available choices are known, compare the actual candidates rather than using
a permanent model ranking. Model names and product tiers change.

- Prefer a fast or inexpensive capable model for bounded, well-specified work with
  short context, little branching, and cheap verification.
- Prefer a stronger general reasoning, coding, or agent model when success depends on
  diagnosis, unfamiliar code, several dependent tool steps, ambiguous evidence, or
  recovery from failures.
- Prefer a specialized model when the task's bottleneck is a specialization such as
  code execution, vision, very long context, or another capability that is materially
  stronger than the general alternatives.
- Account for total expected work, not token price alone. A cheaper run that is likely
  to require a second full attempt can cost more than using the stronger model first.

Do not assume that raising reasoning effort on a weaker model makes it equivalent to a
stronger model. When comparative evidence is unavailable, state the recommendation as
a capability-based judgment rather than inventing a precise performance ranking.

## 3. Choose reasoning effort separately

Map the host's available effort levels to the task. Names such as low, medium, high,
or extra-high are product-specific; use the closest available setting.

- **Low / fast:** direct extraction, rewriting, formatting, simple lookup from supplied
  material, or deterministic edits with obvious checks.
- **Medium:** normal professional work with several constraints, moderate tool use, a
  small amount of diagnosis, or a clear implementation plan that still needs judgment.
- **High:** debugging an unknown cause, architecture or design choices, long-horizon
  agent work, several interacting constraints, independent evaluation, unfamiliar
  repositories, or failures that require diagnosis and recovery.
- **Highest / extra-high:** reserve for unusually difficult work where additional
  reasoning has plausible value: hard research synthesis, difficult math or algorithms,
  subtle architecture, severe ambiguity, or a failed high-effort attempt. Do not choose
  it merely because the task is important or the output is long.

Start at the level that minimizes expected total effort. Escalate when the observed
failure points to insufficient reasoning. If the failure is missing context, tools,
permissions, or domain knowledge, fix that bottleneck instead of merely increasing the
thinking level.

## 4. Make the recommendation useful

When model or effort selection is requested or materially useful, give a concise
execution recommendation after the prompt or artifact:

- the recommended available model or model class;
- the reasoning/thinking level;
- the two or three task features that drive the choice;
- a cheaper/faster alternative when it is genuinely viable, or an escalation condition
  when the first choice may be insufficient.

Do not produce a ceremonial ranking of every model the user mentioned. Recommend one
primary setup unless a real trade-off makes two options useful. If current availability
or model capabilities are uncertain, verify them when possible or state that limitation
rather than guessing.