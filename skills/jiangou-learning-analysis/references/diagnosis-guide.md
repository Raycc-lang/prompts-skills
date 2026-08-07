# Diagnosis Guide

## The healthy structure — diagnose against this, not by label-matching

- **Object layer**: the concrete objects the learner actually needs to handle.
- **Common layer**: concepts representing object groups, and relations between them.
- **Discrimination models**: map real objects → concept labels.
- **Connection model**: maps input concept's extension → output concept's extension.
- **Healthy application**: discriminate the concrete object into a concept, then use
  the connection model. The output is about the concrete object.
- **Language layer**: names and descriptions standing for the above via reference
  links (指代) — auxiliary for building and communicating, never the knowledge itself.

## Pre-check before classifying

The six patterns below are recurring framework-analyzable failures, not an
exhaustive account of why learning fails. Rule out the mundane causes first, because
they are more common and cheaper to fix:

- Sleep, fatigue, illness, stress load
- Attention conditions during study
- Misunderstanding what the task or assignment asked for
- No feedback available, or feedback too delayed to use
- Environment or tooling mismatch (noise, wrong materials at hand, no practice
  partner)
- Simply not enough total practice time yet for the timescale involved

When one of these is live, address it first and defer structural diagnosis until it
is corrected or controlled. Mundane and structural causes coexist freely, and a
structural conclusion drawn while a mundane cause is running is confounded.
Exception: proceed anyway when the episode independently demonstrates a structural
failure the mundane cause cannot explain — handling every paraphrase of a rule while
being unable to start a real case is structural however tired the learner was.

## Six recurring patterns

Ask for a concrete recent episode and match its signature. Several can co-occur;
treat the most upstream first.

| # | Failure | Signature (what the user reports) | Deviation | Fix |
|---|---|---|---|---|
| 1 | Name-only (只记名称) | Uses the term fluently; cannot explain or apply anything behind it | Only a language-layer symbol stored; no concept, no model, no reference target | Run the full loop from step 1; treat the term as unlearned. Name-dropping is sometimes a legitimate social tactic — ask about intent |
| 2 | Description-only (只记描述) | Recites the definition or formula verbatim; fails or objects when the SAME content appears in different wording | The wording became the object of memory; the models were never built | Present the same knowledge in several different wordings alongside instances; practice matching them. Replace definition-recital cards with instance-classification cards |
| 3 | Object-layer loss (对象层丢失 / 下层丢失) | Aces written and oral quizzes; freezes on a real case ("knew the formula, didn't think to use it"; the medical student who answers every viva question but can't start the procedure). Believes the knowledge is "useless in real life" | Symbols allowed a jump straight to the common layer; the discrimination models mapping REAL objects onto the knowledge's concepts were never built. The learner cannot bind reality to the formula's symbols. Not "lacks examples" — lacks the mapping. Specific to language-based learning | For each concept in the knowledge, drill classification of varied REAL instances (which phenomenon is the base? which situation is an isolated system?). Re-drilling the formula trains a component that was not broken. Highest-priority failure: it masquerades as success |
| 4 | Upper-layer loss (上层丢失) | Knows all the examples vividly; helpless on any new case; "the masters already took all the good ideas" | Cases stored as isolated experiences; no abstraction over them — the model collapsed into experiences | Line up known cases side by side; extract the common input→output pattern; immediately test on one novel case. Mildest failure — seen-case ability still works |
| 5 | Layer mismatch (判联错配) | Confident application producing off or absurd conclusions; often FEELS like insight ("entropy explains my messy room"); L2 words used with L1 boundaries; a field's term read with its everyday meaning | A connection model imported intact, but the learner's pre-existing category boundaries were plugged into its concepts, silently swapping the input space | Rebuild each concept's discrimination model against the SOURCE's own definitions, using its stated intension plus instances. Frame respectfully: the prior concept isn't wrong, it's mismatched — it was validated on different boundaries |
| 6 | Reference or production-link gap (指代缺失 / 对应不熟) | "I know exactly what I mean but the word won't come"; knows the term receptively but cannot produce it in real time | The concept and models are intact; what's missing is the symbol→concept reference link, or the meaning→output correspondence is not proceduralized (义存言空) | Do NOT re-teach the concept. Establish and drill the link: declarative retrieval for the reference, find-output-then-proceduralize (with a grader if output-hidden) for production. Cheapest failure to fix — misdiagnosing it as #1 wastes the most effort |

## Evidence bar for #6 — the most over-diagnosed pattern

A learner's *feeling* that "I know this in my first language" does not establish #6.
Require demonstrated evidence: the learner performs the SAME task precisely in L1 or
in another modality — states the distinction exactly, applies it to a fresh case,
picks the right term among near-synonyms. If the L1 performance is itself vague or
imprecise, the concept boundary is the problem: check #5 (mismatched boundaries) or
#1 before treating it as a missing link. Vocabulary-shaped complaints frequently
turn out to be conceptual-precision gaps wearing a lexical costume.

## Interviewing notes

- "Show me the last time it failed" beats "describe your method." Diagnose from the
  episode, not the self-report.
- #2 vs #3: #2 fails on paraphrase of the STATEMENT; #3 handles any paraphrase but
  fails on a concrete INSTANCE.
- #1 vs #6: in #6 the concept demonstrably exists — test by switching language or
  modality (see the evidence bar above). In #1 nothing is behind the word in any
  language.
- #4 vs ordinary forgetting: #4 learners retain the cases vividly.
- A learner who "forgot the wording but still solves problems" has NO failure.
  Knowledge without its language material (义存言空) is healthy; only communication
  needs the names back, which is #6 at most.
- Restatement checks cannot verify learning in either direction for generalization
  goals. When asked "here's my summary, did I understand it?", accept the summary as
  evidence of wording-independence at most, then administer a novel instance. For
  pure reproduction goals, reproduction checks are exactly right.
