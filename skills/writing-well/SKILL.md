---
name: writing-well
description: >
  Audit and improve user-provided prose (emails, docs, posts, reports, specs)
  for clarity, concision, and impact. Use when the user asks to audit, review,
  improve, edit, or rewrite text. Not for reviewing source code.
  Apply seven checks (sentence length, clutter, unsupported modifiers, weasel
  words, jargon/acronyms, "so what", and flow), then return severity-ranked
  findings and a full rewrite suggestion.
---

# writing-well

## When to Use This Skill

Use this skill when:

- The user asks to "audit", "review", "improve", "edit", or "rewrite" text (prose such as emails, docs, posts, or reports — not source code; for code comments or docstrings, only apply it if the user explicitly asks for a writing review).
- The user shares writing and asks for feedback on clarity or impact.
- The user mentions this skill directly (`writing-well` or `writing audit`).

## Workflow

Run all 7 checks in order. For each finding:

- Quote the exact offending text.
- Explain why it is weak.
- Propose a tighter rewrite.

### Check 1: Sentence Length (max 30 words)

Flag sentences longer than 30 words.

Action: Split or tighten so each sentence carries one idea.

### Check 2: Clutter Phrases

Replace wordy phrases with simpler forms. Apply this check in the language of the text: the tables below are examples, not an exhaustive list.

| Cluttered phrase | Replace with |
|---|---|
| with the possible exception of | except |
| due to the fact that | because |
| totally lacked the ability to | could not |
| until such time as | until |
| for the purpose of | for |
| in order to | to |
| it is important to note that | delete or rephrase |
| at the end of the day | delete or rephrase |
| in terms of | rephrase |
| a large number of | many |
| in the event that | if |
| at this point in time | now |
| has the ability to | can |
| on a daily basis | daily |
| the vast majority of | most |

Spanish equivalents:

| Frase recargada | Reemplazo |
|---|---|
| debido al hecho de que | porque |
| con el fin de / a los efectos de | para |
| en el caso de que | si |
| en este momento / en el momento actual | ahora |
| tiene la capacidad de | puede |
| es importante destacar que | eliminar o reformular |
| a nivel de | reformular ("en", "de") |
| un gran número de | muchos |
| la gran mayoría de | la mayoría |
| de manera diaria | a diario |
| hasta tanto | hasta que |
| llevar a cabo | hacer |

Also flag any phrase where one word can do the same job.

### Check 3: Unsupported Adjectives/Adverbs

Flag subjective modifiers without evidence.

Examples (bracketed values are placeholders the author must fill in):

- "Sales increased significantly in Q4" -> "Unit sales increased [X%] in Q4 [year] vs Q4 [previous year]"
- "We made the application much faster" -> "We reduced server-side p90 latency from [X] ms to [Y] ms"
- "This will be extremely successful" -> "This will increase output by [X%]"

Never invent numbers. Use a real figure in the rewrite only if the author provided it; otherwise keep the placeholder and ask for the data.

Common words to flag (or their equivalents in the text's language, e.g. "significativamente", "muy", "extremadamente", "bastante"): significantly, substantially, greatly, very, extremely, considerably, remarkably, tremendously, much, quite, really, incredibly, fairly, pretty (as adverb), a lot.

Action: Ask for a number; if none is available, remove or soften the claim.

### Check 4: Weasel Words

Flag non-committal language when it avoids a commitment or a clear claim: arguably, nearly, practically, virtually, somewhat, relatively, potentially, and hedging uses of would, might, should, could.

Modal verbs are not weasel words by themselves. Leave them alone in genuine conditionals, recommendations, or polite requests ("If the deploy fails, we would roll back"; "You should rotate the key"). Flag them only when they dodge a commitment the author could make ("We should be able to ship soon" -> "We will ship on [date]" or "I don't know the date yet; I will confirm by [day]").

Action: Replace with a concrete commitment, specific number, or explicit uncertainty ("I don't know yet, and I will follow up").

### Check 5: Jargon, Acronyms, Accessibility

- Flag jargon not defined for non-experts.
- Expand acronyms on first use, e.g., "Non-Disclosure Agreement (NDA)".

Action: Define once, then use the short form.

### Check 6: "So What?" Test

For each paragraph, ask if the reader immediately sees relevance.

Action: Add implication, consequence, or numeric impact.

### Check 7: Flow and Rhythm

Check whether the text sounds natural when read aloud.

Flag:

- Repeated words/phrases in nearby sentences.
- Clunky sentences that signal unclear thinking.
- Monotonous sentence length/patterns.
- Ideas presented in an unnatural order.

Action: Reorder ideas and vary sentence rhythm to match idea complexity.

## Response Format

Use this structure:

```markdown
## Writing Audit Report

### Summary
[1-2 sentence assessment of strengths and top improvement area]

### Score: X/10
[10 − 2 per Critical − 1 per Important − 0.5 per Minor (Minor deductions capped at 2), rounded to the nearest integer, minimum 1]

### Findings

#### Critical
[Issues that severely hurt clarity or accuracy]

#### Important
[Issues that materially reduce quality]

#### Minor / Polish
[Flow and wording refinements]

### Rewrite Suggestion
[Full rewrite preserving intent and voice]
```

Default severity per check (move a finding one level up or down when its impact on the reader clearly differs):

| Severity | Default findings |
|---|---|
| Critical | Check 3 when an unsupported claim carries the main argument or decision; Check 5 jargon that blocks understanding for the intended reader; Check 6 when the main point, ask, or consequence is missing |
| Important | Check 1 (sentences over 30 words); other Check 3 modifiers; Check 4 weasel words; Check 5 unexpanded acronyms; Check 6 for secondary paragraphs |
| Minor / Polish | Check 2 (clutter); Check 7 (flow and rhythm) |

## Direct-Answer Rule

When the text being audited answers a question (e.g., a reply to "Will we ship on Friday?"), check that it opens with the answer in one of these forms, then adds context:

1. Yes.
2. No.
3. A number.
4. I don't know (and will follow up).

## Principles

- Clarity is kindness.
- Data beats adjectives.
- If it sounds wrong when read aloud, rewrite it.
- Keep subject-verb-object unless complexity demands otherwise.
- Respect the reader's time.
