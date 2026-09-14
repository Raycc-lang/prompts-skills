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

# Validation — 2026-09-12 — unnecessary constraints

Mechanical checks passed at the time of commit: `git diff --check` and resolution of
local Markdown links throughout the runtime package. Runtime edits and maintenance
notes remained separated.

Static review: the revision retains explicit requirements and consequential-risk
guards while making unsupported additions optional. The no-tool example retains
factuality and conditional clarification. The new fictional example distinguishes
free organization from an explicit no-table requirement and a fixed import format.
These are author-side inspections, not generated outputs from fresh model sessions.

Ready-to-run comparison: use the prior git version and revised package in otherwise
matched fresh author sessions. Supply the project-update packet in worked example 4,
then separate variants with an explicit no-table request and a fixed three-field
import contract. Inspect whether generated prompts preserve progress, remaining work,
and blockers; avoid invented formatting bans in the flexible case; and retain the
explicit requirements in the changed cases. Give downstream runners the resulting
prompts and identical notes, checking factual coverage and consumer usability rather
than adherence to invented rules. No such comparison has run.

The supplied session artifact was subsequently reviewed. It confirms the broader
prompt-authoring context but does not provide a controlled downstream comparison of the
removed section. The user's report remains evidence of editing friction and priorities,
not proof that deletion preserves model behavior in every case.

# Validation — 2026-09-12 — action agents and model/effort selection

## Static integration checks

Inspected the revised entrypoint and `references/model-and-effort-selection.md` after
writing them. The link is resolvable inside the install unit, the new reference contains
runtime guidance rather than maintenance provenance, and the detailed evidence remains
under `meta/`. The entrypoint keeps the model-selection procedure conditional instead
of adding a mandatory recommendation to every prompt task.

The procedure separates hard execution capabilities from task difficulty and separates
model choice from reasoning effort. It explicitly rejects three common but unsupported
shortcuts: judging difficulty from output/diff size, assuming maximum effort is always
best, and assuming extra reasoning can repair missing tools or context.

## Regression cases for difficulty classification

Use matched fresh author sessions with the revised skill and inspect the recommendation,
not merely the generated prompt.

1. **Bounded rewrite.** Ask for a grammar-preserving rewrite of a short supplied
   paragraph with no tools and an obvious acceptance criterion. Expected: a fast capable
   model and low/ordinary reasoning are sufficient; recommending the most expensive
   agent setup without another reason is over-selection.
2. **Repository configuration task.** Use the multi-model proxy task from the supplied
   TraeWork example: inspect an unfamiliar repository, discover provider capabilities
   with live credentials, edit configuration, preserve secrets/unrelated state, run
   probes/tests, and recover from failures. Expected: classify the execution burden as
   high despite a potentially small diff; prefer a strong coding/agent model and a high
   reasoning setting when those are available. A fast/low-effort choice solely because
   "it is only configuration" misses the relevant difficulty.
3. **Known mechanical edit.** Give the exact file, exact JSON change, no discovery,
   no ambiguity, and one deterministic validation command. Expected: choose lower
   reasoning than case 2 even though both ultimately edit configuration.
4. **Missing capability.** Require a tool or modality one candidate lacks. Expected:
   remove that model from consideration rather than compensating with higher thinking.
5. **Escalation.** Start with a capable model on a diagnosis task, then provide an
   observed failure caused by missing source material. Expected: recommend obtaining the
   missing material, not merely raising reasoning effort.

These are expected decisions from the authored procedure, not measured model-quality
results.

## Model-name and effort-level robustness

Repeat case 2 with different fictional or currently available candidate names while
keeping their described capabilities fixed. The recommendation should follow capability
and task fit rather than a hard-coded brand ranking. Change the host's effort labels
while preserving their relative meaning; the procedure should map to the closest
available setting rather than require literal `low/medium/high/extra-high` names.

No controlled cross-model, cross-effort, latency, or cost benchmark was run. The new
rules are structurally validated and ready for fresh-session testing, not empirically
proven to select the globally optimal model for every host.

# Validation — 2026-09-14 — placement and retained capabilities

## Checks performed

Frontmatter, names, description lengths, runtime Markdown resource links, and diff
whitespace passed. The repository-specific optional when_to_use field is preserved.
The entrypoint changed from 16,250 bytes / 245 lines to 9,807 bytes / 147 lines.
Action guidance remains in the runtime package as a selectively loaded reference.

A fresh author session received the revised runtime package and three requests:
a one-off meeting-update prompt; a mixed repository/runtime/release/typo request;
and an unfamiliar API-configuration task with supplied fictional Fast/Deep model
capabilities and low/high effort settings. It returned usable drafts without external
actions. Exact output is in
[author output](experiments/2026-09-14-placement/author-output.md).

Observed: the one-off remained a prompt; the mixed request separated project-wide
compatibility and lint invocation from the monthly skill and today's typo task,
leaving existing CI enforcement intact. The third response preserved discovery,
execution, recovery, and verification and selected Deep/high for dependent diagnosis
despite the possible one-line diff. Model names in that fixture are hypothetical.

A separate runner executed the generated meeting prompt on two input packets.
It preserved completion and the Friday owner/date, kept an unaccepted supplier change
as a proposal, reported missing follow-up ownership/timing without inventing it, and
handled notes with no decisions or assigned work. Exact output is in
[runner output](experiments/2026-09-14-placement/runner-output.md).
The author inspected substantive coverage; this was not blinded grading.

## Reproduction inputs and limits

Use the packets in [cases](experiments/2026-09-14-placement/cases.json).
Both sessions used the host-inherited model/configuration; the exact model identifier
was not recorded. Only the skill/runtime references and task packet were supplied
to the author; only its generated meeting prompt and notes were supplied downstream.
Author instructions to save outputs were sent afterward without asking for revisions.

These are candidate-only smoke tests. No prior-version comparison, live provider task,
automatic host selection, actual AGENTS.md loading, cross-model comparison, or installed
copy synchronization was performed. Placement and artifact decisions were exercised,
not deployment reliability or measured superiority. This exercise does not establish
that every generated instruction is necessary. Removal comparisons remain a supported
evaluation method, not a claimed experiment run in this revision.
