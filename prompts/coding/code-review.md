# Code Review

**Use when:** you want a focused review of a diff or file, not a general "make it better."
**Inputs:** the diff or file contents.
**Output:** ordered findings, each with severity, location, and a concrete fix.

---

## Prompt

```
Review the code below. Report findings in this order: correctness bugs, security
issues, then design problems. Skip style unless it causes one of those.

For each finding give:
- severity (blocker / should-fix / consider)
- the exact location
- what breaks, with the input or sequence that triggers it
- the smallest change that fixes it

If you find nothing in a category, say so in one line rather than padding.
State any assumption you had to make about code you can't see.

{{code or diff}}
```

---

## Notes

- The ordering constraint is what stops the review drifting into naming nits.
- Add "assume this is called concurrently" or similar context when it applies —
  most missed bugs come from context the reviewer didn't have.
