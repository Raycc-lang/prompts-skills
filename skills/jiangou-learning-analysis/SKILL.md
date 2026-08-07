---
name: "jiangou-learning-analysis"
description: "Analyze any learning goal, study method, or learning material with the 渐构分析 (Gradual Construction Analysis) framework. Use when the user asks to design or critique a study plan, diagnose why their learning isn't working (memorized but can't apply, knows the formula but never thinks to use it, read it but can't retell it), extract a text's core knowledge as input/output structures, decide whether something should be memorized or trained, or generate practice materials and verification tests. Works for languages, math, programming, physical skills, and professional knowledge."
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

## Gate 0 — Route on what the available feedback cannot tell them

First question, before any framework vocabulary: **what tells this learner they were
wrong, how fast — and what does that signal leave undetermined?**

Feedback and analysis do different jobs. A compiler, a coach, or a puzzled listener
reports *that* an attempt failed. None of them reports whether the decomposition is
right, whether the material is paired, whether a concept boundary was imported from
L1, or which sub-ability the errors keep landing on. Route on that difference, and
say in one line which row you are in.

| Situation | First move | Analysis still earns its place when |
|---|---|---|
| Fast, honest feedback available (compiler, test suite, coach, opponent, a listener who visibly doesn't understand) and the learner is still improving | Send them to the loop. Name the grader and a return condition. Don't spend the turn on structure the feedback will surface on its own. | progress stalls, one error class keeps recurring, or they can't tell why an attempt failed |
| Same feedback, but plateaued or repeating one error class | Run the loop on that error class | this is the case for it |
| Feedback slow, absent, or flattering — self-taught reading, theory, writing, judgment-heavy professional work | Run the loop. Here analysis substitutes for a missing error signal. | always |
| A specific attempt just failed and can be described | Diagnosis routing; skip steps 1–6 | |
| A text, lecture, or video in hand | io-extraction routing | |

Return conditions are observations, not durations: "come back when the same error
repeats across sessions," not "come back in two weeks."

**Mundane causes.** When a pre-check cause in `references/diagnosis-guide.md` is live
— sleep, attention conditions, a misread assignment, absent or delayed feedback,
tooling, or simply too little elapsed practice for the timescale — address it first
and defer structural diagnosis until it is corrected or controlled. Running both at
once confounds the structural conclusion. Exception: proceed anyway when the episode
independently demonstrates a structural failure, which the mundane cause does not
explain — handling every paraphrase of a rule while being unable to start a real case
is structural regardless of how tired the learner was.

## Gate 1 — Intake. Don't analyze on air.

Broad, useless output is caused by missing step-4 input, not by insufficient
thinking. Four facts are the floor:

1. **The use occasion** — one concrete, dateable situation where the ability gets
   used. Not "for work," not "to read papers." "The Thursday standup where I explain
   a design in English." "The 8/20 exam, section 3."
2. **A real recent episode** — one attempt that went wrong, told as what happened,
   not as a self-diagnosis. "I read the chapter twice and still couldn't start
   problem 4" — not "I think I have a comprehension problem."
3. **The grader** — who or what tells them their output is wrong, and how soon. If
   the answer is "nothing," that is itself the most important finding and usually
   outranks everything else in the analysis.
4. **The budget** — minutes available, cadence, and the deadline if one exists.

**If two or more are missing: ask for them and stop.** Ask at most four questions.
Do not attach a provisional analysis to the questions — a partial analysis in the
same turn is exactly the broad output this gate exists to prevent.

If the learner says to proceed without answering, proceed — but open with an explicit
assumption list and mark every recommendation resting on one, so wrong assumptions
are cheap to spot.

**Proportionality.** The full floor applies to plan design and method choice, the
requests that go generic without it. Scale down elsewhere: diagnosis needs facts 1
and 2 (the guide's own interview covers the rest); a memorize-or-train question and a
text extraction need only fact 1. Never let the gate cost more turns than the answer
is worth.

## Gate 2 — Scope. One sub-task at a time by default.

**Default — interactive coaching.** Carry ONE sub-task through steps 1–3, give the
methods that verdict licenses, and one step-7 test. After step 2's decomposition,
show the list and let the learner choose which goes first. This is right whenever the
learner is about to go practice, because an unexecuted plan teaches nothing and a
multi-part plan hides which part was wrong.

**Full coverage — when the learner asks for it.** "Analyze my whole study plan,"
"what abilities am I missing," "build me a curriculum," "compare these four
sub-skills" are legitimate requests for breadth. Cover every sub-task, but hold each
to the same four fields — type verdict · method · material or grader · test. Breadth
comes from more rows, not longer rows. Close with which one to start on and why.

**Single-turn.** "Should I memorize or train this?" gets step 0, the step-3 verdict,
and one line on verification. Do not expand it into the loop.

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

Then apply gate 2: offer the list and let the learner pick, unless they asked for
full coverage.

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

1. **Paired (有效经验)** — decide first which case you are in, and say which.
   *Supervised target mapping* (the learner must produce a specific correct output —
   a translation, a diagnosis, a solution, a pronunciation): the material must carry
   both the input and its correct output, because input alone cannot identify which
   output was intended. *Unsupervised category formation* (the target is a perceptual
   or distributional boundary rather than a labeled output): structured input alone
   can do the work, as with phoneme categories induced from varied speech. Default to
   the supervised case; when you route to the unsupervised one, name the boundary
   being formed and say why no label is needed.
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

If a draft fails the bar, the fix is more intake, not more analysis.

## What the user receives

- **Triage (gate 0, row one, or a live mundane cause)** — a few lines: the row, the
  loop or the cause, the grader, the return condition. Nothing else, unless the
  documented episode satisfies gate 0's independent structural-evidence exception.
- **Plan design or critique** — the step-1 input/output statement, the step-3 verdict,
  the methods it licenses, and the step-7 test that could falsify it. Scope per gate 2.
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

- **Never invent a number.** No item counts, session counts, durations, or
  percentages unless they come from one of three places: the learner's own log,
  budget, or error record; a source you can cite; or a structural requirement that
  follows from the analysis. Calling a number "conventional" or "a starting point"
  does not license it — that phrasing has been the main vector for invented numbers in
  this skill. Learner data does not determine a quantity by itself. Calculate one only
  when an explicit rule maps the evidence to the quantity; name the rule's source or
  structural rationale and show the calculation. Otherwise prescribe what to measure
  and how to adjust from the result, without supplying a placeholder number that will
  be mistaken for analysis.
- **Cheapest live fix wins.** If a gate-0 row resolves the request, that is the
  answer. Do not append the full structure for completeness.
- When extracting knowledge from a text, output the I/O table and have the learner
  retell THAT, not the text. The retell is the comprehension exercise, not the step-7
  test — for a generalization goal a fluent retell still has to be followed by a novel
  instance.
- Distinguish knowledge (a neutral mapping) from advice (a decision derived from that
  mapping under one goal). Record mappings; derive decisions per goal.
- **The framework locates failing components; it does not schedule.** Spacing,
  retrieval practice, and interleaving are structural choices from outside 渐构 that
  change what gets learned. Import them explicitly and say you are doing so, rather
  than folding them in as though they were framework outputs.
- **Sequencing is not covered by the framework.** When a decomposition has more parts
  than the learner can hold at once, order them by what the learner already has
  automatic, and say that this ordering came from load considerations, not from 渐构.
- Epistemic boundary: present the framework's claims as analyses WITHIN 渐构, not as
  established cognitive-science consensus. For empirical claims about dosing, spacing,
  perceptual learning, or transfer, distinguish the framework's interpretation from
  peer-reviewed evidence and say which supports the recommendation.
- This is 渐构 — gradual construction. Plans produced with this skill must include
  their own step-7 review cadence and are expected to be rewritten by it.
