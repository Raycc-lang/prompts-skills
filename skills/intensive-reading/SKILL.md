---
name: "intensive-reading"
description: "Decide whether a book, paper, or course deserves intensive reading, and if so route it to the right session shape before starting. Use when the user is starting a new material and wants it set up, asks whether something is worth reading properly, or asks which reading approach fits a material. Runs before reading only. Not for summarizing, note-taking, or extracting knowledge from a passage."
---

# Intensive Reading — setup

Runs **before** reading. Decides whether a material earns intensive treatment,
and if it does, what shape the sessions take.

Out of scope, deliberately: extracting knowledge from a passage. That is the
`jiangou-learning-analysis` skill's job — hand off to it rather than duplicating
its extraction table here.

Work through the gates in order. **Stop at the first one that fails** and say so.

**The single most important behavior:** be willing to say the material does not
deserve intensive reading. A router that approves everything is a router that
does nothing. Demotion to casual reading is a successful outcome, not a failure —
say it plainly, without softening it into a maybe.

---

# Output language — read this before writing anything

The vocabulary below (slots, types, letters) is **internal reasoning
scaffolding**. It is compact and useful for thinking. It is bad writing.

**Never put these in the output:** slot letters (K/R/C), type letters
(A/B/C/D/E), "input space," "applicability," "pairing/paired," "object-layer
loss," "upper-layer loss," "discrimination model," "connection model," "novel
case," "refusal item," "anchor," "carving," "the extension differs."

Say the thing instead. Every one of these has a plain rendering that is shorter
than the jargon plus its explanation:

| Internal | Say |
|---|---|
| slot K | the ability you're actually after |
| slot R | the things you just need to memorize |
| slot C | making sense of cases you already know |
| the anchor | the real situation where you'll use this |
| does it pair? | does it tell you whether you got it right |
| input space | the range of situations it covers |
| applicability | where the rule stops working / its boundary |
| a novel case | a case that isn't in the book |
| a refusal item | a trick case the rule *shouldn't* cover |
| object-layer loss | you'll be able to summarize it and still freeze on a real problem |
| upper-layer loss | you'll remember the stories and be stuck on anything new |
| description-only | you'll be able to recite it and unable to use it |

If the user asks what's underneath, explain the framework freely. Don't lead with
it.

**Name the material's shape; don't label it.** Each type has a plain name that
describes the material and doubles as the heading the user looks up in their own
reading process. Use the name. The letter may appear once, in parentheses, only
if they ask.

---

## Gate 1 — Is this worth reading properly?

Ask the user to complete, out loud:

> "I will use this to ______, on ______, by ______."

Accept only a real object and a real date. Reject: "it's interesting," "it's
foundational," "I'll need it eventually," "everyone in my field has read it."
Those are reasons to read — they are not reasons to *process*.

- Completes → intensive, continue.
- Doesn't → **read it casually. Stop here.** No notes, no extraction, no guilt.
  Most materials belong here. The gate exists because intensive attention is
  scarce enough that spending it on the wrong book costs more than not reading
  the book at all.

Ask whether they already have a book in the intensive tier. Running two is
usually how both stall.

---

## Gate 2 — What do they want out of it?

Sort it. Never let one activity serve two of these — an activity serving two
goals gets judged by the wrong test.

| Internal | In the output, call it | Test |
|---|---|---|
| **K** — generalization | the ability you're after | cases that aren't in the book |
| **R** — reproduction | things to memorize (names, signatures, constants) | plain recall |
| **C** — compression | organizing cases you already know | does one rule cover all of them without contradiction |

**No ability in the list → not an intensive material.** Read it casually and stop
here — the same outcome as failing Gate 1. Do not re-run Gate 1; it already passed,
and the goal it accepted is not one this process can serve.

Watch for the third being mistaken for the first: someone reading about a domain
they already work in often wants their existing cases organized, not a new
ability. Judging that by "can you handle a case that isn't in the book" makes a
succeeding process look like a failing one. Explain it that way, not as "C
misfiled as K."

---

## Gate 3 — What is in front of them at the moment of use?

Gate 1 already got the use and the date. This gate gets the **scene**, which is a
different question — and the one that makes Gates 4 and 6 decidable.

> "Picture the moment you use this. What's on your desk or screen, and what are you
> deciding?"

An answer that only replays Gate 1's sentence has not passed. No scene → it serves
nothing; reframe or drop it. A vague scene produces a vague success test, so don't
let one through — this kills more bad plans than any other question.

---

## Gate 4 — What shape is the material?

Ask them to open a **middle chapter**, not the introduction, and answer:

- **Does it tell them whether they got it right?** Exercises with answers, worked
  problems, a runnable environment, or a job where reality corrects them.
- **Does it have both general rules and concrete cases?**
- **Is the ability one that has to run in real time or below conscious
  thought?** Perception, taste, physical skill, live production.

The third overrides everything.

| Internal | Call it | Typical | If they read it the ordinary way | What they have to supply |
|---|---|---|---|---|
| **A** | **Practice included** | textbooks with problem sets, graded courses | fine | nothing |
| **B** | **Rules but no practice** | idea books: economics, psychology, management, design | they'll summarize it well and freeze on a real problem | the practice |
| **C** | **Stories but no rule** | narrative history, case studies, biography, reportage | they'll remember the stories and be stuck on anything new | the rule |
| **D** | **Rules but no examples** | reference/API docs, aphoristic advice books, dense papers | they'll be able to recite it and unable to use it | the examples |
| **A+** | **Drills but no explanation** | LeetCode, workbooks, shared Anki decks | grinding will feel like progress while nothing generalizes | the explanation |
| **E** | **Not learnable by reading** | anything real-time or perceptual | reading won't build it at all | actual practice with feedback |

### What a session looks like (~40 min)

Only the front half changes. Every version ends the same way: extract the
knowledge, then retell it.

- **Practice included** — skim headings (5) · read once, then **do every
  exercise** (15). The exercises are the whole reason this material is easy mode;
  skipping them quietly turns it into the next category.
- **Rules but no practice** — skim (5) · read once, then write **two cases from
  their own work**: one they think the rule covers, one they think it doesn't,
  predicting the answer before checking (15) · have someone or something grade
  those two cases against the rule (5). The case they think it *doesn't* cover is
  the one that teaches; the other only confirms.
- **Stories but no rule** — skim (5) · read, tagging each story with what it's an
  example of (10) · put three or more side by side and **work out the shared
  pattern themselves**, then **test it immediately on a case the book hasn't
  reached** (10). Immediately, not later — an untested pattern is one they'll
  believe for months on no evidence.
- **Rules but no examples** — **collect 3–5 real examples before reading** (10) ·
  read the rule, sort each example against it, find where it stops working (15).
- **Drills but no explanation** — do the items, then run the "stories" or "rules"
  repair on what they just did, depending on which half is missing.

### Honesty checks — apply these, don't skip them to be encouraging

- **Rules but no examples:** if they can't produce three real examples *right
  now*, the material isn't learnable yet. Say so. Reading it harder does not
  create the missing half.
- **Not learnable by reading:** no amount of reading builds a real-time skill.
  The text can only help choose what to practice and make sense of feedback
  *between* attempts.
- **Re-reading:** legitimate, but it builds speed, not range. Don't let it count
  as a test.

**Format notes:** lecture or video → transcribe first, then treat the transcript
as the material; never extract live. Papers → also record what the paper claims
and what evidence would overturn it.

### Before they start — get these in writing

- *Rules but no practice* → who or what is grading their two cases.
- *Stories but no rule* → where untouched cases from the same field will come
  from.
- *Rules but no examples* → the three examples, listed now.

Can't fill it in? Downgrade to casual reading. This is the most useful line in
the whole setup.

---

## Gate 5 — Point at the extraction step; don't perform it

Every session ends by pulling out the knowledge and retelling it. Tell them to
run **`jiangou-learning-analysis`** on the passage for that.

Add only the three notes specific to working through a whole book:

1. **Pull out knowledge where it exists, not once per chapter.** How much a
   chapter holds is a fact about the book. A trade book may hold three real ideas
   across three hundred pages.
2. **Nothing is a legal answer, and worth writing down.** Forcing something out
   of an empty chapter produces a fake idea that then gets rehearsed and
   defended. Several empty chapters in a row is information about the *book* —
   that comes back here, to Gate 1, not into more effort.
3. **Check the result themselves; it's a draft.** The checking is the learning.
   The most valuable question is always *where does this rule stop working* —
   written rules leave out their own limits, and the limit is where people misuse
   them.

---

## Gate 6 — Decide now what will count as success

This has to happen before reading, while the answer can still be inconvenient.

Two tests, run within 48 hours of each session:

- **A case that isn't in the book.** Where will it come from?
  *Practice included* → a problem the book didn't pose. *Rules but no practice* →
  a situation from their own work it never mentions. *Stories but no rule* → a
  case from the same field it didn't cover, often from the news. *Rules but no
  examples* → a real example from their environment, judged cold.
- **A trick case the rule shouldn't cover — and they shouldn't know which is
  which.** This one is mandatory. The first test catches a rule they never
  learned. Only this one catches a rule that has quietly grown to cover
  everything, which is the normal failure for idea books, where every good rule
  feels like it explains the world.

Being able to restate it proves nothing. A perfect summary and total inability to
apply coexist comfortably.

---

## Output

One message, in plain language, in this order: whether it's worth reading properly
and why — carrying Gate 3's scene inside that verdict rather than giving it its own
paragraph, since restating it separately just repeats Gate 1 · what they're actually
after · what shape the material is and what that costs them · what a session looks
like · what to get in writing first · what will count as success. Then the pointer
to `jiangou-learning-analysis` for the per-session extraction.

**Target register — this is roughly the length and tone to aim for:**

> **Worth reading properly? Yes.** You could complete the sentence — you'll use it
> to rewrite the onboarding flow in March, with the current flow open beside you and
> a decision to make about which steps to cut. That's a real use, a real date, and a
> scene you can picture.
>
> **What you're after:** the ability to tell which friction in a signup flow is
> worth removing. Not the vocabulary — you'll pick that up anyway.
>
> **What shape it is: rules but no practice.** It states its principles and gives
> examples of each, but there's nothing to attempt and nothing to check yourself
> against. Read the ordinary way, this book will leave you able to summarize it
> beautifully and stuck the first time you're looking at a real signup flow. So
> you have to supply the practice.
>
> **A session, about 40 minutes:** skim the headings, five minutes. Read the
> chapter once, no stopping. Then write down two flows you've actually seen — one
> you think the principle covers, one you think it doesn't — and commit to an
> answer before you check. Then have me grade both against the principle as you
> stated it. The one you think it *doesn't* cover is where the learning is; the
> other just agrees with you.
>
> **Get this in writing before you start:** who's grading those two cases. If
> it's me, paste the principle in your own words, not the book's.
>
> **What counts as success:** within two days, apply it to a flow the book never
> mentions — plus one case where it *shouldn't* apply, mixed in so you don't know
> which is which. That second one is the point. Every good design principle feels
> like it explains everything, and the only way to find out you've overextended
> it is a case that should be refused.
>
> Per chapter, run `jiangou-learning-analysis` to pull out the knowledge. Two
> things: some chapters will hold nothing, and that's a real answer worth writing
> down. And check its output yourself — especially where the rule stops working.

---

## Operating notes

- Numbers here (3 examples, 48 hours, ~40 minutes) are conventional starting
  points, not results of the analysis. Say so, and tell the user to adjust from
  experience. Never present an invented number as a finding.
- Present the framework's claims as one way of analyzing learning, not as
  established cognitive science. For empirical questions — spacing, dosing,
  transfer — say which source is doing the work.
- Distinguish a neutral rule from advice derived from it under one goal.
- Don't be a cheerleader. The gates only have value if they can fail, and the
  most useful outputs of this skill are "just read it" and "put it down."

