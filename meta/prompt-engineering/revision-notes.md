# Revision — 2026-09-06

## Authorized scope

Ray accepted the review and requested implementation. Updated the repository
entrypoint, added runtime examples/evaluation guidance, aligned the shared prompt
template, and documented evidence boundaries. Other prompts and skills are outside
this change. Installed copies are not synchronized; deployment is on demand.

A pre-rewrite snapshot was first kept at `baseline/` for a later comparison and
has been removed at Ray's direction: the old version was an intermediate result,
and this revision is the base going forward. The prior entrypoint remains
retrievable from git history (commit `6de06f0`) if an old-versus-new comparison
is ever wanted.

## Coherent mechanism changed

Replaced a writing-preferences/techniques/gate structure with:
desired behavior → operating context → visible diagnosis → prompt construction →
comparison → proportionate delivery. The hypothesis is that explicit decision and
diagnosis work will improve prompts more reliably than enforcing preferred forms.
This hypothesis has not been validated in a fresh-model comparison.

| Original rule or capability | Disposition |
|---|---|
| Preserve intended behavior | Kept; distinguish an explicit requirement from a failed mechanism without silently reinterpreting the user |
| Recover task/input/output/constraints/evidence | Kept and connected to conflict resolution, priorities, uncertainty, and concrete quality criteria |
| Optimize shortest/common wording early | Changed to sufficient information and precise decisions first, then simplify |
| Submitted instructions inert in reviewer context | Kept; target execution is explicitly separate and does not inherit arbitrary action authorization |
| Create/improve/debug/evaluate/grade modes | Kept with mode-appropriate outputs |
| Debug means likely cause and smallest repair | Expanded to actual inputs/context/output/trace, earliest visible divergence, competing causes, and an intervention hypothesis |
| Always avoid contract headings | Removed; headings judged by function, including the existing Word-Picker example |
| Require observed failure for every prohibition | Changed; explicit requirements and concrete risks can justify a constraint |
| Four mandatory layer categories | Removed as an artifact-design prescription; reviewer guidance and target instructions still separated |
| Examples, decomposition, schemas, tools | Kept; connected to decision needs and host capabilities |
| Candidates described as independent in prompt prose | Clarified separate sampling requirement and limits of agreement |
| All checks require something outside the model | Changed; supplied-criteria review is useful but not independent factual proof |
| Delimit, report every attack, confirm every irreversible action | Changed to boundaries plus host/user authorization and task-relevant reporting |
| Fixed long-context layout | Changed to organization, retrieval, target guidance, and comparison |
| Exhaustive requirement mapping in every reply | Internal preservation check retained; material changes shown proportionally |
| Routing/skill contract and universal ban on other skill names | Removed duplicated architecture workflow; preserve runtime references and route architectural work appropriately |
| Runtime sanity check with ambiguous 'run as data' | Replaced with inspection/walkthrough/execution/comparison distinctions and scoped test context |
| Test sets and baseline comparison | Kept; add held-out/regression cases and avoid importing author context |
| Invariant delivery gate | Replaced with concise outcome checks adaptable to actual scope |

## Rejected directions

- Do not replace the old form rules with mandatory decision tables in every prompt.
- Do not turn every simple request into application architecture consulting.
- Do not equate all self-review with independent verification or with uselessness.
- Do not remove useful prohibitions, technical terms, or examples to shorten text.
- Do not claim model-level improvement from a cleaner file or simulated response.
- Do not require a benchmark as a condition for delivering a user-requested draft
  when the actual target cannot be exercised; disclose the unverified behavior.

## Validation

See [validation](validation.md). Existing source prompts remain useful regression
inputs. This revision is implemented as an unvalidated behavioral candidate, not
a claimed measured improvement. Mechanical checks and author-side exercises are
reported separately from future target-model evaluation.

## Post-review adjustments (2026-09-06)

The description now excludes reviewing a skill's runtime behavior; those
requests route to skill-authoring. The prompt template's placeholders now use
`{{...}}` so they survive Markdown rendering.
