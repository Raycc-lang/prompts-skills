---
name: "jiangou-learning-analysis"
description: "Use the 渐构分析 (Gradual Construction Analysis) framework after the learner has chosen a learning direction: clarify the target ability, decompose it into sub-skills, design or critique practice and materials, diagnose learning difficulties, extract knowledge from selected material, and verify progress. A chosen direction can still need refinement; beginners need no prior failed attempt. Do not use to choose life or career priorities, decide whether a subject is worth learning, or decide whether material deserves intensive reading."
---

# Jiangou Learning Analysis

渐构分析 is itself a mapping: **input = the knowledge's traits + the learner's
traits; output = the best-fit materials + the best-fit methods.** Both inputs are
mandatory. Analyzing only the knowledge produces generic prescriptions — the most
common way this skill fails, and what the gates below exist to prevent.

Source framework: YJango's 渐构 (Gradual Construction) course. Core doctrine:
knowledge is a generalizable mapping from an input space to an output space;
learning is constructing the discrimination models and connection models that
mapping requires. Many recurring learning failures can be analyzed as defects in
those components, their pairing, or the language links used to access them.

Load `references/framework-core.md` when a typing decision is contested or
borderline; it holds the rigorous definitions and admission tests.

---

# Part I — Gates. Run these before analyzing.

## Gate 0 — Anchor the chosen direction and route the request

Recover the learning direction from the request and conversation. Help turn a chosen
direction into a usable target; do not require the learner to have already done the
decomposition. "I want to explain technical problems in English" is sufficient to
start refining the ability. "Should I learn English or programming?" requires a
priority decision outside this framework. Keep hypothetical learning-cost estimates
separate from deciding whether the goal is worthwhile.

Honor the requested analysis. For a plan or decomposition, proceed even if the
learner already has useful feedback and is improving. For a specific failed attempt,
use Part III's diagnosis route; for learning knowledge from selected text, lecture,
or video, use its extraction route.

For method choice or diagnosis, identify what tells the learner an attempt was wrong,
how soon, and what that feedback leaves unresolved. Feedback can establish failure
without identifying the missing sub-ability. When the question is simply what to do
next and the current practice loop is working, recommend continuing it with a named
grader and an observable return condition, such as a recurring error class. Do not
substitute that advice for an explicitly requested structural analysis. Treat
analysis without performance feedback as a hypothesis to verify, not a replacement
for evidence of learning.

Before diagnosing a structural learning failure, check relevant mundane causes such
as a misread task, tooling, attention, or absent feedback. Use the pre-check and
structural-evidence exception in `references/diagnosis-guide.md`. Do not impose this
failure diagnosis on a beginner asking for a plan.

## Gate 1 — Gather the facts that change the recommendation

Use the conversation first. Establish the target use and current starting point;
collect additional context only where it changes the requested work:

- **Target use:** a concrete situation or kind of task the learner wants to handle.
  Ongoing use and curiosity-driven understanding are valid; a date is optional.
- **Starting point:** demonstrated abilities, prior experience, and relevant attempts.
  For a beginner, use known prerequisites or offer a small initial task if needed.
  Require an actual episode to diagnose a claimed failure, not to design a first plan.
- **Feedback:** who or what can judge the result. If none exists, include a workable
  grader or check in the design and acknowledge its limits.
- **Practical constraints:** available materials, time, cadence, and any deadline
  when these affect method selection or a requested schedule. A decomposition alone
  does not require a time budget.

Ask a focused question when an unknown would materially change the recommendation.
Continue useful independent work; mark assumptions and provisional choices. Do not
invent learner errors or block the whole response because a fixed number of intake
fields is missing. If the learner asks to proceed without clarification, use explicit
assumptions and identify what observation would change the plan.

## Gate 2 — Match the scope to the request

**Plan or decomposition:** cover the chosen target's relevant sub-tasks, linking each
to its method, material or grader, and verification. Recommend a starting point and
sequence from prerequisites and demonstrated competence; explain the rationale.
Do not require the learner to choose a sub-task before delivering the requested plan.

**Interactive practice:** carry one sub-task through steps 1–3, its method, and a
step-7 test. Recommend the next useful sub-task and allow redirection; offer a choice
when the learner's preference would materially change the route.

**Single decision:** "Should I memorize or train this?" gets step 0, the step-3
verdict, and a matching verification check. Do not expand it into the full loop.

---

# Part II — The analysis loop

Run in order. Steps 2–6 iterate until step 7 passes. Name the step you are on so the
user can audit the analysis.

### Step 0 — Judge what the goal actually requires

| Need | Mechanism | Verified by |
|---|---|---|
| Reproduce specific SEEN items (a fixed text, a name↔meaning link, a set routine) | Experience memory / proceduralized correspondence | Stable reproduction of those exact items |
| Compress a BATCH of seen cases into one rule | A model's compression ability | Conflict-free coverage of the seen batch |
| Handle UNSEEN cases | A model's generalization ability | Novel instances + boundary instances |

Seen/unseen is not intrinsic to the material — it is relative to the object layer the
learner's task selects. The same content can be a memorization goal in one task and a
generalization goal in another. Classify per task, not per subject. Mixed goals get
split here and routed separately.

### Step 1 — Specify input and output, anchored to the task

Ask first: what does the learner need to predict, from what information, for which
goal? And for each concept carved out: which downstream processing or connection
model is it meant to serve?

Then state the input space (ALL situations the ability must handle), the output
space, and the mapping. The input space IS the knowledge's scope of applicability.
Carvings are task-relative — multiple valid decompositions exist. Pick the one whose
concepts feed the learner's actual downstream use, and say so rather than presenting
one carving as uniquely correct.

Anchor the input space to the gate-1 use occasion. An input space that would read
identically for a different learner with a different occasion is too abstract to
drive a method; narrow it until it isn't.

### Step 2 — Decompose

Split composite abilities into sub-tasks, each with its own input and output. Prefer
decompositions whose sub-tasks are real tasks occurring in actual use (horizontal
split) over artificial drills that never occur in use (vertical split).

Then apply gate 2: deliver the requested decomposition or plan; for interactive
practice, select a justified starting sub-task and allow redirection.

### Step 3 — Type each sub-task

Two orthogonal typings decide everything downstream.

| Question | Types | Decision rule |
|---|---|---|
| Model kind | Discrimination model (判别模型): {any phenomenon} → {this concept, not} · Connection model (联结模型): {concept A's extension} → {concept B's extension} · Correspondence (对应): one constant → one constant | Does the input BELONG to the output category? Yes → discrimination. Constant-to-constant link (name, fact, symbol→meaning, meaning→motor output)? → correspondence. Otherwise → connection, after applying the admission tests in framework-core. |
| Processing kind | Implicit (autonomous, resists verbalization: perception, listening, physical skills, "feel") · Explicit (conscious, rule-statable: formulas, procedures) | Must it run in real time or below awareness? → implicit. |

Verdicts:

- **Correspondence** → establish and stabilize the specific link. No general mapping
  to induce, but the mechanism varies: declarative recall plus retrieval practice for
  names and symbol↔meaning links, or find-the-correct-output-then-proceduralize for
  motor and production links (with an external grader whenever the learner cannot yet
  perceive their own output). "Memorize" is one mechanism, not the definition.
- **Model, explicit** → construct via worked examples plus the rule, verified on novel
  instances. Taper the worked examples as competence rises; for a learner who already
  solves the class, worked examples cost more than they return.
- **Model, implicit** → construct through sufficiently varied input→output paired
  experiences. When automatic real-time execution is the target, conscious
  rule-hunting during the attempt can interfere; use rules and explanations mainly to
  choose practice and interpret feedback before and after the attempt.

**Boundary note.** The three types assume the output is a label or a determinate
value. When the real output is graded or probabilistic — a calibrated likelihood, a
continuous quantity, a judgment under uncertainty — say so and treat the typing as an
approximation rather than a verdict. Add a calibration check to step 7 in those
cases: track how often the learner's confident judgments were right, not only whether
they can classify.

### Step 4 — Profile the learner

The second formal input, and the one whose absence produces generic output. Gate 1
collects the floor; extend it here with: discrimination and connection models already
built (from L1, prior domains) · likely mismatches imported from L1 or prior domains ·
current explicit vs implicit proficiency per sub-task · available sensory materials
and graders · the input-space region currently handled · actual recent error samples ·
tolerance for training formats.

**Every recommendation must cite a learner fact it used.** If you cannot cite one, you
are reciting the framework — go back to gate 1.

### Step 5 — Judge materials

A valid material for MODEL construction must satisfy:

1. **Paired (有效经验)** — the material must carry both the input and its correct
   output, because input alone cannot identify which output was intended. One
   exception exists: unsupervised category formation, where the target is a
   perceptual boundary rather than a labeled output and structured input alone can
   work. Default to the supervised case and say which you are in; the fork and its
   admission rule are in `references/framework-core.md`.
2. **Novel (新颖情况)** — generality grows only from unseen cases. Repeating exhausted
   material buys fluency, not generality. Tag every activity as fluency-building or
   generality-building. Fluency is frequently a *precondition* for the next level of
   generality rather than an alternative to it — when you prescribe repetition, say
   which higher-level ability it is clearing room for.
3. **Direct (感官刺激)**, for implicit tasks — actual sensory experience, not verbal
   description.

Correspondence tasks are exempt from the novelty requirement (repetition is their
method) but not from pairing.

### Step 6 — Match methods and execute

Templates by type in `references/practice-templates.md`. Each method names a material
the learner can open today.

### Step 7 — Verify to match the step-0 need, then iterate

- **Generalization goals**: performance on NOVEL concrete instances is the only valid
  test. Restatement proves nothing in either direction — perfect restatement can
  coexist with inability to apply, and failed verbalization can coexist with real
  skill.
- **Compression goals**: conflict-free coverage of the seen batch.
- **Reproduction goals**: stable reproduction IS the test. Do not impose transfer
  tests on non-transfer goals.

On failure, diagnose, then re-run steps 2–6.

---

# Part III — Routing

## Learning from language materials

After gate 0, requests whose target is learning knowledge FROM text, lecture, or
video ("extract the knowledge", "why can't I apply this chapter") run the four-step
pipeline in `references/io-extraction.md`: semantic understanding → material
organization → model construction → naming.

If the material itself is the target of a pure reproduction task (verbatim recitation,
quotation, a fixed script), do not force model extraction — train and verify exact
reproduction instead. Split mixed goals and route each separately. The extraction file
also carries the trap checks: symbols mistaken for knowledge, undefined terms, layer
sorting, meaning shifts.

## Failure diagnosis

Classify before prescribing. `references/diagnosis-guide.md` holds the healthy
two-layer structure to diagnose against, the mundane-cause pre-check, and six
recurring patterns: name-only, description-only, object-layer loss, upper-layer loss,
layer mismatch, and reference/production-link gap.

**Evidence bar, applied symmetrically.** The guide sets a strict bar for #6; hold #3
to the same standard. Before diagnosing object-layer loss, require a demonstrated
episode where the learner handled a paraphrase of the statement correctly *and* failed
on a concrete instance. Without both halves, #3 is a guess — and its fix is the most
expensive in the guide, since it rebuilds discrimination models across every concept
in the body of knowledge. Name the episode you read the diagnosis from.

---

# Part IV — Output

## The specificity bar

Every recommendation must carry learner-specific evidence: the gate-1 or step-4 fact
it was derived from, plus a material or grader the learner can open today. A
recommendation citing nothing about this learner is framework recital wearing a
prescription's clothes.

General framework statements are welcome — they explain *why* a recommendation
follows, and a learner who understands the reason can adapt it. What they may not do
is stand in a recommendation's place. Test each general sentence: is it explaining a
specific recommendation nearby, or is it the whole advice? Only the second is a
defect.

Each recommendation names four things:

- the sub-task it serves,
- the learner fact it was derived from,
- the material or grader — nameable, openable today,
- the observation that would show it isn't working.

"Practice more," "use spaced repetition," "find real examples," "build the
discrimination model," "get feedback" are placeholders. Each may appear only attached
to a named object and a named learner fact.

If a draft fails the bar, identify the missing learner fact or concrete practice
resource. Recover it, ask a focused question, or narrow and label the provisional
recommendation; more intake is useful only if its answer changes the advice.

## What the user receives

- **Triage when it answers the request** — the practice loop or relevant mundane
  cause, the grader, and an observable return condition. Preserve an explicitly
  requested plan or structural analysis.
- **Plan design or critique** — the step-1 input/output statement, the step-3 verdict,
  the methods it licenses, and the step-7 test that could falsify it. Include a
  justified sequence when requested. Scope per gate 2.
- **Diagnosis** — the failure pattern, the episode it was read from, the component
  actually missing, and a fix for that component only. Say which components are
  healthy, so the learner stops re-drilling them.
- **Extraction from a text** — the extraction table(s) and the retell skeleton, with
  applicability stated as a boundary.
- **Memorize or train** — the step-0 need, the step-3 type, the verdict, and one line
  on verification; the three needs are verified differently and the wrong test makes a
  working method look broken.
- **Practice materials** — the items themselves, each tagged fluency-building or
  generality-building, and the grader named wherever the learner cannot yet perceive
  their own output.

## Operating notes

- **Never invent a number.** No counts, durations, or percentages unless they come
  from the learner's own records, a citable source, or a structural requirement of
  the analysis; "conventional" and "a starting point" license nothing — that
  phrasing has been the main leak. Calculate a quantity only when an explicit rule
  maps the evidence to it: name the rule, show the calculation. Otherwise prescribe
  what to measure and how to adjust from the result — a placeholder number will be
  mistaken for analysis.
- **Cheapest live fix wins.** If gate-0 triage resolves the request, that is the
  answer. Do not append the full structure for completeness.
- When extracting knowledge from a text, have the learner retell the I/O table, not
  the text. The retell is the comprehension exercise, not the step-7 test — a
  generalization goal still needs a novel instance after a fluent retell.
- Distinguish knowledge (a neutral mapping) from advice (a decision derived from it
  under one goal). Record mappings; derive decisions per goal.
- **Scheduling and sequencing come from outside 渐构 — say so when you import
  them.** Spacing, retrieval practice, and interleaving change what gets learned;
  sub-task ordering, when the learner can't hold all parts at once, comes from load
  considerations — order by what the learner already has automatic. Neither is an
  analysis result; do not present them as one.
- Epistemic boundary: present the framework's claims as analyses within 渐构, not as
  established cognitive science. For empirical claims — dosing, spacing, perceptual
  learning, transfer — say whether the framework's interpretation or peer-reviewed
  evidence is doing the work.
- This is 渐构 — gradual construction. Plans must include their own step-7 review
  cadence and are expected to be rewritten by it.
