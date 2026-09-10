# Frozen pilot protocol — 2026-09-08

Question: does the current skill-authoring package improve conversion of the current
Job_hunting working tree into portable private skills, relative to the same model
without an authoring skill? This is one matched authoring pair, not an estimate of
general skill effectiveness. The unit of treatment is the authored package.

Model: gpt-6-astra, low reasoning, Codex CLI 0.153.4. Each author has a fresh home,
memory disabled, the same tools and sanitized read-only snapshot, and no access to
Windows, the real home, the other run, evaluation fixtures, or conversation history.
Bubblewrap restricts the filesystem; Codex workspace-write additionally restricts
tool execution. System authoring skills are disabled in both arms. The common
search skill is present in both. Only treatment gets the current skill-authoring
runtime folder and a one-sentence explicit invocation. Network-backed job searches
are outside scope; no search API credentials are provided. Author wall cap: 1000 s;
common prompt requests completion in 15 minutes. Save JSONL, final, code, elapsed
time, available usage, exact command, manifests, and isolation probes.

Architecture is an outcome: either one or multiple packages may win. No points for
following skill-authoring's document structure. No feedback/revision after authorship
until the initial evaluation is locked. Preserve incomplete artifacts and failures.

Primary evaluation: six fresh downstream sessions per authored package, same model
and bounded execution settings. Runners see relocated packages, their documented
legitimate runtime data, and only their case's input. They cannot access author
sessions, source repository, treatment skill, grading answers, or other cases.

1. Applied mirror/new opening: preserve applied exclusion without a company ban;
   no unsupported claim of live verification; unknown schedule handled correctly.
2. Policy boundaries: equivalent education passes; hard bachelor fails; generic
   APAC does not override specific exclusion; role-specific China exception can
   pass; equally specific contradictory eligibility stays unresolved.
3. Source recovery: empty sections are incomplete extraction, not absence of an
   education requirement; inaccessible originals stay unverified, not fit-rejected;
   distinguish supported fallback from unavailable/unauthorized paid execution.
4. Cache/state: fresh unchanged rejection reusable; expired/legacy/policy-changed
   rejection reopens; applied exclusion wins; checks do not mutate input state.
5. Opportunity development: no vacancy prerequisite; bounded action tied to actual
   candidate evidence; no invented acceptance/hiring/adoption or unauthorized action;
   separate opportunity state from vacancy/application state.
6. Relocation/update: run supplied helpers from another cwd; preserve existing
   registry/ledger data; record a confirmed application exactly once and update
   generated views if applicable; only designated disposable state changes.

Record each criterion as pass/fail/unclear with observed evidence. Count explicit
material errors separately from output omissions and setup limitations. Inspect
artifact completeness and run preserved tests; this is separate from agent results.
Use anonymous package labels for downstream prompts. Grading follows the source
policy, not the author's self-evaluation. The orchestrator knows condition labels;
report this limitation rather than claiming fully blind evaluation. If possible use
an additional fresh label-blind reviewer on case outputs and frozen criteria.

No statistical inference from the many within-package cases. Report case-level
outcomes, intervention uptake, complexity, cost, and repair requirements. Distinguish
preservation from correction of pre-existing bugs. Report fixture/harness mistakes
and rerun both arms when a shared fixture changes. Do not repair one candidate before
scoring. Private snapshots and raw logs stay under the private WSL study directory;
only protocol, harness, and non-sensitive findings belong in this repository.

## Execution amendments

- Both authors completed on Astra/low. Initial downstream attempts were all quota
  interrupted, retained, and excluded from scoring. After user continuation, the
  next Astra pair was interrupted when the user requested a cheaper test model.
- The user then specifically selected GPT-5.6 Luna. All scored downstream cases
  use gpt-5.6-luna/low with identical fixtures and packages. The intervening Mini
  attempts are retained but excluded. This measures transfer to Luna, not Astra
  downstream performance. No results from different runner models are pooled.
- Downstream pairs run two at a time. A quota error stops further pairs.
