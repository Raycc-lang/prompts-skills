# Validation — 2026-09-06

## Subsequent paired experiment — 2026-09-08

A real Job_hunting consolidation task was authored once with and once without the
current skill using isolated Codex CLI 0.153.4 / GPT-6 Astra low sessions. The treatment
read the entrypoint and all references. Six fresh GPT-5.6 Luna low runner sessions per
artifact tested 37 source-derived criteria; both artifacts passed after evidence-based
adjudication of one blind-grader error. Both also passed independently reproduced
offline relocation/helper checks. The source and frozen packages remained unchanged.

This single pair demonstrated no downstream accuracy lift on the tested cases. The
treatment's installable package was 64.1% smaller through separation of optional
history/maintenance, but authoring took 16.0% longer in the observed run. These are
case-specific observations, not generalized efficacy, cost, or speed estimates.
The baseline already produced useful decision content, portability, and local tests.
The task contained rich existing rules and scripts; new-procedure discovery, live
search performance, other models, and authoring variance remain untested.

See the [complete report](experiments/2026-09-08-job-hunting/report.md) and
[protocol](experiments/2026-09-08-job-hunting/protocol.md). Private snapshots, exact
outputs, traces, blind grading, and adjudication remain under
`/home/<user>/skill-authoring-study-20260908/` in WSL. No runtime skill rule was changed.

The sections below preserve the earlier 2026-09-06 validation record.

## Actual review exercise: consolidate a private workflow

Input: the user's request and result from task
`01a075ae-b798-7061-8923-e071dd7d8a53`, "Expand reusable private agent skill".
Sensitive inputs and outputs remain in their original private location.

Applied the revised review path in this authoring session:

1. Intended difference: the source request asks for folder independence and a fuller
   reusable package, not a controlled improvement in résumé prose.
2. Decision content: installed references preserve source-backed selection and claim
   boundaries; the package is not merely a list of generic phases.
3. Comparison: source instructions and generated references support preservation;
   the trace reports relocation/mechanical tests. Fresh downstream comparison absent.
4. Result: retain useful material and distinguish migration evidence from unmeasured
   authorship quality. No repair to the private workflow made here.

This exercised diagnosis with the author retaining prior context. It is not an
independent test of the rewritten skill and provides no causal efficacy estimate.

## Author-side demonstration on a different task

Fictional source requirements (no claimed real trajectory): write a reusable skill
to group duplicate bug reports. Merge only if component, affected version, and
reproduction steps match. Identical error text alone is insufficient. Missing
version leaves a report pending; it must not block grouping complete reports.
Keep all original report IDs. The user asks only for a grouping recommendation,
not an update to a ticket system.

The intended difference is to prevent error-message-only grouping. From the
requirements, extract the three-field match decision, unknown-field branch,
preservation constraint, and recommendation-only scope. A compact generated artifact:

```markdown
---
name: duplicate-report-grouping
description: "Recommend groups of duplicate bug reports from supplied report data. Use when comparing reports for duplication; excludes changing ticket states."
---

# Duplicate Report Grouping

1. Read each report's ID, component, affected version, and reproduction steps.
   Put reports with a missing comparison field in a pending list and name the field.
   Continue with the complete reports.
2. Group complete reports only when all three comparison fields match. Matching
   error text can suggest a pair to inspect but cannot establish duplication.
   When step equivalence is uncertain, keep the reports separate and explain why.
3. Return proposed groups, their shared reproduction basis, and pending reports.
   Check that every input ID appears once in a group, as a singleton, or as pending.
   Present recommendations without changing tickets.
```

This was authored by applying the revised workflow in the same session. It demonstrates
an output shape, not that a fresh model will produce it or follow it correctly.

Walkthrough inputs: R1 = UI/v2/open-save; R2 = UI/v2/open-save;
R3 = API/v2/open-save; R4 = UI/unknown/open-save. All show identical error text.
Expected result: group R1/R2, retain R3 as singleton, mark R4 pending version.
Boundary change: confirm R4 is UI/v2/open-save; it should join R1/R2.
These outcomes are manual predictions, not downstream agent test results.

## Reproducible next comparison

Use separate fresh sessions with the same model/tools/budget and the same fictional
source packet above. One condition receives the pre-revision authoring skill; the
other receives this candidate. Request one reusable skill from each. Do not provide
the generated artifact above or the author's discussion. Snapshot the exact compared
packages; the prior version must include its references, not just a git filename.

Then give fresh runner sessions each generated package and the four report inputs.
Grade the grouping result, treatment of missing fields, complete ID coverage,
unnecessary questions, and any attempted ticket mutation. Repeat on the boundary
change. This tests both authorship and downstream use; a good-looking Markdown file
alone is insufficient. No comparison has been executed here.

Additional regression case: a user asks to package an existing guide and working
script for a different workspace, with no labeled transcripts. Expected: preserve
the guide/script, repair real path dependencies, and check relocation without
demanding a transcript or inventing extra approval gates. Keep this case separate
from claims of improved judgment.

## Mechanical checks

Passed: entrypoint frontmatter structure (required name/description and optional
when_to_use), all relative Markdown resource links in the four runtime files,
maintenance separation, and `git diff --check`. These checks inspect packaging,
not semantic quality or host routing. No executable helpers were added to the
authoring package; software tests would not establish its behavior.

The repository source and shared template were updated. Installed copies in personal
or project agent directories were not synchronized; deployment remains on demand.
