# Fidelity ledger

Load this file only when the full ledger triggers (SKILL.md §9): the input is about
500 words or more, or the §1 domain caution applies (legal, medical, financial,
safety-critical text). For anything shorter, check the substantive rewrites against
the source directly; do not build the table.

## Procedure

1. Scan the **edited** text and list every checkable item: numbers with units,
   dates, proper nouns, defined terms, direct quotations, citations, URLs.
2. For each item, find its counterpart in the source and mark it:
   - **matched** — same value, wording may differ;
   - **matched — reformatted** — value unchanged, form changed ("$1,250 per month"
     → "$1,250 monthly");
   - **no counterpart**.
3. Every "no counterpart" is invented content: remove it from the edit, or keep it
   only with an explicit flag to the user. There is no third outcome.
4. Reverse direction, domain-caution texts only: list every checkable item in the
   *source* and confirm it still appears in the edit. A silently dropped number is
   a fidelity change too.

## Table format and filled example

Source (domain caution applies — legal):

> "The Tenant shall pay rent of $1,250 per month, due by the 5th day of each
> month. Payments received after the 5th incur a late fee of 5%, as permitted
> under California Civil Code §1671. The Landlord may terminate this lease with
> 60 days' written notice."

Edit:

> "The Tenant must pay $1,250 monthly by the 5th. Late payments incur a 5% fee,
> as California Civil Code §1671 allows. The Landlord may end this lease with
> 60 days' written notice."

Ledger:

| Item in the edit | Type | Source counterpart | Status |
|---|---|---|---|
| $1,250 monthly | number + unit | "$1,250 per month" | matched — reformatted |
| the 5th | date | "the 5th day of each month" | matched |
| 5% | percentage | "a late fee of 5%" | matched |
| California Civil Code §1671 | citation | same | matched (protected span, verbatim) |
| Tenant / Landlord | defined terms | same | matched |
| 60 days' written notice | number + term | same | matched |

Reverse check (required here, because the domain caution applies): every source
item — $1,250, the 5th, 5%, §1671, 60 days — still appears in the edit, so
nothing was silently dropped.

Counterexample: had the edit said "$1,500" or "30 days' notice," that row would
read "no counterpart" — fix it before delivery, not explain it after.

## Computed counts

When you report a word count or a cut percentage, count the words in the source
and in the edit, then compute: cut = 1 − (edit words ÷ source words). The worked
example in this folder shows the convention: "29 words, counted," "a 59% cut,
computed." If you did not count, write "shorter" instead of a number.
