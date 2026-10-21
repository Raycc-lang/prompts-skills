# Core teaching loop — 2026-10-21

## Basis and changes

Ray reported seeing little benefit beyond bounded questioning and accepted making
the teaching procedure more operational. Imported the existing installed package
into this repository, preserving its substantive guidance and evidence boundaries.

The entrypoint now prioritizes target and demonstrated understanding, the next useful
teaching move, a check during agreed practice, and adaptation/closure. It explicitly
checks whether confusion comes from the assistant's interpretation or teaching before
inferring a learner deficit. Detailed prior guidance remains in
references/teaching-guidance.md; research qualifications remain in
references/evidence-and-boundaries.md. Practice is still optional for explanation-only
requests. No new claim about the empirical effectiveness of the workflow is made.

Preservation review: retained load management, direct facts versus purposeful discovery,
bounded questioning, examples and near-misses, procedural contrasts, ICAP caveats,
feedback and support fading, independent versus cued performance, delayed retrieval,
transfer matched to the goal, confusion repair, and conversational continuity.

## Forward check

A fresh subagent loaded only the revised skill and this learner request:

> I understand that "responsible" is an adjective and that "the engineer is
> responsible" needs "is". What I still don't understand is why "the engineer
> responsible for the servers" can omit "is", while "the engineer who responsible
> for the servers" cannot. Explain with contrasting examples. I only want an explanation now.

Criteria: address the structural difference, build on the stated understanding,
provide explained contrasts, and respect the explanation-only request.

Observed: the response distinguished an adjective phrase modifying a noun from a
relative clause needing a verb; compared valid phrase, valid clause, and incomplete
clause in complete sentences; explained removing "who is" together; and distinguished
a noun phrase from a complete statement. It ended without a practice question.

Opening of the actual output:

> The key difference is whether you are describing a noun with an adjective phrase
> or building a clause with its own subject and verb.

This exercises explanation behavior in one fresh session. It does not establish
better retention, adaptive behavior over a lesson, or an improvement over the prior
version. No model override was supplied; exact serving model/settings were not exposed.

## Mechanical checks

Package validation, local links, icons, UI metadata, and whitespace passed. The
preservation check is author inspection, separate from the fresh-agent response.
