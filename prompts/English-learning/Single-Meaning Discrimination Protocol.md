# Single-Meaning Discrimination Protocol

Produce a self-contained worksheet that trains one meaning of one word.

The worksheet let the learner draw the line around `TARGET MEANING` — what falls inside it, what falls outside, and when a rival word is the better choice. 

Explanation exists only to make those decisions possible; the practice items test whether the learner can make them unaided.

## Learner and language

The learner is an advanced English learner whose first language is Mandarin.

- Keep non-target vocabulary and syntax at CEFR B2 or below so `WORD` remains the main difficulty.
- Use natural, contemporary English from general, professional, or accessible technical contexts.
- Do not add unrelated difficulty.
- Give every scored item one clearly best answer, decided by a visible clue.
- If a required contrast can not be made naturally, state the limitation instead of inventing an unnatural example.

## Input

- `WORD`: required
- `SOURCE SENTENCE`: optional
- `PART OF SPEECH`: optional

Treat `WORD` as a lexeme, not as an exact written form. Inflect `WORD` and any compared words when grammar requires it. Keep the selected part of speech unchanged in all examples and exercises; do not switch to a derived word with another part of speech.

### Multi-word items

When `WORD` is a phrasal verb or a fixed expression:

- Treat the whole item as the unit of meaning everywhere this protocol says `WORD`. Analyze meanings of the item, not of its component words.
- Wherever this protocol asks for a part of speech, use the grammatical function of the whole item — verb, adverbial, predicative phrase, and so on.
- For a phrasal verb, inflect the verb head, and treat separated and contiguous orders (looked the word up / looked up the word) as the same item.
- For an expression, change only the parts that normally vary, such as tense or an open slot (get on my/her nerves). Keep the fixed parts fixed.
- Do not switch to a derived compound with another function, such as take off → takeoff.
- Wherever a rule says not to use `WORD` in an item, do not use the whole item; its component words may still appear in their ordinary, unrelated senses.

### Select the target

1. Select the target part of speech in this order:
   - the part of speech used in `SOURCE SENTENCE`;
   - `PART OF SPEECH`, if supplied and not determined by the source sentence;
   - the part of speech of the most common current general-English use of `WORD`.
2. Select `TARGET MEANING` in this order:
   - the meaning used in `SOURCE SENTENCE`;
   - the most common current general-English meaning within the target part of speech.
3. If `SOURCE SENTENCE` and `PART OF SPEECH` conflict, follow the source sentence and note the conflict.
4. If `SOURCE SENTENCE` has more than one plausible reading, list the readings briefly, select the most likely one, and continue with it.
5. If `WORD` is effectively monosemous within the target part of speech, say so. Do not invent another meaning.

## 1. Sense map

List the main current meanings of `WORD`, one line each: part of speech, short English gloss, and a frequency tag (`high-frequency`, `common`, or `less common`).

Merge small variations that share the same core meaning.

Include a meaning only when it is:

- a sense that general learner's dictionaries typically list as its own entry;
- an established professional or technical sense that a general reader of that field needs; or
- required by `SOURCE SENTENCE`.

Exclude archaic, historical, dialectal, and rare senses. Exclude jargon limited to one narrow subfield unless `SOURCE SENTENCE` requires it; in that case, include it and mark it `domain-specific`.

Do not claim that a named dictionary lists a sense unless you have checked that dictionary.

Clearly mark the selected meaning as `TARGET MEANING` and state the target part of speech.

Skip this section entirely when the learner is studying a further meaning of a word whose sense map was already produced in an earlier round. Name `TARGET MEANING` and continue from Section 2.

## 2. Examples

Write six new sentences that use `WORD` in `TARGET MEANING`. Order them from prototypical to subtle. Put a natural Chinese translation directly below each sentence. Translate the meaning, not the word order.

Across the six sentences:

- include two or three useful collocations or grammatical frames;
- vary inflection and syntactic environment where natural;
- keep the same part of speech and meaning;
- vary situation or domain only when it shows a real boundary, register, or domain restriction;
- do not force variation that creates unnatural English.

## 3. Definition and boundary

This section decides what counts as `TARGET MEANING` and what does not.

Provide:

1. **Definition:** a concise, learner-friendly English definition.
2. **Boundary:** what the meaning includes and excludes.
3. **Confusable:** one or more similar or easily confused words that help clarify the boundary, with the key differences;
4. **Patterns:** common grammatical patterns and collocations for `TARGET MEANING`.
5. **Other sense:** one example of `WORD` in a different meaning within the same part of speech, if one exists.
6. **Chinese approximation:** the closest natural Chinese equivalent when it is useful, noting any important mismatch.

## 4. Practice

Use only new sentences. Do not repeat or lightly adapt `SOURCE SENTENCE`, an example, a verification situation, or another practice item.

Label the items `V1–V3`, `J1–J5`, and `S1–S2`. Do not show translations, hints, or answers in this section; place the answers in Section 5. 


### Boundary verification

Include this test when `TARGET MEANING` earns it: when its extension differs from the nearest Chinese equivalents, or when its boundary has a non-obvious edge. When the Chinese equivalent covers the meaning essentially exactly and the boundary is plain, omit `V1–V3` and say so in one line.

When included, write three short situations that test the boundary directly.

- Do not directly use `WORD` or the confusable words named in Section 3.
- Do not build the situations around `WORD`'s typical collocates — the nouns and contexts that usually accompany `WORD` — so the learner must judge from the meaning, not from a familiar pairing.
- Include a clear positive case, a clear negative case, and a genuine edge case, in mixed order — not in that order.
- Make the edge case decidable from the stated boundary, not genuinely ambiguous. Put it on whichever side of the boundary the learner is more likely to get wrong; it may fall inside or outside `TARGET MEANING`.

Ask:

> Does each situation fall within `TARGET MEANING` — would `WORD`, in this meaning, truthfully describe it, even if another word would be the more idiomatic choice?

This tests membership in the meaning, not idiomatic word choice; whether `WORD` is the natural word for a context is tested later in Judgment and Substitution.

### Judgment

Write five sentences containing `WORD` in the target part of speech. Across the set, include:

- at least one use of `WORD` in `TARGET MEANING`;
- at least one use of `WORD` in a different meaning within the same part of speech;
- at least one unnatural use blocked by grammar or a nonstandard collocation, not merely an uncommon collocation;
- one natural near-boundary case with an explicit clue that makes the answer decisive. The near-boundary case counts as the target-meaning or different-meaning item above, whichever it is — it is not a separate slot.

Use the remaining items for any of the first three types. Do not reveal the distribution.

Ask:

> Does `WORD` carry `TARGET MEANING` here? Choose `Yes`, `No`, or `Unnatural` and give the decisive clue. If the use is unnatural, state what blocks it.

### Substitution

Write two sentences, each containing a word a learner could wrongly use in place of `WORD`. Neither sentence contains `WORD`. Use the confusable named in Section 3 for at least one item; the other may use a different word when that yields a sharper contrast.

Ask the learner to replace that word with the grammatically corresponding form of `WORD` and choose one label:

- `N — Not natural`: the replacement uses an unavailable grammatical frame or an unacceptable contemporary collocation. Do not choose `N` only because another expression is more frequent.
- `M — Meaning mismatch`: the replacement is grammatical but conflicts with the stated situation or describes a different situation.
- `S — Shift`: the replacement is natural and still accurate, but changes what the sentence asserts or implies.
- `E — Equivalent here`: the replacement is natural and the context removes the usual difference.

Give the two items different answer labels, with at least one labeled `N` or `M`. Make each answer decidable from a visible collocate, grammatical frame, register marker, or stated fact.

Ask:

> Which label applies, and what visible part of the sentence decides it?

If two natural, clearly decidable contrasts cannot be built, state the limitation instead of fabricating an item.

## 5. Answer key

Place the answer key after a clear divider so the learner can stop before reading it.

Include:

- `V1–V3`, when present: yes or no, and the stated boundary condition that decides each answer;
- `J1–J5`: `Yes`, `No`, or `Unnatural`; the actual meaning or `no coherent reading`; the decisive clue; and why `TARGET MEANING` fits or does not fit;
- `S1–S2`: `N`, `M`, `S`, or `E`; the substituted word; the visible deciding element; the specific change for `S`; or why the context removes the difference for `E`.

## End

End with `TARGET MEANING` in one sentence.

Name the next meaning of `WORD` to study when the sense map holds a meaning not yet studied. If `WORD` is effectively monosemous, or every meaning has been covered, say nothing further.