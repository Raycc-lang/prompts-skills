# Chosen direction and proportional intake — 2026-10-21

## Basis and decisions

Ray clarified that this skill is for learning an already chosen ability rather than
deciding whether to pursue it. He explicitly accepted the refinement that a direction
may be chosen while its target ability still needs clarification or decomposition.

Updated the trigger description to encode this boundary before loading. Removed the
redundant when_to_use field. Allowed a recognizable use situation without a date,
starting prerequisites without a failed attempt, and constraints only where they
change the requested design. Replaced missing-field quotas with focused clarification
and useful independent progress. Preserved the requirement for an actual episode
before diagnosing a failure.

Explicit plan/decomposition requests now receive their requested coverage even when
practice feedback is already useful. Interactive practice still focuses on a sub-task.
A requested sequence uses prerequisites and demonstrated competence, with the existing
boundary that scheduling and sequencing are not deductions from 渐构 alone.

Preserved the framework's task-relative input/output analysis, types, learner-specific
recommendations, paired materials, memorization versus generalization distinctions,
diagnosis evidence bars, extraction route, quantity restrictions, and epistemic limits.
No empirical claim about better learning or universal sequencing was added.

## Forward check

A fresh subagent received the revised package and this request:

> I've decided to learn how to read and explain Linux service logs so I can diagnose
> failed services. I can use the shell, know how to start and stop a service with
> systemctl, and can read simple English error messages. I've never tried log
> diagnosis before. Break the ability down into sub-skills and give a sensible
> sequence with practice and checks. I don't have an exam or deadline.

Criteria: proceed from the chosen direction and given prerequisites; no required past
failure, deadline, or schedule; deliver decomposition, sequence, practice, and checks;
keep claims about a beginner's abilities provisional.

Observed: the response supplied an input/output target, six sub-skills, worked sample
incidents, a sequence from interpretation to retrieval to mixed incidents, and checks
on fresh cases. It called the plan provisional and explicitly separated its sequencing
judgment from the framework. It did not ask for a failed attempt or time budget.
The initial test instruction prohibited commands; a clarification permitted read-only
commands solely to load the skill. This was a harness access clarification, not a
learner-intake question. No exercise commands were executed and no files were created.

Actual opening:

> Your target is to turn an unfamiliar service failure into an evidence-backed
> explanation and a useful next check. Since you already use the shell and systemctl,
> start with interpreting a small incident, then learn to retrieve the right evidence.

## Checks and limits

Package validation, local links, icons, UI metadata, whitespace, and author consistency
inspection passed. One fresh-agent plan exercises execution; no prior-version comparison
or learning-outcome study was run. The skill was explicitly loaded, so automatic host
selection is untested. Description boundaries were inspected, not measured in the host.
No model override was supplied; exact serving model/settings were not exposed.
