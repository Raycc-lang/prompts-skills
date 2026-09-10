# Skill-authoring paired pilot: Job_hunting

## Finding

The direct audit found **no downstream improvement on the predefined checks** in
this experiment. Both authored packages passed all six held-out scenarios and all
37 targeted criteria when used by fresh GPT-5.6 Luna sessions. The treatment made
a substantially smaller installable package, but the baseline already produced a
working, portable result with useful local verification.

This supports a narrow conclusion: **skill-authoring was not necessary for a good
result on this rich-source consolidation task.** It does not establish that the
skill is ineffective on other tasks or that every aspect of either result is correct.

## What was compared

- Source: a frozen copy of the actual Job_hunting working tree, including current
  modified/untracked material, not just Git HEAD. Original source remained unchanged.
- Authors: Codex CLI 0.153.4, `gpt-6-astra`, low reasoning, one fresh run per condition.
- Baseline P: shared search skill, no skill-authoring or competing authoring skills.
- Treatment Q: same environment plus the frozen skill-authoring runtime package
  and explicit invocation. Its trace confirms reading SKILL.md and all three references.
- Both got the same task, source, dated career-reference snapshot, resources,
  ordinary decision authority, and time ceiling. One versus two skills was left open.
- Neither got this conversation, our architecture recommendation, or held-out cases.
- Both independently delivered `ray-job-search` and `searching-the-web` packages.
- Runners: twelve fresh `gpt-5.6-luna`/low sessions, six per frozen package. No
  author context, authoring skill, or original repository was visible to them.

The effect tested is explicit use of skill-authoring for **consolidation/migration**,
followed by transfer to Luna. Automatic authoring-skill retrieval and Astra downstream
performance were not tested. The baseline retained the common web-search skill;
it was not an entirely skill-free agent.

## Isolation and verification

Bubblewrap gave each process its own filesystem view, private home/Codex directory,
PID namespace, work directory, and temporary directory. Only the required system
runtime, that run's files, and explicitly mounted inputs were exposed. The real WSL
home, Windows mounts, other runs, and grading materials were absent. Authors saw a
read-only source snapshot; runners saw read-only installed packages and disposable
state. Codex additionally used workspace-write execution restrictions.

Memory injection/generation was disabled. System authoring skills were disabled
in both conditions. Preflight model catalogs showed only searching-the-web in the
baseline and searching-the-web plus skill-authoring in the treatment. OS probes
confirmed the expected path visibility. Neither author nor any scored runner had
access to the other condition. This was enforced by filesystem boundaries, not
only an instruction to avoid reading other files.

The snapshot replaced embedded search credentials with configuration placeholders.
No live job search, outreach, submission, global installation, or original-state
mutation occurred. Model-service access used the existing authorized account.
Original source and frozen deliverable hashes were verified unchanged. All twelve
installed runner copies also remained unchanged.

Temporary per-run authentication copies were removed after execution. The original
account authentication file was left untouched.

## Observed results

| Held-out scenario | Without skill-authoring | With skill-authoring |
|---|---:|---:|
| Applied variant, distinct opening, missing schedule, old live posting | 6/6 | 6/6 |
| Education and location exceptions/conflict; independent judgments | 7/7 | 7/7 |
| Hollow/blocked/empty original sources and bounded recovery | 5/5 | 5/5 |
| Cached rejection expiry/policy changes and protected application state | 7/7 | 7/7 |
| Opportunity development without a vacancy or invented outcomes | 5/5 | 5/5 |
| Relocation, confirmed update, duplicate refusal, generated views | 7/7 | 7/7 |
| **Targeted criteria total** | **37/37** | **37/37** |

These are criterion counts within one authored artifact per arm, not 37 independent
experiments or a general success-rate estimate. Fixtures used captured/synthetic
source records so changes in live search results could not decide the winner.

The label-blind Luna review initially returned 37/37 for the baseline and 36/37 for
the treatment. Its sole failure confused an allowed lead-ledger append with the
applied-registry check. The registry was byte-identical, all prior ledger rows were
preserved, and the displayed dispositions were correct. The direct audit therefore
adjudicated that criterion as pass. Both the unedited review and correction are
retained. The same reviewer also mistook header-inclusive line counts for inconsistent
row counts; this was not scored as a failure. The final table is an evidence-adjudicated
score, not an assertion that the blind reviewer agreed on every first-pass judgment.

The helper cases exercised actual Python programs. Independent filesystem checks
confirmed that cache checks and opportunity sessions preserved registry/ledger bytes;
the final update added exactly one application, retained prior records, regenerated
the expected count, and rejected a repeated request and tracking variant. Both
packages' own offline validation programs were independently rerun successfully in
relocated, isolated environments. The original source's nine regression tests also passed.

Both authors independently found and repaired the same source liveness issue:
a failed board fetch could otherwise be reported as a missing posting. That finding
cannot be credited uniquely to the treatment. The baseline also supplied an additional
offline-tested Exa adapter. The treatment instead made a cleaner separation between
runtime resources, optional history, and maintenance/testing files.

## Effort and package size

| Measure | Baseline P | Treatment Q |
|---|---:|---:|
| Author elapsed seconds | 387.80 | 449.87 |
| Author completed shell commands | 14 | 21 |
| Author input tokens, summed across calls | 715,144 | 673,825 |
| Author cached input tokens | 616,960 | 603,392 |
| Author output tokens | 10,328 | 11,905 |
| Installable files | 42 | 25 |
| Installable bytes | 521,146 | 186,931 |
| Job-search entrypoint words | 850 | 986 |
| Six runner sessions, summed seconds | 711.30 | 690.35 |
| Runner completed shell commands | 39 | 36 |
| Runner input tokens, summed across calls | 1,283,820 | 1,264,365 |
| Runner cached input tokens | 1,048,832 | 969,984 |
| Runner output tokens | 19,066 | 18,269 |

The treatment's installation is 64.1% smaller, largely because optional historical
reports and author-side tests stay outside it. Both preserve the complete decision
prompt byte-for-byte. The treatment is not simply a shorter instruction: its main
entrypoint is longer, and its total deliverable including history/maintenance is
approximately the same size as the baseline's.

The author took 16.0% longer in the treatment run. Downstream elapsed time differed
by only about 3% in aggregate, with wins in different individual cases. Shared
service timing, cache state, and single-run variation prevent treating these figures
as reliable speed/cost effects. Token totals are cumulative CLI-reported usage, not
unique prompt size or dollar charges. Smaller disk size did not produce a comparable
reduction in measured runner input tokens.

## Limits and execution deviations

- Only one authoring run per condition. There is no estimate of authoring variance,
  confidence interval, or demonstrated causal explanation for every artifact difference.
- Rich source policy, scripts, and facts already existed. This does not test discovering
  a new procedure from ambiguous traces, repairing a brittle skill, or choosing to
  leave an already-effective skill unchanged.
- The six cases test important decisions, but not live provider reliability, search
  recall/yield, job-ranking usefulness, long-term maintenance, or every report-field rule.
- The direct evaluator knew the conditions. A separate Luna review used per-case
  randomized A/B labels and the fixed criteria; its final record is retained privately.
- Initial downstream attempts all hit an account quota and were excluded. Resumed
  Astra and intervening Mini attempts were stopped following the user's model-cost
  steering. All scored runs use Luna; results from different models were not pooled.
- Before downstream execution, the common setup was corrected to initialize a new
  workspace while preserving separately supplied state copies. Before either scored
  cache run, distinct synthetic company identities removed an unintended mirror-rule
  collision. Both changes were applied equally and recorded; original manifests remain.
- The minimal environment lacked the `awk` alternative. One baseline runner recovered
  using other hash checks. That incident is not a defect in the authored package.
- Passing targeted criteria does not mean perfect report compliance. For example,
  the baseline paraphrased the mandatory application-disposition block in later
  cases; the treatment retained its exact form more consistently. Such ancillary
  observations are separate from the frozen 37-criterion score.

## Practical decision

Prefer the treatment package's separation of runtime resources from optional history
as the starting artifact, with the baseline available for comparison and its optional
adapter as a separately reviewable addition. Both candidates remain private, frozen,
and uninstalled; live integration still needs a bounded check before routine use.

For skill-authoring itself, retain it provisionally as an authoring/consolidation aid,
but do not claim that it materially improves task accuracy from this study. A mandatory
large-quality-gain claim is unsupported here. Its clearest observed contribution is
consistent packaging discipline; a strong baseline already preserved the substantive
workflow and produced useful checks. Another revision based only on this pair would
be premature. A different task class is more informative than polishing this successful
source packet until it creates a difference.

## Reproduction and private artifacts

Private WSL study directory: `/home/<user>/skill-authoring-study-20260908/`.

- `runs/candidate-p/work/deliverable/`: baseline packages and author checks.
- `runs/candidate-q/work/deliverable/`: treatment packages, optional history, maintenance.
- `runs/*-luna1/`: exact runner prompts, isolated copies, answers, state and JSONL traces.
- `evaluation/`: frozen criteria, fixtures, amendments, manifests, blind label map.
- `runs/blind-review-luna/`: anonymized grading input/output and trace.
- `artifact-audit.json`, `downstream-audit.json`: independent integrity/state evidence.

This repository retains only the non-sensitive protocol, orchestration code, and
findings. Private source snapshots, candidate data, and raw model outputs remain in
WSL. See [protocol](protocol.md), [harness](harness.py), [cases](cases.py),
[runner](evaluate.py), [filesystem audit](audit_results.py), and
[blind review](blind_review.py). Authoring is frozen; rerunning tests should use new
run names rather than overwriting prior observations.
