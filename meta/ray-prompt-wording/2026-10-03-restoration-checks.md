# Candidate behavior record

Recorded: 2026-10-03. Candidate: capability-restoration package documented in [the comparison](2026-10-03-capability-restoration.md). Tests used fresh agents with the candidate path explicitly provided; the parent conversation was not inherited. This tests loaded behavior, not automatic selection. No target task was executed.

## Independent judgment and advocacy

Request A: improve a prompt that says switching to Vendor A is clearly right but asks whether to switch. Priorities: reliability, migration effort, total cost. Evidence: estimates, incident logs and migration notes for both vendors. Make it reusable; model already selected.

Actual prompt:

> Help me decide whether to switch from the current vendor to the candidate vendor. Evaluate reliability, migration effort, and total cost using the supplied cost estimates, incident logs, and migration notes for both.
>
> Treat my initial preference as a hypothesis. Assess evidence supporting and challenging it, explain the tradeoffs, and recommend whether to switch. Ground your recommendation in the evidence, distinguish facts from inferences, and identify consequential gaps or uncertainties that could change the decision.
>
> Current vendor: [name]
> Candidate vendor: [name]
> Initial preference, if any: [preference]
> Additional constraints or priorities: [details]
>
> Evidence:
> [Insert materials for both vendors]

Request B: a short one-off prompt to prepare a persuasive presentation of Vendor A's advantages. Choice already settled; use supplied evidence; model already selected.

Actual prompt:

> Help me prepare a persuasive presentation explaining Vendor A’s advantages. The vendor choice is already settled. Use the evidence below to develop clear talking points supported by specific examples or figures. Keep claims within what the evidence supports.
>
> Evidence: [insert materials]

Observed: A retains the user's criteria while treating the preferred conclusion as a hypothesis and creates reusable inputs. B preserves advocacy rather than reopening the decision.

## Placement and agent completion

Request: all repository work must support Python 3.11; CI enforces formatting; monthly release review checks migrations and staged rollout. Today's task is implementing and verifying a fix for a CLI crash on empty input. Explain instruction homes and provide today's prompt. Model settled; do not modify repository or create a skill.

Actual placement advice: Python compatibility in AGENTS.md; formatting in existing CI; release-review procedure in a skill, or a reusable template if a short checklist suffices; today's fix in a one-off prompt.

Actual prompt:

> Fix the CLI crash on empty input. Inspect the relevant repository guidance and code, reproduce the crash, and determine the expected empty-input behavior from existing documentation and tests. Implement the fix while preserving Python 3.11 compatibility and unrelated changes. Verify empty input and representative valid input using appropriate checks, and resolve failures caused by the fix. Report what changed, what you actually verified, and any remaining blockers. If the expected behavior is unclear and materially affects the fix, ask a focused question.

Observed: differentiated homes and preserved completion, verification, recovery and scope. The agent did not act on the repository.

## Diagnosis

Request: diagnose a severity-classification prompt whose output includes ID, severity and policy clause but invents definitions. Only reports were supplied, not the company policy. No test campaign wanted.

Actual finding: the first failure was missing policy input; output format worked. Stronger wording cannot supply the absent policy. Supply it or enable retrieval.

Actual repair:

> Classify each report using the company severity policy supplied below. Return ID, severity, and the applicable policy clause. If the policy is missing or does not resolve a report’s severity, identify the missing information and request clarification; do not invent severity definitions or policy clauses.
>
> Company severity policy: {{policy}}
>
> Reports: {{reports}}

Observed: repaired context delivery and missing-input behavior, retained output fields, and did not launch tests.

## Review only

Request: findings-only review of a rewrite from “Extract unfamiliar words for a B1 reader, once each, in passage order. Return None if there are no qualifying words.” to “List difficult words.”

Actual findings: lost the B1 unfamiliarity criterion, explicit extraction from the passage, uniqueness, passage order, and the required None response. No unrequested rewrite was produced.

Observed: identified semantic and functional loss rather than treating shorter prose as automatically better.

## Preservation review

A third agent compared the candidate against the archived September entrypoint and its six references, with the current user requirements supplied. It reported no material omissions or internal conflicts and explicitly distinguished inspection from a performance test.

All observations above concern this small sample. They do not establish downstream task success or a reliable failure rate.
