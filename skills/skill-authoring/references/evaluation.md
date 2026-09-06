# Evaluate the claim, not the checklist

Load before validation or when reviewing a skill's test claims. Scale the effort to
the consequence and requested scope. A small check is useful when described accurately.

## Choose the comparison

| Claimed result | Relevant comparison |
|---|---|
| New skill improves decisions or output | Same agent/task/tools, with and without the skill |
| Revision fixes a defect | Prior and candidate versions on the failing case and a case that should still work |
| Consolidation makes a workflow reusable | Existing workflow and relocated package: preserved decisions, resources, and requested output |
| Description improves selection | Actual host/library, positive requests and nearby requests that should select differently |
| Helper script fixes a mechanical error | Execute the failing condition and a valid case; distinguish this from agent-level quality |

If testing an authoring skill, evaluate both levels: the skill it produces and what
a later agent does with that produced skill. Valid frontmatter or a passing helper
does not establish better authorship or better downstream decisions.

## Prepare a small discriminating test

1. Specify the expected result before inspecting candidate outputs. Use user-approved
   examples or explicit requirements; for subjective work name concrete preferences.
2. Include a typical request and a case that changes a decision-relevant assumption.
   Use held-out material when available. Add a known regression case for revisions.
3. Supply only what deployment provides: the installed package, task inputs, and
   normal tools. The author's transcript and maintenance notes must not silently
   supply missing knowledge. Use fresh agent sessions when available and authorized.
4. Keep model, task inputs, tools, and budget comparable between conditions. For
   a workflow-migration comparison, preserve the original workflow's legitimate
   knowledge access; relocation should not be confused with removing needed inputs.
5. Compare actual outputs and trajectories: decision quality, requirement adherence,
   unsupported claims, missed cases, needless questions, tool calls, and elapsed effort
   when measurable. Blind output labels for subjective judging when feasible.

Separate factual failures from taste differences and uncertain judgments. Repeated
runs increase confidence where model variability matters; one pair is a smoke test,
not a reliable estimate of general effectiveness. Do not fabricate timings or grades.

## When execution is unavailable

Perform available mechanical checks and a clearly labeled walkthrough. Save the
request, supplied context, expected outcome, and comparison condition so a later run
can execute it. Identify what was not tested. Provide the candidate if the user
requested implementation, with its uncertainty; lack of a benchmark is not a reason
to refuse an otherwise useful change.

Distinguish these claims in the delivery and maintenance record:

- **Mechanics checked:** resources resolve, helpers run, or relocation succeeds.
- **Behavior exercised:** an agent used the artifact on specified inputs; name
  whether this was a fresh session or the author retaining extra context.
- **Comparative evidence:** baseline and candidate outputs were compared; record
  the observed difference and its limits.
- **Predicted / not run:** expected behavior only, including simulated walkthroughs.

## Maintenance record

Keep records outside the install unit. A compact entry can contain the task and
criterion, artifact version, source of the criterion, execution context, actual
output locations, observed difference, and unresolved limitations. For private tasks,
leave sensitive inputs/outputs in their original private workspace and record only
the minimum non-sensitive finding. Never label an anticipated failure as an observed one.
