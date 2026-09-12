# Revision — 2026-09-06

## Authorized scope

Ray accepted the review and requested implementation. Updated the repository
entrypoint, added runtime examples/evaluation guidance, aligned the shared prompt
template, and documented evidence boundaries. Other prompts and skills are outside
this change. Installed copies are not synchronized; deployment is on demand.

A pre-rewrite snapshot was first kept at `baseline/` for a later comparison and
has been removed at Ray's direction: the old version was an intermediate result,
and this revision is the base going forward. The prior entrypoint remains
retrievable from git history (commit `6de06f0`) if an old-versus-new comparison
is ever wanted.

## Coherent mechanism changed

Replaced a writing-preferences/techniques/gate structure with:
desired behavior → operating context → visible diagnosis → prompt construction →
comparison → proportionate delivery. The hypothesis is that explicit decision and
diagnosis work will improve prompts more reliably than enforcing preferred forms.
This hypothesis has not been validated in a fresh-model comparison.

| Original rule or capability | Disposition |
|---|---|
| Preserve intended behavior | Kept; distinguish an explicit requirement from a failed mechanism without silently reinterpreting the user |
| Recover task/input/output/constraints/evidence | Kept and connected to conflict resolution, priorities, uncertainty, and concrete quality criteria |
| Optimize shortest/common wording early | Changed to sufficient information and precise decisions first, then simplify |
| Submitted instructions inert in reviewer context | Kept; target execution is explicitly separate and does not inherit arbitrary action authorization |
| Create/improve/debug/evaluate/grade modes | Kept with mode-appropriate outputs |
| Debug means likely cause and smallest repair | Expanded to actual inputs/context/output/trace, earliest visible divergence, competing causes, and an intervention hypothesis |
| Always avoid contract headings | Removed; headings judged by function, including the existing Word-Picker example |
| Require observed failure for every prohibition | Changed; explicit requirements and concrete risks can justify a constraint |
| Four mandatory layer categories | Removed as an artifact-design prescription; reviewer guidance and target instructions still separated |
| Examples, decomposition, schemas, tools | Kept; connected to decision needs and host capabilities |
| Candidates described as independent in prompt prose | Clarified separate sampling requirement and limits of agreement |
| All checks require something outside the model | Changed; supplied-criteria review is useful but not independent factual proof |
| Delimit, report every attack, confirm every irreversible action | Changed to boundaries plus host/user authorization and task-relevant reporting |
| Fixed long-context layout | Changed to organization, retrieval, target guidance, and comparison |
| Exhaustive requirement mapping in every reply | Internal preservation check retained; material changes shown proportionally |
| Routing/skill contract and universal ban on other skill names | Removed duplicated architecture workflow; preserve runtime references and route architectural work appropriately |
| Runtime sanity check with ambiguous 'run as data' | Replaced with inspection/walkthrough/execution/comparison distinctions and scoped test context |
| Test sets and baseline comparison | Kept; add held-out/regression cases and avoid importing author context |
| Invariant delivery gate | Replaced with concise outcome checks adaptable to actual scope |

## Rejected directions

- Do not replace the old form rules with mandatory decision tables in every prompt.
- Do not turn every simple request into application architecture consulting.
- Do not equate all self-review with independent verification or with uselessness.
- Do not remove useful prohibitions, technical terms, or examples to shorten text.
- Do not claim model-level improvement from a cleaner file or simulated response.
- Do not require a benchmark as a condition for delivering a user-requested draft
  when the actual target cannot be exercised; disclose the unverified behavior.

## Validation

See [validation](validation.md). Existing source prompts remain useful regression
inputs. This revision is implemented as an unvalidated behavioral candidate, not
a claimed measured improvement. Mechanical checks and author-side exercises are
reported separately from future target-model evaluation.

## Post-review adjustments (2026-09-06)

The description now excludes reviewing a skill's runtime behavior; those
requests route to skill-authoring. The prompt template's placeholders now use
`{{...}}` so they survive Markdown rendering.

# Revision — 2026-09-10

## Authorized scope

Ray requested implementation of two prompt-engineering techniques discussed while
reviewing *AI Prompting for Everyone*: reduce directional/sycophantic framing in
independent judgments, and evaluate criteria before forming the overall conclusion.
Cross-model review was explicitly left outside this change because it is primarily an
agentic-workflow concern rather than a prompt-only capability.

## Changes

- Added `references/judgment-and-review.md` with conditional guidance for neutral
  assessment, evidence selection, criteria-first evaluation, and conclusion-last
  synthesis.
- Added a core routing rule in `SKILL.md` so the reference is loaded for independent
  judgment, comparison, recommendation, diagnosis, verification, and selection tasks.
- Kept advocacy and intentionally one-sided exploration outside the neutrality rule.
- Added framing-sensitivity tests that hold evidence and criteria fixed while varying
  the user's preferred conclusion.
- Added checks for conclusion-first rationalization and retained the existing rule
  against meaningless numerical scoring.

## Design boundaries

- Neutrality is a property of the procedure, not forced balance in the conclusion.
  Strongly one-sided evidence may still justify a strongly one-sided result.
- User preferences that are genuine decision constraints remain part of the rubric;
  user predictions or favored answers are not treated as evidence.
- Criteria-first evaluation is conditional and proportionate. It is not a requirement
  to generate a rubric for every factual or simple generation task.
- The skill asks for observable evidence and concise rationale, not hidden
  chain-of-thought.

## Validation status

The change is structurally integrated and includes explicit regression-test designs,
but no fresh-model A/B execution has been run yet. Treat the behavioral improvement as
a reasoned, user-approved candidate until measured on representative prompts.

# Revision — 2026-09-12

Ray requested analysis and implementation after reporting that he removed unnecessary
content/restrictions from a generated prompt. The shared example was inaccessible to
the authoring session at that time, so the original change relied on explicit feedback
plus static inspection. Commit `95ebe7d` distinguishes result requirements from
optional methods, selects added restrictions by consequence and existing coverage,
removes the unnecessary sending boundary from the no-tool example, and adds a
contrasting flexible-output example.

The source example later became available in a separate session and the commit was
reviewed. Its result-versus-method repair remains consistent with the observed request;
no fresh downstream A/B execution has been run, so behavioral improvement is still not
claimed.

Rejected directions: banning constraint headings or all prohibitions; accepting only
previously observed failures as reasons for guards; converting every negative rule
to an equally unnecessary positive command; assuming the user's deletion proves
equivalent downstream quality. These preserve the 2026-09-06 review's boundaries.

Repository source only; installed copies are synchronized on demand. See validation for
available checks and remaining behavioral uncertainty.

# Revision — 2026-09-12 — action agents and model/effort selection

## Trigger

Ray supplied the TraeWork example and identified two additional gaps. First, a prompt
for an action-capable coding agent needs rules for how the agent should carry the work,
not merely a description of the desired repository result. Second, the original request
explicitly asked which model and thinking level should run the task, but the skill had
no procedure for assessing difficulty or making that recommendation.

## Changes

- Added an execution contract for action-capable agents: end state and scope, workspace
  inspection before committing to an implementation, autonomous continuation, recovery
  from recoverable failures, protection of unrelated state and secrets, observable
  completion checks, and a concise final handoff.
- Added `references/model-and-effort-selection.md` and a conditional routing rule from
  `SKILL.md` when model/agent-mode/reasoning-level choice is requested or materially
  affects success, cost, or latency.
- Expanded the skill description and delivery contract so a prompt request can include
  an execution recommendation rather than silently dropping that adjacent part of the
  user's request.
- Model selection now separates hard capability requirements from task difficulty and
  evaluates reasoning depth, uncertainty, action horizon, context burden, and
  verification/consequence. Reasoning effort is selected separately.

## Design boundaries

- Do not hard-code a permanent ranking of current model names; available products and
  capabilities change. Compare actual candidates when they are known.
- Do not equate prompt length, output length, or diff size with task difficulty. Small
  edits may still require substantial discovery and verification.
- Do not assume higher reasoning effort fixes missing tools, permissions, context, or
  model capabilities.
- Do not force a model recommendation into every prompt-engineering response. Apply it
  when requested or when the execution choice is open and materially consequential.
- Keep execution advice outside the copyable prompt unless the target prompt itself
  controls model routing.

## Validation status

The runtime reference and entrypoint are structurally integrated, but no controlled
cross-model or cross-effort benchmark was run. The difficulty rubric is a user-approved
engineering procedure derived from the observed task class, not empirical evidence for
a universal model ranking. See validation for static checks and regression cases.
