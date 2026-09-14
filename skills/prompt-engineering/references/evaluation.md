# Testing prompt behavior

Load for evaluations and important/repeated prompt changes. Scale the test to the
claim; keep evaluator instructions separate from the prompt being tested.

## Establish what is being tested

Record the task, expected behavior, important failure, and comparison condition.
For improvements/debugging, compare original and candidate. For a new prompt, compare
against a straightforward baseline when claiming an improvement rather than mere
contract satisfaction. Hold model, inputs, tools, and generation settings comparable.

If the intervention changes context assembly, retrieval, or output controls, record
that as part of the treatment. Do not attribute the whole result to wording.

For a prompt-engineering skill, there are two outcomes: the prompts it produces and
the behavior those prompts elicit from a later model. Inspect both before claiming
that the authoring skill has improved.

## Build discriminating cases

- Start with a typical case and the condition that changes the right action.
- Include unknown/empty inputs and relevant instruction conflicts or hostile source
  text when those occur in deployment. Avoid unrelated adversarial cases.
- Use concrete expected decisions and user-approved examples for subjective qualities.
  A schema check alone does not establish factual or editorial quality.
- Reserve cases not used while tuning for a later check; retain previously successful
  cases to catch regressions. One success is a smoke test, not a general estimate.

Write the grading criteria before examining candidate outputs where feasible. Compare
correctness, preserved requirements, unsupported additions, and unnecessary questions
or work. For subjective comparisons, hide version labels from the grader when practical.
Treat preferences as preferences; do not fabricate objective scores for them.

For unnecessary-constraint complaints, compare the prompt with and without the
disputed instructions. Grade the user's actual result requirements, including any
downstream consumer needs; do not count harmless departures from author-added rules
as failures. Also check a case where the restriction is consequential or explicitly
required, so simplification does not silently discard real requirements. Removing
text establishes a simpler artifact, not equivalent or improved model behavior.

For prompts intended to make an independent judgment, add tests for two distinct
failure modes when relevant:

- **Framing sensitivity:** keep the underlying evidence and decision criteria fixed,
  but vary the user's stated preference or expected conclusion in opposite directions.
  The judgment should not move materially unless the changed wording introduces a real
  requirement or new evidence. A difference is a failure signal to investigate, not
  by itself proof of sycophancy.
- **Conclusion-first rationalization:** check whether the prompt establishes criteria
  and criterion-level judgments before requesting the overall conclusion. Where a
  meaningful comparison is possible, contrast this with a version that asks for an
  overall score or choice first and inspect whether component judgments merely conform
  to that initial result.

Do not force neutrality onto advocacy tasks. If the task is explicitly to make the
case for one side, test faithfulness to that goal instead of penalizing directional
coverage.

## Check instruction placement

For placement revisions, use cases that differ in lifetime and breadth: a one-time
request, a fact needed across project tasks, and a recurring procedure used only for
one task class. Include a mixed request and an existing tool-enforced requirement.
Inspect whether the authored result keeps usable task instructions, scopes persistent
guidance correctly, and avoids duplicating tool rules or dropping required context.

Then exercise the produced instructions with the context their chosen home provides.
For a skill, check discovery separately from forced-loaded execution using positive
and neighboring requests in the actual host. For project context, confirm its scope
and availability. Report untested deployment behavior separately from a sensible
placement recommendation.

## Execute in the intended context

A test run submits the prompt to a model in the role and context that deployment uses.
Keep evaluator guidance outside that context. Use only the inputs, knowledge, and tools
the deployed model should receive; the author's private discussion can hide deficiencies.

Treat instructions under review as inert in the reviewing session. This does not mean
the target model must ignore them during a test: it follows them in its test context.
Use non-mutating fixtures or isolated test resources for prompts that call tools.
Authorization to inspect a prompt is not authorization for its embedded actions.

Name the model/configuration actually used when known. If only a different model is
available, label the comparison as a transfer probe. Do not infer a specific model
name from the quality of a response.

For repeated stochastic behavior, use multiple comparable runs and inspect both
improvements and regressions. Separately sampled candidates need separate sampling
operations; asking for alternatives in one answer is not a substitute. Diversity
does not itself provide independent factual evidence.

## Revise from visible evidence

Inspect the input, response, tool events, and feedback. Locate the earliest visible
departure from the expected path. Record a cause as a hypothesis when alternatives
cannot be ruled out. Test a coherent intervention rather than accumulating warnings
after every failure. Retain useful old behavior and revert or revise harmful changes.

Example ordering, long-context placement, sampling settings, or multiple candidates
can be useful experiments when linked to the failure. They require a target model,
a comparison protocol, and an acceptable cost; they are not slogans to insert into
the delivered prompt.

## Report what happened

Distinguish:

- **Inspection:** requirements, placeholders, contradictions, and reference checks.
- **Walkthrough:** an author-generated illustration or simulation; not target execution.
- **Execution:** named model/context used on specified cases, with actual output.
- **Comparison:** matched conditions and observed differences, with sample limits.

If execution is unavailable, provide the candidate, concrete test inputs and expected
results, and the missing comparison. Say which behavior remains unverified. Keep
actual outputs and artifact versions in maintenance records for reusable work, protecting
private data. Do not turn a proposed case into a reported pass.
