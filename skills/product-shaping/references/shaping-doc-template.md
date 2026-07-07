# Shaping Doc Template

Use this structure. Keep it short — a good shaping doc is 1–3 pages. Fat marker fidelity: boundaries and mechanisms, not pixel or field-level detail.

```markdown
# [Product/Feature name] — Shaping Doc

**Date:** · **Shaped with:** [user] · **Appetite:** [e.g. 2 weeks, one dev]

## Problem
The situation that triggers the need, who has it, and the evidence.
One paragraph. If we can't state this crisply, we're not done shaping.

## Solution shape
The core mechanism in plain language: what the user does, what the
system does back. Include the fat-marker sketch of the flow (text or
reference the prototype.html). NOT a spec — a builder should have room
to improvise on details.

## Key decisions
For each decision that shaped the solution:
- **[Decision]** — what we chose, the alternative we rejected, and why.

## Rabbit holes
Known risky areas a builder could sink time into. For each: the risk
and the patch (a simplifying assumption or fallback we pre-approved).

## No-gos
What this explicitly is NOT. Scope cuts we made on purpose, so nobody
"helpfully" adds them back.

## Deferred unknowns
Open questions we consciously left to the build phase, and any guidance
on how to resolve them (e.g. "pick the conservative option and log it").

## Success signals
How we'd know this worked — behavioral signals over vanity metrics.
2–4 items.

## Artifacts
Links/paths: prototype.html, research notes, references analyzed.
```

Notes:
- "Key decisions" and "Deferred unknowns" come straight from the session's unknowns log — don't reconstruct them from memory.
- Write rejected alternatives down. They're the cheapest insurance against re-litigating decisions later.
