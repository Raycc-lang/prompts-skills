# Validation — 2026-09-06

## Author-side grading exercise

Source: `prompts/English-learning/Word-Picker.md`, inspected in this session.
Applied the revised grading criteria to the source and a hypothetical shorter
rewrite: "List difficult words from the passage."

The source preserves a reader profile, contextual selection threshold, omission
on uncertainty, passage order, uniqueness, list-only output, and the None case.
The shorter rewrite drops these requirements or makes them ambiguous. The source's
Input/Reader/Output labels are functional boundaries and do not justify a negative
finding. This is an author-side inspection, not a run of vocabulary extraction or
an independent evaluation of the revised skill.

## Demonstration included in the package

`references/worked-examples.md` contains a fictional customer-reply case, a missing-
policy diagnosis, and a grading example. The customer-reply prompt was constructed
using the revised workflow: identify the intended goal, distinguish it from five
mandatory questions, establish input authority, and define conditional clarification.
All depicted failures are explicitly fictional. No performance results are claimed.

## Ready-to-run held-out authoring comparison

Compare separate fresh author sessions with and without this skill, using the
same model/tools/budget. Supply only this source packet:

> Improve this prompt for an assistant that drafts meeting summaries from transcripts:
> "Always return exactly five action items, each with an owner and a due date."
> I want a complete, usable record of commitments. Some meetings have fewer than
> five commitments; others have more. Owners and due dates are sometimes unstated.
> The assistant has no tools and only drafts the summary; it cannot assign work.

Before reading outputs, grade whether each generated prompt preserves all actual
commitments, avoids padding/truncation, distinguishes unknown owner/date from known
values, and stays within drafting scope. The five-item instruction is explicitly
contradicted by the user's stated goal in this packet, not silently discarded.

Give later fresh runner sessions the generated prompts and these fictional inputs:

- Typical: "Ari: I will send the design by Friday. Bo: I'll review it; I don't know
  when yet." Expected: two commitments; retain Ari/Friday and Bo/unknown due date.
- Empty: "We discussed the design. No action was agreed." Expected: no invented items.
- Boundary: six distinct named commitments with dates. Expected: preserve all six.

Save exact outputs and compare both authoring quality and downstream results. Keep
grader instructions out of the runner context. No such comparison was run here.

## Ready-to-run diagnosis regression

Packet: a report-classification prompt refers to "the attached policy"; the actual
model input contains only the report, and the observed answer uses incorrect labels.
Expected diagnosis: missing policy is a visible cause to investigate. Supply it or
define an incomplete-result fallback. Adding "strictly follow the policy" alone
does not repair the absent input. Change the packet so the policy is present but
two clauses conflict; the repair should now resolve precedence rather than ask for
the same policy again. These outcomes are expectations, not reported passes.

## Mechanical checks

Passed: frontmatter structure, local Markdown resource links in all three runtime
files, maintenance separation, and `git diff --check`. Inspected the shared template:
execution context is conditional, headings are optional, and author notes/test records
remain outside the copyable prompt. The package contains text instructions and no
executable helpers. Static checks cannot establish behavioral efficacy or routing.

No fresh target-model evaluation was run in this session. The authoring model retained
the review context, so its walkthroughs are not substituted for a controlled test.
