# Preserve prompt-design capabilities while simplifying wording

Recorded: 2026-10-03 (Asia/Shanghai).

## Why this restoration was needed

Ray identified that the rename and simplification had removed useful prompt-design capabilities, not merely unnecessary wording. He specifically named independent analysis learned from the prompting course, reusable versus one-off instructions, and agentic work, and asked for a full comparison and restoration. The earlier assistant interpretation that a personal wording skill should exclude these functions was too narrow.

This record supersedes the scope exclusions in the 2026-10-02 rename notes and subsequent statements that retained that narrower scope. The name remains Ray's Prompt Wording. Simplicity applies to wording and unnecessary process, not to deletion of useful decisions.

Sources inspected: the August entrypoint at commit 6de06f05a81ee7ae947c3bd3506a4c4fbbecfc77; the September entrypoint and six runtime references preserved under legacy-runtime (last pre-rename entrypoint change e9311081a01ff52c9b3ca9b5059b7b7a6789c04a); September evidence/revision notes, including the 2026-09-10 neutral evaluation change; the current package after model-selection restoration at 86ae185b1ac8a01333bb3dc4c7786d6074695c99; and Ray's current correction.

## Capability comparison and disposition

| Capability from prior versions | Before this restoration | Preserved or restored now |
|---|---|---|
| Clarify intended outcome, inputs, audience, constraints and useful result | Largely retained | Core procedure, including forming goals and open exploration |
| Create, revise, diagnose, review/grade and evaluate instructions | Narrowed mainly to wording and model advice | Restore request-specific modes and deliverables; evaluation remains on request |
| Preserve goals rather than failed methods | Retained | Keep; distinguish required outcomes, proposed methods and predicted answers |
| Independent judgment despite a user's favored conclusion | Removed | Restore hypothesis framing, contrary evidence and plausible alternatives |
| Criteria before overall judgment | Removed | Restore evidence against relevant criteria before synthesis; no obligatory scoring rubric |
| Separate requirements/preferences from predictions | Implicit at best | Explicitly distinguish a real preference from an unsupported claim |
| Preserve advocacy and one-sided exploration when intended | Open exploration retained, specific distinction lost | Restore conditional boundary; avoid forced neutrality or false balance |
| One-off task versus reusable template | Removed | Restore stable guidance, variable inputs and self-contained reuse |
| Prompt versus project instructions versus skill | Removed | Restore placement by lifetime and task breadth; recurrence alone does not require a skill |
| Tools/configuration and maintenance as separate homes | Removed | Restore enforceable controls and keep rationale/history outside runtime |
| Target context, tools, permissions and capability checks | Mostly removed | Restore; distinguish missing setup from weak wording and data from authority |
| Agent discovery, continuation, recovery, state and completion | Removed | Restore conditional execution guidance, including analysis-only versus implementation requests |
| Diagnose earliest visible divergence | Removed | Restore input/output/tool-event inspection and competing explanations |
| Repair information, priority, criterion or setup gaps differently | Removed | Restore cause-specific repair and preserve behavior already meeting the goal |
| Precise language, justified constraints and selective structure | Partly retained | Keep admission rule; restore conditional branches, dependent stages and useful examples |
| Required output fields, order, unknown/empty behavior and schemas | Mostly removed | Restore consumer-dependent requirements; schemas do not ensure factual truth |
| Sources, checks and inspectable reasons | Mostly removed | Restore observable verification without demanding hidden reasoning |
| Long-context organization and example calibration | Removed | Restore selectively; no universal placement rule or ritual repetition |
| Model and reasoning choice | Restored immediately before this update | Preserve the revised 472-word reference unchanged |
| Matched comparisons, regression cases and evidence labels | Excluded from routine work | Restore as optional requested evaluation; preserve limits on automatic execution |
| Author guidance versus target instructions | Strengthened recently | Preserve the self-contained-prompt example and keep design discussion outside artifacts |
| Corrections across the whole artifact; preserve unaffected content | Strengthened recently | Preserve and add explicit capability accounting before substantial removal |
| Skill applies its own brevity/preservation principles | Lost or weak | Explicit in opening; concise core plus conditional references |

## What was not restored as a default

The August version's mandatory typical-input runs, exhaustive public requirement maps, tagged rule layers, ban on contract headings, universal long-context positioning, blanket confirmation gates, and broad claims about self-review were already revised or rejected in later work. Their useful underlying functions are preserved through conditional checks, clear author/target separation, meaningful structure, context-aware authorization, and honest evidence labels.

No automatic target-prompt execution, reviewer launch, benchmark, or broad workflow project is required during ordinary prompt work. Explicitly requested evaluations retain a compact procedure. This respects Ray's prior objection to turning simple wording into repeated model trials.

## Package and wording

The core is 833 words and routes to seven focused references: instruction placement, independent judgment, agent execution, diagnosis/review, examples, model/effort selection, and evaluation. The restored detail is loaded when its task applies. The language uses direct actions and concrete distinctions; there are no mandatory intake fields, scoring systems, or response layouts for every request.

The frontmatter, UI metadata, README and AGENTS routing now describe the restored scope consistently. Historical files remain unchanged. The preservation map lives here, outside the installable package.

## Validation and limits

- quick_validate.py passed; all local Markdown references resolved; diff whitespace checks passed.
- An independent agent inspected the historical and candidate packages and reported no material omissions or internal conflicts. This is a static preservation review.
- Two fresh agents exercised five candidate requests. The prompts given to them contained the task data and candidate path, not the author's diagnosis or expected answers. Their actual outputs are in [the behavior record](2026-10-03-restoration-checks.md).
- The examples covered independent assessment versus advocacy, mixed instruction placement and agent completion, missing-context diagnosis, and findings-only review.
- The retained model/effort reference had already been exercised in the preceding restoration. It was not changed or retested here.
- Final saved package contents are checked across the installed version and GitHub, allowing equivalent YAML serialization.

These checks establish instruction coverage and a small sample of authored outputs. They do not prove general behavioral improvement, test automatic host selection, or evaluate the eventual vendor analysis or code repair. Neither target task was executed. No old-versus-new performance benchmark was run.
