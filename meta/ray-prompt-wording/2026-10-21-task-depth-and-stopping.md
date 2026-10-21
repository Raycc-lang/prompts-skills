# Task depth and stopping — 2026-10-21

## Basis and scope

Ray requested updates to the repository and the installed Work Mode skills. He
accepted a nuanced stopping condition: simple prompts may need only clear, concise
wording; agent prompts may need help defining intended objectives and completion.
He did not accept adding a special rule about preserving the specific relationship
asked about. No such rule was added to this package.

Preserved the repository's October 9 fact-assertion and concrete-obstacle safeguards,
which were missing from the installed Work Mode copy. Preserved independent judgment,
one-off/reusable use, placement, model/effort selection, execution, and evaluation.

## Decisions

- Scale help by unresolved decisions and the requested service, not prompt length.
- Refine settled wording directly; clarify unsettled goals without selecting Ray's
  priorities or inventing requirements.
- For agents, express the intended end state, scope, and evidence of completion.
  Distinguish attempts, artifacts, verified outcomes, and partial results.
- Stop failure-driven rule accumulation when no concrete wording defect is visible.
  Keep explicit wording-polish requests valid; do not use the stopping rule to skip
  consequential gaps in an agent's objective or completion criteria.

## Forward checks

Fresh subagents used the prior GitHub package at f0f5ab0 and the revised package,
respectively, with the same three requests. Neither saw the maintenance record or
expected answers. No model override was supplied; exact serving model/settings were
not exposed by the agent interface. These are one pair of smoke runs, not a reliability
benchmark. The revised prompt was not subsequently executed by an app-building agent.

Requests:

1. Make clearer and shorter: "Please read the article that I provide and then give
   me a summary in plain English, but be sure to keep any caveats that matter."
2. Write an agent prompt: "Improve my app." Context: a small language-practice app;
   the user has not decided which improvement matters most.
3. Diagnose an exact delivered prompt requiring a plain-English summary preserving
   caveats. Source: "The pilot improved accuracy on familiar cases, but it has not
   been tested on unfamiliar cases." Complete output: "The pilot improved accuracy."
   No other instructions or tools. User asks whether the prompt needs changing.

Criteria: edit directly in case 1; preserve the open choice and identify objectives
and completion in case 2; distinguish the observed output failure from an evidenced
wording defect in case 3. Avoid invented restrictions and certainty about hidden causes.

Observed:

- Both variants produced a concise faithful sentence in case 1.
- Both offered discovery rather than silently choosing an app feature in case 2.
  The revised output additionally requested a specific scope and an observable way
  to check success for the recommended improvement; the baseline requested benefits,
  tradeoffs, and focused questions without explicit completion criteria.
- Both said case 3 did not indicate a necessary prompt change. The baseline also
  explicitly identified the loss of "on familiar cases." Thus this run does not
  demonstrate an improvement in failure diagnosis over the baseline.

Representative revised outputs:

> Summarize the article I provide in plain English, preserving any important caveats.

> Help me choose what to improve in my small language-practice app. Review the app
> and ask about any goals or user problems that would materially affect your
> recommendation. Explain the worthwhile options and their tradeoffs. For your
> recommended improvement, propose a specific scope and an observable way to check success.

> No prompt change is indicated by this run. "Preserve its caveats" clearly covers
> the limitation that unfamiliar cases have not been tested. The output omitted
> that limitation despite receiving it.

## Mechanical checks and limits

Validated all three revised packages with quick_validate.py; checked local resource
links, icon paths, UI description lengths and default prompt names, and whitespace.
Checked the diff against existing capabilities and the user's accepted scope.
Host automatic skill selection and repeated real-user outcomes remain untested.
