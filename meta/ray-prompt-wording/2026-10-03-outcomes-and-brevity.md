# Outcome clarification and concise wording

Recorded: 2026-10-03 (Asia/Shanghai).

Ray requested two changes after comparing the current skill with OpenAI’s [A model guide for the GPT-6 family](https://openai.com/index/practical-guide-building-gpt-6/): help clarify the outcome he wants when it is still forming, and explicitly prefer the shortest clear, faithful prompt.

The opening now makes outcome clarification part of the skill’s purpose without choosing Ray’s goal for him. The editing rule now prefers the shortest wording that preserves meaning and necessary context, includes only guidance serving the desired result, and leaves routine execution choices to the model.

These replace two existing passages. The current name, selection metadata, clarification threshold, openness, constraint-admission rule, and distinction between authoring guidance and target-agent instructions are retained. No mandatory questionnaire or output checklist was added. The blog is supporting practitioner guidance, not proof that fewer words always produce better results; Ray’s explicit preference is the basis for the brevity default.

Validation: the personal skill passed quick_validate.py and git diff --check. The diff was reviewed against the two approved revisions. Existing UI metadata still fits the skill’s scope. Author-side boundary review: a settled goal still proceeds directly to editing; an unresolved goal can be clarified when the distinction matters; necessary context remains even when it makes the prompt longer. These are static checks and an author walkthrough, not independent behavioral trials or measured improvement. Final saved contents are checked across GitHub and the installed personal skill.
