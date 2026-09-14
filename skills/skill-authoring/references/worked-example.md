# From experience to a useful decision

Load when authoring a procedure from source material or repairing generic steps.
This example is invented to demonstrate the transformation, not an empirical run.

## Source packet

A user supplies these requirements for a vendor-comparison workflow:

- A mandatory deployment requirement must be satisfied before price is considered.
- A missing answer is unknown, not a failure and not evidence of support.
- If only a marketing page supports a capability, obtain technical documentation
  before describing that capability as confirmed.
- When an unknown could change the shortlist, request that information. Otherwise
  finish the comparison and list the limitation without blocking the whole task.

An existing answer lists features and prices and recommends the cheapest vendor.
The user rejects it because the recommended vendor cannot satisfy the mandatory
deployment requirement. The failure and correction are labels in this fictional packet.

## Weak extraction

1. Gather vendor information.
2. Analyze requirements carefully.
3. Compare options objectively.
4. Recommend the best vendor and verify the answer.

These steps describe the task but omit the criterion that changes the outcome.
Adding preconditions, provenance tags, or a "do not hallucinate" warning would not
supply that missing decision.

## Recover the choices

| Cue | Decision and reason | Boundary / check |
|---|---|---|
| A mandatory deployment requirement | Filter on documented compatibility before ranking price | A preference can affect ranking without excluding a vendor |
| Capability absent from documentation | Mark unknown, preserving the distinction from confirmed incompatibility | Ask only if resolving it could change the shortlist |
| Marketing assertion only | Treat support as unconfirmed until technical evidence is found | Retain the source and uncertainty if no stronger evidence exists |

The reusable content is the eligibility-before-ranking decision and its handling
of unknowns. The original vendor names, page-navigation order, and rejected draft's
wording are incidental. A definition of "mandatory" is useful if the user's domain
distinguishes it from a preference; facts and concepts need not be stripped out.

## Resulting procedure

1. Separate mandatory requirements from preferences using the user's stated criteria.
   If an ambiguous requirement changes eligibility, clarify that requirement.
2. For each mandatory requirement, record confirmed support, confirmed incompatibility,
   or unknown, with a source. Use technical documentation to confirm capabilities;
   a marketing claim alone remains unconfirmed.
3. Exclude confirmed incompatible options from the eligible shortlist. Keep options
   with decisive unknowns pending and seek the missing evidence. Continue evaluating
   other options; explain if a pending option could change the recommendation.
4. Rank eligible options using the user's preferences, including price. State the
   deciding tradeoff and show the evidence for mandatory compatibility. When none
   qualifies, report that result instead of recommending the cheapest incompatible option.

The check is source-backed eligibility plus a defensible comparison, not an invented
software runtime check. The decision table above is authoring scaffolding; the short
procedure is enough for this runner. Keep a contrasting example only if it helps
distinguish unknown from incompatible in actual use.

## Refactor warnings into a boundary

Suppose later edits append "Never recommend the cheapest vendor", "Never omit price",
and "Never stop for missing documentation." Recover their shared decision instead:
establish eligibility, seek decisive missing evidence while continuing independent
work, then rank eligible options. A cheap compatible vendor can win; an incompatible
one cannot satisfy a mandatory requirement. A decisive unknown may leave that option
pending without blocking comparisons supported by complete evidence.

Keep this procedure in a vendor-comparison skill if it is reused for that task class.
Keep today's vendors and requirements in the current prompt. A stable deployment
constraint needed across the project can live in project context and be supplied to
the comparison. If an importer enforces required fields, keep its schema in tooling
and give the runner the field meanings and invocation. Keep the rejected drafts in
maintenance. These placements follow use and enforcement needs, not the mere fact
that all of them were mentioned in one incident.

## Probe whether it adds value

Give a fresh runner three fictional vendor records: cheap/incompatible,
moderate/confirmed-compatible, and cheapest/undocumented. With the stated mandatory
requirement, it should recommend the confirmed-compatible option while explaining
the unresolved cheaper option. Change deployment from mandatory to preferred: the
runner should now weigh the tradeoff instead of mechanically excluding it.

Run the same cases without the skill and compare decisions and unnecessary questions.
If both versions already make the right choices, this packet has not demonstrated
incremental benefit. It may still encode a user's reusable policy, but report that
purpose honestly. For migration of an established workflow, preserving these choices
in a new workspace is the relevant comparison.
