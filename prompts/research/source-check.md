# Source Check

**Use when:** you have a claim and want to know how well it's actually supported.
**Inputs:** the claim, plus any sources you already have.
**Output:** a verdict separating what's established from what's inferred.

---

## Prompt

```
Assess how well the following claim is supported.

Claim: {{claim}}

Do this:
1. State what would have to be true for the claim to hold.
2. Search for primary sources. Prefer originals over reporting about them.
3. Separate: established fact / reasonable inference / contested / unsupported.
4. Give the strongest case against the claim, even if you think it's correct.
5. Name what evidence would settle it, if it isn't settled.

Cite each source you rely on. Say plainly when you couldn't verify something
rather than filling the gap.
```

---

## Notes

- Step 4 is the load-bearing one; without it the answer tends to confirm the claim.
- For fast-moving topics, add the current date so it knows what "recent" means.
