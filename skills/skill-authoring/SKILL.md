---
name: "skill-authoring"
description: "Create, consolidate, revise, or review reusable agent skills (SKILL.md folders). Use for 写技能 / 做技能 / 把流程沉淀成 skill, packaging a project's workflow, distilling execution traces, or diagnosing skills that are ignored, generic, rigid, unstable, or unhelpful. Not for one-off prompts or pure wording edits with no skill behavior to improve."
when_to_use: "Use when creating, consolidating, evaluating, or repairing a reusable agent skill; includes wording changes needed for that work. Excludes one-off prompts and standalone prose polishing."
---

# Skill Authoring

Turn useful experience, knowledge, and user standards into instructions another
agent can apply. Start with the behavior or capability the skill should add;
choose the document structure after discovering what needs to be carried forward.

## 1. Establish the intended difference

Recover the task class, requested scope, target agent/tools, and an observable
good result. Use available artifacts and user corrections before asking questions.
Ask only for missing information that would change the design; continue independent work.

Identify the kind of work:

- **Create / distill:** what does an ordinary attempt miss, and what should change?
  If no baseline exists, state the suspected gap as a hypothesis.
- **Consolidate / migrate:** what already works, what must travel with the skill,
  and which dependencies prevent reuse? Preserve established decisions, facts,
  examples, and tools. Portability with equivalent behavior can be the whole goal.
- **Review / revise:** compare the user's complaint with the actual artifact and
  available runs. Locate the failure before prescribing edits; a good result is
  counter-evidence to a proposed diagnosis, even if it came from a strong model.

Define what would count as improvement: output quality, fewer recurring errors,
less user intervention, or successful reuse in a new environment. A passing task
alone does not show that a skill helped. If the existing prompt, tool, or skill
already covers the need, explain that finding instead of manufacturing a new skill.

## 2. Recover the decisions worth preserving

Read [the worked example](references/worked-example.md) when constructing a new
procedure or when a draft contains only generic phases.

Use real runs, accepted artifacts, user corrections, requirements, and domain
references. For traces, retain known outcome labels; mark unknown outcomes unknown.
If evidence is missing, execute a representative task when feasible, or draft from
explicit requirements and label untested choices. A transcript is not a prerequisite
for packaging an existing knowledge base or implementing a user's stated method.

For each consequential choice, recover:

- **Cue:** what feature of the input or intermediate result mattered?
- **Decision:** what action was selected, and over which plausible alternative?
- **Reason:** what criterion or constraint makes that choice appropriate?
- **Boundary:** when would another action be better?
- **Check:** what observable result would show the choice worked?

These are authoring questions, not mandatory headings in the generated skill.
Distinguish essential decisions from incidental chronology. Preserve useful recovery
logic from failed attempts while removing the exploratory transcript. A successful
run supports a candidate procedure; it does not prove every step was necessary.

Retain knowledge that enables a decision: definitions, domain facts, user preferences,
contrasting examples, schemas, or tested code. For an established workflow, reuse
its sound material directly rather than translating everything into new prose.

## 3. Write the smallest sufficient working package

Use [anatomy](references/anatomy.md) for packaging and routing. Write the core
decision procedure first, then describe when it should load.

- Replace generic directions such as "analyze carefully" with the criteria that
  determine the next action. Keep familiar steps when their order or checkpoint
  addresses a real need; omit reminders that add no useful direction.
- Choose the useful representation: ordered steps for fixed sequences, branches
  for conditional choices, examples for judgment, scripts for repeatable mechanics.
  Put substantial runtime knowledge in linked references with clear loading cues.
- Preserve exact syntax and ordering where execution depends on them. For variable
  steps, state what observation changes the action. Repair a recoverable precondition,
  choose a valid fallback, or stop only the affected work when essential input is absent.
- State the action to take. Use guards for evidenced failures, explicit requirements,
  or concrete consequential risks; pair them with a replacement or recovery path.
  Carry user authorization forward rather than inventing repeated approval steps.
- Show what a useful result looks like and how to check it. Match verification to
  the task: execution for code, inspection for rendered artifacts, source comparison
  for factual work, or concrete criteria and user examples for judgment tasks.
  Keep author-side evaluation machinery out of the generated runner's workflow.

Length follows the task. Remove duplication and irrelevant material; retain an
example or explanation when it changes a decision. There is no target line count.

## 4. Check the claimed improvement

Use [evaluation](references/evaluation.md) before claiming validation. Select a
typical task and a case that changes an important assumption. Test the actual package
with the context a future runner will receive, in fresh sessions when available.

For a new behavioral claim, compare with the same agent without the skill. For a
revision, compare with the prior version; for migration, check behavior preservation
and independence from the original location. Keep inputs, tools, and grading criteria
comparable. Inspect quality and friction, not only completion or format compliance.

Separate mechanical checks from agent behavior. If fresh execution or a baseline is
unavailable, perform useful available checks, provide runnable cases, and report the
missing comparison. A self-review or simulated walkthrough is not measured improvement.
Ship an explicitly unvalidated candidate when appropriate to the user's request;
do not claim stability from one or two successful examples.

## 5. Revise from the result

Read the skill's maintenance record when one exists. Choose the repair that
addresses the observed problem:

- **Not loaded / wrong skill:** check deployment first, then description overlap and
  host selection behavior. Wording alone may not fix retrieval.
- **Loaded but generic:** recover missing decisions or knowledge; remove redundant
  advice. Consider that the agent may already handle this task without a skill.
- **Wrong context / brittle procedure:** correct the applicability condition and
  the branch or recovery action that depends on it.
- **Harmful or burdensome:** remove or replace the responsible instruction; measure
  whether the repair restores quality or reduces unnecessary work.
- **Works as requested:** preserve it; distinguish proven scope from untested claims.

Make changes around a coherent failure mechanism so results remain interpretable.
Use a coordinated rewrite when scattered patches are the mechanism; otherwise keep
the repair narrow. Correct or retire failed rules rather than accumulating exceptions.

## 6. Deliver and retain maintenance evidence

Deliver the skill folder or requested review, the consequential decisions, checks
actually performed, and remaining uncertainty. For reviews, report findings and
evidence without treating a proposed cause as an observed execution failure.

Keep maintenance records outside the install unit, using the project's established
location (otherwise a sibling `meta/<skill-name>/`). Record sources for consequential
rule groups, observed failures, rejected changes, and evaluation results. Distinguish
paper findings, field observations, user requirements, and design hypotheses. Preserve
private source material in its private location; reference it without copying it into
a public maintenance record. Record host/model boundaries when they affect behavior.

Before delivery, check that the package has useful decision content, a discriminating
description, resolvable resources, task-appropriate verification, and an honest account
of what was tested. Maintenance records and test scaffolding stay outside the package.
