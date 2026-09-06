# Evidence base

Empirical findings behind this skill's rules, from three studies. Each was measured
on particular models and benchmarks; treat as strong priors, not universal laws.
This file is part of the skill's **maintenance record** (`meta/skill-authoring/`),
not the skill itself: it is used when creating or revising the skill, is never
installed to runtime skill directories, and the SKILL.md body carries no citation
tags — the rule→evidence map below is the crosswalk. When a finding's limitation
changes where its derived rule is safe to apply, the rule in SKILL.md carries that
limitation — it does not stay confined to this file.

Numbers here were extracted from the papers' HTML full texts on the access date;
claims that also appear in the abstracts were re-checked against the abstract
pages the same day. Re-verify against the PDF tables before formal citation.

## 1. Demystifying Agent Skills (arXiv:2608.14036v1, accessed 2026-08-29)

Controlled trials (8,135 normalized runs) on Terminal-Bench 2.0 (89 tasks),
Terminal-Bench-Pro (200 tasks), and SkillsBench (86 tasks), with Codex +
GPT-5.x and Gemini CLI + Gemini-3.x; 238 open-coded labels aggregated at κ=0.952
(paper §4 agreement table).

**F1 — Procedural anchoring dominates the measured mechanism labels.**
`procedural_anchor` accounts for 65.7% of skill mechanism labels; `knowledge_injection` only
4.5%. Skill beats raw experience (61.9% vs 59.1%) and Workflow Memory (55.9%),
a +6.06-point gain over Workflow Memory (95% CI [+0.76, +11.36]). Skills cut
execution-layer failures sharply: environment setup 5.3% → 0.2%, output format
7.4% → 3.2%, service lifecycle 2.7% → 0.8%.
These frequencies do not establish that removing facts or examples improves skills.
Section 5.1 also reports short-plan and test-first baselines below distilled skills;
generic procedural form alone does not reproduce the measured result.

**F2 — Distillation needs outcome labels.**
Removing success/failure labels from the same trajectories degrades the distilled
skill (e.g., Gemini on Terminal-Bench 2.0 at 3-success/2-failure mix: 0.75 with
labels vs 0.40 without). Failure traces are useful raw material, but only when
their outcomes are known.

**F3 — Noise in the artifact causes drift.**
Workflow Memory fails not from missing information but from retaining exploration,
failed branches, and verbose debugging: timeout/budget exhaustion hits 10.6% of
Workflow Memory runs vs 4.4% for skills (raw: 1.7%). Compression is a proposed
explanation for the advantage, not an isolated ablation of artifact length.

**F4 — Three failure classes.**
Skills fail through (a) **brittle assumptions** — a premise no longer holds and
steps are executed mechanically; (b) **context mismatch** — retrieved but applied
in the wrong situation; (c) **adaptation shortfall** — invoked superficially, not
translated into fitting action. Invoking the ground-truth skill raises a new
failure surface (invocation/applicability failures: 78/528 with skills vs 19/528
raw; guidance misapplied or ignored 10.0% vs 0.8%).

Historical Diagnose-mode subdivisions: **D1** = brittle assumption,
**D2** = context mismatch, **D3** = adaptation shortfall — F4's three failure
classes, named separately because each maps to a distinct repair.

Patterns named in the paper's main text, useful as Diagnose anchors:
skill_guided_success, environment_infrastructure_failure,
output_format_schema_mismatch, background_service_lifecycle_failure,
algorithmic_logic_error, static_verification_without_runtime,
skill_guidance_misapplied_or_ignored, timeout_budget_exhaustion. The full
12-pattern taxonomy (appendix Table 11) was not included in the accessed text.

**F5 — Retrieval is an independent bottleneck.**
As the pool grows 5 → 100 skills, usage precision collapses (29.6% → 3.3%) while
downstream success barely moves (36.4% → 39.3%): agents see the right skill but
don't commit to it alone. Similar distractors hurt identification most (offline
top-1 precision at k=5: 97.7% random pool vs 70.5% similar pool). Conclusion:
correct retrieval is neither sufficient nor necessary; the description must
discriminate, and the body must still work once loaded.

**F6 — What skills can't fix.**
Algorithmic logic errors (8.3% → 7.4%) and static-verification-only runs
(~12% across all arms) are barely affected. Requiring a runtime check was our
design inference, not a tested intervention from this finding. The current rule
requires task-appropriate observable verification; it does not impose a software
execution ritual on judgment or reference tasks.

**F7 — Distilled skills outperform transferred workflow memory in this setting (RQ3).**
Skills built from Codex trajectories and evaluated under Gemini CLI beat the
Gemini raw baseline (56%) in all six trajectory mixtures: 62–84%. Per mixture
(WfM / Skill): 0s5f 60/62, 1s4f 58/76, 2s3f 60/76, 3s2f 56/76, 4s1f 70/74,
5s0f 54/84 — skill beats transferred workflow memory every time, by +2 to +30
(smallest lifts 0s5f +2 and 4s1f +4). Values are Figure 4's printed bar labels,
coordinate-extracted from the PDF text layer; no appendix table reports RQ3.
One transfer direction only (Codex → Gemini CLI, one target model). Some transferred
workflow-memory conditions also beat baseline. This does not isolate standardized
format as the causal component or prove universal portability.

## 2. WikiSkill (arXiv:2608.27454v1, accessed 2026-08-29)

Skill evolution with a persistent knowledge base, on LiveMath, SealQA,
SpreadSheetBench, OfficeQA, ALFWorld; models Qwen-3.5-4B/9B, Qwen-3.6-27B,
Gemma-4-31B, Gemini-3.5-Flash.

**W1 — Separate raw experience, knowledge, and executable skill.**
Raw trajectories stay immutable; distilled patterns accumulate in a wiki layer;
skills are compiled from the wiki. Skills may roll back; the knowledge never does.
Mixing all three into one file makes skills bloated and un-maintainable.

**W2 — Persistent accumulation is the load-bearing component.**
Ablation: skill proposer without the wiki averages 48.7; with the wiki 63.7
(LiveMath 51.3 → 72.6). One-shot summaries of experience don't substitute for
cumulative evidence.

**W3 — Keep an audit trail.**
Every proposal records its diff, validation score, and accept/reject outcome
(`skill-impact.md`), so failed modifications are not re-proposed.

**W4 — Atomic, validated updates.**
Each proposal targets one skill, creating it or applying a patch; accept only if
validation exceeds the previous best (initialized from the empty-skill baseline).
This does not establish that a revision must change exactly one textual rule.
Many accepted updates arrive mid-to-late in a skill's life (on SealQA: 33% mid,
28% late), so skills are maintained, not finished.

**W5 — Portability is conditional.**
Skills distilled by a stronger model often beat self-evolution (Qwen-9B on
SpreadSheet: self 33.6 vs Qwen-27B's skills 50.5). But low-level workarounds
tuned to a weak model can actively hurt a strong one (Gemini-Flash on SpreadSheet:
50.5 → 18.1 with the 4B model's skills). General procedure transfers; model-
specific patches must be labeled as such.

**W6 — Observed skill lengths vary.**
Evolved skill bodies average about 45–129 lines across models. Section 5.2 also
reports variation across benchmarks (SpreadSheet averages 142.5 lines). This is
a descriptive statistic, not evidence of an optimal line budget or a short-vs-long
intervention. Retire the former heading and derived writing target.

**W7 — Record provenance.**
Each skill maps back to the evidence patterns that produced it, so rules can be
re-examined when models or tasks change.

Known limits: skills were injected wholesale (retrieval not evaluated); the
accept-only-if-better gate drops neutral-but-preparatory changes; the wiki has
no pruning mechanism; the validation sets are small (10–40 samples), so
accept/reject decisions themselves carry noise.

## 3. Memp: Agent Procedural Memory (arXiv:2508.06433, accessed 2026-08-29)

Procedural memory on TravelPlanner and ALFWorld with GPT-4o, Claude-3.5-Sonnet,
Qwen2.5-72B.

**M1 — Two granularities beat either alone.**
The combined condition ("proceduralization") includes full retrieved trajectories
alongside high-level scripts: GPT-4o on ALFWorld test goes 42.1% → 77.9% with fewer
steps. This supports retaining useful concrete examples alongside abstraction;
it does not establish that every skill should use abstract phases by default.

**M2 — Retrieval must be semantic.**
Keyword/feature-based matching (AveFact) and query-similarity retrieval both beat
random sampling consistently across models.

**M3 — Fix failing memories; don't just append.**
Update strategies compared: blind append < keep-only-successes < adjust-in-place
(merge the failure trace into the offending memory and rewrite it). Adjustment
wins: +0.7 over the runner-up and −14 steps in the final task batch.

**M4 — More retrieved memory is not better.**
Performance rises, plateaus, then falls as retrieved items grow — long context
plus inaccurate memories interferes. Cap what gets loaded.

**M5 — Procedural knowledge transfers downward.**
Memory built by GPT-4o improves Qwen2.5-14B (+5% completion on TravelPlanner,
−1.6 steps); a curated procedure library can be worth more than model scale.

**M6 — Memory is a lifecycle.**
Build, retrieval, and update are first-class operations; content is continuously
corrected and deprecated, never append-only.

Known limits: relies on benchmark-provided success signals; only two benchmarks;
no published memory schema.

## Field observations

Incidents from real runs of this skill. Not benchmark findings — single cases,
recorded per the maintenance loop so their derived rules can be re-examined.

**FO1 — Prohibition piles, inline provenance, portability tags (2026-09-02,
evox Cowork, kimi-k3, Author mode).** A drafted resume-workflow skill carried a
five-item "Invariants (never adapt these)" section of prohibitions against
failures the target model had never shown, inline "(Source: 2026-08-24 audit —
…)" annotations, and a *(portable)* tag on every step — each defensible as a
literal reading of rules 4/7/10 and the then-current skeleton. User verdict:
telling the model not to 乱写 when it wasn't going to made it start reasoning
about what counts as 乱写; provenance and portability serve the maintainer, not
the runner. Rewriting as eight positive procedural steps, with provenance moved
to a maintenance note, was accepted. Derived: rule 11 (instruct positively),
rule 4 rewording, provenance placement in rule 7, portability placement in
rule 10, skeleton and template cleanup.

## Historical rule → evidence map (before 2026-09-06 rewrite)

Retained to explain earlier decisions and FO1; these numbered rules no longer
identify the current entrypoint. See the current crosswalk below.

| SKILL.md rule | Evidence |
|---|---|
| 1. Frontmatter is the router | F5 |
| 2. Procedure over facts | F1 |
| 3. Scope is content | D1, D2 (F4) |
| 4. License to adapt | D3 (F4), FO1 |
| 5. End with a runtime check | F6 |
| 6. One mechanism per rule | F1 |
| 7. Provenance | W7, M3, FO1 |
| 8. Stay retrievable | F5 |
| 9. Compress | F3, M4, W6 |
| 10. Mark portability | M5, W5, F7, FO1 |
| 11. Instruct positively | FO1 |
| Maintenance loop | M6 |
| Author mode step 2 (ground in a real run) | W2 |
| Distill mode | F2, F3, M1 |
| Diagnose classes | D1–D3 (F4), F5 |
| Revise discipline | W3, W4, M3, M4 |
| Ship gate runtime-execution item | F6 |

## Review follow-up — 2026-09-06

Rechecked the relevant HTML sections in this review:
[Demystifying Agent Skills](https://arxiv.org/html/2608.14036v1),
[WikiSkill](https://arxiv.org/html/2608.27454v1), and
[Memp](https://arxiv.org/html/2508.06433).
Corrections above distinguish observations from authoring prescriptions. Other
historical quantitative claims retain the original verification caveat.

**FO2 — Useful consolidation with limited attribution (2026-09-06).**
Reviewed task `01a075ae-b798-7061-8923-e071dd7d8a53`, titled
"Expand reusable private agent skill", its installed package, source policies,
maintenance record, and synthetic drafting output recorded in the transcript. The user reports a strong model;
the task summary does not establish a specific model identity.

Observed: the package preserves substantive decision criteria and existing runtime
knowledge, introduces scoped modes, and bundles relative resources and executable
helpers. The source policies already contain many of the useful decisions. The task
reports executed relocation and negative-path helper tests; the visible command output
also shows sample preflight success. The referenced sample files were not present
at their recorded paths when this review attempted to read them; the transcript
supports what was written and checked, but that fixture cannot now be rerun as-is.
Its sample draft was produced in the author's
session, with source context available. The maintenance record explicitly leaves real
office rendering and routing provisional.

Interpretation: this is counter-evidence to a blanket claim that the old authoring
skill always produces generic results. It supports consolidation as a distinct goal.
It does not isolate the contribution of model capability, source quality, or the
authoring skill, and does not compare downstream judgment with a baseline. Do not
relabel successful migration as a failure merely because it lacks that comparison.
Private source content remains in its original workspace; only this finding is retained.

## Current rule-group crosswalk

| Current instruction | Basis and status |
|---|---|
| Establish intended difference; test against appropriate baseline | User-approved review diagnosis; F1 paired methodology and W4 motivate comparison. Specific workflow is design judgment, not a measured treatment. |
| Preserve knowledge and decisions during consolidation | FO2 and current user request; W1 separation does not require excluding runtime knowledge. |
| Recover cue, decision, reason, boundary, check | Design hypothesis from the 2026-09-06 review, supported by F1/F4's problem framing; not directly tested by the papers. |
| Keep outcome labels; avoid incidental chronology | F2/F3; retain useful recovery choices as design judgment. |
| Keep useful concepts, examples, scripts, assets | M1, FO2, and runner needs; format selection is design judgment. |
| Proportional guards; contextual recovery and verification | FO1, F4/F6, explicit requirements; guard policy is not a universal empirical law. |
| Compare fresh-context behavior; distinguish mechanical checks | W4, FO2, user-approved diagnosis; the evaluation protocol is proposed, not yet validated for this authoring skill. |
| Diagnose generic/no-benefit as well as harmful behavior | Review hypothesis; acknowledge works-as-requested using FO2 counter-evidence. |
| Coherent revisions; correct or retire rules | W3/W4, M3/M6; permits coordinated repair rather than literal one-rule changes. |
| Grouped provenance outside install unit; protect private source content | Repository AGENTS.md, W1/W3/W7, FO1; grouping and privacy placement are maintenance design choices. |
| Routing and conditional dependencies | Host-dependent packaging contract, F5, FO2's missing-dependency repair; names are not globally forbidden. |

The implementation and validation limits are in [revision notes](revision-notes.md).
