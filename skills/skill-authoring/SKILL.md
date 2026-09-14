---
name: "skill-authoring"
description: "Create, consolidate, revise, or review reusable agent skills (SKILL.md folders). Use for 写技能 / 做技能 / 把流程沉淀成 skill, packaging workflows, extracting reusable decisions from experience, or repairing skills that are ignored, generic, rigid, or unstable. Includes deciding which parts belong in a skill; one-off prompt design and standalone wording edits belong to prompt engineering."
when_to_use: "Use for skill design, consolidation, diagnosis, and maintenance, including the wording and placement decisions required by that work."
---

# Skill Authoring

Build guidance that helps a future agent choose well in the intended situation.
Extract the condition that changes the right action, place that guidance where it
will be available, and check both sides of the condition. Apply this same standard
when revising this authoring skill.

## 1. Establish the task and evidence

Recover the task class, requested scope, target environment, and observable good
result from available artifacts and user corrections. Ask for missing information
when its answer changes the design; otherwise proceed with a narrow assumption.
For revisions, read existing instructions, resources, and maintenance records before
changing rules so established requirements and rejected approaches remain visible.

- **Create / distill:** identify what ordinary execution misses. Without a baseline,
  treat the suspected gap as a hypothesis; explicit user methods can still be encoded.
- **Consolidate / migrate:** preserve useful decisions, knowledge, examples, and tools.
  Equivalent behavior in the new environment can be the complete goal.
- **Review / repair:** compare the complaint with actual inputs, outputs, and available
  traces. Locate the earliest visible divergence; successful runs are counter-evidence
  to a blanket failure claim. Mark uncertain causes and outcomes as uncertain.

Define the intended difference: better decisions or output, less needless work,
or preserved behavior after relocation. An existing prompt, tool, or skill may
already meet that need; reuse it when no additional capability is needed.

## 2. Derive the decision and choose its home

For each consequential choice, identify the observable cue, plausible actions,
criterion that selects between them, and result that would verify the choice.
Change the cue in a nearby case: when should the action change? This contrast
defines the decision boundary. These are authoring questions, not required headings.

When a failure suggests a new warning, first locate the decision that produced it.
A missing condition calls for a branch; missing knowledge calls for context; a
mechanical failure calls for a tool repair. Merge related incidents into the same
decision where they share a cause. Keep incidental names, chronology, and raw
failure records in maintenance evidence. Retain useful domain facts and examples
when they enable the runner to recognize the condition.

Choose placement by lifetime, frequency across tasks, and enforcement needs:

- **Current prompt:** the particular request, inputs, and one-time exceptions.
- **Project context, such as AGENTS.md or the host equivalent:** stable project
  information needed across many tasks, including short pointers to maintained
  documents and commands. Scope it to the relevant project or directory.
- **Skill:** reusable knowledge or procedures needed for a recognizable task class;
  load substantial conditional detail through references.
- **Tools / configuration:** deterministic checks, schemas, permissions, formatting,
  or repeated mechanics. Context carries the invocation and judgment needed to use
  them. A new runtime mechanism needs an evidenced gap or a concrete requirement.
- **Maintenance / eval:** source traces, rationale, rejected changes, and regression
  fixtures. Preserve diagnostic detail here, outside the install unit.

A recurring project workflow can still belong in a skill when most project tasks
do not need it. Split mixed requests across homes and keep each rule at its source;
existing authorization determines which files or configuration may actually change.
If the requested package needs a dependency elsewhere, preserve or identify it.

Admit an instruction when it changes a relevant decision or satisfies an explicit
user, domain, or consumer requirement. For an extra restriction, identify the
consequential failure it prevents and the gap left by existing instructions or
tools. If that gap is absent, omit the restriction. Prefer the desired action and
recovery path; retain negative boundaries when they communicate a real distinction.
Positive wording alone does not justify a constraint.

Read [the worked example](references/worked-example.md) when source material or
accumulated warnings are difficult to turn into decisions.

## 3. Encode the working procedure

Write the core decisions, then the description that makes the skill discoverable.
Use [anatomy](references/anatomy.md) when packaging, relocating, or changing routing.

Use ordered steps where order affects correctness, branches where observations
change the action, examples where a distinction is hard to recognize, and scripts
for repeatable mechanics. Preserve exact syntax or ordering when execution depends
on it. For missing prerequisites, recover or use a valid alternative; pause only
the work that depends on an unresolved input or authorization.

Keep shared decisions and loading cues in SKILL.md. Put substantial mode-specific
knowledge in references and read it when that mode applies. Reuse sound existing
material rather than translating it into new prose. Dependencies should be available
in the target environment, with a fallback or a clear blocked condition if needed.

State the useful output and how to check it: execute code, inspect rendered artifacts,
compare factual claims with sources, or apply concrete criteria to judgment tasks.
Choose checks that establish the task's result; authoring experiments belong in
maintenance, unless evaluation itself is the skill's runtime task.

Review this package using its own admission and placement decisions. Consolidate
duplicate rules, replace vague reminders with actionable criteria, and remove
unsupported restrictions. Keep examples and explanations that improve decisions;
length follows their function rather than a fixed budget.

## 4. Test the boundary and revise the mechanism

Read [evaluation](references/evaluation.md) for the comparison appropriate to the
claim. Exercise the actual package with deployment-available context: a typical
case, the reported failure where available, and a nearby case requiring a different
action. For meta-skills, inspect the generated artifact and its downstream use.
When selection changes, also test positive and neighboring requests in the host;
forced loading tests execution, not discovery.

Compare a new behavioral claim with ordinary execution, a revision with its prior
version, or a migration with the original workflow. For a suspect legacy constraint,
remove it in a comparison variant and check the original failure plus a normal case.
Grade actual requirements, including a case where the boundary is necessary, so
neither harmless freedom nor justified constraints are penalized.

Use results to update the responsible decision in place. If the skill was unavailable,
repair deployment or selection; if relevant context was absent, repair delivery;
if the choice was wrong, refine its criterion or branch. Preserve working behavior.
Use a coordinated rewrite when scattered rules cause the conflict; otherwise keep
the repair local. A fixed incident plus a failing contrast signals overfitting.

## 5. Deliver with traceable evidence

Deliver the requested package or review, material decisions, checks performed, and
remaining uncertainty. Distinguish structural checks, author walkthroughs, actual
agent runs, and comparative evidence. When execution is unavailable, provide the
candidate and runnable cases with the unverified claim stated explicitly.

Keep maintenance outside the install unit in the existing project location, or a
sibling meta/<skill-name>/. Record the source and strength of consequential decisions,
their applicability, compared versions, actual outputs/traces, and remaining limits.
Keep private evidence at its private source. Retain enough detail to revisit a rule
without loading historical incidents into every runtime session.
