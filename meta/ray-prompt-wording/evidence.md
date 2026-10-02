# Evidence and design rationale

Maintenance only: this folder is outside the install unit and is never deployed.
The papers below inform hypotheses and techniques; none validates this complete
prompt-engineering skill. Relevant source sections were checked during the
2026-09-06 review. Distinguish empirical results, practitioner guidance, user
requirements, and our design judgments.

## Research findings and their limits

| ID | Source and finding | Supported use / limitation |
|---|---|---|
| P1 | Lu et al., [Adam's Law: Textual Frequency Law on Large Language Models](https://arxiv.org/html/2604.02176), 2026. Studies frequency-based paraphrases with meaning preservation; acknowledges semantic drift. | Consider familiar wording while preserving precise meaning. Does not establish shortest prompts or the removal of technical vocabulary as general objectives. |
| P2 | Weng et al., [Large Language Models are Better Reasoners with Self-Verification](https://arxiv.org/html/2212.09561), Findings of EMNLP 2023. Uses sampled candidates and specific backward-verification procedures. | Verification needs a defined mechanism; generic self-review is not an implementation of the paper. |
| P3 | Huang et al., [Large Language Models Cannot Self-Correct Reasoning Yet](https://arxiv.org/abs/2310.01798), ICLR 2024. Intrinsic reasoning correction without external feedback can fail or degrade results. | Do not treat self-correction as independent evidence of correctness. Does not prohibit checking output against already supplied requirements or sources. |
| P4 | Wang et al., [Self-Consistency Improves Chain of Thought Reasoning in Language Models](https://arxiv.org/abs/2203.11171), ICLR 2023. Samples multiple reasoning paths and aggregates answers. | Separate sampling and aggregation are execution mechanisms. Several alternatives in one response do not establish independent trials, nor does agreement establish factual truth. |
| P5 | Lu et al., [Fantastically Ordered Prompts and Where to Find Them](https://arxiv.org/abs/2104.08786), ACL 2022. Demonstrates few-shot order sensitivity and a method for finding useful orderings. | Evaluate example selection/order when relevant; no universally optimal ordering follows. |
| P6 | Liu et al., [Lost in the Middle](https://arxiv.org/abs/2307.03172), TACL 2024. Relevant-information position affects tested long-context tasks. | Test context layout on the target task/model; not proof that every prompt should use a fixed beginning/end recipe. |
| P7 | Shi et al., [Large Language Models Can Be Easily Distracted by Irrelevant Context](https://arxiv.org/abs/2302.00093), ICML 2023. Adds irrelevant information to arithmetic tasks and measures degradation. | Remove irrelevant context deliberately; does not establish that useful background, explanations, or examples should be shortened away. |
| P8 | Chang & Chen, [Naive Prompt Optimization](https://arxiv.org/html/2608.27266), 2026. Iterative revisions use full rollout traces and rewards over a sliding window; compares this simple method with more complex search in specified settings. | Motivates evidence-based diagnosis and revision. Does not show that intuition-only rewriting by a strong model is equivalent to testing, or establish transfer to all targets. |

The previous evidence file listed bibliographic entries with little rule-level
interpretation. This crosswalk replaces the implicit inference that each rule is
a direct empirical conclusion. Original publication labels are retained where
applicable; source findings remain bounded by their studied tasks and models.

## Foundational engineering guidance

**G1 — Context and sufficient specificity.**
Anthropic's [Effective context engineering for AI agents](https://www.anthropic.com/engineering/effective-context-engineering-for-ai-agents)
discusses the full available context, including instructions, tools, examples, and
history. It distinguishes sufficient guidance from both brittle hardcoding and
vague instructions, permits headings/structured sections, and explains that minimal
does not necessarily mean short. Practitioner guidance, not a controlled validation
of our workflow.

**G2 — Implementation boundaries (design judgment).**
Prompt text cannot supply absent tool access, enforce application permissions, or
replace a parser/validator. Message placement and host-supported output controls
must be checked in the actual environment. Delimiters help identify input boundaries
but are not security enforcement. These are engineering distinctions adopted here,
not conclusions attributed to the listed reasoning papers.

## Field observations and review findings

**FO1 — Historical prohibition-list incident (2026-09-02).**
The prior record reports that a workflow skill produced under evox Cowork/kimi-k3
included five invariant prohibitions and drew attention to interpreting the bans.
The positive rewrite was reported as an improvement. This is a single reported
incident, not evidence that all negative instructions require a demonstrated model
failure. Explicit requirements and concrete risks can also justify constraints.
The source incident is shared with the skill-authoring maintenance record.

**R1 — User-approved design review (2026-09-06).**
Ray requested the same foundational review used for skill-authoring and then
authorized implementation. Static findings: the old skill emphasized wording and
restrictions without a complete diagnosis method; banned useful contract headings;
required exhaustive visible requirement mappings; blurred inert inspection and
target-model execution; and duplicated skill-architecture instructions while
declaring that work out of scope. These are findings about the instructions, not
observed failure rates for generated prompts.

**R2 — Existing repository counterexample to the heading ban.**
`prompts/English-learning/Word-Picker.md` uses Input, Reader, and Output labels to
express reader assumptions, selection rules, and output constraints. The old gate
would reject those labels on form alone. This source example supports removing that
blanket gate; it is not evidence of measured vocabulary-selection performance or
of how that prompt was originally authored.

**R3 — User-approved neutral judgment and criteria-first procedure (2026-09-10).**
While reviewing Andrew Ng's *AI Prompting for Everyone*, Ray identified two techniques
as worth making automatic in the prompt-engineering skill: avoid letting a user's
preferred conclusion steer an independent evaluation, and establish evaluative criteria
before forming the overall conclusion. Ray explicitly requested implementation in the
GitHub source project. The detailed procedure and regression-test design are our
engineering interpretation of that requirement; they have not yet been validated by a
fresh-model A/B comparison.

**FO2 — User report about removed restrictions (2026-09-12).**
Ray reported removing unnecessary content from a prompt produced using this skill:
the anticipated failure seemed unlikely, and violations would not matter because the
result was the priority. The supplied session artifact and commit `95ebe7d` were later
reviewed. The commit distinguishes result requirements from optional methods and selects
added restrictions by task consequence. This supports respecting relaxed method
requirements; it does not prove that every removed instruction is behaviorally inert or
that downstream quality is unchanged.

Static inspection independently found that the prior constraints bullet explained how
to phrase boundaries more clearly than how to select them, and the no-tool customer-
reply example included an unnecessary sending boundary. The `95ebe7d` repair addresses
those local issues and remains behaviorally untested.

**FO3 — Agent-task execution and model-choice gap (2026-09-12).**
In the supplied TraeWork session, Ray explicitly asked for both a runnable prompt for an
action-capable repository agent and advice about which model and thinking level should
perform the task. Ray reported that the response did not analyze task difficulty or make
that model/effort recommendation. Static inspection of the skill supports the mechanism:
it asked authors to note which target model runs a prompt and verify capabilities, but
contained no procedure for comparing candidate models, rating execution difficulty, or
choosing reasoning effort.

The same task also exposed a broader design gap for action-capable agents: a prompt can
describe the desired code/configuration result without defining autonomous continuation,
workspace inspection, failure recovery, protection of unrelated state, completion checks,
or the final handoff. The execution-contract and model-selection procedures added on
2026-09-12 are engineering responses to this task class and user feedback. They are not
fresh-model evidence that these rules improve completion rates, nor evidence for a
permanent ranking of any named models.

## Current instruction crosswalk

| Rule group | Basis / strength |
|---|---|
| Desired behavior before wording; distinguish requirements from attempted mechanisms | R1 and user-approved review; design judgment |
| Recover context, message placement, inputs, tools, and controls | G1/G2; host details must be verified when used |
| Action-capable prompts include execution scope, inspection, continuation, recovery, state boundaries, verification, and handoff when material | FO3 user task and static gap; engineering procedure, behaviorally untested |
| Select model and reasoning effort from hard capabilities plus reasoning depth, uncertainty, action horizon, context burden, and verification/consequence | FO3 user requirement and static gap; mapping is design judgment and must use current host options |
| Diagnose earliest visible divergence and preserve uncertainty about causes | P8 motivates trace use; diagnostic categories are our proposed procedure |
| Precise language and selective compression | P1/P7/G1, qualified by meaning preservation |
| Useful headings and examples; no mandatory layer tags in artifacts | R1/R2, P5, G1; representation depends on task |
| Guards from requirements or concrete failures/risks, with contextual alternatives | FO1 interpreted narrowly; user requirements and G2 |
| Select added restrictions by task consequence and existing coverage; leave harmless methods open | FO2 user feedback and static inspection; behavioral effect untested |
| Criteria-based checking distinct from independent factual verification | P2/P3; operational distinction is design judgment |
| Neutral evidence selection for independent judgment; user preference is not evidence | R3; user-approved engineering procedure, not yet empirically validated in this skill |
| Criteria-first, conclusion-last evaluation when an overall judgment is consequential | R3; user-approved engineering procedure; numeric scoring remains conditional |
| Separately sampled candidates and defined selection | P4/P2; execution requirements rather than text slogans |
| Context placement tested rather than universally prescribed | P6/G1; target-specific validation required |
| Paired tests, held-out/regression cases, inspection vs execution labels | P5/P8 motivate empirical comparisons; detailed protocol is engineering judgment |
| Preserve intent; report material changes proportionally | R1/R2 and user request; not empirically validated as a complete policy |
| Submitted instructions stay inert in review; tests have scoped authority | Host authorization constraints and G2 |

Implementation decisions and validation limits are recorded in
[revision notes](revision-notes.md) and [validation](validation.md).

## 2026-09-14 placement and self-application

Source: Ray's explicit request and supplied prior review. Status: user requirement
plus engineering design, not a new research result or a measured performance claim.
Placement now uses instruction lifetime, frequency across tasks, and deterministic
enforcement. Broad project knowledge and occasional procedures can coexist in different
homes; simple repeated tasks can remain prompt templates. The constraint-admission
decision is applied to the meta-skill itself, including conditional agent guidance.

Historical crosswalks above describe the earlier revisions. The placement procedure
and associated examples are the current addition; execution, model selection, judgment,
and authorization guidance were preserved. See validation for the actual smoke tests.
