# Design for independent judgment

Preserve what the user wants to achieve without treating their predicted answer as established. "Cost matters most" is a preference; "A must be cheapest" is a claim to examine.

For an independent comparison, diagnosis, recommendation, or verification:

- Frame a suspected conclusion as a hypothesis. Ask for evidence that supports or weakens it and plausible alternatives, rather than merely asking the model to justify it.
- Establish the criteria from the goal, constraints, and relevant standards before the overall judgment. Assess evidence against those criteria, handle conflicts using stated priorities, then form the conclusion.
- Distinguish known facts, user interpretations, and model inferences. Mark consequential gaps and uncertainty rather than inventing an explanation.
- Make the basis inspectable through evidence and concise reasons. Use scores or weights only when they have a meaningful interpretation; a small factual question does not need a rubric.

This describes how to assess, not a compulsory answer layout. The final response may lead with the conclusion. Do not demand private reasoning traces or force equal weight on unequal evidence.

Preserve advocacy, persuasion, or exploration of one side when explicitly intended. If the distinction is genuinely unresolved and changes the task, clarify it. Do not convert "help me present the advantages of A" into an unwanted neutral comparison, or convert "is A actually better?" into a sales pitch.

Apply the same distinction while helping design the prompt: a user's proposed explanation for a poor answer is evidence to investigate, not proof of its cause.
