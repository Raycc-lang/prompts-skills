---
name: "skill-authoring"
description: "Author, distill, revise, diagnose, or gate agent skills (SKILL.md folders), using an evidence base for when skills help, why they work, and where they fail. Use when the user wants to create a skill from a goal or proven workflow (写技能、做技能、把这个流程沉淀成 skill), extract a skill from execution traces, asks why a skill misfired or was ignored, or wants a skill reviewed before shipping. For editing or grading prompt text rather than building a skill, use prompt-engineering."
---

# Skill Authoring

Build skills that change agent behavior reliably. In the cited controlled trials,
skills worked mainly as **procedural anchors** — they stabilized what the agent
does — not as fact delivery (procedural anchoring explained 65.7% of helpful cases;
injecting missing facts only 4.5%). That is a strong prior from those models and
benchmarks, not a universal law. So write procedure, make scope explicit, and keep
every rule traceable to a source. Full findings: `references/evidence.md`.
Skeleton and description examples: `references/anatomy.md`.

## When this applies

- Authoring a new skill from a goal or a workflow the user has proven.
- Distilling a skill from execution traces (success and failure runs).
- Diagnosing a skill that loaded but misfired, was ignored, or made runs worse.
- Revising a skill after new evidence; gating a skill before shipping.

Not for: one-shot instructions that happen once — write a prompt. Not for:
text-level fixes to existing prompt text — use prompt-engineering.

## Four failure surfaces

Design against all four, because a skill can break at any of them:

1. **Content** — rules that are vague, decorative, or fact-piles instead of procedure.
2. **Scope** — missing preconditions and non-triggers, so the skill gets applied where its assumptions don't hold.
3. **Retrieval** — a name and description that don't survive contact with near-duplicate siblings.
4. **Adaptation** — mechanical application; the agent follows steps that no longer fit the context.

Loading the correct skill is neither sufficient nor necessary for success, so the
artifact itself must carry scope and adaptation guidance.

## Maintenance loop

A skill is maintained, not finished: run → observe failures → record them with
provenance → revise or deprecate → run again [M6]. Revise is the entry point
after deployment. Record every observed failure as evidence even when no fix is
asked for — unrecorded failures cannot become rules or deprecations later.

## Modes

Pick an entry point. Diagnose flows naturally into Revise when the repair needs
tracking; the other modes stand alone.

### Author — goal → skill

1. Recover the contract: task class, trigger language, adjacent skills that own nearby cases, success criteria, tools the target agent has.
2. Ground the procedure in a real run. Execute the workflow once yourself, or ask for one real transcript. A skill written from imagination encodes imagined constraints. A skill built from a single run is **provisional** — say so in the delivery; treat it as stable only after it passes at least one further labelled run [W2].
3. Draft the frontmatter description using `references/anatomy.md`; it must separate this skill from adjacent ones.
4. Write the body against the same skeleton. Apply the writing rules below.
5. Run the ship gate.

### Distill — traces → skill

1. Require outcome labels. Distilling without success/failure labels measurably degrades the result [F2]; if labels are missing, establish them first.
2. From successes, extract the stable sequence: environment setup, tool order, intermediate checkpoints, output constraints.
3. From failures, extract pitfalls: symptom → cause → avoidance. Don't generalize incidental one-off noise — but retain a single failure when its cause is clearly generalizable, or its consequence is catastrophic, irreversible, or costly enough to warrant a preventive guard.
4. Compress. Strip exploratory branches, retries, and anything not needed to reproduce the working sequence; noise left in the artifact causes drift and budget exhaustion in runs that consume it [F3].
5. Keep two granularities [M1]: high-level phases are the default, portable layer; write exact step-level instructions only where order, syntax, tooling, or safety makes them necessary. Duplicating the same procedure at both levels is noise, not granularity.
6. Run the ship gate.

### Diagnose — a skill misfired

Map the observed failure to a class before touching text:

- **Routing** — never loaded, or a near-duplicate loaded instead → fix the frontmatter description, not the body [F5].
- **Brittle assumption** — a precondition no longer holds → state the precondition and add an explicit check [D1].
- **Context mismatch** — right skill, wrong situation → sharpen applies-to and non-triggers [D2].
- **Adaptation shortfall** — applied mechanically where steps no longer fit → mark which steps are invariant and which must adapt [D3].
- **Counterproductive** — content actively misled → retract the rule and record the counter-evidence.

These classes map onto the four surfaces: Routing → Retrieval; Brittle assumption
and Context mismatch → Scope; Adaptation shortfall → Adaptation; Counterproductive
→ Content.

Then change only the parts tied to the observed failure.

### Revise — new evidence → update

- One atomic change per revision; record what changed and why, so a bad change can be identified and rolled back. Record field failures as evidence even when no fix is asked for [W4].
- When a rule fails, merge the failure trace into the rule rather than deleting it — failure-driven correction beats appending successes and beats discarding [M3].
- Accept by kind [W4]: a behavior change must pass at least one representative task, or fix a demonstrated failure; a structural change (provenance, layout, references) is acceptable when behavior is unchanged; a speculative change stays flagged as an experiment rather than merged. One representative task is low-confidence evidence — say so when that is all the verification you have, and if verification isn't possible at all, say that plainly.
- When a skill accumulates three-plus revisions or recurring failures on one surface, upgrade the scattered notes into `references/notes.md` — phenomenon, root cause, current rule, rejected changes — so failed fixes are not re-proposed [W3].
- Deprecate rules whose reason no longer exists. A skill that only accumulates eventually poisons its own context [M4].

## Writing rules — what the artifact must satisfy

1. **Frontmatter is the router.** The description alone decides loading. State what it does in verbs, include the words users actually say, and hand off adjacent cases by name. No critical routing rule may live only in the body, because the body may never load [F5].
2. **Procedure over facts.** Order steps as actions; name tools; place intermediate checkpoints and output constraints. If a rule's value is a fact, check whether it belongs in the prompt or context instead of the skill [F1].
3. **Scope is content.** Applicability conditions, preconditions to check first, and non-triggers are part of the skill, not documentation about it [D1, D2].
4. **License to adapt.** Name which steps are invariant and which adapt to context, and when to abandon the skill entirely [D3].
5. **End with a runtime check.** Verify by executing, observing output, or running a test — never by rereading. Static-only verification is a failure mode (~12% of failures) that skills demonstrably do not fix [F6].
6. **One mechanism per rule.** Each rule anchors procedure, warns of a pitfall, or supplies a genuinely missing fact. Cut anything that does none of these [F1].
7. **Provenance.** Record each rule's traceable source — observed success or failure, user requirement, platform contract, or external spec. Rules without provenance cannot be safely revised or deprecated [W7, M3].
8. **Stay retrievable.** Name and description must discriminate among sibling skills; merge near-duplicates rather than shipping confusables. Retrieval is an independent bottleneck, and similar distractors measurably degrade identification [F5]. Description design improves discrimination but cannot compensate for an unsuitable retriever — persistent mis-routing in a large library is a library problem, not a wording problem [M2].
9. **Compress.** Heavy material goes to `references/`, loaded on demand. The artifact stays short; irrelevant detail in context degrades execution [F3, M4].
10. **Mark portability.** Separate portable procedure (task-level phases, checks, invariants — these transfer, even from stronger models to weaker ones [M5]) from conditional implementation (tool- or environment-specific details) and local workaround (compensates a known model weakness — label it; low-level patches tuned to a weak model measurably hurt stronger ones [W5]). Write procedures in framework-neutral terms; a standardized skill format travels across agent harnesses because it sheds the source harness's prompt style [F7].

## Output

- **Author / Distill:** the skill folder (SKILL.md, `references/` if needed) + up to five bullets on key decisions + open assumptions + a test proposal: 2–3 representative tasks with pass conditions. Routing behavior can only be tested outside the skill, so label trigger claims as predictions.
- **Diagnose:** failure class first, then the minimal repair. Leave working parts alone.
- **Revise:** the change, its evidence, and how it was verified.

## Ship gate

Before delivery, check:

- [ ] The description carries what it does, the user's trigger language, and handoffs; no critical routing rule lives only in the body.
- [ ] Every skill named in the frontmatter exists, in both directions — the skills this one hands off to, and the skills that hand off to it.
- [ ] Every rule anchors procedure, warns of a pitfall, or supplies a missing fact.
- [ ] Scope names preconditions and at least one non-trigger.
- [ ] The procedure ends with a runtime check that needs no tooling beyond the task's own.
- [ ] Adaptation guidance marks invariant versus adaptable steps.
- [ ] Heavy material is in `references/`; the body stays under ~150 lines [W6].
- [ ] Rules distilled from observed failures carry provenance.
- [ ] A test proposal exists, and at least its Task 1 was actually executed against the artifact before delivery — or it says plainly why execution wasn't possible. This gate itself must not be rereading-only [F6]. Routing checks remain predictions.
