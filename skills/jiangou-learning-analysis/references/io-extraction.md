# Learning from Language Materials: Pipeline + Knowledge Extraction

Entered from SKILL.md routing, AFTER step 0. Use for requests whose target is
learning knowledge FROM text, lecture, or video: "extract the knowledge," "help me
study this chapter," "why can't I apply what I read."

Do NOT enter here when the material itself is the target of a pure reproduction task
(verbatim recitation, quotation, memorizing a definition word-for-word for a quiz,
a fixed script). Those are step-0 reproduction goals: train and verify exact
reproduction instead. Split mixed goals — "recite the definition" and "apply the
definition" are two tasks with two verifications — and route each separately.

## Part 1 — The four-step pipeline (run in order)

Language is a proxy layer: symbols stand for concepts, which stand for phenomena.
Learning from language therefore has extra steps — and extra failure modes — that
interaction-based learning does not.

**Step 1 — Semantic understanding (理解语义): language world → meaning world.**
Convert symbols to the concepts they stand for. Checks before proceeding:
- Does the learner actually possess the referenced concepts, or only recognize the
  words? (Fluent wording with no concepts behind it = name-only failure.)
- **Quarantine undefined terms.** Words the material itself is introducing
  ("entropy," "isolated system") cannot be semantically understood yet — their
  concepts must be BUILT in step 3 before their names can be linked in step 4. List
  them as prerequisites, and do not let the learner's everyday sense of the same
  word fill the gap (that is how layer mismatch starts).
- **Watch for meaning shifts.** The same symbol can change referents across a
  passage (many-to-many reference); flag any term used in two senses.

**Step 2 — Material organization (组织材料).** Sort the material's content into
layers: concrete cases (stories, examples, demonstrations) = lower layer; general
statements (definitions, laws, rules) = upper layer. Flag a material that has only
one layer — it cannot support model construction by itself. Match each concept in
the upper-layer statements to its instances in the lower-layer cases.

**Step 3 — Model construction (建构模型).** From the organized material, build the
discrimination models (which phenomena count as each concept) and the connection
model (the general relation). This is where the extraction table in Part 2 is
produced. The language description of the knowledge is an INGREDIENT here, never the
product — memorizing the description and stopping is the description-only failure.

**Step 4 — Naming (建立指代), only if needed.** Attach the material's names
("Second Law of Thermodynamics") to the models just built, for communication and
storage. Forgetting names later costs only communication, not the knowledge.

## Part 2 — The extraction table

Produce one table per knowledge found (a passage often contains more than one; the same
passage frequently supports both a discrimination reading and a connection reading —
give both when so, and note that carvings are task-relative: present the one(s)
serving the learner's stated task, not a unique "true" structure).

| Field | Content |
|---|---|
| Task | What inference this knowledge performs, one line: "from X, predict Y" |
| Type | Discrimination model / Connection model |
| Input space | The set of ALL cases it applies to — stated as a set, including unseen members. List dimensions (sub-concepts) if multi-dimensional. |
| Output space | The set of possible results. For a discrimination model: {concept, not-concept}. |
| Mapping | The rule(s), as stated by the source, in the analyst's own words |
| Intension (discrimination models only) | The defining features used to classify |
| Applicability | = the input space, restated as a boundary: what falls OUTSIDE (this is where misuse happens) |
| Prerequisite concepts | Terms the source introduces that need their own discrimination models first |
| Worked examples | One positive instance; for discrimination models also one negative/near-miss |

## Part 3 — Extraction rules

1. **Layer-sort first** (= pipeline step 2). The knowledge is the upper layer; the
   examples are evidence and material for it. Both are needed.
2. **Constants vs variables.** "This apple is sour" relates constants → an
   experience, not a knowledge. Only variable-to-variable general relations go in
   the table. Apply the five admission tests in framework-core.md before typing a
   relation as a connection model.
3. **Knowledge vs derived advice.** "State your conclusion first" is advice; the
   knowledge behind it is "summary-first structures → lower reader difficulty" (a
   neutral mapping usable under other goals). Extract the mapping; list advice
   separately as "derived decision (under goal G)".
4. **The input space is usually understated.** Natural-language laws omit domain
   restrictions ("divisor" silently means positive integers; Newtonian inputs
   exclude relativistic speeds). Reconstruct the restriction into Applicability —
   the single highest-value field.
5. **Inputs are minimal-sufficient.** If the output is determined without a
   mentioned quantity, that quantity is not an input (the dividend is not an input
   to "largest remainder = divisor − 1").
6. **Constants in formulas** (G, π, coefficients) belong to the mapping, not the
   input or output.
7. **Intermediate concepts** (computed mid-quantities like the normal in
   reflection; unobservables like energy) are legitimate — mark as intermediates,
   neither input nor output.
8. **Task anchoring.** Before finalizing, ask: which downstream use does each carved
   concept serve for this learner? If a concept serves nothing downstream, either
   find its connection or drop it from the table.

## Part 4 — Retell skeleton (hand to the learner)

"This section is about [task]. It applies to [input space], and tells you
[output space]. The rule is [mapping]. For example, [worked example]. It does NOT
apply to [outside-the-boundary case]."

Retelling this skeleton — not the source's wording — is the comprehension exercise.
In a foreign-language context, retell it once in L1 (verifies comprehension only)
and once in L2 (trains production, with meaning already secured): two different
tasks, deliberately separated.
