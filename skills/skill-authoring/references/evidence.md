# Evidence base

Empirical findings behind this skill's rules, from three studies. Each was measured
on particular models and benchmarks; treat as strong priors, not universal laws.
Rule IDs in SKILL.md cite these entries. When a finding's limitation changes where
its derived rule is safe to apply, the rule in SKILL.md carries that limitation —
it does not stay confined to this file.

Numbers here were extracted from the papers' HTML full texts on the access date;
claims that also appear in the abstracts were re-checked against the abstract
pages the same day. Re-verify against the PDF tables before formal citation.

## 1. Demystifying Agent Skills (arXiv:2608.14036v1, accessed 2026-08-29)

Controlled trials (8,135 normalized runs) on Terminal-Bench 2.0 (89 tasks),
Terminal-Bench-Pro (200 tasks), and SkillsBench (86 tasks), with Codex +
GPT-5.x and Gemini CLI + Gemini-3.x; 238 open-coded labels aggregated at κ=0.952
(paper §4 agreement table).

**F1 — Mechanism: skills stabilize action, they don't inject facts.**
`procedural_anchor` explains 65.7% of helpful cases; `knowledge_injection` only
4.5%. Skill beats raw experience (61.9% vs 59.1%) and Workflow Memory (55.9%),
a +6.06-point gain over Workflow Memory (95% CI [+0.76, +11.36]). Skills cut
execution-layer failures sharply: environment setup 5.3% → 0.2%, output format
7.4% → 3.2%, service lifecycle 2.7% → 0.8%.

**F2 — Distillation needs outcome labels.**
Removing success/failure labels from the same trajectories degrades the distilled
skill (e.g., Gemini on Terminal-Bench 2.0 at 3-success/2-failure mix: 0.75 with
labels vs 0.40 without). Failure traces are useful raw material, but only when
their outcomes are known.

**F3 — Noise in the artifact causes drift.**
Workflow Memory fails not from missing information but from retaining exploration,
failed branches, and verbose debugging: timeout/budget exhaustion hits 10.6% of
Workflow Memory runs vs 4.4% for skills (raw: 1.7%). Compression is what makes
the skill format win.

**F4 — Three failure classes.**
Skills fail through (a) **brittle assumptions** — a premise no longer holds and
steps are executed mechanically; (b) **context mismatch** — retrieved but applied
in the wrong situation; (c) **adaptation shortfall** — invoked superficially, not
translated into fitting action. Invoking the ground-truth skill raises a new
failure surface (invocation/applicability failures: 78/528 with skills vs 19/528
raw; guidance misapplied or ignored 10.0% vs 0.8%).

Diagnose-mode subdivisions cited as D1–D3 in SKILL.md: **D1** = brittle assumption,
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
(~12% across all arms) are barely affected. A skill should end in a runtime check
because rereading one's own output is not verification.

**F7 — Distilled skills transfer across frameworks; raw traces barely do (RQ3).**
Skills built from Codex trajectories and evaluated under Gemini CLI beat the
Gemini raw baseline (56%) in all six trajectory mixtures: 62–84%. Per mixture
(WfM / Skill): 0s5f 60/62, 1s4f 58/76, 2s3f 60/76, 3s2f 56/76, 4s1f 70/74,
5s0f 54/84 — skill beats transferred workflow memory every time, by +2 to +30
(smallest lifts 0s5f +2 and 4s1f +4). Values are Figure 4's printed bar labels,
coordinate-extracted from the PDF text layer; no appendix table reports RQ3.
One transfer direction only (Codex → Gemini CLI, one target model).

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
One atomic change per skill per revision; accept only if validation improves.
Many accepted updates arrive mid-to-late in a skill's life (on SealQA: 33% mid,
28% late), so skills are maintained, not finished.

**W5 — Portability is conditional.**
Skills distilled by a stronger model often beat self-evolution (Qwen-9B on
SpreadSheet: self 33.6 vs Qwen-27B's skills 50.5). But low-level workarounds
tuned to a weak model can actively hurt a strong one (Gemini-Flash on SpreadSheet:
50.5 → 18.1 with the 4B model's skills). General procedure transfers; model-
specific patches must be labeled as such.

**W6 — Short beats long.**
Evolved skill bodies average 45–129 lines across models; they are executable
procedure, not encyclopedias.

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
Best construction ("proceduralization") combines step-by-step instructions with
script-like abstractions: GPT-4o on ALFWorld test goes 42.1% → 77.9% with fewer
steps. Scripts generalize to new tasks; concrete steps help near-duplicate tasks.

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

## Rule → evidence map

| SKILL.md rule | Evidence |
|---|---|
| 1. Frontmatter is the router | F5 |
| 2. Procedure over facts | F1 |
| 3. Scope is content | D1, D2 (F4) |
| 4. License to adapt | D3 (F4) |
| 5. End with a runtime check | F6 |
| 6. One mechanism per rule | F1 |
| 7. Provenance | W7, M3 |
| 8. Stay retrievable | F5 |
| 9. Compress | F3, M4, W6 |
| 10. Mark portability | M5, W5, F7 |
| Maintenance loop | M6 |
| Author mode step 2 (ground in a real run) | W2 |
| Distill mode | F2, F3, M1 |
| Diagnose classes | D1–D3 (F4), F5 |
| Revise discipline | W3, W4, M3, M4 |
| Ship gate runtime-execution item | F6 |
