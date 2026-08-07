# Framework Core: Definitions and Tests

Load when a typing decision is contested, a diagnosis needs the healthy structure,
or a relation's status (connection model or not) is unclear.

These are definitions and tests WITHIN the 渐构 framework — an analytical vocabulary
for describing learning, not a claim that cognition is literally organized this way.
Where empirical questions arise (how much practice, what spacing, whether a given
skill transfers), defer to the relevant literature and say which source is doing
the work.

## 1. Two inference types, three abilities

- **Experience inference (经验推测):** recall a specific seen input→output pair.
  Single layer; no model involved.
- **Model inference (模型推测):** use a general mapping across a class. Two distinct
  abilities live here:
  - **Compression:** one rule replaces many SEEN pairs (verified by conflict-free
    coverage of the seen batch).
  - **Generalization:** the rule extends to UNSEEN cases (verified only by novel and
    boundary instances; never guaranteed — models are kept until they fail and are
    then rebuilt).
Seen/unseen exists only in the object layer, and the object layer is chosen by the
learner's task — the same content can be a reproduction goal in one task and a
generalization goal in another.

## 2. The healthy two-layer structure (下上结构)

- **Object layer (对象层 / lower):** the concrete objects actually being predicted
  and handled. Always the core — it is the problem; the upper layer is the tool.
- **Common layer (共象层 / upper):** concepts representing groups of objects, and
  the relations between concepts.
- **Discrimination model:** maps object layer → concept labels.
- **Connection model:** maps one concept's extension → another concept's extension.
- **Application sequence:** discriminate the concrete object into a concept, THEN
  apply the connection model — whose output is about the concrete object, not the
  abstract concept. Minimum kit for solving a real problem: two discrimination
  models + one connection model (plus one discrimination model per extra dimension).
All six failure patterns in the diagnosis guide are deviations from this structure.

## 3. Discrimination models, rigorously

- **General input space:** {all phenomena, pre-classification} — every
  discrimination model can in principle receive anything.
- **Standard input space:** {all phenomena within the current domain / universe of
  discourse} — what is actually used; objects outside it need a second
  discrimination model composed in front (e.g., "positive externality" presupposes
  "economic activity").
- **Output:** exactly two bare labels — {concept, not-concept}. One cut always
  produces BOTH a positive and a negative concept.
- **Labels carry no properties.** The concept's properties live in the intension,
  which is the model's judging criterion — not its output.
- **Definition ≠ model.** A definition is language material FOR building the model
  (and exists only for explicit models); reciting it is not possessing the model.
  Implicit discrimination models (e.g., recognizing sadness, a phoneme) exist
  without any statable definition.
- **Recognition ≠ generation (判别能力 ≠ 具象能力).** A discrimination model can
  classify an object when handed one; it cannot enumerate the extension from the
  label. "Sees a problem, picks the right formula" and "names the formula, lists
  situations it solves" are different abilities requiring different drills — train
  the one the target use needs.

## 4. Connection models, with admission tests

Definition: a mapping from one concept's extension (input space) to another's
(output space), used to infer an unknown state from a known one. All physical laws
are connection models. Before accepting a stated relation as one, check ALL five:

1. Are both sides used as VARIABLES (ranging over extensions), not as two constants?
   ("Humans include men" relates constants — not a model.)
2. Do input constants NOT belong to output constants? (Belonging → it is a
   discrimination model in disguise: "all men are human" is really
   {men} → {human, not-human}.)
3. Does every input value map to exactly ONE output value? (Non-unique → no
   inference performed; not admissible.)
4. Is it used to infer a target state from a known state (directional)?
5. Does each concept in it have a matching discrimination model? (Without them the
   model's input space is undefined for the learner — see object-layer loss.)

## 5. Correspondences

Definition: one constant → one constant (a name↔meaning link, a fact, a
meaning→motor-output link). No general mapping to induce. Establishment mechanisms
differ by kind:
- Declarative links: memorize + retrieval practice.
- Motor/production links: FIND the correct output first — with an external grader
  whenever the learner cannot yet perceive their own output — then proceduralize
  through repetition.
Repetition is the correct method here (fluency, not generality), which is why the
novelty requirement does not apply to correspondences.

## 6. Three worlds, and why carvings are task-relative

Physical world → (abstraction) → meaning world (concepts + relations, representing
events) → (reference links, 指代) → language world (symbols + organization rules).
Symbols are themselves concepts; every reference link presupposes two discrimination
models. Concept carving is chosen by the subject's goal; multiple carvings of the
same phenomena are valid, and a carving's legitimacy comes from the predictive
success of the connection models built on it — not from matching some pre-given
"correct" decomposition. Practical consequence: never present one extracted
structure as the unique truth of a material; present it as the carving that serves
the stated task.
