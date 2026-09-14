```markdown
---
name: report-comparison
description: Compare vendor reports and recommend options using mandatory deployment requirements, stated preferences, evidence, and price. Use when assessing vendor eligibility, ranking alternatives, or resolving gaps in comparison reports.
---

# Report Comparison

Produce an evidence-backed recommendation that separates deployment eligibility from ranking and makes consequential uncertainty visible.

## Compare requirements and evidence

1. Identify the user's mandatory deployment requirements and ranking preferences. A mandatory requirement determines eligibility; a preference affects ranking. If an ambiguous requirement could change eligibility, ask for clarification while continuing work that does not depend on the answer.

2. Assess each vendor against every mandatory requirement using the supplied reports and available supporting sources. Record the evidence and distinguish:
   - **Supported:** evidence establishes compatibility.
   - **Incompatible:** evidence establishes a conflict with the requirement.
   - **Unknown:** evidence is missing, insufficient, or conflicting.

   Missing evidence establishes neither support nor incompatibility. Apply the same evidence discipline to claims about preferences, without making those preferences additional eligibility requirements.

3. Assign each vendor an overall status:
   - **Eligible:** every mandatory requirement is supported.
   - **Ineligible:** at least one mandatory requirement is demonstrably incompatible.
   - **Pending:** no mandatory requirement is demonstrably incompatible, but at least one remains unknown.

   Preserve unknowns in the underlying assessment even when a confirmed incompatibility already determines overall status.

## Resolve uncertainty and rank options

4. Investigate unknowns that could change eligibility, the shortlist, or the recommendation. Use available reports, accessible sources, and supported research tools. If necessary evidence is unavailable, identify the exact unresolved question and its consequence. When vendor-contact tools are unavailable, explain that the question remains unresolved; do not claim vendor confirmation.

   Continue independent comparison work while an answer is missing. Defer only conclusions that depend on that answer. For unknowns that would not change the decision, disclose the limitation without delaying completion.

5. Rank eligible vendors using the user's preferences and relevant price comparisons. Price may decide among eligible options, including selecting the cheapest. Prices and other independent facts can be collected alongside deployment research; establish eligibility before using them to select a vendor.

   Keep pending vendors visible as unresolved alternatives. If one could change the recommendation, state that the recommendation is provisional and explain what evidence would change it. If no vendor is confirmed eligible, report that result and distinguish pending options from ineligible ones.

## Deliver and check

6. Present the recommendation, vendor statuses, decisive evidence, relevant tradeoffs, and remaining uncertainty. Use paragraphs, lists, tables, or another clear format suited to the reader.

   Only when the user explicitly requests importer output, produce JSON following the existing importer schema, with the required fields `vendor`, `status`, and `reason`. Use `reason` to explain the decisive requirement and any consequential uncertainty. Rely on the importer's existing schema validation; do not add a separate validation mechanism or impose JSON on ordinary reports.

7. Before delivering, check that:
   - Each eligible vendor has evidence supporting every mandatory requirement.
   - Documented incompatibility excludes a vendor regardless of price.
   - Missing evidence remains unknown and does not halt independent work.
   - Preferences influence ranking without becoming unstated eligibility gates.
   - The recommendation and its certainty match the available evidence.
```

The revision replaces blanket prohibitions with eligibility, evidence, and ranking decisions. An author walkthrough covers both reported failures and the contrasting cases: the cheapest eligible vendor can win, a deployment preference need not exclude a vendor, and missing documentation leaves that vendor pending while other comparison work continues. No downstream agent runs or comparative tests were performed; this is a draft only.
