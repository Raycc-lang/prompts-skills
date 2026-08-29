# Ship gate: `prompt-engineering`

Date: 2026-08-29 · Standard: `skills/skill-authoring/SKILL.md` (Gate mode)
Artifact: `skills/prompt-engineering/SKILL.md` (198 lines) + `references/evidence.md` (12 lines)
Deployment: repo == `~/.workbuddy/skills/` == `~/.agents/skills/` (three-way in sync)

Verdict: **3 pass · 1 partial · 5 fail.** One failure (#5) is behavioral; four are
convention gaps. Evidence base: 2 representative tasks executed against the
artifact in clean contexts — low-confidence, per W4.

---

## Gate checklist

| # | Item | Result | Minimal repair |
|---|---|---|---|
| 1 | Description: what it does, trigger language, handoffs; no routing rule only in body | **PASS** | — |
| 2 | Skills named in frontmatter exist, both directions | **PASS** | — |
| 3 | Every rule anchors procedure / pitfall / missing fact | **PARTIAL** | Compress the layer taxonomy; delete "stable name" |
| 4 | Scope names preconditions + ≥1 non-trigger | **PARTIAL** | Add a 2-line Preconditions block |
| 5 | Procedure ends with a runtime check | **FAIL** | Add one executable verification step |
| 6 | Adaptation guidance: invariant vs adaptable | **FAIL** | Add a 4-line Notes section |
| 7 | Heavy material in `references/`; body 45–129 lines | **FAIL** | 198 lines; split is inverted |
| 8 | Failure-derived rules carry provenance | **FAIL** | Map citations → rules; tag rule kinds |
| 9 | Test proposal exists; Task 1 executed | **FAIL** (as shipped) | Executed today; record it |

---

## Passes

**#1 Retrieval.** The description leads with verbs (create, improve, debug, grade,
evaluate), names the artifact types users name ("prompts, system instructions,
policies, and the wording of skill files"), and hands off both adjacent cases by
name. The handoff is *also* restated in the body — redundant, not harmful, since
the router-visible copy is complete on its own.

**#2 Bidirectionality.** `prompt-engineering` ↔ `skill-authoring` ✓ (SA's
description and `when_to_use` both name prompt-engineering back).
`prompt-engineering` ↔ `edit-my-writing` ✓ (EMW's `description` and `when_to_use`
both name prompt-engineering back). Both siblings exist in repo and both runtime
locations.

---

## Failures

### #5 — No runtime check (the one that matters)

The Delivery gate is a reread-and-confirm checklist. Testing is tagged `[offline]`
and explicitly pushed outside the run: "propose a small evaluation set to the
user." Observed consequence (Task 1): the agent shipped a four-case test table it
had not run and could not run, and said so only in its self-report.

The skill's own line 164 is half-right — routing genuinely cannot be tested from
inside a skill — but it over-generalizes. Content can be tested: run the rewrite on
one representative input and compare against the original.

Fair repair, narrower than the generic rule: for a prompt artifact, running it on
the model in the loop does **not** validate it for a different target model. So:

> Before delivering a Create, Improve, or Debug result, run the rewritten prompt on
> at least one representative input and report the observed difference from the
> original. If the target model is not the model in the loop — or no model call is
> available — label the delivery **unverified** and say why. Routing claims stay
> predictions.

This preserves the skill's correct instinct while satisfying the standard.

### #6 — No invariant/adaptable marking

Nothing names invariants, and there is no "abandon this skill" clause. Task 1 found
three decisions the skill left to guesswork:

- **Untrusted-input threshold** — "text the user does not control." A pasted CSV
  export is ambiguous: the user made it, but did not author its contents. No
  threshold given.
- **When testing is proportionate** — "only for important, repeated, or
  high-risk use" with no criterion.
- **Artifact language** — the skill never says which language the delivered prompt
  should be in. Resolved from host instruction, not from the skill.

Repair (4 lines): invariants = preserve intended behavior; never cut text you
cannot explain; never emit contract fields as literal headings. Adaptable = which
contract fields matter, which techniques fire, artifact language follows the
user's, whether testing is proportionate. Abandon = the request is really about
skill routing, evidence, or ship-readiness.

### #7 — Budget and the inverted split

198 lines against a 45–129 reference point. Meanwhile `references/evidence.md` is
12 lines of bare citations. Heavy material is in the body; the reference file holds
almost nothing. The two should trade places: technique catalog detail and the
folklore list are reference-loadable; what stays in the body is the mode routing,
the contract fields, and the delivery gate.

### #8 — No provenance

Zero inline provenance in the body. `evidence.md` lists seven papers but never says
which rule each supports. Nothing distinguishes platform contract, external
spec, observed run, or design judgment — so no rule can be safely revised or
deprecated later (W7, M3). Minimal version: in `evidence.md`, map each citation to
the rule name it backs and tag each rule's kind; the body keeps one pointer line
per contested rule, not inline citations.

### #9 — No test proposal; Task 1 never executed before today

Fixed by this audit. Both tasks are recorded below.

### #3 — Dead weight (partial)

Task 1's self-report, verbatim: the four-layer tag system is "the most decorative
part of the skill… the tiebreaker never fired." `Default objective` is "standard
prompt-writing sense… didn't change a decision." Two specific cuts:

- **`stable name`** (line 142) — never defined, never used again anywhere. Dead
  concept; delete the clause.
- **Rule layers** (lines 11–20) — 10 lines whose only operational payoff is one
  clause in the delivery gate. Compress to one line per tag plus the tiebreaker.

Keep `Default objective` item 5 ("when you only suspect text is inert, flag it
instead of cutting it") — that one is a real decision rule, not folklore.

### #4 — Preconditions missing (partial)

Non-triggers are strong — frontmatter `when_to_use`, plus line 82. Preconditions
are absent entirely. Task 2 exposed the one that costs the least and saves the
most: **a "my skill never triggers" report is often a file that isn't deployed
where the user thinks it is.** The test case literally had no file on disk; the
agent found this only by searching. One `ls` before diagnosing wording.

---

## Executed tasks

### Task 1 (typical) — Improve a folklore-laden prompt · **PASS with conditions**

Input: a Chinese sales-analysis prompt containing role-play ("世界级的资深数据分析专
家，20年经验"), "深呼吸", "一步一步地思考", "double-check everything", a
self-review demand, and vague intensity ("非常专业、非常详细、全面、深入").

Result: correct artifact — four-part output shape, delimited untrusted input,
per-number row/column traceability, missing-field handling, competing-explanation
guard. All four folklore items removed with reasons. Requirements mapping produced,
one row per source requirement, each marked kept/modified/dropped. No contract
field leaked into the artifact as a literal heading.

Two conditions: (a) **the test set was proposed, not run** — see #5; (b) the
requirements mapping had no rule for pseudo-requirements like "非常专业", so the
agent invented one ("Modified" + explanation). The gate's kept/modified/dropped
vocabulary doesn't cover entries that are none of the three.

### Task 2 (edge) — "my skill never loads" · **handoff fired, by judgment not rule**

The agent classified it as Routing → handed to `skill-authoring` → correct minimal
repair (frontmatter only) → correctly labeled the routing fix an untested
prediction.

But the handoff was a judgment call, and the self-report names the reason
precisely: **both skills exclude the same edit.** `prompt-engineering` says
"reviewing a skill's routing behavior… belongs to skill-authoring"; `
skill-authoring` says "wording-only edits… use prompt-engineering." A routing
failure is repaired *by a wording edit*, so it sits in the intersection of two
exclusions. The agent resolved it by weighting an explicit handoff command over a
competence argument.

Further gaps this exposed: no handoff *procedure* (invoke the sibling? tell the
user to re-ask? do a partial pass?); the bidirectional handoff check is
unsatisfiable as written for newly named skills (`edit-my-writing` cannot
enumerate every future skill that names it); and the artifact-language question
again.

**Recorded as one observed failure on the Scope surface.** Not yet three — hold off
on `references/notes.md` (W3).

---

## Also observed — in `skill-authoring`, not this skill

Two unsound spots in the standard itself, surfaced by using it. Not changed here;
flagged as follow-up.

1. **Gate item 5 is unsatisfiable for routing-only skills** — including
   `skill-authoring` itself. The escape hatch ("or it says plainly why execution
   wasn't possible") exists but is implied, not stated at the item.
2. **Gate item 2 read literally fails one-way naming.** A new skill naming
   `edit-my-writing` cannot make `edit-my-writing` name it back. The rule needs
   "the named sibling must exist; back-references are required only where the
   sibling's scope is affected."

---

## Recommended order of repair

One atomic change per revision (W4), highest behavioral value first:

1. **#5** runtime check — the only failure that changes what gets delivered.
2. **#6** adaptation notes — resolves three guesswork decisions observed in Task 1.
3. **#4** preconditions — 2 lines, catches the missing-file case.
4. **#3 + #7** compress to ~130 lines; move technique detail to `references/`.
5. **#8** provenance mapping in `evidence.md`.
6. Scope-boundary rule for the PE/SA intersection — needs a change in *both*
   skills to be coherent.

Confidence: two executed tasks is low-confidence evidence (W4). Items #1, #2, #7
are checkable by rereading and hold regardless. Items #3, #4, #5, #6 rest on a
single run each.

---

## Addendum — field corroboration from a real session (2026-08-29, 21:50)

Source: the "审阅 skill-authoring 技能的措辞与表达" session (17:00–17:51,
session file `52331a13…jsonl`, analyzed from the local transcript). The user
invoked `/prompt-engineering` explicitly; the agent reviewed skill-authoring's
wording and later applied 20 wording fixes. Process-level findings:

- **#3 layer tags — confirmed (2nd observation).** `[runner]/[property]/[technique]/[offline]`
  appear zero times in agent-authored text; no decision was tag-framed. Same
  verdict as Task 1 ("most decorative part") from an independent, non-test run.
- **Working-mode selection — new observation, same surface.** The agent never
  chose or stated a mode ("Choose one mode" never cited). The five modes did not
  fit the actual workflow (review now → apply fixes later); behavior resembled
  Grade, silently. No visible harm, but the taxonomy was ignored, not adapted.
- **#5 no runtime check — nuanced.** The procedure still contains no runtime
  check, but the agent compensated with generic competence: grep verification of
  every edit, a python consistency check, pyyaml parsing of all five
  frontmatters. The failure mode (unverified delivery) did *not* occur — but
  none of those checks came from the skill. The routing test was proposed-not-run,
  per the skill's own `[offline]` rule.
- **#6 artifact language — confirmed (2nd observation).** The report was written
  in Chinese with zero discussion; resolved by user-language convention, not the
  skill.
- **Requirements-mapping gate — confirmed (2nd observation).** The session applied
  20+ wording fixes (Improve-mode work) and produced no requirements mapping,
  despite the gate's "do not deliver until it exists." The kept/modified/dropped
  vocabulary does not fit "apply N behavior-neutral wording fixes" — the agent
  silently substituted per-item disposition notes in the report instead. Same
  shape as Task 1's pseudo-requirement gap: the gate's vocabulary doesn't cover
  real task shapes.
- **PE/SA named-handoff dilemma — did not fire.** The user's explicit
  `/prompt-engineering` invocation plus skill-authoring's then-named handoff
  settled routing silently. Honest note: the named handoff did positive work here,
  though the slash command made it unnecessary; the de-naming rationale
  (dangling references, O(n²) maintenance) is unaffected.
- **#4 preconditions, #7 budget, #8 provenance — not exercised** in this session.

Observation counts after this addendum: layer tags 2 (Content), artifact language
2 (Adaptation), requirements-mapping edge 2 (Scope/Content). All below the W3
threshold of three — no `notes.md` yet.

---

## Execution record (2026-08-29, 22:20 — Ray's decisions, repo copy, deployed)

**Declined by Ray:** the artifact-language repair ("跟随用户语言" has never failed)
and the requirements-mapping vocabulary repair (the observed case was atypical).

**Applied:**

- **#5 runtime check** — new Delivery gate bullet: run the delivered prompt on one
  typical input and say which model you ran on; for Improve/Debug run the original
  too and report what concretely changed or did not change; sanity check, not an
  evaluation — still propose the eval set for important or repeated prompts;
  label **unverified** when the target model is not in the loop.
- **#6 Notes section** — Invariant (default objective, trust boundary, delivery
  gate) / Adaptable (contract fields, technique triggers, user-specified output
  format; judgment calls decided from the task, assumption stated) / Abandon
  (routing, evidence, or ship-readiness review → say so and stop).
- **#3 dead weight** — deleted the Rule layers closing paragraph (decorative
  tiebreaker) and the undefined "stable name" clause. Definitions of the four
  tags kept: the Delivery gate's "no [runner] or [offline] rule copied into the
  artifact" clause depends on them. Nothing else added.

**Verification (W4: one representative task, executed):** re-ran Task 1 (Improve
the folklore prompt) against the revised skill, with a small real dataset so the
runtime check could execute. The gate fired and earned its place twice in one
run: (a) it caught a draft bug — sample-specific dates hard-coded into the
prompt — that would otherwise have shipped; (b) it killed an overclaim — the
draft asserted the original "misses problems", but the side-by-side run showed
both find the anomaly on an easy input. The agent reported exactly the intended
output: what concretely changed and what did not. Two confusions surfaced and
were fixed in the same revision (say which model you ran on; sanity check ≠
evaluation). Two further notes left as-is with reasons: "Default objective" has
no layer tag (the deleted tiebreaker would not have resolved it either — the
section is genuinely dual); the Notes "Abandon" line near-duplicates the skill
contract's closing paragraph (kept — rule 4 requires an explicit abandon
condition in the adaptation guidance).

Body: 203 lines. Deployed to both runtimes; three-way diff clean. Not committed
to git — Ray commits through his own flow.
