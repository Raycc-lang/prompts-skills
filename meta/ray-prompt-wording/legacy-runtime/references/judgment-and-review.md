# Designing prompts for independent judgment

Load when the target task asks for an independent judgment, comparison,
recommendation, diagnosis, verification, or selection. Skip the neutral-framing
rules when the user explicitly requests advocacy, persuasion, or exploration of one
side; in those tasks the direction is part of the goal.

## Neutralize directional framing

A user's stated preference, suspicion, or expected conclusion is context about the
request, not evidence that the conclusion is correct. Preserve it when it is a real
constraint, but do not let it silently determine which evidence the target model is
asked to seek.

For independent assessment:

- Treat the user's preferred conclusion as a hypothesis rather than a premise.
- Define criteria and evidence needs so a contrary conclusion remains possible.
- When gathering evidence, include information that could support or weaken plausible
  alternatives instead of searching only for confirmation of the user's wording.
- Do not manufacture symmetry. If the evidence is genuinely one-sided, the conclusion
  may be one-sided too; neutrality concerns the procedure, not forced balance.
- Keep user requirements distinct from user predictions. "Choose the cheapest option"
  is a decision criterion; "I think option A is best" is not evidence that A wins.

A directional request such as "find the advantages of option A" can be valid when
one-sided exploration is the intended task. Do not rewrite advocacy into neutral
assessment unless the user's actual goal is to decide what is true or best.

## Define criteria before the conclusion

For evaluative tasks, establish the decision criteria before judging the candidate
or choosing the overall result where feasible. Derive them from the user's objective,
hard constraints, supplied evidence, and relevant domain standards rather than from
features noticed only after seeing a favored answer.

Use this order when it materially improves the decision:

1. Define the criteria and distinguish hard constraints from preferences.
2. Gather the evidence relevant to each criterion.
3. Make criterion-level judgments from that evidence.
4. Resolve conflicts using stated priorities or an explicit tradeoff.
5. Synthesize the overall conclusion only after the component judgments.

Do not ask for a total score first and then category scores that merely explain it.
Use numeric scores or weights only when the scale has a real interpretation or helps
a specified decision; otherwise use concrete qualitative judgments such as strong,
partial, weak, unmet, or unknown.

Ask for observable evidence, concise rationale, or criterion-level results rather
than hidden chain-of-thought. The procedure should make the basis of the decision
inspectable without requiring private reasoning traces.

## Proportionate use

A rubric is unnecessary for every factual check or simple generation task. Use this
procedure when an overall judgment could otherwise be driven by first impressions,
leading framing, or post-hoc justification. Keep the smallest set of criteria that
can change the decision.
